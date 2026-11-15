"""In-force tests for UL_US_SEC: the splice, future business, counts, regeneration.

``UL_US_SEC`` is ``UL_US_S`` taught to run in force at a valuation date
(USLIB-SEC-PLAN.md, milestone M3).  It runs on two clocks: ``t`` counts months from the
valuation date, the same month for every model point, and ``duration_mth(t)`` counts the
months the policy has been in force, ``duration_mth_init() + t``.  A model point may be a
policy already in force at the valuation date, in any month of its policy year, one issued
at it, or one to be issued after it, as in ``basiclife/BasicTerm_SE``.  A policy in force
opens with six columns of state beside its count: the account value and the loan entering
month 0, which are ``UL_US_S``'s own columns, and the face in force, the free withdrawal
allowance already used in the policy year, the premiums less withdrawals paid to date and
the MEC latch.

The worked example is not restated here.  On a point issued at the valuation date the two
clocks coincide and the model is ``UL_US_S``, and ``test_model_conventions.py`` asserts
that cell by cell on the twins of S's two new-business points (T1), so every golden of
``test_universal_life_us.py`` on S's points 1 and 2, the worked example among them, holds
on this model with no number copied.  S's point 3 is in force at its own month 120, and S
already counts its months from the start of its own projection, so the twin of that point
opens at offset 0 and is a splice case (T2): at the shipped assumptions it is S's point in
every cell but those expense inflation moves, which carries S's goldens on it over.  The
conventions also hold the SEC family's other rules: every frame opens at ``t = 0``,
``pols_if`` is the ``BEF_DECR`` count, ``BEF_DECR`` is ``BEF_NB`` plus the month's new
business, new business enters once, and nothing happens before issue.  This module holds
the rest of the plan's tests (its §5.2) and the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's,
  ``result_pols`` and ``result_av`` among them.  The months straddle the product's events:
  the first anniversary, where withdrawals open; the surrender charge's first month at
  zero, the lapse shock of the year after it and the per-unit charge's step after year
  10; the month a shortfall begins; the attained age at which the splice's charges cease;
  and the last covered month.  Seven variants of S's points, in a copy of S's table and
  each with input rows of its own, add withdrawals on either death benefit option, a
  single premium with no surrender charge, a TARGET premium on a second schedule, a
  premium that fails the 7-pay and guideline premium tests, the youngest issue age, and a
  premium that takes an Option B account value past the face, where the corridor binds,
  and between them every sex and every class.
* T3, future new business: a point issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before issue and no rate evaluated there.
* D11's R1 and R2, and D3 and D5's chains: on the splice's grid no cell is called at a
  negative month, none evaluated on the books reads a month before them, and none reads
  beyond ``t + 1``; on the committed points no recursion runs backward over the frame,
  and the policy clock is a closed form; and every chain of the model runs one cell a
  month from a cold start, as far as the contract's longest cover.
* T4, the count algebra: the count rolls forward through new business and decrements,
  ``result_pols`` is S's report with the new business beside it, and multiplying
  ``policy_count`` by 2.5, with every assumption that ships at zero switched on,
  multiplies every flow and moves no per-policy value.
* T5, validation: each malformed in-force row is refused as the table is read, naming its
  point; each assumption table read at a policy year or an age is refused, naming its file
  and the column, if a key is blank, text or fractional, with the lines it is on, or if
  the keys repeat or leave a gap, with each key that repeats, its lines, and each that is
  missing; so is one whose rates, the class factors or the surrender-charge schedules
  hold a value that is blank, text or infinite, with its lines; a text value no decode
  knows raises ``UL_US_S``'s message; the future horizon is a Reference that bounds future
  business, and at 0 refuses it; a point at or past the end of the projection is refused
  by ``proj_len()``; the edges of the interface are accepted, the tables' keys written as
  floats among them, and each rule just outside its window of months; and every state S
  reaches, restated in force, is accepted on each set of inputs S runs on, but an account
  value below 0, which is refused by name.
* T6, regeneration: the committed ``model_point_table_sec.csv`` is what the generator makes
  of ``UL_US_S`` and its table as they stand, and each of its derived and future rows
  projects its S point's numbers from its month on.
* Then the two clocks on the shipped points, S's in-force point as its twin, the values
  outside cover, each new opening-state column on the variants, the survivors the end of
  the projection carries, expense inflation and the declared rates on the valuation
  clock, a check whose residual is not a number, the margin identity once a loan exceeds
  the cash value, a first 7-pay failure in policy year 7, acquisition on new business,
  the mortality cap and a NaN that reaches it, the docstrings, the shared input tables,
  what the default grid reaches, the block, an in-force extract and the runner.
* C2, the fingerprint: every committed point computes what the model computed when Phase 1
  ended, frozen at the end of this module before Phase 2 changed anything (§5.4).

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``, 0 for
the twin of S's point 3, ``-k`` for one issued ``k`` months on.

**The core grid and the full one** (USLIB-SEC-PLAN.md K6).  A UL projection runs 1,032
months, and T2 and T3 over every case, 54 splices and 11 future points, would take this
module far past three minutes in every run.  By default they run a core of 20 and 5
cases, chosen so that between them they reach every branch, every opening-state column,
every kind of valuation month and every premium pattern the full grid reaches, which
``test_the_core_grid_reaches_every_branch`` asserts.  UL premiums are monthly, the one
mode the product models, so there is no mode to reach.  The other cases, and the rules
test's scan of their rows, carry the ``sec_full`` marker and are skipped, with the reason
shown, unless ``USLIB_SEC_FULL=1`` is set.  They are never dropped: one leg of the CI
matrix sets it, so every CI run runs the full grid, and
``USLIB_SEC_FULL=1 python -m pytest -m sec_full tests/test_universal_life_us_sec.py`` runs
them alone.  Memory is the other cost: a projected point holds tens of megabytes of
cached values and their dependency graph, so a row read once, a splice case's or a point
of a temporary copy, is released as soon as it has been read (``_release``), and the
splice's rows are held one at a time, however large the grid.

Every test keeps five rules.  Each model is read under a name of its own and closed:
``test_universal_life_us.py`` reads S under its default name, and reading a model under a
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
no keys to give: its first row's key is taken from the parameter (``_first_key``).  And a
timing or a kind is passed through ``_code``, which gives the model's Reference of that
name where the model defines one and the string otherwise, and every cell-by-cell
comparison goes through ``_twin``: Phase 2 changes the call syntax only (C1), each in one
place.  At stage ``"EC"``, where the model now stands, the codes are the model's int
References (USLIB-SEC-PLAN.md R9), ``Projection`` is keyed by position, and ``_twin`` maps
S's ``claims(t, None)`` onto the total ``claims(t)``.
"""
import ast
import dataclasses
import gc
import itertools
import json
import math
import os
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
    GENERATED_COLUMNS, SEC_SPECS, TWIN_EXEMPT_DEFAULT, build_sec_table, check_generated,
    codes, compiled_case, compiled_mismatches, exact_here, fingerprint_mismatches,
    frame_mismatches, run_compiled, sweep, temp_inputs, twin_mismatches)
from us_registry import model_path, point_keys, projection

SEC, TWIN, TABLE = "UL_US_SEC", "UL_US_S", "model_point_table_sec.csv"
SPEC = SEC_SPECS[SEC]

# S's three points: 1, the worked example, on death benefit Option A, and 2, the same cell
# on Option B, both issued at the valuation date; 3, in force at its own month 120 with a
# loan, the point S opens at its own t = 0.
NEW_BUSINESS = (1, 2)
IN_FORCE = 3

# Seven more S points, in the splice's copy of S's table and never in the committed one.
# S's three points are all M35 StdNT, LEVEL at $1,800 a year on the UL9 schedule, and
# withdraw nothing, so each variant changes S's anchor cell to reach what they cannot, and
# carries one of the sexes and classes they lack:
#
# 4, withdrawals of $60 a month on Option A, F PNT: the year's free allowance is spent part
#   way through the policy year, the excess cuts the face, and the allowance restarts on the
#   anniversary;
# 5, the same withdrawals on Option B, M PPlusNT: the usage moves, the face never does;
# 6, a single premium of $50,000, capped at the guideline single premium, with no surrender
#   charge, M StdPlusNT: the 7-pay test fails in the issue month, and from policy year 8 the
#   MEC latch holds alone;
# 7, a TARGET premium of $6,000 a year, M PTob, on UL7, a second surrender charge schedule
#   of $12.00 per $1,000 run off over seven years: the guideline premium limit binds at
#   month 71 and suspends the premium until year 13, and the lapse shock falls in year 8;
# 8, LEVEL at $24,000 a year, M StdTob: the 7-pay test fails in policy year 1 by the in-year
#   test, and the guideline premium test fails from year 2;
# 9, issue age 18, the youngest the product spec issues at: its own COI rows and the
#   contract's longest cover, 1,236 months;
# 10, LEVEL at $24,000 a year on Option B, M PNT: the account value outgrows the face, and
#   the corridor binds on Option B, from month 34 to 479, 528 to 695 and 1004 to the end.
#
# Each variant is (the S point it changes, the columns it changes); the policy_id keeps the
# generated ids apart.
VARIANTS = {
    4: (1, {"policy_id": "UL-900004", "wd_pp": 60.0, "sex": "F", "rate_class": "PNT"}),
    5: (2, {"policy_id": "UL-900005", "wd_pp": 60.0, "rate_class": "PPlusNT"}),
    6: (1, {"policy_id": "UL-900006", "premium_type": "SINGLE", "premium_pp_ann": 50000.0,
            "has_surr_charge": False, "rate_class": "StdPlusNT"}),
    7: (1, {"policy_id": "UL-900007", "premium_type": "TARGET", "premium_pp_ann": 6000.0,
            "surr_charge_id": "UL7", "rate_class": "PTob"}),
    8: (1, {"policy_id": "UL-900008", "premium_pp_ann": 24000.0, "rate_class": "StdTob"}),
    9: (1, {"policy_id": "UL-900009", "age_at_entry": 18}),
    10: (2, {"policy_id": "UL-900010", "premium_pp_ann": 24000.0, "rate_class": "PNT"}),
}

# The variants' own input rows, in the copies only.  The shipped COI table covers the anchor
# cell, M StdNT 35, alone, so each new key gets the anchor's rows at a scale of its own, and
# a COI read under the wrong key reads a different number.  Issue age 18 gets rows geometric
# in the policy year, never flat, for every policy year its cover reaches, so that a scale
# read at the wrong year changes a number too.  UL7 is the second schedule.
COI_KEYS = ["sex", "rate_class", "age_at_entry", "policy_year"]
COI_SCALES = {("F", "PNT", 35): 0.70, ("M", "PPlusNT", 35): 0.55,
              ("M", "StdPlusNT", 35): 0.85, ("M", "PTob", 35): 0.95,
              ("M", "StdTob", 35): 0.90, ("M", "PNT", 35): 0.65}
YOUNGEST = 18


def _coi_rates_with_variants(rates):
    """S's COI table with rows for every key the variants and the extremes use, sorted.

    Sorted by its four keys, as ``Data.coi_rates()`` indexes it, so that pandas can slice
    a cell's scale without a warning about the index's sort order.
    """
    anchor = rates[(rates["sex"] == "M") & (rates["rate_class"] == "StdNT")
                   & (rates["age_at_entry"] == 35)]
    blocks = [rates]
    for (sex, rate_class, age), scale in COI_SCALES.items():
        blocks.append(anchor.assign(
            sex=sex, rate_class=rate_class, age_at_entry=age,
            coi_rate_guar=(anchor["coi_rate_guar"] * scale).round(6),
            provenance="test copy"))
    years = list(range(1, 105))
    blocks.append(pd.DataFrame({
        "sex": "M", "rate_class": "StdNT", "age_at_entry": YOUNGEST, "policy_year": years,
        "coi_rate_guar": [round(0.08 * 1.075 ** (y - 1), 6) for y in years],
        "provenance": "test copy"}))
    return pd.concat(blocks, ignore_index=True).sort_values(COI_KEYS, ignore_index=True)


def _surr_charges_with_ul7(table):
    """S's surrender charge schedules with UL7: $12.00 per $1,000, run off over 7 years."""
    ul7 = pd.DataFrame([{"surr_charge_id": "UL7", "sc_per_1000_init": 12.0,
                         "runoff_years": 7, "provenance": "test copy"}])
    return pd.concat([table, ul7], ignore_index=True)


SPLICED_EDITS = {"coi_rates.csv": _coi_rates_with_variants,
                 "surr_charge_table.csv": _surr_charges_with_ul7}

# T2's months (USLIB-SEC-PLAN.md §7.3), by event rather than month by month, so that the
# grid is sized for what T2 and Phase 2's C4 both need.  On S's points 1 and 2: 1, the
# first month after issue; 11, the month before the first anniversary, which falls at
# t = 1; 12, the first anniversary, where withdrawals open and the policy year steps; 13,
# the month after it; 107, the first month the surrender charge is zero; 108, the first of
# the lapse shock's year; 113, the middle of it; 119, its last month, after which the
# per-unit charge steps down; 120, the anniversary that ends the shock; and 125, mid year
# 11.  Then point 1's last covered month, 1031, a frame of one row whose t = 1 is the month
# the survivors are carried into; its months 779 and 780, either side of attained age 100,
# where the splice's charges cease; point 2's month 676, where its shortfall begins; and
# S's in-force point restated at months 1, 6 and 12 after its own 120.  On the variants:
#   4, withdrawals on A: 12, the first withdrawal month; 13, the year's usage entering the
#     month; 15, after the face cut, with the allowance spent; 23, the last month of a
#     cutting year; 24, the anniversary, the usage restarted on the cut face;
#   5, withdrawals on B: 13 and 24;
#   6, the single premium: 1, 12, and 85, policy year 8, where the MEC latch holds alone;
#   7, TARGET: 70, 71 and 72 around the month the guideline premium limit binds; 83 and 84,
#     either side of UL7's shock year; 144, where year 13's guideline level premium room
#     opens;
#   8, over-funded LEVEL: 1; 3, where the 7-pay test first fails, in the valuation month,
#     from an is_mec_init of 0; 11; and 84, policy year 8;
#   9, issue age 18: 12, and its last covered month, 1235;
#   10, over-funded on Option B: 33 and 34, either side of the month the corridor first
#     binds, and 479 and 480, either side of the month it first stops.
# T3's: S's points issued one month on, which puts the policy anniversaries a month off the
# valuation years, and twelve, which puts them back on; and each variant issued thirteen
# months on, more than a year, so that its months before issue read policy years -1 and 0,
# where a cell read without its guard would show: issued within a year, a point reads
# policy year 0 alone before issue (USLIB-SEC-PLAN.md D4).
PT_MTHS = (1, 11, 12, 13, 107, 108, 113, 119, 120, 125)
VARIANT_MTHS = {3: (1, 6, 12), 4: (12, 13, 15, 23, 24), 5: (13, 24), 6: (1, 12, 85),
                7: (70, 71, 72, 83, 84, 144), 8: (1, 3, 11, 84), 9: (12, 1235),
                10: (33, 34, 479, 480)}
SPLICES = (tuple(("derived", p, d) for p in NEW_BUSINESS for d in PT_MTHS)
           + (("derived", 1, 1031), ("derived", 1, 779), ("derived", 1, 780),
              ("derived", 2, 676))
           + tuple(("derived", p, d) for p, mths in VARIANT_MTHS.items() for d in mths))
IN_FORCE_TWINS = (("twin", IN_FORCE, 0),)
FUTURES = (tuple((p, k) for p in NEW_BUSINESS for k in (1, 12))
           + tuple((p, 13) for p in VARIANTS))

# The default run's cases (the module docstring), each with what it is there for.  The
# rest of SPLICES and FUTURES run with USLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("twin", 3, 0): "S's in-force row, at offset 0: 120 months in, with a loan",
    ("derived", 3, 6): "S's in-force row restated mid-year: the loan entering month 0",
    ("derived", 1, 11): "the month before the first anniversary, which falls at t = 1",
    ("derived", 1, 12): "the first anniversary: withdrawals open, the policy year steps",
    ("derived", 1, 107): "the first month without a surrender charge",
    ("derived", 1, 113): "mid shock year: the shock ends inside the frame, at t = 7",
    ("derived", 1, 1031): "the last covered month: t = 1 is the month carried into",
    ("derived", 2, 12): "Option B on the first anniversary; the block test's row",
    ("derived", 2, 119): "the shock year's last month: the unit charge steps at t = 1",
    ("derived", 2, 676): "Option B in the month its shortfall begins",
    ("derived", 4, 13): "withdrawals: the year's usage entering month 0",
    ("derived", 4, 15): "withdrawals: the face already cut, and cut again at t = 0",
    ("derived", 4, 24): "withdrawals on an anniversary: the usage restarts on the cut face",
    ("derived", 5, 13): "withdrawals on Option B: the usage moves, the face never",
    ("derived", 6, 85): "a single premium, no surrender charge: the MEC latch alone",
    ("derived", 7, 71): "TARGET: the guideline premium cap binds at t = 0 on cum_prem_init",
    ("derived", 7, 84): "TARGET under the cap, in the 7-year schedule's shock year",
    ("derived", 8, 3): "over-funded LEVEL: the 7-pay test fails at t = 0, the GPT later",
    ("derived", 9, 12): "issue age 18: its own COI rows, the longest cover",
    ("derived", 10, 33): "over-funded on Option B: the corridor binds from t = 1",
}
CORE_FUTURES = {
    (1, 1): "issued a month off the valuation anniversaries",
    (2, 12): "Option B issued on them, a year on; the block test's row",
    (4, 13): "withdrawals, issued more than a year on: policy year -1 before issue",
    (6, 13): "the single premium in its issue month, with no surrender charge",
    (7, 13): "TARGET's cumulative premium and guideline premium limit from issue",
}

SEC_FULL = os.environ.get("USLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "USLIB_SEC_FULL=1 (USLIB-SEC-PLAN.md K6)"))

# What the splice sets in both models, S and SEC alike, before either evaluates anything.
# Expense inflation is the one input UL reads on the valuation clock that moves (D7): S
# inflates from issue and SEC from the valuation date, so at the shipped 2.5% the expenses
# of a point opened at d differ by design, and at 0 both factors are 1.  The clock itself
# is then asserted on its own, at the shipped rate.  The declared rates are flat as
# shipped, so no input table moves with d, and their clock is asserted with a formula
# override, which the splice leaves alone so that it runs unchanged once the model compiles
# (K7); that test also moves the dynamic lapse multiplier off 1 and compares the result
# with S.  The rest switch on what the shipped values leave unreached:
#   expense_acq, which ships at 0, so that acquisition on future business shows at all;
#   mort_ae_factor at 0.56, which leaves lives at the end of every frame, so that the
#     survivors carried into t = proj_len(), which S's roll-forwards read there, are
#     compared on every row, and which keeps every class's annual rate below 1, StdTob's
#     oldest at 1.75 x 0.56 = 0.98: at an A/E of 1 its product passes 1 at attained age
#     113, where both models cap it (the mortality cap test);
#   charges_cease_age at 100, inside every frame, where the shipped 121 is one past the
#     table's last age: premiums, charges and withdrawals cease in cover, at attained age
#     100, policy month 780 at issue age 35;
#   lapse_shock_mult at 10, so that the shock year's rate, 0.04 x 10, meets the lapse
#     rate's cap of 0.35, which the shipped multiplier of 2 never reaches.
# rider_charge_pp is S's placeholder and reads no state, so it stays at its zero.  The
# identity does not depend on the values, only on both models having the same ones.
SPLICED_REFS = {"inflation_rate": 0.0, "expense_acq": 250.0, "mort_ae_factor": 0.56,
                "charges_cease_age": 100, "lapse_shock_mult": 10.0}

# Every assumption that ships at zero, switched on in T4 at the value T2 gives it, in the
# SEC model itself, so that every flow is nonzero on some point (§5.2, T4, precised at
# M11): expense_acq, the one Reference above that ships at 0, and the planned withdrawal,
# a column at 0 on every S point, at variant 4's $60 a month on every committed row.
SWITCHED_ON = {"expense_acq": SPLICED_REFS["expense_acq"]}
SWITCHED_ON_COLUMNS = {"wd_pp": VARIANTS[4][1]["wd_pp"]}

# The cells T2 and T3 skip beyond T1's, which already drop result_pols as a whole (the
# spec's exempt).  S's own accessors of the point it opens: proj_len counts from the
# valuation date on SEC and from S's own start on S, so it differs by d, or by -k, by
# design, and frame_mismatches asserts what it must get right, that both frames end at the
# same instant; duration_mth_init is d, or -k, on SEC and S's own on S; and av_pp_init and
# loan_bal_init, S's columns, hold S's month-0 values on S and month d's on SEC.  Every
# cell that reads them is compared.  A future point compares pols_if_at at every key but
# one, which _issued_later leaves out: S's returns its issued policies under every timing
# at its t = 0, where SEC's BEF_NB counts them as the month's new business, not yet in
# (D5).  BEF_DECR and BEF_MAT keep S's meaning, pols_if, in every month, and BEF_NB is S's
# from the month after issue.
SPLICE_EXEMPT = (TWIN_EXEMPT_DEFAULT | SPEC.exempt
                 | {"proj_len", "duration_mth_init", "av_pp_init", "loan_bal_init"})
FUTURE_EXEMPT = TWIN_EXEMPT_DEFAULT | SPEC.exempt | {"proj_len", "duration_mth_init"}


def _issued_later(name, args):
    """The ``arg_map`` of a point issued at or after the valuation date, compared with S.

    S's keys as they are, but ``pols_if_at(0, "BEF_NB")``, S's issue month, which it
    leaves out (``None``): there S's cell counts the issued policies, as it does under
    every timing, and this model counts them as the month's new business, not yet in.
    """
    return None if name == "pols_if_at" and args == (0, "BEF_NB") else args

# The result_cf columns that expense inflation moves, and the cells they are made of: on
# the committed points, at the shipped 2.5%, the only places an in-force row departs from
# S.
INFLATED = ("expenses", "net_cf")
INFLATION_CELLS = frozenset({"inflation_factor", "expenses", "margin_expense", "net_cf",
                             "result_cf"})

# The decrement rates keyed by month, none of which may be evaluated before issue (R1,
# D4), and the readers keyed by a policy year or an attained age.
DECREMENT_RATES = ("mort_rate", "mort_rate_mth", "lapse_rate_base", "lapse_rate",
                   "lapse_rate_mth")
KEYED_BY_YEAR = ("prem_persistency_py", "coi_rate_guar_py", "lapse_rate_base_py")
KEYED_BY_AGE = ("corridor_factor_at", "mort_rate_base_at")

# The cells that scale with policy_count.  Every other cell is a per-policy amount, a rate,
# a clock or a flag, and must not move when the count does.  The two residuals are
# relative, so a doubled count moves them in the last digits.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz",
    "pols_death", "pols_lapse", "pols_maturity", "premiums", "prem_to_av", "coi",
    "maint_fee", "mth_deduction", "inv_income", "av_at", "av_change", "surr_charge",
    "claims_from_av", "claims_over_av", "claims", "claims_death", "claims_lapse",
    "withdrawals", "wd_fees", "expenses",
    "premium_taxes", "margin_expense", "margin_mortality", "net_cf",
    "check_av_roll_fwd_resid", "check_margin_resid", "result_cf", "result_pols"})

# What T4 multiplies policy_count by: not a whole number, because a count of policies need
# not be one, so that a flow which read the count as whole policies would not follow it.
COUNT_FACTOR = 2.5

# The counted cells T4 holds otherwise than to 1e-12 of themselves, value by value (§5.2,
# T4, precised at M4 and M10): the differences of counted amounts, whose sides round apart
# where they nearly cancel, as the change in the account value in force does on point 6 at
# t = 0 by 3.4e-10 of itself, the mortality margin by 1.5e-12 and the net cash flow and
# the expense margin by 8.4e-13 and 2.1e-13, each to 1e-12 of its largest magnitude on the
# point; and the two residuals, whose exact value is 0, to the residuals' floor of 1e-9.
# And the one counted cell no point makes nonzero, the maturities, which a contract with
# no maturity date never has.
CANCELLING = frozenset({"av_change", "net_cf", "margin_expense", "margin_mortality"})
RESIDUALS = frozenset({"check_av_roll_fwd_resid", "check_margin_resid"})
ALWAYS_ZERO = frozenset({"pols_maturity"})

# result_pols' columns, in its order: the count, the new business within it, the month's
# deaths and lapses in processing order, the maturities, always zero, then S's two monthly
# decrement rates, which no count moves.
RESULT_POLS = ["pols_if", "pols_new_biz", "pols_death", "pols_lapse", "pols_maturity",
               "mort_rate_mth", "lapse_rate_mth"]
OUTFLOWS = RESULT_POLS[2:5]
RATES = RESULT_POLS[5:]
REPORTS = ("result_cf", "result_pols", "result_av")

# The timings and kinds the model knows: the count's three, which S's stub names and
# answers with pols_if for each; the account value's four, before each BOM event, and
# av_at's EOM; and the claim kinds, with claims_from_av's MATURITY, always zero.  At stage
# EC each is the model's int Reference of its name, through _code, and S's
# claims(t, kind=None) is two cells, claims_death and claims_lapse, and their total,
# claims(t), which this module calls by name (USLIB-SEC-PLAN.md D11, R12).
TIMINGS = ("BEF_MAT", "BEF_NB", "BEF_DECR")
AV_TIMINGS = ("BEF_PREM", "BEF_WD", "BEF_FEE", "BEF_INV")
KINDS = ("DEATH", "LAPSE")
AV_KINDS = ("DEATH", "LAPSE", "MATURITY")

# The opening state, in Data's order, and the cells running in force adds to UL_US_S's or
# gives a new meaning, each of which the symbol map must name.
STATE = ("av_pp_init", "loan_bal_init", "sum_assured_init", "wd_used_year_init",
         "cum_prem_init", "is_mec_init")
NEW_CELLS = ("policy_count", "duration_mth_init", "t_entry", "omega_mth", "is_active",
             "pols_new_biz", "pols_if_at", *STATE, *KEYED_BY_YEAR, *KEYED_BY_AGE,
             "surr_charge_rate_max", "surr_charge_runoff_years", "is_db_option_a",
             "is_db_option_b", "is_gpt", "is_level_premium", "is_single_premium",
             "is_target_premium", "check_av_roll_fwd_resid", "check_margin_resid",
             "result_pols", "coi_rate_last_year", "wd_pp_mth", "point_id", "coi_schedule",
             "claims_death", "claims_lapse")

INFLATION = 0.025       # the shipped inflation_rate, which the inflation test reads

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A report evaluates each column in ascending t, so a forward
# recursion, through t - 1, finds the month before already cached, and the committed
# points' sweep runs under a limit of 15, as UL_US_S's does.  A backward recursion over
# the frame, through t + 1, opens a chain as long as the frame, and the shortest frame
# longer than a month is 24, so a limit of 40 lets every forward sweep through and stops
# every backward one.
CALL_DEPTH = 40

# How deep a cold call may run beyond its chain, one cell a month from its month back to
# t_entry() (D5): the cells above the chain and those below it, the first month's charges
# and Data's first reads of its tables.  A cold net_cf in the last month, which descends
# the account value's chain, runs 17 cells beyond it, on 1,032 months and at the contract's
# longest cover alike, the deepest of them the month-0 COI rate's extent, the vector it
# reads, coi_schedules, the check of its table, below it, and the read; each chain called
# alone runs at most 9 beyond (measured at M16, one more each than at stage E).  Term's 16
# would leave no level for another Data cell below a table reader, so UL allows 20.  Any
# chain of two cells a month runs a frame's length beyond.
CHAIN_OVERHEAD = 20


# ---------------------------------------------------------------------------
# Helpers

_names = itertools.count(1)


def _name(tag):
    """A model name that no other read in this session uses."""
    return f"{SEC}_{tag}_{next(_names)}"


def _code(proj, label):
    """The argument that selects timing or kind ``label`` on ``proj``, a Space.

    The model's int Reference of that name where it defines one, as Phase 2 does (R9:
    ``pols_if_at(t, BEF_DECR)`` with ``BEF_DECR = 2``), else the string itself, as at stage
    ``"E"``.  The conventions' ``_timing`` does the same, so every call in this module reads
    the same at both stages.
    """
    value = proj.refs.get(label)
    return value if isinstance(value, int) and not isinstance(value, bool) else label


def _twin(s_proj, sec_proj, *, arg_map=None, **kwargs):
    """``sec_support.twin_mismatches``, which every comparison in this module calls here.

    It passes the SEC Space's ``sec_support.codes``, which map S's timing and kind strings
    to the int codes Phase 2 gives them, and the spec's ``twin_arg_map``, which maps S's
    ``claims(t, None)``, the total, onto Phase 2's ``claims(t)`` and skips S's
    ``claims(t, kind)``, whose values are Phase 2's ``claims_death`` and ``claims_lapse``
    (R12).  The spec's map runs first, then the caller's ``arg_map``, on S's arguments.  At
    stage ``"E"`` there were no codes; every comparison goes through here, so each took
    Phase 2's codes and split when they came.
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

    ``month`` is the row's ``source_mth``: 0 for a twin, S's point 3 included, which S
    opens at its own ``t = 0``; ``d`` for a derived row; ``-k`` for a future one.  The twins
    keep S's ``point_id`` and ``policy_id``, so the S policy is the twin's.
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


def _release(model, key):
    """Drop the ItemSpace at ``key``, the registry's key, and every value it has cached.

    A projected UL point holds tens of megabytes of cached values and their dependency
    graph.  The splice's rows and the doubled and extract copies' points are each needed
    once, so each is released when read, as ``run_sec.py --block`` releases its points
    (USLIB-SEC-PLAN.md F5).  Asked for again, the ItemSpace is made afresh and recomputes.
    """
    del model.Projection[key]


def _committed():
    """The committed SEC table as the file holds it, unvalidated, indexed by point_id."""
    return pd.read_csv(model_path(SEC).parent / TABLE, index_col="point_id")


# The labels of the extract the refusals read beside the committed table: 100 plus the
# committed label, in reverse order, so that no label is its position plus one and a label
# read as one names another point (USLIB-SEC-PLAN.md R4).
EXTRACT_LABELS = tuple(range(109, 100, -1))


def _extract():
    """The committed table as an administration extract would hold it: without the
    generator's columns, and labelled :data:`EXTRACT_LABELS`, row 9 first."""
    extract = _committed().drop(columns=list(GENERATED_COLUMNS)).iloc[::-1]
    extract.index = pd.Index(EXTRACT_LABELS, name="point_id")
    return extract


def _sec_inputs(tmp_path, table, edits=None):
    """A copy of the product directory whose SEC table is ``table``; its SEC folder."""
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=edits)


def _read_edited(tmp_path, edit):
    """UL_US_SEC read from a copy whose SEC table is ``edit(_committed())``."""
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


def _moved(point, month, **columns):
    """An edit that moves row ``point`` to policy month ``month`` and sets ``columns``."""
    def edit(table):
        table = _set("duration_mth", [point], month)(table)
        for column, value in columns.items():
            table = _set(column, [point], value)(table)
        return table
    return edit


def _refused(call, message):
    """``call()`` raises ``ValueError`` with ``message``, inside modelx's wrapper.

    modelx re-raises an error inside a formula as ``FormulaError``, with the original type
    and message on its second line, which :func:`_raised` reads, so that line is asserted
    rather than a modelx class, as a compiled model's bare ``ValueError`` is read too.
    """
    with pytest.raises(Exception) as excinfo:
        call()
    line = _raised(excinfo.value)
    assert line.startswith("ValueError: ") and message in line, str(excinfo.value)


def _raised(err):
    """The line that names an error: modelx's ``FormulaError`` puts it second."""
    lines = [line for line in str(err).splitlines() if line.strip()]
    if type(err).__name__ == "FormulaError" and len(lines) > 1:
        return lines[1]
    return f"{type(err).__name__}: {lines[0] if lines else ''}"


# The S cells no report or check of UL_US_S evaluates (USLIB-SEC-PLAN.md §7.3, C), which
# the splice compares only because _sweep_s evaluates them first.
NEVER_REACHED = ("is_shortfall", "cure_premium_pp", "cum_prem_pp", "gpt_limit", "gpt_ok",
                 "seven_pay_limit", "is_mec", "wd_used_year", "wd_free_pp", "policy_year")


def _sweep_s(proj):
    """Evaluate on an S point what the comparisons compare: the sweep, and more.

    :func:`sec_support.sweep` reaches none of :data:`NEVER_REACHED`, of the three inputs
    of the tax tests or of ``pols_if_at`` on ``UL_US_S``, because no result column or check
    reads them, and a cell S never evaluates is compared nowhere.  So the guideline premium
    and 7-pay tests, the MEC latch, the year's withdrawal usage, the shortfall trigger and
    the cure payment are evaluated here, over the frame, and ``pols_if_at`` at each of its
    timings, so that the splice and the future comparison see them too.
    """
    sweep(proj)
    proj.gsp(), proj.glp(), proj.seven_pay_prem()
    for t in range(proj.proj_len()):
        for name in NEVER_REACHED:
            proj.cells[name](t)
        for timing in TIMINGS:
            proj.pols_if_at(t, _code(proj, timing))


def _compare(s_proj, sec_proj, month, exempt, arg_map=None, columns=None):
    """Where SEC's row departs from S's point from S month ``month`` on.

    First the frames, ``result_cf`` (over ``columns``, or every column both hold),
    ``result_pols`` and ``result_av``, SEC row ``t`` against S row ``t + month``, frames
    ending together; then every cell of S's but ``exempt``, at every argument S cached
    inside its frame from ``month`` on, through ``arg_map``, moved onto SEC's clock.  All
    to 1e-9 relative with no absolute floor: a count late in a long frame falls far below
    1e-7, as the committed point valued at 1008 holds 1.8e-10 of a policy, and a floor of
    1e-9 would pass any error in it (§5.2, precised at M11).  ``UL_US_S`` has no
    roll-forward residual cell, whose exact value is 0 and whose computed one is rounding
    about it, to keep the floor: its checks compute theirs inline.  Returns the mismatch
    lines, empty when the row is S's.
    """
    found = []
    for report in REPORTS:
        found += [f"{report}: {line}" for line in frame_mismatches(
            s_proj.cells[report](), sec_proj.cells[report](), t_offset=month,
            columns=columns if report == "result_cf" else None, atol=0.0)]
    return found + _twin(s_proj, sec_proj, t_offset=month, exempt=exempt,
                         arg_map=arg_map, atol=0.0)


def _continues_s(s_proj, sec_proj, month):
    """Where a committed row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison (:func:`_compare`), on the committed model at the shipped
    assumptions: frame by frame, ``result_cf``, ``result_pols`` and ``result_av``, then cell
    by cell over every cell of S's but T1's exemptions.  The shipped 2.5% expense inflation
    runs from issue in S and from the valuation date here (D7), so :data:`INFLATED`'s two
    columns, and :data:`INFLATION_CELLS`, differ by design and are left out; the inflation
    test holds them.  Every other column and cell must agree, to 1e-9 relative with no
    absolute floor.
    """
    keep = [c for c in s_proj.result_cf().columns if c not in INFLATED]
    return _compare(s_proj, sec_proj, month,
                    TWIN_EXEMPT_DEFAULT | SPEC.exempt | INFLATION_CELLS, columns=keep)


def _case_id(kind, s_point, month):
    """A case's id: ``point2-d12``, ``point3-twin0``, or ``point2-k3`` if issued later."""
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


# ---------------------------------------------------------------------------
# Fixtures


@pytest.fixture(scope="module")
def sec_read():
    """UL_US_SEC read in place, as committed, and swept once, cold; what it met.

    The model is first asked for ``duration_mth(500)`` on the twin of S point 1, and the
    keys that call leaves in ``duration_mth`` are kept.  Then every committed point is
    swept (:func:`sec_support.sweep`: ``result_cf``, the other reports and the checks), in
    table order and each column in ascending ``t``, under a recursion limit lowered to
    :data:`CALL_DEPTH`, and whatever that raises is kept, point by point, rather than
    raised.  So the record says what a cold model does, which the clock test asserts (D3,
    R2), and every test on the committed model reads a model already swept: the sweep is
    paid once, not once for each.  Returns ``(model, record)``.
    """
    model = mx.read_model(model_path(SEC), name=_name("sec"))
    first = _row(model, "twin", 1, 0)
    record = {"duration_mth(500)": first.duration_mth(500),
              "keys": list(first.cells["duration_mth"].keys()), "deep": []}
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
    yield model, record
    model.close()


@pytest.fixture(scope="module")
def sec_model(sec_read):
    """UL_US_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """UL_US_S read in place, as committed, with every point swept (:func:`_sweep_s`).

    T6 regenerates the SEC table from it, which would otherwise project every S point again
    (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the in-force tests read S's months
    off it.
    """
    model = mx.read_model(model_path(TWIN), name=_name("s"))
    for key in point_keys(model):
        _sweep_s(projection(model, key))
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


@pytest.fixture(scope="module")
def spliced(tmp_path_factory):
    """S and SEC on the splice's inputs, with :data:`SPLICED_REFS` set in both.

    S is read from a copy of the product directory whose table has the variants appended
    and whose COI and surrender charge tables carry the variants' rows
    (:data:`SPLICED_EDITS`).  SEC runs on the same assumption tables, and on a model point
    table of its own, built by the generator from the registered spec with its rows
    replaced by the cases this run selects, the core or the full grid (:func:`_selected`),
    out of this S model, so each row opens with the state of the very run it is compared
    with.  Every S point is then swept (:func:`_sweep_s`), and stays swept; each SEC row is
    projected by the case that compares it and released once compared (:func:`_settle`).

    Once S is swept the heap is frozen, so that the collections the released rows trigger
    scan the rows alone and not S's swept points, which stay alive to the end of the module
    (measured at M3, it took the core's cases from 82 s to 43 s).  In teardown the models
    are closed first, then the heap is thawed and collected, so that what the closed
    models held is freed before the next module runs, rather than left frozen beyond any
    collection's reach.
    """
    root = tmp_path_factory.mktemp("spliced")
    s_folder = temp_inputs(root / "s", model_path(TWIN),
                           model_points=_s_table_with_variants(), edits=SPLICED_EDITS)
    s = mx.read_model(s_folder, name=_name("s_spliced"))
    for ref, value in SPLICED_REFS.items():
        setattr(s.Projection, ref, value)
    derived = [(p, d) for kind, p, d in _selected(SPLICES, CORE_SPLICES)]
    spec = dataclasses.replace(SPEC, derived=tuple(derived),
                               future=tuple(_selected(FUTURES, CORE_FUTURES)))
    table, companions = build_sec_table(spec, s)
    assert companions == {}
    sec_folder = temp_inputs(root / "sec", model_path(SEC), model_points=table,
                             model_point_file=spec.model_point_file, edits=SPLICED_EDITS)
    sec = mx.read_model(sec_folder, name=_name("sec_spliced"))
    for ref, value in SPLICED_REFS.items():
        setattr(sec.Projection, ref, value)
    for key in point_keys(s):
        _sweep_s(projection(s, key))
    gc.collect()
    gc.freeze()
    try:
        yield s, sec
    finally:
        sec.close()
        s.close()
        gc.unfreeze()
        gc.collect()


@pytest.fixture(scope="module")
def splice_records():
    """What each splice row was found to do once compared, by case (:func:`_settle`)."""
    return {}


# ---------------------------------------------------------------------------
# The splice's records
#
# Each T2 and T3 case first scans its row for the rules test (_scanned), before the
# comparison with S evaluates its cells at S's keys, then compares it, then records what the
# guard test, the end-of-projection test and the core grid's reach need of the row, and
# releases it (_settle).  So each of those tests reads the records, and computes any case no
# earlier test has recorded, which keeps it whole when run alone.


def _cached_args(cells):
    """The argument tuple of every key ``cells`` has cached (:func:`sec_support._args`)."""
    n = len(cells.parameters)
    return [() if n == 0 else (key,) if n == 1 else tuple(key)
            for key in list(cells.keys())]


def _month(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _rule_breaches(proj):
    """R1 and R2's look-ahead on one row, once it has run what the splice compares.

    ``{"negative": [...], "early": [...], "ahead": [...], "edges": n}``: every cached call
    with a negative argument; every precedent keyed by a month before ``t_entry()`` of a
    call keyed by a month at or after it; every precedent keyed by a month beyond ``t + 1``
    of a call keyed by ``t``; and how many precedents of calls keyed by ``t`` the scan read,
    which must not be 0, or the two scans held of nothing.  A precedent is a call's as
    modelx's dependency graph records it.
    UL reads nothing further ahead than ``t + 1`` anywhere: R2's one exception, a read at
    the anniversary that closes the policy year, has no use here.  The row first runs what
    :func:`_sweep_s` runs on an S point, at the row's own months: the reports, the checks,
    and the cells no report reaches, the MEC latch, the tax tests, the year's withdrawal
    usage and the cure payment among them, and the count at each timing, so that a chain
    only those cells run is scanned too.
    """
    _sweep_s(proj)
    entry = proj.t_entry()
    negative, early, ahead, edges = [], [], [], 0
    for name, cells in proj.cells.items():
        t_pos = cells.parameters.index("t") if "t" in cells.parameters else None
        for args in _cached_args(cells):
            if any(_month(a) and a < 0 for a in args):
                negative.append(f"{name}{args}")
            if t_pos is None:
                continue
            t = args[t_pos]
            for node in cells.preds(*args):
                edges += 1
                params = getattr(node.obj, "parameters", None) or ()
                u = node.args[params.index("t")] if "t" in params else None
                if not _month(u):
                    continue
                if u < entry <= t:
                    early.append(f"{name}{args} -> {node.obj.name}{node.args}")
                if u > t + 1:
                    ahead.append(f"{name}{args} -> {node.obj.name}{node.args}")
    return {"negative": negative, "early": early, "ahead": ahead, "edges": edges}


# What each monthly cell holds outside cover, before issue and in the month after the
# frame, t = proj_len(), which the roll-forwards read, as its docstring says: no count
# carried, no value, premium, withdrawal, charge, rate, decrement, claim or flow, and no
# question about the contract answered yes.  The type is part of the value: an amount, a
# rate or a count is a float in every branch and a flag a bool, because Phase 2 types a
# cell by the values it returns (USLIB-SEC-PLAN.md F3).
OUTSIDE_COVER = {
    # flags
    "is_active": False, "gpt_ok": False, "is_mec": False, "is_shortfall": False,
    # premiums and withdrawals
    "premium_pp": 0.0, "prem_to_av_pp": 0.0, "prem_persistency": 0.0, "wd_pp": 0.0,
    "wd_used_year": 0.0, "wd_free_pp": 0.0, "wd_fee_pp": 0.0, "face_reduction_pp": 0.0,
    # the face, the death benefit and the cost of insurance
    "sum_assured_at": 0.0, "units": 0.0, "corridor_factor": 0.0, "av_pp_db_basis": 0.0,
    "db_pp": 0.0, "net_amt_at_risk": 0.0, "coi_rate_guar": 0.0, "coi_rate": 0.0,
    "coi_pp": 0.0, "rider_charge_pp": 0.0,
    # charges and values
    "maint_fee_pp": 0.0, "mth_deduction_pp": 0.0, "inv_income_pp": 0.0, "av_pp": 0.0,
    "loan_bal_pp_bom": 0.0, "loan_bal_pp": 0.0, "surr_charge_rate": 0.0,
    "surr_charge_pp": 0.0, "csv_pp": 0.0, "ncsv_pp": 0.0, "cure_premium_pp": 0.0,
    # the tax tests
    "cum_prem_pp": 0.0, "gpt_limit": 0.0, "seven_pay_limit": 0.0,
    # rates
    "mort_rate": 0.0, "mort_rate_mth": 0.0, "lapse_rate_base": 0.0, "lapse_rate": 0.0,
    "lapse_rate_mth": 0.0,
    # counts
    "pols_new_biz": 0.0, "pols_death": 0.0, "pols_lapse": 0.0, "pols_maturity": 0.0,
    # flows
    "premiums": 0.0, "prem_to_av": 0.0, "coi": 0.0, "maint_fee": 0.0,
    "mth_deduction": 0.0, "inv_income": 0.0, "withdrawals": 0.0, "wd_fees": 0.0,
    "surr_charge": 0.0, "expenses": 0.0, "premium_taxes": 0.0, "claims_over_av": 0.0,
    "claims": 0.0, "claims_death": 0.0, "claims_lapse": 0.0,
    "margin_expense": 0.0, "margin_mortality": 0.0, "net_cf": 0.0,
    # the cells that read t + 1, which return their zero before they read it
    "av_change": 0.0, "check_av_roll_fwd_resid": 0.0, "check_margin_resid": 0.0,
}
# 1.0, the multiplier's neutral value: no month outside cover is in a shock year.  Before
# issue the valuation clock reaches policy year 0, which is the shock year
# lapse_shock_year() gives a point with no surrender charge.
NEUTRAL = {"lapse_rate_sc_mult": 1.0}
# The policy clock, a Python int at every month, outside cover too: before issue its
# values are negative, or 0, and a cell keyed by them must not read a table there.
CLOCK = ("duration_mth", "duration", "policy_year", "age")
# The economic inputs, on the valuation clock (D7): floats at every month, one function of
# t for every point.
VALUATION_CLOCK = ("crediting_rate_ann", "comp_rate_ann", "inv_return_mth",
                   "inflation_factor", "lapse_rate_dyn_mult")
# Cells with a timing or a kind, 0.0 at every one of these outside cover.
BY_ARGUMENT = {"claim_pp": KINDS, "claims_from_av": AV_KINDS,
               "av_pp_at": AV_TIMINGS[1:], "av_at": (*AV_TIMINGS[1:], "EOM")}
# The opening timings, 0.0 before issue, and in the month after the frame what the
# survivors of its last month carry into it (CARRIED): the count, at every timing, and the
# account value per policy and in force.
OPENING = {"pols_if_at": TIMINGS, "av_pp_at": AV_TIMINGS[:1], "av_at": AV_TIMINGS[:1]}
CARRIED = ("pols_if",)
# The sets above, which together must hold every cell whose first parameter is t, once.
GUARD_SETS = {"OUTSIDE_COVER": set(OUTSIDE_COVER), "NEUTRAL": set(NEUTRAL),
              "CLOCK": set(CLOCK), "VALUATION_CLOCK": set(VALUATION_CLOCK),
              "BY_ARGUMENT, OPENING": set(BY_ARGUMENT) | set(OPENING),
              "CARRIED": set(CARRIED)}


def _monthly_cells(proj):
    """Every cell of ``proj`` whose first parameter is ``t``."""
    return {name for name, cells in proj.cells.items()
            if cells.parameters and cells.parameters[0] == "t"}


def _on_the_clocks(p, t):
    """What each cell of :data:`CLOCK` and :data:`VALUATION_CLOCK` holds at month ``t``.

    The policy clock in closed form from the point's ``duration_mth``, and the economic
    inputs from the Projection's References and ``t`` alone, the same for every point: the
    flat declared rate, and expense inflation stepping on valuation years.
    """
    d = p.duration_mth_init() + t
    rate = p.crediting_rate_curr
    excess = max(0.0, rate - rate - p.lapse_dyn_threshold)
    return {"duration_mth": d, "duration": d // 12, "policy_year": d // 12 + 1,
            "age": p.age_at_entry() + d // 12,
            "crediting_rate_ann": rate, "comp_rate_ann": rate,
            "inv_return_mth": (1 + rate) ** (1 / 12) - 1,
            "inflation_factor": (1 + p.inflation_rate) ** (t // 12),
            "lapse_rate_dyn_mult": min(p.lapse_dyn_cap, 1 + p.lapse_dyn_slope * excess)}


def _outside_cover_faults(p, where):
    """Where ``p``, an ItemSpace, departs from what each monthly cell holds outside cover.

    In every month before issue and at ``t = proj_len()``: every cell of
    :data:`OUTSIDE_COVER` and :data:`NEUTRAL`, each cell of :data:`BY_ARGUMENT` at each of
    its timings or kinds, and before issue :data:`OPENING`'s and ``pols_if``, against their
    values with their types; :data:`CLOCK` and :data:`VALUATION_CLOCK` against
    :func:`_on_the_clocks`.  At ``t = proj_len()`` the count at every timing is the
    survivors of the last month, out of its count by its deaths and lapses, in the products
    those take, and the account value per policy is the last month's close.  Then the
    keyed readers: those keyed by a policy year hold keys from 1 to the year of the last
    month, and those keyed by an attained age keys from the age at the first month on the
    books to the age of the last, so no table was read at a year or an age the policy does
    not have.  And no monthly cell holds a ``t`` past ``proj_len()``.  A cell that raises
    is a fault too, so the scan goes on.
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
    survivors = p.pols_if(L - 1) - p.pols_death(L - 1) - p.pols_lapse(L - 1)
    check("pols_if", (L,), survivors)
    for timing in TIMINGS:
        check("pols_if_at", (L, _code(p, timing)), survivors)
    bef_prem = _code(p, "BEF_PREM")
    check("av_pp_at", (L, bef_prem), p.av_pp(L - 1))
    check("av_at", (L, bef_prem), p.av_pp_at(L, bef_prem) * p.pols_if(L))
    ranges = {**{name: range(1, p.policy_year(L - 1) + 1) for name in KEYED_BY_YEAR},
              **{name: range(p.age(entry), p.age(L - 1) + 1) for name in KEYED_BY_AGE}}
    for name, allowed in ranges.items():
        outside = sorted(k for k in p.cells[name].keys() if k not in allowed)
        if outside:
            faults.append(f"{where}: {name} read at {outside[:5]}, outside "
                          f"{allowed.start}..{allowed.stop - 1}")
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
    policy there and the last month's close; the account value in force there; both
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
        "checks": (p.check_av_roll_fwd(), p.check_margin()),
        "flows": [p.premiums(L), p.pols_death(L), p.pols_lapse(L), p.expenses(L),
                  p.net_cf(L), p.claims_death(L), p.claims_lapse(L)]}


def _in_year_test(x, t):
    """Whether the 7-pay test fails in month ``t`` itself, inside the first seven years."""
    return x.policy_year(t) <= 7 and x.cum_prem_pp(t) > x.seven_pay_limit(t)


def _option_db(x, t):
    """The death benefit of the option before the corridor: the face, or face plus AV'."""
    extra = x.av_pp_db_basis(t) if x.is_db_option_b() else 0.0
    return x.sum_assured_at(t) + extra


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, every opening-state column is in use
# and the face in force is below the face at issue, so that a column read in another's
# place, or as zero, would show; and every read of the state at t = 0 is taken where it
# changes a number: the guideline premium cap on cum_prem_init, the year's allowance
# reduced by the usage already taken, a face cut in the valuation month, the MEC latch
# holding alone, the 7-pay test failing in the valuation month from a latch that is off,
# and the shortfall; and the end of the frame leaves survivors to carry.  Later in the
# frame, the branches the account value, the tax tests, the lapse shock and the age that
# ends the charges drive.
AT_VALUATION = {
    **{f"{c} in use": (lambda x, c=c: bool(x.cells[c]())) for c in STATE},
    "the face in force below the face at issue": lambda x: (
        0.0 < x.sum_assured_init() < x.sum_assured()),
    "the GPT cap at t = 0 on cum_prem_init": lambda x: (
        x.is_target_premium()
        and 0.0 < x.premium_pp(0) < x.premium_pp_ann() / 12 * x.prem_persistency(0)),
    "the allowance at t = 0 reduced by usage": lambda x: (
        x.wd_pp(0) > 0.0
        and x.wd_free_pp(0) < x.wd_free_rate * x.av_pp_at(0, _code(x, "BEF_WD"))),
    "a face cut at t = 0": lambda x: x.face_reduction_pp(0) > 0.0,
    "the MEC latch alone at t = 0": lambda x: x.is_mec(0) and not _in_year_test(x, 0),
    "the 7-pay test failing at t = 0": lambda x: x.is_mec(0) and not x.is_mec_init(),
    "the shortfall at t = 0": lambda x: x.is_shortfall(0),
    "survivors carried into proj_len()": lambda x: x.pols_if(x.proj_len()) > 0.0,
}
IN_FRAME = {
    "the death benefit floor": lambda x, t: x.av_pp_at(t, _code(x, "BEF_FEE")) < 0.0,
    "the corridor binding on Option A": lambda x, t: (
        x.is_db_option_a() and x.db_pp(t) > _option_db(x, t)),
    "the corridor binding on Option B": lambda x, t: (
        x.is_db_option_b() and x.db_pp(t) > _option_db(x, t)),
    "the lapse shock": lambda x, t: x.lapse_rate_sc_mult(t) > 1.0,
    "the lapse rate's cap binding": lambda x, t: (
        x.lapse_rate_base(t) * x.lapse_rate_sc_mult(t) * x.lapse_rate_dyn_mult(t)
        > x.lapse_rate_cap),
    "charges ceased in cover": lambda x, t: x.age(t) >= x.charges_cease_age,
    "the guideline premium test failed": lambda x, t: not x.gpt_ok(t),
    "a TARGET premium cut to 0 by the cap": lambda x, t: (
        x.is_target_premium() and x.premium_pp(t) == 0.0
        and x.age(t) < x.charges_cease_age),
}


def _branches(x):
    """The names in :data:`AT_VALUATION` and :data:`IN_FRAME` that hold of row ``x``."""
    reached = {what for what, holds in AT_VALUATION.items() if holds(x)}
    return reached | {what for what, holds in IN_FRAME.items()
                      if any(holds(x, t) for t in range(x.proj_len()))}


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
        record = {"negative": [], "early": [], "ahead": [], "edges": 0,
                  "raised": _raised(err)}
    records[case] = record
    return record


def _settle(records, case, model, key):
    """Record what the tests after the splice need of a row, and release it.

    ``case`` is the row's (row_kind, S point, source_mth) and ``key`` its registry key in
    ``model``, the splice's SEC model.  A T2 or T3 case calls this once it has compared
    the row, whatever the comparison found, so the row is released either way.  To the
    scan's record (:func:`_scanned`) it adds the row's :func:`_branches` for an in-force
    row, what :func:`_carry` reads at ``t = proj_len()`` and, last, so that its key ranges
    see every read the others made, :func:`_outside_cover_faults`.  A row no case has
    scanned is scanned here first.  A row that raises is recorded as raising, which each of
    those tests reports.
    """
    try:
        proj = projection(model, key)
        record = records.get(case) or _scanned(records, case, proj)
        record.update(branches=set(), carry=None, guard=[])
        if record["raised"] is None:
            record["branches"] = _branches(proj) if case[0] != "future" else set()
            record["carry"] = _carry(proj)
            record["guard"] = _outside_cover_faults(proj, _case_id(*case))
    except Exception as err:                    # recorded, and reported by each test
        record = records.setdefault(case, {"negative": [], "early": [], "ahead": [],
                                           "edges": 0})
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
    opening state is zero.  For the same reason it is the test that catches a policy month
    passed as ``t`` (R1a) and a look-back that stops at the wrong month.  The frame
    comparisons read SEC row ``t`` against S row ``t + d`` in every column of
    ``result_cf``, ``result_av`` and the columns of ``result_pols`` both reports hold, and
    fail frames that end apart.  The cell comparison then evaluates every cell of S's but
    :data:`SPLICE_EXEMPT`, at every argument S cached inside its own frame from month ``d``
    on, moved onto SEC's clock, to 1e-9 relative with no absolute floor
    (:func:`_compare`): the account value at every timing, the loan, the face, the year's
    withdrawal usage, the cumulative premium, the guideline premium and 7-pay tests and
    the MEC latch, the counts and both checks among them.  An S cell this model lacked
    would fail it.

    Both checks read the opening account value in force of the month after the frame, so
    the survivors the last month carries into ``t = proj_len()`` are compared through them.
    The row is scanned for the rules test first (:func:`_scanned`), then compared, then
    recorded for the tests after this one and released (:func:`_settle`).
    """
    s, sec = spliced
    key = _row_key(sec, kind, s_point, month)
    s_proj, sec_proj = _point(s, s_point), projection(sec, key)
    try:
        _scanned(splice_records, (kind, s_point, month), sec_proj)
        assert _compare(s_proj, sec_proj, month, SPLICE_EXEMPT) == []
    finally:
        _settle(splice_records, (kind, s_point, month), sec, key)


# ---------------------------------------------------------------------------
# T3 -- future new business


@pytest.mark.parametrize(
    "s_point, k",
    [_case(case, CORE_FUTURES, _case_id("future", case[0], -case[1]))
     for case in FUTURES])
def test_future_new_business_is_the_s_projection_k_months_on(spliced, splice_records,
                                                             s_point, k):
    """Issued k months after the valuation date, the point is S's projection k months on.

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at the end of the projection, in
    ``result_cf``, ``result_av`` and every column of ``result_pols`` S's has, and every cell
    of S's but :data:`FUTURE_EXEMPT` agrees at every argument S cached inside its own
    frame, moved ``k`` later, ``pols_if_at`` at every timing but ``"BEF_NB"`` in the issue
    month (:func:`_issued_later`), to 1e-9 relative with no absolute floor
    (:func:`_compare`).  An S cell this model lacked would fail it.  Before issue
    every column of the three reports is an exact zero, and the policies arrive in month
    ``k`` as new business.  A single premium is collected once, in the issue month.

    The last assertions are R1 and D4's base rule made testable.  After every report, no
    decrement rate keyed by month has been evaluated at a month before issue, and no table
    keyed by a policy year or an attained age has been read below year 1 or the issue age,
    where it has been read at all: a single premium never reads the premium persistency
    scale.
    A chain based at ``t == 0`` rather than at ``t_entry()``, or a rate evaluated before
    the month is asked whether it is in cover, still gives the right numbers.  This is the
    only test that sees the first, and the guard test sees the second too.

    The pre-issue rows are asserted present before they are asserted zero, in each of the
    reports: a frame that opened at issue would have none, its zeros would hold of nothing,
    and the comparisons with S, which start at issue, would not see it.  The row is scanned
    for the rules test first (:func:`_scanned`), then compared, then recorded for the tests
    after this one and released (:func:`_settle`).
    """
    s, sec = spliced
    key = _row_key(sec, "future", s_point, -k)
    s_proj, sec_proj = _point(s, s_point), projection(sec, key)
    try:
        _scanned(splice_records, ("future", s_point, -k), sec_proj)
        frames = {report: sec_proj.cells[report]() for report in REPORTS}
        assert _compare(s_proj, sec_proj, -k, FUTURE_EXEMPT, _issued_later) == []
        for report, frame in frames.items():
            assert list(frame.index[:k]) == list(range(k)), report
            assert (frame.loc[:k - 1] == 0.0).all().all(), report
        assert sec_proj.pols_new_biz(k) == sec_proj.policy_count() == 1.0
        early = {name: sorted(t for t in sec_proj.cells[name].keys() if t < k)
                 for name in DECREMENT_RATES}
        assert not any(early.values()), f"rates evaluated before issue: {early}"
        floors = {**dict.fromkeys(KEYED_BY_YEAR, 1),
                  **dict.fromkeys(KEYED_BY_AGE, sec_proj.age_at_entry())}
        for name, floor in floors.items():
            keys = sorted(sec_proj.cells[name].keys())
            assert all(key >= floor for key in keys), f"{name} read at {keys[:5]}"
        assert sec_proj.cells["mort_rate_base_at"].keys(), "no mortality rate was read"
        if sec_proj.is_single_premium():
            single = min(sec_proj.premium_pp_ann(), sec_proj.gsp())
            assert [sec_proj.premium_pp(t) for t in range(sec_proj.proj_len())] == [
                single if t == k else 0.0 for t in range(sec_proj.proj_len())]
    finally:
        _settle(splice_records, ("future", s_point, -k), sec, key)


# ---------------------------------------------------------------------------
# D11's R1 and R2, D3's closed-form clock and D5's chains


@pytest.mark.parametrize("grid", [pytest.param("core", id="core"),
                                  pytest.param("full", id="full", marks=FULL_ONLY)])
def test_no_cell_is_called_before_the_valuation_date_or_reads_far_ahead(spliced,
                                                                        splice_records,
                                                                        grid):
    """R1, its look-back and R2's look-ahead, on the rows T2 and T3 compare: core or rest.

    Each is a rule of how the model computes, not of what, so no number shows a breach,
    and on a point issued at ``t = 0`` the two clocks coincide and hide it from T1 too.
    The splice's rows are points in force at every month T2 names, the variants among them,
    and points issued later, and on each the reports, the checks and the cells no report
    reaches are run first, at the row's own months (:func:`_rule_breaches`):

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and
      a compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  The keys of
      the readers keyed by a policy year or an attained age are held to it too.
    * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
      ``t_entry()`` on read a month before it.  On a point issued later a chain based at
      ``t == 0``, as ``UL_US_S``'s account value, loan, face, cumulative premium, TARGET
      cap, MEC latch and count all were, reads the pre-issue zeros, so no number shows it
      and no argument goes negative.  This is the test that holds those eight bases at
      ``t_entry()`` (R1a).
    * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month beyond
      ``t + 1``, as modelx's dependency graph records each cached call's precedents.  UL
      has no read further ahead, so R2's one exception has no use here.

    Each row was scanned by the T2 or T3 case that compared it, before it compared it
    (:func:`_scanned`), so the scan holds what the row computes of itself and not the
    cells the comparison asks of it at S's keys, and a row no case has scanned is scanned
    here.  The core case covers the core's rows, the
    full case every other row of the full grid, with ``USLIB_SEC_FULL=1``.  The
    new-business twins in the splice's table are no case's, and are left out: on them the
    clocks coincide, and T1 compares them with S cell by cell.  The closed-form clock and
    the recursion depth are asserted on the committed model, in the tests after this one.
    """
    cases = [case for case in GRID if (case in CORE_GRID) == (grid == "core")]
    negative, early, ahead, raised, unscanned = [], [], [], [], []
    for case in cases:
        record, where = _record_of(spliced, splice_records, case), _case_id(*case)
        negative += [f"{where}: {call}" for call in record["negative"]]
        early += [f"{where}: {read}" for read in record["early"]]
        ahead += [f"{where}: {read}" for read in record["ahead"]]
        if record["raised"]:
            raised.append(f"{where}: {record['raised']}")
        elif not record["edges"]:
            unscanned.append(where)
    assert cases, f"the {grid} grid has no rows"
    assert not raised, f"rows that raised: {raised[:10]}"
    assert not unscanned, f"rows whose scan read no precedent: {unscanned[:10]}"
    assert not negative, f"called before the valuation date: {negative[:10]}"
    assert not early, f"read before issue from the books: {early[:10]}"
    assert not ahead, f"read beyond t + 1: {ahead[:10]}"


def test_the_policy_clock_is_a_closed_form_and_no_recursion_runs_backward(sec_read):
    """D3 and R2's recursions, on the committed model as it was first swept, cold.

    Both need a model on which nothing had been evaluated yet, which is what the fixture
    held when it made the record asserted here:

    * D3: the policy clock is the closed form.  Called first, ``duration_mth(500)``
      evaluates ``duration_mth`` once, where ``BasicTerm_SE``'s recursion would evaluate
      it at all 501 months from 0.
    * R2's recursions run forward: under modelx's recursion limit lowered to
      :data:`CALL_DEPTH`, every committed point is swept, each column in ascending ``t``.
      A forward recursion, through ``t - 1``, finds the month before already cached and
      stays shallow, which is why D3 is asserted on its own.  A backward recursion over the
      frame, through ``t + 1``, keeps every step within the look-ahead but opens a chain as
      long as the frame, which a compiled model would run on the C stack (F7), and fails
      here.
    """
    record = sec_read[1]
    assert record["duration_mth(500)"] == 500
    assert record["keys"] == [500]
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


def _one_cell_a_month(p, label, cell, args, t):
    """Whether a cold ``cell(*args)`` at month ``t`` on ``p`` runs one cell a month.

    It must run at least as deep as the months from ``t`` back to ``t_entry()``, or it did
    not run its chain cold, and at most :data:`CHAIN_OVERHEAD` cells deeper.  Returns the
    finding, or nothing.
    """
    depth, chain = _cold_depth(p, cell, args), t - p.t_entry()
    if chain <= depth <= chain + CHAIN_OVERHEAD:
        return []
    return [f"point {label}: {cell}{args} cold runs {depth} cells deep, where one cell a "
            f"month back to t_entry() {p.t_entry()} is {chain} and {CHAIN_OVERHEAD} more "
            f"are allowed"]


def _longest_cover(tmp_path):
    """A copy whose table holds S point 1 at issue age 18, issued now and 120 months on.

    ``UL_US_S``'s frame from issue is ``12 * (omega_age - issue age + 1)`` months, so the
    longest cover is at the youngest issue age the product spec issues at, 18: 1,236
    months, and the longest frame is that issued 120 months on, the shipped
    ``future_horizon_mth``, 1,356 months, whose chains stop at ``t_entry()``.  The copy's
    COI table gains the ``(M, StdNT, 18)`` rows of :func:`_coi_rates_with_variants`,
    geometric in the policy year.
    """
    committed = _committed()
    now, later = _label(committed, "twin", 1, 0), _label(committed, "future", 1, -25)
    table = _set("duration_mth", [later], -120)(
        committed.loc[[now, later]].assign(age_at_entry=YOUNGEST))
    return _sec_inputs(tmp_path, table, edits=SPLICED_EDITS), (now, later)


# Each chain of the model and the cell that heads it, called cold at the last month the
# chain reaches: (cell, its month as months from proj_len(), its timing, the chain's own
# recursive cell).  They are called in this order on one fresh read, an order in which no
# chain is reached before its own head is called: the loan, the face, the cumulative
# premium, the MEC latch, the count and the account value.  The MEC latch reads the
# cumulative premium in the first seven policy years, already cached by then; every other
# chain reads none of the others on the points this test reads, which withdraw nothing.
CHAIN_HEADS = (("loan_bal_pp", -1, None, "loan_bal_pp_bom"),
               ("sum_assured_at", -1, None, "sum_assured_at"),
               ("cum_prem_pp", -1, None, "cum_prem_pp"),
               ("is_mec", -1, None, "is_mec"),
               ("pols_if_at", 0, "BEF_NB", "pols_if_at"),
               ("av_pp_at", 0, "BEF_PREM", "av_pp_at"))


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_every_chain_runs_one_cell_a_month_from_a_cold_start(tmp_path):
    """Called cold, each chain runs one cell a month back to ``t_entry()``, no more (D5).

    No number shows how deep a chain runs, and a compiled model runs it on the C stack, so
    a chain of two cells a month, which gives the same numbers, needs twice the stack on
    every platform (F7).  ``UL_US_S``'s account value ran through five cells a month and its
    loan through two; here each forms the previous month's close itself.  On a model just
    read, nothing is cached, so modelx's stack trace counts how deep a call runs, against
    one cell a month and :data:`CHAIN_OVERHEAD` more (:func:`_one_cell_a_month`):

    * ``net_cf`` in the last month, on a read of its own: the deepest call a projection
      makes, down the account value's chain, which caches every other on the way, and what
      bounds the stack a compiled model needs;
    * then, on a second read, each of :data:`CHAIN_HEADS` alone, in an order that leaves
      each chain cold until its own head is called, which is checked: so a chain that a
      ``net_cf`` call reaches from the side, the loan's, the face's, the cumulative
      premium's, the MEC latch's, the count's, is measured too, where a ``net_cf`` call
      would have found it cached.

    On S's point 1 issued now, 1,032 months, and on its point 3, in force 120 months with a
    loan; and at the contract's longest cover, issue age 18, issued now and 120 months on
    (:func:`_longest_cover`).
    """
    committed = _committed()
    extremes, labels = _longest_cover(tmp_path)
    reads = [(model_path(SEC), [_label(committed, "twin", 1, 0),
                                _label(committed, "twin", IN_FORCE, 0)]),
             (extremes, list(labels))]
    found = []
    for folder, points in reads:
        for label in points:
            fresh = mx.read_model(folder, name=_name("cold"))
            try:
                p = _point(fresh, label)
                last = p.proj_len() - 1
                found += _one_cell_a_month(p, label, "net_cf", (last,), last)
            finally:
                fresh.close()
            fresh = mx.read_model(folder, name=_name("chains"))
            try:
                p = _point(fresh, label)
                end = p.proj_len()
                for cell, offset, timing, chain in CHAIN_HEADS:
                    if len(p.cells[chain].keys()):
                        found.append(f"point {label}: {chain} was reached before {cell} "
                                     f"was called, so its chain was not cold")
                        continue
                    t = end + offset
                    args = (t,) if timing is None else (t, _code(p, timing))
                    found += _one_cell_a_month(p, label, cell, args, t)
            finally:
                fresh.close()
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
    last month's count less its deaths and lapses, exactly, the products they take.  And
    ``"BEF_MAT"``, the count before any maturity, is the ``"BEF_DECR"`` count in every
    month, that one included, ``UL_US_S``'s meaning, since nothing matures.

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
                                  - p.pols_lapse(end - 1)), point_id
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(end))
        carried = (pols["pols_if"] - pols[OUTFLOWS].sum(axis=1)).shift(1)
        expected = carried.fillna(p.pols_if_init()) + pols["pols_new_biz"]
        assert ((pols["pols_if"] - expected).abs() <= 1e-12).all(), point_id


def test_result_pols_is_s_report_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's, column for column, with ``pols_new_biz`` second (D5).

    T1 skips the report as a whole, because its frame has a column S's lacks (the spec's
    exempt), so it is compared here, on every twin: on the two issued at the valuation
    date and on S's in-force point, all at offset 0.  Every column S's report has agrees,
    to 1e-9, frames ending together, and ``pols_new_biz`` holds the count in the issue
    month and 0 in every other, so 0 throughout on the point in force.  The counts and
    rates carry no inflation, so the shipped assumptions serve.
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
        assert frame_mismatches(theirs, mine, t_offset=month) == [], point_id
        issue = -int(table.at[point_id, "duration_mth"])
        assert list(mine["pols_new_biz"]) == [
            p.policy_count() if t == issue else 0.0 for t in mine.index], point_id


def _switched_on(folder, tag):
    """The model in ``folder``, read under a name of its own, :data:`SWITCHED_ON` set."""
    model = mx.read_model(folder, name=_name(tag))
    for ref, value in SWITCHED_ON.items():
        setattr(model.Projection, ref, value)
    return model


def _scaled_apart(name, got, want, peak):
    """Whether counted cell ``name`` is off its scaled value ``want``, by T4's rules.

    To 1e-12 of itself; :data:`CANCELLING`'s cells to 1e-12 of ``peak``, their largest
    scaled magnitude on the point; :data:`RESIDUALS` to their floor of 1e-9.
    """
    if name in RESIDUALS:
        return abs(got - want) > 1e-9
    return abs(got - want) > 1e-12 * (peak if name in CANCELLING else abs(want))


def test_scaling_the_count_scales_every_flow_and_no_per_policy_value(tmp_path):
    """``policy_count`` is a weight: 2.5 times the count, 2.5 times every flow, the same per
    policy.

    The committed table, with the planned withdrawal switched on
    (:data:`SWITCHED_ON_COLUMNS`), and a copy with every count multiplied by
    :data:`COUNT_FACTOR`, are each read with :data:`SWITCHED_ON` set before either
    computes anything: every assumption that ships at zero is on at the value the splice
    gives it, so that every flow is nonzero on some point, the acquisition, the
    withdrawals and their fees among them, which the shipped zeros leave 0 on every point
    (§5.2, T4, precised at M11).  On every point ``result_cf`` and the counts of
    ``result_pols`` are 2.5 times the committed table's, element by element, to 1e-12
    relative: a scaled count is a computed float, which may come back from the CSV within
    two ulps (``sec_support``'s module docstring).  So is every other cell of
    :data:`COUNTED`, at every argument the sweep of the committed table's point cached
    (:func:`_sweep_s`), the counts at each timing, the account value in force, the cost of
    insurance and the claims beyond the account value among them, which no report shows;
    but the differences of counted amounts, :data:`CANCELLING`, each to 1e-12 of its
    largest magnitude on the point, and the two residuals, :data:`RESIDUALS`, to their
    floor of 1e-9 (:func:`_scaled_apart`).  Every column of the reports' counts and flows,
    and every cell of :data:`COUNTED`, is nonzero on some point, but the maturities, which
    the contract never has (:data:`ALWAYS_ZERO`).  ``result_pols``'s two rates, and every
    cell outside :data:`COUNTED` (the premium, the account value at every timing, the
    death benefit, the loan, the face, the opening state, the tax tests, the rates, both
    clocks, the flags, ``result_av``), are the committed table's exactly, at every argument
    that sweep cached.  So a flow that dropped the count, or read it as whole policies,
    which a table of counts of 1 hides from every comparison with S, fails here.  Each
    point is released once compared.
    """
    table = _committed().assign(**SWITCHED_ON_COLUMNS)
    base = _switched_on(_sec_inputs(tmp_path / "base", table), "counted")
    scaled = _switched_on(_sec_inputs(tmp_path / "scaled", table.assign(
        policy_count=COUNT_FACTOR * table["policy_count"])), "scaled")
    counted = sorted(COUNTED - set(REPORTS))
    columns, nonzero = set(), set()
    try:
        for key, scaled_key in zip(point_keys(base), point_keys(scaled)):
            one, many = projection(base, key), projection(scaled, scaled_key)
            _sweep_s(one)
            for report in REPORTS[:2]:
                b, d = one.cells[report](), many.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                for column in b.columns:
                    if column in RATES:
                        assert d[column].equals(b[column]), (key, report, column)
                        continue
                    want = COUNT_FACTOR * b[column]
                    peak = want.abs().max() if column in CANCELLING else want.abs()
                    bad = (d[column] - want).abs() > 1e-12 * peak
                    assert not bad.any(), (key, report, column, list(bad[bad].index))
                    columns.add(column)
                    if (b[column] != 0.0).any():
                        nonzero.add(column)
            for name in counted:
                cached = _cached_args(one.cells[name])
                wants = [COUNT_FACTOR * one.cells[name](*args) for args in cached]
                peak = max(map(abs, wants), default=0.0)
                for args, want in zip(cached, wants):
                    got = many.cells[name](*args)
                    assert not _scaled_apart(name, got, want, peak), (key, name, args, got,
                                                                      want)
                if any(wants):
                    nonzero.add(name)
            assert many.check_av_roll_fwd() and many.check_margin(), key
            assert _twin(one, many, exempt=TWIN_EXEMPT_DEFAULT | COUNTED, rtol=0.0,
                         atol=0.0) == []
            _release(base, key)
            _release(scaled, scaled_key)
    finally:
        scaled.close()
        base.close()
    zero = sorted({*counted, *columns} - nonzero)
    assert zero == sorted(ALWAYS_ZERO), f"0 on every point: {zero}"


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault.  The checks run over the whole
# table as it is read, in Data, and the message names the file it read and the column or
# every point at fault.  A blank cell reads as NaN, and so does a text cell once the checks
# coerce the column to numbers, so each is refused as a count, a duration or a balance
# that is not a number.  The repeated point_id holds another policy under the same label,
# as a bad extract would, so that the check must look at the labels and not at whole rows.
# The point_ids are the committed table's: 1 and 2, S's new business; 3, S's in-force
# point at 120; 4, S point 1 at 12, the first anniversary; 5, S point 1 at 113; 6, S point
# 3 six months on, at 126; 7, S point 2 at 676; 8, S point 1 at 1008; 9, issued 25 months
# on.  Each check over a window of policy months is refused in the window's first month and
# its last, where an off-by-one would let a row through (§5.2, T5, precised at M10): the
# year's usage on the first anniversary and on later ones; the face above 0 and at most the
# face at issue from month 1, the first in force; and the MEC latch from month 1 to month
# 84, whose month before is in policy year 7, the last the 7-pay test runs in, and at 12,
# whose month before is in policy year 1, a cent past that year's limit.  The edges test
# and test_each_rule_reads_the_months_just_outside_it read the months just outside, 11 and
# 13, 0 and 85, and the latch at the limit.  A {file} in a message is the table's
# filename: every case is read from a file of its own (the malformed fixture).


def _drop(column):
    return lambda table: table.drop(columns=column)


_NUMBER = ("{{file}}: {column} must be a number, zero or more; it is not at point_id "
           "[{point}]")
_AV_NUMBER = ("{file}: av_pp_init must be a number, zero or more: no policy in force "
              "holds a negative account value, so restate a point in permanent "
              "shortfall no later than the last month its account value is still zero "
              "or more; it is not at point_id [{point}]")
_CUM_NUMBER = "{file}: cum_prem_init must be a number; it is not at point_id [6]"
_MEC_CODE = ("{{file}}: is_mec_init must be 0 or 1, an int code; it is not at point_id "
             "[{point}]")
_NOT_IN_FORCE = ("{{file}}: {column} must be 0 on a policy not yet in force, "
                 "duration_mth 0 or less; it is not at point_id [{point}]")
_ANNIV_USAGE = ("{{file}}: wd_used_year_init must be 0 on a point valued on a policy "
                "anniversary, duration_mth a multiple of 12, where the year's free "
                "allowance restarts; it is not at point_id [{point}]")
_LATCH = ("{{file}}: is_mec_init must be 1 where the 7-pay test has already failed, "
          "cum_prem_init above seven_pay_prem times the policy years to date, in the first "
          "seven; it is not at point_id [{point}]")
_FACE_HELD = ("{{file}}: sum_assured_init must be above 0 on a policy in force, "
              "duration_mth above 0, which holds a face; it is not at point_id [{point}]")
_FACE_ISSUED = ("{{file}}: sum_assured_init must be at most sum_assured, the face at "
                "issue, since face increases are not modelled; it is not at point_id "
                "[{point}]")

# VUL's rule for model point values (USLIB-SEC-PLAN.md §7.3, *Model point values*), which
# UL takes at its C step: the columns a projection reads beyond the in-force interface's,
# each present, and each value of the contract a number in the quantity's range, the face
# at issue above 0, the premium, the withdrawal and the tax limits' inputs zero or more,
# the load from 0 to 1 and the surrender-charge flag True or False alone, as pandas reads
# those words, so that 1, 0, 1.0, 0.0 and a blank are refused (§7.8, *Flag spellings*).
# The issue age is a finite number below 2**53 in size, and the duration below 2**53
# months, where their int64 vectors hold them; a fractional age truncates, as UL_US_S's
# int does (§7.2, *For M16 and later*, item 5).  Each case breaks one rule: the faces sit
# on new-business points, which no rule on the face in force reads, and the 7-pay premium
# on S point 1 at 1008, past the seven years the latch's rule reads it in.
READ_COLUMNS = ("age_at_entry", "sex", "rate_class", "sum_assured", "db_option",
                "qual_test", "premium_type", "premium_pp_ann", "load_prem_rate", "wd_pp",
                "has_surr_charge", "surr_charge_id", "gsp", "glp", "seven_pay_prem")
_FACE_AT_ISSUE = ("{{file}}: sum_assured must be a number above 0, the face at issue, "
                  "which every policy holds; it is not at point_id [{point}]")
_LOAD = ("{{file}}: load_prem_rate must be a number from 0 to 1; it is not at point_id "
         "[{point}]")
_FLAG = "{{file}}: has_surr_charge must be True or False; it is not at point_id [{point}]"
_AGE_FINITE = ("{{file}}: age_at_entry must be a finite number; it is not at point_id "
               "[{point}]")
_AGE_INT64 = ("{{file}}: age_at_entry must be below 2**53 in size; it is not at point_id "
              "[{point}]")
_DURATION_INT64 = ("{{file}}: duration_mth must be below 2**53 months in size; it is not "
                   "at point_id [{point}]")

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
    ("a fractional duration", _set("duration_mth", [6], 126.5),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [6]"),
    ("a blank duration", _set("duration_mth", [9], float("nan")),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [9]"),
    ("a text duration", _set("duration_mth", [6], "x126"),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [6]"),
    ("issued beyond the horizon", _set("duration_mth", [9], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [9]"),
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("policy_count", "duration_mth", *STATE)],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[4]].assign(policy_id="UL-900099")]),
     "{file}: point_id [4] appears more than once"),
    *[(f"a {what} av_pp_init", _set("av_pp_init", [point], value),
       _AV_NUMBER.format(file="{file}", point=point))
      for what, point, value in (("negative", 6, -1.0), ("blank", 7, float("nan")),
                                 ("text", 4, "x1244"), ("infinite", 8, float("inf")))],
    *[(f"a {what} {column}", _set(column, [point], value),
       _NUMBER.format(column=column, point=point))
      for what, column, point, value in (
          ("negative", "loan_bal_init", 6, -1.0), ("text", "loan_bal_init", 6, "x"),
          ("negative", "sum_assured_init", 5, -1.0),
          ("infinite", "sum_assured_init", 5, float("inf")),
          ("text", "sum_assured_init", 5, "100k"),
          ("negative", "wd_used_year_init", 5, -1.0),
          ("text", "wd_used_year_init", 5, "five"))],
    *[(f"a {what} cum_prem_init", _set("cum_prem_init", [6], value), _CUM_NUMBER)
      for what, value in (("blank", float("nan")), ("text", "x"),
                          ("infinite", float("inf")))],
    *[(f"is_mec_init {value!r}", _set("is_mec_init", [point], value),
       _MEC_CODE.format(point=point))
      for point, value in ((4, 2), (5, 0.5), (6, -1), (7, float("nan")), (8, "yes"))],
    *[(f"{column} before issue", _set(column, [point], value),
       _NOT_IN_FORCE.format(column=column, point=point))
      for column, point, value in (
          ("av_pp_init", 1, 100.0), ("loan_bal_init", 9, 10.0),
          ("sum_assured_init", 2, 100000.0), ("wd_used_year_init", 9, 5.0),
          ("cum_prem_init", 9, 50.0), ("is_mec_init", 2, 1))],
    ("a zero face in force", _set("sum_assured_init", [5], 0.0),
     _FACE_HELD.format(point=5)),
    ("a face above the face at issue", _set("sum_assured_init", [5], 100000.01),
     _FACE_ISSUED.format(point=5)),
    ("usage on the first anniversary", _set("wd_used_year_init", [4], 10.0),
     _ANNIV_USAGE.format(point=4)),
    ("usage on a later anniversary", _set("wd_used_year_init", [3], 10.0),
     _ANNIV_USAGE.format(point=3)),
    ("usage on an anniversary, moved there", _moved(6, 24, wd_used_year_init=10.0),
     _ANNIV_USAGE.format(point=6)),
    ("no latch after a failure in policy year 1", _set("cum_prem_init", [4], 7000.0),
     _LATCH.format(point=4)),
    ("no latch after a failure in policy year 7",
     _moved(5, 84, cum_prem_init=50000.0), _LATCH.format(point=5)),
    # The first month of each window from month 1 not yet met there above, the face's and
    # the latch's, and the latch a cent past the 7-pay limit of policy year 1.
    ("a zero face in force in its first month", _moved(4, 1, sum_assured_init=0.0),
     _FACE_HELD.format(point=4)),
    ("a face above the face at issue in its first month",
     _moved(4, 1, sum_assured_init=100000.01), _FACE_ISSUED.format(point=4)),
    ("no latch after a failure in the first month", _moved(4, 1, cum_prem_init=7000.0),
     _LATCH.format(point=4)),
    ("no latch a cent past the 7-pay limit", _set("cum_prem_init", [4], 6702.11),
     _LATCH.format(point=4)),
    # Every column a projection reads, by VUL's rule for model point values (the comment
    # above READ_COLUMNS): present, and each value of the contract a number in its range.
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in READ_COLUMNS],
    *[(f"a {what} sum_assured", _set("sum_assured", [point], value),
       _FACE_AT_ISSUE.format(point=point))
      for what, point, value in (("zero", 1, 0.0), ("negative", 2, -1.0),
                                 ("blank", 9, float("nan")), ("text", 1, "100k"),
                                 ("infinite", 2, float("inf")))],
    *[(f"a {what} {column}", _set(column, [point], value),
       _NUMBER.format(column=column, point=point))
      for column, point in (("premium_pp_ann", 4), ("wd_pp", 6), ("gsp", 7), ("glp", 3),
                            ("seven_pay_prem", 8))
      for what, value in (("negative", -0.01), ("blank", float("nan")), ("text", "x"),
                          ("infinite", float("inf")))],
    *[(f"a load of {what}", _set("load_prem_rate", [point], value),
       _LOAD.format(point=point))
      for what, point, value in (("-0.01", 5, -0.01), ("1.01", 6, 1.01),
                                 ("blank", 7, float("nan")), ("text", 8, "6%"))],
    ("loads past 1 at two points", _set("load_prem_rate", [1, 9], 2.0),
     _LOAD.format(point="1, 9")),
    *[(f"has_surr_charge {value!r}", _set("has_surr_charge", [point], value),
       _FLAG.format(point=point))
      for point, value in ((2, "yes"), (3, float("nan")), (4, 1), (5, 0), (6, 1.0),
                           (7, 0.0))],
    *[(f"a {what} age_at_entry", _set("age_at_entry", [point], value),
       _AGE_FINITE.format(point=point))
      for what, point, value in (("blank", 1, float("nan")), ("text", 3, "35x"),
                                 ("infinite", 9, float("inf")))],
    ("an issue age of 2**53", _set("age_at_entry", [2], 2.0 ** 53),
     _AGE_INT64.format(point=2)),
    ("an issue age past int64", _set("age_at_entry", [9], -1e30),
     _AGE_INT64.format(point=9)),
    ("a duration of 2**53 months", _set("duration_mth", [3], 2.0 ** 53),
     _DURATION_INT64.format(point=3)),
    ("durations of 2**53 months at two points",
     lambda t: _set("duration_mth", [5], -(2.0 ** 53))(_set("duration_mth", [8], 1e30)(t)),
     _DURATION_INT64.format(point="5, 8")),
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


def _first_key(model):
    """The key of the committed table's first row, which a refused table cannot give.

    Its label while ``Projection`` is keyed by ``point_id``, at stage ``"E"``, and its
    position, 0, once it is keyed by ``idx`` (``us_registry``'s two parameters).
    ``us_registry.projection`` reads the table to check the key, and the table is what is
    refused, so this is the one place the module indexes ``Projection`` without it.
    """
    return 0 if model.Projection.parameters == ("idx",) else int(_committed().index[0])


@pytest.mark.parametrize("case, edit, message", MALFORMED, ids=[c[0] for c in MALFORMED])
def test_a_malformed_in_force_row_is_refused_naming_its_point(malformed, case, edit,
                                                               message):
    """``Data.model_point_table()`` refuses the table, naming the fault (D6, T5).

    And so does the first projection of a point, the table's first, read on its own: the
    projection reaches the table through ``model_point()``, and a compiled model's must
    reach the same check, rather than a value it has no number for.
    """
    folder, files = malformed
    model = mx.read_model(folder, name=_name("malformed"))
    try:
        model.Data.model_point_file = files[case]
        text = message.format(file=files[case])
        _refused(model.Data.model_point_table, text)
        _refused(model.Projection[_first_key(model)].result_cf, text)
    finally:
        model.close()


# Each assumption table read at a policy year or an attained age, with one fault in its key
# column, as an extract or an edit by hand can leave it: a blank key, which pandas reads as
# a missing value, a key written as text, a fractional one, keys that repeat or leave a
# gap, a first policy year missing and no row at all.  The blank is the case that matters
# most: UL_US_S's readers take a table's extent from the key column as pandas reads it,
# where a blank last key is a missing value the extent skips, so the table is cut short
# and every later year reads the last good row without a word.  Here each table is checked
# once, in the Data cell its reader takes its extent from, and refused naming the file and
# the column: the lines a key that is blank, text or fractional is on, and each key that
# repeats, with its lines, and each that is missing.  Each case is (case, the file, its
# edit, the Data cell that checks it, the message), and the message is matched whole.  The
# lines count the header as line 1: the policy year y of a table that starts at year 1 is
# on line y + 1, and the anchor cell's year y of the COI scale too; the age tables start at
# age 18, on line 2.
_WHOLE = "{file}: {column} must be a whole number; it is not on line {lines}"
_RUNS = {"policy_year": ("{file}: the policy years must run from 1, one row a year, "
                         "without a gap or a repeat; "),
         "age": "{file}: the ages must run one row an age, without a gap or a repeat; "}
_COI_RUN = ("coi_rates.csv: the policy years of each sex, rate_class and age_at_entry "
            "must run from 1, one row a year, without a gap or a repeat; at ('M', "
            "'StdNT', 35), ")


def _write_at(column, row, value):
    """An edit that writes ``value`` into ``column`` of the table's ``row``-th row."""
    def edit(table):
        cells = table[column].astype(object)
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
# checks it, its first key).
KEY_TABLES = {
    "prem_persistency.csv": ("policy_year", "prem_persistency_last_year", 1),
    "lapse_table.csv": ("policy_year", "lapse_last_year", 1),
    "corridor_factors.csv": ("age", "corridor_age_last", 18),
    "mort_table.csv": ("age", "mort_age_last", 18),
}
MALFORMED_KEYS = [
    *[(f"{file}: {what}", file, _write_at(column, row, value), check,
       _WHOLE.format(file=file, column=column, lines=f"[{line}]"))
      for file, (column, check, _) in KEY_TABLES.items()
      for what, row, value, line in (
          ("its last key blank", -1, float("nan"),
           {"prem_persistency.csv": 17, "lapse_table.csv": 12, "corridor_factors.csv": 105,
            "mort_table.csv": 104}[file]),
          ("a key written as text", 4, "6x", 6),
          ("a fractional key", 9, 10.5, 11))],
    *[(f"{file}: {what}", file, edit, check, _RUNS[column].format(file=file) + fault)
      for file, (column, check, first) in KEY_TABLES.items()
      for what, edit, fault in (
          ("a repeated key", _repeat_key(column, 9),
           f"{column} {first + 8} is on line [10, 11]; no line holds {column} {first + 9}"),
          ("a gap", _drop_row(4), f"no line holds {column} {first + 4}"),
          ("no row", _no_row, "no line holds policy_year 1" if column == "policy_year"
           else "no line holds an age"))],
    *[(f"{file}: its first year missing", file, _drop_row(0), check,
       _RUNS[column].format(file=file) + "no line holds policy_year 1")
      for file, (column, check, _) in KEY_TABLES.items() if column == "policy_year"],
    # An age table is held from age 0, its age the index of its array, so a negative age,
    # which UL_US_S reads as the nearest row to any age below it, is refused (R7).
    *[(f"{file}: a negative first age", file, _write_at(column, 0, -1), check,
       f"{file}: age must be 0 or more; it is not on line [2]")
      for file, (column, check, _) in KEY_TABLES.items() if column == "age"],
    *[(f"coi_rates.csv: {what}", "coi_rates.csv", edit, "coi_rate_last_years", message)
      for what, edit, message in (
          ("its last policy year blank", _write_at("policy_year", -1, float("nan")),
           _WHOLE.format(file="coi_rates.csv", column="policy_year", lines="[88]")),
          ("an issue age written as text", _write_at("age_at_entry", 4, "35x"),
           _WHOLE.format(file="coi_rates.csv", column="age_at_entry", lines="[6]")),
          ("a fractional policy year", _write_at("policy_year", 9, 10.5),
           _WHOLE.format(file="coi_rates.csv", column="policy_year", lines="[11]")),
          ("its last sex blank", _write_at("sex", -1, float("nan")),
           "coi_rates.csv: sex must not be blank; it is on line [88]"),
          ("a repeated policy year", _repeat_key("policy_year", 9),
           _COI_RUN + "policy_year 9 is on line [10, 11]; at ('M', 'StdNT', 35), no line "
           "holds policy_year 10"),
          ("a gap", _drop_row(4), _COI_RUN + "no line holds policy_year 5"),
          ("its first year missing", _drop_row(0),
           _COI_RUN + "no line holds policy_year 1"))],
]

# Each rate a keyed reader reads, the class factor and the surrender-charge schedule's two
# columns, blank, written as text and, once, infinite.  UL_US_S reads a blank as a missing
# value, which shows in its flows or is lost in a min or a max, a blank lapse rate reading
# as the cap of 35% and a blank surrender charge as none, and this model's capped
# mortality, min(q, 1.0), keeps a blank base rate or class factor missing.  The Data cell
# that checks a keyed table's keys checks its rate column too, and class_count and
# surr_charge_count check the two tables read by point, whose classes and schedules may be
# neither blank nor repeated.  Each case is as in MALFORMED_KEYS.  The schedule table holds
# one row, UL9 on line 2, so its repeat is that row written twice.
_RATE = "{file}: {column} must be a number; it is not on line {lines}"
# Each table: (its rate column, the Data cell that checks it, the row edited, its line).
RATE_TABLES = {
    "prem_persistency.csv": ("prem_persistency", "prem_persistency_last_year", 15, 17),
    "lapse_table.csv": ("lapse_rate_ann", "lapse_last_year", 4, 6),
    "corridor_factors.csv": ("corridor_factor", "corridor_age_last", 22, 24),
    "mort_table.csv": ("mort_rate", "mort_age_last", 42, 44),
    "coi_rates.csv": ("coi_rate_guar", "coi_rate_last_years", 9, 11),
    "class_factor_table.csv": ("factor", "class_count", 2, 4),
}
MALFORMED_RATES = [
    *[(f"{file}: {what.format(column)}", file, _write_at(column, row, value), check,
       _RATE.format(file=file, column=column, lines=f"[{line}]"))
      for file, (column, check, row, line) in RATE_TABLES.items()
      for what, value in (("a blank {}", float("nan")), ("{} written as text", "x"))],
    ("mort_table.csv: an infinite mort_rate", "mort_table.csv",
     _write_at("mort_rate", 42, float("inf")), "mort_age_last",
     _RATE.format(file="mort_table.csv", column="mort_rate", lines="[44]")),
    ("class_factor_table.csv: a blank rate_class", "class_factor_table.csv",
     _write_at("rate_class", 2, float("nan")), "class_count",
     "class_factor_table.csv: rate_class must not be blank; it is on line [4]"),
    ("class_factor_table.csv: a repeated rate_class", "class_factor_table.csv",
     _repeat_key("rate_class", 3), "class_count",
     "class_factor_table.csv: each rate_class must have one row; rate_class StdPlusNT is "
     "on line [4, 5]"),
    *[(f"surr_charge_table.csv: {what}", "surr_charge_table.csv",
       _write_at(column, 0, value), "surr_charge_count",
       _RATE.format(file="surr_charge_table.csv", column=column, lines="[2]"))
      for what, column, value in (
          ("a blank sc_per_1000_init", "sc_per_1000_init", float("nan")),
          ("runoff_years written as text", "runoff_years", "x"))],
    ("surr_charge_table.csv: a blank surr_charge_id", "surr_charge_table.csv",
     _write_at("surr_charge_id", 0, float("nan")), "surr_charge_count",
     "surr_charge_table.csv: surr_charge_id must not be blank; it is on line [2]"),
    ("surr_charge_table.csv: a repeated surr_charge_id", "surr_charge_table.csv",
     _twice(0), "surr_charge_count",
     "surr_charge_table.csv: each surr_charge_id must have one row; surr_charge_id UL9 is "
     "on line [2, 3]"),
]


def _refused_exactly(call, message):
    """``call()`` raises ``ValueError`` with ``message`` as its whole message.

    :func:`_refused` finds the message in the error's text; this compares the line that
    names the error (:func:`_raised`), so that a key named wrongly, or one too many, fails.
    """
    with pytest.raises(Exception) as excinfo:
        call()
    assert _raised(excinfo.value) == f"ValueError: {message}"


def _table_refused(tmp_path, file, edit, check, message):
    """Data's ``check``, then a projection, refuse the copy whose ``file`` is ``edit``-ed.

    The Data cell is asked first, and with it the first-age cell an age table's reader
    also asks, and then ``net_cf(0)`` of the committed table's first point, which reads
    every one of these tables: the premium persistency scale, since the point pays a level
    premium; the COI scale through the month's deduction, which the surrender value reads;
    the mortality table and the class factor through the month's deaths; and the lapse
    table and the surrender-charge schedule through its lapses and their surrender value.
    """
    folder = temp_inputs(tmp_path, model_path(SEC), edits={file: edit})
    model = mx.read_model(folder, name=_name("tables"))
    try:
        _refused_exactly(model.Data.cells[check], message)
        if check.endswith("_age_last"):
            _refused_exactly(model.Data.cells[check.replace("_last", "_first")], message)
        first = _point(model, _label(_committed(), "twin", 1, 0))
        _refused_exactly(lambda: first.net_cf(0), message)
    finally:
        model.close()


@pytest.mark.parametrize("case, file, edit, check, message", MALFORMED_KEYS,
                         ids=[c[0] for c in MALFORMED_KEYS])
def test_an_assumption_table_with_a_malformed_key_is_refused(tmp_path, case, file, edit,
                                                             check, message):
    """The Data cell a keyed reader takes its extent from refuses the table, by name (T5).

    And so does the projection of the committed table's first point, in its first month
    (:func:`_table_refused`).  The reader asks for its extent before it reads a value, so a
    projection meets the check first, as a compiled model's must.  The age tables' first
    age is counted from their last, so it meets the same check.  The message is matched
    whole, so that each key it names, repeated or missing, is held, and nothing else.
    """
    _table_refused(tmp_path, file, edit, check, message)


@pytest.mark.parametrize("case, file, edit, check, message", MALFORMED_RATES,
                         ids=[c[0] for c in MALFORMED_RATES])
def test_an_assumption_table_with_a_rate_that_is_not_a_number_is_refused(
        tmp_path, case, file, edit, check, message):
    """A blank, text or infinite rate is refused, naming its file, column and line (T5).

    By the Data cell that checks the table's keys, or, for the class factors and the
    surrender-charge schedules, by ``class_count`` and ``surr_charge_count``, which their
    per-point readers ask before they read a value; and by the projection of the committed
    table's first point, in its first month (:func:`_table_refused`).  So is a class or a
    schedule that is blank or on two rows.  ``UL_US_S`` reads a blank rate as a missing
    value, and so does this model's capped mortality, ``min(q, 1.0)``, which written
    ``min(1.0, q)`` would read one as 1.0, every policy in force dying in that month
    without a word.
    """
    _table_refused(tmp_path, file, edit, check, message)
# A text column UL_US_S branches on, holding a value its formulas do not know: the decodes
# read it as no known value, and the cell that branches on it raises UL_US_S's own message,
# on the committed table's first point, LEVEL on Option A under the GPT, with one column
# changed.  UL_US_S compares the text exactly, so a known value in another case or with a
# space beside it is unknown too, and each of the six decodes meets one such spelling of
# its own value, which a decode that folded case or stripped spaces would read as known,
# projecting the point.  (case, column, value, message).
UNDECODABLE = [
    ("db_option C", "db_option", "C", "invalid db_option"),
    ("db_option a", "db_option", "a", "invalid db_option"),
    ("db_option b", "db_option", "b", "invalid db_option"),
    ("db_option ' A'", "db_option", " A", "invalid db_option"),
    ("db_option 'B '", "db_option", "B ", "invalid db_option"),
    ("qual_test CVAT", "qual_test", "CVAT", "invalid qual_test"),
    ("qual_test gpt", "qual_test", "gpt", "invalid qual_test"),
    ("qual_test ' GPT'", "qual_test", " GPT", "invalid qual_test"),
    ("premium_type FLEX", "premium_type", "FLEX", "invalid premium type"),
    ("premium_type level", "premium_type", "level", "invalid premium type"),
    ("premium_type single", "premium_type", "single", "invalid premium type"),
    ("premium_type target", "premium_type", "target", "invalid premium type"),
    ("premium_type ' LEVEL'", "premium_type", " LEVEL", "invalid premium type"),
    ("premium_type 'SINGLE '", "premium_type", "SINGLE ", "invalid premium type"),
    ("premium_type 'TARGET '", "premium_type", "TARGET ", "invalid premium type"),
]


@pytest.mark.parametrize("case, column, value, message", UNDECODABLE,
                         ids=[c[0] for c in UNDECODABLE])
def test_a_value_no_decode_knows_is_refused_as_in_ul_us_s(tmp_path, case, column, value,
                                                         message):
    """An unknown option, test or pattern raises ``UL_US_S``'s message, not a branch.

    The six decodes each compare the text with one value, so a value none of them names
    reads as no known one, and the cell that branches on them must raise as ``UL_US_S``'s
    does, rather than take its last branch.  The table reads, because the text columns
    are the product's to judge, and the point's first projection raises.
    """
    point = _label(_committed(), "twin", 1, 0)
    model = _read_edited(tmp_path, _set(column, [point], value))
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_point(model, point).result_cf, message)
    finally:
        model.close()


# What Data cannot number or join, refused when the vector is first read, naming every
# point at fault (the Data docstring): a label that is not a whole number, or one of 2**53
# or more in size, which numpy would read as the least int64 once past int64; a rate_class
# the class factors lack; and, on a point that has_surr_charge, a surr_charge_id the
# schedules lack, a run-off of 0 years of either sign, which UL_US_S's surr_charge_rate
# divides by in every month of such a point's cover, or one of 2**53 years or more, the
# bound of every number read as an int, past which lapse_shock_year's compiled int()
# would in time raise OverflowError.  The surrender-charge cases leave the
# charge on points 4 and 6 alone, so that the message names those two and not the table.
# Each case is (case, the table's edit, the schedules' run-off or None, the Data cell
# asked, the message, the label whose projection meets it): a label's refusal is met by
# that point's own point_id(), which every refusal names it by; the class factors' by
# point 1's result_cf(), since every point reads its factor in its first month; and the
# schedules' by point 4's, which has a charge, since a point without one never reads
# them.
_CHARGED = (4, 6)
_NO_CLASS = "class_factor_table.csv has no factor for the rate_class of point_id [3, 6]"
_NO_SCHEDULE = ("surr_charge_table.csv has no schedule for the surr_charge_id of point_id "
                "[6], each of which has_surr_charge")
_RUNOFF_ZERO = ("surr_charge_table.csv: runoff_years must not be 0 on the schedule of "
                "point_id [4, 6], each of which has_surr_charge, since the charge runs off "
                "over it")
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


UNJOINED = [
    ("a label that is not whole", _relabelled(4, 4.5), None, "point_id",
     f"{TABLE}: point_id must be a whole number; [4.5] is not", 4.5),
    ("a label written as text", _relabelled(4, "4x"), None, "point_id",
     f"{TABLE}: point_id must be a whole number; ['4x'] is not", "4x"),
    ("a label of 2**53", _relabelled(4, 2 ** 53), None, "point_id",
     f"{TABLE}: point_id must be below 2**53 in size; [{2 ** 53}] is not", 2 ** 53),
    ("a class the table lacks, at two points", _set("rate_class", [3, 6], "SuperPNT"), None,
     "class_factor", _NO_CLASS, 1),
    ("a schedule the table lacks, on a point with a charge",
     _charged_only(_CHARGED, _set("surr_charge_id", [6, 7], "UL5")), None,
     "surr_charge_rate_max", _NO_SCHEDULE, 4),
    ("a schedule the table lacks, by the run-off's vector",
     _charged_only(_CHARGED, _set("surr_charge_id", [6, 7], "UL5")), None,
     "surr_charge_runoff_years", _NO_SCHEDULE, 4),
    ("a run-off of 0", _charged_only(_CHARGED), 0, "surr_charge_runoff_years",
     _RUNOFF_ZERO, 4),
    ("a run-off of -0.0", _charged_only(_CHARGED), -0.0, "surr_charge_rate_max",
     _RUNOFF_ZERO, 4),
    ("a run-off of 2**53 years", _charged_only(_CHARGED), 2.0 ** 53,
     "surr_charge_runoff_years", _RUNOFF_HUGE, 4),
    ("a run-off past int64", _charged_only(_CHARGED), -1e30, "surr_charge_rate_max",
     _RUNOFF_HUGE, 4),
]


def _runoff(years):
    """The edits that give the surrender-charge schedules a run-off of ``years``."""
    return None if years is None else {
        "surr_charge_table.csv": lambda table: table.assign(runoff_years=years)}


@pytest.mark.parametrize("case, edit, runoff, cell, message, label", UNJOINED,
                         ids=[c[0] for c in UNJOINED])
def test_what_data_cannot_number_or_join_is_refused_naming_it(tmp_path, case, edit, runoff,
                                                             cell, message, label):
    """``Data`` refuses what it cannot number or join, naming every point at fault.

    ``UL_US_S`` reads a point's class factor in every month on the books, and the
    schedule of a point with a surrender charge in every month of its cover, so it fails
    every projection of a point whose class or charged schedule the tables lack, or whose
    run-off is 0, and this model refuses the table at the first read instead
    (:data:`UNJOINED`), in the
    vector's own cell and in a projection, with the message matched whole.  A label is
    read by no projection but in a refusal, which names the point by ``point_id()``, so
    that cell refuses it.  The message names every point at fault and no other.
    """
    model = mx.read_model(_sec_inputs(tmp_path, edit(_committed()), _runoff(runoff)),
                          name=_name("unjoined"))
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused_exactly(model.Data.cells[cell], message)
        call = "point_id" if cell == "point_id" else "result_cf"
        _refused_exactly(_point(model, label).cells[call], message)
    finally:
        model.close()


def test_a_schedule_no_charged_point_reads_is_accepted(tmp_path):
    """A schedule no point with a charge reads may be missing, or run off over 0 years.

    ``UL_US_S`` reads a point's schedule only if it ``has_surr_charge``, so a point without
    one projects whatever its ``surr_charge_id`` names, as it does in ``UL_US_S``.  With
    the charge off on every point, the schedule run off over 0 years, and the twin of S's
    point 2 naming a schedule the table lacks, the table reads; both join vectors read the
    schedule, 9.0 and 0.0, at every point but that one, which is NaN with a
    ``has_surr_charge_schedule`` of 0; and every point projects exactly what it projects
    on the committed schedule with the charge off.  The joins refuse a charged point alone
    (:data:`UNJOINED`).
    """
    committed = _committed()
    lost = _label(committed, "twin", 2, 0)
    uncharged = _charged_only([])(committed)
    base = mx.read_model(_sec_inputs(tmp_path / "base", uncharged),
                         name=_name("uncharged"))
    model = mx.read_model(_sec_inputs(tmp_path / "zero",
                                      _set("surr_charge_id", [lost], "UL5")(uncharged),
                                      _runoff(0)), name=_name("runoff_0"))
    try:
        assert len(model.Data.model_point_table()) == len(committed)
        lost_at = list(committed.index).index(lost)
        for cell, value in (("surr_charge_rate_max", 9.0),
                            ("surr_charge_runoff_years", 0.0)):
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
# value f77b290's model, UL_US_SEC at stage E, read there, its .loc reading the schedule of
# a point with a charge or without, and raising KeyError on an id the table lacks: SC7, a
# second schedule the copy adds; Z0, a third, run off over 0 years, which only a point
# with a charge is refused; UL9 as shipped; UL5, which no table has; and a blank id.
UNCHARGED = ((3, "SC7", (9.5, 7.0)), (5, "Z0", (3.0, 0.0)), (6, "UL9", (9.0, 9.0)),
             (7, "UL5", None), (8, None, None))
_NO_ID = ("KeyError: 'point_id {}: surr_charge_table.csv has no schedule for its "
          "surr_charge_id'")


def _surr_charges_with_sc7(table):
    """The shipped schedules with SC7, $9.50 per $1,000 over 7 years, and Z0, $3.00 per
    $1,000 over 0 years."""
    added = pd.DataFrame([
        {"surr_charge_id": "SC7", "sc_per_1000_init": 9.5, "runoff_years": 7,
         "provenance": "test copy"},
        {"surr_charge_id": "Z0", "sc_per_1000_init": 3.0, "runoff_years": 0,
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
    without a charge, since ``surr_charge_rate`` returns 0.0 and ``lapse_shock_year`` 0
    first, but each is a cell, and Phase 2 moves no number (D2): so each reads the point's
    schedule wherever the table holds its id, a run-off of 0 included, and raises
    ``KeyError`` where it does not, naming the point, as the ``.loc`` of the model at stage
    ``E`` did (:data:`UNCHARGED`, pinned to f77b290's values).  ``Data`` joins the schedule
    wherever it can, NaN and a ``has_surr_charge_schedule`` of 0 where it cannot, and
    refuses no point without a charge, which projects as ``UL_US_S`` projects it, its
    schedule unread.
    """
    folder = _sec_inputs(tmp_path, _uncharged(),
                         edits={"surr_charge_table.csv": _surr_charges_with_sc7})
    model = mx.read_model(folder, name=_name("uncharged"))
    try:
        for point, label, want in UNCHARGED:
            p = _point(model, point)
            have = p.surr_charge_id()
            assert not p.has_surr_charge() and (have == label if label else have != have)
            assert len(p.result_cf()) == p.proj_len() and p.surr_charge_rate(0) == 0.0
            assert p.lapse_shock_year() == 0
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


# A point the contract does not issue, refused by proj_len() in its three rules' order, as
# (case, the table's edit, the References set, the label, the message, and the frame the
# point projects once issue_age_min is lowered to its issue age, or None).  The first rule,
# issued above omega_age, is asked before the cover's, so a point to be issued there, or in
# force there, is refused as never in cover; the cover's before issue_age_min's, so a point
# issued at 17 and past its cover is refused as past it.  An age of 17.9 is read as
# UL_US_S's int reads it, 17.  At issue age 17 the copy's COI table gains rows of its own
# (_coi_at), so the point projects once the bound is lowered.
NOT_ISSUED = [
    ("an issue age of 17", _set("age_at_entry", [1], 17), {}, 1,
     "point_id 1: issue age 17 is below issue_age_min, 18", 1248),
    ("an issue age of 17.9, read as 17", _set("age_at_entry", [2], 17.9), {}, 2,
     "point_id 2: issue age 17 is below issue_age_min, 18", 1248),
    ("an issue age below a bound raised to 36", None, {"issue_age_min": 36}, 1,
     "point_id 1: issue age 35 is below issue_age_min, 36", 1032),
    ("to be issued above omega_age", _set("age_at_entry", [9], 121), {}, 9,
     "point_id 9: age_at_entry 121 is above omega_age, 120: a policy issued there would "
     "never be in cover", None),
    ("in force above omega_age: the first rule before the cover's",
     _set("age_at_entry", [3], 121), {}, 3,
     "point_id 3: age_at_entry 121 is above omega_age, 120: a policy issued there would "
     "never be in cover", None),
    ("issued at 17 and past its cover: the cover's rule before the bound's",
     _moved(3, 1248, age_at_entry=17), {}, 3,
     "point_id 3: duration_mth 1248 is at or past the end of the projection, policy month "
     "1248, attained age 121", None),
]


def _coi_at(age):
    """An edit of the COI scale that adds ``(M, StdNT, age)``, geometric in the year."""
    def edit(rates):
        years = list(range(1, 122 - age))
        added = pd.DataFrame({
            "sex": "M", "rate_class": "StdNT", "age_at_entry": age, "policy_year": years,
            "coi_rate_guar": [round(0.07 * 1.08 ** (y - 1), 6) for y in years],
            "provenance": "test copy"})
        return pd.concat([rates, added], ignore_index=True)
    return edit


@pytest.mark.parametrize("case, edit, refs, label, message, frame", NOT_ISSUED,
                         ids=[c[0] for c in NOT_ISSUED])
def test_a_point_the_contract_does_not_issue_is_refused_by_proj_len(tmp_path, case, edit,
                                                                    refs, label, message,
                                                                    frame):
    """``proj_len()`` refuses a point the contract does not issue, naming it (§6.1).

    ``UL_US_S`` projects a point issued at any age its tables serve, and so would modelx
    here, but the compiled caches are sized from the contract, cover from
    ``issue_age_min``, 18, to attained age 121 and the shipped horizon (``spec_sec.py``),
    and a younger point runs past them.  So the frame refuses such a point, naming it,
    and one issued above ``omega_age``, which ``UL_US_S`` projects as months in which
    nothing happens, each by the rule asked first (:data:`NOT_ISSUED`).  The table reads,
    since these are rules of the product, and every report is refused with the frame.  The
    point issued at 17 projects once the bound is lowered to 17, a frame of 1,248 months,
    and the one refused at a bound of 36 projects at the shipped 18: the Reference is what
    refuses each, and a bound off by one, or a refusal lost or asked in another order,
    lets a point through or names the wrong rule.
    """
    table = _committed() if edit is None else edit(_committed())
    model = mx.read_model(_sec_inputs(tmp_path, table, {"coi_rates.csv": _coi_at(17)}),
                          name=_name("not_issued"))
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        for report in REPORTS:
            _refused_exactly(_point(model, label).cells[report], message)
    finally:
        model.close()
    if frame is None:
        return
    model = mx.read_model(_sec_inputs(tmp_path / "issued", table,
                                      {"coi_rates.csv": _coi_at(17)}),
                          name=_name("issued"))
    try:
        model.Projection.issue_age_min = min(17, model.Projection.issue_age_min)
        p = _point(model, label)
        assert p.proj_len() == len(p.result_cf()) == frame
        assert p.check_av_roll_fwd() and p.check_margin()
    finally:
        model.close()


# The reads beyond a table on the committed inputs, as (cell, arguments, the message after
# the point's label): a policy year below 1, where UL_US_S's .loc and slice raised KeyError,
# which each reader refuses before it reads its padded array.
BEYOND = [
    ("prem_persistency_py", (0,), "prem_persistency.csv has no factor for policy year 0"),
    ("lapse_rate_base_py", (0,), "lapse_table.csv has no rate for policy year 0"),
    ("coi_rate_guar_py", (0,), "coi_rates.csv has no rate for policy year 0"),
    ("prem_persistency_py", (-1,), "prem_persistency.csv has no factor for policy year -1"),
    ("lapse_rate_base_py", (-1,), "lapse_table.csv has no rate for policy year -1"),
    ("coi_rate_guar_py", (-1,), "coi_rates.csv has no rate for policy year -1"),
]
NO_SCALE = "coi_rates.csv has no scale for the point's sex, rate_class and age_at_entry"


def test_a_read_beyond_a_table_is_refused_naming_its_point(sec_model, tmp_path):
    """The one reader of each padded table refuses a key before the table, by name.

    ``prem_persistency_py``, ``lapse_rate_base_py`` and ``coi_rate_guar_py`` refuse a
    policy year below 1 (:data:`BEYOND`), naming the point by its label, on the
    extract labelled otherwise than by position, where a label read as ``idx + 1`` would
    name another; a year past the table reads its last row, as ``UL_US_S`` reads it.  The
    two age tables read an age outside them at the nearest row, as ``UL_US_S``'s clamp
    does, so they have no key to refuse.  A point issued at 36, for which the COI scale has
    no rows, has schedule 0 and is refused by ``coi_rate_last_year()`` once a rate is read,
    by its projection, and projects once ``charges_cease_age`` is 30, where no rate is
    read, as ``UL_US_S`` projects it.

    The padding is NaN, as the ``Data`` docstrings say, so that a read past a check, were
    one lost, would make every number after it NaN rather than another key's value: row 0
    of the COI scale, its column of policy year 0 and every year past its last; year 0 of
    the two policy-year tables; the ages below each age table's first; and nothing inside.
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
        assert p.prem_persistency_py(500) == p.prem_persistency_py(16) == 0.70
        assert p.lapse_rate_base_py(500) == p.lapse_rate_base_py(11)
        assert p.coi_rate_guar_py(500) == p.coi_rate_guar_py(87)
        data = model.Data
        assert [p.corridor_factor_at(a) for a in (0, 17, 18)] == [2.5] * 3
        assert p.corridor_factor_at(500) == p.corridor_factor_at(data.corridor_age_last())
        assert p.mort_rate_base_at(0) == p.mort_rate_base_at(data.mort_age_first())
        coi = data.coi_rate_array()
        last = data.coi_rate_last_years()
        assert np.isnan(coi[0]).all() and np.isnan(coi[:, 0]).all()
        for s in range(1, coi.shape[0]):
            years = last[data.coi_schedule() == s]
            assert len(set(years)) == 1, s
            assert not np.isnan(coi[s, 1:years[0] + 1]).any(), s
            assert np.isnan(coi[s, years[0] + 1:]).all(), s
        for array, first in ((data.prem_persistency_array(), 1),
                             (data.lapse_rate_array(), 1),
                             (data.corridor_factor_array(), data.corridor_age_first()),
                             (data.mort_table_array(), data.mort_age_first())):
            assert np.isnan(array[:first]).all() and not np.isnan(array[first:]).any()
        assert first == 18
    finally:
        model.close()
    unscaled = _set("age_at_entry", [label], 36)(extract)
    for cease in (None, 30):
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
            assert len(p.result_cf()) == p.proj_len() == 1045
            assert not p.cells["coi_rate_guar_py"].keys()
        finally:
            model.close()


def test_a_fractional_issue_age_truncates_as_ul_us_s_truncates_it(sec_model, tmp_path):
    """An issue age of 35.5 or 35.9 is 35, and -0.5 is 0, as ``UL_US_S``'s ``int`` reads.

    ``UL_US_S`` and Phase 1 take ``int`` of the issue age, which truncates a fraction
    toward zero, and Phase 2 changes no number (D2), so ``Data.age_at_entry`` truncates
    too, and refuses only a non-finite age or one of ``2**53`` or more
    (:data:`MALFORMED`).  The twins of S's points 1 and 2, issued at 35.5 and 35.9, read 35
    and project every report exactly as the committed twins do; and S's in-force point
    issued at -0.5 reads 0, which ``proj_len()`` then refuses as below ``issue_age_min``,
    where a floor would have read -1.
    """
    committed = _committed()
    one, two = (_label(committed, "twin", p, 0) for p in NEW_BUSINESS)
    young = _label(committed, "twin", IN_FORCE, 0)
    table = _set("age_at_entry", [young], -0.5)(
        _set("age_at_entry", [two], 35.9)(_set("age_at_entry", [one], 35.5)(committed)))
    model = mx.read_model(_sec_inputs(tmp_path, table), name=_name("fraction"))
    try:
        assert list(model.Data.age_at_entry()[:3]) == [35, 35, 0]
        for label in (one, two):
            mine, base = _point(model, label), _point(sec_model, label)
            assert mine.age_at_entry() == 35 and type(mine.age_at_entry()) is int
            for report in REPORTS:
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=0, atol=0) == [], (label, report)
        _refused_exactly(_point(model, young).proj_len,
                         f"point_id {young}: issue age 0 is below issue_age_min, 18")
    finally:
        model.close()


def test_the_claims_total_is_s_claims_bit_for_bit(sec_model, s_model):
    """``claims(t)`` is ``UL_US_S``'s ``claims(t)``, bit for bit (R12, M15).

    S's ``claims(t, kind=None)`` is the two kinds and their total in one cell, the total a
    ``sum`` of a generator.  Here the kinds are ``claims_death`` and ``claims_lapse`` and
    ``claims(t)`` their total written out from ``0.0``, and T1 reaches S's total through
    the spec's ``twin_arg_map``, to T1's tolerance.  The total is held here to S's exactly:
    on the twins of S's points 1 and 2, issued at the valuation date, in every month of the
    frame, equal to S's total, type and the sign of a zero included, and each kind equal to
    S's ``claims(t, kind)``.  Python's ``sum`` of two floats is their one rounded sum, so
    the total written out is S's float in every month.
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
                if mine.cells[cell](t) != theirs.claims(t, kind):
                    found.append(f"point {point}: {cell}({t}) is not S's "
                                 f"claims({t}, {kind!r})")
    assert not found, found[:20]


# The month at which the sign test sets the two kinds on the worked example's twin: in
# cover, where the death claim is nonzero.
ZERO_MONTH = 5


def test_two_negative_zero_kinds_total_a_positive_zero_as_s_sum_does():
    """``claims(t)`` is ``0.0``, not ``-0.0``, where both kinds are ``-0.0``, as S's.

    S's total is ``sum`` of the two kinds, which starts at the int 0, and ``0 + -0.0`` is
    ``0.0``, so S's total of two negative zeros is a positive zero.  ``claims(t)`` starts
    its sum at ``0.0`` for that reason, and the claims test cannot hold it: no committed
    month has two negative zero kinds.  So here, on a read of each model of their own, the
    two kinds of the worked example's twin at :data:`ZERO_MONTH` are set to ``-0.0`` as
    modelx input values, and so are S's ``claims(t, kind)`` of its point 1 in the same
    month, and the totals must be S's: ``0.0``, a float, with a positive sign.  A total
    written without its ``0.0`` start gives ``-0.0`` and fails.
    """
    s = mx.read_model(model_path(TWIN), name=_name("s_zeros"))
    sec = mx.read_model(model_path(SEC), name=_name("zeros"))
    try:
        theirs, mine = _point(s, 1), _row(sec, "twin", 1, 0)
        assert mine.claims_death(ZERO_MONTH) == theirs.claims(ZERO_MONTH, "DEATH") != 0.0
        assert mine.claims_lapse(ZERO_MONTH) == theirs.claims(ZERO_MONTH, "LAPSE")
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


def _coi_unsorted(rates):
    """The splice's COI copy with a schedule no point reads, written in reverse key order.

    :func:`_coi_rates_with_variants`, sorted by its keys, and ``(M, PPlusNT, 30)``, which
    sorts between schedules the points read, then every line reversed, so that the file's
    order of the schedules is the reverse of their keys' and a schedule numbered in file
    order is another schedule's number.
    """
    rates = _coi_rates_with_variants(rates)
    anchor = rates[(rates["sex"] == "M") & (rates["rate_class"] == "StdNT")
                   & (rates["age_at_entry"] == 35)]
    unread = anchor.assign(rate_class="PPlusNT", age_at_entry=30,
                           coi_rate_guar=(anchor["coi_rate_guar"] * 0.6).round(6))
    rates = pd.concat([rates, unread]).sort_values(COI_KEYS, ignore_index=True)
    return rates.iloc[::-1].reset_index(drop=True)


# The points of the numbering test: the committed twin of S's point 1 under each key of
# the copy it reads, as (sex, rate_class, age_at_entry), and the schedule number each must
# have, its keys' place in their order.
NUMBERED = {("F", "PNT", 35): 1, ("M", "PNT", 35): 2, ("M", "PTob", 35): 5,
            ("M", "StdNT", 18): 6, ("M", "StdNT", 35): 7, ("M", "StdTob", 35): 9}


def test_the_coi_schedules_are_numbered_by_key_whatever_the_file_order(tmp_path):
    """Every COI schedule has one number, in its keys' order, in each cell that reads one.

    ``Data`` numbers the schedules of *coi_rates.csv* three times, in
    ``coi_schedule``, ``coi_rate_last_years`` and ``coi_rate_array``, and a point reads
    its rates at its number's row.  Every other copy of the table is sorted by its keys,
    so file order and key order agree there, and a cell that numbered in file order would
    pass every comparison.  Here the copy is written in reverse (:func:`_coi_unsorted`),
    with a schedule no point reads between two that points read, and six points read six
    of its nine schedules (:data:`NUMBERED`): each point's schedule is its keys' place, the
    same as on the copy sorted, and every COI rate a point reads in every month of its
    frame is the file's rate for its own keys and policy year, read from the file by key,
    so that a cell numbering otherwise reads another schedule's rate.  Each point then
    projects ``result_cf`` and ``result_av`` exactly as on the sorted copy.
    """
    committed = _committed()
    one = committed.loc[[_label(committed, "twin", 1, 0)]]
    table = pd.concat([one.assign(sex=sex, rate_class=rate_class, age_at_entry=age)
                       for sex, rate_class, age in NUMBERED])
    table.index = pd.Index(range(1, len(table) + 1), name="point_id")
    edits = dict(SPLICED_EDITS)
    models = {}
    try:
        for order, edit in (("sorted", lambda r: _coi_unsorted(r).iloc[::-1]),
                            ("unsorted", _coi_unsorted)):
            edits["coi_rates.csv"] = edit
            folder = _sec_inputs(tmp_path / order, table, edits)
            models[order] = mx.read_model(folder, name=_name(f"coi_{order}"))
        written = pd.read_csv(folder.parent / "coi_rates.csv")
        keys = list(zip(written["sex"], written["rate_class"], written["age_at_entry"]))
        assert keys != sorted(keys) and len(set(keys)) == 9
        rate = {(*key, year): value for key, year, value in zip(
            keys, written["policy_year"], written["coi_rate_guar"])}
        for order, model in models.items():
            data = model.Data
            assert data.coi_schedules() == 9
            assert list(data.coi_schedule()) == list(NUMBERED.values()), order
            for key, p in zip(NUMBERED, (projection(model, k) for k in point_keys(model))):
                assert p.coi_schedule() == NUMBERED[key], (order, key)
                last = max(y for k, y in ((r[:3], r[3]) for r in rate) if k == key)
                assert p.coi_rate_last_year() == last, (order, key)
                for t in range(p.proj_len()):
                    if p.is_active(t):
                        want = rate[(*key, min(p.policy_year(t), last))]
                        assert p.coi_rate_guar(t) == want, (order, key, t)
        for key, label in zip(NUMBERED, table.index):
            for report in ("result_cf", "result_av"):
                assert frame_mismatches(
                    _point(models["sorted"], label).cells[report](),
                    _point(models["unsorted"], label).cells[report](), rtol=0,
                    atol=0) == [], (key, report)
    finally:
        for model in models.values():
            model.close()


def test_a_load_of_1_projects_and_its_cure_payment_divides_by_zero_as_in_ul_us_s(
        tmp_path):
    """At each end of each value's range the point is read and projects, as in ``UL_US_S``.

    ``Data`` holds each value of the contract to its range (:data:`MALFORMED`), and reads
    each bound itself: a load of 1 and of 0, and a premium, a withdrawal and tax limits
    of 0.  A load of 1 is VUL's range, and ``UL_US_S`` projects it in full, since no report
    reads the cure payment, which divides by ``1 - load_prem_rate``: its
    ``cure_premium_pp`` raises ``ZeroDivisionError: float division by zero``, Python's own
    text.  So here the worked example's twin at a load of 1 projects ``result_cf`` exactly
    as S's point 1 does at a load of 1, both checks hold, and ``cure_premium_pp`` raises
    S's error with S's text; compiled, a C division would raise another text, so the cell
    raises it first, and the compiled refusals test holds that.  The other bounds sit on
    the other twins, each read and projected.
    """
    committed = _committed()
    one, two = (_label(committed, "twin", p, 0) for p in NEW_BUSINESS)
    table = _set("load_prem_rate", [one], 1.0)(committed)
    table = _set("load_prem_rate", [two], 0.0)(table)
    for column in ("premium_pp_ann", "gsp", "glp", "seven_pay_prem"):
        table = _set(column, [two], 0.0)(table)
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN),
                                  model_points=_set("load_prem_rate", [1], 1.0)(s_table)),
                      name=_name("s_load"))
    sec = mx.read_model(_sec_inputs(tmp_path / "sec", table), name=_name("load"))
    try:
        theirs, mine = _point(s, 1), _point(sec, one)
        for p in (theirs, mine):
            with pytest.raises(Exception) as excinfo:
                p.cure_premium_pp(0)
            assert _raised(excinfo.value) == "ZeroDivisionError: float division by zero"
        assert frame_mismatches(theirs.result_cf(), mine.result_cf(), rtol=0,
                                atol=0) == []
        assert mine.check_av_roll_fwd() and mine.check_margin()
        zero = _point(sec, two)
        assert (zero.load_prem_rate(), zero.premium_pp_ann(), zero.gsp()) == (0.0,) * 3
        assert len(zero.result_cf()) == zero.proj_len() == 1032
        assert zero.check_av_roll_fwd() and zero.check_margin()
    finally:
        sec.close()
        s.close()


# The spellings of the surrender-charge flag pandas reads as True or False, on the four
# twins and restatements of S's points 1 and 2 they are written on, as (label's row, the
# spelling, the flag it is).
SPELLED = ((("twin", 1, 0), "TRUE", True), (("twin", 2, 0), "true", True),
           (("derived", 1, 12), "FALSE", False), (("derived", 1, 113), "false", False))


def test_the_surrender_charge_flag_reads_true_or_false_in_any_case(tmp_path):
    """``TRUE``, ``true``, ``FALSE`` and ``false`` are the flags ``True`` and ``False``.

    pandas reads each of those words as a bool, so ``UL_US_S``'s ``bool()`` reads it as
    the flag it spells, and ``Data`` reads it the same way, refusing only what pandas
    reads otherwise (:data:`MALFORMED`: ``yes``, a blank, 1, 0, 1.0 and 0.0).  Written so
    on four points (:data:`SPELLED`), each point's flag is what the word spells and it
    projects ``result_cf`` and ``result_pols`` exactly as it does with the flag written
    ``True`` or ``False``.
    """
    committed = _committed()
    labels = [_label(committed, *row) for row, _, _ in SPELLED]
    plain, spelled = committed.copy(), committed.copy()
    for label, (_, word, flag) in zip(labels, SPELLED):
        plain = _set("has_surr_charge", [label], flag)(plain)
        spelled = _set("has_surr_charge", [label], word)(spelled)
    models = [mx.read_model(_sec_inputs(tmp_path / name, table), name=_name(name))
              for name, table in (("plain", plain), ("spelled", spelled))]
    try:
        written = (tmp_path / "spelled" / TABLE).read_text(encoding="utf-8")
        assert all(f",{word}," in written for _, word, _ in SPELLED)
        for label, (_, word, flag) in zip(labels, SPELLED):
            base, mine = (_point(model, label) for model in models)
            assert mine.has_surr_charge() is flag, (word, mine.has_surr_charge())
            for report in ("result_cf", "result_pols"):
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=0, atol=0) == [], (word, report)
    finally:
        for model in models:
            model.close()


# The References under which a lapse rate passes 1 in the shock year: the cap raised to 2
# and the shock multiplied 60 times, 0.04 x 60 capped at 2.
PAST_1 = {"lapse_rate_cap": 2.0, "lapse_shock_mult": 60.0}


def test_a_count_that_is_not_real_makes_each_check_raise(tmp_path):
    """A decrement rate past 1 makes the count complex, and each check raises on it.

    ``UL_US_S``'s checks are ``math.isclose`` loops, which raise ``TypeError`` on a
    complex number, and a lapse rate past 1, which the References allow once the cap is
    raised past 1 (:data:`PAST_1`), makes the monthly rate ``1 - (1 - q)^(1/12)`` complex
    in modelx, and every count after it.  Each residual is ``float(...)`` of its ratio, as
    the life chassis returns them (USLIB-SEC-PLAN.md §7.9, *Residuals as floats*), so it
    raises rather than pass its check on its real magnitude: in the first month of the
    shock year, policy year 10 on the worked example's twin, each residual and each check
    raises ``TypeError``.
    """
    model = mx.read_model(model_path(SEC), name=_name("complex"))
    try:
        for ref, value in PAST_1.items():
            setattr(model.Projection, ref, value)
        p = _row(model, "twin", 1, 0)
        month = 12 * (p.lapse_shock_year() - 1)
        assert p.lapse_rate(month) == 2.0 and p.lapse_rate(month - 1) < 1.0
        assert isinstance(p.pols_lapse(month), complex)
        for call in (lambda: p.check_av_roll_fwd_resid(month),
                     lambda: p.check_margin_resid(month), p.check_av_roll_fwd,
                     p.check_margin):
            with pytest.raises(Exception) as excinfo:
                call()
            assert _raised(excinfo.value).startswith("TypeError: float() argument"), (
                _raised(excinfo.value))
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
    future = _label(_committed(), "future", 1, -25)
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
                _refused(model.Data.model_point_table, refusal)
            if horizon == 25:
                p = _point(model, future)
                assert len(p.result_cf()) == p.proj_len() == 1057
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


# The refusals of proj_len(), as (case, the row moved, as (row_kind, S point, source_mth),
# and the policy month it is moved to): to the month the projection ends, the first at
# attained age 121, and a year past it.  Both are anniversaries, so that Data, which holds
# the year's usage to 0 there, has nothing to refuse: every row moved has none.
PAST_COVER = [
    ("at the end", ("derived", 1, 113), 1032),
    ("past the end", ("derived", 1, 12), 1044),
]


@pytest.mark.parametrize("case, row, month", PAST_COVER, ids=[c[0] for c in PAST_COVER])
def test_a_point_past_its_cover_is_refused_by_proj_len(tmp_path, case, row, month):
    """A point at or past the end of the projection has no frame, and is refused by name.

    The row is moved on to a policy month at or past ``omega_mth()``, the month the
    projection ends at attained age 121.  That is a rule of the product, not of the table:
    it needs ``omega_age``, a Projection Reference, so the table reads, and the point is
    refused where its frame is defined, on its first projection, rather than projecting
    nothing.  A loop over the block would meet the point only when it reached it, after
    projecting the points before it, so ``run_sec.py --block``, run beside the table, asks
    every point for its frame first: it fails naming the point, and prints nothing before.
    """
    moved = _label(_committed(), *row)
    folder = _sec_inputs(tmp_path, _set("duration_mth", [moved], month)(_committed()))
    message = (f"point_id {moved}: duration_mth {month} is at or past the end of the "
               f"projection, policy month 1032, attained age 121")
    model = mx.read_model(folder, name=_name("past"))
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_point(model, moved).result_cf, message)
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert message in done.stderr.decode(errors="replace")


# The key columns of every table read at a policy year or an attained age, which the edges
# test writes as floats, 16.0 for 16, as a spreadsheet can save them; and the extents Data
# reads from them.
FLOAT_KEYS = {"prem_persistency.csv": ("policy_year",), "lapse_table.csv": ("policy_year",),
              "corridor_factors.csv": ("age",), "mort_table.csv": ("age",),
              "coi_rates.csv": ("age_at_entry", "policy_year")}
EXTENTS = ("prem_persistency_last_year", "lapse_last_year", "corridor_age_first",
           "corridor_age_last", "mort_age_first", "mort_age_last")


def _as_floats(columns):
    """An edit that writes the table's ``columns`` as floats."""
    def edit(table):
        return table.assign(**{column: table[column].astype(float) for column in columns})
    return edit


def test_the_edges_of_the_in_force_interface_are_accepted(sec_model, tmp_path):
    """A zero count, whole numbers in any type, the horizon and the years' edges are read.

    A count of 0 is a point that projects zeros.  ``126.0`` is a whole number of months,
    read back as the int the policy clock counts in, and ``1.0`` an int code, read back by
    ``is_mec_init()`` as a bool; and the face, the year's usage and the premiums to date
    written without a decimal point, as an extract that holds whole dollars writes them,
    read as the floats every per-policy value is.  The same copy writes the key columns of
    the five tables read at a policy year or an attained age as floats
    (:data:`FLOAT_KEYS`): ``Data`` reads each key by value, so every extent is the
    committed table's, an int, and the twins of S's new business, which read every one of
    those tables, project exactly what the committed tables project.  A policy issued 120
    months after the valuation date, the shipped ``future_horizon_mth``, is the last one the
    table admits, with a frame of 1,152 months, 1,032 of cover after 120 before issue.

    Either side of each check that turns on the policy year, where an off-by-one would
    refuse the row: S point 1 on its first anniversary, month 12, with no usage, and S's
    in-force point moved on to month 13 with $25 of the year's allowance used; S point 1
    moved to month 84 with $50,000 of premiums and the latch on, and S's in-force point
    moved to month 85 with the same premiums and the latch off, since the month before it
    is in policy year 8, where the 7-pay test no longer runs, so that it is no MEC there,
    over the limit as it is.  And two values ``UL_US_S`` can produce or the model can
    project as given: a face in force below the face at issue on the point valued as its
    shortfall begins, projected from the value given, its Option B death benefit that face
    plus the floored account value; and premiums less withdrawals below 0, a tax measure
    rather than a balance.
    """
    committed = _committed()
    last = _label(committed, "derived", 1, 1008)
    future = _label(committed, "future", 1, -25)
    anniv = _label(committed, "derived", 1, 12)
    mid = _label(committed, "derived", IN_FORCE, 6)
    latched = _label(committed, "derived", 1, 113)
    unlatched = _label(committed, "twin", IN_FORCE, 0)
    shortfall = _label(committed, "derived", 2, 676)
    whole = ("sum_assured_init", "wd_used_year_init", "cum_prem_init")

    def edit(table):
        table = _set("policy_count", [last], 0.0)(table)
        table = _moved(mid, 13, wd_used_year_init=25.0)(table)
        table = _moved(latched, 84, cum_prem_init=50000.0, is_mec_init=1)(table)
        table = _moved(unlatched, 85, cum_prem_init=50000.0)(table)
        table = _set("sum_assured_init", [shortfall], 99000.0)(table)
        table = _set("cum_prem_init", [shortfall], -500.0)(table)
        table = table.assign(duration_mth=table["duration_mth"].astype(float),
                             is_mec_init=table["is_mec_init"].astype(float))
        table = table.assign(**{c: table[c].astype("int64") for c in whole})
        return _set("duration_mth", [future], -120.0)(table)

    assert all((committed[c] % 1 == 0).all() for c in whole)
    folder = _sec_inputs(tmp_path, edit(committed), edits={
        file: _as_floats(columns) for file, columns in FLOAT_KEYS.items()})
    for file, columns in FLOAT_KEYS.items():
        written = pd.read_csv(folder.parent / file)
        assert all(written[c].dtype == float for c in columns), file
    model = mx.read_model(folder, name=_name("edges"))
    try:
        for cell in EXTENTS:
            value = model.Data.cells[cell]()
            assert (type(value), value) == (int, sec_model.Data.cells[cell]()), cell
        assert np.array_equal(model.Data.coi_rate_last_years(),
                              sec_model.Data.coi_rate_last_years())
        read = model.Data.model_point_table()
        assert read["duration_mth"].dtype == float and read["is_mec_init"].dtype == float
        assert all(read[c].dtype == "int64" for c in whole)
        df = _point(model, last).result_cf()
        assert len(df) == 24 and (df == 0.0).all().all()
        assert _point(model, anniv).wd_used_year(0) == 0.0
        p = _point(model, mid)
        assert p.duration_mth(0) == 13 and type(p.duration_mth(0)) is int
        assert p.wd_used_year_init() == 25.0 and type(p.wd_used_year_init()) is float
        assert p.wd_used_year(0) == 25.0
        p = _point(model, latched)
        assert p.is_mec_init() is True and p.is_mec(0) is True
        p = _point(model, unlatched)
        assert p.is_mec_init() is False and p.policy_year(0) == 8
        assert p.is_mec(0) is False
        assert p.cum_prem_init() == 50000.0 and type(p.cum_prem_init()) is float
        p = _point(model, shortfall)
        assert p.sum_assured_init() == 99000.0 and type(p.sum_assured_init()) is float
        assert p.db_pp(0) == p.sum_assured_init() + p.av_pp_db_basis(0)
        assert p.av_pp_db_basis(0) == pytest.approx(407.74, abs=0.005)
        assert p.cum_prem_init() == -500.0
        assert p.cum_prem_pp(0) == -500.0 + p.premium_pp(0)
        for twin in NEW_BUSINESS:
            mine, base = _row(model, "twin", twin, 0), _row(sec_model, "twin", twin, 0)
            for report in REPORTS:
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=0, atol=0) == [], (twin, report)
        late = _point(model, future)
        assert (late.t_entry(), late.proj_len(), late.pols_new_biz(120)) == (
            120, 1152, 1.0)
    finally:
        model.close()


def test_each_rule_reads_the_months_just_outside_it(s_model, tmp_path):
    """Each window of policy months, and the 7-pay limit, is read just outside its rule.

    The malformed table refuses each rule over a window of policy months in the window's
    first month and its last: the face above 0 and at most the face at issue from month 1,
    the year's usage on the anniversaries, and the MEC latch from month 1 to month 84 and
    a cent past the 7-pay limit.  Here each is read just outside, so that a window moved a
    month either way fails the one test or the other (§5.2, T5, precised at M10).  Rows
    appended to the committed table under ids of their own:

    * S's point 1 restated with S's state at month 1: one month in force it holds a
      state, which a policy not yet in force may not;
    * the same at month 11, the month before the first anniversary, with $25 of the
      year's allowance used, which the year's usage rule refuses on the anniversary alone;
    * the point valued at the first anniversary with its premiums to date at the 7-pay
      limit of policy year 1, $6,702.10, exactly, and the latch off, which the latch
      refuses only past it.

    ``Data`` reads the table, and no row's ``proj_len()`` refuses it.  The committed rows
    and the edges test read the other sides: month 0, where a policy not yet in force holds
    no state, for the face's rules and the latch; month 13 for the year's usage; month 85
    for the latch; and a splice row at the last projected month, 1031, for
    ``proj_len()``.
    """
    committed = _committed()
    s1 = _point(s_model, 1)
    anniv = _label(committed, "derived", 1, 12)

    def restated(d, **columns):
        return {**{column: extract(s1, d) for column, extract in SPEC.state.items()},
                "duration_mth": d, "policy_count": s1.pols_if(d), **columns}

    copies = {101: (anniv, restated(1)), 102: (anniv, restated(11, wd_used_year_init=25.0)),
              103: (anniv, {"cum_prem_init": committed.at[anniv, "seven_pay_prem"]})}
    rows = [committed.loc[[point]].assign(**changes, row_kind="copy").set_axis([label])
            for label, (point, changes) in copies.items()]
    table = pd.concat([committed, *rows]).rename_axis("point_id")
    model = mx.read_model(_sec_inputs(tmp_path, table), name=_name("outside"))
    try:
        assert len(model.Data.model_point_table()) == len(table)
        assert _point(model, 101).sum_assured_init() == 100000.0
        assert _point(model, 102).wd_used_year(0) == 25.0
        p = _point(model, 103)
        assert p.cum_prem_init() == p.seven_pay_prem() and not p.is_mec_init()
        for label in copies:
            assert _point(model, label).proj_len() > 0, label
    finally:
        model.close()


def _every_state_months(sp):
    """The months S point ``sp``, swept, is restated at by the every-state test, from 1.

    By default the edges of the windows ``Data``'s rules turn on (USLIB-SEC-PLAN.md §5.2,
    T5): every month of the first policy year of S's frame, and each anniversary with the
    months either side of it, where the year's usage restarts and the MEC latch's seven
    years run out; the months either side of each change in the sign of the account value
    entering a month, where a point enters and leaves the state the product refuses; and
    the last month of the frame.  With ``USLIB_SEC_FULL=1``, every month of the frame.
    """
    n = sp.proj_len()
    if SEC_FULL:
        return list(range(1, n))
    d0, bef_prem = sp.duration_mth_init(), _code(sp, "BEF_PREM")
    below = [sp.av_pp_at(d, bef_prem) < 0.0 for d in range(n)]
    months = {*range(1, min(12, n)), n - 1}
    for d in range(1, n):
        if (d0 + d) % 12 in (0, 1, 11):
            months.add(d)
        if below[d] != below[d - 1]:
            months |= {d - 1, d}
    return sorted(m for m in months if m >= 1)


def _states_s_reaches(s):
    """The states ``s``'s points reach, as ``(S point, month)``: ``(kept, below)``.

    Each month of :func:`_every_state_months` of each point of ``s``, an S model.
    ``below`` holds the months whose account value entering is below 0, the one
    state the product refuses by name: ``UL_US_S`` carries one once a point is in
    permanent shortfall, having no grace cascade to end it, and no policy in force holds
    one (D6).  ``kept`` holds every other.
    """
    kept, below = [], []
    for key, point_id in zip(point_keys(s), s.Data.model_point_table().index):
        sp = projection(s, key)
        bef_prem = _code(sp, "BEF_PREM")
        for d in _every_state_months(sp):
            (below if sp.av_pp_at(d, bef_prem) < 0.0 else kept).append((point_id, d))
    return kept, below


def _every_state_folder(root, s, states, edits):
    """SEC's inputs for one table of every S point's twin and a derived row at ``states``.

    Built by the generator from ``s`` (``sec_support.build_sec_table``) and written into
    a copy of the product directory, with ``edits`` beside it.  Returns its SEC folder.
    """
    spec = dataclasses.replace(SPEC, derived=tuple(states), future=())
    table, _ = build_sec_table(spec, s)
    return temp_inputs(root, model_path(SEC), model_points=table, model_point_file=TABLE,
                       edits=edits)


def _refused_in_force(s, states, root, refs, edits):
    """What ``Data`` and ``proj_len()`` refuse of ``states`` of ``s``, restated in force.

    One table of every S point's twin and a derived row at each state
    (:func:`_every_state_folder`), which a model read with ``refs`` set first reads,
    through ``Data``, and then asks every row for its frame, releasing each.  Returns each
    refusal, the line naming it: ``Data``'s, or each row's ``proj_len()``'s.
    """
    model = mx.read_model(_every_state_folder(root, s, states, edits), name=_name("every"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        try:
            read = model.Data.model_point_table()
        except Exception as err:                # reported, with the rows' states
            return [f"Data: {_raised(err)}"]
        assert len(read) == len(s.Data.model_point_table()) + len(states)
        refused = []
        for key in point_keys(model):
            try:
                projection(model, key).proj_len()
            except Exception as err:            # reported, so every row is asked
                refused.append(_raised(err))
            _release(model, key)
        return refused
    finally:
        model.close()


def test_every_state_s_reaches_is_accepted_in_force(s_model, spliced, tmp_path):
    """Every state ``UL_US_S`` reaches is a valid opening state, but one, on each input set.

    ``Data``'s rules and ``proj_len()``'s hold an opening state to what a policy in force
    can hold, so they must accept each state the S model reaches: a rule exercised only on
    the rows the other tests choose could refuse a state S reaches elsewhere (D6).  So
    every S point is restated in force by the generator at the edges of the windows those
    rules turn on, or with ``USLIB_SEC_FULL=1`` at every month of its frame
    (:func:`_every_state_months`), into one table beside the twins: ``Data`` reads it, and
    no row's ``proj_len()`` refuses it (:func:`_refused_in_force`).  It runs on each set
    of inputs the module runs S on whose states differ in more than the count (§5.2, T5,
    precised at M9): S's shipped References and inputs, on S's three points, about 700
    states; the splice's (:data:`SPLICED_REFS`, :data:`SPLICED_EDITS`), on those and the
    seven variants, about 2,200, where the charges cease at 100 and the lapse shock and
    the variants' withdrawals, premiums and classes move every balance; the margin test's,
    the splice's References on the point of :data:`LENT`, whose loan passes its cash value;
    and the cap test's, :data:`CAPPED_REFS` on the point of :data:`CAPPED`, whose policies
    all die at attained age 113.  The acquisition test's inputs move only the count, 3.7
    times S's, which ``Data`` holds only to 0 or more, and the declared-rates test moves
    its rates by formula, not by an input.

    But for one state, set aside first: an account value below 0, which ``UL_US_S``
    carries once a point is in permanent shortfall, as S's point 2 is from its month 677,
    the splice's points 2, 4 and 5 and the lent point too, and ``Data`` refuses by name,
    since no policy in force holds one.  It is the only state set aside, and a table
    holding one is refused, naming the point and saying what to do.
    """
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    (lent, lent_changes), (capped, capped_changes) = LENT, CAPPED
    others, aside = {}, {}
    try:
        for label, row, refs in (
                ("lent", s_table.loc[[lent]].assign(**lent_changes).set_axis(
                    pd.Index([10], name="point_id")), SPLICED_REFS),
                ("capped", s_table.loc[[capped]].assign(**capped_changes), CAPPED_REFS)):
            others[label] = mx.read_model(temp_inputs(
                tmp_path / f"s_{label}", model_path(TWIN), model_points=row,
                edits=SPLICED_EDITS), name=_name(f"s_{label}"))
            for ref, value in refs.items():
                setattr(others[label].Projection, ref, value)
        sets = (("shipped", s_model, {}, None, {2}),
                ("spliced", spliced[0], SPLICED_REFS, SPLICED_EDITS, {2, 4, 5}),
                ("lent", others["lent"], SPLICED_REFS, SPLICED_EDITS, {10}),
                ("capped", others["capped"], CAPPED_REFS, SPLICED_EDITS, set()))
        for label, s, refs, edits, short in sets:
            kept, aside[label] = _states_s_reaches(s)
            assert {point for point, _ in aside[label]} == short, (label, aside[label][:5])
            assert len(kept) >= 100 * len(s.Data.model_point_table()), (label, len(kept))
            refused = _refused_in_force(s, kept, tmp_path / label, refs, edits)
            assert not refused, f"{label}: {len(refused)} refused, first: {refused[:5]}"
    finally:
        for s in others.values():
            s.close()
    below = aside["shipped"][0]
    folder = _every_state_folder(tmp_path / "below", s_model, [below], None)
    point = _label(pd.read_csv(folder.parent / TABLE, index_col="point_id"), "derived",
                   *below)
    model = mx.read_model(folder, name=_name("below"))
    try:
        _refused_exactly(model.Data.model_point_table,
                         _AV_NUMBER.format(file=TABLE, point=point))
    finally:
        model.close()


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_table_is_what_s_generates(s_model):
    """``model_point_table_sec.csv`` is what UL_US_S and its table generate today.

    Every row and column, the text cells and the six opening-state columns included: an
    edit to an S row the table copies or derives from, or to an S formula a row's state is
    read from, fails here until ``python tools/gen_sec_points.py UL_US_SEC`` regenerates
    it, in the same commit.  Text and integers compare exactly, and a float by its value,
    to 1e-12, because the text the writer picks for a computed float depends on the
    platform's parser (§5.2).
    """
    assert check_generated(SEC, s_model=s_model) == []


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_two_clocks_on_the_shipped_points(sec_model):
    """``t`` counts from the valuation date; ``duration_mth(t)`` from issue (D3, D4).

    On a twin of S's new business the two coincide, its policies enter as new business at
    ``t = 0``, and its frame is 1,032 months, the projection's end at attained age 121.
    S's in-force point is in policy year 11 at attained age 45 at ``t = 0``, past its
    surrender charge, with 912 months left.  The point valued at 113 is in the lapse
    shock's year, which ends at ``t = 7``, its tenth anniversary.  The point valued six
    months after S's in-force point is in force 126 months, with its loan.  The point valued
    at 1008, the first month at attained age 119, where the table's rate reaches 1, loses
    every life in month 0.  The point issued 25 months on has nothing in force and nothing
    to do before ``t = 25``, and before issue its policy years are -2, -1 and 0, which the
    guards must answer for.

    ``pols_if_at``'s ``"BEF_NB"`` counts the policies before the month's new business, so
    in the issue month it is 0 where ``pols_if`` holds the issued count; ``"BEF_MAT"``
    keeps ``UL_US_S``'s meaning, that count, since nothing matures; and a timing the model
    does not know is refused rather than answered with another count.
    """
    twin = _row(sec_model, "twin", 1, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 1031)] == [0, 1, 1031]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0), twin.pols_if(0)) == (
        0, 0.0, 1.0, 1.0)
    assert twin.omega_mth() == twin.proj_len() == 1032
    assert twin.is_active(1031) and not twin.is_active(1032)
    assert twin.pols_if_at(0, _code(twin, "BEF_MAT")) == twin.pols_if(0) == 1.0
    assert twin.pols_if_at(0, _code(twin, "BEF_NB")) == 0.0
    in_force = _row(sec_model, "twin", IN_FORCE, 0)
    assert (in_force.duration_mth(0), in_force.policy_year(0), in_force.age(0),
            in_force.proj_len()) == (120, 11, 45, 912)
    assert in_force.pols_if(0) == in_force.pols_if_init() == in_force.policy_count() == 1.0
    assert in_force.surr_charge_pp(0) == 0.0 and in_force.pols_new_biz(0) == 0.0
    shock = _row(sec_model, "derived", 1, 113)
    assert [shock.lapse_rate_sc_mult(t) for t in range(8)] == [2.0] * 7 + [1.0]
    assert (shock.policy_year(6), shock.policy_year(7)) == (10, 11)
    assert shock.surr_charge_pp(0) == 0.0
    loan = _row(sec_model, "derived", IN_FORCE, 6)
    assert (loan.duration_mth(0), loan.policy_year(0), loan.age(0)) == (126, 11, 45)
    assert loan.loan_bal_pp_bom(0) == loan.loan_bal_init() == pytest.approx(2027.31,
                                                                           abs=0.005)
    last = _row(sec_model, "derived", 1, 1008)
    assert (last.proj_len(), last.age(0), last.mort_rate(0)) == (24, 119, 1.0)
    assert last.pols_if(0) > 0.0 and last.pols_if(1) == 0.0
    fut = _row(sec_model, "future", 1, -25)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-25, 25, 1057)
    assert [fut.policy_year(t) for t in range(26)] == [-2] + [-1] * 12 + [0] * 12 + [1]
    assert not any(fut.is_active(t) for t in range(25)) and fut.is_active(25)
    assert (fut.pols_if(24), fut.pols_new_biz(25), fut.pols_if(25), fut.premium_pp(25)) == (
        0.0, 1.0, 1.0, 150.0)
    _refused(lambda: twin.pols_if_at(0, "BEF_LUNCH"), "invalid timing")
    _refused(lambda: twin.av_pp_at(0, "BEF_LUNCH"), "invalid timing")


def test_s_point_3_is_its_twin_from_the_valuation_date(sec_model, s_model):
    """At the shipped assumptions S's in-force point is S's own projection, in force.

    ``UL_US_S`` opens its point 3 at its own ``t = 0``, 120 months in, with the account
    value and the loan of its own columns, and with the four restarts it assumes: the face
    at issue in force, no withdrawal used, no premiums paid and the latch off.  Its twin
    carries those as its opening state, and from the valuation date on it is S's point in
    every cell but those expense inflation moves, which carries S's goldens on the point
    over: the loan entering month 0 and rolled forward a year at the charged rate, the
    duration offset, and the shortfall table's 912 months, none in shortfall.
    """
    p, s = _row(sec_model, "twin", IN_FORCE, 0), _point(s_model, IN_FORCE)
    assert p.av_pp_init() == s.av_pp_init() == 15000.0
    assert p.loan_bal_init() == s.loan_bal_init() == 2000.0
    assert p.sum_assured_init() == p.sum_assured() == 100000.0
    assert (p.wd_used_year_init(), p.cum_prem_init(), p.is_mec_init()) == (0.0, 0.0, False)
    assert p.loan_bal_pp_bom(0) == 2000.0
    assert p.loan_bal_pp(11) == pytest.approx(2000.0 * 1.0275, rel=1e-12)
    assert p.wd_used_year(0) == 0.0
    assert p.proj_len() == 912 and not any(p.is_shortfall(t) for t in range(912))
    assert _continues_s(s, p, 0) == []


def test_every_committed_row_continues_its_s_point(sec_model, s_model):
    """Each derived and future row of the committed table is its S point from its month on.

    T6 holds the committed table to what the generator makes of S, each float to 1e-12
    absolute and relative, which pins a count as small as point 8's, 1.765e-10, only to
    about half a percent.  So each derived and future row is projected too, at the shipped
    assumptions, and its three reports compared with its S point's from the row's
    ``source_mth`` on, frame by frame, to 1e-9 relative with no absolute floor, as the
    splice compares them (§5.2, precised at M11): point 8's count itself, which a floor of
    1e-9 would compare against nothing, and the flows a count or an opening value gone
    stale moves, point 8's death claim at ``t = 0``, 8.3e-5, among them.  The shipped
    expense inflation runs from issue in S and from the valuation date here (D7), so
    ``result_cf``'s :data:`INFLATED` columns are left out, as in :func:`_continues_s`; the
    inflation test holds them.  S's in-force point, a twin, is compared cell by cell by
    the test before this one.
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
        s_df = theirs.result_cf()
        keep = [c for c in s_df.columns if c not in INFLATED]
        found = frame_mismatches(s_df, mine.result_cf(), t_offset=month, columns=keep,
                                 atol=0.0)
        for report in REPORTS[1:]:
            found += frame_mismatches(theirs.cells[report](), mine.cells[report](),
                                      t_offset=month, atol=0.0)
        assert found == [], (point_id, found)


def test_every_guarded_cell_holds_its_outside_cover_value(sec_model, spliced,
                                                          splice_records):
    """Outside cover each monthly cell holds its value, and no table is read past cover.

    The sets of the guard (:data:`OUTSIDE_COVER`, :data:`NEUTRAL`, :data:`CLOCK`,
    :data:`VALUATION_CLOCK`, :data:`BY_ARGUMENT` with :data:`OPENING`, and
    :data:`CARRIED`) are disjoint and together hold every cell of the model whose first
    parameter is ``t``, so a new cell must be placed in one before this test passes.  Then
    in every month before issue and at ``t = proj_len()``, the month after the frame, which
    the roll-forwards read, every one of them holds its value
    (:func:`_outside_cover_faults`):

    * on every committed point, once swept, at the shipped References;
    * on every row the splice compared, the core's or, with ``USLIB_SEC_FULL=1``, all of
      them, as each was recorded once compared (:func:`_settle`): there the survivors
      carried into ``t = proj_len()`` are not zero, and the variants' future rows read
      policy years -1 and 0 before issue, the single premium's among them, whose shock year,
      with no surrender charge, is 0;
    * and on two withdrawal rows read afresh with charges ceasing at attained age 125, past
      the frame's end, where no contractual age stops a withdrawal, a premium or a charge at
      ``t = proj_len()`` and only the guard can.

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
    cases = _selected(GRID, CORE_GRID)
    for case in cases:
        record = _record_of(spliced, splice_records, case)
        if record["raised"]:
            faults.append(f"{_case_id(*case)}: raised {record['raised']}")
        faults += record["guard"]
    sec = spliced[1]
    late = mx.read_model(sec.Data.input_dir() / SEC, name=_name("charges_125"))
    try:
        for ref, value in {**SPLICED_REFS, "charges_cease_age": 125}.items():
            setattr(late.Projection, ref, value)
        for case in (("future", 4, -13), ("derived", 5, 13)):
            key = _row_key(late, *case)
            faults += _outside_cover_faults(projection(late, key),
                                            f"{_case_id(*case)}, charges_cease_age 125")
            _release(late, key)
    finally:
        late.close()
    assert cases and not faults, (
        f"{len(faults)} faults outside cover, first:\n  " + "\n  ".join(faults[:20]))


# Each new opening-state column on a splice row, beside the same row with the column as
# UL_US_S assumes for its in-force point: (the row, the column, its value there).  The face
# goes to the face at issue, None here; the rest to zero.
SHOWN = ((("derived", 7, 71), "cum_prem_init", 0.0),
         (("derived", 6, 85), "is_mec_init", 0),
         (("derived", 4, 13), "wd_used_year_init", 0.0),
         (("derived", 4, 24), "sum_assured_init", None))


def test_the_opening_state_shows_on_the_variants(spliced, sec_model, s_model, tmp_path):
    """Each new opening-state column changes what the point does, where it is in force.

    ``UL_US_S`` takes four restarts in force: the face at issue, nothing used of the
    year's allowance, no premiums paid and the latch off.  In one copy with the splice's
    inputs, four of the splice's rows are read twice, as built and with their column as S
    assumes, and month 0 and month 1 differ as the column says:

    * ``cum_prem_init``.  TARGET at $6,000 a year, S's month 71: the premiums of 33,750.00
      paid leave 388.15 of guideline premium room, so month 0 collects 388.15 and the rest
      of the year nothing, 388.15 over the twelve months.  Restarted, it collects the
      planned 450.00 at once and 5,290.00 over the year.
    * ``is_mec_init``.  The single premium at the guideline single premium, S's month 85,
      policy year 8: the 7-pay test no longer runs, and ``is_mec(0)`` is ``True`` from the
      latch alone.  Restarted, it is ``False``.
    * ``wd_used_year_init``.  Option A withdrawing $60 a month, S's month 13: 60.00 of the
      year's allowance is used, so the free amount at ``t = 0`` is 82.39 rather than
      142.39, and at ``t = 1`` the face is cut by 35.66, to 99,964.34.  Restarted, the face
      is not cut.
    * ``sum_assured_init``.  The same point at S's month 24: the face in force is
      99,442.27, and so is ``db_pp(0)``.  At the face at issue both are 100,000.00.  The
      surrender charge stays 691.67 either way, on the face at issue.

    And the two columns ``UL_US_S`` has: S's in-force point restated six months on carries
    15,755.09 of account value and a loan of 2,027.31, S's own close of its month 5, where
    S's in-force columns carry 15,000.00 and 2,000.00.
    """
    sec = spliced[1]
    table = sec.Data.model_point_table()
    rows, zeroed = [], {}
    for number, (case, column, value) in enumerate(SHOWN):
        built = table.loc[[_label(table, *case)]]
        row = built.assign(**{column: built["sum_assured"] if value is None else value},
                           policy_id=built["policy_id"] + "-S")
        row.index = pd.Index([1000 + number], name="point_id")
        rows += [built, row]
        zeroed[case] = (built.index[0], 1000 + number)
    model = mx.read_model(_sec_inputs(tmp_path, pd.concat(rows), edits=SPLICED_EDITS),
                          name=_name("shown"))
    try:
        for ref, value in SPLICED_REFS.items():
            setattr(model.Projection, ref, value)
        a, z = (_point(model, i) for i in zeroed[("derived", 7, 71)])
        assert a.cum_prem_init() == 33750.0
        assert (a.premium_pp(0), z.premium_pp(0)) == pytest.approx((388.15, 450.00),
                                                                   abs=0.005)
        assert sum(a.premium_pp(t) for t in range(12)) == pytest.approx(388.15, abs=0.005)
        assert sum(z.premium_pp(t) for t in range(12)) == pytest.approx(5290.00, abs=0.005)
        a, z = (_point(model, i) for i in zeroed[("derived", 6, 85)])
        assert a.policy_year(0) == 8 and not _in_year_test(a, 0)
        assert (a.is_mec_init(), a.is_mec(0), z.is_mec(0)) == (True, True, False)
        a, z = (_point(model, i) for i in zeroed[("derived", 4, 13)])
        assert a.wd_used_year_init() == pytest.approx(60.0, abs=1e-9)
        assert (a.wd_free_pp(0), z.wd_free_pp(0)) == pytest.approx((82.39, 142.39),
                                                                   abs=0.005)
        assert (a.face_reduction_pp(1), z.face_reduction_pp(1)) == pytest.approx(
            (35.66, 0.0), abs=0.005)
        assert (a.sum_assured_at(1), z.sum_assured_at(1)) == pytest.approx(
            (99964.34, 100000.0), abs=0.005)
        a, z = (_point(model, i) for i in zeroed[("derived", 4, 24)])
        assert a.sum_assured_init() == pytest.approx(99442.27, abs=0.005)
        assert (a.db_pp(0), z.db_pp(0)) == pytest.approx((99442.27, 100000.0), abs=0.005)
        assert a.surr_charge_pp(0) == z.surr_charge_pp(0) == pytest.approx(691.67,
                                                                           abs=0.005)
    finally:
        model.close()
    p, s = _row(sec_model, "derived", IN_FORCE, 6), _point(s_model, IN_FORCE)
    assert p.av_pp_init() == pytest.approx(15755.09, abs=0.005)
    assert p.loan_bal_init() == pytest.approx(2027.31, abs=0.005)
    assert p.av_pp_init() == pytest.approx(s.av_pp_at(6, "BEF_PREM"), rel=1e-12)
    assert p.loan_bal_init() == pytest.approx(s.loan_bal_pp(5), rel=1e-12)
    assert (s.av_pp_init(), s.loan_bal_init()) == (15000.0, 2000.0)


def test_the_end_of_the_projection_carries_the_survivors(spliced, splice_records,
                                                         sec_model):
    """The survivors of the last month, and their account value, are carried, as in S.

    The projection ends where the mortality table does, not where the contract does, and
    S's roll-forwards read the month after the frame.  At the splice's A/E of 0.56 there
    are lives left at the end of every frame, 9.27e-6 of a policy on S's in-force point, so
    on every row the splice compared, the core's or, with ``USLIB_SEC_FULL=1``, all of them:

    * the count at ``t = proj_len()``, at every timing, is the survivors of the last month,
      exactly, and not zero;
    * the account value per policy there is the last month's close, exactly, and the
      account value in force there the two multiplied;
    * both are S's at the same month, ``proj_len() + source_mth`` on S's clock, to 1e-9,
      exactly on the twin and the future rows, whose opening values are S's own and not
      read back from a CSV, and both checks, which read them, hold in both models;
    * and nothing else happens there: no premium, death, lapse, claim or expense, and a net
      cash flow of 0.

    On the committed points, at the shipped A/E, every life has died by then, and the count
    carried is exactly 0.
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
        theirs = (s_proj.pols_if(s_month), s_proj.av_at(s_month, _code(s_proj, "BEF_PREM")))
        mine = (carry["pols_if"], carry["av_at"])
        if not carry["survivors"] > 0.0:
            faults.append(f"{where}: no survivors at t = proj_len()")
        if carry["pols_if"] != carry["survivors"] or any(
                count != carry["survivors"] for count in carry["timings"]):
            faults.append(f"{where}: the count carried is not the survivors: {carry}")
        if (carry["av_pp"] != carry["av_pp_last"]
                or carry["av_at"] != carry["av_pp"] * carry["pols_if"]):
            faults.append(f"{where}: the account value carried is not the close: {carry}")
        if not (mine == theirs if exact else mine == pytest.approx(theirs, rel=1e-9)):
            faults.append(f"{where}: {mine} carried, where S carries {theirs}")
        if carry["checks"] != (True, True) or not (s_proj.check_av_roll_fwd()
                                                   and s_proj.check_margin()):
            faults.append(f"{where}: a check fails: {carry['checks']}")
        if any(flow != 0.0 for flow in carry["flows"]):
            faults.append(f"{where}: flows at t = proj_len(): {carry['flows']}")
    assert cases and not faults, faults[:10]
    twin = _record_of(spliced, splice_records, ("twin", IN_FORCE, 0))["carry"]
    assert twin["pols_if"] == pytest.approx(9.27e-6, rel=1e-3)
    for key in point_keys(sec_model):
        p = projection(sec_model, key)
        assert p.pols_if(p.proj_len()) == 0.0, key


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date dollars, for every point alike (D7).

    At the shipped 2.5%, the factor at ``t`` is ``1.025^(t // 12)`` on every point,
    whatever its duration: ``UL_US_S``'s step by policy year moved onto ``t``, so every
    point of a block steps on the valuation anniversaries.  So S's in-force point, valued on
    its tenth anniversary, pays S's expenses deflated by ``1.025^10``, the inflation S had
    applied since issue, in every month.  The point valued at 113 pays S's month
    ``113 + t`` deflated by ``1.025^9`` for ``t = 0 .. 6``, by ``1.025^10`` for
    ``t = 7 .. 11``, where S has stepped at the policy anniversary and this model has not,
    and by ``1.025^9`` again at ``t = 12``, where this model steps.  The point issued 25
    months on pays S's month-``s`` maintenance inflated by the valuation years that have
    passed before its policy years, ``1.025^((25 + s) // 12 - s // 12)``.  This is the only
    test that sees inflation run on its clock: the splice sets the rate to 0, and on a point
    issued at ``t = 0`` the clocks agree.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    for key in point_keys(sec_model):
        p = projection(sec_model, key)
        assert all(p.inflation_factor(t) == (1 + INFLATION) ** (t // 12)
                   for t in range(p.proj_len())), key
    p, s = _row(sec_model, "twin", IN_FORCE, 0), _point(s_model, IN_FORCE)
    for t in range(p.proj_len()):
        assert p.expenses(t) == pytest.approx(s.expenses(t) / (1 + INFLATION) ** 10,
                                              rel=1e-12), t
    p, s = _row(sec_model, "derived", 1, 113), _point(s_model, 1)
    for t, years in [*((t, 9) for t in range(7)), *((t, 10) for t in range(7, 12)),
                     (12, 9)]:
        assert s.expenses(113 + t) == pytest.approx(
            p.expenses(t) * (1 + INFLATION) ** years, rel=1e-12), t
    p = _row(sec_model, "future", 1, -25)
    for s_t in range(s.proj_len()):
        steps = (25 + s_t) // 12 - s_t // 12
        assert p.expenses(25 + s_t) == pytest.approx(
            s.expenses(s_t) * (1 + INFLATION) ** steps, rel=1e-12), s_t


def _rising_credited_rate(t):
    """The declared rate, rising a basis point a month from the valuation date."""
    return crediting_rate_curr + 0.0001 * t                          # noqa: F821


def _rising_competitor_rate(t):
    """A competitor rate rising two basis points a month from 6%, apart from the rate."""
    return 0.06 + 0.0002 * t


def test_the_declared_rates_run_on_the_valuation_clock():
    """The credited and competitor rates are paths on ``t``, one for every point (D7).

    Both ship flat, so no number shows the clock they are read on, and the test overrides
    their formulas in models just read, before anything is computed.  That is a formula
    override, so the test is modelx's alone (USLIB-SEC-PLAN.md K7).  On the twins of S's
    points 1 and 3, the point restated six months after S's in-force point and the point
    issued 25 months on, at ``t = 0``, 1 and 12, policies of four durations read one
    month:

    * with the credited rate rising a basis point a month, ``crediting_rate_ann``,
      ``comp_rate_ann``, which follows it, the monthly credited rate and the dynamic lapse
      multiplier, still 1, are one number for every point at each ``t``, the rate's at
      ``t``;
    * with the competitor rate also on a path of its own, the dynamic lapse multiplier is
      one number for every point, ``1 + 5 (0.01 + 0.0001 t)``, its excess over the credited
      rate at ``t``.

    A rate read at a policy month, as a declared-rate scenario keyed by the policy's
    duration would be, gives each point another number.

    On the second pair of paths every number moves, and each is checked where it lands.
    On the four points the account value entering each month, ``av_pp_at(t, "BEF_PREM")``,
    which forms the previous month's close itself, is that close, ``av_pp(t - 1)``,
    exactly, from ``t_entry() + 1`` to the last month, so it credits month ``t - 1`` at that
    month's rate; and both checks hold.  And ``UL_US_S``, given the same paths, which on a
    twin are the same months, projects what the twins of its points 1 and 3 project, in
    ``result_cf``, ``result_pols`` and ``result_av``, to 1e-9, with the dynamic lapse
    multiplier above 1 in every month, which no other comparison with S reaches.  Expense
    inflation is set to 0 in both models for that, since it runs on the two clocks by
    design.
    """
    points = (("twin", 1, 0), ("twin", IN_FORCE, 0), ("derived", IN_FORCE, 6),
              ("future", 1, -25))
    for overrides in ({"crediting_rate_ann": _rising_credited_rate},
                      {"crediting_rate_ann": _rising_credited_rate,
                       "comp_rate_ann": _rising_competitor_rate}):
        moved = "comp_rate_ann" in overrides
        fresh = mx.read_model(model_path(SEC), name=_name("rates"))
        s = mx.read_model(model_path(TWIN), name=_name("s_rates")) if moved else None
        try:
            for model in (fresh, s) if moved else (fresh,):
                if moved:
                    model.Projection.inflation_rate = 0.0
                for cell, formula in overrides.items():
                    model.Projection.cells[cell].formula = formula
            ps = [_row(fresh, *point) for point in points]
            for t in (0, 1, 12):
                rate = 0.04 + 0.0001 * t
                if moved:
                    want = {"lapse_rate_dyn_mult": 1 + 5 * (0.01 + 0.0001 * t)}
                else:
                    want = {"crediting_rate_ann": rate, "comp_rate_ann": rate,
                            "inv_return_mth": (1 + rate) ** (1 / 12) - 1,
                            "lapse_rate_dyn_mult": 1.0}
                for cell, value in want.items():
                    got = [p.cells[cell](t) for p in ps]
                    assert got == pytest.approx([value] * len(ps), rel=1e-12), (cell, t)
            if not moved:
                continue
            del ps
            for point in points:
                key = _row_key(fresh, *point)
                p = projection(fresh, key)
                if point[0] == "twin":
                    theirs = _point(s, point[1])
                    for report in REPORTS:
                        assert frame_mismatches(theirs.cells[report](),
                                                p.cells[report]()) == [], (point, report)
                    assert all(p.lapse_rate_dyn_mult(t) > 1.0
                               for t in range(p.proj_len())), point
                    _release(s, _key(s, point[1]))
                bef_prem = _code(p, "BEF_PREM")
                apart = [t for t in range(p.t_entry() + 1, p.proj_len())
                         if p.av_pp_at(t, bef_prem) != p.av_pp(t - 1)]
                assert not apart, (point, apart[:5])
                assert p.check_av_roll_fwd() and p.check_margin(), point
                del p
                _release(fresh, key)
        finally:
            fresh.close()
            if s is not None:
                s.close()


def _not_a_number(t):
    """A declared rate that is not a number, in every month."""
    return float("nan")


def test_a_residual_that_is_not_a_number_fails_its_check():
    """A check whose residual is not a number fails, as ``UL_US_S``'s ``math.isclose`` does.

    The checks are the model's one guard against an account value that is not a number:
    the floors at zero in the cash surrender value and in the death benefit's basis turn
    a NaN account value into 0, so the cash flows stay numbers and nothing else shows it.
    On a model just read, with the credited rate overridden to NaN before anything is
    computed (a formula override, so modelx's alone), each check's residual is NaN in some
    month, on S's in-force point and on the worked example's, and each check is
    ``False``, where a check that asked whether the residual is above its tolerance would
    pass it.  The year's cash flows are finite floats, so the checks are what fails.
    """
    fresh = mx.read_model(model_path(SEC), name=_name("nan"))
    try:
        fresh.Projection.cells["crediting_rate_ann"].formula = _not_a_number
        for point in (IN_FORCE, 1):
            p = _row(fresh, "twin", point, 0)
            for check in ("check_av_roll_fwd", "check_margin"):
                resid, months = p.cells[f"{check}_resid"], range(p.proj_len())
                assert any(math.isnan(resid(t)) for t in months), (point, check)
                assert p.cells[check]() is False, (point, check)
            flows = [p.cells[c](t) for c in ("premiums", "expenses", "net_cf")
                     for t in range(12)]
            assert all(math.isfinite(v) for v in flows), point
    finally:
        fresh.close()


# S's in-force point withdrawing $50 a month on Option B, F PNT, with its loan: from S's
# month 454 the loan exceeds the cash value, the surrender pays the net cash value floored
# at 0, and recovers only the cash value of the loan.  Restated in force at 453, the month
# before, its account value still above 0, it is read under the splice's References with
# the class's COI rows.
LENT = (IN_FORCE, {"policy_id": "UL-900016", "wd_pp": 50.0, "db_option": "B", "sex": "F",
                   "rate_class": "PNT"})
LENT_MTH = 453


def test_the_margin_identity_holds_once_a_loan_exceeds_the_cash_value(tmp_path):
    """Once the loan exceeds the cash value, the margin identity still closes (a departure).

    ``UL_US_S``'s identity adds back the whole loan on every lapse,
    ``L(t) x pols_lapse(t)``, as though the lapse claim were ``CSV - L``.  The claim is the
    net cash value, floored at 0, so once the loan exceeds the cash value the identity is
    off by ``(CSV(t) - L(t)) x pols_lapse(t)``, and ``UL_US_S``'s check fails on a
    projection that is right.  This model's adds back the loan the surrender recovers,
    ``min(L(t), CSV(t)) x pols_lapse(t)``.  On the point of :data:`LENT`, restated in force
    in the month before its loan passes its cash value:

    * its three reports are S's from that month on, to 1e-9 relative with no absolute
      floor, as a splice row's are (:func:`_compare`): the projection is S's;
    * from ``t = 1`` its loan exceeds its cash value, policies lapse, and in each such month
      S's identity misses by ``(CSV - L) x pols_lapse``, to the identity's own tolerance;
    * this model's two checks hold, and ``UL_US_S``'s ``check_margin`` fails.
    """
    base, changes = LENT
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    row = s_table.loc[[base]].assign(**changes)
    row.index = pd.Index([10], name="point_id")
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=row,
                                  edits=SPLICED_EDITS), name=_name("lent_s"))
    sec = None
    try:
        for ref, value in SPLICED_REFS.items():
            setattr(s.Projection, ref, value)
        spec = dataclasses.replace(SPEC, derived=((10, LENT_MTH),), future=())
        table, _ = build_sec_table(spec, s)
        sec = mx.read_model(_sec_inputs(tmp_path / "sec", table, SPLICED_EDITS),
                            name=_name("lent"))
        for ref, value in SPLICED_REFS.items():
            setattr(sec.Projection, ref, value)
        sp, p = _point(s, 10), _row(sec, "derived", 10, LENT_MTH)
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
        assert p.check_margin() and p.check_av_roll_fwd()
        assert not sp.check_margin() and sp.check_av_roll_fwd()
    finally:
        if sec is not None:
            sec.close()
        s.close()


# ---------------------------------------------------------------------------
# The 7-pay test's last year
#
# S's point 1 at $4,700 a year, under a premium persistency that rises 12% a year,
# 1.12^(y - 1), where S's falls 2 points a year: its premiums to date stay inside the 7-pay
# limit through policy year 6, 38,141.39 against 40,212.60, and through month 82, 46,645.28
# against 46,914.70, and pass it in month 83, the last of policy year 7, at 47,418.36.
# With a persistency that falls, as shipped, a level premium that ever fails the test fails
# it in its first year, so neither the committed table nor the splice's variants reach the
# window's last year.  It is read under the splice's References, with the persistency
# table its own (MEC7_EDITS).
MEC7 = (1, {"policy_id": "UL-900021", "premium_pp_ann": 4700.0})
MEC7_MTH = 83


def _rising_persistency(table):
    """S's persistency table with each year's factor ``1.12^(y - 1)``, rising from 1."""
    return table.assign(prem_persistency=[round(1.12 ** (y - 1), 6)
                                          for y in table["policy_year"]],
                        provenance="test copy")


MEC7_EDITS = {**SPLICED_EDITS, "prem_persistency.csv": _rising_persistency}


def test_a_first_7_pay_failure_in_policy_year_7_is_latched(tmp_path):
    """The 7-pay test runs to the last month of policy year 7, and a failure there latches.

    ``is_mec`` tests ``CumPrem(t) > 7-pay limit`` in the first seven policy years and
    latches; no committed row or splice variant first fails it later than year 1, so a
    window a year or a month short would pass every other test (§7.4, *Record — M6*,
    *Carried into M13*: the 7-pay window, pinned in UL by a splice of its own).  On the
    point of :data:`MEC7`, under :data:`MEC7_EDITS`, ``UL_US_S``'s test first fails in
    month :data:`MEC7_MTH`, the last of policy year 7, and holds to the end.  Three rows of
    the point, built from S by the generator, each continue S from their month on
    (:func:`_compare`), the 7-pay test and the latch among the cells compared, to 1e-9
    relative with no absolute floor: the twin issued at the valuation date, which latches
    from month 83; the row restated at 83, which fails the test in the valuation month
    with no latch carried in; and the row at 84, in policy year 8, where the test no
    longer runs and the latch carried in holds alone.  A fourth, the row at 84 with its
    premiums to date at the limit of year 7, $46,914.70, and no latch, which ``Data``
    accepts, is no MEC though its premium of the month takes it past the limit: the test
    is not read a month past its window.
    """
    base, changes = MEC7
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    row = s_table.loc[[base]].assign(**changes)
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=row,
                                  edits=MEC7_EDITS), name=_name("mec7_s"))
    sec = None
    try:
        for ref, value in SPLICED_REFS.items():
            setattr(s.Projection, ref, value)
        sp = _point(s, base)
        _sweep_s(sp)
        failed = [t for t in range(sp.proj_len()) if sp.is_mec(t)]
        assert failed == list(range(MEC7_MTH, sp.proj_len()))
        assert sp.policy_year(MEC7_MTH) == 7 and sp.policy_year(MEC7_MTH + 1) == 8
        assert sp.cum_prem_pp(MEC7_MTH) > sp.seven_pay_limit(MEC7_MTH)
        assert sp.cum_prem_pp(MEC7_MTH - 1) <= sp.seven_pay_limit(MEC7_MTH - 1)
        spec = dataclasses.replace(SPEC, derived=((base, MEC7_MTH), (base, 84)), future=())
        table, _ = build_sec_table(spec, s)
        late = table[table["source_mth"] == 84]
        limit = 7 * float(late["seven_pay_prem"].iloc[0])
        table = pd.concat([table, late.assign(
            point_id=table["point_id"].max() + 1, policy_id=f"{changes['policy_id']}-L84",
            cum_prem_init=limit, is_mec_init=0, row_kind="copy")], ignore_index=True)
        sec = mx.read_model(_sec_inputs(tmp_path / "sec", table, MEC7_EDITS),
                            name=_name("mec7"))
        for ref, value in SPLICED_REFS.items():
            setattr(sec.Projection, ref, value)
        rows = ((("twin", base, 0), FUTURE_EXEMPT, _issued_later),
                (("derived", base, MEC7_MTH), SPLICE_EXEMPT, None),
                (("derived", base, 84), SPLICE_EXEMPT, None))
        for case, exempt, arg_map in rows:
            key = _row_key(sec, *case)
            p = projection(sec, key)
            assert _compare(sp, p, case[2], exempt, arg_map) == [], case
            assert [t for t in range(p.proj_len()) if p.is_mec(t)] == list(
                range(max(MEC7_MTH - case[2], 0), p.proj_len())), case
            if case[0] == "derived":
                assert p.is_mec_init() is (case[2] > MEC7_MTH), case
                assert p.policy_year(0) == (7 if case[2] == MEC7_MTH else 8), case
            del p
            _release(sec, key)
        p = _point(sec, int(table["point_id"].max()))
        assert p.cum_prem_init() == limit and not p.is_mec_init()
        assert p.policy_year(0) == 8 and p.cum_prem_pp(0) > p.seven_pay_limit(0)
        assert not any(p.is_mec(t) for t in range(12))
    finally:
        if sec is not None:
            sec.close()
        s.close()


# Inputs at which a product or sum taken in another order than UL_US_S's differs in its
# last bit: an acquisition expense, a maintenance expense and a multiple of the counts that
# no binary fraction holds exactly.
ACQ, MAINT, COUNTS = 123.456, 77.7, 3.7


def test_acquisition_is_charged_on_new_business_only(tmp_path):
    """``expense_acq`` per policy issued, in the issue month, never on a policy in force.

    ``expense_acq`` ships at 0.  On a copy whose counts are :data:`COUNTS` times the
    committed table's, with :data:`ACQ` and :data:`MAINT` set, a charge per model point
    would show beside one per policy.  On every point, what ``expenses(t)`` holds beyond its
    maintenance part is ``ACQ * policy_count()`` in the issue month, ``t = -duration_mth``,
    and 0 in every other month to ``t = 26``, to 1e-9: the twins of S's new business bear it
    at ``t = 0``, the point issued 25 months on at ``t = 25``, and the points already in
    force never, though on the valuation clock their row 0 is ``t = 0``.

    ``UL_US_S`` charges acquisition on the count in force in the issue month, which on a
    point issued at the valuation date is the issued count, so the twins agree with S at
    any count, and T1 needs no S point to count one policy.  The formula is S's, in S's
    order, no product or sum reordered, so on the twins of S's new business, read by S at
    the same counts and inputs, the expenses are S's bit for bit: the acquisition charged
    on the issued count before the maintenance part is added, rather than after, differs
    in the last bit at these inputs.
    """
    table = _committed()
    model = mx.read_model(_sec_inputs(tmp_path / "sec", table.assign(
        policy_count=COUNTS * table["policy_count"])), name=_name("acquisition"))
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    s_folder = temp_inputs(tmp_path / "s", model_path(TWIN), model_points=s_table.assign(
        pols_if_init=COUNTS * s_table["pols_if_init"]))
    s = mx.read_model(s_folder, name=_name("acquisition_s"))
    try:
        for space in (model.Projection, s.Projection):
            space.expense_acq, space.expense_maint = ACQ, MAINT
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
# mort_rate caps the annual rate at 1, as UL_US_S's does.  At the shipped A/E UL_US_S's
# StdTob class, 1.75 times the base table, takes the product past 1 at attained age 113, at
# 1.095, and keeps it past 1 to the end of the projection.  The committed points are all
# StdNT, and the splice's A/E of 0.56 keeps every class below 1, so neither comes near it.
# One point is made to pass it, the way the variants are made: S's anchor cell in the StdTob
# class, with its own COI rows (SPLICED_EDITS), alone in a copy of S's table, under the
# splice's References with the A/E back at the shipped 1.0 (CAPPED_REFS).
CAPPED = (1, {"policy_id": "UL-900020", "rate_class": "StdTob"})
CAPPED_REFS = {**SPLICED_REFS, "mort_ae_factor": 1.0}
CAPPED_MTH = 936        # the first month at attained age 113, where the product passes 1


def _uncapped_mort_rate(proj, t):
    """``UL_US_S``'s annual mortality product in month t, the one its cap bounds."""
    table = proj.data.mort_table()
    a = min(max(proj.age(t), int(table.index.min())), int(table.index.max()))
    return float(table.loc[a, "mort_rate"]) * proj.class_factor() * proj.mort_ae_factor


def _sweep_months(proj):
    """Evaluate every monthly cell of an S point at every month of its frame.

    At each of its timings or kinds, as :func:`_sweep_s` reaches them, so that the cap test
    compares every monthly cell in every month the cap binds, those no report or check
    reads among them.
    """
    arguments = {**BY_ARGUMENT, **OPENING, "av_pp_at": AV_TIMINGS,
                 "av_at": (*AV_TIMINGS, "EOM")}
    names = sorted(_monthly_cells(proj))
    for t in range(proj.proj_len()):
        for name in names:
            labels = arguments.get(name)
            if labels is None:
                proj.cells[name](t)
            else:
                for label in labels:
                    proj.cells[name](t, _code(proj, label))


def test_an_annual_mortality_past_1_is_capped_in_both_models(tmp_path):
    """Where the annual mortality product passes 1, both models' rate is 1.

    On the point of :data:`CAPPED`, ``UL_US_S``'s product of the base rate, the class
    factor and the A/E (:func:`_uncapped_mort_rate`) passes 1 in month :data:`CAPPED_MTH`
    and stays past it to the end of the projection, on a point the contract issues.  Both
    models cap it: ``mort_rate`` and the monthly rate, ``1 - (1 - q)^(1/12)``, are 1.0 in
    every one of those months, the float, not the int 1, which compares equal to it, and
    S's are floats below 1 in every month before.  So every policy in force at the start of
    the first capped month dies in it, and none is in force after it.  ``result_cf()``,
    ``result_pols()`` and ``result_av()`` hold finite floats alone, and both checks hold.

    Each of the first three rows below agrees with S in every cell, as T1, T3 and the
    splice compare them (:data:`FUTURE_EXEMPT`, :data:`SPLICE_EXEMPT`: ``result_pols`` by
    its columns), at every argument S cached (``sec_support.twin_mismatches``), the capped
    months, ``result_cf()`` and ``result_av()`` included, but, in the issue month, the
    count before new business, which S counts as in force (:func:`_issued_later`).  It
    holds them to 1e-9 relative with no absolute floor, because the count before the cap
    falls to 2.1e-13, where the default floor of 1e-9 would compare it against nothing.
    S is swept as the splice sweeps it (:func:`_sweep_s`), and every monthly cell in
    every month (:func:`_sweep_months`).

    Four rows of the point, built from S by the generator under :data:`CAPPED_REFS`:
    issued at the valuation date and 25 months after it; restated in force in the month
    before the cap, opened with S's count and state there, and compared cell by cell as a
    splice row is; and restated five months into the capped year, opened with S's state
    there and one policy, since S's count there is 0.  On each, the rate is 1.0 from its
    first capped month, every policy in force there dies in it, and the count is 0.0
    after it.
    """
    base, changes = CAPPED
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN),
                                  model_points=s_table.loc[[base]].assign(**changes),
                                  edits=SPLICED_EDITS), name=_name("capped_s"))
    sec = None
    try:
        for ref, value in CAPPED_REFS.items():
            setattr(s.Projection, ref, value)
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
        sec = mx.read_model(_sec_inputs(tmp_path / "sec", table, SPLICED_EDITS),
                            name=_name("capped"))
        for ref, value in CAPPED_REFS.items():
            setattr(sec.Projection, ref, value)
        # Each row with the month its rate is first capped and, for the three S's count
        # opens, the exemptions of its comparison with S.
        rows = ((("twin", base, 0), cap, FUTURE_EXEMPT),
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
            assert p.check_av_roll_fwd() and p.check_margin(), case
            del p
            _release(sec, key)
    finally:
        if sec is not None:
            sec.close()
        s.close()


def _nan_factor():
    """NaN, what a blank factor carries: the formula a test puts in place of a cell's."""
    return float("nan")


def test_a_nan_that_reaches_the_cap_stays_nan():
    """A NaN that reaches the cap on mortality stays NaN, and is not read as 1.

    ``min`` keeps its first argument unless a later one compares smaller, in modelx and
    compiled alike, and no comparison with NaN holds, so with its bound first the cap would
    turn a NaN into 1.0: a blank class factor read as certain death, every flow finite.
    It is written ``min(q, 1.0)``, as ``UL_US_S`` writes it.  ``Data`` refuses a blank
    factor or rate as it reads the tables, so to send the cap a NaN, the formula of
    ``class_factor``, which feeds it, is replaced by one returning NaN, in a model read for
    the test, which modelx allows.  ``mort_rate`` must then be the float NaN in the first
    month and the last, and so must the monthly rate and the count after the first month.
    """
    model = mx.read_model(model_path(SEC), name=_name("nan"))
    try:
        model.Projection.cells["class_factor"].formula = _nan_factor
        p = _row(model, "twin", 1, 0)
        calls = [("mort_rate", (0,)), ("mort_rate", (p.proj_len() - 1,)),
                 ("mort_rate_mth", (0,)), ("pols_if", (1,))]
        lost = [f"{name}{args} = {value!r}" for name, args in calls
                for value in [p.cells[name](*args)]
                if not (type(value) is float and math.isnan(value))]
        assert not lost, f"the cap loses a NaN class_factor(): {lost}"
    finally:
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


# What only UL_US_S's docstrings may say: a reference into its Spaces, which the SEC pages
# would link to the wrong model; its clock, t counting policy months and t = 0 the issue
# month; "policy month t", which on the valuation clock is not one; the in-force restarts
# S assumes, which this model's opening state replaces; and the stub's timings, which here
# part in the issue month.
STALE = re.compile(r"~\.UL_US_S\.|``t`` counts \*\*policy months\*\*"
                   r"|``t = 0`` is the \*\*issue month\*\*|policy month ``?t\b"
                   r"|pols_if\(0\) = (?:l\(0\) = )?pols_if_init\(\)"
                   r"|opens at zero even for an in-force"
                   r"|[Zz]ero at ``t = 0`` for an in-force"
                   r"|All three ``CashValue_SE`` timings coincide")


def test_the_docstrings_describe_the_valuation_clock(sec_model):
    """The docstrings say what this model is, and none says what only UL_US_S is.

    Whitespace is collapsed first, as ``test_model_conventions`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock, the SEC table and the product.  The
    symbol map in the Projection docstring maps every cell running in force adds or gives
    a new meaning, and names nothing the model lacks: every name in it is a cell, or a
    Reference the notes give a symbol to, as the declared and guaranteed rates are in
    ``UL_US_S``'s map.  And no docstring says what :data:`STALE` matches.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE,
                   "current-assumption universal life"):
        assert phrase in flat["model"], phrase
    mapped = _mapped_cells(sec_model.Projection.doc)
    missing = [cells for cells in NEW_CELLS if cells not in mapped]
    assert not missing, f"the symbol map does not map {missing}"
    known = set(sec_model.Projection.cells) | set(sec_model.Projection.refs)
    unknown = sorted(mapped - known)
    assert not unknown, f"the symbol map names what the model lacks: {unknown}"
    stale = sorted(where for where, doc in flat.items() if STALE.search(doc))
    assert not stale, f"docstrings that describe UL_US_S: {stale}"


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


def test_the_core_grid_reaches_every_branch(spliced, splice_records):
    """What the default run's T2 and T3 cases reach, which the full grid only multiplies.

    The default run thins the splice to a core (the module docstring), and this test is
    what keeps the thinning from costing a branch.  First, statically, over S's table with
    the variants, each property below holds of some core case: each death benefit option,
    each premium pattern, withdrawals on either option, a loan, each sex, each of the six
    classes, each surrender charge schedule and none, each issue age, S's in-force row as
    its twin and restated, and each kind of valuation month, on the policy clock: mid-year,
    the month before an anniversary, on an anniversary, the surrender charge's first month
    at zero, inside the shock year that follows and in its last month, in shortfall, and
    the last covered month.  And of some core future case: issued off the valuation
    anniversaries and on them, more than a year on, with withdrawals, a single premium, a
    TARGET premium and no surrender charge.  UL premiums are monthly, the one mode the
    product models (S's symbol map: ``premium_mode (not modelled)``), so no mode is asked
    for.

    Then, on the splice's model, of some core row, each of :data:`AT_VALUATION` and
    :data:`IN_FRAME`, what no column of the table shows:

    * every opening-state column is in use, and the face in force below the face at issue;
    * each read of the state at ``t = 0`` changes a number: the guideline premium cap on
      ``cum_prem_init``, the year's allowance reduced by the usage taken, a face cut in the
      valuation month, the MEC latch holding alone, the 7-pay test failing in the valuation
      month from a latch that is off, and the shortfall;
    * survivors are carried into ``t = proj_len()``;
    * later in the frame, the death benefit floor, the corridor binding on Option A and on
      Option B, the lapse shock, the lapse rate's cap binding, charges ceased in cover, a
      failed guideline premium test and a TARGET premium cut to 0 by its cap.

    Each core row's branches were recorded by the T2 case that compared it
    (:func:`_settle`), and a row no case has recorded is evaluated here.
    """
    s = spliced[0]
    s_table = _s_table_with_variants()
    schedules = _surr_charges_with_ul7(pd.read_csv(
        model_path(TWIN).parent / "surr_charge_table.csv")).set_index("surr_charge_id")
    classes = pd.read_csv(model_path(TWIN).parent / "class_factor_table.csv")["rate_class"]

    def at(p, column):
        return s_table.at[p, column]

    def month(p, d):
        return int(at(p, "duration_mth")) + d

    def frame(p):
        return 12 * (s.Projection.omega_age - int(at(p, "age_at_entry")) + 1)

    def runoff(p):
        if not at(p, "has_surr_charge"):
            return None
        return int(schedules.at[at(p, "surr_charge_id"), "runoff_years"])

    def shock(p, d, first, last):
        r = runoff(p)
        return r is not None and 12 * r + first <= month(p, d) <= 12 * r + last

    splices = {
        **{f"Option {o}": (lambda k, p, d, o=o: at(p, "db_option") == o) for o in "AB"},
        **{f"{pattern} premiums": (lambda k, p, d, x=pattern: at(p, "premium_type") == x)
           for pattern in ("LEVEL", "SINGLE", "TARGET")},
        **{f"withdrawals on Option {o}": (
            lambda k, p, d, o=o: at(p, "wd_pp") > 0.0 and at(p, "db_option") == o)
           for o in "AB"},
        "a loan": lambda k, p, d: at(p, "loan_bal_init") > 0.0,
        **{f"sex {x}": (lambda k, p, d, x=x: at(p, "sex") == x) for x in "MF"},
        **{f"class {c}": (lambda k, p, d, c=c: at(p, "rate_class") == c) for c in classes},
        **{f"schedule {i}": (
            lambda k, p, d, i=i: at(p, "has_surr_charge") and at(p, "surr_charge_id") == i)
           for i in schedules.index},
        "no surrender charge": lambda k, p, d: not at(p, "has_surr_charge"),
        **{f"issue age {a}": (lambda k, p, d, a=a: at(p, "age_at_entry") == a)
           for a in (35, YOUNGEST)},
        "S's in-force row as its twin": lambda k, p, d: (k, p) == ("twin", IN_FORCE),
        "S's in-force row restated": lambda k, p, d: (k, p) == ("derived", IN_FORCE),
        "mid-year": lambda k, p, d: month(p, d) % 12 not in (0, 11),
        "the month before an anniversary": lambda k, p, d: month(p, d) % 12 == 11,
        "on an anniversary": lambda k, p, d: month(p, d) > 0 and month(p, d) % 12 == 0,
        "the surrender charge's first month at zero": lambda k, p, d: shock(p, d, -1, -1),
        "inside the shock year": lambda k, p, d: shock(p, d, 0, 10),
        "the shock year's last month": lambda k, p, d: shock(p, d, 11, 11),
        "in shortfall": lambda k, p, d: _point(s, p).is_shortfall(d),
        "the last covered month": lambda k, p, d: month(p, d) == frame(p) - 1,
    }
    futures = {
        "issued off the anniversaries": lambda p, k: k % 12 != 0,
        "issued on them": lambda p, k: k % 12 == 0,
        "issued more than a year on": lambda p, k: k > 12,
        "withdrawals": lambda p, k: at(p, "wd_pp") > 0.0,
        "a single premium": lambda p, k: at(p, "premium_type") == "SINGLE",
        "a TARGET premium": lambda p, k: at(p, "premium_type") == "TARGET",
        "no surrender charge": lambda p, k: not at(p, "has_surr_charge"),
    }
    missing = [what for what, holds in splices.items()
               if not any(holds(*case) for case in CORE_SPLICES)]
    missing += [what for what, holds in futures.items()
                if not any(holds(*case) for case in CORE_FUTURES)]
    assert not missing, f"no core case reaches: {missing}"

    reached, raised = set(), []
    for case in CORE_SPLICES:
        record = _record_of(spliced, splice_records, case)
        reached |= record["branches"]
        if record["raised"]:
            raised.append(f"{_case_id(*case)}: {record['raised']}")
    assert not raised, raised
    missing = [what for what in (*AT_VALUATION, *IN_FRAME) if what not in reached]
    assert not missing, f"no core row reaches: {missing}"


def test_the_points_sum_row_by_row_into_a_block(spliced):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    S point 2's twin, the point restated at month 12 and the point issued 12 months on,
    summed as ``run_sec.py --block`` sums them, are indexed 0..1043 and equal S's frame
    added to itself moved 12 months earlier and 12 months later.  A model whose frames sat
    on the policy clock would fail it.
    """
    s, sec = spliced
    keys = [_row_key(sec, *case)
            for case in (("twin", 2, 0), ("derived", 2, 12), ("future", 2, -12))]
    try:
        frames = [projection(sec, key).result_cf() for key in keys]
    finally:
        for key in keys:
            _release(sec, key)
    block = pd.concat(frames).groupby(level="t").sum()
    sdf = _point(s, 2).result_cf()
    expected = pd.concat([sdf, sdf.set_axis(sdf.index - 12).loc[0:],
                          sdf.set_axis(sdf.index + 12)]).groupby(level=0).sum()
    assert list(block.index) == list(range(1044))
    assert frame_mismatches(expected, block) == []


def _standing(p):
    """What ``run_sec.py`` says of point ``p`` at the valuation date, stated here."""
    d = p.duration_mth_init()
    if d < 0:
        return f"to be issued at t = {-d}, {-d} months after the valuation date"
    if d == 0:
        return "issued at the valuation date, t = 0"
    return (f"in force {d} months: policy year {p.policy_year(0)}, attained age "
            f"{p.age(0)}, {p.pols_if(0):.6f} in force, account value "
            f"{p.av_pp_init():,.2f}, loan {p.loan_bal_init():,.2f}")


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
    the labels it has.  Its refusals name the label too: ``Data``'s of a malformed row, and
    ``proj_len()``'s of a point past the end of the projection, which ``run_sec.py
    --block`` meets before it projects any point.  On every shipped row ``source_mth``
    equals ``duration_mth`` but on S's in-force point, so a formula that read the one for
    the other would pass every test that leaves ``duration_mth`` as generated.
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
        "model point 106: UL-000003-M6 - M35 StdNT face 100,000 option A GPT, LEVEL "
        "premium 1,800.00/yr",
        f"at the valuation date: {_standing(_row(sec_model, 'derived', IN_FORCE, 6))}"]
    done = _run_sec(runner, "6", check=False)
    assert done.returncode == 1 and done.stdout == b""
    assert (f"no model point 6 in the table: {list(range(109, 100, -1))}"
            in done.stderr.decode(errors="replace"))
    model = mx.read_model(_sec_inputs(tmp_path / "mec", _set("is_mec_init", [104], 2)(
        extract)), name=_name("mec"))
    try:
        _refused(model.Data.model_point_table,
                 "is_mec_init must be 0 or 1, an int code; it is not at point_id [104]")
    finally:
        model.close()
    moved = _sec_inputs(tmp_path / "moved", _set("duration_mth", [105], 1032)(extract))
    message = ("point_id 105: duration_mth 1032 is at or past the end of the projection, "
               "policy month 1032, attained age 121")
    model = mx.read_model(moved, name=_name("moved"))
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
    the model's.  The worked example's point, the runner's default, with its lines at the
    valuation date, each asserted whole, so that a longer number cannot pass for the one
    asserted, and its first twelve rows of cash flows, of the account value roll-forward
    and of counts; the first two are ``run.py``'s, ``UL_US_S``'s runner, row for row, since
    the point is S's point 1.  Point 6, restated in force at S's month 6 on S's in-force
    point, and point 9, to be issued 25 months on, each with the two lines that say where
    its row came from and where it stands, which only the committed table's generator
    columns can say.  And the block: a line for each of the nine points, in table order,
    its first twelve rows, which must be the committed points' frames summed row by row, as
    this test sums them, and those frames summed into projection years, each year's count
    the one in force in its first month.  Nothing else runs the runner on the committed
    table.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    out = _run_sec(runner)
    assert out.splitlines()[:3] == [
        "model point 1: UL-000001 (S's UL-000001) - M35 StdNT face 100,000 option A GPT, "
        "LEVEL premium 1,800.00/yr",
        "at the valuation date: issued at the valuation date, t = 0",
        "proj_len = 1032 months from the valuation date (t = 0..1031); the projection ends "
        "at policy month 1032, attained age 121"]
    anchor, s_anchor = _row(sec_model, "twin", 1, 0), _point(s_model, 1)
    for report in REPORTS:
        assert anchor.cells[report]().head(12).round(
            6 if report == "result_pols" else 2).to_string() in out, report
    for report in ("result_cf", "result_av"):
        assert s_anchor.cells[report]().head(12).round(2).to_string() in out, report
    for point, kind, s_point, month, origin in (
            ("6", "derived", IN_FORCE, 6, "UL-000003-M6 (S's UL-000003 at its month 6)"),
            ("9", "future", 1, -25, "UL-000001-F25 (S's UL-000001, issued 25 months on)")):
        p = _row(sec_model, kind, s_point, month)
        assert _run_sec(runner, point).splitlines()[:2] == [
            f"model point {point}: {origin} - M35 StdNT face 100,000 option A GPT, LEVEL "
            f"premium 1,800.00/yr",
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


# run_sec.py run as though it sat at /m/products/universal_life, a copy too shallow to have
# a repository above it: the source compiled under that name, so that its own __file__ is
# it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/universal_life/run_sec.py"
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


def test_the_sample_raises_the_recursion_limit_its_comment_derives():
    """``sample_sec.py`` sets the recursion limit its comment derives, before the import.

    The export does not raise the recursion limit as modelx does (F7), so the sample sets
    it, and its comment records the measured need: a cold ``net_cf`` in the last month of
    the longest frame, issue age 18 issued 120 months on, needs a limit of 2,530 in the
    export, and the reports the sample runs in ascending ``t``, the export's import among
    the frames they run under, 130.  The limit is four times the first, rounded up to the
    thousand.  No build can tell a lower limit: the reports alone need 130, so a limit of
    1,000 builds the same model.  So this holds the limit,
    read from the sample's code, to the value derived from its comment's need, and holds
    the call before the import of the export.  A change to the need is measured again and
    written in the comment.
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


def _references(space):
    """The References a space's ``__init__.py`` assigns, a name to a literal value."""
    source = (model_path(SEC) / space / "__init__.py").read_text(encoding="utf-8")
    return {node.targets[0].id: node.value.value for node in ast.parse(source).body
            if isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Constant)}


def test_the_spec_sizes_each_cache_as_its_comment_derives():
    """``spec_sec.py`` gives each cache the size its comment derives from the contract.

    The spec check, C3, holds the compiled caches to the spec, and C4 at the contract's
    extremes holds the spec to the largest argument a projection reads; neither sees a
    size one below the comment's, which drops the headroom and reads the same numbers.
    So this reads the spec as mx2cy does, and the four bounds of the contract from the
    model's own References, and holds each size to the comment's derivation from them:
    ``t`` to ``12 * (omega_age - issue_age_min + 1) + the horizon + 2``, ``y`` to
    ``omega_age - issue_age_min + 3`` and ``a`` to ``omega_age + 2``, and the timing and
    kind caches to ``t`` by one inner width, the timings' count, which the kinds fit in
    (§7.2, *For M16 and later*).  A change to a bound or a size is derived again in the
    comment and here.
    """
    source = (model_path(SEC).parent / "spec_sec.py").read_text(encoding="utf-8")
    comment = " ".join(line.lstrip("# ") for line in source.splitlines()
                       if line.startswith("#"))
    for formula in ("needs t raised to 12 * (omega_age - issue_age_min + 1) + the "
                    "horizon + 2", "needs y raised to omega_age - issue_age_min + 3",
                    "needs a raised to omega_age + 2"):
        assert formula in comment, formula
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    proj, data = _references("Projection"), _references("Data")
    low, omega, horizon = proj["issue_age_min"], proj["omega_age"], data[
        "future_horizon_mth"]
    timings = [proj[code] for code in ("BEF_NB", "BEF_DECR", "BEF_MAT", "BEF_PREM",
                                       "BEF_WD", "BEF_FEE", "BEF_INV", "EOM")]
    kinds = [proj[code] for code in ("DEATH", "LAPSE", "MATURITY")]
    assert sorted(timings) == list(range(len(timings))), timings
    assert sorted(kinds) == list(range(len(kinds))), kinds
    t = 12 * (omega - low + 1) + horizon + 2
    width = len(timings)
    assert len(kinds) <= width
    assert sizes == {"t": t, ("t", "timing"): (t, width), ("t", "kind"): (t, width),
                     "y": omega - low + 3, "a": omega + 2}, sizes


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
    exactly.  ``python tools/gen_sec_fingerprint.py UL_US_SEC --check`` runs the same
    comparison from the command line.
    """
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# UL_US_SEC's fingerprint, frozen at M13 from the model as Phase 1 left it and committed
# alone, before Phase 2 changed anything.  Each point is keyed by its point_id; each column
# holds (its sum over the frame, its largest absolute value, (its values at the months)).
# The block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a
# refreeze goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: UL_US_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 1032, "months": (0, 257, 515, 773, 1031),
        "result_cf": {
            "pols_if": (261.8489048739566, 1.0, (
                1.0, 0.4199523867277358, 0.17161219976202097, 0.015611231510741204, 0.0)),
            "premiums": (30915.58238352191, 150.0, (
                150.0, 44.09500060641226, 18.0192809750122, 1.6391793086278263, 0.0)),
            "claims_death": (26866.573593044726, 73.04636364226944, (
                6.06035295860341, 13.128563968236914, 34.76437238636103, 55.742782120545904,
                0.0)),
            "claims_lapse": (22995.039251480423, 55.20206318762075, (
                0.0, 33.57914421900876, 38.44168544693173, 8.642155836487175, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2767.4536237911243, 6.25, (
                6.25, 4.408402544731493, 3.0257324435488417, 0.47385401705933394, 0.0)),
            "premium_taxes": (772.8895595880477, 3.75, (
                3.75, 1.1023750151603067, 0.45048202437530505, 0.04097948271569566, 0.0)),
            "net_cf": (-22486.37364438241, 133.9396470413966, (
                133.9396470413966, -8.123485140725208, -58.662991326204704,
                -63.26059214818028, 0.0)),
        },
        "result_pols": {
            "pols_if": (261.8489048739566, 1.0, (
                1.0, 0.4199523867277358, 0.17161219976202097, 0.015611231510741204, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.19752955859025143, 0.00046272042608115773, (
                6.06035295860341e-05, 0.00013128563968236914, 0.00034764372386361035,
                0.0002494449741213684, 0.0)),
            "pols_lapse": (0.8024704414097493, 0.005142701147092632, (
                0.005142701147092632, 0.001064266900372662, 0.00043416397538388656,
                3.8942875665713206e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.43639611546768, 1.0, (
                6.06035295860341e-05, 0.00031262029656586865, 0.0020257518075387226,
                0.01597855838277329, 1.0)),
            "lapse_rate_mth": (2.7932253753803304, 0.006924382628299419, (
                0.005143012831822946, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    2: {"rows": 1032, "months": (0, 257, 515, 773, 1031),
        "result_cf": {
            "pols_if": (261.8489048739566, 1.0, (
                1.0, 0.4199523867277358, 0.17161219976202097, 0.015611231510741204, 0.0)),
            "premiums": (30915.58238352191, 150.0, (
                150.0, 44.09500060641226, 18.0192809750122, 1.6391793086278263, 0.0)),
            "claims_death": (26080.639665776773, 67.89370191353584, (
                6.0688980562750405, 17.142350218208524, 55.96088430349206,
                24.94449741213684, 0.0)),
            "claims_lapse": (16679.77240645144, 54.84699918028075, (
                0.0, 32.58356054217763, 26.4330094262392, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2767.4536237911243, 6.25, (
                6.25, 4.408402544731493, 3.0257324435488417, 0.47385401705933394, 0.0)),
            "premium_taxes": (772.8895595880477, 3.75, (
                3.75, 1.1023750151603067, 0.45048202437530505, 0.04097948271569566, 0.0)),
            "net_cf": (-15385.17287208548, 133.93110194372497, (
                133.93110194372497, -11.141687713865695, -67.85082722264322,
                -23.820151603284042, 0.0)),
        },
        "result_pols": {
            "pols_if": (261.8489048739566, 1.0, (
                1.0, 0.4199523867277358, 0.17161219976202097, 0.015611231510741204, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.19752955859025143, 0.00046272042608115773, (
                6.06035295860341e-05, 0.00013128563968236914, 0.00034764372386361035,
                0.0002494449741213684, 0.0)),
            "pols_lapse": (0.8024704414097493, 0.005142701147092632, (
                0.005142701147092632, 0.001064266900372662, 0.00043416397538388656,
                3.8942875665713206e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.43639611546768, 1.0, (
                6.06035295860341e-05, 0.00031262029656586865, 0.0020257518075387226,
                0.01597855838277329, 1.0)),
            "lapse_rate_mth": (2.7932253753803304, 0.006924382628299419, (
                0.005143012831822946, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    3: {"rows": 912, "months": (0, 227, 455, 683, 911),
        "result_cf": {
            "pols_if": (272.3730943270291, 1.0, (
                1.0, 0.525750482909782, 0.20545279417882928, 0.013749192783173249, 0.0)),
            "premiums": (29109.438494877577, 120.0, (
                120.0, 55.20380070552711, 21.572543388777074, 1.443665242233191, 0.0)),
            "claims_death": (42251.66696275481, 119.70740112656743, (
                12.307497561934833, 29.2750482846668, 77.21526898211243, 66.23677557154491,
                0.0)),
            "claims_lapse": (34121.06469981956, 65.17567386403877, (
                33.256355605911324, 62.54592354811801, 58.0972350483602, 8.370426942516644,
                0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2691.503708983327, 6.25, (
                6.25, 5.124945775054033, 3.2016591061984045, 0.3425261086801733, 0.0)),
            "premium_taxes": (727.7359623719394, 3.0, (
                3.0, 1.3800950176381779, 0.5393135847194269, 0.03609163105582978, 0.0)),
            "net_cf": (-50682.53283905206, 150.57902136656023, (
                65.18614683215384, -43.122211919949905, -117.48093333261339,
                -73.54215501156436, 0.0)),
        },
        "result_pols": {
            "pols_if": (272.3730943270291, 1.0, (
                1.0, 0.525750482909782, 0.20545279417882928, 0.013749192783173249, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.3103076096555758, 0.0007572063032210974, (
                0.00012558670981566156, 0.0003028699861031033, 0.0006574255781048947,
                0.00026844029246073065, 0.0)),
            "pols_lapse": (0.6896923903444242, 0.0025347302454220536, (
                0.0025347302454220536, 0.0013320352427859687, 0.0005191662152914399,
                3.4174362915056244e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.426188133861935, 1.0, (
                0.00012558670981566156, 0.0005760717221349188, 0.0031998862840125764,
                0.019524076554461978, 1.0)),
            "lapse_rate_mth": (2.3119643358190594, 0.002535048613836688, (
                0.002535048613836688, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    4: {"rows": 1020, "months": (0, 254, 509, 764, 1019),
        "result_cf": {
            "pols_if": (250.1864357758114, 0.9393166200000005, (
                0.9393166200000005, 0.4092910531738536, 0.16681288181089216,
                0.014761951800716593, 0.0)),
            "premiums": (29166.212018800124, 138.07954314000008, (
                138.07954314000008, 42.97556058325463, 17.515352590143678,
                1.5500049390752422, 0.0)),
            "claims_death": (26795.894913941156, 73.04636364226944, (
                6.084242169341483, 13.948833704575208, 37.01519386946166, 53.25713214086886,
                0.0)),
            "claims_lapse": (22989.69616158522, 55.20206318762075, (
                2.224625244594611, 34.19550059821271, 38.214560549242364, 8.25679866364436,
                0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2628.8421384660655, 5.870728875000003, (
                5.870728875000003, 4.296486405058173, 2.9411146130462664,
                0.43714681649541903, 0.0)),
            "premium_taxes": (729.1553004700031, 3.451988578500002, (
                3.451988578500002, 1.0743890145813657, 0.43788381475359195,
                0.03875012347688106, 0.0)),
            "net_cf": (-23977.37649566232, 120.44795827256398, (
                120.44795827256398, -10.539649139172829, -61.09340025636021,
                -60.43982280541028, 0.0)),
        },
        "result_pols": {
            "pols_if": (250.1864357758114, 0.9393166200000005, (
                0.9393166200000005, 0.4092910531738536, 0.16681288181089216,
                0.014761951800716593, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.19682277179921578, 0.00046272042608115773, (
                6.0842421693414824e-05, 0.00013948833704575207, 0.00037015193869461665,
                0.00023587470869143535, 0.0)),
            "pols_lapse": (0.7424938482007856, 0.00460524379384535, (
                0.004006225305037078, 0.0010372191072886615, 0.00042194041164570867,
                3.682431159662324e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.435668873112654, 1.0, (
                6.477307054719716e-05, 0.0003408047548659754, 0.002218964954482594,
                0.01597855838277329, 1.0)),
            "lapse_rate_mth": (2.731509221398455, 0.006924382628299419, (
                0.004265318777560645, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    5: {"rows": 919, "months": (0, 229, 459, 688, 918),
        "result_cf": {
            "pols_if": (170.84486142591246, 0.6420685009867007, (
                0.6420685009867007, 0.32632263007939605, 0.1277318883245529,
                0.00878440794067361, 0.0)),
            "premiums": (18329.73888555292, 78.97442562136418, (
                78.97442562136418, 34.263876158336586, 13.411848274078055,
                0.922362833770729, 0.0)),
            "claims_death": (26127.29078033657, 73.04636364226944, (
                7.4581080720002335, 18.798523948143373, 47.10992026496807,
                42.17034601536912, 0.0)),
            "claims_lapse": (21232.67656400992, 55.20206318762075, (
                54.577183568467184, 38.167221590554945, 35.53175944814965,
                5.331307232325219, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1695.9762338936816, 4.012928131166879, (
                4.012928131166879, 3.26047333223719, 2.0402633810203583, 0.2243121719463447,
                0.0)),
            "premium_taxes": (458.2434721388231, 1.9743606405341045, (
                1.9743606405341045, 0.8565969039584147, 0.3352962068519514,
                0.023059070844268226, 0.0)),
            "net_cf": (-31184.44816482607, 91.73753545828501, (
                10.951845209195772, -26.818939616557333, -71.60539102691197,
                -46.82666165671422, 0.0)),
        },
        "result_pols": {
            "pols_if": (170.84486142591246, 0.6420685009867007, (
                0.6420685009867007, 0.32632263007939605, 0.1277318883245529,
                0.00878440794067361, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.19013673046316992, 0.00046272042608115773, (
                7.458108072000233e-05, 0.00018798523948143373, 0.00040872751748076294,
                0.00017150745311933524, 0.0)),
            "pols_lapse": (0.45193177052353156, 0.0044454115464708215, (
                0.0044454115464708215, 0.000826767179325546, 0.00032277040231327395,
                2.1834121442087795e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.42700123645807, 1.0, (
                0.00011615751373161842, 0.0005760717221349188, 0.0031998862840125764,
                0.019524076554461978, 1.0)),
            "lapse_rate_mth": (2.3604350142171553, 0.006924382628299419, (
                0.006924382628299419, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    6: {"rows": 906, "months": (0, 226, 452, 678, 905),
        "result_cf": {
            "pols_if": (266.41285781774855, 0.9841438817571342, (
                0.9841438817571342, 0.517516117021537, 0.20181827403923053,
                0.01344657812779746, 0.0)),
            "premiums": (28394.210113763915, 118.0972658108561, (
                118.0972658108561, 54.33919228726138, 21.190918774119204,
                1.4118907034187334, 0.0)),
            "claims_death": (42178.3198362329, 119.70740112656743, (
                12.108972603408656, 31.4730003158507, 84.07707264075458, 71.9695165598717,
                0.0)),
            "claims_lapse": (33918.284573404184, 65.17567386403877, (
                34.550665337579986, 62.8151396280737, 57.68130921305066, 8.19604797251308,
                0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2621.908175278496, 6.150899260982088, (
                6.150899260982088, 5.044678271664118, 3.145020818322508, 0.3349872355281207,
                0.0)),
            "premium_taxes": (709.8552528440981, 2.952431645271403, (
                2.952431645271403, 1.3584798071815347, 0.5297729693529801,
                0.035297267585468334, 0.0)),
            "net_cf": (-51034.15772399576, 150.52761844554865, (
                62.334296963613966, -46.35210573550867, -124.24225686736152,
                -79.12395833207964, 0.0)),
        },
        "result_pols": {
            "pols_if": (266.41285781774855, 0.9841438817571342, (
                0.9841438817571342, 0.517516117021537, 0.20181827403923053,
                0.01344657812779746, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.3095590831626521, 0.0007572063032210974, (
                0.00012359539209509196, 0.00032573727026923753, 0.0007080270579230947,
                0.0002906968560545895, 0.0)),
            "pols_lapse": (0.6745847985944821, 0.0024945392629368733, (
                0.0024945392629368733, 0.0013111027552781217, 0.0005098242528383174,
                3.335079858173181e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.425434613603045, 1.0, (
                0.00012558670981566156, 0.0006294243977249536, 0.0035082405758036783,
                0.021618649242341137, 1.0)),
            "lapse_rate_mth": (2.2967540441360392, 0.002535048613836688, (
                0.002535048613836688, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    7: {"rows": 356, "months": (0, 88, 177, 266, 355),
        "result_cf": {
            "pols_if": (4.026042299609751, 0.05830987033439344, (
                0.05830987033439344, 0.018351291937034605, 0.002034770067939675,
                1.5956825588686453e-05, 0.0)),
            "premiums": (422.7344414590239, 6.122536385111312, (
                6.122536385111312, 1.9268856533886336, 0.21365085713366588,
                0.0016754666868120775, 0.0)),
            "claims_death": (4822.766890173694, 43.725577137919274, (
                43.25402603659622, 26.56523528785448, 6.717195455154589,
                0.12546115617301087, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (27.852201473732695, 0.364436689589959, (
                0.364436689589959, 0.13633699554349604, 0.017969230235623572,
                0.00017169259081035475, 0.0)),
            "premium_taxes": (10.568361036475599, 0.1530634096277828, (
                0.1530634096277828, 0.04817214133471584, 0.005341271428341648,
                4.188666717030194e-05, 0.0)),
            "net_cf": (-4438.4530112248785, 38.54955258835948, (
                -37.648989750702654, -24.82285877134406, -6.526855099684888,
                -0.12399926874417945, 0.0)),
        },
        "result_pols": {
            "pols_if": (4.026042299609751, 0.05830987033439344, (
                0.05830987033439344, 0.018351291937034605, 0.002034770067939675,
                1.5956825588686453e-05, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.048225912415940896, 0.0004372557713791927, (
                0.0004307837745699173, 0.0002656523528785448, 6.717195455154589e-05,
                1.2546115617301089e-06, 0.0)),
            "pols_lapse": (0.010083957918452532, 0.0001467262981536143, (
                0.0001467262981536143, 4.584797555816475e-05, 4.987956869932259e-06,
                3.727082728936599e-08, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (41.48971294550492, 1.0, (
                0.00738783626338857, 0.01447594827601395, 0.033012061465776066,
                0.0786253854037009, 1.0)),
            "lapse_rate_mth": (0.9024773065258609, 0.002535048613836688, (
                0.002535048613836688, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    8: {"rows": 24, "months": (0, 5, 11, 17, 23),
        "result_cf": {
            "pols_if": (1.7653195878159383e-10, 1.7653195878159383e-10, (
                1.7653195878159383e-10, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (1.853585567206735e-08, 1.853585567206735e-08, (
                1.853585567206735e-08, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (8.341958705721902e-05, 8.341958705721902e-05, (
                8.341958705721902e-05, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1.1033247423849614e-09, 1.1033247423849614e-09, (
                1.1033247423849614e-09, 0.0, 0.0, 0.0, 0.0)),
            "premium_taxes": (4.633963918016838e-10, 4.633963918016838e-10, (
                4.633963918016838e-10, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-8.340261792268115e-05, 8.340261792268115e-05, (
                -8.340261792268115e-05, 0.0, 0.0, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (1.7653195878159383e-10, 1.7653195878159383e-10, (
                1.7653195878159383e-10, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (1.7653195878159383e-10, 1.7653195878159383e-10, (
                1.7653195878159383e-10, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (24.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lapse_rate_mth": (0.06084116673208051, 0.002535048613836688, (
                0.002535048613836688, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    9: {"rows": 1057, "months": (0, 264, 528, 792, 1056),
        "result_cf": {
            "pols_if": (261.8489048739566, 1.0, (
                0.0, 0.44190720497733604, 0.1812457366906935, 0.01743256369987107, 0.0)),
            "premiums": (30915.582383521916, 150.0, (
                0.0, 46.40025652262028, 19.030802352522816, 1.8304191884864622, 0.0)),
            "claims_death": (26866.573593044723, 73.04636364226944, (
                0.0, 11.642698168009336, 33.525062827118546, 55.238080729618325, 0.0)),
            "claims_lapse": (22995.039251480426, 55.20206318762075, (
                0.0, 32.2666482326831, 38.82776420084951, 9.46736378682136, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2913.4716844086925, 6.566406249999999, (
                0.0, 4.754842527959663, 3.357359864496931, 0.5559252422947653, 0.0)),
            "premium_taxes": (772.8895595880479, 3.75, (
                0.0, 1.160006413065507, 0.47577005881307044, 0.04576047971216156, 0.0)),
            "net_cf": (-22632.39170499998, 133.6232407913966, (
                0.0, -3.42393881909733, -57.155154598755246, -63.47671104996015, 0.0)),
        },
        "result_pols": {
            "pols_if": (261.8489048739566, 1.0, (
                0.0, 0.44190720497733604, 0.1812457366906935, 0.01743256369987107, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.19752955859025143, 0.00046272042608115773, (
                0.0, 0.00011642698168009336, 0.00033525062827118545, 0.00025235289043765196,
                0.0)),
            "pols_lapse": (0.8024704414097493, 0.005142701147092632, (
                0.0, 0.0011199610993637196, 0.0004586168769210651, 4.3552669597876264e-05,
                0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (42.43639611546768, 1.0, (
                0.0, 0.0002634647735287876, 0.001849702146888621, 0.01447594827601395,
                1.0)),
            "lapse_rate_mth": (2.7932253753803304, 0.006924382628299419, (
                0.0, 0.002535048613836688, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688)),
        },
    },
}
# END generated fingerprint: UL_US_SEC


# ---------------------------------------------------------------------------
# Compiled (USLIB-SEC-PLAN.md Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython CI job, which sets USLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is UL's
# own: the comparison on the splice grid, at the contract's extremes and where the cap on
# mortality binds, the refusals, the deepest call, a Reference set late and the runner.
# None asks for sec_read, sec_model or s_model, which sweep every committed point; the grid
# test alone asks for spliced.


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)


# How many rows of the splice grid C4 compares at once.  compiled_mismatches sweeps every
# row of its case in one modelx read, and keeps every value of every row, in the parent and
# in the child, until it compares them.  A UL row runs up to 1,236 months, against
# WholeLife's 660, and twenty of them peaked at 3.64 GB in the comparison alone, ten at
# 2.17 GB, for 162 s against 157 on the full grid (measured at M16), so UL compares ten
# rows at a time, near the module's own peak, for one modelx read and one child more a
# chunk (USLIB-SEC-PLAN.md §7.2, *For M16 and later*, item 7).
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
    and the variants, withdrawals on either option, a single premium without a surrender
    charge, TARGET on the second schedule, over-funding past the 7-pay and guideline
    tests, the youngest issue age and Option B's corridor, under the splice's References,
    with charges ceasing in cover and the lapse rate's cap binding (:data:`SPLICED_REFS`),
    on the splice's COI and surrender-charge copies (:data:`SPLICED_EDITS`).  The grid is
    the one this run's ``spliced`` selects, the core by default and the full grid under
    ``USLIB_SEC_FULL=1``, and the test carries no ``sec_full`` mark, since a skipped
    compile test fails the cython job.  The grid's SEC table goes beside the build
    :data:`C4_CHUNK` rows at a time; modelx sweeps every row fully, and the compiled model
    must agree at every argument modelx caches, identically on x86-64 and to 1e-12
    relative elsewhere, with every raise and every ``Data`` array
    (``sec_support.compiled_mismatches``).
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
        found += compiled_mismatches(build, folder, refs=SPLICED_REFS)
        shutil.rmtree(tmp_path / f"grid{i}")
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


# The COI keys the contract's extremes read beyond the splice's, each with its own rows,
# geometric in the policy year from a base of its own at a ratio of its own, every policy
# year its cover reaches, as (sex, rate_class, age_at_entry, base, ratio).
EXTREME_COI = ((("F", "PNT", 18), 0.061, 1.071), (("M", "PTob", 18), 0.093, 1.077),
               (("M", "StdPlusNT", 18), 0.074, 1.073), (("M", "StdTob", 85), 3.1, 1.09),
               (("M", "StdNT", 120), 41.0, 1.0))


def _coi_extremes(rates):
    """:func:`_coi_unsorted`'s copy with :data:`EXTREME_COI`'s keys, in reverse order."""
    rates = _coi_unsorted(rates)
    added = [pd.DataFrame({"sex": sex, "rate_class": rate_class, "age_at_entry": age,
                           "policy_year": range(1, 122 - age),
                           "coi_rate_guar": [round(base * ratio ** (y - 1), 6)
                                             for y in range(1, 122 - age)],
                           "provenance": "test copy"})
             for (sex, rate_class, age), base, ratio in EXTREME_COI]
    rates = pd.concat([rates, *added]).sort_values(COI_KEYS, ignore_index=True)
    return rates.iloc[::-1].reset_index(drop=True)


def _surr_charges_extremes(table):
    """The splice's schedules, UL7 among them, and UL0, run off over 0 years, which only
    a point without a charge names."""
    ul0 = pd.DataFrame([{"surr_charge_id": "UL0", "sc_per_1000_init": 5.0,
                         "runoff_years": 0, "provenance": "test copy"}])
    return pd.concat([_surr_charges_with_ul7(table), ul0], ignore_index=True)


# The frames of the contract's extremes, in _contract_extremes' order, and the COI
# schedule each reads, its keys' place among the copy's fourteen.
EXTREME_FRAMES = [1356, 1236, 1356, 1236, 552, 1, 12, 1032, 1032]
EXTREME_SCHEDULES = [8, 1, 6, 11, 14, 8, 10, 9, 9]


def _contract_extremes():
    """Inputs for the contract's longest frames, its oldest issue age and the bounds of its
    values: a table and edits.

    Nine points made from the committed twins.  Four are issued at 18, the youngest age
    the contract issues at (:data:`YOUNGEST`), so cover runs 1,236 months, 103 policy
    years, the longest: the worked example issued 120 months on, the shipped
    ``future_horizon_mth``, a frame of 1,356 months, the longest the contract allows,
    which reads every cache as far as ``spec_sec.py`` sizes it, ``t`` to 1,356 in C4's
    sweep of the month after it, the policy year to 103 and the attained age to 120;
    Option B, F PNT, issued now; TARGET at $6,000 a year on UL7, M PTob, issued 120 months
    on; and a single premium of $50,000 without a charge, withdrawing $60 a month, M
    StdPlusNT, issued now.  Then StdTob issued at 85 and 120 months on, where the annual
    mortality passes 1 at attained age 113 and is capped; the worked example at 18 in
    force in its last covered month, a frame of one row; and Option B at 120, the oldest
    issue age, a frame of twelve months.  And at the bounds of the values: the worked
    example at a load of 1, whose cure payment divides by zero, and S's point 2 without a
    charge on UL0, a schedule run off over 0 years, which it never reads.

    The shipped tables stop short of such policies, so the copies extend them
    (:data:`EXTREME_COI`, on :func:`_coi_unsorted`'s copy, in reverse key order), each key
    with rates of its own, so that a read of the key beside the right one, which a padded
    array allows, changes a number the compiled comparison sees.
    """
    committed = _committed()

    def twin(s_point, **columns):
        return committed.loc[[_label(committed, "twin", s_point, 0)]].assign(**columns)

    later, last = -120, 12 * (121 - YOUNGEST) - 1
    rows = pd.concat([
        twin(1, age_at_entry=YOUNGEST, duration_mth=later),
        twin(2, age_at_entry=YOUNGEST, sex="F", rate_class="PNT"),
        twin(1, age_at_entry=YOUNGEST, premium_type="TARGET", premium_pp_ann=6000.0,
             surr_charge_id="UL7", rate_class="PTob", duration_mth=later),
        twin(1, age_at_entry=YOUNGEST, premium_type="SINGLE", premium_pp_ann=50000.0,
             has_surr_charge=False, wd_pp=60.0, rate_class="StdPlusNT"),
        twin(1, age_at_entry=85, rate_class="StdTob", duration_mth=later),
        twin(1, age_at_entry=YOUNGEST, duration_mth=last, policy_count=0.5,
             av_pp_init=50000.0, sum_assured_init=100000.0, cum_prem_init=185400.0),
        twin(2, age_at_entry=120),
        twin(1, load_prem_rate=1.0),
        twin(2, has_surr_charge=False, surr_charge_id="UL0")])
    rows.index = pd.Index(range(1, len(rows) + 1), name="point_id")
    return rows, {"coi_rates.csv": _coi_extremes,
                  "surr_charge_table.csv": _surr_charges_extremes}


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_contract_extremes(
        sec_build, tmp_path):
    """C4 where the caches end: the contract's longest frames, every cell compiled.

    The nine points of :func:`_contract_extremes`, the longest frames the contract allows,
    its oldest issue ages and the bounds of its values, read every cache as far as
    ``spec_sec.py`` sizes it: ``t`` to 1,356, the month after the 1,356-month frame, which
    the roll-forwards read, the policy year to 103 and the attained age to 120.  They run
    under :data:`SWITCHED_ON`, every premium pattern among them, from a COI copy written in
    reverse key order, with a schedule no point reads between two that points read, so
    that the compiled numbering of the schedules is held to modelx's on a file whose order
    is not its keys'.  modelx sweeps each fully, and the compiled model must agree
    everywhere, every raise included: the cure payment's ``ZeroDivisionError`` at a load
    of 1, S's own text, in every month.  A cache one too small for the contract raises
    ``IndexError`` compiled where modelx reads on, and fails here, though the spec check
    passes it, which holds the caches to the spec and not the spec to the contract.
    """
    build = sec_build(SEC)
    rows, edits = _contract_extremes()
    folder = compiled_case(build, tmp_path / "extremes", model_points=rows, edits=edits)
    model = mx.read_model(folder, name=_name("extremes_frames"))
    try:
        frames = [projection(model, key).proj_len() for key in point_keys(model)]
        schedules = list(model.Data.coi_schedule())
    finally:
        model.close()
    assert frames == EXTREME_FRAMES, frames
    assert schedules == EXTREME_SCHEDULES, schedules
    found = compiled_mismatches(build, folder, refs=SWITCHED_ON)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


def _labels_not_text():
    """The labels ``Data`` accepts that are not text, as (case, the table's rows).

    Made from the committed twins of S's points 1 and 2: on a point without a charge, a
    blank ``surr_charge_id``, NaN as pandas reads it, beside a point with one; a blank
    option, test and pattern, which the point's first projection refuses, issued at 120
    for a frame of twelve months, since modelx sweeps a raise in every cell of every
    month, about 17 minutes over the twin's 1,032 (measured at M16); and an id column of
    numbers, ints, on points without a charge.
    """
    committed = _committed()

    def twin(s_point, **columns):
        return committed.loc[[_label(committed, "twin", s_point, 0)]].assign(**columns)

    cases = [
        ("blank", pd.concat([twin(1), twin(2, has_surr_charge=False, surr_charge_id=None),
                             twin(1, age_at_entry=120, db_option=None, qual_test=None,
                                  premium_type=None)])),
        ("numeric", pd.concat([twin(1, has_surr_charge=False, surr_charge_id=0),
                               twin(2, has_surr_charge=False, surr_charge_id=9)]))]
    for _, rows in cases:
        rows.index = pd.Index(range(1, len(rows) + 1), name="point_id")
    return cases


@pytest.mark.cython
def test_the_compiled_model_returns_a_label_that_is_not_text_as_modelx_does(sec_build,
                                                                             tmp_path):
    """C4 on labels that are not text: the compiled accessors return what modelx returns.

    ``Data`` accepts a blank ``surr_charge_id`` on a point without a charge, and an id
    column of numbers, since ``UL_US_S`` never reads such a point's schedule and projects
    it; and it accepts blank options, which the point's first projection refuses.  modelx
    returns each label as pandas reads it, NaN or an int, and an accessor typed ``str``
    would raise ``TypeError`` compiled; the sample types the six as Python objects
    (sample_sec.py).  So on each case of :func:`_labels_not_text`, after checking that
    the file reads as the case says, modelx sweeps every point fully and the compiled
    model must agree everywhere, the label accessors and every raise included.
    """
    build = sec_build(SEC)
    found = []
    for case, rows in _labels_not_text():
        folder = compiled_case(build, tmp_path / case, model_points=rows)
        model = mx.read_model(folder, name=_name(f"labels_{case}"))
        try:
            ids = [projection(model, key).surr_charge_id() for key in point_keys(model)]
            options = [projection(model, key).db_option() for key in point_keys(model)]
        finally:
            model.close()
        if case == "blank":
            assert ids[0] == "UL9" and math.isnan(ids[1]), ids
            assert options[:2] == ["A", "B"] and math.isnan(options[2]), options
        else:
            assert ids == [0, 9] and all(isinstance(i, (int, np.integer)) for i in ids), ids
        found += compiled_mismatches(build, folder)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


@pytest.mark.cython
def test_the_compiled_model_reads_the_schedule_of_a_point_without_a_charge(sec_build,
                                                                           tmp_path):
    """Compiled, a point without a charge reads its schedule as modelx does, as at E.

    On :data:`UNCHARGED`'s table, beside the copy's SC7 and Z0, the compiled model's
    ``surr_charge_rate_max()`` and ``surr_charge_runoff_years()`` on each point without a
    charge are f77b290's numbers, pinned, of type float, and modelx's, and on the points
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
    model = mx.read_model(folder, name=_name("uncharged_cy"))
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
    s = mx.read_model(temp_inputs(tmp_path, model_path(TWIN),
                                  model_points=s_table.loc[[base]].assign(**changes),
                                  edits=SPLICED_EDITS), name=_name("capped_s"))
    try:
        for ref, value in CAPPED_REFS.items():
            setattr(s.Projection, ref, value)
        spec = dataclasses.replace(SPEC, derived=((base, CAPPED_MTH - 1),),
                                   future=((base, 25),))
        table, _ = build_sec_table(spec, s)
    finally:
        s.close()
    return table


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_where_the_cap_binds(sec_build,
                                                                              tmp_path):
    """C4 where ``mort_rate`` caps the annual rate at 1, and where it meets a NaN.

    The three rows of the cap's test (:func:`_capped_table`), on whose frames the annual
    rate passes 1 from attained age 113, go beside the build, under :data:`CAPPED_REFS`.
    modelx sweeps them fully, and the compiled model must agree at every argument modelx
    caches, identically on x86-64 and to 1e-12 relative elsewhere.  The extremes reach
    the side of ``min(q, 1.0)`` that returns 1 too, on one point; these reach it on a
    point in force when it binds, and on one issued later.

    And the committed twins of S's points 1 and 3 under an A/E of NaN, a Reference, which
    the compiled model reads as modelx does, so that a NaN reaches the cap compiled:
    ``min`` keeps its first argument there as in modelx, and C4 holds the compiled NaN to
    modelx's, in every cell it reaches.
    """
    build = sec_build(SEC)
    rows = _capped_table(tmp_path / "s")
    folder = compiled_case(build, tmp_path / "capped", model_points=rows,
                           edits=SPLICED_EDITS)
    found = compiled_mismatches(build, folder, refs=CAPPED_REFS)
    committed = _committed()
    twins = committed.loc[[_label(committed, "twin", p, 0) for p in (1, IN_FORCE)]]
    folder = compiled_case(build, tmp_path / "nan", model_points=twins)
    model = mx.read_model(folder, name=_name("nan_ref"))
    try:
        model.Projection.mort_ae_factor = float("nan")
        for key in point_keys(model):
            assert math.isnan(projection(model, key).mort_rate(0))
    finally:
        model.close()
    found += compiled_mismatches(build, folder, refs={"mort_ae_factor": float("nan")})
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


# The compiled model's own refusals: what it does with a key past the caches spec_sec.py
# sizes, which no projection the contract allows reaches, as (cell, arguments, what modelx
# does).  modelx answers a month outside cover with a zero and a policy year or an age
# past its table with the table's last row, as the cells say, and refuses a code past the
# timings and the kinds, and a policy year below 0 by name; compiled, each is past a cache,
# and raises IndexError rather than read or write beyond it.  The timing and kind caches
# are eight wide (spec_sec.py), so their first code past the cache is 8.
COMPILED_ONLY = [
    ("net_cf", (1358,), ("ok", 0.0)),
    ("net_cf", (-1,), ("ok", 0.0)),
    ("pols_if_at", (0, 8), ("raised", "ValueError: invalid timing")),
    ("av_at", (0, 8), ("raised", "ValueError: invalid timing")),
    ("claim_pp", (0, 8), ("raised", "ValueError: invalid kind")),
    ("claims_from_av", (0, 8), ("raised", "ValueError: invalid kind")),
    ("prem_persistency_py", (105,), ("ok", 0.70)),
    ("prem_persistency_py", (-1,), ("raised", "ValueError: point_id 1: "
                                    "prem_persistency.csv has no factor for policy year "
                                    "-1")),
    ("corridor_factor_at", (122,), ("ok", 1.01)),
]

# The codes inside the timing and kind caches that a cell does not take, since one
# numbering serves both timing families and every 2-D cache is timing's width
# (spec_sec.py): there the cell itself refuses the code, compiled as in modelx.  As
# (cell, the code's name or number).
CODES_IN_CACHE = [("pols_if_at", "BEF_PREM"), ("pols_if_at", "EOM"),
                  ("av_pp_at", "BEF_NB"), ("av_pp_at", "EOM"), ("av_at", "BEF_MAT"),
                  ("claim_pp", "MATURITY"), ("claim_pp", 3), ("claim_pp", 7),
                  ("claims_from_av", 3), ("claims_from_av", 7)]


def _refusal_cases():
    """Every refusal the compiled model must make as modelx does, as (case, the table, the
    edits, the References, [(position, cell, arguments)], the Data cells to read).

    A position, not a label, since a table ``Data`` refuses has no keys to give: each is
    the row's place in the table written, ``Projection``'s ``idx``, which the test indexes
    ``Projection`` by in modelx too, as :func:`_first_key` does.
    """
    committed, extract = _committed(), _extract()

    def at(table, label):
        return list(table.index).index(label)

    moved = _label(committed, "derived", 1, 113)
    cases = [
        ("past its cover", _set("duration_mth", [moved], 1032)(committed), None, {},
         [(at(committed, moved), "proj_len", ())], ()),
        ("past its cover, on the extract", _set("duration_mth", [105], 1032)(extract),
         None, {}, [(at(extract, 105), "proj_len", ())], ()),
        ("beyond the tables, on the extract", extract, None, {},
         [(0, cell, args) for cell, args, _ in BEYOND if args[0] >= 0], ()),
        ("a point without a COI scale, on the extract",
         _set("age_at_entry", [109], 36)(extract), None, {}, [(0, "result_cf", ())], ()),
        ("a load of 1: the cure payment", _set("load_prem_rate", [1], 1.0)(committed),
         None, {}, [(0, "cure_premium_pp", (0,)), (0, "cure_premium_pp", (500,))], ()),
        ("an issue age of 17, on the extract", _set("age_at_entry", [104], 17)(extract),
         None, {}, [(at(extract, 104), "proj_len", ())], ()),
        ("a class the table lacks, on the extract",
         _set("rate_class", [103, 106], "SuperPNT")(extract), None, {},
         [(0, "result_cf", ())], ("class_factor",)),
        ("a label written as text, on the extract", _relabelled(107, "7x")(extract),
         None, {}, [(at(extract, 107), "point_id", ())], ("point_id",)),
        ("codes no cell of the family takes, inside the caches", committed, None, {},
         [(0, cell, (0, code)) for cell, code in CODES_IN_CACHE], ()),
    ]
    for case, edit, refs, label, _, _ in NOT_ISSUED:
        table = committed if edit is None else edit(committed)
        cases.append((case, table, {"coi_rates.csv": _coi_at(17)}, refs,
                      [(at(table, label), "result_cf", ())], ()))
    for case, edit, runoff, cell, _, label in UNJOINED:
        table = edit(committed)
        call = "point_id" if cell == "point_id" else "result_cf"
        cases.append((case, table, _runoff(runoff), {}, [(at(table, label), call, ())],
                      (cell,)))
    for case, column, value, _ in UNDECODABLE:
        cases.append((case, _set(column, [1], value)(committed), None, {},
                      [(0, "result_cf", ())], ()))
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
def test_the_compiled_model_refuses_what_modelx_refuses(sec_build, tmp_path):
    """Compiled, the model refuses what modelx refuses, with modelx's error and message.

    A ``ValueError`` raised in a cell typed ``long long`` or ``double`` propagates out of
    the compiled model as out of modelx.  So, each on its own inputs and References
    (:func:`_refusal_cases`): ``proj_len()`` refuses a point past its cover, naming it
    by ``point_id()``, on the committed table and on the extract whose labels are not its
    positions plus one (:func:`_extract`), and a point the contract does not issue,
    which the compiled caches are not sized for (:data:`NOT_ISSUED`), on the extract too;
    each reader of a padded table refuses policy year 0, below it, and a point without a
    COI scale is refused where its first rate is read, on the extract (:data:`BEYOND`;
    a year below 0 is past the cache, below); the cure
    payment at a load of 1 raises ``UL_US_S``'s ``ZeroDivisionError`` with Python's text,
    where a C division's would differ; every case of :data:`UNJOINED`, the run-offs of 0
    and past int64 among them, of :data:`UNDECODABLE`, of :data:`MALFORMED`, VUL's value
    rule and the flag's spellings among them, and of :data:`MALFORMED_KEYS` and
    :data:`MALFORMED_RATES`, is refused by a projection, and by the ``Data`` cell that
    checks it, compiled as in modelx, so a compiled ``Data`` cell refuses each value its
    modelx cell refuses; and a code a cell does not take, inside its cache, is refused by
    the cell (:data:`CODES_IN_CACHE`).

    And the refusals that are the compiled model's alone (:data:`COMPILED_ONLY`): a month
    past the ``t`` cache either side, a code past the timing and kind caches, and a policy
    year past the ``y`` cache and an age past the ``a`` cache, each raising ``IndexError``
    compiled, beside what modelx does.

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
    found, refused, compared = [], 0, 0
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
            compared += 1
            if case == "compiled only":
                expected = next(w for c, a, w in COMPILED_ONLY if (c, a) == (cell, args))
                if modelx_did != expected:
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
            compared += 1
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

# How long the stack test waits for each child, in seconds: one runs in about a second, a
# few under load.  A bracketing size may kill its child on a stack overflow by design, and
# where the overflow hangs instead, as Windows Error Reporting could, the wait ends sooner
# than for the two runs asserted, and the size is recorded as timed out.
BRACKET_TIMEOUT, ASSERTED_TIMEOUT = 120, 300


@pytest.mark.cython
def test_the_longest_frame_runs_cold_on_a_one_megabyte_stack(sec_build, tmp_path):
    """The deepest call the contract allows runs compiled on a 1 MiB stack (F7).

    On the two points of :func:`_longest_cover`, S's point 1 at issue age 18, issued now
    and 120 months on, whose cover runs 1,236 months, a cold ``net_cf`` in the last month
    runs the account value's chain from the end of the frame back to ``t_entry``, 1,235
    months and the cells above and below it deep in modelx on a model just read
    (:func:`test_every_chain_runs_one_cell_a_month_from_a_cold_start`), and compiled it
    runs on the C stack, which the interpreter's recursion limit does not count.  1 MiB
    is the stack MSVC gives an executable's main thread unless the executable asks for
    more: a host that embeds Python, where python.exe itself asks for 2,000,000 bytes.  A
    thread whose stack is reserved at 1 MiB stands in for it on every platform
    (``sec_support.run_compiled``), and in one each call runs cold and returns modelx's
    number, identically on x86-64 (``sec_support.exact_here``) and to 1e-12 elsewhere.
    With gcc the calls need between 256 and 384 KiB.  A stack too small kills the child,
    and the test fails naming the stack.  The thread's stack is read back too, from
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
    extremes, labels = _longest_cover(tmp_path / "copy")
    rows = pd.read_csv(extremes.parent / TABLE, index_col="point_id")
    folder = compiled_case(build, tmp_path / "extremes", model_points=rows,
                           edits=SPLICED_EDITS)
    model = mx.read_model(folder, name=_name("longest"))
    try:
        calls, want = {}, {}
        for key, label in zip(point_keys(model), labels):
            proj = projection(model, key)
            last = proj.proj_len() - 1
            assert last - proj.t_entry() == 12 * (121 - YOUNGEST) - 1, label
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


# A compiled model's Reference set after it has computed, in a child of its own: what the
# base Projection, an ItemSpace made before the change and one made after give for
# expenses(12), before inflation_rate is set to 0 and after.
STALE_CHILD = """\\
import json, sys
sys.path.insert(0, sys.argv[1])
model = __import__(sys.argv[2]).mx_model
p = model.Projection
early = p[2]
values = [p.expenses(12), early.expenses(12)]
p.inflation_rate = 0.0
values += [p.expenses(12), early.expenses(12), p[3].expenses(12)]
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
    which moves ``expenses(12)`` on every point in force then: the base ``Projection``,
    the worked example's twin at ``idx`` 0, S's in-force point's twin, made before, and
    S's point 1 restated at its month 12, made after, so that a modelx-cython that began
    to clear caches would be seen here, and the advice changed with it.  A compiled value
    meets modelx's as C4 holds it (:func:`_as_modelx`), and one the compiled model kept,
    its own value of before, identically.
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
        before = (p.expenses(12), projection(model, 2).expenses(12))
        p.inflation_rate = 0.0
        fresh = (p.expenses(12), projection(model, 2).expenses(12),
                 projection(model, 3).expenses(12))
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
    modelx's: point 6's description, S's in-force point restated six months on, with its
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
