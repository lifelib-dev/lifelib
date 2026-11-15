"""In-force tests for IUL_US_SEC: the splice, future business, counts, regeneration.

``IUL_US_SEC`` is ``IUL_US_S`` taught to run in force at a valuation date
(USLIB-SEC-PLAN.md, milestone M6).  It runs on two clocks: ``t`` counts months from the
valuation date, the same month for every model point, and ``duration_mth(t)`` counts the
months the policy has been in force, ``duration_mth_init() + t``.  A model point may be a
policy already in force at the valuation date, in any month of its policy year, one issued
at it, or one to be issued after it, as in ``basiclife/BasicTerm_SE``.  A policy in force
opens with the state its past has left it, per policy: its account value and its loan,
which are ``IUL_US_S``'s own columns, and six more, the fixed account and the loan
collateral apart from the loan, the face in force, the premiums paid to date, the no-lapse
guarantee's accumulator and the MEC latch; and its live index segments, each with its
balance, the deductions and draws charged to it, its index level at creation and the cap
declared then, in a companion of the model point table, ``inforce_segments_sec.csv``.

``IUL_US_S`` ships no point in force: its five points are new business, issued at its own
``t = 0``, where the two clocks coincide, and ``test_model_conventions.py`` asserts the
model is S there cell by cell (T1), which carries every golden of
``test_indexed_ul_us.py`` over, the worked example's engine cells and the anchor's months
among them.  The conventions also hold the SEC family's other rules: every frame opens at
``t = 0``, ``pols_if`` is the ``BEF_DECR`` count, ``BEF_DECR`` is ``BEF_NB`` plus the
month's new business, new business enters once, and nothing happens before issue.  This
module holds the rest of the plan's tests (its §5.2) and the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d`` and the segments it holds live there, continues S's projection from
  ``d`` on, in every cell of S's, the four reports among them, the fixed account, the
  collateral and the account value at every timing, each segment's balance, deductions and
  draws, its credit, the loan, the face, the two premium accumulators and the counts.  The
  months straddle the product's events: a segment's creation and its maturity, the first
  anniversaries, the surrender charge's last month, the lapse shock year, the no-lapse
  guarantee failing, passing again and expiring, with its lapse shock on an exhausted
  account, the 7-pay test's seventh year and the MEC latch it leaves, the guideline cap on
  a target premium, a loan whose collateral is credited apart from it, charges ceasing in
  cover, a face withdrawn to nothing, a segment closing on a rounding about zero, and S
  point 5's fixed account and then its account value running below zero, the exhausted
  states ``IUL_US_S`` carries by design.  Fourteen variants of S's points, in a copy of
  S's table and each with input rows of its own, add every class and sex, both death
  benefit options, the single and the target premium, a premium mode of each kind, a
  second surrender charge schedule and none, issue ages 50 and 65, loans from the sixth
  year, withdrawals from the issue month and a split allocation; the twin of each variant
  issued at the valuation date is its S point in every cell, as a row issued there is.
  A second fixture, on References of its own, binds the bounds S ships idle, the index
  cap and the dynamic lapse multiplier's floor, under the guaranteed basis and the
  adjusted-beginning credit base; a formula override of the index path binds the index
  floor and the multiplier's cap; splices of their own move the segment term off its 12
  months and fail the 7-pay test first in its seventh policy year; and on a variant's twin
  ``seg_count`` and ``seg_share`` read a rounding about zero by S's tests of 0.
* T3, future new business: a point issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before issue and no rate or table read there.
* D11's R1, R1a and R2, and D3 and D5's chains: on the splice's grid no cell is called at a
  negative month, none evaluated on the books reads a month before them, and none reads
  beyond ``t + 1``, the segment's creation balance followed to the sweep it reads; on the
  committed points no recursion runs backward over the frame, the policy clock is a closed
  form and no label accessor is read; and every chain of the model runs one cell a month
  from a cold start, as far as the contract's longest cover, the guarantee's expiry read
  after a lapsed guarantee bounded apart.
* T4, the count algebra: the count rolls forward through new business and decrements,
  ``result_pols`` is S's report with the new business beside it, and a count 2.5 times the
  table's, with every assumption that ships at zero switched on, scales every counted cell
  and moves no per-policy value.
* T5, validation: each malformed in-force row, and each malformed row of the segment
  ladder, is refused as the table is read, naming its point or its line, by one rule; each
  assumption table is refused, naming its file and the column, if a key is blank, text or
  fractional, with the lines it is on, or if the keys repeat or leave a gap, and so is one
  whose rates, factors or charges hold a value that is blank, text or infinite, or outside
  its range, while the bounds of each range are read; a text value no decode knows raises
  ``IUL_US_S``'s message, and a key no join finds names the point; the future horizon is a
  Reference that bounds future business; a point issued at or past the age the projection
  ends at, one at or past the end of the projection, one withdrawing less than its fee and
  one holding other than a ladder row for each live segment are refused by ``proj_len()``,
  each rule on its Reference, and read at it, just past it and with it moved, and two
  neighbouring rules broken together are refused by the first; a reader of the ladder asks
  ``proj_len()`` first; every state S reaches, restated in force, is accepted by ``Data``
  and ``proj_len()``, the exhausted accounts and a face of nothing among them, under the
  shipped References and each splice's; an extract with every amount carried to the cent
  is read and holds its checks; each flag reads the same in every spelling ``Data``
  accepts; and the edges of the interface are accepted, the tables' keys written as floats
  among them.
* T6, regeneration: the committed ``model_point_table_sec.csv`` and
  ``inforce_segments_sec.csv`` are what the generator makes of ``IUL_US_S`` and its table as
  they stand, and each derived and future row continues its S point from its month on.
* Then the two clocks on the shipped points, the values outside cover, the survivors the
  end of the projection carries, each opening column moving its chain, the index path on
  the valuation clock and the credits that stay S's, the cap a segment keeps from its
  creation and the fixed account's rate, each read at the valuation clock's month, the MEC
  latch, expense inflation, each check failing on a residual that is not a number and
  deciding as S's where its sides are small, a lapse rate past 1, which makes the checks
  raise, the margin identity once a loan exceeds the cash value, the worked example
  through this model's engine, the mortality cap and a NaN that reaches it, the corridor,
  the mortality and the COI tables read at their ends, the docstrings, the shared input
  tables and every Reference held to S's, those that ship equal to another set apart, what
  the default grid reaches, the block, an in-force extract and the runner.
* Stage EC, what compiling changed, held in modelx: the total claims and each kind are
  ``IUL_US_S``'s bit for bit, a total of negative zeros included, and so are the
  compensated sums of the segments; the account value a point in force opens with is its
  parts summed compensated, on parts where a plain fold differs; a participation rate past
  1 is applied inside the cap, as in S; the padding of every
  array ``Data`` pads is NaN and no reader reads it; the COI scales are numbered by key on
  a file out of key order; what ``Data`` cannot number or join is refused by name; a point
  the contract does not issue is refused by ``proj_len()``; the runner refuses to build
  from a copy without the repository, and sums the block as ``groupby`` does; the
  benchmark's block repeats the ladder with its points; the sample's
  recursion limit and the spec's sizes are what their comments derive; and the segment
  cells take a slot and no projection cell calls the engine.
* C2, the fingerprint: every committed point computes what the model computed when Phase 1
  ended, frozen at the end of this module before Phase 2 changed anything (§5.4).
* The compiled model (Phase 2), in the ``cython`` job: it computes what modelx computes on
  the splice grid, on the second fixture's and the own splices' References, at the
  contract's extremes, where the cap on mortality binds and a NaN meets a bound, on labels
  that are not text and on keys written as floats; it refuses what modelx refuses, and
  what only its caches bound; a point without a charge reads its schedule as modelx does;
  it opens an account value from its parts as modelx does, bit for bit where a plain fold
  differs; its deepest call runs on a 1 MiB stack and on the main thread; past a lapse rate
  of 1 its checks fail rather than raise; it clears no cache when a Reference is set; and
  the runner prints it as it prints modelx.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``, 0 for
the twins of S's points, ``-k`` for one issued ``k`` months on.

**Roundings about zero.**  A segment, the pool of live segments or the fixed account can
close a month on a rounding about zero, a balance of the order of 1e-14 of either sign,
where a draw or a deduction took exactly what it held.  Off the valuation date each such
state is reached through other arithmetic than S's: the creation balance of a segment
carried in is its balance, deductions and draws summed, which is S's sweep only to
rounding, and each segment's return is a ratio of two levels on the valuation-clock path,
which is S's ratio only to its last bit.  So the comparisons hold every value to 1e-9
relative with no absolute floor (``ATOL``), but for a value both models give below
``FLOOR``, 1e-9, per policy, which is held to that floor, a count-weighted value to the
floor times the count in force, and for ``seg_count`` and ``seg_share``, which read such a
value by ``IUL_US_S``'s own tests of zero, in a month where a live segment or the pool is a
nonzero rounding below the floor in either model (:func:`_rounding_map`).  A count is never
floored.

**The core grid and the full one** (USLIB-SEC-PLAN.md K6).  An IUL projection runs up to 912
months on the grid, and T2 and T3 over every case would take this module far past three
minutes in every run.  By default they run a core, chosen by the lines of the model each row
runs, so that between them they reach every line, every opening-state column, every kind of
valuation month and every premium pattern and mode the full grid reaches, which
``test_the_core_grid_reaches_every_branch`` asserts, each bound by the raw value it bounds
and each side of every ``min`` and ``max`` by the values it compares, and which holds,
besides, the row on which each fault the build's and M13's sweeps recorded was first caught.
The splice's three comparisons are parametrized by S point at class scope (``_held``), so
that pytest runs every case of one S point together and ``_swept`` sweeps each S point once
a run, not once for each test that compares one of its rows.  The core does not make the
module short: its default run took 912 seconds under load at M13, the longest of
the product modules, where it took 936 to 955 at M6 (USLIB-SEC-PLAN.md K6, weighed at M13),
and 1,045 to 1,078 at M19 without the compiled tests, at a peak of 4.36 GB.
The other cases, the rules test's scan of their rows, the second fixture's other rows, the
every-state test's months between the windows' edges and its run under the main splice's
References, the depth test's cold calls but the deepest and its ascending sweeps at the
contract's longest cover, the splice at a segment term of 24 months, the References set
apart on S's twins, the index path's override, the flag spellings, the block and the
runner's test on the committed table carry the ``sec_full`` marker and are skipped, with the
reason shown, unless ``USLIB_SEC_FULL=1`` is set.  Each was moved only where every fault the
sweeps recorded keeps a catcher in the default run.  They are never dropped: one leg of the
CI matrix sets it, and ``USLIB_SEC_FULL=1 python -m pytest -m sec_full
tests/test_indexed_ul_us_sec.py`` runs them alone.  Memory is the other cost: a projected
point holds tens of megabytes of cached values and their dependency graph, so a row read
once is released as soon as it has been read (``_release``), the splice's rows are held one
at a time, and so are the splice's S points: the generator builds a splice's rows one S
point at a time, and each comparison sweeps the one S point it needs (``_swept``).  Each
splice's two models are fixtures of the class that holds every test reading them, so they
are closed before the committed model and S are first read, and the tests that read models
of their own run next, before those are first read, so that none of the models they read
sits in memory beside them (USLIB-SEC-PLAN.md §7.7, *Record — M9*, *Memory*).

Every test keeps five rules.  Each model is read under a name of its own and closed:
``test_indexed_ul_us.py`` reads S under its default name, and reading a model under a name
in use renames the open one.  Every Reference a test sets, ``Data``'s included, is set on a
model just read, before anything is computed: a compiled model never clears a cache.  No
test writes inside the library tree: every changed input goes through
``sec_support.temp_inputs`` into a temporary directory, because a CSV added beside the
models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``us_registry.point_keys`` and the ItemSpaces from
``us_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor Phase 2's positions can
point a test at the wrong row.  The one exception is a table ``Data`` refuses, which has
no keys to give: it is read through the base ``Projection``'s default point.  And a timing
or a kind is passed through ``_code``, which gives the model's Reference of that name where
the model defines one and the string otherwise, and every cell-by-cell comparison goes
through ``_twin``: Phase 2 changes the call syntax only (C1), each in one place.
"""
import ast
import builtins
import collections
import contextlib
import dataclasses
import gc
import inspect
import io
import itertools
import json
import math
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import warnings

import modelx as mx
import numpy as np
import pandas as pd
import pytest

from sec_support import (
    GENERATED_COLUMNS, SEC_SPECS, TWIN_EXEMPT_DEFAULT, build_sec_table, check_generated,
    codes, compiled_case, compiled_mismatches, exact_here, fingerprint_mismatches,
    frame_mismatches, run_compiled, sweep, temp_inputs, twin_mismatches)
from us_registry import model_path, point_keys, projection

SEC, TWIN = "IUL_US_SEC", "IUL_US_S"
TABLE, LADDER = "model_point_table_sec.csv", "inforce_segments_sec.csv"
SPEC = SEC_SPECS[SEC]

# S's five points, all M45 NT with $250,000 of face on the IUL10 schedule, the GPT, and the
# guarantee's minimum premium of $20.80 per $1,000 a year: 1, the anchor, $10,000 a year,
# annual, Option A, its fixed account swept whole into the index; 2, the same on Option B;
# 3, the same with nothing allocated to the index; 4, the same paying monthly; and 5, $6,000
# a year, withdrawing $200 a month from policy year 2 and borrowing $6,000 a year from
# policy year 21, whose guarantee fails for good at policy month 49 and whose fixed account
# and then account value run below 0.  Every one is new business, issued at S's t = 0.
NEW_BUSINESS = (1, 2, 3, 4, 5)
IN_FORCE = ()

# Fourteen more S points, in the splice's copy of S's table and never in the committed
# one.  Each changes S's columns, never a formula, to reach what S's five cannot, and
# between them they carry every class and both sexes:
#
# 6, S's point 1 paying $1,000 a year, M PElite: underfunded, its guarantee holding only in
#   policy months 0 and 1, its fixed account, the whole account value, below 0 from month
#   27, and the guarantee's expiry at 240 shocking a policy with no cash value;
# 7, S's point 4 paying $1,500 a year monthly, M PPlus: never under the guarantee, its
#   account value below 0 from month 76, a monthly payer exhausted;
# 8, S's point 1 paying $25,000 a year, M Pref: over the 7-pay limit from its first month,
#   which IUL_US_S flags in policy years 1 to 7 alone and this model latches, and its
#   corridor binding from month 60;
# 9, S's point 1 on a target premium of $30,000 a year, M PTob: the guideline cap binds on
#   each anniversary from month 36, and the 7-pay test fails in years 1 to 4;
# 10, S's point 2 on a single premium of $120,000, above its guideline single premium, M
#   Tob, withdrawing $300 a month: the premium capped at $95,000, Option B with
#   withdrawals, its account below 0 from month 388;
# 11, S's point 2 on a single premium of $50,000, below its guideline single premium,
#   with no surrender charge and half the fixed account swept into the index: the cap's
#   other side, has_surr_charge False, so the lapse shock year 0 that its guard reads, and
#   a split allocation, whose fixed account closes on a rounding about zero under the
#   splice's References in S's months 22, 23 and 590, and a segment's credit in 592;
# 12, S's point 5 borrowing from policy year 6, F Juv, on IUL07, a second schedule of
#   $30.00 per $1,000 run off over 7 years: the collateral credited at 2% against a loan at
#   3%, the loan above the cash value from month 98, the schedule's last charge at 82 and
#   its lapse shock in policy year 8;
# 13, S's point 1 issued at age 50, monthly: a guarantee of 15 years, its expiry at 180,
#   another COI cell and attained age;
# 14, S's point 5 issued at age 65 paying $4,000 a year: a guarantee of 5 years, failing at
#   month 16, its expiry shock in policy year 6, and the account below 0 from month 62;
# 15, S's point 4 paying $1,500 a year monthly: a segment closing on a rounding about zero
#   at month 15 and the pool at 16, its account below 0 from 16;
# 16, S's point 4 paying $1,800 a year monthly: segments closing on roundings about zero at
#   months 187 to 189 under the splice's References, its account below 0 from 188;
# 17, S's point 4 paying $36,000 a year monthly, M NT: the 7-pay test passing at month 6,
#   on the limit exactly, and failing in month 7, the valuation month of a row restated
#   there, which opens with no latch;
# 18, S's point 1 withdrawing $450 a month from policy year 2: the withdrawals cut its
#   Option A face to nothing at month 567, the cut taking what the face has left, and the
#   policy stays in force with a face of 0;
# 19, S's point 1 withdrawing $450 a month from policy year 1: a withdrawal in the issue
#   month, whose cut is taken from the face at issue, on a row issued later (T3) the one
#   base at t_entry() reached only under a condition its issue month must meet.
#
# Each variant is (the S point it changes, the columns it changes); the policy_id keeps
# the generated ids apart.
VARIANTS = {
    6: (1, {"policy_id": "IUL-900006", "premium_pp_ann": 1000.0, "rate_class": "PElite"}),
    7: (4, {"policy_id": "IUL-900007", "premium_pp_ann": 1500.0, "rate_class": "PPlus"}),
    8: (1, {"policy_id": "IUL-900008", "premium_pp_ann": 25000.0, "rate_class": "Pref"}),
    9: (1, {"policy_id": "IUL-900009", "premium_type": "TARGET", "premium_pp_ann": 30000.0,
            "rate_class": "PTob"}),
    10: (2, {"policy_id": "IUL-900010", "premium_type": "SINGLE",
             "premium_pp_ann": 120000.0, "rate_class": "Tob", "wd_pp": 300.0}),
    11: (2, {"policy_id": "IUL-900011", "premium_type": "SINGLE", "premium_pp_ann": 50000.0,
             "has_surr_charge": False, "index_alloc_rate": 0.5}),
    12: (5, {"policy_id": "IUL-900012", "loan_first_year": 6, "sex": "F",
             "rate_class": "Juv", "surr_charge_id": "IUL07"}),
    13: (1, {"policy_id": "IUL-900013", "age_at_entry": 50, "premium_mode": "MONTHLY"}),
    14: (5, {"policy_id": "IUL-900014", "age_at_entry": 65, "premium_pp_ann": 4000.0}),
    15: (4, {"policy_id": "IUL-900015", "premium_pp_ann": 1500.0}),
    16: (4, {"policy_id": "IUL-900016", "premium_pp_ann": 1800.0}),
    17: (4, {"policy_id": "IUL-900017", "premium_pp_ann": 36000.0}),
    18: (1, {"policy_id": "IUL-900018", "wd_pp": 450.0}),
    19: (1, {"policy_id": "IUL-900019", "wd_pp": 450.0, "wd_first_year": 1}),
}

# The variants' own input rows, in the copies only.  The shipped COI scale covers the
# anchor cell, M NT issued at 45, alone, so each new class and sex gets the anchor's rows
# at a scale of its own, and a COI read under the wrong key reads a different number; the
# issue ages 50 and 65 get the anchor's rows to their own last policy year, at scales of
# their own.  IUL07 is the second schedule.
COI_KEYS = ["sex", "rate_class", "age_at_entry", "policy_year"]
COI_SCALES = {("M", "PElite"): 0.55, ("M", "PPlus"): 0.70, ("M", "Pref"): 0.85,
              ("M", "PTob"): 1.40, ("M", "Tob"): 1.75, ("F", "Juv"): 0.45}
COI_AGES = {50: 1.35, 65: 2.9}


def _coi_rates_with_variants(rates):
    """S's COI scale with rows for every cell the variants use, sorted by its four keys,
    as ``Data.coi_rates()`` indexes it, so that pandas slices a cell without a warning."""
    anchor = rates[(rates["sex"] == "M") & (rates["rate_class"] == "NT")
                   & (rates["age_at_entry"] == 45)]
    blocks = [rates]
    for (sex, rate_class), scale in COI_SCALES.items():
        blocks.append(anchor.assign(
            sex=sex, rate_class=rate_class,
            coi_rate_guar=(anchor["coi_rate_guar"] * scale).round(6),
            provenance="test copy"))
    for age, scale in COI_AGES.items():
        rows = anchor[anchor["policy_year"] <= 121 - age]
        blocks.append(rows.assign(age_at_entry=age,
                                  coi_rate_guar=(rows["coi_rate_guar"] * scale).round(6),
                                  provenance="test copy"))
    return pd.concat(blocks, ignore_index=True).sort_values(COI_KEYS, ignore_index=True)


def _surr_charges_with_iul07(table):
    """S's surrender charge schedule with IUL07: $30.00 per $1,000 over 7 years."""
    iul07 = pd.DataFrame([{"surr_charge_id": "IUL07", "sc_per_1000_init": 30.0,
                           "runoff_years": 7, "provenance": "test copy"}])
    return pd.concat([table, iul07], ignore_index=True)


# The input files the splice's copies change, S's and SEC's alike.
SPLICED_EDITS = {"coi_rates.csv": _coi_rates_with_variants,
                 "surr_charge_table.csv": _surr_charges_with_iul07}

# T2's months (USLIB-SEC-PLAN.md §7.4), by event rather than month by month, so that the
# grid is sized for what T2 and Phase 2's C4 both need.  All are S's months, under the
# splice's References.  On S's point 1, annual: 1, 11, 12 and 13 around the first
# segment's maturity and the first anniversary premium, 12 reading the maturing segment
# from the ladder's slot 12; 60, the committed row's, and 65 mid-year; 118 and 119 either
# side of the surrender charge's last month; 120, the first month of the lapse shock year;
# 239 and 240 either side of the guarantee's expiry, which shocks no policy with a cash
# value; 659 and 660 either side of the month charges cease, attained age 100 under the
# splice; 911, the last month, a frame of one row.  On S's point 2, Option B: 12, 65, and
# 131, the shock year's last month, the lapse cap binding.  On S's point 3, nothing
# allocated: 12 and 60, a ladder of empty segments.  On S's point 4, monthly: 1, 11, 12,
# 13, 59, 60, 61, 64, 65 and 66, a ladder of eleven or twelve live segments in every
# month, mid-year and either side of an anniversary; 118 and 119; 660.  On S's point 5:
# 21, 22 and 24, the guarantee holding, failing at t = 0 and passing again, its
# accumulator carried in deciding it; 239, 240 and 241 around its expiry, the account
# value's chain read cold after the lapsed guarantee; 371 and 372, the loan passing the
# cash value at 372; 373 and 374, the fixed account entering the month below 0; 577, 578
# and 579, the account value entering the month below 0 from 578.  On the variants:
#   6: 8, two months before its account runs out; 239, 240 and 241, the expiry shock on a
#     policy with no cash value at t = 0 and a month either side; 252, after it;
#   8: 12; 83 and 84, the 7-pay test's last month and the first after it, the latch held;
#   9: 36, the guideline cap's first anniversary; 37; 48, the latch held;
#   10: 12; 386, two months before the account runs out;
#   11: 12, running through S's months 22 and 23, and 12 and 100 through 590 and 592,
#     where the fixed account and then a segment's credit close on roundings about zero;
#   12: 60 and 61 around the first loan; 82, 83 and 84, the schedule's last charge, the
#     first month without and the shock year's first; 98, the loan passing the cash value;
#   13: 12; 179 and 180 either side of the guarantee's expiry at 15 years;
#   14: 34; 59 and 60 either side of its expiry shock at 5 years;
#   15: 15 and 16, a segment and then the pool on a rounding about zero;
#   16: 187 and 188, the same under the splice's References;
#   17: 6 and 7, the 7-pay test on the limit and then failing in the valuation month;
#   18: 566, 567 and 568, the face cut to nothing at 567.
# T3's: S's point 4 issued 25 months on, the committed row's, its months before issue
# reading policy years -2 to 0; S's point 1 a month on, the policy anniversaries a month
# off the valuation years; S's point 5 thirteen months on; variants 8, 9 and 14 thirteen
# months on, the 7-pay test failing, the target premium's guideline cap read from the
# premiums paid at its base, and the age-65 guarantee, in their issue months; variant 19
# thirteen months on, its face cut by a withdrawal in its issue month, from the face at
# issue, a base at t_entry() reached only under a condition (USLIB-SEC-PLAN.md §7.11,
# Record — M8, The core by line coverage, precised at M5); and variant 11 six months on,
# within a year, whose months before issue read the lapse shock year 0 of a point
# without a surrender charge, where an unguarded multiplier would read its shock
# (USLIB-SEC-PLAN.md §7.3, Record — M3).
PT_MTHS = {1: (1, 11, 12, 13, 60, 65, 118, 119, 120, 239, 240, 659, 660, 911),
           2: (12, 65, 131),
           3: (12, 60),
           4: (1, 11, 12, 13, 59, 60, 61, 64, 65, 66, 118, 119, 660),
           5: (21, 22, 24, 239, 240, 241, 371, 372, 373, 374, 577, 578, 579)}
VARIANT_MTHS = {6: (8, 239, 240, 241, 252), 8: (12, 83, 84), 9: (36, 37, 48),
                10: (12, 386), 11: (12, 100), 12: (60, 61, 82, 83, 84, 98),
                13: (12, 179, 180), 14: (34, 59, 60), 15: (15, 16), 16: (187, 188),
                17: (6, 7), 18: (566, 567, 568)}
SPLICES = tuple(("derived", p, d)
                for p, mths in (*PT_MTHS.items(), *VARIANT_MTHS.items()) for d in mths)
# S ships no point in force, so no twin of an S point is a splice case (§7.4, Today).
IN_FORCE_TWINS = ()
# The twins of the variants, every one issued at the valuation date, each compared with its
# S point cell by cell, as a row issued there is (USLIB-SEC-PLAN.md §7.7, Record — M9,
# Variants' twins): an issue rule that only a variant takes at t = 0 is reached nowhere
# else.
VARIANT_TWINS = tuple(("twin", p, 0) for p in VARIANTS)
FUTURES = ((4, 25), (1, 1), (5, 13), (8, 13), (9, 13), (14, 13), (19, 13), (11, 6))

# The default run's cases (the module docstring), each with what it is there for.  The
# rest of SPLICES, VARIANT_TWINS and FUTURES run with USLIB_SEC_FULL=1.  Each event has a
# core row in its own month, each kind of valuation month among them, as the core-reach
# test asserts, by AT_VALUATION.  Every variant's issue month is taken by its twin in the
# core or by a core row issued later.
CORE_SPLICES = {
    ("derived", 1, 12): "a segment maturing at t = 0 from the ladder's slot 12, an annual "
                        "premium and the deductions it carried",
    ("derived", 1, 119): "the surrender charge's first month without, at t = 0",
    ("derived", 1, 660): "charges ceasing at t = 0, at attained age 100",
    ("derived", 1, 911): "the last covered month, a frame of one row",
    ("derived", 2, 131): "Option B in the shock year's last month, the lapse cap binding",
    ("derived", 3, 12): "nothing allocated: a ladder of empty segments",
    ("derived", 4, 1): "the first month after issue, monthly, a ladder of one segment",
    ("derived", 4, 65): "mid-year, monthly, twelve live segments carried in",
    ("derived", 5, 22): "the guarantee failing at t = 0, decided by the accumulator",
    ("derived", 5, 373): "the fixed account entering t = 0 below 0, the loan above the "
                         "cash value",
    ("derived", 6, 240): "the expiry shock at t = 0 on a policy with no cash value",
    ("derived", 8, 84): "the MEC latch carried in where S's 7-pay test passes",
    ("derived", 11, 12): "a split allocation, its fixed account closing on roundings "
                         "about zero in S's months 22, 23 and 590",
    ("derived", 12, 84): "a loan drawn with its collateral carried apart, IUL07's lapse "
                         "shock year",
    ("derived", 12, 98): "the shortfall test at t = 0 netting the loan, which the "
                         "collateral carried apart from it would pass",
    ("derived", 15, 16): "the pool on a rounding about zero at t = 0",
    ("derived", 16, 188): "segments on roundings about zero carried in",
    ("derived", 17, 7): "the 7-pay test failing in the valuation month, no latch carried",
    ("derived", 18, 567): "the face cut to nothing at t = 0, the cut taking what is left",
    ("twin", 6, 0): "issued at the valuation date: PElite, underfunded",
    ("twin", 7, 0): "issued at the valuation date: PPlus, monthly, underfunded",
    ("twin", 9, 0): "issued at the valuation date: a target premium",
    ("twin", 10, 0): "issued at the valuation date: a single premium capped at its GSP",
    ("twin", 12, 0): "issued at the valuation date: F Juv on IUL07",
    ("twin", 13, 0): "issued at the valuation date at age 50, monthly",
    ("twin", 15, 0): "issued at the valuation date: S point 4 paying $1,500 a year",
    ("twin", 16, 0): "issued at the valuation date: S point 4 paying $1,800 a year",
    ("twin", 17, 0): "issued at the valuation date: over the 7-pay limit, monthly",
    ("twin", 18, 0): "issued at the valuation date: withdrawals that cut the face to 0",
}
CORE_FUTURES = {
    (4, 25): "policy years -2 to 0 before issue: the committed row's",
    (8, 13): "Pref over the 7-pay limit in its issue month",
    (14, 13): "issued at 65 thirteen months on",
    (19, 13): "a withdrawal in the issue month, the face cut from the face at issue",
    (11, 6): "issued within a year without a surrender charge: shock year 0 before issue",
}

SEC_FULL = os.environ.get("USLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "USLIB_SEC_FULL=1 (USLIB-SEC-PLAN.md K6)"))

# What the splice sets in both models, S and SEC alike, before either evaluates anything
# (USLIB-SEC-PLAN.md §7.5, Record — M5, The main splice's switches):
#   charges_cease_age at 100: charges, premiums and withdrawals cease in cover, at
#     attained age 100, and the frame runs on to maturity_age, 121, with rows either side
#     of the cessation; it ships at 121, equal to maturity_age, which a rewritten cell
#     reading the one for the other would hide;
#   lapse_rate_cap at 0.35 and lapse_shock_mult at 10.0: the cap, shipped at 1.0, binds in
#     the lapse shock year, the base rate's 4% times 10 against 35%; each ships equal to
#     another Reference a rewritten cell reads, the cap to index_par, the multiplier to
#     lapse_dyn_cap;
#   expense_unit_mth_2 at 0.05: the per-unit charge from policy year 11, which ships at 0,
#     equal to index_floor and inflation_rate;
#   mort_ae_factor at 0.56: the table's rate of 1.0 from attained age 119 would end every
#     life before the end of the frame, and at 0.56 survivors reach it on every point, so
#     that the survivors carried into t = proj_len(), which S's roll-forwards read there,
#     are compared; Tob's oldest rate is then 0.98, below the cap, which a test of its own
#     takes past 1.
# inflation_rate stays at its shipped 0, as does the second fixture's: IUL_US_S ships
# inflation at 0 and no improvement, so restated rows are S frame by frame, and a test of
# its own switches inflation on (USLIB-SEC-PLAN.md §7.1, Precised at M3, item 11, as
# precised at M5).
SPLICED_REFS = {"mort_ae_factor": 0.56, "charges_cease_age": 100, "lapse_rate_cap": 0.35,
                "lapse_shock_mult": 10.0, "expense_unit_mth_2": 0.05}

# The cells T2 and T3 skip beyond T1's: result_pols as a whole and check_margin, whose
# identity this model states with the debt a surrender recovers (the spec's exempt).  On a
# restated row S's own accessors of the point it opens differ by design: proj_len counts
# from the valuation date on SEC and from S's own start on S, so it differs by d, or by -k,
# and frame_mismatches asserts what it must get right, that both frames end at the same
# instant; duration_mth_init is d, or -k, on SEC and 0 on S; av_pp_init and loan_bal_init
# hold S's month-0 values on S and month d's on SEC.  index_level runs on the valuation
# clock (D7): on a row restated at d, S's level at t + d is SEC's at t times
# (1 + index_return_ann)^(d / 12), by design, and every credit, a ratio of two levels, is
# compared, so result_seg leaves too and is compared without its index_level column.  And
# is_mec latches here, where IUL_US_S's flag is the month's 7-pay test alone, so it is
# compared with S's flag accumulated over the months before, by _latch_faults.  Every cell
# that reads them is compared.
TWIN_EXEMPT = TWIN_EXEMPT_DEFAULT | SPEC.exempt
LATCHED = frozenset({"is_mec"})
SPLICE_EXEMPT = TWIN_EXEMPT | LATCHED | {"proj_len", "duration_mth_init", "av_pp_init",
                                         "loan_bal_init", "index_level", "result_seg"}
FUTURE_EXEMPT = TWIN_EXEMPT | LATCHED | {"proj_len", "duration_mth_init", "index_level",
                                         "result_seg"}
VARIANT_EXEMPT = TWIN_EXEMPT | LATCHED

# Every value is held to 1e-9 relative with no absolute floor, from Python 3.12, whose
# sum() of floats compensates as this model's two pools do: there the ladder's pools are
# S's bit for bit.  Python 3.11's sum() is a plain fold, which can leave a pool S closes on
# a rounding about zero on its other side, so below 3.12 every value takes the 1e-9 floor
# and the assertions that a pool is S's bit for bit are skipped.
EXACT_SUMS = sys.version_info >= (3, 12)
ATOL = 0.0 if EXACT_SUMS else 1e-9
FLOOR = 1e-9


def _issued_later(name, args):
    """The ``arg_map`` of a point issued at or after the valuation date, compared with S.

    S's keys as they are, but ``pols_if_at(0, "BEF_NB")``, S's issue month, which it
    leaves out (``None``): there S's cell counts the issued policies, as it does under
    every timing, and this model counts them as the month's new business, not yet in.
    """
    return None if name == "pols_if_at" and args[0] == 0 and args[1] == "BEF_NB" else args


def _carried_segments(d, term):
    """The ``arg_map`` of a row restated at S month ``d``: S's keys as they are, but
    ``seg_new_pp(m)`` of each segment S created and matured before month ``d - term``,
    which the row never reads, since no such segment is live at the valuation date.
    ``term`` is the models' ``seg_term_mth``, read off S's model by each caller, so that a
    splice at another segment term cuts off where its segments do."""
    def arg_map(name, args):
        return None if name == "seg_new_pp" and args[0] < d - term else args
    return arg_map

# The decrement rates keyed by month, none of which may be evaluated before issue (R1,
# D4); and the readers keyed by a policy year, by an attained age reached in cover and by a
# slot of the segment ladder.
DECREMENT_RATES = ("mort_rate", "mort_rate_mth", "lapse_rate_base", "lapse_rate",
                   "lapse_rate_mth")
KEYED_BY_YEAR = ("lapse_rate_base_py", "coi_rate_guar_py")
KEYED_BY_AGE = ("mort_rate_base_at", "corridor_factor_at")
KEYED_BY_SLOT = ("seg_bal_pp_init", "seg_ded_cum_pp_init", "seg_wd_cum_pp_init",
                 "seg_index_start_init", "seg_index_cap_init")

# The counts, which no floor ever reaches: a count falls far below 1e-7 late in a long
# frame, and is compared there at 1e-9 relative alone (USLIB-SEC-PLAN.md §5.2, T2).
COUNTS = frozenset({"policy_count", "pols_if_init", "pols_if", "pols_if_at",
                    "pols_new_biz", "pols_death", "pols_lapse", "pols_maturity"})
# The cells that scale with policy_count.  Every other cell is a per-policy amount, a
# rate, a clock or a flag, and must not move when the count does.  The residuals are
# relative, so a scaled count moves them in the last digits.
COUNTED = COUNTS | {
    "premiums", "prem_to_av", "maint_fee", "coi", "mth_deduction", "index_credits",
    "inv_income", "av_at", "av_change", "surr_charge", "claims_from_av", "claims_over_av",
    "claims", "claims_death", "claims_lapse", "withdrawals", "wd_fees", "net_loan_cf",
    "expenses", "premium_taxes", "margin_expense", "margin_mortality", "net_cf"}
RESIDUALS = ("check_av_components_resid", "check_av_roll_fwd_resid", "check_margin_resid",
             "check_seg_count_resid", "check_seg_credit_resid", "check_seg_bal_resid",
             "check_seg_closure_resid")
RELATIVE = ("check_av_components_resid", "check_av_roll_fwd_resid", "check_margin_resid",
            "check_seg_closure_resid")
CHECKS = ("check_av_components", "check_av_roll_fwd", "check_seg_ladder", "check_margin")
# The cells that read a segment's balance by IUL_US_S's own tests of zero: a balance of
# either sign that the arithmetic closes on a rounding about zero is read as one segment
# more or less, and a pool of such a rounding as one share of 1 (§7.7, Record — M9,
# Rounding about a bound).
TESTS_OF_ZERO = ("seg_count", "seg_share")

# result_pols' columns, in its order: the count, the new business within it, the month's
# deaths and lapses, the maturities, always zero, then S's two monthly decrement rates,
# which no count moves.
RESULT_POLS = ["pols_if", "pols_new_biz", "pols_death", "pols_lapse", "pols_maturity",
               "mort_rate_mth", "lapse_rate_mth"]
OUTFLOWS = RESULT_POLS[2:5]
RATES = RESULT_POLS[5:]
REPORTS = ("result_cf", "result_pols", "result_av", "result_seg")
# The reports whose columns are per-policy amounts, and result_seg's two columns that are
# not: the index level, on the valuation clock, and the segment count, an int.
PER_POLICY_REPORTS = ("result_av", "result_seg")

# The timings and kinds the model knows: the count's three, which S's stub names and
# answers with pols_if for each; the fixed account's six intra-month points, the
# collateral's two and the account value's five, and av_at's EOM; and the claim kinds,
# with claim_pp's WITHDRAWAL and claims_from_av's MATURITY.  No call here takes claims'
# kind=None default, which Phase 2 replaces with an explicit total cell
# (USLIB-SEC-PLAN.md D11, R12).
TIMINGS = ("BEF_MAT", "BEF_NB", "BEF_DECR")
FA_TIMINGS = ("BEF_PREM", "BEF_CREDIT", "BEF_WD", "BEF_FEE", "BEF_SWEEP", "BEF_INV")
LCA_TIMINGS = ("BEF_PREM", "BEF_INV")
AV_TIMINGS = ("BEF_PREM", "BEF_CREDIT", "BEF_WD", "BEF_FEE", "BEF_INV")
KINDS = ("DEATH", "LAPSE")
CLAIM_KINDS = ("DEATH", "LAPSE", "WITHDRAWAL")
AV_KINDS = ("DEATH", "LAPSE", "MATURITY")

# The opening state, in Data's order: IUL_US_S's two columns and the six this model adds.
# The ladder's five value columns.  S's label accessors, which no projection cell may read.
STATE = ("av_pp_init", "loan_bal_init", "fa_pp_init", "lca_pp_init", "sum_assured_init",
         "cum_prem_init", "cum_prem_net_init", "is_mec_init")
LADDER_VALUES = ("seg_bal_pp_init", "seg_ded_cum_pp_init", "seg_wd_cum_pp_init",
                 "seg_index_start_init", "seg_index_cap_init")
LABELS = ("sex", "rate_class", "db_option", "qual_test", "premium_type", "premium_mode",
          "surr_charge_id")
# IUL_US_S's engine cells, which take floats, kept for S's worked example and for T1, which
# compares S's keys through them (R14): no projection cell calls them, the credit inlined
# into seg_return, seg_credit_rate and index_credit_pp, and seg_matured_value no cell
# reads at all.
ENGINE = ("index_change", "index_credit_rate", "seg_credit_base", "index_credit",
          "seg_matured_value")

# The cells running in force adds to IUL_US_S's, each of which the symbol map must name.
NEW_CELLS = ("policy_count", "maturity_mth", "t_entry", "is_active", "pols_new_biz",
             "fa_pp_init", "lca_pp_init", "sum_assured_init", "cum_prem_init",
             "cum_prem_net_init", "is_mec_init", *LADDER_VALUES, "seg_index_start",
             "seg_index_cap", "is_db_option_a", "is_db_option_b", "is_gpt",
             "is_level_premium", "is_single_premium", "is_target_premium",
             "is_annual_premium", "is_monthly_premium", "wd_pp_mth", "loan_new_pp_ann",
             "corridor_factor_at", "mort_rate_base_at", "lapse_rate_base_py",
             "coi_rate_guar_py", "coi_rate_last_year", "surr_charge_rate_max",
             "surr_charge_runoff_years", *RESIDUALS, "point_id", "coi_schedule",
             "claims_death", "claims_lapse", "seg_credit_rate")

INFLATION = 0.025       # IUL ships 0; the inflation and scaling tests switch it on
COUNT_FACTOR = 2.5      # T4's factor, not a whole number (USLIB-SEC-PLAN.md §5.2)

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A report evaluates each column in ascending t, so a forward
# recursion, through t - 1, finds the month before already cached, and the committed rows
# sweep under limits of 18 to 28.  The exception is a chain read conditionally:
# IUL_US_S's count reads the net cash value only while the no-lapse guarantee holds, and
# then in its expiry year, so on S's point 5, whose guarantee holds last in month 48, the
# expiry's first month, 240, reads the account value's chain cold back to 49, one cell a
# month.  Each row sweeps under CALL_DEPTH plus an allowance derived from the row, the
# months from the guarantee's last holding month to its expiry (_expiry_gap), 192 on the
# twin of S's point 5 and on its row restated at 6, and 0 on every other committed row.  A
# backward recursion over a frame, through t + 1, opens a chain as long as the frame, and
# every committed frame but the row at 888's, 24 months, is 307 months or more, so 40
# stops every backward one there.
CALL_DEPTH = 40

# How deep a cold call may run beyond its chain, one cell a month from its month back to
# the chain's base (D5): the cells above the chain and those below it, the first month's
# charges and Data's first reads of its tables and of the ladder.  A cold net_cf in the
# last month runs 16 to 18 cells beyond one cell a month back to t_entry() on the
# committed rows and at the contract's longest cover, issue age 0, issued now and 120
# months on; each chain's head called alone, on a read of its own, runs at most 14 beyond.
# 25 leaves Phase 2 seven levels for a Data vector read below a table's reader.  Any chain
# of two cells a month runs a frame's length beyond.  The expiry read after a lapsed
# guarantee runs its chain back to the month after the guarantee last held, with the
# expiry's own cells above it, and takes a bound of its own (EXPIRY_OVERHEAD).
CHAIN_OVERHEAD = 25
EXPIRY_OVERHEAD = 30


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


def _seg(proj, name, t, m):
    """Segment cell ``name`` in month ``t`` of the segment born in policy month ``m``.

    ``IUL_US_S`` keys its six segment cells by the creation month, ``(t, m)``; Phase 2
    keys ``IUL_US_SEC``'s by the slot, ``(t, k)``, ``k = duration_mth(t) - m``, the
    segment's months since creation (USLIB-SEC-PLAN.md R15).  So a call that names a
    segment by its creation month reads either model: by slot where the cell takes ``k``,
    and 0.0 without a call for a segment not yet born, ``k`` below 0, which is the value
    ``IUL_US_S`` gives there.
    """
    cells = proj.cells[name]
    if cells.parameters[1] != "k":
        return cells(t, m)
    k = proj.duration_mth(t) - m
    return 0.0 if k < 0 else cells(t, k)


def _claims(proj, t, kind):
    """The claims of ``kind`` in month ``t``: Phase 2's cell of the kind where the model
    has it, ``claims_death(t)`` or ``claims_lapse(t)`` (R12), else ``claims(t, kind)``."""
    cell = {"DEATH": "claims_death", "LAPSE": "claims_lapse"}[kind]
    if cell in proj.cells:
        return proj.cells[cell](t)
    return proj.claims(t, _code(proj, kind))


def _keyed_as_s(proj):
    """Whether ``proj`` keys its segment cells as ``IUL_US_S`` does, by creation month."""
    return proj.cells["seg_bal_pp"].parameters[1] == "m"


def _twin(s_proj, sec_proj, *, arg_map=None, **kwargs):
    """``sec_support.twin_mismatches``, which every comparison in this module calls here.

    It passes the SEC Space's ``sec_support.codes``, which map S's timing and kind strings
    to the int codes Phase 2 gives them, and the spec's ``twin_arg_map``, which maps S's
    ``claims(t, None)``, the total, onto Phase 2's ``claims(t)``, skips S's
    ``claims(t, kind)``, whose values are Phase 2's ``claims_death`` and
    ``claims_lapse`` (R12), and moves S's segment cells from the creation month to the
    slot (R15).  The caller's ``arg_map`` runs first, on S's arguments, which it reads S
    at, then the spec's.  At stage ``"E"`` there were no codes; every comparison goes
    through here, so each took Phase 2's codes, split and slots when they came.  A
    comparison of SEC with SEC, T4's scaling, has keys alike on both sides, and takes
    the caller's map alone.
    """
    last = SPEC.twin_arg_map if _keyed_as_s(s_proj) else None

    def both(name, args):
        if arg_map is not None:
            args = arg_map(name, args)
        if args is not None and last is not None:
            args = last(name, args)
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

    ``month`` is the row's ``source_mth``: 0 for a twin; ``d`` for a derived row; ``-k``
    for a future one.  The twins keep S's ``point_id`` and ``policy_id``, so the S policy is
    the twin's.
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

    A projected IUL point holds tens of megabytes of cached values and their dependency
    graph, the ladder's two-month cells among them.  The splice's rows and the scaled and
    extract copies' points are each needed once, so each is released when read, as
    ``run_sec.py --block`` releases its points (USLIB-SEC-PLAN.md F5), and collected at
    once.  That costs little, because the swept models the module holds are frozen out of
    the collector (:func:`_freeze`), so the collection scans only what the row made.  Asked
    for again, the ItemSpace is made afresh and recomputes.  Without ``collect`` the
    collector is left to run when it will, as the every-state test leaves it for rows that
    computed nothing but their frame.
    """
    del model.Projection[key]
    if collect:
        gc.collect()


def _freeze():
    """Collect what is garbage, then freeze everything still alive out of the collector.

    Each fixture that sweeps a model calls this once its sweep is done, so that the
    collections after it, automatic or :func:`_release`'s, no longer scan the millions of
    objects a swept model holds.  The splices' fixtures undo their freezes as they close
    their models, and :func:`_collector` the rest as the module ends.
    """
    gc.collect()
    gc.freeze()


def _committed():
    """The committed SEC table as the file holds it, unvalidated, indexed by point_id."""
    return pd.read_csv(model_path(SEC).parent / TABLE, index_col="point_id")


def _committed_ladder():
    """The committed segment ladder as the file holds it, unvalidated, on a plain index."""
    return pd.read_csv(model_path(SEC).parent / LADDER)


def _s_table():
    """S's committed table as the file holds it, indexed by point_id."""
    return pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                       index_col="point_id")


def _sec_inputs(tmp_path, table, edits=None, ladder=None):
    """A copy of the product directory whose SEC table is ``table``; its SEC folder.

    ``ladder``, where given, is written over the segment ladder, a DataFrame on a plain
    index as the generator builds it, or an edit of the committed one.
    """
    edits = dict(edits or {})
    if ladder is not None:
        edits[LADDER] = ladder
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=edits)


def _s_inputs(tmp_path, table, edits=None):
    """A copy of the product directory whose S table is ``table``; its S folder."""
    return temp_inputs(tmp_path, model_path(TWIN), model_points=table, edits=edits)


def _read(folder, tag, refs=None, data=None):
    """The model in ``folder``, read under a name of its own, with References set first.

    ``refs`` are ``Projection`` References and ``data`` ``Data`` References, set on the
    model just read, before anything is computed: a compiled model clears no cache.  A
    text value that names a code of the model, ``"GUARANTEED"`` or ``"ADJ_BEGIN"``, is
    set as that code where the model has one, as Phase 2's has (R9), so that one dict of
    References serves S and SEC alike.
    """
    model = mx.read_model(folder, name=_name(tag))
    for ref, value in (refs or {}).items():
        if isinstance(value, str):
            value = _code(model.Projection, value)
        setattr(model.Projection, ref, value)
    for ref, value in (data or {}).items():
        setattr(model.Data, ref, value)
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


def _both(*edits):
    """An edit that applies each of ``edits`` in turn."""
    def edit(table):
        for each in edits:
            table = each(table)
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


# The S cells no report or check of IUL_US_S evaluates, which the comparisons compare only
# because _sweep_s evaluates them first: the premiums paid to date, the guideline and
# 7-pay limits and tests, the MEC flag and the shortfall test, each a flag or a total no
# report shows.  Their keyless readers, gsp, glp and seven_pay_prem, follow.
NEVER_REACHED = ("cum_prem_pp", "gpt_limit", "gpt_ok", "seven_pay_limit", "is_mec",
                 "is_shortfall")


def _sweep_s(proj):
    """Evaluate on an S point what the comparisons compare: the sweep, and more.

    :func:`sec_support.sweep` reaches none of :data:`NEVER_REACHED`, ``pols_if_at`` on
    ``IUL_US_S``, the maturity at ``claims_from_av``, or the account value in force at its
    timings past the opening one, because no result column or check reads them, and a cell
    S never evaluates is compared nowhere.  So they are evaluated here, over the frame,
    each at every timing or kind it takes, so that the comparisons see them too.
    """
    sweep(proj)
    for t in range(proj.proj_len()):
        for timing in TIMINGS:
            proj.pols_if_at(t, _code(proj, timing))
        for name in NEVER_REACHED:
            proj.cells[name](t)
        for kind in AV_KINDS:
            proj.claims_from_av(t, _code(proj, kind))
        for timing in (*AV_TIMINGS, "EOM"):
            proj.av_at(t, _code(proj, timing))


def _rounds(x):
    """Whether ``x`` is a nonzero rounding about zero: a float below :data:`FLOOR`."""
    return isinstance(x, float) and x != 0.0 and abs(x) < FLOOR


def _zero_test_rounds(s_proj, sec_proj, name, args, t_offset):
    """Whether a test of zero reads a rounding at S's key ``name(*args)`` in either model.

    ``seg_count(t)`` reads each live segment's balance at ``t`` and ``seg_share(t, m)`` the
    pool at ``t``: a nonzero rounding below :data:`FLOOR` there, in S at its month or in
    SEC at its own, is read as a segment more or less, or as a whole share, by the test of
    zero both models keep, so the two may part there by design (the module docstring).
    """
    t = args[0]
    u = t - t_offset
    if name == "seg_share":
        return _rounds(s_proj.seg_bal_active_pp(t)) or (
            u >= 0 and _rounds(sec_proj.seg_bal_active_pp(u)))
    lo = max(0, t - s_proj.seg_term_mth + 1)
    if any(_rounds(s_proj.seg_bal_pp(t, m)) for m in range(lo, t + 1)):
        return True
    if u < 0:
        return False
    d = sec_proj.duration_mth(u)
    return any(_rounds(_seg(sec_proj, "seg_bal_pp", u, m))
               for m in range(max(0, d - sec_proj.seg_term_mth + 1), d + 1))


def _floor_of(s_proj, name, args, value):
    """The absolute floor S's value at ``name(*args)`` is held to, or ``None`` for none.

    None for a count, a value that is not a float, or one at or above :data:`FLOOR`
    per policy; :data:`FLOOR` for a per-policy value below it; and for a count-weighted
    value, :data:`FLOOR` times S's count in force in its month, where the value is below
    that, its per-policy factor a rounding (the module docstring).
    """
    if name in COUNTS or type(value) is not float:
        return None
    if name in COUNTED:
        floor = FLOOR * abs(s_proj.pols_if(args[0]))
        return floor if abs(value) < floor else None
    return FLOOR if abs(value) < FLOOR else None


def _rounding_map(s_proj, sec_proj, t_offset, base, found):
    """An ``arg_map`` that holds S's roundings about zero to their floor, and passes on.

    Each key ``base`` keeps goes on to the comparison at ``ATOL``, but a key whose S value
    is a rounding by :func:`_floor_of`, which is compared here, with SEC's value, to its
    floor, any miss added to ``found``, and a key of :data:`TESTS_OF_ZERO` in a month where
    either model reads a rounding (:func:`_zero_test_rounds`), which is skipped.  Both kinds
    are left out of the comparison (``None``).  SEC's value is read at the arguments the
    comparison would read it at: S's ``t`` moved by ``t_offset``, and S's strings turned
    into SEC's codes, through the spec's ``twin_arg_map``, as :func:`_twin` maps them.
    """
    sec_codes = codes(sec_proj)
    last = SPEC.twin_arg_map if _keyed_as_s(s_proj) else None

    def arg_map(name, args):
        if base is not None:
            args = base(name, args)
            if args is None:
                return None
        params = s_proj.cells[name].parameters
        mapped = args if last is None else last(name, tuple(args))
        if mapped is None:
            return args
        sec_args = [sec_codes.get(a, a) if isinstance(a, str) else a for a in mapped]
        if "t" in params:
            at = params.index("t")
            if args[at] - t_offset < 0:
                return args
            sec_args[at] = args[at] - t_offset
        if name in TESTS_OF_ZERO and _zero_test_rounds(s_proj, sec_proj, name, args,
                                                       t_offset):
            return None
        value = s_proj.cells[name](*args)
        floor = _floor_of(s_proj, name, args, value)
        if floor is None:
            return args
        try:
            mine = sec_proj.cells[name](*sec_args)
        except Exception:                       # the comparison reports it
            return args
        if not abs(mine - value) <= floor:
            found.append(f"{name}{args}: S {value!r}, SEC {mine!r}, beyond the floor "
                         f"{floor:.3g}")
        return None
    return arg_map


def _floored_frame(s_df, sec_df, t_offset, report, s_proj, sec_proj):
    """``sec_df`` with each value that only a rounding sets apart from S's given S's.

    In ``report``'s per-policy columns (:data:`PER_POLICY_REPORTS`), a value S gives below
    :data:`FLOOR` and SEC within the floor of it; in ``result_cf``'s amounts, the same to
    the floor times the count in force; and in ``result_seg``'s ``seg_count``, a month where
    a test of zero reads a rounding (:func:`_zero_test_rounds`).  Every other value is left
    as SEC computed it, so :func:`sec_support.frame_mismatches` then reports it.
    """
    out = sec_df.copy()
    theirs = s_df.copy()
    theirs.index = s_df.index - t_offset
    shared = out.index.intersection(theirs.index)
    if report not in (*PER_POLICY_REPORTS, "result_cf") or not len(shared):
        return out
    for column in out.columns:
        if column not in theirs.columns or column in ("pols_if", "index_level"):
            continue
        a, b = theirs.loc[shared, column], out.loc[shared, column]
        if column == "seg_count":
            for t in a.index[a != b]:
                if _zero_test_rounds(s_proj, sec_proj, "seg_count", (t + t_offset,),
                                     t_offset):
                    out.at[t, column] = a[t]
            continue
        if report == "result_cf":
            floor = FLOOR * theirs.loc[shared, "pols_if"].abs()
        else:
            floor = FLOOR
        held = (a.abs() < floor) & ((b - a).abs() <= floor)
        out.loc[held[held].index, column] = a[held]
    return out


def _frame_faults(s_proj, sec_proj, month):
    """Where the four reports of ``sec_proj`` part from S's, frame by frame, from ``month``.

    Each report SEC row ``t`` against S row ``t + month``, at 1e-9 relative and ``ATOL``,
    every column both hold, frames ending together, but each value only a rounding sets
    apart (:func:`_floored_frame`) and, on a row restated or issued later, ``result_seg``'s
    ``index_level``, on the valuation clock.
    """
    found = []
    for report in REPORTS:
        theirs, mine = s_proj.cells[report](), sec_proj.cells[report]()
        columns = [c for c in theirs.columns if month == 0 or c != "index_level"]
        mine = _floored_frame(theirs, mine, month, report, s_proj, sec_proj)
        found += [f"{report}: {line}" for line in frame_mismatches(
            theirs, mine, t_offset=month, columns=columns, atol=ATOL)]
    return found


def _latch_faults(s_proj, sec_proj, month):
    """Where SEC's MEC latch is not S's 7-pay test failed in any month so far, by month.

    ``IUL_US_S``'s ``is_mec(t)`` is the month's 7-pay test alone, which no longer fails
    once the policy is past its seventh year; this model latches it, as ``UL_US_S``
    does.  So on SEC's every month ``t`` on the books, ``is_mec(t)`` is whether S's test
    failed in any month up to ``t + month``, its own months before the valuation date
    included.
    """
    found, latched = [], False
    for s in range(sec_proj.proj_len() + month):
        latched = latched or bool(s_proj.is_mec(s))
        t = s - month
        if t < sec_proj.t_entry():
            continue
        mine = sec_proj.is_mec(t)
        if mine is not latched:
            found.append(f"is_mec({t}) = {mine!r}, where S's test has failed so far: "
                         f"{latched}")
    return found


def _continues_s(s_proj, sec_proj, month, exempt=TWIN_EXEMPT, arg_map=None):
    """Where a row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison, on models at the same assumptions: frame by frame, the four
    reports (:func:`_frame_faults`); cell by cell over every other cell of S's but
    ``exempt``, every one to 1e-9 relative with no absolute floor, through ``arg_map``
    where it is given, but S's roundings about zero, each held to its floor
    (:func:`_rounding_map`); and, where ``exempt`` takes ``is_mec`` out, the latch against
    S's flag accumulated (:func:`_latch_faults`).
    """
    floored = []
    found = _frame_faults(s_proj, sec_proj, month)
    found += _twin(s_proj, sec_proj, t_offset=month, exempt=exempt | set(REPORTS),
                   arg_map=_rounding_map(s_proj, sec_proj, month, arg_map, floored),
                   atol=ATOL, limit=100)
    found += floored[:50]
    if LATCHED <= set(exempt):
        found += _latch_faults(s_proj, sec_proj, month)[:20]
    return found


def _case_id(kind, s_point, month):
    """A case's id: ``point4-d65``, ``point9-twin0``, or ``point4-k25`` if issued later."""
    if kind == "future":
        return f"point{s_point}-k{-month}"
    return f"point{s_point}-" + (f"d{month}" if kind == "derived" else f"{kind}{month}")


def _case(case, core, case_id):
    """One parametrized case: run by default if it is in ``core``, else on the full grid."""
    return pytest.param(*case, id=case_id, marks=() if case in core else FULL_ONLY)


def _held(case, s_point, core, case_id):
    """A splice case, ``(s_point, case)``: run by default if ``case`` is in ``core``.

    The splice's three comparisons parametrize ``s_point`` and ``case`` at class scope, so
    that pytest runs every case of one S point together, whichever test it belongs to, and
    ``_swept`` sweeps each S point once in a run rather than once for each test that
    compares one of its rows (USLIB-SEC-PLAN.md K6).  ``case`` itself is unique to its
    row, so it groups nothing.  The ids are the cases' own.
    """
    return pytest.param(s_point, case, id=case_id, marks=() if case in core else FULL_ONLY)


def _selected(cases, core):
    """The cases this run makes rows for: the core, or every one under USLIB_SEC_FULL."""
    return [case for case in cases if SEC_FULL or case in core]


# Every row the splice compares, as (row_kind, S point, source_mth), T3's included, and the
# default run's among them.
GRID = (*SPLICES, *IN_FORCE_TWINS, *VARIANT_TWINS,
        *(("future", p, -k) for p, k in FUTURES))
CORE_GRID = frozenset({*CORE_SPLICES, *(("future", p, -k) for p, k in CORE_FUTURES)})


def _s_table_with_variants(variants=VARIANTS):
    """S's committed table with ``variants`` appended, under their own point_ids."""
    table = _s_table()
    rows = []
    for point_id, (base, changes) in variants.items():
        row = table.loc[[base]].astype(object)
        for column, value in changes.items():
            row[column] = value
        row.index = pd.Index([point_id], name="point_id")
        rows.append(row)
    return pd.concat([table, *rows])


def _spliced_folder(root, s, derived, future, edits=SPLICED_EDITS):
    """The SEC folder for ``derived`` and ``future`` rows of ``s``, a model on S's copy.

    The generator builds the rows from the registered spec, out of ``s`` as it stands, and
    their segment ladder with them, so each opens with the state of the very run it is
    compared with, and the folder holds ``edits``.
    """
    spec = dataclasses.replace(SPEC, derived=tuple(derived), future=tuple(future))
    table, companions = build_sec_table(spec, s)
    assert set(companions) == {LADDER}
    return temp_inputs(root, model_path(SEC), model_points=table,
                       model_point_file=spec.model_point_file,
                       edits={**edits, **companions})


def _generated(root, refs, variants, derived=(), future=(), restate=None, points=None):
    """The SEC folder for ``derived`` and ``future`` rows of S's points with ``variants``.

    The generator builds the rows from the registered spec out of S on the splice's copy
    of its inputs, S's table with ``variants`` appended and :data:`SPLICED_EDITS`, with
    ``refs`` set, one S point at a time: each point is read alone, from a copy holding its
    row only, because the generator projects every point of the model it is given, and
    closed once its rows are built, so that one point's projection is held at a time.
    ``restate``, where given, is a function of a point's ItemSpace on that model that
    gives the months to restate the point at, in place of ``derived``.  The rows are then
    put in one table as the generator orders them, the twins in S's order, the derived and
    the future rows after them, in the order asked, under point_ids after the largest S
    one, and their segments in one ladder, renumbered alike.  So each row opens with the
    state of an S run on the inputs and References of the one it is compared with.
    ``points``, where given, are the S points of the table, its others left out.
    """
    table = _s_table_with_variants(variants)
    if points is not None:
        table = table.loc[list(points)]
    rows, ladders, asked = {}, {}, []
    for point_id in table.index:
        folder = temp_inputs(root / f"s{point_id}", model_path(TWIN),
                             model_points=table.loc[[point_id]], edits=SPLICED_EDITS)
        s = _read(folder, f"gen_s{point_id}", refs)
        try:
            months = (restate(_point(s, point_id)) if restate is not None
                      else [d for p, d in derived if p == point_id])
            spec = dataclasses.replace(
                SPEC, derived=tuple((point_id, d) for d in months),
                future=tuple((p, k) for p, k in future if p == point_id))
            built, companions = build_sec_table(spec, s)
        finally:
            s.close()
        asked += [("derived", point_id, d) for d in months]
        ladder = companions[LADDER]
        for row in built.to_dict("records"):
            case = (row["row_kind"], point_id, int(row["source_mth"]))
            rows[case] = row
            ladders[case] = ladder[ladder["point_id"] == row["point_id"]]
    if restate is None:
        asked = [("derived", p, d) for p, d in derived]
    order = [("twin", p, 0) for p in table.index] + asked + [
        ("future", p, -k) for p, k in future]
    labels = itertools.count(int(table.index.max()) + 1)
    out, segments = [], []
    for case in order:
        row = dict(rows[case])
        if case[0] != "twin":
            row["point_id"] = next(labels)
        out.append(row)
        segments.append(ladders[case].assign(point_id=row["point_id"]))
    return temp_inputs(root / "sec", model_path(SEC), model_points=pd.DataFrame(out),
                       model_point_file=SPEC.model_point_file,
                       edits={**SPLICED_EDITS,
                              LADDER: pd.concat(segments, ignore_index=True)})


def _splice(root, tag, refs, variants, splices, futures, core, points=None):
    """S and SEC on the splice's inputs with ``refs`` set in both: ``(s, sec)``.

    S is read from a copy of the product directory whose table has ``variants`` appended
    and whose COI and surrender charge tables are the splice's (:data:`SPLICED_EDITS`).
    SEC runs on the same tables, and on a model point table and a segment ladder of its
    own, built by the generator from the registered spec with its rows replaced by the
    cases this run selects of ``splices`` and ``futures``, the ``core`` or the full grid
    (:func:`_selected`), out of S on the same inputs and References, one point at a time
    (:func:`_generated`).  S is left unswept: each comparison sweeps the one S point it
    compares with, and releases the one swept before (:func:`_swept`), so that the class
    holds one S point at a time (USLIB-SEC-PLAN.md K6).  ``points``, where given, are the
    S points of the table both models read, its others left out.
    """
    derived = [(p, d) for kind, p, d in _selected(splices, core) if kind == "derived"]
    future = [(p, k) for p, k in futures if SEC_FULL or ("future", p, -k) in core]
    sec = _read(_generated(root / "gen", refs, variants, derived, future, points=points),
                f"sec_{tag}", refs)
    table = _s_table_with_variants(variants)
    try:
        s = _read(temp_inputs(root / "s", model_path(TWIN),
                              model_points=table if points is None
                              else table.loc[list(points)],
                              edits=SPLICED_EDITS), f"s_{tag}", refs)
    except BaseException:
        sec.close()
        raise
    return s, sec


_SWEPT_POINT = {}


def _swept(s, point_id):
    """S point ``point_id`` of ``s``, a splice's S model, swept (:func:`_sweep_s`).

    The one point of ``s`` held swept: asked for another, it releases the point it holds
    first, collecting it, so that a splice's class holds one S point's projection at a
    time, not all of them (USLIB-SEC-PLAN.md K6), and sweeps the new one, then freezes it
    out of the collector (:func:`_freeze`), as the module's swept models are, so that the
    collections the released SEC rows trigger do not scan it.  Asked for the point it
    holds, it returns it as swept.
    """
    held = _SWEPT_POINT.get(s.name)
    if held != point_id:
        if held is not None:
            _release(s, _key(s, held), collect=False)
            gc.unfreeze()
            gc.collect()
        _SWEPT_POINT[s.name] = point_id
        _sweep_s(_point(s, point_id))
        gc.freeze()
    return _point(s, point_id)


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


def _expiry_gap(p):
    """The months the guarantee's expiry reads the account value's chain back over, cold.

    ``IUL_US_S``'s count reads the net cash value in a month only while the no-lapse
    guarantee holds (``lapse_rate``'s first test) and in the guarantee's expiry year (its
    shock), so where the guarantee fails before its expiry, nothing reads the account value
    from the month after it last held to the expiry's first month, whose read then runs the
    chain back cold.  This is that gap, the months from the one after the guarantee last
    held to the expiry's first, both counted, ``0`` where the guarantee holds to its
    expiry, has expired before the valuation date, or expires after the frame: the
    allowance a row's ascending sweep takes beyond :data:`CALL_DEPTH`.  It reads the
    guarantee's test month by month, which reads the accumulator alone, one cell a month.
    """
    entry, end = p.t_entry(), p.proj_len()
    expiry = 12 * p.nlg_period_years() - p.duration_mth_init()
    if not entry < expiry < end:
        return 0
    held = [t for t in range(entry, expiry) if p.nlg_in_effect(t)]
    last = held[-1] if held else entry - 1
    return 0 if last == expiry - 1 else expiry - last


@pytest.fixture(scope="module")
def sec_read():
    """IUL_US_SEC read in place, as committed, and swept once, cold; what it met.

    The model is first asked for ``duration_mth(400)`` on the twin of S point 1, and the
    keys that call leaves in ``duration_mth`` are kept.  Then every committed point is
    swept (:func:`sec_support.sweep`: ``result_cf``, the other reports and the checks), in
    table order and each column in ascending ``t``, under a recursion limit lowered to
    :data:`CALL_DEPTH` plus the row's own allowance (:func:`_expiry_gap`), and whatever
    that raises is kept, point by point, rather than raised.  Last, the keys
    ``IUL_US_S``'s label accessors hold on each point, which no projection cell may read,
    are counted.  So the record says what a cold model does, which the clock test asserts
    (D3, R2), and every test on the committed model reads a model already swept: the
    sweep is paid once, not once for each.  The swept model is then frozen out of the
    collector (:func:`_freeze`).  Returns ``(model, record)``.
    """
    model = mx.read_model(model_path(SEC), name=_name("sec"))
    first = _row(model, "twin", 1, 0)
    record = {"duration_mth(400)": first.duration_mth(400),
              "keys": list(first.cells["duration_mth"].keys()), "deep": [], "labels": {},
              "gaps": {}}
    labels = model.Data.model_point_table().index
    limit = mx.get_recursion()
    try:
        for key, point_id in zip(point_keys(model), labels):
            p = projection(model, key)
            record["gaps"][point_id] = gap = _expiry_gap(p)
            mx.set_recursion(CALL_DEPTH + gap)
            try:
                sweep(p)
            except Exception as err:            # kept, so every point is swept
                record["deep"].append(f"point {point_id}: the sweep raised {_raised(err)}")
            finally:
                mx.set_recursion(limit)
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
    """IUL_US_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """IUL_US_S read in place, as committed, with every point swept (:func:`_sweep_s`).

    T6 regenerates the SEC table and its ladder from it, which would otherwise project
    every S point again (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the tests on
    the committed rows read S's months off it, the cells its own sweep misses among them.
    Frozen once swept (:func:`_freeze`).
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

    The main splice's grid, :data:`VARIANTS` and the rows the run selects of
    :data:`SPLICES` and :data:`FUTURES` (:func:`_splice`).  Each SEC row is projected by
    the case that compares it and released once compared (:func:`_settle`).

    Scoped to the class that holds every test of the splice, so that its two models are
    closed before the committed model and S are first read: the module never holds both,
    which keeps its peak at the larger of the two.  S is swept one point at a time, as the
    cases ask for it (:func:`_swept`).  Once both are read the heap is frozen, so that the
    collections the released rows trigger scan the rows alone; at teardown the models are
    closed, then the freeze is undone and the collector run.
    """
    s, sec = _splice(tmp_path_factory.mktemp("spliced"), "spliced", SPLICED_REFS,
                     VARIANTS, SPLICES + IN_FORCE_TWINS + VARIANT_TWINS, FUTURES,
                     CORE_GRID)
    try:
        gc.collect()
        gc.freeze()
        yield s, sec
    finally:
        sec.close()
        s.close()
        gc.unfreeze()
        gc.collect()


@pytest.fixture(scope="class")
def splice_records():
    """What each splice row was found to do, by case (:func:`_scanned`, :func:`_settle`)."""
    return {}


@pytest.fixture(scope="class")
def splice_bounds(spliced):
    """The record of the splice's SEC model's ``min`` and ``max`` (:class:`_BoundSides`)."""
    return _BoundSides(spliced[1])


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


# The cells that loop over the frame by design: the reports and the checks.  Every other
# cell without a t reads none keyed by t but those FOLLOWED names, which the rules test
# asserts, since it is what lets the scan judge a read through a cell keyed by an attained
# age, a policy year or a slot of the ladder by the month that asked.
LOOPS = frozenset({*REPORTS, *CHECKS})
# The one cell keyed by no month that reads a cell keyed by t: seg_new_pp(m), a segment's
# balance at its creation in policy month m, which reads the sweep of that month,
# sweep_pp(m - duration_mth_init()), for a segment created on the books, and the ladder for
# one carried in.  The scan follows it to what it reads and judges each such read against
# the month of the cell that asked, as R1 and R2 judge a read of t (USLIB-SEC-PLAN.md
# §5.2, T2, as precised at M12).
FOLLOWED = frozenset({"seg_new_pp"})
# The cells keyed by a policy month m beside t, the segment ladder's: segment m's share,
# draw, deduction, balance and running totals in month t.
SEGMENT = ("seg_share", "seg_wd_pp", "seg_ded_pp", "seg_bal_pp", "seg_ded_cum_pp",
           "seg_wd_cum_pp")


def _segment_months(proj, t, name):
    """The keys after ``t`` at which month ``t`` is swept in segment cell ``name``.

    The segments live in the month, born in policy months ``duration_mth(t) - 11`` to
    ``duration_mth(t)``, those at or after the policy's issue, in every segment cell: the
    month's own segment included, whose share the pool, which reads the segments born
    before the month, gives no draw, and whose share at ``t_entry()`` is 0, as
    ``IUL_US_S``'s read of a balance outside its segment's life gives, with no ladder row
    asked for.  The segment maturing in month ``t`` is read at ``t - 1``, where it is
    live.  Each is keyed by its creation month ``m`` where the cell takes ``m``, as at
    stage ``"E"``, and by its slot, ``duration_mth(t) - m``, 0 to
    ``min(seg_term_mth - 1, duration_mth(t))``, where it takes ``k``, as Phase 2's
    cells do (R15).
    """
    d = proj.duration_mth(t)
    months = range(max(0, d - proj.seg_term_mth + 1), d + 1)
    if proj.cells[name].parameters[1] == "k":
        return [d - m for m in months]
    return months


def _sweep_on_the_books(proj):
    """Evaluate every monthly cell of ``proj`` at every month on the books.

    Each cell whose first parameter is ``t``, at each month from ``t_entry()`` to
    ``proj_len() - 1``, and at each timing or kind the guard test's sets give it, and each
    segment cell at each segment the month reads it at (:func:`_segment_months`), as
    Phase 2's full sweep does; the months outside cover are the guard test's
    (:func:`_outside_cover_faults`).  The loops over the frame leave cells unread on the
    books, the account value in force at its later timings and the shortfall test among
    them, and a read no cell makes is a read the scan cannot judge.  A cell with a
    parameter the sets give no values raises.
    """
    months = range(proj.t_entry(), proj.proj_len())
    for name in sorted(_monthly_cells(proj)):
        cells, rest = proj.cells[name], proj.cells[name].parameters[1:]
        if name in SEGMENT:
            for t in months:
                for m in _segment_months(proj, t, name):
                    cells(t, m)
            continue
        values = [_code(proj, kind)
                  for kind in (*BY_ARGUMENT.get(name, ()), *OPENING.get(name, ()))]
        if rest and not values:
            raise ValueError(f"{name}{cells.parameters}: no timing or kind to sweep it at")
        for t in months:
            if not rest:
                cells(t)
            else:
                for value in values:
                    cells(t, value)


def _judge(found, call, t, entry, node):
    """Judge one precedent ``node`` of ``call``, a call at month ``t``, by its month."""
    params = getattr(node.obj, "parameters", None) or ()
    if "t" not in params:
        return
    u = node.args[params.index("t")]
    if not _month(u):
        return
    if u < entry <= t:
        found["early"].append(f"{call} -> {node.obj.name}{node.args}")
    if u > t + 1:
        found["ahead"].append(f"{call} -> {node.obj.name}{node.args}")


def _rule_breaches(proj):
    """R1, R1a and R2 on one row, once it has run on the books.

    The row runs each loop over the frame, the four reports first (:data:`LOOPS`), and
    then every monthly cell at every month on the books (:func:`_sweep_on_the_books`):
    what the row computes of itself, at its own months, which is what Phase 2 sweeps, and
    not S's keys, at which the comparison then evaluates SEC's cells.  Returns
    ``{"negative": [...], "early": [...], "ahead": [...], "unjudged": [...],
    "defaults": [...], "followed": n, "edges": n}``: every cached call with a negative
    argument, a month, a policy month of creation, an attained age, a policy year or a
    slot; every precedent keyed by a month before ``t_entry()`` of a call keyed by a month
    at or after it; every precedent keyed by a month beyond ``t + 1`` of a call keyed by
    ``t``; and each read through a cell of :data:`FOLLOWED`, judged so against the month
    of the call that asked, and counted; every call of a cell without a ``t``, the loops
    over the frame and the followed cell excepted, that reads one keyed by ``t``; every key
    of an engine cell that takes S's ``None`` for the cap or the convention, which this
    model passes explicitly on its projection path, or of ``seg_matured_value``, which no
    cell reads; and how many precedents the scan read, which must not be 0, or the scans
    held of nothing.  A precedent is a call's as modelx's dependency graph records it.
    """
    for name in (*REPORTS, *CHECKS):
        proj.cells[name]()
    _sweep_on_the_books(proj)
    entry = proj.t_entry()
    found = {"negative": [], "early": [], "ahead": [], "unjudged": [], "defaults": []}
    edges = followed = 0
    for name, cells in proj.cells.items():
        params = cells.parameters
        for args in _cached_args(cells):
            if any(_month(a) and a < 0 for a in args):
                found["negative"].append(f"{name}{args}")
            if name in ENGINE and (None in args or name == "seg_matured_value"):
                found["defaults"].append(f"{name}{args}")
            if "t" in params:
                t = args[params.index("t")]
                call = f"{name}{args}"
                for node in cells.preds(*args):
                    edges += 1
                    if node.obj.name in FOLLOWED:
                        for inner in node.obj.preds(*node.args):
                            followed += 1
                            _judge(found, f"{call} -> {node.obj.name}{node.args}", t,
                                   entry, inner)
                        continue
                    _judge(found, call, t, entry, node)
            elif name not in LOOPS | FOLLOWED:
                for node in cells.preds(*args):
                    edges += 1
                    if "t" in (getattr(node.obj, "parameters", None) or ()):
                        found["unjudged"].append(f"{name}{args} -> {node.obj.name}"
                                                 f"{node.args}")
    return {**found, "followed": followed, "edges": edges}


# What each monthly cell holds outside cover, before issue and in the month after the
# frame, t = proj_len(), which the roll-forwards read, as its docstring says: no count
# carried, no value, premium, withdrawal, loan, charge, credit, rate, decrement, claim or
# flow, and no question about the contract answered yes.  The type is part of the value:
# an amount, a rate or a count is a float in every branch, a flag a bool and the segment
# count an int, because Phase 2 types a cell by the values it returns (USLIB-SEC-PLAN.md
# F3).
OUTSIDE_COVER = {
    # flags
    "is_active": False, "nlg_test_ok": False, "nlg_in_effect": False,
    "nlg_expiry_shock": False, "is_shortfall": False, "gpt_ok": False, "is_mec": False,
    # the segment count, an int
    "seg_count": 0,
    # premiums, withdrawals and loans
    "prem_persistency": 0.0, "premium_pp": 0.0, "prem_to_av_pp": 0.0, "wd_pp": 0.0,
    "wd_fee_pp": 0.0, "loan_new_pp": 0.0, "draw_pp": 0.0, "draw_from_seg_pp": 0.0,
    "draw_from_fa_pp": 0.0, "cum_prem_pp": 0.0, "cum_prem_net_pp": 0.0,
    "cum_mnlp_pp": 0.0, "gpt_limit": 0.0, "seven_pay_limit": 0.0,
    # the face, the death benefit and the cost of insurance
    "face_reduction_pp": 0.0, "sum_assured_at": 0.0, "units": 0.0,
    "corridor_factor": 0.0, "db_pp": 0.0, "net_amt_at_risk": 0.0, "coi_rate_guar": 0.0,
    "coi_rate": 0.0, "coi_pp": 0.0, "rider_charge_pp": 0.0,
    # charges, the accounts, the ladder and the loan
    "expense_unit_mth_at": 0.0, "maint_fee_pp": 0.0, "mth_deduction_pp": 0.0,
    "mth_deduction_from_seg_pp": 0.0, "mth_deduction_from_fa_pp": 0.0,
    "seg_bal_active_pp": 0.0, "seg_bal_tot_pp": 0.0, "sweep_pp": 0.0, "seg_return": 0.0,
    "seg_index_start": 0.0, "seg_index_cap": 0.0, "index_credit_pp": 0.0,
    "seg_roll_pp": 0.0, "seg_credit_rate": 0.0, "cred_rate_ann": 0.0,
    "comp_rate_ann": 0.0, "fa_pp": 0.0, "lca_pp": 0.0, "loan_bal_pp": 0.0,
    "loan_credit_rate_ann": 0.0, "loan_credit_rate_mth": 0.0, "inv_income_pp": 0.0,
    "av_pp": 0.0,
    "surr_charge_rate": 0.0, "surr_charge_pp": 0.0, "csv_pp": 0.0, "ncsv_pp": 0.0,
    # rates
    "mort_rate": 0.0, "mort_rate_mth": 0.0, "lapse_rate_base": 0.0, "lapse_rate": 0.0,
    "lapse_rate_mth": 0.0,
    # counts
    "pols_new_biz": 0.0, "pols_death": 0.0, "pols_lapse": 0.0, "pols_maturity": 0.0,
    # flows
    "premiums": 0.0, "prem_to_av": 0.0, "maint_fee": 0.0, "coi": 0.0,
    "mth_deduction": 0.0, "index_credits": 0.0, "inv_income": 0.0, "surr_charge": 0.0,
    "claims_over_av": 0.0, "claims": 0.0, "claims_death": 0.0, "claims_lapse": 0.0,
    "withdrawals": 0.0, "wd_fees": 0.0, "net_loan_cf": 0.0,
    "expenses": 0.0, "premium_taxes": 0.0, "margin_expense": 0.0,
    "margin_mortality": 0.0, "net_cf": 0.0,
    # the cells that read t + 1, and the residuals, which return their zero before they
    # read it
    "av_change": 0.0, **{name: 0.0 for name in RESIDUALS},
}
# 1.0, the two lapse multipliers' neutral value.
NEUTRAL = {"lapse_rate_sc_mult": 1.0, "lapse_rate_dyn_mult": 1.0}
# The policy clock, a Python int at every month, outside cover too: before issue its values
# are negative, or 0, and a cell keyed by them must not read a table there.
CLOCK = ("duration_mth", "duration", "policy_year", "age")
# The inputs read on the valuation clock (D7), floats at every month, one function of t
# for every point: the index path, expense inflation stepping on valuation years, and the
# level inputs read at t, the cap declared, the fixed account's rate and its monthly
# rate, and the policy fee, each of which holds its value outside cover.
VALUATION_CLOCK = ("index_level", "inflation_factor", "index_cap_at", "fixed_rate_ann",
                   "inv_return_mth", "expense_pol_mth_at")
# Cells with a timing or a kind, 0.0 at every one of these outside cover.
BY_ARGUMENT = {"claim_pp": CLAIM_KINDS, "claims_from_av": AV_KINDS,
               "fa_pp_at": FA_TIMINGS, "lca_pp_at": LCA_TIMINGS,
               "av_pp_at": AV_TIMINGS[1:], "av_at": (*AV_TIMINGS[1:], "EOM")}
# The opening timings carried into the month after the frame, 0.0 before issue, and there
# what the survivors of its last month carry into it (CARRIED): the count, at every
# timing, and the account value per policy and in force.
OPENING = {"pols_if_at": TIMINGS, "av_pp_at": AV_TIMINGS[:1], "av_at": AV_TIMINGS[:1]}
CARRIED = ("pols_if",)
# The sets above, which together must hold every cell whose first parameter is t, once.
GUARD_SETS = {"OUTSIDE_COVER": set(OUTSIDE_COVER), "NEUTRAL": set(NEUTRAL),
              "CLOCK": set(CLOCK), "VALUATION_CLOCK": set(VALUATION_CLOCK),
              "BY_ARGUMENT, OPENING": set(BY_ARGUMENT) | set(OPENING),
              "SEGMENT": set(SEGMENT), "CARRIED": set(CARRIED)}


def _monthly_cells(proj):
    """Every cell of ``proj`` whose first parameter is ``t``."""
    return {name for name, cells in proj.cells.items()
            if cells.parameters and cells.parameters[0] == "t"}


def _on_the_clocks(p, t):
    """What each cell of :data:`CLOCK` and :data:`VALUATION_CLOCK` holds at month ``t``.

    The policy clock in closed form from the point's ``duration_mth``, and the inputs on
    the valuation clock from the Projection's References and ``t`` alone: the index path
    from its level at the valuation date, expense inflation stepping on valuation years,
    and the level inputs of the basis the References set.
    """
    d = p.duration_mth_init() + t
    guaranteed = p.basis == _code(p, "GUARANTEED")
    rate = p.guar_rate_ann if guaranteed else p.fixed_rate_curr
    return {"duration_mth": d, "duration": d // 12, "policy_year": d // 12 + 1,
            "age": p.age_at_entry() + d // 12,
            "index_level": p.index_level_init * (1 + p.index_return_ann) ** (t / 12),
            "inflation_factor": (1 + p.inflation_rate) ** (t // 12),
            "index_cap_at": p.index_cap_guar if guaranteed else p.index_cap_curr,
            "fixed_rate_ann": rate, "inv_return_mth": (1 + rate) ** (1 / 12) - 1,
            "expense_pol_mth_at": (p.expense_pol_mth_guar if guaranteed
                                   else p.expense_pol_mth)}


def _survivors(p, t):
    """The count the last month ``t - 1`` leaves for ``t``: its count, out of its deaths
    and its lapses, in that order, as the count's recursion takes them."""
    return p.pols_if(t - 1) - p.pols_death(t - 1) - p.pols_lapse(t - 1)


def _outside_cover_faults(p, where):
    """Where ``p``, an ItemSpace, departs from what each monthly cell holds outside cover.

    In every month before issue and at ``t = proj_len()``: every cell of
    :data:`OUTSIDE_COVER` and :data:`NEUTRAL`, :data:`BY_ARGUMENT` at each of its timings
    or kinds, and each segment cell at the policy months of creation about that month, and
    before issue :data:`OPENING`'s and ``pols_if``, against their values with their types;
    :data:`CLOCK` and :data:`VALUATION_CLOCK` against :func:`_on_the_clocks`.  At
    ``t = proj_len()`` the count at every timing is the survivors of the last month, out of
    its count by its deaths and its lapses, and the account value per policy is the last
    month's close.  Then the keyed readers: the policy-year tables' keys run from 1 to the
    policy year of the last month, the age-keyed tables' from the age at the first month
    on the books to the age of the last, and the ladder's slots from 1 to the twelve, or
    the fewer months in force, a point in force holds, and none on a point not yet in force,
    so no table was read at a year, an age or a slot the policy does not have.  And no
    monthly cell holds a ``t`` past ``proj_len()``.  A cell that raises is a fault too, so
    the scan goes on.
    """
    faults = []
    L, entry, d0 = p.proj_len(), p.t_entry(), p.duration_mth_init()

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
        for name, labels in BY_ARGUMENT.items():
            for label in labels:
                check(name, (t, _code(p, label)), 0.0)
        d = d0 + t
        for name in SEGMENT:
            keys = ({0, 1, p.seg_term_mth - 1} if p.cells[name].parameters[1] == "k"
                    else {0, max(d - 12, 0), max(d - 1, 0), max(d, 0)})
            for m in sorted(keys):
                check(name, (t, m), 0.0)
        if t < entry:
            for name, labels in OPENING.items():
                for label in labels:
                    check(name, (t, _code(p, label)), 0.0)
            check("pols_if", (t,), 0.0)
        for name, want in _on_the_clocks(p, t).items():
            check(name, (t,), want)
    survivors = _survivors(p, L)
    check("pols_if", (L,), survivors)
    for timing in TIMINGS:
        check("pols_if_at", (L, _code(p, timing)), survivors)
    bef_prem = _code(p, "BEF_PREM")
    check("av_pp_at", (L, bef_prem), p.av_pp(L - 1))
    check("av_at", (L, bef_prem), p.av_pp_at(L, bef_prem) * p.pols_if(L))
    ranges = {**{name: range(1, p.policy_year(L - 1) + 1) for name in KEYED_BY_YEAR},
              **{name: range(p.age(entry), p.age(L - 1) + 1) for name in KEYED_BY_AGE},
              **{name: range(1, min(p.seg_term_mth, max(d0, 0)) + 1)
                 for name in KEYED_BY_SLOT}}
    for name, allowed in ranges.items():
        outside = sorted(k for k in p.cells[name].keys() if k not in allowed)
        if outside:
            faults.append(f"{where}: {name} read at {outside[:5]}, outside {allowed}")
    past = sorted(f"{name}{key}" for name in _monthly_cells(p)
                  for key in p.cells[name].keys()
                  if (key[0] if isinstance(key, tuple) else key) > L)
    if past:
        faults.append(f"{where}: evaluated past t = proj_len() = {L}: {past[:5]}")
    return faults


def _least_live(p, where):
    """Where ``check_seg_bal_resid`` is not the least live segment's balance, and if met.

    On every month ``t`` on the books of row ``p``, the residual is the least balance of
    the segments live in the month, born in policy months ``duration_mth(t) - 11`` to
    ``duration_mth(t)``, or 0 where none is below 0 (R1a).  Returns the months where it is
    not, and whether some month's least live segment was below 0, the one state in which a
    residual over the wrong segments, which on a row in force are segments long matured, at
    0, gives another number.
    """
    faults, met = [], False
    for t in range(p.t_entry(), p.proj_len()):
        d = p.duration_mth(t)
        least = min([0.0, *(_seg(p, "seg_bal_pp", t, m)
                            for m in range(max(0, d - p.seg_term_mth + 1), d + 1))])
        met = met or least < 0.0
        if p.check_seg_bal_resid(t) != least:
            faults.append(f"{where}: check_seg_bal_resid({t}) = "
                          f"{p.check_seg_bal_resid(t)!r}, the least live segment {least!r}")
    return faults, met


def _carry(p):
    """What the survivors of the last month carry into ``t = proj_len()`` on ``p``.

    The values the end-of-projection test asserts, read once the row is projected: the
    count there, at every timing, and the survivors it must be; the account value per
    policy there and the last month's close; the account value in force there; the four
    checks, which read it; and the flows of that month, which must be zero.
    """
    L = p.proj_len()
    bef_prem = _code(p, "BEF_PREM")
    return {
        "L": L, "pols_if": p.pols_if(L),
        "timings": [p.pols_if_at(L, _code(p, timing)) for timing in TIMINGS],
        "survivors": _survivors(p, L),
        "av_pp": p.av_pp_at(L, bef_prem), "av_pp_last": p.av_pp(L - 1),
        "av_at": p.av_at(L, bef_prem),
        "checks": tuple(p.cells[check]() for check in CHECKS),
        "flows": [p.premiums(L), p.pols_death(L), p.pols_lapse(L), p.expenses(L),
                  p.withdrawals(L), p.net_loan_cf(L), p.index_credits(L), p.net_cf(L),
                  *(_claims(p, L, kind) for kind in KINDS)]}


def _lapse_raw(x, t):
    """The annual lapse rate before its cap: S's product of three factors."""
    return x.lapse_rate_base(t) * x.lapse_rate_sc_mult(t) * x.lapse_rate_dyn_mult(t)


def _surr_charge_raw(x, t):
    """The surrender charge per $1,000 of month ``t`` before its floor at 0."""
    init, yrs = x.surr_charge_rate_max(), x.surr_charge_runoff_years()
    return init - (init / yrs) * ((x.duration_mth(t) + 1) / 12)


def _option(x, t):
    """The death benefit option's amount in month ``t``, which the corridor bounds."""
    face = x.sum_assured_at(t)
    return face + x.av_pp_at(t, _code(x, "BEF_FEE")) if x.is_db_option_b() else face


def _corridor_raw(x, t):
    """The corridor's death benefit in month ``t``: its factor times the account value."""
    return x.corridor_factor(t) * x.av_pp_at(t, _code(x, "BEF_FEE"))


def _naar_raw(x, t):
    """The net amount at risk of month ``t`` before its floor at 0."""
    return x.db_pp(t) / x.naar_factor() - x.av_pp_at(t, _code(x, "BEF_FEE"))


def _seven_pay_failed(x, t):
    """Whether the month's 7-pay test fails: ``IUL_US_S``'s ``is_mec(t)``, unlatched."""
    return x.policy_year(t) <= 7 and x.cum_prem_pp(t) > x.seven_pay_limit(t)


def _slots(x):
    """The ladder's slots a point in force holds: 1 to twelve, or its months in force."""
    return range(1, min(x.seg_term_mth, max(x.duration_mth_init(), 0)) + 1)


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, on a row in force there, each kind of
# valuation month the full grid has, each on the raw value at t = 0 (USLIB-SEC-PLAN.md
# §7.7, Record — M9, Each kind of valuation month): every opening-state column in use, a
# ladder of each kind and the segment maturing at t = 0 from it, its deductions and draws
# carried, a premium of each mode, the surrender charge's last month, the lapse shock
# year's last, the guarantee failing on the accumulator carried in, its expiry and its
# shock, a loan drawn and one carried with its collateral apart, the fixed account and the
# account value entering below 0 and the loan above the cash value, the MEC latch carried
# where S's test passes and the test failing where none is carried, a segment and the pool
# on roundings about zero, the face cut to nothing and charges ceasing.  Of every row, the
# end of the frame leaves survivors to carry.  Later in the frame, on every row, a premium
# of each kind, the guideline cap, a withdrawal and a loan, the corridor, the lapse cap,
# the shock year, lapses the guarantee suppresses, its expiry shock, the shortfall, the
# accounts below 0, draws and deductions on the segments, a credit, the two rates' second
# steps, charges ceased, the latch held and a face of nothing; the test also reads each
# side of every min and max by the values it compares (_BoundSides).
AT_VALUATION = {
    **{f"{column} in use": (lambda x, column=column: x.cells[column]() != 0)
       for column in STATE},
    "a ladder of fewer than twelve segments": lambda x: x.duration_mth_init() < 12,
    "twelve live segments carried in": lambda x: (
        len(_slots(x)) == 12 and all(x.seg_bal_pp_init(k) > 0.0 for k in _slots(x))),
    "a ladder of empty segments": lambda x: (
        x.index_alloc_rate() == 0.0
        and all(x.seg_bal_pp_init(k) == 0.0 for k in _slots(x))),
    "the segment maturing at t = 0 holding a balance": lambda x: (
        x.duration_mth_init() >= 12 and x.seg_bal_pp_init(12) > 0.0),
    "deductions carried on a segment": lambda x: any(
        x.seg_ded_cum_pp_init(k) > 0.0 for k in _slots(x)),
    "draws carried on a segment": lambda x: any(
        x.seg_wd_cum_pp_init(k) > 0.0 for k in _slots(x)),
    "an annual premium at t = 0": lambda x: (
        x.is_annual_premium() and x.premium_pp(0) > 0.0),
    "a monthly premium at t = 0": lambda x: (
        x.is_monthly_premium() and x.premium_pp(0) > 0.0),
    "a withdrawal at t = 0": lambda x: x.wd_pp(0) > 0.0,
    "a loan drawn at t = 0": lambda x: x.loan_new_pp(0) > 0.0,
    "the surrender charge's first month without, at t = 0": lambda x: (
        x.has_surr_charge() and _surr_charge_raw(x, 0) <= 0.0 < _surr_charge_raw(x, 0)
        + x.surr_charge_rate_max() / (12 * x.surr_charge_runoff_years())),
    "the lapse shock year's last month at t = 0": lambda x: (
        x.lapse_rate_sc_mult(0) != 1.0 and x.duration_mth(0) % 12 == 11),
    "the guarantee failing at t = 0 on the accumulator carried in": lambda x: (
        x.cum_prem_net_init() != 0.0 and x.policy_year(0) <= x.nlg_period_years()
        and x.cum_prem_net_pp(0) < x.cum_mnlp_pp(0)),
    "the guarantee holding at t = 0 on the accumulator carried in": lambda x: (
        x.cum_prem_net_init() != 0.0 and x.nlg_in_effect(0)),
    "the guarantee's expiry at t = 0": lambda x: (
        x.policy_year(0) == x.nlg_period_years() + 1 and x.duration_mth(0) % 12 == 0),
    "the guarantee's expiry shock at t = 0": lambda x: x.nlg_expiry_shock(0),
    "a loan carried in, its collateral apart from it": lambda x: (
        x.loan_bal_init() > 0.0 and x.lca_pp_init() != x.loan_bal_init()),
    "the shortfall test at t = 0 failing on the loan carried in": lambda x: (
        x.loan_bal_init() > 0.0 and x.is_shortfall(0)
        and x.av_pp_at(0, _code(x, "BEF_FEE")) - x.surr_charge_pp(0)
        >= x.mth_deduction_pp(0)),
    "the shortfall test at t = 0 netting the loan, which its collateral would pass": (
        lambda x: x.loan_bal_init() != x.lca_pp_init() and x.is_shortfall(0)
        and x.av_pp_at(0, _code(x, "BEF_FEE")) - x.surr_charge_pp(0) - x.lca_pp_init()
        >= x.mth_deduction_pp(0)),
    "the fixed account entering t = 0 below 0, the account value above": lambda x: (
        x.fa_pp_init() < 0.0 < x.av_pp_init()),
    "the account value entering t = 0 below 0": lambda x: x.av_pp_init() < 0.0,
    "the loan above the cash value at t = 0": lambda x: (
        x.loan_bal_pp(0) > x.csv_pp(0)),
    "the MEC latch carried in where S's test passes at t = 0": lambda x: (
        x.is_mec_init() and not _seven_pay_failed(x, 0)),
    "the 7-pay test failing at t = 0 with no latch carried in": lambda x: (
        not x.is_mec_init() and _seven_pay_failed(x, 0)),
    "a segment carried in on a rounding about zero": lambda x: any(
        _rounds(x.seg_bal_pp_init(k)) for k in _slots(x)),
    "the pool on a rounding about zero at t = 0": lambda x: (
        _rounds(x.seg_bal_active_pp(0))),
    "the face cut to nothing at t = 0": lambda x: (
        x.sum_assured_init() > 0.0 == x.sum_assured_at(0)
        and x.face_reduction_pp(0) == x.sum_assured_init()),
    "charges ceasing at t = 0": lambda x: (
        x.age(0) == x.charges_cease_age and x.duration_mth(0) % 12 == 0),
}
ON_THE_ROW = {
    "survivors carried into proj_len()": lambda x: x.pols_if(x.proj_len()) > 0.0,
}
IN_FRAME = {
    "an annual premium": lambda x, t: x.is_annual_premium() and x.premium_pp(t) > 0.0,
    "a monthly premium": lambda x, t: (
        x.is_monthly_premium() and not x.is_single_premium() and x.premium_pp(t) > 0.0),
    "the single premium capped at its guideline single premium": lambda x, t: (
        x.is_single_premium() and x.premium_pp(t) > 0.0
        and x.premium_pp_ann() > x.gsp()),
    "the single premium below its guideline single premium": lambda x, t: (
        x.is_single_premium() and 0.0 < x.premium_pp(t) == x.premium_pp_ann()),
    "the guideline cap cutting a target premium": lambda x, t: (
        x.is_target_premium() and x.duration_mth(t) % 12 == 0
        and x.premium_pp(t) < x.premium_pp_ann() * x.prem_persistency(t)),
    "a withdrawal and its fee": lambda x, t: x.wd_pp(t) > 0.0 and x.wd_fee_pp(t) > 0.0,
    "a loan drawn": lambda x, t: x.loan_new_pp(t) > 0.0,
    "the corridor binding": lambda x, t: _corridor_raw(x, t) > _option(x, t),
    "the net amount at risk floored": lambda x, t: _naar_raw(x, t) < 0.0,
    "the lapse cap binding": lambda x, t: (
        _lapse_raw(x, t) > x.lapse_rate_cap and x.pols_lapse(t) > 0.0
        and not x.nlg_expiry_shock(t)),
    "the lapse shock year": lambda x, t: x.lapse_rate_sc_mult(t) != 1.0,
    "lapses the guarantee suppresses": lambda x, t: (
        x.nlg_in_effect(t) and x.ncsv_pp(t) <= 0.0),
    "the guarantee's expiry shock": lambda x, t: x.nlg_expiry_shock(t),
    "the shortfall test failing": lambda x, t: x.is_shortfall(t),
    "the fixed account entering a month below 0": lambda x, t: (
        x.fa_pp_at(t, _code(x, "BEF_PREM")) < 0.0),
    "the account value entering a month below 0": lambda x, t: (
        x.av_pp_at(t, _code(x, "BEF_PREM")) < 0.0),
    "a draw on the segments": lambda x, t: x.draw_from_seg_pp(t) > 0.0,
    "a deduction on the segments": lambda x, t: x.mth_deduction_from_seg_pp(t) > 0.0,
    "a segment's index credit": lambda x, t: x.index_credit_pp(t) > 0.0,
    "the collateral credited at its second rate": lambda x, t: (
        x.lca_pp(t) > 0.0 and x.policy_year(t) > x.loan_credit_step_year),
    "the per-unit charge at its second rate": lambda x, t: (
        x.policy_year(t) > x.expense_unit_step_year and x.maint_fee_pp(t) > 0.0
        and x.expense_unit_mth_at(t) == x.expense_unit_mth_2),
    "charges ceased in the frame": lambda x, t: (
        x.age(t) >= x.charges_cease_age and x.av_pp(t) != 0.0),
    "the lapse table read past its last year": lambda x, t: (
        x.policy_year(t) > x.data.lapse_last_year()),
    "the MEC latch holding where S's test passes": lambda x, t: (
        x.is_mec(t) and not _seven_pay_failed(x, t)),
    "a face of nothing in force": lambda x, t: (
        x.sum_assured_at(t) == 0.0 and x.pols_if(t) > 0.0),
}


class _BoundSides:
    """Which side of each ``min`` and ``max`` in a model's ``Projection`` wins, by case.

    Every bound binds, with an effect, on a row the default run compares with S cell by
    cell, and the core-reach test checks each by the values it bounds, never by the
    bounded output (USLIB-SEC-PLAN.md §7.6, *Record — M4*, *Every bound binds*, precised
    at M9).  So, while a splice case is swept and compared, ``builtins.min`` and ``max``
    are wrapped (:meth:`watch`): a call made from one of the model's formulas with two
    arguments or more, not all equal, records each argument equal to its result as a side
    that won, ``(cell, call, i)``, the cell, the call's text with its comments dropped and
    its spaces collapsed, and the argument's position.  Every other call passes straight
    through.  The sides are the formulas' own calls, found in their source
    (:attr:`sides`), but those in the message a ``raise`` builds, which bound nothing; a
    call is told apart by its position in its formula's code, which Python gives from
    3.11, and before it :meth:`watch` records nothing.  It is ``VA_US_SEC``'s module's
    record, as that module keeps it.  The engine cells (:data:`ENGINE`) are left out: kept
    for ``IUL_US_S``'s worked example, no projection cell calls them (R14), so no row binds
    their bounds, which :func:`seg_credit_rate`'s calls hold in the projection.
    """

    def __init__(self, model):
        self.codes = {cells.formula.func.__code__: name
                      for name, cells in model.Projection.cells.items()}
        self.sites, self.positions = {}, {}
        for name, cells in model.Projection.cells.items():
            if name in ENGINE:
                continue
            source = cells.formula.source
            fn = ast.parse(source).body[0]
            messages = {id(node) for raised in ast.walk(fn) if isinstance(raised, ast.Raise)
                        for node in ast.walk(raised)}
            for node in ast.walk(fn):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                        and node.func.id in ("min", "max") and len(node.args) > 1
                        and id(node) not in messages):
                    text = re.sub(r"#[^\n]*", "", ast.get_source_segment(source, node))
                    self.sites[name, node.lineno - fn.lineno, node.col_offset] = (
                        name, " ".join(text.split()), len(node.args))
        named = collections.Counter(site[:2] for site in self.sites.values())
        twice = [site for site, n in named.items() if n > 1]
        assert not twice, f"a cell calls the same min or max twice: {twice}"
        self.sides = {(name, call, i) for name, call, n in self.sites.values()
                      for i in range(n)}

    def _wrap(self, builtin, won):
        def call(*args, **kwargs):
            result = builtin(*args, **kwargs)
            frame = sys._getframe(1)
            code = frame.f_code
            if code in self.codes and len(args) > 1 and not kwargs:
                if code not in self.positions:
                    self.positions[code] = list(code.co_positions())
                line, _, col, _ = self.positions[code][frame.f_lasti // 2]
                site = self.sites.get((self.codes[code], line - code.co_firstlineno, col))
                try:
                    if site and any(a != args[0] for a in args[1:]):
                        won.update((*site[:2], i) for i, a in enumerate(args)
                                   if a == result)
                except (TypeError, ValueError):     # an array has no one side: not a bound
                    pass
            return result
        return call

    @contextlib.contextmanager
    def watch(self):
        """Wrap the two builtins while the block runs, yielding the sides that won."""
        won = set()
        if sys.version_info < (3, 11):
            yield won
            return
        saved = builtins.min, builtins.max
        builtins.min, builtins.max = self._wrap(saved[0], won), self._wrap(saved[1], won)
        try:
            yield won
        finally:
            builtins.min, builtins.max = saved


# The sides of a min or max no core row of the main splice binds, each with the test that
# binds it, compared with S cell by cell, which asserts that the side wins there
# (_BoundSides): the index cap and the dynamic lapse multiplier's floor, which IUL_US_S
# ships idle, its index rising at a level 6.4% a year under a cap of 10% and the
# multiplier's raw value 1 in every month, on the second splice's core under the
# guaranteed cap of 2% and a floor of 1.2; the index floor and the multiplier's cap, which
# one pair of models binds no more than one side of each, on the index path overridden in
# both models; the cap on mortality, on a point made to pass it; the corridor, mortality and
# COI tables' clamps at their ends, on tables cut shorter than the cover, the shipped ones
# reaching past every age and year in cover.  The core-reach test holds the core to the
# rest: a side named here that a core row binds fails it, as does a side named nowhere
# that none binds.
BOUND_ELSEWHERE = {
    ("seg_credit_rate", "min(seg_index_cap(t), index_par * seg_return(t))", 0):
        "test_the_idle_core_reaches_each_bound",
    ("lapse_rate_dyn_mult", "max(lapse_dyn_floor, raw)", 0):
        "test_the_idle_core_reaches_each_bound",
    ("seg_credit_rate",
     "max(index_floor, min(seg_index_cap(t), index_par * seg_return(t)))", 0):
        "test_the_index_path_is_overridden_alike_in_both_models",
    ("lapse_rate_dyn_mult", "min(lapse_dyn_cap, max(lapse_dyn_floor, raw))", 0):
        "test_the_index_path_is_overridden_alike_in_both_models",
    ("mort_rate", "min(q, 1.0)", 1):
        "test_an_annual_mortality_past_1_is_capped_in_both_models",
    ("corridor_factor_at", "min(max(a, data.corridor_age_first()), last)", 1):
        "test_a_table_shorter_than_the_cover_is_read_at_its_ends_in_both_models",
    ("corridor_factor_at", "max(a, data.corridor_age_first())", 1):
        "test_a_table_shorter_than_the_cover_is_read_at_its_ends_in_both_models",
    ("mort_rate_base_at", "min(max(a, data.mort_age_first()), last)", 1):
        "test_a_table_shorter_than_the_cover_is_read_at_its_ends_in_both_models",
    ("mort_rate_base_at", "max(a, data.mort_age_first())", 1):
        "test_a_table_shorter_than_the_cover_is_read_at_its_ends_in_both_models",
    ("coi_rate_guar_py", "min(y, last)", 1):
        "test_a_table_shorter_than_the_cover_is_read_at_its_ends_in_both_models",
}
# The sides no row compared with S can bind, each with its premise, which a probe of every
# month of S's points and the variants, from issue, under each splice's References
# confirms, S projecting every month either splice compares: the face can never fall
# below 0, since the cut a withdrawal makes in it is the min of the withdrawal and the
# face left; a withdrawal is never below its fee, since proj_len() refuses one above 0
# and below the fee, and one of 0 takes no fee; the guideline cap's room is never below
# 0, since the premiums paid never pass the guideline limit, which the cap itself holds
# them to, and the limit, the max of the GSP and the GLP times the policy year, never
# falls; the pool a draw reaches is never below 0: a draw and a deduction take at most
# what the pool holds, pro rata, so a segment closes below 0 only on a rounding about
# zero, -1.1e-16 on variant 16 from its month 187, where no draw reaches the pool, and
# under either set the least pool a draw reaches, in any month of any point, is 0.0; and
# the guarantee's period to age 65 is read only at issue ages 46 to 60, where it is 5
# years or more.
IDLE_SIDES = {
    ("sum_assured_at", "max(0.0, opening - face_reduction_pp(t))", 0):
        "the cut is min(wd_pp(t), opening), never more than the face left",
    ("claim_pp", "max(0.0, wd_pp(t) - wd_fee_pp(t))", 0):
        "proj_len() refuses 0 < wd_pp < wd_fee, and no withdrawal takes no fee",
    ("premium_pp", "max(0.0, gpt_limit(t) - paid)", 0):
        "the premiums paid never pass the guideline limit, which never falls",
    ("draw_from_seg_pp", "max(0.0, seg_bal_active_pp(t))", 0):
        "the least pool a draw reaches is 0.0, on every point under either set",
    ("nlg_period_years", "max(0, 65 - x)", 0):
        "read only at issue ages 46 to 60, where 65 - x is 5 or more",
}


def _sides_bound_by(test):
    """The sides :data:`BOUND_ELSEWHERE` says ``test`` binds."""
    return {side for side, name in BOUND_ELSEWHERE.items() if name == test}


def _branches(x):
    """The names in :data:`AT_VALUATION`, :data:`ON_THE_ROW` and :data:`IN_FRAME` of ``x``.

    :data:`AT_VALUATION` asks about the state at the valuation date, which only a row in
    force holds; :data:`ON_THE_ROW` about the frame's end; :data:`IN_FRAME` about the
    frame on the books, which a future row has too, and which alone has the single premium
    of new business.
    """
    reached = {what for what, holds in ON_THE_ROW.items() if holds(x)}
    if x.duration_mth_init() > 0:
        reached |= {what for what, holds in AT_VALUATION.items() if holds(x)}
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
        record = {"negative": [], "early": [], "ahead": [], "unjudged": [],
                  "defaults": [], "followed": 0, "edges": 0, "raised": _raised(err)}
    records[case] = record
    return record


def _settle(records, case, model, key):
    """Record what the tests after the splice need of a row, and release it.

    ``case`` is the row's (row_kind, S point, source_mth) and ``key`` its registry key in
    ``model``, the splice's SEC model.  A T2 or T3 case calls this once it has compared
    the row, whatever the comparison found, so the row is released either way.  To the
    scan's record it adds the row's :func:`_branches`, what :func:`_carry` reads at
    ``t = proj_len()``, :func:`_least_live` and, last, so that its key ranges see every
    read the others made, :func:`_outside_cover_faults`.  A row no case has scanned is
    scanned here first.
    """
    try:
        proj = projection(model, key)
        record = records.get(case) or _scanned(records, case, proj)
        record.update(branches=set(), carry=None, guard=[], least=([], False))
        if record["raised"] is None:
            record["branches"] = _branches(proj)
            record["carry"] = _carry(proj)
            record["least"] = _least_live(proj, _case_id(*case))
            record["guard"] = _outside_cover_faults(proj, _case_id(*case))
    except Exception as err:                    # recorded, and reported by each test
        record = records.setdefault(case, {"negative": [], "early": [], "ahead": [],
                                           "unjudged": [], "defaults": [], "followed": 0,
                                           "edges": 0})
        record.update(branches=set(), carry=None, guard=[], least=([], False),
                      raised=_raised(err))
    finally:
        _release(model, key)
    records[case] = record
    return record


def _record_of(spliced, records, case, bounds):
    """The record of ``case``, from the case that compared its row or, failing it, now.

    A row no case has recorded is scanned and settled here (:func:`_settle`), the sides of
    the bounds its scan binds kept, as a case keeps those of its scan and comparison, by
    ``bounds``, the splice's :class:`_BoundSides`.
    """
    if case not in records or "guard" not in records[case]:
        sec = spliced[1]
        with bounds.watch() as won:
            _settle(records, case, sec, _row_key(sec, *case))
        records[case].setdefault("bounds", won)
    return records[case]


def _compare_case(spliced, records, bounds, case):
    """Scan the row of ``case``, compare it with its S point, then record and release it.

    The rules scan first (:func:`_scanned`), then the comparison of T2, T3 or a variant's
    twin (:func:`_continues_s`), each with its exemptions and its ``arg_map``, the sides of
    each ``min`` and ``max`` both bind kept (:class:`_BoundSides`), and last the records
    the tests after the comparisons read (:func:`_settle`), with what S carries into the
    month after the row's frame (:func:`_s_end`), read while its S point is held swept
    (:func:`_swept`).  Returns what the comparison found, and the row's frames, for the
    case's own assertions.
    """
    s, sec = spliced
    kind, s_point, month = case
    key = _row_key(sec, *case)
    s_end = None
    exempt, arg_map = {"twin": (VARIANT_EXEMPT, _issued_later),
                       "derived": (SPLICE_EXEMPT,
                                   _carried_segments(month, s.Projection.seg_term_mth)),
                       "future": (FUTURE_EXEMPT, _issued_later)}[kind]
    try:
        with bounds.watch() as won:
            sec_proj = projection(sec, key)
            _scanned(records, case, sec_proj)["bounds"] = won
            s_proj = _swept(s, s_point)
            found = _continues_s(s_proj, sec_proj, month, exempt, arg_map)
            s_end = _s_end(s_proj, sec_proj.proj_len() + month)
            frames = {report: sec_proj.cells[report]() for report in REPORTS}
            facts = {"pols_new_biz": [sec_proj.pols_new_biz(t)
                                      for t in range(sec_proj.proj_len())],
                     "policy_count": sec_proj.policy_count(),
                     "single": sec_proj.is_single_premium(),
                     "premium_pp_ann": sec_proj.premium_pp_ann(),
                     "gsp": sec_proj.gsp(),
                     "early": {name: sorted(t for t in sec_proj.cells[name].keys()
                                            if t < sec_proj.t_entry())
                               for name in DECREMENT_RATES},
                     "keys": {name: sorted(sec_proj.cells[name].keys())
                              for name in (*KEYED_BY_YEAR, *KEYED_BY_AGE)},
                     "age_at_entry": sec_proj.age_at_entry(),
                     "premiums": [sec_proj.premium_pp(t)
                                  for t in range(sec_proj.proj_len())]}
    finally:
        _settle(records, case, sec, key)
        records[case]["s_end"] = s_end
    return found, frames, facts


def _s_end(s_proj, s_month):
    """What S point ``s_proj`` carries into its month ``s_month``, the month after a row's
    frame on S's clock, for the end-of-projection test: the count, the account value in
    force at its opening timing, and the verdicts of the three checks this model states as
    S does."""
    return (s_proj.pols_if(s_month), s_proj.av_at(s_month, _code(s_proj, "BEF_PREM")),
            tuple(s_proj.cells[check]() for check in CHECKS[:3]))


def _every_state_months(sp):
    """The months S point ``sp`` is restated at by the every-state test.

    By default the edges of its windows (USLIB-SEC-PLAN.md §5.2, T5): every month of its
    first policy year after S's own start, each anniversary and the month before it, where
    the withdrawals' and the loans' first years, the surrender charge, the guarantee and
    the 7-pay years open and close, and the months either side of each change in a state
    a rule of ``Data`` or ``proj_len()`` reads: the fixed account's and the account value's
    sign entering a month, a loan, a face of nothing, the guarantee's test, the 7-pay test,
    and a segment or the pool closing on a rounding about zero; and the last month of its
    frame.  With ``USLIB_SEC_FULL=1``, every month of its frame.
    """
    n = sp.proj_len()
    if SEC_FULL:
        return list(range(1, n))
    bef_prem = _code(sp, "BEF_PREM")
    states = [(sp.fa_pp_at(d, bef_prem) < 0.0, sp.av_pp_at(d, bef_prem) < 0.0,
               sp.loan_bal_pp(d) > 0.0, sp.sum_assured_at(d) == 0.0,
               sp.nlg_in_effect(d), bool(sp.is_mec(d)),
               any(_rounds(sp.seg_bal_pp(d, m))
                   for m in range(max(0, d - sp.seg_term_mth + 1), d + 1)),
               _rounds(sp.seg_bal_active_pp(d)))
              for d in range(n)]
    months = {*range(1, min(12, n)), n - 1}
    for d in range(1, n):
        if d % 12 in (0, 11):
            months.add(d)
        if states[d] != states[d - 1]:
            months |= {d - 1, d, d + 1}
    return sorted(m for m in months if 1 <= m < n)


# What the every-state test must have met among the states it restates, each by the raw
# value S carries into the month, so that a rule of Data that refuses one, or a probe that
# never reached one, fails: the exhausted states IUL_US_S carries by design, the fixed
# account and the account value below 0, as point 5's from 373 and 578 under the splice's
# References; the accumulator below 0, its loans and withdrawals past its premiums; a loan
# with its collateral; a face of nothing, which variant 18's withdrawals reach at 567; a
# segment and the pool closing on roundings about zero; and the MEC latch.
STATES_MET = {
    "a fixed account below -0.01": lambda row: row["fa_pp_init"] < -0.01,
    "an account value below -0.01": lambda row: row["av_pp_init"] < -0.01,
    "a no-lapse accumulator below 0": lambda row: row["cum_prem_net_init"] < 0.0,
    "a loan and its collateral": lambda row: row["loan_bal_init"] > 0.0,
    "a face of nothing in force": lambda row: row["sum_assured_init"] == 0.0,
    "the MEC latch": lambda row: row["is_mec_init"] == 1,
}
LADDER_MET = {
    "a segment closing on a rounding about zero": lambda bal: _rounds(bal),
}


def _first_latched(table, policy_id):
    """The first month a derived row of S's ``policy_id`` opens with the MEC latch."""
    rows = table[(table["row_kind"] == "derived")
                 & (table["source_policy_id"] == policy_id)]
    latched = rows.loc[rows["is_mec_init"] == 1, "duration_mth"]
    return int(latched.min()) if len(latched) else None


# What the every-state test must meet of the restated rows as a whole, under a set of its
# own (EVERY_STATE): a ladder of as many slots as a segment term other than the twelve
# months IUL_US_S ships, which proj_len() asks for; and variant 21's 7-pay test failing
# first in policy year 7, the window's last, its rows carrying no latch to month 72 and the
# latch from month 73, which Data's 7-pay rule decides by the year.
FRAMES_MET = {
    "a ladder of six slots, the segment term's": lambda table, ladder: (
        ladder.groupby("point_id").size().max() == 6),
    "the latch carried in from policy year 7 alone": lambda table, ladder: (
        _first_latched(table, "IUL-900021") == 73),
}


def _refused_in_force(root, refs, variants, points=None):
    """What ``Data`` and ``proj_len()`` refuse of every state S reaches, restated in force.

    S's points, with ``variants`` and ``refs``, or ``points`` of them where given, each
    restated by the generator at each month of :func:`_every_state_months`, one S point
    at a time, into one table of every
    point's twin and a derived row at each state, and one segment ladder for them
    (:func:`_generated`).  ``IUL_US_S`` lapses no policy for insufficiency, so a policy is
    in force to restate in every month of its frame.  A model read with ``refs`` set first
    reads both, through ``Data``, and then asks every row for its frame, releasing each,
    collecting every 500.  Returns the number of states, each refusal, the line naming it,
    ``Data``'s or each row's ``proj_len()``'s, and what of :data:`STATES_MET`,
    :data:`LADDER_MET` and :data:`FRAMES_MET` the restated rows hold.
    """
    folder = _generated(root, refs, variants, restate=_every_state_months, points=points)
    table = pd.read_csv(folder.parent / TABLE)
    ladder = pd.read_csv(folder.parent / LADDER)
    derived = table[table["row_kind"] == "derived"]
    met = {what for what, holds in STATES_MET.items()
           if any(holds(row) for row in derived.to_dict("records"))}
    met |= {what for what, holds in LADDER_MET.items()
            if any(holds(bal) for bal in ladder["seg_bal_pp_init"])}
    met |= {what for what, holds in FRAMES_MET.items() if holds(derived, ladder)}
    model = _read(folder, "every", refs)
    try:
        try:
            read = model.Data.model_point_table()
            model.Data.inforce_segments()
        except Exception as err:                # reported, with the rows' states
            return len(derived), [f"Data: {_raised(err)}"], met
        assert len(read) == len(table)
        refused = []
        for i, key in enumerate(point_keys(model)):
            try:
                projection(model, key).proj_len()
            except Exception as err:            # reported, so every row is asked
                refused.append(_raised(err))
            _release(model, key, collect=i % 500 == 499)
        return len(derived), refused, met
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
        "s_point, case",
        [_held(case, case[1], CORE_SPLICES, _case_id(*case))
         for case in SPLICES + IN_FORCE_TWINS], scope="class")
    def test_an_in_force_point_continues_its_s_projection(self, spliced, splice_records,
                                                          splice_bounds, s_point, case):
        """Opened with S's state at month d, the point is S from d on, in every cell of S's.

        This is the test that says the opening state is complete: a state column the SEC
        row did not carry, or carried from the wrong instant, or a segment of the ladder
        read from the wrong slot, would make SEC part from S here, and nowhere else,
        because on a point issued at ``t = 0`` the two clocks coincide and the opening
        state is zero.  The fixed account and the collateral open from their own columns,
        apart from the account value and the loan, which open from S's; the face, the
        premiums paid, the no-lapse accumulator and the MEC latch from theirs; and each live
        segment from its row of the ladder, its balance, its deductions and draws, its
        start level and its cap, so that each segment carried in matures with S's credit.
        For the same reason it is the test that catches a policy month passed as ``t``
        (R1a): the rows valued mid-year put the segments' maturities, the anniversary
        premium and the policy-year steps off the valuation years.  The frame comparisons
        read SEC row ``t`` against S row ``t + d`` in every column of the four reports both
        models hold but ``result_seg``'s ``index_level``, which runs on the valuation clock,
        and fail frames that end apart.  The cell comparison then evaluates every cell of
        S's but :data:`SPLICE_EXEMPT`, at every argument S cached inside its own frame from
        month ``d`` on, moved onto SEC's clock: the accounts at every timing, the segment
        cells at every policy month of creation, the loan, the counts, the four checks'
        verdicts and the engine cells; and the MEC latch against S's 7-pay test failed in
        any month before (:func:`_latch_faults`).  An S cell this model lacked would fail
        it.

        Every value is held to 1e-9 relative with no absolute floor, because near the end
        of a long frame the counts fall far below 1e-7, where the floor would compare them
        against nothing, but S's roundings about zero, each held to its floor, and the two
        tests of zero that read one (:func:`_rounding_map`).  ``IUL_US_S`` has no residual
        cell, its checks being bools, so no compared cell is a residual rounding around 0
        that keeps the floor; this model's residual cells are held through the checks,
        which are compared as bools.

        The row is scanned for the rules test first (:func:`_scanned`), then compared, the
        sides of each ``min`` and ``max`` both bind kept (:class:`_BoundSides`), then
        recorded for the tests after this one and released (:func:`_settle`).
        """
        kind, s_point, month = case
        found, _, _ = _compare_case(spliced, splice_records, splice_bounds,
                                    (kind, s_point, month))
        assert found == []

    @pytest.mark.parametrize(
        "s_point, case",
        [_held(case, case[0], CORE_FUTURES, _case_id("future", case[0], -case[1]))
         for case in FUTURES], scope="class")
    def test_future_new_business_is_the_s_projection_k_months_on(self, spliced,
                                                                 splice_records,
                                                                 splice_bounds, s_point,
                                                                 case):
        """Issued k months after the valuation date, the point is S's projection k on.

        SEC rows ``k ..`` are S rows ``0 ..``, ending together at the end of the
        projection, in the four reports, and every cell of S's but :data:`FUTURE_EXEMPT`
        agrees at every argument S cached inside its own frame, moved ``k`` later, to 1e-9
        relative with no absolute floor but S's roundings about zero, ``pols_if_at`` at
        every timing but ``"BEF_NB"`` in the issue month (:func:`_issued_later`), and the
        MEC latch against S's 7-pay test failed so far.  An S cell this model lacked would
        fail it.  Before issue every column of the four reports is an exact zero but the
        index level, which runs on the valuation clock, and the policies arrive in month
        ``k`` as new business.  A single premium is collected once, in the issue month.

        The last assertions are R1 and D4's base rule made testable.  After every report,
        no decrement rate keyed by month has been evaluated at a month before issue, and no
        table keyed by a policy year has been read below year 1, no age-keyed table below
        the issue age.  A chain based at ``t == 0`` rather than at ``t_entry()``, or a rate
        evaluated before the month is asked whether it is in cover, still gives the right
        numbers.  This is the only test that sees the first, and the guard test sees the
        second too.

        The pre-issue rows are asserted present before they are asserted zero, in each of
        the reports: a frame that opened at issue would have none, its zeros would hold of
        nothing, and the comparisons with S, which start at issue, would not see it.  The
        row is scanned for the rules test first (:func:`_scanned`), the sides of each
        ``min`` and ``max`` its scan and comparison bind kept (:class:`_BoundSides`), and
        recorded and released once compared (:func:`_settle`).
        """
        s_point, k = case
        found, frames, facts = _compare_case(spliced, splice_records, splice_bounds,
                                             ("future", s_point, -k))
        assert found == []
        for report, frame in frames.items():
            assert list(frame.index[:k]) == list(range(k)), report
            before = frame.loc[:k - 1].drop(columns=["index_level"], errors="ignore")
            assert (before == 0).all().all(), report
        assert [t for t, n in enumerate(facts["pols_new_biz"]) if n] == [k]
        assert facts["pols_new_biz"][k] == facts["policy_count"] == 1.0
        assert not any(facts["early"].values()), f"rates before issue: {facts['early']}"
        for name, keys in facts["keys"].items():
            floor = facts["age_at_entry"] if name in KEYED_BY_AGE else 1
            assert keys and all(key >= floor for key in keys), f"{name} read at {keys[:5]}"
        if facts["single"]:
            assert facts["premiums"] == [min(facts["premium_pp_ann"], facts["gsp"])
                                         if t == k else 0.0
                                         for t in range(len(facts["premiums"]))]

    @pytest.mark.parametrize(
        "s_point, case",
        [_held(case, case[1], CORE_SPLICES, _case_id(*case)) for case in VARIANT_TWINS],
        scope="class")
    def test_a_variant_issued_at_the_valuation_date_is_its_s_point(self, spliced,
                                                                   splice_records,
                                                                   splice_bounds, s_point,
                                                                   case):
        """Issued at the valuation date, each variant is its S point in every cell of S's.

        T1 compares the twins of S's own new business with S cell by cell, in the
        conventions suite; the variants carry what those cannot, and an issue rule that only
        a variant takes at ``t = 0`` is reached nowhere else, a row issued later taking it
        at ``t = k`` and a row restated taking none (USLIB-SEC-PLAN.md §7.7, *Record —
        M9*, *Variants' twins*).  So the twin of each variant, which the generator puts in
        the splice's table beside the rows it derives, is compared as a row issued there
        is: frame by frame, the four reports, and cell by cell over every cell of S's but
        T1's exemptions, every one to 1e-9 relative with no absolute floor but S's
        roundings about zero, at every argument S cached but ``pols_if_at(0, "BEF_NB")``
        (:func:`_continues_s`, :func:`_issued_later`); and the MEC latch, which on variants
        8 to 11 and 17 holds where S's 7-pay test passes again, against S's test failed so
        far.  The row is scanned first, the sides of each ``min`` and ``max`` kept, and
        recorded and released once compared, as T2's rows are.
        """
        kind, s_point, month = case
        found, _, _ = _compare_case(spliced, splice_records, splice_bounds,
                                    (kind, s_point, month))
        assert found == []

    @pytest.mark.parametrize("grid", [pytest.param("core", id="core"),
                                      pytest.param("full", id="full", marks=FULL_ONLY)])
    def test_no_cell_is_called_before_the_valuation_date_or_reads_far_ahead(
            self, spliced, splice_records, splice_bounds, grid):
        """R1, its look-back and R2's look-ahead, on the rows T2 and T3 compare.

        Each is a rule of how the model computes, not of what, so no number shows a
        breach, and on a point issued at ``t = 0`` the two clocks coincide and hide it from
        T1 too.  The splice's rows are points in force at every month T2 names, the
        variants among them, and points issued later; and each is run on the books first,
        its four reports, its checks and every monthly cell at every month on the books,
        the segment cells at every segment live, as Phase 2's sweep
        (:func:`_sweep_on_the_books`), so that a read no report makes is judged too:

        * R1: no cell holds a negative argument, a month, a policy month of creation, an
          attained age, a policy year or a slot of the ladder.  modelx evaluates one without
          complaint, and a compiled cache raises ``IndexError`` below 0
          (USLIB-SEC-PLAN.md F4).
        * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
          ``t_entry()`` on read a month before it.  On a point issued later a chain based
          at ``t == 0``, as ``IUL_US_S``'s accounts, segments, loan, face, accumulators and
          count all were, reads the pre-issue zeros, so no number shows it and no argument
          goes negative.  This is the test that holds those bases at ``t_entry()`` (R1a).
          IUL has no improvement and reads no input a year back, so no look-back is
          admitted.
        * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month
          beyond ``t + 1``, as modelx's dependency graph records each cached call's
          precedents.  IUL reads nothing at the anniversary ahead, so R2's one exception
          has no use here.
        * The premise of the two scans: no cell without a ``t`` but the loops over the
          frame reads one keyed by ``t``, so a read through a cell keyed by an attained age,
          a policy year or a slot is a read of the month that asked, but
          :data:`FOLLOWED`'s, ``seg_new_pp(m)``, which reads the sweep of a segment's
          creation month, and which the scan follows to that read and judges against the
          month of the call that asked, on the core's rows at least once.
        * No projection call reads S's ``None`` default for an engine cell's cap or
          convention, which reads the cap at the literal month 0, and none reads
          ``seg_matured_value``: the projection passes each segment's cap and the convention
          explicitly (R14).

        Each row was scanned by the case that compared it, before the comparison
        (:func:`_scanned`), and a row no case has scanned is scanned here.  The core case
        covers the core's rows, the full case every other row of the full grid, with
        ``USLIB_SEC_FULL=1``.  The twins of S's own new business in the splice's table are
        no case's, and are left out: on them the clocks coincide, and T1 compares them with
        S cell by cell.
        """
        cases = [case for case in GRID if (case in CORE_GRID) == (grid == "core")]
        found = {"negative": [], "early": [], "ahead": [], "unjudged": [], "defaults": []}
        raised, unscanned, followed = [], [], 0
        for case in cases:
            record = _record_of(spliced, splice_records, case, splice_bounds)
            where = _case_id(*case)
            for rule, calls in found.items():
                calls += [f"{where}: {call}" for call in record[rule]]
            followed += record["followed"]
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
        assert not found["defaults"], (
            f"an engine cell read at S's None default: {found['defaults'][:10]}")
        assert followed, "no read through seg_new_pp was judged"

    def test_every_guarded_cell_holds_its_outside_cover_value_on_the_splice(
            self, spliced, splice_records, splice_bounds):
        """Outside cover each monthly cell holds its value on every row the splice compared.

        :data:`GUARD_SETS` say what each cell whose first parameter is ``t`` holds before
        issue and at ``t = proj_len()``, the month after the frame, which the roll-forwards
        read (:func:`_outside_cover_faults`).  On every row the splice compared, the core's
        or, with ``USLIB_SEC_FULL=1``, all of them, as each was recorded once compared
        (:func:`_settle`): there the survivors carried into ``t = proj_len()`` are not zero,
        the splice's A/E keeping lives to the end of every frame, and the future rows read
        policy years -2 to 0 before issue, the one without a surrender charge its lapse
        shock year 0 within a year of issue.

        That every monthly cell is in one set, and in one only, is asserted on the committed
        model (:func:`test_every_guarded_cell_holds_its_outside_cover_value`).
        """
        faults = []
        cases = _selected(GRID, CORE_GRID)
        for case in cases:
            record = _record_of(spliced, splice_records, case, splice_bounds)
            if record["raised"]:
                faults.append(f"{_case_id(*case)}: raised {record['raised']}")
            faults += record["guard"]
        assert cases and not faults, (
            f"{len(faults)} faults outside cover, first:\n  " + "\n  ".join(faults[:20]))

    def test_the_end_of_the_projection_carries_the_survivors(self, spliced, splice_records,
                                                             splice_bounds):
        """The survivors of the last month, and their account value, are carried, as in S.

        The projection ends at attained age 121, ``maturity_age``, while the contract is
        described as continuing in force, and S's roll-forwards read the month after the
        frame.  At the splice's A/E of 0.56 there are lives left at the end of every frame,
        2.3e-6 of a policy on S's point 1, so on every row the splice compared, the core's
        or, with ``USLIB_SEC_FULL=1``, all of them:

        * the count at ``t = proj_len()``, at every timing, is the survivors of the last
          month, exactly;
        * the account value per policy there is the last month's close, exactly, and the
          account value in force there the two multiplied;
        * both are S's at the same month, ``proj_len() + source_mth`` on S's clock,
          exactly on the twins, whose clock is S's and whose opening values are S's own,
          not read back from a CSV, and to 1e-9 on the rest: a row issued later reads the
          index path on the valuation clock, whose levels part from S's in their last
          bits, and so does its account value from its first segment's maturity on; and
          the four checks, which read them, decide as S's do, but ``check_margin``, whose
          identity this model states with the debt a surrender recovers, and which holds
          here on every row;
        * and nothing else happens there: no premium, death, lapse, withdrawal, loan,
          credit, claim or expense, and a net cash flow of 0.

        At least one row carries survivors.
        """
        cases = _selected(GRID, CORE_GRID)
        faults, survivors = [], []
        for case in cases:
            kind, s_point, month = case
            where = _case_id(*case)
            record = _record_of(spliced, splice_records, case, splice_bounds)
            carry = record["carry"]
            if carry is None:
                faults.append(f"{where}: raised {record['raised']}")
                continue
            exact = kind == "twin"
            s_end = record.get("s_end") or _s_end(_swept(spliced[0], s_point),
                                                  carry["L"] + month)
            theirs, s_checks = s_end[:2], s_end[2]
            mine = (carry["pols_if"], carry["av_at"])
            if carry["pols_if"] > 0.0:
                survivors.append(where)
            if carry["pols_if"] != carry["survivors"] or any(
                    count != carry["survivors"] for count in carry["timings"]):
                faults.append(f"{where}: the count carried is not the survivors: {carry}")
            if (carry["av_pp"] != carry["av_pp_last"]
                    or carry["av_at"] != carry["av_pp"] * carry["pols_if"]):
                faults.append(f"{where}: the account value carried is not the close: "
                              f"{carry}")
            close = pytest.approx(theirs, rel=1e-9, abs=ATOL) == mine
            if not (mine == theirs if exact and EXACT_SUMS else close):
                faults.append(f"{where}: {mine} carried, where S carries {theirs}")
            if carry["checks"][:3] != s_checks or carry["checks"][3] is not True:
                faults.append(f"{where}: the checks decide {carry['checks']}, S's "
                              f"{s_checks}")
            if any(flow != 0.0 for flow in carry["flows"]):
                faults.append(f"{where}: flows at t = proj_len(): {carry['flows']}")
        assert cases and not faults, faults[:10]
        assert survivors

    def test_the_lowest_balance_check_reads_the_segments_live_in_the_month(
            self, spliced, splice_records, splice_bounds):
        """``check_seg_bal_resid(t)`` is the least balance of the segments live in month t.

        The segments born in policy months ``duration_mth(t) - 11`` to ``duration_mth(t)``,
        or 0 where none is below 0, on every month of every row the splice compared, the
        core's or, with ``USLIB_SEC_FULL=1``, all of them (:func:`_least_live`).  The check
        it feeds passes either way while the segments hold 0 or more, so the check alone
        cannot tell a residual over the wrong segments, ``IUL_US_S``'s months of the frame
        among them, which on a row in force are segments long matured, at 0.  Variant 16's
        row at 188 carries in a segment closed on a rounding about zero, -1.1e-16, live in
        its months 0 and 1, which the residual must read, and some row meets one.
        """
        faults, met = [], []
        cases = _selected(GRID, CORE_GRID)
        for case in cases:
            record = _record_of(spliced, splice_records, case, splice_bounds)
            if record["raised"]:
                faults.append(f"{_case_id(*case)}: raised {record['raised']}")
            found, below = record["least"]
            faults += found
            if below:
                met.append(_case_id(*case))
        assert cases and not faults, faults[:10]
        assert met, "no row compared met a live segment below 0"

    @pytest.mark.skipif(not EXACT_SUMS, reason="a pool is S's bit for bit from Python "
                        "3.12, whose sum() of floats compensates")
    def test_the_tests_of_zero_read_a_rounding_about_zero_as_s_does(self, spliced):
        """``seg_count`` and ``seg_share`` keep ``IUL_US_S``'s tests of 0 (§7.7, M9).

        The comparisons hold neither where a segment or the pool is a rounding below
        :data:`FLOOR` (:func:`_rounding_map`), which are the very months a threshold other
        than S's 0 would read differently, so they are asserted here, on the twin of
        variant 15, issued at the valuation date, where both clocks and both index paths
        coincide and the pool is S's bit for bit.  In its month 15 the segment born in
        month 9 closes on a rounding of ``5.6e-17`` above 0, which ``seg_count`` counts,
        as S's does, where a test of ``1e-9`` would count none; in month 16 the pool is
        that segment alone, and ``seg_share`` gives it the whole draw, a share of 1.0, as
        S's does, where a pool test of ``1e-9`` would give it none.
        """
        s, sec = spliced
        sp = _swept(s, 15)
        key = _row_key(sec, "twin", 15, 0)
        try:
            x = projection(sec, key)
            assert 0.0 < sp.seg_bal_pp(15, 9) < FLOOR
            assert 0.0 < sp.seg_bal_active_pp(16) < FLOOR
            mine = (_seg(x, "seg_bal_pp", 15, 9), x.seg_count(15),
                    x.seg_bal_active_pp(16), _seg(x, "seg_share", 16, 9))
            theirs = (sp.seg_bal_pp(15, 9), sp.seg_count(15), sp.seg_bal_active_pp(16),
                      sp.seg_share(16, 9))
            assert mine == theirs and theirs[1] == 1 and theirs[3] == 1.0, (mine, theirs)
            assert sum(_seg(x, "seg_bal_pp", 15, m) > FLOOR for m in range(4, 16)) == 0
        finally:
            _release(sec, key)

    def test_the_core_grid_reaches_every_branch(self, spliced, splice_records,
                                                splice_bounds):
        """What the default run's T2 and T3 cases reach, which the full grid multiplies.

        The default run thins the splice to a core (the module docstring), and this test is
        what keeps the thinning from costing a branch.  The core was chosen by the lines of
        the model each row of the full grid runs, so that the core runs every one; and
        since a branch that differs only in the month it fires covers no line of its own,
        each event has a core row in its own month.  First, statically, over S's table with
        the variants, each property below holds of some core case: each premium type and
        mode, each sex and class, each death benefit option, each surrender charge schedule
        and none, nothing allocated and part of the fixed account allocated, withdrawals,
        loans, a variant issued at the valuation date as its twin, and each kind of
        valuation month, on the policy clock: the first month after issue, mid-year, the
        month before an anniversary, on an anniversary and the last covered month.  And of
        some core future case: issued within a year and more than two years on.  Each issue
        age, of some core case or core future case, either of which T2 or T3 compares with
        S from the age-keyed joins on.  And the issue month of each variant, on its twin or
        on a row issued later (:data:`VARIANT_TWINS`).

        Then, on the splice's model, of some core row, each of :data:`AT_VALUATION`,
        :data:`ON_THE_ROW` and :data:`IN_FRAME`, what no column of the table shows: each
        kind of valuation month the full grid has, every opening-state column in use among
        them, each on its raw value at ``t = 0``; survivors carried; and later in the frame
        each event, each floor and cap of S's by the raw value it bounds, never the bounded
        output, which equals the bound where the bound changes nothing too.

        Last, each bound by the values it compares: each side of every ``min`` and ``max``
        in ``Projection`` wins, the others not all equal to it, in some call the scan or
        the comparison of a core row makes (:class:`_BoundSides`), but those
        :data:`BOUND_ELSEWHERE` names, each with the test that binds it on rows of its own
        and asserts it there, and those :data:`IDLE_SIDES` names, with their premises; and
        no side either names wins on a core row.

        Each core row's branches were recorded by the case that compared it
        (:func:`_settle`), and a row no case has recorded is evaluated here.
        """
        s_table = _s_table_with_variants()
        schedules = _surr_charges_with_iul07(pd.read_csv(
            model_path(TWIN).parent / "surr_charge_table.csv"))["surr_charge_id"]
        classes = pd.read_csv(model_path(TWIN).parent / "class_factor_table.csv")[
            "rate_class"]
        end = spliced[0].Projection.maturity_age

        def at(p, column):
            return s_table.at[p, column]

        def month(p, d):
            return int(at(p, "duration_mth")) + d

        splices = {
            **{f"{pattern} premiums": (
                lambda k, p, d, x=pattern: at(p, "premium_type") == x)
               for pattern in ("LEVEL", "SINGLE", "TARGET")},
            **{f"mode {m}": (
                lambda k, p, d, m=m: at(p, "premium_mode") == m
                and at(p, "premium_type") != "SINGLE")
               for m in ("ANNUAL", "MONTHLY")},
            **{f"sex {x}": (lambda k, p, d, x=x: at(p, "sex") == x) for x in "MF"},
            **{f"class {c}": (lambda k, p, d, c=c: at(p, "rate_class") == c)
               for c in classes},
            **{f"option {o}": (lambda k, p, d, o=o: at(p, "db_option") == o)
               for o in "AB"},
            **{f"schedule {i}": (
                lambda k, p, d, i=i: bool(at(p, "has_surr_charge"))
                and at(p, "surr_charge_id") == i)
               for i in schedules},
            "no surrender charge": lambda k, p, d: not at(p, "has_surr_charge"),
            "nothing allocated": lambda k, p, d: at(p, "index_alloc_rate") == 0.0,
            "part of the fixed account allocated": lambda k, p, d: (
                0.0 < at(p, "index_alloc_rate") < 1.0),
            "withdrawals": lambda k, p, d: at(p, "wd_pp") > 0.0,
            "loans": lambda k, p, d: at(p, "loan_new_pp_ann") > 0.0,
            "a variant issued at the valuation date as its twin": lambda k, p, d: (
                k == "twin" and p in VARIANTS),
            "the first month after issue": lambda k, p, d: month(p, d) == 1,
            "mid-year": lambda k, p, d: month(p, d) % 12 not in (0, 11),
            "the month before an anniversary": lambda k, p, d: month(p, d) % 12 == 11,
            "on an anniversary": lambda k, p, d: month(p, d) > 0 and month(p, d) % 12 == 0,
            "the last covered month": lambda k, p, d: (
                month(p, d) == 12 * (end - int(at(p, "age_at_entry"))) - 1),
        }
        futures = {
            "issued within a year": lambda p, k: k < 12,
            "issued more than two years on, as the committed future row": lambda p, k: (
                k > 24),
        }
        core = [case for case in CORE_SPLICES]
        missing = [what for what, holds in splices.items()
                   if not any(holds(*case) for case in core)]
        missing += [what for what, holds in futures.items()
                    if not any(holds(*case) for case in CORE_FUTURES)]
        ages = {at(p, "age_at_entry") for _, p, _ in core} | {
            at(p, "age_at_entry") for p, _ in CORE_FUTURES}
        missing += [f"issue age {a}" for a in (45, 50, 65) if a not in ages]
        issued = ({p for k, p, d in CORE_SPLICES if k == "twin"}
                  | {p for p, k in CORE_FUTURES})
        missing += [f"the issue month of variant {p}" for _, p, _ in VARIANT_TWINS
                    if p not in issued]
        assert not missing, f"no core case reaches: {missing}"

        reached, won, raised = set(), set(), []
        for case in CORE_GRID:
            record = _record_of(spliced, splice_records, case, splice_bounds)
            reached |= record["branches"]
            won |= record["bounds"]
            if record["raised"]:
                raised.append(f"{_case_id(*case)}: {record['raised']}")
        assert not raised, raised
        missing = [what for what in (*AT_VALUATION, *ON_THE_ROW, *IN_FRAME)
                   if what not in reached]
        assert not missing, f"no core row reaches: {missing}"
        sides = splice_bounds.sides
        named = set(IDLE_SIDES) | set(BOUND_ELSEWHERE)
        assert named <= sides, sorted(named - sides)
        assert not set(IDLE_SIDES) & set(BOUND_ELSEWHERE)
        if sys.version_info >= (3, 11):
            unbound = sorted(sides - won - named)
            assert not unbound, f"sides of a bound no core row binds: {unbound}"
            bound = sorted(named & won)
            assert not bound, f"sides named idle or bound elsewhere that bind here: {bound}"

    @pytest.mark.sec_full
    @pytest.mark.skipif(not SEC_FULL, reason="the block test runs with USLIB_SEC_FULL=1 "
                        "(USLIB-SEC-PLAN.md K6)")
    def test_the_points_sum_row_by_row_into_a_block(self, spliced):
        """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

        The twin of S point 4's variant 15, the point restated at month 16 and the point
        issued six months on from variant 11, summed as ``run_sec.py --block`` sums them,
        are indexed 0..917 and equal the S frames of variants 15 and 11, the first added to
        itself moved 16 months earlier and the second moved six months later, with no
        tolerance beyond 1e-9 relative.  A model whose frames sat on the policy clock would
        fail it, and would fail T2's frame-by-frame comparison too, so it runs with
        ``USLIB_SEC_FULL=1`` only (USLIB-SEC-PLAN.md K6, weighed at M13).
        """
        s, sec = spliced
        cases = (("twin", 15, 0), ("derived", 15, 16), ("future", 11, -6))
        keys = [_row_key(sec, *case) for case in cases]
        try:
            frames = [projection(sec, key).result_cf() for key in keys]
        finally:
            for key in keys:
                _release(sec, key)
        block = pd.concat(frames).groupby(level="t").sum()
        first = _swept(s, 15).result_cf()
        later = _swept(s, 11).result_cf()
        expected = pd.concat([first, first.set_axis(first.index - 16).loc[0:],
                              later.set_axis(later.index + 6)]).groupby(level=0).sum()
        assert list(block.index) == list(range(918))
        assert frame_mismatches(expected, block, atol=0.0) == []


# ---------------------------------------------------------------------------
# The second splice: the bounds IUL_US_S ships idle
#
# Two of IUL_US_S's bounds bind on no row at its shipped References or the splice's: the
# index cap of 10%, which the level path's return of 6.4% a year never meets, and the
# dynamic lapse multiplier's floor of 0.5, under a raw multiplier of 1 in every month,
# comp_rate_ann being cred_rate_ann.  A second pair of models, read with References of its
# own (IDLE_REFS), binds one side of each, with a core and a reach assertion of its own
# (USLIB-SEC-PLAN.md §7.11, Switches and bounds S ships idle): the guaranteed basis, whose
# cap of 2% binds every segment's credit, and a multiplier's floor of 1.2, which binds in
# every month, set strictly apart from the cap of 2.0 and the neutral 1.0.  The same
# References switch on the two switches IUL_US_S ships off, the guaranteed basis and the
# adjusted-beginning credit base, which half-weights a segment's deductions, so T1 runs
# under them on S's five twins: under the base a segment carried in reads its deductions
# from the ladder into its credit, which under the remaining balance they leave.  The other
# sides, the index floor and the multiplier's cap, take the index path overridden in both
# models (test_the_index_path_is_overridden_alike_in_both_models).
IDLE_REFS = {**SPLICED_REFS, "basis": "GUARANTEED", "lapse_dyn_floor": 1.2,
             "seg_credit_base_conv": "ADJ_BEGIN"}
IDLE_GRID = (("twin", 1, 0), ("twin", 2, 0), ("twin", 3, 0), ("twin", 4, 0), ("twin", 5, 0),
             ("derived", 1, 12), ("derived", 1, 60), ("derived", 4, 11),
             ("derived", 4, 65), ("derived", 5, 6), ("derived", 5, 12),
             ("future", 4, -13))
CORE_IDLE = {
    ("twin", 1, 0): "T1 under the guaranteed basis and the adjusted-beginning base",
    ("derived", 1, 60): "the segment maturing at t = 0 carried with its deductions, "
                        "half-weighted, at the guaranteed cap",
    ("derived", 4, 65): "twelve segments carried in, each credited at the cap",
    ("future", 4, -13): "both bounds from the issue month",
}


@pytest.fixture(scope="class")
def idle_spliced(tmp_path_factory):
    """S and SEC on the splice's inputs, with :data:`IDLE_REFS` set in both.

    S's five points, and the rows this run selects of :data:`IDLE_GRID`, the
    :data:`CORE_IDLE` or all of them (:func:`_splice`).  Scoped to its class, whose tests
    alone read it, and frozen once read, S swept a point at a time, as the main splice's
    fixture is.
    """
    splices = tuple(case for case in IDLE_GRID if case[0] != "future")
    futures = tuple((p, -k) for kind, p, k in IDLE_GRID if kind == "future")
    s, sec = _splice(tmp_path_factory.mktemp("idle"), "idle", IDLE_REFS, {}, splices,
                     futures, frozenset(CORE_IDLE))
    try:
        gc.collect()
        gc.freeze()
        yield s, sec
    finally:
        sec.close()
        s.close()
        gc.unfreeze()
        gc.collect()


@pytest.fixture(scope="class")
def idle_records():
    """What each row of the second splice was found to reach, by case."""
    return {}


@pytest.fixture(scope="class")
def idle_bounds(idle_spliced):
    """The record of the second splice's SEC model's ``min`` and ``max``
    (:class:`_BoundSides`)."""
    return _BoundSides(idle_spliced[1])


def _maturing_deductions(x, t):
    """The deductions charged to the segment maturing in month ``t``, over its term."""
    m = x.duration_mth(t) - x.seg_term_mth
    if t > x.t_entry():
        return _seg(x, "seg_ded_cum_pp", t - 1, m)
    return x.seg_ded_cum_pp_init(x.seg_term_mth)


def _idle_reach(x):
    """Which of the second splice's bounds and switches bind on row ``x``, by raw values.

    The index cap, where a maturing segment's return times the participation passes the
    cap it was created under, and it is credited; the multiplier's floor, where the raw
    multiplier is below it, the multiplier is the floor and policies lapse; and the
    adjusted-beginning base, where a segment credited carried deductions.
    """
    months = range(x.t_entry(), x.proj_len())
    credited = [t for t in months if x.index_credit_pp(t) > 0.0]
    return {
        "the index cap": any(x.index_par * x.seg_return(t) > x.seg_index_cap(t)
                             for t in credited),
        "the multiplier's floor": any(
            1 + x.lapse_dyn_slope * (x.comp_rate_ann(t) - x.cred_rate_ann(t))
            < x.lapse_dyn_floor == x.lapse_rate_dyn_mult(t) and x.pols_lapse(t) > 0.0
            for t in months),
        "deductions half-weighted": (
            x.seg_credit_base_conv == _code(x, "ADJ_BEGIN")
            and any(_maturing_deductions(x, t) > 0.0 for t in credited))}


class TestTheIdleBounds:
    """The second splice, where each bound IUL_US_S ships idle binds in both models."""

    @pytest.mark.parametrize(
        "kind, s_point, month",
        [_case(case, CORE_IDLE, _case_id(*case)) for case in IDLE_GRID])
    def test_a_bound_s_ships_idle_binds_in_both_models(self, idle_spliced, idle_records,
                                                       idle_bounds, kind, s_point, month):
        """With the index cap and the multiplier's floor binding, each row is S from d on.

        T1's comparison on S's five twins, T2's on the restated rows and T3's on the row
        issued 13 months on, each at 1e-9 relative with no absolute floor but S's roundings
        about zero, every cell of S's but T1's, T2's or T3's exemptions: a bound left out,
        or written in another order, or a segment carried in without its deductions, parts
        the two.  What each row binds is recorded, by the raw value each bound bounds
        (:func:`_idle_reach`) and by the sides of each ``min`` and ``max`` its comparison
        binds (:class:`_BoundSides`), and the row released.
        """
        s, sec = idle_spliced
        case = (kind, s_point, month)
        key = _row_key(sec, *case)
        exempt, arg_map = {"twin": (TWIN_EXEMPT, _issued_later),
                           "derived": (SPLICE_EXEMPT,
                                       _carried_segments(month, s.Projection.seg_term_mth)),
                           "future": (FUTURE_EXEMPT, _issued_later)}[kind]
        try:
            with idle_bounds.watch() as won:
                sec_proj = projection(sec, key)
                found = _continues_s(_swept(s, s_point), sec_proj, month, exempt, arg_map)
                idle_records[case] = {"reach": _idle_reach(sec_proj), "bounds": won}
            assert found == []
        finally:
            _release(sec, key)

    def test_the_idle_core_reaches_each_bound(self, idle_spliced, idle_records,
                                              idle_bounds):
        """Each idle bound binds with an effect on some row of the second splice's core.

        The index cap, where a maturing segment's raw return passes the cap it was created
        under and it is credited at the cap, the guaranteed 2%; the multiplier's floor,
        where its raw value is below 1.2, the multiplier is the floor and policies lapse;
        each by the raw value it bounds, never the bounded output, and by the side of its
        ``min`` or ``max`` that wins there, the two sides :data:`BOUND_ELSEWHERE` names this
        test for (:class:`_BoundSides`); and the adjusted-beginning base, on a segment
        credited with deductions charged to it, the core's row at 60 crediting the one it
        carries in at ``t = 0``.  A row no case has recorded is read here.
        """
        sec = idle_spliced[1]
        reached, won = set(), set()
        for case in CORE_IDLE:
            if case not in idle_records:
                key = _row_key(sec, *case)
                with idle_bounds.watch() as bounds:
                    idle_records[case] = {"reach": _idle_reach(projection(sec, key)),
                                          "bounds": bounds}
                _release(sec, key)
            record = idle_records[case]
            reached |= {bound for bound, binds in record["reach"].items() if binds}
            won |= record["bounds"]
        assert reached == {"the index cap", "the multiplier's floor",
                           "deductions half-weighted"}, reached
        mine = _sides_bound_by("test_the_idle_core_reaches_each_bound")
        assert len(mine) == 2
        if sys.version_info >= (3, 11):
            assert mine <= won, sorted(mine - won)


# ---------------------------------------------------------------------------
# The tests that read models of their own
#
# Each test below reads, and closes, the models it needs, and none asks for the
# committed model or S, the module's fixtures: so they run once the splices' models
# are closed and before those are first read, and none of the models they read sits in
# memory beside them (USLIB-SEC-PLAN.md §7.7, Record — M9, Memory).  The tests that
# read the committed fixtures follow them.


# ---------------------------------------------------------------------------
# Splices on References of their own


# Variant 21, S point 1 paying $15,000 a year, under a premium persistency of 1.12 a year
# where S ships 0.98: its premiums paid to date stay inside the 7-pay limit through policy
# year 6, 121,728 against 126,000, and pass it at its seventh anniversary, month 72,
# 151,335 against 147,000.  With a persistency below 1, as shipped, a policy that ever
# fails the test fails it in its first year, so the window's last year decides nothing.
MEC7_VARIANT = {21: (1, {"policy_id": "IUL-900021", "premium_pp_ann": 15000.0})}
# Each splice of its own, as (References, variants, the S points both models read, the
# rows): the segment term at 6 and at 24 months, where IUL_US_S ships 12, on S's points 1
# and 4, each restated where its ladder holds the term's slots and issued 13 months on,
# and S's point 4's twin; and variant 21's twin, its row restated at 72, the 7-pay test
# failing first in the valuation month, in policy year 7, with no latch carried in, and
# at 84, in policy year 8, the latch carried.
OWN_SPLICES = {
    "seg_term_mth 6": ({**SPLICED_REFS, "seg_term_mth": 6}, {}, (1, 4),
                       (("twin", 4, 0), ("derived", 1, 30), ("derived", 4, 65),
                        ("future", 4, -13))),
    "seg_term_mth 24": ({**SPLICED_REFS, "seg_term_mth": 24}, {}, (1, 4),
                        (("twin", 4, 0), ("derived", 1, 30), ("derived", 4, 65),
                         ("future", 4, -13))),
    "7-pay year 7": ({**SPLICED_REFS, "prem_persistency_rate": 1.12}, MEC7_VARIANT, (21,),
                     (("twin", 21, 0), ("derived", 21, 72), ("derived", 21, 84))),
}


def _own_reach(name, sec, s):
    """What the splice ``name`` must reach, by raw values, or the faults found."""
    faults = []
    if name.startswith("seg_term_mth"):
        term = sec.Projection.seg_term_mth
        table = sec.Data.model_point_table()
        held = dict(zip(table.index, sec.Data.inforce_segment_count()))
        for point_id in table.index[table["row_kind"] == "derived"]:
            want = min(term, int(table.at[point_id, "duration_mth"]))
            if held[point_id] != want:
                faults.append(f"point {point_id}: {held[point_id]} segments, not {want}")
        return faults
    sp = _swept(s, 21)
    first = next(t for t in range(sp.proj_len()) if sp.is_mec(t))
    if (first, sp.policy_year(first)) != (72, 7):
        faults.append(f"S's 7-pay test fails first at {first}")
    x = _row(sec, "twin", 21, 0)
    if [t for t in range(x.proj_len()) if x.is_mec(t)] != list(range(72, x.proj_len())):
        faults.append("the twin does not latch from month 72")
    x = _row(sec, "derived", 21, 72)
    if x.is_mec_init() or not x.is_mec(0):
        faults.append("the row at 72 does not fail the test at t = 0 on its own")
    x = _row(sec, "derived", 21, 84)
    if not (x.is_mec_init() and x.is_mec(0)) or x.policy_year(0) != 8:
        faults.append("the row at 84 does not carry the latch into policy year 8")
    return faults


@pytest.mark.parametrize("name", [
    pytest.param(name, marks=FULL_ONLY if name == "seg_term_mth 24" else ())
    for name in OWN_SPLICES])
def test_a_splice_on_references_of_its_own_continues_s(tmp_path, name):
    """On References no other splice sets, each row is S from its month on (T2, T3).

    Two kinds of Reference the main splice cannot set beside its own, in the sets of
    :data:`OWN_SPLICES`, each read in S and SEC, with the generator restating S's rows out
    of S under them, and each row compared with its S point, as T2, T3 and the variants'
    twins compare one (:func:`_continues_s`), every cell of S's but their exemptions:

    * the segment term moved from 12 months to 6, and to 24 with ``USLIB_SEC_FULL=1``:
      the ladder holds ``min(seg_term_mth, duration_mth)`` slots, which ``proj_len()``
      asks, every segment cell and the index credit read the Reference, not the twelve it
      ships at, and the comparison drops S's keys of the segments matured before the
      valuation date at the term the models read (:func:`_carried_segments`), which
      Phase 2's slot dimension is sized from (R15);
    * a premium persistency above 1, under which variant 21's 7-pay test fails first in
      policy year 7, the window's last: its twin latches from that month, its row
      restated there fails the test in the valuation month with no latch carried in, and
      its row in year 8 carries the latch, where ``IUL_US_S``'s flag no longer applies.

    Each splice's own reach is asserted by raw values (:func:`_own_reach`).
    """
    refs, variants, points, rows = OWN_SPLICES[name]
    splices = tuple(case for case in rows if case[0] != "future")
    futures = tuple((p, -k) for kind, p, k in rows if kind == "future")
    s, sec = _splice(tmp_path, "own", refs, variants, splices, futures, frozenset(rows),
                     points)
    try:
        assert all(getattr(m.Projection, ref) == value
                   for m in (s, sec) for ref, value in refs.items())
        found = {}
        term = s.Projection.seg_term_mth
        for case in rows:
            kind, s_point, month = case
            exempt, arg_map = {"twin": (VARIANT_EXEMPT, _issued_later),
                               "derived": (SPLICE_EXEMPT, _carried_segments(month, term)),
                               "future": (FUTURE_EXEMPT, _issued_later)}[kind]
            key = _row_key(sec, *case)
            lines = _continues_s(_swept(s, s_point), projection(sec, key), month, exempt,
                                 arg_map)
            if lines:
                found[case] = lines[:5]
            _release(sec, key)
        assert not found, found
        faults = _own_reach(name, sec, s)
        assert not faults, faults
    finally:
        sec.close()
        s.close()


# ---------------------------------------------------------------------------
# Every state S reaches, under each set of References on which they differ


EXHAUSTED = frozenset({"a fixed account below -0.01", "an account value below -0.01"})
# Each set of inputs the every-state test runs on, as (References, variants, what it must
# meet, the least number of states, the S points it restates, or None for all): the
# shipped References, which the committed table is generated under, on S's points and the
# variants; the main splice's, where point 5's fixed account and account value turn
# negative at 373 and 578 rather than 383 and 604; the second splice's, on S's five
# points, whose guaranteed basis exhausts points 2 and 3 too; and the two sets of the
# splices of their own, on their own points (OWN_SPLICES), on which the states S reaches
# differ in what Data and proj_len() decide by a Reference or a window: the segment term
# at 6 months, on S's points 1 and 4, whose ladders hold six slots, and the premium
# persistency of 1.12, on variant 21, whose 7-pay test fails first in policy year 7.
EVERY_STATE = {
    "shipped": ({}, VARIANTS, frozenset({*STATES_MET, *LADDER_MET}), 2000, None),
    "splice": (SPLICED_REFS, VARIANTS, frozenset({*STATES_MET, *LADDER_MET}), 2000, None),
    "idle": (IDLE_REFS, {}, EXHAUSTED, 500, None),
    "seg_term_mth 6": (*OWN_SPLICES["seg_term_mth 6"][:2],
                       frozenset({"a ladder of six slots, the segment term's"}), 100,
                       OWN_SPLICES["seg_term_mth 6"][2]),
    "7-pay year 7": (*OWN_SPLICES["7-pay year 7"][:2],
                     frozenset({"the latch carried in from policy year 7 alone"}), 30,
                     OWN_SPLICES["7-pay year 7"][2]),
}


@pytest.mark.parametrize("inputs", [
    pytest.param(inputs, id=inputs, marks=FULL_ONLY if inputs == "splice" else ())
    for inputs in EVERY_STATE])
def test_every_state_s_reaches_is_accepted_in_force(tmp_path, inputs):
    """Every state S reaches is a valid opening state, under each set of References (T5).

    ``Data``'s rules and ``proj_len()``'s hold an opening state to what a policy in force
    can hold, so they must accept each state ``IUL_US_S`` reaches: a rule exercised only
    on the rows the other tests choose could refuse a state S reaches elsewhere (D6).  The
    states S reaches differ with the References, so the test runs under each set the
    module projects on (:data:`EVERY_STATE`; USLIB-SEC-PLAN.md §5.2, T5, as precised at
    M9): the shipped References, which the committed table is generated under, the main
    splice's and the second splice's, and the References of the two splices of their own
    whose states differ in what ``Data`` and ``proj_len()`` decide, a segment term of 6
    months and a premium persistency of 1.12, on their own points.  Under each, every S
    point, with the variants where the set takes them, is restated in force by the
    generator, one S point at a time, at the edges of its windows, or with
    ``USLIB_SEC_FULL=1`` at every month of its frame (:func:`_every_state_months`), into
    one table and one segment ladder beside the twins:
    ``Data`` reads both, and no row's ``proj_len()`` refuses it
    (:func:`_refused_in_force`).  ``IUL_US_S`` lapses no policy for insufficiency, and
    carries an exhausted policy on, so this model accepts what it carries, and the test
    asserts it met each such state by its raw value (:data:`STATES_MET`): S point 5's fixed
    account and then its account value below 0, the accumulator below 0, a loan with its
    collateral, variant 18's face cut to nothing, the MEC latch, and segments closing on
    roundings about zero, which ``Data`` holds to ``-1e-8`` or more.  The second splice
    meets the exhausted accounts on S's points alone; the splices of their own meet ladders
    of six slots and a latch carried in from policy year 7 alone (:data:`FRAMES_MET`),
    which none of the other sets reaches.  The main splice's set runs with
    ``USLIB_SEC_FULL=1`` only (K6): the shipped set must meet every state the main
    splice's must, so the default run meets each of them all the same.
    """
    refs, variants, want, least, points = EVERY_STATE[inputs]
    n, refused, met = _refused_in_force(tmp_path / "every", refs, variants, points)
    assert n > least, n
    assert not refused, f"{len(refused)} refused, first: {refused[:5]}"
    assert want <= met, sorted(want - met)


# ---------------------------------------------------------------------------
# The index path, overridden alike in both models (K7)


def _s_stepped_index_level(t):
    """A stepped index path on S's own clock: up 3% a month for nine months, then down
    1.5% a month for nine, from S's own start."""
    n = duration_mth(t)                                              # noqa: F821
    up = (n // 18) * 9 + min(n % 18, 9)
    return index_level_init * 1.03 ** up * 0.985 ** (n - up)         # noqa: F821


def _sec_stepped_index_level(t):
    """The same path on SEC's clock: S's level at the row's own month, ``t`` plus its
    months in force, rebased so that the path's level at the valuation date is
    ``index_level_init``, as the generator rebases the levels of the ladder."""
    d = duration_mth_init()                                          # noqa: F821
    n = d + t
    up = (n // 18) * 9 + min(n % 18, 9)
    up0 = (d // 18) * 9 + min(d % 18, 9)
    return (index_level_init * (1.03 ** up * 0.985 ** (n - up))      # noqa: F821
            / (1.03 ** up0 * 0.985 ** (d - up0)))


# The two References the override sets in both models beside it: an index floor of 0.5%,
# apart from 0, so that a credit floored reads it, and a multiplier's cap of 0.8, which its
# raw value of 1 passes in every month, apart from the floor of 0.5 and the neutral 1.0.
OVERRIDE_REFS = {"index_floor": 0.005, "lapse_dyn_cap": 0.8}
OVERRIDE_ROWS = (("twin", 4, 0), ("derived", 4, 65), ("derived", 1, 60),
                 ("future", 4, -25))


@pytest.mark.sec_full
@pytest.mark.skipif(not SEC_FULL, reason="the index path's override runs with "
                    "USLIB_SEC_FULL=1 (USLIB-SEC-PLAN.md K6)")
def test_the_index_path_is_overridden_alike_in_both_models(tmp_path):
    """A stepped index path, given to both models, moves every credit alike (K7, D7).

    ``IUL_US_S``'s index rises at one level rate, so every segment returns the same 6.4% a
    year, the floor and the cap never bind, and a segment's start level read from the
    References rather than from the ladder changes no credit.  So both models'
    ``index_level`` is overridden, on models just read, so modelx's alone (C1), by a path
    that rises 3% a month for nine months and falls 1.5% a month for nine, on S's own clock
    and on SEC's, rebased to ``index_level_init`` at the valuation date
    (:func:`_sec_stepped_index_level`), with :data:`OVERRIDE_REFS` set first.  The
    generator restates S's points 4 and 1 at 65 and 60 out of that S, so the ladder carries
    the stepped levels at each segment's creation, rebased.  Then the twin of S's point 4,
    the two restated rows and S's point 4 issued 25 months on are S's points cell by cell,
    to 1e-9 relative with no absolute floor but S's roundings about zero, the segments
    carried in among them; S's point 4 credits 400 of its segments at the cap and 300 at
    the floor; and the index floor's side of its ``max`` and the multiplier's cap's side of
    its ``min`` win, the sides :data:`BOUND_ELSEWHERE` names this test for
    (:class:`_BoundSides`).  A start level read from the References would part the
    restated rows from S here.  It runs with ``USLIB_SEC_FULL=1`` only (USLIB-SEC-PLAN.md
    K6, weighed at M13): of the faults swept at M6 and M13 it is the only catcher of
    none, since the valuation-clock index test and the opening-column test also catch a
    start level read from the References.
    """
    s = _read(_s_inputs(tmp_path / "s", _s_table().loc[[1, 4]]), "stepped_s",
              OVERRIDE_REFS)
    sec = None
    try:
        s.Projection.cells["index_level"].formula = _s_stepped_index_level
        for key in point_keys(s):
            _sweep_s(projection(s, key))
        derived = [(p, d) for kind, p, d in OVERRIDE_ROWS if kind == "derived"]
        future = [(p, -k) for kind, p, k in OVERRIDE_ROWS if kind == "future"]
        sec = _read(_spliced_folder(tmp_path / "sec", s, derived, future, {}), "stepped",
                    OVERRIDE_REFS)
        sec.Projection.cells["index_level"].formula = _sec_stepped_index_level
        sp = _point(s, 4)
        months = range(sp.seg_term_mth, sp.proj_len())
        capped = sum(sp.seg_return(t) * sp.index_par > sp.index_cap_at(t) for t in months)
        floored = sum(sp.seg_return(t) * sp.index_par < sp.index_floor for t in months)
        assert (capped, floored) == (400, 300), (capped, floored)
        found = {}
        bounds = _BoundSides(sec)
        with bounds.watch() as won:
            for case in OVERRIDE_ROWS:
                kind, s_point, month = case
                term = s.Projection.seg_term_mth
                exempt, arg_map = {"twin": (TWIN_EXEMPT, _issued_later),
                                   "derived": (SPLICE_EXEMPT,
                                               _carried_segments(month, term)),
                                   "future": (FUTURE_EXEMPT, _issued_later)}[kind]
                key = _row_key(sec, *case)
                lines = _continues_s(_point(s, s_point), projection(sec, key), month,
                                     exempt, arg_map)
                if lines:
                    found[case] = lines[:5]
                _release(sec, key)
        assert not found, found
        mine = _sides_bound_by("test_the_index_path_is_overridden_alike_in_both_models")
        assert len(mine) == 2
        if sys.version_info >= (3, 11):
            assert mine <= won, sorted(mine - won)
    finally:
        if sec is not None:
            sec.close()
        s.close()


# ---------------------------------------------------------------------------
# The cap and the fixed account's rate, stepped on the valuation clock (K7, D7)


STEP_MTH = 30           # the month from the valuation date the two steps fall in


def _stepped_cap(t):
    """A cap declared at 10% before month 30 from the valuation date and at 5% from it."""
    return 0.10 if t < 30 else 0.05


def _stepped_fixed_rate(t):
    """A fixed account rate of 4.5% before month 30 from the valuation date, 3% from it."""
    return 0.045 if t < 30 else 0.03


# The rows the steps are read on: S point 4's twin, its row restated at 65, carrying
# twelve segments in, and the row issued 25 months on, whose first segment is created
# five months before the step and matures after it.
CLOCK_ROWS = (("twin", 4, 0), ("derived", 4, 65), ("future", 4, -25))


def test_the_cap_and_the_fixed_rate_are_read_on_the_valuation_clock(tmp_path):
    """A segment keeps the cap declared at its creation; the fixed account reads month t.

    ``IUL_US_S`` holds both rates level, and its engine reads ``index_cap_at(0)`` for every
    segment, so no comparison with S can tell which month either is read at.  So, on the
    committed model just read, so modelx's alone (K7, C1), ``index_cap_at`` and
    ``fixed_rate_ann`` are overridden by paths that step in month 30 from the valuation
    date, the cap from 10% to 5%, below the 6.4% return, and the rate from 4.5% to 3%, and
    on :data:`CLOCK_ROWS`, in every month of the frame:

    * a segment created in the frame is capped at the cap of its creation month,
      ``index_cap_at(t - 12)``, not at its maturity's, and one carried in at its ladder
      row's cap; each maturing segment is credited by the engine at that cap, and where it
      is 5% the credited rate is the cap, below the return times the participation, and so
      is the trailing rate dynamic lapse reads;
    * the fixed account's monthly rate is ``fixed_rate_ann(t)``'s, and its interest that
      rate on the fixed account, with the collateral's at its own rate, and before a
      policy's first maturity, or with nothing allocated, the trailing rate is
      ``fixed_rate_ann(t)``.

    A cell reading either at the policy month, or the cap at a segment's maturity, gives
    other rates at the step on each row.
    """
    model = _read(model_path(SEC), "clocks")
    try:
        model.Projection.cells["index_cap_at"].formula = _stepped_cap
        model.Projection.cells["fixed_rate_ann"].formula = _stepped_fixed_rate
        term = model.Projection.seg_term_mth
        faults, capped, born = [], 0, 0
        for case in CLOCK_ROWS:
            x = _row(model, *case)
            where = _case_id(*case)
            for t in range(x.t_entry(), x.proj_len()):
                rate = x.inv_return_mth(t)
                if rate != (1 + _stepped_fixed_rate(t)) ** (1 / 12) - 1:
                    faults.append(f"{where}: inv_return_mth({t}) {rate}")
                bef_inv = _code(x, "BEF_INV")
                interest = (x.fa_pp_at(t, bef_inv) * rate
                            + x.lca_pp_at(t, bef_inv) * x.loan_credit_rate_mth(t))
                if x.inv_income_pp(t) != interest:
                    faults.append(f"{where}: inv_income_pp({t}) {x.inv_income_pp(t)}")
                if x.duration_mth(t) < term:
                    if x.cred_rate_ann(t) != _stepped_fixed_rate(t):
                        faults.append(f"{where}: cred_rate_ann({t}) {x.cred_rate_ann(t)}")
                    continue
                if t - term >= x.t_entry():
                    cap = _stepped_cap(t - term)
                    born += STEP_MTH <= t < STEP_MTH + term
                else:
                    cap = x.seg_index_cap_init(term - t)
                if x.seg_index_cap(t) != cap:
                    faults.append(f"{where}: seg_index_cap({t}) {x.seg_index_cap(t)}, "
                                  f"declared {cap}")
                m = x.duration_mth(t) - term
                if t > x.t_entry():
                    draws = _seg(x, "seg_wd_cum_pp", t - 1, m)
                    ded = _seg(x, "seg_ded_cum_pp", t - 1, m)
                else:
                    draws, ded = x.seg_wd_cum_pp_init(term), x.seg_ded_cum_pp_init(term)
                credit = x.index_credit(x.seg_new_pp(m) - draws, ded, x.seg_return(t),
                                        x.seg_credit_base_conv, cap)
                if x.index_credit_pp(t) != credit:
                    faults.append(f"{where}: index_credit_pp({t}) {x.index_credit_pp(t)}")
                rate = x.index_credit_rate(x.seg_return(t), cap)
                if x.cred_rate_ann(t) != rate:
                    faults.append(f"{where}: cred_rate_ann({t}) {x.cred_rate_ann(t)}")
                if cap == 0.05 and x.index_par * x.seg_return(t) > cap == rate:
                    capped += 1
            _release(model, _key(model, _label(model.Data.model_point_table(), *case)))
        assert not faults, faults[:10]
        assert capped and born, (capped, born)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# D5's chains, called cold on models read for the test


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


def _one_cell_a_month(label, depth, chain, call, overhead=CHAIN_OVERHEAD):
    """Whether a cold call ran ``depth`` cells deep over a chain ``chain`` steps long.

    It must run at least as deep as its chain, or it did not run its chain cold, and at
    most ``overhead`` cells deeper.  Returns the finding, or nothing.
    """
    if chain <= depth <= chain + overhead:
        return []
    return [f"point {label}: {call} cold runs {depth} cells deep, where its chain is "
            f"{chain} steps and {overhead} more are allowed"]


# The two rows of the longest cover (_longest_cover), as (duration_mth_init(), t_entry(),
# proj_len()): issued at the valuation date at age 0, and 120 months on.
LONGEST_FRAMES = ((0, 0, 1452), (-120, 120, 1572))


def _longest_cover(tmp_path):
    """A copy whose table holds S point 4 at issue age 0, issued now and 120 months on.

    ``IUL_US_S``'s frame from issue is ``12 * (maturity_age - issue age)`` months, and the
    product spec issues from age 0, so the longest cover is 1,452 months, and the longest
    frame that issued 120 months on, the shipped ``future_horizon_mth``, 1,572 months,
    whose chains stop at ``t_entry()``.  The second row takes its own label before its
    duration is written, so that the edit lands on it alone, and the test asserts both
    frames (:data:`LONGEST_FRAMES`).  The copy's COI scale gains a cell for issue age 0, the
    anchor cell's first year's rate falling 6% a year back from the anchor's, for 121
    policy years, and its mortality table the ages 0 to 17, each geometric in the age, so
    that an age or a year read for another changes a number; the corridor table starts at
    0 already.
    """
    committed = _committed()
    now, later = _label(committed, "twin", 4, 0), _label(committed, "future", 4, -25)
    table = committed.loc[[now, now]].assign(age_at_entry=0)
    table.index = pd.Index([now, later], name="point_id")
    table = _set("duration_mth", [later], -120)(table)
    table = table.assign(policy_id=[f"{committed.at[now, 'policy_id']}-A0",
                                    f"{committed.at[now, 'policy_id']}-A0F120"])

    def coi(rates):
        years = range(1, 122)
        young = pd.DataFrame({
            "sex": "M", "rate_class": "NT", "age_at_entry": 0, "policy_year": list(years),
            "coi_rate_guar": [round(0.05 * 1.07 ** (y - 1), 6) for y in years],
            "provenance": "test copy"})
        return pd.concat([young, rates], ignore_index=True).sort_values(
            COI_KEYS, ignore_index=True)

    def mort(rates):
        ages = range(0, 18)
        young = pd.DataFrame({"age": list(ages),
                              "mort_rate": [round(0.0002 * 1.03 ** a, 6) for a in ages],
                              "provenance": "test copy"})
        return pd.concat([young, rates], ignore_index=True)

    return _sec_inputs(tmp_path, table, edits={"coi_rates.csv": coi,
                                               "mort_table.csv": mort},
                       ladder=_committed_ladder().iloc[0:0]), (now, later)


# Each chain of the model and the cell that heads it, called cold at the last month the
# chain reaches: (cell, its month as months from proj_len(), its other arguments, the
# chain's own recursive cells): the loan, the premiums paid, the no-lapse accumulator, the
# face, the collateral, the fixed account, the account value, the MEC latch and the count.
# Each head is called alone, on a read of its own, with every chain cold, which is checked
# (USLIB-SEC-PLAN.md §7.3, Record — M3, Chains, precised at M9): a head that reads other
# chains runs deepest only while those are cold too, the account value reading the fixed
# account, the collateral and the face through the death benefit, the latch the premiums
# paid, and the count the account value through the guarantee's test.  The account value's
# opening timing and the count are carried into t = proj_len(), so their heads are read
# there.  The segment cells, keyed by a month of creation, live at most twelve months, and
# are no chain.
CHAIN_HEADS = (("loan_bal_pp", -1, (), ("loan_bal_pp",)),
               ("cum_prem_pp", -1, (), ("cum_prem_pp",)),
               ("cum_prem_net_pp", -1, (), ("cum_prem_net_pp",)),
               ("sum_assured_at", -1, (), ("sum_assured_at",)),
               ("lca_pp_at", -1, ("BEF_PREM",), ("lca_pp_at",)),
               ("fa_pp_at", -1, ("BEF_PREM",), ("fa_pp_at",)),
               ("av_pp_at", 0, ("BEF_PREM",), ("av_pp_at",)),
               ("is_mec", -1, (), ("is_mec",)),
               ("pols_if_at", 0, ("BEF_NB",), ("pols_if_at",)))


def _chains_cold(folder, labels, refs, heads=CHAIN_HEADS):
    """The cold depths of ``heads`` on ``labels`` of the model in ``folder``.

    Each head on a read of its own, with ``refs`` set first, so that every chain is cold
    when it is called, which is checked first: a head called after another on one read
    would find that one's chain warm, and run shallower than it can.  Each chain runs back
    to ``t_entry()``.  Returns the findings.
    """
    chains = [name for *_, chain in CHAIN_HEADS for name in chain]
    found = []
    for label in labels:
        for cell, offset, rest, chain in heads:
            fresh = _read(folder, "chains", refs)
            try:
                p = _point(fresh, label)
                end = p.proj_len()
                warm = [name for name in chains if len(p.cells[name].keys())]
                if warm:
                    found.append(f"point {label}: {warm} reached before {cell} was "
                                 f"called, so not every chain was cold")
                    continue
                t = end + offset
                args = (t, *(_code(p, x) for x in rest))
                found += _one_cell_a_month(label, _cold_depth(p, cell, args),
                                           t - p.t_entry(), f"{cell}{args}")
            finally:
                fresh.close()
    return found


def _net_cf_cold(folder, labels, refs):
    """The cold depth of ``net_cf`` in the last month of each of ``labels``, one read each.

    The chain runs back to ``t_entry()``.
    """
    found = []
    for label in labels:
        fresh = _read(folder, "cold", refs)
        try:
            p = _point(fresh, label)
            last = p.proj_len() - 1
            found += _one_cell_a_month(label, _cold_depth(p, "net_cf", (last,)),
                                       last - p.t_entry(), f"net_cf({last})")
        finally:
            fresh.close()
    return found


def _expiry_cold(folder, label):
    """The cold depth of the guarantee's expiry read after a lapsed guarantee, on a read.

    The count of every month to the expiry's first is asked for in ascending ``t``, as a
    report asks for it, which reads the account value only while the guarantee holds; then
    the count of the month after the expiry's first, whose lapse rate reads the net cash
    value there, cold back to the month after the guarantee last held.  Returns the
    findings and the months the account value was read at before that read.
    """
    fresh = _read(folder, "expiry")
    try:
        p = _point(fresh, label)
        gap = _expiry_gap(p)
        expiry = 12 * p.nlg_period_years() - p.duration_mth_init()
        for t in range(expiry + 1):
            p.pols_if(t)
        read = sorted(key[0] for key in p.cells["av_pp_at"].keys())
        depth = _cold_depth(p, "pols_if", (expiry + 1,))
        found = _one_cell_a_month(label, depth, gap, f"pols_if({expiry + 1})",
                                  EXPIRY_OVERHEAD)
        return found, read, (gap, expiry)
    finally:
        fresh.close()


def _ascending(folder, limits, refs=None):
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
    pytest.param("expiry", id="expiry"),
    pytest.param("deepest call at the longest cover", id="longest-net_cf"),
    pytest.param("longest cover", id="longest", marks=FULL_ONLY),
    pytest.param("ascending at the longest cover", id="longest-ascending",
                 marks=FULL_ONLY)])
def test_every_chain_runs_one_cell_a_month_from_a_cold_start(tmp_path, case):
    """Called cold, each chain runs one cell a month back to its base, no more (D5, R2).

    No number shows how deep a chain runs, and a compiled model runs it on the C stack, so
    a chain of two cells a month, which gives the same numbers, needs twice the stack on
    every platform (F7).  ``IUL_US_S``'s account value ran through five cells a month, its
    fixed account through six and its collateral through two; here each forms the previous
    month's close itself.  On a model just read, nothing is cached, so modelx's stack trace
    counts how deep a call runs, against one cell a month and :data:`CHAIN_OVERHEAD` more:

    * ``shipped``, at the shipped References: on the twins of S's points 1 and 3, the row
      of S point 5 at 384 and the row issued 25 months on, ``net_cf`` in the last month,
      each on a read of its own, the deepest call a projection makes, down the account
      value's chain to ``t_entry()``; then, on S point 4's twin, monthly and with a full
      ladder, each of :data:`CHAIN_HEADS` alone, each on a read of its own, its own chain
      checked cold, so the chains a ``net_cf`` call reaches from the side are measured too,
      each while every other is cold.  No IUL point lapses for insufficiency, so every
      count runs its whole chain.
    * ``expiry``: the twin of S's point 5, whose guarantee holds last in month 48, read in
      ascending ``t`` to its expiry's first month, 240, as a report reads it; the account
      value was read at no month from 49 to 239, and the count of month 241 then runs the
      account value's chain cold from 240 back to 49, 192 months, the deepest read an
      ascending sweep makes, within :data:`EXPIRY_OVERHEAD` beyond it (:func:`_expiry_gap`).
    * ``deepest call at the longest cover``: the row issued now at issue age 0, of the two
      below, ``net_cf`` in its last month, 1,451 months above ``t_entry()``, the deepest
      call a projection makes on the longest chain the contract allows, both rows' frames
      asserted first, so that the stack's bound is measured by default, as the cases
      below measure it with every chain head on the full grid (USLIB-SEC-PLAN.md §7.5,
      *Record — M5*, *Carried into IUL (M6)*, depth at the longest cover).
    * ``longest cover``, with the full grid: at the contract's longest cover, issue age 0,
      issued now and 120 months on (:func:`_longest_cover`), each row's frame asserted
      first (:data:`LONGEST_FRAMES`), ``net_cf`` in the last month and each of
      :data:`CHAIN_HEADS` alone, each on a read of its own: the deepest cold calls the
      contract allows, which are what bound the stack, and where a level Phase 2 adds
      below each table's reader would first pass :data:`CHAIN_OVERHEAD`
      (USLIB-SEC-PLAN.md §7.1, *Record — M14*, *Carried into Phase 1*).
    * ``ascending at the longest cover``, with the full grid: both rows swept in ascending
      ``t`` under :data:`CALL_DEPTH`, as the committed points are.
    """
    committed = _committed()
    found = []
    if case == "shipped":
        labels = [_label(committed, "twin", p, 0) for p in (1, 3)]
        labels += [_label(committed, "derived", 5, 384),
                   _label(committed, "future", 4, -25)]
        found += _net_cf_cold(model_path(SEC), labels, {})
        found += _chains_cold(model_path(SEC), [_label(committed, "twin", 4, 0)], {})
    elif case == "expiry":
        found, read, (gap, expiry) = _expiry_cold(model_path(SEC),
                                                  _label(committed, "twin", 5, 0))
        assert (gap, expiry) == (192, 240)
        assert not [t for t in read if 49 <= t < expiry], read[-5:]
    else:
        folder, labels = _longest_cover(tmp_path)
        model = _read(folder, "longest")
        try:
            frames = [(p.duration_mth_init(), p.t_entry(), p.proj_len())
                      for p in (_point(model, label) for label in labels)]
        finally:
            model.close()
        assert tuple(frames) == LONGEST_FRAMES, frames
        if case == "deepest call at the longest cover":
            found += _net_cf_cold(folder, labels[:1], {})
        elif case == "longest cover":
            found += _net_cf_cold(folder, labels, {})
            found += _chains_cold(folder, labels, {})
        else:
            found += _ascending(folder, dict.fromkeys(labels, CALL_DEPTH))
    assert not found, found


# ---------------------------------------------------------------------------
# T4 -- the count's scale


# The References the scaling test sets in both copies: the splice's, which switch on the
# per-unit charge's second rate, which ships at zero, and charges ceasing in cover, with
# expense inflation, which ships at zero too, at 2.5% a year (USLIB-SEC-PLAN.md §5.2, T4).
SWITCHED_ON = {**SPLICED_REFS, "inflation_rate": INFLATION}

# The counted cells, and report columns, that are differences of products of the count:
# each side scales by the factor rounded its own way, so where the two sides nearly cancel
# the difference keeps their rounding, which is relative to the sides, not to it.  These
# are held to 1e-12 of their largest magnitude on the point; every other counted value to
# 1e-12 relative, value by value.
DIFFERENCES = frozenset({"av_change", "net_cf", "margin_expense", "margin_mortality"})
REPORT_DIFFERENCES = {"result_cf": ("net_cf",)}
# The committed rows the scaling test reads: the twin of S's point 1, S's point 4 restated
# at 65, its twelve segments carried in, S's point 5 restated at 384, with its loan, its
# collateral and its withdrawals, and at 605, its account value below 0, and S's point 4
# issued 25 months on, so that every counted cell is nonzero on some row.
SCALED_ROWS = (("twin", 1, 0), ("derived", 4, 65), ("derived", 5, 384),
               ("derived", 5, 605), ("future", 4, -25))


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

    Two copies of the committed table's rows of :data:`SCALED_ROWS`, the second with every
    count :data:`COUNT_FACTOR` times the first's, are read with :data:`SWITCHED_ON` set
    first: the per-unit charge's second rate, which ships at zero, switched on, with
    inflation on and charges ceasing in cover, so that every flow is nonzero on some
    point.  A factor that is not whole sees a count truncated to whole policies, and a flow
    left at zero sees no count at all.  Point by point, each released once compared:

    * every counted column of the four reports is 2.5 times the first's, to 1e-12 relative,
      value by value, a difference of products (``net_cf``) to 1e-12 of its peak;
    * every cell of :data:`COUNTED` at every key the first's sweep cached is 2.5 times the
      first's, value by value (:func:`_scaled_faults`);
    * ``result_pols``' rates and the whole of ``result_av`` and ``result_seg``, the
      roll-forwards per policy, are the first's exactly;
    * every other cell is the first's exactly, at every key, but the residuals, which are
      relative and move in the last digits; and the four checks hold on both;

    and every cell of :data:`COUNTED` but ``pols_maturity`` is nonzero on some point.
    """
    committed = _committed()
    labels = [_label(committed, *case) for case in SCALED_ROWS]
    base_table = committed.loc[labels]
    ladder = _committed_ladder()
    ladder = ladder[ladder["point_id"].isin(labels)]
    models = {}
    try:
        for tag, factor in (("one", 1.0), ("scaled", COUNT_FACTOR)):
            table = base_table.assign(policy_count=factor * base_table["policy_count"])
            models[tag] = _read(_sec_inputs(tmp_path / tag, table, ladder=ladder), tag,
                                SWITCHED_ON)
        one, scaled = models["one"], models["scaled"]
        faults, nonzero = [], set()
        for key, two_key, point_id in zip(point_keys(one), point_keys(scaled),
                                          base_table.index):
            base, two = projection(one, key), projection(scaled, two_key)
            sweep(base)
            for report in REPORTS:
                b, d = base.cells[report](), two.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                if report in PER_POLICY_REPORTS:
                    assert d.equals(b), (point_id, report)
                    continue
                same = RATES if report == "result_pols" else ()
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
            assert tuple(base.cells[c]() for c in CHECKS) + tuple(
                two.cells[c]() for c in CHECKS) == (True,) * 8, point_id
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
# coerce the column to numbers, so each is refused as a count, a duration, an age, a year,
# an amount, a share or a balance that is not a number, and a share past 1 as well as
# below 0.  The repeated point_id holds another policy under the same label, as a bad
# extract would, so that the check must look at the labels and not at whole rows.  The
# point_ids are the committed table's: 1 to 5, S's five points, issued at the valuation
# date; 6, S point 1 at 60; 7, S point 4 at 65, its twelve segments carried in; 8, S point
# 5 at 6; 9, S point 5 at 384, its fixed account below 0, with a loan and its collateral;
# 10, S point 5 at 605, its account value below 0 too; 11, S point 1 at 888; 12, S point 4
# issued 25 months on.  Each case is refused by its own rule alone, or, where a case pins
# a rule's place, by its rule first, on a row a later rule would refuse differently: a
# fractional duration on the future row past the horizon, which the horizon would refuse;
# a collateral below 0 on a row not yet in force, which the rule that holds the state there
# at 0 would refuse; and a blank fixed account on a row in force, which the segment
# ladder's identity would refuse.  A flag is True or False in any case, as pandas reads
# those words, and nothing else: the life chassis keeps S's bool(), which reads "0" or
# "0.0" in a column made text by one such cell as true, so 1, 0, 1.0 and 0.0 are refused,
# as a blank and any other text are (USLIB-SEC-PLAN.md §7.8, Record — M10, Flag
# spellings); a TRUE beside the bad cell, which the column's text keeps as written, is
# still a flag, so the message names the bad cell's point alone; and the spellings
# accepted are read in a test of their own.  Each rule over a window of policy months is
# refused at the window's first month and its last (USLIB-SEC-PLAN.md §5.2, T5, precised
# at M10): the state of a policy not yet in force at months 0 and -120, the horizon; the
# face in force at months 1 and 911, the last of cover; and the 7-pay test at months 1
# and 84.  The edges test reads the state at month 1 and the 7-pay test at month 85 and on
# its limit, just outside; the face has no month outside its window that the state's rule
# or proj_len() does not refuse first.
# A {file} in a message is the table's filename: every case is read from a file of its own
# (the malformed fixture).

_NUMBER = ("{{file}}: {column} must be a number, zero or more; it is not at point_id "
           "[{point}]")
_SIGNED = "{{file}}: {column} must be a number; it is not at point_id [{point}]"
_DURATION = ("{{file}}: duration_mth must be a whole number of months; it is not at "
             "point_id [{point}]")
_AGE = ("{{file}}: age_at_entry must be a whole number of years, 0 or more; it is not at "
        "point_id [{point}]")
_YEARS = ("{{file}}: {column} must be a whole number of policy years, 1 or more; it is not "
          "at point_id [{point}]")
_FACE = ("{{file}}: sum_assured must be a number above 0, the face at issue, which every "
         "policy holds; it is not at point_id [{point}]")
_SHARE = "{{file}}: {column} must be a number from 0 to 1; it is not at point_id [{point}]"
_FLAG = "{{file}}: has_surr_charge must be True or False; it is not at point_id [{point}]"
_MEC_CODE = ("{{file}}: is_mec_init must be 0 or 1, an int code; it is not at point_id "
             "[{point}]")
_NOT_IN_FORCE = ("{{file}}: {column} must be 0 on a policy not yet in force, duration_mth "
                 "0 or less; it is not at point_id [{point}]")
_FACE_IN_FORCE = ("{{file}}: sum_assured_init must be at most sum_assured, the face at "
                  "issue, since face increases are not modelled; it is not at point_id "
                  "[{point}]")
_COLLATERAL = ("{{file}}: lca_pp_init must be above 0 where loan_bal_init is, and 0 where "
               "it is 0: the collateral account holds a loan's collateral while the loan "
               "is outstanding; it is not at point_id [{point}]")
_NET = ("{{file}}: cum_prem_net_init must be at most cum_prem_init, to a cent and a half, "
        "since loans only lower it; it is not at point_id [{point}]")
_MEC = ("{{file}}: is_mec_init must be 1 where the 7-pay test has already failed, "
        "cum_prem_init above seven_pay_prem times the policy years to date, in the first "
        "seven; it is not at point_id [{point}]")

# The columns Data reads, each refused when the table lacks it.
READ_COLUMNS = ("policy_count", "duration_mth", "age_at_entry", "wd_first_year",
                "loan_first_year", "sum_assured", "premium_pp_ann", "wd_pp",
                "loan_new_pp_ann", "mnlp_rate", "gsp", "glp", "seven_pay_prem",
                "load_prem_rate", "index_alloc_rate", "has_surr_charge", *STATE)


def _in_force_at(point, months, **columns):
    """An edit that puts the twin ``point`` in force ``months`` months, with ``columns``.

    The twin carries no segment, so its account value is its fixed account and its
    collateral, which a ladder of no rows holds to; ``proj_len()`` would ask for the
    rows, and ``Data`` does not.
    """
    def edit(table):
        for column, value in {"duration_mth": months, **columns}.items():
            table = _set(column, [point], value)(table)
        return table
    return edit


MALFORMED = [
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in READ_COLUMNS],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[4]].assign(policy_id="IUL-900099")]),
     "{file}: point_id [4] appears more than once"),
    *[(f"a {what} count", _set("policy_count", [point], value),
       _NUMBER.format(column="policy_count", point=point))
      for what, point, value in (("negative", 4, -0.1), ("blank", 6, float("nan")),
                                 ("text", 7, "abc"), ("infinite", 7, float("inf")))],
    ("two bad counts", _set("policy_count", [4, 6], -1.0),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [4, 6]"),
    ("a fractional duration on the future row past the horizon",
     _set("duration_mth", [12], -120.5), _DURATION.format(point=12)),
    ("a blank duration", _set("duration_mth", [12], float("nan")),
     _DURATION.format(point=12)),
    ("a text duration", _set("duration_mth", [6], "x60"), _DURATION.format(point=6)),
    ("issued beyond the horizon", _set("duration_mth", [12], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [12]"),
    *[(f"an age_at_entry {what}", _set("age_at_entry", [8], value), _AGE.format(point=8))
      for what, value in (("of 45.5", 45.5), ("below 0", -1), ("as text", "45y"),
                          ("blank", float("nan")))],
    *[(f"a {column} {what}", _set(column, [4], value),
       _YEARS.format(column=column, point=4))
      for column in ("wd_first_year", "loan_first_year")
      for what, value in (("of 2.5", 2.5), ("of 0", 0), ("as text", "2y"),
                          ("blank", float("nan")))],
    *[(f"a {what} face", _set("sum_assured", [point], value), _FACE.format(point=point))
      for what, point, value in (("blank", 3, float("nan")), ("blank, in force,", 7,
                                                              float("nan")),
                                 ("zero", 1, 0.0), ("text", 12, "250k"),
                                 ("infinite", 2, float("inf")), ("negative", 2, -1.0))],
    *[(f"a {what} {column}", _set(column, [point], value),
       _NUMBER.format(column=column, point=point))
      for what, column, point, value in (
          ("text", "premium_pp_ann", 4, "x"), ("blank", "premium_pp_ann", 3, float("nan")),
          ("negative", "premium_pp_ann", 2, -1.0), ("text", "wd_pp", 2, "a lot"),
          ("infinite", "wd_pp", 8, float("inf")), ("negative", "wd_pp", 8, -1.0),
          ("negative", "loan_new_pp_ann", 9, -6000.0),
          ("blank", "loan_new_pp_ann", 5, float("nan")), ("text", "mnlp_rate", 1, "x"),
          ("negative", "mnlp_rate", 2, -20.8), ("blank", "gsp", 1, float("nan")),
          ("infinite", "glp", 3, float("inf")), ("negative", "seven_pay_prem", 4, -1.0))],
    *[(f"a {column} {what}", _set(column, [point], value),
       _SHARE.format(column=column, point=point))
      for what, column, point, value in (
          ("infinite", "load_prem_rate", 6, float("inf")),
          ("below 0", "load_prem_rate", 2, -0.1), ("above 1", "load_prem_rate", 3, 1.5),
          ("blank", "load_prem_rate", 5, float("nan")),
          ("as text", "load_prem_rate", 7, "5%"),
          ("above 1", "index_alloc_rate", 1, 1.5),
          ("below 0", "index_alloc_rate", 4, -0.5),
          ("blank", "index_alloc_rate", 12, float("nan")))],
    *[(f"has_surr_charge {what}", _set("has_surr_charge", [3], value),
       _FLAG.format(point=3))
      for what, value in (("blank", float("nan")), ("x", "x"), ("Yes", "Yes"), ("1", 1),
                          ("0", 0), ("1.0", 1.0), ("0.0", 0.0))],
    ("has_surr_charge x beside one written TRUE",
     _both(_set("has_surr_charge", [3], "x"), _set("has_surr_charge", [5], "TRUE")),
     _FLAG.format(point=3)),
    *[(f"a {what} {column}", _set(column, [point], value),
       _SIGNED.format(column=column, point=point))
      for what, column, point, value in (
          ("blank", "av_pp_init", 6, float("nan")), ("text", "av_pp_init", 7, "x"),
          ("infinite", "av_pp_init", 6, float("inf")),
          ("negative infinite", "av_pp_init", 7, -float("inf")),
          ("blank, in force,", "fa_pp_init", 9, float("nan")),
          ("text", "fa_pp_init", 10, "x"), ("infinite", "fa_pp_init", 6, float("inf")),
          ("blank", "cum_prem_init", 6, float("nan")), ("text", "cum_prem_init", 7, "x"),
          ("infinite", "cum_prem_init", 8, float("inf")),
          ("blank", "cum_prem_net_init", 9, float("nan")),
          ("text", "cum_prem_net_init", 10, "x"),
          ("negative infinite", "cum_prem_net_init", 6, -float("inf")))],
    *[(f"a {what} {column}", _set(column, [point], value),
       _NUMBER.format(column=column, point=point))
      for what, column, point, value in (
          ("negative", "lca_pp_init", 9, -0.01), ("blank", "lca_pp_init", 9, float("nan")),
          ("text", "lca_pp_init", 10, "x"),
          ("negative, on the future row,", "lca_pp_init", 12, -1.0),
          ("negative", "loan_bal_init", 6, -0.01), ("text", "loan_bal_init", 9, "x"),
          ("infinite", "loan_bal_init", 10, float("inf")),
          ("negative", "sum_assured_init", 6, -0.01),
          ("blank", "sum_assured_init", 7, float("nan")),
          ("infinite", "sum_assured_init", 11, float("inf")))],
    *[(f"an is_mec_init {what}", _set("is_mec_init", [point], value),
       _MEC_CODE.format(point=point))
      for what, point, value in (("of 2", 6, 2), ("of 0.5", 7, 0.5),
                                 ("blank", 8, float("nan")), ("as text", 9, "yes"),
                                 ("of -1", 10, -1), ("of 2 on the future row", 12, 2))],
    *[(f"{column} before issue", _set(column, [point], value),
       _NOT_IN_FORCE.format(column=column, point=point))
      for column, point, value in (
          ("av_pp_init", 3, 100.0), ("loan_bal_init", 12, 10.0), ("fa_pp_init", 1, -50.0),
          ("lca_pp_init", 12, 10.0), ("sum_assured_init", 2, 250000.0),
          ("cum_prem_init", 4, 10000.0), ("cum_prem_net_init", 5, -5.0),
          ("is_mec_init", 12, 1))],
    ("cum_prem_init before issue, issued at the horizon",
     _both(_set("duration_mth", [12], -120), _set("cum_prem_init", [12], 10000.0)),
     _NOT_IN_FORCE.format(column="cum_prem_init", point=12)),
    ("a face in force above the face at issue",
     _set("sum_assured_init", [7], 250000.01), _FACE_IN_FORCE.format(point=7)),
    ("a face above the face at issue in the first month in force",
     _in_force_at(1, 1, sum_assured_init=250000.01), _FACE_IN_FORCE.format(point=1)),
    ("a face above the face at issue in the last month of cover",
     _both(_set("duration_mth", [11], 911), _set("sum_assured_init", [11], 250000.01)),
     _FACE_IN_FORCE.format(point=11)),
    ("a collateral without a loan", _set("lca_pp_init", [6], 100.0),
     _COLLATERAL.format(point=6)),
    ("a loan without its collateral", _set("lca_pp_init", [9], 0.0),
     _COLLATERAL.format(point=9)),
    ("an accumulator two cents past the premiums paid",
     lambda t: _set("cum_prem_net_init", [6], t.at[6, "cum_prem_init"] + 0.02)(t),
     _NET.format(point=6)),
    ("the 7-pay test failed in its first month with no latch",
     _in_force_at(1, 1, cum_prem_init=21000.01, cum_prem_net_init=21000.01),
     _MEC.format(point=1)),
    ("the 7-pay test failed by the seventh year's last month with no latch",
     _in_force_at(1, 84, cum_prem_init=147000.01, cum_prem_net_init=147000.01),
     _MEC.format(point=1)),
    ("the 7-pay test failed on a row restated in its first year",
     _set("cum_prem_init", [8], 21000.01), _MEC.format(point=8)),
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
    model = _read(folder, "malformed", data={"model_point_file": files[case]})
    try:
        text = message.format(file=files[case])
        _refused_exactly(model.Data.model_point_table, text)
        _refused_exactly(lambda: model.Projection.net_cf(0), text)
    finally:
        model.close()


# Each malformed segment ladder is the committed one with one fault, read beside the
# committed table, each from a file of its own, which the message names, with the lines
# at fault, the header line 1, or the points.  The ladder's rows are the derived rows' in
# table order, twelve each but the row of S point 5 at 6, which holds six: the rows of
# point 6, S point 1 at 60, on lines 2 to 13, whose slots 1 to 11 are empty, the segment
# its anniversary premium swept maturing from slot 12; those of point 7, S point 4 at 65,
# on lines 14 to 25, every slot holding a balance; those of point 8 on lines 26 to 31;
# and the last row, point 11's slot 12, on line 67, so that a row added is on line 68.
# Each case is refused by one rule, or, where a case pins a rule's place, by its rule
# first, on a row a later rule would refuse differently: a slot on a point not yet in force
# by the slot's range, before the count proj_len() holds a point in force to, and a
# balance a dime below 0 by the balances' rule, before the account value's identity, which
# its point fails by more than its slack, 0.08 on twelve segments.
_LINE = "{{file}}: {column} must be a whole number; it is not on line [{line}]"
_SEGMENT = ("{{file}}: {column} must be a number, -1e-8 or more, zero to IUL_US_S's "
            "tolerance; it is not on line [{line}]")
_START = ("{{file}}: seg_index_start_init must be a number above 0, the level the "
          "segment's return divides by; it is not on line [{line}]")
_CAP = ("{{file}}: seg_index_cap_init must be a number, zero or more; it is not on line "
        "[{line}]")
_SLOT = ("{{file}}: slot must be from 1 to its point's duration_mth, the months since the "
         "segment's creation at the valuation date; it is not on line [{line}]")
_IDENTITY = (f"{TABLE}: av_pp_init must be fa_pp_init plus lca_pp_init plus the point's "
             "segments in {{file}}, to half a cent an amount and half a cent more; it is "
             "not at point_id [{point}]")


def _ladder_at(line, column, value):
    """An edit of the ladder that writes ``value`` into ``column`` on file line ``line``."""
    def edit(ladder):
        cells = ladder[column].astype(object)
        cells.iloc[line - 2] = value
        return ladder.assign(**{column: cells})
    return edit


def _ladder_row(point, slot, **columns):
    """An edit of the ladder that adds a row for ``point`` at ``slot``, empty, its start
    level and cap its point's slot 1's, at the end of the file, with ``columns``."""
    def edit(ladder):
        row = ladder[ladder["point_id"] == point].iloc[[0]].assign(
            slot=slot, seg_bal_pp_init=0.0, seg_ded_cum_pp_init=0.0,
            seg_wd_cum_pp_init=0.0, **columns)
        return pd.concat([ladder, row], ignore_index=True)
    return edit


MALFORMED_LADDER = [
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("point_id", "slot", *LADDER_VALUES)],
    *[(f"a {column} {what}", _ladder_at(line, column, value),
       _LINE.format(column=column, line=line))
      for column, line in (("point_id", 5), ("slot", 16))
      for what, value in (("of 6.5", 6.5), ("as text", "x"), ("blank", float("nan")))],
    # A key numpy would cast to the least int64, so that the refusal would name a point
    # the file does not write, or a slot no rule then refuses for what it is.
    *[(f"a {column} of {what}", _ladder_at(line, column, value),
       f"{{file}}: {column} must be below 2**53 in size; it is not on line [{line}]")
      for column, line in (("point_id", 2), ("slot", 16))
      for what, value in (("2**53", 2.0 ** 53), ("1e19", 1e19), ("-1e19", -1e19))],
    ("a point_id no point of the table has", _ladder_at(2, "point_id", 99),
     f"{{file}}: point_id [99] on line [2] is no point of {TABLE}"),
    ("a slot held twice", _ladder_at(3, "slot", 1),
     "{file}: each point_id and slot must have one row; point_id 6 slot 1 is on line "
     "[2, 3]"),
    ("a slot of 0", _ladder_at(2, "slot", 0), _SLOT.format(line=2)),
    ("a slot past its point's months in force", _ladder_row(8, 7), _SLOT.format(line=68)),
    ("a slot on a point not yet in force", _ladder_row(8, 1, point_id=1),
     _SLOT.format(line=68)),
    *[(f"a {column} {what}", _ladder_at(line, column, value),
       _SEGMENT.format(column=column, line=line))
      for column, line, what, value in (
          ("seg_bal_pp_init", 2, "2e-8 below 0", -2e-8),
          ("seg_bal_pp_init", 2, "two cents below 0", -0.02),
          ("seg_bal_pp_init", 2, "a dime below 0, past the identity's slack", -0.1),
          ("seg_bal_pp_init", 3, "blank", float("nan")),
          ("seg_bal_pp_init", 4, "as text", "x"),
          ("seg_bal_pp_init", 5, "infinite", float("inf")),
          ("seg_ded_cum_pp_init", 6, "two cents below 0", -0.02),
          ("seg_ded_cum_pp_init", 7, "blank", float("nan")),
          ("seg_wd_cum_pp_init", 8, "as text", "x"),
          ("seg_wd_cum_pp_init", 9, "infinite", float("inf")))],
    *[(f"a seg_index_start_init {what}", _ladder_at(14, "seg_index_start_init", value),
       _START.format(line=14))
      for what, value in (("of 0", 0.0), ("below 0", -4500.0), ("blank", float("nan")),
                          ("as text", "x"), ("infinite", float("inf")))],
    *[(f"a seg_index_cap_init {what}", _ladder_at(15, "seg_index_cap_init", value),
       _CAP.format(line=15))
      for what, value in (("below 0", -0.01), ("blank", float("nan")), ("as text", "x"),
                          ("infinite", float("inf")))],
    ("a balance a dime past the account value's identity",
     lambda ladder: _ladder_at(14, "seg_bal_pp_init", ladder.at[12, "seg_bal_pp_init"]
                               + 0.1)(ladder), _IDENTITY.format(point=7)),
    ("a balance half a cent past the identity's slack",
     lambda ladder: _ladder_at(14, "seg_bal_pp_init", ladder.at[12, "seg_bal_pp_init"]
                               + 0.085)(ladder), _IDENTITY.format(point=7)),
]


@pytest.fixture(scope="module")
def malformed_ladders(tmp_path_factory):
    """One copy of the product directory, and beside it each ladder of
    :data:`MALFORMED_LADDER`, each a file of its own.  Returns ``(the copy's SEC folder,
    {case: filename})``."""
    root = tmp_path_factory.mktemp("ladders")
    files = {}
    for number, (case, edit, _) in enumerate(MALFORMED_LADDER):
        files[case] = f"ladder_{number:02d}_sec.csv"
        temp_inputs(root, model_path(SEC), model_points=edit(_committed_ladder()),
                    model_point_file=files[case])
    return root / SEC, files


@pytest.mark.parametrize("case, edit, message", MALFORMED_LADDER,
                         ids=[c[0] for c in MALFORMED_LADDER])
def test_a_malformed_segment_ladder_is_refused_naming_its_line(malformed_ladders, case,
                                                               edit, message):
    """``Data.inforce_segments()`` refuses the ladder, naming the fault (D6, T5).

    And so do the cells that read it, ``Data``'s count and last slot, and the base
    ``Projection``'s frame at its default point: ``proj_len()`` asks for the ladder's count
    before anything is projected, as a compiled model must.  The message is matched whole,
    so that a case another rule refused first would fail here.  The table is read as
    committed, and ``Data`` reads it whole.
    """
    folder, files = malformed_ladders
    model = _read(folder, "ladder", data={"inforce_segments_file": files[case]})
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        text = message.format(file=files[case])
        for call in (model.Data.inforce_segments, model.Data.inforce_segment_count,
                     model.Data.inforce_segment_last, model.Projection.proj_len):
            _refused_exactly(call, text)
    finally:
        model.close()


# Each assumption table, with one fault in its key column, as an extract or an edit by hand
# can leave it: a blank key, which pandas reads as a missing value, a key written as text,
# a fractional one, keys that repeat or leave a gap, a first year missing or one below the
# fixed first year, and no row at all.  The blank is the case that matters most: IUL_US_S's
# readers take a table's extent from the key column as pandas reads it, where a blank last
# key is a missing value the extent skips, so the table is cut short and every later key
# reads the last good row without a word.  Here each table is checked once, in the Data
# cell its reader asks first, and refused naming the file and the column: the lines a key
# that is blank, text or fractional is on, and each key that repeats or falls below its
# first, with its lines, and each that is missing.  Each case is (case, the file, its edit,
# the Data cell that checks it, the message), and the message is matched whole.  The lines
# count the header as line 1: the policy year y of the lapse table and of the COI scale's
# cell is on line y + 1, the age a of the corridor table on line a + 2 and of the mortality
# table on line a - 16.
_WHOLE = "{file}: {column} must be a whole number; it is not on line {lines}"
_RUNS = {"policy_year": ("{file}: the policy years must run from 1, one row a year, "
                         "without a gap or a repeat; "),
         "age": "{file}: the ages must run one row an age, without a gap or a repeat; "}
_COI_RUN = ("coi_rates.csv: the policy years of each sex, rate_class and age_at_entry must "
            "run from 1, one row a year, without a gap or a repeat; ")
_CELL = "at ('M', 'NT', 45)"


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


def _drop_rows(*rows):
    """An edit that drops the table's ``rows``, which leaves a gap in its keys."""
    return lambda table: table.drop(index=table.index[list(rows)])


def _no_row(table):
    """An edit that leaves the table its header and no row."""
    return table.iloc[0:0]


def _twice(row):
    """An edit that writes the table's ``row``-th row again, at its end."""
    return lambda table: pd.concat([table, table.iloc[[row]]], ignore_index=True)


def _shifted(column, by):
    """An edit that moves every key of ``column`` by ``by``."""
    return lambda table: table.assign(**{column: table[column] + by})


def _second_coi_cell(rates):
    """The COI scale with a second cell, F NT issued at 45, the anchor's rows with policy
    year 30 left out, and the anchor's own year 5 left out too: a gap in each of two
    cells."""
    second = rates[rates["policy_year"] != 30].assign(sex="F", provenance="test copy")
    return pd.concat([rates[rates["policy_year"] != 5], second], ignore_index=True)


# Each table read at a policy year or an attained age: (its key column, the Data cell that
# checks it, its first key, the row each case edits, which leaves a key before it, and the
# line of its last row).  The lapse table holds the policy years 1 to 11, the corridor
# table the ages 0 to 121 and the mortality table 18 to 120.
KEY_TABLES = {
    "lapse_table.csv": ("policy_year", "lapse_last_year", 1, 4, 12),
    "corridor_factors.csv": ("age", "corridor_age_last", 0, 9, 123),
    "mort_table.csv": ("age", "mort_age_last", 18, 9, 104),
}
MALFORMED_KEYS = [
    *[(f"{file}: {what}", file, _write_at(column, row, value), check,
       _WHOLE.format(file=file, column=column, lines=f"[{line}]"))
      for file, (column, check, _, edited, last) in KEY_TABLES.items()
      for what, row, value, line in (
          ("its last key blank", -1, float("nan"), last),
          ("a key written as text", edited, "6x", edited + 2),
          ("a fractional key", edited, 10.5, edited + 2))],
    *[(f"{file}: {what}", file, edit, check, _RUNS[column].format(file=file) + fault)
      for file, (column, check, first, edited, _) in KEY_TABLES.items()
      for what, edit, fault in (
          ("a repeated key", _repeat_key(column, edited),
           f"{column} {first + edited - 1} is on line [{edited + 1}, {edited + 2}]; "
           f"no line holds {column} {first + edited}"),
          ("a gap", _drop_rows(edited), f"no line holds {column} {first + edited}"),
          ("a gap of three keys", _drop_rows(edited, edited + 1, edited + 2),
           f"no line holds {column} {first + edited} to {first + edited + 2}"),
          ("no row", _no_row, "no line holds policy_year 1" if column == "policy_year"
           else "no line holds an age"))],
    ("lapse_table.csv: its first year missing", "lapse_table.csv", _drop_rows(0),
     "lapse_last_year", _RUNS["policy_year"].format(file="lapse_table.csv")
     + "no line holds policy_year 1"),
    ("lapse_table.csv: a first policy year written 0", "lapse_table.csv",
     _write_at("policy_year", 0, 0), "lapse_last_year",
     _RUNS["policy_year"].format(file="lapse_table.csv")
     + "policy_year 0 is on line [2]; no line holds policy_year 1"),
    ("lapse_table.csv: its policy years from 0", "lapse_table.csv",
     _shifted("policy_year", -1), "lapse_last_year",
     _RUNS["policy_year"].format(file="lapse_table.csv") + "policy_year 0 is on line [2]"),
    ("lapse_table.csv: its policy years from 2", "lapse_table.csv",
     _shifted("policy_year", 1), "lapse_last_year",
     _RUNS["policy_year"].format(file="lapse_table.csv") + "no line holds policy_year 1"),
    *[(f"coi_rates.csv: {what}", "coi_rates.csv", edit, "coi_schedules", message)
      for what, edit, message in (
          ("its last sex blank", _write_at("sex", -1, float("nan")),
           "coi_rates.csv: sex must not be blank; it is on line [77]"),
          ("a blank rate_class", _write_at("rate_class", 3, float("nan")),
           "coi_rates.csv: rate_class must not be blank; it is on line [5]"),
          ("an issue age written as text", _write_at("age_at_entry", 4, "45x"),
           _WHOLE.format(file="coi_rates.csv", column="age_at_entry", lines="[6]")),
          ("a fractional policy year", _write_at("policy_year", 9, 10.5),
           _WHOLE.format(file="coi_rates.csv", column="policy_year", lines="[11]")),
          ("its last policy year blank", _write_at("policy_year", -1, float("nan")),
           _WHOLE.format(file="coi_rates.csv", column="policy_year", lines="[77]")),
          ("a repeated policy year", _repeat_key("policy_year", 9),
           _COI_RUN + f"{_CELL}, policy_year 9 is on line [10, 11]; {_CELL}, no line holds "
           "policy_year 10"),
          ("a gap", _drop_rows(4), _COI_RUN + f"{_CELL}, no line holds policy_year 5"),
          ("a gap of three years", _drop_rows(4, 5, 6),
           _COI_RUN + f"{_CELL}, no line holds policy_year 5 to 7"),
          ("its first year missing", _drop_rows(0),
           _COI_RUN + f"{_CELL}, no line holds policy_year 1"),
          ("a gap in each of two cells", _second_coi_cell,
           _COI_RUN + "at ('F', 'NT', 45), no line holds policy_year 30; "
           f"{_CELL}, no line holds policy_year 5"))],
    ("class_factor_table.csv: a blank rate_class", "class_factor_table.csv",
     _write_at("rate_class", 2, float("nan")), "class_count",
     "class_factor_table.csv: rate_class must not be blank; it is on line [4]"),
    ("class_factor_table.csv: a repeated rate_class", "class_factor_table.csv",
     _repeat_key("rate_class", 3), "class_count",
     "class_factor_table.csv: each rate_class must have one row; rate_class Pref is on "
     "line [4, 5]"),
    ("surr_charge_table.csv: a blank surr_charge_id", "surr_charge_table.csv",
     _write_at("surr_charge_id", 0, float("nan")), "surr_charge_count",
     "surr_charge_table.csv: surr_charge_id must not be blank; it is on line [2]"),
    ("surr_charge_table.csv: a repeated surr_charge_id", "surr_charge_table.csv",
     _twice(0), "surr_charge_count",
     "surr_charge_table.csv: each surr_charge_id must have one row; surr_charge_id IUL10 "
     "is on line [2, 3]"),
]

# Each value a reader reads, blank, written as text and infinite, in every table: the rates
# and factors keyed by a policy year or an age, the COI scale, the class factors and the
# surrender charge.  IUL_US_S reads a blank as a missing value, which shows in its flows
# or is lost in a min or a max: a blank corridor factor reads as no corridor, a blank
# surrender charge as none, and a blank lapse rate as the cap, through its min written
# bound first; and this model's capped mortality, min(q, 1.0), keeps a blank base rate or
# class factor missing, where its bound first would read it as 1.  Then values outside
# their range: a lapse or mortality rate above 1 or below 0, neither a probability, and a
# class factor, a guaranteed COI rate or a surrender charge below 0, each of which
# projects, with every check passing, a negative death or charge, or a surrender charge
# that rises once its schedule has run off; and a corridor factor below 0, which no
# statutory percentage is, and which IUL_US_S's death benefit, with no floor on the
# account value, would turn above the face on an exhausted account.  Then values no point
# reads, a factor of a class no committed point carries and rates at ages none reaches,
# and two lines at fault in one column; and the run-off, which must be a whole number of
# years, 1 or more, since the model divides by it.
# Each case is as in MALFORMED_KEYS.
_RATE = "{file}: {column} must be {what}; it is not on line {lines}"
# Each value column: (its file, the column, the Data cell that checks it, the row edited,
# its line, what each value must be, the values outside its range).
RATE_COLUMNS = (
    ("lapse_table.csv", "lapse_rate_ann", "lapse_last_year", 4, 6, "a number from 0 to 1",
     (1.2, -0.05)),
    ("corridor_factors.csv", "corridor_factor", "corridor_age_last", 50, 52,
     "a number, zero or more", (-0.5,)),
    ("mort_table.csv", "mort_rate", "mort_age_last", 29, 31, "a number from 0 to 1",
     (1.01, -0.01)),
    ("coi_rates.csv", "coi_rate_guar", "coi_schedules", 9, 11,
     "a number, zero or more", (-1.0,)),
    ("class_factor_table.csv", "factor", "class_count", 3, 5, "a number, zero or more",
     (-0.5,)),
    ("surr_charge_table.csv", "sc_per_1000_init", "surr_charge_count", 0, 2,
     "a number, zero or more", (-18.0,)),
)
_RUNOFF = ("surr_charge_table.csv: runoff_years must be a whole number of years, 1 or "
           "more; it is not on line [2]")
MALFORMED_RATES = [
    *[(f"{file}: {what.format(column)}", file, _write_at(column, row, value), check,
       _RATE.format(file=file, column=column, what=rule, lines=f"[{line}]"))
      for file, column, check, row, line, rule, _ in RATE_COLUMNS
      for what, value in (("a blank {}", float("nan")), ("{} written as text", "x"),
                          ("an infinite {}", float("inf")))],
    *[(f"{file}: a {column} of {value}", file, _write_at(column, row, value), check,
       _RATE.format(file=file, column=column, what=rule, lines=f"[{line}]"))
      for file, column, check, row, line, rule, outside in RATE_COLUMNS
      for value in outside],
    ("mort_table.csv: a mort_rate no point reads", "mort_table.csv",
     _write_at("mort_rate", 0, float("nan")), "mort_age_last",
     _RATE.format(file="mort_table.csv", column="mort_rate", what="a number from 0 to 1",
                  lines="[2]")),
    ("mort_table.csv: two mort_rate lines", "mort_table.csv",
     _write_rows("mort_rate", (30, 33), "n/a"), "mort_age_last",
     _RATE.format(file="mort_table.csv", column="mort_rate", what="a number from 0 to 1",
                  lines="[32, 35]")),
    ("class_factor_table.csv: a factor no point reads", "class_factor_table.csv",
     _write_at("factor", 0, float("inf")), "class_count",
     _RATE.format(file="class_factor_table.csv", column="factor",
                  what="a number, zero or more", lines="[2]")),
    ("corridor_factors.csv: a factor no point reads", "corridor_factors.csv",
     _write_at("corridor_factor", 0, float("nan")), "corridor_age_last",
     _RATE.format(file="corridor_factors.csv", column="corridor_factor",
                  what="a number, zero or more", lines="[2]")),
    *[(f"surr_charge_table.csv: runoff_years {what}", "surr_charge_table.csv",
       _write_at("runoff_years", 0, value), "surr_charge_count", _RUNOFF)
      for what, value in (("blank", float("nan")), ("written as text", "x"),
                          ("infinite", float("inf")), ("of 7.5", 7.5), ("of 0", 0))],
]


def _table_refused(tmp_path, file, edit, check, message):
    """Data's ``check``, then a projection, refuse the copy whose ``file`` is ``edit``-ed.

    The Data cell is asked first, and with it the first-age cell an age table's reader
    also asks, and then ``net_cf(0)`` of the base ``Projection``'s default point, the twin
    of S's anchor point, issued at the valuation date, which reads every one of these
    tables in its first month: the corridor through its death benefit, the mortality table
    and the class factor through the month's deaths, the lapse table through its lapses,
    the COI scale through the deduction the cash value a lapse is paid is net of, and the
    surrender charge through that cash value.
    """
    folder = temp_inputs(tmp_path, model_path(SEC), edits={file: edit})
    model = _read(folder, "tables")
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
    """The Data cell a reader asks first refuses the table (T5).

    And so does the projection of the committed table's first point, in its first month
    (:func:`_table_refused`).  The reader asks for its extent or its count before it reads
    a value, so a projection meets the check first, as a compiled model's must.  The age
    tables' first age is counted from their last, so it meets the same check.  The message
    is matched whole, so that each key it names, repeated or missing, is held, and nothing
    else.
    """
    _table_refused(tmp_path, file, edit, check, message)


@pytest.mark.parametrize("case, file, edit, check, message", MALFORMED_RATES,
                         ids=[c[0] for c in MALFORMED_RATES])
def test_an_assumption_table_with_a_value_that_is_not_a_number_is_refused(
        tmp_path, case, file, edit, check, message):
    """A value blank, text, infinite or out of range is refused, naming its lines (T5).

    By the Data cell that checks the table, and by the projection of the committed
    table's first point, in its first month (:func:`_table_refused`), a value no point
    reads included, since a table is checked whole.  So is a run-off that is not a whole
    number of years, 1 or more, by one rule: ``IUL_US_S`` divides by it.  And so is a
    lapse or mortality rate outside 0 to 1, and a class factor, a corridor factor, a
    guaranteed COI rate or a surrender charge below 0, each by the one rule that refuses a
    blank in its column.  ``IUL_US_S`` reads a blank value as a missing one, and so would
    this model's capped mortality, ``min(q, 1.0)``, which written ``min(1.0, q)`` would
    read one as 1.0, every policy in force dying in that month without a word.
    """
    _table_refused(tmp_path, file, edit, check, message)


def _where(column, key_column, key, value):
    """An edit that writes ``value`` into ``column`` of the rows whose key is ``key``."""
    def edit(table):
        cells = table[column].astype(object)
        cells[table[key_column] == key] = value
        return table.assign(**{column: cells})
    return edit


# The bounds of each range, which a table may hold, by file, each read by a committed
# point: a lapse rate of 0 in policy year 2 and of 1 in policy year 3, and a mortality
# rate, a corridor factor and a guaranteed COI rate of 0 at attained age 61, policy year
# 17 of the anchor cell, all read by S's point 2; a class factor of 0 for NT, every
# committed point's class; and a surrender charge of 0 and a run-off of a year on IUL10,
# every point's schedule.  The shipped mortality table reaches 1 at attained age 119.
AT_BOUNDS = {
    "lapse_table.csv": _both(_write_at("lapse_rate_ann", 1, 0.0),
                             _write_at("lapse_rate_ann", 2, 1.0)),
    "mort_table.csv": _where("mort_rate", "age", 61, 0.0),
    "coi_rates.csv": _where("coi_rate_guar", "policy_year", 17, 0.0),
    "corridor_factors.csv": _where("corridor_factor", "age", 61, 0.0),
    "class_factor_table.csv": _where("factor", "rate_class", "NT", 0.0),
    "surr_charge_table.csv": _both(_write_at("sc_per_1000_init", 0, 0.0),
                                   _write_at("runoff_years", 0, 1)),
}


def test_a_rate_or_factor_at_the_bound_of_its_range_is_read(tmp_path):
    """A rate of 0 or 1, and a factor or a charge of 0, are read (T5).

    The ranges ``Data`` holds the tables to are closed: a lapse or mortality rate from 0 to
    1, and a class factor, a corridor factor, a guaranteed COI rate or a surrender charge
    of 0 or more, and a run-off of 1 year or more.  So a copy holding each bound
    (:data:`AT_BOUNDS`) reads, every extent and count as shipped, and the twin of S's point
    2 reads each value as written: a lapse rate of 0 in its second year and of 1 in its
    third, every policy lapsing then; a mortality rate, a COI rate and a corridor factor of
    0 at 61, the option its death benefit and no charge for the insurance; a class factor
    of 0, so no death, and a surrender charge of 0.  Every flow is a finite float.
    """
    folder = temp_inputs(tmp_path, model_path(SEC), edits=AT_BOUNDS)
    model = _read(folder, "bounds_read")
    try:
        assert (model.Data.lapse_last_year(), model.Data.mort_age_last(),
                model.Data.corridor_age_last(), model.Data.class_count(),
                model.Data.surr_charge_count()) == (11, 120, 121, 7, 1)
        p = _row(model, "twin", 2, 0)
        assert (p.lapse_rate_base(12), p.lapse_rate_base(24)) == (0.0, 1.0)
        assert (p.lapse_rate(12), p.lapse_rate(24)) == (0.0, 1.0)
        assert p.pols_lapse(24) == p.pols_if(24) - p.pols_death(24) > 0.0
        assert p.pols_if(25) == 0.0
        t = 12 * (61 - p.age_at_entry())
        assert (p.mort_rate_base_at(61), p.coi_rate_guar_py(17)) == (0.0, 0.0)
        assert (p.corridor_factor_at(61), p.corridor_factor(t), p.coi_rate_guar(t)) == (
            0.0, 0.0, 0.0)
        assert p.db_pp(t) == p.sum_assured_at(t) + p.av_pp_at(t, _code(p, "BEF_FEE"))
        assert (p.class_factor(), p.mort_rate(12), p.pols_death(12)) == (0.0, 0.0, 0.0)
        assert (p.surr_charge_rate_max(), p.surr_charge_runoff_years()) == (0.0, 1.0)
        assert p.surr_charge_rate(0) == 0.0 and p.lapse_shock_year() == 2
        flows = p.result_cf().to_numpy().ravel()
        assert all(type(v) is float and math.isfinite(v) for v in flows.tolist())
    finally:
        model.close()


# A text column IUL_US_S branches on, holding a value its formulas do not know: the decodes
# read it as no known value, and the cell that branches on it raises IUL_US_S's own
# message; and a key a join finds no row for, which IUL_US_S's join raises pandas'
# KeyError on, and this model's names the point and the file.  On S point 2's twin, an
# annual level payer on Option B, so that its mode is decoded, with one column changed.
# (case, column, value, the message SEC raises, what S raises).
UNDECODABLE = [
    ("db_option C", "db_option", "C", "invalid db_option", "invalid db_option"),
    ("qual_test CVAT", "qual_test", "CVAT", "invalid qual_test", "invalid qual_test"),
    ("premium_type LEVELX", "premium_type", "LEVELX", "invalid premium type",
     "invalid premium type"),
    ("premium_mode QUARTERLY", "premium_mode", "QUARTERLY", "invalid premium mode",
     "invalid premium mode"),
    # Each value a decode names, in a case and a whitespace variant, which an exact
    # comparison, S's, reads as no value it knows (USLIB-SEC-PLAN.md §7.3, *For M17 and
    # later*, item 2): a decode that folded case or stripped space would take it.
    *[(f"{column} {value!r}", column, value, message, message)
      for column, message, named in (
          ("db_option", "invalid db_option", ("A", "B")),
          ("qual_test", "invalid qual_test", ("GPT",)),
          ("premium_type", "invalid premium type", ("LEVEL", "SINGLE", "TARGET")),
          ("premium_mode", "invalid premium mode", ("ANNUAL", "MONTHLY")))
      for each in named for value in (each.lower(), each + " ")],
    # Phase 2 joins the class factor and the schedule to the table, refusing at the first
    # read, naming every point; the COI scale by number, refused where read, by the age
    # alone, since a label is a reporting cell's (R17; M19).
    ("rate_class Std", "rate_class", "Std",
     "class_factor_table.csv has no factor for the rate_class of point_id [2]", "KeyError"),
    ("a COI cell the scale lacks", "sex", "F",
     "point_id 2: coi_rates.csv has no rates for its sex, rate_class and age_at_entry 45",
     "KeyError"),
    ("surr_charge_id IUL99", "surr_charge_id", "IUL99",
     "surr_charge_table.csv has no schedule for the surr_charge_id of point_id [2], each "
     "of which has_surr_charge", "KeyError"),
    # Each key the point's joins find, in a case and a whitespace variant, which S's
    # lookups, exact, find no row for (USLIB-SEC-PLAN.md §7.3, *For M17 and later*, item
    # 2): the point's class, its sex in the COI key and its charged schedule.  A join that
    # folded case or stripped space would take it, or refuse it where another join reads.
    *[(f"{column} {value!r}", column, value, message, "KeyError")
      for column, key, message in (
          ("rate_class", "NT",
           "class_factor_table.csv has no factor for the rate_class of point_id [2]"),
          ("sex", "M", "point_id 2: coi_rates.csv has no rates for its sex, rate_class "
                       "and age_at_entry 45"),
          ("surr_charge_id", "IUL10",
           "surr_charge_table.csv has no schedule for the surr_charge_id of point_id [2], "
           "each of which has_surr_charge"))
      for value in (key.lower(), key + " ")],
]


@pytest.mark.parametrize("case, column, value, message, theirs", UNDECODABLE,
                         ids=[c[0] for c in UNDECODABLE])
def test_a_value_no_decode_or_join_knows_is_refused(tmp_path, case, column, value, message,
                                                    theirs):
    """An unknown decode raises ``IUL_US_S``'s message, and a missing join names the point.

    The decodes of each text column compare the text with one value each, so a value none
    of them names reads as no known one, and the cell that branches on them must raise as
    ``IUL_US_S``'s does, rather than take its last branch.  A key the class factors, the
    COI scale or the surrender charge schedules have no row for raises pandas' own
    ``KeyError`` in ``IUL_US_S``, naming neither the point nor the file, and here a
    ``ValueError`` naming both.  The table reads, because the text columns are the
    product's to judge, and the point's first projection raises, in this model as in
    ``IUL_US_S``.
    """
    point = _label(_committed(), "twin", 2, 0)
    model = _read(_sec_inputs(tmp_path / "sec", _set(column, [point], value)(_committed())),
                  "undecodable")
    s = _read(_s_inputs(tmp_path / "s", _set(column, [point], value)(_s_table())),
              "undecodable_s")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_point(model, point).result_cf, message)
        with pytest.raises(Exception) as excinfo:
            _point(s, point).result_cf()
        assert theirs in str(excinfo.value), str(excinfo.value)
    finally:
        s.close()
        model.close()


def test_a_point_without_a_charge_reads_its_schedule_as_at_stage_e(tmp_path):
    """The surrender-charge accessors keep stage ``E``'s value on a point without a charge.

    At stage ``E`` ``surr_charge_rate_max()`` and ``surr_charge_runoff_years()`` joined the
    point's schedule whether or not it carried a charge, and refused an id the table
    lacked with a ``ValueError`` naming the point, though no projection reads either on
    such a point (USLIB-SEC-PLAN.md §7.5, *For M19 and later*, item 1: D2 keeps every
    cell's value, read or not).  So on S point 2's twin made to carry no charge, the two
    read the shipped schedule's $25.00 and 10 years, as stage ``E`` read them, the shock
    year is 0 and every flow is the charged row's but the charge's; and with an id the
    table lacks, the table reads and the point projects, as in ``IUL_US_S``, and each
    accessor raises stage ``E``'s ``ValueError``, naming the point, where its ``.loc`` did,
    the id itself, a label, not quoted (R17).
    """
    point = _label(_committed(), "twin", 2, 0)
    off = _set("has_surr_charge", [point], False)
    model = _read(_sec_inputs(tmp_path / "off", off(_committed())), "no_charge")
    try:
        p = _point(model, point)
        assert (p.has_surr_charge(), p.surr_charge_rate_max(),
                p.surr_charge_runoff_years()) == (False, 25.0, 10.0)
        assert p.lapse_shock_year() == 0 and p.surr_charge_rate(0) == 0.0
        assert model.Data.has_surr_charge_schedule()[_key(model, point)] == 1
    finally:
        model.close()
    unknown = _both(off, _set("surr_charge_id", [point], "IUL99"))
    model = _read(_sec_inputs(tmp_path / "unknown", unknown(_committed())), "no_schedule")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        p = _point(model, point)
        assert len(p.result_cf()) == p.proj_len()
        for cell in (p.surr_charge_rate_max, p.surr_charge_runoff_years):
            _refused_exactly(cell, f"point_id {point}: surr_charge_table.csv has no row "
                                   f"for its surr_charge_id")
    finally:
        model.close()


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses a policy issued later than it, and 0 refuses all.

    The committed table's one future point is issued 25 months on.  It reads at the shipped
    120 months and at 25, the shortest horizon that admits it, where it also projects, its
    frame opening at the valuation date and its policies arriving at ``t = 25``, and it is
    refused at 24, by name.  At 0 the model takes no future new business, D4's fallback for
    a product that cannot support it, and the message says so.  A negative horizon is
    itself refused.  Each value is set on a model just read, before its table is.
    """
    future = _label(_committed(), "future", 4, -25)
    later = (f"{TABLE}: duration_mth must be -24 or more, a policy issued at most 24 "
             f"months after the valuation date; it is not at point_id [{future}]")
    no_future = (f"{TABLE}: duration_mth must be 0 or more: this model takes no future new "
                 f"business; it is not at point_id [{future}]")
    negative = "future_horizon_mth must be 0 months or more, not -1"
    folder = _sec_inputs(tmp_path, _committed())
    for horizon, refusal in ((None, None), (25, None), (24, later), (0, no_future),
                             (-1, negative)):
        model = _read(folder, "horizon",
                      data=None if horizon is None else {"future_horizon_mth": horizon})
        try:
            if horizon is None:
                assert model.Data.future_horizon_mth == 120
            if refusal is None:
                assert len(model.Data.model_point_table()) == len(_committed()), horizon
            else:
                _refused_exactly(model.Data.model_point_table, refusal)
            if horizon == 25:
                p = _point(model, future)
                assert len(p.result_cf()) == p.proj_len() == 937
                assert p.pols_new_biz(25) == p.policy_count()
        finally:
            model.close()


def _run_sec(script, *args, check=True):
    """Run ``script``, a ``run_sec.py``, with ``args``; its output, checked ASCII.

    With ``check=False`` the finished process is returned instead, whatever its exit code,
    for a test that expects the runner to fail.
    """
    done = subprocess.run([sys.executable, str(script), *args], capture_output=True,
                          timeout=600)
    if not check:
        return done
    assert done.returncode == 0, done.stderr.decode(errors="replace")
    assert done.stdout.isascii(), "run_sec.py printed a non-ASCII character"
    # Windows ends each printed line with "\r\n"; read them as "\n", as a frame's
    # to_string() writes them.
    return done.stdout.decode("ascii").replace("\r\n", "\n")


_PAST_AGE = ("point_id {point}: age_at_entry {age} is at or past maturity_age, 121: a "
             "policy issued there would never be in cover")
_PAST_END = ("point_id {point}: duration_mth {d} is at or past the end of the projection, "
             "policy month 912, attained age 121")
_BELOW_FEE = ("point_id {point}: wd_pp {wd} is above 0 and below wd_fee, {fee}: a "
              "withdrawal pays its fee out of itself, so it must be at least the fee")
_HELD = ("point_id {point}: inforce_segments_sec.csv holds {held} segments, its last in "
         "slot {last}, where a policy in force {months} months holds one a month for its "
         "last {want}, slots 1 to {want}")


def _ladder_without(point, slot, moved_to_fa):
    """A table and ladder edit: ``point``'s ``slot`` dropped from the ladder and, where
    ``moved_to_fa``, its balance moved into the point's fixed account, so that ``Data``'s
    identity holds and ``proj_len()`` alone refuses the ladder."""
    ladder = _committed_ladder()
    gone = (ladder["point_id"] == point) & (ladder["slot"] == slot)
    balance = float(ladder.loc[gone, "seg_bal_pp_init"].iloc[0])
    table = _committed()
    if moved_to_fa:
        table = _set("fa_pp_init", [point], table.at[point, "fa_pp_init"] + balance)(table)
    return table, ladder[~gone]


def _ladder_with(point, slot, inputs=None):
    """The committed table and the ladder, or ``inputs``, a table and a ladder, with an
    empty row added for ``point`` at ``slot``, its start level and cap its first row's."""
    table, ladder = inputs or (_committed(), _committed_ladder())
    row = ladder[ladder["point_id"] == point].iloc[[0]].assign(
        slot=slot, seg_bal_pp_init=0.0, seg_ded_cum_pp_init=0.0, seg_wd_cum_pp_init=0.0)
    return table, pd.concat([ladder, row], ignore_index=True)


# The refusals of proj_len(), in the order it checks them, as (case, the table and ladder,
# the point it refuses, its message, the References read with it, those under which the
# same point projects, and whether the runner is run on it): the future row issued at
# attained age 121, maturity_age, so that no month of its frame is in cover, and at 122,
# 25 months on and 5 months on, where the frame itself would end before the valuation
# date, so that the age is checked first and its message names the age, not a policy
# month below 0; the row of S point 1 at 888 moved to the month the projection ends,
# policy month 912 at attained age 121, and a year past it; the row of S point 5 at 6
# withdrawing a cent below its fee, half its fee, a cent, just inside the window's other
# end, and its own $25.00 under a fee moved to $30.00; and the ladder's count: a slot more
# than twelve on the row of S point 1 at 60, its slot 1 missing, and its slot 1 missing
# with a slot 13 held, twelve rows on the wrong slots, which Data's slot rule accepts, its
# balance in the fixed account, the maturing
# segment missing from the row of S point 4 at 65, its balance in the fixed account, and
# the row of S point 5 at 6 holding five of its six months.  Then the order: the row at
# 888 moved to the end of the projection withdrawing half its fee, refused as past the
# end, and the row of S point 5 at 6 withdrawing half its fee with a month of its ladder
# missing, refused for the withdrawal.  Each needs a Projection Reference, maturity_age,
# wd_fee or seg_term_mth, and the ages past 121 issue_age_max too (M19), so the
# table reads; each is read with the Reference moved past it, where the same point
# projects (USLIB-SEC-PLAN.md §7.7, Record — M9, Rules on a Reference), but those whose
# ladder no Reference would make whole.  The windows' other sides are accepted elsewhere:
# the row restated at 911, the last covered month; a withdrawal at its fee, and of 0 on
# every committed row but those of S point 5; and a point
# issued at attained age 120 (test_a_point_issued_at_attained_age_120_has_a_year_of_cover).
NOT_ISSUED = [
    ("issued at attained age 121", lambda: (_set("age_at_entry", [12], 121)(_committed()),
                                            None), 12,
     _PAST_AGE.format(point=12, age=121), {}, {"maturity_age": 122, "issue_age_max": 121},
     True),
    ("issued past attained age 121", lambda: (_set("age_at_entry", [12], 122)(
        _committed()), None), 12, _PAST_AGE.format(point=12, age=122), {},
     {"maturity_age": 123, "issue_age_max": 122}, False),
    ("issued past attained age 121 within a year",
     lambda: (_both(_set("age_at_entry", [12], 122), _set("duration_mth", [12], -5))(
         _committed()), None), 12, _PAST_AGE.format(point=12, age=122), {},
     {"maturity_age": 123, "issue_age_max": 122}, False),
    ("at the end", lambda: (_set("duration_mth", [11], 912)(_committed()), None), 11,
     _PAST_END.format(point=11, d=912), {}, {"maturity_age": 122}, True),
    ("past the end", lambda: (_set("duration_mth", [11], 924)(_committed()), None), 11,
     _PAST_END.format(point=11, d=924), {}, {"maturity_age": 123}, False),
    ("a withdrawal a cent below its fee", lambda: (_set("wd_pp", [8], 24.99)(_committed()),
                                                   None), 8,
     _BELOW_FEE.format(point=8, wd=24.99, fee=25.0), {}, {"wd_fee": 20.0}, True),
    ("a withdrawal of half its fee", lambda: (_set("wd_pp", [8], 12.5)(_committed()),
                                              None), 8,
     _BELOW_FEE.format(point=8, wd=12.5, fee=25.0), {}, {"wd_fee": 12.5}, False),
    ("a withdrawal of a cent", lambda: (_set("wd_pp", [8], 0.01)(_committed()), None), 8,
     _BELOW_FEE.format(point=8, wd=0.01, fee=25.0), {}, {"wd_fee": 0.01}, False),
    ("a withdrawal at the fee, the fee moved past it",
     lambda: (_set("wd_pp", [8], 25.0)(_committed()), None), 8,
     _BELOW_FEE.format(point=8, wd=25.0, fee=30.0), {"wd_fee": 30.0}, {"wd_fee": 25.0},
     False),
    ("a slot more than twelve", lambda: _ladder_with(6, 13), 6,
     _HELD.format(point=6, held=13, last=13, months=60, want=12), {},
     {"seg_term_mth": 13}, True),
    ("its slot 1 missing", lambda: _ladder_without(6, 1, False), 6,
     _HELD.format(point=6, held=11, last=12, months=60, want=12), {}, None, False),
    ("the maturing segment missing", lambda: _ladder_without(7, 12, True), 7,
     _HELD.format(point=7, held=11, last=11, months=65, want=12), {}, None, False),
    ("a month of the first year missing", lambda: _ladder_without(8, 6, True), 8,
     _HELD.format(point=8, held=5, last=5, months=6, want=6), {}, None, False),
    ("its slot 1 missing and a slot 13 held",
     lambda: _ladder_with(6, 13, _ladder_without(6, 1, True)), 6,
     _HELD.format(point=6, held=12, last=13, months=60, want=12), {}, None, False),
    ("at the end, withdrawing half its fee",
     lambda: (_both(_set("duration_mth", [11], 912), _set("wd_pp", [11], 12.5))(
         _committed()), None), 11, _PAST_END.format(point=11, d=912), {}, None, False),
    ("withdrawing half its fee, a month of the ladder missing",
     lambda: (_set("wd_pp", [8], 12.5)(_ladder_without(8, 6, True)[0]),
              _ladder_without(8, 6, True)[1]), 8,
     _BELOW_FEE.format(point=8, wd=12.5, fee=25.0), {}, None, False),
]


@pytest.mark.parametrize("case, inputs, point, message, refs, moved, run", NOT_ISSUED,
                         ids=[c[0] for c in NOT_ISSUED])
def test_a_point_past_its_cover_or_its_ladder_is_refused_by_proj_len(tmp_path, case, inputs,
                                                                   point, message, refs,
                                                                   moved, run):
    """A point with no month in cover, a withdrawal below its fee or a short ladder is
    refused, by name.

    A point at or past the end of the projection has no frame; one issued at or past the
    age the projection ends at, 121, would have a frame with no month in cover; one
    withdrawing less than the withdrawal fee pays the fee out of nothing, where
    ``IUL_US_S`` projects it and its own roll-forward and margin checks fail; and one in
    force whose ladder does not hold a row for each of its last ``min(12, duration_mth)``
    months opens with segments missing or ones that matured.  Each is a rule of the
    product, not of the table: it needs ``maturity_age``, ``wd_fee`` or ``seg_term_mth``, a
    Projection Reference, so the table and the ladder read, and the point is refused where
    its frame is defined, on its first projection, rather than projecting nothing or the
    wrong policy.  Each rule is stated on its Reference: with the Reference moved past the
    point, set first, the same point projects, and with ``wd_fee`` moved to $30.00 a
    withdrawal of $25.00 is refused, naming the Reference's value.  A loop over the block
    would meet the point only when it reached it, after projecting the points before it,
    so ``run_sec.py --block``, run beside the table at the shipped References, asks every
    point for its frame first: it fails naming the point, and prints nothing before.  And
    a ladder's segments, read before the frame is asked for, are refused by the same name,
    since each reader of the ladder asks ``proj_len()`` first, where a slot it lacks would
    otherwise raise pandas' ``KeyError``, naming no point.
    """
    table, ladder = inputs()
    folder = _sec_inputs(tmp_path, table, ladder=ladder)
    model = _read(folder, "past", refs)
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        assert len(model.Data.inforce_segments()) == (
            len(_committed_ladder()) if ladder is None else len(ladder))
        _refused_exactly(_point(model, point).proj_len, message)
        _refused(_point(model, point).result_cf, message)
        if "segments" in message:
            _refused(lambda: _point(model, point).seg_bal_tot_pp(0), message)
    finally:
        model.close()
    if moved is not None:
        model = _read(folder, "past_moved", moved)
        try:
            p = _point(model, point)
            assert p.proj_len() > 0 and len(p.result_cf()) == p.proj_len()
        finally:
            model.close()
    if not run:
        return
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert message in done.stderr.decode(errors="replace")


def test_a_point_issued_at_attained_age_120_has_a_year_of_cover(tmp_path):
    """The age rule's window is accepted just outside it: a point issued at 120 projects.

    ``proj_len()`` refuses a point to be issued at or past attained age 121, where the
    projection ends; one to be issued at 120, the last age with cover, is a policy, and is
    read (USLIB-SEC-PLAN.md §5.2, T5, each rule refused just inside its window and accepted
    just outside).  The committed table's future row, issued 25 months on, with its issue
    age at 120, on a COI scale given a cell for it: its frame is 37 months, its cover the
    12 from ``t = 25``, its policies arrive then as new business, the table's rate of 1.0 at
    attained age 120 ends every one of them in that month, and every flow is a finite
    float, zero outside cover.  The contract issues to age 85, which Phase 2's
    ``proj_len()`` refuses past, ``issue_age_max``; this test raises that Reference to 120
    first, C1's one departure from call syntax (M19).
    """
    committed = _committed()
    future = _label(committed, "future", 4, -25)

    def coi(rates):
        cell = rates[rates["policy_year"] == 1].assign(age_at_entry=120,
                                                       provenance="test copy")
        return pd.concat([rates, cell], ignore_index=True).sort_values(
            COI_KEYS, ignore_index=True)

    model = _read(_sec_inputs(tmp_path, _set("age_at_entry", [future], 120)(committed),
                              edits={"coi_rates.csv": coi}), "issued_at_120",
                  {"issue_age_max": 120})
    try:
        p = _point(model, future)
        assert (p.maturity_mth(), p.proj_len(), p.t_entry()) == (12, 37, 25)
        assert [t for t in range(p.proj_len()) if p.is_active(t)] == list(range(25, 37))
        assert (p.pols_new_biz(25), p.pols_if(25), p.mort_rate(25)) == (1.0, 1.0, 1.0)
        assert p.pols_death(25) == p.pols_if(25) and p.pols_if(26) == 0.0
        flows = p.result_cf()
        assert len(flows) == 37 and (flows.loc[:24] == 0.0).all().all()
        assert all(type(v) is float and math.isfinite(v)
                   for v in flows.to_numpy().ravel().tolist())
    finally:
        model.close()


# The key columns of every keyed table, which the edges test writes as floats, 61.0 for
# 61, as a spreadsheet can save them, and the run-off, a whole number of years; and the
# extents Data reads from them.
FLOAT_KEYS = {"lapse_table.csv": ("policy_year",), "corridor_factors.csv": ("age",),
              "mort_table.csv": ("age",),
              "coi_rates.csv": ("age_at_entry", "policy_year"),
              "surr_charge_table.csv": ("runoff_years",)}
EXTENTS = ("lapse_last_year", "corridor_age_first", "corridor_age_last", "mort_age_first",
           "mort_age_last")
INT_COLUMNS = ("duration_mth", "age_at_entry", "wd_first_year", "loan_first_year",
               "is_mec_init")


def _as_floats(columns):
    """An edit that writes the table's ``columns`` as floats."""
    def edit(table):
        return table.assign(**{column: table[column].astype(float) for column in columns})
    return edit


def test_the_edges_of_the_in_force_interface_are_accepted(tmp_path):
    """A zero count, whole numbers in any type, and the state's and the ladder's edges.

    One copy of the committed table and ladder, edited at the edges a real extract
    reaches, is read beside a copy of every keyed table with its keys written as floats,
    61.0 for 61, as a spreadsheet can save them (:data:`FLOAT_KEYS`), and again beside the
    tables as shipped, so that every table is read:

    * ``Data`` reads each key by value, so every extent is the one read beside the tables
      as shipped, an int, the COI cells' last years are the shipped ones, and the twins of
      S's points 1 and 5, the row of S point 5 at 384 and the row issued 120 months on,
      which between them read every table, project exactly what they project beside the
      tables as shipped;
    * the table's integer columns written as floats (:data:`INT_COLUMNS`) are whole numbers
      read back as the ints the clocks count in, and the MEC latch as its code;
    * an exhausted account, its fixed account and its account value below 0, and a face in
      force of 0 are a policy in force, which ``IUL_US_S`` carries;
    * a premium load of 1 and of 0, a share at each of its bounds, is read as written;
    * a count of 0 is a point that projects zeros;
    * the accumulator a cent and a half past the premiums paid, the 7-pay test passing on
      its limit in the first month, and failing in the eighth policy year, outside the
      7-pay years, each with no latch;
    * a segment balance at ``-1e-8``, ``IUL_US_S``'s tolerance, and the account value's
      identity off by seven and a half cents, inside its slack of eight on twelve
      segments, which half a cent past it refuses (:data:`MALFORMED_LADDER`);
    * a withdrawal at its fee;
    * and a policy issued 120 months after the valuation date, the shipped
      ``future_horizon_mth``, is the last one the table admits, with a frame of 1,032
      months, 912 of cover after 120 before issue.
    """
    committed = _committed()
    zero = _label(committed, "derived", 4, 65)
    full_load = _label(committed, "derived", 1, 60)
    no_load = _label(committed, "twin", 4, 0)
    loaned, exhausted = _label(committed, "derived", 5, 384), _label(committed, "derived",
                                                                     5, 605)
    future = _label(committed, "future", 4, -25)
    restated = _label(committed, "derived", 5, 6)
    late, first = _label(committed, "twin", 3, 0), _label(committed, "twin", 2, 0)
    probes = [_label(committed, "twin", p, 0) for p in (1, 5)] + [loaned, future]
    edited = _both(
        _set("policy_count", [zero], 0.0), _set("load_prem_rate", [full_load], 1.0),
        _set("load_prem_rate", [no_load], 0.0),
        _set("sum_assured_init", [exhausted], 0.0),
        lambda t: _set("cum_prem_net_init", [full_load],
                       t.at[full_load, "cum_prem_init"] + 0.015)(t),
        _set("wd_pp", [restated], 25.0),
        _in_force_at(first, 1, cum_prem_init=21000.0, cum_prem_net_init=21000.0),
        _in_force_at(late, 85, cum_prem_init=147000.01, cum_prem_net_init=147000.01),
        _as_floats(INT_COLUMNS), _set("duration_mth", [future], -120.0))(committed)
    ladder = _committed_ladder()
    ladder = _ladder_at(2, "seg_bal_pp_init", -1e-8)(ladder)
    ladder = _ladder_at(14, "seg_bal_pp_init", ladder.at[12, "seg_bal_pp_init"] + 0.075)(
        ladder)
    floats = _sec_inputs(tmp_path / "floats", edited, ladder=ladder, edits={
        file: _as_floats(columns) for file, columns in FLOAT_KEYS.items()})
    for file, columns in FLOAT_KEYS.items():
        written = pd.read_csv(floats.parent / file)
        assert all(written[c].dtype == float for c in columns), file
    shipped = _sec_inputs(tmp_path / "shipped", edited, ladder=ladder)
    model = _read(floats, "edges")
    plain = _read(shipped, "edges_shipped")
    try:
        for cell in EXTENTS:
            value = model.Data.cells[cell]()
            assert (type(value), value) == (int, plain.Data.cells[cell]()), cell
        assert model.Data.coi_schedules() == plain.Data.coi_schedules()
        got, want = model.Data.coi_rate_last_years(), plain.Data.coi_rate_last_years()
        assert np.array_equal(got, want) and got.dtype == "int64"
        read = model.Data.model_point_table()
        assert all(read[column].dtype == float for column in INT_COLUMNS)
        assert len(model.Data.inforce_segments()) == len(ladder)
        for label in probes:
            mine, base = _point(model, label), _point(plain, label)
            for report in REPORTS:
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=0, atol=0) == [], (label, report)
        p = _point(model, loaned)
        assert [(type(v), v) for v in (p.duration_mth(0), p.age_at_entry(),
                                       p.wd_first_year(), p.loan_first_year())] == [
            (int, 384), (int, 45), (int, 2), (int, 21)]
        assert (type(p.is_mec_init()), p.is_mec_init()) == (bool, False)
        assert p.fa_pp_init() < 0.0 < p.av_pp_init() and p.lca_pp_init() > 0.0
        p = _point(model, exhausted)
        assert p.av_pp_init() < 0.0 and p.sum_assured_init() == 0.0
        assert p.sum_assured_at(0) == 0.0 and p.proj_len() == 307
        p = _point(model, full_load)
        assert p.load_prem_rate() == 1.0 and p.prem_to_av_pp(0) == 0.0 < p.premium_pp(0)
        assert p.cum_prem_net_init() == pytest.approx(p.cum_prem_init() + 0.015, abs=1e-9)
        p = _point(model, no_load)
        assert p.load_prem_rate() == 0.0 and p.prem_to_av_pp(0) == p.premium_pp(0) > 0.0
        p = _point(model, zero)
        df = p.result_cf()
        assert len(df) == 847 and (df == 0.0).all().all()
        p = _point(model, restated)
        assert p.wd_pp(6) == p.wd_fee_pp(6) == 25.0 and p.proj_len() == 906
        assert p.claim_pp(6, _code(p, "WITHDRAWAL")) == 0.0
        p = _point(model, future)
        assert (p.t_entry(), p.proj_len(), p.pols_new_biz(120)) == (120, 1032, 1.0)
        assert (read.at[first, "is_mec_init"], read.at[late, "is_mec_init"]) == (0.0, 0.0)
    finally:
        plain.close()
        model.close()


# Each spelling of a flag Data accepts: True and False in any case, which pandas reads as
# the bools.
SPELLINGS = {True: ("TRUE", "true", "tRuE"), False: ("FALSE", "false", "FaLsE")}


def _respelled(table):
    """``table`` with ``has_surr_charge`` written as text, each value's spellings of
    :data:`SPELLINGS` taken in turn, row by row."""
    turns = {True: itertools.count(), False: itertools.count()}
    words = [SPELLINGS[bool(v)][next(turns[bool(v)]) % 3] for v in table["has_surr_charge"]]
    return table.assign(has_surr_charge=words)


@pytest.mark.sec_full
@pytest.mark.skipif(not SEC_FULL, reason="the flag spellings run with USLIB_SEC_FULL=1 "
                    "(USLIB-SEC-PLAN.md K6)")
def test_a_flag_reads_the_same_in_every_spelling_data_accepts(tmp_path):
    """The flag decodes, and projects, as written in every spelling ``Data`` accepts.

    ``Data`` accepts ``has_surr_charge`` written ``True`` or ``False`` in any case, which
    pandas reads as the bools, and refuses a blank, any other text and any number, 1, 0,
    1.0 and 0.0 among them (:data:`MALFORMED`).  The model decodes the flag with
    ``IUL_US_S``'s ``bool()``, which reads any text but the empty string as true, so a
    spelling pandas left as text would project a point with no surrender charge as one with
    it (USLIB-SEC-PLAN.md §7.8, Record — M10, Flag spellings).  So the committed table,
    with the surrender charge taken off the twins of S points 2, 3 and 4, so that the flag
    is False on three rows, is read as written and again with the flag in a spelling of
    :data:`SPELLINGS`, each taken in turn (:func:`_respelled`), every one of the six in the
    file: ``Data`` reads the flag as bools, the same in both, every row decodes it the same,
    and the twins of S points 1 and 2, which read a True and a False, project the same
    four reports, bit for bit.  It runs with ``USLIB_SEC_FULL=1`` only (USLIB-SEC-PLAN.md
    K6, weighed at M13): :data:`MALFORMED` refuses every other spelling by default, and a
    flag read as text would part variant 11's twin, the core's one False, from S in T2.
    """
    committed = _committed()
    twins = {p: _label(committed, "twin", p, 0) for p in (1, 2, 3, 4)}
    table = _set("has_surr_charge", [twins[2], twins[3], twins[4]], False)(committed)
    spelled = _respelled(table)
    models = {}
    try:
        for tag, written in (("written", table), ("spelled", spelled)):
            models[tag] = _read(_sec_inputs(tmp_path / tag, written), f"flags_{tag}")
        text = (tmp_path / "spelled" / TABLE).read_text()
        assert all(f",{word}," in text for words in SPELLINGS.values() for word in words), (
            text[:400])
        base, respelled = models["written"], models["spelled"]
        want, got = (m.Data.model_point_table()["has_surr_charge"] for m in (base,
                                                                              respelled))
        assert want.dtype == bool and got.equals(want), got
        for key, other in zip(point_keys(respelled), point_keys(base)):
            mine, theirs = projection(respelled, key), projection(base, other)
            assert (type(mine.has_surr_charge()), mine.has_surr_charge()) == (
                bool, theirs.has_surr_charge()), key
        for point in (1, 2):
            mine, theirs = _point(respelled, twins[point]), _point(base, twins[point])
            for report in REPORTS:
                assert frame_mismatches(theirs.cells[report](), mine.cells[report](),
                                        rtol=0, atol=0) == [], (point, report)
    finally:
        for model in models.values():
            model.close()


# ---------------------------------------------------------------------------
# The product's own facts, on models read for the test


def test_expense_inflation_runs_on_the_valuation_clock(tmp_path):
    """Maintenance is in valuation-date dollars, for every point alike (D7).

    ``IUL_US_S`` inflates its maintenance expense by policy year,
    ``(1 + inflation_rate)^(policy_year - 1)``; this model by valuation year,
    ``(1 + inflation_rate)^(t // 12)``, so every point of a block steps on the valuation
    anniversaries.  ``IUL_US_S`` ships inflation at 0, which hides the clock, so both models
    are read with :data:`INFLATION` set first.  Then on every committed row the factor is
    ``(1 + INFLATION)^(t // 12)`` at every month of its frame and the month after it; on the
    twins of S's new business, where the two clocks coincide, the expenses are S's bit for
    bit; and on the rows restated or issued later, S's month ``s`` and this model's month
    ``t`` of the same instant, ``s = t + source_mth``, part by ``1.025`` to the policy years
    S has counted that the valuation years have not, ``(s // 12) - (t // 12)``: on the row
    of S point 4 at 65, mid-year, five steps for ``t = 0..6`` and six for ``t = 7..11``,
    where S has stepped at the policy anniversary and this model has not, and five again at
    ``t = 12``; on the row issued 25 months on, two or three steps fewer, the valuation
    years that had passed before its issue.  The maintenance per policy in force is held so
    in every month a policy is in force in both models after the first, which bears
    acquisition, to 1e-12; every other cell is S's (T2).
    """
    refs = {"inflation_rate": INFLATION}
    sec = _read(model_path(SEC), "inflation", refs)
    s = _read(model_path(TWIN), "inflation_s", refs)
    try:
        table = sec.Data.model_point_table()
        s_points = {policy: point for point, policy
                    in s.Data.model_point_table()["policy_id"].items()}
        steps_at = {}
        for point_id in table.index:
            p = _point(sec, point_id)
            assert all(p.inflation_factor(t) == (1 + INFLATION) ** (t // 12)
                       for t in range(p.proj_len() + 1)), point_id
            month = int(table.at[point_id, "source_mth"])
            sp = _point(s, s_points[table.at[point_id, "source_policy_id"]])
            if table.at[point_id, "row_kind"] == "twin":
                assert [p.expenses(t) for t in range(p.proj_len())] == [
                    sp.expenses(t) for t in range(sp.proj_len())], point_id
                continue
            for t in range(p.t_entry(), min(p.proj_len(), p.t_entry() + 120)):
                u = t + month
                if p.policy_year(t) < 2 or not (p.pols_if(t) > 0.0 and sp.pols_if(u) > 0.0):
                    continue
                steps_at[point_id, t] = steps = u // 12 - t // 12
                assert sp.expenses(u) / sp.pols_if(u) == pytest.approx(
                    p.expenses(t) / p.pols_if(t) * (1 + INFLATION) ** steps,
                    rel=1e-12), (point_id, t)
        mid = _label(table, "derived", 4, 65)
        assert [steps_at[mid, t] for t in range(13)] == [5] * 7 + [6] * 5 + [5]
        later = _label(table, "future", 4, -25)
        assert [steps_at[later, 25 + u] for u in range(12, 24)] == [-2] * 11 + [-3]
    finally:
        s.close()
        sec.close()


def test_a_residual_that_is_not_a_number_fails_its_check():
    """A check whose residual is not a number fails, as ``IUL_US_S``'s ``isclose`` does.

    The checks are the model's one guard against a value that is not a number: the floors
    at zero of the cash value and the segments' pool, and the maxes of the death benefit
    and the net amount at risk, turn a NaN into a number, so the cash flows can stay
    numbers.  On models just read, with a Reference set to NaN before anything is
    computed, which runs compiled as it runs here (USLIB-SEC-PLAN.md §7.12, *Record —
    M12*), the NaN is sent through one the counts read and through one that reaches the
    residuals without them (§7.8, *Record — M10*, *NaN checks*):

    * ``expense_unit_mth_2``, the per-unit charge from policy year 11, which reaches the
      deduction, and through it the accounts, the segments and the counts' lapses, from
      ``t = 120``: on the twins of S's points 1 and 4 every residual is within its
      tolerance before ``t = 120`` and the account value's, the components', the margin's
      and the segment balances' NaN from it, and all four checks ``False``, as S's are; a
      segment's balance NaN fails ``check_seg_bal_resid`` through its own test, which keeps
      a NaN;
    * ``fixed_rate_curr``, the fixed account's declared rate, which reaches its interest
      and no count, the cash value's floor at 0 turning the account value's NaN into a
      number: on S's point 4's twin and the row of S point 4 at 65 the account value's,
      the components' and the margin's residuals are NaN from ``t = 0``, and on the row
      issued 25 months on 0.0 before its issue and NaN from it, while every count stays a
      number; the checks decide as S's do.

    A check that asked whether the residual is above its tolerance would pass each of them,
    since no comparison with NaN holds, so each loop stops at ``not abs(r) <= 1e-9``, or
    ``not r >= -1e-8`` for the segments' balances.
    """
    models = {}
    try:
        for ref in ("expense_unit_mth_2", "fixed_rate_curr"):
            for name in (SEC, TWIN):
                models[ref, name] = _read(model_path(name), f"nan_{ref}",
                                          {ref: float("nan")})
        sec, s = models["expense_unit_mth_2", SEC], models["expense_unit_mth_2", TWIN]
        for point in (1, 4):
            p = _row(sec, "twin", point, 0)
            months = range(p.proj_len())
            for resid in ("check_av_components_resid", "check_av_roll_fwd_resid",
                          "check_margin_resid"):
                values = [p.cells[resid](t) for t in months]
                assert all(abs(r) <= 1e-9 for r in values[:120]), (point, resid)
                assert any(math.isnan(r) for r in values[120:]), (point, resid)
            assert all(p.check_seg_bal_resid(t) >= -1e-8 for t in range(120)), point
            assert any(math.isnan(p.check_seg_bal_resid(t)) for t in months), point
            assert tuple(p.cells[c]() for c in CHECKS) == (False,) * 4, point
            sp = _point(s, point)
            assert tuple(sp.cells[c]() for c in CHECKS) == (False,) * 4, point
        sec, s = models["fixed_rate_curr", SEC], models["fixed_rate_curr", TWIN]
        for case in (("twin", 4, 0), ("derived", 4, 65)):
            p = _row(sec, *case)
            months = range(p.proj_len())
            for resid in ("check_av_components_resid", "check_av_roll_fwd_resid",
                          "check_margin_resid"):
                assert math.isnan(p.cells[resid](0)), (case, resid)
            assert all(math.isfinite(p.pols_if(t)) for t in months), case
            verdicts = tuple(p.cells[c]() for c in CHECKS)
            assert verdicts[:2] == (False, False) and verdicts[3] is False, (case, verdicts)
        sp = _point(s, 4)
        assert (sp.check_av_components(), sp.check_av_roll_fwd(), sp.check_margin()) == (
            False, False, False)
        p = _row(sec, "future", 4, -25)
        values = [p.check_av_roll_fwd_resid(t) for t in range(p.proj_len())]
        assert values[:25] == [0.0] * 25 and math.isnan(values[25])
        assert all(math.isfinite(p.pols_if(t)) for t in range(p.proj_len()))
    finally:
        for model in models.values():
            model.close()


# The point at which IUL's annual lapse rate passes 1: S's point 1 paying $1,000 a year,
# whose guarantee holds in policy months 0 and 1 alone, and whose cash value is 0 at its
# expiry, policy month 240, where the expiry shock returns nlg_shock_lapse before the cap;
# at 1.2, set first, the rate is 1.2 there.  None of S's five points takes the shock.
SHOCKED = {"premium_pp_ann": 1000.0}
LAPSE_PAST_1 = {"nlg_shock_lapse": 1.2}


def test_a_lapse_rate_past_1_makes_each_check_raise_as_in_iul_us_s(tmp_path):
    """Past 1 the monthly lapse rate is complex, and the checks it reaches raise, in both.

    ``IUL_US_S`` caps its lapse rate at ``lapse_rate_cap``, 1.0 as shipped, but returns the
    no-lapse guarantee's expiry shock, ``nlg_shock_lapse``, before the cap, and that is a
    Reference nothing refuses.  On S's point 1 paying $1,000 a year (:data:`SHOCKED`),
    whose cash value is 0 at its guarantee's expiry, a shock of 1.2, set before anything is
    computed (:data:`LAPSE_PAST_1`), takes the annual rate to 1.2 in policy month 240, where
    ``1 - (1 - q)^(1/12)`` has no real value, and every count after it is complex.
    ``IUL_US_S``'s ``math.isclose`` raises ``TypeError`` on it, and this model's account
    value's and margin's residuals are each a ``float`` of their ratio, so they raise too,
    where a residual left complex would pass its check on its magnitude, a real number.
    The components' check and the ladder's read no count, and hold in both.  The point is
    the twin of the S point, built by the generator from an S read with the shock set.
    """
    s = _read(_s_inputs(tmp_path / "s", _s_table().loc[[1]].assign(**SHOCKED)),
              "lapse_past_1_s", LAPSE_PAST_1)
    sec = None
    try:
        table, ladder = build_sec_table(dataclasses.replace(SPEC, derived=(), future=()), s)
        sec = _read(_sec_inputs(tmp_path / "sec", table, ladder=ladder[LADDER]),
                    "lapse_past_1", LAPSE_PAST_1)
        for x in (_point(sec, 1), _point(s, 1)):
            assert x.nlg_expiry_shock(240) and x.ncsv_pp(240) == 0.0
            assert (type(x.lapse_rate(240)), x.lapse_rate(240)) == (float, 1.2)
            assert type(x.lapse_rate_mth(240)) is complex
            assert type(x.pols_if(240)) is float and type(x.pols_if(241)) is complex
            for check in ("check_av_roll_fwd", "check_margin"):
                with pytest.raises(Exception) as excinfo:
                    x.cells[check]()
                text = str(excinfo.value)
                assert "TypeError" in text and "complex" in text, (x.name, check, text)
            assert x.check_av_components() is True and x.check_seg_ladder() is True
    finally:
        if sec is not None:
            sec.close()
        s.close()


# How far each check's two sides are moved apart, and whether every check then passes:
# inside the checks' absolute tolerance, 1e-8, and outside it wherever the sides are below
# 10, where the relative tolerance's 1e-9 of 10 is that 1e-8.
CHECK_MISSES = {5e-9: True, 2e-8: False}


def _moved(model, cell, formula):
    """Give ``cell`` of ``model``'s Projection ``formula``, its own kept in a new cell.

    The new cell is ``<cell>_unmoved``, which ``formula`` may call.  A formula override
    through a new cell, so modelx's alone (C1), set before anything is computed.
    """
    proj = model.Projection
    proj.new_cells(name=f"{cell}_unmoved", formula=proj.cells[cell].formula.source)
    proj.cells[cell].formula = formula


def test_each_check_decides_as_isclose_does_where_its_sides_are_small(tmp_path):
    """Each check decides as ``IUL_US_S``'s ``isclose`` does, where its sides are small.

    ``IUL_US_S`` asks ``isclose`` with a relative tolerance of ``1e-9`` and an absolute one
    of ``1e-8``, which holds where the two sides differ by at most ``1e-9`` times the
    larger of them, or ``1e-8``.  ``IUL_US_SEC`` divides each month's difference by the
    larger of the two and 10 and asks whether the residual is within ``1e-9``, which is the
    same test through the floor of 10: over the larger side alone, a miss inside the
    absolute tolerance fails where the sides are below 10, and over a floor above 10 a miss
    outside it passes.  So, in both models, on models just read, the investment income in
    force, which only the account value's roll-forward and the margin identity read, is
    moved by each miss of :data:`CHECK_MISSES` in every month of the twin of S's point 1,
    whose sides are 0 from attained age 119, where the table's rate of 1.0 ends every
    policy; and both checks of each model pass the miss of ``5e-9`` and fail the one of
    ``2e-8``, the floor of 10 winning in each residual (:class:`_BoundSides`), where the
    check that passes reads every month: the one that fails stops at the first month whose
    residual is past its tolerance, where the sides are below 20.  The account value's
    components and the ladder's closure take the same floor, written alike; no shipped
    point brings both sides of the components' identity below 10 in one month, so neither
    is moved here, but on a row of the test's own, in the test after this one.
    """
    floors, won = set(), set()
    for miss, passes in CHECK_MISSES.items():
        models = []
        try:
            for name in (SEC, TWIN):
                model = _read(model_path(name), "moved_credit")
                _moved(model, "inv_income", f"lambda t: inv_income_unmoved(t) + {miss!r}")
                models.append(model)
            p, sp = _row(models[0], "twin", 1, 0), _point(models[1], 1)
            assert p.pols_if(889) == 0.0 and p.av_at(889, _code(p, "BEF_PREM")) == 0.0
            bounds = _BoundSides(models[0])
            with bounds.watch() as these:
                verdicts = tuple(p.cells[check]() for check in ("check_av_roll_fwd",
                                                                "check_margin"))
            won |= these
            floors |= {side for side in bounds.sides if side[2] == 2 and side[0] in (
                "check_av_roll_fwd_resid", "check_margin_resid")}
            assert verdicts == (passes, passes), miss
            assert (sp.check_av_roll_fwd(), sp.check_margin()) == (passes, passes), miss
        finally:
            for model in models:
                model.close()
    if sys.version_info >= (3, 11):
        assert len(floors) == 2 and floors <= won, sorted(floors - won)


# A row of the test's own: the committed row of S point 1 at 888, two years from the end
# of its cover, its opening state and its ladder scaled to an account value of $5, read
# with charges ceasing at attained age 100, so that nothing is charged in any of its 24
# months and the account stays below $10.  Each miss is a twentieth of the checks'
# absolute tolerance of 1e-8 to one side of it, so that a floor of 9 or of 11 in place of
# 10 changes a verdict.
SMALL_ACCOUNT = 5.0
SMALL_REFS = {"charges_cease_age": 100}
SMALL_MISSES = {9.5e-9: True, 1.05e-8: False}


def test_the_components_and_the_closure_take_the_floor_of_10_on_a_small_account(tmp_path):
    """The components' identity and the ladder's closure decide as ``isclose`` below 10.

    Each divides its month's difference by the larger of its two sides and 10, as the
    roll-forward and the margin identity do (the test before this one), so that it holds
    exactly where ``IUL_US_S``'s ``math.isclose`` with ``rel_tol=1e-9`` and
    ``abs_tol=1e-8`` holds; the floor of 10 decides only where both sides are below 10,
    which no committed row and no splice row reaches (USLIB-SEC-PLAN.md §7.4, *Record —
    M6*, *Carried into M13*, the isclose floors).  So a row is built for the test beside the
    committed table, from the generator's row of S point 1 at 888, its account value, its
    fixed account and its segments scaled to :data:`SMALL_ACCOUNT`, read under
    :data:`SMALL_REFS`, past the cessation of charges, so that the account, $5.32 to $5.66,
    and its one segment created in the frame, maturing at ``t = 12``, stay below 10.  On
    models just read, the collateral at the end of each month, which only the components'
    identity and ``result_seg`` read, and that segment's deductions to date in its last
    month, which only its closure and its credit read, are each moved by each miss of
    :data:`SMALL_MISSES`: both checks pass the miss of ``9.5e-9`` and fail the one of
    ``1.05e-8``, each as ``isclose`` decides on the two sides this model computes, the floor
    of 10 winning in each residual (:class:`_BoundSides`), and the roll-forward and the
    margin identity, which read neither moved cell, hold.
    """
    committed = _committed()
    late = _label(committed, "derived", 1, 888)
    label = int(committed.index.max()) + 1
    scale = SMALL_ACCOUNT / committed.at[late, "av_pp_init"]
    money = ("av_pp_init", "fa_pp_init", "lca_pp_init")
    row = committed.loc[[late]].assign(
        **{c: committed.at[late, c] * scale for c in money}, row_kind="copy")
    table = pd.concat([committed, row.set_axis([label])]).rename_axis("point_id")
    ladder = _committed_ladder()
    seg = ladder[ladder["point_id"] == late]
    seg = seg.assign(point_id=label, **{c: seg[c] * scale for c in LADDER_MONEY})
    folder = _sec_inputs(tmp_path, table, ladder=pd.concat([ladder, seg],
                                                           ignore_index=True))
    floors, won = set(), set()
    for miss, passes in SMALL_MISSES.items():
        model = _read(folder, "small", SMALL_REFS)
        try:
            _moved(model, "lca_pp", f"lambda t: lca_pp_unmoved(t) + {miss!r}")
            _moved(model, "seg_ded_cum_pp",
                   f"lambda t, k: seg_ded_cum_pp_unmoved(t, k) + ({miss!r} if "
                   f"k == seg_term_mth - 1 and seg_new_pp(duration_mth(t) - k) != 0.0 "
                   f"else 0.0)")
            p = _point(model, label)
            bounds = _BoundSides(model)
            with bounds.watch() as these:
                verdicts = (p.check_av_components(), p.check_seg_ladder())
            won |= these
            floors |= {side for side in bounds.sides if side[2] == 2 and side[0] in (
                "check_av_components_resid", "check_seg_closure_resid")}
            assert verdicts == (passes, passes), miss
            n = p.proj_len()
            sides = [(p.av_pp(t), p.fa_pp(t) + p.seg_bal_tot_pp(t) + p.lca_pp(t))
                     for t in range(n)]
            maturing = [t for t in range(1, n) if p.seg_new_pp(p.duration_mth(t) - 12)]
            assert (n, maturing) == (24, [12]) and p.mth_deduction_pp(0) == 0.0
            m = p.duration_mth(12) - 12
            closed = (_seg(p, "seg_bal_pp", 11, m) + _seg(p, "seg_ded_cum_pp", 11, m)
                      + _seg(p, "seg_wd_cum_pp", 11, m))
            sides.append((p.seg_new_pp(m), closed))
            assert max(abs(x) for pair in sides for x in pair) < 10.0, sides
            assert all(math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-8)
                       for a, b in sides) is passes, miss
            assert (p.check_av_roll_fwd(), p.check_margin()) == (True, True), miss
        finally:
            model.close()
    if sys.version_info >= (3, 11):
        assert len(floors) == 2 and floors <= won, sorted(floors - won)


# Inputs at which a product or sum taken in another order than IUL_US_S's differs in its
# last bit: an acquisition expense, a maintenance expense and a multiple of the counts that
# no binary fraction holds exactly.
ACQ, MAINT, COUNTS_SCALE = 123.456, 77.7, 3.7


def test_acquisition_is_charged_on_new_business_only(tmp_path):
    """Acquisition per policy issued, in the issue month, never inflated.

    ``IUL_US_S`` charges ``expense_acq`` per policy in its issue month, on the count in
    force there, which on a point issued at the valuation date is the issued count, so the
    twins agree with S at any count.  On a copy whose counts are :data:`COUNTS_SCALE` times
    the committed table's, with :data:`ACQ` and :data:`MAINT` set and inflation at 2.5% a
    year, a charge per model point would show beside one per policy, and an inflated one
    beside one that is not.  On every point, what ``expenses(t)`` holds beyond its
    maintenance is ``ACQ`` per policy in the issue month, ``t = -duration_mth``, and 0 in
    every other month to ``t = 37``, to 1e-9: the twins of S's new business bear it at
    ``t = 0``, the point issued 25 months on at ``t = 25``, where the maintenance is
    inflated by ``1.025^2``, two valuation years on, and the acquisition is not, and the
    points already in force never, though on the valuation clock their row 0 is ``t = 0``.
    The formula is S's, in S's order, so on the twins, read by S at the same counts and
    inputs, the expenses are S's bit for bit.
    """
    refs = {"expense_acq": ACQ, "expense_maint": MAINT, "inflation_rate": INFLATION}
    table = _committed()
    model = _read(_sec_inputs(tmp_path / "sec", table.assign(
        policy_count=COUNTS_SCALE * table["policy_count"])), "acquisition", refs)
    s_table = _s_table()
    s = _read(_s_inputs(tmp_path / "s", s_table.assign(
        pols_if_init=COUNTS_SCALE * s_table["pols_if_init"])), "acquisition_s", refs)
    try:
        read = model.Data.model_point_table()
        months = range(38)
        for key, point_id in zip(point_keys(model), read.index):
            p = projection(model, key)
            acq = [p.expenses(t) - MAINT / 12 * p.inflation_factor(t) * p.pols_if(t)
                   if p.is_active(t) else 0.0 for t in months]
            issue = -read.at[point_id, "duration_mth"]
            expected = [ACQ * p.pols_if(t) if t == issue else 0.0 for t in months]
            assert acq == pytest.approx(expected, abs=1e-9), point_id
            assert (issue in months) == (sum(expected) > 0.0), point_id
        later = _row(model, "future", 4, -25)
        assert later.inflation_factor(25) == (1 + INFLATION) ** 2 == 1.050625
        assert later.expenses(25) == pytest.approx(
            (ACQ + MAINT / 12 * 1.050625) * COUNTS_SCALE, rel=1e-12)
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
# mort_rate caps the annual rate at 1, as IUL_US_S's does since USLIB-SEC-PLAN.md §8.2 item
# 4's fix, so the cap is no departure.  On the mortality rates UL, VUL and IUL share, the
# Tob class, 1.75 times the table, first passes 1 at attained age 113, 0.625687 x 1.75 =
# 1.0949523 (§7.6, Record — M4, The cap's month), and stays past it to the end of the
# projection.  The committed points are all NT, whose table rate reaches 1.0 itself at 119,
# and the splice's A/E of 0.56 keeps every class below 1, so neither binds the cap.  One
# point is made to pass it, the way the variants are made: S's point 1 in the Tob class,
# alone in a copy of S's table, on the variants' COI rows, under the splice's References
# with the A/E back at the shipped 1.0 (CAPPED_REFS).
CAPPED = (1, {"policy_id": "IUL-900020", "rate_class": "Tob"})
CAPPED_REFS = {**SPLICED_REFS, "mort_ae_factor": 1.0}
CAPPED_MTH = 816        # the first month at attained age 113, where the product passes 1


def _uncapped_mort_rate(proj, t):
    """``IUL_US_S``'s annual mortality product in month t, the one its cap bounds.

    The table's rate at the attained age, read at the table's nearest age, times the class
    factor and the A/E, computed from S's own cells and tables.
    """
    table = proj.data.mort_table()
    a = min(max(proj.age(t), int(table.index.min())), int(table.index.max()))
    return float(table.loc[a, "mort_rate"]) * proj.class_factor() * proj.mort_ae_factor


def _report_faults(p, case):
    """Where a report of ``p`` holds a value that is not a finite float, the segment count
    and the index level aside."""
    faults = []
    for report in REPORTS:
        frame = p.cells[report]().drop(columns=["seg_count"], errors="ignore")
        if not (frame.dtypes == "float64").all():
            faults.append(f"{case}: {report} holds {dict(frame.dtypes)}")
        if not all(math.isfinite(v) for v in frame.to_numpy().ravel()):
            faults.append(f"{case}: {report} holds a value that is not finite")
    return faults


def test_an_annual_mortality_past_1_is_capped_in_both_models(tmp_path):
    """Where the annual mortality product passes 1, both models' rate is 1.

    On the point of :data:`CAPPED`, ``IUL_US_S``'s product of the table's rate, the class
    factor and the A/E (:func:`_uncapped_mort_rate`) passes 1 in month :data:`CAPPED_MTH`
    and stays past it to the end of the projection.  Both models cap it: ``mort_rate`` and
    the monthly rate, ``1 - (1 - q)^(1/12)``, are 1.0 in every one of those months, the
    float, not the int 1, which compares equal to it, and S's are floats below 1 in every
    month before.  So every policy in force at the start of the first capped month dies in
    it, and none is in force after it.  The four reports hold finite floats alone, and the
    four checks hold.

    In every cell of S's this model agrees with S at every argument S cached, the capped
    months and the reports included, at 1e-9 relative with no absolute floor but S's
    roundings about zero, because the count falls to 1.4e-7 by the cap's month, where the
    default floor of 1e-9 would compare it against little.

    Four rows of the point, built from S by the generator under :data:`CAPPED_REFS`:
    issued at the valuation date, compared as a new-business twin, and 25 months after it;
    restated in force in the month before the cap, opened with S's count and state there,
    and compared cell by cell as a splice row is; and restated five months into the capped
    year, opened with S's state and segments there and one policy, since S's count there is
    0.  On each, the rate is 1.0 from its first capped month, every policy in force there
    dies in it, and the count is 0.0 after it: a cap applied to new business alone would
    pass both comparisons, which see S's capped rate, and fail here, on the rows in force.
    And the cap's side of its ``min`` wins, the side :data:`BOUND_ELSEWHERE` names this
    test for, which no row of the splice binds (:class:`_BoundSides`).
    """
    base, changes = CAPPED
    s = _read(_s_inputs(tmp_path / "s", _s_table().loc[[base]].assign(**changes),
                        SPLICED_EDITS), "capped_s", CAPPED_REFS)
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
        assert sp.pols_if(cap) > 0.0 and sp.pols_death(cap) == sp.pols_if(cap)
        assert [sp.pols_if(t) for t in range(cap + 1, end)] == [0.0] * (len(after) - 1)
        inside = cap + 5
        spec = dataclasses.replace(SPEC, derived=((base, cap - 1), (base, inside)),
                                   future=((base, 25),))
        table, ladder = build_sec_table(spec, s)
        table.loc[table["source_mth"] == inside, "policy_count"] = 1.0
        sec = _read(_sec_inputs(tmp_path / "sec", table, SPLICED_EDITS,
                                ladder=ladder[LADDER]), "capped", CAPPED_REFS)
        # Each row with the month its rate is first capped and, for the three S's count
        # opens, the exemptions and the arg_map of its comparison with S.
        rows = ((("twin", base, 0), cap, VARIANT_EXEMPT, _issued_later),
                (("future", base, -25), cap + 25, FUTURE_EXEMPT, _issued_later),
                (("derived", base, cap - 1), 1, SPLICE_EXEMPT,
                 _carried_segments(cap - 1, s.Projection.seg_term_mth)),
                (("derived", base, inside), 0, None, None))
        faults, bounds = [], _BoundSides(sec)
        for case, first, exempt, arg_map in rows:
            key = _row_key(sec, *case)
            with bounds.watch() as won:
                p = projection(sec, key)
                if exempt is not None:
                    assert _continues_s(sp, p, case[2], exempt, arg_map) == [], case
                capped = range(first, p.proj_len())
                later = range(first + 1, p.proj_len() + 1)
                for rate in (p.mort_rate, p.mort_rate_mth):
                    assert [(type(rate(t)), rate(t)) for t in capped] == (
                        [(float, 1.0)] * len(capped)), case
            assert p.pols_if(first) > 0.0 and p.pols_death(first) == p.pols_if(first), case
            assert [p.pols_if(t) for t in later] == [0.0] * len(later), case
            faults += _report_faults(p, case)
            assert tuple(p.cells[c]() for c in CHECKS) == (True,) * 4, case
            mine = _sides_bound_by(
                "test_an_annual_mortality_past_1_is_capped_in_both_models")
            if sys.version_info >= (3, 11):
                assert len(mine) == 1 and mine <= won, (case, sorted(mine - won))
            del p
            _release(sec, key)
        assert not faults, faults
    finally:
        if sec is not None:
            sec.close()
        s.close()


@pytest.mark.parametrize("case, ref", [("the A/E", "mort_ae_factor")], ids=["the A/E"])
def test_a_nan_that_reaches_the_cap_stays_nan(case, ref):
    """A NaN that reaches the cap on mortality stays NaN, and is not read as 1.

    ``min`` keeps its first argument unless a later one compares smaller, in modelx and
    compiled alike, and no comparison with NaN holds, so with its bound first the cap would
    turn a NaN into 1.0: a blank factor read as certain death, every flow finite.  It is
    written ``min(q, 1.0)``, in both models.  ``Data`` refuses a blank rate or factor as it
    reads the tables, so a NaN is sent to the cap through a Reference, the A/E, in models
    read for the test: ``mort_rate`` and ``mort_rate_mth`` are then the float NaN in every
    month in cover, on the twin of S's point 2 in both models and on the row issued 25
    months on, 0.0 before its issue.
    """
    models = []
    try:
        for name in (SEC, TWIN):
            models.append(_read(model_path(name), "nan_cap", {ref: float("nan")}))
        sec, s = models
        rows = [(_row(sec, "twin", 2, 0), 0), (_point(s, 2), 0),
                (_row(sec, "future", 4, -25), 25)]
        lost = []
        for x, issue in rows:
            for t in range(x.proj_len()):
                for name in ("mort_rate", "mort_rate_mth"):
                    value = x.cells[name](t)
                    if t < issue:
                        want = value == 0.0
                    else:
                        want = type(value) is float and math.isnan(value)
                    if not want:
                        lost.append(f"{x.name}.{name}({t}) = {value!r}")
        assert not lost, f"the cap loses a NaN sent through {case}: {lost[:5]}"
    finally:
        for model in models:
            model.close()


# ---------------------------------------------------------------------------
# The tables' ends
#
# A corridor table, a mortality table and a COI scale shorter than the cover, each read
# past its ends at its nearest row, as IUL_US_S reads them (USLIB-SEC-PLAN.md §7.6, Record
# — M4, Every bound binds, and Keys and clamps).  Data accepts any run of ages or years,
# and the shipped tables reach past every age and year in cover, so no other row reads
# their clamps: here the corridor's ages are cut to 50 to 94, so that attained ages below
# 50 read 50's 1.85, where the shipped table gives 2.15 to 1.91 at 45 to 49, and ages from
# 95 read 94's 1.01, where it gives 1.00; the mortality table to 50 to 110, so that ages 45
# to 49 read 50's 0.002256 and 111 to 120 read 110's 0.476604; and the anchor COI cell to
# its first 60 policy years, so that years 61 to 76 read year 60's 36.876 a thousand.  Each
# end is on a value other than the next age's or year's, so that a read of the wrong row
# past it changes a number.  S's point 1 paying $60,000 a year binds the corridor from its
# second policy year, at 46, below the corridor's first age, and every point binds it past
# 95.
SHORT_CORRIDOR = (50, 94)
SHORT_MORTALITY = (50, 110)
SHORT_COI = 60
SHORTENED = {
    "corridor_factors.csv": lambda t: t[t["age"].between(*SHORT_CORRIDOR)],
    "mort_table.csv": lambda t: t[t["age"].between(*SHORT_MORTALITY)],
    "coi_rates.csv": lambda t: t[t["policy_year"] <= SHORT_COI]}
FUNDED = {"premium_pp_ann": 60000.0}


def _clamped(p, shipped):
    """What ``p``'s months read past each shortened table's end, and how that is read.

    ``shipped`` is the shipped tables' columns, by age or year.  For each end: in every
    month in cover whose attained age or policy year is past it, the value read must be
    the end row's, and the end's name is returned where, in some such month, it differs
    from the shipped table's and reaches a number, the corridor binding by the raw value it
    bounds, a death, or a charge for the insurance.  Returns ``(reached, faults)``.
    """
    data, reached, faults = p.data, set(), []
    first, last = data.corridor_age_first(), data.corridor_age_last()
    mort_first, mort_last = data.mort_age_first(), data.mort_age_last()
    corridor, mortality, coi = (shipped["corridor"], shipped["mortality"],
                                shipped["coi"])
    for t in range(p.t_entry(), p.proj_len()):
        a, y = p.age(t), p.policy_year(t)
        binds = _corridor_raw(p, t) > _option(p, t)
        for end, past, held, read, shipped_value, reaches in (
                ("the corridor's first age", a < first, p.corridor_factor_at(first),
                 p.corridor_factor(t), corridor[a], binds),
                ("the corridor's last age", a > last, p.corridor_factor_at(last),
                 p.corridor_factor(t), corridor[a], binds),
                ("the mortality table's first age", a < mort_first,
                 p.mort_rate_base_at(mort_first), p.mort_rate_base_at(a), mortality[a],
                 p.pols_death(t) > 0.0),
                ("the mortality table's last age", a > mort_last,
                 p.mort_rate_base_at(mort_last), p.mort_rate_base_at(a), mortality[a],
                 p.pols_death(t) > 0.0),
                ("the COI scale's last year", y > SHORT_COI, p.coi_rate_guar_py(SHORT_COI),
                 p.coi_rate_guar(t), coi[y], p.coi_pp(t) > 0.0)):
            if not past:
                continue
            if read != held:
                faults.append(f"point {p.point_id()}, t = {t}: {end} read as {read}, not "
                              f"{held}")
            if read != shipped_value and reaches:
                reached.add(end)
    return reached, faults


def test_a_table_shorter_than_the_cover_is_read_at_its_ends_in_both_models(tmp_path):
    """Past a table's first or last key each model reads its nearest row, as S does.

    ``corridor_factor_at`` and ``mort_rate_base_at`` clamp the attained age to their
    tables' first and last ages, and ``coi_rate_guar_py`` the policy year to the scale's
    last year, as ``IUL_US_S``'s readers do, and on the shipped tables no age or year in
    cover is past either end.  So S's points 1 and 4, and S's point 1 paying $60,000 a
    year, in a copy of S's table whose corridor, mortality and COI tables are shortened
    (:data:`SHORTENED`), are read by ``IUL_US_S`` and, as twins built by the generator, by
    this model: each twin is S's point in every cell and every report, the checks' verdicts
    among them, to 1e-9 relative with no absolute floor but S's roundings about zero; in
    every month in cover past an end each model reads the end's row; and each of the five
    ends is read in some month where its value differs from the shipped table's and reaches
    a number (:func:`_clamped`).  A clamp dropped would raise at the read, and one to the
    wrong row would part the two models.  And each of the five clamps' sides wins at its
    ``min`` or ``max``, the sides :data:`BOUND_ELSEWHERE` names this test for, which no row
    of the splice binds (:class:`_BoundSides`).
    """
    rows = pd.concat([_s_table().loc[[1, 4]], _s_table_with_variants(
        {20: (1, {"policy_id": "IUL-900021", **FUNDED})}).loc[[20]]])
    s = _read(_s_inputs(tmp_path / "s", rows, SHORTENED), "ends_s")
    sec = None
    try:
        table, ladder = build_sec_table(dataclasses.replace(SPEC, derived=(), future=()), s)
        sec = _read(_sec_inputs(tmp_path / "sec", table, SHORTENED, ladder=ladder[LADDER]),
                    "ends")
        assert (sec.Data.corridor_age_first(), sec.Data.corridor_age_last(),
                sec.Data.mort_age_first(), sec.Data.mort_age_last()) == (50, 94, 50, 110)
        product = model_path(SEC).parent
        coi = pd.read_csv(product / "coi_rates.csv")
        shipped = {
            "corridor": pd.read_csv(product / "corridor_factors.csv",
                                    index_col="age")["corridor_factor"],
            "mortality": pd.read_csv(product / "mort_table.csv",
                                     index_col="age")["mort_rate"],
            "coi": coi.set_index("policy_year")["coi_rate_guar"]}
        reached, faults = set(), []
        with _BoundSides(sec).watch() as won:
            for point in rows.index:
                sp, p = _point(s, point), _row(sec, "twin", point, 0)
                _sweep_s(sp)
                assert _continues_s(sp, p, 0, VARIANT_EXEMPT, _issued_later) == [], point
                found, wrong = _clamped(p, shipped)
                reached |= found
                faults += wrong
        assert not faults, faults[:5]
        assert reached == {"the corridor's first age", "the corridor's last age",
                           "the mortality table's first age",
                           "the mortality table's last age",
                           "the COI scale's last year"}, reached
        mine = _sides_bound_by(
            "test_a_table_shorter_than_the_cover_is_read_at_its_ends_in_both_models")
        assert len(mine) == 5
        if sys.version_info >= (3, 11):
            assert mine <= won, sorted(mine - won)
    finally:
        if sec is not None:
            sec.close()
        s.close()


# ---------------------------------------------------------------------------
# A Reference that ships equal to another


# The shipped References a rewritten cell reads that ship equal to another and that the
# splice leaves equal, since moving one there would move the events its months are chosen
# on: loan_credit_rate_ann_1, 0.02, which the collateral's credited rate reads, equal to
# index_cap_guar and premium_tax_rate; loan_credit_rate_ann_2, 0.03, equal to
# loan_rate_ann, the loan's own rate; and loan_credit_step_year, 10, equal to
# expense_unit_step_year, which the per-unit charge steps on.  Each is moved apart, so that
# a rewritten cell reading one for the other parts the two models.  The other pairs a
# rewritten cell reads are set apart where they are compared: charges_cease_age from
# maturity_age, 121, lapse_rate_cap and mort_ae_factor from index_par, 1.0,
# lapse_shock_mult from lapse_dyn_cap, 2.0, and expense_unit_mth_2 from index_floor and
# inflation_rate, 0.0, in the splice (SPLICED_REFS); index_floor and lapse_dyn_cap in the
# index path's override (OVERRIDE_REFS); and inflation_rate in the inflation test.
APART_REFS = {"loan_credit_rate_ann_1": 0.0225, "loan_credit_rate_ann_2": 0.0275,
              "loan_credit_step_year": 8}
# The rows compared under APART_REFS: the twins of S's points, point 5 borrowing from
# policy year 21; and variant 12, borrowing from policy year 6, as its twin and restated
# at 82, a month before the moved step at year 8.
APART_VARIANTS = {12: VARIANTS[12]}
APART_ROWS = (*(("twin", p, 0) for p in NEW_BUSINESS), ("twin", 12, 0), ("derived", 12, 82))
# The default run's: variant 12's two rows, whose collateral reads all three, the twins of
# S's points with USLIB_SEC_FULL=1 (USLIB-SEC-PLAN.md K6).
APART_CORE = (("twin", 12, 0), ("derived", 12, 82))


def test_each_reference_that_ships_equal_to_another_is_read_as_itself(tmp_path):
    """A rewritten cell reads each loan Reference as itself, not as one equal to it.

    The collateral's credited rates and its step year ship equal to other References a
    rewritten cell reads (:data:`APART_REFS`), and the splice leaves them as shipped, its
    months being chosen on the events they set.  So both models are read on the variants'
    copy with :data:`APART_REFS` set before either computes anything: every row of
    :data:`APART_ROWS` is then S's point in every cell S evaluates, every one to 1e-9
    relative with no absolute floor but S's roundings about zero, the twins as T1 holds
    them at the shipped values, and the row restated as T2 holds it; the collateral is
    credited at 2.25% in policy years 6 to 8 and at 2.75% after, apart from the loan's 3%.
    A credited rate, a step or a collateral reading the equal Reference for its own passes
    every comparison at the shipped values and the splice's, and fails here
    (USLIB-SEC-PLAN.md §7.7, *Record — M9*, *References held to S's*).  By default the
    test reads variant 12 alone, its twin and its row at 82 (:data:`APART_CORE`), whose
    collateral reads all three; S's twins join with ``USLIB_SEC_FULL=1``.
    """
    rows = APART_ROWS if SEC_FULL else APART_CORE
    table = _s_table_with_variants(APART_VARIANTS)
    table = table.loc[sorted({p for _, p, _ in rows})]
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=table,
                          edits=SPLICED_EDITS), "apart_s", APART_REFS)
    sec = None
    try:
        for key in point_keys(s):
            _sweep_s(projection(s, key))
        sec = _read(_spliced_folder(tmp_path / "sec", s, [(12, 82)], ()), "apart",
                    APART_REFS)
        assert all(getattr(sec.Projection, name) == value
                   for name, value in APART_REFS.items())
        found = {}
        for case in rows:
            kind, s_point, month = case
            exempt, arg_map = ((VARIANT_EXEMPT, _issued_later) if kind == "twin"
                               else (SPLICE_EXEMPT,
                                     _carried_segments(month, s.Projection.seg_term_mth)))
            key = _row_key(sec, *case)
            lines = _continues_s(_point(s, s_point), projection(sec, key), month, exempt,
                                 arg_map)
            if lines:
                found[case] = lines[:5]
            _release(sec, key)
        assert not found, found
        p = _row(sec, "twin", 12, 0)
        assert [p.loan_credit_rate_ann(t) for t in (60, 95, 96)] == [0.0225, 0.0225, 0.0275]
        assert p.lca_pp(60) != p.loan_bal_pp(60)
    finally:
        if sec is not None:
            sec.close()
        s.close()


# ---------------------------------------------------------------------------
# Stage EC -- what compiling changed, held in modelx (USLIB-SEC-PLAN.md Phase 2)
#
# What compiling changed, on models read for the test; the tests of it on the committed
# model follow the others that read it, below.


# The opening account values of two points put in force a month, each opening from three
# parts: the fixed account, the collateral and the ladder's slot 1, as (point, the parts,
# the value av_pp_at opens with).  The first is CPython's sum's own case, 1e16, 1.0 and
# -1e16, in the one order Data accepts, the fixed account the only part of either sign:
# folded plainly, the 1.0 is lost.  The second is three negative zeros, which stage E's
# loop, started at its first part, opens as -0.0.
OPENING_PARTS = ((1, (-1e16, 1.0, 1e16), 1.0), (2, (-0.0, -0.0, -0.0), -0.0))


def _opening_inputs():
    """The committed table's points 1 and 2 put in force a month, opening from
    :data:`OPENING_PARTS`, and a ladder of their two slots; a table and a ladder that
    ``Data`` accepts.

    ``Data`` holds ``av_pp_init`` to the parts, summed as pandas adds the columns, to half
    a cent an amount and half a cent more, and reads nothing else from it: the plain fold
    of the first point's parts is 0.0, which the column holds, and the projection opens
    from the parts.  A collateral above 0 needs a loan (``Data``'s rule 18).
    """
    table = _committed().loc[[1, 2]]
    ladder = _committed_ladder().iloc[[0, 0]].reset_index(drop=True)
    for row, (point, (fa, lca, slot), _) in enumerate(OPENING_PARTS):
        columns = {"duration_mth": 1, "fa_pp_init": fa, "lca_pp_init": lca,
                   "loan_bal_init": 1.0 if lca > 0 else 0.0, "av_pp_init": 0.0,
                   "sum_assured_init": table.at[point, "sum_assured"]}
        for column, value in columns.items():
            table = _set(column, [point], value)(table)
        ladder.loc[row, ["point_id", "slot", "seg_bal_pp_init", "seg_ded_cum_pp_init",
                         "seg_wd_cum_pp_init"]] = [point, 1, slot, 0.0, 0.0]
    return table, ladder


def _opened_as_written(got, want):
    """Whether ``got`` is ``want`` bit for bit: a float of the same hex, sign included."""
    return type(got) is float and got.hex() == want.hex()


def test_the_opening_account_value_is_summed_compensated_from_its_parts(tmp_path):
    """``av_pp_at(t_entry(), BEF_PREM)`` sums its parts as stage ``E`` did, compensated.

    A point in force opens its account value from its parts, the fixed account, the
    collateral and the ladder's balances, in a loop compensated as Python's ``sum`` is
    (USLIB-SEC-PLAN.md §7.5, *For M19 and later*, item 2).  No committed row tells that
    loop from a plain fold, whose sums agree there, so C2, T2 and C4 pass without its
    correction: so on inputs ``Data`` accepts (:func:`_opening_inputs`), the opening of
    parts ``-1e16``, ``1.0`` and ``1e16`` is ``1.0``, as ``sum`` gives, where the fold
    gives 0.0, and of three negative zeros is ``-0.0``, stage ``E``'s value: its loop starts
    at the fixed account, not at ``0.0``, so a sign of zero carries, as it does in
    :func:`test_the_compiled_opening_account_value_is_summed_as_modelx_sums_it`, the same
    inputs compiled.  Each is compared by ``float.hex``.  The inputs are read as written,
    the sign of each zero included.
    """
    table, ladder = _opening_inputs()
    model = _read(_sec_inputs(tmp_path, table, ladder=ladder), "opening")
    try:
        for point, parts, want in OPENING_PARTS:
            p = _point(model, point)
            read = (p.fa_pp_init(), p.lca_pp_init(), p.seg_bal_pp_init(1))
            assert [x.hex() for x in read] == [x.hex() for x in parts], (point, read)
            assert p.t_entry() == 0 and p.duration_mth_init() == 1
            got = p.av_pp_at(p.t_entry(), _code(p, "BEF_PREM"))
            assert _opened_as_written(got, want), (point, got, want)
    finally:
        model.close()


# The balances the compensated-sum test sets in both models, on the twins of S's points 1
# and 2, at the end of POOL_MTH - 1, as (S point, the three live segments' balances by
# creation month): CPython's own case, where a plain sum loses the 1.0, and three negative
# zeros, whose sum from 0.0 is a positive zero.
POOL_MTH = 3
POOL_PARTS = ((1, (1e16, 1.0, -1e16)), (2, (-0.0, -0.0, -0.0)))


@pytest.mark.skipif(not EXACT_SUMS, reason="IUL_US_S's sum is compensated from Python 3.12")
def test_the_compensated_sums_are_s_sums_where_a_plain_sum_is_not():
    """The two compensated pools are S's ``sum`` where a plain sum differs.

    The twins' months hold no balances on which a plain running sum and a compensated one
    differ, so :func:`test_the_compensated_sums_are_s_sums_bit_for_bit` cannot tell the two
    loops apart (USLIB-SEC-PLAN.md §7.5, *For M19 and later*, item 2).  So the balances
    enter as modelx input values, on a read of each model of its own: on the twins of S's
    points 1 and 2, the three segments live at the end of month ``POOL_MTH - 1`` are set
    to :data:`POOL_PARTS` in both models, each segment at its creation month in S and at
    its slot in this model, and the pool those segments open month ``POOL_MTH`` with and
    their total at the end of the month before must each be S's, by ``float.hex``:
    ``1.0`` from ``1e16``, ``1.0`` and ``-1e16``, which a plain sum gives as 0.0, and a
    positive zero from three negative zeros, as ``sum`` from ``0`` gives.
    """
    s = mx.read_model(model_path(TWIN), name=_name("s_pool"))
    sec = mx.read_model(model_path(SEC), name=_name("pool"))
    try:
        found = []
        for point, parts in POOL_PARTS:
            theirs, mine = _point(s, point), _row(sec, "twin", point, 0)
            assert mine.duration_mth(POOL_MTH) == POOL_MTH
            for m, value in enumerate(parts):
                theirs.seg_bal_pp[POOL_MTH - 1, m] = value
                mine.seg_bal_pp[POOL_MTH - 1, POOL_MTH - 1 - m] = value
            for cell, t in (("seg_bal_active_pp", POOL_MTH), ("seg_bal_tot_pp",
                                                               POOL_MTH - 1)):
                got, want = mine.cells[cell](t), theirs.cells[cell](t)
                if not (type(got) is float and got.hex() == float(want).hex()):
                    found.append(f"point {point}: {cell}({t}) {got!r}, S's {want!r}")
            assert theirs.seg_bal_active_pp(POOL_MTH) == sum(parts)
    finally:
        sec.close()
        s.close()
    assert not found, found


# A participation rate past 1, set in both models: the year's return of 6.4% then
# participates at 11.2%, past the shipped cap of 10%.
PAR = {"index_par": 1.75}


def test_the_participation_rate_applies_inside_the_cap_in_both_models(tmp_path):
    """Past a participation rate of 1 the cap binds on the participating return, as in S.

    ``IUL_US_S`` credits a maturing segment ``max(index_floor, min(cap, index_par *
    return))``, the participation inside the cap, and ships ``index_par`` at 1.0, where
    the participation applied outside the cap, ``index_par * min(cap, return)``, credits
    the same, and no other test moves it.  At 1.75 (:data:`PAR`) the year's return of 6.4%
    participates at 11.2%, past the 10% cap, which then binds, where the other order
    credits 11.2%.  So under it, set before anything computes in both models, on the twins
    of S's points 1 and 4, every segment maturing in cover is credited the cap, and each
    twin's credits are S's in every month, and its cash flows S's frame.
    """
    table = _committed().loc[[1, 4]]
    sec = _read(_sec_inputs(tmp_path / "sec", table, ladder=_committed_ladder().iloc[0:0]),
                "par", PAR)
    s = _read(_s_inputs(tmp_path / "s", _s_table().loc[[1, 4]]), "s_par", PAR)
    try:
        for point in (1, 4):
            p, sp = _point(sec, point), _point(s, point)
            matured = [t for t in range(p.proj_len())
                       if p.is_active(t) and p.duration_mth(t) >= p.seg_term_mth]
            assert matured and all(
                p.index_par * p.seg_return(t) > p.seg_index_cap(t) == p.seg_credit_rate(t)
                for t in matured), point
            assert [p.index_credit_pp(t) for t in range(p.proj_len())] == pytest.approx(
                [sp.index_credit_pp(t) for t in range(sp.proj_len())], rel=1e-12, abs=0)
            assert frame_mismatches(sp.result_cf(), p.result_cf()) == [], point
    finally:
        s.close()
        sec.close()


# The month at which the sign test sets the two kinds on the anchor's twin: in cover, where
# its death claims are not zero.
ZERO_MONTH = 5


def test_negative_zero_parts_total_a_positive_zero_as_s_sum_does():
    """The total is ``0.0``, not ``-0.0``, where both kinds are ``-0.0``, as S's ``sum``.

    S's total is ``sum`` of its kinds, which starts at the int 0, and ``0 + -0.0`` is
    ``0.0``, so S's total of negative zeros is a positive zero.  ``claims(t)`` starts its
    sum at ``0.0`` for that reason, and the split test cannot hold it: no committed month
    has negative zero kinds, and S's total cannot be set by a Reference.  So the zeros
    enter as modelx input values: on a read of each model of its own, the two kinds of the
    anchor's twin at :data:`ZERO_MONTH`, ``claims_death`` and ``claims_lapse``, are set to
    ``-0.0``, and so are S's ``claims(t, "DEATH")`` and ``claims(t, "LAPSE")`` of its point
    1 in the same month, and each total must be S's: ``0.0``, a float, with a positive
    sign.  A total started at its first kind, or written without its ``0.0``, gives
    ``-0.0`` and fails.  The compiled total's sign of a zero is not held: C4 compares by
    value (``model-sec.md``).
    """
    s = mx.read_model(model_path(TWIN), name=_name("s_zeros"))
    sec = mx.read_model(model_path(SEC), name=_name("zeros"))
    try:
        theirs, mine = _point(s, 1), _row(sec, "twin", 1, 0)
        assert mine.claims_death(ZERO_MONTH) == theirs.claims(ZERO_MONTH, "DEATH") != 0.0
        for kind in ("DEATH", "LAPSE"):
            theirs.claims[ZERO_MONTH, kind] = -0.0
        for cell in ("claims_death", "claims_lapse"):
            mine.cells[cell][ZERO_MONTH] = -0.0
        totals = (theirs.claims(ZERO_MONTH), mine.claims(ZERO_MONTH))
    finally:
        sec.close()
        s.close()
    for total in totals:
        assert type(total) is float and total == 0.0, totals
        assert math.copysign(1.0, total) == 1.0, totals


def _extract():
    """The committed table and ladder as an administration extract would hold them: without
    the generator's columns, labelled ``100 + point_id``, in reverse order, 112 first, the
    ladder through the same map, so that a label read as a position, or as a position
    plus one, names another point; as (table, ladder)."""
    extract = _committed().drop(columns=list(GENERATED_COLUMNS))
    extract.index = pd.Index(extract.index + 100, name="point_id")
    ladder = _committed_ladder().assign(point_id=lambda f: f["point_id"] + 100)
    return extract.iloc[::-1], ladder


# The reads beyond a table, as (cell, arguments, the message after the point's label), on
# the extract's row of S point 4 at 65, which holds the ladder's twelve slots: a policy year
# below 1, where IUL_US_S's .loc raised KeyError, which each year reader refuses before it
# reads its padded array; and a slot below 1 or past the point's last, which each reader of
# the ladder refuses before it reads, where stage E's .loc raised KeyError.  On the row of S
# point 5 at 6, which holds six, a slot inside the ladder's width past its own last.
_NO_SLOT = "inforce_segments_sec.csv holds no segment in slot {}"
BEYOND = [
    ("coi_rate_guar_py", (0,), "coi_rates.csv has no rate for policy year 0"),
    ("lapse_rate_base_py", (0,), "lapse_table.csv has no rate for policy year 0"),
    ("coi_rate_guar_py", (-1,), "coi_rates.csv has no rate for policy year -1"),
    ("lapse_rate_base_py", (-1,), "lapse_table.csv has no rate for policy year -1"),
    *[(cell, (k,), _NO_SLOT.format(k)) for cell in LADDER_VALUES for k in (0, 13, -1)],
]
BEYOND_SHORT = [(cell, (k,), _NO_SLOT.format(k)) for cell in LADDER_VALUES
                for k in (7, 12)]


def test_every_padded_array_holds_nan_and_no_reader_reads_it(tmp_path):
    """The padding is NaN, the readers refuse a key before a table, by name (§7.1 item 9).

    Each reader of a padded table refuses a key outside it (:data:`BEYOND`), naming the
    point by its label, on the extract labelled otherwise than by position
    (:func:`_extract`), where a label read as ``idx + 1`` would name another: a policy
    year below 1 in the two year readers, and a slot below 1 or past the point's last in
    the five readers of the ladder, on the point holding twelve slots and on the one
    holding six (:data:`BEYOND_SHORT`), whose seventh to twelfth lie inside the ladder's
    width.  A year past a table reads its last row and an age outside the two age tables
    the nearest row, as ``IUL_US_S`` reads them.

    The padding is NaN, as the ``Data`` docstrings say, so that a read past a check, were
    one lost, would make every number after it NaN rather than another key's value: row 0
    of the COI scales, the column of policy year 0 and every year past each scale's last;
    year 0 of the lapse table; the ages below the mortality table's first, 18; and, in the
    five ladder arrays, column 0, which is no slot, and every slot a point does not hold,
    the whole row of a point without a ladder; and nothing inside.  The ladder's width is
    the most rows one point holds, plus one.
    """
    extract, ladder = _extract()
    model = _read(_sec_inputs(tmp_path / "extract", extract, ladder=ladder), "beyond")
    try:
        full, short = 107, 108
        p = _point(model, full)
        assert p.point_id() == full != point_keys(model)[0] + 1
        found = []
        for label, cases in ((full, BEYOND), (short, BEYOND_SHORT)):
            p = _point(model, label)
            for cell, args, message in cases:
                with pytest.raises(Exception) as excinfo:
                    p.cells[cell](*args)
                if _raised(excinfo.value) != f"ValueError: point_id {label}: {message}":
                    found.append(f"{label}: {cell}{args}: {_raised(excinfo.value)}")
        assert not found, found
        data = model.Data
        p = _point(model, full)
        assert p.lapse_rate_base_py(500) == p.lapse_rate_base_py(data.lapse_last_year())
        assert p.coi_rate_guar_py(500) == p.coi_rate_guar_py(p.coi_rate_last_year())
        assert p.corridor_factor_at(500) == p.corridor_factor_at(data.corridor_age_last())
        assert p.mort_rate_base_at(0) == p.mort_rate_base_at(data.mort_age_first())
        assert p.mort_rate_base_at(500) == p.mort_rate_base_at(data.mort_age_last())
        coi, last = data.coi_rate_array(), data.coi_rate_last_years()
        assert np.isnan(coi[0]).all() and np.isnan(coi[:, 0]).all() and last[0] == 0
        for s in range(1, data.coi_schedules() + 1):
            assert not np.isnan(coi[s, 1:last[s] + 1]).any(), s
            assert np.isnan(coi[s, last[s] + 1:]).all(), s
        for array, first in ((data.lapse_rate_array(), 1),
                             (data.corridor_factor_array(), data.corridor_age_first()),
                             (data.mort_table_array(), data.mort_age_first())):
            assert np.isnan(array[:first]).all() and not np.isnan(array[first:]).any()
        assert first == 18
        width = data.inforce_segment_max() + 1
        held = dict(zip(data.model_point_table().index, data.inforce_segment_count()))
        assert width == 13 and max(held.values()) == 12 and held[short] == 6
        for cell in LADDER_VALUES:
            array = data.cells[cell]()
            assert array.shape == (len(extract), width), cell
            for i, label in enumerate(data.model_point_table().index):
                n = held[label]
                assert np.isnan(array[i, 0]) and np.isnan(array[i, n + 1:]).all(), (
                    cell, label)
                assert not np.isnan(array[i, 1:n + 1]).any(), (cell, label)
    finally:
        model.close()


# The COI copy's scales in the order the numbering test writes them, out of their keys'
# order, and the scale each twin of S's points 1, 2 and 4 is given, by its sex and class.
COI_FILE_ORDER = (("M", "Tob", 45), ("F", "Juv", 45), ("M", "PElite", 45), ("M", "NT", 50),
                  ("M", "NT", 45), ("M", "PPlus", 45), ("M", "NT", 65), ("M", "PTob", 45),
                  ("M", "Pref", 45))
COI_KEYS_OF = {1: ("M", "Tob"), 2: ("F", "Juv"), 4: ("M", "PElite")}


def _coi_shuffled(rates):
    """The splice's COI scales, in :data:`COI_FILE_ORDER`, each scale's lines reversed."""
    rates = _coi_rates_with_variants(rates)
    place = {key: k for k, key in enumerate(COI_FILE_ORDER)}
    rates = rates.iloc[::-1].reset_index(drop=True)
    order = rates[["sex", "rate_class", "age_at_entry"]].apply(
        lambda row: place[tuple(row)], axis=1)
    return rates.iloc[order.argsort(kind="stable")].reset_index(drop=True)


def _coi_keys(table):
    """``table`` with the sex and class :data:`COI_KEYS_OF` gives each of S's points."""
    rows = table.copy()
    for point, (sex, rate_class) in COI_KEYS_OF.items():
        rows.loc[point, ["sex", "rate_class"]] = (sex, rate_class)
    return rows


# IUL_US_S slices its COI scale from a MultiIndex the shuffled file leaves unsorted, which
# pandas warns may be slow; the slice is the scale all the same.
@pytest.mark.filterwarnings("ignore:indexing past lexsort depth")
def test_the_coi_scales_are_numbered_by_key_on_a_file_out_of_key_order(tmp_path):
    """On a COI file written out of its keys' order, each point reads its own scale, as S.

    ``Data`` numbers the COI scales in their keys' order in all three cells that number
    them, ``coi_schedule()``, the point's number, and ``coi_rate_array()`` and
    ``coi_rate_last_years()``, the scales and their last policy years by number, so that
    a point's number is the row of its own scale, whatever order the file is written in.
    A ``Data`` numbering cannot be held by the compiled model's comparison with modelx,
    which share ``Data``, nor by the fingerprint, on a file of one scale: it is held here,
    against the file and against ``IUL_US_S``.  On the splice's copy of nine scales,
    written in an order of their own, each scale's lines reversed (:func:`_coi_shuffled`),
    the twins of S's points 1, 2 and 4 are given three of them (:data:`COI_KEYS_OF`), in
    both models: each scale's row of ``coi_rate_array()`` is the file's rates for its keys,
    found by key, and its last year the file's; and each twin reads S's guaranteed COI
    rate in every month, by S's own slice of the file, and projects S's cash flows.
    """
    edits = {"coi_rates.csv": _coi_shuffled}
    sec = _read(_sec_inputs(tmp_path / "sec", _coi_keys(_committed().loc[[1, 2, 3, 4, 5]]),
                            edits, ladder=_committed_ladder().iloc[0:0]), "coi_order")
    s = _read(_s_inputs(tmp_path / "s", _coi_keys(_s_table()), edits), "s_coi_order")
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
        for point, (sex, rate_class) in COI_KEYS_OF.items():
            sp, p = _point(s, point), _point(sec, point)
            assert (p.sex(), p.rate_class()) == (sp.sex(), sp.rate_class()) == (
                sex, rate_class)
            assert p.coi_schedule() == sorted(keys).index((sex, rate_class, 45)) + 1
            assert [p.coi_rate_guar(t) for t in range(p.proj_len())] == [
                sp.coi_rate_guar(t) for t in range(sp.proj_len())], point
            assert frame_mismatches(sp.result_cf(), p.result_cf(), rtol=1e-9,
                                    atol=1e-9) == [], point
    finally:
        s.close()
        sec.close()


# A point the contract does not issue, refused by proj_len() in its rules' order, as (case,
# the table and ladder, the inputs' edits, the References set, the label, the message, and,
# where it projects once its bound is moved, the References that move it and its frame
# then).  The two issue-age rules are asked after stage E's four, so a point issued at 86
# and past its cover is refused as past it, one withdrawing half its fee for the
# withdrawal, one missing a month of its ladder for the ladder, and one to be issued at 122
# as never in cover.  The issue age of 86 projects once issue_age_max is 86, and 85, the
# bound, at the shipped References, each on a COI copy with a scale of its own
# (_coi_at); the point at 45 refused under an issue_age_min raised to 46 projects at the
# shipped 0.
_ABOVE_MAX = "point_id {}: issue age 86 is above issue_age_max, 85"


def _coi_at(*ages):
    """An edit of the COI scale that adds ``(M, NT, age)`` for each of ``ages``: the
    anchor's rows to the age's last policy year, at a scale of its own."""
    def edit(rates):
        anchor = rates[(rates["sex"] == "M") & (rates["rate_class"] == "NT")
                       & (rates["age_at_entry"] == 45)]
        blocks = [rates]
        for n, age in enumerate(ages):
            rows = anchor[anchor["policy_year"] <= 121 - age]
            blocks.append(rows.assign(age_at_entry=age, provenance="test copy",
                                      coi_rate_guar=(rows["coi_rate_guar"]
                                                     * (3.1 + 0.2 * n)).round(6)))
        return pd.concat(blocks, ignore_index=True).sort_values(COI_KEYS,
                                                                ignore_index=True)
    return edit


def _issue_age_cases():
    """:data:`ISSUE_AGES`' inputs, as (case, the table, the ladder or None, the edits, the
    References set, the label, the message or None, the References that issue it or None,
    its frame then)."""
    committed = _committed()
    at_86 = {"coi_rates.csv": _coi_at(85, 86)}
    short, gapped = _ladder_without(8, 6, True)
    return [
        ("an issue age of 86", _set("age_at_entry", [3], 86)(committed), None, at_86, {},
         3, _ABOVE_MAX.format(3), {"issue_age_max": 86}, 12 * (121 - 86)),
        ("an issue age of 85, at the bound", _set("age_at_entry", [3], 85)(committed),
         None, at_86, {}, 3, None, {}, 12 * (121 - 85)),
        ("an issue age below a bound raised to 46", committed, None, None,
         {"issue_age_min": 46}, 3, "point_id 3: issue age 45 is below issue_age_min, 46",
         {}, 912),
        ("issued at 86 and past its cover: the cover's rule first",
         _set("age_at_entry", [11], 86)(committed), None, at_86, {}, 11,
         "point_id 11: duration_mth 888 is at or past the end of the projection, policy "
         "month 420, attained age 121", None, None),
        ("issued at 86, withdrawing half its fee: the fee's rule first",
         _both(_set("age_at_entry", [8], 86), _set("wd_pp", [8], 12.5))(committed), None,
         at_86, {}, 8, _BELOW_FEE.format(point=8, wd=12.5, fee=25.0), None, None),
        ("issued at 86, a month of its ladder missing: the ladder's rule first",
         _set("age_at_entry", [8], 86)(short), gapped, at_86, {}, 8,
         _HELD.format(point=8, held=5, last=5, months=6, want=6), None, None),
        ("to be issued at 122: the maturity rule first",
         _set("age_at_entry", [12], 122)(committed), None, None, {}, 12,
         _PAST_AGE.format(point=12, age=122), None, None),
    ]


ISSUE_AGES = _issue_age_cases()


@pytest.mark.parametrize("case, table, ladder, edits, refs, label, message, issue, frame",
                         ISSUE_AGES, ids=[c[0] for c in ISSUE_AGES])
def test_a_point_the_contract_does_not_issue_is_refused_by_proj_len(tmp_path, case, table,
                                                                    ladder, edits, refs,
                                                                    label, message, issue,
                                                                    frame):
    """``proj_len()`` refuses a point issued outside the contract's ages, naming it (§6.1).

    ``IUL_US_S`` projects a point issued at any age its tables serve, and so would modelx
    here, but the compiled caches are sized from the youngest age the contract issues at,
    ``issue_age_min``, 0 (``spec_sec.py``), and a younger point would run past them; and
    ``product-spec.md`` issues to 85, ``issue_age_max``, which no cache needs.  So the frame
    refuses a point issued above ``issue_age_max`` or below ``issue_age_min``, naming it,
    and each rule after stage ``E``'s four, so that every message stage ``E`` gave a point
    it still gives (:data:`ISSUE_AGES`).  ``Data`` refuses an age below 0 first, so the
    lower rule is read under a bound raised to 46.  The table reads, since these are rules
    of the product, and every report is refused with the frame.  The point issued at 86
    projects once ``issue_age_max`` is 86, the one at 85 at the shipped bound, and the one
    refused at a bound of 46 at the shipped 0, each with its frame and its checks: the
    Reference is what refuses each, and a bound off by one, or a refusal lost or asked in
    another order, lets a point through or names the wrong rule.
    """
    model = _read(_sec_inputs(tmp_path, table, edits, ladder), "not_issued", refs)
    try:
        assert len(model.Data.model_point_table()) == len(table)
        if message is not None:
            _refused_exactly(_point(model, label).proj_len, message)
            for report in REPORTS:
                _refused_exactly(_point(model, label).cells[report], message)
    finally:
        model.close()
    if issue is None:
        return
    model = _read(_sec_inputs(tmp_path / "issued", table, edits, ladder), "issued", issue)
    try:
        p = _point(model, label)
        assert p.proj_len() == len(p.result_cf()) == frame
        assert all(p.cells[check]() for check in CHECKS)
    finally:
        model.close()


# What Data cannot number or join, refused when the vector is first read, naming every
# point at fault (the Data docstring): a label that is not a whole number, or one of 2**53
# or more in size, which numpy would read as the least int64 once past int64; an issue age,
# a duration or a first year of withdrawals or loans of 2**53 or more, past which a float
# no longer holds every whole number; a rate_class the class factors lack; and, on a point
# that has_surr_charge, a surr_charge_id the schedules lack, or a run-off of 2**53 years or
# more, the bound of every number read as an int, past which lapse_shock_year's compiled
# int() would in time raise OverflowError; and a negative age in the corridor or the
# mortality table, which an array indexed by age cannot hold.  The surrender-charge cases
# leave the charge on points 4 and 6 alone, so that the message names those two and not
# the table; a point without a charge projects whatever its schedule
# (test_a_point_without_a_charge_reads_its_schedule_as_at_stage_e).  Each case is (case,
# the table's edit, the inputs' edits or None, the Data cell asked, the message, the label
# whose projection meets it, or None for the base Projection's): a label's refusal is met
# by that point's own point_id(), which every refusal names it by; the schedules' by point
# 4's projection, which has a charge; and the table's own checks and the class join by the
# projection of the table's first point, which reads its class and both age tables in its
# first month.
_CHARGED = (4, 6)
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


def _runoff(years):
    """An edit of the schedules that runs every one off over ``years``."""
    return {"surr_charge_table.csv": lambda table: table.assign(runoff_years=years)}


def _from_age(first, column):
    """An edit of an age table that adds the ages from ``first`` below its own first, each
    at its first age's ``column``, so that the ages still run one row an age."""
    def edit(rows):
        low = int(rows["age"].min())
        added = pd.DataFrame({"age": list(range(first, low)),
                              column: rows.loc[rows["age"] == low, column].iloc[0],
                              "provenance": "test copy"})
        return pd.concat([added, rows], ignore_index=True)
    return edit


_HUGE = 2 ** 53
UNJOINED = [
    ("a label that is not whole", _relabelled(4, 4.5), None, "point_id",
     f"{TABLE}: point_id must be a whole number; [4.5] is not", 4.5),
    ("a label written as text", _relabelled(4, "4x"), None, "point_id",
     f"{TABLE}: point_id must be a whole number; ['4x'] is not", "4x"),
    ("a label of 2**53", _relabelled(4, _HUGE), None, "point_id",
     f"{TABLE}: point_id must be below 2**53 in size; [{_HUGE}] is not", _HUGE),
    ("an issue age of 2**53", _set("age_at_entry", [4], _HUGE), None,
     "model_point_table",
     f"{TABLE}: age_at_entry must be below 2**53 in size; it is not at point_id [4]",
     None),
    ("a duration of 2**53 months", _set("duration_mth", [4], _HUGE), None,
     "model_point_table",
     f"{TABLE}: duration_mth must be below 2**53 months in size; it is not at point_id "
     f"[4]", None),
    *[(f"a {column} of 2**53", _set(column, [4], _HUGE), None, "model_point_table",
       f"{TABLE}: {column} must be below 2**53 policy years; it is not at point_id [4]",
       None) for column in ("wd_first_year", "loan_first_year")],
    ("a class the table lacks, at two points", _set("rate_class", [3, 6], "SuperNT"),
     None, "class_factor",
     "class_factor_table.csv has no factor for the rate_class of point_id [3, 6]", None),
    *[(f"a schedule the table lacks, on a point with a charge, by {cell}",
       _charged_only(_CHARGED, _set("surr_charge_id", [6, 7], "IUL99")), None, cell,
       _NO_SCHEDULE, 4)
      for cell in ("surr_charge_rate_max", "surr_charge_runoff_years")],
    *[(f"a run-off of 2**53 years, by {cell}", _charged_only(_CHARGED),
       _runoff(2.0 ** 53), cell, _RUNOFF_HUGE, 4)
      for cell in ("surr_charge_runoff_years", "surr_charge_rate_max")],
    ("a negative age in the corridor table", lambda table: table,
     {"corridor_factors.csv": _from_age(-1, "corridor_factor")}, "corridor_age_last",
     "corridor_factors.csv: age must be 0 or more; it is not on line [2]", None),
    ("a negative age in the mortality table", lambda table: table,
     {"mort_table.csv": _from_age(-1, "mort_rate")}, "mort_age_last",
     "mort_table.csv: age must be 0 or more; it is not on line [2]", None),
]


def _met_by(model, cell, label):
    """The call that meets an :data:`UNJOINED` case's refusal: the label's own
    ``point_id()`` where ``point_id`` refuses it, else the projection of the label's
    point, or of the table's first point where there is no label."""
    if label is None:
        return model.Projection.result_cf
    return _point(model, label).cells["point_id" if cell == "point_id" else "result_cf"]


@pytest.mark.parametrize("case, edit, edits, cell, message, label", UNJOINED,
                         ids=[c[0] for c in UNJOINED])
def test_what_data_cannot_number_or_join_is_refused_naming_it(tmp_path, case, edit, edits,
                                                             cell, message, label):
    """``Data`` refuses what it cannot number or join, naming every point at fault.

    ``IUL_US_S`` reads a point's class factor in its first month in cover, and the
    schedule of a point with a surrender charge in every month of its cover, so it fails
    every projection of a point whose class or charged schedule the tables lack, and this
    model refuses the table at the first read instead (:data:`UNJOINED`), in the vector's
    own cell and in a projection, with the message matched whole.  A label is read by no
    projection but in a refusal, which names the point by ``point_id()``, so that cell
    refuses it, and the table reads.  Every number ``Data`` reads into an int64 is held
    below ``2**53``, and every age of an age table to 0 or more, by the table's own check,
    which the base ``Projection``'s point meets too.  Each message names every point or
    line at fault and no other.
    """
    model = _read(_sec_inputs(tmp_path, edit(_committed()), edits), "unjoined")
    try:
        if cell != "model_point_table":
            assert len(model.Data.model_point_table()) == len(_committed())
        _refused_exactly(model.Data.cells[cell], message)
        _refused_exactly(_met_by(model, cell, label), message)
    finally:
        model.close()


# run_sec.py run as though it sat at /m/products/indexed_ul, a copy too shallow to have a
# repository above it: the source compiled under that name, so that its own __file__ is
# it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/indexed_ul/run_sec.py"
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


def _bench_tool():
    """The repository's ``tools/bench_sec_cy.py``, imported as a module of its own, or a
    skip where the tool is absent, as from a ``lifelib.create()`` copy or from lifelib."""
    import importlib.util
    path = model_path(SEC).parents[5] / "tools" / "bench_sec_cy.py"
    if not path.is_file():
        pytest.skip("tools/bench_sec_cy.py is the source repository's, and it is absent")
    spec = importlib.util.spec_from_file_location(f"bench_sec_cy_{next(_names)}", path)
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    return tool


def test_the_benchmark_block_repeats_the_ladder_with_its_points(tmp_path):
    """C6's block repeats the segment ladder with the table, each row naming its copy.

    ``tools/bench_sec_cy.py`` times a block of the committed table repeated, each copy's
    points renumbered after the last copy's; a point in force reads its segments from the
    ladder by ``point_id``, so the tool repeats the ladder too, each row's ``point_id`` the
    one its point has in that copy, matched by value as ``Data`` matches it (``6.0`` is
    6), and refuses a row naming no point of the table, as ``Data`` would.  So:
    a block of two copies, read in modelx, holds the ladder twice, the second copy's rows
    each the first's on its point's label plus the table's length, and each point in
    force opens the same account value over the same frame in both copies; the ladder
    written with its ``point_id`` as floats is renumbered alike; and one naming point 99
    is refused, naming it.  The tool's timing and checks run only where it is run, by hand
    (``model-sec.md``).
    """
    tool = _bench_tool()
    folder = _sec_inputs(tmp_path / "block", _committed())
    product = folder.parent
    header, rows = tool.read_table(product / TABLE)
    assert [path.name for path in tool.companions(product, TABLE)] == [LADDER]
    text = tool.companion_text(product / LADDER, header, rows, 2)
    (product / TABLE).write_text(tool.block_text(header, rows, 2), encoding="utf-8")
    (product / LADDER).write_text(text, encoding="utf-8")
    floats = _sec_inputs(tmp_path / "floats", _committed(), ladder=lambda ladder: (
        ladder.astype({"point_id": "float64"}))).parent
    as_floats = tool.companion_text(floats / LADDER, header, rows, 2)
    assert "6.0," in (floats / LADDER).read_text(encoding="utf-8")
    assert ([line.split(",")[0] for line in as_floats.splitlines()]
            == [line.split(",")[0] for line in text.splitlines()])
    model = _read(folder, "block")
    try:
        ladder = model.Data.inforce_segments().reset_index()
        n, first = len(rows), _committed_ladder()
        assert len(model.Data.model_point_table()) == 2 * n
        assert len(ladder) == 2 * len(first)
        second = ladder.iloc[len(first):].reset_index(drop=True)
        assert second["point_id"].tolist() == (first["point_id"] + n).tolist()
        assert second.drop(columns="point_id").equals(
            ladder.iloc[:len(first)].reset_index(drop=True).drop(columns="point_id"))
        bef_prem = _code(model.Projection, "BEF_PREM")
        for point in sorted(set(first["point_id"])):
            p, q = _point(model, point), _point(model, point + n)
            assert p.proj_len() == q.proj_len()
            assert p.av_pp_at(p.t_entry(), bef_prem) == q.av_pp_at(q.t_entry(), bef_prem)
    finally:
        model.close()
    stray = _sec_inputs(tmp_path / "stray", _committed(),
                        ladder=_ladder_at(2, "point_id", 99)).parent
    with pytest.raises(ValueError) as excinfo:
        tool.companion_text(stray / LADDER, header, rows, 2)
    assert str(excinfo.value) == f"{LADDER}: point_id ['99'] is no point of the table"


def test_the_sample_raises_the_recursion_limit_its_comment_derives():
    """``sample_sec.py`` sets the recursion limit its comment derives, before the import.

    The export does not raise the recursion limit as modelx does (F7), so the sample sets
    it, and its comment records the measured need: a cold ``net_cf`` in the last month of
    the longest frame, issue age 0, issued now or 120 months on, needs a limit of 2,966 in
    the export, and the reports the sample runs in ascending ``t``, the export's import
    among the frames they run under, 438.  The limit is four times the first, rounded up
    to the thousand.  No build can tell a lower limit above the reports' need: a limit of
    1,000 builds the same model.  So this holds the limit, read from the sample's code, to
    the value derived from its comment's need, and holds the call before the import of the
    export.  A change to the need is measured again and written in the comment.
    """
    source = (model_path(SEC).parent / "sample_sec.py").read_text(encoding="utf-8")
    comment = " ".join(line.lstrip("# ") for line in source.splitlines()
                       if line.startswith("#"))
    need = re.search(r"needs a limit of ([\d,]+) in the export", comment)
    reports = re.search(r"which run in ascending t, need ([\d,]+)", comment)
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


# The codes, in their numbering's order: the timings, the count's three and the accounts'
# seven, one numbering; the kinds; and the two code families that select a basis.
TIMING_CODES = ("BEF_NB", "BEF_DECR", "BEF_MAT", "BEF_PREM", "BEF_CREDIT", "BEF_WD",
                "BEF_FEE", "BEF_SWEEP", "BEF_INV", "EOM")
KIND_CODES = ("DEATH", "LAPSE", "MATURITY", "WITHDRAWAL")
BASIS_CODES = (("CURRENT", "GUARANTEED"), ("REMAINING", "ADJ_BEGIN"))


def test_the_spec_sizes_each_cache_as_its_comment_derives():
    """``spec_sec.py`` gives each cache the size its comment derives from the contract.

    The spec check, C3, holds the compiled caches to the spec, and C4 at the contract's
    extremes holds the spec to the largest argument a projection reads; neither sees a
    size one below the comment's, which drops the headroom and reads the same numbers.
    So this reads the spec as mx2cy does, and the bounds of the contract from the model's
    own References, and holds each size to the comment's derivation from them: ``t`` to
    ``12 * (maturity_age - issue_age_min) + the horizon + 2``, ``m`` to
    ``12 * (maturity_age - issue_age_min) + 1``, ``y`` to ``maturity_age - issue_age_min +
    2``, ``a`` to ``maturity_age + 1`` and the ladder's ``k`` to ``seg_term_mth + 2``; every
    2-D cache to ``(t, width)``, one width, the widest of the timings' count, the kinds' and
    ``seg_term_mth``, the slots' (§7.2, *For M16 and later*, item 16); and the codes dense
    from 0, each family in its order.  A change to a bound or a size is derived again in
    the comment and here.
    """
    source = (model_path(SEC).parent / "spec_sec.py").read_text(encoding="utf-8")
    comment = " ".join(line.lstrip("# ") for line in source.splitlines()
                       if line.startswith("#"))
    for formula in ("needs t raised to 12 * (maturity_age - issue_age_min) + the horizon "
                    "+ 2", "needs m raised to 12 * (maturity_age - issue_age_min) + 1",
                    "needs y raised to maturity_age - issue_age_min + 2",
                    "needs a raised to maturity_age + 1",
                    "needs k raised to seg_term_mth + 2",
                    "a higher seg_term_mth needs the width raised to it"):
        assert formula in comment, formula
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    proj, data = _references("Projection"), _references("Data")
    low, end, horizon = proj["issue_age_min"], proj["maturity_age"], data[
        "future_horizon_mth"]
    term = proj["seg_term_mth"]
    timings = [proj[code] for code in TIMING_CODES]
    kinds = [proj[code] for code in KIND_CODES]
    assert timings == list(range(len(timings))), timings
    assert kinds == list(range(len(kinds))), kinds
    for family in BASIS_CODES:
        assert [proj[code] for code in family] == list(range(len(family))), family
    assert proj["basis"] == proj["CURRENT"] and (
        proj["seg_credit_base_conv"] == proj["REMAINING"])
    t = 12 * (end - low) + horizon + 2
    width = max(len(timings), len(kinds), term)
    assert sizes == {"t": t, ("t", "timing"): (t, width), ("t", "kind"): (t, width),
                     ("t", "k"): (t, width), "k": term + 2, "m": 12 * (end - low) + 1,
                     "y": end - low + 2, "a": end + 1}, sizes


def test_the_segment_cells_take_a_slot_and_no_projection_cell_calls_the_engine():
    """The six segment cells take ``(t, k)``, and no projection formula calls the engine.

    R15 keys each segment cell by its slot, ``k``, the months since the segment's
    creation, 0 to ``seg_term_mth - 1``, where ``IUL_US_S`` keys it by the creation month,
    so that every 2-D cache is twelve wide; ``seg_new_pp`` keeps its creation month, of
    one parameter.  And R14 inlines the index engine into ``seg_return``,
    ``seg_credit_rate`` and ``index_credit_pp``, so that the five engine cells, kept for
    S's worked example and T1, each with a dict cache of float and object keys, are called
    by no projection formula: one that called them would cache each segment's credit by
    its floats, on every point, in a dict.  C5 holds the engine to the registry's
    ``"engine"`` cells; this names the two rules, read from the model's source.
    """
    source = (model_path(SEC) / "Projection" / "__init__.py").read_text(encoding="utf-8")
    formulas = {node.name: node for node in ast.parse(source).body
                if isinstance(node, ast.FunctionDef)}
    for name in SEGMENT:
        assert [a.arg for a in formulas[name].args.args] == ["t", "k"], name
    assert [a.arg for a in formulas["seg_new_pp"].args.args] == ["m"]
    calling = {}
    for name, node in formulas.items():
        called = {call.func.id for call in ast.walk(node)
                  if isinstance(call, ast.Call) and isinstance(call.func, ast.Name)}
        if name not in ENGINE and called & set(ENGINE):
            calling[name] = sorted(called & set(ENGINE))
    assert not calling, calling
    assert set(ENGINE) <= set(formulas)


# ---------------------------------------------------------------------------
# The tests that read the committed model and S
#
# sec_read and s_model are first asked for here, once every test that reads models of
# its own has run.


# ---------------------------------------------------------------------------
# D3's closed-form clock and R2's forward recursions, on the committed model


def test_the_policy_clock_is_a_closed_form_and_no_recursion_runs_backward(sec_read):
    """D3 and R2's recursions, on the committed model as it was first swept, cold.

    Both need a model on which nothing had been evaluated yet, which is what the fixture
    held when it made the record asserted here:

    * D3: the policy clock is the closed form.  Called first, ``duration_mth(400)`` on
      the twin of S's point 1 is 400 and evaluates ``duration_mth`` once, where
      ``BasicTerm_SE``'s recursion would evaluate it at all 401 months from 0.
    * R2's recursions run forward: under modelx's recursion limit lowered to
      :data:`CALL_DEPTH`, every committed point is swept, each column in ascending ``t``.
      A forward recursion, through ``t - 1``, finds the month before already cached and
      stays shallow, which is why D3 is asserted on its own.  A backward recursion over the
      frame, through ``t + 1``, keeps every step within the look-ahead but opens a chain as
      long as the frame, which a compiled model would run on the C stack (F7), and fails
      here.  The two rows whose guarantee's expiry reads the account value's chain cold
      after a lapsed guarantee, the twin of S's point 5 and its row restated at 6, sweep
      under their allowance of 192 months beyond it, and every other row under none
      (:func:`_expiry_gap`).
    * No projection cell reads a label accessor (``sex``, ``rate_class``, ``db_option``,
      ``qual_test``, ``premium_type``, ``premium_mode``, ``surr_charge_id``): once every
      point is swept, none holds a key.  The decodes and the per-point joins read
      ``model_point()``, and the accessors are kept for reporting, as Phase 2 declares them
      (USLIB-SEC-PLAN.md R17).
    """
    model, record = sec_read
    assert record["duration_mth(400)"] == 400
    assert record["keys"] == [400]
    assert not record["deep"], f"under a recursion limit of {CALL_DEPTH}: {record['deep']}"
    table = model.Data.model_point_table()
    gapped = {_label(table, "twin", 5, 0), _label(table, "derived", 5, 6)}
    assert record["gaps"] == {point: 192 if point in gapped else 0
                              for point in table.index}, record["gaps"]
    read = {point: labels for point, labels in record["labels"].items() if labels}
    assert not read, f"label accessors read by the sweep, by point: {read}"


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and is not repeated here.


def test_the_count_rolls_forward_through_new_business_and_decrements(sec_model):
    """The count leaves month t by its decrements alone.

    On every committed point and at every ``t`` of its frame, the count carried into
    ``t + 1``, ``pols_if_at(t + 1, "BEF_NB")``, is the count weighting month ``t``,
    ``pols_if(t)``, less its deaths and its lapses, in that order, exactly, the last row
    included, whose survivors are carried into ``t = proj_len()``.  ``IUL_US_S`` lapses no
    policy for insufficiency, so there is no other outflow.  And ``"BEF_MAT"``, the count
    before any maturity, is the ``"BEF_DECR"`` count in every month, that one included,
    ``IUL_US_S``'s meaning, since nothing matures in the frame, and ``pols_maturity`` is
    0.0.

    ``result_pols()`` sets the same movement out row by row, in :data:`RESULT_POLS`'s
    columns, indexed by ``t`` over the frame: ``pols_if`` at ``t + 1`` is ``pols_if`` less
    the outflows at ``t``, to 1e-12, plus the new business of ``t + 1``, and row 0 opens
    from ``pols_if_init()``.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        bef_nb, bef_decr, bef_mat = (_code(p, x) for x in ("BEF_NB", "BEF_DECR", "BEF_MAT"))
        end = p.proj_len()
        for t in range(end):
            assert p.pols_if_at(t + 1, bef_nb) == _survivors(p, t + 1), (point_id, t)
            assert p.pols_if(t) == p.pols_if_at(t, bef_decr), (point_id, t)
            assert p.pols_maturity(t) == 0.0, (point_id, t)
        assert all(p.pols_if_at(t, bef_mat) == p.pols_if_at(t, bef_decr)
                   for t in range(end + 1)), point_id
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(end))
        carried = (pols["pols_if"] - pols[OUTFLOWS].sum(axis=1)).shift(1)
        expected = carried.fillna(p.pols_if_init()) + pols["pols_new_biz"]
        assert ((pols["pols_if"] - expected).abs() <= 1e-12).all(), point_id


def test_result_pols_is_s_report_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's, column for column, with ``pols_new_biz`` second (D5).

    T1 skips the report as a whole, because its frame has a column S's lacks (the spec's
    exempt), so it is compared here, on every twin, all at offset 0, S's five points of
    new business.  Every column S's report has agrees, to 1e-9 relative with no absolute
    floor, frames ending together, and ``pols_new_biz`` holds the count in the issue month
    and 0 in every other.
    """
    table = sec_model.Data.model_point_table()
    twins = table.index[table["row_kind"] == "twin"].tolist()
    assert twins == sorted(s_model.Data.model_point_table().index)
    for point_id in twins:
        p = _point(sec_model, point_id)
        mine, theirs = p.result_pols(), _point(s_model, point_id).result_pols()
        assert list(mine.columns) == [theirs.columns[0], "pols_new_biz",
                                      *theirs.columns[1:]], point_id
        assert frame_mismatches(theirs, mine, atol=0.0) == [], point_id
        assert list(mine["pols_new_biz"]) == [
            p.policy_count() if t == 0 else 0.0 for t in mine.index], point_id


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_inputs_are_what_s_generates(s_model):
    """The SEC table and its segment ladder are what IUL_US_S and its table generate today.

    ``model_point_table_sec.csv`` and ``inforce_segments_sec.csv``, every row and column,
    the text cells, the opening-state columns and every segment included: an edit to an S
    row the table copies or derives from, or to an S formula a row's state or a segment is
    read from, fails here until ``python tools/gen_sec_points.py IUL_US_SEC`` regenerates
    both, in the same commit.  Text and integers compare exactly, and a float by its value,
    to 1e-12, because the text the writer picks for a computed float depends on the
    platform's parser (§5.2).
    """
    assert check_generated(SEC, s_model=s_model) == []


def test_the_spec_restates_each_row_and_its_segments_from_s(sec_model, s_model):
    """Each derived row's state and each of its segments are S's own at its month.

    The opening state of each restated row is what the spec's extractors read off S at the
    row's month, each float to 1e-12 relative, and the latch S's 7-pay test failed in any
    month before; and its segments are S's: one row of the ladder for each of its last
    ``min(12, d)`` policy months, slot ``k`` the segment S created at ``d - k``, its
    balance, deductions and draws S's at the close of month ``d - 1``, its cap S's, and its
    start level S's level at its creation rebased onto this model's path, so that its
    return, a ratio of two levels, is S's.  The twins and the future row hold no segment.
    """
    table = sec_model.Data.model_point_table()
    ladder = sec_model.Data.inforce_segments()
    s_points = {policy: point for point, policy
                in s_model.Data.model_point_table()["policy_id"].items()}
    for point_id in table.index:
        held = point_id in ladder.index.get_level_values(0)
        rows = ladder.loc[point_id] if held else None
        if table.at[point_id, "row_kind"] != "derived":
            assert rows is None, point_id
            continue
        d = int(table.at[point_id, "source_mth"])
        s = _point(s_model, s_points[table.at[point_id, "source_policy_id"]])
        state = {"policy_count": s.pols_if(d),
                 **{column: extract(s, d) for column, extract in SPEC.state.items()}}
        for column, value in state.items():
            assert table.at[point_id, column] == pytest.approx(value, rel=1e-12,
                                                               abs=0.0), (point_id, column)
        assert table.at[point_id, "is_mec_init"] == int(any(s.is_mec(u)
                                                            for u in range(d)))
        assert list(rows.index) == list(range(1, min(12, d) + 1)), point_id
        base = s.index_level_init / s.index_level(d)
        for k in rows.index:
            m = d - k
            want = (s.seg_bal_pp(d - 1, m), s.seg_ded_cum_pp(d - 1, m),
                    s.seg_wd_cum_pp(d - 1, m), s.index_level(m) * base, s.index_cap_at(m))
            got = tuple(rows.loc[k, column] for column in LADDER_VALUES)
            assert got == pytest.approx(want, rel=1e-12, abs=1e-12), (point_id, k)


def test_every_committed_row_continues_its_s_point(sec_model, s_model):
    """Each derived and future row of the committed table is its S point from its month on.

    T6 holds the committed table to what the generator makes of S, each float to 1e-12
    absolute and relative, which pins a count as small as the row's of S point 1 at 888,
    1.0e-10, only to about a percent.  So each derived and future row is projected too,
    and compared with its S point frame by frame and cell by cell at the shipped
    References (USLIB-SEC-PLAN.md §7.1, *Precised at M3*, item 11): ``IUL_US_S`` ships
    inflation at 0 and no improvement, so nothing on the valuation clock moves a count,
    and every value is held to 1e-9 relative with no absolute floor, but S's roundings
    about zero, each held to its floor, as on S's point 5 at its month 384, where a
    segment closes on one, and the index level, on the valuation clock, with the latch
    against S's 7-pay test failed so far (:func:`_continues_s`), as T2 and T3 compare a
    row.
    """
    table = sec_model.Data.model_point_table()
    s_points = {policy: point for point, policy
                in s_model.Data.model_point_table()["policy_id"].items()}
    rows = table.index[table["row_kind"] != "twin"].tolist()
    assert rows, "the committed table has no derived or future row"
    for point_id in rows:
        kind, month = table.at[point_id, "row_kind"], int(table.at[point_id, "source_mth"])
        theirs = _point(s_model, s_points[table.at[point_id, "source_policy_id"]])
        mine = _point(sec_model, point_id)
        term = s_model.Projection.seg_term_mth
        exempt, arg_map = ((SPLICE_EXEMPT, _carried_segments(month, term))
                           if kind == "derived" else (FUTURE_EXEMPT, _issued_later))
        found = _continues_s(theirs, mine, month, exempt, arg_map)
        assert found == [], (point_id, found)


# ---------------------------------------------------------------------------
# The product's own facts, on the committed model


def test_the_two_clocks_on_the_shipped_points(sec_model):
    """``t`` counts from the valuation date; ``duration_mth(t)`` from issue (D3, D4).

    On the twin of S's new business the two coincide, its policies enter as new business
    at ``t = 0``, and its frame is 912 months, to policy month 912 at attained age 121,
    where the projection ends.  The row of S point 1 at 60 is on its fifth anniversary at
    attained age 50, its premium falling at ``t = 0`` and the segment its fourth
    anniversary's premium swept maturing there; the row of S point 4 at 65, mid-year, has
    its anniversaries at ``t = 7`` and ``19`` and twelve segments live, one maturing each
    month; the row of S point 5 at 384 opens with its fixed account below 0, the account
    value above, and a loan and its collateral, and the row at 605 with its account value
    below 0, -241.18; the row at 888 has a frame of 24 months.  The point issued 25 months
    on has nothing in force and nothing to do before ``t = 25``, and before issue its policy
    years are -2, -1 and 0, which the guards must answer for.  Expense inflation is
    ``(1 + inflation_rate)^(t // 12)`` on every row alike, and the index path is one path
    for every row, ``index_level_init`` at the valuation date.

    ``pols_if_at``'s ``"BEF_NB"`` counts the policies before the month's new business, so
    in the issue month it is 0 where ``pols_if`` holds the issued count; ``"BEF_MAT"``
    keeps ``IUL_US_S``'s meaning, that count, since nothing matures; and a timing or a kind
    the model does not know is refused by every cell that takes one, rather than answered
    with another value.
    """
    twin = _row(sec_model, "twin", 2, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 911)] == [0, 1, 911]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0), twin.pols_if(0)) == (
        0, 0.0, 1.0, 1.0)
    assert twin.maturity_mth() == twin.proj_len() == 912
    assert twin.is_active(911) and not twin.is_active(912)
    assert twin.pols_if_at(0, _code(twin, "BEF_MAT")) == twin.pols_if(0) == 1.0
    assert twin.pols_if_at(0, _code(twin, "BEF_NB")) == 0.0
    anniv = _row(sec_model, "derived", 1, 60)
    assert (anniv.duration_mth(0), anniv.policy_year(0), anniv.age(0), anniv.proj_len(),
            anniv.premium_pp(0) > 0.0, anniv.seg_bal_pp_init(12) > 0.0) == (
        60, 6, 50, 852, True, True)
    mid = _row(sec_model, "derived", 4, 65)
    assert (mid.policy_year(0), mid.age(0), mid.proj_len(), mid.seg_count(0)) == (
        6, 50, 847, 12)
    assert [t for t in range(24) if mid.duration_mth(t) % 12 == 0] == [7, 19]
    loaned = _row(sec_model, "derived", 5, 384)
    assert loaned.fa_pp_init() < 0.0 < loaned.av_pp_init()
    assert loaned.loan_bal_init() == loaned.lca_pp_init() > 0.0
    exhausted = _row(sec_model, "derived", 5, 605)
    assert exhausted.av_pp_init() == pytest.approx(-241.18, abs=0.005)
    assert _row(sec_model, "derived", 1, 888).proj_len() == 24
    fut = _row(sec_model, "future", 4, -25)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-25, 25, 937)
    assert [fut.policy_year(t) for t in range(26)] == [-2] + [-1] * 12 + [0] * 12 + [1]
    assert not any(fut.is_active(t) for t in range(25)) and fut.is_active(25)
    assert (fut.pols_if(24), fut.pols_new_biz(25), fut.pols_if(25), fut.premium_pp(25)) == (
        0.0, 1.0, 1.0, 10000.0 / 12)
    points = [projection(sec_model, key) for key in point_keys(sec_model)]
    for t in (0, 1, 12, 23):
        assert {p.index_level(t) for p in points} == {
            twin.index_level_init * (1 + twin.index_return_ann) ** (t / 12)}, t
    for p in points:
        assert all(p.inflation_factor(t) == (1 + p.inflation_rate) ** (t // 12)
                   for t in range(p.proj_len() + 1))
    for name, rest in (("pols_if_at", ()), ("av_pp_at", ()), ("av_at", ()),
                       ("fa_pp_at", ()), ("lca_pp_at", ())):
        _refused(lambda: twin.cells[name](0, *rest, "BEF_LUNCH"), "invalid timing")
    for name in ("claim_pp", "claims_from_av"):
        _refused(lambda: twin.cells[name](0, "LUNCH"), "invalid kind")


def test_every_guarded_cell_holds_its_outside_cover_value(sec_model):
    """Outside cover each monthly cell holds its value, and no table is read past cover.

    The sets of the guard (:data:`GUARD_SETS`) are disjoint and together hold every cell of
    the model whose first parameter is ``t``, so a new cell must be placed in one before
    this test passes.  Then on every committed point, once swept, at the shipped
    References, in every month before issue and at ``t = proj_len()``, the month after the
    frame, which the roll-forwards read, every one of them holds its value
    (:func:`_outside_cover_faults`); the splice's rows are held to the same in the splice's
    class, where the survivors carried there are not zero.

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


def test_the_index_path_runs_on_the_valuation_clock_and_the_credits_stay_s(sec_model,
                                                                           s_model):
    """Each segment's credit is S's; the level it is read from is the valuation clock's.

    ``IUL_US_S`` reads its index at ``duration_mth(t)``, a path of each point's own from
    its issue; this model at ``t``, one path for every point, whose level at the valuation
    date is ``index_level_init`` (D7).  So on a row restated at S's month ``d``, the level
    in every month is S's at ``t + d`` over ``(1 + index_return_ann)^(d / 12)``, to 1e-12,
    and on a twin it is S's; and every segment carried in reads its start level from the
    ladder, on the same path, so that its return, a ratio of two levels, and the cap it
    was created under are S's, to 1e-12, in each of the twelve months the ladder's segments
    mature on the row of S point 4 at 65, and so is every credit (T2).  A segment created
    in the frame reads its start level and its cap on the path at ``t - 12``.
    """
    table = sec_model.Data.model_point_table()
    s_points = {policy: point for point, policy
                in s_model.Data.model_point_table()["policy_id"].items()}
    for point_id in table.index[table["row_kind"] != "future"]:
        p = _point(sec_model, point_id)
        d = int(table.at[point_id, "source_mth"])
        sp = _point(s_model, s_points[table.at[point_id, "source_policy_id"]])
        shift = (1 + p.index_return_ann) ** (d / 12)
        for t in (0, 1, 11, 12, p.proj_len() - 1):
            assert p.index_level(t) == pytest.approx(sp.index_level(t + d) / shift,
                                                     rel=1e-12), (point_id, t)
    mid = _row(sec_model, "derived", 4, 65)
    sp = _point(s_model, 4)
    for t in range(13):
        assert mid.seg_return(t) == pytest.approx(sp.seg_return(t + 65), rel=1e-12), t
        assert mid.seg_index_cap(t) == sp.index_cap_at(t + 65 - 12), t
        if t < 12:
            assert mid.seg_index_start(t) == mid.seg_index_start_init(12 - t), t
    assert mid.seg_index_start(12) == mid.index_level(0)


def test_the_worked_example_is_s_through_this_models_engine(sec_model, s_model):
    """The worked example's credits come out of this model's engine cells as out of S's.

    ``IUL_US_S``'s engine cells, which take floats, are kept at stage E (R14): the credited
    rate, the credit base, the credit and the matured value of the technical notes' worked
    example, 10.00% on scenario A's 12% return and 0.00% on scenario B's -15%, a credit of
    1,182.00 and a matured value of 13,002.00 on a segment of 12,000.00 charged 180.00, and
    the adjusted-beginning base's 1,191.00 and the guaranteed cap's 236.40, are the same
    numbers in both models, through the projection's explicit cap and convention as well as
    through S's defaults, which the projection never reads.
    """
    p, sp = _row(sec_model, "twin", 1, 0), _point(s_model, 1)
    cap = p.index_cap_at(0)
    for x in (p, sp):
        assert x.index_change(4500.0, 5040.0) == pytest.approx(0.12, abs=5e-7)
        assert x.index_credit_rate(0.12) == x.index_credit_rate(0.12, cap) == 0.10
        assert x.index_credit_rate(-0.15) == x.index_credit_rate(-0.15, cap) == 0.0
        assert x.index_credit(12000.0, 180.0, 0.12, _code(x, "REMAINING"),
                              cap) == pytest.approx(
            1182.0, abs=0.005)
        assert x.seg_matured_value(12000.0, 180.0, 0.12) == pytest.approx(13002.0,
                                                                          abs=0.005)
        assert x.index_credit(12000.0, 180.0, 0.12, _code(x, "ADJ_BEGIN"),
                              cap) == pytest.approx(
            1191.0, abs=0.005)
        assert x.index_credit(12000.0, 180.0, 0.12, None,
                              x.index_cap_guar) == pytest.approx(236.4, abs=0.005)


def test_point_5_is_exhausted_where_s_says_and_this_model_carries_it(sec_model, s_model):
    """S's point 5 is exhausted at the months S's tests pin, and its rows carry it on.

    ``IUL_US_S`` lapses no policy for insufficiency, and charges an exhausted policy on, its
    fixed account carrying what the segments cannot.  On the twin of S's point 5, as on S's
    point, the loan passes the cash value at ``t = 383``, policy year 32, where the net
    cash value is 0 and the shortfall test fails, the fixed account enters 384 below 0, and
    the account value closes 604 at -241.18; the row restated at 384 opens with its fixed
    account below 0 and the loan, and the row at 605 with its account value below 0, each
    projecting on with every check holding, the margin's included.  ``IUL_US_S``'s margin
    check is ``False`` on the point, from the loan past the cash value on, and this model's
    ``True``, its identity stated with the debt a surrender recovers.
    """
    twin, sp = _row(sec_model, "twin", 5, 0), _point(s_model, 5)
    for x in (twin, sp):
        over = [t for t in range(240, x.proj_len()) if x.loan_bal_pp(t) > x.csv_pp(t)]
        assert over[0] == 383 and x.policy_year(383) == 32
        assert x.ncsv_pp(383) == 0.0 and x.is_shortfall(383)
        bef_prem = _code(x, "BEF_PREM")
        assert x.fa_pp_at(384, bef_prem) < 0.0 <= x.fa_pp_at(383, bef_prem)
        assert x.av_pp(604) == pytest.approx(-241.18, abs=0.005) and x.av_pp(603) > 0.0
    assert sp.check_margin() is False and twin.check_margin() is True
    for month in (384, 605):
        p = _row(sec_model, "derived", 5, month)
        assert tuple(p.cells[c]() for c in CHECKS) == (True,) * 4, month
    assert _row(sec_model, "derived", 5, 384).fa_pp_init() < 0.0
    assert _row(sec_model, "derived", 5, 605).av_pp_init() < 0.0


def test_the_margin_identity_holds_once_a_loan_exceeds_the_cash_value(sec_model, s_model):
    """Once the loan exceeds the cash value, the margin identity still closes.

    ``IUL_US_S``'s identity adds back the whole loan on every lapse,
    ``L(t) x pols_lapse(t)``, as though the lapse claim were ``CSV - L``.  The claim is the
    net cash value, floored at 0, so once the loan exceeds the cash value the identity is
    off by ``(CSV(t) - L(t)) x pols_lapse(t)``, and ``IUL_US_S``'s ``check_margin`` fails
    on a projection that is right, as on its point 5 from ``t = 383``.  This model's adds
    back the loan the surrender recovers, ``min(L(t), CSV(t)) x pols_lapse(t)``, as
    ``UL_US_SEC``, ``VUL_US_SEC`` and ``ULSG_US_SEC`` do.  On the twin of S's point 5,
    which is S's point in every cell but ``check_margin`` (T1):

    * the loan exceeds the cash value in every month from 383, with lapses there;
    * in each month with lapses S's identity misses by ``(CSV - L) x pols_lapse``, to the
      identity's own tolerance, and ``IUL_US_S``'s ``check_margin`` is ``False``;
    * and this model's margin residual is within 1e-9 in every month, its check ``True``,
      and the other three checks hold in both models; where the loan is within the cash
      value, the two identities are one.
    """
    p, sp = _row(sec_model, "twin", 5, 0), _point(s_model, 5)
    months = range(p.proj_len())
    over = [t for t in months if p.loan_bal_pp(t) > p.csv_pp(t)]
    assert over == list(range(383, p.proj_len()))
    assert any(p.pols_lapse(t) > 0.0 for t in over)
    for t in months:
        if not p.pols_lapse(t) > 0.0:
            continue
        s_rhs = (p.margin_expense(t) + p.margin_mortality(t) + p.av_change(t)
                 - p.inv_income(t) - p.index_credits(t)
                 + p.loan_bal_pp(t) * p.pols_lapse(t) + p.net_loan_cf(t))
        gap = p.net_cf(t) - s_rhs
        floored = (min(p.loan_bal_pp(t), p.csv_pp(t)) - p.loan_bal_pp(t)) * p.pols_lapse(t)
        assert abs(gap - floored) <= 1e-9 * max(abs(p.net_cf(t)), abs(s_rhs), 10.0), t
    assert all(abs(p.check_margin_resid(t)) <= 1e-9 for t in months)
    assert tuple(p.cells[c]() for c in CHECKS) == (True,) * 4
    assert tuple(sp.cells[c]() for c in CHECKS) == (True, True, True, False)


def test_each_opening_column_opens_its_chain(s_model, tmp_path):
    """Each opening-state column moves the projection as S's own state there does.

    ``IUL_US_S`` opens a point in force with its fixed account at the account value less
    the loan, the face at issue, both premium accumulators at 0, no latch and no live
    segment; each column of this model's opening state carries what S's own projection
    holds there instead.  So rows restated by the generator from S at the shipped
    References are read beside rows of their own that open one column as ``IUL_US_S``'s
    in-force entry would:

    * the row of S point 5 at 24, its guarantee holding on the accumulator it carries,
      $9,480.00, its two premiums less a year of withdrawals, which would fail at ``t = 0``
      on an accumulator restarted at 0;
    * the row of S point 5 at 384, its face cut to $175,600 by twenty-six years of
      withdrawals, which would die for $249,800 on the face at issue;
    * the row of S point 4 at 65, its account value $47,950.61 in twelve live segments and
      none in its fixed account, which ``Data`` refuses opened at the account value less
      the loan, the ladder then counted twice; the same row with each segment's cap
      declared at 5%, below the 10% in force, whose segments carried in credit the 5% they
      were created under, below their return of 6.4%, where those it creates credit the
      6.4% under the cap in force; and the same row with each segment's start level 1%
      above the path's, whose segments carried in return the less for it, where those it
      creates start on the path;
    * and on a copy of S point 1 paying $25,000 a year, the row restated at 85, past the
      7-pay test's years with the latch carried, a MEC, which with no latch would not be.
    """
    spec = dataclasses.replace(SPEC, derived=((5, 24), (5, 384), (4, 65)), future=())
    table, companions = build_sec_table(spec, s_model)
    table = table.set_index("point_id")
    accum, cut, laddered = (_label(table, "derived", *case)
                            for case in ((5, 24), (5, 384), (4, 65)))

    def opened(label, new, **columns):
        row = table.loc[[label]].assign(policy_id=f"{table.at[label, 'policy_id']}-X",
                                        **columns)
        row.index = pd.Index([new], name="point_id")
        return row

    restarted = opened(accum, 101, cum_prem_net_init=0.0, cum_prem_init=0.0)
    face = opened(cut, 102, sum_assured_init=table.at[cut, "sum_assured"])
    capped, started = opened(laddered, 103), opened(laddered, 104)
    ladder = companions[LADDER]
    copies = pd.concat([ladder[ladder["point_id"] == old].assign(point_id=new)
                        for old, new in ((accum, 101), (cut, 102))])
    own = ladder[ladder["point_id"] == laddered]
    caps = own.assign(point_id=103, seg_index_cap_init=0.05)
    starts = own.assign(point_id=104,
                        seg_index_start_init=own["seg_index_start_init"] * 1.01)
    model = _read(_sec_inputs(
        tmp_path / "sec", pd.concat([table, restarted, face, capped, started]),
        ladder=pd.concat([ladder, copies, caps, starts])), "opened")
    try:
        p, zero = _point(model, accum), _point(model, 101)
        assert p.cum_prem_net_init() == pytest.approx(9480.0, abs=1e-9)
        assert (p.nlg_in_effect(0), zero.nlg_in_effect(0)) == (True, False)
        q, whole = _point(model, cut), _point(model, 102)
        assert (q.sum_assured_init(), whole.sum_assured_init()) == (175600.0, 250000.0)
        assert (q.db_pp(0), whole.db_pp(0)) == (175400.0, 249800.0)
        r, lower = _point(model, laddered), _point(model, 103)
        assert [r.cred_rate_ann(t) for t in range(12)] == pytest.approx(
            [r.index_return_ann] * 12, rel=1e-12)
        assert [lower.cred_rate_ann(t) for t in range(12)] == [0.05] * 12
        assert [lower.seg_index_cap(t) for t in (11, 12)] == [0.05, lower.index_cap_curr]
        assert lower.cred_rate_ann(12) == r.cred_rate_ann(12)
        assert lower.index_credit_pp(0) < r.index_credit_pp(0)
        later, level = _point(model, 104), dict(zip(starts["slot"],
                                                     starts["seg_index_start_init"]))
        assert [later.seg_index_start(t) for t in range(12)] == [level[12 - t]
                                                                 for t in range(12)]
        assert later.seg_index_start(12) == r.seg_index_start(12)
        assert later.seg_return(0) < r.seg_return(0)
        assert later.index_credit_pp(0) < r.index_credit_pp(0)
    finally:
        model.close()
    merged = _set("fa_pp_init", [laddered],
                  table.at[laddered, "av_pp_init"] - table.at[laddered, "loan_bal_init"])(
        table)
    model = _read(_sec_inputs(tmp_path / "merged", merged, ladder=ladder), "merged")
    try:
        assert len(model.Data.model_point_table()) == len(table)
        _refused_exactly(model.Data.inforce_segments, _IDENTITY.format(
            point=laddered).format(file=LADDER))
    finally:
        model.close()
    funded = {8: VARIANTS[8]}
    s = _read(_s_inputs(tmp_path / "s", _s_table_with_variants(funded).loc[[8]],
                        SPLICED_EDITS), "latch_s")
    sec = None
    try:
        built, extra = build_sec_table(dataclasses.replace(SPEC, derived=((8, 85),),
                                                           future=()), s)
        built = built.set_index("point_id")
        row = _label(built, "derived", 8, 85)
        unlatched = built.loc[[row]].assign(is_mec_init=0, policy_id="IUL-900008-X")
        unlatched.index = pd.Index([201], name="point_id")
        ladder = extra[LADDER]
        ladder = pd.concat([ladder, ladder[ladder["point_id"] == row].assign(point_id=201)])
        sec = _read(_sec_inputs(tmp_path / "latch", pd.concat([built, unlatched]),
                                SPLICED_EDITS, ladder=ladder), "latch")
        latched, unset = _point(sec, row), _point(sec, 201)
        assert built.at[row, "is_mec_init"] == 1 and not _seven_pay_failed(latched, 0)
        assert all(latched.is_mec(t) for t in range(latched.proj_len()))
        assert not any(unset.is_mec(t) for t in range(unset.proj_len()))
    finally:
        if sec is not None:
            sec.close()
        s.close()


# ---------------------------------------------------------------------------
# The docstrings, the inputs and the runner


def _docs(model):
    """``(where, docstring)`` for the model, each Space and each cells, blanks as ``""``."""
    yield "model", model.doc or ""
    for space in model.spaces.values():
        yield space.name, space.doc or ""
        for cells in space.cells.values():
            yield f"{space.name}.{cells.name}", cells.doc or ""


def _symbol_map(doc):
    """The rows of the symbol map in ``doc``, the Projection docstring, column by column.

    The map is an RST simple table whose header row starts ``Notes symbol``.  The runs of
    ``=`` in the border under the header give the column spans, and a line whose first two
    columns are blank continues the meaning of the row above.  Returns ``[[symbol, cells,
    meaning], ...]``, each meaning with its continuation lines joined.
    """
    lines = doc.splitlines()
    head = next(i for i, line in enumerate(lines) if line.startswith("Notes symbol"))
    spans = [m.span() for m in re.finditer("=+", lines[head + 1])]
    rows = []
    for line in lines[head + 2:]:
        if line.startswith("="):
            break
        cols = [line[a:b if k < len(spans) - 1 else None].strip()
                for k, (a, b) in enumerate(spans)]
        if cols[0] or cols[1] or not rows:
            rows.append(cols)
        else:
            rows[-1][2] = f"{rows[-1][2]} {cols[2]}".strip()
    return rows


def _mapped_cells(doc):
    """The names in the Cells column of the symbol map in ``doc``: the identifier that
    opens the column, ``age`` of ``age(t)``."""
    names = set()
    for _, cells, _ in _symbol_map(doc):
        found = re.match(r"[a-z_][a-z0-9_]*", cells)
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
    parenthesis where the notes have none (USLIB-SEC-PLAN.md §7.11, Record — M8,
    Docstring tables).
    """
    faults = []
    for row in _map_rows(doc):
        if not all(any(line[k] for line in row) for k in range(len(row[0]))):
            faults.append(f"a blank column in the row of {row[0][1]!r}")
        for above, line in zip(row, row[1:]):
            if re.match(r"[a-z_][a-z0-9_]*\(", line[1]) and not above[1].endswith(","):
                faults.append(f"{line[1]} runs into the row of {row[0][1]!r}")
    return faults


def _doctree_faults(tree):
    """What docutils reads from a docstring into the wrong markup, warning of none of it.

    ``tree`` is the docstring's doctree.  A list in a table cell, which a symbol written as
    an enumerator makes of it, and which renders the cell blank; literal markup inside
    strong or emphasis, as in ``**the notes' ``X_t``**``, which docutils does not nest, so
    that the backticks print; and an identifier split across the lines of a table cell, at
    an underscore or inside a literal, which renders as two words.
    """
    from docutils import nodes
    faults = []
    for entry in tree.findall(nodes.entry):
        row = " / ".join(cell.astext() for cell in entry.parent.findall(nodes.paragraph))
        text = " ".join(cell.astext() for cell in entry.findall(nodes.paragraph))
        if [*entry.findall(nodes.enumerated_list), *entry.findall(nodes.bullet_list)]:
            faults.append(f"a list in a table cell: the row {row!r}")
        if re.search(r"_\n|\n_", text) or any("\n" in literal.astext()
                                               for literal in entry.findall(nodes.literal)):
            faults.append(f"an identifier split across a table cell's lines: {text!r}")
    for node in [*tree.findall(nodes.strong), *tree.findall(nodes.emphasis)]:
        if "``" in node.astext():
            faults.append(f"literal markup inside {node.tagname}: {node.astext()!r}")
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


# What only IUL_US_S's docstrings may say, each phrase a pattern with every space a \s+, so
# that one wrapped across lines still matches: a reference into its Spaces, which the SEC
# pages would link to the wrong model; its clock, t a policy month counted from its own
# start, its projected months and its projection start, its reports indexed by policy
# month and its opening at t == 0 and at the outset, where this model opens at t_entry();
# the first twelve months of a new policy, which a policy in force is past, and the first
# twelve of the frame, t = 0 ... 11, in which S's first segments mature; the README, where
# the sections are in model.md; modelx's advice to clear the cache, which a compiled model
# never does; and two slips of its text.  Each phrase is asserted to be one some docstring
# of IUL_US_S says, so that none holds of nothing.
STALE_PHRASES = (
    r"~\.IUL_US_S\.", r"[Pp]olicy\s+months?\s+(?:``)?t\b", r"the\s+outset",
    r"``t\s+==\s+0``", r"t\s+=\s+0\s+\.\.\.\s+11", r"projection\s+start",
    r"projected\s+months?\b", r"first\s+projected\s+month", r"the\s+README",
    r"clear\s+the\s+cache", r"indexed\s+by\s+policy\s+month", r"first\s+twelve\s+months",
    r"``t\s+=\s+0``\s+is\s+the\s+issue\s+month", r"\bthis\s+cells\b", r"\ba\s+cells\b")
STALE = re.compile("|".join(STALE_PHRASES))


def test_the_docstrings_describe_the_valuation_clock(sec_model, s_model):
    """The docstrings say what this model is, and none says what only IUL_US_S is.

    The model docstring names the valuation date, ``BasicTerm_SE``, the policy clock, the
    SEC table, the segment ladder's file and the product.  The symbol map in the Projection
    docstring maps every cell running in force adds, which are exactly the cells
    ``IUL_US_S`` lacks, every opening-state column and every column of the ladder, and
    names nothing the model lacks: every name in it is a cell or a Reference; and docutils
    reads each of its rows into the right cells (:func:`_map_faults`): each row, with the
    lines under it whose symbol is blank, has text in every column, a symbol, a cell and a
    meaning, and no cell runs into the row above.  No row of a simple table in any docstring
    puts text between two of its columns (:func:`_table_overruns`), which would drop the
    table from the rendered page.  And no docstring says what :data:`STALE` matches, each of
    whose phrases ``IUL_US_S``'s docstrings say.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE, LADDER,
                   "indexed universal life"):
        assert phrase in flat["model"], phrase
    assert set(NEW_CELLS) == set(sec_model.Projection.cells) - set(s_model.Projection.cells)
    rows = _symbol_map(sec_model.Projection.doc)
    mapped = _mapped_cells(sec_model.Projection.doc)
    missing = [cells for cells in (*NEW_CELLS, *STATE) if cells not in mapped]
    assert not missing, f"the symbol map does not map {missing}"
    known = set(sec_model.Projection.cells) | set(sec_model.Projection.refs)
    unknown = sorted(mapped - known)
    assert not unknown, f"the symbol map names what the model lacks: {unknown}"
    empty = [row for row in rows if not all(row)]
    assert not empty, f"symbol map rows without text in every column: {empty}"
    assert _map_faults(sec_model.Projection.doc) == []
    run_in = "\n".join(("Notes symbol  Cells  Meaning", "============  =====  =======",
                        "x             a(t)   One", "              b(t)   Two",
                        "============  =====  ======="))
    assert _map_faults(run_in) == ["b(t) runs into the row of 'a(t)'"]
    overruns = {where: found for where, found in ((where, _table_overruns(doc))
                                                  for where, doc in _docs(sec_model))
                if found}
    assert not overruns, f"table rows that run into a column gap: {overruns}"
    stale = sorted(where for where, doc in flat.items() if STALE.search(doc))
    assert not stale, f"docstrings that describe IUL_US_S: {stale}"
    s_flat = [re.sub(r"\s+", " ", doc) for _, doc in _docs(s_model)]
    unsaid = [phrase for phrase in STALE_PHRASES
              if not any(re.search(phrase, doc) for doc in s_flat)]
    assert not unsaid, f"phrases IUL_US_S does not say, so STALE holds nothing: {unsaid}"
    broken = ("=" * 24 + "  " + "=" * 4 + "\n(the ladder's slot k)   seg_bal_pp_init\n"
              + "=" * 24 + "  " + "=" * 4 + "\n")
    assert _table_overruns(broken) == ["(the ladder's slot k)   seg_bal_pp_init"]


def _doctree(core, doc, stream):
    """``doc``'s doctree, dedented as autodoc dedents it and its Sphinx roles read as plain
    interpreted text, which docutils alone does not know; its warnings go to ``stream``."""
    return core.publish_doctree(re.sub(r":[a-z]+:`", "`", inspect.cleandoc(doc)),
                                settings_overrides={"report_level": 2, "halt_level": 5,
                                                    "warning_stream": stream})


# The faults docutils finds in IUL_US_S's own docstrings, which this model's text corrects:
# five literals inside bold in the Projection Space's docstring, which print their
# backticks.
S_DOCTREE_FAULTS = [("Projection", "literal markup inside strong")] * 5


@pytest.mark.docutils
def test_the_docstrings_parse_as_rst(sec_model, s_model):
    """Every docstring of the model parses as reStructuredText, and renders as written.

    The docs build reads each docstring through docutils, which reports a malformed table, a
    bad indentation or an unclosed inline markup and drops what it cannot read; a raw-text
    test sees none of it.  Each docstring, dedented as autodoc dedents it and its Sphinx
    roles read as plain interpreted text, is parsed here (:func:`_doctree`), and any
    warning or error is a fault.  So is what docutils reads into the wrong markup without a
    warning (:func:`_doctree_faults`): a list in a table cell, literal markup inside strong
    or emphasis, and an identifier split across a table cell's lines.  ``IUL_US_S``'s
    docstrings hold the second, which this model's text corrects, so the check is asserted
    to find those there (:data:`S_DOCTREE_FAULTS`), and the third kind in a table made for
    it.  docutils comes with the docs build, not with the models' requirements, so the test
    is skipped where it is absent; the column checks in the test above run everywhere.
    """
    core = pytest.importorskip("docutils.core")
    faults = []
    for where, doc in _docs(sec_model):
        stream = io.StringIO()
        tree = _doctree(core, doc, stream)
        faults += [f"{where}: {line}" for line in stream.getvalue().splitlines()
                   if re.search(r"\((WARNING|ERROR|SEVERE)/", line)]
        faults += [f"{where}: {fault}" for fault in _doctree_faults(tree)]
    assert not faults, f"{len(faults)} docutils faults, first:\n  " + "\n  ".join(
        faults[:10])
    s_faults = [(where, fault.split(":")[0]) for where, doc in _docs(s_model)
                for fault in _doctree_faults(_doctree(core, doc, io.StringIO()))]
    assert s_faults == S_DOCTREE_FAULTS, s_faults
    split = "\n".join(("=====  ======", "Sym    Cells", "=====  ======", "x      ``BEF_",
                       "       WD``", "y      pols_", "       if", "=====  ======"))
    assert [fault.split(":")[0] for fault in _doctree_faults(
        _doctree(core, split, io.StringIO()))] == [
        "an identifier split across a table cell's lines"] * 2


def _values(refs):
    """The values of ``refs``, a Space's References, each as it compares: a module by its
    name; the Interface to the other Space left out."""
    return {name: value.__name__ if inspect.ismodule(value) else value
            for name, value in refs.items() if name != "data"}


# The References this model adds to IUL_US_S's, on Data, the segment ladder's file and the
# horizon of future business (D4), and the one it leaves out, on Projection, the math
# module, which S's checks alone call, for math.isclose, where this model's checks read
# residual cells instead.
#
# Phase 2 (M19) indexes Projection by position, idx, for S's point_id, and adds the codes,
# each named as S's text (R9, R10), and the contract's issue ages, which proj_len()
# refuses a point outside of; and Data reads numpy, for its vectors.  S's two text
# References that select a basis and a convention, basis and seg_credit_base_conv, are
# codes here, compared with S's through their names.
ADDED_REFERENCES = {"Projection": {"idx": 0, "BEF_NB": 0, "BEF_DECR": 1, "BEF_MAT": 2,
                                   "BEF_PREM": 3, "BEF_CREDIT": 4, "BEF_WD": 5,
                                   "BEF_FEE": 6, "BEF_SWEEP": 7, "BEF_INV": 8, "EOM": 9,
                                   "DEATH": 0, "LAPSE": 1, "MATURITY": 2, "WITHDRAWAL": 3,
                                   "CURRENT": 0, "GUARANTEED": 1, "REMAINING": 0,
                                   "ADJ_BEGIN": 1, "issue_age_min": 0, "issue_age_max": 85},
                    "Data": {"future_horizon_mth": 120, "inforce_segments_file": LADDER,
                             "np": "numpy"}}
DROPPED_REFERENCES = {"Projection": ("math", "point_id"), "Data": ()}
CODED_REFERENCES = ("basis", "seg_credit_base_conv")


def test_the_sec_model_reads_the_s_tables_in_place(sec_model, s_model):
    """One copy of each assumption table serves both models (D1), on S's own References.

    The two ``input_dir()`` s are one directory, and SEC's filename References are S's with
    ``model_point_file`` alone changed, to ``model_point_table_sec.csv``, and the segment
    ladder's added: an edit to a table reaches both models, and the two can never drift
    apart.  And every other Reference of either Space is S's, value for value, but those
    this model adds and the one it leaves out (:data:`ADDED_REFERENCES`,
    :data:`DROPPED_REFERENCES`): a constant copied wrong that changes no number a
    comparison reads, an index floor of 0.001 for S's 0, which no shipped or spliced
    return meets, would otherwise pass every test whose rows never reach it
    (USLIB-SEC-PLAN.md §7.7, *Record — M9*, *References held to S's*).
    """
    assert sec_model.Data.input_dir() == s_model.Data.input_dir()
    files = {r: v for r, v in s_model.Data.refs.items() if r.endswith("_file")}
    assert {r: v for r, v in sec_model.Data.refs.items() if r.endswith("_file")} == {
        **files, "model_point_file": TABLE, "inforce_segments_file": LADDER}
    for space in ("Projection", "Data"):
        theirs = _values(s_model.spaces[space].refs)
        mine = _values(sec_model.spaces[space].refs)
        assert set(DROPPED_REFERENCES[space]) <= set(theirs), space
        theirs = {name: value for name, value in theirs.items()
                  if name not in DROPPED_REFERENCES[space]}
        if space == "Data":
            theirs["model_point_file"] = TABLE
        else:
            theirs.update({name: _code(sec_model.Projection, theirs[name])
                           for name in CODED_REFERENCES})
        assert mine == {**theirs, **ADDED_REFERENCES[space]}, space


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
    live = min(p.seg_term_mth, d)
    held = 0.0
    for k in range(1, live + 1):
        held = held + p.seg_bal_pp_init(k)
    return (f"in force {_months(d)}: policy year {p.policy_year(0)}, attained age "
            f"{p.age(0)}, {p.pols_if(0):.6f} in force, account value "
            f"{p.av_pp_init():,.2f}: fixed account {p.fa_pp_init():,.2f}, segments of the "
            f"last {_months(live)} {held:,.2f}, collateral {p.lca_pp_init():,.2f}; loan "
            f"{p.loan_bal_init():,.2f}, face in force {p.sum_assured_init():,.2f}, "
            f"premiums paid {p.cum_prem_init():,.2f}, no-lapse accumulator "
            f"{p.cum_prem_net_init():,.2f}, {'a MEC' if p.is_mec_init() else 'not a MEC'}")


def _heading(label, origin, p):
    """``run_sec.py``'s first line for point ``p``, labelled ``label``."""
    return (f"model point {label}: {origin} - {p.sex()}{p.age_at_entry()} {p.rate_class()} "
            f"face {p.sum_assured():,.0f} option {p.db_option()} {p.premium_type()}, "
            f"premium {p.premium_pp_ann():,.2f}/yr {p.premium_mode()}, indexed allocation "
            f"{p.index_alloc_rate():.0%}")


# The amounts of the opening state, and of the ladder, an extract carries to the cent.
MONEY = ("av_pp_init", "loan_bal_init", "fa_pp_init", "lca_pp_init", "sum_assured_init",
         "cum_prem_init", "cum_prem_net_init")
LADDER_MONEY = ("seg_bal_pp_init", "seg_ded_cum_pp_init", "seg_wd_cum_pp_init")


def test_an_extract_carried_to_the_cent_is_read(sec_model, tmp_path):
    """The opening state carried to the cent, as an extract carries it, is read and holds.

    D6 tests each rule that holds one amount to another on an extract with every amount
    carried to the cent, not only with one column moved: here the account value's identity
    with its parts, the no-lapse accumulator held to the premiums paid within a cent and a
    half, and each segment held to ``-1e-8`` or more.  The committed table with its seven
    amounts (:data:`MONEY`) and the ladder with its three (:data:`LADDER_MONEY`) rounded to
    the cent are read by ``Data``, every row passes ``proj_len()``, and each holds its four
    checks, as each committed point does: the account value opens from its parts, so the
    carried roundings open one account and ``check_av_components`` holds, and a segment
    closed on a rounding about zero is carried as 0.  Each row projects within a cent a
    policy of its committed row, the committed model's, swept, in every month's net cash
    flow, and the row of S point 4 at 65, whose twelve segments carry the most roundings,
    opens its account value off the column it carries, which ``Data`` admits within its
    slack.
    """
    committed, ladder = _committed(), _committed_ladder()
    table = committed.assign(**{c: committed[c].round(2) for c in MONEY})
    cents = ladder.assign(**{c: ladder[c].round(2) for c in LADDER_MONEY})
    model = _read(_sec_inputs(tmp_path, table, ladder=cents), "cents")
    try:
        assert list(model.Data.model_point_table().index) == list(committed.index)
        assert len(model.Data.inforce_segments()) == len(ladder)
        faults = []
        for label in committed.index:
            p, q = _point(model, label), _point(sec_model, label)
            assert p.proj_len() == q.proj_len(), label
            checks = {check: p.cells[check]() for check in CHECKS}
            if not all(checks.values()):
                faults.append(f"point {label}: {checks}")
            worst = max(abs(p.net_cf(t) - q.net_cf(t)) / p.policy_count()
                        for t in range(p.proj_len()))
            if not worst <= 0.01:
                faults.append(f"point {label}: net_cf off by {worst} a policy")
            _release(model, _key(model, label))
        assert not faults, faults
        p = _row(model, "derived", 4, 65)
        assert p.av_pp_at(0, _code(p, "BEF_PREM")) != p.av_pp_init()
    finally:
        model.close()


def test_an_in_force_extract_needs_none_of_the_generator_columns(sec_model, tmp_path):
    """The model reads the in-force interface and S's columns, never where a row came from.

    ``row_kind``, ``source_policy_id`` and ``source_mth`` record how the generator made each
    shipped row, and an administration extract carries none of them.  Every generated table
    also numbers its points 1, 2, ... in table order, so an extract here is relabelled too,
    ``100 + point_id``, in reverse order, 112 first, and its segment ladder through the same
    map: a label read as a position would then project the wrong point, which no other
    table can show.  Read so, every point projects what the committed point it came from
    projects, in ``result_cf`` and ``result_pols``, to 1e-12, and ``run_sec.py``, run beside
    that extract, prints the point it is given by its label, without saying where it came
    from, and refuses a label the extract lacks, naming the labels it has, or a label that
    is not a number, without a traceback.  Its refusals name the label too: ``Data``'s of a
    malformed row, and ``proj_len()``'s of a point missing a segment of its ladder, which
    ``run_sec.py --block`` meets before it projects any point.
    """
    extract = _committed().drop(columns=list(GENERATED_COLUMNS))
    extract.index = pd.Index(extract.index + 100, name="point_id")
    extract = extract.iloc[::-1]
    ladder = _committed_ladder().assign(point_id=lambda f: f["point_id"] + 100)
    folder = _sec_inputs(tmp_path / "extract", extract, ladder=ladder)
    model = _read(folder, "extract")
    try:
        table = model.Data.model_point_table()
        assert not set(GENERATED_COLUMNS) & set(table.columns)
        assert list(table.index) == list(range(112, 100, -1))
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
    out = _run_sec(runner, "107")
    mid = _row(sec_model, "derived", 4, 65)
    assert out.splitlines()[:2] == [_heading(107, "IUL-000004-M65", mid),
                                    f"at the valuation date: {_standing(mid)}"]
    for label in ("7", "x"):
        done = _run_sec(runner, label, check=False)
        errors = done.stderr.decode(errors="replace")
        assert done.returncode == 1 and done.stdout == b"", label
        assert (f"no model point {label} in the table: {list(range(112, 100, -1))}"
                in errors and "Traceback" not in errors), errors
    model = _read(_sec_inputs(tmp_path / "negative", _set("loan_bal_init", [109], -1.0)(
        extract), ladder=ladder), "negative_loan")
    try:
        _refused(model.Data.model_point_table,
                 "loan_bal_init must be a number, zero or more; it is not at point_id "
                 "[109]")
    finally:
        model.close()
    short = ladder[~((ladder["point_id"] == 106) & (ladder["slot"] == 1))]
    moved = _sec_inputs(tmp_path / "moved", extract, ladder=short)
    message = (f"point_id 106: {LADDER} holds 11 segments, its last in slot 12, where a "
               f"policy in force 60 months holds one a month for its last 12, slots 1 to "
               f"12")
    model = _read(moved, "moved")
    try:
        _refused(_point(model, 106).proj_len, message)
    finally:
        model.close()
    runner = moved.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert message in done.stderr.decode(errors="replace")


@pytest.mark.sec_full
@pytest.mark.skipif(not SEC_FULL, reason="the runner's test runs with USLIB_SEC_FULL=1 "
                    "(USLIB-SEC-PLAN.md K6)")
def test_run_sec_prints_a_point_and_the_block(sec_model, s_model):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  The runner's default is point 1, the twin of S's anchor point, issued at
    the valuation date: its lines at the valuation date, each asserted whole, so that a
    longer number cannot pass for the one asserted, and its first twelve rows of cash
    flows, of the account value, of the segment ladder and of counts, ``IUL_US_S``'s own,
    row for row, since the point is S's point 1 on the same clock.  Point 7, restated in
    force at S's month 65 of S's point 4 with twelve segments, and point 12, to be issued
    25 months on, each with the two lines that say where its row came from and where it
    stands, which only the committed table's generator columns can say.  And the block: a
    line for each of the twelve points, in table order, its first twelve rows, which must
    be the committed points' frames summed row by row, as this test sums them, and those
    frames summed into projection years, each year's count the one in force in its first
    month.  Nothing else runs the runner on the committed table, and this test runs with
    ``USLIB_SEC_FULL=1`` only (K6): by default the runner runs on the extracts and the
    tables ``proj_len()`` refuses, each in an interpreter of its own.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    anchor, s_anchor = _row(sec_model, "twin", 1, 0), _point(s_model, 1)
    out = _run_sec(runner)
    assert out.splitlines()[:3] == [
        _heading(1, "IUL-000001 (S's IUL-000001)", anchor),
        f"at the valuation date: {_standing(anchor)}",
        "proj_len = 912 months from the valuation date (t = 0..911); the projection ends "
        "at policy month 912, attained age 121"]
    for report, digits in (("result_cf", 2), ("result_av", 2), ("result_seg", 4),
                           ("result_pols", 6)):
        assert anchor.cells[report]().head(12).round(digits).to_string() in out, report
    for report, digits in (("result_cf", 2), ("result_av", 2), ("result_seg", 4)):
        assert s_anchor.cells[report]().head(12).round(digits).to_string() in out, report
    for point, kind, s_point, month, origin in (
            ("7", "derived", 4, 65, "IUL-000004-M65 (S's IUL-000004 at its month 65)"),
            ("12", "future", 4, -25,
             "IUL-000004-F25 (S's IUL-000004, issued 25 months on)")):
        p = _row(sec_model, kind, s_point, month)
        assert _run_sec(runner, point).splitlines()[:2] == [
            _heading(point, origin, p), f"at the valuation date: {_standing(p)}"], point
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
# Stage EC -- what compiling changed, held in modelx, on the committed model


def test_the_split_totals_are_s_totals_bit_for_bit(sec_model, s_model):
    """``claims(t)`` is ``IUL_US_S``'s total, and each kind S's kind, bit for bit (R12).

    S's ``claims(t, kind=None)`` is the two kinds and their total in one cell, the total a
    ``sum`` of a generator over the kinds.  Here the kinds are ``claims_death`` and
    ``claims_lapse``, and the total is written out from ``0.0``; T1 reaches S's total
    through the spec's ``twin_arg_map`` to its tolerance, and skips S's keys of a kind.  So
    they are held here, exactly: on the twins of S's five points, which S opens at its own
    ``t = 0``, in every month of the frame, the total equal to S's, its type and the sign
    of a zero included, and each kind equal to S's ``claims(t, kind)``, its type included.
    Python's ``sum`` of two floats is their one rounded sum, so the total written out is
    S's float in every month.
    """
    found = []
    for point in NEW_BUSINESS:
        mine, theirs = _row(sec_model, "twin", point, 0), _point(s_model, point)
        assert mine.proj_len() == theirs.proj_len()
        for t in range(mine.proj_len()):
            got, want = mine.claims(t), theirs.claims(t)
            if (got != want or type(got) is not type(want)
                    or math.copysign(1.0, got) != math.copysign(1.0, want)):
                found.append(f"point {point}: claims({t}) {got!r}, S's {want!r}")
            for cell, kind in (("claims_death", "DEATH"), ("claims_lapse", "LAPSE")):
                got, want = mine.cells[cell](t), theirs.claims(t, kind)
                if got != want or type(got) is not type(want):
                    found.append(f"point {point}: {cell}({t}) {got!r}, S's "
                                 f"claims({t}, {kind!r}) {want!r}")
    assert not found, found[:20]


@pytest.mark.skipif(not EXACT_SUMS, reason="IUL_US_S's sum is compensated from Python 3.12")
def test_the_compensated_sums_are_s_sums_bit_for_bit(sec_model, s_model):
    """``seg_bal_active_pp`` and ``seg_bal_tot_pp`` are ``IUL_US_S``'s ``sum``, bit for bit.

    S sums the live segments with Python's ``sum``, which from Python 3.12 adds floats with
    Neumaier's compensation; a compiled formula has no such builtin, so this model writes
    the loop out, compensated as ``sum`` compensates it, the correction added where it is
    a finite number (USLIB-SEC-PLAN.md R16), so that each sum is S's float.  T1 holds the
    two cells to S at its tolerance, which a plain running sum, off in its last bits,
    passes, and C4 compares the compiled loop with the same loop in modelx.  So they are
    held here, exactly: on the twins of S's five points, which S opens at its own
    ``t = 0``, in every month of the frame, each sum equal to S's, the sign of a zero
    included.  S's ``sum`` of no segment is the int 0 and this model's the float 0.0, so
    the two are compared as numbers.
    """
    found = []
    for point in NEW_BUSINESS:
        mine, theirs = _row(sec_model, "twin", point, 0), _point(s_model, point)
        for t in range(mine.proj_len()):
            for cell in ("seg_bal_active_pp", "seg_bal_tot_pp"):
                got, want = mine.cells[cell](t), theirs.cells[cell](t)
                if got != want or math.copysign(1.0, got) != math.copysign(1.0, want):
                    found.append(f"point {point}: {cell}({t}) {got!r}, S's {want!r}")
    assert not found, found[:20]


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
    exactly.  ``python tools/gen_sec_fingerprint.py IUL_US_SEC --check`` runs the same
    comparison from the command line.
    """
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# IUL_US_SEC's fingerprint, frozen at M13 from the model as Phase 1 left it and committed
# alone, before Phase 2 changed anything.  Each point is keyed by its point_id; each column
# holds (its sum over the frame, its largest absolute value, (its values at the months)).
# The block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a
# refreeze goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: IUL_US_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 912, "months": (0, 227, 455, 683, 911),
        "result_cf": {
            "pols_if": (192.2806881801633, 1.0, (
                1.0, 0.3355274054974994, 0.10768391762744339, 0.005918429425043654, 0.0)),
            "premiums": (127723.36865581936, 10000.0, (
                10000.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (191940.24335051377, 645.3709505884079, (
                31.396677453915387, 59.92146457051111, 353.798212186078, 370.0855744199881,
                0.0)),
            "claims_lapse": (185079.24541899044, 409.54411988003653, (
                16.38214283998015, 284.66170391571137, 356.40200321595745,
                63.11632700716718, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1351.7543011260207, 156.25, (
                156.25, 2.097046284359371, 0.6730244851715212, 0.03699018390652284, 0.0)),
            "premium_taxes": (2554.4673731163875, 200.0, (
                200.0, 0.0, 0.0, 0.0, 0.0)),
            "net_loan_cf": (0.0, 0.0, (
                -0.0, -0.0, -0.0, -0.0, -0.0)),
            "net_cf": (-253202.34178792723, 9595.971179706105, (
                9595.971179706105, -346.6802147705818, -710.8732398872069,
                -433.23889161106183, 0.0)),
        },
        "result_pols": {
            "pols_if": (192.2806881801633, 1.0, (
                1.0, 0.3355274054974994, 0.10768391762744339, 0.005918429425043654, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.17077650937820688, 0.00038119576996242685, (
                0.00012558670981566156, 0.00019328785030840566, 0.0003445762910247962,
                0.0001155518691767327, 0.0)),
            "pols_lapse": (0.8292234906217928, 0.005142366937762858, (
                0.005142366937762858, 0.00113881250294194, 0.00036453011351524815,
                1.9706880886528767e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.426188133861935, 1.0, (
                0.00012558670981566156, 0.0005760717221349188, 0.0031998862840125764,
                0.019524076554461978, 1.0)),
            "lapse_rate_mth": (3.3491756265140427, 0.006924382628299419, (
                0.005143012831822946, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    2: {"rows": 912, "months": (0, 227, 455, 683, 911),
        "result_cf": {
            "pols_if": (192.2806881801633, 1.0, (
                1.0, 0.3355274054974994, 0.10768391762744339, 0.005918429425043654, 0.0)),
            "premiums": (127723.36865581936, 10000.0, (
                10000.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (180263.15086344408, 559.1063552279749, (
                32.589751197164176, 94.26624590699619, 368.74472245709035,
                258.57767326651214, 0.0)),
            "claims_lapse": (162566.06071342377, 403.2722081066813, (
                16.375771898458154, 270.51318204531964, 298.6649836782846, 39.0831105929512,
                0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1351.7543011260207, 156.25, (
                156.25, 2.097046284359371, 0.6730244851715212, 0.03699018390652284, 0.0)),
            "premium_taxes": (2554.4673731163875, 200.0, (
                200.0, 0.0, 0.0, 0.0, 0.0)),
            "net_loan_cf": (0.0, 0.0, (
                -0.0, -0.0, -0.0, -0.0, -0.0)),
            "net_cf": (-219012.06459529084, 9594.784476904377, (
                9594.784476904377, -366.87647423667516, -668.0827306205465,
                -297.69777404336986, 0.0)),
        },
        "result_pols": {
            "pols_if": (192.2806881801633, 1.0, (
                1.0, 0.3355274054974994, 0.10768391762744339, 0.005918429425043654, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.17077650937820688, 0.00038119576996242685, (
                0.00012558670981566156, 0.00019328785030840566, 0.0003445762910247962,
                0.0001155518691767327, 0.0)),
            "pols_lapse": (0.8292234906217928, 0.005142366937762858, (
                0.005142366937762858, 0.00113881250294194, 0.00036453011351524815,
                1.9706880886528767e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.426188133861935, 1.0, (
                0.00012558670981566156, 0.0005760717221349188, 0.0031998862840125764,
                0.019524076554461978, 1.0)),
            "lapse_rate_mth": (3.3491756265140427, 0.006924382628299419, (
                0.005143012831822946, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    3: {"rows": 912, "months": (0, 227, 455, 683, 911),
        "result_cf": {
            "pols_if": (192.2806881801633, 1.0, (
                1.0, 0.3355274054974994, 0.10768391762744339, 0.005918429425043654, 0.0)),
            "premiums": (127723.36865581936, 10000.0, (
                10000.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (113361.99517741842, 343.8497640650438, (
                31.396677453915387, 51.23668625064992, 231.70839378202183,
                177.87327833978466, 0.0)),
            "claims_lapse": (135260.33451973266, 372.04655032914457, (
                16.559467477135883, 244.29677735979948, 234.27014843529426,
                30.446812235369325, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1351.7543011260207, 156.25, (
                156.25, 2.097046284359371, 0.6730244851715212, 0.03699018390652284, 0.0)),
            "premium_taxes": (2554.4673731163875, 200.0, (
                200.0, 0.0, 0.0, 0.0, 0.0)),
            "net_loan_cf": (0.0, 0.0, (
                -0.0, -0.0, -0.0, -0.0, -0.0)),
            "net_cf": (-124805.18271557413, 9595.793855068949, (
                9595.793855068949, -297.63050989480877, -466.6515667024876,
                -208.3570807590605, 0.0)),
        },
        "result_pols": {
            "pols_if": (192.2806881801633, 1.0, (
                1.0, 0.3355274054974994, 0.10768391762744339, 0.005918429425043654, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.17077650937820688, 0.00038119576996242685, (
                0.00012558670981566156, 0.00019328785030840566, 0.0003445762910247962,
                0.0001155518691767327, 0.0)),
            "pols_lapse": (0.8292234906217928, 0.005142366937762858, (
                0.005142366937762858, 0.00113881250294194, 0.00036453011351524815,
                1.9706880886528767e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.426188133861935, 1.0, (
                0.00012558670981566156, 0.0005760717221349188, 0.0031998862840125764,
                0.019524076554461978, 1.0)),
            "lapse_rate_mth": (3.3491756265140427, 0.006924382628299419, (
                0.005143012831822946, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    4: {"rows": 912, "months": (0, 227, 455, 683, 911),
        "result_cf": {
            "pols_if": (200.18986900437739, 1.0, (
                1.0, 0.3496574314028977, 0.11221879770203677, 0.006167671542751287, 0.0)),
            "premiums": (129273.5622068928, 833.3333333333334, (
                833.3333333333334, 202.54936188739458, 44.28423696288661,
                1.6580599539183325, 0.0)),
            "claims_death": (194165.16796074825, 634.4858950690905, (
                31.396677453915387, 62.31666238466947, 368.4309491585528, 385.7626745332781,
                0.0)),
            "claims_lapse": (184466.51496899838, 391.49833263143734, (
                0.0, 296.0402580807593, 371.14242760929915, 65.78998159881777, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1401.1866812773585, 156.25, (
                156.25, 2.1853589462681104, 0.7013674856377298, 0.038547947142195546, 0.0)),
            "premium_taxes": (2585.4712441378565, 16.666666666666668, (
                16.666666666666668, 4.050987237747892, 0.8856847392577322,
                0.03316119907836665, 0.0)),
            "net_loan_cf": (0.0, 0.0, (
                -0.0, -0.0, -0.0, -0.0, -0.0)),
            "net_cf": (-253344.77864826907, 876.3994796679071, (
                629.0199892127514, -162.04390476205023, -696.8761920298608,
                -449.96630532439815, 0.0)),
        },
        "result_pols": {
            "pols_if": (200.18986900437739, 1.0, (
                1.0, 0.3496574314028977, 0.11221879770203677, 0.006167671542751287, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.17794475068552715, 0.0003972490222939648, (
                0.00012558670981566156, 0.0002014277586655395, 0.0003590873915751295,
                0.00012041809136345274, 0.0)),
            "pols_lapse": (0.8220552493144733, 0.005137202704592155, (
                0.0, 0.0011867711790569406, 0.00037988152702983475, 2.0536794428250903e-05,
                0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.426188133861935, 1.0, (
                0.00012558670981566156, 0.0005760717221349188, 0.0031998862840125764,
                0.019524076554461978, 1.0)),
            "lapse_rate_mth": (3.308031523859459, 0.006924382628299419, (
                0.0, 0.003396053198917559, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559)),
        },
    },
    5: {"rows": 912, "months": (0, 227, 455, 683, 911),
        "result_cf": {
            "pols_if": (204.14313983778172, 1.0, (
                1.0, 0.3569440484015955, 0.11455735917813153, 0.006296201516003894, 0.0)),
            "premiums": (81142.57573775708, 6000.0, (
                6000.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (15828.971028500977, 46.23239384229848, (
                31.396677453915387, 42.5233270678493, 6.047969843124791, 0.0, 0.0)),
            "claims_lapse": (17142.907027217472, 110.7966857951484, (
                0.0, 61.314825714244094, 0.0, 0.0, 0.0)),
            "withdrawals": (33626.49939105889, 174.73644999999993, (
                0.0, 62.46520847027921, 20.04753785617302, 1.1018352653006813, 0.0)),
            "expenses": (1425.8946239861355, 156.25, (
                156.25, 2.230900302509972, 0.7159834948633221, 0.03935125947502434, 0.0)),
            "premium_taxes": (1622.8515147551418, 120.0, (
                120.0, 0.0, 0.0, 0.0, 0.0)),
            "net_loan_cf": (-29869.474895748517, 2032.4210068029688, (
                -0.0, -0.0, -0.0, -0.0, -0.0)),
            "net_cf": (-18374.022743510046, 5692.353322546084, (
                5692.353322546084, -168.5342615548826, -26.811491194161132,
                -1.1411865247757056, 0.0)),
        },
        "result_pols": {
            "pols_if": (204.14313983778172, 1.0, (
                1.0, 0.3569440484015955, 0.11455735917813153, 0.006296201516003894, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.18162554865576053, 0.00040552741485364653, (
                0.00012558670981566156, 0.00020562537266851692, 0.00036657052236680534,
                0.00012292752040077957, 0.0)),
            "pols_lapse": (0.8183744513442401, 0.005134569392338102, (
                0.0, 0.0012115026627041929, 0.00038779799310132877, 2.0964766900562536e-05,
                0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.426188133861935, 1.0, (
                0.00012558670981566156, 0.0005760717221349188, 0.0031998862840125764,
                0.019524076554461978, 1.0)),
            "lapse_rate_mth": (3.2874594725321673, 0.006924382628299419, (
                0.0, 0.003396053198917559, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559)),
        },
    },
    6: {"rows": 852, "months": (0, 212, 425, 638, 851),
        "result_cf": {
            "pols_if": (140.7407217904928, 0.7273990569809461, (
                0.7273990569809461, 0.27883712330947724, 0.08686645563504028,
                0.004041165457692752, 0.0)),
            "premiums": (85134.19429247231, 6575.111351777853, (
                6575.111351777853, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (190047.95264381391, 645.3709505884078, (
                34.22315685277804, 93.42234287715482, 455.9504446429573, 351.8046862514718,
                0.0)),
            "claims_lapse": (179669.54934109788, 409.54411988003653, (
                194.78381727859926, 326.74916663419623, 347.94688995064485,
                48.64823907008101, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (879.62951119058, 4.546244106130913, (
                4.546244106130913, 1.7427320206842327, 0.5429153477190017,
                0.0252572841105797, 0.0)),
            "premium_taxes": (1702.6838858494464, 131.50222703555707, (
                131.50222703555707, 0.0, 0.0, 0.0, 0.0)),
            "net_loan_cf": (0.0, 0.0, (
                -0.0, -0.0, -0.0, -0.0, -0.0)),
            "net_cf": (-287165.6210894795, 6210.055906504788, (
                6210.055906504788, -421.91424153203525, -804.4402499413212,
                -400.4781826056634, 0.0)),
        },
        "result_pols": {
            "pols_if": (140.7407217904928, 0.7273990569809461, (
                0.7273990569809461, 0.27883712330947724, 0.08686645563504028,
                0.004041165457692752, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.16320734655140762, 0.00038119576996242685, (
                0.00013689262741111216, 0.0002292152102608468, 0.0003665307671753,
                9.68673710972872e-05, 0.0)),
            "pols_lapse": (0.5641917104295384, 0.003740318643369559, (
                0.003740318643369559, 0.000946167277544073, 0.0002937583465536414,
                1.3395046134466937e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.417285778659874, 1.0, (
                0.00018819467264541423, 0.0008220397898971443, 0.004219474185930161,
                0.023970157151791627, 1.0)),
            "lapse_rate_mth": (3.040594856604666, 0.006924382628299419, (
                0.005143012831822946, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    7: {"rows": 847, "months": (0, 211, 423, 634, 846),
        "result_cf": {
            "pols_if": (142.9177496320974, 0.7380436912913005, (
                0.7380436912913005, 0.28571112564097517, 0.0884760163240132,
                0.00409644469483337, 0.0)),
            "premiums": (83491.52753446279, 555.9442012543714, (
                555.9442012543714, 149.60484106427486, 32.86149684631966,
                1.0576409072713917, 0.0)),
            "claims_death": (192022.66877187145, 634.4858950690904, (
                34.723972720144864, 104.24720512594236, 456.47290658024605,
                342.21724786067017, 0.0)),
            "claims_lapse": (179174.2996328578, 391.49833263143734, (
                174.43268364647682, 336.2445297802052, 348.34554231586975,
                47.32246388290789, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (893.235935200609, 4.612773070570628, (
                4.612773070570628, 1.785694535256095, 0.5529751020250825,
                0.025602779342708562, 0.0)),
            "premium_taxes": (1669.8305506892557, 11.118884025087427, (
                11.118884025087427, 2.9920968212854975, 0.6572299369263932,
                0.021152818145427833, 0.0)),
            "net_loan_cf": (0.0, 0.0, (
                -0.0, -0.0, -0.0, -0.0, -0.0)),
            "net_cf": (-290268.50735615636, 876.3994796679069, (
                331.0558877920916, -295.66468519841425, -773.1671570887476,
                -388.5288264337948, 0.0)),
        },
        "result_pols": {
            "pols_if": (142.9177496320974, 0.7380436912913005, (
                0.7380436912913005, 0.28571112564097517, 0.0884760163240132,
                0.00409644469483337, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.16937475393002016, 0.0003972490222939648, (
                0.00013889589088057945, 0.000256834626159841, 0.00037332226695310924,
                9.819242309877896e-05, 0.0)),
            "pols_lapse": (0.5686689373612808, 0.0037996382615736674, (
                0.0037950538314080458, 0.0009694179581456075, 0.0002992014359857339,
                1.3578277417503657e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.41634480529664, 1.0, (
                0.00018819467264541423, 0.0008989311339684392, 0.004219474185930161,
                0.023970157151791627, 1.0)),
            "lapse_rate_mth": (3.014879792445551, 0.006924382628299419, (
                0.005143012831822946, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    8: {"rows": 906, "months": (0, 226, 452, 678, 905),
        "result_cf": {
            "pols_if": (198.14502332301822, 0.9992467162818198, (
                0.9992467162818198, 0.34983973511988586, 0.11223965003873858,
                0.006152309228702552, 0.0)),
            "premiums": (75142.5757377571, 5871.144719999998, (
                0.0, 0.0, 0.0, 11.670130722408475, 0.0)),
            "claims_death": (15640.650098955944, 46.23239384229848, (
                31.3730268479844, 45.31667937017122, 3.4576499039354114, 0.0, 0.0)),
            "claims_lapse": (17142.907027217476, 110.79668579514839, (
                0.0, 66.72336463245784, 0.0, 0.0, 0.0)),
            "withdrawals": (33626.49939105889, 174.73644999999993, (
                0.0, 61.22195364598003, 19.64193875677925, 1.0766541150229465, 0.0)),
            "expenses": (1238.406395768864, 6.245291976761374, (
                6.245291976761374, 2.1864983444992867, 0.7014978127421161,
                0.03845193267939095, 0.0)),
            "premium_taxes": (1502.851514755142, 117.42289439999998, (
                0.0, 0.0, 0.0, 0.2334026144481695, 0.0)),
            "net_loan_cf": (-29869.474895748517, 2032.4210068029688, (
                -0.0, -0.0, -0.0, -36.91385537221531, -0.0)),
            "net_cf": (-23878.213585747737, 5516.935497182081, (
                -37.61831882474577, -175.44849599310837, -23.801086473456778,
                -26.592233311957344, 0.0)),
        },
        "result_pols": {
            "pols_if": (198.14502332301822, 0.9992467162818198, (
                0.9992467162818198, 0.34983973511988586, 0.11223965003873858,
                0.006152309228702552, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.18087226493758035, 0.00040552741485364653, (
                0.0001254921073919376, 0.00022019766457809147, 0.0003937636944799076,
                0.0001330046152457388, 0.0)),
            "pols_lapse": (0.81837445134424, 0.005134569392338102, (
                0.0, 0.0011873265485791754, 0.00037983458010518937, 2.044187868778923e-05,
                0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.425434613603045, 1.0, (
                0.00012558670981566156, 0.0006294243977249536, 0.0035082405758036783,
                0.021618649242341137, 1.0)),
            "lapse_rate_mth": (3.2874594725321673, 0.006924382628299419, (
                0.0, 0.003396053198917559, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559)),
        },
    },
    9: {"rows": 528, "months": (0, 131, 263, 395, 527),
        "result_cf": {
            "pols_if": (21.529956785260648, 0.17506359449396397, (
                0.17506359449396397, 0.07245007406432317, 0.013475960582347324,
                0.00019619582795042174, 0.0)),
            "premiums": (5126.28828640322, 550.2771938508721, (
                550.2771938508721, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (1317.4485222107937, 28.889362004806184, (
                28.889362004806184, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (3767.7424374206134, 30.636129036443695, (
                30.636129036443695, 12.678762961256556, 2.358293101910782,
                0.03433426989132381, 0.0)),
            "expenses": (134.56222990787904, 1.0941474655872747, (
                1.0941474655872747, 0.45281296290201983, 0.08422475363967077,
                0.001226223924690136, 0.0)),
            "premium_taxes": (102.5257657280644, 11.005543877017443, (
                11.005543877017443, 0.0, 0.0, 0.0, 0.0)),
            "net_loan_cf": (-11256.78406765147, 1050.3815669637838, (
                -1050.3815669637838, -0.0, -0.0, -0.0, -0.0)),
            "net_cf": (-11452.774736515601, 571.7295554967664, (
                -571.7295554967664, -13.131575924158575, -2.4425178555504528,
                -0.03556049381601394, 0.0)),
        },
        "result_pols": {
            "pols_if": (21.529956785260648, 0.17506359449396397, (
                0.17506359449396397, 0.07245007406432317, 0.013475960582347324,
                0.00019619582795042174, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.10229411212754391, 0.00040552741485364653, (
                0.00035463539298037346, 0.0003680189712011967, 0.0001950773083596627,
                9.12345836873647e-06, 0.0)),
            "pols_lapse": (0.07276948236642006, 0.0005933209194344523, (
                0.0005933209194344523, 0.0002447944937835486, 4.51025861270765e-05,
                6.353077191469701e-07, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.18122877673659, 1.0, (
                0.0020257518075387226, 0.005079621738888207, 0.01447594827601395,
                0.04650179600680371, 1.0)),
            "lapse_rate_mth": (1.7931160890284712, 0.003396053198917559, (
                0.003396053198917559, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    10: {"rows": 307, "months": (0, 76, 153, 229, 306),
        "result_cf": {
            "pols_if": (1.3887597469650328, 0.02664514305544116, (
                0.02664514305544116, 0.006594161006076276, 0.0005427274404040737,
                3.4952815271833727e-06, 0.0)),
            "premiums": (227.08897778252646, 51.63036983622137, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (243.03295571888074, 4.662900034702203, (
                4.662900034702203, 1.1539781760633483, 0.0949773020707129,
                0.0006116742672570902, 0.0)),
            "expenses": (8.679748418531455, 0.16653214409650727, (
                0.16653214409650727, 0.04121350628797672, 0.0033920465025254606,
                2.184550954489608e-05, 0.0)),
            "premium_taxes": (4.54177955565053, 1.0326073967244274, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_loan_cf": (-674.4416783438456, 144.66896541382584, (
                -0.0, -0.0, -0.0, -0.0, -0.0)),
            "net_cf": (-703.607184254382, 98.44141130453824, (
                -4.829432178798711, -1.1951916823513251, -0.09836934857323835,
                -0.0006335197768019864, 0.0)),
        },
        "result_pols": {
            "pols_if": (1.3887597469650328, 0.02664514305544116, (
                0.02664514305544116, 0.006594161006076276, 0.0005427274404040737,
                3.4952815271833727e-06, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.02200356635614398, 0.0002881221817005378, (
                0.0002881221817005378, 0.00012874490429508123, 2.244011549343189e-05,
                3.2087679921539607e-07, 0.0)),
            "pols_lapse": (0.004641576699297162, 8.950984505220372e-05, (
                8.950984505220372e-05, 2.195689703478712e-05, 1.7669234341190446e-06,
                1.078044733107467e-08, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (41.05406209061758, 1.0, (
                0.010813309618981415, 0.019524076554461978, 0.041346933696082666,
                0.0918028481310833, 1.0)),
            "lapse_rate_mth": (1.0425883320676905, 0.003396053198917559, (
                0.003396053198917559, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    11: {"rows": 24, "months": (0, 5, 11, 17, 23),
        "result_cf": {
            "pols_if": (1.041752613298826e-10, 1.041752613298826e-10, (
                1.041752613298826e-10, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (2.3361149022914464e-07, 2.3361149022914464e-07, (
                2.3361149022914464e-07, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (0.0010275485372562524, 0.0010275485372562524, (
                0.0010275485372562524, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (6.510953833117662e-10, 6.510953833117662e-10, (
                6.510953833117662e-10, 0.0, 0.0, 0.0, 0.0)),
            "premium_taxes": (4.6722298045828925e-09, 4.6722298045828925e-09, (
                4.6722298045828925e-09, 0.0, 0.0, 0.0, 0.0)),
            "net_loan_cf": (0.0, 0.0, (
                -0.0, -0.0, -0.0, -0.0, -0.0)),
            "net_cf": (-0.0010273202490912112, 0.0010273202490912112, (
                -0.0010273202490912112, 0.0, 0.0, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (1.041752613298826e-10, 1.041752613298826e-10, (
                1.041752613298826e-10, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (1.041752613298826e-10, 1.041752613298826e-10, (
                1.041752613298826e-10, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (24.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lapse_rate_mth": (0.08150527677402142, 0.003396053198917559, (
                0.003396053198917559, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    12: {"rows": 937, "months": (0, 234, 468, 702, 936),
        "result_cf": {
            "pols_if": (200.18986900437739, 1.0, (
                0.0, 0.37548502749353446, 0.12144375299469405, 0.007085394229769159, 0.0)),
            "premiums": (129273.56220689279, 833.3333333333334, (
                0.0, 221.94975239675185, 48.902679821340385, 1.904772060034782, 0.0)),
            "claims_death": (194165.16796074822, 634.4858950690905, (
                0.0, 54.639633578371004, 340.973569641037, 429.6450885484427, 0.0)),
            "claims_lapse": (184466.51496899832, 391.4983326314372, (
                0.0, 279.01325010294266, 376.61381237386144, 73.27391051449897, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1401.1866812773585, 156.25, (
                0.0, 2.3467814218345904, 0.7590234562168379, 0.04428371393605724, 0.0)),
            "premium_taxes": (2585.471244137856, 16.666666666666668, (
                0.0, 4.438995047935037, 0.9780535964268077, 0.03809544120069564, 0.0)),
            "net_loan_cf": (0.0, 0.0, (
                -0.0, -0.0, -0.0, -0.0, -0.0)),
            "net_cf": (-253344.77864826896, 876.3994796679069, (
                0.0, -118.48890775433144, -670.4217792462016, -501.0966061580437, 0.0)),
        },
        "result_pols": {
            "pols_if": (200.18986900437739, 1.0, (
                0.0, 0.37548502749353446, 0.12144375299469405, 0.007085394229769159, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.17794475068552715, 0.0003972490222939648, (
                0.0, 0.00019804734908618194, 0.00035452484313835237, 0.00013833577936055622,
                0.0)),
            "pols_lapse": (0.8220552493144733, 0.005137202704592155, (
                0.0, 0.0012744945494316642, 0.0004112254606185489, 2.3592580073577395e-05,
                0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.42618813386195, 1.0, (
                0.0, 0.0005274440645695044, 0.002919251376839793, 0.019524076554461978,
                1.0)),
            "lapse_rate_mth": (3.308031523859459, 0.006924382628299419, (
                0.0, 0.003396053198917559, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559)),
        },
    },
}
# END generated fingerprint: IUL_US_SEC


# ---------------------------------------------------------------------------
# Compiled (USLIB-SEC-PLAN.md Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython CI job, which sets USLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is IUL's
# own: the comparison on the splice grid, on the second fixture's and the own splices'
# References, at the contract's extremes, on labels that are not text, on keys written as
# floats and where the cap on mortality binds, the refusals, a point without a charge, the
# deepest call, a lapse rate past 1, a Reference set late and the runner.  Each comparison
# on points that all project adds _iul_c4_also's calls, the codes and slots no swept cell
# reaches.  None asks for sec_read, sec_model or s_model, which sweep every committed
# point; the grid test alone asks for spliced.


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)


def _iul_c4_also(proj):
    """What C4 compares of an ``IUL_US_SEC`` point beyond its full sweep (M19).

    ``sec_support.full_sweep`` reaches a cell of more than ``t`` only at the keys some
    swept cell asks of it.  So, as ``sample_sec.py`` does, this calls, at
    ``t = 0 .. proj_len()``, ``pols_if_at`` at ``BEF_MAT``, every account cell at every
    timing it takes and ``av_at`` at ``EOM``, and both claim cells at every kind they
    take; and, on the books, ``t_entry() <= t < proj_len()``, each of the six segment
    cells at every slot ``0 .. min(seg_term_mth - 1, duration_mth(t))``, so that slot 0
    of the share cells and the slots no draw reaches are compiled and compared; then the
    engine cells at the worked example's arguments, ``None`` among them, which no
    projection cell calls.  It calls no cell that raises on a point the contract issues,
    so it is passed only where every point projects.  Passed to
    ``sec_support.compiled_mismatches`` as ``also``.
    """
    av = (proj.BEF_PREM, proj.BEF_CREDIT, proj.BEF_WD, proj.BEF_FEE, proj.BEF_INV)
    fa = av[:4] + (proj.BEF_SWEEP, proj.BEF_INV)
    n = proj.proj_len()
    for t in range(n + 1):
        proj.pols_if_at(t, proj.BEF_MAT)
        for timing in av:
            proj.av_pp_at(t, timing)
            proj.av_at(t, timing)
        proj.av_at(t, proj.EOM)
        for timing in fa:
            proj.fa_pp_at(t, timing)
        for timing in (proj.BEF_PREM, proj.BEF_INV):
            proj.lca_pp_at(t, timing)
        for kind in (proj.DEATH, proj.LAPSE, proj.WITHDRAWAL):
            proj.claim_pp(t, kind)
        for kind in (proj.DEATH, proj.LAPSE, proj.MATURITY):
            proj.claims_from_av(t, kind)
        if proj.t_entry() <= t < n:
            for k in range(min(proj.seg_term_mth - 1, proj.duration_mth(t)) + 1):
                for cell in SEGMENT:
                    proj.cells[cell](t, k)
    proj.index_change(4500.0, 5040.0)
    proj.index_credit_rate(0.12)
    proj.index_credit_rate(0.12, 0.02)
    proj.seg_credit_base(12000.0, 180.0)
    proj.seg_credit_base(12000.0, 180.0, proj.ADJ_BEGIN)
    proj.index_credit(12000.0, 180.0, 0.12)
    proj.index_credit(12000.0, 180.0, 0.12, proj.REMAINING, 0.1)
    proj.seg_matured_value(12000.0, 180.0, 0.12)
    proj.seg_matured_value(12000.0, 180.0, 0.12, proj.REMAINING, 0.1)


def _coded(refs):
    """``refs`` as both engines take them set directly: a text value that names a code of
    the model, ``"GUARANTEED"`` or ``"ADJ_BEGIN"``, as that code, read from the model's
    source.  ``sec_support.compiled_mismatches`` sets each Reference on modelx and on the
    compiled model as given, and the compiled model refuses text in a Reference typed
    ``long long`` with ``TypeError``, so a dict of References written for S and SEC alike
    goes through here first."""
    codes = _references("Projection")
    return {ref: codes[value] if isinstance(value, str) else value
            for ref, value in refs.items()}


# How many rows of a grid C4 compares at once.  compiled_mismatches sweeps every row of its
# case in one modelx read, _iul_c4_also's calls with it, and keeps every value of every
# row, in the parent and in the child, until it compares them.  An IUL row runs up to 912
# months on the grid, and its slot cells and its account timings make a full sweep of a
# 912-month row hold about 0.3 GB in modelx; the whole core grid in one comparison was
# killed at 15 GB, and six rows at a time, the splice's two models alive beside them,
# peaked at 2.4 GB for the process tree on the core grid's 43 rows, in 22 to 30 s a chunk
# (measured at M19, under load), so IUL compares six rows at a time (USLIB-SEC-PLAN.md
# §7.2, *For M16 and later*, item 7).
C4_CHUNK = 6


def _c4_in_chunks(build, root, table, ladder, refs, edits=SPLICED_EDITS):
    """C4 on ``table`` and its ``ladder``, :data:`C4_CHUNK` rows at a time, under ``refs``.

    Each chunk's rows go beside the build with their own segments and ``edits``; modelx
    sweeps every row fully, with every code and slot (:func:`_iul_c4_also`), and the
    compiled model must agree at every argument modelx caches, identically on x86-64 and to
    1e-12 relative elsewhere, with every raise and every ``Data`` array
    (``sec_support.compiled_mismatches``).  Returns the mismatches, each naming its chunk.
    """
    chunks = [table.iloc[i:i + C4_CHUNK] for i in range(0, len(table), C4_CHUNK)]
    assert sum(len(chunk) for chunk in chunks) == len(table)
    found = []
    for i, chunk in enumerate(chunks):
        segments = ladder[ladder["point_id"].isin(chunk.index)]
        folder = compiled_case(build, root / f"chunk{i}", model_points=chunk,
                               edits={**edits, LADDER: segments})
        found += [f"chunk {i}: {line}" for line in compiled_mismatches(
            build, folder, refs=_coded(refs), also=_iul_c4_also)]
        shutil.rmtree(root / f"chunk{i}")
    return found


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_the_splice_grid(spliced,
                                                                             sec_build,
                                                                             tmp_path):
    """C4 on the branches: compiled, every cell of the splice grid is modelx's.

    The sample traces the committed points alone, and they leave branches untaken, which
    are typed all the same, because every branch of a cell returns the one type the
    others return (sample_sec.py).  What the compiled model computes on them is held
    here: the splice grid's points, S's restated in force at T2's months, a segment
    maturing from the ladder and one created in the valuation month among them, and
    issued later, and the variants, every class and sex, both options, the single and the
    target premium, a monthly mode, a second surrender schedule and none, issue ages 50
    and 65, loans, withdrawals from the issue month and a split allocation, under the
    splice's References (:data:`SPLICED_REFS`), on the splice's COI and surrender-charge
    copies (:data:`SPLICED_EDITS`).  The grid is the one this run's ``spliced`` selects,
    the core by default and the full grid under ``USLIB_SEC_FULL=1``, and the test carries
    no ``sec_full`` mark, since a skipped compile test fails the cython job.  The grid's
    SEC table and its ladder go beside the build :data:`C4_CHUNK` rows at a time, and the
    compiled model must agree with modelx at every argument modelx caches, every code and
    slot among them (:func:`_c4_in_chunks`).  Compiled against modelx, every row is exact,
    the restated and the later ones too: §7.4's "only the twins bit for bit" was T2's,
    against S.
    """
    build = sec_build(SEC)
    inputs = spliced[1].Data.input_dir()
    table = pd.read_csv(inputs / TABLE, index_col="point_id")
    ladder = pd.read_csv(inputs / LADDER)
    assert len(table) == len(spliced[1].Data.model_point_table()) > C4_CHUNK
    assert set(ladder["point_id"]) <= set(table.index)
    found = _c4_in_chunks(build, tmp_path, table, ladder, SPLICED_REFS)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_references_of_their_own(
        sec_build, tmp_path):
    """C4 on the second fixture's References and on the own splices': every cell modelx's.

    The main splice runs the current basis and the remaining-balance credit base, and the
    segment term S ships, so the compiled branches of the other codes are held here, each
    on rows the generator builds from S under the References they are compared under
    (:func:`_generated`): the second fixture's, the guaranteed basis, the
    adjusted-beginning credit base and the dynamic lapse multiplier's floor bound
    (:data:`IDLE_REFS`), on S's five twins and the rows this run selects of
    :data:`IDLE_GRID`, the core's by default; a segment term of 6 months, on S's points 1
    and 4 with their own ladders of six; and the 7-pay test failing first in its seventh
    policy year, on variant 21 (:data:`OWN_SPLICES`).  The References' codes are set as
    codes (:func:`_coded`).  Not the splice at a segment term of 24 months: its slots pass
    the twelve-wide caches, where the compiled model raises ``IndexError`` and modelx
    projects (``spec_sec.py``), which the refusals test holds at 13.
    """
    build = sec_build(SEC)
    cases = [("idle", IDLE_REFS, {}, IDLE_GRID, frozenset(CORE_IDLE), None)]
    for name in ("seg_term_mth 6", "7-pay year 7"):
        refs, variants, points, rows = OWN_SPLICES[name]
        cases.append((name, refs, variants, rows, frozenset(rows), points))
    found = []
    for tag, refs, variants, rows, core, points in cases:
        root = tmp_path / tag.replace(" ", "_")
        selected = _selected(rows, core)
        derived = [(p, d) for kind, p, d in selected if kind == "derived"]
        future = [(p, -k) for kind, p, k in selected if kind == "future"]
        folder = _generated(root, refs, variants, derived, future, points=points)
        table = pd.read_csv(folder.parent / TABLE, index_col="point_id")
        ladder = pd.read_csv(folder.parent / LADDER)
        assert len(table) == len(points or NEW_BUSINESS) + len(derived) + len(future), tag
        found += [f"{tag}: {line}" for line in _c4_in_chunks(
            build, root / "c4", table, ladder, refs)]
        shutil.rmtree(root)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


# The committed rows C4 compares with _iul_c4_also's calls, as (row_kind, S point,
# source_mth): the anchor's twin, S's point 4 restated at 65 with twelve segments, S's
# point 1 restated at 888, in force near its end, and the row issued 25 months on.  The
# conventions compare all twelve without them.
COMMITTED_ALSO = (("twin", 1, 0), ("derived", 4, 65), ("derived", 1, 888),
                  ("future", 4, -25))


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_every_code_and_slot(
        sec_build, tmp_path):
    """C4 on committed rows at the codes and slots no swept cell reaches.

    ``test_compiled_conventions.py`` compares the compiled model with modelx on every
    committed point, at every argument a full sweep reaches.  The sweep reaches a timing,
    a kind or a slot only where a swept cell asks for it, so here four committed rows
    (:data:`COMMITTED_ALSO`), new business, a full ladder, a point near its end and one
    issued later, are swept with :func:`_iul_c4_also`'s calls too: every account at every
    timing it takes, both claim cells at every kind, each segment cell at every slot of
    its life, slot 0 of the share cells among them, and the engine at the worked
    example's arguments; and the compiled model must agree at each.  Four rows, not
    twelve, which the conventions' comparison already reads (USLIB-SEC-PLAN.md K6).
    """
    build = sec_build(SEC)
    committed, ladder = _committed(), _committed_ladder()
    labels = [_label(committed, *case) for case in COMMITTED_ALSO]
    found = _c4_in_chunks(build, tmp_path, committed.loc[labels], ladder, {}, edits={})
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


# The COI scales of the extremes' copy, beside the shipped anchor, M NT 45, as (issue age,
# base, ratio), each geometric in the policy year from a base of its own at a ratio of its
# own, to its last policy year: the two issue ages the extremes read, 0 and 85, and 60,
# which none reads, between the anchor and 85 in key order.
EXTREME_COI = ((0, 0.05, 1.07), (60, 0.4, 1.06), (85, 3.1, 1.05))


def _coi_extremes(rates):
    """The extremes' COI scales (:data:`EXTREME_COI`) beside the anchor's, every line in
    reverse key order, so that a scale numbered in file order is another scale's number."""
    added = pd.concat([pd.DataFrame({
        "sex": "M", "rate_class": "NT", "age_at_entry": age,
        "policy_year": range(1, 122 - age),
        "coi_rate_guar": [round(base * ratio ** (y - 1), 6) for y in range(1, 122 - age)],
        "provenance": "test copy"}) for age, base, ratio in EXTREME_COI])
    rates = pd.concat([rates, added], ignore_index=True).sort_values(COI_KEYS,
                                                                    ignore_index=True)
    return rates.iloc[::-1].reset_index(drop=True)


def _mort_from_0(rates):
    """The mortality table with ages 0 to 17, each its own rate, geometric in the age."""
    ages = range(0, 18)
    young = pd.DataFrame({"age": list(ages),
                          "mort_rate": [round(0.0002 * 1.03 ** a, 6) for a in ages],
                          "provenance": "test copy"})
    return pd.concat([young, rates], ignore_index=True)


EXTREME_EDITS = {"coi_rates.csv": _coi_extremes, "mort_table.csv": _mort_from_0}

# The frames of the contract's extremes, in _contract_extremes' order, and the COI
# schedule each reads, its key's place among the copy's four.
EXTREME_FRAMES = [1452, 1572, 432, 1, 847]
EXTREME_SCHEDULES = [1, 1, 4, 2, 2]


def _contract_extremes():
    """Inputs for the contract's longest frames, its oldest issue age, its shortest frame
    and its fullest ladder: a table and its ladder.

    Five points made from the committed rows.  S's point 4 at issue age 0, the youngest
    the contract issues at, issued now, 1,452 months, and 120 months on, the shipped
    ``future_horizon_mth``: a frame of 1,572 months, the longest the contract allows, which
    reads every cache as far as ``spec_sec.py`` sizes it, ``t`` to 1,572 in C4's sweep of
    the month after it, ``m`` to 1,451, the policy year to 121 and the attained age from 0
    to 120.  S's point 1 at 85, the oldest issue age.  S's point 1 restated at 888, moved
    to 911, its last covered month, a frame of one row that opens with the ladder's twelve
    segments, the maturing one in slot 12.  And S's point 4 restated at 65, whose twelve
    segments carried in each mature in the first year.
    """
    committed, ladder = _committed(), _committed_ladder()
    four = _label(committed, "twin", 4, 0)
    rows = pd.concat([
        committed.loc[[four]].assign(age_at_entry=0),
        committed.loc[[four]].assign(age_at_entry=0, duration_mth=-120),
        committed.loc[[_label(committed, "twin", 1, 0)]].assign(age_at_entry=85),
        committed.loc[[_label(committed, "derived", 1, 888)]].assign(duration_mth=911),
        committed.loc[[_label(committed, "derived", 4, 65)]]])
    labels = dict(zip(rows.index[3:], (4, 5)))
    segments = ladder[ladder["point_id"].isin(labels)].assign(
        point_id=lambda f: f["point_id"].map(labels))
    rows.index = pd.Index(range(1, len(rows) + 1), name="point_id")
    return rows, segments


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_contract_extremes(
        sec_build, tmp_path):
    """C4 where the caches end: the contract's longest frames, every cell compiled.

    The five points of :func:`_contract_extremes`, the longest frames the contract allows,
    its oldest issue age, a frame of one row and a full ladder at the valuation date, read
    every cache as far as ``spec_sec.py`` sizes it: ``t`` to 1,572, the month after the
    1,572-month frame, which the roll-forwards read, the creation month to 1,451, the
    policy year to 121 and the attained age from 0 to 120, and the ladder's twelve slots.
    They run under :data:`SWITCHED_ON`, from a COI copy written in reverse key order, with
    a scale no point reads between two that points read, and a mortality table from 0
    (:data:`EXTREME_EDITS`), each key with values of its own, so that a compiled read of
    the key beside the right one, which a padded array allows, changes a number the
    comparison sees.  ``Data``'s numbering of the scales, which both engines share, moves
    both alike, so the comparison cannot see it: it is held against the file by
    :func:`test_the_coi_scales_are_numbered_by_key_on_a_file_out_of_key_order`.  Frames and
    schedules are asserted first.

    modelx sweeps each point fully, with every code and slot (:func:`_iul_c4_also`), and
    the compiled model must agree everywhere.  A cache one too small for the contract
    raises ``IndexError`` compiled where modelx reads on, and fails here, though the spec
    check passes it, which holds the caches to the spec and not the spec to the contract.
    """
    build = sec_build(SEC)
    rows, segments = _contract_extremes()
    folder = compiled_case(build, tmp_path / "extremes", model_points=rows,
                           edits={**EXTREME_EDITS, LADDER: segments})
    model = _read(folder, "extremes_frames", SWITCHED_ON)
    try:
        points = [projection(model, key) for key in point_keys(model)]
        frames = [p.proj_len() for p in points]
        schedules = list(model.Data.coi_schedule())
        assert points[1].age(frames[1] - 1) == 120 and points[1].policy_year(
            frames[1] - 1) == 121
    finally:
        model.close()
    assert frames == EXTREME_FRAMES, frames
    assert schedules == EXTREME_SCHEDULES, schedules
    found = compiled_mismatches(build, folder, refs=SWITCHED_ON, also=_iul_c4_also)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


def _labels_not_text():
    """The labels ``Data`` accepts that are not text, as (case, the table's rows, their
    ladder).

    Made from the committed twins of S's points 1, 2 and 3 and S's point 1 restated at
    888, moved to 911, its last covered month, a frame of one row, with its ladder: on a
    point without a charge, a blank ``surr_charge_id``, NaN as pandas reads it, beside a
    point with one; a blank ``premium_mode`` on a single premium, which never reads its
    mode, and projects; and a blank ``premium_type`` on the one-row frame, which the
    point's first projection refuses.  An id column and a mode column of numbers, ints, on
    single premiums without a charge.  And a blank ``rate_class`` and a blank ``sex``,
    each on the one-row frame alone, which ``Data`` refuses at its class join and the
    point at its COI scale, the label accessors returning NaN all the same.
    """
    committed, ladder = _committed(), _committed_ladder()

    def twin(s_point, **columns):
        return committed.loc[[_label(committed, "twin", s_point, 0)]].assign(**columns)

    last = _label(committed, "derived", 1, 888)

    def one_row(**columns):
        return committed.loc[[last]].assign(duration_mth=911, **columns)

    single = {"premium_type": "SINGLE", "has_surr_charge": False}
    cases = [
        ("blank", pd.concat([twin(1), twin(2, has_surr_charge=False, surr_charge_id=None),
                             twin(3, premium_type="SINGLE", premium_mode=None),
                             one_row(premium_type=None)])),
        ("numeric", pd.concat([twin(3, **single, surr_charge_id=0, premium_mode=1),
                               twin(3, **single, surr_charge_id=9, premium_mode=12)])),
        ("blank class", one_row(rate_class=None)),
        ("blank sex", one_row(sex=None)),
    ]
    out = []
    for case, rows in cases:
        labels = dict(zip(rows.index, range(1, len(rows) + 1)))
        segments = ladder[ladder["point_id"] == last].assign(point_id=labels.get(last, 0))
        rows.index = pd.Index(range(1, len(rows) + 1), name="point_id")
        out.append((case, rows, segments if last in labels else segments.iloc[0:0]))
    return out


@pytest.mark.cython
def test_the_compiled_model_returns_a_label_that_is_not_text_as_modelx_does(sec_build,
                                                                             tmp_path):
    """C4 on labels that are not text: the compiled accessors return what modelx returns.

    ``Data`` accepts a blank ``surr_charge_id`` on a point without a charge, and an id
    column of numbers, since ``IUL_US_S`` never reads such a point's schedule and projects
    it; a blank or numeric mode on a single premium, which never reads it; and a blank
    premium type, which the point's first projection refuses, and a blank class or sex,
    which a join refuses.  modelx returns each label as pandas reads it, NaN or an int,
    and an accessor typed ``str`` would raise ``TypeError`` compiled; the sample types the
    seven as Python objects, from a row with every label blank (sample_sec.py).  So on
    each case of :func:`_labels_not_text`, after checking that the file reads as the case
    says, modelx sweeps every point fully, with every code and slot where no point refuses
    (:func:`_iul_c4_also`), and the compiled model must agree everywhere, the label
    accessors and every raise included.  A sample that blanked the class or the sex alone,
    or left either out, fails on its own case.
    """
    build = sec_build(SEC)
    found = []
    for case, rows, segments in _labels_not_text():
        tag = case.replace(" ", "_")
        folder = compiled_case(build, tmp_path / tag, model_points=rows,
                               edits={LADDER: segments})
        model = mx.read_model(folder, name=_name(f"labels_{tag}"))
        try:
            points = [projection(model, key) for key in point_keys(model)]
            labels = {label: [p.cells[label]() for p in points] for label in LABELS}
        finally:
            model.close()
        if case == "blank":
            ids, modes = labels["surr_charge_id"], labels["premium_mode"]
            types = labels["premium_type"]
            assert ids[0] == "IUL10" and math.isnan(ids[1]), ids
            assert modes[:2] == ["ANNUAL", "ANNUAL"] and math.isnan(modes[2]), modes
            assert types[:3] == ["LEVEL", "LEVEL", "SINGLE"] and math.isnan(types[3]), types
        elif case == "numeric":
            for label, want in (("surr_charge_id", [0, 9]), ("premium_mode", [1, 12])):
                got = labels[label]
                assert got == want and all(isinstance(i, (int, np.integer))
                                           for i in got), (label, got)
        else:
            column = "rate_class" if case == "blank class" else "sex"
            assert math.isnan(labels[column][0]), labels
        also = _iul_c4_also if case == "numeric" else None
        found += [f"{case}: {line}" for line in compiled_mismatches(build, folder,
                                                                     also=also)]
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


@pytest.mark.cython
def test_the_compiled_model_reads_keys_written_as_floats_as_modelx_does(sec_build,
                                                                         tmp_path):
    """C4 on keys written as floats: the compiled model reads 61.0 as 61, as modelx does.

    Every keyed table's key columns written as floats, as a spreadsheet can save them
    (:data:`FLOAT_KEYS`), the model point table's whole-number columns
    (:data:`INT_COLUMNS`) and the ladder's ``point_id`` and ``slot`` too: ``Data`` reads
    each by value, so every extent, every int vector and every padded array's index is an
    int, and the edges test holds modelx to the shipped tables' numbers.  Here the twin of
    S's point 1, S's point 4 restated at 65 with its twelve segments and the row issued 25
    months on, which between them read every table, are swept in modelx with every code
    and slot (:func:`_iul_c4_also`), and the compiled model must agree everywhere, every
    ``Data`` array included, in dtype and shape.  First, in seconds, modelx's ``Data`` on
    the floats is held to its ``Data`` on the same rows as written: every array of the
    same dtype, and every extent and count of the same type, so that a key read as a float
    fails here, naming its cell, and not in the compiled sweep, where each typed read of a
    float array would raise (USLIB-SEC-PLAN.md §7.6, *For M18 and later*, item 11).
    """
    build = sec_build(SEC)
    committed = _committed()
    labels = [_label(committed, "twin", 1, 0), _label(committed, "derived", 4, 65),
              _label(committed, "future", 4, -25)]
    rows = committed.loc[labels]
    segments = _committed_ladder()
    segments = segments[segments["point_id"].isin(labels)]
    as_written = _read(_sec_inputs(tmp_path / "ints", rows, ladder=segments), "keys_ints")
    rows = _as_floats(INT_COLUMNS)(rows)
    folder = compiled_case(build, tmp_path / "floats", model_points=rows, edits={
        **{file: _as_floats(columns) for file, columns in FLOAT_KEYS.items()},
        LADDER: _as_floats(("point_id", "slot"))(segments)})
    for file, columns in (*FLOAT_KEYS.items(), (LADDER, ("point_id", "slot")),
                          (TABLE, INT_COLUMNS)):
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
    found = compiled_mismatches(build, folder, also=_iul_c4_also)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


def _capped_table(tmp_path):
    """The cap test's rows and their ladder, built by the generator from S under
    :data:`CAPPED_REFS`.

    The point of :data:`CAPPED`, alone in a copy of S's table on the splice's COI copy:
    its twin, issued at the valuation date; issued 25 months after it; and restated in
    force in the month before the cap first binds, :data:`CAPPED_MTH`, opened with S's
    count, state and segments there.  As the cap test builds them.
    """
    base, changes = CAPPED
    s = _read(_s_inputs(tmp_path, _s_table().loc[[base]].assign(**changes),
                        SPLICED_EDITS), "capped_rows_s", CAPPED_REFS)
    try:
        spec = dataclasses.replace(SPEC, derived=((base, CAPPED_MTH - 1),),
                                   future=((base, 25),))
        table, companions = build_sec_table(spec, s)
    finally:
        s.close()
    return table, companions[LADDER]


# The References the NaN cases set to NaN before anything computes, as (Reference, the
# rows, by kind, S point and month, and the cell and month the NaN reaches): the A/E, which
# reaches the cap on mortality, min(q, 1.0), bound second; and the index's annual return,
# which reaches the segment's credit, max(index_floor, min(cap, index_par * return)), where
# min keeps the cap, its first argument, and the credit is the cap, in both engines.
NAN_REFS = (("mort_ae_factor", (("twin", 1, 0), ("twin", 3, 0)), "mort_rate", 0),
            ("index_return_ann", (("twin", 1, 0), ("derived", 4, 65)), "seg_return", 12))


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_where_the_cap_binds(sec_build,
                                                                              tmp_path):
    """C4 where ``mort_rate`` caps the annual rate at 1, and where a NaN meets a bound.

    The three rows of the cap's test (:func:`_capped_table`), on whose frames the annual
    rate passes 1 from attained age 113, go beside the build with their segments, under
    :data:`CAPPED_REFS`.  modelx sweeps them fully, with every code and slot
    (:func:`_iul_c4_also`), and the compiled model must agree at every argument modelx
    caches, identically on x86-64 and to 1e-12 relative elsewhere: the side of
    ``min(q, 1.0)`` that returns 1 on a point issued at the valuation date, on one issued
    later and on one in force when it binds.

    And committed rows under each of :data:`NAN_REFS`' References at NaN, which the
    compiled model reads as modelx does: the A/E, so that a NaN reaches the cap on
    mortality, where ``min`` keeps its first argument, the NaN, as in modelx; and the
    index's annual return, so that every return a segment matures on is NaN, and the
    credit's bounds, in S's order, keep the cap, a number, in both engines.  modelx's NaN
    is asserted where it is meant, and C4 holds the compiled values to modelx's, NaN to
    NaN, in every cell it reaches.
    """
    build = sec_build(SEC)
    table, segments = _capped_table(tmp_path / "s")
    folder = compiled_case(build, tmp_path / "capped", model_points=table,
                           edits={**SPLICED_EDITS, LADDER: segments})
    found = compiled_mismatches(build, folder, refs=CAPPED_REFS, also=_iul_c4_also)
    committed, ladder = _committed(), _committed_ladder()
    for ref, cases, cell, month in NAN_REFS:
        labels = [_label(committed, *case) for case in cases]
        folder = compiled_case(build, tmp_path / ref, model_points=committed.loc[labels],
                               edits={LADDER: ladder[ladder["point_id"].isin(labels)]})
        model = _read(folder, f"nan_{ref}", {ref: float("nan")})
        try:
            for key in point_keys(model):
                p = projection(model, key)
                t = max(month, p.t_entry())
                assert math.isnan(p.cells[cell](t)), (ref, key, cell, t)
                if ref == "index_return_ann":
                    assert p.seg_credit_rate(t) == p.seg_index_cap(t) > 0.0, (key, t)
        finally:
            model.close()
        found += [f"{ref}: {line}" for line in compiled_mismatches(
            build, folder, refs={ref: float("nan")}, also=_iul_c4_also)]
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


# The compiled model's own refusals: what it does with a key past the caches spec_sec.py
# sizes, which no projection the contract allows reaches, as (cell, arguments, what modelx
# does, or ("ok", None) where modelx answers with a number).  modelx answers a month after
# cover or before it with a zero, a slot or a creation month outside a segment's life with
# a zero, a policy year or an age past its table with the table's last row and an age
# below it with its first, as the cells say; and it refuses a code past the timings and
# the kinds, a policy year below 1 and a ladder slot the point does not hold, by name.
# Compiled, each is past a cache, and raises IndexError rather than read or write beyond
# it.  Every 2-D cache is twelve wide (spec_sec.py), so the first code and the first slot
# past it are 12.
_NO_SLOT_AT = "ValueError: point_id 1: inforce_segments_sec.csv holds no segment in slot {}"
COMPILED_ONLY = [
    ("net_cf", (1574,), ("ok", 0.0)),
    ("net_cf", (-1,), ("ok", 0.0)),
    ("pols_if_at", (0, 12), ("raised", "ValueError: invalid timing")),
    ("fa_pp_at", (0, 12), ("raised", "ValueError: invalid timing")),
    ("lca_pp_at", (0, 12), ("raised", "ValueError: invalid timing")),
    ("av_pp_at", (0, 12), ("raised", "ValueError: invalid timing")),
    ("av_at", (0, 12), ("raised", "ValueError: invalid timing")),
    ("claim_pp", (0, 12), ("raised", "ValueError: invalid kind")),
    ("claims_from_av", (0, 12), ("raised", "ValueError: invalid kind")),
    *[(cell, (0, 12), ("ok", 0.0)) for cell in SEGMENT],
    *[(cell, (0, -1), ("ok", 0.0)) for cell in SEGMENT],
    ("seg_new_pp", (1453,), ("ok", 0.0)),
    ("seg_new_pp", (-1,), ("ok", 0.0)),
    *[(cell, (14,), ("raised", _NO_SLOT_AT.format(14))) for cell in LADDER_VALUES],
    *[(cell, (-1,), ("raised", _NO_SLOT_AT.format(-1))) for cell in LADDER_VALUES],
    ("lapse_rate_base_py", (123,), ("ok", None)),
    ("lapse_rate_base_py", (-1,), ("raised", "ValueError: point_id 1: lapse_table.csv has "
                                   "no rate for policy year -1")),
    ("coi_rate_guar_py", (123,), ("ok", None)),
    ("coi_rate_guar_py", (-1,), ("raised", "ValueError: point_id 1: coi_rates.csv has no "
                                 "rate for policy year -1")),
    ("corridor_factor_at", (122,), ("ok", None)),
    ("corridor_factor_at", (-1,), ("ok", None)),
    ("mort_rate_base_at", (122,), ("ok", None)),
    ("mort_rate_base_at", (-1,), ("ok", None)),
]

# The codes inside the timing and kind caches that a cell does not take, since one
# numbering serves the timing families and every 2-D cache is the slots' width
# (spec_sec.py): there the cell itself refuses the code, compiled as in modelx.  As
# (cell, the code's name or number).
CODES_IN_CACHE = [("pols_if_at", "BEF_PREM"), ("pols_if_at", "EOM"), ("pols_if_at", 11),
                  ("fa_pp_at", "BEF_NB"), ("fa_pp_at", "EOM"), ("lca_pp_at", "BEF_WD"),
                  ("lca_pp_at", "BEF_SWEEP"), ("av_pp_at", "BEF_SWEEP"),
                  ("av_pp_at", "EOM"), ("av_at", "BEF_MAT"), ("av_at", "BEF_SWEEP"),
                  ("claim_pp", "MATURITY"), ("claim_pp", 11),
                  ("claims_from_av", "WITHDRAWAL"), ("claims_from_av", 11)]


def _refusal_cases():
    """Every refusal the compiled model must make as modelx does, as (case, the table, its
    ladder or None, the edits, the References, [(position, cell, arguments)], the Data
    cells to read).

    A position, not a label, since a table ``Data`` refuses has no keys to give: each is
    the row's place in the table written, ``Projection``'s ``idx``, which the test indexes
    ``Projection`` by in modelx too.
    """
    committed = _committed()
    extract, ladder = _extract()

    def at(table, label):
        return list(table.index).index(label)

    cases = [
        ("past its cover, on the extract", _set("duration_mth", [111], 912)(extract),
         ladder, None, {}, [(at(extract, 111), "proj_len", ())], ()),
        ("beyond the tables, on the extract", extract, ladder, None, {},
         [(at(extract, 107), cell, args) for cell, args, _ in BEYOND if args[0] >= 0]
         + [(at(extract, 108), cell, args) for cell, args, _ in BEYOND_SHORT], ()),
        ("a label written as text, on the extract", _relabelled(107, "7x")(extract),
         ladder, None, {}, [(at(extract, 107), "point_id", ())], ("point_id",)),
        ("a segment term past the slots' width, set first",
         committed.loc[[_label(committed, "twin", 4, 0)]], _committed_ladder().iloc[0:0],
         None, {"seg_term_mth": 13}, [(0, "result_seg", ())], ()),
        ("codes no cell of the family takes, inside the caches", committed, None, None, {},
         [(0, cell, (0, code)) for cell, code in CODES_IN_CACHE], ()),
    ]
    for case, table, ladder_in, edits, refs, label, message, _, _ in ISSUE_AGES:
        if message is not None:
            cases.append((case, table, ladder_in, edits, refs,
                          [(at(table, label), "proj_len", ()),
                           (at(table, label), "result_cf", ())], ()))
    for case, inputs, point, _, refs, _, _ in NOT_ISSUED:
        table, ladder_in = inputs()
        cases.append((case, table, ladder_in, None, refs,
                      [(at(table, point), "proj_len", ()),
                       (at(table, point), "result_cf", ())], ()))
    for case, edit, edits, cell, _, label in UNJOINED:
        table = edit(committed)
        call = (0, "result_cf", ()) if label is None else (
            at(table, label), "point_id" if cell == "point_id" else "result_cf", ())
        cases.append((case, table, None, edits, {}, [call], (cell,)))
    point = _label(committed, "twin", 2, 0)
    for case, column, value, message, _ in UNDECODABLE:
        data = (("class_factor",) if message.startswith("class_factor_table")
                else ("surr_charge_rate_max",) if message.startswith("surr_charge_table")
                else ())
        cases.append((case, _set(column, [point], value)(committed), None, None, {},
                      [(at(committed, point), "result_cf", ())], data))
    for case, edit, _ in MALFORMED:
        cases.append((case, edit(committed), None, None, {}, [(0, "result_cf", ())],
                      ("model_point_table",)))
    for case, edit, _ in MALFORMED_LADDER:
        cases.append((case, committed, edit(_committed_ladder()), None, {},
                      [(0, "result_cf", ())], ("inforce_segments",)))
    for case, file, edit, check, _ in MALFORMED_KEYS + MALFORMED_RATES:
        cases.append((case, committed, None, {file: edit}, {}, [(0, "net_cf", (0,))],
                      (check,)))
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
    (:func:`_refusal_cases`): ``proj_len()`` refuses a point past its cover, naming it by
    ``point_id()``, on the extract labelled otherwise than by position (:func:`_extract`),
    and every case of :data:`ISSUE_AGES` and of :data:`NOT_ISSUED`, issued outside the
    contract's ages, at or past the end of the projection, withdrawing below its fee, or
    holding other than a ladder row for each live segment, on the committed table; each
    reader of a padded table refuses a key outside it, a policy year below 1 and a slot
    the point does not hold, on the extract (:data:`BEYOND` and :data:`BEYOND_SHORT`; a
    key below 0 is past the cache, below); every case of :data:`UNJOINED`, a label written
    as text on the extract among them, of :data:`UNDECODABLE`, each case and whitespace
    variant among them, of :data:`MALFORMED`, of :data:`MALFORMED_LADDER`, and of
    :data:`MALFORMED_KEYS` and :data:`MALFORMED_RATES`, is refused by a projection, and by
    the ``Data`` cell that checks it, compiled as in modelx, so a compiled ``Data`` cell
    refuses each value its modelx cell refuses; and a code a cell does not take, inside
    its cache, is refused by the cell (:data:`CODES_IN_CACHE`).

    And the refusals that are the compiled model's alone (:data:`COMPILED_ONLY`): a month
    past the ``t`` cache either side, a code past the timing and kind caches, a slot past
    the segment caches either side, a creation month past ``m``'s, a ladder slot past the
    readers', a policy year past the ``y`` cache and an age past the ``a`` cache, each
    raising ``IndexError`` compiled, beside what modelx does; and a ``seg_term_mth`` of 13,
    set before anything computes, whose first slot past 11 passes the twelve-wide caches,
    where modelx projects (``spec_sec.py``).

    The cases share one directory, which each case's inputs overwrite in turn, and one
    copy of the compiled package: each child reads its inputs afresh, as the compiled
    ``Data`` reads its files once an import.
    """
    build = sec_build(SEC)
    cases = _refusal_cases()
    cases.append(("compiled only", _committed(), None, None, {},
                  [(0, cell, args) for cell, args, _ in COMPILED_ONLY], ()))
    dest = tmp_path / "refused"
    folder = compiled_case(build, dest)
    found, refused = [], 0
    for case, table, ladder, edits, refs, calls, data in cases:
        edits = dict(edits or {})
        edits[LADDER] = _committed_ladder() if ladder is None else ladder
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
                expected = next(w for c, a, w in COMPILED_ONLY if (c, a) == (cell, args))
                if (expected[1] is None and modelx_did[0] != "ok"
                        or expected[1] is not None and modelx_did != expected):
                    found.append(f"{where}: modelx {modelx_did}, not {expected}")
                if (status, text.split(":")[0]) != ("raised", "IndexError"):
                    found.append(f"{where}: compiled {status} {text!r}, not IndexError")
                continue
            if case.startswith("a segment term past"):
                if modelx_did[0] != "ok":
                    found.append(f"{where}: modelx {modelx_did}, where it projects")
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
    assert refused == sum(len(calls) + len(data) for case, *_, calls, data in cases[:-1]
                          if not case.startswith("a segment term past"))


# The points the compiled schedule test reads, as (the S point whose twin it is made from,
# its surr_charge_id, the schedule's (sc_per_1000_init, runoff_years) pinned at stage E, or
# None where the table lacks the id), each without a charge: the shipped IUL10, the
# splice's IUL07 and IUL99, which no table holds.
UNCHARGED = ((2, "IUL10", (25.0, 10.0)), (3, "IUL07", (30.0, 7.0)), (4, "IUL99", None))
_NO_ROW = ("ValueError: point_id {}: surr_charge_table.csv has no row for its "
           "surr_charge_id")


@pytest.mark.cython
def test_the_compiled_model_reads_the_schedule_of_a_point_without_a_charge(sec_build,
                                                                           tmp_path):
    """Compiled, a point without a charge reads its schedule as modelx does, as at E.

    On the twins of :data:`UNCHARGED`, each without a charge, beside the splice's IUL07,
    the compiled model's ``surr_charge_rate_max()`` and ``surr_charge_runoff_years()`` are
    stage ``E``'s numbers, pinned, of type float, and modelx's, and on the point whose id
    the table lacks each raises stage ``E``'s ``ValueError``, naming the point, with
    modelx's message; ``Data``'s two joins and ``has_surr_charge_schedule`` are modelx's
    arrays, NaN where the id is missing included, and each point's ``net_cf(0)`` is
    modelx's.
    """
    build = sec_build(SEC)
    committed = _committed()
    table = pd.concat([committed.loc[[_label(committed, "twin", s_point, 0)]].assign(
        has_surr_charge=False, surr_charge_id=schedule)
        for s_point, schedule, _ in UNCHARGED])
    folder = compiled_case(build, tmp_path / "uncharged", model_points=table,
                           edits={"surr_charge_table.csv": _surr_charges_with_iul07,
                                  LADDER: _committed_ladder().iloc[0:0]})
    cells = ("surr_charge_rate_max", "surr_charge_runoff_years", "net_cf")
    data = ("surr_charge_rate_max", "surr_charge_runoff_years", "has_surr_charge_schedule")
    calls = [(cell, (0,) if cell == "net_cf" else ()) for cell in cells]
    model = _read(folder, "uncharged_cy")
    try:
        want = {idx: [_modelx_did(lambda: model.Projection[idx].cells[cell](*args))
                      for cell, args in calls] for idx in range(len(table))}
        want_data = {name: model.Data.cells[name]() for name in data}
    finally:
        model.close()
    job = {"refs": {}, "data": list(data),
           "calls": {idx: calls for idx in range(len(table))}}
    got = run_compiled(tmp_path / "uncharged", build.package.name, job)
    assert got["exit"] == 0, got["stderr"]
    assert all(got["compiled"].values()), got["compiled"]
    for idx, (point, (_, _, pinned)) in enumerate(zip(table.index, UNCHARGED)):
        accessors = (("raised", _NO_ROW.format(point)),) * 2 if pinned is None else tuple(
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


# The cold call the stack test makes compiled, in a thread whose stack is reserved at each
# of these sizes in KiB, and then on the main thread.  1 MiB is the size asserted; the
# others bracket what the call needs, and the test reports the smallest that ran.
STACK_KIB = (256, 320, 352, 384, 512, 1024, 2048)

# How long the stack test waits for each child, in seconds: one runs in a few seconds, more
# under load.  A bracketing size may kill its child on a stack overflow by design, and
# where the overflow hangs instead, as Windows Error Reporting could, the wait ends sooner
# than for the two runs asserted, and the size is recorded as timed out.
BRACKET_TIMEOUT, ASSERTED_TIMEOUT = 120, 300


@pytest.mark.cython
def test_the_longest_frame_runs_cold_on_a_one_megabyte_stack(sec_build, tmp_path):
    """The deepest call the contract allows runs compiled on a 1 MiB stack (F7).

    On the two points of :func:`_longest_cover`, S's point 4 at issue age 0, issued now
    and 120 months on, whose cover runs 1,452 months, a cold ``net_cf`` in the last month
    runs the account value's chain from the end of the frame back to ``t_entry()``, 1,451
    months, and the cells above and below it, which modelx bounds on a model just read
    (:func:`test_every_chain_runs_one_cell_a_month_from_a_cold_start`), and compiled it
    runs on the C stack, which the interpreter's recursion limit does not count.  1 MiB is
    the stack MSVC gives an executable's main thread unless the executable asks for more:
    a host that embeds Python, where python.exe itself asks for 2,000,000 bytes.  A thread
    whose stack is reserved at 1 MiB stands in for it on every platform
    (``sec_support.run_compiled``), and in one each call runs cold and returns modelx's
    number, identically on x86-64 (``sec_support.exact_here``) and to 1e-12 elsewhere.
    With gcc the calls need between 320 and 352 KiB, about 230 bytes a level: at the 325
    to 433 bytes a level MSVC took on WholeLife's chain, they would need 470 to 630 KiB,
    and VUL's chain of 1,484 levels, beside this one's, ran on Windows' 1 MiB.  A stack too
    small kills the child, and the test fails naming the stack.  The thread's stack is read
    back too, from Windows or from glibc, and must be at most 1 MiB and a page: a stand-in
    larger than asked for would stand for nothing.  And the calls run again on the child's
    main thread, which is what ``run_sec.py --cython`` runs on.

    No run has measured what the calls need with MSVC.  So they run first at each size of
    :data:`STACK_KIB`, before anything is asserted, and every size's outcome goes into a
    warning, which the job's summary shows, and into the failure, if there is one: the
    smallest size that ran bounds the stack the chain needs on the compiler at hand.  A
    size below the need kills its child on a stack overflow, by design: with gcc, 256 and
    320 KiB do.  Each bracketing child is waited for :data:`BRACKET_TIMEOUT` seconds and
    the two asserted runs :data:`ASSERTED_TIMEOUT`, so that an overflow that hangs, rather
    than ends its child, costs minutes, not the job's hour, and a bracketing size that
    timed out is recorded as such.
    """
    build = sec_build(SEC)
    longest, labels = _longest_cover(tmp_path / "copy")
    rows = pd.read_csv(longest.parent / TABLE, index_col="point_id")
    folder = compiled_case(build, tmp_path / "extremes", model_points=rows, edits={
        **{file: (lambda name: lambda _: pd.read_csv(longest.parent / name))(file)
           for file in ("coi_rates.csv", "mort_table.csv")},
        LADDER: _committed_ladder().iloc[0:0]})
    model = mx.read_model(folder, name=_name("longest"))
    try:
        calls, want = {}, {}
        for key, label, frame in zip(point_keys(model), labels, LONGEST_FRAMES):
            proj = projection(model, key)
            assert (proj.duration_mth_init(), proj.t_entry(), proj.proj_len()) == frame
            last = proj.proj_len() - 1
            assert last - proj.t_entry() == 1451 and proj.age(last) == 120, label
            calls[key] = [("net_cf", (last,))]
            want[key] = proj.net_cf(last)
    finally:
        model.close()
    job = {"refs": {}, "calls": calls}

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

    ``IUL_US_S`` returns the no-lapse guarantee's expiry shock, ``nlg_shock_lapse``, a
    Reference nothing refuses, before its cap, and under :data:`LAPSE_PAST_1` the twin of
    S's point 1 paying $1,000 a year (:data:`SHOCKED`) has an annual rate of 1.2 in policy
    month 240, where ``1 - (1 - q)^(1/12)`` has no real value.  modelx computes it complex
    and the account value's and the margin's checks raise ``TypeError``
    (:func:`test_a_lapse_rate_past_1_makes_each_check_raise_as_in_iul_us_s`).  Compiled,
    the power is C's ``pow`` of a negative base, NaN, and NaN runs through every count and
    residual after it, so each of those checks' tolerance test is false: the compiled
    model reports a failed check rather than an error.  The components' check and the
    ladder's read no count and hold, as in modelx.  This pins that behaviour, which
    ``model-sec.md`` records among what the compiled model does differently: the rate
    itself is 1.2, its monthly rate NaN, the two checks ``False`` and the other two
    ``True``.
    """
    build = sec_build(SEC)
    s = _read(_s_inputs(tmp_path / "s", _s_table().loc[[1]].assign(**SHOCKED)),
              "lapse_past_1_s_cy", LAPSE_PAST_1)
    try:
        table, companions = build_sec_table(dataclasses.replace(SPEC, derived=(),
                                                                future=()), s)
    finally:
        s.close()
    folder = compiled_case(build, tmp_path / "lapse", model_points=table,
                           edits={LADDER: companions[LADDER]})
    model = _read(folder, "lapse_past_1_compiled", LAPSE_PAST_1)
    try:
        assert projection(model, 0).lapse_rate(240) == 1.2
        assert type(projection(model, 0).lapse_rate_mth(240)) is complex
    finally:
        model.close()
    checks = ("check_av_roll_fwd", "check_margin", "check_av_components",
              "check_seg_ladder")
    job = {"refs": LAPSE_PAST_1,
           "calls": {0: [("lapse_rate", (240,)), ("lapse_rate_mth", (240,)),
                         *((check, ()) for check in checks)]}}
    got = run_compiled(folder.parent, build.package.name, job)
    assert got["exit"] == 0, got["stderr"]
    assert all(got["compiled"].values()), got["compiled"]
    (rate, monthly, *verdicts) = got["values"][0]
    assert rate == ("ok", 1.2), rate
    assert monthly[0] == "ok" and math.isnan(monthly[1]), monthly
    assert verdicts == [("ok", False), ("ok", False), ("ok", True), ("ok", True)], verdicts


@pytest.mark.cython
def test_the_compiled_opening_account_value_is_summed_as_modelx_sums_it(sec_build,
                                                                        tmp_path):
    """Compiled, the opening of :data:`OPENING_PARTS` is modelx's, bit for bit.

    The compensated loop is C on doubles in the order written, with no reassociation and
    no fused multiply and add (``model-sec.md``, *Two compiler directives*); C4 compares it
    by value on committed rows, where a plain fold sums alike.  So on the inputs of
    :func:`test_the_opening_account_value_is_summed_compensated_from_its_parts`, which
    ``Data`` accepts, ``av_pp_at(t_entry(), BEF_PREM)`` compiled is ``1.0`` on the parts
    ``-1e16``, ``1.0`` and ``1e16``, and ``-0.0`` on three negative zeros, by
    ``float.hex``, the sign of the zero included.
    """
    build = sec_build(SEC)
    table, ladder = _opening_inputs()
    folder = compiled_case(build, tmp_path / "opening", model_points=table,
                           edits={LADDER: ladder})
    model = _read(folder, "opening_compiled")
    try:
        code = _code(model.Projection, "BEF_PREM")
    finally:
        model.close()
    job = {"refs": {}, "calls": {row: [("av_pp_at", (0, code))]
                                 for row in range(len(OPENING_PARTS))}}
    got = run_compiled(folder.parent, build.package.name, job)
    assert got["exit"] == 0, got["stderr"]
    assert all(got["compiled"].values()), got["compiled"]
    for row, (point, _, want) in enumerate(OPENING_PARTS):
        (opened,) = got["values"][row]
        assert opened[0] == "ok" and _opened_as_written(opened[1], want), (point, opened)


# A compiled model's Reference set after it has computed, in a child of its own: what the
# base Projection, an ItemSpace made before the change and one made after give for
# expenses(12), before inflation_rate is set to 2.5% and after.
STALE_CHILD = """\\
import json, sys
sys.path.insert(0, sys.argv[1])
model = __import__(sys.argv[2]).mx_model
p = model.Projection
early = p[5]
values = [p.expenses(12), early.expenses(12)]
p.inflation_rate = 0.025
values += [p.expenses(12), early.expenses(12), p[6].expenses(12)]
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
    which IUL ships at 0 and which, at 2.5%, moves ``expenses(12)`` on every point in
    force then: the base ``Projection``, the anchor's twin at ``idx`` 0, and S's point 1
    restated at its month 60, at ``idx`` 5, made before, and S's point 4 restated at 65,
    at ``idx`` 6, made after, so that a modelx-cython that began to clear caches would be
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
        before = (p.expenses(12), projection(model, 5).expenses(12))
        p.inflation_rate = 0.025
        fresh = (p.expenses(12), projection(model, 5).expenses(12),
                 projection(model, 6).expenses(12))
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
    modelx's: point 7's description, S's point 4 restated at its month 65 with twelve
    segments, and its first twelve rows of cash flows, of the account value, of the
    segment ladder and of counts, and the block's lines for each point, its first twelve
    rows and its first twelve projection years.

    The same output is what a runner that ignored ``--build`` and ran modelx would print,
    so the runner is also given a directory that holds no build, and must refuse it,
    saying so, rather than print anything.
    """
    build = sec_build(SEC)
    runner = model_path(SEC).parent / "run_sec.py"
    for args in (("7",), ("--block",)):
        expected = _run_sec(runner, *args)
        assert _run_sec(runner, *args, "--cython", "--build", str(build.out)) == expected
    empty = tmp_path / "no_build"
    empty.mkdir()
    done = _run_sec(runner, "7", "--build", str(empty), check=False)
    stderr = done.stderr.decode(errors="replace")
    assert done.returncode != 0 and done.stdout == b"", stderr
    assert f"holds no build of {SEC} for this interpreter" in stderr, stderr
