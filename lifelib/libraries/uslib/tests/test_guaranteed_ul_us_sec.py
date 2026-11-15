"""In-force tests for ULSG_US_SEC: the splice, future business, counts, regeneration.

``ULSG_US_SEC`` is ``ULSG_US_S`` taught to run in force at a valuation date
(USLIB-SEC-PLAN.md, milestone M5).  It runs on two clocks: ``t`` counts months from the
valuation date, the same month for every model point, and ``duration_mth(t)`` counts the
months the policy has been in force, ``duration_mth_init() + t``.  A model point may be a
policy already in force at the valuation date, in any month of its policy year, one issued
at it, or one to be issued after it, as in ``basiclife/BasicTerm_SE``.  A policy in force
opens with the state its past has left it, per policy: its account value, its shadow
account, its loan and the premiums it has paid to date, which are ``ULSG_US_S``'s own
columns, and one more, the months it has already spent in grace.

The worked example is not restated here.  ``ULSG_US_S`` counts its months from the start of
its own projection, and opens its point 1, the worked example's policy, in force 300
months, at its own ``t = 0``, so the twin of that point opens at offset 0 and is a splice
case (T2): it is S's point in every cell of S's, at no tolerance beyond the relative 1e-9,
which carries every golden of ``test_guaranteed_ul_us.py`` on it over, the worked
example's five months at ``t = 0..4`` and the return of premium at its 25th anniversary,
``t = 0``, among them.  S's points 2 to 4 are new business, issued at the valuation date,
where the two clocks coincide, and ``test_model_conventions.py`` asserts the model is S
there cell by cell (T1).  The conventions also hold the SEC family's other rules: every
frame opens at ``t = 0``, ``pols_if`` is the ``BEF_DECR`` count, ``BEF_DECR`` is
``BEF_NB`` plus the month's new business, new business enters once, and nothing happens
before issue.  This module holds the rest of the plan's tests (its §5.2) and the
product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's, the
  four reports among them, its account value, shadow account and loan at every timing,
  its grace counter and its lapse latch.  The months straddle the product's events: the
  first anniversaries, the surrender charge's last month, a grace that opens in the
  valuation month, a counter carried into it that lapses the policy a month on and one
  that the anniversary premium resets, the return-of-premium windows at the 20th and 25th
  anniversaries, at ``t = 0`` and at ``t = 1`` of a row valued mid-year, the account
  exhausted under the guarantee, the shadow account's net amount at risk floored, ten-pay
  premiums stopping, withdrawals outrunning an exhausted account, the corridor's first and
  last months, a COI scale read past its last age and the last covered month.  Twelve
  variants of S's points, in a copy of S's table and each with input rows of its own, add
  ten-pay premiums, every premium mode, withdrawals, a loan under a funded account and one
  on an exhausted account, a single premium that binds the corridor, a guarantee to 99
  with neither surrender charge nor endorsement and one to 100, either side of the
  lifetime guarantee's age the splice sets, each pin alone, an issue age below the
  mortality table's first age on a second schedule, and a premium that cures a grace and
  one too small for the first month's deductions, and between them every sex and every
  class; the twin of each variant issued at the valuation date is its S point in every
  cell, as a row issued there is.  A second fixture, on References of its own, binds
  the two bounds S ships idle: the lapse rate's cap and the credited rate's floor.
* T3, future new business: a point issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before issue and no rate or table read there.
* D11's R1, R1a and R2, and D3 and D5's chains: on the splice's grid no cell is called at a
  negative month, none evaluated on the books reads a month before them but the
  improvement factor, which runs from the valuation date for every row (D7), and none
  reads beyond ``t + 1``; on the committed points no recursion runs backward over the
  frame, the policy clock is a closed form, no label accessor is read and the
  funding-premium solve is not in the model; and every chain of the model runs one cell a
  month from a cold start, as far as the contract's longest cover.
* T4, the count algebra: the count rolls forward through new business and decrements, the
  lapse latch included, ``result_pols`` is S's report with the new business beside it, and
  a count 2.5 times the table's, with every assumption that ships at zero switched on,
  scales every counted cell and moves no per-policy value.
* T5, validation: each malformed in-force row is refused as the table is read, naming its
  point, by one rule; each assumption table is refused, naming its file and the column, if
  a key is blank, text or fractional, with the lines it is on, or if the keys repeat or
  leave a gap, with each key that repeats, its lines, and each that is missing; so is one
  whose rates, factors, charges or return-of-premium terms hold a value that is blank,
  text or infinite, or outside its range, while the bounds of each range are read; a text
  value no decode knows raises ``ULSG_US_S``'s message; the future horizon is a Reference
  that bounds future business, and at 0 refuses it; a point to be issued at or past the
  age at which charges cease, one at or past the end of the projection, and one whose
  grace has expired are refused by ``proj_len()``, each rule on its Reference, and read at
  it, just past it and with it moved, and one issued at the last age with cover is not;
  every state S reaches on the splice's inputs, restated in force, is
  accepted by ``Data`` and ``proj_len()``, but the one the product refuses by name, an
  account value below 0; each flag reads the same in every spelling ``Data`` accepts; and
  the edges of the interface are accepted, the tables' keys written as floats among them.
* T6, regeneration: the committed ``model_point_table_sec.csv`` is what the generator makes
  of ``ULSG_US_S`` and its table as they stand, the generator refuses a month after a
  lapse, and each derived and future row continues its S point from its month on.
* Then the two clocks on the shipped points, S's in-force point as its twin, the values
  outside cover, the survivors the end of the projection carries, the grace counter, the
  shadow account and the premiums paid opening from their own columns, mortality
  improvement, expense inflation and the declared rate on the valuation clock, each check
  failing on a residual that is not a number and deciding as S's where its sides are
  small, a lapse rate past 1, which makes the checks raise, the margin identity once a loan
  exceeds the cash value, acquisition on new business, the mortality cap and a NaN that
  reaches it or a bound written second, a corridor and a mortality table shorter than the
  cover, read at their ends, the pins and the premium, the docstrings, the shared input
  tables and every Reference held to S's, the one that ships equal to another and that
  the splice leaves so set apart, what the default grid reaches, the block, an in-force
  extract and the runner.
* Stage EC, what compiling changed, held in modelx: the claims total S's ``sum`` bit for
  bit, the codes and the status labels, the spec's sizes and the sample's limit to their
  comments, the padding and the readers' refusals, the COI scales numbered by key, what
  ``Data`` cannot number or join, a point issued below ``issue_age_min`` and the runner
  outside the repository.
* C2, the fingerprint: every committed point computes what the model computed when Phase 1
  ended, frozen at the end of this module before Phase 2 changed anything (§5.4).
* Compiled, after the fingerprint: the compiled model against modelx on the splice grid,
  at the contract's extremes, on labels that are not text, on keys written as floats and
  where the cap binds, its refusals, the deepest call on a 1 MiB stack, a lapse rate past
  1, a Reference set late and the runner, each marked ``cython``.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``, 0 for
the twins of S's points, in force or not, ``-k`` for one issued ``k`` months on.

**The core grid and the full one** (USLIB-SEC-PLAN.md K6).  A ULSG projection runs up to
985 months on the grid, and T2 and T3 over every case, 59 restated rows, three in-force
twins, ten variants issued at the valuation date and 15 future points, would take this
module far past three minutes in every run.  By default they run a core of 26 and 6
cases, chosen by the lines of the model each row runs, so that between them they reach
every line, every opening-state column, every kind of valuation month and every premium
pattern and mode the full grid reaches, which ``test_the_core_grid_reaches_every_branch``
asserts, each bound by the raw value it bounds and each side of every ``min`` and ``max``
by the values it compares.  The other cases, the rules test's scan of their rows, the
second fixture's other rows, the every-state test's months between the windows' edges
and the depth test's ascending sweeps at the contract's longest cover carry the
``sec_full`` marker and are skipped, with the reason shown, unless ``USLIB_SEC_FULL=1`` is
set.  They are never dropped: one leg of the CI matrix sets it, so every CI run runs the
full grid, and
``USLIB_SEC_FULL=1 python -m pytest -m sec_full tests/test_guaranteed_ul_us_sec.py`` runs
them alone.  Memory is the other cost: a projected point holds tens of megabytes of
cached values and their dependency graph, so a row read once, a splice case's or a point
of a temporary copy, is released as soon as it has been read (``_release``), and the
splice's rows are held one at a time, however large the grid.  Each splice's two models
are fixtures of the class that holds every test reading them, so they are closed before
the committed model and S are first read, and the module never holds both.  And the tests
that read models of their own run next, before the committed model and S are first read,
so that none of the models they read sits in memory beside those (USLIB-SEC-PLAN.md §7.7,
*Record — M9*, *Memory*).

Every test keeps five rules.  Each model is read under a name of its own and closed:
``test_guaranteed_ul_us.py`` reads S under its default name, and reading a model under a
name in use renames the open one.  Every Reference a test sets, ``Data``'s included, is set
on a model just read, before anything is computed: a compiled model never clears a cache.
No test writes inside the library tree: every changed input goes through
``sec_support.temp_inputs`` into a temporary directory, because a CSV added beside the
models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``us_registry.point_keys`` and the ItemSpaces from
``us_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor Phase 2's positions can
point a test at the wrong row.  The one exception is a table ``Data`` refuses, which has
no keys to give: it is read through the base ``Projection``'s default point.  And a timing,
a kind or a status label is passed through ``_code``, which gives the model's Reference of
that name where the model defines one and the string otherwise, a status read in a month
is compared through ``_status_is``, and every cell-by-cell comparison goes through
``_twin``: Phase 2 changes the call syntax only (C1), each in one place.
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

SEC, TWIN, TABLE = "ULSG_US_SEC", "ULSG_US_S", "model_point_table_sec.csv"
SPEC = SEC_SPECS[SEC]

# S's four points, all M60 StdNT with $500,000 of face, annual premiums on the GUL15
# schedule, withdrawing nothing: 1, the worked example's policy, in force 300 months, level
# at $10,800 a year with a guarantee to 121, the return-of-premium endorsement and both
# pins, its account value 2,400, its shadow account 118,000 and $270,000 paid to date; 2,
# the same, new business, without the pins; 3, a single premium of $152,300 for life; and
# 4, level at $6,000 a year with a guarantee to 90 and no endorsement.  S opens point 1 at
# its own t = 0, so its twin opens at offset 0.
NEW_BUSINESS = (2, 3, 4)
IN_FORCE = (1,)

# Twelve more S points, in the splice's copy of S's table and never in the committed one.
# Each changes S's columns, never a formula, to reach what S's four cannot, and between
# them they carry the sexes and classes S's four lack:
#
# 5, S's point 2 paying $26,000 a year for ten years, quarterly, M PPlusNT: its premiums
#   stop at policy year 11, t = 120 on new business, and its account runs out at 384, the
#   guarantee carrying it from there;
# 6, S's point 2 paying semi-annually and withdrawing $150 a month from policy year 2,
#   F PNT: its account is exhausted at 209 and its withdrawals then outrun it, the account
#   before the maintenance fee below 0 from 213; its grace opens at 447 and it lapses at
#   449;
# 7, S's point 1 in force at 300 with an account value of $400,000 under a loan of $50,000
#   and neither pin, M StdPlusNT: the loan chain and its credited interest, the corridor
#   binding from S's month 48 and the net amount at risk floored at 0 from 120, where the
#   corridor factor is 1 and the account value passes the face; S opens it at its own
#   t = 0, so its twin is a splice case too;
# 8, S's point 3 at a single premium of $700,000 withdrawing $2,000 a month, M PTob: the
#   corridor binds from its issue month to 131, the shadow account's net amount at risk is
#   floored from 18, the guarantee carries it from 314, and its COI scale stops at attained
#   age 110 (COI_LAST_AGE), so that ages 111 to 120, from S's month 612, read age 110's
#   rate;
# 9, S's point 2 paying monthly, with no surrender charge, no endorsement and a guarantee
#   to 99, M StdTob: a guarantee a year short of the lifetime guarantee's age the splice
#   sets, 100, which leaves the lapse multiplier at 1, and a grace that opens at 272 and
#   lapses the policy at 274;
# 10, S's point 2 with the premium persistency pin alone, 0.9;
# 11, S's point 2 with the COI precision pin alone, 2 places;
# 12, S's point 2 issued at age 40 on GUL10, a second schedule of $12.00 per $1,000 run off
#   over 10 years: the mortality table, which starts at 45, is read at 45 for its first five
#   years, its schedule reaches 0 at S month 119, and its corridor binds from 472;
# 13, S's point 4 paying $6,150 a year: its grace opens at 239 and the anniversary premium
#   at 240 cures it, a counter of 1 carried into 240 resetting there, as S's does; its grace
#   opens again at 242 and it lapses at 244;
# 14, S's point 2 paying $100 a year, too little for its first month's deductions, with
#   the shadow account short too: its grace opens in its issue month and it lapses two
#   months on, so that a row issued later reads its grace counter's base in its issue
#   month, which no other row in grace does;
# 15, S's point 1 in force at 300 with a loan of $10,000 on an account value of $2,400, and
#   neither pin: its account is exhausted at its month 3, and from month 4 the loaned
#   part's credit, below the declared rate's, takes the account value entering a month
#   below 0 in 65 of the 74 months to its lapse, all but a few after each anniversary's
#   premium; at months 76 and 77 the shadow account after its charges is above 0 but not
#   above the loan, so the loan decides the guarantee test, and the policy lapses at 78.  A
#   row restated at 3, the last month before its account value goes below 0, opens it
#   there (D6);
# 16, S's point 2 with a guarantee to 100, the lifetime guarantee's age the splice sets
#   (SPLICED_REFS), met exactly, the lapse multiplier at 0.55, where variant 9's 99, a year
#   short, leaves it at 1; it lapses at 504, its grace opening at 502, as S's point 2
#   does.  The guarantee's age is read by the lapse multiplier alone, so it moves no event
#   of either.
#
# Each variant is (the S point it changes, the columns it changes); the policy_id keeps the
# generated ids apart.  None stands for a blank cell.
VARIANTS = {
    5: (2, {"policy_id": "GUL-900005", "premium_type": "TEN_PAY", "premium_mode": "Q",
            "premium_pp_ann": 26000.0, "rate_class": "PPlusNT"}),
    6: (2, {"policy_id": "GUL-900006", "premium_mode": "S", "wd_pp": 150.0, "sex": "F",
            "rate_class": "PNT"}),
    7: (1, {"policy_id": "GUL-900007", "av_pp_init": 400000.0, "loan_bal_init": 50000.0,
            "rate_class": "StdPlusNT", "prem_persistency_override": None,
            "coi_rate_dp": None}),
    8: (3, {"policy_id": "GUL-900008", "premium_pp_ann": 700000.0, "wd_pp": 2000.0,
            "rate_class": "PTob"}),
    9: (2, {"policy_id": "GUL-900009", "premium_mode": "M", "has_surr_charge": False,
            "rop_elected": False, "guarantee_age": 99, "rate_class": "StdTob"}),
    10: (2, {"policy_id": "GUL-900010", "prem_persistency_override": 0.9}),
    11: (2, {"policy_id": "GUL-900011", "coi_rate_dp": 2}),
    12: (2, {"policy_id": "GUL-900012", "age_at_entry": 40, "surr_charge_id": "GUL10"}),
    13: (4, {"policy_id": "GUL-900013", "premium_pp_ann": 6150.0}),
    14: (2, {"policy_id": "GUL-900014", "premium_pp_ann": 100.0}),
    15: (1, {"policy_id": "GUL-900015", "loan_bal_init": 10000.0,
             "prem_persistency_override": None, "coi_rate_dp": None}),
    16: (2, {"policy_id": "GUL-900016", "guarantee_age": 100}),
}

# The variants' own input rows, in the copies only.  The shipped COI table covers the anchor
# cell, M StdNT, alone, from attained age 45, so each new key gets the anchor's rows at a
# scale of its own, and a COI read under the wrong key reads a different number; variant
# 8's scale stops at age 110, short of its cover, on a rate of $982.85 per $1,000, not 0, so
# that the clamp past the scale's last age is read with an effect.  Issue age 40 gets the
# anchor cell's rows from 40 to 44, geometric in the age, never flat, so that a rate read at
# the wrong age changes a number.  GUL10 is the second schedule.
COI_KEYS = ["sex", "rate_class", "age"]
COI_SCALES = {("M", "PPlusNT"): 0.70, ("F", "PNT"): 0.80, ("M", "StdPlusNT"): 0.90,
              ("M", "PTob"): 1.40, ("M", "StdTob"): 1.60}
COI_LAST_AGE = {("M", "PTob"): 110}
YOUNG_AGES = range(40, 45)


def _coi_rates_with_variants(rates):
    """S's COI table with rows for every key the variants use, sorted.

    Sorted by its three keys, as ``Data.coi_rates()`` indexes it, so that pandas can slice
    a cell's scale without a warning about the index's sort order.
    """
    anchor = rates[(rates["sex"] == "M") & (rates["rate_class"] == "StdNT")]
    blocks = [rates, pd.DataFrame({
        "sex": "M", "rate_class": "StdNT", "age": list(YOUNG_AGES),
        "coi_rate_guar_ann": [round(1.479757 * 0.9 ** (45 - a), 6) for a in YOUNG_AGES],
        "provenance": "test copy"})]
    for (sex, rate_class), scale in COI_SCALES.items():
        last = COI_LAST_AGE.get((sex, rate_class), anchor["age"].max())
        blocks.append(anchor[anchor["age"] <= last].assign(
            sex=sex, rate_class=rate_class,
            coi_rate_guar_ann=(anchor["coi_rate_guar_ann"] * scale).round(6),
            provenance="test copy"))
    return pd.concat(blocks, ignore_index=True).sort_values(COI_KEYS, ignore_index=True)


def _surr_charges_with_gul10(table):
    """S's surrender charge schedule with GUL10: $12.00 per $1,000 over 10 years."""
    gul10 = pd.DataFrame([{"surr_charge_id": "GUL10", "sc_per_1000_init": 12.0,
                           "runoff_years": 10, "provenance": "test copy"}])
    return pd.concat([table, gul10], ignore_index=True)


# The input files the splice's copies change, S's and SEC's alike.
SPLICED_EDITS = {"coi_rates.csv": _coi_rates_with_variants,
                 "surr_charge_table.csv": _surr_charges_with_gul10}

# T2's months (USLIB-SEC-PLAN.md §7.5), by event rather than month by month, so that the
# grid is sized for what T2 and Phase 2's C4 both need.  All are S's months, under the
# splice's References.  On S's point 1, in force at 300: 1; 12, the first valuation
# anniversary; 79, the month before its grace; 80, where its grace opens, in the valuation
# month; and 81, a month into it, the counter of 1 carried in, which lapses the policy at
# t = 1, S's month 82.  No row is restated at or after a lapse: there S's count is 0 and
# its latch shut, and the in-force interface carries no latch, so the generator refuses
# those months (test_the_generator_refuses_a_month_after_the_lapse), and S's 82 and 83 are
# compared as t = 1 and 2 of the row at 81.  On S's point 2, new business: 1, the first
# month after issue; 11, 12 and 13 around the first anniversary; 179, where the surrender
# charge reaches 0; 239, 240 and 241 around the 20th anniversary's 50% window; 244, where
# its account runs out and the guarantee carries it; 299, 300 and 301 around the 25th
# anniversary's 100% window, its refund capped at 40% of the face; 305, mid-year after it,
# where the policy's anniversaries, at t = 7 and 19, and the valuation date's part; 502 and
# 503, its grace.  On S's point 3, the lifetime single premium: 240 and 300, the windows on
# a funded account; 588, from which its shadow account's net amount at risk is floored;
# 731, its last covered month, a frame of one row whose t = 1 is the month carried into.
# On S's point 4, to age 90 with no endorsement: 81, where its account runs out; 233, 234
# and 235 around its grace, which opens at 234.  239 and 299 put a window at t = 1 of a row
# valued mid-year, where a window tested on t rather than the policy month falls at t = 12.
# On the variants:
#   5, ten-pay: 12; 119, 120 and 121 either side of the month its premiums stop;
#   6, withdrawals: 12, 13; 213, the first month they outrun the account; 447 and 448, its
#     grace;
#   7, the loan: 6 and 12, besides its twin;
#   8, the single premium on the corridor: 12; 131, the corridor's last month; 612, the
#     first month read past its COI scale's last age; 731;
#   9, monthly, to 99: 1, 12; 272, 273, its grace;
#   10 and 11, each pin alone: 12 and a window month;
#   12, issue age 40 on GUL10: 12; 119, the schedule's last month; 472, the corridor's
#     first;
#   13, the cure: 239, its grace opening; 240, the counter carried in and reset; 241; 243,
#     the counter carried into the lapse at t = 1;
#   15, the loan on an exhausted account: 3, its last month at 0 or more, besides its twin.
# T3's: S's point 2 issued one month on, which puts the policy anniversaries a month off the
# valuation years, twelve, which puts them back on, thirteen and twenty-five, the committed
# row's; and each new-business variant issued thirteen months on, more than a year, so that
# its months before issue read policy years -1 and 0, where a cell read without its guard
# would show: issued within a year, a point reads policy year 0 alone before issue
# (USLIB-SEC-PLAN.md D4).  Variants 7 and 15 are in force in S and cannot be issued later;
# variant 14 is there only to be issued later, in its grace from its issue month.  Its
# first month's counter reads its base there, where a base at t == 0 would read the month
# before issue, which no number shows and the rules test refuses.
PT_MTHS = {1: (1, 12, 79, 80, 81),
           2: (1, 11, 12, 13, 179, 239, 240, 241, 244, 299, 300, 301, 305, 502, 503),
           3: (240, 300, 588, 731),
           4: (81, 233, 234, 235)}
VARIANT_MTHS = {5: (12, 119, 120, 121), 6: (12, 13, 213, 447, 448), 7: (6, 12),
                8: (12, 131, 612, 731), 9: (1, 12, 272, 273), 10: (12, 240), 11: (12, 300),
                12: (12, 119, 472), 13: (239, 240, 241, 243), 15: (3,)}
SPLICES = tuple(("derived", p, d)
                for p, mths in (*PT_MTHS.items(), *VARIANT_MTHS.items()) for d in mths)
IN_FORCE_TWINS = (("twin", 1, 0), ("twin", 7, 0), ("twin", 15, 0))
# The twins of the variants issued at the valuation date, each compared with its S point
# cell by cell, as a row issued there is (USLIB-SEC-PLAN.md §7.7, Record — M9, Variants'
# twins): an issue rule that only a variant takes at t = 0 is reached nowhere else.  The
# variants of S's point 1, in force 300 months, take no issue rule there, and are splice
# cases at offset 0 instead (IN_FORCE_TWINS).
VARIANT_TWINS = tuple(("twin", p, 0) for p, (base, _) in VARIANTS.items()
                      if base in NEW_BUSINESS)
FUTURES = ((2, 1), (2, 12), (2, 13), (2, 25), (3, 13), (4, 13), (5, 13), (6, 13), (8, 13),
           (9, 13), (10, 13), (11, 13), (12, 13), (13, 13), (14, 13))

# The default run's cases (the module docstring), each with what it is there for.  The
# rest of SPLICES, IN_FORCE_TWINS, VARIANT_TWINS and FUTURES run with USLIB_SEC_FULL=1.
# Each event has a core row in its own month, each kind of valuation month among them, as
# the core-reach test asserts, by AT_VALUATION and, for the last covered month, by a
# predicate of its own: the grace's opening, the counter carried into the lapse and the
# one reset, the surrender charge's last month, a window at t = 0 and at t = 1, ten-pay's
# first unpaid anniversary and the last covered month.  The variants' twins in the core
# are those whose issue month no core row issued later takes, 6, 9, 10, 12, 13 and 16,
# those of 9 and 16 meeting the lifetime guarantee's age on both sides; the issue months
# of 5, 8, 11 and 14 are taken by core rows issued 13 months on.
CORE_SPLICES = {
    ("twin", 1, 0): "S's in-force point 1 at offset 0: the worked example's months, both "
                    "pins, the 25th window at t = 0 with its refund capped",
    ("twin", 7, 0): "in force with a loan under a funded account: the loan chain, the "
                    "corridor and the net amount at risk floored",
    ("twin", 15, 0): "in force with a loan on an exhausted account: the account entering "
                     "months below 0, and the loan deciding the guarantee test",
    ("derived", 1, 80): "the grace opening in the valuation month",
    ("derived", 1, 81): "a counter of 1 carried into the grace: the lapse at t = 1",
    ("derived", 2, 1): "the first month after issue",
    ("derived", 2, 12): "a premium anniversary at t = 0; the block test's row",
    ("derived", 2, 179): "the surrender charge reaching 0 at t = 0",
    ("derived", 2, 240): "the 20th anniversary's 50% window at t = 0",
    ("derived", 2, 299): "a window at t = 1 of a row valued mid-year",
    ("derived", 2, 305): "mid-year, exhausted, the guarantee carrying the policy",
    ("derived", 3, 588): "the shadow account's net amount at risk floored from t = 0",
    ("derived", 3, 731): "the last covered month: t = 1 is the month carried into",
    ("derived", 4, 234): "a guarantee to 90 failing at t = 0, with no endorsement",
    ("derived", 5, 120): "ten-pay's premiums stopping at t = 0, quarterly",
    ("derived", 6, 213): "withdrawals outrunning an exhausted account, semi-annual, F",
    ("derived", 8, 12): "the corridor binding from t = 0, PTob, its COI scale read past "
                        "its last age",
    ("derived", 10, 12): "the persistency pin alone",
    ("derived", 11, 12): "the precision pin alone",
    ("derived", 13, 240): "a counter of 1 carried in and reset by the anniversary premium",
    ("twin", 6, 0): "issued at the valuation date: semi-annual, withdrawals from year 2",
    ("twin", 9, 0): "issued at the valuation date: monthly, a guarantee to 99, a year "
                    "short of the lifetime guarantee's age",
    ("twin", 10, 0): "issued at the valuation date: the persistency pin alone",
    ("twin", 12, 0): "issued at the valuation date at age 40, on GUL10",
    ("twin", 13, 0): "issued at the valuation date: S point 4 paying $6,150 a year",
    ("twin", 16, 0): "issued at the valuation date: a guarantee to the lifetime "
                     "guarantee's age, 100",
}
CORE_FUTURES = {
    (2, 1): "issued a month off the valuation anniversaries; the block test's row",
    (2, 25): "policy years -2 to 0 before issue: the committed row's",
    (5, 13): "ten-pay, quarterly, in its issue month",
    (8, 13): "the single premium in its issue month, the corridor binding",
    (11, 13): "the precision pin alone, issued later",
    (14, 13): "a grace opening in the issue month: the counter's base read there",
}

SEC_FULL = os.environ.get("USLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "USLIB_SEC_FULL=1 (USLIB-SEC-PLAN.md K6)"))

# What the splice sets in both models, S and SEC alike, before either evaluates anything:
#   inflation_rate at 0 and mort_improve_rate_init at 0: the two valuation-clock inputs
#     (D7), which run from the valuation date on this model and from S's own start on S, so
#     that a row restated at d and its S point part by design where either is on
#     (USLIB-SEC-PLAN.md §5.2, T2); each is held on the valuation clock at its shipped value
#     by a test of its own;
#   mort_ae_factor at 0.56: with improvement off, the table's rate of 1.0 at attained age
#     120 would end every life in the last month, and at 0.56 survivors reach the end of
#     the frame on every point that does not lapse, so that the survivors carried into
#     t = proj_len(), which S's roll-forwards read there, are compared; it keeps every
#     class below 1 too, StdTob's oldest rate at 1.75 x 0.56 = 0.98, where its own test
#     takes the product past 1 (the mortality cap);
#   premium_tax_rate at 2%: the one assumption ULSG ships at zero, a percent-of-premium
#     expense, so that premium_taxes shows.  rider_charge_pp is S's placeholder and reads no
#     input, and a loan and withdrawals ship at zero as columns, which the variants switch
#     on;
#   lifetime_guarantee_age at 100 and lapse_pattern_mult_single at 0.65: each ships equal
#     to a Reference a rewritten cell reads, 121 to charges_cease_age, which proj_len() and
#     every guard against charges ceasing read, and 0.6 to lapse_dyn_mult_guar_only, which
#     the dynamic lapse multiplier reads, so that a rewritten cell reading the one for the
#     other would change no number (USLIB-SEC-PLAN.md §7.8, Record — M10, Set-apart
#     References).  Set apart, each reads as before on S's points and every variant but
#     16: the guarantees they elect, 121, 99 and 90, fall on the same sides of 100 as of
#     121; and variants 9 and 16, to 99 and 100, meet the boundary exactly on both sides
#     (USLIB-SEC-PLAN.md §7.7, Record — M9, Contract boundaries).
# charges_cease_age stays 121: ULSG_US_S's frame ends where its charges cease, so no value
# of it puts the cessation in cover, in either model, and the six branches that read it
# stay unreached in both (USLIB-SEC-PLAN.md §7.5).  The identity does not depend on the
# values, only on both models having the same.
SPLICED_REFS = {"inflation_rate": 0.0, "mort_improve_rate_init": 0.0,
                "mort_ae_factor": 0.56, "premium_tax_rate": 0.02,
                "lifetime_guarantee_age": 100, "lapse_pattern_mult_single": 0.65}

# The cells T2 and T3 skip beyond T1's: result_pols as a whole and the four cells of S's
# funding-premium solve, which this model leaves to S (the spec's exempt).  The twins of
# S's in-force points take no more: S opens them at its own t = 0, from the columns their
# twins carry, so S's opening accessors are theirs, and S's frame is theirs.  On a restated
# row, S's own accessors of the point it opens differ by design: proj_len counts from the
# valuation date on SEC and from S's own start on S, so it differs by d, or by -k, and
# frame_mismatches asserts what it must get right, that both frames end at the same
# instant; duration_mth_init is d, or -k, on SEC and S's own on S; and av_pp_init,
# sg_pp_init, loan_bal_init and cum_prem_init hold S's month-0 values on S and month d's on
# SEC.  Every cell that reads them is compared.  grace_mth_init is this model's alone.
TWIN_EXEMPT = TWIN_EXEMPT_DEFAULT | SPEC.exempt
SPLICE_EXEMPT = TWIN_EXEMPT | {"proj_len", "duration_mth_init", "av_pp_init", "sg_pp_init",
                               "loan_bal_init", "cum_prem_init"}
FUTURE_EXEMPT = TWIN_EXEMPT | {"proj_len", "duration_mth_init"}


def _issued_later(name, args):
    """The ``arg_map`` of a point issued at or after the valuation date, compared with S.

    S's keys as they are, but ``pols_if_at(0, "BEF_NB")``, S's issue month, which it
    leaves out (``None``): there S's cell counts the issued policies, as it does under
    every timing, and this model counts them as the month's new business, not yet in.
    """
    return None if name == "pols_if_at" and args == (0, "BEF_NB") else args


# The decrement rates keyed by month, none of which may be evaluated before issue (R1,
# D4); and the readers keyed by a policy year, by an attained age reached in cover and by a
# completed policy year at an anniversary, the return of premium's.
DECREMENT_RATES = ("mort_rate", "mort_rate_mth", "lapse_rate_base", "lapse_rate",
                   "lapse_rate_mth")
KEYED_BY_YEAR = ("lapse_rate_base_py",)
KEYED_BY_AGE = ("mort_rate_base_at", "corridor_factor_at", "coi_rate_guar_at")
KEYED_BY_ANNIV = ("is_rop_anniv", "rop_ratio_anniv", "rop_rate_anniv")

# The cells that scale with policy_count.  Every other cell is a per-policy amount, a
# rate, a clock or a flag, and must not move when the count does.  The three residuals are
# relative, so a scaled count moves them in the last digits.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz", "pols_death",
    "pols_lapse", "pols_rop", "pols_lapse_grace", "pols_maturity", "premiums",
    "prem_to_av", "maint_fee", "coi", "mth_deduction", "mth_deduction_forgone",
    "inv_income", "av_at", "av_change", "surr_charge", "claims_from_av", "claims_over_av",
    "claims", "claims_death", "claims_lapse", "claims_refund", "withdrawals", "wd_fees",
    "expenses", "premium_taxes", "margin_expense",
    "margin_mortality", "margin_rop", "net_cf"})
RELATIVE = ("check_av_roll_fwd_resid", "check_sg_roll_fwd_resid", "check_margin_resid")
CHECKS = ("check_av_roll_fwd", "check_sg_roll_fwd", "check_margin")

# result_pols' columns, in its order: the count, the new business within it, the month's
# deaths, lapses, refunds and lapses at the end of a grace in processing order, the
# maturities, always zero, then S's two monthly decrement rates, which no count moves.
RESULT_POLS = ["pols_if", "pols_new_biz", "pols_death", "pols_lapse", "pols_rop",
               "pols_lapse_grace", "pols_maturity", "mort_rate_mth", "lapse_rate_mth"]
OUTFLOWS = RESULT_POLS[2:7]
RATES = RESULT_POLS[7:]
REPORTS = ("result_cf", "result_pols", "result_av", "result_guar")
# The report columns that are not amounts: the status label, the guarantee's flag and the
# grace counter.  Every other column of every report is a float.
LABEL_COLUMNS = {"result_av": ("status",), "result_guar": ("is_guar_active", "grace_mth")}

# The timings and kinds the model knows: the count's three, which S's stub names and
# answers with pols_if for each; the five intra-month points of the account value and the
# shadow account, and av_at's EOM; the loan's one; and the claim kinds, with claim_pp's
# WITHDRAWAL, and claims_from_av's WITHDRAWAL and MATURITY.  No call here takes claims'
# kind=None default, which Phase 2 replaces with an explicit total cell (USLIB-SEC-PLAN.md
# D11, R12).
TIMINGS = ("BEF_MAT", "BEF_NB", "BEF_DECR")
AV_TIMINGS = ("BEF_PREM", "BEF_WD", "BEF_FEE", "BEF_COI", "BEF_INV")
LOAN_TIMINGS = ("BEF_INT",)
KINDS = ("DEATH", "LAPSE", "REFUND", "GRACE")
CLAIM_KINDS = ("DEATH", "LAPSE", "REFUND", "WITHDRAWAL", "GRACE")
AV_KINDS = ("DEATH", "LAPSE", "REFUND", "GRACE", "WITHDRAWAL", "MATURITY")

# The opening state, in Data's order: ULSG_US_S's four columns and the grace counter.  The
# two pins, which hold in every month.  S's label accessors, which no projection cell may
# read.  And the four cells of S's funding-premium solve, which this model leaves to S.
STATE = ("av_pp_init", "sg_pp_init", "loan_bal_init", "cum_prem_init", "grace_mth_init")
PINS = ("prem_persistency_override", "coi_rate_dp")
LABELS = ("sex", "rate_class", "premium_type", "premium_mode", "surr_charge_id")
SOLVER = ("solve_len", "sg_pp_solve", "guar_min_sg", "no_lapse_premium")

# The cells running in force adds to ULSG_US_S's, each of which the symbol map must name.
NEW_CELLS = ("policy_count", "grace_mth_init", "t_entry", "charges_cease_mth", "is_active",
             "pols_new_biz", "is_level_premium", "is_single_premium", "is_ten_pay_premium",
             "wd_pp_mth", "prem_persistency_override", "has_prem_persistency_override",
             "corridor_factor_at", "mort_rate_base_at", "coi_rate_last_age",
             "coi_rate_guar_at", "lapse_rate_base_py", "surr_charge_rate_max",
             "surr_charge_runoff_years", "is_rop_anniv", "rop_ratio_anniv",
             "rop_rate_anniv", *RELATIVE,
             # Phase 2's (USLIB-SEC-PLAN.md D11): the label, the COI scale's number and its
             # first age, and the claims split by kind (R12)
             "point_id", "coi_schedule", "coi_rate_first_age", "claims_death",
             "claims_lapse", "claims_refund")

INFLATION = 0.025       # ULSG ships 2.5% a year; the splice sets 0
IMPROVEMENT = 0.01      # ULSG ships 1% a year; the splice sets 0
COUNT_FACTOR = 2.5      # T4's factor, not a whole number (USLIB-SEC-PLAN.md §5.2)

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A report evaluates each column in ascending t, so a forward
# recursion, through t - 1, finds the month before already cached, and the committed points'
# sweep runs under a limit of 17, where ULSG_US_S's runs under 14: the two differ by this
# model's guards, and at stage EC by Data's vectors (measured at M18; 16 at E).  A row
# issued at the horizon, 120 months on, needs 19, since its first month's mortality reads
# the improvement factor of the ten valuation years before its issue cold.  A backward
# recursion over the frame, through t + 1, opens a chain as long as the frame, and the
# shortest committed frame of more than a month is 351 months, so a limit of 40 lets every
# forward sweep through and stops every backward one.
CALL_DEPTH = 40

# How deep a cold call may run beyond its chain, one cell a month from its month back to the
# chain's base (D5): the cells above the chain and those below it, the first month's charges
# and Data's first reads of its tables.  A cold net_cf in the last month runs 15 to 18 cells
# beyond one cell a month back to t_entry() on the committed points, 18 at the contract's
# longest cover, issue age 18, and 21 issued 120 months on, where the first month's
# mortality reads the improvement factor of the ten valuation years before issue.  Each
# chain's head called alone, on a read of its own, runs at most 12 beyond on the committed
# points, the count's, 14 at the longest cover and 17 issued 120 months on: the loan 3, the
# premiums paid 5, the account value 8, the shadow account 10, the latch 10 to 11 and the
# count 12 to 17 (measured at stage EC, M18; a level more than at E in places, Data's
# vectors read below a table's reader, as Phase 1 left room for).  Any chain of two cells a
# month runs a frame's length beyond.  The improvement factor is a chain of one cell a year,
# at most mort_improve_max_years + 2 cells, 22, from t = 252 on, 27 levels called cold, and
# takes a bound of its own (IMPROVEMENT_OVERHEAD).
CHAIN_OVERHEAD = 25
IMPROVEMENT_OVERHEAD = 9


# ---------------------------------------------------------------------------
# Helpers

_names = itertools.count(1)


def _name(tag):
    """A model name that no other read in this session uses."""
    return f"{SEC}_{tag}_{next(_names)}"


def _code(proj, label):
    """The argument that selects timing, kind or status ``label`` on ``proj``, a Space.

    The model's int Reference of that name where it defines one, as Phase 2 does (R9:
    ``pols_if_at(t, BEF_DECR)`` with ``BEF_DECR = 1``), else the string itself, as at stage
    ``"E"``.  The conventions' ``_timing`` does the same, so every call in this module reads
    the same at both stages.  Two of S's status labels are not names, ``"IN FORCE"`` and
    ``"IN FORCE - GUARANTEE"``, and their codes join the words with underscores, the
    hyphen dropped, ``IN_FORCE`` and ``IN_FORCE_GUARANTEE`` (R10), so a label is looked up
    so joined.
    """
    value = proj.refs.get(label.replace(" - ", "_").replace(" ", "_"))
    return value if isinstance(value, int) and not isinstance(value, bool) else label


def _status_is(x, t, *labels):
    """Whether ``x.status(t)`` is one of ``labels``, each compared as its code.

    Phase 2 makes the status a code (USLIB-SEC-PLAN.md §7.5, C), so every status this
    module reads in a month is compared here, through :func:`_code`, as FIA's module
    compares its phases.
    """
    return x.status(t) in [_code(x, label) for label in labels]


def _twin(s_proj, sec_proj, *, arg_map=None, **kwargs):
    """``sec_support.twin_mismatches``, which every comparison in this module calls here.

    It passes the SEC Space's ``sec_support.codes``, which map S's timing and kind strings
    to the int codes Phase 2 gives them, and the spec's ``twin_arg_map``, which maps S's
    ``claims(t, None)``, the total, onto Phase 2's ``claims(t)`` and skips S's
    ``claims(t, kind)``, whose values are Phase 2's ``claims_death``, ``claims_lapse`` and
    ``claims_refund`` (R12).  The spec's map runs first, then the caller's ``arg_map``, on
    S's arguments.  At stage ``"E"`` there were no codes; every comparison goes through
    here, so each took Phase 2's codes and split when they came.
    """
    first = SPEC.twin_arg_map

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

    A projected ULSG point holds tens of megabytes of cached values and their dependency
    graph.  The splice's rows and the scaled and extract copies' points are each needed
    once, so each is released when read, as ``run_sec.py --block`` releases its points
    (USLIB-SEC-PLAN.md F5), and collected at once.  That costs little, because the swept
    models the module holds are frozen out of the collector (:func:`_freeze`), so the
    collection scans only what the row made.  Asked for again, the ItemSpace is made afresh
    and recomputes.  Without ``collect`` the collector is left to run when it will, as the
    every-state test leaves it for rows that computed nothing but their frame.
    """
    del model.Projection[key]
    if collect:
        gc.collect()


def _freeze():
    """Collect what is garbage, then freeze everything still alive out of the collector.

    Each fixture that sweeps a model calls this once its sweep is done, so that the
    collections after it, automatic or :func:`_release`'s, no longer scan the millions of
    objects a swept model holds.  The collection first means no garbage is frozen with
    them.  The splices' fixtures undo their freezes as they close their models, and
    :func:`_collector` the rest as the module ends.
    """
    gc.collect()
    gc.freeze()


def _committed():
    """The committed SEC table as the file holds it, unvalidated, indexed by point_id."""
    return pd.read_csv(model_path(SEC).parent / TABLE, index_col="point_id")


def _s_table():
    """S's committed table as the file holds it, indexed by point_id."""
    return pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                       index_col="point_id")


def _sec_inputs(tmp_path, table, edits=None):
    """A copy of the product directory whose SEC table is ``table``; its SEC folder."""
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=edits)


def _s_inputs(tmp_path, table, edits=None):
    """A copy of the product directory whose S table is ``table``; its S folder."""
    return temp_inputs(tmp_path, model_path(TWIN), model_points=table, edits=edits)


def _read(folder, tag, refs=None, data=None):
    """The model in ``folder``, read under a name of its own, with References set first.

    ``refs`` are ``Projection`` References and ``data`` ``Data`` References, set on the
    model just read, before anything is computed: a compiled model clears no cache.
    """
    model = mx.read_model(folder, name=_name(tag))
    for ref, value in (refs or {}).items():
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


# The S cell no report or check of ULSG_US_S evaluates (USLIB-SEC-PLAN.md §7.5, C), which
# the comparisons compare only because _sweep_s evaluates it first: the premium that would
# cure a month's forgone deductions.
NEVER_REACHED = ("cure_premium_pp",)


def _sweep_s(proj):
    """Evaluate on an S point what the comparisons compare: the sweep, and more.

    :func:`sec_support.sweep` reaches none of :data:`NEVER_REACHED`, ``pols_if_at`` on
    ``ULSG_US_S``, the claim and account-value claim kinds no report reads, the withdrawal
    and the grace's at ``claim_pp``, the withdrawal and maturity at ``claims_from_av``, or
    the account value in force at its timings past the opening one, because no result
    column or check reads them, and a cell S never evaluates is compared nowhere.  So they
    are evaluated here, over the frame, each at every timing or kind it takes, so that the
    comparisons see them too.
    """
    sweep(proj)
    for t in range(proj.proj_len()):
        for timing in TIMINGS:
            proj.pols_if_at(t, _code(proj, timing))
        for name in NEVER_REACHED:
            proj.cells[name](t)
        for kind in CLAIM_KINDS:
            proj.claim_pp(t, _code(proj, kind))
        for kind in AV_KINDS:
            proj.claims_from_av(t, _code(proj, kind))
        for kind in KINDS:
            proj.claims(t, _code(proj, kind))
        for timing in (*AV_TIMINGS, "EOM"):
            proj.av_at(t, _code(proj, timing))


def _continues_s(s_proj, sec_proj, month, exempt=TWIN_EXEMPT, arg_map=None):
    """Where a row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison, on models at the same assumptions: frame by frame, the four
    reports, then cell by cell over every cell of S's but ``exempt``, every one to 1e-9
    relative with no absolute floor, through ``arg_map`` where it is given
    (:func:`_issued_later`, for a point issued at or after the valuation date).
    """
    found = []
    for report in REPORTS:
        found += [f"{report}: {line}" for line in frame_mismatches(
            s_proj.cells[report](), sec_proj.cells[report](), t_offset=month, atol=0.0)]
    return found + _twin(s_proj, sec_proj, t_offset=month, exempt=exempt, arg_map=arg_map,
                         atol=0.0)


def _case_id(kind, s_point, month):
    """A case's id: ``point2-d12``, ``point1-twin0``, or ``point2-k13`` if issued later."""
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
GRID = (*SPLICES, *IN_FORCE_TWINS, *VARIANT_TWINS,
        *(("future", p, -k) for p, k in FUTURES))
CORE_GRID = frozenset({*CORE_SPLICES, *(("future", p, -k) for p, k in CORE_FUTURES)})


def _s_table_with_variants(variants=VARIANTS):
    """S's committed table with ``variants`` appended, under their own point_ids.

    A ``None`` in a variant's columns writes a blank, as a pin left unset is.
    """
    table = _s_table()
    rows = []
    for point_id, (base, changes) in variants.items():
        row = table.loc[[base]].astype(object)
        for column, value in changes.items():
            row[column] = float("nan") if value is None else value
        row.index = pd.Index([point_id], name="point_id")
        rows.append(row)
    return pd.concat([table, *rows])


def _spliced_folder(root, s, derived, future, edits=SPLICED_EDITS):
    """The SEC folder for ``derived`` and ``future`` rows of ``s``, a model on S's copy.

    The generator builds the rows from the registered spec, out of ``s`` as it stands, so
    each opens with the state of the very run it is compared with, and the folder holds
    ``edits``.  ULSG reads no scenario, so no row needs a re-based input of its own.
    """
    spec = dataclasses.replace(SPEC, derived=tuple(derived), future=tuple(future))
    table, companions = build_sec_table(spec, s)
    assert companions == {}
    return temp_inputs(root, model_path(SEC), model_points=table,
                       model_point_file=spec.model_point_file, edits=edits)


def _splice(root, tag, refs, variants, splices, futures, core):
    """S and SEC on the splice's inputs with ``refs`` set in both, S swept: (s, sec).

    S is read from a copy of the product directory whose table has ``variants`` appended
    and whose COI and surrender charge tables are the splice's (:data:`SPLICED_EDITS`).
    SEC runs on the same tables, and on a model point table of its own, built by the
    generator from the registered spec with its rows replaced by the cases this run
    selects of ``splices`` and ``futures``, the ``core`` or the full grid
    (:func:`_selected`), out of this S model, so each row opens with the state of the very
    run it is compared with.  Every S point is then swept (:func:`_sweep_s`).
    """
    s_folder = temp_inputs(root / "s", model_path(TWIN),
                           model_points=_s_table_with_variants(variants),
                           edits=SPLICED_EDITS)
    s = _read(s_folder, f"s_{tag}", refs)
    try:
        derived = [(p, d) for kind, p, d in _selected(splices, core) if kind == "derived"]
        future = [(p, k) for p, k in futures if SEC_FULL or ("future", p, -k) in core]
        sec = _read(_spliced_folder(root / "sec", s, derived, future), f"sec_{tag}", refs)
    except BaseException:
        s.close()
        raise
    for key in point_keys(s):
        _sweep_s(projection(s, key))
    return s, sec


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
    """ULSG_US_SEC read in place, as committed, and swept once, cold; what it met.

    The model is first asked for ``duration_mth(400)`` on the twin of S point 1, and the
    keys that call leaves in ``duration_mth`` are kept.  Then every committed point is
    swept (:func:`sec_support.sweep`: ``result_cf``, the other reports and the checks), in
    table order and each column in ascending ``t``, under a recursion limit lowered to
    :data:`CALL_DEPTH`, and whatever that raises is kept, point by point, rather than
    raised.  Last, the keys ``ULSG_US_S``'s label accessors hold on each point, which no
    projection cell may read, are counted.  So the record says what a cold model does,
    which the clock test asserts (D3, R2), and every test on the committed model reads a
    model already swept: the sweep is paid once, not once for each.  The swept model is
    then frozen out of the collector (:func:`_freeze`).  Returns ``(model, record)``.
    """
    model = mx.read_model(model_path(SEC), name=_name("sec"))
    first = _row(model, "twin", 1, 0)
    record = {"duration_mth(400)": first.duration_mth(400),
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
    """ULSG_US_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """ULSG_US_S read in place, as committed, with every point swept (:func:`_sweep_s`).

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

    The main splice's grid, :data:`VARIANTS` and the rows the run selects of
    :data:`SPLICES`, :data:`IN_FORCE_TWINS` and :data:`FUTURES` (:func:`_splice`).  Each
    SEC row is projected by the case that compares it and released once compared
    (:func:`_settle`).

    Scoped to the class that holds every test of the splice, so that its two models are
    closed before the committed model and S are first read: the module never holds both,
    which keeps its peak at the larger of the two.  Once S is swept the heap is frozen, so
    that the collections the released rows trigger scan the rows alone; at teardown the
    models are closed, then the freeze is undone and the collector run.
    """
    s, sec = _splice(tmp_path_factory.mktemp("spliced"), "spliced", SPLICED_REFS,
                     VARIANTS, SPLICES + IN_FORCE_TWINS, FUTURES, CORE_GRID)
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
# cell without a t reads none keyed by t, which the rules test asserts, since it is what
# lets the scan judge a read through a cell keyed by an attained age, a policy year or an
# anniversary by the month that asked.
LOOPS = frozenset({*REPORTS, *CHECKS})

# The one look-back R1 admits, by reader and cell: mortality improvement runs from the
# valuation date for every row (D7, USLIB-SEC-PLAN.md §7.5), so on a row issued k months
# after it the improvement factor of a month on the books is the product of the valuation
# years before it, issue included, and reads the factor and the graded rate a year back, at
# months before t_entry().  It reads no balance of the books, only the clock and
# References.  Each such read is at t - 12, or at month 12 x mort_improve_max_years, where
# the factor stops growing.
EARLY_ADMITTED = frozenset({("mort_improve_factor", "mort_improve_factor"),
                            ("mort_improve_factor", "mort_improve_rate")})


def _sweep_on_the_books(proj):
    """Evaluate every monthly cell of ``proj`` at every month on the books.

    Each cell whose first parameter is ``t``, at each month from ``t_entry()`` to
    ``proj_len() - 1``, and at each timing or kind the guard test's sets give it, as Phase
    2's full sweep does; the months outside cover are the guard test's
    (:func:`_outside_cover_faults`).  The loops over the frame leave cells unread on the
    books, the cure premium and the account value in force at its later timings among
    them, and a read no cell makes is a read the scan cannot judge.  A cell with a
    parameter the sets give no values raises.
    """
    months = range(proj.t_entry(), proj.proj_len())
    for name in sorted(_monthly_cells(proj)):
        cells, rest = proj.cells[name], proj.cells[name].parameters[1:]
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


def _rule_breaches(proj):
    """R1, R1a and R2 on one row, once it has run on the books.

    The row runs each loop over the frame, the four reports first (:data:`LOOPS`), and
    then every monthly cell at every month on the books (:func:`_sweep_on_the_books`):
    what the row computes of itself, at its own months, which is what Phase 2 sweeps, and
    not S's keys, at which the comparison then evaluates SEC's cells.  Returns
    ``{"negative": [...], "early": [...], "admitted": [...], "ahead": [...],
    "unjudged": [...], "edges": n}``: every cached call with a negative argument, a month,
    an attained age, a policy year or an anniversary; every precedent keyed by a month
    before ``t_entry()`` of a call keyed by a month at or after it, but those
    :data:`EARLY_ADMITTED` admits at the months it may read, which are listed apart; every
    precedent keyed by a month beyond ``t + 1`` of a call keyed by ``t``; every call of a
    cell without a ``t``, the loops over the frame excepted (:data:`LOOPS`), that reads one
    keyed by ``t``; and how many precedents the scan read, which must not be 0, or the
    scans held of nothing.  A precedent is a call's as modelx's dependency graph records
    it.  ULSG reads nothing further ahead than ``t + 1`` anywhere, so R2's one exception, a
    read at the anniversary that closes the policy year, has no use here.
    """
    for name in (*REPORTS, *CHECKS):
        proj.cells[name]()
    _sweep_on_the_books(proj)
    entry, years = proj.t_entry(), proj.mort_improve_max_years
    found = {"negative": [], "early": [], "admitted": [], "ahead": [], "unjudged": []}
    edges = 0
    for name, cells in proj.cells.items():
        params = cells.parameters
        for args in _cached_args(cells):
            if any(_month(a) and a < 0 for a in args):
                found["negative"].append(f"{name}{args}")
            if "t" in params:
                t = args[params.index("t")]
                for node in cells.preds(*args):
                    edges += 1
                    node_params = getattr(node.obj, "parameters", None) or ()
                    if "t" not in node_params:
                        continue
                    u = node.args[node_params.index("t")]
                    if not _month(u):
                        continue
                    call = f"{name}{args} -> {node.obj.name}{node.args}"
                    if u < entry <= t:
                        admitted = ((name, node.obj.name) in EARLY_ADMITTED
                                    and u in (t - 12, 12 * years))
                        found["admitted" if admitted else "early"].append(call)
                    if u > t + 1:
                        found["ahead"].append(call)
            elif name not in LOOPS:
                for node in cells.preds(*args):
                    edges += 1
                    if "t" in (getattr(node.obj, "parameters", None) or ()):
                        found["unjudged"].append(f"{name}{args} -> {node.obj.name}"
                                                 f"{node.args}")
    return {**found, "edges": edges}


# What each monthly cell holds outside cover, before issue and in the month after the
# frame, t = proj_len(), which the roll-forwards read, as its docstring says: no count
# carried, no value, premium, withdrawal, charge, rate, decrement, claim or flow, and no
# question about the contract answered yes.  The type is part of the value: an amount, a
# rate or a count is a float in every branch, a flag a bool and the grace counter and the
# anniversary an int, because Phase 2 types a cell by the values it returns
# (USLIB-SEC-PLAN.md F3).
OUTSIDE_COVER = {
    # flags
    "is_active": False, "is_premium_mth": False, "is_shortfall": False,
    "is_guar_active": False, "is_guar_supported": False,
    # the grace counter and the anniversary, ints
    "grace_mth": 0, "rop_anniversary": 0,
    # premiums and withdrawals
    "premium_pp": 0.0, "prem_persistency": 0.0, "prem_to_av_pp": 0.0, "prem_to_sg_pp": 0.0,
    "cum_prem_pp": 0.0, "wd_pp": 0.0, "wd_fee_pp": 0.0,
    # the face, the death benefit and the cost of insurance
    "sum_assured_at": 0.0, "units": 0.0, "corridor_factor": 0.0, "db_pp": 0.0,
    "net_amt_at_risk": 0.0, "sg_net_amt_at_risk": 0.0, "coi_rate_guar": 0.0,
    "coi_rate": 0.0, "sg_coi_rate": 0.0, "coi_pp": 0.0, "sg_coi_pp": 0.0,
    "rider_charge_pp": 0.0,
    # charges, values, the loan and the guarantee
    "maint_fee_pp": 0.0, "sg_maint_fee_pp": 0.0, "mth_deduction_pp": 0.0,
    "sg_deduction_pp": 0.0, "maint_fee_taken_pp": 0.0, "coi_taken_pp": 0.0,
    "mth_deduction_taken_pp": 0.0, "mth_deduction_forgone_pp": 0.0, "inv_income_pp": 0.0,
    "av_pp": 0.0, "sg_inv_income_pp": 0.0, "sg_pp": 0.0, "sg_net_pp": 0.0,
    "catch_up_prem_pp": 0.0, "loan_bal_pp": 0.0, "surr_charge_rate": 0.0,
    "surr_charge_pp": 0.0, "csv_pp": 0.0, "ncsv_pp": 0.0, "cure_premium_pp": 0.0,
    "rop_ratio": 0.0, "rop_rate": 0.0,
    # rates
    "mort_rate": 0.0, "mort_rate_mth": 0.0, "lapse_rate_base": 0.0, "lapse_rate": 0.0,
    "lapse_rate_mth": 0.0,
    # counts
    "pols_new_biz": 0.0, "pols_death": 0.0, "pols_lapse": 0.0, "pols_rop": 0.0,
    "pols_lapse_grace": 0.0, "pols_maturity": 0.0,
    # flows
    "premiums": 0.0, "prem_to_av": 0.0, "maint_fee": 0.0, "coi": 0.0,
    "mth_deduction": 0.0, "mth_deduction_forgone": 0.0, "inv_income": 0.0,
    "withdrawals": 0.0, "wd_fees": 0.0, "surr_charge": 0.0, "expenses": 0.0,
    "premium_taxes": 0.0, "claims_over_av": 0.0, "margin_expense": 0.0,
    "margin_mortality": 0.0, "margin_rop": 0.0, "net_cf": 0.0,
    # the claims, split by kind at stage EC (R12), and their total
    "claims": 0.0, "claims_death": 0.0, "claims_lapse": 0.0, "claims_refund": 0.0,
    # the cells that read t + 1, which return their zero before they read it
    "av_change": 0.0, "check_av_roll_fwd_resid": 0.0, "check_sg_roll_fwd_resid": 0.0,
    "check_margin_resid": 0.0,
}
# 1.0, the dynamic lapse multiplier's neutral value.
NEUTRAL = {"lapse_rate_dyn_mult": 1.0}
# The status label: before issue, and from t = proj_len() on.
LABELLED = {"status": ("PRE_ISSUE", "CEASED")}
# The policy clock, a Python int at every month, outside cover too: before issue its values
# are negative, or 0, and a cell keyed by them must not read a table there.
CLOCK = ("duration_mth", "duration", "policy_year", "age")
# The inputs read on the valuation clock (D7), floats at every month, one function of t
# and the point's ages for every point: the flat declared rate and its monthly rate,
# floored at the guarantee, expense inflation stepping on valuation years, and mortality
# improvement, the graded rate and the factor it builds from the valuation date, which a
# row issued later reads before its issue.
VALUATION_CLOCK = ("crediting_rate_ann", "inv_return_mth", "inflation_factor",
                   "mort_improve_rate", "mort_improve_factor")
# Cells with a timing or a kind, 0.0 at every one of these outside cover.
BY_ARGUMENT = {"claim_pp": CLAIM_KINDS, "claims_from_av": AV_KINDS,
               "av_pp_at": AV_TIMINGS[1:], "av_at": (*AV_TIMINGS[1:], "EOM"),
               "sg_pp_at": AV_TIMINGS, "loan_bal_pp_at": LOAN_TIMINGS}
# The opening timings, 0.0 before issue, and in the month after the frame what the
# survivors of its last month carry into it (CARRIED): the count, at every timing, the
# account value per policy and in force, and the lapse latch, which the last month's
# lapse at the end of a grace reads there.
OPENING = {"pols_if_at": TIMINGS, "av_pp_at": AV_TIMINGS[:1], "av_at": AV_TIMINGS[:1]}
CARRIED = ("pols_if", "is_lapsed")
# The sets above, which together must hold every cell whose first parameter is t, once.
GUARD_SETS = {"OUTSIDE_COVER": set(OUTSIDE_COVER), "NEUTRAL": set(NEUTRAL),
              "LABELLED": set(LABELLED), "CLOCK": set(CLOCK),
              "VALUATION_CLOCK": set(VALUATION_CLOCK),
              "BY_ARGUMENT, OPENING": set(BY_ARGUMENT) | set(OPENING),
              "CARRIED": set(CARRIED)}


def _monthly_cells(proj):
    """Every cell of ``proj`` whose first parameter is ``t``."""
    return {name for name, cells in proj.cells.items()
            if cells.parameters and cells.parameters[0] == "t"}


def _age_at(p, t):
    """The attained age of month ``t`` on ``p``'s policy clock, before issue included."""
    return p.age_at_entry() + (p.duration_mth_init() + t) // 12


def _improvement_rate(p, a):
    """``ULSG_US_S``'s graded improvement rate at attained age ``a``, from the References.

    The initial rate up to ``mort_improve_full_age``, graded linearly to 0 at
    ``mort_improve_end_age``, 0 from there.
    """
    full, end, rate = (p.mort_improve_full_age, p.mort_improve_end_age,
                       p.mort_improve_rate_init)
    if a <= full:
        return rate
    if a >= end:
        return 0.0
    return rate * ((end - a) / (end - full))


def _improvement_factor(p, t):
    """The improvement factor of month ``t``, built from the valuation date.

    One minus the graded rate of each valuation year before month ``t``, at most
    ``mort_improve_max_years`` of them, each at the attained age of the month a whole
    number of years before ``t``, multiplied in the order S's recursion multiplies them:
    a year accrues on each anniversary of the valuation date, and between them the factor
    moves only where a graded rate it reads moves with the age, at the policy's own
    anniversaries.  Written as a loop from the References, so that the expected value is
    not the model's cell read back.
    """
    years = p.mort_improve_max_years
    base = t if t // 12 <= years else 12 * years
    factor = 1.0
    for j in range(base // 12, 0, -1):
        factor = factor * (1 - _improvement_rate(p, _age_at(p, base - 12 * j)))
    return factor


def _on_the_clocks(p, t):
    """What each cell of :data:`CLOCK` and :data:`VALUATION_CLOCK` holds at month ``t``.

    The policy clock in closed form from the point's ``duration_mth``, and the inputs on
    the valuation clock from the Projection's References, ``t`` and the policy clock's
    ages alone: the flat declared rate and its monthly rate floored at the guaranteed one,
    expense inflation stepping on valuation years, and the graded improvement rate and its
    factor (:func:`_improvement_factor`).
    """
    d = p.duration_mth_init() + t
    rate = p.crediting_rate_curr
    return {"duration_mth": d, "duration": d // 12, "policy_year": d // 12 + 1,
            "age": p.age_at_entry() + d // 12,
            "crediting_rate_ann": rate,
            "inv_return_mth": max((1 + rate) ** (1 / 12) - 1,
                                  (1 + p.guar_rate_ann) ** (1 / 12) - 1),
            "inflation_factor": (1 + p.inflation_rate) ** (t // 12),
            "mort_improve_rate": _improvement_rate(p, _age_at(p, t)),
            "mort_improve_factor": _improvement_factor(p, t)}


def _survivors(p, t):
    """The count the last month ``t - 1`` leaves for ``t``: 0.0 once the latch is shut."""
    if p.is_lapsed(t - 1) or p.grace_mth(t - 1) >= p.grace_months:
        return 0.0
    return (p.pols_if(t - 1) - p.pols_death(t - 1) - p.pols_lapse(t - 1)
            - p.pols_rop(t - 1) - p.pols_lapse_grace(t - 1))


def _outside_cover_faults(p, where):
    """Where ``p``, an ItemSpace, departs from what each monthly cell holds outside cover.

    In every month before issue and at ``t = proj_len()``: every cell of
    :data:`OUTSIDE_COVER`, :data:`NEUTRAL` and :data:`LABELLED`, and :data:`BY_ARGUMENT`
    at each of its timings or kinds, and before issue :data:`OPENING`'s, ``pols_if`` and
    the latch, against their values with their types; :data:`CLOCK` and
    :data:`VALUATION_CLOCK` against :func:`_on_the_clocks`.  At ``t = proj_len()`` the
    latch is the one the last month leaves, the count at every timing is the survivors of
    the last month, out of its count by its deaths, lapses, refunds and lapses at the end
    of a grace, in the products those take, 0.0 once the latch is shut, and the account
    value per policy is the last month's close.  Then the keyed readers: the lapse table's
    keys run from 1 to the policy year of the last month, the age-keyed tables' from the
    age at the first month on the books to the age of the last, the endorsement's
    membership test reads completed years from the first month on the books to the last,
    and its two readers read the table's anniversaries alone, so no table was read at a
    year, an age or an anniversary the policy does not have.  And no monthly cell holds a
    ``t`` past ``proj_len()``.  A cell that raises is a fault too, so the scan goes on.
    """
    faults = []
    L, entry = p.proj_len(), p.t_entry()

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
        check("status", (t,), _code(p, LABELLED["status"][0 if t < entry else 1]))
        for name, labels in BY_ARGUMENT.items():
            for label in labels:
                check(name, (t, _code(p, label)), 0.0)
        if t < entry:
            for name, labels in OPENING.items():
                for label in labels:
                    check(name, (t, _code(p, label)), 0.0)
            check("pols_if", (t,), 0.0)
            check("is_lapsed", (t,), False)
        for name, want in _on_the_clocks(p, t).items():
            check(name, (t,), want)
    check("is_lapsed", (L,), p.is_lapsed(L - 1) or p.grace_mth(L - 1) >= p.grace_months)
    survivors = _survivors(p, L)
    check("pols_if", (L,), survivors)
    for timing in TIMINGS:
        check("pols_if_at", (L, _code(p, timing)), survivors)
    bef_prem = _code(p, "BEF_PREM")
    check("av_pp_at", (L, bef_prem), p.av_pp(L - 1))
    check("av_at", (L, bef_prem), p.av_pp_at(L, bef_prem) * p.pols_if(L))
    ranges = {**{name: range(1, p.policy_year(L - 1) + 1) for name in KEYED_BY_YEAR},
              **{name: range(p.age(entry), p.age(L - 1) + 1) for name in KEYED_BY_AGE},
              "is_rop_anniv": range(p.duration(entry), p.duration(L - 1) + 1)}
    windows = [int(y) for y in p.data.rop_table().index]
    ranges.update({name: windows for name in KEYED_BY_ANNIV[1:]})
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


def _carry(p):
    """What the survivors of the last month carry into ``t = proj_len()`` on ``p``.

    The values the end-of-projection test asserts, read once the row is projected: the
    count there, at every timing, and the survivors it must be; the latch; the account
    value per policy there and the last month's close; the account value in force there;
    the three checks, which read it; and the flows of that month, which must be zero.
    """
    L = p.proj_len()
    bef_prem = _code(p, "BEF_PREM")
    return {
        "L": L, "pols_if": p.pols_if(L), "latch": p.is_lapsed(L),
        "timings": [p.pols_if_at(L, _code(p, timing)) for timing in TIMINGS],
        "survivors": _survivors(p, L),
        "av_pp": p.av_pp_at(L, bef_prem), "av_pp_last": p.av_pp(L - 1),
        "av_at": p.av_at(L, bef_prem),
        "checks": tuple(p.cells[check]() for check in CHECKS),
        "flows": [p.premiums(L), p.pols_death(L), p.pols_lapse(L), p.pols_rop(L),
                  p.pols_lapse_grace(L), p.expenses(L), p.withdrawals(L), p.net_cf(L),
                  p.claims(L), p.claims_death(L), p.claims_lapse(L), p.claims_refund(L)]}


def _lapse_raw(x, t):
    """The annual lapse rate before its floor and its cap: S's product of four factors."""
    return (x.lapse_rate_base(t) * x.lapse_rate_guar_mult() * x.lapse_rate_pattern_mult()
            * x.lapse_rate_dyn_mult(t))


def _surr_charge_raw(x, t):
    """The surrender charge per $1,000 of month ``t`` before its floor at 0."""
    init, yrs = x.surr_charge_rate_max(), x.surr_charge_runoff_years()
    return init - (init / yrs) * ((x.duration_mth(t) + 1) / 12)


def _corridor_raw(x, t):
    """The corridor's death benefit in month ``t``, which the face bounds from below."""
    return x.corridor_factor(t) * max(x.av_pp_at(t, _code(x, "BEF_COI")), 0.0)


def _naar_raw(x, t, factor, account):
    """A net amount at risk before its floor at 0: the base's or the shadow account's."""
    return x.db_pp(t) / factor - max(account(t, _code(x, "BEF_COI")), 0.0)


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, on a row in force there, each kind of
# valuation month the full grid has, each on the raw value at t = 0 (USLIB-SEC-PLAN.md
# §7.7, Record — M9, Each kind of valuation month): every opening-state column in use, the
# shadow account below 0, a window, a 50% window, a refund capped and a window at t = 1, a
# premium, one into an exhausted account, and a withdrawal, the account carrying its
# deduction, running out, and exhausted under the guarantee, the corridor binding, the
# shadow account's net amount at risk floored, a surrender charge and its last month,
# ten-pay's first unpaid anniversary, the net cash value floored under a loan, a grace
# opening, a counter carried in that advances and another that resets, and each pin alone
# and both together.  Of every row, the end of the frame leaves survivors to carry and a
# latch shut, and the lifetime guarantee's boundary is met on each side.  Later in the
# frame, on every row, a premium in each mode, the single premium and ten-pay's stop, the
# account exhausted under the guarantee, a grace, a lapse, each branch of the dynamic
# multiplier and each pattern and guarantee multiplier, a loan on an exhausted account,
# which takes the account below 0 and decides the guarantee test, and each floor and cap S
# writes, passed by the raw value it bounds; the test also reads each side of every min
# and max by the values it compares (_BoundSides).
AT_VALUATION = {
    **{f"{column} in use": (lambda x, column=column: x.cells[column]() != 0)
       for column in STATE},
    "the shadow account below 0 at t = 0": lambda x: x.sg_pp_init() < 0.0,
    "a window at t = 0": lambda x: x.rop_anniversary(0) > 0,
    "a 50% window at t = 0": lambda x: x.rop_ratio(0) == 0.5,
    "the refund capped at t = 0": lambda x: (
        x.rop_ratio(0) > 0.0
        and x.rop_ratio(0) * x.cum_prem_pp(0) > x.rop_cap_rate * x.sum_assured_at(0)),
    "a window at t = 1": lambda x: x.rop_anniversary(1) > 0,
    "a premium at t = 0": lambda x: x.premium_pp(0) > 0.0,
    "a premium into an exhausted account at t = 0": lambda x: (
        x.av_pp_init() == 0.0 and x.premium_pp(0) > 0.0),
    "a withdrawal at t = 0": lambda x: x.wd_pp(0) > 0.0,
    "the account carrying its deduction at t = 0": lambda x: (
        x.av_pp_init() > 0.0 and x.av_pp_at(0, _code(x, "BEF_COI")) - x.coi_pp(0) >= 0.0),
    "the account running out at t = 0": lambda x: (
        x.av_pp_init() > 0.0 and x.av_pp_at(0, _code(x, "BEF_COI")) - x.coi_pp(0) < 0.0),
    "the guarantee carrying an exhausted account at t = 0": lambda x: (
        x.av_pp_init() == 0.0 and x.is_shortfall(0) and x.is_guar_supported(0)),
    "the corridor binding at t = 0": lambda x: (
        _corridor_raw(x, 0) > x.sum_assured_at(0)),
    "the shadow net amount at risk floored at t = 0": lambda x: (
        _naar_raw(x, 0, x.sg_naar_factor(), x.sg_pp_at) < 0.0),
    "a surrender charge at t = 0": lambda x: (
        x.has_surr_charge() and _surr_charge_raw(x, 0) > 0.0),
    "the surrender charge's last month at t = 0": lambda x: (
        x.has_surr_charge() and _surr_charge_raw(x, 0) <= 0.0 < _surr_charge_raw(x, 0)
        + x.surr_charge_rate_max() / (12 * x.surr_charge_runoff_years())),
    "ten-pay's first unpaid anniversary at t = 0": lambda x: (
        x.is_ten_pay_premium() and x.duration_mth(0) == 12 * x.ten_pay_years),
    "the net cash value's floor at t = 0": lambda x: (
        x.pols_lapse(0) > 0.0 and x.csv_pp(0) - x.loan_bal_pp(0) < 0.0),
    "the grace opening at t = 0": lambda x: (
        x.grace_mth_init() == 0 and x.grace_mth(0) == 1),
    "a counter carried in and advanced at t = 0": lambda x: (
        x.grace_mth_init() > 0 and x.grace_mth(0) == x.grace_mth_init() + 1),
    "a counter carried in and reset at t = 0": lambda x: (
        x.grace_mth_init() > 0 and x.grace_mth(0) == 0),
    "the persistency pin alone at t = 0": lambda x: (
        x.has_prem_persistency_override() and x.coi_rate_dp() < 0
        and x.prem_persistency(0) == x.prem_persistency_override()),
    "the precision pin alone at t = 0": lambda x: (
        not x.has_prem_persistency_override() and x.coi_rate_dp() >= 0
        and x.coi_rate(0) == round(x.coi_curr_factor * x.coi_rate_guar(0),
                                   x.coi_rate_dp())),
    "both pins at t = 0": lambda x: (
        x.has_prem_persistency_override() and x.coi_rate_dp() >= 0),
}
ON_THE_ROW = {
    "survivors carried into proj_len()": lambda x: x.pols_if(x.proj_len()) > 0.0,
    "the latch shut at proj_len()": lambda x: x.is_lapsed(x.proj_len()),
    "a guarantee to the lifetime guarantee's age": lambda x: (
        x.guarantee_age() == x.lifetime_guarantee_age),
    "a guarantee to a year short of it": lambda x: (
        x.guarantee_age() == x.lifetime_guarantee_age - 1),
}
IN_FRAME = {
    **{f"a premium paid {mode}": (
        lambda x, t, n=n: x.premium_freq() == n and x.premium_pp(t) > 0.0
        and not x.is_single_premium())
       for mode, n in (("annually", 1), ("semi-annually", 2), ("quarterly", 4),
                       ("monthly", 12))},
    "the single premium collected": lambda x, t: (
        x.is_single_premium() and x.premium_pp(t) > 0.0),
    "ten-pay's premiums stopped": lambda x, t: (
        x.is_ten_pay_premium() and x.duration(t) >= x.ten_pay_years
        and x.duration_mth(t) % (12 // x.premium_freq()) == 0),
    "the account exhausted under the guarantee": lambda x, t: (
        x.is_shortfall(t) and x.is_guar_supported(t)),
    "a month in grace": lambda x, t: x.grace_mth(t) > 0,
    "a grace opening in the issue month": lambda x, t: (
        x.duration_mth(t) == 0 and x.grace_mth(t) == 1),
    "a lapse at the end of a grace": lambda x, t: x.pols_lapse_grace(t) > 0.0,
    "the dynamic multiplier with the guarantee failed": lambda x, t: (
        not x.is_guar_active(t)),
    "the dynamic multiplier with the account positive": lambda x, t: (
        x.is_guar_active(t) and x.av_pp(t) > 0.0),
    "the dynamic multiplier with the guarantee alone": lambda x, t: (
        x.is_guar_active(t) and not x.av_pp(t) > 0.0),
    **{f"the pattern multiplier {ref}": (
        lambda x, t, ref=ref: x.lapse_rate_pattern_mult() == (
            1.0 if ref == "of a level premium" else x.refs[ref]))
       for ref in ("lapse_pattern_mult_single", "lapse_pattern_mult_ten_pay",
                   "of a level premium")},
    "the lifetime guarantee's lapse multiplier": lambda x, t: (
        x.lapse_rate_guar_mult() == x.lapse_guar_mult),
    "a guarantee short of lifetime": lambda x, t: x.lapse_rate_guar_mult() == 1.0,
    "the lapse rate's floor binding": lambda x, t: _lapse_raw(x, t) < x.lapse_rate_floor,
    "the corridor binding": lambda x, t: _corridor_raw(x, t) > x.sum_assured_at(t),
    "the net amount at risk floored": lambda x, t: (
        _naar_raw(x, t, x.naar_factor(), x.av_pp_at) < 0.0),
    "the shadow net amount at risk floored": lambda x, t: (
        _naar_raw(x, t, x.sg_naar_factor(), x.sg_pp_at) < 0.0),
    "the account before its COI below 0": lambda x, t: (
        x.av_pp_at(t, _code(x, "BEF_COI")) < 0.0),
    "the shadow account before its COI below 0": lambda x, t: (
        x.sg_pp_at(t, _code(x, "BEF_COI")) < 0.0),
    "the maintenance fee taken bounded by the account": lambda x, t: (
        x.maint_fee_pp(t) > max(x.av_pp_at(t, _code(x, "BEF_FEE")), 0.0)),
    "the account before the fee below 0": lambda x, t: (
        x.av_pp_at(t, _code(x, "BEF_FEE")) < 0.0),
    "the COI taken bounded by the account": lambda x, t: (
        x.coi_pp(t) > max(x.av_pp_at(t, _code(x, "BEF_COI")), 0.0)),
    "the account value's floor": lambda x, t: (
        x.av_pp_at(t, _code(x, "BEF_COI")) - x.coi_pp(t) < 0.0),
    "a catch-up premium": lambda x, t: -x.sg_net_pp(t) > 0.0,
    "the catch-up premium's floor": lambda x, t: -x.sg_net_pp(t) < 0.0,
    "the surrender charge's floor": lambda x, t: (
        x.has_surr_charge() and _surr_charge_raw(x, t) < 0.0),
    "the cash value's floor": lambda x, t: x.av_pp(t) - x.surr_charge_pp(t) < 0.0,
    "the net cash value's floor": lambda x, t: (
        x.pols_lapse(t) > 0.0 and x.csv_pp(t) - x.loan_bal_pp(t) < 0.0),
    "the refund's cap": lambda x, t: (
        x.rop_ratio(t) > 0.0
        and x.rop_ratio(t) * x.cum_prem_pp(t) > x.rop_cap_rate * x.sum_assured_at(t)),
    "a 50% window": lambda x, t: x.rop_ratio(t) == 0.5,
    "a 100% window": lambda x, t: x.rop_ratio(t) == 1.0,
    "a window at a t not a multiple of 12": lambda x, t: (
        x.rop_anniversary(t) > 0 and t % 12 != 0),
    "the lapse table read past its last year": lambda x, t: (
        x.policy_year(t) > x.data.lapse_last_year()),
    "the mortality table read below its first age": lambda x, t: (
        x.age(t) < x.data.mort_age_first()),
    "a COI scale read past its last age": lambda x, t: x.age(t) > x.coi_rate_last_age(),
    "a loan outstanding": lambda x, t: x.loan_bal_pp(t) > 0.0,
    "the account entering a month below 0": lambda x, t: (
        x.av_pp_at(t, _code(x, "BEF_PREM")) < 0.0),
    "the loan deciding the guarantee test": lambda x, t: (
        x.is_shortfall(t) and x.sg_pp_at(t, _code(x, "BEF_INV")) > 0.0
        and not x.is_guar_supported(t)),
    "a withdrawal and its fee": lambda x, t: x.wd_pp(t) > 0.0 and x.wd_fee_pp(t) > 0.0,
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
    (:attr:`sides`); a call is told apart by its position in its formula's code, which
    Python gives from 3.11, and before it :meth:`watch` records nothing.  It is
    ``VA_US_SEC``'s module's record, as that module keeps it.
    """

    def __init__(self, model):
        self.codes = {cells.formula.func.__code__: name
                      for name, cells in model.Projection.cells.items()}
        self.sites, self.positions = {}, {}
        for name, cells in model.Projection.cells.items():
            source = cells.formula.source
            fn = ast.parse(source).body[0]
            for node in ast.walk(fn):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                        and node.func.id in ("min", "max") and len(node.args) > 1):
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
# (_BoundSides): the lapse rate's cap and the credited rate's floor at the guarantee, which
# ULSG_US_S ships idle, on the second splice's core; the cap on mortality, on a point made
# to pass it; the corridor table's clamps at its first and last ages and the mortality
# table's at its last, on tables shorter than the cover, the shipped ones reaching past
# every age in cover; and the shadow account residual's floor of 1, which wins only where
# both its sides are below 1, in no month of any row of the splice's grids.  The core-reach
# test holds the core to the rest: a side named here that a core row binds fails it, as
# does a side named nowhere that none binds.  No side is idle: each binds on some row
# compared with S.
BOUND_ELSEWHERE = {
    ("inv_return_mth", "max((1 + crediting_rate_ann(t)) ** (1 / 12) - 1, guar_rate_mth())",
     1): "test_the_idle_core_reaches_each_bound",
    ("lapse_rate", "min(lapse_rate_cap, max(lapse_rate_floor, rate))", 0):
        "test_the_idle_core_reaches_each_bound",
    ("mort_rate", "min(mort_rate_base_at(age(t)) * class_factor() * mort_ae_factor * "
                  "mort_improve_factor(t), 1.0)", 1):
        "test_an_annual_mortality_past_1_is_capped_in_both_models",
    ("corridor_factor_at", "min(max(a, data.corridor_age_first()), last)", 1):
        "test_a_table_shorter_than_the_cover_is_read_at_its_ends_in_both_models",
    ("corridor_factor_at", "max(a, data.corridor_age_first())", 1):
        "test_a_table_shorter_than_the_cover_is_read_at_its_ends_in_both_models",
    ("mort_rate_base_at", "min(max(a, data.mort_age_first()), last)", 1):
        "test_a_table_shorter_than_the_cover_is_read_at_its_ends_in_both_models",
    ("check_sg_roll_fwd_resid", "max(abs(end), abs(sg), 1.0)", 2):
        "test_each_check_decides_as_isclose_does_where_its_sides_are_small",
}
# The sides no row compared with S can bind, each with its premise: none.
IDLE_SIDES = {}


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
        record = {"negative": [], "early": [], "admitted": [], "ahead": [],
                  "unjudged": [], "edges": 0, "raised": _raised(err)}
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
        record = records.setdefault(case, {"negative": [], "early": [], "admitted": [],
                                           "ahead": [], "unjudged": [], "edges": 0})
        record.update(branches=set(), carry=None, guard=[], raised=_raised(err))
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


def _every_state_months(sp):
    """The months S point ``sp``, swept, is restated at by the every-state test.

    By default the edges of its windows (USLIB-SEC-PLAN.md §5.2, T5): every month of its
    first policy year after S's own start, each anniversary and the month before it, where
    the withdrawals' first year, the ten-pay years, the surrender charge and the
    return-of-premium windows open and close, each month a grace opens in or runs through,
    the month either side of each change in the sign of the account value entering a month,
    and the last month of its frame.  With ``USLIB_SEC_FULL=1``, every month of its frame.
    The caller stops at its lapse.
    """
    n = sp.proj_len()
    if SEC_FULL:
        return list(range(1, n))
    d0, bef_prem = sp.duration_mth_init(), _code(sp, "BEF_PREM")
    below = [sp.av_pp_at(d, bef_prem) < 0.0 for d in range(n)]
    months = {*range(1, min(12, n)), n - 1}
    for d in range(1, n):
        if (d0 + d) % 12 in (0, 11) or sp.grace_mth(d) > 0 or sp.grace_mth(d - 1) > 0:
            months.add(d)
        if below[d] != below[d - 1]:
            months |= {d - 1, d}
    return sorted(m for m in months if m >= 1)


def _states_s_reaches(s):
    """The states ``s``'s points reach, as ``(S point, month)``: ``(kept, below)``.

    Each month of :func:`_every_state_months` of each point of ``s``, an S model already
    swept, before the point's lapse, from which on no policy is in force to restate.
    ``below`` holds the months whose account value entering is below 0, the one state the
    product refuses by name: ``ULSG_US_S`` carries one under a loan on an exhausted
    account, and no policy in force holds one (D6).  ``kept`` holds every other.
    """
    kept, below = [], []
    for key, point_id in zip(point_keys(s), s.Data.model_point_table().index):
        sp = projection(s, key)
        bef_prem = _code(sp, "BEF_PREM")
        for d in _every_state_months(sp):
            if sp.is_lapsed(d):
                break
            (below if sp.av_pp_at(d, bef_prem) < 0.0 else kept).append((point_id, d))
    return kept, below


def _refused_in_force(s, states, root, refs):
    """What ``Data`` and ``proj_len()`` refuse of ``states`` of ``s``, restated in force.

    The generator builds one table of every point's twin and a derived row at each state
    (:func:`_spliced_folder`), which a model read with ``refs`` set first reads, through
    ``Data``, and then asks every row for its frame, releasing each, collecting every 500.
    Returns each refusal, the line naming it, ``Data``'s or each row's ``proj_len()``'s.
    """
    model = _read(_spliced_folder(root, s, states, ()), "every", refs)
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
            except Exception as err:            # reported, so every row is asked
                refused.append(_raised(err))
            _release(model, key, collect=i % 500 == 499)
        return refused
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
                                                          splice_bounds, kind, s_point,
                                                          month):
        """Opened with S's state at month d, the point is S from d on, in every cell of S's.

        This is the test that says the opening state is complete: a state column the SEC
        row did not carry, or carried from the wrong instant, would make SEC part from S
        here, and nowhere else, because on a point issued at ``t = 0`` the two clocks
        coincide and the opening state is zero.  The account value, the shadow account,
        never floored, the loan and the premiums paid to date open from their own columns,
        and the grace counter from its own, so that a counter carried in advances to the
        lapse a month on, or resets where the month's deduction stops failing, as S's does.
        For the same reason it is the test that catches a policy month passed as ``t``
        (R1a), a look-back that stops at the wrong month, a pin applied in the wrong month,
        and a return-of-premium window tested on the valuation clock: the rows valued
        mid-year put a window at ``t = 1``.  The frame comparisons read SEC row ``t``
        against S row ``t + d`` in every column of the four reports both models hold, and
        fail frames that end apart.  The cell comparison then evaluates every cell of S's
        but :data:`SPLICE_EXEMPT`, at every argument S cached inside its own frame from
        month ``d`` on, moved onto SEC's clock: the account value and the shadow account at
        every timing, the loan, the counts, the grace counter, the latch, the status and
        the checks.  An S cell this model lacked would fail it.

        S's own in-force points, opened at its ``t = 0``, are cases too, at offset 0, and
        their twins skip only T1's exemptions: their opening accessors are S's.  Every
        value is held to 1e-9 relative with no absolute floor, because near the end of a
        long frame the counts fall far below 1e-7, to 1.2e-10 on variant 8, where the
        floor would compare them against nothing.  ``ULSG_US_S`` has no residual cell, its
        checks being bools, so no compared cell is a residual rounding around 0 that keeps
        the floor; this model's three residual cells are held through the checks, which are
        compared as bools.

        The row is scanned for the rules test first (:func:`_scanned`), then compared, the
        sides of each ``min`` and ``max`` both bind kept (:class:`_BoundSides`), then
        recorded for the tests after this one and released (:func:`_settle`).
        """
        s, sec = spliced
        case = (kind, s_point, month)
        key = _row_key(sec, *case)
        try:
            with splice_bounds.watch() as won:
                sec_proj = projection(sec, key)
                _scanned(splice_records, case, sec_proj)["bounds"] = won
                s_proj = _point(s, s_point)
                for report in REPORTS:
                    assert frame_mismatches(s_proj.cells[report](),
                                            sec_proj.cells[report](), t_offset=month,
                                            atol=0.0) == [], report
                exempt = TWIN_EXEMPT if kind == "twin" else SPLICE_EXEMPT
                assert _twin(s_proj, sec_proj, t_offset=month, exempt=exempt,
                             atol=0.0) == []
        finally:
            _settle(splice_records, case, sec, key)

    @pytest.mark.parametrize(
        "s_point, k",
        [_case(case, CORE_FUTURES, _case_id("future", case[0], -case[1]))
         for case in FUTURES])
    def test_future_new_business_is_the_s_projection_k_months_on(self, spliced,
                                                                 splice_records,
                                                                 splice_bounds, s_point,
                                                                 k):
        """Issued k months after the valuation date, the point is S's projection k on.

        SEC rows ``k ..`` are S rows ``0 ..``, ending together at the end of the
        projection, in the four reports, and every cell of S's but :data:`FUTURE_EXEMPT`
        agrees at every argument S cached inside its own frame, moved ``k`` later, to 1e-9
        relative with no absolute floor, ``pols_if_at`` at every timing but ``"BEF_NB"`` in
        the issue month (:func:`_issued_later`).  An S cell this model lacked would fail
        it.  Before issue every column of the four reports is an exact zero, or the status
        ``PRE_ISSUE``, and the policies arrive in month ``k`` as new business.  A single
        premium is collected once, in the issue month.

        The last assertions are R1 and D4's base rule made testable.  After every report,
        no decrement rate keyed by month has been evaluated at a month before issue; no
        table keyed by a policy year has been read below year 1, no age-keyed table below
        the issue age, and the endorsement's table at no completed year below 0.  A chain
        based at ``t == 0`` rather than at ``t_entry()``, or a rate evaluated before the
        month is asked whether it is in cover, still gives the right numbers.  This is the
        only test that sees the first, and the guard test sees the second too.

        The pre-issue rows are asserted present before they are asserted zero, in each of
        the reports: a frame that opened at issue would have none, its zeros would hold of
        nothing, and the comparisons with S, which start at issue, would not see it.  The
        row is scanned for the rules test first (:func:`_scanned`), the sides of each
        ``min`` and ``max`` its scan and comparison bind kept (:class:`_BoundSides`), and
        recorded and released once compared (:func:`_settle`).
        """
        s, sec = spliced
        case = ("future", s_point, -k)
        key = _row_key(sec, *case)
        try:
            with splice_bounds.watch() as won:
                sec_proj = projection(sec, key)
                _scanned(splice_records, case, sec_proj)["bounds"] = won
                s_proj = _point(s, s_point)
                frames = {report: sec_proj.cells[report]() for report in REPORTS}
                for report, frame in frames.items():
                    assert frame_mismatches(s_proj.cells[report](), frame, t_offset=-k,
                                            atol=0.0) == [], report
                assert _twin(s_proj, sec_proj, t_offset=-k, exempt=FUTURE_EXEMPT,
                             arg_map=_issued_later, atol=0.0) == []
            for report, frame in frames.items():
                assert list(frame.index[:k]) == list(range(k)), report
                before = frame.loc[:k - 1]
                labels = list(LABEL_COLUMNS.get(report, ()))
                amounts = before.drop(columns=labels)
                assert (amounts == 0.0).all().all(), report
                if "status" in labels:
                    assert all(_status_is(sec_proj, t, "PRE_ISSUE")
                               for t in range(k)), report
                    assert (before["status"] == "PRE_ISSUE").all(), report
            assert sec_proj.pols_new_biz(k) == sec_proj.policy_count() == 1.0
            early = {name: sorted(t for t in sec_proj.cells[name].keys() if t < k)
                     for name in DECREMENT_RATES}
            assert not any(early.values()), f"rates evaluated before issue: {early}"
            floors = {**dict.fromkeys(KEYED_BY_YEAR, 1),
                      **dict.fromkeys(KEYED_BY_AGE, sec_proj.age_at_entry()),
                      "is_rop_anniv": 0}
            for name, floor in floors.items():
                keys = sorted(sec_proj.cells[name].keys())
                assert all(key >= floor for key in keys), f"{name} read at {keys[:5]}"
            assert sec_proj.cells["mort_rate_base_at"].keys(), "no mortality rate was read"
            if sec_proj.is_single_premium():
                assert [sec_proj.premium_pp(t) for t in range(sec_proj.proj_len())] == [
                    sec_proj.premium_pp_ann() if t == k else 0.0
                    for t in range(sec_proj.proj_len())]
        finally:
            _settle(splice_records, case, sec, key)

    @pytest.mark.parametrize(
        "kind, s_point, month",
        [_case(case, CORE_SPLICES, _case_id(*case)) for case in VARIANT_TWINS])
    def test_a_variant_issued_at_the_valuation_date_is_its_s_point(self, spliced,
                                                                   splice_records,
                                                                   splice_bounds, kind,
                                                                   s_point, month):
        """Issued at the valuation date, each variant is its S point in every cell of S's.

        T1 compares the twins of S's own new business with S cell by cell, in the
        conventions suite; the variants carry what those cannot, and an issue rule that
        only a variant takes at ``t = 0`` is reached nowhere else, a row issued later
        taking it at ``t = k`` and a row restated taking none (USLIB-SEC-PLAN.md §7.7,
        *Record — M9*, *Variants' twins*).  So the twin of each variant issued at the
        valuation date, which the generator puts in the splice's table beside the rows it
        derives, is compared as a row issued there is: frame by frame, the four reports,
        and cell by cell over every cell of S's but T1's exemptions, every one to 1e-9
        relative with no absolute floor, at every argument S cached but
        ``pols_if_at(0, "BEF_NB")`` (:func:`_continues_s`, :func:`_issued_later`).  Among
        them, variants 9 and 16 meet the lifetime guarantee's age exactly on both sides.
        The variants of S's point 1, in force 300 months, take no issue rule at
        ``t = 0``, and are splice cases at offset 0 (:data:`IN_FORCE_TWINS`).  The row is
        scanned first, the sides of each ``min`` and ``max`` kept, and recorded and
        released once compared, as T2's rows are.
        """
        s, sec = spliced
        case = (kind, s_point, month)
        key = _row_key(sec, *case)
        try:
            with splice_bounds.watch() as won:
                sec_proj = projection(sec, key)
                _scanned(splice_records, case, sec_proj)["bounds"] = won
                assert _continues_s(_point(s, s_point), sec_proj, 0, TWIN_EXEMPT,
                                    _issued_later) == []
        finally:
            _settle(splice_records, case, sec, key)

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
        as Phase 2's sweep (:func:`_sweep_on_the_books`), so that a read no report makes is
        judged too:

        * R1: no cell holds a negative argument, a month, an attained age, a policy year
          or an anniversary.  modelx evaluates one without complaint, and a compiled cache
          raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).
        * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
          ``t_entry()`` on read a month before it.  On a point issued later a chain based
          at ``t == 0``, as ``ULSG_US_S``'s account value, shadow account, loan, premiums
          paid, grace counter, latch and count all were, reads the pre-issue zeros, so no
          number shows it and no argument goes negative.  This is the test that holds
          those bases at ``t_entry()`` (R1a).  The one look-back allowed is the improvement
          factor's (:data:`EARLY_ADMITTED`): it runs from the valuation date for every row,
          so a row issued later reads the factor and the graded rate a year back, before
          its issue, at no month but ``t - 12`` or ``12 x mort_improve_max_years``, which
          is checked read by read, and the core's future rows must make such a read, or
          the admission would hold of nothing.
        * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month
          beyond ``t + 1``, as modelx's dependency graph records each cached call's
          precedents.  ULSG has no read further ahead, so R2's one exception has no use
          here.
        * The premise of the two scans: no cell without a ``t`` but the loops over the
          frame reads one keyed by ``t``, so a read through a cell keyed by an attained age,
          a policy year or an anniversary is a read of the month that asked.

        Each row was scanned by the case that compared it, before the comparison
        (:func:`_scanned`), and a row no case has scanned is scanned here.  The core case
        covers the core's rows, the full case every other row of the full grid, with
        ``USLIB_SEC_FULL=1``, the variants' twins among them.  The twins of S's own new
        business in the splice's table are no case's, and are left out: on them the clocks
        coincide, and T1 compares them with S cell by cell.  The closed-form clock and the
        recursion depth are asserted on the committed model and on models read for the
        test.
        """
        cases = [case for case in GRID if (case in CORE_GRID) == (grid == "core")]
        found = {"negative": [], "early": [], "ahead": [], "unjudged": []}
        admitted = []
        raised, unscanned = [], []
        for case in cases:
            record = _record_of(spliced, splice_records, case, splice_bounds)
            where = _case_id(*case)
            for rule, calls in found.items():
                calls += [f"{where}: {call}" for call in record[rule]]
            if case[0] == "future":
                admitted += record["admitted"]
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
        assert admitted, "no future row read the improvement factor before its issue"

    def test_every_guarded_cell_holds_its_outside_cover_value_on_the_splice(
            self, spliced, splice_records, splice_bounds):
        """Outside cover each monthly cell holds its value on every row the splice compared.

        :data:`GUARD_SETS` say what each cell whose first parameter is ``t`` holds before
        issue and at ``t = proj_len()``, the month after the frame, which the roll-forwards
        read (:func:`_outside_cover_faults`).  On every row the splice compared, the core's
        or, with ``USLIB_SEC_FULL=1``, all of them, as each was recorded once compared
        (:func:`_settle`): there the survivors carried into ``t = proj_len()`` are not zero
        on the rows that do not lapse, the latch is shut there on those that do, and the
        variants' future rows read policy years -1 and 0 before issue, the single
        premium's and ten-pay's among them.

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

        The projection ends where premiums and charges cease, at attained age 121, while
        the contract's coverage continues, and S's roll-forwards read the month after the
        frame.  At the splice's A/E of 0.56 there are lives left at the end of every frame
        that does not lapse, 3.2e-6 of a policy on S's point 3, so on every row the splice
        compared, the core's or, with ``USLIB_SEC_FULL=1``, all of them:

        * the latch at ``t = proj_len()`` is the one the last month leaves, and the count
          there, at every timing, is the survivors of the last month, exactly, or 0.0 once
          the latch is shut;
        * the account value per policy there is the last month's close, exactly, and the
          account value in force there the two multiplied;
        * all three are S's at the same month, ``proj_len() + source_mth`` on S's clock,
          exactly on the twins and the future rows, whose opening values are S's own and
          not read back from a CSV, and to 1e-9 on the rest; and the three checks, which
          read them, decide as S's do, which on the two variants whose withdrawals outrun
          an exhausted account, and on the one whose loan takes its account below 0, is
          ``False`` for the account value's and the margin's in both models (ULSG_US_S pays
          the withdrawal out of nothing, and credits the account a loan exceeds below 0);
        * and nothing else happens there: no premium, death, lapse, refund, withdrawal,
          claim or expense, and a net cash flow of 0.

        At least one row carries survivors, and at least one a shut latch.
        """
        s = spliced[0]
        cases = _selected(GRID, CORE_GRID)
        faults, survivors, shut = [], [], []
        for case in cases:
            kind, s_point, month = case
            where = _case_id(*case)
            record = _record_of(spliced, splice_records, case, splice_bounds)
            carry = record["carry"]
            if carry is None:
                faults.append(f"{where}: raised {record['raised']}")
                continue
            exact = kind != "derived"
            s_proj, s_month = _point(s, s_point), carry["L"] + month
            theirs = (s_proj.pols_if(s_month), s_proj.is_lapsed(s_month),
                      s_proj.av_at(s_month, _code(s_proj, "BEF_PREM")))
            mine = (carry["pols_if"], carry["latch"], carry["av_at"])
            if carry["pols_if"] > 0.0:
                survivors.append(where)
            if carry["latch"]:
                shut.append(where)
            if carry["pols_if"] != carry["survivors"] or any(
                    count != carry["survivors"] for count in carry["timings"]):
                faults.append(f"{where}: the count carried is not the survivors: {carry}")
            if (carry["av_pp"] != carry["av_pp_last"]
                    or carry["av_at"] != carry["av_pp"] * carry["pols_if"]):
                faults.append(f"{where}: the account value carried is not the close: "
                              f"{carry}")
            close = mine[1] == theirs[1] and pytest.approx(
                (theirs[0], theirs[2]), rel=1e-9, abs=0.0) == (mine[0], mine[2])
            if not (mine == theirs if exact else close):
                faults.append(f"{where}: {mine} carried, where S carries {theirs}")
            s_checks = tuple(s_proj.cells[check]() for check in CHECKS)
            if carry["checks"] != s_checks:
                faults.append(f"{where}: the checks decide {carry['checks']}, S's "
                              f"{s_checks}")
            if any(flow != 0.0 for flow in carry["flows"]):
                faults.append(f"{where}: flows at t = proj_len(): {carry['flows']}")
        assert cases and not faults, faults[:10]
        assert survivors and shut, (survivors, shut)

    def test_the_core_grid_reaches_every_branch(self, spliced, splice_records,
                                                splice_bounds):
        """What the default run's T2 and T3 cases reach, which the full grid multiplies.

        The default run thins the splice to a core (the module docstring), and this test is
        what keeps the thinning from costing a branch.  The core was chosen by the lines of
        the model each row of the full grid runs, so that the core runs every one; and
        since a branch that differs only in the month it fires covers no line of its own,
        each event has a core row in its own month.  First, statically, over S's table with
        the variants, each property below holds of some core case: each premium pattern and
        mode, each sex and class, each surrender charge schedule and none, the endorsement
        and none, each guarantee age, each issue age, withdrawals, a loan, both pins and
        each alone, S's in-force points as their twins and restated, the worked example's
        point as its twin, a variant issued at the valuation date as its twin, and each
        kind of valuation month, on the policy clock: the first month after issue,
        mid-year, the month before an anniversary, on an anniversary and the last covered
        month.  And of some core future case: issued within a year, more than a year on
        and more than two, a single premium, ten-pay and a pin.  And the issue month of
        each variant issued at the valuation date, on its twin or on a row issued later
        (:data:`VARIANT_TWINS`).

        Then, on the splice's model, of some core row, each of :data:`AT_VALUATION`,
        :data:`ON_THE_ROW` and :data:`IN_FRAME`, what no column of the table shows: each
        kind of valuation month the full grid has, every opening-state column in use among
        them, each on its raw value at ``t = 0``; survivors carried, a latch shut and the
        lifetime guarantee's age met on each side; and later in the frame a premium in each
        mode, the single premium and ten-pay's stop, the account exhausted under the
        guarantee, a grace and a lapse, each branch of the dynamic multiplier, each pattern
        and guarantee multiplier, a loan on an exhausted account taking the account
        entering a month below 0 and deciding the guarantee test, and each floor and cap of
        S's by the raw value it bounds, never the bounded output, which equals the bound
        where the bound changes nothing too.

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
        schedules = _surr_charges_with_gul10(pd.read_csv(
            model_path(TWIN).parent / "surr_charge_table.csv"))["surr_charge_id"]
        classes = pd.read_csv(model_path(TWIN).parent / "class_factor_table.csv")[
            "rate_class"]
        frame = 12 * (spliced[0].Projection.charges_cease_age)

        def at(p, column):
            return s_table.at[p, column]

        def month(p, d):
            return int(at(p, "duration_mth")) + d

        splices = {
            **{f"{pattern} premiums": (
                lambda k, p, d, x=pattern: at(p, "premium_type") == x)
               for pattern in ("LEVEL", "SINGLE", "TEN_PAY")},
            **{f"mode {m}": (
                lambda k, p, d, m=m: at(p, "premium_mode") == m
                and at(p, "premium_type") != "SINGLE")
               for m in "ASQM"},
            **{f"sex {x}": (lambda k, p, d, x=x: at(p, "sex") == x) for x in "MF"},
            **{f"class {c}": (lambda k, p, d, c=c: at(p, "rate_class") == c)
               for c in classes},
            **{f"schedule {i}": (
                lambda k, p, d, i=i: bool(at(p, "has_surr_charge"))
                and at(p, "surr_charge_id") == i)
               for i in schedules},
            "no surrender charge": lambda k, p, d: not at(p, "has_surr_charge"),
            "the endorsement": lambda k, p, d: bool(at(p, "rop_elected")),
            "no endorsement": lambda k, p, d: not at(p, "rop_elected"),
            **{f"a guarantee to {a}": (lambda k, p, d, a=a: at(p, "guarantee_age") == a)
               for a in (121, 90, 99, 100)},
            **{f"issue age {a}": (lambda k, p, d, a=a: at(p, "age_at_entry") == a)
               for a in (60, 40)},
            "withdrawals": lambda k, p, d: at(p, "wd_pp") > 0.0,
            "a loan": lambda k, p, d: at(p, "loan_bal_init") > 0.0,
            "both pins": lambda k, p, d: (not pd.isna(at(p, "prem_persistency_override"))
                                          and not pd.isna(at(p, "coi_rate_dp"))),
            "the persistency pin alone": lambda k, p, d: (
                not pd.isna(at(p, "prem_persistency_override"))
                and pd.isna(at(p, "coi_rate_dp"))),
            "the precision pin alone": lambda k, p, d: (
                pd.isna(at(p, "prem_persistency_override"))
                and not pd.isna(at(p, "coi_rate_dp"))),
            "S's in-force point as its twin": lambda k, p, d: (
                k == "twin" and at(p, "duration_mth") > 0),
            "S's own in-force point as its twin, the worked example's": lambda k, p, d: (
                k == "twin" and p in IN_FORCE),
            "S's in-force point restated": lambda k, p, d: (
                k == "derived" and at(p, "duration_mth") > 0),
            "a variant issued at the valuation date as its twin": lambda k, p, d: (
                k == "twin" and p in VARIANTS and at(p, "duration_mth") == 0),
            "the first month after issue": lambda k, p, d: month(p, d) == 1,
            "mid-year": lambda k, p, d: month(p, d) % 12 not in (0, 11),
            "the month before an anniversary": lambda k, p, d: month(p, d) % 12 == 11,
            "on an anniversary": lambda k, p, d: month(p, d) > 0 and month(p, d) % 12 == 0,
            "the last covered month": lambda k, p, d: (
                month(p, d) == frame - 12 * int(at(p, "age_at_entry")) - 1),
        }
        futures = {
            "issued within a year": lambda p, k: k < 12,
            "issued more than a year on": lambda p, k: k > 12,
            "issued more than two years on, as the committed future row": lambda p, k: (
                k > 24),
            "a single premium": lambda p, k: at(p, "premium_type") == "SINGLE",
            "ten-pay": lambda p, k: at(p, "premium_type") == "TEN_PAY",
            "a pin": lambda p, k: not pd.isna(at(p, "coi_rate_dp")),
        }
        missing = [what for what, holds in splices.items()
                   if not any(holds(*case) for case in CORE_SPLICES)]
        missing += [what for what, holds in futures.items()
                    if not any(holds(*case) for case in CORE_FUTURES)]
        issued = ({p for k, p, d in CORE_SPLICES if (k, p, d) in VARIANT_TWINS}
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

    def test_the_points_sum_row_by_row_into_a_block(self, spliced):
        """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

        S point 2's twin, the point restated at month 12 and the point issued a month on,
        summed as ``run_sec.py --block`` sums them, are indexed 0..732 and equal S's frame
        added to itself moved 12 months earlier and a month later, with no tolerance
        beyond 1e-9 relative.  A model whose frames sat on the policy clock would fail it.
        """
        s, sec = spliced
        keys = [_row_key(sec, *case)
                for case in (("twin", 2, 0), ("derived", 2, 12), ("future", 2, -1))]
        try:
            frames = [projection(sec, key).result_cf() for key in keys]
        finally:
            for key in keys:
                _release(sec, key)
        block = pd.concat(frames).groupby(level="t").sum()
        sdf = _point(s, 2).result_cf()
        expected = pd.concat([sdf, sdf.set_axis(sdf.index - 12).loc[0:],
                              sdf.set_axis(sdf.index + 1)]).groupby(level=0).sum()
        assert list(block.index) == list(range(733))
        assert frame_mismatches(expected, block, atol=0.0) == []

    def test_every_state_s_reaches_is_accepted_in_force(self, spliced, tmp_path):
        """Every state the splice's S reaches is a valid opening state, but one (T5).

        ``Data``'s rules and ``proj_len()``'s hold an opening state to what a policy in
        force can hold, so they must accept each state ``ULSG_US_S`` reaches: a rule
        exercised only on the rows the other tests choose could refuse a state S reaches
        elsewhere (D6).  So every S point of the splice, S's four and the variants, under
        the splice's References and swept, is restated in force by the generator at the
        edges of its windows, or with ``USLIB_SEC_FULL=1`` at every month of its frame, each
        before its lapse (:func:`_every_state_months`), into one table beside the twins:
        ``Data`` reads it, and no row's ``proj_len()`` refuses it
        (:func:`_refused_in_force`).  But for one state, set aside first: an account value
        below 0, which ``ULSG_US_S`` carries under a loan on an exhausted account, as on
        variant 15 from its month 4, and ``Data`` refuses by name, since no policy in force
        holds one.  It is the only state set aside, every one of them variant 15's, and a
        table holding one is refused, naming the point and saying what to do.
        """
        s = spliced[0]
        kept, below = _states_s_reaches(s)
        assert below and {point for point, _ in below} == {15}, below[:5]
        assert len(kept) > 1000, len(kept)
        refused = _refused_in_force(s, kept, tmp_path / "every", SPLICED_REFS)
        assert not refused, f"{len(refused)} refused, first: {refused[:5]}"
        folder = _spliced_folder(tmp_path / "below", s, below[:1], ())
        label = _label(pd.read_csv(folder.parent / TABLE, index_col="point_id"),
                       "derived", *below[0])
        model = _read(folder, "below", SPLICED_REFS)
        try:
            _refused_exactly(model.Data.model_point_table, _AV_NUMBER.format(
                point=label).format(file=TABLE))
        finally:
            model.close()


# ---------------------------------------------------------------------------
# The second splice: the bounds ULSG_US_S ships idle
#
# Two of ULSG_US_S's bounds bind on no row at its shipped References or the splice's: the
# lapse rate's cap of 0.5, which the largest raw annual rate on the main grid, 0.04, in
# the first policy year of S's point 4, whose guarantee to 90 leaves the multiplier at 1,
# never meets, and the credited rate's floor at the guaranteed 2%, under a declared rate of
# 3.5%.  A second pair of models, read with References of their own (IDLE_REFS), binds
# both, with a core and a reach assertion of its own (USLIB-SEC-PLAN.md §7.11, Switches
# and bounds S ships idle).
# At a cap of 0.0125 the lapse rate is capped, with an effect, in the first three policy
# years of a level lifetime payer, 0.022, 0.0165 and 0.01375, and of ten-pay, 0.04 x 0.55
# x 0.8 = 0.0176; and the value sits strictly apart from every bound and rate it could be
# read as: the floor 0.003, the table's rates 0.0075 to 0.04, and the 0.01 of years 11 to
# 20.  A declared rate of 1.5% puts the floor, the 2% guarantee, in every month, apart from
# the loan's credited 3% and from 0.  ULSG has no Reference-level switch S ships off, so T1
# runs under no switch.
IDLE_REFS = {**SPLICED_REFS, "lapse_rate_cap": 0.0125, "crediting_rate_curr": 0.015}
IDLE_VARIANTS = {p: VARIANTS[p] for p in (5, 7)}
IDLE_SPLICES = (("twin", 1, 0), ("twin", 7, 0), ("derived", 2, 12), ("derived", 2, 121),
                ("derived", 5, 12))
IDLE_FUTURES = ((2, 13),)
IDLE_GRID = (*IDLE_SPLICES, *(("future", p, -k) for p, k in IDLE_FUTURES))
CORE_IDLE = {("derived", 2, 12): "the lapse cap binding in policy years 2 and 3",
             ("twin", 7, 0): "the credited rate's floor under a loan",
             ("future", 2, -13): "both bounds from the issue month"}


@pytest.fixture(scope="class")
def idle_spliced(tmp_path_factory):
    """S and SEC on the splice's inputs, with :data:`IDLE_REFS` set in both.

    S's four points and variants 5 and 7, and the rows this run selects of
    :data:`IDLE_SPLICES` and :data:`IDLE_FUTURES`, the :data:`CORE_IDLE` or all of them
    (:func:`_splice`).  Scoped to its class, whose tests alone read it, and frozen once S is
    swept, as the main splice's fixture is.
    """
    s, sec = _splice(tmp_path_factory.mktemp("idle"), "idle", IDLE_REFS, IDLE_VARIANTS,
                     IDLE_SPLICES, IDLE_FUTURES, frozenset(CORE_IDLE))
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


def _idle_reach(x):
    """Which of the two idle bounds bind on row ``x``, each by the raw value it bounds."""
    months = range(x.t_entry(), x.proj_len())
    floor = x.guar_rate_mth()
    return {
        "the lapse rate's cap": any(_lapse_raw(x, t) > x.lapse_rate_cap
                                    and x.pols_lapse(t) > 0.0 for t in months),
        "the credited rate's floor": any(
            (1 + x.crediting_rate_ann(t)) ** (1 / 12) - 1 < floor
            and x.inv_return_mth(t) == floor and x.inv_income_pp(t) != 0.0
            for t in months)}


class TestTheIdleBounds:
    """The second splice, where each bound ULSG_US_S ships idle binds in both models."""

    @pytest.mark.parametrize(
        "kind, s_point, month",
        [_case(case, CORE_IDLE, _case_id(*case)) for case in IDLE_GRID])
    def test_a_bound_s_ships_idle_binds_in_both_models(self, idle_spliced, idle_records,
                                                       idle_bounds, kind, s_point, month):
        """With the lapse cap and the credited floor binding, each row is S from its month.

        T2's comparison on the restated rows and the in-force twins, and T3's on the row
        issued 13 months on, each at 1e-9 relative with no absolute floor, every cell of
        S's but T2's or T3's exemptions: a bound left out, or written in another order, or
        read in another month, parts the two.  What each row binds is recorded, by the raw
        value each bound bounds (:func:`_idle_reach`) and by the sides of each ``min`` and
        ``max`` its comparison binds (:class:`_BoundSides`), and the row released.
        """
        s, sec = idle_spliced
        case = (kind, s_point, month)
        key = _row_key(sec, *case)
        exempt, arg_map = {"twin": (TWIN_EXEMPT, None),
                           "derived": (SPLICE_EXEMPT, None),
                           "future": (FUTURE_EXEMPT, _issued_later)}[kind]
        try:
            with idle_bounds.watch() as won:
                sec_proj = projection(sec, key)
                found = _continues_s(_point(s, s_point), sec_proj, month, exempt, arg_map)
                idle_records[case] = {"reach": _idle_reach(sec_proj), "bounds": won}
            assert found == []
        finally:
            _release(sec, key)

    def test_the_idle_core_reaches_each_bound(self, idle_spliced, idle_records,
                                              idle_bounds):
        """Each idle bound binds with an effect on some row of the second splice's core.

        The lapse rate's cap, where the raw product of S's four factors passes
        ``lapse_rate_cap`` in a month with lapses, and the credited rate's floor, where the
        declared rate's monthly rate is below the guaranteed one, the account is credited at
        the guarantee, and its credit is not 0: each by the raw value it bounds, never the
        bounded output, and by the side of its ``min`` or ``max`` that wins there, the two
        sides :data:`BOUND_ELSEWHERE` names this test for (:class:`_BoundSides`).  A row no
        case has recorded is read here.
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
        assert reached == {"the lapse rate's cap", "the credited rate's floor"}, reached
        mine = _sides_bound_by("test_the_idle_core_reaches_each_bound")
        assert len(mine) == 2
        if sys.version_info >= (3, 11):
            assert mine <= won, sorted(mine - won)

    def test_every_state_its_s_reaches_is_accepted_in_force(self, idle_spliced, tmp_path):
        """Under the second splice's References too, every state S reaches is accepted.

        As on the main splice, at the second splice's References, the declared rate below
        the guarantee and the lapse rate capped: every state of S's four points and variants
        5 and 7 at the edges of their windows, or at every month with ``USLIB_SEC_FULL=1``,
        before each lapse, restated in force by the generator, is read by ``Data`` and has a
        frame (:func:`_refused_in_force`).  None is an account value below 0 here: variant
        7's loan is credited at 3%, above the declared rate's floor of 2%, so its account
        never runs below 0.
        """
        s = idle_spliced[0]
        kept, below = _states_s_reaches(s)
        assert not below and len(kept) > 300, (below[:5], len(kept))
        refused = _refused_in_force(s, kept, tmp_path / "every", IDLE_REFS)
        assert not refused, f"{len(refused)} refused, first: {refused[:5]}"


# ---------------------------------------------------------------------------
# The tests that read models of their own
#
# Each test below reads, and closes, the models it needs, and none asks for the
# committed model or S, the module's fixtures: so they run once the splices' models
# are closed and before those are first read, and none of the models they read sits in
# memory beside them (USLIB-SEC-PLAN.md §7.7, Record — M9, Memory).  The tests that
# read the committed fixtures follow them.


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
# proj_len()): issued at the valuation date at age 18, and 120 months on.
LONGEST_FRAMES = ((0, 0, 1236), (-120, 120, 1356))


def _longest_cover(tmp_path):
    """A copy whose table holds S point 3 at issue age 18, issued now and 120 months on.

    ``ULSG_US_S``'s frame from issue is ``12 * (charges_cease_age - issue age)`` months,
    and the product spec issues from age 18, so the longest cover is 1,236 months, and the
    longest frame that issued 120 months on, the shipped ``future_horizon_mth``, 1,356
    months, whose chains stop at ``t_entry()``.  The second row takes its own label before
    its duration is written, so that the edit lands on it alone, and the test asserts both
    frames (:data:`LONGEST_FRAMES`).  The copy's COI table gains the anchor cell's rows at
    ages 18 to 44, and its mortality table the same ages, each geometric in the age, so
    that an age read for another changes a number; the corridor table starts at 18
    already.
    """
    committed = _committed()
    now, later = _label(committed, "twin", 3, 0), _label(committed, "future", 2, -25)
    table = committed.loc[[now, now]].assign(age_at_entry=18)
    table.index = pd.Index([now, later], name="point_id")
    table = _set("duration_mth", [later], -120)(table)
    table = table.assign(policy_id=[f"{committed.at[now, 'policy_id']}-A18",
                                    f"{committed.at[now, 'policy_id']}-A18F120"])

    def coi(rates):
        ages = range(18, 45)
        young = pd.DataFrame({
            "sex": "M", "rate_class": "StdNT", "age": list(ages),
            "coi_rate_guar_ann": [round(0.6 * 1.09 ** (a - 18), 6) for a in ages],
            "provenance": "test copy"})
        return pd.concat([young, rates], ignore_index=True).sort_values(
            COI_KEYS, ignore_index=True)

    def mort(rates):
        ages = range(18, 45)
        young = pd.DataFrame({"age": list(ages),
                              "mort_rate": [round(0.0004 * 1.08 ** (a - 18), 6)
                                            for a in ages],
                              "provenance": "test copy"})
        return pd.concat([young, rates], ignore_index=True)

    return _sec_inputs(tmp_path, table, edits={"coi_rates.csv": coi,
                                               "mort_table.csv": mort}), (now, later)


# Each chain of the model and the cell that heads it, called cold at the last month the
# chain reaches: (cell, its month as months from proj_len(), its other arguments, the
# chain's own recursive cells): the loan, the premiums paid, the account value, the shadow
# account, the grace counter with its latch, and the count.  Each head is called alone, on
# a read of its own, with every chain cold, which is checked (USLIB-SEC-PLAN.md §7.3,
# Record — M3, Chains, precised at M9): a head that reads other chains runs deepest only
# while those are cold too, the account value reading the loan, the shadow account the
# account value through the death benefit, the grace counter both accounts, and the count
# the latch.  The account value's opening timing, the latch and the count are carried into
# t = proj_len(), so their heads are read there.
CHAIN_HEADS = (("loan_bal_pp_at", -1, ("BEF_INT",), ("loan_bal_pp_at",)),
               ("cum_prem_pp", -1, (), ("cum_prem_pp",)),
               ("av_pp_at", 0, ("BEF_PREM",), ("av_pp_at",)),
               ("sg_pp_at", -1, ("BEF_PREM",), ("sg_pp_at",)),
               ("is_lapsed", 0, (), ("is_lapsed", "grace_mth")),
               ("pols_if_at", 0, ("BEF_NB",), ("pols_if_at",)))


def _chains_cold(folder, labels, refs):
    """The cold depths of :data:`CHAIN_HEADS` on ``labels`` of the model in ``folder``.

    Each head on a read of its own, with ``refs`` set first, so that every chain is cold
    when it is called, which is checked first: a head called after another on one read
    would find that one's chain warm, and run shallower than it can.  Each chain runs back
    to ``t_entry()``.  Returns the findings.  The points it reads must never lapse, since
    once the latch is shut the count returns 0.0 before it recurses, which the count's read
    checks, the latch being cached there.
    """
    chains = [name for *_, chain in CHAIN_HEADS for name in chain]
    found = []
    for label in labels:
        for cell, offset, rest, chain in CHAIN_HEADS:
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
                if cell == "pols_if_at":
                    assert not p.is_lapsed(end), (
                        f"point {label} lapses, so its count is no chain")
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


def _improvement_cold(folder, labels):
    """The cold depth of the improvement factor, a chain of one cell a year, on each point.

    One fresh read a month: 252, the first month whose factor has stopped growing, which
    reads the factor at 240, its deepest; and the point's last month.  Its chain is the
    valuation years it multiplies, at most ``mort_improve_max_years``, and it may run
    :data:`IMPROVEMENT_OVERHEAD` cells beyond them.
    """
    found = []
    for label in labels:
        for which in ("the factor's deepest", "the last month"):
            fresh = _read(folder, "improvement")
            try:
                p = _point(fresh, label)
                t = 252 if which == "the factor's deepest" else p.proj_len() - 1
                years = min(t // 12, p.mort_improve_max_years)
                found += _one_cell_a_month(
                    label, _cold_depth(p, "mort_improve_factor", (t,)), years,
                    f"mort_improve_factor({t})", IMPROVEMENT_OVERHEAD)
            finally:
                fresh.close()
    return found


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
    pytest.param("longest cover", id="longest"),
    pytest.param("ascending at the longest cover", id="longest-ascending",
                 marks=FULL_ONLY)])
def test_every_chain_runs_one_cell_a_month_from_a_cold_start(tmp_path, case):
    """Called cold, each chain runs one cell a month back to its base, no more (D5, R2).

    No number shows how deep a chain runs, and a compiled model runs it on the C stack, so
    a chain of two cells a month, which gives the same numbers, needs twice the stack on
    every platform (F7).  ``ULSG_US_S``'s account value and shadow account ran through six
    cells a month and its loan through two; here each forms the previous month's close
    itself.  On a model just read, nothing is cached, so modelx's stack trace counts how
    deep a call runs, against one cell a month and :data:`CHAIN_OVERHEAD` more:

    * ``shipped``, at the shipped References: on the twins of S's points 1 and 3, the row
      issued 25 months on and the row of S point 1 at 81, whose cold call runs the deepest
      of the committed points, 18 above its chain, ``net_cf`` in the last month, each on a
      read of its own, the deepest call a projection makes, down the account value's chain
      to ``t_entry()``; then, on S point 3's twin, the one committed row that never lapses
      and so the one whose count runs its whole chain, each of :data:`CHAIN_HEADS` alone,
      each on a read of its own, its own chain checked cold, so the chains a ``net_cf``
      call reaches from the side are measured too, each while every other is cold; and the
      improvement factor, a chain of one cell a year, at most ``mort_improve_max_years``
      years plus :data:`IMPROVEMENT_OVERHEAD` cells deep, however long the frame.
    * ``longest cover``: at the contract's longest cover, issue age 18, issued now and 120
      months on (:func:`_longest_cover`), each row's frame asserted first
      (:data:`LONGEST_FRAMES`), ``net_cf`` in the last month and each of
      :data:`CHAIN_HEADS` alone, each on a read of its own: the deepest cold calls the
      contract allows, which are what bound the stack, the first month of the later row
      reading the improvement factor of the ten valuation years before its issue cold, and
      where a level Phase 2 adds below each table's reader would first pass
      :data:`CHAIN_OVERHEAD` (USLIB-SEC-PLAN.md §7.1, *Record — M14*, *Carried into Phase
      1*).
    * ``ascending at the longest cover``, with the full grid: both rows swept in ascending
      ``t`` under :data:`CALL_DEPTH`, as the committed points are.
    """
    committed = _committed()
    found = []
    if case == "shipped":
        labels = [_label(committed, "twin", p, 0) for p in (1, 3)]
        labels.append(_label(committed, "future", 2, -25))
        deepest = _label(committed, "derived", 1, 81)
        found += _net_cf_cold(model_path(SEC), [*labels, deepest], {})
        found += _chains_cold(model_path(SEC), [labels[1]], {})
        found += _improvement_cold(model_path(SEC), labels[1:])
    else:
        folder, labels = _longest_cover(tmp_path)
        model = _read(folder, "longest")
        try:
            frames = [(p.duration_mth_init(), p.t_entry(), p.proj_len())
                      for p in (_point(model, label) for label in labels)]
        finally:
            model.close()
        assert tuple(frames) == LONGEST_FRAMES, frames
        if case == "longest cover":
            found += _net_cf_cold(folder, labels, {})
            found += _chains_cold(folder, labels, {})
        else:
            found += _ascending(folder, dict.fromkeys(labels, CALL_DEPTH))
    assert not found, found


# ---------------------------------------------------------------------------
# T4 -- the count's scale


# The References the scaling test sets in both copies: the splice's, which switch on the one
# assumption that ships at zero, the premium tax, with expense inflation and mortality
# improvement at their shipped values, which scaling leaves alone (USLIB-SEC-PLAN.md §5.2,
# T4).
SWITCHED_ON = {**SPLICED_REFS, "inflation_rate": INFLATION,
               "mort_improve_rate_init": IMPROVEMENT}

# The counted cells, and report columns, that are differences of products of the count:
# each side scales by the factor rounded its own way, so where the two sides nearly cancel
# the difference keeps their rounding, which is relative to the sides, not to it.  These
# are held to 1e-12 of their largest magnitude on the point; every other counted value to
# 1e-12 relative, value by value.
DIFFERENCES = frozenset({"av_change", "net_cf", "margin_expense", "margin_mortality"})
REPORT_DIFFERENCES = {"result_cf": ("net_cf",)}
# The per-policy columns of the reports: the rates of result_pols, every column of
# result_guar but the deductions forgone in force, and the whole of result_av.
PER_POLICY = {"result_pols": RATES,
              "result_guar": ("net_amt_at_risk", "coi_pp", "sg_net_amt_at_risk",
                              "sg_coi_pp", "sg_net_pp", "is_guar_active",
                              "catch_up_prem_pp", "grace_mth")}


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

    Two copies of the committed table and one row of the test's own, the twin of S's point
    1 with an account value of $400,000, a loan of $50,000, $500 a month of withdrawals and
    neither pin, so that the loan, the withdrawals and their fees flow, the second copy
    with every count :data:`COUNT_FACTOR` times the first's, are read with
    :data:`SWITCHED_ON` set first: the premium tax switched on, so that every flow is
    nonzero on some point, with inflation and improvement on.  A factor that is not whole
    sees a count truncated to whole policies, and a flow left at zero sees no count at
    all.  Point by point, each released once compared:

    * every counted column of the four reports is 2.5 times the first's, to 1e-12 relative,
      value by value, a difference of products (``net_cf``) to 1e-12 of its peak;
    * every cell of :data:`COUNTED` at every key the first's sweep cached is 2.5 times the
      first's, value by value (:func:`_scaled_faults`);
    * ``result_pols``' rates, ``result_guar``'s columns but the deductions forgone in force
      and the whole of ``result_av``, the roll-forwards per policy, are the first's
      exactly;
    * every other cell is the first's exactly, at every key, but the three residuals, which
      are relative and move in the last digits; and the three checks hold on both;

    and every cell of :data:`COUNTED` but ``pols_maturity`` is nonzero on some point.
    """
    committed = _committed()
    funded = committed.loc[[_label(committed, "twin", 1, 0)]].assign(
        av_pp_init=400000.0, loan_bal_init=50000.0, wd_pp=500.0,
        prem_persistency_override=float("nan"), coi_rate_dp=float("nan"),
        policy_id="GUL-000001-T4")
    funded.index = pd.Index([committed.index.max() + 1], name="point_id")
    base_table = pd.concat([committed, funded])
    models = {}
    try:
        for tag, factor in (("one", 1.0), ("scaled", COUNT_FACTOR)):
            table = base_table.assign(policy_count=factor * base_table["policy_count"])
            models[tag] = _read(_sec_inputs(tmp_path / tag, table), tag, SWITCHED_ON)
        one, scaled = models["one"], models["scaled"]
        faults, nonzero = [], set()
        for key, two_key, point_id in zip(point_keys(one), point_keys(scaled),
                                          base_table.index):
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
            assert tuple(base.cells[c]() for c in CHECKS) + tuple(
                two.cells[c]() for c in CHECKS) == (True,) * 6, point_id
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
# coerce the column to numbers, so each is refused as a count, a duration, an age, an
# amount, a share or a balance that is not a number, and a share, the premium load or the
# persistency pin, past 1 as well as below 0.  The repeated point_id holds another policy
# under the same label, as a bad extract would, so that the check must look at the labels
# and not at whole rows.  The point_ids are the committed table's: 1, S's point 1 in force
# at 300 with both pins; 2 to 4, S's new business; 5, S point 1 at 381, a month into its
# grace, its shadow account below 0; 6, S point 2 at 240; 7, S point 2 at 305; 8, S point
# 3 at 731; 9, S point 2 issued 25 months on.  Each case is refused by its own rule alone,
# or, where a case pins a rule's place, by its rule first, on a row a later rule would
# refuse differently: a fractional duration on the future row, which the horizon would
# refuse; and a state column that is not a number, or below 0, on a row not yet in force,
# which the rule that holds the state there at 0 would refuse.  A flag is True or False in
# any case, as pandas reads those words, and nothing else: the life chassis keeps S's
# bool(), which reads "0" or "0.0" in a column made text by one such cell as true, so 1,
# 0, 1.0 and 0.0 are refused, as a blank and any other text are (USLIB-SEC-PLAN.md §7.8,
# Record — M10, Flag spellings); a TRUE beside the bad cell, which the column's text keeps
# as written, is still a flag, so the message names the bad cell's point alone; and the
# spellings accepted are read in a test of their own.
# A {file} in a message is the table's filename: every case is read from a file of its own
# (the malformed fixture).

_NUMBER = ("{{file}}: {column} must be a number, zero or more; it is not at point_id "
           "[{point}]")
_AV_NUMBER = ("{{file}}: av_pp_init must be a number, zero or more: no policy in force "
              "holds a negative account value, so restate a point with a loan on an "
              "exhausted account no later than the last month its account value is still "
              "zero or more; it is not at point_id [{point}]")
_SG_NUMBER = "{{file}}: sg_pp_init must be a number; it is not at point_id [{point}]"
_GRACE = ("{{file}}: grace_mth_init must be a whole number of months, 0 or more; it is not "
          "at point_id [{point}]")
_NOT_IN_FORCE = ("{{file}}: {column} must be 0 on a policy not yet in force, duration_mth "
                 "0 or less; it is not at point_id [{point}]")
_YEARS = ("{{file}}: {column} must be a whole number of years, 0 or more; it is not at "
          "point_id [{point}]")
_FACE = ("{{file}}: sum_assured must be a number above 0, the face, which every policy "
         "holds; it is not at point_id [{point}]")
_LOAD = ("{{file}}: load_prem_rate must be a number from 0 to 1; it is not at point_id "
         "[{point}]")
_OVERRIDE = ("{{file}}: prem_persistency_override must be blank or a number from 0 to 1; "
             "it is not at point_id [{point}]")
_DP = ("{{file}}: coi_rate_dp must be blank or a whole number, 0 or more; it is not at "
       "point_id [{point}]")
_FLAG = "{{file}}: {column} must be True or False; it is not at point_id [{point}]"
_INT64 = ("{{file}}: {column} must be below 2**53 in size, where an int64 holds it; it is "
          "not at point_id [{point}]")

# The columns Data reads, each refused when the table lacks it.
READ_COLUMNS = ("policy_count", "duration_mth", "age_at_entry", "sum_assured",
                "guarantee_age", "premium_pp_ann", "wd_pp", "load_prem_rate", *PINS,
                "has_surr_charge", "rop_elected", *STATE)

MALFORMED = [
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in READ_COLUMNS],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[4]].assign(policy_id="GUL-900099")]),
     "{file}: point_id [4] appears more than once"),
    *[(f"a {what} count", _set("policy_count", [point], value),
       _NUMBER.format(column="policy_count", point=point))
      for what, point, value in (("negative", 4, -0.1), ("blank", 5, float("nan")),
                                 ("text", 6, "abc"), ("infinite", 6, float("inf")))],
    ("two bad counts", _set("policy_count", [4, 6], -1.0),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [4, 6]"),
    ("a fractional duration on the future row", _set("duration_mth", [9], -120.5),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [9]"),
    ("a blank duration", _set("duration_mth", [9], float("nan")),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [9]"),
    ("a text duration", _set("duration_mth", [6], "x240"),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [6]"),
    ("issued beyond the horizon", _set("duration_mth", [9], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [9]"),
    *[(f"an {column} {what}", _set(column, [point], value),
       _YEARS.format(column=column, point=point))
      for column, point in (("age_at_entry", 5), ("guarantee_age", 4))
      for what, value in (("of 60.5", 60.5), ("below 0", -1), ("as text", "60y"),
                          ("blank", float("nan")))],
    *[(f"a {what} face", _set("sum_assured", [point], value), _FACE.format(point=point))
      for what, point, value in (("blank", 3, float("nan")), ("blank, in force,", 5,
                                                              float("nan")),
                                 ("zero", 1, 0.0), ("text", 9, "500k"),
                                 ("infinite", 2, float("inf")))],
    *[(f"a {what} {column}", _set(column, [point], value),
       _NUMBER.format(column=column, point=point))
      for what, column, point, value in (
          ("text", "premium_pp_ann", 4, "x"), ("blank", "premium_pp_ann", 3, float("nan")),
          ("negative", "premium_pp_ann", 2, -1.0), ("text", "wd_pp", 2, "a lot"),
          ("infinite", "wd_pp", 8, float("inf")), ("negative", "wd_pp", 6, -1.0))],
    *[(f"a load_prem_rate {what}", _set("load_prem_rate", [point], value),
       _LOAD.format(point=point))
      for what, point, value in (("infinite", 6, float("inf")), ("below 0", 2, -0.1),
                                 ("above 1", 3, 1.5), ("blank", 5, float("nan")),
                                 ("as text", 7, "25%"))],
    *[(f"a prem_persistency_override {what}",
       _set("prem_persistency_override", [point], value), _OVERRIDE.format(point=point))
      for what, point, value in (("below 0", 1, -0.1), ("above 1", 1, 1.5),
                                 ("as text", 1, "0.98x"), ("infinite", 1, float("inf")),
                                 ("above 1 on the future row", 9, 1.5))],
    *[(f"a coi_rate_dp {what}", _set("coi_rate_dp", [point], value),
       _DP.format(point=point))
      for what, point, value in (("of 2.5", 1, 2.5), ("below 0", 1, -1),
                                 ("as text", 1, "2dp"), ("infinite", 1, float("inf")),
                                 ("of 2.5 on the future row", 9, 2.5))],
    *[(f"{column} {what}", _set(column, [point], value),
       _FLAG.format(column=column, point=point))
      for column, point in (("has_surr_charge", 3), ("rop_elected", 4))
      for what, value in (("blank", float("nan")), ("x", "x"), ("Yes", "Yes"), ("1", 1),
                          ("0", 0), ("1.0", 1.0), ("0.0", 0.0))],
    ("has_surr_charge x beside one written TRUE",
     _both(_set("has_surr_charge", [3], "x"), _set("has_surr_charge", [5], "TRUE")),
     _FLAG.format(column="has_surr_charge", point=3)),
    *[(f"a {what} av_pp_init", _set("av_pp_init", [point], value),
       _AV_NUMBER.format(point=point))
      for what, point, value in (("negative", 7, -0.01), ("blank", 6, float("nan")),
                                 ("text", 5, "x"), ("infinite", 6, float("inf")),
                                 ("negative, on the future row,", 9, -0.01))],
    *[(f"a {what} sg_pp_init", _set("sg_pp_init", [point], value),
       _SG_NUMBER.format(point=point))
      for what, point, value in (("infinite", 6, float("inf")), ("blank", 7, float("nan")),
                                 ("text", 5, "x"), ("negative infinite", 5, -float("inf")),
                                 ("text, issued at the valuation date,", 3, "x"))],
    *[(f"a {what} {column}", _set(column, [point], value),
       _NUMBER.format(column=column, point=point))
      for what, column, point, value in (
          ("negative", "loan_bal_init", 6, -0.01), ("text", "loan_bal_init", 7, "x"),
          ("infinite", "loan_bal_init", 5, float("inf")),
          ("negative, on the future row,", "loan_bal_init", 9, -0.01),
          ("negative", "cum_prem_init", 5, -0.01),
          ("blank", "cum_prem_init", 6, float("nan")),
          ("blank, on the future row,", "cum_prem_init", 9, float("nan")))],
    *[(f"a grace_mth_init {what}", _set("grace_mth_init", [point], value),
       _GRACE.format(point=point))
      for what, point, value in (("below 0", 5, -1), ("of 0.5", 5, 0.5),
                                 ("blank", 6, float("nan")), ("as text", 7, "one"),
                                 ("of 0.5 on the future row", 9, 0.5))],
    *[(f"{column} before issue", _set(column, [point], value),
       _NOT_IN_FORCE.format(column=column, point=point))
      for column, point, value in (
          ("av_pp_init", 3, 100.0), ("sg_pp_init", 9, -50.0), ("loan_bal_init", 9, 10.0),
          ("cum_prem_init", 2, 10800.0), ("grace_mth_init", 9, 1))],
    # Stage EC's rule, asked last: each whole number Data hands Projection as an int64,
    # below 2**53, where a float holds every whole number exactly, so that its int64 is the
    # number read (USLIB-SEC-PLAN.md §7.1, Record — M14, item 4).  Each value passes every
    # rule before it, on a point in force where a state column is one.
    *[(f"{column} of 2**53", _set(column, [point], 2.0 ** 53),
       _INT64.format(column=column, point=point))
      for column, point in (("age_at_entry", 4), ("guarantee_age", 4), ("duration_mth", 6),
                            ("grace_mth_init", 5), ("coi_rate_dp", 1))],
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


# Each assumption table, with one fault in its key column, as an extract or an edit by hand
# can leave it: a blank key, which pandas reads as a missing value, a key written as text,
# a fractional one, keys that repeat or leave a gap, a first year missing or one below the
# fixed first year, and no row at all.  The blank is the case that matters most: ULSG_US_S's
# readers take a table's extent from the key column as pandas reads it, where a blank last
# key is a missing value the extent skips, so the table is cut short and every later key
# reads the last good row without a word.  Here each table is checked once, in the Data
# cell its reader asks first, and refused naming the file and the column: the lines a key
# that is blank, text or fractional is on, and each key that repeats or falls below its
# first, with its lines, and each that is missing.  The return-of-premium table, read by
# membership, takes the cases its own key rule refuses: an anniversary that is not a whole
# number of years, 1 or more, or that repeats.  Each case is (case, the file, its edit, the
# Data cell that checks it, the message), and the message is matched whole.  The lines
# count the header as line 1: the policy year y of the lapse table is on line y + 1, and
# the age a of the corridor table on line a - 16, of the mortality table on line a - 43 and
# of the COI table's anchor cell on line a - 43.
_WHOLE = "{file}: {column} must be a whole number; it is not on line {lines}"
_RUNS = {"policy_year": ("{file}: the policy years must run from 1, one row a year, "
                         "without a gap or a repeat; "),
         "age": "{file}: the ages must run one row an age, without a gap or a repeat; "}
_COI_RUN = ("coi_rates.csv: the ages of each sex and rate_class must run one row an age, "
            "without a gap or a repeat; ")
_ANNIV = ("rop_table.csv: anniversary must be a whole number of years, 1 or more; it is "
          "not on line [{line}]")


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
    """The COI table with a second cell, F StdNT, the anchor's rows with age 60 left out,
    and the anchor's own age 49 left out too: a gap in each of two cells."""
    anchor = rates[(rates["sex"] == "M") & (rates["rate_class"] == "StdNT")]
    second = anchor[anchor["age"] != 60].assign(sex="F", provenance="test copy")
    return pd.concat([rates[rates["age"] != 49], second], ignore_index=True)


# Each table read at a policy year or an attained age: (its key column, the Data cell that
# checks it, its first key, the row each case edits, which leaves a key before it, and the
# line of its last row).  The lapse table holds the policy years 1 to 21, the corridor
# table the ages 18 to 121 and the mortality table 45 to 120.
KEY_TABLES = {
    "lapse_table.csv": ("policy_year", "lapse_last_year", 1, 4, 22),
    "corridor_factors.csv": ("age", "corridor_age_last", 18, 9, 105),
    "mort_table.csv": ("age", "mort_age_last", 45, 9, 77),
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
           "coi_rates.csv: sex must not be blank; it is on line [78]"),
          ("a blank rate_class", _write_at("rate_class", 3, float("nan")),
           "coi_rates.csv: rate_class must not be blank; it is on line [5]"),
          ("an age written as text", _write_at("age", 4, "49x"),
           _WHOLE.format(file="coi_rates.csv", column="age", lines="[6]")),
          ("a fractional age", _write_at("age", 9, 54.5),
           _WHOLE.format(file="coi_rates.csv", column="age", lines="[11]")),
          ("its last age blank", _write_at("age", -1, float("nan")),
           _WHOLE.format(file="coi_rates.csv", column="age", lines="[78]")),
          ("a repeated age", _repeat_key("age", 9),
           _COI_RUN + "at ('M', 'StdNT'), age 53 is on line [10, 11]; at ('M', 'StdNT'), "
           "no line holds age 54"),
          ("a gap", _drop_rows(4), _COI_RUN + "at ('M', 'StdNT'), no line holds age 49"),
          ("a gap of three ages", _drop_rows(4, 5, 6),
           _COI_RUN + "at ('M', 'StdNT'), no line holds age 49 to 51"),
          ("a gap in each of two cells", _second_coi_cell,
           _COI_RUN + "at ('F', 'StdNT'), no line holds age 60; at ('M', 'StdNT'), no "
           "line holds age 49"))],
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
     "surr_charge_table.csv: each surr_charge_id must have one row; surr_charge_id GUL15 "
     "is on line [2, 3]"),
    *[(f"rop_table.csv: {what}", "rop_table.csv", _write_at("anniversary", row, value),
       "rop_count", _ANNIV.format(line=row + 2))
      for what, row, value in (("a blank anniversary", 0, float("nan")),
                               ("an anniversary written as text", 1, "25y"),
                               ("a fractional anniversary", 0, 20.5),
                               ("an anniversary of 0", 0, 0),
                               ("an anniversary of -1", 1, -1))],
    ("rop_table.csv: a repeated anniversary", "rop_table.csv",
     _repeat_key("anniversary", 1), "rop_count",
     "rop_table.csv: each anniversary must have one row; anniversary 20 is on line [2, 3]"),
    # Stage EC's: an age table is padded from age 0 (the Data docstring), so a negative age,
    # which S's .loc would read, is refused, after every rule before it: each table's ages
    # moved to start at -1, which leaves its run whole (USLIB-SEC-PLAN.md §7.3, *For M17
    # and later*, item 10).
    *[(f"{file}: its ages from -1", file, _shifted("age", -first - 1), check,
       f"{file}: age must be 0 or more; it is not on line [2]")
      for file, first, check in (("corridor_factors.csv", 18, "corridor_age_last"),
                                 ("mort_table.csv", 45, "mort_age_last"),
                                 ("coi_rates.csv", 45, "coi_schedules"))],
]

# Each value a reader reads, blank, written as text and infinite, in every table: the rates
# and factors keyed by a policy year or an age, the COI scale, the class factors, the
# surrender charge and the return-of-premium terms.  ULSG_US_S reads a blank as a missing
# value, which shows in its flows or is lost in a min or a max: a blank corridor factor
# reads as no corridor, a blank surrender charge as none, and a blank lapse rate as the
# floor, through its max written bound first; and this model's capped mortality,
# min(q, 1.0), keeps a blank base rate or class factor missing, where its bound first would
# read it as 1.  Then values outside their range: a lapse or mortality rate, a refund ratio
# or an exercise rate above 1 or below 0, none a probability or a share, and a class
# factor, a guaranteed COI rate or a surrender charge below 0, each of which projects,
# with every check passing, a negative death or charge, or a surrender charge that rises
# once its schedule has run off; and a corridor factor below 0, which no statutory
# percentage is, and which would leave db_pp's floor on the account value the one thing
# between an account below 0 and a death benefit above the face.  Then values no point
# reads, a factor of a class no point carries and rates at ages none reaches, and two
# lines at fault in one column; and the run-off, which must be a whole number of years, 1
# or more, since the model divides by it.
# Each case is as in MALFORMED_KEYS.
_RATE = "{file}: {column} must be {what}; it is not on line {lines}"
# Each value column: (its file, the column, the Data cell that checks it, the row edited,
# its line, what each value must be, the values outside its range).
RATE_COLUMNS = (
    ("lapse_table.csv", "lapse_rate_ann", "lapse_last_year", 4, 6, "a number from 0 to 1",
     (1.2, -0.05)),
    ("corridor_factors.csv", "corridor_factor", "corridor_age_last", 29, 31,
     "a number, zero or more", (-0.5,)),
    ("mort_table.csv", "mort_rate", "mort_age_last", 29, 31, "a number from 0 to 1",
     (1.01, -0.01)),
    ("coi_rates.csv", "coi_rate_guar_ann", "coi_schedules", 9, 11,
     "a number, zero or more", (-1.0,)),
    ("class_factor_table.csv", "factor", "class_count", 3, 5, "a number, zero or more",
     (-0.5,)),
    ("surr_charge_table.csv", "sc_per_1000_init", "surr_charge_count", 0, 2,
     "a number, zero or more", (-18.0,)),
    ("rop_table.csv", "refund_ratio", "rop_count", 0, 2, "a number from 0 to 1",
     (1.5, -0.1)),
    ("rop_table.csv", "exercise_rate", "rop_count", 1, 3, "a number from 0 to 1",
     (1.5, -0.1)),
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
    ("coi_rates.csv: a rate no point reads", "coi_rates.csv",
     _write_at("coi_rate_guar_ann", 0, float("nan")), "coi_schedules",
     _RATE.format(file="coi_rates.csv", column="coi_rate_guar_ann",
                  what="a number, zero or more", lines="[2]")),
    *[(f"surr_charge_table.csv: runoff_years {what}", "surr_charge_table.csv",
       _write_at("runoff_years", 0, value), "surr_charge_count", _RUNOFF)
      for what, value in (("blank", float("nan")), ("written as text", "x"),
                          ("infinite", float("inf")), ("of 7.5", 7.5), ("of 0", 0))],
]


def _table_refused(tmp_path, file, edit, check, message):
    """Data's ``check``, then a projection, refuse the copy whose ``file`` is ``edit``-ed.

    The Data cell is asked first, and with it the first-age cell an age table's reader
    also asks, and then ``net_cf(0)`` of the base ``Projection``'s default point, S's
    worked-example policy in force, which reads every one of these tables: the corridor
    through its death benefit, the mortality table and the class factor through the
    month's deaths, the lapse table through its lapses, the COI scale through the shadow
    account's charge, which the lapses' dynamic multiplier reads, the surrender charge
    through the cash value a lapse is paid, and the return-of-premium table through its
    window, its 25th anniversary, at ``t = 0``.
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
    number of years, 1 or more, by one rule: ``ULSG_US_S`` divides by it.  And so is a
    lapse or mortality rate, a refund ratio or an exercise rate outside 0 to 1, and a class
    factor, a corridor factor, a guaranteed COI rate or a surrender charge below 0, each by
    the one rule that refuses a blank in its column.  ``ULSG_US_S`` reads a blank value as
    a missing one, and so would this model's capped mortality, ``min(q, 1.0)``, which
    written ``min(1.0, q)`` would read one as 1.0, every policy in force dying in that month
    without a word.
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
# rate, a guaranteed COI rate and a corridor factor of 0 at attained age 61, all read by
# S's point 2 in its second and third years; a class factor of 0 for StdNT, every
# committed point's class; a surrender charge of 0 and a run-off of a year on GUL15, every
# point's schedule; and a refund ratio of 0 at the 20th anniversary and an exercise rate of
# 1 at the 25th, the window S's point 1 opens at t = 0.  The shipped mortality table
# reaches 1 at attained age 120, read by the row restated at 731.
AT_BOUNDS = {
    "lapse_table.csv": _both(_write_at("lapse_rate_ann", 1, 0.0),
                             _write_at("lapse_rate_ann", 2, 1.0)),
    "mort_table.csv": _where("mort_rate", "age", 61, 0.0),
    "coi_rates.csv": _where("coi_rate_guar_ann", "age", 61, 0.0),
    "corridor_factors.csv": _where("corridor_factor", "age", 61, 0.0),
    "class_factor_table.csv": _where("factor", "rate_class", "StdNT", 0.0),
    "surr_charge_table.csv": _both(_write_at("sc_per_1000_init", 0, 0.0),
                                   _write_at("runoff_years", 0, 1)),
    "rop_table.csv": _both(_write_at("refund_ratio", 0, 0.0),
                           _write_at("exercise_rate", 1, 1.0)),
}


def test_a_rate_or_factor_at_the_bound_of_its_range_is_read(tmp_path):
    """A rate or a share of 0 or 1, and a factor or a charge of 0, are read (T5).

    The ranges ``Data`` holds the tables to are closed: a lapse or mortality rate, a
    refund ratio and an exercise rate from 0 to 1, and a class factor, a corridor factor, a
    guaranteed COI rate or a surrender charge of 0 or more, and a run-off of 1 year or
    more.  So a copy holding each bound (:data:`AT_BOUNDS`) reads, every extent and count as
    shipped, and the committed points read each value as written: S's point 2 a lapse rate
    of 0 in its second year, floored, and of 1 in its third, capped at 0.5, a mortality
    rate, a COI rate and a corridor factor of 0 at 61, the face its death benefit, and,
    with every point, a class factor and a surrender charge of 0; and S's point 1 every
    policy taking the refund at its 25th anniversary, at ``t = 0``.  Every flow is a finite
    float.
    """
    folder = temp_inputs(tmp_path, model_path(SEC), edits=AT_BOUNDS)
    model = _read(folder, "bounds_read")
    try:
        assert (model.Data.lapse_last_year(), model.Data.mort_age_last(),
                model.Data.corridor_age_last(), model.Data.class_count(),
                model.Data.surr_charge_count(), model.Data.rop_count()) == (
            21, 120, 121, 6, 1, 2)
        p = _row(model, "twin", 2, 0)
        assert (p.lapse_rate_base(12), p.lapse_rate_base(24)) == (0.0, 1.0)
        assert (p.lapse_rate(12), p.lapse_rate(24)) == (p.lapse_rate_floor,
                                                        p.lapse_rate_cap)
        assert (p.mort_rate_base_at(61), p.coi_rate_guar_at(61)) == (0.0, 0.0)
        assert (p.corridor_factor_at(61), p.corridor_factor(12), p.db_pp(12)) == (
            0.0, 0.0, p.sum_assured_at(12))
        assert (p.class_factor(), p.mort_rate(12), p.pols_death(12)) == (0.0, 0.0, 0.0)
        assert (p.surr_charge_rate_max(), p.surr_charge_runoff_years()) == (0.0, 1.0)
        assert p.surr_charge_rate(0) == 0.0 and p.rop_ratio(240) == 0.0
        q = _row(model, "twin", 1, 0)
        assert (q.rop_ratio(0), q.rop_rate(0)) == (1.0, 1.0)
        assert q.pols_rop(0) == q.pols_if(0) - q.pols_death(0) - q.pols_lapse(0) > 0.0
        for x in (p, q):
            flows = x.result_cf().to_numpy().ravel()
            assert all(type(v) is float and math.isfinite(v) for v in flows.tolist())
    finally:
        model.close()


# A text column ULSG_US_S branches on or joins on, holding a value its formulas or its
# tables do not know: the decodes read it as no known value, and the cell that branches on
# it raises ULSG_US_S's own message, on S point 2's twin, a level payer, so that its mode is
# decoded, with one column changed.  Each value a decode or a join names is given in
# another case and with a space before or after it, which S's exact comparisons and its
# .loc do not know (USLIB-SEC-PLAN.md §7.3, *For M17 and later*, item 2): a decode that
# folded case or stripped spaces would project such a point where S refuses it.  A class,
# a sex or a schedule the tables do not know is refused by Data's join, the table at its
# first read, where S raises KeyError on the point (UNJOINED), and each cell that joins
# is named with its message: a class neither table knows is refused by both joins, and the
# projection meets the COI scale's first.  (case, column, value, the projection's message,
# {each Data cell that refuses it: its message}.)  A mode on a single premium is never
# decoded, in S as here.
_NO_TYPE, _NO_MODE = "invalid premium type", "invalid premium mode"
_NO_SCALE_2 = "coi_rates.csv has no scale for the sex and rate_class of point_id [2]"
_NO_SCHEDULE_2 = ("surr_charge_table.csv has no schedule for the surr_charge_id of "
                  "point_id [2], each of which has_surr_charge")
_JOINS = {
    "rate_class": (_NO_SCALE_2, {
        "class_factor": "class_factor_table.csv has no factor for the rate_class of "
                        "point_id [2]", "coi_schedule": _NO_SCALE_2}),
    "sex": (_NO_SCALE_2, {"coi_schedule": _NO_SCALE_2}),
    "surr_charge_id": (_NO_SCHEDULE_2, {"surr_charge_rate_max": _NO_SCHEDULE_2,
                                        "surr_charge_runoff_years": _NO_SCHEDULE_2}),
}
UNDECODABLE = [
    ("premium_type LEVELX", "premium_type", "LEVELX", _NO_TYPE, {}),
    ("premium_mode W", "premium_mode", "W", _NO_MODE, {}),
    *[(f"premium_type {value!r}", "premium_type", value, _NO_TYPE, {})
      for value in ("level", " LEVEL", "single", "SINGLE ", "ten_pay", "TEN_PAY ")],
    *[(f"premium_mode {value!r}", "premium_mode", value, _NO_MODE, {})
      for value in ("a", " A", "s", "Q ", "m")],
    *[(f"{column} {value!r}", column, value, *_JOINS[column])
      for column, value in (("rate_class", "stdnt"), ("rate_class", "StdNT "),
                            ("sex", "m"), ("sex", " M"), ("surr_charge_id", "gul15"))],
]


@pytest.mark.parametrize("case, column, value, message, data", UNDECODABLE,
                         ids=[c[0] for c in UNDECODABLE])
def test_a_value_no_decode_knows_is_refused_as_in_ulsg_us_s(tmp_path, case, column, value,
                                                            message, data):
    """An unknown premium type or mode raises ``ULSG_US_S``'s message, not a branch.

    The three decodes of the premium type each compare the text with one value, so a value
    none of them names reads as no known one, and the cell that branches on them must raise
    as ``ULSG_US_S``'s does, rather than take its last branch; the mode's decode raises in
    the cell that reads it.  The table reads, because the text columns are the product's to
    judge, and the point's first projection raises, in this model as in ``ULSG_US_S``.  A
    class, a sex or a surrender schedule the tables do not know is refused by the ``Data``
    cells that join it, with the message matched whole, and by the point's projection,
    where ``ULSG_US_S``'s ``.loc`` raises ``KeyError``.  Each value is given in another case
    and with a space beside it (:data:`UNDECODABLE`), and is refused in both models.
    """
    point = _label(_committed(), "twin", 2, 0)
    model = _read(_sec_inputs(tmp_path / "sec", _set(column, [point], value)(_committed())),
                  "undecodable")
    s = _read(_s_inputs(tmp_path / "s", _set(column, [point], value)(_s_table())),
              "undecodable_s")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        for cell, refusal in data.items():
            _refused_exactly(model.Data.cells[cell], refusal)
        _refused(_point(model, point).result_cf, message)
        with pytest.raises(Exception) as excinfo:
            _point(s, point).result_cf()
        text = str(excinfo.value)
        assert ("KeyError" if data else f"ValueError: {message}") in text, text
    finally:
        s.close()
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
    future = _label(_committed(), "future", 2, -25)
    later = (f"model_point_table_sec.csv: duration_mth must be -24 or more, a policy "
             f"issued at most 24 months after the valuation date; it is not at point_id "
             f"[{future}]")
    no_future = (f"model_point_table_sec.csv: duration_mth must be 0 or more: this model "
                 f"takes no future new business; it is not at point_id [{future}]")
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
                assert len(p.result_cf()) == p.proj_len() == 757
                assert p.pols_new_biz(25) == p.policy_count()
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


_PAST_END = ("point_id {point}: duration_mth {d} is at or past the end of the projection, "
             "policy month 732, attained age 121")
_PAST_AGE = ("point_id {point}: age_at_entry {age} is at or past charges_cease_age, 121: a "
             "policy issued there would never be in cover")
_PAST_GRACE = ("point_id {point}: grace_mth_init {counter} is at or past grace_months, "
               "{months}: the grace expired before the valuation date, so the policy "
               "lapsed then, with no value")


@pytest.fixture(scope="module")
def s_at_82():
    """S's point 1's state entering its month 82, the month its latch shuts.

    The account value, the shadow account, the loan and the premiums paid as the spec's
    extractors read them, and the grace counter S's ``grace_mth(81)``, 2, which the spec's
    own extractor refuses to read there, off ``ULSG_US_S`` read for it and closed at once,
    so that the tests that read it hold no model of the module's.
    """
    model = _read(model_path(TWIN), "at_82")
    try:
        s = _point(model, 1)
        state = {column: extract(s, 82) for column, extract in SPEC.state.items()
                 if column != "grace_mth_init"}
        return {**state, "grace_mth_init": s.grace_mth(81)}
    finally:
        model.close()


def _lapsed_at_82(state, count):
    """An edit that restates the committed row of S point 1 at 81 at S's month 82.

    With ``state``, S's own state entering 82, the month its latch shuts (:func:`s_at_82`),
    and the count ``count``, S's 0.0 or one policy.
    """
    def edit(table):
        point = _label(table, "derived", 1, 81)
        for column, value in {"duration_mth": 382, "policy_count": count,
                              **state}.items():
            table = _set(column, [point], value)(table)
        return table
    return edit


# The refusals of proj_len(), in the order it checks them, as (case, the edit, the point it
# refuses, its message, the References read with it, those under which the same point
# projects): the future row issued at attained age 121, where charges cease, so that no
# month of its frame is in cover, and at 122, 25 months on, and 5 months on, where the
# frame itself would end before the valuation date, so that the age is checked first and
# its message names the age, not a policy month below 0; S's new business point 2 moved to
# the month the projection ends, policy month 732 at attained age 121, and a year past it;
# the row of S point 1 restated at its month 82, the month its grace expired, with S's
# count there, 0.0, and with one policy; and the row of S point 1 at 81 carrying a counter
# of 3, just past grace_months, and again with grace_months moved to 3, where a counter of
# 3 is refused and, the cases with S's count show, one of 2 projects (USLIB-SEC-PLAN.md
# §7.7, Record — M9, Rules on a Reference).  Each needs a Projection Reference,
# charges_cease_age or grace_months, so the table reads.  The windows' other sides are
# accepted elsewhere: the row restated at 731, the last covered month; the row of S point
# 1 at 81, carrying a counter of 1, part of the grace; and a point issued at attained age
# 120 (test_a_point_issued_at_attained_age_120_has_a_year_of_cover).
NOT_ISSUED = [
    ("issued at attained age 121", lambda s: _set("age_at_entry", [9], 121), 9,
     _PAST_AGE.format(point=9, age=121), {}, {"charges_cease_age": 123}),
    ("issued past attained age 121", lambda s: _set("age_at_entry", [9], 122), 9,
     _PAST_AGE.format(point=9, age=122), {}, {"charges_cease_age": 123}),
    ("issued past attained age 121 within a year",
     lambda s: _both(_set("age_at_entry", [9], 122), _set("duration_mth", [9], -5)), 9,
     _PAST_AGE.format(point=9, age=122), {}, {"charges_cease_age": 123}),
    ("at the end", lambda s: _set("duration_mth", [2], 732), 2,
     _PAST_END.format(point=2, d=732), {}, {"charges_cease_age": 123}),
    ("past the end", lambda s: _set("duration_mth", [2], 744), 2,
     _PAST_END.format(point=2, d=744), {}, {"charges_cease_age": 123}),
    ("its grace expired, with S's count", lambda s: _lapsed_at_82(s, 0.0), 5,
     _PAST_GRACE.format(point=5, counter=2, months=2), {}, {"grace_months": 3}),
    ("its grace expired, with a policy", lambda s: _lapsed_at_82(s, 1.0), 5,
     _PAST_GRACE.format(point=5, counter=2, months=2), {}, {"grace_months": 3}),
    ("a counter past its grace", lambda s: _set("grace_mth_init", [5], 3), 5,
     _PAST_GRACE.format(point=5, counter=3, months=2), {}, {"grace_months": 4}),
    ("a counter at a grace moved to 3 months", lambda s: _set("grace_mth_init", [5], 3), 5,
     _PAST_GRACE.format(point=5, counter=3, months=3), {"grace_months": 3},
     {"grace_months": 4}),
]


@pytest.mark.parametrize("case, edit, point, message, refs, moved", NOT_ISSUED,
                         ids=[c[0] for c in NOT_ISSUED])
def test_a_point_past_its_cover_or_its_grace_is_refused_by_proj_len(s_at_82, tmp_path,
                                                                  case, edit, point,
                                                                  message, refs, moved):
    """A point with no month in cover, or whose grace has expired, is refused by name.

    A point at or past the end of the projection has no frame; one issued at or past the
    age at which premiums and charges cease, 121, would have a frame with no month in
    cover; and one carried into the valuation date with a grace counter at
    ``grace_months`` or past it lapsed at its start, with no value, and is no policy in
    force: the in-force interface carries no lapse latch to restate it with.  Each is a
    rule of the product, not of the table: it needs ``charges_cease_age`` or
    ``grace_months``, a Projection Reference, so the table reads, and the point is refused
    where its frame is defined, on its first projection, rather than projecting nothing or
    a lapsed policy.  Each rule is stated on its Reference: with ``charges_cease_age`` at
    123, or ``grace_months`` moved past the counter, set first, the same point projects,
    and with ``grace_months`` moved to 3 a counter of 3 is refused, naming the Reference's
    value.  A loop over the block would meet the point only when it reached it, after
    projecting the points before it, so ``run_sec.py --block``, run beside the table at
    the shipped References, asks every point for its frame first: it fails naming the
    point, and prints nothing before.
    """
    folder = _sec_inputs(tmp_path, edit(s_at_82)(_committed()))
    model = _read(folder, "past", refs)
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused_exactly(_point(model, point).proj_len, message)
        _refused(_point(model, point).result_cf, message)
    finally:
        model.close()
    model = _read(folder, "past_moved", moved)
    try:
        p = _point(model, point)
        assert p.proj_len() > 0 and len(p.result_cf()) == p.proj_len()
    finally:
        model.close()
    if refs:
        return
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert message in done.stderr.decode(errors="replace")


def test_a_point_issued_at_attained_age_120_has_a_year_of_cover(tmp_path):
    """The age rule's window is accepted just outside it: a point issued at 120 projects.

    ``proj_len()`` refuses a point to be issued at or past attained age 121, where charges
    cease; one to be issued at 120, the last age with cover, is a policy, and is read
    (USLIB-SEC-PLAN.md §5.2, T5, each rule refused just inside its window and accepted
    just outside).  The committed table's future row, issued 25 months on, with its issue
    age at 120: its frame is 37 months, its cover the 12 from ``t = 25``, its policies
    arrive then as new business, the table's rate of 1.0 at attained age 120, which
    improvement does not reach there, ends every one of them in that month, and every flow
    is a finite float, zero outside cover.
    """
    committed = _committed()
    future = _label(committed, "future", 2, -25)
    model = _read(_sec_inputs(tmp_path, _set("age_at_entry", [future], 120)(committed)),
                  "issued_at_120")
    try:
        p = _point(model, future)
        assert (p.charges_cease_mth(), p.proj_len(), p.t_entry()) == (12, 37, 25)
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
# extents and counts Data reads from them, each an int, which sizes an array at stage EC.
FLOAT_KEYS = {"lapse_table.csv": ("policy_year",), "corridor_factors.csv": ("age",),
              "mort_table.csv": ("age",), "coi_rates.csv": ("age",),
              "rop_table.csv": ("anniversary",), "surr_charge_table.csv": ("runoff_years",)}
EXTENTS = ("lapse_last_year", "corridor_age_first", "corridor_age_last", "mort_age_first",
           "mort_age_last", "rop_count", "rop_last_anniv", "coi_schedules")
INT_COLUMNS = ("duration_mth", "age_at_entry", "guarantee_age", "grace_mth_init",
               "coi_rate_dp")


def _as_floats(columns):
    """An edit that writes the table's ``columns`` as floats."""
    def edit(table):
        return table.assign(**{column: table[column].astype(float) for column in columns})
    return edit


def test_the_edges_of_the_in_force_interface_are_accepted(tmp_path):
    """A zero count, whole numbers in any type, the horizon and the state's edges are read.

    One copy of the committed table, edited at the edges a real extract reaches, is read
    beside a copy of every keyed table with its keys written as floats, 61.0 for 61, as a
    spreadsheet can save them (:data:`FLOAT_KEYS`), and again beside the tables as
    shipped, so that every table is read:

    * ``Data`` reads each key by value, so every extent and count is the one read beside
      the tables as shipped, an int, the COI cells' last ages are the shipped ones, and the
      twins of S's points 1 and 3, the row in grace and the row issued 120 months on, which
      between them read every table, project exactly what they project beside the tables
      as shipped;
    * the table's integer columns written as floats (:data:`INT_COLUMNS`) are whole numbers
      read back as the ints the clocks and the counters count in;
    * a shadow account below 0 and a grace counter of 1 are a policy in force in its grace;
    * a premium load of 1 and of 0, a share at each of its bounds, is read as written, the
      load taking the whole premium or none of it;
    * the persistency pin at 0, as at the shipped 1, is a pin, and a premium of 0;
    * a COI precision of 0 places rounds each rate to a whole number;
    * a count of 0 is a point that projects zeros;
    * and a policy issued 120 months after the valuation date, the shipped
      ``future_horizon_mth``, is the last one the table admits, with a frame of 852 months,
      732 of cover after 120 before issue.
    """
    committed = _committed()
    zero = _label(committed, "derived", 2, 305)
    full_load = _label(committed, "derived", 2, 240)
    no_load = _label(committed, "twin", 4, 0)
    unpaid = _label(committed, "twin", 2, 0)
    grace = _label(committed, "derived", 1, 81)
    future = _label(committed, "future", 2, -25)
    probes = [_label(committed, "twin", p, 0) for p in (1, 3)] + [grace, future]
    edited = _both(
        _set("policy_count", [zero], 0.0), _set("load_prem_rate", [full_load], 1.0),
        _set("load_prem_rate", [no_load], 0.0), _set("coi_rate_dp", [no_load], 0.0),
        _set("prem_persistency_override", [unpaid], 0.0),
        _as_floats(INT_COLUMNS), _set("duration_mth", [future], -120.0))(committed)
    floats = _sec_inputs(tmp_path / "floats", edited, edits={
        file: _as_floats(columns) for file, columns in FLOAT_KEYS.items()})
    for file, columns in FLOAT_KEYS.items():
        written = pd.read_csv(floats.parent / file)
        assert all(written[c].dtype == float for c in columns), file
    shipped = _sec_inputs(tmp_path / "shipped", edited)
    model = _read(floats, "edges")
    plain = _read(shipped, "edges_shipped")
    try:
        for cell in EXTENTS:
            value = model.Data.cells[cell]()
            assert (type(value), value) == (int, plain.Data.cells[cell]()), cell
        got, want = model.Data.coi_rate_last_ages(), plain.Data.coi_rate_last_ages()
        assert np.array_equal(got, want) and got.dtype == "int64"
        read = model.Data.model_point_table()
        assert all(read[column].dtype == float for column in INT_COLUMNS)
        for label in probes:
            mine, base = _point(model, label), _point(plain, label)
            for report in REPORTS:
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=0, atol=0) == [], (label, report)
        p = _point(model, grace)
        assert [(type(v), v) for v in (p.duration_mth(0), p.age_at_entry(),
                                       p.guarantee_age(), p.grace_mth_init(),
                                       p.coi_rate_dp())] == [
            (int, 381), (int, 60), (int, 121), (int, 1), (int, 2)]
        assert p.sg_pp_init() < 0.0 and p.grace_mth(0) == 2 and _status_is(p, 0, "GRACE")
        p = _point(model, full_load)
        assert p.load_prem_rate() == 1.0 and p.prem_to_av_pp(0) == 0.0 < p.premium_pp(0)
        p = _point(model, no_load)
        assert p.load_prem_rate() == 0.0 and p.prem_to_av_pp(0) == p.premium_pp(0) > 0.0
        rates = [(p.coi_rate(t), round(p.coi_curr_factor * p.coi_rate_guar(t), 0))
                 for t in range(p.proj_len())]
        assert all(got == want and got % 1 == 0.0 for got, want in rates)
        assert rates[0][0] == 0.0 < rates[-1][0]
        p = _point(model, unpaid)
        assert (p.prem_persistency(0), p.premium_pp(0)) == (0.0, 0.0)
        assert all(math.isfinite(v) for v in p.result_cf().to_numpy().ravel())
        p = _point(model, zero)
        df = p.result_cf()
        assert len(df) == 427 and (df == 0.0).all().all()
        p = _point(model, future)
        assert (p.t_entry(), p.proj_len(), p.pols_new_biz(120)) == (120, 852, 1.0)
    finally:
        plain.close()
        model.close()


# The two flags, and each spelling of a flag Data accepts: True and False in any case,
# which pandas reads as the bools.
FLAGS = ("has_surr_charge", "rop_elected")
SPELLINGS = {True: ("TRUE", "true", "tRuE"), False: ("FALSE", "false", "FaLsE")}


def _respelled(table):
    """``table`` with each flag of :data:`FLAGS` written as text, each value's spellings of
    :data:`SPELLINGS` taken in turn, row by row and column by column."""
    turns = {True: itertools.count(), False: itertools.count()}
    for column in FLAGS:
        words = [SPELLINGS[bool(v)][next(turns[bool(v)]) % 3] for v in table[column]]
        table = table.assign(**{column: words})
    return table


def test_a_flag_reads_the_same_in_every_spelling_data_accepts(tmp_path):
    """Each flag decodes, and projects, as written in every spelling ``Data`` accepts.

    ``Data`` accepts a flag written ``True`` or ``False`` in any case, which pandas reads
    as the bools, and refuses a blank, any other text and any number, 1, 0, 1.0 and 0.0
    among them (:data:`MALFORMED`).  The model decodes a flag with ``ULSG_US_S``'s
    ``bool()``, which reads any text but the empty string as true, so a spelling pandas left
    as text would project a point with no surrender charge or no endorsement as one with
    it (USLIB-SEC-PLAN.md §7.8, Record — M10, Flag spellings).  So the committed table, with
    the surrender charge taken off the twins of S points 2 and 3 and the endorsement off the
    twin of S point 3, so that each flag is False on two rows, is read as written and again
    with every flag in a spelling of :data:`SPELLINGS`, each taken in turn
    (:func:`_respelled`), every one of the six in the file: ``Data`` reads both flags as
    bools, the same in both, every row decodes both flags the same, and the twins of S
    points 2 and 4, which read a False of each flag beside a True of the other, project
    the same four reports, bit for bit.
    """
    committed = _committed()
    twins = {p: _label(committed, "twin", p, 0) for p in (2, 3, 4)}
    table = _both(_set("has_surr_charge", [twins[2], twins[3]], False),
                  _set("rop_elected", [twins[3]], False))(committed)
    spelled = _respelled(table)
    models = {}
    try:
        for tag, written in (("written", table), ("spelled", spelled)):
            models[tag] = _read(_sec_inputs(tmp_path / tag, written), f"flags_{tag}")
        text = (tmp_path / "spelled" / TABLE).read_text()
        assert all(f",{word}," in text or f",{word}\n" in text
                   for words in SPELLINGS.values() for word in words), text[:400]
        base, respelled = models["written"], models["spelled"]
        want, got = (m.Data.model_point_table()[list(FLAGS)] for m in (base, respelled))
        assert (want.dtypes == bool).all() and got.equals(want), got
        for key, other in zip(point_keys(respelled), point_keys(base)):
            mine, theirs = projection(respelled, key), projection(base, other)
            assert [(type(v), v) for v in (mine.has_surr_charge(), mine.rop_elected())] == [
                (bool, v) for v in (theirs.has_surr_charge(), theirs.rop_elected())], key
        for point in (2, 4):
            mine, theirs = _point(respelled, twins[point]), _point(base, twins[point])
            for report in REPORTS:
                assert frame_mismatches(theirs.cells[report](), mine.cells[report](),
                                        rtol=0, atol=0) == [], (point, report)
    finally:
        for model in models.values():
            model.close()


# ---------------------------------------------------------------------------
# The product's own facts, on models read for the test


def test_the_grace_counter_the_shadow_account_and_premiums_paid_open_from_their_columns(
        tmp_path):
    """Each opening-state column moves the projection as S's own state there does.

    ``ULSG_US_S`` opens its points with a grace counter of 0, and so restarts a grace, and
    keeps no column for the counter; it never floors its shadow account; and it opens its
    premiums paid from ``cum_prem_init``, which a row in force carries.  So each committed
    row is read in a copy beside a row of its own that opens one column as a model might
    have assumed, at the shipped References:

    * the row of S point 1 at 381, a month into its grace, carries a counter of 1: its first
      month takes it to 2, and the policy lapses at ``t = 1``, S's month 82, every policy
      in force at ``t = 0`` but the month's deaths and lapses leaving at its end, where the
      counter at 0 would restart the grace, and the policy lapse a month late, 0.4232 of a
      policy still in force at ``t = 1``;
    * the same row carries its shadow account below 0, at -1,365.21: it closes month 0 at
      -5,551.43 and asks a catch-up premium of 6,034.16, where floored at 0, as the account
      value is, it would close at -4,180.11 and ask 4,543.60;
    * the twin of S point 1 carries $270,000 paid to date: its 25th anniversary's refund
      at ``t = 0`` is the cap, 40% of the face, $200,000, where premiums paid from 0 would
      refund the month's premium, $10,800; and the row of S point 2 at 240, $211,680 paid,
      refunds half of $222,264 at its 20th, $111,132, where from 0 it would refund $5,292.

    And on a copy of S point 4 paying $6,150 a year, restated from S at its month 240, the
    counter carried in, 1, resets at ``t = 0``, as S's does: the anniversary premium cures
    the grace, the policy does not lapse, and its count runs on; restated at 243 its counter
    of 1 is carried into the lapse at ``t = 1``, S's month 244.  T2 holds every column of
    every restated row against S.
    """
    committed = _committed()
    grace = _label(committed, "derived", 1, 81)
    twin = _label(committed, "twin", 1, 0)
    window = _label(committed, "derived", 2, 240)

    def restart(point, label, **columns):
        row = committed.loc[[point]].assign(
            policy_id=committed.at[point, "policy_id"] + "-X", **columns)
        row.index = pd.Index([label], name="point_id")
        return row

    table = pd.concat([committed.loc[[grace, twin, window]],
                       restart(grace, 101, grace_mth_init=0),
                       restart(grace, 102, sg_pp_init=0.0),
                       restart(twin, 103, cum_prem_init=0.0),
                       restart(window, 104, cum_prem_init=0.0)])
    model = _read(_sec_inputs(tmp_path / "sec", table), "opened")
    try:
        p, no_counter, floored = (_point(model, i) for i in (grace, 101, 102))
        assert (p.grace_mth_init(), p.grace_mth(0), p.is_lapsed(1)) == (1, 2, True)
        assert p.pols_if(1) == 0.0
        assert p.pols_lapse_grace(0) == (p.pols_if(0) - p.pols_death(0) - p.pols_lapse(0)
                                         - p.pols_rop(0))
        assert (no_counter.grace_mth(0), no_counter.is_lapsed(1)) == (1, False)
        assert no_counter.pols_if(1) == pytest.approx(0.4232, abs=5e-5)
        assert no_counter.is_lapsed(2) and no_counter.pols_if(2) == 0.0
        assert (p.sg_pp_init(), p.sg_pp(0), p.catch_up_prem_pp(0)) == pytest.approx(
            (-1365.21, -5551.43, 6034.16), abs=0.005)
        assert (floored.sg_pp(0), floored.catch_up_prem_pp(0)) == pytest.approx(
            (-4180.11, 4543.60), abs=0.005)
        q, from_zero = _point(model, twin), _point(model, 103)
        refund = _code(q, "REFUND")
        assert (q.claim_pp(0, refund), from_zero.claim_pp(0, refund)) == (200000.0, 10800.0)
        assert q.cum_prem_pp(0) == 270000.0 + 10800.0
        r, from_zero = _point(model, window), _point(model, 104)
        assert r.cum_prem_pp(0) == pytest.approx(222264.0, abs=1e-6)
        assert (r.claim_pp(0, refund), from_zero.claim_pp(0, refund)) == pytest.approx(
            (111132.0, 5292.0), abs=1e-6)
    finally:
        model.close()
    cure = {13: VARIANTS[13]}
    s = _read(_s_inputs(tmp_path / "s", _s_table_with_variants(cure)), "cure_s")
    sec = None
    try:
        sp = _point(s, 13)
        assert [sp.grace_mth(t) for t in range(238, 245)] == [0, 1, 0, 0, 1, 2, 0]
        assert sp.is_lapsed(244) and not sp.is_lapsed(243)
        spec = dataclasses.replace(SPEC, derived=((13, 240), (13, 243)), future=())
        built, _ = build_sec_table(spec, s)
        sec = _read(_sec_inputs(tmp_path / "cure", built), "cure")
        cured, lapsing = _row(sec, "derived", 13, 240), _row(sec, "derived", 13, 243)
        assert (cured.grace_mth_init(), cured.grace_mth(0)) == (1, 0)
        assert not cured.is_lapsed(1) and cured.pols_if(1) > 0.0
        assert cured.premium_pp(0) == 6150.0 * 0.98 and not cured.is_shortfall(0)
        assert (lapsing.grace_mth_init(), lapsing.grace_mth(0), lapsing.is_lapsed(1)) == (
            1, 2, True)
        assert lapsing.pols_if(1) == 0.0
    finally:
        if sec is not None:
            sec.close()
        s.close()


def _rising_credited_rate(t):
    """The declared rate, rising a basis point a month from the valuation date."""
    return crediting_rate_curr + 0.0001 * t                          # noqa: F821


def _rising_credited_rate_from_12(t):
    """The same path for an S point that started 12 months before the valuation date."""
    return crediting_rate_curr + 0.0001 * (t - 12)                   # noqa: F821


def test_the_declared_rate_runs_on_the_valuation_clock(tmp_path):
    """The declared rate is a path on ``t``, the same instant for every point (D7).

    ``ULSG_US_S``'s declared rate is flat, so a rate read at another month than its own
    changes no number, and a formula override moves it, in models just read, so modelx's
    alone (C1): the rate rising a basis point a month from the valuation date.  Then
    ``crediting_rate_ann(t)`` and the account's monthly credited rate are one number at each
    ``t`` for every committed point, the path's at ``t``, and the account value entering
    each month is the previous month's close, exactly.  On S's new business the two clocks
    coincide, so ``ULSG_US_S`` given the same path projects what the twin of its point 2
    projects, in every report and every cell of S's.  And a row restated at S's month 12
    reads the path at its own ``t``, where S, whose own start is 12 months before the
    valuation date, reads the same path at its month ``t + 12``: with S given the path from
    12 months before, the row generated from that S continues it in every cell of S's, with
    improvement and inflation at 0 in both, as T2 compares a restated row.  A credited rate
    read on the policy clock would part them.
    """
    models = []
    try:
        for name in (SEC, TWIN):
            model = _read(model_path(name), f"{name}_rising")
            model.Projection.cells["crediting_rate_ann"].formula = _rising_credited_rate
            models.append(model)
        sec, s = models
        ps = [projection(sec, key) for key in point_keys(sec)]
        for t in (0, 1, 12, 25):
            rate = sec.Projection.crediting_rate_curr + 0.0001 * t
            for cell, value in (("crediting_rate_ann", rate),
                                ("inv_return_mth", (1 + rate) ** (1 / 12) - 1)):
                got = [p.cells[cell](t) for p in ps]
                assert got == pytest.approx([value] * len(ps), rel=1e-12), (cell, t)
        for p in ps:
            bef_prem = _code(p, "BEF_PREM")
            apart = [t for t in range(p.t_entry() + 1, p.proj_len())
                     if p.av_pp_at(t, bef_prem) != p.av_pp(t - 1)]
            assert not apart, (p.point_id, apart[:5])
        sp = _point(s, 2)
        _sweep_s(sp)
        assert _continues_s(sp, _row(sec, "twin", 2, 0), 0, arg_map=_issued_later) == []
    finally:
        for model in models:
            model.close()
    neutral = {"inflation_rate": 0.0, "mort_improve_rate_init": 0.0}
    s = _read(_s_inputs(tmp_path / "s", _s_table().loc[[2]]), "s_rising_12", neutral)
    s.Projection.cells["crediting_rate_ann"].formula = _rising_credited_rate_from_12
    sec = None
    try:
        spec = dataclasses.replace(SPEC, derived=((2, 12),), future=())
        table, _ = build_sec_table(spec, s)
        sec = _read(_sec_inputs(tmp_path / "sec", table), "sec_rising_12", neutral)
        sec.Projection.cells["crediting_rate_ann"].formula = _rising_credited_rate
        sp = _point(s, 2)
        _sweep_s(sp)
        p = _row(sec, "derived", 2, 12)
        assert (p.crediting_rate_ann(0), sp.crediting_rate_ann(12)) == (
            sec.Projection.crediting_rate_curr,) * 2
        assert _continues_s(sp, p, 12, SPLICE_EXEMPT) == []
    finally:
        if sec is not None:
            sec.close()
        s.close()


def test_a_residual_that_is_not_a_number_fails_its_check():
    """A check whose residual is not a number fails, as ``ULSG_US_S``'s ``isclose`` does.

    The checks are the model's one guard against a value that is not a number: the floors
    at zero of the account value and the cash value, and the maxes of the death benefit
    and the net amount at risk, turn a NaN into a number, so the cash flows can stay
    numbers.  On models just read, with a Reference set to NaN before anything is
    computed, which runs compiled as it runs here (USLIB-SEC-PLAN.md §7.12, *Record —
    M12*), the NaN is sent through one the counts read and through two that reach a
    residual without them (§7.8, *Record — M10*, *NaN checks*):

    * ``mort_improve_rate_init``, which reaches mortality, and through it the counts, from
      ``t = 12``, its factor 1.0 in the first valuation year: on the twins of S's points 1
      and 2 and the row of S point 2 at 240, the account value's and the margin's residuals
      are within 1e-9 before ``t = 12`` and NaN from it, and their checks ``False``, as S's
      are; the shadow account's, which no mortality reaches, is within 1e-9 throughout and
      its check ``True``;
    * ``crediting_rate_curr``, the declared rate, which reaches the account value's credit
      and no count: on the same three rows the account value's and the margin's residuals
      are NaN from ``t = 0``, and on the row issued 25 months on 0.0 before its issue and
      NaN from it, while every count stays a number; the checks decide as above, as S's do;
    * ``sg_rate_ann``, which reaches the shadow account's interest: on the row issued 25
      months on, its residual is 0.0 before its issue, at ``t = 25``, and NaN from it, and
      its check ``False``, as S's is on its point 2.

    A check that asked whether the residual is above its tolerance would pass each of them,
    since no comparison with NaN holds, so each loop stops at ``not abs(r) <= 1e-9``.
    """
    models = {}
    try:
        for ref in ("mort_improve_rate_init", "crediting_rate_curr", "sg_rate_ann"):
            for name in (SEC, TWIN):
                models[ref, name] = _read(model_path(name), f"nan_{ref}",
                                          {ref: float("nan")})
        # Each Reference, with the first month its NaN reaches the two residuals on a row
        # in force or issued at the valuation date.
        for ref, first in (("mort_improve_rate_init", 12), ("crediting_rate_curr", 0)):
            sec, s = models[ref, SEC], models[ref, TWIN]
            for case in (("twin", 1, 0), ("twin", 2, 0), ("derived", 2, 240)):
                p = _row(sec, *case)
                months = range(p.proj_len())
                for resid, check in (("check_av_roll_fwd_resid", "check_av_roll_fwd"),
                                     ("check_margin_resid", "check_margin")):
                    values = [p.cells[resid](t) for t in months]
                    assert all(abs(r) <= 1e-9 for r in values[:first]), (ref, case, resid)
                    assert all(math.isnan(r) for r in values[first:]), (ref, case, resid)
                    assert p.cells[check]() is False, (ref, case, check)
                assert all(abs(p.check_sg_roll_fwd_resid(t)) <= 1e-9 for t in months), (
                    ref, case)
                assert p.check_sg_roll_fwd() is True, (ref, case)
            for point in (1, 2):
                sp = _point(s, point)
                assert (sp.check_av_roll_fwd(), sp.check_sg_roll_fwd(),
                        sp.check_margin()) == (False, True, False), (ref, point)
        sec = models["crediting_rate_curr", SEC]
        p = _row(sec, "future", 2, -25)
        for resid in ("check_av_roll_fwd_resid", "check_margin_resid"):
            values = [p.cells[resid](t) for t in range(p.proj_len())]
            assert values[:25] == [0.0] * 25 and all(math.isnan(r) for r in values[25:])
        for case in (("twin", 1, 0), ("twin", 2, 0), ("future", 2, -25)):
            x = _row(sec, *case)
            assert all(math.isfinite(x.pols_if(t)) for t in range(x.proj_len())), case
        sec, s = models["sg_rate_ann", SEC], models["sg_rate_ann", TWIN]
        p = _row(sec, "future", 2, -25)
        values = [p.check_sg_roll_fwd_resid(t) for t in range(p.proj_len())]
        assert values[:25] == [0.0] * 25 and all(math.isnan(r) for r in values[25:])
        assert p.check_sg_roll_fwd() is False
        assert _point(s, 2).check_sg_roll_fwd() is False
    finally:
        for model in models.values():
            model.close()


# The References at which ULSG's annual lapse rate passes 1: its cap raised past 1 and the
# lifetime guarantee's multiplier at 30, so that S's point 2, in its first policy year at
# the table's 0.04, lapses at 1.2 from t = 0.  Data holds the table's rates to 0 to 1, but
# the cap and the multipliers are References, which nothing refuses; at the shipped cap of
# 0.5 no rate passes 1.
LAPSE_PAST_1 = {"lapse_rate_cap": 5.0, "lapse_guar_mult": 30.0}


def test_a_lapse_rate_past_1_makes_each_check_raise_as_in_ulsg_us_s():
    """Past 1 the monthly lapse rate is complex, and the checks it reaches raise, in both.

    ``ULSG_US_S`` caps its lapse rate at ``lapse_rate_cap``, 0.5 as shipped, so no count
    turns complex through it; a cap set past 1 is a Reference nothing refuses.  Set before
    anything is computed, :data:`LAPSE_PAST_1` takes S's point 2's annual rate to 1.2 in
    its first month, where ``1 - (1 - q)^(1/12)`` has no real value, and every count after
    it is complex.  ``ULSG_US_S``'s ``math.isclose`` raises ``TypeError`` on it, and this
    model's account value and margin residuals are each a ``float`` of their ratio, so they
    raise too, where a residual left complex would pass its check on its magnitude, a real
    number.  The shadow account's check reads no count, and holds in both.
    """
    models = {}
    try:
        for name in (SEC, TWIN):
            models[name] = _read(model_path(name), "lapse_past_1", LAPSE_PAST_1)
        p, s = _row(models[SEC], "twin", 2, 0), _point(models[TWIN], 2)
        for x in (p, s):
            assert (type(x.lapse_rate(0)), x.lapse_rate(0)) == (float, 1.2)
            assert type(x.lapse_rate_mth(0)) is complex
            assert type(x.pols_if(0)) is float and type(x.pols_if(1)) is complex
            for check in ("check_av_roll_fwd", "check_margin"):
                with pytest.raises(Exception) as excinfo:
                    x.cells[check]()
                text = str(excinfo.value)
                assert "TypeError" in text and "complex" in text, (x.name, check, text)
            assert x.check_sg_roll_fwd() is True
    finally:
        for model in models.values():
            model.close()


# How far each check's two sides are moved apart, and whether every check then passes:
# inside the checks' absolute tolerance, and outside it wherever the sides are below 1.
CHECK_MISSES = {5e-10: True, 2e-9: False}


def _moved(model, cell, formula):
    """Give ``cell`` of ``model``'s Projection ``formula``, its own kept in a new cell.

    The new cell is ``<cell>_unmoved``, which ``formula`` may call.

    A formula override through a new cell, so modelx's alone (C1), set before anything is
    computed.
    """
    proj = model.Projection
    proj.new_cells(name=f"{cell}_unmoved", formula=proj.cells[cell].formula.source)
    proj.cells[cell].formula = formula


def test_each_check_decides_as_isclose_does_where_its_sides_are_small(tmp_path):
    """Each check decides as ``ULSG_US_S``'s ``isclose`` does, where its sides are small.

    ``ULSG_US_S`` asks ``isclose`` with both tolerances at ``1e-9``, which holds where the
    two sides differ by at most ``1e-9`` times the larger of them and 1.  ``ULSG_US_SEC``
    divides each month's difference by that larger value and asks whether the residual is
    within ``1e-9``, which is the same test only through the floor of 1: over the larger
    side alone, a miss inside the absolute tolerance fails where the sides are below 1, and
    over a floor above 1 a miss outside it passes.  So, in both models, on models just read,
    each check's sides are moved apart by each miss of :data:`CHECK_MISSES` where they are
    small, and each check of each model passes the miss of ``5e-10`` and fails the one of
    ``2e-9``:

    * the shadow account's deduction, which only its check and ``result_av`` read, moved in
      month 0 of a row of S's own, S's point 1 in force 305 months with a shadow account of
      2,373.57, which closes month 0 at 0.2541 in both models;
    * the investment credit in force, which only the account value's check and the
      margin's read, moved in every month of the twin of S's point 1, whose sides are 0
      from its lapse at ``t = 82`` on.

    The shadow account's check is the one place its residual's floor of 1 wins, the side
    :data:`BOUND_ELSEWHERE` names this test for, which no row of the splice's grids binds,
    none closing its shadow account within 1 of 0 (:class:`_BoundSides`).
    """
    row = _s_table().loc[[1]].assign(duration_mth=305, sg_pp_init=2373.57)
    s_folder = _s_inputs(tmp_path / "s", row)
    s_built = _read(s_folder, "moved_shadow_build")
    try:
        table, _ = build_sec_table(dataclasses.replace(SPEC, derived=(), future=()),
                                   s_built)
    finally:
        s_built.close()
    sec_folder = _sec_inputs(tmp_path / "sec", table)
    for miss, passes in CHECK_MISSES.items():
        models = []
        try:
            for folder in (sec_folder, s_folder):
                model = _read(folder, "moved_shadow")
                _moved(model, "sg_deduction_pp", "lambda t: sg_deduction_pp_unmoved(t) + "
                       f"({miss!r} if t == 0 else 0.0)")
                models.append(model)
            p, sp = (_point(model, 1) for model in models)
            with _BoundSides(models[0]).watch() as won:
                verdict = p.check_sg_roll_fwd()
            assert (p.sg_pp(0), sp.sg_pp(0)) == pytest.approx((0.2541, 0.2541), abs=5e-5)
            assert (verdict, sp.check_sg_roll_fwd()) == (passes, passes), miss
            mine = _sides_bound_by(
                "test_each_check_decides_as_isclose_does_where_its_sides_are_small")
            if sys.version_info >= (3, 11):
                assert len(mine) == 1 and mine <= won, sorted(mine - won)
        finally:
            for model in models:
                model.close()
        models = []
        try:
            for name in (SEC, TWIN):
                model = _read(model_path(name), "moved_credit")
                _moved(model, "inv_income", f"lambda t: inv_income_unmoved(t) + {miss!r}")
                models.append(model)
            p, sp = _row(models[0], "twin", 1, 0), _point(models[1], 1)
            assert p.is_lapsed(82)
            assert p.av_at(83, _code(p, "BEF_PREM")) == p.net_cf(100) == 0.0
            for check in ("check_av_roll_fwd", "check_margin"):
                assert (p.cells[check](), sp.cells[check]()) == (passes, passes), (
                    miss, check)
        finally:
            for model in models:
                model.close()


def _s_row_in_force(tmp_path, point, month, refs=None, **columns):
    """S's point ``point``, with ``columns``, restated by S in force at its ``month``.

    The point is read alone by ``ULSG_US_S`` with ``columns`` changed and ``refs`` set
    first, and its own state entering ``month`` is written into a row of S's table: the
    account value, the shadow account and the loan at their opening timings and the
    premiums paid to the month before, the columns S opens a point in force from.  Returns
    that one-row table, ``point_id`` kept.
    """
    row = _s_table().loc[[point]].assign(**columns)
    s = _read(_s_inputs(tmp_path / "issue", row), "in_force_at", refs)
    try:
        p = _point(s, point)
        state = {"av_pp_init": p.av_pp_at(month, "BEF_PREM"),
                 "sg_pp_init": p.sg_pp_at(month, "BEF_PREM"),
                 "loan_bal_init": p.loan_bal_pp_at(month, "BEF_INT"),
                 "cum_prem_init": p.cum_prem_pp(month - 1),
                 "pols_if_init": p.pols_if(month)}
    finally:
        s.close()
    return row.assign(duration_mth=month, **state)


def test_the_margin_identity_holds_once_a_loan_exceeds_the_cash_value(tmp_path):
    """Once the loan exceeds the cash value, the margin identity still closes.

    ``ULSG_US_S``'s identity adds back the whole loan on every lapse,
    ``L(t) x pols_lapse(t)``, as though the lapse claim were ``CSV - L``.  The claim is the
    net cash value, floored at 0, so once the loan exceeds the cash value the identity is
    off by ``(CSV(t) - L(t)) x pols_lapse(t)``, and ``ULSG_US_S``'s ``check_margin`` fails
    on a projection that is right.  This model's adds back the loan the surrender recovers,
    ``min(L(t), CSV(t)) x pols_lapse(t)``.  On a row of S's own, S's point 3 at a single
    premium of $700,000 restated by S in force at its month 24, with a loan of its account
    value less $3,000, $555,103.17, read in both models with the loan's rate at the 3% it
    is credited at, so that the account never runs out while the loan exceeds the cash
    value, and inflation at 0, which runs from the valuation date here and by policy year in
    S, each set first:

    * the loan exceeds the cash value in every month of the frame, so the net cash value's
      floor binds with lapses there, ``ncsv_pp(0) == 0.0``, and the refund's floor at both
      windows, ``claim_pp(t, "REFUND") == 0.0`` at S's months 240 and 300;
    * the projection is S's, in every report and every cell of S's but ``check_margin``,
      to 1e-9 relative with no absolute floor;
    * in each month with lapses S's identity misses by ``(CSV - L) x pols_lapse``, to the
      identity's own tolerance, and ``ULSG_US_S``'s ``check_margin`` is ``False``;
    * and this model's margin residual is within 1e-9 in every month, its check ``True``,
      and the other two checks hold in both models.
    """
    refs = {"loan_rate_ann": 0.03, "inflation_rate": 0.0}
    row = _s_row_in_force(tmp_path, 3, 24, refs, premium_pp_ann=700000.0)
    row = row.assign(loan_bal_init=round(float(row["av_pp_init"].iloc[0]) - 3000.0, 2))
    assert float(row["loan_bal_init"].iloc[0]) == pytest.approx(555103.17, abs=0.005)
    s = _read(_s_inputs(tmp_path / "s", row), "lent_s", refs)
    sec = None
    try:
        table, _ = build_sec_table(dataclasses.replace(SPEC, derived=(), future=()), s)
        sec = _read(_sec_inputs(tmp_path / "sec", table), "lent", refs)
        sp, p = _point(s, 3), _point(sec, 3)
        _sweep_s(sp)
        assert _continues_s(sp, p, 0, TWIN_EXEMPT | {"check_margin"}) == []
        months = range(p.proj_len())
        assert all(p.loan_bal_pp(t) > p.csv_pp(t) for t in months)
        assert p.ncsv_pp(0) == 0.0 and p.pols_lapse(0) > 0.0
        windows = [t for t in months if p.rop_anniversary(t)]
        assert windows == [216, 276]
        refund = _code(p, "REFUND")
        assert all(p.claim_pp(t, refund) == 0.0 < p.rop_ratio(t) for t in windows)
        for t in months:
            if not p.pols_lapse(t) > 0.0:
                continue
            s_rhs = (p.margin_expense(t) + p.margin_mortality(t) + p.margin_rop(t)
                     + p.av_change(t) - p.inv_income(t)
                     + p.loan_bal_pp(t) * p.pols_lapse(t))
            gap = p.net_cf(t) - s_rhs
            floored = (p.csv_pp(t) - p.loan_bal_pp(t)) * p.pols_lapse(t)
            assert abs(gap - floored) <= 1e-9 * max(abs(p.net_cf(t)), abs(s_rhs), 1.0), t
        assert all(abs(p.check_margin_resid(t)) <= 1e-9 for t in months)
        assert tuple(p.cells[c]() for c in CHECKS) == (True, True, True)
        assert tuple(sp.cells[c]() for c in CHECKS) == (True, True, False)
    finally:
        if sec is not None:
            sec.close()
        s.close()


def test_the_one_state_data_refuses_that_s_carries_fails_s_own_checks(tmp_path):
    """An account value below 0, which ``Data`` refuses, is a state S's own checks fail.

    ``Data`` refuses an account value below 0 at the valuation date: no policy in force
    holds one.  ``ULSG_US_S`` carries one with a loan on an exhausted account, through
    the split of its credit between the unloaned and the loaned parts, ``(0 - L) x j_c +
    L x j_l``, below 0 wherever the loan's credited rate is below the declared one.  So S's
    point 4 restated by S at its month 12 with a loan of $4,000 runs its account value below
    0, and S's own roll-forward of the account value and its margin identity fail on that
    row: the state is one S cannot project either.  The generator, asked to restate the row
    in its first month below 0, writes the value as S carries it, and ``Data`` refuses the
    table naming the point and saying what to do; restated a month earlier, at 0 or more,
    it reads.
    """
    row = _s_row_in_force(tmp_path, 4, 12).assign(loan_bal_init=4000.0)
    s = _read(_s_inputs(tmp_path / "s", row), "negative_s")
    try:
        sp = _point(s, 4)
        below = [t for t in range(sp.proj_len()) if sp.av_pp_at(t, "BEF_PREM") < 0.0]
        assert below and not sp.is_lapsed(below[0]), below[:3]
        assert (sp.check_av_roll_fwd(), sp.check_margin()) == (False, False)
        first = below[0]
        for month, refused in ((first, True), (first - 1, False)):
            spec = dataclasses.replace(SPEC, derived=((4, month),), future=())
            table, _ = build_sec_table(spec, s)
            folder = _sec_inputs(tmp_path / f"sec{month}", table)
            model = _read(folder, "negative")
            try:
                label = _label(table.set_index("point_id"), "derived", 4, month)
                if refused:
                    _refused(model.Data.model_point_table,
                             f"av_pp_init must be a number, zero or more: no policy in "
                             f"force holds a negative account value, so restate a point "
                             f"with a loan on an exhausted account no later than the last "
                             f"month its account value is still zero or more; it is not at "
                             f"point_id [{label}]")
                else:
                    assert len(model.Data.model_point_table()) == len(table)
            finally:
                model.close()
    finally:
        s.close()


# Inputs at which a product or sum taken in another order than ULSG_US_S's differs in its
# last bit: an acquisition expense, a maintenance expense and a multiple of the counts that
# no binary fraction holds exactly.
ACQ, MAINT, COUNTS = 123.456, 77.7, 3.7


def test_acquisition_is_charged_on_new_business_only(tmp_path):
    """Acquisition per policy issued, in the issue month and its first year, never inflated.

    ``ULSG_US_S`` charges ``expense_acq`` per policy in the issue month and 90% of each
    first-year premium, on the count in force there, which on a point issued at the
    valuation date is the issued count, so the twins agree with S at any count, and T1
    needs no S point to count one policy.  On a copy whose counts are :data:`COUNTS` times
    the committed table's, with :data:`ACQ` and :data:`MAINT` set and inflation at the
    shipped 2.5%, a charge per model point would show beside one per policy, and an
    inflated one beside one that is not.  On every point, what ``expenses(t)`` holds beyond
    its maintenance and claim parts is ``ACQ`` per policy in the issue month,
    ``t = -duration_mth``, plus 90% of the premium in each month of the first policy year,
    and 0 in every other month to ``t = 37``, to 1e-9: the twins of S's new business bear
    it from ``t = 0``, the point issued 25 months on from ``t = 25``, where the maintenance
    part is inflated by ``1.025^2``, two valuation years on, and the acquisition is not,
    and the points already in force never, though on the valuation clock their row 0 is
    ``t = 0``.  The formula is S's, in S's order, so on the twins, read by S at the same
    counts and inputs, the expenses are S's bit for bit.
    """
    refs = {"expense_acq": ACQ, "expense_maint": MAINT}
    table = _committed()
    model = _read(_sec_inputs(tmp_path / "sec", table.assign(
        policy_count=COUNTS * table["policy_count"])), "acquisition", refs)
    s_table = _s_table()
    s = _read(_s_inputs(tmp_path / "s", s_table.assign(
        pols_if_init=COUNTS * s_table["pols_if_init"])), "acquisition_s", refs)
    try:
        read = model.Data.model_point_table()
        months = range(38)
        for key, point_id in zip(point_keys(model), read.index):
            p = projection(model, key)
            acq = [p.expenses(t) - (MAINT / 12 * p.inflation_factor(t) * p.pols_if(t)
                                    + p.expense_claim * p.pols_death(t))
                   for t in months]
            issue = -read.at[point_id, "duration_mth"]
            expected = [((ACQ if t == issue else 0.0)
                         + (p.expense_acq_prem_rate * p.premium_pp(t)
                            if 0 <= t - issue < 12 else 0.0)) * p.pols_if(t)
                        for t in months]
            assert acq == pytest.approx(expected, abs=1e-9), point_id
            assert (issue in months) == (sum(expected) > 0.0), point_id
        later = _row(model, "future", 2, -25)
        assert later.inflation_factor(25) == (1 + INFLATION) ** 2 == 1.050625
        assert later.expenses(25) == pytest.approx(
            (ACQ + later.expense_acq_prem_rate * 10800.0 * 0.98 + MAINT / 12 * 1.050625)
            * COUNTS + later.expense_claim * later.pols_death(25), rel=1e-12)
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
# mort_rate caps the annual rate at 1, as ULSG_US_S's does since USLIB-SEC-PLAN.md §8.2
# item 4's fix, so the cap is no departure.  ULSG's own mortality table is not UL's: at
# A/E 1.0, with improvement off, its StdTob class, 1.75 times the table, first passes 1 at
# attained age 107, 0.582849 x 1.75 = 1.019986, and stays past it to the end of the
# projection; with the shipped improvement it would be 111.  The committed points are all
# StdNT, and the splice's A/E of 0.56 keeps every class below 1, so neither comes near it.
# One point is made to pass it, the way the variants are made: S's point 3 in the StdTob
# class at a single premium of $300,000, which funds it past 107, on the variants' COI
# rows, alone in a copy of S's table, under the splice's References with the A/E back at
# the shipped 1.0 (CAPPED_REFS).
CAPPED = (3, {"policy_id": "GUL-900020", "rate_class": "StdTob",
              "premium_pp_ann": 300000.0})
CAPPED_REFS = {**SPLICED_REFS, "mort_ae_factor": 1.0}
CAPPED_MTH = 564        # the first month at attained age 107, where the product passes 1


def _uncapped_mort_rate(proj, t):
    """``ULSG_US_S``'s annual mortality product in month t, the one its cap bounds.

    The table's rate at the attained age, read at the table's nearest age, times the class
    factor, the A/E and the improvement factor, computed from S's own cells and tables.
    """
    table = proj.data.mort_table()
    a = min(max(proj.age(t), int(table.index.min())), int(table.index.max()))
    return (float(table.loc[a, "mort_rate"]) * proj.class_factor() * proj.mort_ae_factor
            * proj.mort_improve_factor(t))


def _sweep_months(proj):
    """Evaluate every monthly cell of an S point at every month of its frame.

    At each timing or kind it takes, as :func:`_sweep_s` reaches them, so that the cap test
    compares every monthly cell in every month the cap binds, those no report or check
    reads among them; S's funding-premium solve, which takes a premium too and which this
    model leaves to S, is not swept.
    """
    arguments = {**BY_ARGUMENT, **OPENING, "av_pp_at": AV_TIMINGS,
                 "av_at": (*AV_TIMINGS, "EOM")}
    names = sorted(_monthly_cells(proj) - set(SOLVER))
    for t in range(proj.proj_len()):
        for name in names:
            cells = proj.cells[name]
            if name in arguments:
                for label in arguments[name]:
                    cells(t, _code(proj, label))
            else:
                cells(t)


def _report_faults(p, case):
    """Where a report of ``p`` holds a value that is not a finite float, or a label column
    a value of another kind."""
    faults = []
    for report in REPORTS:
        frame = p.cells[report]()
        labels = list(LABEL_COLUMNS.get(report, ()))
        amounts = frame.drop(columns=labels)
        if not (amounts.dtypes == "float64").all():
            faults.append(f"{case}: {report} holds {dict(amounts.dtypes)}")
        if not all(math.isfinite(v) for v in amounts.to_numpy().ravel()):
            faults.append(f"{case}: {report} holds a value that is not finite")
        for column in labels:
            kinds = {type(v).__name__ for v in frame[column].tolist()}
            want = {"str"}
            if column == "status" and kinds != want:
                faults.append(f"{case}: {report}.{column} holds {kinds}, not {want}")
    return faults


def test_an_annual_mortality_past_1_is_capped_in_both_models(tmp_path):
    """Where the annual mortality product passes 1, both models' rate is 1.

    On the point of :data:`CAPPED`, ``ULSG_US_S``'s product of the table's rate, the class
    factor, the A/E and the improvement factor (:func:`_uncapped_mort_rate`) passes 1 in
    month :data:`CAPPED_MTH` and stays past it to the end of the projection, on a point the
    contract issues.  Both models cap it: ``mort_rate`` and the monthly rate,
    ``1 - (1 - q)^(1/12)``, are 1.0 in every one of those months, the float, not the int
    1, which compares equal to it, and S's are floats below 1 in every month before.  So
    every policy in force at the start of the first capped month dies in it, and none is in
    force after it.  The four reports hold finite floats alone, and the three checks hold.

    In every cell of S's this model agrees with S at every argument S cached, the capped
    months and the reports included, at 1e-9 relative with no absolute floor, because the
    count falls to 2.6e-9 by the cap's month, where the default floor of 1e-9 would compare
    it against almost nothing.  S is swept as the splice sweeps it (:func:`_sweep_s`), and
    every monthly cell in every month (:func:`_sweep_months`).

    Four rows of the point, built from S by the generator under :data:`CAPPED_REFS`:
    issued at the valuation date, compared as a new-business twin, and 25 months after it;
    restated in force in the month before the cap, opened with S's count and state there,
    and compared cell by cell as a splice row is; and restated five months into the capped
    year, opened with S's state there and one policy, since S's count there is 0.  On each,
    the rate is 1.0 from its first capped month, every policy in force there dies in it,
    and the count is 0.0 after it: a cap applied to new business alone would pass both
    comparisons, which see S's capped rate, and fail here, on the rows in force.  And the
    cap's side of its ``min`` wins, the side :data:`BOUND_ELSEWHERE` names this test for,
    which no row of the splice binds (:class:`_BoundSides`).
    """
    base, changes = CAPPED
    s = _read(_s_inputs(tmp_path / "s", _s_table().loc[[base]].assign(**changes),
                        SPLICED_EDITS), "capped_s", CAPPED_REFS)
    sec = None
    try:
        sp = _point(s, base)
        end = sp.proj_len()
        cap = next(t for t in range(end) if _uncapped_mort_rate(sp, t) > 1)
        assert (cap, sp.age(cap)) == (CAPPED_MTH, 107)
        assert _uncapped_mort_rate(sp, cap) == pytest.approx(0.582849 * 1.75, rel=1e-12)
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
        sec = _read(_sec_inputs(tmp_path / "sec", table, SPLICED_EDITS), "capped",
                    CAPPED_REFS)
        # Each row with the month its rate is first capped and, for the three S's count
        # opens, the exemptions of its comparison with S.
        rows = ((("twin", base, 0), cap, TWIN_EXEMPT),
                (("future", base, -25), cap + 25, FUTURE_EXEMPT),
                (("derived", base, cap - 1), 1, SPLICE_EXEMPT),
                (("derived", base, cap + 5), 0, None))
        faults, bounds = [], _BoundSides(sec)
        for case, first, exempt in rows:
            key = _row_key(sec, *case)
            with bounds.watch() as won:
                p = projection(sec, key)
                if exempt is not None:
                    assert _twin(sp, p, t_offset=case[2], exempt=exempt,
                                 arg_map=_issued_later, atol=0.0) == [], case
                capped = range(first, p.proj_len())
                later = range(first + 1, p.proj_len() + 1)
                for rate in (p.mort_rate, p.mort_rate_mth):
                    assert [(type(rate(t)), rate(t)) for t in capped] == (
                        [(float, 1.0)] * len(capped)), case
            assert p.pols_if(first) > 0.0 and p.pols_death(first) == p.pols_if(first), case
            assert [p.pols_if(t) for t in later] == [0.0] * len(later), case
            faults += _report_faults(p, case)
            assert tuple(p.cells[c]() for c in CHECKS) == (True, True, True), case
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


# How a NaN is sent to the cap, each a Reference set to NaN before the model computes
# anything, which runs compiled as it runs here: (case, the Reference, the first month on
# the twin of S's point 2 whose mortality it reaches).  The A/E reaches every month; the
# improvement rate from t = 12, the factor being 1.0 in the first valuation year.
NAN_CAP = [("the A/E", "mort_ae_factor", 0),
           ("the improvement rate", "mort_improve_rate_init", 12)]


@pytest.mark.parametrize("case, ref, first", NAN_CAP, ids=[c[0] for c in NAN_CAP])
def test_a_nan_that_reaches_the_cap_stays_nan(case, ref, first):
    """A NaN that reaches the cap on mortality stays NaN, and is not read as 1.

    ``min`` keeps its first argument unless a later one compares smaller, in modelx and
    compiled alike, and no comparison with NaN holds, so with its bound first the cap would
    turn a NaN into 1.0: a blank factor read as certain death, every flow finite.  It is
    written ``min(q, 1.0)``, in both models.  ``Data`` refuses a blank rate or factor as it
    reads the tables, so a NaN is sent to the cap through a Reference, in models read for
    the test (:data:`NAN_CAP`): ``mort_rate`` and ``mort_rate_mth`` are then the float NaN
    in every month in cover from the first month the Reference reaches, and a number before
    it, on the twin of S's point 2 in both models and on the row issued 25 months on, 0.0
    before its issue; improvement runs from the valuation date, so that row's mortality
    reads two valuation years' rates in its issue month, and is NaN from it.
    """
    models = []
    try:
        for name in (SEC, TWIN):
            models.append(_read(model_path(name), "nan_cap", {ref: float("nan")}))
        sec, s = models
        rows = [(_row(sec, "twin", 2, 0), 0), (_point(s, 2), 0),
                (_row(sec, "future", 2, -25), 25)]
        lost = []
        for x, issue in rows:
            start = max(issue, first)
            for t in range(x.proj_len()):
                for name in ("mort_rate", "mort_rate_mth"):
                    value = x.cells[name](t)
                    if t < issue:
                        want = value == 0.0
                    elif t < start:
                        want = type(value) is float and math.isfinite(value)
                    else:
                        want = type(value) is float and math.isnan(value)
                    if not want:
                        lost.append(f"{x.name}.{name}({t}) = {value!r}")
        assert not lost, f"the cap loses a NaN sent through {case}: {lost[:5]}"
    finally:
        for model in models:
            model.close()


# Each min or max written with its bound second that a NaN can reach, beyond the cap on
# mortality, each sent its NaN through a Reference set before the model computes anything:
# (case, the Reference, the cell that must be NaN in month 0 of the twins of S's points 1
# and 2, in both models).  The declared rate reaches the credited rate's floor at the
# guarantee, max(rate, guar_rate_mth()), which keeps the rate; the policy fee reaches the
# maintenance fee taken, min(fee, the account available), which keeps the fee; and the
# current COI scale reaches the COI taken, min(charge, the account available), which keeps
# the charge.  The floors inside them, max(AV', 0.0) and max(SG', 0.0), are written second
# too, but each feeds an outer bound written first, in S's order, the face in db_pp and
# 0.0 in each net amount at risk and in the account value's own floor, which takes a NaN,
# so a NaN reaches no cell through them; and Data's refusals keep a NaN from every input
# they read.  The lapse rate's floor and cap are written first, as S writes them.
NAN_BOUNDS = [("the credited rate's floor", "crediting_rate_curr", "inv_return_mth"),
              ("the maintenance fee taken", "expense_pol_mth", "maint_fee_taken_pp"),
              ("the COI taken", "coi_curr_factor", "coi_taken_pp")]


@pytest.mark.parametrize("case, ref, cell", NAN_BOUNDS, ids=[c[0] for c in NAN_BOUNDS])
def test_a_nan_that_reaches_a_bound_written_second_stays_nan(case, ref, cell):
    """A NaN that reaches a ``min`` or ``max`` with its bound second stays NaN, in both.

    ``min(x, bound)`` and ``max(x, bound)`` keep ``x`` unless the bound compares smaller,
    or larger, and no comparison with NaN holds, so a NaN stays NaN, where the bound first
    would turn it into the bound: a blank rate read as the guarantee, a blank fee as the
    account it may take.  ``Data`` refuses a blank value as it reads a table, so the NaN is
    sent through a Reference (:data:`NAN_BOUNDS`), and the bounded cell is then the float
    NaN in month 0, on the twins of S's points 1 and 2, in both models.
    """
    models = {}
    try:
        for name in (SEC, TWIN):
            models[name] = _read(model_path(name), "nan_bound", {ref: float("nan")})
        lost = []
        for name, model in models.items():
            for point in (1, 2):
                p = _row(model, "twin", point, 0) if name == SEC else _point(model, point)
                value = p.cells[cell](0)
                if not (type(value) is float and math.isnan(value)):
                    lost.append(f"{name} point {point}: {cell}(0) = {value!r}")
        assert not lost, f"{case} loses a NaN: {lost}"
    finally:
        for model in models.values():
            model.close()


# ---------------------------------------------------------------------------
# The tables' ends
#
# A corridor table and a mortality table shorter than the cover, each read past its ends
# at its nearest row, as ULSG_US_S reads them (USLIB-SEC-PLAN.md §7.6, Record — M4, Every
# bound binds, and Keys and clamps).  Data accepts any run of ages, and the shipped tables
# reach past every age in cover, so no other row reads their clamps: here the corridor's
# ages are cut to 61 to 94, so that attained ages below 61 read 61's 1.28, where the shipped
# table gives 1.30 at 60, and ages from 95 read 94's 1.01, where it gives 1.00; and the
# mortality table ends at 110, so that ages 111 to 120 read 110's 0.679115, below the
# shipped rates there.  Each end is on a value other than the next age's, so that a read
# of the wrong row past it changes a number.  Variant 8's single premium binds the corridor
# from its issue month, at 60, variant 7's funded account binds it from 89, past 95 too, and
# both live past 110, under the splice's References.
SHORT_CORRIDOR = (61, 94)
SHORT_MORTALITY = 110
SHORTENED = {**SPLICED_EDITS,
             "corridor_factors.csv": lambda t: t[t["age"].between(*SHORT_CORRIDOR)],
             "mort_table.csv": lambda t: t[t["age"] <= SHORT_MORTALITY]}


def _clamped(p, shipped):
    """What ``p``'s months read past each shortened table's end, and how that is read.

    ``shipped`` is ``{(file, column): the shipped column by age}``.  For each end: in every
    month in cover whose attained age is past it, the value read must be the end row's, and
    the end's name is returned where, in some such month, it differs from the shipped
    table's at that age and reaches a number, the corridor binding by the raw value it
    bounds, or a death.  Returns ``(reached, faults)``.
    """
    data, reached, faults = p.data, set(), []
    first, last, mort_last = (data.corridor_age_first(), data.corridor_age_last(),
                              data.mort_age_last())
    corridor = shipped["corridor_factors.csv", "corridor_factor"]
    mortality = shipped["mort_table.csv", "mort_rate"]
    for t in range(p.t_entry(), p.proj_len()):
        a = p.age(t)
        binds = _corridor_raw(p, t) > p.sum_assured_at(t)
        for end, past, held, shipped_value, reaches in (
                ("the corridor's first age", a < first, p.corridor_factor_at(first),
                 corridor[a], binds),
                ("the corridor's last age", a > last, p.corridor_factor_at(last),
                 corridor[a], binds),
                ("the mortality table's last age", a > mort_last,
                 p.mort_rate_base_at(mort_last), mortality[a], p.pols_death(t) > 0.0)):
            if not past:
                continue
            read = (p.corridor_factor(t) if "corridor" in end
                    else p.mort_rate_base_at(a))
            if read != held:
                faults.append(f"point {p.point_id}, t = {t}: {end} read as {read}, not "
                              f"{held}")
            if read != shipped_value and reaches:
                reached.add(end)
    return reached, faults


def test_a_table_shorter_than_the_cover_is_read_at_its_ends_in_both_models(tmp_path):
    """Past a table's first or last age each model reads its nearest row, as S does.

    ``corridor_factor_at`` clamps the attained age to the corridor table's first and last
    ages and ``mort_rate_base_at`` to the mortality table's, as ``ULSG_US_S``'s readers
    do, and on the shipped tables no age in cover is past either end but the mortality
    table's first, 45, which the splice's issue age 40 reads.  So variants 7 and 8, in a
    copy of S's table whose corridor and mortality tables are shortened at both ends of
    their cover (:data:`SHORTENED`), are read by ``ULSG_US_S`` and, as twins built by the
    generator, by this model, under the splice's References: each twin is S's point in
    every cell and every report, the checks' verdicts among them, to 1e-9 relative with no
    absolute floor; in every month in cover whose attained age is past an end, each model
    reads the end's row, and each of the three ends is read in some month where its value
    differs from the shipped table's at that age and the corridor binds, by the raw value
    it bounds, or a policy dies (:func:`_clamped`).  A clamp dropped would raise at the
    read, and one to the wrong row would part the two models.  And each of the three
    clamps' sides wins at its ``min`` or ``max``, the sides :data:`BOUND_ELSEWHERE` names
    this test for, which no row of the splice binds (:class:`_BoundSides`).
    """
    variants = {p: VARIANTS[p] for p in (7, 8)}
    rows = _s_table_with_variants(variants).loc[list(variants)]
    s = _read(_s_inputs(tmp_path / "s", rows, SHORTENED), "ends_s", SPLICED_REFS)
    sec = None
    try:
        table, _ = build_sec_table(dataclasses.replace(SPEC, derived=(), future=()), s)
        sec = _read(_sec_inputs(tmp_path / "sec", table, SHORTENED), "ends", SPLICED_REFS)
        assert (sec.Data.corridor_age_first(), sec.Data.corridor_age_last(),
                sec.Data.mort_age_first(), sec.Data.mort_age_last()) == (61, 94, 45, 110)
        shipped = {(file, column): pd.read_csv(model_path(SEC).parent / file,
                                               index_col="age")[column]
                   for file, column in (("corridor_factors.csv", "corridor_factor"),
                                        ("mort_table.csv", "mort_rate"))}
        reached, faults = set(), []
        with _BoundSides(sec).watch() as won:
            for point in variants:
                sp, p = _point(s, point), _row(sec, "twin", point, 0)
                _sweep_s(sp)
                issued = None if sp.duration_mth_init() > 0 else _issued_later
                assert _continues_s(sp, p, 0, arg_map=issued) == [], point
                found, wrong = _clamped(p, shipped)
                reached |= found
                faults += wrong
        assert not faults, faults[:5]
        assert reached == {"the corridor's first age", "the corridor's last age",
                           "the mortality table's last age"}, reached
        mine = _sides_bound_by(
            "test_a_table_shorter_than_the_cover_is_read_at_its_ends_in_both_models")
        assert len(mine) == 3
        if sys.version_info >= (3, 11):
            assert mine <= won, sorted(mine - won)
    finally:
        if sec is not None:
            sec.close()
        s.close()


# ---------------------------------------------------------------------------
# The pins


def test_each_pin_holds_in_every_month_and_alone(tmp_path):
    """Each pin applies in every month, alone, on a row in force and one issued later.

    ``ULSG_US_S``'s two pins hold in every month, where ``VUL_US_S``'s first-month pins
    keep ``t == 0``: the persistency pin replaces the persistency rate of level premiums,
    and the precision pin rounds the current and shadow COI rates to its places.  So on
    variants 10 and 11, each S's point 2 with one pin alone, read in a copy of their own at
    the shipped References, the twin, the row restated at 12 and the row issued 13 months
    on each keep the pin in every month on the books, and the other pin's rule in force:
    on variant 10 the persistency is 0.9 and the COI rates unrounded, on variant 11 the
    persistency is the shipped 0.98 for level premiums and the COI rates rounded to 2
    places.  T2 compares both variants with S cell by cell.
    """
    pinned = {p: VARIANTS[p] for p in (10, 11)}
    s = _read(_s_inputs(tmp_path / "s", _s_table_with_variants(pinned)), "pins_s")
    sec = None
    try:
        spec = dataclasses.replace(SPEC, derived=((10, 12), (11, 12)),
                                   future=((10, 13), (11, 13)))
        table, _ = build_sec_table(spec, s)
        sec = _read(_sec_inputs(tmp_path / "sec", table), "pins")
        for point, persistency, dp in ((10, 0.9, None), (11, 0.98, 2)):
            for case in (("twin", point, 0), ("derived", point, 12),
                         ("future", point, -13)):
                p = _row(sec, *case)
                assert p.has_prem_persistency_override() == (point == 10), case
                assert p.coi_rate_dp() == (-1 if dp is None else dp), case
                for t in range(p.t_entry(), p.proj_len()):
                    assert p.prem_persistency(t) == persistency, (case, t)
                    for cell, factor in (("coi_rate", p.coi_curr_factor),
                                         ("sg_coi_rate", p.coi_sg_factor)):
                        r = factor * p.coi_rate_guar(t)
                        want = r if dp is None else round(r, dp)
                        assert p.cells[cell](t) == want, (case, cell, t)
    finally:
        if sec is not None:
            sec.close()
        s.close()


# The precision pin's boundary, from both sides: S's point 2 at 0 places, the least a pin
# may be, which rounds every COI rate to a whole number per $1,000, and S's point 2 itself,
# blank, -1 in both models, which rounds none.
PRECISION_0 = {17: (2, {"policy_id": "GUL-900017", "coi_rate_dp": 0})}


def test_the_precision_pin_at_0_and_blank_is_s_pin_cell_by_cell(tmp_path):
    """The precision pin at 0 places, and blank, is ``ULSG_US_S``'s, cell by cell.

    ``coi_rate`` and ``sg_coi_rate`` round where ``coi_rate_dp() >= 0`` and not where it is
    -1, blank's sentinel, so 0, the pin's least value, is the side of the boundary that a
    test against Python's ``round`` alone, as the edges test of the in-force interface
    is, can hold to the wrong rule.  Here the twins of :data:`PRECISION_0`'s point,
    at 0 places, and of S's point 2, blank, are each compared with S's point, swept, in
    every cell of S's and every report, to 1e-9 relative with no absolute floor, the issue
    month's count before new business apart (:func:`_continues_s`,
    :func:`_issued_later`): a 0 read as exact leaves the rates unrounded and fails it.
    And each twin's ``coi_rate_dp()`` is the int S's is, of S's own type, so that an
    accessor that returns ``Data``'s numpy element, dropping its ``int()`` (R11), fails
    here, where T1 compares by value.
    """
    s = _read(_s_inputs(tmp_path / "s", _s_table_with_variants(PRECISION_0)), "dp0_s")
    sec = None
    try:
        table, _ = build_sec_table(dataclasses.replace(SPEC, derived=(), future=()), s)
        sec = _read(_sec_inputs(tmp_path / "sec", table), "dp0")
        for point, dp in ((17, 0), (2, -1)):
            sp, p = _point(s, point), _row(sec, "twin", point, 0)
            assert (type(sp.coi_rate_dp()), sp.coi_rate_dp()) == (int, dp), point
            assert (type(p.coi_rate_dp()), p.coi_rate_dp()) == (int, dp), point
            _sweep_s(sp)
            assert _continues_s(sp, p, 0, arg_map=_issued_later) == [], point
            rates = [p.coi_rate(t) for t in range(p.t_entry(), p.proj_len())]
            assert all(r % 1 == 0.0 for r in rates) == (dp == 0), point
    finally:
        if sec is not None:
            sec.close()
        s.close()


# ---------------------------------------------------------------------------
# A Reference that ships equal to another


# The shipped References a rewritten cell reads that ship equal to another and that the
# splice leaves equal, since moving one there would move the events its months are chosen
# on: grace_months, 2, which proj_len(), the grace counter and the latch read, and
# lapse_dyn_mult_guar_failed, 2.0, which the dynamic lapse multiplier reads.  The grace is
# set to three months, so that the two part, and expense inflation to 0, so that S's
# in-force point compares from t = 0 (test_s_in_force_point_is_its_twin_from_the_valuation
# _date).  The other pairs a rewritten cell reads are set apart where they are compared:
# the lifetime guarantee's age and charges_cease_age, 121, and the single premium's lapse
# factor and the guarantee-only multiplier, 0.6, in the splice (SPLICED_REFS); the A/E and
# the withdrawals' first year, 1, in the splice; the shadow account's unit expense and the
# loan rate, 0.05, in the margin identity's test; and the acquisition and claim expenses,
# 300, in the acquisition test.
APART_REFS = {"grace_months": 3, "inflation_rate": 0.0}
# The twins compared under APART_REFS, S's points that lapse, and the month each one's latch
# shuts there, a month later than at the shipped two months' grace: S's point 3, the single
# premium, never opens a grace.
APART_LAPSES = {1: 83, 2: 505, 4: 237}


def test_each_reference_that_ships_equal_to_another_is_read_as_itself():
    """A rewritten cell reads ``grace_months`` as itself, not as the multiplier equal to it.

    ``grace_months`` and ``lapse_dyn_mult_guar_failed`` both ship at 2, and the splice
    leaves both as shipped, its months being chosen on the graces and lapses they decide.
    So both models are read in place with :data:`APART_REFS` set before either computes
    anything: the twin of each of S's points that lapses is then S's point in every cell
    S evaluates, every one to 1e-9 relative with no absolute floor, points 2 and 4, issued
    at the valuation date, as T1 holds them at the shipped values, and point 1, in force
    300 months, from ``t = 0``, as the splice's twins are (:func:`_continues_s`); and on
    each the grace runs three months, its latch shutting a month later than at the
    shipped two (:data:`APART_LAPSES`).  A latch, a counter or a rule
    reading the multiplier's 2.0 for the grace's length passes every comparison at the
    shipped values and the splice's, and fails here (USLIB-SEC-PLAN.md §7.7, *Record —
    M9*, *References held to S's*).
    """
    s = _read(model_path(TWIN), "apart_s", APART_REFS)
    sec = _read(model_path(SEC), "apart", APART_REFS)
    try:
        assert all(getattr(sec.Projection, name) == value
                   for name, value in APART_REFS.items())
        found, lapses = {}, {}
        for point in APART_LAPSES:
            s_proj = _point(s, point)
            _sweep_s(s_proj)
            p = _row(sec, "twin", point, 0)
            issued = None if point in IN_FORCE else _issued_later
            lines = _continues_s(s_proj, p, 0, TWIN_EXEMPT, issued)
            if lines:
                found[point] = lines[:5]
            lapses[point] = next((t for t in range(p.proj_len() + 1) if p.is_lapsed(t)),
                                 None)
        assert not found, found
        assert lapses == APART_LAPSES, lapses
    finally:
        sec.close()
        s.close()


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
      the twin of S's point 1, in force 300 months, is 700 and evaluates ``duration_mth``
      once, where ``BasicTerm_SE``'s recursion would evaluate it at all 401 months from 0.
    * R2's recursions run forward: under modelx's recursion limit lowered to
      :data:`CALL_DEPTH`, every committed point is swept, each column in ascending ``t``.
      A forward recursion, through ``t - 1``, finds the month before already cached and
      stays shallow, which is why D3 is asserted on its own.  A backward recursion over the
      frame, through ``t + 1``, keeps every step within the look-ahead but opens a chain as
      long as the frame, which a compiled model would run on the C stack (F7), and fails
      here.
    * No projection cell reads a label accessor (``sex``, ``rate_class``,
      ``premium_type``, ``premium_mode``, ``surr_charge_id``): once every point is swept,
      none holds a key.  The decodes and the per-point joins read ``model_point()``, and
      the accessors are kept for reporting, as Phase 2 declares them (USLIB-SEC-PLAN.md
      R17).
    """
    record = sec_read[1]
    assert record["duration_mth(400)"] == 700
    assert record["keys"] == [400]
    assert not record["deep"], f"under a recursion limit of {CALL_DEPTH}: {record['deep']}"
    read = {point: labels for point, labels in record["labels"].items() if labels}
    assert not read, f"label accessors read by the sweep, by point: {read}"


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and is not repeated here.


def test_the_count_rolls_forward_through_new_business_and_decrements(sec_model):
    """The count leaves month t by its decrements alone, or all at once at a lapse.

    On every committed point and at every ``t`` of its frame, the count carried into
    ``t + 1``, ``pols_if_at(t + 1, "BEF_NB")``, is the count weighting month ``t``,
    ``pols_if(t)``, less its deaths, lapses, refunds and lapses at the end of a grace, in
    that order, exactly, or 0.0 once the latch is shut, the last row included, whose
    survivors are carried into ``t = proj_len()``.  The lapse at the end of a grace takes
    what the other three leave, so the count after it is 0.0 too.  And ``"BEF_MAT"``, the
    count before any maturity, is the ``"BEF_DECR"`` count in every month, that one
    included, ``ULSG_US_S``'s meaning, since nothing matures, and ``pols_maturity`` is 0.0.

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
    lapsing = _row(sec_model, "derived", 1, 81)
    assert lapsing.pols_lapse_grace(0) == (
        lapsing.pols_if(0) - lapsing.pols_death(0) - lapsing.pols_lapse(0)
        - lapsing.pols_rop(0)) > 0.0
    assert lapsing.is_lapsed(1) and lapsing.pols_if(1) == 0.0


def test_result_pols_is_s_report_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's, column for column, with ``pols_new_biz`` second (D5).

    T1 skips the report as a whole, because its frame has a column S's lacks (the spec's
    exempt), so it is compared here, on every twin, all at offset 0: the three of new
    business and S's point 1 in force.  Every column S's report has agrees, to 1e-9
    relative with no absolute floor, frames ending together, and ``pols_new_biz`` holds the
    count in the issue month and 0 in every other, so 0 throughout on the point in force.
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


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_table_is_what_s_generates(s_model):
    """``model_point_table_sec.csv`` is what ULSG_US_S and its table generate today.

    Every row and column, the text cells and the opening-state columns included: an edit
    to an S row the table copies or derives from, or to an S formula a row's state is read
    from, fails here until ``python tools/gen_sec_points.py ULSG_US_SEC`` regenerates it, in
    the same commit.  Text and integers compare exactly, and a float by its value, to
    1e-12, because the text the writer picks for a computed float depends on the platform's
    parser (§5.2).
    """
    assert check_generated(SEC, s_model=s_model) == []


# S's months a row may not be restated at, each after the policy's lapse: S point 1 at 82,
# the month its latch shuts, and 83; S point 2 at 504; S point 4 at 236.  And the months
# before, each in its grace with a counter of 1, which the generator builds.
LAPSED = ((1, 82), (1, 83), (2, 504), (4, 236))
IN_GRACE = ((1, 81), (2, 503), (4, 235))


def test_the_generator_refuses_a_month_after_the_lapse(s_model):
    """The spec restates no policy after its lapse, and restates one in its grace.

    The in-force interface carries no lapse latch: a policy whose grace has expired lapsed
    at the start of that month, with no value, and S's count there is 0.  So the grace
    counter's extractor refuses a month by which S's latch has shut (:data:`LAPSED`),
    naming the point and the month, rather than writing a row with no policy whose latch
    would open again; and the month before, the policy a month into its grace, is built,
    its counter S's ``grace_mth`` of the month before, 1 (:data:`IN_GRACE`).
    """
    for point, month in LAPSED:
        spec = dataclasses.replace(SPEC, derived=((point, month),), future=())
        with pytest.raises(ValueError) as excinfo:
            build_sec_table(spec, s_model)
        assert str(excinfo.value) == (
            f"ULSG_US_S point {point} has lapsed by month {month}: its grace expired, so "
            f"no policy is in force to restate"), (point, month)
    for point, month in IN_GRACE:
        spec = dataclasses.replace(SPEC, derived=((point, month),), future=())
        table, _ = build_sec_table(spec, s_model)
        row = table[table["row_kind"] == "derived"].iloc[0]
        assert (row["source_mth"], row["grace_mth_init"]) == (month, 1), (point, month)
        assert row["policy_count"] == _point(s_model, point).pols_if(month) > 0.0


def test_the_spec_keeps_each_pin_and_restates_the_grace(sec_model, s_model):
    """Each derived and future row keeps its S point's pins, and the twins S's grace.

    The two pins hold in every month, so a row restated in force or issued later keeps its
    S point's values, blank where S's are: S's point 1 has both, and its row at 81 keeps
    them, where S's points 2 to 4 have neither.  The twins' grace counter is 0, what S
    assumes at its own ``t = 0``, and the row of S point 1 at 81 carries S's
    ``grace_mth(80)``, 1.
    """
    table = sec_model.Data.model_point_table()
    s_table = s_model.Data.model_point_table()
    s_points = {policy: point for point, policy in s_table["policy_id"].items()}
    for point_id in table.index[table["row_kind"] != "twin"]:
        source = s_points[table.at[point_id, "source_policy_id"]]
        for pin in PINS:
            mine, theirs = table.at[point_id, pin], s_table.at[source, pin]
            assert (pd.isna(mine) and pd.isna(theirs)) or mine == theirs, (point_id, pin)
    twins = table[table["row_kind"] == "twin"]
    assert (twins["grace_mth_init"] == 0).all()
    grace = _label(table, "derived", 1, 81)
    assert table.at[grace, "grace_mth_init"] == _point(s_model, 1).grace_mth(80) == 1
    assert not pd.isna(table.at[grace, "prem_persistency_override"])
    assert not pd.isna(table.at[grace, "coi_rate_dp"])


# The cells the two valuation-clock inputs move on a row restated or issued later, against
# its S point at the shipped References, by design: improvement and inflation run from the
# valuation date on this model, and from S's own start on S (USLIB-SEC-PLAN.md §7.1,
# Precised at M3, item 11, as precised at M5).
MOVED_BY_THE_CLOCK = frozenset({"mort_improve_factor", "mort_rate", "mort_rate_mth",
                                "inflation_factor"})


def test_every_committed_row_continues_its_s_point(sec_model, s_model, tmp_path):
    """Each derived and future row of the committed table is its S point from its month on.

    T6 holds the committed table to what the generator makes of S, each float to 1e-12
    absolute and relative, which pins a count as small as the row's of S point 3 at 731,
    4.0e-10, only to about a quarter of a percent.  So each derived and future row is
    projected too.  At the shipped References, ``ULSG_US_S``'s improvement and inflation
    run from the valuation date on this model and from S's own start on S, so a row and its
    S point part by design in the cells those move, the counts and every counted flow
    with them.  So, on each row:

    * its count and opening state are S's own at its month, read by the spec's extractors,
      each float to 1e-12 relative, value by value;
    * it continues its S point in every value per policy, frame by frame and cell by cell,
      at no tolerance beyond 1e-9 relative and no absolute floor: ``result_av`` whole,
      ``result_guar`` but the deductions forgone in force, ``result_pols``' lapse rate, and
      every cell of S's but the spec's exemptions, the counted cells, the reports and the
      cells the two inputs move (:data:`MOVED_BY_THE_CLOCK`);
    * and the future row, read again in both models with ``inflation_rate`` and
      ``mort_improve_rate_init`` at 0 set first, continues its S point in every cell of
      S's, the counts among them, frame by frame and cell by cell, as T3 compares a future
      row.

    T2 and T3 hold the counts of restated and future rows with the two inputs neutralized.
    """
    table = sec_model.Data.model_point_table()
    s_points = {policy: point for point, policy
                in s_model.Data.model_point_table()["policy_id"].items()}
    rows = table.index[table["row_kind"] != "twin"].tolist()
    assert rows, "the committed table has no derived or future row"
    per_policy = {"result_av": None, "result_guar": PER_POLICY["result_guar"],
                  "result_pols": ("lapse_rate_mth",)}
    for point_id in rows:
        kind, month = table.at[point_id, "row_kind"], int(table.at[point_id, "source_mth"])
        theirs = _point(s_model, s_points[table.at[point_id, "source_policy_id"]])
        mine = _point(sec_model, point_id)
        if kind == "derived":
            state = {"policy_count": theirs.pols_if(month),
                     **{column: extract(theirs, month)
                        for column, extract in SPEC.state.items()}}
            for column, value in state.items():
                assert table.at[point_id, column] == pytest.approx(value, rel=1e-12,
                                                                   abs=0.0), (
                    point_id, column)
        found = []
        for report, columns in per_policy.items():
            found += frame_mismatches(theirs.cells[report](), mine.cells[report](),
                                      t_offset=month, columns=columns, atol=0.0)
        exempt = (SPLICE_EXEMPT if kind == "derived" else FUTURE_EXEMPT) | COUNTED | set(
            REPORTS) | MOVED_BY_THE_CLOCK
        found += _twin(theirs, mine, t_offset=month, exempt=exempt,
                       arg_map=None if kind == "derived" else _issued_later, atol=0.0)
        assert found == [], (point_id, found)
    neutral = {"inflation_rate": 0.0, "mort_improve_rate_init": 0.0}
    sec = _read(model_path(SEC), "neutral", neutral)
    s = _read(model_path(TWIN), "neutral_s", neutral)
    try:
        for point_id in table.index[table["row_kind"] == "future"]:
            month = int(table.at[point_id, "source_mth"])
            theirs = _point(s, s_points[table.at[point_id, "source_policy_id"]])
            _sweep_s(theirs)
            assert _continues_s(theirs, _point(sec, point_id), month, FUTURE_EXEMPT,
                                _issued_later) == [], point_id
    finally:
        s.close()
        sec.close()


# ---------------------------------------------------------------------------
# The product's own facts, on the committed model


def test_the_two_clocks_on_the_shipped_points(sec_model):
    """``t`` counts from the valuation date; ``duration_mth(t)`` from issue (D3, D4).

    On the twin of S's new business the two coincide, its policies enter as new business
    at ``t = 0``, and its frame is 732 months, to policy month 732 at attained age 121,
    where premiums and charges cease.  S's point 1 is in policy year 26 at attained age 85
    at ``t = 0``, with 432 months left, on its 25th anniversary, whose window falls at
    ``t = 0``.  The row of S point 1 at 381 is a month into its grace, ``GRACE`` at
    ``t = 0`` and ``LAPSED`` from ``t = 1``.  The row of S point 2 at 240 opens its 20th
    anniversary's window at ``t = 0``, and the row at 305, mid-year, its policy
    anniversaries at ``t = 7`` and ``t = 19``, with its account exhausted and the guarantee
    carrying it.  The row at 731 has a frame of one month, at attained age 120.  The point
    issued 25 months on has nothing in force and nothing to do before ``t = 25``, and
    before issue its policy years are -2, -1 and 0, which the guards must answer for, and
    its status ``PRE_ISSUE``.  Expense inflation is ``(1 + inflation_rate)^(t // 12)`` on
    every row alike, ``ULSG_US_S``'s step by policy year moved onto the valuation clock.

    ``pols_if_at``'s ``"BEF_NB"`` counts the policies before the month's new business, so
    in the issue month it is 0 where ``pols_if`` holds the issued count; ``"BEF_MAT"``
    keeps ``ULSG_US_S``'s meaning, that count, since nothing matures; and a timing or a
    kind the model does not know is refused by every cell that takes one, rather than
    answered with another value.
    """
    twin = _row(sec_model, "twin", 2, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 731)] == [0, 1, 731]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0), twin.pols_if(0)) == (
        0, 0.0, 1.0, 1.0)
    assert twin.charges_cease_mth() == twin.proj_len() == 732
    assert twin.is_active(731) and not twin.is_active(732)
    assert twin.pols_if_at(0, _code(twin, "BEF_MAT")) == twin.pols_if(0) == 1.0
    assert twin.pols_if_at(0, _code(twin, "BEF_NB")) == 0.0
    anchor = _row(sec_model, "twin", 1, 0)
    assert (anchor.duration_mth(0), anchor.policy_year(0), anchor.age(0),
            anchor.proj_len(), anchor.rop_anniversary(0)) == (300, 26, 85, 432, 25)
    grace = _row(sec_model, "derived", 1, 81)
    assert (grace.duration_mth(0), grace.policy_year(0), grace.age(0),
            grace.proj_len()) == (381, 32, 91, 351)
    assert [_status_is(grace, t, label) for t, label in enumerate(
        ("GRACE", "LAPSED", "LAPSED"))] == [True] * 3
    window = _row(sec_model, "derived", 2, 240)
    assert (window.policy_year(0), window.age(0), window.rop_anniversary(0),
            window.rop_ratio(0)) == (21, 80, 20, 0.5)
    mid = _row(sec_model, "derived", 2, 305)
    assert (mid.policy_year(0), mid.age(0), mid.proj_len()) == (26, 85, 427)
    assert [t for t in range(24) if mid.duration_mth(t) % 12 == 0] == [7, 19]
    assert _status_is(mid, 0, "IN FORCE - GUARANTEE")
    last = _row(sec_model, "derived", 3, 731)
    assert (last.proj_len(), last.age(0)) == (1, 120)
    fut = _row(sec_model, "future", 2, -25)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-25, 25, 757)
    assert [fut.policy_year(t) for t in range(26)] == [-2] + [-1] * 12 + [0] * 12 + [1]
    assert not any(fut.is_active(t) for t in range(25)) and fut.is_active(25)
    assert all(_status_is(fut, t, "PRE_ISSUE") for t in range(25))
    assert (fut.pols_if(24), fut.pols_new_biz(25), fut.pols_if(25), fut.premium_pp(25)) == (
        0.0, 1.0, 1.0, 10800.0 * 0.98)
    for key in point_keys(sec_model):
        p = projection(sec_model, key)
        assert all(p.inflation_factor(t) == (1 + INFLATION) ** (t // 12)
                   for t in range(p.proj_len() + 1)), key
    for name, rest in (("pols_if_at", ()), ("av_pp_at", ()), ("av_at", ()),
                       ("sg_pp_at", ()), ("loan_bal_pp_at", ())):
        _refused(lambda: twin.cells[name](0, *rest, "BEF_LUNCH"), "invalid timing")
    for name in ("claim_pp", "claims_from_av"):
        _refused(lambda: twin.cells[name](0, "LUNCH"), "invalid kind")


def test_s_in_force_point_is_its_twin_from_the_valuation_date(sec_model, s_model, tmp_path):
    """S's point 1 is its own projection in force, the worked example's months among them.

    ``ULSG_US_S`` opens its point 1 at its own ``t = 0``, 300 months in, with the account
    value, the shadow account, the loan and the premiums paid of its own columns, and with
    the grace counter at 0, which it assumes there; its twin carries those as its opening
    state and both pins.  Read in both models with ``inflation_rate`` at 0 set first, and
    improvement at its shipped 1% a year, which both run from the same instant here, the
    twin is S's point in every cell of S's and every report, nothing left out, to 1e-9
    relative with no absolute floor (:func:`_continues_s`).  So every golden of
    ``test_guaranteed_ul_us.py`` on S's point 1, the worked example's five months at
    ``t = 0..4`` and the refund capped at 40% of the face at its 25th anniversary,
    ``t = 0``, among them, holds on its twin with no number restated.  At the shipped
    References, inflation runs on the valuation clock here and by policy year in S, so the
    two part in the maintenance expense alone: in the inflation factor, the expenses, the
    expense margin and the net cash flow, and no other cell.
    """
    p, s = _row(sec_model, "twin", 1, 0), _point(s_model, 1)
    opening = (2400.0, 118000.0, 0.0, 270000.0)
    assert (p.av_pp_init(), p.sg_pp_init(), p.loan_bal_init(), p.cum_prem_init()) == opening
    assert (s.av_pp_init(), s.sg_pp_init(), s.loan_bal_init(), s.cum_prem_init()) == opening
    assert p.grace_mth_init() == 0 and p.duration_mth_init() == s.duration_mth_init() == 300
    assert (p.has_prem_persistency_override(), p.prem_persistency_override(),
            p.coi_rate_dp()) == (True, 1.0, 2)
    inflated = {"inflation_factor", "expenses", "margin_expense", "net_cf", "result_cf"}
    assert _twin(s, p, exempt=TWIN_EXEMPT | inflated, atol=0.0) == []
    apart = {name for name in inflated
             if _twin(s, p, exempt=TWIN_EXEMPT | (set(s.cells) - {name}), atol=0.0)}
    assert apart == inflated, apart
    refs = {"inflation_rate": 0.0}
    sec = _read(model_path(SEC), "twin_inflation_0", refs)
    s0 = _read(model_path(TWIN), "twin_inflation_0_s", refs)
    try:
        sp = _point(s0, 1)
        _sweep_s(sp)
        assert _continues_s(sp, _row(sec, "twin", 1, 0), 0) == []
    finally:
        s0.close()
        sec.close()


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


def test_mortality_improvement_runs_from_the_valuation_date(sec_model, s_model):
    """Mortality improves from the valuation date, the same for every row (D7).

    ``ULSG_US_S``'s improvement factor is 1.0 in the projection's first year and steps on
    each anniversary of its start, for at most 20 years, at the rate graded at the
    attained age a year before; this model keeps its formula, on ``t``, so a row in force
    takes improvement from the valuation date, what S already does for its own in-force
    point.  At the shipped References, on every committed row at every month of its frame
    and the month after it:

    * the factor is the product, over the valuation years before month ``t``, at most 20,
      of one minus the rate graded at the attained age of the month a whole number of years
      before ``t`` (:func:`_improvement_factor`), so a year accrues on each anniversary of
      the valuation date, and between them the factor moves only where a graded rate it
      reads moves with the age, at the policy's anniversaries, at ages 85 to 95;
    * and mortality is the table's rate at the attained age times the class factor, the
      A/E and that factor, capped at 1.

    So the row valued mid-year, S point 2 at 305, is not improved at its first policy
    anniversary, ``t = 7``, but at the valuation date's, ``t = 12``, and its factor moves
    again at ``t = 19``, ``24``, ``31`` and ``36``, its age at 86 to 88 a year before; the
    twins of S's points 2 and 3 and the row issued 25 months on, whose ages are below 85
    until ``t = 300``, have one factor there, 0.99 to the valuation years; and the row
    issued 25 months on dies at 0.9801 of the table's rate in its issue month, the two
    valuation years before its issue having passed, where S's point 2, issued at its own
    ``t = 0``, dies at 1.0 times it.
    """
    for key in point_keys(sec_model):
        p = projection(sec_model, key)
        table = p.data.mort_table()
        first, last = p.data.mort_age_first(), p.data.mort_age_last()
        for t in range(p.proj_len() + 1):
            assert p.mort_improve_factor(t) == _improvement_factor(p, t), (key, t)
            if not p.is_active(t):
                continue
            a = min(max(p.age(t), first), last)
            q = (float(table.loc[a, "mort_rate"]) * p.class_factor() * p.mort_ae_factor
                 * _improvement_factor(p, t))
            assert p.mort_rate(t) == min(q, 1.0), (key, t)
    mid = _row(sec_model, "derived", 2, 305)
    steps = [t for t in range(1, 40) if mid.mort_improve_factor(t)
             != mid.mort_improve_factor(t - 1)]
    assert steps == [12, 19, 24, 31, 36], steps
    assert mid.mort_improve_factor(7) == 1.0 and mid.mort_improve_factor(12) == 0.99
    rows = [_row(sec_model, "twin", 2, 0), _row(sec_model, "twin", 3, 0),
            _row(sec_model, "future", 2, -25)]
    for t in range(300):
        assert len({p.mort_improve_factor(t) for p in rows}) == 1, t
        assert rows[0].mort_improve_factor(t) == pytest.approx(
            0.99 ** min(t // 12, 20), rel=1e-12), t
    fut = rows[2]
    assert fut.mort_improve_factor(25) == pytest.approx(0.9801, rel=1e-12)
    assert _point(s_model, 2).mort_improve_factor(0) == 1.0
    assert fut.mort_rate(25) == pytest.approx(
        fut.mort_rate_base_at(60) * fut.class_factor() * 0.9801, rel=1e-12)


def _maintenance_pp(x, t):
    """The maintenance expense of month ``t`` per policy in force: the expenses less the
    claim expense on the deaths, over the count, in a month with no acquisition."""
    return (x.expenses(t) - x.expense_claim * x.pols_death(t)) / x.pols_if(t)


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date dollars, for every point alike (D7).

    ``ULSG_US_S`` inflates its maintenance expense by policy year,
    ``(1 + inflation_rate)^(policy_year - 1)``; this model by valuation year,
    ``(1 + inflation_rate)^(t // 12)``, so every point of a block steps on the valuation
    anniversaries.  So at the shipped 2.5%, S's month ``s`` and this model's month ``t``
    of the same instant, ``s = t + source_mth``, part by ``1.025`` to the policy years S
    has counted that the valuation years have not, ``(d + s) // 12 - t // 12`` on an S
    point ``d`` months in force at its own start: on the twin of S point 1, valued on its
    25th anniversary, S's maintenance per policy is this model's times ``1.025^25`` in
    every month; on the row of S point 2 at 305, mid-year, ``1.025^25`` for ``t = 0..6``,
    ``1.025^26`` for ``t = 7..11``, where S has stepped at the policy anniversary and this
    model has not, and ``1.025^25`` again at ``t = 12``, where this model steps; and on the
    row issued 25 months on, this model's is S's inflated by the valuation years that had
    passed before its issue, ``1.025^((25 + s) // 12 - s // 12)``, two or three.  Per
    policy, in every month a policy is in force on both sides after the first policy year,
    which bears acquisition, to 1e-12, on every committed row; the counts part by
    improvement, which runs from the valuation date here (the improvement test).
    """
    table = sec_model.Data.model_point_table()
    s_points = {policy: point for point, policy
                in s_model.Data.model_point_table()["policy_id"].items()}
    steps_at = {}
    for point_id in table.index:
        p = _point(sec_model, point_id)
        month = int(table.at[point_id, "source_mth"])
        sp = _point(s_model, s_points[table.at[point_id, "source_policy_id"]])
        d = sp.duration_mth_init()
        checked = 0
        for t in range(p.t_entry(), p.proj_len()):
            s = t + month
            if p.policy_year(t) < 2 or not (p.pols_if(t) > 0.0 and sp.pols_if(s) > 0.0):
                continue
            steps = (d + s) // 12 - t // 12
            steps_at[point_id, t] = steps
            assert _maintenance_pp(sp, s) == pytest.approx(
                _maintenance_pp(p, t) * (1 + INFLATION) ** steps, rel=1e-12), (point_id, t)
            checked += 1
        assert checked, point_id
    anchor = _label(table, "twin", 1, 0)
    assert {steps_at[key] for key in steps_at if key[0] == anchor} == {25}
    mid = _label(table, "derived", 2, 305)
    assert [steps_at[mid, t] for t in range(13)] == [25] * 7 + [26] * 5 + [25]
    later = _label(table, "future", 2, -25)
    assert [steps_at[later, 25 + s] for s in range(12, 24)] == [-2] * 11 + [-3]


# ---------------------------------------------------------------------------
# The premium


def test_the_premium_is_an_input_and_the_solve_stays_s(sec_model, s_model):
    """The premium is the model point's, fixed at issue; the funding-premium solve is S's.

    ``ULSG_US_S`` solves, beside its projection, the level premium that funds the shadow
    account to the guarantee age, and reads its projection's premium from the model point.
    This model has no cell of the solve (:data:`SOLVER`): the premium is an input, fixed at
    issue, as ``basiclife.BasicTerm_SE`` reads its premium from a table (USLIB-SEC-PLAN.md
    D6, §7.5).  So every committed row pays its column's premium, at its mode, times its
    persistency, in each premium month on the books, and none in any other; and S's own
    solve on its point 2 is $10,803.93, where the column, which a row in force carries
    from issue, holds $10,800.00.
    """
    assert not set(SOLVER) & set(sec_model.Projection.cells)
    assert set(SOLVER) <= set(s_model.Projection.cells)
    for key in point_keys(sec_model):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            want = 0.0
            if p.is_premium_mth(t):
                want = (p.premium_pp_ann() * p.prem_persistency(t) if p.is_single_premium()
                        else p.premium_pp_ann() / p.premium_freq() * p.prem_persistency(t))
            assert p.premium_pp(t) == want, (key, t)
    assert _row(sec_model, "twin", 2, 0).premium_pp(0) == 10800.0 * 0.98
    assert _point(s_model, 2).no_lapse_premium() == pytest.approx(10803.93, abs=0.01)
    assert _point(s_model, 2).premium_pp_ann() == 10800.0


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
    parenthesis where the notes have none (USLIB-SEC-PLAN.md §7.11, Record — M8, Docstring
    tables).
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
    an enumerator, ``(MD)``, makes of it, and which renders the cell blank; literal markup
    inside strong or emphasis, as in ``**the notes' ``AV'(t)``**``, which docutils does not
    nest, so that the backticks print; and an identifier split across the lines of a table
    cell, at an underscore or inside a literal, which renders as two words.
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


# What only ULSG_US_S's docstrings may say, each phrase a pattern with every space a \s+, so
# that one wrapped across lines still matches: a reference into its Spaces, which the SEC
# pages would link to the wrong model; its clock, t counting its own projected months from
# its start, and its frame opening at its first month; its opening at t == 0, where this
# model opens at t_entry(); its funding-premium solve, which this model leaves to it; and
# three slips of its text.  Each phrase is asserted to be one some docstring of ULSG_US_S
# says, so that none holds of nothing.
STALE_PHRASES = (
    r"~\.ULSG_US_S\.", r"\*\*policy\s+months\*\*\s+from\s+the\s+start",
    r"first\s+projected\s+month", r"projected\s+months?\b", r"projection\s+start",
    r"the\s+outset", r"first\s+month\s+of\s+the\s+frame", r"Never\s+at\s+``t\s+=\s+0``",
    r"[Pp]olicy\s+months?\s+(?:``)?t\b", r"``t\s+=\s+0``\s+is\s+the\s+issue\s+month",
    r"no_lapse_premium", r"sg_pp_solve", r"guar_min_sg", r"\bthe\s+cells\s+is\b",
    r"\bthis\s+cells\b", r"\ba\s+cells\b")
STALE = re.compile("|".join(STALE_PHRASES))


def test_the_docstrings_describe_the_valuation_clock(sec_model, s_model):
    """The docstrings say what this model is, and none says what only ULSG_US_S is.

    The model docstring names the valuation date, ``BasicTerm_SE``, the policy clock, the
    SEC table and the product.  The symbol map in the Projection docstring maps every cell
    running in force adds, which are exactly the cells ``ULSG_US_S`` lacks, and every
    opening-state column, and names nothing the model lacks: every name in it is a cell or
    a Reference; and docutils reads each of its rows into the right cells
    (:func:`_map_faults`): each row, with the lines under it whose symbol is blank, has
    text in every column, a symbol, a cell and a meaning, and no cell runs into the row
    above.  No row of a simple table in any docstring puts text between two of its columns
    (:func:`_table_overruns`), which would drop the table from the rendered page.  And no
    docstring says what :data:`STALE` matches, each of whose phrases ``ULSG_US_S``'s
    docstrings say.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE,
                   "guaranteed universal life", "shadow account"):
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
    assert not stale, f"docstrings that describe ULSG_US_S: {stale}"
    s_flat = [re.sub(r"\s+", " ", doc) for _, doc in _docs(s_model)]
    unsaid = [phrase for phrase in STALE_PHRASES
              if not any(re.search(phrase, doc) for doc in s_flat)]
    assert not unsaid, f"phrases ULSG_US_S does not say, so STALE holds nothing: {unsaid}"
    broken = ("=" * 24 + "  " + "=" * 4 + "\n(grace counter carried in) grace_mth_init\n"
              + "=" * 24 + "  " + "=" * 4 + "\n")
    assert _table_overruns(broken) == ["(grace counter carried in) grace_mth_init"]


def _doctree(core, doc, stream):
    """``doc``'s doctree, dedented as autodoc dedents it and its Sphinx roles read as plain
    interpreted text, which docutils alone does not know; its warnings go to ``stream``."""
    return core.publish_doctree(re.sub(r":[a-z]+:`", "`", inspect.cleandoc(doc)),
                                settings_overrides={"report_level": 2, "halt_level": 5,
                                                    "warning_stream": stream})


@pytest.mark.docutils
def test_the_docstrings_parse_as_rst(sec_model, s_model):
    """Every docstring of the model parses as reStructuredText, and renders as written.

    The docs build reads each docstring through docutils, which reports a malformed table, a
    bad indentation or an unclosed inline markup and drops what it cannot read; a raw-text
    test sees none of it.  Each docstring, dedented as autodoc dedents it and its Sphinx
    roles read as plain interpreted text, is parsed here (:func:`_doctree`), and any
    warning or error is a fault.  So is what docutils reads into the wrong markup without a
    warning (:func:`_doctree_faults`): a list in a table cell, literal markup inside strong
    or emphasis, and an identifier split across a table cell's lines.  ``ULSG_US_S``'s
    docstrings hold the first two, which this model's text corrects: the symbol map's
    ``(MD)``, an enumerator to docutils, and three literals in bold, the Space's ``t = 0``
    and the notes' ``AV'(t)`` and ``SG'(t)``, so the check is asserted to find those four
    there, and the third kind in a table made for it.  docutils comes with the docs build,
    not with the models' requirements, so the test is skipped where it is absent; the
    column checks in the test above run everywhere.
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
    assert s_faults == [("Projection", "a list in a table cell"),
                        ("Projection", "literal markup inside strong"),
                        ("Projection.av_pp_at", "literal markup inside strong"),
                        ("Projection.sg_pp_at", "literal markup inside strong")], s_faults
    split = "\n".join(("=====  ======", "Sym    Cells", "=====  ======", "x      ``AFT_",
                       "       WD``", "y      pols_", "       if", "=====  ======"))
    assert [fault.split(":")[0] for fault in _doctree_faults(
        _doctree(core, split, io.StringIO()))] == [
        "an identifier split across a table cell's lines"] * 2


def _values(refs):
    """The values of ``refs``, a Space's References, each as it compares: a module by its
    name; the Interface to the other Space left out."""
    return {name: value.__name__ if inspect.ismodule(value) else value
            for name, value in refs.items() if name != "data"}


# The References this model adds to ULSG_US_S's, on Data, the horizon of future business
# (D4) and numpy, for the vectors (R5), and on Projection, Phase 2's: the position idx, the
# codes of the timings, kinds and statuses (R9, R10) and the youngest issue age the
# caches are sized from; and those it leaves out, on Projection: the funding-premium
# solve's tolerance and its limit of doublings, the solve staying ULSG_US_S's (the spec's
# exempt), the math module, which S's checks alone call, for math.isclose, where this
# model's checks read residual cells instead, and point_id, which idx replaces.
TIMING_CODES = ("BEF_NB", "BEF_DECR", "BEF_MAT", "BEF_PREM", "BEF_WD", "BEF_FEE", "BEF_COI",
                "BEF_INV", "EOM", "BEF_INT")
KIND_CODES = ("DEATH", "LAPSE", "REFUND", "GRACE", "WITHDRAWAL", "MATURITY")
STATUS_CODES = ("PRE_ISSUE", "IN_FORCE", "IN_FORCE_GUARANTEE", "GRACE", "LAPSED", "CEASED")
ADDED_REFERENCES = {
    "Projection": {"idx": 0, **{c: i for i, c in enumerate(TIMING_CODES)},
                   **{c: i for i, c in enumerate(KIND_CODES)},
                   **{c: i for i, c in enumerate(STATUS_CODES)}, "issue_age_min": 18},
    "Data": {"future_horizon_mth": 120, "np": "numpy"}}
DROPPED_REFERENCES = {"Projection": ("solve_tol", "solve_max_doublings", "math",
                                     "point_id"),
                      "Data": ()}


def test_the_sec_model_reads_the_s_tables_in_place(sec_model, s_model):
    """One copy of each assumption table serves both models (D1), on S's own References.

    The two ``input_dir()`` s are one directory, and SEC's filename References are S's with
    ``model_point_file`` alone changed, to ``model_point_table_sec.csv``: an edit to a table
    reaches both models, and the two can never drift apart.  And every other Reference of
    either Space is S's, value for value, but those this model adds and those it leaves
    out with the solve (:data:`ADDED_REFERENCES`, :data:`DROPPED_REFERENCES`): a constant
    copied wrong that changes no number a comparison reads, a lapse rate's cap of 0.4 for
    S's 0.5, which no shipped or spliced rate meets, would otherwise pass every test whose
    rows never reach it (USLIB-SEC-PLAN.md §7.7, *Record — M9*, *References held to S's*).
    """
    assert sec_model.Data.input_dir() == s_model.Data.input_dir()
    files = {r: v for r, v in s_model.Data.refs.items() if r.endswith("_file")}
    assert {r: v for r, v in sec_model.Data.refs.items() if r.endswith("_file")} == {
        **files, "model_point_file": TABLE}
    for space in ("Projection", "Data"):
        theirs = _values(s_model.spaces[space].refs)
        mine = _values(sec_model.spaces[space].refs)
        assert set(DROPPED_REFERENCES[space]) <= set(theirs), space
        theirs = {name: value for name, value in theirs.items()
                  if name not in DROPPED_REFERENCES[space]}
        if space == "Data":
            theirs["model_point_file"] = TABLE
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
    return (f"in force {_months(d)}: policy year {p.policy_year(0)}, attained age "
            f"{p.age(0)}, {p.pols_if(0):.6f} in force, account value "
            f"{p.av_pp_init():,.2f}, shadow account {p.sg_pp_init():,.2f}, loan "
            f"{p.loan_bal_init():,.2f}, premiums paid {p.cum_prem_init():,.2f}, "
            f"{_months(p.grace_mth_init())} in grace")


def _heading(point, origin, guarantee=121, premium="LEVEL", amount=10800.0):
    """``run_sec.py``'s first line for a committed point of S's anchor cell."""
    return (f"model point {point}: {origin} - M60 StdNT face 500,000 guarantee to age "
            f"{guarantee} {premium}, premium {amount:,.2f}/yr mode A")


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
    name the label too: ``Data``'s of a malformed row, and ``proj_len()``'s of a point whose
    grace has expired, which ``run_sec.py --block`` meets before it projects any point.  On
    S's in-force row ``source_mth`` is 0 and ``duration_mth`` 300, so a formula that read
    the one for the other would pass every test that leaves ``duration_mth`` as generated
    but this one.
    """
    extract = _committed().drop(columns=list(GENERATED_COLUMNS))
    extract.index = pd.Index(extract.index + 100, name="point_id")
    extract = extract.iloc[::-1]
    folder = _sec_inputs(tmp_path / "extract", extract)
    model = _read(folder, "extract")
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
    out = _run_sec(runner, "105")
    assert out.splitlines()[:2] == [
        _heading(105, "GUL-000001-M81"),
        f"at the valuation date: {_standing(_row(sec_model, 'derived', 1, 81))}"]
    for label in ("5", "x"):
        done = _run_sec(runner, label, check=False)
        errors = done.stderr.decode(errors="replace")
        assert done.returncode == 1 and done.stdout == b"", label
        assert (f"no model point {label} in the table: {list(range(109, 100, -1))}"
                in errors and "Traceback" not in errors), errors
    model = _read(_sec_inputs(tmp_path / "negative", _set("loan_bal_init", [101], -1.0)(
        extract)), "negative_loan")
    try:
        _refused(model.Data.model_point_table,
                 "loan_bal_init must be a number, zero or more; it is not at point_id "
                 "[101]")
    finally:
        model.close()
    moved = _sec_inputs(tmp_path / "moved", _set("grace_mth_init", [105], 2)(extract))
    message = ("point_id 105: grace_mth_init 2 is at or past grace_months, 2: the grace "
               "expired before the valuation date, so the policy lapsed then, with no "
               "value")
    model = _read(moved, "moved")
    try:
        _refused(_point(model, 105).proj_len, message)
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
    the model's.  The runner's default is S's point 1, in force 300 months, whose rows
    ``t = 0..4`` are the worked example's five months: its lines at the valuation date, each
    asserted whole, so that a longer number cannot pass for the one asserted, and its first
    twelve rows of cash flows, of the account value and the shadow account, of the
    guarantee's diagnostics and of counts, the account value's and the guarantee's
    ``ULSG_US_S``'s own, row for row, since the point is S's point 1, and the cash flows
    but for the maintenance expense, which is in valuation-date dollars here.  Point 5,
    restated in force at S's month 81 of S's point 1, a month into its grace, and point 9,
    to be issued 25 months on, each with the two lines that say where its row came from and
    where it stands, which only the committed table's generator columns can say.  And the
    block: a line for each of the nine points, in table order, its first twelve rows, which
    must be the committed points' frames summed row by row, as this test sums them, and
    those frames summed into projection years, each year's count the one in force in its
    first month.  Nothing else runs the runner on the committed table.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    anchor, s_anchor = _row(sec_model, "twin", 1, 0), _point(s_model, 1)
    out = _run_sec(runner)
    assert out.splitlines()[:3] == [
        _heading(1, "GUL-000001 (S's GUL-000001)"),
        f"at the valuation date: {_standing(anchor)}",
        "proj_len = 432 months from the valuation date (t = 0..431); the projection ends "
        "at policy month 732, attained age 121, where premiums and charges cease"]
    for report, digits in (("result_cf", 2), ("result_av", 2), ("result_guar", 2),
                           ("result_pols", 6)):
        assert anchor.cells[report]().head(12).round(digits).to_string() in out, report
    for report in ("result_av", "result_guar"):
        assert s_anchor.cells[report]().head(12).round(2).to_string() in out, report
    mine, theirs = anchor.result_cf().head(12), s_anchor.result_cf().head(12)
    shared = [c for c in theirs.columns if c not in ("expenses", "net_cf")]
    assert frame_mismatches(theirs, mine, columns=shared, rtol=0.0, atol=0.0) == []
    assert (mine["expenses"] < theirs["expenses"]).all()
    for point, kind, s_point, month, origin in (
            ("5", "derived", 1, 81, "GUL-000001-M81 (S's GUL-000001 at its month 81)"),
            ("9", "future", 2, -25,
             "GUL-000002-F25 (S's GUL-000002, issued 25 months on)")):
        p = _row(sec_model, kind, s_point, month)
        assert _run_sec(runner, point).splitlines()[:2] == [
            _heading(point, origin), f"at the valuation date: {_standing(p)}"], point
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


def _references(space):
    """The References a space's ``__init__.py`` assigns, a name to a literal value."""
    source = (model_path(SEC) / space / "__init__.py").read_text(encoding="utf-8")
    return {node.targets[0].id: node.value.value for node in ast.parse(source).body
            if isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Constant)}


def _status_labels():
    """``result_av``'s status labels, by code: the tuple of text its formula indexes."""
    source = (model_path(SEC) / "Projection" / "__init__.py").read_text(encoding="utf-8")
    cell = next(node for node in ast.parse(source).body
                if isinstance(node, ast.FunctionDef) and node.name == "result_av")
    found = [node for node in ast.walk(cell) if isinstance(node, ast.Tuple)
             and node.elts and all(isinstance(e, ast.Constant) and isinstance(e.value, str)
                                   for e in node.elts)]
    assert len(found) == 1, ast.dump(cell)
    return tuple(e.value for e in found[0].elts)


def _same_float(a, b):
    """Whether ``a`` and ``b`` are the same float, its type and the sign of a zero
    included: the comparison ``float.hex`` makes."""
    return type(a) is float and type(b) is float and a.hex() == b.hex()


# The months of the committed points in which all three kinds pay together, a death, a
# surrender and a refund, each on a return-of-premium anniversary in the window, and the
# months among them in which a total summed left to right from 0.0 is not S's sum
# (measured at M18).  The second figure is what makes the split test able to fail.
THREE_KINDS, THREE_KINDS_APART = 8, 3
SPLIT = (("claims_death", "DEATH"), ("claims_lapse", "LAPSE"),
         ("claims_refund", "REFUND"))


def test_the_claims_total_is_s_sum_bit_for_bit(sec_model, s_model):
    """``claims(t)`` is ``ULSG_US_S``'s total, bit for bit, and each kind is S's (R12).

    S's ``claims(t, kind=None)`` is the kinds and their total in one cell, the total a
    ``sum`` of a generator over DEATH, LAPSE, REFUND and GRACE, which is 0.0.  Here the
    kinds are ``claims_death``, ``claims_lapse`` and ``claims_refund``, and the total is
    that ``sum`` written out: Python's float ``sum`` is compensated from 3.12, and all three
    kinds pay in a month of a return-of-premium window, where a sum from left to right
    loses a last bit S keeps.  T1 reaches S's total through the spec's ``twin_arg_map`` to
    its tolerance, and skips S's keys of a kind, so they are held here, exactly: on the
    twins of S's four points, which S opens at its own ``t = 0``, in every month of the
    frame, the total equal to S's, its type and the sign of a zero included, and each kind
    equal to S's ``claims(t, kind)``.  And on every committed point, in each of the
    :data:`THREE_KINDS` months in which all three kinds pay, which must be there, the total
    is the ``sum`` of its kinds, as S sums them, and in :data:`THREE_KINDS_APART` of them a
    total written ``0.0 + d + l + r`` is not: a total so written fails here.
    """
    found = []
    for point in (*IN_FORCE, *NEW_BUSINESS):
        mine, theirs = _row(sec_model, "twin", point, 0), _point(s_model, point)
        assert mine.proj_len() == theirs.proj_len()
        for t in range(mine.proj_len()):
            got, want = mine.claims(t), theirs.claims(t)
            if not _same_float(got, want):
                found.append(f"point {point}: claims({t}) {got!r}, S's {want!r}")
            for cell, kind in SPLIT:
                if not _same_float(mine.cells[cell](t), theirs.claims(t, kind)):
                    found.append(f"point {point}: {cell}({t}) is not S's "
                                 f"claims({t}, {kind!r})")
    three, apart = [], []
    for key, label in zip(point_keys(sec_model), sec_model.Data.model_point_table().index):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            parts = [p.cells[cell](t) for cell, _ in SPLIT]
            if not all(parts):
                continue
            three.append((label, t))
            total = p.claims(t)
            if not _same_float(total, sum((*parts, 0.0))):
                found.append(f"point {label}: claims({t}) {total!r} is not the sum of "
                             f"{parts}")
            if 0.0 + parts[0] + parts[1] + parts[2] != total:
                apart.append((label, t))
    assert not found, found[:20]
    assert (len(three), len(apart)) == (THREE_KINDS, THREE_KINDS_APART), (three, apart)


# The month at which the parts are set on the worked example's twin and S's point 1, and
# the parts set there, by (case, the three kinds' values, S's total of them): three
# negative zeros, whose sum from S's int 0 is a positive zero, and parts whose sum from left
# to right loses the 1.0 that Python's compensated sum keeps.
PARTS_MONTH = 5
SET_PARTS = [("three negative zeros", (-0.0, -0.0, -0.0), 0.0),
             ("a part a sum from left to right loses", (1e16, 1.0, -1e16), 1.0)]


@pytest.mark.parametrize("case, parts, total", SET_PARTS, ids=[c[0] for c in SET_PARTS])
def test_the_claims_total_sums_any_parts_as_s_sum_does(case, parts, total):
    """``claims(t)`` sums any three kinds as S's ``sum`` does, the sign of a zero included.

    No committed month has kinds that tell the compensated sum from a plain one by more
    than a last bit, nor negative zero kinds.  So, on a read of each model of its own, the
    worked example's twin's three kinds at :data:`PARTS_MONTH` are set as modelx input
    values, and S's ``claims(t, kind)`` of its point 1 in the same month to the same
    (:data:`SET_PARTS`): each total must be S's, a float, its sign included.  S's ``sum``
    starts from the int 0, so three negative zeros total ``0.0``, which a total without its
    ``0.0`` start would make ``-0.0``; and ``1e16``, ``1.0`` and ``-1e16`` total ``1.0``,
    which a total written from left to right would make ``0.0``.  The values are set before
    anything is computed, on models read for the test (K7).
    """
    s = _read(model_path(TWIN), "s_parts")
    sec = _read(model_path(SEC), "parts")
    try:
        theirs, mine = _point(s, 1), _row(sec, "twin", 1, 0)
        for (cell, kind), value in zip(SPLIT, parts):
            theirs.claims[PARTS_MONTH, kind] = value
            mine.cells[cell][PARTS_MONTH] = value
        totals = (theirs.claims(PARTS_MONTH), mine.claims(PARTS_MONTH))
    finally:
        sec.close()
        s.close()
    for got in totals:
        assert _same_float(got, total), (case, totals)


def test_the_codes_are_dense_and_grace_is_one_code(sec_model):
    """The timings, kinds and statuses are numbered from 0, and ``GRACE`` is one Reference.

    R9 and R10: the timings one numbering for the count's three, the accounts' six and
    the loan's one, ``BEF_NB`` 0 to ``BEF_INT`` 9; the kinds ``DEATH`` 0 to ``MATURITY``
    5; and the statuses ``PRE_ISSUE`` 0 to ``CEASED`` 5, each dense, so that every cache
    of a code is as wide as its family and no wider (``spec_sec.py``).  S spells a claim
    kind and a status alike, ``"GRACE"``, and one Reference serves both, 3 in each family,
    assigned once.  S's two status labels with spaces map to ``IN_FORCE`` and
    ``IN_FORCE_GUARANTEE`` by :func:`_code`'s rule, and ``result_av`` writes, at each code,
    the label S writes for that status, so that a code numbered off by one, or a label put
    at another's code, fails here.
    """
    refs = _references("Projection")
    for family in (TIMING_CODES, KIND_CODES, STATUS_CODES):
        assert [refs[code] for code in family] == list(range(len(family))), family
    assert KIND_CODES.index("GRACE") == STATUS_CODES.index("GRACE") == refs["GRACE"]
    source = (model_path(SEC) / "Projection" / "__init__.py").read_text(encoding="utf-8")
    assert len(re.findall(r"^GRACE = ", source, re.M)) == 1
    labels = _status_labels()
    p = _row(sec_model, "twin", 1, 0)
    for label in ("PRE_ISSUE", "IN FORCE", "IN FORCE - GUARANTEE", "GRACE", "LAPSED",
                  "CEASED"):
        code = _code(p, label)
        assert type(code) is int and labels[code] == label, (label, code, labels)


def test_status_is_a_code_and_the_report_keeps_s_labels(sec_model, s_model):
    """``status(t)`` is an int code, and ``result_av`` holds S's labels (R10).

    ``status`` is exempt from T1, since ``codes`` cannot map S's labels with spaces
    (``sec_support.SEC_SPECS``), so it is held here.  On the twins of S's four points, in
    every month, ``status(t)`` is the code of S's ``status(t)`` and ``result_av()``'s
    column is S's, label for label.  On every committed point, in every month and the
    month after the frame, ``status(t)`` is an int among the six codes, ``PRE_ISSUE``
    before issue and ``CEASED`` from the month the projection ends, and ``result_av`` the
    label of each month's code.
    """
    labels = _status_labels()
    for point in (*IN_FORCE, *NEW_BUSINESS):
        mine, theirs = _row(sec_model, "twin", point, 0), _point(s_model, point)
        for t in range(mine.proj_len()):
            assert mine.status(t) == _code(mine, theirs.status(t)), (point, t)
        assert mine.result_av()["status"].tolist() == theirs.result_av()[
            "status"].tolist(), point
    for key in point_keys(sec_model):
        p = projection(sec_model, key)
        codes_ = [p.status(t) for t in range(p.proj_len() + 1)]
        assert all(type(c) is int and 0 <= c < len(labels) for c in codes_), key
        assert all(c == p.PRE_ISSUE for c in codes_[:p.t_entry()]), key
        assert codes_[-1] == p.CEASED, key
        assert p.result_av()["status"].tolist() == [labels[c] for c in codes_[:-1]], key


def test_the_spec_sizes_each_cache_as_its_comment_derives():
    """``spec_sec.py`` gives each cache the size its comment derives from the contract.

    The spec check, C3, holds the compiled caches to the spec, and C4 at the contract's
    extremes holds the spec to the largest argument a projection reads; neither sees a
    size one above the need, which keeps the headroom and reads the same numbers, nor the
    headroom dropped.  So this reads the spec as mx2cy does, and the bounds of the
    contract from the model's own References, and holds each size to the comment's
    derivation from them: ``t`` to ``12 * (charges_cease_age - issue_age_min) + the
    horizon + 2``, ``y`` to ``charges_cease_age - issue_age_min + 2`` and ``a`` to
    ``charges_cease_age + 1``, and the timing and kind caches to ``t`` by one inner width,
    the timings' count, which the kinds fit in (§7.2, *For M16 and later*).  A change to a
    bound or a size is derived again in the comment and here.
    """
    source = (model_path(SEC).parent / "spec_sec.py").read_text(encoding="utf-8")
    comment = " ".join(line.lstrip("# ") for line in source.splitlines()
                       if line.startswith("#"))
    for formula in ("needs t raised to 12 * (charges_cease_age - issue_age_min) + the "
                    "horizon + 2",
                    "needs y raised to charges_cease_age - issue_age_min + 2",
                    "needs a raised to charges_cease_age + 1"):
        assert formula in comment, formula
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    proj, data = _references("Projection"), _references("Data")
    low, cease, horizon = (proj["issue_age_min"], proj["charges_cease_age"],
                           data["future_horizon_mth"])
    width = len(TIMING_CODES)
    assert len(KIND_CODES) <= width
    t = 12 * (cease - low) + horizon + 2
    assert sizes == {"t": t, ("t", "timing"): (t, width), ("t", "kind"): (t, width),
                     "y": cease - low + 2, "a": cease + 1}, sizes


def test_the_sample_raises_the_recursion_limit_its_comment_derives():
    """``sample_sec.py`` sets the recursion limit its comment derives, before the import.

    The export does not raise the recursion limit as modelx does (F7), so the sample sets
    it, and its comment records the measured need: a cold ``net_cf`` in the last month of
    the longest frame, issue age 18 issued 120 months on, needs a limit of 2,526 in the
    export, and the reports the sample runs in ascending ``t``, the export's import among
    the frames they run under, 128.  The limit is four times the first, rounded up to the
    thousand.  No build can tell a lower limit: the reports alone need 128, so a limit of
    1,000 builds the same model.  So this holds the limit, read from the sample's code, to
    the value derived from its comment's need, and holds the call before the import of the
    export.  A change to the need is measured again and written in the comment.
    """
    source = (model_path(SEC).parent / "sample_sec.py").read_text(encoding="utf-8")
    comment = " ".join(line.lstrip("# ") for line in source.splitlines()
                       if line.startswith("#"))
    need = re.search(r"needs a limit of ([\d,]+) in the export", comment)
    reports = re.search(r"ascending t, need ([\d,]+)", comment)
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


# The extract's labels, in the order its rows are written: the committed table's point_id
# plus 100, row 9 first, so that a label read as a position, or as a position plus one,
# names another point.
EXTRACT_LABELS = list(range(109, 100, -1))


def _extract():
    """The committed table as an administration extract would hold it: without the
    generator's columns, and labelled :data:`EXTRACT_LABELS`, row 9 first."""
    extract = _committed().drop(columns=list(GENERATED_COLUMNS)).iloc[::-1]
    extract.index = pd.Index(EXTRACT_LABELS, name="point_id")
    return extract


# The reads below a table on the committed inputs, as (cell, arguments, the message after
# the point's label): a policy year below 1, where ULSG_US_S's .loc raised KeyError, which
# the reader refuses before it reads its padded array; an attained age below the point's
# COI scale, the anchor cell's from 45, where S's .loc raised KeyError; and a completed
# year that is no anniversary of the return-of-premium table, which S's .loc refused, by
# the two readers of its terms.  A year below 0 is past the compiled cache, and is
# COMPILED_ONLY's.
_NO_COI = "coi_rates.csv has no rate for the point's sex and rate_class at attained age {}"
BEYOND = [
    ("lapse_rate_base_py", (0,), "lapse_table.csv has no rate for policy year 0"),
    ("lapse_rate_base_py", (-1,), "lapse_table.csv has no rate for policy year -1"),
    ("coi_rate_guar_at", (44,), _NO_COI.format(44)),
    ("coi_rate_guar_at", (0,), _NO_COI.format(0)),
    ("rop_ratio_anniv", (3,), "rop_table.csv has no anniversary 3"),
    ("rop_rate_anniv", (3,), "rop_table.csv has no anniversary 3"),
    ("rop_ratio_anniv", (0,), "rop_table.csv has no anniversary 0"),
    ("rop_rate_anniv", (26,), "rop_table.csv has no anniversary 26"),
]


def test_every_padded_array_holds_nan_and_no_reader_reads_it(sec_model, tmp_path):
    """The padding is NaN, the readers refuse a key below a table, by name (§7.1 item 9).

    Each reader of a padded table refuses a key below it (:data:`BEYOND`), naming the
    point by its label, on the extract labelled otherwise than by position, where a label
    read as ``idx + 1`` would name another: a policy year below 1, an attained age below
    the point's COI scale and a year that is no anniversary of the return-of-premium
    table, which ``is_rop_anniv`` answers False, below 0 and past the table's last
    anniversary too.  A year past the lapse table reads its last row, an age past the COI
    scale its last age, and an age outside the corridor and mortality tables the nearest
    row, as ``ULSG_US_S`` reads them.

    The padding is NaN, as the ``Data`` docstrings say, so that a read past a check, were
    one lost, would make every number after it NaN rather than another key's value: row 0
    of the COI scale and every age outside each schedule's own; the ages below each age
    table's first; year 0 of the lapse table; and the return-of-premium terms at every
    year that is no anniversary, where the flag array holds 0 and holds 1 at each
    anniversary.  And the pins, a value array and a flag (R8): the persistency pin is NaN
    exactly where its column is blank and its flag 0 there and 1 elsewhere, the precision
    -1 where blank; on every committed point ``prem_persistency_override()`` is NaN where
    the point has no pin and the column's value where it has, and
    ``prem_persistency(t)`` reads the pin only where its flag is set.
    """
    extract = _extract()
    label = extract.index[0]
    model = _read(_sec_inputs(tmp_path / "extract", extract), "beyond")
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
        data = model.Data
        anniversaries = set(data.rop_table().index)
        assert [y for y in range(-2, 110) if p.is_rop_anniv(y)] == sorted(anniversaries)
        assert p.lapse_rate_base_py(500) == p.lapse_rate_base_py(data.lapse_last_year())
        assert p.coi_rate_guar_at(500) == p.coi_rate_guar_at(p.coi_rate_last_age())
        assert p.corridor_factor_at(0) == p.corridor_factor_at(data.corridor_age_first())
        assert p.corridor_factor_at(500) == p.corridor_factor_at(data.corridor_age_last())
        assert p.mort_rate_base_at(0) == p.mort_rate_base_at(data.mort_age_first())
        assert p.mort_rate_base_at(500) == p.mort_rate_base_at(data.mort_age_last())
        coi, first, last = (data.coi_rate_array(), data.coi_rate_first_ages(),
                            data.coi_rate_last_ages())
        assert np.isnan(coi[0]).all() and first[0] == last[0] == 0
        for s in range(1, data.coi_schedules() + 1):
            assert not np.isnan(coi[s, first[s]:last[s] + 1]).any(), s
            assert np.isnan(coi[s, :first[s]]).all(), s
            assert np.isnan(coi[s, last[s] + 1:]).all(), s
        for array, start in ((data.lapse_rate_array(), 1),
                             (data.corridor_factor_array(), data.corridor_age_first()),
                             (data.mort_table_array(), data.mort_age_first())):
            assert np.isnan(array[:start]).all() and not np.isnan(array[start:]).any()
        flags = data.rop_anniv_flags()
        held = np.array([y in anniversaries for y in range(len(flags))])
        assert flags.dtype == "int64" and (flags == held).all()
        for array in (data.rop_ratio_array(), data.rop_rate_array()):
            assert np.isnan(array[~held]).all() and not np.isnan(array[held]).any()
        column = data.model_point_table()["prem_persistency_override"]
        values, pinned = (data.prem_persistency_override(),
                          data.has_prem_persistency_override())
        assert (np.isnan(values) == column.isna().to_numpy()).all()
        assert (pinned == column.notna().to_numpy()).all() and pinned.dtype == "int64"
        assert (data.coi_rate_dp() == data.model_point_table()["coi_rate_dp"].fillna(
            -1).to_numpy()).all()
    finally:
        model.close()
    table = sec_model.Data.model_point_table()
    assert table["prem_persistency_override"].isna().any()
    assert table["prem_persistency_override"].notna().any()
    for key, label in zip(point_keys(sec_model), table.index):
        p, pin = projection(sec_model, key), table.at[label, "prem_persistency_override"]
        if pd.isna(pin):
            assert not p.has_prem_persistency_override(), label
            assert math.isnan(p.prem_persistency_override()), label
        else:
            assert p.has_prem_persistency_override(), label
            assert p.prem_persistency_override() == pin, label
        active = [t for t in range(p.proj_len()) if p.is_active(t)]
        assert all(math.isfinite(p.prem_persistency(t)) for t in active), label


def _coi_out_of_order(rates):
    """:func:`_coi_rates_with_variants`' copy, every line in reverse key order.

    Six schedules, numbered by key F PNT, M PPlusNT, M PTob, M StdNT, M StdPlusNT and M
    StdTob, each with rates of its own; the test's points read the first, the fourth and
    the last, so that two schedules no point reads lie between schedules points read.
    """
    return _coi_rates_with_variants(rates).iloc[::-1].reset_index(drop=True)


def test_the_coi_schedules_are_numbered_by_key_whatever_the_file_order(tmp_path):
    """The COI schedules are numbered in their keys' order, not the file's (§7.3 item 4).

    ``coi_schedules()`` counts the ``(sex, rate_class)`` scales, ``coi_schedule()`` gives
    each point its scale's number and ``coi_rate_array``, ``coi_rate_first_ages`` and
    ``coi_rate_last_ages`` are by number; all four number the scales in sorted key order.
    The shipped table holds one scale, so file order and key order agree there, and a
    cell that numbered in file order would read the same numbers; C4 compares the compiled
    model with modelx, which share ``Data``'s numbering, so it cannot see one either.  So
    on a copy written in reverse key order, with scales no point reads between those
    points read (:func:`_coi_out_of_order`), and points of three scales, each point's row
    of each array is its own scale's, read from the file by key; and each point's
    guaranteed rate in its first month is the file's at its attained age.
    """
    committed = _committed()
    table = _both(_set("sex", [2], "F"), _set("rate_class", [2], "PNT"),
                  _set("rate_class", [3], "StdTob"))(committed)
    model = _read(_sec_inputs(tmp_path, table, {"coi_rates.csv": _coi_out_of_order}),
                  "coi_order")
    try:
        data = model.Data
        written = pd.read_csv(data.input_dir() / "coi_rates.csv")
        keys = sorted(set(zip(written["sex"], written["rate_class"])))
        assert list(dict.fromkeys(zip(written["sex"], written["rate_class"]))) == (
            keys[::-1])
        assert data.coi_schedules() == len(keys) == 6
        schedules = data.coi_schedule()
        coi, first, last = (data.coi_rate_array(), data.coi_rate_first_ages(),
                            data.coi_rate_last_ages())
        for label, s in zip(table.index, schedules):
            key = (table.at[label, "sex"], table.at[label, "rate_class"])
            assert s == keys.index(key) + 1, (label, s, key)
            mine = written[(written["sex"] == key[0]) & (written["rate_class"] == key[1])]
            rates = mine.set_index("age")["coi_rate_guar_ann"].sort_index()
            assert (first[s], last[s]) == (rates.index.min(), rates.index.max()), label
            assert np.array_equal(coi[s, rates.index.to_numpy()], rates.to_numpy()), label
            p = _point(model, label)
            t = p.t_entry()
            assert p.coi_rate_guar(t) == rates[p.age(t)] / 12, label
        assert sorted(set(schedules)) == [1, 4, 6]
    finally:
        model.close()


# What Data cannot number or join, refused when the vector is first read, naming every
# point at fault (the Data docstring): a label that is not a whole number, or one of 2**53
# or more in size, which numpy would read as the least int64 once past int64; a rate_class
# the class factors lack; a sex and rate_class the COI scales lack; and, on a point that
# has_surr_charge, a surr_charge_id the schedules lack, by either of its two vectors.  The
# surrender-charge cases leave the charge on points 4 and 6 alone, so that the message
# names point 6 and not the table, and point 2, without a charge, projects: ULSG_US_S reads
# a schedule only where a point has a charge.  The class and COI joins refuse the table:
# every point reads its class factor, through mortality, and its COI scale, through the
# shadow account's charge, in its first month in cover; a class the class factors lack is
# given a COI scale of its own (_coi_with), so that the class join is what a projection
# meets.  Each case is (case, the table's edit, the inputs' edits, the Data cell asked, the
# message, the label whose projection meets it, a label that projects regardless or None):
# a label's refusal is met by that point's own point_id(), which every refusal names it
# by; a table's by point 1's result_cf(); and the schedules' by point 4's, which has a
# charge.
_CHARGED = (4, 6)
_NO_CLASS = "class_factor_table.csv has no factor for the rate_class of point_id [3, 6]"
_NO_SCALE = "coi_rates.csv has no scale for the sex and rate_class of point_id [3, 6]"
_NO_SCHEDULE = ("surr_charge_table.csv has no schedule for the surr_charge_id of point_id "
                "[6], each of which has_surr_charge")


def _charged_only(points, edit=None):
    """An edit that leaves the surrender charge on ``points`` alone, after ``edit``."""
    def charged(table):
        table = table if edit is None else edit(table)
        return table.assign(has_surr_charge=table.index.isin(points))
    return charged


def _relabelled(label, new):
    """An edit that labels the table's row ``label`` ``new``, a label as written."""
    return lambda table: table.rename(index={label: new})


def _coi_with(rate_class):
    """An edit of the COI scale that adds ``(M, rate_class)``, the anchor's rates."""
    def edit(rates):
        anchor = rates[(rates["sex"] == "M") & (rates["rate_class"] == "StdNT")]
        return pd.concat([rates, anchor.assign(rate_class=rate_class)],
                         ignore_index=True).sort_values(COI_KEYS, ignore_index=True)
    return edit


UNJOINED = [
    ("a label that is not whole", _relabelled(4, 4.5), None, "point_id",
     f"{TABLE}: point_id must be a whole number; [4.5] is not", 4.5, None),
    ("a label written as text", _relabelled(4, "4x"), None, "point_id",
     f"{TABLE}: point_id must be a whole number; ['4x'] is not", "4x", None),
    ("a label of 2**53", _relabelled(4, 2 ** 53), None, "point_id",
     f"{TABLE}: point_id must be below 2**53 in size; [{2 ** 53}] is not", 2 ** 53, None),
    ("a class the table lacks, at two points", _set("rate_class", [3, 6], "SuperPNT"),
     {"coi_rates.csv": _coi_with("SuperPNT")}, "class_factor", _NO_CLASS, 1, None),
    ("a scale the COI table lacks, at two points", _set("rate_class", [3, 6], "PNT"),
     None, "coi_schedule", _NO_SCALE, 1, None),
    ("a schedule the table lacks, on a point with a charge",
     _charged_only(_CHARGED, _set("surr_charge_id", [2, 6], "GUL5")), None,
     "surr_charge_rate_max", _NO_SCHEDULE, 4, 2),
    ("a schedule the table lacks, by the run-off's vector",
     _charged_only(_CHARGED, _set("surr_charge_id", [2, 6], "GUL5")), None,
     "surr_charge_runoff_years", _NO_SCHEDULE, 4, 2),
]


@pytest.mark.parametrize("case, edit, edits, cell, message, label, projects", UNJOINED,
                         ids=[c[0] for c in UNJOINED])
def test_what_data_cannot_number_or_join_is_refused_naming_it(tmp_path, case, edit, edits,
                                                             cell, message, label,
                                                             projects):
    """``Data`` refuses what it cannot number or join, naming every point at fault.

    ``ULSG_US_S`` reads a point's class factor and its COI scale in its first month in
    cover, and the schedule of a point with a surrender charge in every month of its
    cover, so it fails every projection of a point whose class, scale or charged schedule
    the tables lack, and this model refuses at the first read instead (:data:`UNJOINED`),
    in the vector's own cell and in a projection, with the message matched whole.  A label
    is read by no projection but in a refusal, which names the point by ``point_id()``, so
    that cell refuses it.  The message names every point at fault and no other, and a
    point without a charge, which never reads its schedule, projects as it does on the
    committed table.
    """
    model = _read(_sec_inputs(tmp_path, edit(_committed()), edits), "unjoined")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused_exactly(model.Data.cells[cell], message)
        call = "point_id" if cell == "point_id" else "result_cf"
        _refused_exactly(_point(model, label).cells[call], message)
        if projects is not None:
            p = _point(model, projects)
            assert not p.has_surr_charge() and len(p.result_cf()) == p.proj_len()
    finally:
        model.close()


# Points without a surrender charge, as (point_id, the surr_charge_id written, the charge
# and the run-off their accessors read, or None where the table lacks the id).  Each is the
# value 3eacf45's model, ULSG_US_SEC at stage E, read there, its .loc reading the schedule
# of a point with a charge or without, and raising KeyError on an id the table lacks: SC7,
# a second schedule the copy adds, GUL15 as shipped, and GUL5, which no table has.
UNCHARGED = ((3, "SC7", (9.5, 7.0)), (4, "GUL15", (18.0, 15.0)), (2, "GUL5", None))
_NO_ID = ("KeyError: 'point_id {}: surr_charge_table.csv has no schedule for its "
          "surr_charge_id'")


def _surr_charges_with_sc7(table):
    """The shipped schedules with SC7: $9.50 per $1,000 over 7 years."""
    sc7 = pd.DataFrame([{"surr_charge_id": "SC7", "sc_per_1000_init": 9.5,
                         "runoff_years": 7, "provenance": "test copy"}])
    return pd.concat([table, sc7], ignore_index=True)


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
    without a charge, since ``surr_charge_rate`` returns 0.0 first, but each is a cell,
    and Phase 2 moves no number (D2): so each reads the point's schedule wherever the
    table holds its id, and raises ``KeyError`` where it does not, naming the point, as
    the ``.loc`` of the model at stage ``E`` did (:data:`UNCHARGED`, pinned to 3eacf45's
    values).  ``Data`` joins the schedule wherever it can, NaN and a
    ``has_surr_charge_schedule`` of 0 where it cannot, and refuses no point without a
    charge, which projects as ``ULSG_US_S`` projects it, its schedule unread.
    """
    folder = _sec_inputs(tmp_path, _uncharged(),
                         edits={"surr_charge_table.csv": _surr_charges_with_sc7})
    model = _read(folder, "uncharged")
    try:
        for point, label, want in UNCHARGED:
            p = _point(model, point)
            assert (p.has_surr_charge(), p.surr_charge_id()) == (False, label)
            assert len(p.result_cf()) == p.proj_len() and p.surr_charge_rate(0) == 0.0
            cells = (p.cells["surr_charge_rate_max"], p.cells["surr_charge_runoff_years"])
            if want is None:
                for cell in cells:
                    with pytest.raises(Exception) as excinfo:
                        cell()
                    assert _raised(excinfo.value) == _NO_ID.format(point)
            else:
                assert [(type(v), v) for v in (cell() for cell in cells)] == [
                    (float, want[0]), (float, want[1])]
        known = dict(zip(model.Data.model_point_table().index,
                         model.Data.has_surr_charge_schedule()))
        assert [known[point] for point, _, _ in UNCHARGED] == [1, 1, 0]
    finally:
        model.close()


def _coi_from(age):
    """An edit of the COI scale that adds the anchor cell's ages from ``age`` to 44,
    geometric in the age, each its own rate."""
    def edit(rates):
        ages = range(age, 45)
        young = pd.DataFrame({
            "sex": "M", "rate_class": "StdNT", "age": list(ages),
            "coi_rate_guar_ann": [round(0.55 * 1.09 ** (a - age), 6) for a in ages],
            "provenance": "test copy"})
        return pd.concat([young, rates], ignore_index=True).sort_values(
            COI_KEYS, ignore_index=True)
    return edit


# The point issued below issue_age_min, 18, the youngest issue age product-spec.md admits:
# S's point 2, new business, issued at 17, which ULSG_US_S projects on a COI scale from 17.
_BELOW_MIN = "point_id 2: issue age 17 is below issue_age_min, 18"


def test_a_point_issued_below_issue_age_min_is_refused_by_proj_len(tmp_path):
    """``proj_len()`` refuses a point issued below ``issue_age_min``, naming it (§6.1).

    ``ULSG_US_S`` projects a point issued at any age its tables serve, and so would modelx
    here, but the compiled caches are sized from the contract, cover from
    ``issue_age_min``, 18, to ``charges_cease_age``, 121 (``spec_sec.py``), and a point
    issued younger runs past them.  So the frame refuses it, on a COI scale from 17, where
    S's point projects, and every report is refused with the frame.  The rule is asked
    last, after Phase 1's, whose messages keep their order (D2).  The table reads, since
    the rule is the product's, and the same point projects with ``issue_age_min`` at 17,
    its frame 1,248 months, so that the Reference is what refuses it and a bound off by
    one lets it through.  ``ULSG_US_S`` projects it on the same inputs.
    """
    table = _set("age_at_entry", [2], 17)(_committed())
    edits = {"coi_rates.csv": _coi_from(17)}
    folder = _sec_inputs(tmp_path / "sec", table, edits)
    model = _read(folder, "below_min")
    try:
        assert len(model.Data.model_point_table()) == len(table)
        _refused_exactly(_point(model, 2).proj_len, _BELOW_MIN)
        for report in REPORTS:
            _refused(_point(model, 2).cells[report], _BELOW_MIN)
    finally:
        model.close()
    model = _read(folder, "below_min_moved", {"issue_age_min": 17})
    try:
        p = _point(model, 2)
        assert p.proj_len() == len(p.result_cf()) == 12 * (121 - 17)
        assert p.check_av_roll_fwd() and p.check_margin()
    finally:
        model.close()
    s = _read(_s_inputs(tmp_path / "s", _set("age_at_entry", [2], 17)(_s_table()), edits),
              "below_min_s")
    try:
        assert len(_point(s, 2).result_cf()) == 12 * (121 - 17)
    finally:
        s.close()


# run_sec.py run as though it sat at /m/products/guaranteed_ul, a copy too shallow to have
# a repository above it: the source compiled under that name, so that its own __file__ is
# it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/guaranteed_ul/run_sec.py"
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
    for args in ((copy, "5", "--cython"), (shallow, runner)):
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
    exactly.  ``python tools/gen_sec_fingerprint.py ULSG_US_SEC --check`` runs the same
    comparison from the command line.
    """
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# ULSG_US_SEC's fingerprint, frozen at M13 from the model as Phase 1 left it and committed
# alone, before Phase 2 changed anything.  Each point is keyed by its point_id; each column
# holds (its sum over the frame, its largest absolute value, (its values at the months)).
# The block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a
# refreeze goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: ULSG_US_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 432, "months": (0, 107, 215, 323, 431),
        "result_cf": {
            "pols_if": (54.20059666882125, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (52987.411866347524, 10800.0, (
                10800.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (231304.09975314722, 3311.861402550298, (
                3311.861402550298, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (11.304701421534048, 2.627248402547843, (
                2.627248402547843, 0.0, 0.0, 0.0, 0.0)),
            "claims_rop": (19860.683135909803, 19860.683135909803, (
                19860.683135909803, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (499.6386889330604, 8.23711684153018, (
                8.23711684153018, 0.0, 0.0, 0.0, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-198688.31441306413, 12383.408903704178, (
                -12383.408903704178, 0.0, 0.0, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (54.20059666882125, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.4626081995062945, 0.006623722805100596, (
                0.006623722805100596, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.014661958651910549, 0.0003421203994092697, (
                0.0003421203994092697, 0.0, 0.0, 0.0, 0.0)),
            "pols_rop": (0.09930341567954902, 0.09930341567954902, (
                0.09930341567954902, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse_grace": (0.4234264261622465, 0.4234264261622465, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (26.612923471652344, 0.21627595513048758, (
                0.006623722805100596, 0.014139367673717596, 0.04163882208025793,
                0.0889457750609135, 0.21627595513048758)),
            "lapse_rate_mth": (0.26407615418854835, 0.0006901133944458016, (
                0.00034440162027560284, 0.0006901133944458016, 0.0006901133944458016,
                0.0006901133944458016, 0.0006901133944458016)),
        },
    },
    2: {"rows": 732, "months": (0, 182, 365, 548, 731),
        "result_cf": {
            "pols_if": (263.7812769530893, 1.0, (
                1.0, 0.7217304923698212, 0.2540353329854334, 0.0, 0.0)),
            "premiums": (237852.00351403383, 10584.0, (
                10584.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (370602.9971089007, 1208.0155294963315, (
                226.8987912442677, 710.9405409707264, 1137.9835623134693, 0.0, 0.0)),
            "claims_lapse": (2749.419246095865, 21.482139597866365, (
                0.0, 13.278207969575622, 0.0, 0.0, 0.0)),
            "claims_rop": (12308.1006756347, 8928.5542351175, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (12406.508841093426, 9831.986139274746, (
                9831.986139274746, 6.959570254613623, 4.0131418774598995, 0.0, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-160215.0223576909, 10039.980326721661, (
                525.1150694809858, -731.1783191949156, -1141.9967041909292, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (263.7812769530893, 1.0, (
                1.0, 0.7217304923698212, 0.2540353329854334, 0.0, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.7412059942178015, 0.002416031058992663, (
                0.0004537975824885354, 0.0014218810819414528, 0.002275967124626939, 0.0,
                0.0)),
            "pols_lapse": (0.16484849200698357, 0.0018512430472809528, (
                0.0018512430472809528, 0.0003309766145521, 6.302654998362554e-05, 0.0,
                0.0)),
            "pols_rop": (0.07505297202248308, 0.0446427711755875, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse_grace": (0.018892541752731584, 0.018892541752731584, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (20.583629910042173, 0.1323236037593104, (
                0.0004537975824885354, 0.0019700997768192785, 0.00895925420247523,
                0.044961146581067424, 0.1323236037593104)),
            "lapse_rate_mth": (0.3987663827639696, 0.0018520835183041262, (
                0.0018520835183041262, 0.00045949279151380473, 0.0002503444102988084,
                0.0006901133944458016, 0.0006901133944458016)),
        },
    },
    3: {"rows": 732, "months": (0, 182, 365, 548, 731),
        "result_cf": {
            "pols_if": (277.3948973553521, 1.0, (
                1.0, 0.7649142137594749, 0.2728182693574706, 0.0034431125800530493,
                4.0120432955769327e-10)),
            "premiums": (152300.0, 152300.0, (
                152300.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (405239.1359254395, 1296.1140984926292, (
                226.8987912442677, 753.4786609067178, 1222.1241131264692, 77.4031447034412,
                2.6544401365455996e-05)),
            "claims_lapse": (9031.815641394529, 116.52773087033205, (
                116.52773087033205, 17.065640020045965, 0.0, 0.0, 0.0)),
            "claims_rop": (9776.50927796131, 7295.627080544823, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (140109.08632241588, 137376.38613927475, (
                137376.38613927475, 7.375986279770221, 4.309866697784832,
                0.11181590555038137, 2.6959232671574497e-08)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-411856.5471672112, 14580.187338610645, (
                14580.187338610645, -777.920287206534, -1226.433979824254,
                -77.51496060899159, -2.657136059812757e-05)),
        },
        "result_pols": {
            "pols_if": (277.3948973553521, 1.0, (
                1.0, 0.7649142137594749, 0.2728182693574706, 0.0034431125800530493,
                4.0120432955769327e-10)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.810478271850879, 0.002592228196985258, (
                0.0004537975824885354, 0.0015069573218134354, 0.0024442482262529383,
                0.0001548062894068824, 5.308880273091199e-11)),
            "pols_lapse": (0.109039840241161, 0.0011062094465917026, (
                0.0011062094465917026, 0.00021025519629962888, 6.768662488021225e-05,
                8.232090992136766e-07, 8.714877627930958e-14)),
            "pols_rop": (0.080481887559933, 0.04790300118545517, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse_grace": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (20.583629910042173, 0.1323236037593104, (
                0.0004537975824885354, 0.0019700997768192785, 0.00895925420247523,
                0.044961146581067424, 0.1323236037593104)),
            "lapse_rate_mth": (0.22577300503773756, 0.0011067116696719115, (
                0.0011067116696719115, 0.0002754168165505222, 0.0002503444102988084,
                0.0002503444102988084, 0.0002503444102988084)),
        },
    },
    4: {"rows": 732, "months": (0, 182, 365, 548, 731),
        "result_cf": {
            "pols_if": (178.8369961686587, 1.0, (
                1.0, 0.654011752281597, 0.0, 0.0, 0.0)),
            "premiums": (89966.05608889938, 5880.0, (
                5880.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (108367.01109535492, 829.9897818685043, (
                226.8987912442677, 644.2342036035798, 0.0, 0.0, 0.0)),
            "claims_lapse": (23.241291446564585, 1.8201481655977232, (
                0.0, 0.6013669256445401, 0.0, 0.0, 0.0)),
            "claims_rop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (7048.424974377961, 5598.386139274747, (
                5598.386139274747, 6.306565657772477, 0.0, 0.0, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-25472.62127228004, 5368.863004774371, (
                54.71506948098522, -651.1421361869968, 0.0, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (178.8369961686587, 1.0, (
                1.0, 0.654011752281597, 0.0, 0.0, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.21673402219070984, 0.0016599795637370087, (
                0.0004537975824885354, 0.0012884684072071596, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.22733684086377998, 0.003394512078185888, (
                0.003394512078185888, 0.0005464451550304801, 0.0, 0.0, 0.0)),
            "pols_rop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse_grace": (0.5559291369455108, 0.5559291369455108, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (20.583629910042173, 0.1323236037593104, (
                0.0004537975824885354, 0.0019700997768192785, 0.00895925420247523,
                0.044961146581067424, 0.1323236037593104)),
            "lapse_rate_mth": (0.9021999996154818, 0.003396053198917559, (
                0.003396053198917559, 0.0008371773591205889, 0.0012586770182638762,
                0.0012586770182638762, 0.0012586770182638762)),
        },
    },
    5: {"rows": 351, "months": (0, 87, 175, 262, 350),
        "result_cf": {
            "pols_if": (0.4287262958536435, 0.4287262958536435, (
                0.4287262958536435, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (2627.6596573514757, 2627.6596573514757, (
                2627.6596573514757, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_rop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (4.256135143496158, 4.256135143496158, (
                4.256135143496158, 0.0, 0.0, 0.0, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-2631.915792494972, 2631.915792494972, (
                -2631.915792494972, 0.0, 0.0, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (0.4287262958536435, 0.4287262958536435, (
                0.4287262958536435, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.005255319314702952, 0.005255319314702952, (
                0.005255319314702952, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.0002922429930685667, 0.0002922429930685667, (
                0.0002922429930685667, 0.0, 0.0, 0.0, 0.0)),
            "pols_rop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse_grace": (0.423178733545872, 0.423178733545872, (
                0.423178733545872, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (29.820577666632, 0.31890667595955724, (
                0.012257982226723474, 0.032125965898521125, 0.06393814334250081,
                0.11452145564222782, 0.31890667595955724)),
            "lapse_rate_mth": (0.24222980145047635, 0.0006901133944458016, (
                0.0006901133944458016, 0.0006901133944458016, 0.0006901133944458016,
                0.0006901133944458016, 0.0006901133944458016)),
        },
    },
    6: {"rows": 492, "months": (0, 122, 245, 368, 491),
        "result_cf": {
            "pols_if": (64.11395265984982, 0.6103591832068608, (
                0.6103591832068608, 0.23411337350189726, 0.024268938256944757, 0.0, 0.0)),
            "premiums": (59871.17394837737, 6460.041595061414, (
                6460.041595061414, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (253917.6314751826, 1345.089100608926, (
                1194.1278539405484, 1178.4559036216656, 387.2163214262909, 0.0, 0.0)),
            "claims_lapse": (14.916170692747537, 1.4862571622351992, (
                1.4862571622351992, 0.0, 0.0, 0.0, 0.0)),
            "claims_rop": (11877.518471084155, 8500.4306905495, (
                3377.0877805346554, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (620.1752811244215, 4.531221607407209, (
                4.531221607407209, 2.5801042359820467, 0.48087655045716315, 0.0, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-206559.06744970658, 5321.6479455956505, (
                1882.808481816568, -1181.0360078576475, -387.69719797674804, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (64.11395265984982, 0.6103591832068608, (
                0.6103591832068608, 0.23411337350189726, 0.024268938256944757, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.5078352629503653, 0.002690178201217852, (
                0.0023882557078810968, 0.0023569118072433314, 0.0007744326428525819, 0.0,
                0.0)),
            "pols_lapse": (0.017157430020491856, 0.00020938617251110964, (
                0.00020938617251110964, 5.801893473588651e-05, 5.881718153221949e-06, 0.0,
                0.0)),
            "pols_rop": (0.07289023051907093, 0.0425021534527475, (
                0.03038807706632343, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse_grace": (0.01247625971693231, 0.01247625971693231, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (24.129376417638717, 0.17454341487096336, (
                0.003912869296621491, 0.01006739500605347, 0.03191044596402859,
                0.07569561640264932, 0.17454341487096336)),
            "lapse_rate_mth": (0.22742020415005637, 0.0006901133944458016, (
                0.00034440162027560284, 0.0002503444102988084, 0.0002503444102988084,
                0.0006901133944458016, 0.0006901133944458016)),
        },
    },
    7: {"rows": 427, "months": (0, 106, 213, 319, 426),
        "result_cf": {
            "pols_if": (32.33835631507287, 0.3927760044924489, (
                0.3927760044924489, 0.12718827769440927, 0.0, 0.0, 0.0)),
            "premiums": (27974.540794276523, 3961.230481905986, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (186922.72367974804, 1379.4100069000028, (
                1300.819689126464, 1000.3753982367805, 0.0, 0.0, 0.0)),
            "claims_lapse": (3.217471751991964, 0.6160192957814714, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_rop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (338.5341793757491, 3.235341841553684, (
                3.235341841553684, 1.5687662768930948, 0.0, 0.0, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-159289.93453659926, 2582.0133439770284, (
                -1304.0550309680177, -1001.9441645136736, 0.0, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (32.33835631507287, 0.3927760044924489, (
                0.3927760044924489, 0.12718827769440927, 0.0, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.3738454473594961, 0.0027588200138000058, (
                0.002601639378252928, 0.002000750796473561, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.0083336279371691, 0.0001279503835092402, (
                9.767797134822536e-05, 3.133999759802993e-05, 0.0, 0.0, 0.0)),
            "pols_rop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse_grace": (0.010596929195784147, 0.010596929195784147, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (26.613799254393335, 0.21627595513048758, (
                0.006623722805100596, 0.01573062260722402, 0.046383809023931244,
                0.09631544494067523, 0.21627595513048758)),
            "lapse_rate_mth": (0.20936073049107473, 0.0006901133944458016, (
                0.0002503444102988084, 0.0002503444102988084, 0.0006901133944458016,
                0.0006901133944458016, 0.0006901133944458016)),
        },
    },
    8: {"rows": 1, "months": (0,),
        "result_cf": {
            "pols_if": (4.0120432955769327e-10, 4.0120432955769327e-10, (
                4.0120432955769327e-10,)),
            "premiums": (0.0, 0.0, (
                0.0,)),
            "claims_death": (0.00020060216477884663, 0.00020060216477884663, (
                0.00020060216477884663,)),
            "claims_lapse": (0.0, 0.0, (
                0.0,)),
            "claims_rop": (0.0, 0.0, (
                0.0,)),
            "withdrawals": (0.0, 0.0, (
                0.0,)),
            "expenses": (1.2286882592704356e-07, 1.2286882592704356e-07, (
                1.2286882592704356e-07,)),
            "premium_taxes": (0.0, 0.0, (
                0.0,)),
            "net_cf": (-0.00020072503360477368, 0.00020072503360477368, (
                -0.00020072503360477368,)),
        },
        "result_pols": {
            "pols_if": (4.0120432955769327e-10, 4.0120432955769327e-10, (
                4.0120432955769327e-10,)),
            "pols_new_biz": (0.0, 0.0, (
                0.0,)),
            "pols_death": (4.0120432955769327e-10, 4.0120432955769327e-10, (
                4.0120432955769327e-10,)),
            "pols_lapse": (0.0, 0.0, (
                0.0,)),
            "pols_rop": (0.0, 0.0, (
                0.0,)),
            "pols_lapse_grace": (0.0, 0.0, (
                0.0,)),
            "pols_maturity": (0.0, 0.0, (
                0.0,)),
            "mort_rate_mth": (1.0, 1.0, (
                1.0,)),
            "lapse_rate_mth": (0.0002503444102988084, 0.0002503444102988084, (
                0.0002503444102988084,)),
        },
    },
    9: {"rows": 757, "months": (0, 189, 378, 567, 756),
        "result_cf": {
            "pols_if": (264.62389958119144, 1.0, (
                0.0, 0.753660771598438, 0.28396705305429987, 0.0, 0.0)),
            "premiums": (238597.94708196726, 10584.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (370139.3229540867, 1215.698512395333, (
                0.0, 599.0898989228382, 1150.4160008632687, 0.0, 0.0)),
            "claims_lapse": (2755.470027653446, 21.51616309860551, (
                0.0, 13.290408572445035, 0.0, 0.0, 0.0)),
            "claims_rop": (12386.380238025358, 8985.33987058844, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (12539.981044564118, 9832.299829713362, (
                0.0, 7.181488399776005, 4.506068888733269, 0.0, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-159223.2071823624, 10045.662924341901, (
                0.0, -619.5617958950592, -1154.922069752002, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (264.62389958119144, 1.0, (
                0.0, 0.753660771598438, 0.28396705305429987, 0.0, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.7402786459081735, 0.0024313970247906657, (
                0.0, 0.0011981797978456764, 0.0023008320017265374, 0.0, 0.0)),
            "pols_lapse": (0.16517834652770774, 0.0018512598136459712, (
                0.0, 0.00034575113681616673, 7.051356401050027e-05, 0.0, 0.0)),
            "pols_rop": (0.07553030918122675, 0.0449266993529422, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse_grace": (0.019012698382891293, 0.019012698382891293, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (20.577300532251645, 0.1323236037593104, (
                0.0, 0.0015898131400742255, 0.008102461102368008, 0.044961146581067424,
                0.1323236037593104)),
            "lapse_rate_mth": (0.3987663827639696, 0.0018520835183041262, (
                0.0, 0.00045949279151380473, 0.0002503444102988084, 0.0006901133944458016,
                0.0006901133944458016)),
        },
    },
}
# END generated fingerprint: ULSG_US_SEC


# ---------------------------------------------------------------------------
# Compiled (USLIB-SEC-PLAN.md Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython CI job, which sets USLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is ULSG's
# own: the comparison on the splice grid, at the contract's extremes, on labels that are
# not text, on keys written as floats and where the cap on mortality binds, the refusals,
# the deepest call, a lapse rate past 1, a Reference set late and the runner.  Each
# comparison on points that all project adds _ulsg_c4_also's calls, the codes no swept
# cell reaches.  None asks for sec_read, sec_model or s_model, which sweep every committed
# point; the grid test alone asks for spliced.


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)


def _ulsg_c4_also(proj):
    """What C4 compares of a ``ULSG_US_SEC`` point beyond its full sweep (M18).

    ``sec_support.full_sweep`` reaches a cell of a timing or a kind only at the codes some
    swept cell asks of it.  So, as ``sample_sec.py`` does, this calls, at ``t = 0 ..
    proj_len()``, ``pols_if_at`` at ``BEF_MAT``, ``av_at`` at the account's later timings,
    ``BEF_WD``, ``BEF_FEE``, ``BEF_COI``, ``BEF_INV`` and ``EOM``, ``claim_pp`` at
    ``GRACE`` and ``claims_from_av`` at ``WITHDRAWAL`` and ``MATURITY``, the codes no
    formula passes those cells.  It calls no cell of ``t`` alone, which the sweep reaches,
    and none that raises on a point the contract issues, ``cure_premium_pp`` at a load of
    1 among them, so it is passed only where every point projects.  Passed to
    ``sec_support.compiled_mismatches`` as ``also``.
    """
    account = (proj.BEF_WD, proj.BEF_FEE, proj.BEF_COI, proj.BEF_INV, proj.EOM)
    for t in range(proj.proj_len() + 1):
        proj.pols_if_at(t, proj.BEF_MAT)
        for timing in account:
            proj.av_at(t, timing)
        proj.claim_pp(t, proj.GRACE)
        for kind in (proj.WITHDRAWAL, proj.MATURITY):
            proj.claims_from_av(t, kind)


def _signs_apart(build, folder, table, refs):
    """Where a compiled ``claims(t)`` is not S's ``sum`` of the compiled kinds, bit for bit.

    C4 compares two floats by value, so it holds ``-0.0`` and ``0.0`` alike; the total's
    sign of a zero is R12's, and this holds it compiled: in a child of its own, every
    point of ``table``, beside the build in ``folder``, is asked ``claims(t)`` and its
    three kinds in every month of its frame and the month after, and the total must be
    ``sum`` of the kinds and S's GRACE 0.0, by ``float.hex``.  The kinds themselves are
    C4's to hold to modelx.  Returns readable lines, empty when every total agrees.
    """
    cease = refs.get("charges_cease_age", 121)
    frames = (12 * (cease - table["age_at_entry"]) - table["duration_mth"]).tolist()
    cells = ("claims", *(cell for cell, _ in SPLIT))
    job = {"refs": refs, "calls": {
        idx: [(cell, (t,)) for t in range(n + 1) for cell in cells]
        for idx, n in enumerate(frames)}}
    got = run_compiled(folder.parent, build.package.name, job)
    if got["exit"]:
        return [f"the compiled run failed with exit code {got['exit']}:\n{got['stderr']}"]
    found = []
    for idx, n in enumerate(frames):
        values = got["values"][idx]
        for t in range(n + 1):
            (status, total), *parts = values[4 * t:4 * t + 4]
            if status != "ok" or any(s != "ok" for s, _ in parts):
                found.append(f"idx {idx}: claims({t}) or a kind raised")
                continue
            want = sum((*(v for _, v in parts), 0.0))
            if not _same_float(total, want):
                found.append(f"idx {idx}: claims({t}) {total!r}, the sum of its kinds "
                             f"{want!r}")
    return found


# How many rows of the splice grid C4 compares at once.  compiled_mismatches sweeps every
# row of its case in one modelx read, _ulsg_c4_also's calls with it, and keeps every value
# of every row, in the parent and in the child, until it compares them.  A ULSG row runs
# up to 985 months on the grid, and a full sweep of a 732-month row holds about 130 MB in
# modelx; ten rows at a time, the splice's two models alive beside them, peaked at 3.3 GB
# for the process tree on the core grid, in 74 s (measured at M18, under load), below the
# 3.6 GB a VUL chunk of four reached, so ULSG compares ten rows at a time, as UL does
# (USLIB-SEC-PLAN.md §7.2, *For M16 and later*, item 7).
C4_CHUNK = 10


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_the_splice_grid(spliced,
                                                                             sec_build,
                                                                             tmp_path):
    """C4 on the branches: compiled, every cell of the splice grid is modelx's.

    The sample traces the committed points alone, and they leave branches untaken, which
    are typed all the same, because every branch of a cell returns the one type the
    others return (sample_sec.py).  What the compiled model computes on them is held
    here: the splice grid's points, S's restated in force at T2's months and issued later,
    and the variants, ten-pay premiums, every premium mode, withdrawals outrunning an
    exhausted account, a loan under a funded account and one on an exhausted account, a
    single premium on the corridor, a COI scale read past its last age, each pin alone,
    an issue age below the mortality table's first age on a second surrender schedule, a
    cure and a grace in the issue month, under the splice's References
    (:data:`SPLICED_REFS`), on the splice's COI and surrender-charge copies
    (:data:`SPLICED_EDITS`).  The grid is the one this run's ``spliced`` selects, the core
    by default and the full grid under ``USLIB_SEC_FULL=1``, and the test carries no
    ``sec_full`` mark, since a skipped compile test fails the cython job.  The grid's SEC
    table goes beside the build :data:`C4_CHUNK` rows at a time; modelx sweeps every row
    fully, with every code (:func:`_ulsg_c4_also`), and the compiled model must agree at
    every argument modelx caches, identically on x86-64 and to 1e-12 relative elsewhere,
    with every raise and every ``Data`` array (``sec_support.compiled_mismatches``).  And
    every compiled ``claims(t)`` is the ``sum`` of its compiled kinds, the sign of a zero
    included, which C4's comparison by value cannot see (:func:`_signs_apart`).
    """
    build = sec_build(SEC)
    table = pd.read_csv(spliced[1].Data.input_dir() / TABLE, index_col="point_id")
    assert len(table) == len(spliced[1].Data.model_point_table())
    chunks = [table.iloc[i:i + C4_CHUNK] for i in range(0, len(table), C4_CHUNK)]
    assert sum(len(chunk) for chunk in chunks) == len(table) and len(chunks) > 1
    found = []
    for i, chunk in enumerate(chunks):
        folder = compiled_case(build, tmp_path / f"grid{i}", model_points=chunk,
                               edits=SPLICED_EDITS)
        found += compiled_mismatches(build, folder, refs=SPLICED_REFS, also=_ulsg_c4_also)
        found += [f"chunk {i}: {line}"
                  for line in _signs_apart(build, folder, chunk, SPLICED_REFS)]
        shutil.rmtree(tmp_path / f"grid{i}")
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


# The References at the contract's extremes: inflation and improvement on, and the A/E at
# the shipped 1.0, so that StdTob's annual mortality passes 1 and is capped.
EXTREME_REFS = {**SWITCHED_ON, "mort_ae_factor": 1.0}

# The COI scales of the extremes' copy, each from its first age to 120, geometric in the
# attained age from a base of its own at a ratio of its own, as (sex, rate_class, first
# age, base, ratio): the four the extremes read and M PTob, which none reads, between two
# that they read in key order.
EXTREME_COI = ((("F", "PNT", 18), 0.061, 1.051), (("M", "PPlusNT", 18), 0.052, 1.053),
               (("M", "PTob", 18), 0.093, 1.047), (("M", "StdNT", 18), 0.071, 1.049),
               (("M", "StdTob", 85), 3.1, 1.09))


def _coi_extremes(_):
    """The extremes' COI scales (:data:`EXTREME_COI`), every line in reverse key order,
    so that a scale numbered in file order is another scale's number."""
    rates = pd.concat([pd.DataFrame({
        "sex": sex, "rate_class": rate_class, "age": range(first, 121),
        "coi_rate_guar_ann": [round(base * ratio ** (a - first), 6)
                              for a in range(first, 121)],
        "provenance": "test copy"})
        for (sex, rate_class, first), base, ratio in EXTREME_COI])
    rates = rates.sort_values(COI_KEYS, ignore_index=True)
    return rates.iloc[::-1].reset_index(drop=True)


def _mort_from_18(rates):
    """The mortality table with ages 18 to 44, each its own rate, geometric in the age."""
    ages = range(18, 45)
    young = pd.DataFrame({"age": list(ages),
                          "mort_rate": [round(0.00037 * 1.083 ** (a - 18), 6)
                                        for a in ages],
                          "provenance": "test copy"})
    return pd.concat([young, rates], ignore_index=True)


def _rop_at_the_ends(rows):
    """The return-of-premium table with anniversaries 1 and 102 added, the first and the
    last a policy issued at 18 completes in cover, each with terms of its own."""
    ends = pd.DataFrame({"anniversary": [1, 102], "refund_ratio": [0.15, 0.85],
                         "exercise_rate": [0.02, 0.3], "provenance": "test copy"})
    return pd.concat([rows, ends], ignore_index=True).sort_values(
        "anniversary", ignore_index=True)


EXTREME_EDITS = {"coi_rates.csv": _coi_extremes, "mort_table.csv": _mort_from_18,
                 "rop_table.csv": _rop_at_the_ends}

# The frames of the contract's extremes, in _contract_extremes' order, and the COI
# schedule each reads, its key's place among the copy's five.
EXTREME_FRAMES = [1356, 1236, 1356, 552, 1, 12, 432]
EXTREME_SCHEDULES = [4, 1, 2, 5, 4, 4, 4]


def _contract_extremes():
    """Inputs for the contract's longest frames, its oldest issue ages and the bounds of
    its values: a table.

    Seven points made from the committed twins.  S's point 3, the single premium for life,
    at 18, the youngest age the contract issues at, 120 months on, the shipped
    ``future_horizon_mth``: a frame of 1,356 months, the longest the contract allows,
    which reads every cache as far as ``spec_sec.py`` sizes it, ``t`` to 1,356 in C4's
    sweep of the month after it, the attained age from 18 to 120, the policy year to 103
    and the anniversaries 0 to 102.  S's point 2 at 18, F PNT, issued now.  S's point 2 at
    18 paying ten-pay quarterly and withdrawing $60 a month, M PPlusNT, 120 months on.
    StdTob at 85, 120 months on, whose annual mortality passes 1 and is capped.  S's point
    3 at 18 in force in its last covered month, a frame of one row.  S's point 2 at 120, a
    year of cover.  And S's point 1, the worked example, at a load of 1, whose cure
    payment divides by zero in every month, ``ULSG_US_S``'s ``ZeroDivisionError``.
    """
    committed = _committed()

    def twin(s_point, **columns):
        return committed.loc[[_label(committed, "twin", s_point, 0)]].assign(**columns)

    later, last = -120, 12 * (121 - 18) - 1
    rows = pd.concat([
        twin(3, age_at_entry=18, duration_mth=later),
        twin(2, age_at_entry=18, sex="F", rate_class="PNT"),
        twin(2, age_at_entry=18, premium_type="TEN_PAY", premium_mode="Q", wd_pp=60.0,
             rate_class="PPlusNT", duration_mth=later),
        twin(2, age_at_entry=85, rate_class="StdTob", duration_mth=later),
        twin(3, age_at_entry=18, duration_mth=last, policy_count=0.5, av_pp_init=50000.0,
             sg_pp_init=60000.0, cum_prem_init=152300.0),
        twin(2, age_at_entry=120),
        twin(1, load_prem_rate=1.0)])
    rows.index = pd.Index(range(1, len(rows) + 1), name="point_id")
    return rows


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_contract_extremes(
        sec_build, tmp_path):
    """C4 where the caches end: the contract's longest frames, every cell compiled.

    The seven points of :func:`_contract_extremes`, the longest frames the contract
    allows, its oldest issue ages and the bounds of its values, read every cache as far
    as ``spec_sec.py`` sizes it: ``t`` to 1,356, the month after the 1,356-month frame,
    which the roll-forwards read, the attained age from 18 to 120, the policy year to 103
    and the anniversaries to 102.  They run under :data:`EXTREME_REFS`, every premium
    pattern among them, from a COI copy written in reverse key order, with a scale no
    point reads between two that points read, a mortality table from 18 and a
    return-of-premium table with anniversaries 1 and 102 added (:data:`EXTREME_EDITS`),
    each key with values of its own, so that a compiled read of the key beside the right
    one, which a padded array allows, changes a number the comparison sees.  ``Data``'s
    numbering of the scales, which both engines share, moves both alike, so the
    comparison cannot see it: it is held against the file by
    :func:`test_the_coi_schedules_are_numbered_by_key_whatever_the_file_order`.  Frames,
    schedules and the cap are asserted first.

    modelx sweeps each point fully, with every code (:func:`_ulsg_c4_also`), and the
    compiled model must agree everywhere, every raise included: the cure payment's
    ``ZeroDivisionError`` at a load of 1, S's own text, in every month.  A cache one too
    small for the contract raises ``IndexError`` compiled where modelx reads on, and fails
    here, though the spec check passes it, which holds the caches to the spec and not the
    spec to the contract.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "extremes", model_points=_contract_extremes(),
                           edits=EXTREME_EDITS)
    model = _read(folder, "extremes_frames", EXTREME_REFS)
    try:
        points = [projection(model, key) for key in point_keys(model)]
        frames = [p.proj_len() for p in points]
        schedules = list(model.Data.coi_schedule())
        capped = points[3]
        assert any(capped.mort_rate(t) == 1.0 for t in range(capped.proj_len()))
        assert points[0].is_rop_anniv(102) and points[0].is_rop_anniv(1)
    finally:
        model.close()
    assert frames == EXTREME_FRAMES, frames
    assert schedules == EXTREME_SCHEDULES, schedules
    found = compiled_mismatches(build, folder, refs=EXTREME_REFS, also=_ulsg_c4_also)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


def _labels_not_text():
    """The labels ``Data`` accepts that are not text, as (case, the table's rows).

    Made from the committed twins of S's points 1, 2 and 3: on a point without a charge,
    a blank ``surr_charge_id``, NaN as pandas reads it, beside a point with one; a blank
    ``premium_mode`` on the single premium, which never reads its mode, and projects; and
    a blank ``premium_type``, which the point's first projection refuses, issued at 120
    for a frame of twelve months, since modelx sweeps a raise in every cell of every
    month.  An id column and a mode column of numbers, ints, on single premiums without a
    charge.  And a blank ``rate_class`` and a blank ``sex``, each on a point issued at
    120 alone, which ``Data`` refuses at its class join and its COI join, the label
    accessors returning NaN all the same.
    """
    committed = _committed()

    def twin(s_point, **columns):
        return committed.loc[[_label(committed, "twin", s_point, 0)]].assign(**columns)

    cases = [
        ("blank", pd.concat([twin(1), twin(2, has_surr_charge=False, surr_charge_id=None),
                             twin(3, premium_mode=None),
                             twin(2, age_at_entry=120, premium_type=None)])),
        ("numeric", pd.concat([
            twin(3, has_surr_charge=False, surr_charge_id=0, premium_mode=1),
            twin(3, has_surr_charge=False, surr_charge_id=9, premium_mode=12)])),
        ("blank class", twin(2, age_at_entry=120, rate_class=None)),
        ("blank sex", twin(2, age_at_entry=120, sex=None)),
    ]
    for _, rows in cases:
        rows.index = pd.Index(range(1, len(rows) + 1), name="point_id")
    return cases


@pytest.mark.cython
def test_the_compiled_model_returns_a_label_that_is_not_text_as_modelx_does(sec_build,
                                                                             tmp_path):
    """C4 on labels that are not text: the compiled accessors return what modelx returns.

    ``Data`` accepts a blank ``surr_charge_id`` on a point without a charge, and an id
    column of numbers, since ``ULSG_US_S`` never reads such a point's schedule and
    projects it; a blank or numeric mode on a single premium, which never reads it; and a
    blank premium type, which the point's first projection refuses, and a blank class or
    sex, which a join refuses.  modelx returns each label as pandas reads it, NaN or an
    int, and an accessor typed ``str`` would raise ``TypeError`` compiled; the sample
    types the five as Python objects (sample_sec.py).  So on each case of
    :func:`_labels_not_text`, after checking that the file reads as the case says, modelx
    sweeps every point fully, with every code where no point refuses
    (:func:`_ulsg_c4_also`), and the compiled model must agree everywhere, the label
    accessors and every raise included.
    """
    build = sec_build(SEC)
    found = []
    for case, rows in _labels_not_text():
        folder = compiled_case(build, tmp_path / case.replace(" ", "_"), model_points=rows)
        model = mx.read_model(folder, name=_name(f"labels_{case.replace(' ', '_')}"))
        try:
            points = [projection(model, key) for key in point_keys(model)]
            labels = {label: [p.cells[label]() for p in points] for label in LABELS}
        finally:
            model.close()
        if case == "blank":
            ids, modes = labels["surr_charge_id"], labels["premium_mode"]
            types = labels["premium_type"]
            assert ids[0] == "GUL15" and math.isnan(ids[1]), ids
            assert modes[:2] == ["A", "A"] and math.isnan(modes[2]), modes
            assert types[:3] == ["LEVEL", "LEVEL", "SINGLE"] and math.isnan(types[3]), types
        elif case == "numeric":
            for label, want in (("surr_charge_id", [0, 9]), ("premium_mode", [1, 12])):
                got = labels[label]
                assert got == want and all(isinstance(i, (int, np.integer))
                                           for i in got), (label, got)
        else:
            column = "rate_class" if case == "blank class" else "sex"
            assert math.isnan(labels[column][0]), labels
        also = _ulsg_c4_also if case == "numeric" else None
        found += [f"{case}: {line}" for line in compiled_mismatches(build, folder,
                                                                     also=also)]
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


@pytest.mark.cython
def test_the_compiled_model_reads_keys_written_as_floats_as_modelx_does(sec_build,
                                                                         tmp_path):
    """C4 on keys written as floats: the compiled model reads 61.0 as 61, as modelx does.

    Every keyed table's key columns written as floats, as a spreadsheet can save them
    (:data:`FLOAT_KEYS`), and the model point table's ``duration_mth`` and
    ``age_at_entry`` too: ``Data`` reads each key by value, so every extent and every
    padded array's index is an int, and the edges test holds modelx to the shipped
    tables' numbers.  Here the twins of S's points 1 and 4 and the row issued 25 months
    on, which between them read every table, are swept in modelx with every code
    (:func:`_ulsg_c4_also`), and the compiled model must agree everywhere, every ``Data``
    array included, in dtype and shape.  First, in seconds, modelx's ``Data`` on the floats
    is held to its ``Data`` on the same rows as written: every array of the same dtype,
    and every extent and count of the same type, so that a key read as a float fails here,
    naming its cell, and not in the compiled sweep, where each typed read of a float array
    would raise.
    """
    build = sec_build(SEC)
    committed = _committed()
    rows = committed.loc[[_label(committed, "twin", 1, 0), _label(committed, "twin", 4, 0),
                          _label(committed, "future", 2, -25)]]
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
    found = compiled_mismatches(build, folder, also=_ulsg_c4_also)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


def _capped_table(tmp_path):
    """The cap test's rows, built by the generator from S under :data:`CAPPED_REFS`.

    The point of :data:`CAPPED`, alone in a copy of S's table on the splice's COI copy:
    its twin, issued at the valuation date; issued 25 months after it; and restated in
    force in the month before the cap first binds, :data:`CAPPED_MTH`, opened with S's
    count and state there.  As the cap test builds them.
    """
    base, changes = CAPPED
    s = _read(_s_inputs(tmp_path, _s_table().loc[[base]].assign(**changes),
                        SPLICED_EDITS), "capped_rows_s", CAPPED_REFS)
    try:
        spec = dataclasses.replace(SPEC, derived=((base, CAPPED_MTH - 1),),
                                   future=((base, 25),))
        table, _ = build_sec_table(spec, s)
    finally:
        s.close()
    return table


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_where_the_cap_binds(sec_build,
                                                                              tmp_path):
    """C4 where ``mort_rate`` caps the annual rate at 1, and where a NaN meets a bound.

    The three rows of the cap's test (:func:`_capped_table`), on whose frames the annual
    rate passes 1 from attained age 107, go beside the build, under :data:`CAPPED_REFS`.
    modelx sweeps them fully, with every code (:func:`_ulsg_c4_also`), and the compiled
    model must agree at every argument modelx caches, identically on x86-64 and to 1e-12
    relative elsewhere.  The extremes reach the side of ``min(q, 1.0)`` that returns 1
    too, on one point issued later; these reach it on a point issued at the valuation
    date, on one issued later and on one in force when it binds.

    And the committed twins of S's points 1 and 3 under each of :data:`NAN_CAP`'s
    References at NaN, the A/E and the improvement rate, which the compiled model reads as
    modelx does, so that a NaN reaches the cap compiled: ``min`` keeps its first argument
    there as in modelx, and C4 holds the compiled NaN to modelx's, in every cell it
    reaches.  The same for each of :data:`NAN_BOUNDS`' References, on the worked
    example's twin and the row issued 25 months on: a NaN that reaches a ``min`` or a
    ``max`` written with its bound second, which modelx and the compiled model must keep
    alike.
    """
    build = sec_build(SEC)
    rows = _capped_table(tmp_path / "s")
    folder = compiled_case(build, tmp_path / "capped", model_points=rows,
                           edits=SPLICED_EDITS)
    found = compiled_mismatches(build, folder, refs=CAPPED_REFS, also=_ulsg_c4_also)
    committed = _committed()
    cases = [(ref, (("twin", 1, 0), ("twin", 3, 0)), "mort_rate", first)
             for _, ref, first in NAN_CAP]
    cases += [(ref, (("twin", 1, 0), ("future", 2, -25)), cell, 0)
              for _, ref, cell in NAN_BOUNDS]
    for ref, points, cell, first in cases:
        twins = committed.loc[[_label(committed, *point) for point in points]]
        folder = compiled_case(build, tmp_path / ref, model_points=twins)
        model = _read(folder, f"nan_{ref}", {ref: float("nan")})
        try:
            for key in point_keys(model):
                p = projection(model, key)
                t = max(first, p.t_entry())
                assert math.isnan(p.cells[cell](t)), (ref, key, cell, t)
        finally:
            model.close()
        found += [f"{ref}: {line}" for line in compiled_mismatches(
            build, folder, refs={ref: float("nan")}, also=_ulsg_c4_also)]
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


# The compiled model's own refusals: what it does with a key past the caches spec_sec.py
# sizes, which no projection the contract allows reaches, as (cell, arguments, what modelx
# does, or ("ok", None) where modelx answers with a number).  modelx answers a month after
# cover with a zero, and runs a month before the valuation date of a point in force back
# through its accounts, the policy being in force then; it answers a policy year or an age
# past its table with the table's last row, as the cells say, and a year that is no
# anniversary, below 0 or past the table, with False; and it refuses a code past the
# timings and the kinds, and a policy year below 0, by name.  Compiled, each is past a
# cache, and raises IndexError rather than read or write beyond it.  Every 2-D cache is
# ten wide (spec_sec.py), so the first code past it is 10.
COMPILED_ONLY = [
    ("net_cf", (1358,), ("ok", 0.0)),
    ("net_cf", (-1,), ("ok", None)),
    ("pols_if_at", (0, 10), ("raised", "ValueError: invalid timing")),
    ("av_at", (0, 10), ("raised", "ValueError: invalid timing")),
    ("claim_pp", (0, 10), ("raised", "ValueError: invalid kind")),
    ("claims_from_av", (0, 10), ("raised", "ValueError: invalid kind")),
    ("lapse_rate_base_py", (105,), ("ok", None)),
    ("lapse_rate_base_py", (-1,), ("raised", "ValueError: point_id 1: lapse_table.csv has "
                                   "no rate for policy year -1")),
    ("is_rop_anniv", (105,), ("ok", False)),
    ("is_rop_anniv", (-1,), ("ok", False)),
    ("corridor_factor_at", (122,), ("ok", None)),
    ("mort_rate_base_at", (122,), ("ok", None)),
    ("coi_rate_guar_at", (122,), ("ok", None)),
]

# The codes inside the timing and kind caches that a cell does not take, since one
# numbering serves the three timing families and every 2-D cache is the timings' width
# (spec_sec.py): there the cell itself refuses the code, compiled as in modelx.  As
# (cell, the code's name or number).
CODES_IN_CACHE = [("pols_if_at", "BEF_PREM"), ("pols_if_at", "BEF_INT"),
                  ("av_pp_at", "BEF_NB"), ("av_pp_at", "EOM"), ("av_pp_at", "BEF_INT"),
                  ("av_at", "BEF_MAT"), ("sg_pp_at", "EOM"), ("loan_bal_pp_at", "BEF_PREM"),
                  ("claim_pp", "MATURITY"), ("claim_pp", 9), ("claims_from_av", 6),
                  ("claims_from_av", 9)]


def _refusal_cases(s_at_82):
    """Every refusal the compiled model must make as modelx does, as (case, the table, the
    edits, the References, [(position, cell, arguments)], the Data cells to read).

    A position, not a label, since a table ``Data`` refuses has no keys to give: each is
    the row's place in the table written, ``Projection``'s ``idx``, which the test indexes
    ``Projection`` by in modelx too.
    """
    committed, extract = _committed(), _extract()

    def at(table, label):
        return list(table.index).index(label)

    cases = [
        ("past its cover, on the extract", _set("duration_mth", [102], 732)(extract),
         None, {}, [(at(extract, 102), "proj_len", ())], ()),
        ("beyond the tables, on the extract", extract, None, {},
         [(0, cell, args) for cell, args, _ in BEYOND if args[0] >= 0], ()),
        ("an issue age of 17, on the extract", _set("age_at_entry", [102], 17)(extract),
         {"coi_rates.csv": _coi_from(17)}, {}, [(at(extract, 102), "proj_len", ()),
                                               (at(extract, 102), "result_cf", ())], ()),
        ("a load of 1: the cure payment", _set("load_prem_rate", [1], 1.0)(committed),
         None, {}, [(0, "cure_premium_pp", (0,)), (0, "cure_premium_pp", (500,))], ()),
        ("a class the table lacks, on the extract",
         _set("rate_class", [103, 106], "SuperPNT")(extract),
         {"coi_rates.csv": _coi_with("SuperPNT")}, {},
         [(0, "result_cf", ())], ("class_factor",)),
        ("a scale the COI table lacks, on the extract",
         _set("rate_class", [103, 106], "PNT")(extract), None, {},
         [(0, "result_cf", ())], ("coi_schedule",)),
        ("a label written as text, on the extract", _relabelled(107, "7x")(extract),
         None, {}, [(at(extract, 107), "point_id", ())], ("point_id",)),
        ("codes no cell of the family takes, inside the caches", committed, None, {},
         [(0, cell, (0, code)) for cell, code in CODES_IN_CACHE], ()),
    ]
    for case, edit, point, _, refs, _ in NOT_ISSUED:
        table = edit(s_at_82)(committed)
        cases.append((case, table, None, refs, [(at(table, point), "proj_len", ()),
                                                (at(table, point), "result_cf", ())], ()))
    for case, edit, edits, cell, _, label, _ in UNJOINED:
        table = edit(committed)
        call = "point_id" if cell == "point_id" else "result_cf"
        cases.append((case, table, edits, {}, [(at(table, label), call, ())], (cell,)))
    point = _label(committed, "twin", 2, 0)
    for case, column, value, _, data in UNDECODABLE:
        cases.append((case, _set(column, [point], value)(committed), None, {},
                      [(at(committed, point), "result_cf", ())], tuple(data)))
    for case, edit, _ in MALFORMED:
        cases.append((case, edit(committed), None, {}, [(0, "result_cf", ())],
                      ("model_point_table",)))
    for case, file, edit, check, _ in MALFORMED_KEYS + MALFORMED_RATES:
        cases.append((case, committed, {file: edit}, {}, [(0, "net_cf", (0,))], (check,)))
    return cases


def _modelx_did(call):
    """``("ok", value)`` or ``("raised", "Type: message")``: what modelx did on ``call``."""
    try:
        return ("ok", call())
    except Exception as err:                    # what modelx raised is what compiled must
        return ("raised", _raised(err))


@pytest.mark.cython
def test_the_compiled_model_refuses_what_modelx_refuses(sec_build, s_at_82, tmp_path):
    """Compiled, the model refuses what modelx refuses, with modelx's error and message.

    A ``ValueError`` raised in a cell typed ``long long`` or ``double`` propagates out of
    the compiled model as out of modelx.  So, each on its own inputs and References
    (:func:`_refusal_cases`): ``proj_len()`` refuses a point past its cover, naming it by
    ``point_id()``, on the extract labelled otherwise than by position (:func:`_extract`),
    and every case of :data:`NOT_ISSUED`, issued past the age charges cease, at or past
    the end of the projection, or past its grace, on the committed table; and a point
    issued below ``issue_age_min``, which the compiled caches are not sized for, on the
    extract.  Each reader of a padded table refuses a key below it, policy year 0, an age
    below the point's COI scale or a year that is no anniversary, on the extract
    (:data:`BEYOND`; a key below 0 is past the cache, below); the cure payment at a load
    of 1 raises ``ULSG_US_S``'s ``ZeroDivisionError`` with Python's text, where a C
    division's would differ; every case of :data:`UNJOINED`, on the extract a class and a
    COI scale the tables lack and a label written as text among them, of
    :data:`UNDECODABLE`, each case and whitespace variant among them, of :data:`MALFORMED`,
    the int64 bound among them, and of :data:`MALFORMED_KEYS` and :data:`MALFORMED_RATES`,
    a negative age among them, is refused by a projection, and by the ``Data`` cell that
    checks it, compiled as in modelx, so a compiled ``Data`` cell refuses each value its
    modelx cell refuses; and a code a cell does not take, inside its cache, is refused by
    the cell (:data:`CODES_IN_CACHE`).

    And the refusals that are the compiled model's alone (:data:`COMPILED_ONLY`): a month
    past the ``t`` cache either side, a code past the timing and kind caches, a policy
    year or an anniversary past the ``y`` cache either side and an age past the ``a``
    cache, each raising ``IndexError`` compiled, beside what modelx does.

    The cases share one directory, which each case's inputs overwrite in turn, and one
    copy of the compiled package: each child reads its inputs afresh, as the compiled
    ``Data`` reads its files once an import.
    """
    build = sec_build(SEC)
    cases = _refusal_cases(s_at_82)
    cases.append(("compiled only", _committed(), None, {},
                  [(0, cell, args) for cell, args, _ in COMPILED_ONLY], ()))
    dest = tmp_path / "refused"
    folder = compiled_case(build, dest)
    found, refused = [], 0
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
                expected = next(w for c, a, w in COMPILED_ONLY if (c, a) == (cell, args))
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


@pytest.mark.cython
def test_the_compiled_model_reads_the_schedule_of_a_point_without_a_charge(sec_build,
                                                                           tmp_path):
    """Compiled, a point without a charge reads its schedule as modelx does, as at E.

    On :data:`UNCHARGED`'s table, beside the copy's SC7, the compiled model's
    ``surr_charge_rate_max()`` and ``surr_charge_runoff_years()`` on each point without a
    charge are 3eacf45's numbers, pinned, of type float, and modelx's, and on the point
    whose id the table lacks each raises ``KeyError``, naming the point, with modelx's
    message; ``Data``'s two joins and ``has_surr_charge_schedule`` are modelx's arrays,
    NaN where the id is missing included, and each point's ``net_cf(0)`` is modelx's.
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

    On the two points of :func:`_longest_cover`, S's point 3 at issue age 18, issued now
    and 120 months on, whose cover runs 1,236 months, a cold ``net_cf`` in the last month
    runs the account value's chain from the end of the frame back to ``t_entry()``, 1,235
    months, and the cells above and below it, 1,253 and 1,256 deep in modelx on a model
    just read (:func:`test_every_chain_runs_one_cell_a_month_from_a_cold_start`), and
    compiled it runs on the C stack, which the interpreter's recursion limit does not
    count.  1 MiB is the stack MSVC gives an executable's main thread unless the
    executable asks for more: a host that embeds Python, where python.exe itself asks for
    2,000,000 bytes.  A thread whose stack is reserved at 1 MiB stands in for it on every
    platform (``sec_support.run_compiled``), and in one each call runs cold and returns
    modelx's number, identically on x86-64 (``sec_support.exact_here``) and to 1e-12
    elsewhere.  With gcc the calls need between 256 and 384 KiB, about 250 bytes a level:
    at the 325 to 433 bytes a level MSVC took on WholeLife's chain, they would need 400 to
    530 KiB.  A stack too small kills the child, and the test fails naming the stack.  The
    thread's stack is read back too, from Windows or from glibc, and must be at most 1 MiB
    and a page: a stand-in larger than asked for would stand for nothing.  And the calls
    run again on the child's main thread, which is what ``run_sec.py --cython`` runs on.

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
        file: (lambda name: lambda _: pd.read_csv(longest.parent / name))(file)
        for file in ("coi_rates.csv", "mort_table.csv")})
    model = mx.read_model(folder, name=_name("longest"))
    try:
        calls, want = {}, {}
        for key, label, frame in zip(point_keys(model), labels, LONGEST_FRAMES):
            proj = projection(model, key)
            assert (proj.duration_mth_init(), proj.t_entry(), proj.proj_len()) == frame
            last = proj.proj_len() - 1
            assert last - proj.t_entry() == 1235 and proj.age(last) == 120, label
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

    ``ULSG_US_S`` caps its lapse rate at ``lapse_rate_cap``, a Reference nothing refuses
    set past 1, and under :data:`LAPSE_PAST_1` S's point 2's annual rate is 1.2 in its
    first month, where ``1 - (1 - q)^(1/12)`` has no real value.  modelx computes it
    complex and the account value's and the margin's checks raise ``TypeError``
    (:func:`test_a_lapse_rate_past_1_makes_each_check_raise_as_in_ulsg_us_s`).  Compiled,
    the power is C's ``pow`` of a negative base, NaN, and NaN runs through every count and
    residual after it, so each of those checks' ``abs(residual) <= tolerance`` is false:
    the compiled model reports a failed check rather than an error.  The shadow account's
    check reads no count and holds, as in modelx.  This pins that behaviour, which
    ``model-sec.md`` records among what the compiled model does differently, on the twin
    of S's point 2: the rate itself is 1.2, its monthly rate NaN, the two checks
    ``False`` and the shadow account's ``True``.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "lapse")
    committed = _committed()
    idx = list(committed.index).index(_label(committed, "twin", 2, 0))
    model = _read(folder, "lapse_past_1_compiled", LAPSE_PAST_1)
    try:
        assert projection(model, idx).lapse_rate(0) == 1.2
        assert type(projection(model, idx).lapse_rate_mth(0)) is complex
    finally:
        model.close()
    checks = ("check_av_roll_fwd", "check_margin", "check_sg_roll_fwd")
    job = {"refs": LAPSE_PAST_1,
           "calls": {idx: [("lapse_rate", (0,)), ("lapse_rate_mth", (0,)),
                           *((check, ()) for check in checks)]}}
    got = run_compiled(folder.parent, build.package.name, job)
    assert got["exit"] == 0, got["stderr"]
    assert all(got["compiled"].values()), got["compiled"]
    (rate, monthly, *verdicts) = got["values"][idx]
    assert rate == ("ok", 1.2), rate
    assert monthly[0] == "ok" and math.isnan(monthly[1]), monthly
    assert verdicts == [("ok", False), ("ok", False), ("ok", True)], verdicts


# A compiled model's Reference set after it has computed, in a child of its own: what the
# base Projection, an ItemSpace made before the change and one made after give for
# expenses(12), before inflation_rate is set to 0 and after.
STALE_CHILD = """\\
import json, sys
sys.path.insert(0, sys.argv[1])
model = __import__(sys.argv[2]).mx_model
p = model.Projection
early = p[5]
values = [p.expenses(12), early.expenses(12)]
p.inflation_rate = 0.0
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
    which ULSG ships at 2.5% and which moves ``expenses(12)`` on every point in force
    then: the base ``Projection``, the worked example's twin at ``idx`` 0, and S's point 2
    restated at its month 240, at ``idx`` 5, made before, and S's point 2 restated at 305,
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
        p.inflation_rate = 0.0
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
    modelx's: point 5's description, S's point 1 restated at its month 81, a month into
    its grace, and its first twelve rows of cash flows, of the account value and the
    shadow account, of the guarantee's diagnostics and of counts, and the block's lines for
    each point, its first twelve rows and its first twelve projection years.

    The same output is what a runner that ignored ``--build`` and ran modelx would print,
    so the runner is also given a directory that holds no build, and must refuse it,
    saying so, rather than print anything.
    """
    build = sec_build(SEC)
    runner = model_path(SEC).parent / "run_sec.py"
    for args in (("5",), ("--block",)):
        expected = _run_sec(runner, *args)
        assert _run_sec(runner, *args, "--cython", "--build", str(build.out)) == expected
    empty = tmp_path / "no_build"
    empty.mkdir()
    done = _run_sec(runner, "5", "--build", str(empty), check=False)
    stderr = done.stderr.decode(errors="replace")
    assert done.returncode != 0 and done.stdout == b"", stderr
    assert f"holds no build of {SEC} for this interpreter" in stderr, stderr
