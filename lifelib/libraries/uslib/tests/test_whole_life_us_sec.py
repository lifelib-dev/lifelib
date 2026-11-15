"""In-force tests for WholeLife_US_SEC: the splice, future business, counts, regeneration.

``WholeLife_US_SEC`` is ``WholeLife_US_S`` taught to run in force at a valuation date
(USLIB-SEC-PLAN.md, milestone M2).  It runs on two clocks: ``t`` counts months from the
valuation date, the same month for every model point, and ``duration_mth(t)`` counts the
months the policy has been in force, ``duration_mth_init() + t``.  A model point may be a
policy already in force at the valuation date, in any month of its policy year, one issued
at it, or one to be issued after it, as in ``basiclife/BasicTerm_SE``.  A policy in force
opens with seven columns of state beside its count: the paid-up additions, the loan and
the accumulation balance entering month 0, the paid-up additions and the loan at the
anniversary that opened its policy year, the dividend credited there, and the gross
premium paid to date.

The worked example is not restated here.  On a point issued at the valuation date the two
clocks coincide and the model is ``WholeLife_US_S``, and ``test_model_conventions.py``
asserts that cell by cell on the twins of S's fourteen new-business points (T1), so every
golden of ``test_whole_life_us.py`` on them holds on this model with no number copied.
The worked example itself sits on S's point 1, in force at its month 108.  Its twin is a
splice case (T2), and at the shipped assumptions it is S's point from month 108 on, in
every cell but those expense inflation moves.  The conventions also hold the SEC family's
other rules: every frame opens at ``t = 0``, ``pols_if`` is the ``BEF_DECR`` count,
``BEF_DECR`` is ``BEF_NB`` plus the month's new business, new business enters once, and
nothing happens before issue.  This module holds the rest of the plan's tests (its §5.2)
and the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's and in
  ``result_pols``.  The months straddle the policy year: its first month, its middle and
  its last, which credits the dividend; then the late years and the last covered month.
  They run on every dividend option, the loan, the PUA rider, both term blends, limited
  pay, final expense level and graded, and the female cell, and five variants of S's
  points, in a copy of S's table, add the rider paid monthly, REDUCE_PREM paid
  semi-annually, the graded plan paid quarterly, and premiums paid for twenty years and to
  attained age 65.
* T3, future new business: a point issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before issue and no rate evaluated there.
* D11's R1 and R2, and D3's clock: on the splice's grid no cell is called at a negative
  month, none evaluated on the books reads a month before them, and none reads beyond
  ``t + 1`` but the term blend's one read of the dividend at the anniversary that closes
  its year; on the committed points no recursion runs backward over the frame; the
  policy clock is a closed form; and every chain of the model runs one cell a month from
  a cold start, as far as the contract's longest cover.
* T4, the count algebra: the count rolls forward through new business and decrements,
  ``result_pols`` is S's report with the new business beside it, multiplying
  ``policy_count`` by 2.5, with the switches that ship off switched on, multiplies every
  flow and every counted cell by 2.5 and moves no per-policy value, and the count's check,
  whose tolerance scales with the count, closes on a million policies.
* T5, validation: each malformed in-force row is refused as the table is read, naming its
  point, each rule over a window of months just inside its edges; the future horizon is
  a Reference that bounds future business, and at 0 refuses it; a point past maturity is
  refused by ``proj_len()``, and so is a point the contract does not issue; the edges of
  the interface, and of every range ``Data`` holds a value to, are accepted; and so is
  every state ``WholeLife_US_S`` reaches, on each set of inputs on which those states
  differ.
* Phase 2's decoding: what ``Data`` cannot decode is refused by name, a key written as
  text among it, and so is a read beyond a table, whose padding is NaN; a key written as
  a float reads as ``WholeLife_US_S`` reads it; and a value a cap, a ``min`` or a ``max``
  reads, an amount, a share, a rate or a net single premium, is a number in its range,
  or ``Data`` refuses it, blank, text, infinite or outside it, naming the file, the
  column and every line, schedule or point at fault, when its array is first read.
* T6, regeneration: the committed ``model_point_table_sec.csv`` is what the generator makes
  of ``WholeLife_US_S`` and its table as they stand.
* Then the two clocks on the shipped points, the worked example's pre-frame values as the
  opening state, a policy valued mid-year, the dividend options and the graded benefit in
  force, the last dividend, expense inflation on the valuation clock, acquisition on new
  business, the cap on mortality and a NaN that reaches it, the values outside cover, the
  block, an in-force extract, the runner and its block's sum, the docstrings, the shared
  input tables, and what the default grid reaches; and what Phase 2 split or decoded,
  held to S: the claims total, bit for bit, every premium period, a dividend option none
  of the four, and rounding switched off, which is a digit count below -400.
* C2, the fingerprint: every committed point computes what the model computed when Phase 1
  ended, frozen at the end of this module before Phase 2 changed anything (§5.4).
* Compiled (marked ``cython``): C4 on the splice grid, at the contract's extremes and where
  the cap binds, the compiled model refusing what modelx refuses, the deepest cold call on
  a 1 MiB stack, a Reference set late, which clears no compiled cache, and the runner
  compiled.  ``test_compiled_conventions.py`` holds the rest of Phase 2's tests for every
  compiled model: C3, C5, C4 on the committed points and the release.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``, 108
for the twin of S's point 1, ``-k`` for one issued ``k`` months on.

**The core grid and the full one** (USLIB-SEC-PLAN.md K6).  A WholeLife projection costs
about ten times a Term one, and T2 and T3 over every point at every month, 107 cases and
34, would nearly double this module's run time in every run.  By default they run a
core of 35 and 9 cases, chosen so that between them they reach every branch, every
opening-state column, every kind of valuation month and every premium mode the full grid
reaches, which ``test_the_core_grid_reaches_every_branch`` asserts.  The other cases, and
the rules test's scan of their rows, carry the ``sec_full`` marker and are skipped, with
the reason shown, unless ``USLIB_SEC_FULL=1`` is set.  They are never dropped: one leg of
the CI matrix sets it, so every CI run runs the full grid, and
``USLIB_SEC_FULL=1 python -m pytest -m sec_full tests/test_whole_life_us_sec.py`` runs
them alone.  The compiled comparison on the splice grid follows the same split through
the splice's fixture, and carries no ``sec_full`` marker, since the cython job fails a
compile test that skips.  Memory is the other cost: a projected point holds about 40 MB of
cached values and their dependency graph, so a row read once, a splice case's or a point
of a temporary copy, is released as soon as it has been read (``_release``), and the
splice's rows are held one at a time, however large the grid.

Every test keeps four rules.  Each model is read under a name of its own and closed:
``test_whole_life_us.py`` reads S under its default name, and reading a model under a name
in use renames the open one.  No test writes inside the library tree: every changed input
goes through ``sec_support.temp_inputs`` into a temporary directory, because a CSV added
beside the models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``us_registry.point_keys`` and the ItemSpaces from
``us_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor Phase 2's positions can
point a test at the wrong row.  And a timing or a kind is passed as the model's int
Reference of its name, ``pols_if_at(t, p.BEF_DECR)``, as at stage ``"EC"``, where Phase 2
made the strings int codes and changed the call syntax only (C1); comparing with S, which
passes the strings, maps one onto the other through ``sec_support.codes``.
"""
import ast
import dataclasses
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
    frame_mismatches, label_mismatches, run_compiled, sweep, temp_inputs,
    twin_mismatches)
from us_registry import model_path, point_keys, projection

SEC, TWIN, TABLE = "WholeLife_US_SEC", "WholeLife_US_S", "model_point_table_sec.csv"
SPEC = SEC_SPECS[SEC]

# S's fourteen new-business points: the participating ones, issued at 45 with 660 months
# of cover, and final expense, issued at 65 with 420.  S's point 1 is the worked example,
# in force at its month 108.
PAR_NB = (2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 15)
FE_NB = (11, 12, 13)
NEW_BUSINESS = PAR_NB + FE_NB

# T2's months (USLIB-SEC-PLAN.md §7.2).  On the participating points: the first
# anniversary, a premium due at t = 0; the anniversary that opens policy year 10, the
# worked example's year; 115, the middle of that year; 119, its last month, which credits
# the dividend at t = 0 and has the following year read it back from inside the frame;
# 120, the anniversary after; and 600, in the last five policy years, where the lapse rate
# falls to zero and the cash value schedule ends.  On final expense, whose graded death
# benefit runs through policy year 2: 12 and 18 inside the graded years, 23 their last
# month, 24 the first after them, 115 and 400 later.  Then months of a point's own: the
# funded blend mid-year before its crossover (78) and in the month that closes that year
# (83), and the last covered month of ACCUM, REDUCE_PREM and final expense level.  S's
# in-force point 1 is restated too, at months after its own 108.  T3's: issued one month
# on, which puts the policy anniversaries a month off the valuation years, and twelve,
# which puts them back on; and, on S point 2 alone, thirteen, more than a year after the
# valuation date (§7.1, *Record — M14*, *Splice grid*).
PAR_MTHS = (12, 108, 115, 119, 120, 600)
FE_MTHS = (12, 18, 23, 24, 115, 400)
EXTRA_MTHS = {8: (78, 83), 4: (659,), 5: (659,), 11: (419,)}
IN_FORCE_MTHS = {1: (115, 119, 120, 600)}
FUTURE_MTHS = (1, 12)
LATE_FUTURES = ((2, 13),)

# Three more S points, in the splice's copy of S's table and never in the committed one,
# each one of S's points paying in a mode S never pairs it with:
#
# 16, S point 7's PUA rider paid monthly: an instalment buys additions in every month, at
#   t = 0 of a valuation mid-year among them, which WholeLife_US_S priced at
#   nsp_mth(t - 1) (R1), and the additions at the anniversary differ from those entering
#   the month;
# 17, S point 5's REDUCE_PREM paid semi-annually: the year's second instalment, at policy
#   month 12y + 6, is net of the dividend that opened the year, div_prev_anniv_init when
#   the point is valued at 114;
# 18, S point 12's graded plan paid quarterly: the premiums paid before a valuation inside
#   the graded years are instalments, at final expense's own modal factor;
# 19 and 20, S point 9 with premiums paid for twenty years and to attained age 65: the two
#   premium periods no S point carries, which Data decodes to their codes and joins to the
#   cash value schedule and the net level premium by their text (M15).
#
# Each variant is (the S point it changes, the columns it changes); the policy_id keeps the
# generated ids apart.  Between them and S's points every mode is reached: annual on most,
# monthly on S point 15 and on 16, semi-annual on 17, quarterly on 18; and every premium
# period, TO_100 on most, PAY_10 on S point 9, PAY_20 on 19 and TO_65 on 20.  At issue age
# 45 the last two both pay for twenty years, so the test of the premium period's decoding
# tells them apart at other ages; a premium period ending on the policy clock is S point
# 9's PAY_10, restated at 115.
VARIANTS = {
    16: (7, {"policy_id": "WLPAR-900016", "premium_mode": "M"}),
    17: (5, {"policy_id": "WLPAR-900017", "premium_mode": "SA"}),
    18: (12, {"policy_id": "WLFE-900018", "premium_mode": "Q"}),
    19: (9, {"policy_id": "WLPAR-900019", "premium_period": "PAY_20"}),
    20: (9, {"policy_id": "WLPAR-900020", "premium_period": "TO_65"}),
}
VARIANT_MTHS = {16: (12, 115, 120), 17: (114, 115, 120, 600), 18: (7, 12, 18, 24),
                19: (115,), 20: (115,)}

# T2's cases, as (row_kind, S point, source_mth): each S point restated in force at each
# of its months, then the twin of S's own in-force row, which is a splice case too (§5.2),
# aligned at its source_mth, the first row of its S frame.  T3's cases, as (S point, k).
SPLICES = (tuple(("derived", p, d) for p in PAR_NB for d in PAR_MTHS)
           + tuple(("derived", p, d) for p in FE_NB for d in FE_MTHS)
           + tuple(("derived", p, d) for p, mths in EXTRA_MTHS.items() for d in mths)
           + tuple(("derived", p, d) for p, mths in IN_FORCE_MTHS.items() for d in mths)
           + tuple(("derived", p, d) for p, mths in VARIANT_MTHS.items() for d in mths))
IN_FORCE_TWINS = (("twin", 1, 108),)
FUTURES = (tuple((p, k) for p in NEW_BUSINESS for k in FUTURE_MTHS)
           + tuple((p, 1) for p in VARIANTS) + LATE_FUTURES)

# The default run's cases (the module docstring), each with what it is there for.  The
# rest of SPLICES and FUTURES run with USLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("twin", 1, 108): "S's in-force row, the worked example's year",
    ("derived", 1, 115): "S's in-force row restated mid-year",
    ("derived", 2, 12): "PUA on the first anniversary, a premium due at t = 0",
    ("derived", 2, 115): "PUA mid-year, in the worked example's year",
    ("derived", 2, 119): "PUA in an anniversary month, with years to run",
    ("derived", 2, 600): "PUA late: the final-year lapse and the schedule's end",
    ("derived", 3, 600): "CASH late, with the premium-offset overlay live",
    ("derived", 4, 108): "ACCUM on an anniversary: div_accum_init",
    ("derived", 4, 115): "ACCUM mid-year",
    ("derived", 4, 659): "ACCUM in the last month: maturity with the balance",
    ("derived", 5, 108): "REDUCE_PREM on an anniversary: div_prev_anniv_init at t = 0",
    ("derived", 5, 119): "REDUCE_PREM in an anniversary month: next year's offset",
    ("derived", 5, 659): "REDUCE_PREM's last dividend",
    ("derived", 6, 115): "the loan mid-year: loan_bal_prev_anniv_init",
    ("derived", 6, 119): "the loan in an anniversary month: interest at t = 0",
    ("derived", 6, 120): "the loan on an anniversary",
    ("derived", 7, 12): "the PUA rider on the first anniversary: additions there",
    ("derived", 7, 120): "the PUA rider, annual: a purchase at t = 0",
    ("derived", 8, 78): "the funded blend mid-year: pua_face_prev_anniv_init in the gap",
    ("derived", 8, 83): "the funded blend in an anniversary month",
    ("derived", 9, 115): "limited pay: the premium period ends at t = 5",
    ("derived", 10, 12): "the female cell",
    ("derived", 11, 400): "final expense level late: the final-year lapse",
    ("derived", 12, 18): "final expense graded, inside the graded years: prem_cum_init",
    ("derived", 12, 23): "final expense graded, in the last graded month",
    ("derived", 12, 24): "final expense graded, the first month after them",
    ("derived", 13, 12): "final expense female",
    ("derived", 14, 12): "the unfunded blend early: its dividend's leftover below 1e-7",
    ("derived", 14, 600): "the unfunded blend late: the cap binds",
    ("derived", 15, 115): "monthly mode mid-year",
    ("derived", 16, 115): "the rider monthly mid-year: an instalment at t = 0",
    ("derived", 17, 114): "REDUCE_PREM semi-annual: an instalment at t = 0, net",
    ("derived", 18, 7): "final expense graded quarterly: instalments before t = 0",
    ("derived", 19, 115): "premiums for twenty years: the period's schedule and NNLP",
    ("derived", 20, 115): "premiums to attained age 65: the period's schedule and NNLP",
}
CORE_FUTURES = {
    (2, 1): "issued a month off the valuation anniversaries",
    (2, 12): "issued on them, a year on",
    (4, 12): "ACCUM",
    (5, 1): "REDUCE_PREM",
    (8, 1): "the funded blend and its rider",
    (12, 1): "final expense graded",
    (15, 1): "monthly mode",
    (16, 1): "the rider paid monthly",
    (2, 13): "issued more than a year on",
}

SEC_FULL = os.environ.get("USLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "USLIB_SEC_FULL=1 (USLIB-SEC-PLAN.md K6)"))

# What the splice sets in both models, S and SEC alike, before either evaluates anything.
# Expense inflation is the one input WholeLife reads on the valuation clock (D7): S
# inflates from issue and SEC from the valuation date, so at the shipped 2% the expenses of
# a point opened at d differ by 1.02^(d/12), by design, and at 0 both factors are 1.  The
# clock itself is then asserted on its own, at the shipped rate.  There is no scenario
# table and no mortality improvement, so no input table moves with d.  The rest are
# switches that ship off, or at a value that hides some of the state from any comparison:
#   pua_div_on, the PUA-block dividend, without which the paid-up additions at the
#     anniversary are read by the term blend alone;
#   prem_offset_on, the premium-offset overlay, without which last year's dividend reaches
#     the premium under REDUCE_PREM alone;
#   dyn_lapse_on, the dynamic lapse overlay, at a competitor rate of 8% for a factor of
#     1.02, so that its cell is reached at all;
#   int_rate_loan apart from the shipped dividend rate: at i_L = i_d the loan cancels out
#     of the dividend's interest margin, and a wrong loan at the anniversary would show in
#     the loan interest alone.
# The identity does not depend on the values, only on both models having the same ones.
SPLICED_REFS = {
    "inflation_rate": 0.0, "pua_div_on": True, "prem_offset_on": True,
    "dyn_lapse_on": True, "competitor_rate": 0.08, "int_rate_loan": 0.08}

# The splice's switches, for T4, at the shipped inflation: the three overlays that ship
# off, the competitor rate at which the dynamic lapse factor is not 1, and the loan rate
# apart from the dividend rate, at which direct recognition is not 0.
SWITCHED_ON = {ref: value for ref, value in SPLICED_REFS.items() if ref != "inflation_rate"}

# The cells T2 and T3 skip beyond T1's, which already drop result_pols as a whole and S's
# proj_start and duration_inforce, cells this model does not have (the spec's exempt).
# proj_len counts from the valuation date on SEC and from issue on S, so it differs by d,
# or by -k, by design; frame_mismatches asserts what it must get right, that both frames
# end at the same instant.  anniv_mth returns a month, and on SEC's clock that month is
# S's less d: the cells that read it are compared, so a wrong anniversary still fails.
# result_cf_annual groups by policy year, and a point opened at d lacks S's earlier years
# and, opened mid-year, holds only the rest of the current one (the mid-year test compares
# the later years).  A future point's years are all whole once its pre-issue months are
# dropped, so T3 compares it.  Both tests compare result_pols column by column instead.
SPLICE_EXEMPT = (TWIN_EXEMPT_DEFAULT | SPEC.exempt
                 | {"proj_len", "anniv_mth", "result_cf_annual"})
FUTURE_EXEMPT = TWIN_EXEMPT_DEFAULT | SPEC.exempt | {"proj_len", "anniv_mth"}

# The result_cf columns that expense inflation moves, and the cells they are made of: on
# the committed points, at the shipped 2%, the only places an in-force row departs from S.
INFLATED = ("expenses", "net_cf", "liability_cf")
INFLATION_CELLS = frozenset({"inflation_factor", "expenses", "liability_cf", "net_cf",
                             "result_cf", "result_cf_annual"})

# The S cells whose exact value is 0 and whose computed value is rounding about it, the two
# roll-forward residuals: a comparison with S holds them at the harness's absolute floor
# of 1e-9, and every other cell at none (_compare).
RESIDUALS = frozenset({"check_pols_roll_fwd_resid", "check_pua_roll_fwd_resid"})

# The decrement rates, none of which may be evaluated before issue (R1, D4).
DECREMENT_RATES = ("mort_rate_guar_at", "mort_rate", "mort_rate_mth", "lapse_rate",
                   "lapse_rate_mth")

# The cells that scale with policy_count.  Every other cell is a per-policy amount, a rate,
# a clock or a flag, and must not move when the count does.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz",
    "pols_death", "pols_lapse", "pols_maturity", "premiums", "rider_premiums",
    "premium_taxes", "expenses", "claims", "claims_death", "claims_lapse",
    "claims_maturity", "div_cash_paid", "loan_draws",
    "liability_cf", "net_cf", "check_pols_roll_fwd_resid",
    "result_cf", "result_cf_annual", "result_pols"})

# result_pols' columns, in its order: the count, the new business within it, the month's
# deaths and surrenders in processing order, the maturities of the last covered month,
# then S's four decrement rates, which no count moves.
RESULT_POLS = ["pols_if", "pols_new_biz", "pols_death", "pols_lapse", "pols_maturity",
               "mort_rate", "mort_rate_mth", "lapse_rate", "lapse_rate_mth"]
OUTFLOWS = RESULT_POLS[2:5]
RATES = RESULT_POLS[5:]

# The four timings S knows, then BEF_NB, the one running in force adds; and the kinds.  Each
# is the name of the model's int Reference for it, read off the ItemSpace by that name.
TIMINGS = ("BEF_NB", "BEF_DECR", "BEF_SURR", "BEF_MAT", "AFT_DECR")
KINDS = ("DEATH", "LAPSE", "MATURITY")

# What each cell holds outside cover, before issue and from the month cover has ended, as
# its docstring says: no count, so no cash flow; no value, no dividend and no premium; no
# question about the contract answered yes; and no table read at a policy year or an age
# the policy does not have.  The type is part of the value.  A count is a float in every
# branch and a flag a bool, because Phase 2 types a cell by the values it returns
# (USLIB-SEC-PLAN.md F3).  The guard test also calls claim_pp at each kind and pols_if_at
# at each timing, all 0.0.
OUTSIDE_COVER = {
    "is_active": False, "prem_due": False, "is_anniv": False,
    "premium_pp_ann": 0.0, "premium_net_pp_ann": 0.0, "premium_pp": 0.0,
    "premium_net_pp": 0.0, "rider_premium_pp_ann": 0.0, "rider_premium_pp": 0.0,
    "prem_cum": 0.0, "cv_pp": 0.0, "nsp_mth": 0.0, "mort_rate_guar": 0.0,
    "div_prev_anniv": 0.0, "div_int": 0.0, "div_base": 0.0, "div_pua": 0.0,
    "div_credited": 0.0,
    "oyt_face": 0.0, "oyt_cost": 0.0, "div_to_pua": 0.0, "div_cash": 0.0,
    "div_accum": 0.0, "pua_face_purch": 0.0, "pua_face_rider": 0.0,
    "pua_face_offset": 0.0, "pua_face": 0.0, "pua_cv": 0.0, "loan_int": 0.0,
    "loan_bal": 0.0, "loan_draw": 0.0,
    "pols_if": 0.0, "pols_new_biz": 0.0, "pols_death": 0.0, "pols_lapse": 0.0,
    "pols_maturity": 0.0, "premiums": 0.0, "rider_premiums": 0.0, "premium_taxes": 0.0,
    "expenses": 0.0, "claims": 0.0, "claims_death": 0.0, "claims_lapse": 0.0,
    "claims_maturity": 0.0, "div_cash_paid": 0.0, "loan_draws": 0.0,
    "liability_cf": 0.0, "net_cf": 0.0}

# The cells a month outside cover may not reach: the decrement rates, the dividend's
# mortality and expense margins, and every read keyed by an attained age or a policy year.
# mort_rate_guar and nsp_mth are the two attained-age reads the guard test calls itself,
# and are held by their values instead, as is the interest margin, which is zero in every
# month but an anniversary and so reads the schedule's policy year in cover alone.  The
# other margins and the rates have no guard of their own: no formula reaches them outside
# cover, and a caller must not either (USLIB-SEC-PLAN.md F4).
IN_COVER_ONLY = ("age", "age_anniv", "cv_pp_anniv", "nsp", "net_amt_at_risk",
                 "mort_rate_scale", "dyn_lapse_factor", "div_mort", "div_exp",
                 *DECREMENT_RATES)

# The opening state, in Data's order, and the cells running in force and then compiling add
# to WholeLife_US_S's or rename, each of which the symbol map must name.
STATE = ("pua_face_init", "pua_face_prev_anniv_init", "loan_bal_init",
         "loan_bal_prev_anniv_init", "div_accum_init", "div_prev_anniv_init",
         "prem_cum_init")
NEW_CELLS = ("policy_count", "duration_mth_init", "t_entry", "maturity_mth", "is_active",
             "pols_new_biz", *STATE, "point_id", "is_graded", "premium_period_code",
             "dividend_option_code", "annual_premium", "pua_rider_premium", "cv_schedule",
             "nsp_schedule", "mort_schedule", "claims_death", "claims_lapse",
             "claims_maturity")

INFLATION = 0.02        # the shipped inflation_rate, which the inflation test reads

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A report evaluates each column in ascending t, so a forward
# recursion, through t - 1, finds the month before already cached: the committed points'
# sweep runs under a limit of 28 and not under 27, the graded final-expense point being
# the deepest, at 29 cells.  A backward recursion over the frame, through t + 1, opens a
# chain as long as the frame, and the shortest frame longer than a month is 402.
CALL_DEPTH = 60

# The one read beyond t + 1 the model makes, as (reader, cell read): the term-blend layer
# of a policy year is bought with the dividend credited at the anniversary that closes it,
# so every month of the year reads that dividend, up to eleven months ahead: the read at
# anniv_mth(t) that R2 allows (USLIB-SEC-PLAN.md R2, precised at M2).  It opens no chain
# forward, since that dividend depends on the year's opening balances and the schedules
# alone, and never leaves the frame, which ends on an anniversary.  The rules test admits
# it there and nowhere else.
LOOK_AHEAD = {("oyt_face", "div_credited")}

REPORTS = ("result_cf", "result_pols", "result_cv", "result_cf_annual")


# ---------------------------------------------------------------------------
# Helpers

_names = itertools.count(1)


def _name(tag):
    """A model name that no other read in this session uses."""
    return f"{SEC}_{tag}_{next(_names)}"


def _key(model, point_id):
    """The registry's key for the row labelled ``point_id`` (``us_registry.point_keys``)."""
    return dict(zip(model.Data.model_point_table().index, point_keys(model)))[point_id]


def _point(model, point_id):
    """The ItemSpace of the row labelled ``point_id``, through the registry's keys."""
    return projection(model, _key(model, point_id))


def _label(table, kind, s_point, month):
    """The ``point_id`` of the one ``kind`` row generated from S point ``s_point``.

    ``month`` is the row's ``source_mth``: 0 for a new-business twin, 108 for the twin of
    S's point 1, ``d`` for a derived row, ``-k`` for a future one.  The twins keep S's
    ``point_id`` and ``policy_id``, so the S policy is the twin's.
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

    A projected WholeLife point holds about 40 MB of cached values and their dependency
    graph.  The splice's rows and the doubled and extract copies' points are each needed
    once, so each is released when read, as ``run_sec.py --block`` releases its points
    (USLIB-SEC-PLAN.md F5): held together they would raise this module's memory by
    gigabytes.  Asked for again, the ItemSpace is made afresh and recomputes.
    """
    del model.Projection[key]


def _committed():
    """The committed SEC table as the file holds it, unvalidated, indexed by point_id."""
    return pd.read_csv(model_path(SEC).parent / TABLE, index_col="point_id")


def _sec_inputs(tmp_path, table):
    """A copy of the product directory whose SEC table is ``table``; its SEC folder."""
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE)


def _read_edited(tmp_path, edit):
    """WholeLife_US_SEC read from a copy whose SEC table is ``edit(_committed())``."""
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
    """Evaluate on an S point what the splice compares: the sweep, and two cells more.

    :func:`sec_support.sweep` reaches neither ``mec_flag`` nor ``policy_year`` on
    ``WholeLife_US_S``, because no result column or check reads them, and a cell S never
    evaluates is compared nowhere.  They are evaluated here, ``policy_year`` over the
    frame, so the splice and the future comparison see them too.  At the shipped
    assumptions the sweep leaves ``dyn_lapse_factor`` unreached as well, which is why T1
    never compares it; under :data:`SPLICED_REFS` it reaches it.
    """
    sweep(proj)
    proj.mec_flag()
    for t in range(proj.proj_start(), proj.proj_len()):
        proj.policy_year(t)


def _compare(s_proj, sec_proj, month, exempt, columns=None):
    """Where SEC's row departs from S's point from S month ``month`` on, in two passes.

    First the frames, ``result_cf`` (over ``columns``, or every column both hold) and
    ``result_pols``, SEC row ``t`` against S row ``t + month``, frames ending together;
    then every cell of S's but ``exempt`` and :data:`RESIDUALS`, at every argument S cached
    inside its frame from ``month`` on, moved onto SEC's clock, S's timing and kind strings
    mapped onto SEC's codes (``sec_support.codes``).  Both to 1e-9 relative with
    no absolute floor (USLIB-SEC-PLAN.md §5.2, T2, precised at M11): a floor of 1e-9 passes
    an error of 1% in any value below 1e-7, and of 1.4e-5 in the splice's fewest deaths in
    a month, 6.9e-5.  Where the unfunded blend's cap takes a dividend whole, its leftover is
    a rounding about 0, from 3e-16 to 3e-13, which the two models compute alike.  Then the
    cells of :data:`RESIDUALS` alone, at the floor of 1e-9: their exact value is 0, and the
    computed one moves by an ulp of what it closes when an opening state comes back from the
    CSV one ulp off.  Returns the mismatch lines, empty when the row is S's.
    """
    found = []
    for report, keep in (("result_cf", columns), ("result_pols", None)):
        found += [f"{report}: {line}" for line in frame_mismatches(
            s_proj.cells[report](), sec_proj.cells[report](), t_offset=month,
            columns=keep, atol=0.0)]
    found += twin_mismatches(s_proj, sec_proj, t_offset=month, exempt=exempt | RESIDUALS,
                             atol=0.0, codes=codes(sec_proj))
    return found + twin_mismatches(s_proj, sec_proj, t_offset=month,
                                   exempt=exempt | (set(s_proj.cells) - RESIDUALS),
                                   codes=codes(sec_proj))


def _continues_s(s_proj, sec_proj, month):
    """Where a committed row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison (:func:`_compare`), on the committed model at the shipped
    assumptions: frame by frame, ``result_cf`` and ``result_pols``, then cell by cell over
    every cell of S's but :data:`SPLICE_EXEMPT`.  The shipped 2% expense inflation runs
    from issue in S and from the valuation date here (D7), so :data:`INFLATED`'s three
    columns, and :data:`INFLATION_CELLS`, differ by design and are left out; the inflation
    test holds them.  Every other column and cell must agree, to 1e-9 relative, with no
    absolute floor but on the residuals.
    """
    keep = [c for c in s_proj.result_cf().columns if c not in INFLATED]
    return _compare(s_proj, sec_proj, month, SPLICE_EXEMPT | INFLATION_CELLS, keep)


def _case_id(kind, s_point, month):
    """A case's id: ``point2-d12``, ``point1-twin108``, or ``point2-k3`` if issued later."""
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
    """WholeLife_US_SEC read in place, as committed, and swept once, cold; what it met.

    The model is first asked for ``duration_mth(500)`` on the twin of S point 2, and the
    keys that call leaves in ``duration_mth`` are kept.  Then every committed point is
    swept (:func:`sec_support.sweep`: ``result_cf``, the other reports and the checks), in
    table order and each column in ascending ``t``, under a recursion limit lowered to
    :data:`CALL_DEPTH`, and whatever that raises is kept, point by point, rather than
    raised.  So the record says what a cold model does, which the clock and depth test
    asserts (D3, R2), and every test on the committed model reads a model already swept:
    the sweep is paid once, not once for each.  Returns ``(model, record)``.
    """
    model = mx.read_model(model_path(SEC), name=_name("sec"))
    first = _row(model, "twin", 2, 0)
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
    """WholeLife_US_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """WholeLife_US_S read in place, as committed, with every point swept.

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


@pytest.fixture(scope="module")
def spliced(tmp_path_factory):
    """S and SEC on the splice's inputs, with :data:`SPLICED_REFS` set in both.

    S is read from a copy of the product directory whose table has the variants appended.
    SEC runs on the same assumption tables, and on a model point table of its own, built by
    the generator from the registered spec with its rows replaced by the cases this run
    selects, the core or the full grid (:func:`_selected`), out of this S model, so each
    row opens with the state of the very run it is compared with.  No input table moves
    with ``d``: WholeLife's one valuation-clock input is the ``inflation_rate`` Reference.
    Every S point is then swept (:func:`_sweep_s`), and stays swept; each SEC row is
    projected by the case that compares it and released once compared (:func:`_settle`).
    """
    root = tmp_path_factory.mktemp("spliced")
    s_folder = temp_inputs(root / "s", model_path(TWIN),
                           model_points=_s_table_with_variants())
    s = mx.read_model(s_folder, name=_name("s_spliced"))
    for ref, value in SPLICED_REFS.items():
        setattr(s.Projection, ref, value)
    derived = [(p, d) for kind, p, d in _selected(SPLICES, CORE_SPLICES)]
    spec = dataclasses.replace(SPEC, derived=tuple(derived),
                               future=tuple(_selected(FUTURES, CORE_FUTURES)))
    table, companions = build_sec_table(spec, s)
    assert companions == {}
    sec_folder = temp_inputs(root / "sec", model_path(SEC), model_points=table,
                             model_point_file=spec.model_point_file)
    sec = mx.read_model(sec_folder, name=_name("sec_spliced"))
    for ref, value in SPLICED_REFS.items():
        setattr(sec.Projection, ref, value)
    for key in point_keys(s):
        _sweep_s(projection(s, key))
    yield s, sec
    sec.close()
    s.close()


@pytest.fixture(scope="module")
def splice_records():
    """What each splice row was found to do once compared, by case (:func:`_settle`)."""
    return {}


# ---------------------------------------------------------------------------
# The splice's records
#
# Each T2 and T3 case compares its row with S, then records what the rules test and the
# core grid's reach need of the row, and releases it (_settle): held together, the rows of
# the core grid alone come to about 1.4 GB.  So each of the two tests reads the records,
# and computes any case no earlier test has recorded, which keeps it whole when run alone.


def _cached_args(cells):
    """The argument tuple of every key ``cells`` has cached (:func:`sec_support._args`)."""
    n = len(cells.parameters)
    return [() if n == 0 else (key,) if n == 1 else tuple(key)
            for key in list(cells.keys())]


def _month(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _the_closing_anniversary(proj, t, u):
    """Whether month ``u`` is the anniversary closing the policy year of month ``t``.

    That is the one look-ahead :data:`LOOK_AHEAD` admits, and only there: ``u`` is
    ``anniv_mth(t)``, later than ``t`` and at most eleven months on, an anniversary on the
    policy clock, and inside the frame.
    """
    return (u == proj.anniv_mth(t) and t < u <= t + 11
            and proj.duration_mth(u) % 12 == 11 and u < proj.proj_len())


def _rule_breaches(proj):
    """R1 and R2's look-ahead on one row, once its four reports have run.

    ``{"negative": [...], "early": [...], "ahead": [...], "admitted": n,
    "three kinds": [...]}``: every cached call with a negative argument; every precedent
    keyed by a month before ``t_entry()`` of a call keyed by a month at or after it; every
    precedent keyed by a month beyond ``t + 1`` of a call keyed by ``t``, but
    :data:`LOOK_AHEAD`'s read at the anniversary closing the policy year of ``t``; how many
    of those were admitted; and every month whose claims are non-zero in all three kinds,
    where ``claims(t)`` written out would part from ``WholeLife_US_S``'s compensated
    ``sum`` (:func:`test_the_claims_total_is_s_claims_bit_for_bit`).  A precedent is a
    call's as modelx's dependency graph records it.
    """
    for report in REPORTS:
        proj.cells[report]()
    three = [t for t in range(proj.proj_len())
             if proj.claims_death(t) and proj.claims_lapse(t) and proj.claims_maturity(t)]
    entry = proj.t_entry()
    negative, early, ahead, admitted = [], [], [], 0
    for name, cells in proj.cells.items():
        t_pos = cells.parameters.index("t") if "t" in cells.parameters else None
        for args in _cached_args(cells):
            if any(_month(a) and a < 0 for a in args):
                negative.append(f"{name}{args}")
            if t_pos is None:
                continue
            t = args[t_pos]
            for node in cells.preds(*args):
                params = getattr(node.obj, "parameters", None) or ()
                u = node.args[params.index("t")] if "t" in params else None
                if not _month(u):
                    continue
                if u < entry <= t:
                    early.append(f"{name}{args} -> {node.obj.name}{node.args}")
                if u <= t + 1:
                    continue
                if ((name, node.obj.name) in LOOK_AHEAD
                        and _the_closing_anniversary(proj, t, u)):
                    admitted += 1
                    continue
                ahead.append(f"{name}{args} -> {node.obj.name}{node.args}")
    return {"negative": negative, "early": early, "ahead": ahead, "admitted": admitted,
            "three kinds": three}


def _gap(x, t):
    """The term-blend gap of the policy year of month ``t``, on the additions opening it."""
    prev = x.anniv_mth(t) - 12
    puaf = x.pua_face(prev) if prev >= x.t_entry() else x.pua_face_prev_anniv_init()
    return max(x.term_blend_target() - x.sum_assured() - puaf, 0.0)


def _apart(x):
    """Which of the two anniversary columns differ from the current ones on row ``x``."""
    return {"additions": x.pua_face_prev_anniv_init() != x.pua_face_init(),
            "loan": x.loan_bal_prev_anniv_init() != x.loan_bal_init()}


def _year_under_way(x):
    """The months of the policy year under way at the valuation date, in the frame."""
    return range(min(x.anniv_mth(0) + 1, x.proj_len()))


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, every opening-state column is in use,
# each anniversary column apart from its current one, so that a column read in its pair's
# place would show, additions at the first anniversary, the edge of the first policy year,
# and every read of the anniversary before the valuation date is taken with that value
# apart: the PUA-block dividend, the loan interest and the term-blend gap of the year under
# way, a premium net of div_prev_anniv_init, the graded benefit on prem_cum_init.  Later in
# the frame, every branch the dividend drives.
AT_VALUATION = {
    **{f"{c} non-zero": (lambda x, c=c: x.cells[c]() != 0.0) for c in STATE},
    "the anniversary additions apart": lambda x: _apart(x)["additions"],
    "the anniversary loan apart": lambda x: _apart(x)["loan"],
    "additions at the first anniversary": lambda x: (
        x.duration_mth_init() == 12 and x.pua_face_prev_anniv_init() > 0.0),
    "the PUA-block dividend on them": lambda x: (
        _apart(x)["additions"] and x.div_pua(x.anniv_mth(0)) > 0.0),
    "the loan interest on it": lambda x: (
        _apart(x)["loan"] and x.loan_int(x.anniv_mth(0)) > 0.0),
    "the term-blend gap on them": lambda x: _apart(x)["additions"] and x.oyt_face(0) > 0.0,
    "a premium net of div_prev_anniv_init": lambda x: (
        x.div_prev_anniv_init() > 0.0
        and any(x.premium_net_pp(t) < x.premium_pp(t) for t in _year_under_way(x))),
    "the graded benefit on prem_cum_init": lambda x: (
        x.product() == "WL_FE_GRADED" and x.prem_cum_init() > 0.0
        and x.claim_pp(0, x.DEATH) < x.sum_assured()),
}
IN_FRAME = {
    "the REDUCE_PREM excess buying additions": lambda x, t: x.pua_face_offset(t) > 0.0,
    "the premium-offset overlay": lambda x, t: (
        x.dividend_option() != "REDUCE_PREM"
        and x.premium_net_pp_ann(t) < x.premium_pp_ann(t)),
    "the blend's cap binding": lambda x, t: (
        x.is_blended() and 0.0 < x.oyt_face(t) < _gap(x, t)),
    "a blend past its crossover": lambda x, t: x.is_blended() and _gap(x, t) == 0.0,
    "the last dividend buying additions at maturity": lambda x, t: (
        x.dividend_option() == "REDUCE_PREM" and t == x.proj_len() - 1
        and x.div_to_pua(t) > 0.0),
}


def _branches(x):
    """The names in :data:`AT_VALUATION` and :data:`IN_FRAME` that hold of row ``x``."""
    reached = {what for what, holds in AT_VALUATION.items() if holds(x)}
    return reached | {what for what, holds in IN_FRAME.items()
                      if any(holds(x, t) for t in range(x.proj_len()))}


def _settle(records, case, model, key):
    """Record what the rules and the core grid's reach need of a row, and release it.

    ``case`` is the row's (row_kind, S point, source_mth) and ``key`` its registry key in
    ``model``, the splice's SEC model.  A T2 or T3 case calls this once it has compared
    the row, whatever the comparison found, so the row is released either way.  The record
    is :func:`_rule_breaches`'s, with the row's :func:`_branches` for an in-force row, and
    a row that raises is recorded as raising, which the rules test reports.
    """
    try:
        proj = projection(model, key)
        record = _rule_breaches(proj)
        record["branches"] = _branches(proj) if case[0] != "future" else set()
        record["raised"] = None
    except Exception as err:                    # recorded, and reported by the rules test
        record = {"negative": [], "early": [], "ahead": [], "admitted": 0,
                  "three kinds": [], "branches": set(), "raised": _raised(err)}
    finally:
        _release(model, key)
    records[case] = record
    return record


def _record_of(spliced, records, case):
    """The record of ``case``, from the case that compared its row or, failing it, now."""
    if case not in records:
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
    ``result_cf`` and every column of ``result_pols`` both reports hold, and fail frames
    that end apart.  The cell comparison then evaluates every cell of S's but
    :data:`SPLICE_EXEMPT`, at every argument S cached inside its own frame from month ``d``
    on, moved onto SEC's clock: the value state, the dividend steps, the counts and
    ``result_cv`` among them.  Each compares to 1e-9 relative with no absolute floor, but
    the roll-forward residuals, which keep the floor of 1e-9 (:func:`_compare`).  An S cell
    this model lacked would fail it.

    The anniversary-month cases, ``d = 12y + 11``, are the ones that see a look-back to the
    year's anniversary stop a month early: the next anniversary's dividend, its loan
    interest and its PUA block read month ``t - 12 = 0``, the valuation month itself.  The
    row is then recorded for the rules test and released (:func:`_settle`).
    """
    s, sec = spliced
    key = _row_key(sec, kind, s_point, month)
    s_proj, sec_proj = _point(s, s_point), projection(sec, key)
    try:
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

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at maturity, in ``result_cf``
    and in every column of ``result_pols`` S's has, and every cell of S's but
    :data:`FUTURE_EXEMPT` agrees at every argument S cached inside its own frame, moved
    ``k`` later, ``result_cf_annual`` and ``result_cv`` included: once its pre-issue
    months are dropped, its policy years are S's.  Each compares as the splice compares,
    with no absolute floor but on the residuals (:func:`_compare`).  An S cell this model
    lacked would fail it.  Before issue every column of ``result_cf``, ``result_pols`` and
    ``result_cv`` is an exact zero, and the policies arrive in month ``k`` as new business.

    The last assertions are R1 and D4's base rule made testable.  After every report, no
    decrement rate keyed by month has been evaluated at a month before issue, and the
    guarantee mortality keyed by age has not been read below the issue age.  A count
    recursion based at ``t == 0`` rather than at ``t_entry()``, or a decrement count that
    evaluates its rate before asking whether the month is in cover, still gives the right
    numbers.  This is the only test that sees the first, and the guard test sees the second
    too.

    The pre-issue rows are asserted present before they are asserted zero, in each of the
    three reports: a frame that opened at issue would have none, its zeros would hold of
    nothing, and the comparisons with S, which start at issue, would not see it.  The row
    is then recorded for the rules test and released (:func:`_settle`).
    """
    s, sec = spliced
    key = _row_key(sec, "future", s_point, -k)
    s_proj, sec_proj = _point(s, s_point), projection(sec, key)
    try:
        df, pols = sec_proj.result_cf(), sec_proj.result_pols()
        sec_proj.result_cf_annual()
        cv = sec_proj.result_cv()
        assert _compare(s_proj, sec_proj, -k, FUTURE_EXEMPT) == []
        for report, frame in (("result_cf", df), ("result_pols", pols), ("result_cv", cv)):
            assert list(frame.index[:k]) == list(range(k)), report
            assert (frame.loc[:k - 1] == 0.0).all().all(), report
        assert sec_proj.pols_new_biz(k) == sec_proj.policy_count() == 1.0
        early = {name: sorted(t for t in sec_proj.cells[name].keys() if t < k)
                 for name in DECREMENT_RATES if name != "mort_rate_guar_at"}
        assert not any(early.values()), f"rates evaluated before issue: {early}"
        ages = sorted(sec_proj.cells["mort_rate_guar_at"].keys())
        assert ages and ages[0] >= sec_proj.age_at_entry(), f"ages read: {ages[:5]}"
    finally:
        _settle(splice_records, ("future", s_point, -k), sec, key)


# ---------------------------------------------------------------------------
# D11's R1 and R2, and D3's closed-form clock


@pytest.mark.parametrize("grid", [pytest.param("core", id="core"),
                                  pytest.param("full", id="full", marks=FULL_ONLY)])
def test_no_cell_is_called_before_the_valuation_date_or_reads_far_ahead(spliced,
                                                                        splice_records,
                                                                        grid):
    """R1, its look-back and R2's look-ahead, on the rows T2 and T3 compare: core or rest.

    Each is a rule of how the model computes, not of what, so no number shows a breach,
    and on a point issued at ``t = 0`` the two clocks coincide and hide it from T1 too.
    The splice's rows are points in force at every month T2 names, the variants among them,
    and points issued later, and on each the four reports are run first:

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and
      a compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  A policy
      month turned into ``t`` by subtracting ``duration_mth_init()`` (R1a) goes negative
      on a point in force past it, and so does a balance read a month or a year back
      without the opening state's branch.  The keys of ``cv_pp_anniv``, ``nsp`` and
      ``mort_rate_guar_at``, a policy year and ages, are held to it too: a schedule read
      at a policy year before issue would wrap round in a compiled model.
    * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
      ``t_entry()`` on read a month before it.  On a point issued later a recursion based
      at ``t == 0`` reads the pre-issue zeros, so no number shows it and no argument goes
      negative.
    * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month beyond
      ``t + 1``, as modelx's dependency graph records each cached call's precedents, with
      one exception, :data:`LOOK_AHEAD`'s, admitted at the anniversary closing the policy
      year of ``t`` and nowhere else, and asserted to occur.  ``WholeLife_US_S``'s
      ``anniv_mth`` returned a policy month, which on this clock lands a policy's age away.

    And no month of any row has claims of all three kinds, so ``claims(t)``, the three
    summed left to right, is ``WholeLife_US_S``'s compensated ``sum`` on every row too
    (:func:`test_the_claims_total_is_s_claims_bit_for_bit`).

    Each row was scanned by the T2 or T3 case that compared it (:func:`_settle`), and a
    row no case has scanned is scanned here.  The core case covers the core's rows, the
    full case every other row of the full grid, with ``USLIB_SEC_FULL=1``.  The
    new-business twins in the splice's table are no case's, and are left out: on them the
    clocks coincide, and T1 compares them with S cell by cell.  The closed-form clock and
    the recursion depth are asserted on the committed model, in the test after this one.
    """
    cases = [case for case in GRID if (case in CORE_GRID) == (grid == "core")]
    negative, early, ahead, raised, three, admitted = [], [], [], [], [], 0
    for case in cases:
        record, where = _record_of(spliced, splice_records, case), _case_id(*case)
        three += [f"{where}: t = {t}" for t in record["three kinds"]]
        negative += [f"{where}: {call}" for call in record["negative"]]
        early += [f"{where}: {read}" for read in record["early"]]
        ahead += [f"{where}: {read}" for read in record["ahead"]]
        if record["raised"]:
            raised.append(f"{where}: {record['raised']}")
        admitted += record["admitted"]
    assert cases, f"the {grid} grid has no rows"
    assert not raised, f"rows that raised: {raised[:10]}"
    assert not negative, f"called before the valuation date: {negative[:10]}"
    assert not early, f"read before issue from the books: {early[:10]}"
    assert not ahead, f"read beyond t + 1: {ahead[:10]}"
    assert admitted, f"no read of {sorted(LOOK_AHEAD)} at the closing anniversary"
    assert not three, f"claims of all three kinds in one month: {three[:10]}"


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


# How deep a cold call may run beyond its chain, one cell a month from its month back to
# t_entry() (D5): the cells above the chain and those below it, the first month's rates and
# Data's first reads of its tables.  A cold net_cf in the last month runs 12 cells beyond
# the count's chain, on 660 months and at the contract's longest cover alike, and each
# chain called alone at most 6 beyond (measured at M15, the accessors reading Data's
# vectors).  Term's 16, as for Term, MYGA, FIA and DIA.  Any chain of two cells a month
# runs a frame's length beyond.
CHAIN_OVERHEAD = 16

# The youngest issue age product-spec.md admits, level pay from 0 (USLIB-SEC-PLAN.md D5,
# F7): the longest cover from issue, to the maturity age of 100, is 1,200 months.
YOUNGEST = 0

# Each chain of the model and the cell that heads it, called cold in the last month of the
# frame: (cell, the name of its timing's Reference).  They are called in this order on one
# fresh read, an order in which no chain is reached before its own head is called: the
# premiums paid to date, the accumulated dividends, the paid-up additions and the count.
# On S's point 4, which leaves its dividends to accumulate, every one runs the frame's
# length.
CHAIN_HEADS = (("prem_cum", None), ("div_accum", None), ("pua_face", None),
               ("pols_if_at", "BEF_NB"))


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


def _younger(table):
    """An age-keyed table with its first age's rows repeated down to :data:`YOUNGEST`."""
    first = table[table["age"] == table["age"].min()]
    rows = [first.assign(age=age, provenance="test copy")
            for age in range(YOUNGEST, int(table["age"].min()))]
    return pd.concat([*rows, table], ignore_index=True)


def _as_issued_at_45(table):
    """A table keyed by issue age, its issue-age-45 rows repeated at :data:`YOUNGEST`."""
    rows = table[table["issue_age"] == 45].assign(issue_age=YOUNGEST,
                                                  provenance="test copy")
    return pd.concat([table, rows], ignore_index=True)


def _cash_values_from_youngest(table):
    """The cash value table with a level-pay male schedule at :data:`YOUNGEST`, rising
    $10 per $1,000 a policy year to the face at year 100."""
    years = range(1, 101)
    rows = pd.DataFrame({"premium_period": "TO_100", "sex": "M", "issue_age": YOUNGEST,
                         "policy_year": list(years),
                         "cv_per_1000": [10.0 * y for y in years],
                         "provenance": "test copy"})
    return pd.concat([table, rows], ignore_index=True)


def _longest_cover(tmp_path):
    """A copy whose table holds S point 4 at issue age 0, issued now and 120 months on.

    The frame from issue is ``12 * (100 - issue age)`` months, so the longest cover is at
    the youngest issue age the product spec issues at, level pay from 0: 1,200 months, and
    the longest frame is that issued 120 months on, the shipped ``future_horizon_mth``,
    1,320 months, whose chains stop at ``t_entry()``.  S's tables price issue ages 45 and
    65 alone, from attained age 18, so the copy's age-keyed tables repeat their first age
    down to 0, its issue-age tables their issue-age-45 rows at 0, and its cash values run
    up to the face; how deep a chain runs does not depend on the values.  S point 4
    accumulates its dividends, so every chain of the model runs on it.
    """
    committed = _committed()
    now = _label(committed, "twin", 4, 0)
    rows = committed.loc[[now, now]].assign(issue_age=YOUNGEST).set_axis(
        [now, committed.index.max() + 1]).rename_axis("point_id")
    rows = _set("duration_mth", [rows.index[1]], -120)(rows)
    edits = {"mort_table.csv": _younger, "nsp_table.csv": _younger,
             "cv_table.csv": _cash_values_from_youngest,
             "premium_rates.csv": _as_issued_at_45,
             "np_guar_table.csv": _as_issued_at_45}
    folder = temp_inputs(tmp_path, model_path(SEC), model_points=rows,
                         model_point_file=TABLE, edits=edits)
    return folder, list(rows.index)


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_every_chain_runs_one_cell_a_month_from_a_cold_start(tmp_path):
    """Called cold, each chain runs one cell a month back to ``t_entry()``, no more (D5).

    No number shows how deep a chain runs, and a compiled model runs it on the C stack, so
    a chain of two cells a month, which gives the same numbers, needs twice the stack on
    every platform (F7); ``WholeLife_US_S``'s cold ``net_cf`` runs 3,304 cells deep on a
    660-month frame.  On a model just read, nothing is cached, so modelx's stack trace
    counts how deep a call runs, against one cell a month and :data:`CHAIN_OVERHEAD` more
    (:func:`_one_cell_a_month`), with modelx's recursion limit where the module leaves it:

    * ``net_cf`` in the last month, on a read of its own: the deepest call a projection
      makes, and what bounds the stack a compiled model needs;
    * then, on a second read, each of :data:`CHAIN_HEADS` alone, in an order that leaves
      each chain cold until its own head is called, which is checked: so a chain that a
      ``net_cf`` call reaches from the side is measured too, where a ``net_cf`` call would
      have found it cached.

    On the twin of S's point 4, issued now, 660 months; and by default, as §7.5's
    *Record — M5* and M14's carried rule ask, at the contract's longest cover, issue age 0,
    issued now and 120 months on (:func:`_longest_cover`), each row's frame asserted first.
    """
    committed = _committed()
    extremes, labels = _longest_cover(tmp_path)
    reads = [(model_path(SEC), [_label(committed, "twin", 4, 0)], 660),
             (extremes, labels, 1200)]
    found = []
    for folder, points, months in reads:
        for label in points:
            fresh = mx.read_model(folder, name=_name("cold"))
            try:
                p = _point(fresh, label)
                assert p.proj_len() - p.t_entry() == months, (label, p.proj_len())
                last = p.proj_len() - 1
                found += _one_cell_a_month(p, label, "net_cf", (last,), last)
            finally:
                fresh.close()
            fresh = mx.read_model(folder, name=_name("chains"))
            try:
                p = _point(fresh, label)
                last = p.proj_len() - 1
                for cell, timing in CHAIN_HEADS:
                    if len(p.cells[cell].keys()):
                        found.append(f"point {label}: {cell} was reached before it was "
                                     f"called, so its chain was not cold")
                        continue
                    args = (last,) if timing is None else (last, p.refs[timing])
                    found += _one_cell_a_month(p, label, cell, args, last)
            finally:
                fresh.close()
    assert not found, found


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and is not repeated here.


def test_the_count_rolls_forward_through_new_business_and_decrements(sec_model):
    """The count leaves month t by its deaths, surrenders and maturities alone.

    On every committed point and at every ``t`` of its frame, the count weighting month
    ``t``, ``pols_if_at(t, BEF_DECR)``, less the count carried into ``t + 1``,
    ``pols_if_at(t + 1, BEF_NB)``, is the three outflows of month ``t``, to 1e-12.  The
    step from the last row to ``t = proj_len()`` is what catches cover that runs a month too
    long: the maturities would then leave a month late, and the count would carry over.
    And the notes' end-of-period count, ``pols_if_at(t, AFT_DECR)``, is exactly the count
    carried into the next month before its new business, in every month: the two are one
    product in one order.

    ``result_pols()`` sets the same movement out row by row, in :data:`RESULT_POLS`'s
    columns, indexed by ``t`` over the frame: ``pols_if`` at ``t + 1`` is ``pols_if`` less
    the outflows at ``t``, plus the new business of ``t + 1``, and row 0 opens from
    ``pols_if_init()``.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            out = p.pols_death(t) + p.pols_lapse(t) + p.pols_maturity(t)
            moved = p.pols_if_at(t, p.BEF_DECR) - p.pols_if_at(t + 1, p.BEF_NB)
            assert moved == pytest.approx(out, abs=1e-12), (point_id, t)
            assert p.pols_if_at(t, p.AFT_DECR) == p.pols_if_at(t + 1, p.BEF_NB), (
                point_id, t)
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(p.proj_len()))
        carried = (pols["pols_if"] - pols[OUTFLOWS].sum(axis=1)).shift(1)
        expected = carried.fillna(p.pols_if_init()) + pols["pols_new_biz"]
        assert ((pols["pols_if"] - expected).abs() <= 1e-12).all(), point_id


def test_result_pols_is_s_report_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's, column for column, with ``pols_new_biz`` second (D5).

    T1 skips the report as a whole, because its frame has a column S's lacks (the spec's
    exempt), so it is compared here, on every twin: on the fourteen issued at the
    valuation date at offset 0, and on S's in-force point at its month 108.  Every column
    S's report has agrees, to 1e-9, frames ending together, and ``pols_new_biz`` holds the
    count in the issue month and 0 in every other.  The counts and rates carry no
    inflation, so the shipped assumptions serve.
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


def test_the_claims_total_is_s_claims_bit_for_bit(sec_model, s_model):
    """``claims(t)`` is ``WholeLife_US_S``'s ``claims(t)``, bit for bit (R12, M15).

    S's ``claims(t, kind=None)`` is the three kinds and their total in one cell, the total
    a ``sum`` of a generator.  Here the kinds are ``claims_death``, ``claims_lapse`` and
    ``claims_maturity`` and ``claims(t)`` their total written out, so T1 exempts S's cell,
    whose keys no cell here takes (the spec's exempt), and the total is compared here: on
    the fourteen twins issued at the valuation date, in every month of the frame, equal to
    S's total, sign of a zero and type included, and each kind equal to S's
    ``claims(t, kind)``.  Python's ``sum`` of floats is compensated, so the total written
    out is S's float only where at most two kinds are non-zero in a month, which holds on
    every committed point: maturities fall in the last covered month, where
    ``lapse_rate`` is 0.
    """
    table = sec_model.Data.model_point_table()
    found = []
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            kinds = (p.claims_death(t), p.claims_lapse(t), p.claims_maturity(t))
            if all(kinds):
                found.append(f"point {point_id}: all three kinds non-zero at t = {t}")
        if table.at[point_id, "row_kind"] != "twin" or table.at[point_id, "duration_mth"]:
            continue
        s = _point(s_model, point_id)
        for t in range(p.proj_len()):
            mine, theirs = p.claims(t), s.claims(t)
            if (mine != theirs or type(mine) is not type(theirs)
                    or math.copysign(1.0, mine) != math.copysign(1.0, theirs)):
                found.append(f"point {point_id}: claims({t}) {mine!r}, S's {theirs!r}")
            for cell, kind in (("claims_death", "DEATH"), ("claims_lapse", "LAPSE"),
                               ("claims_maturity", "MATURITY")):
                if p.cells[cell](t) != s.claims(t, kind):
                    found.append(f"point {point_id}: {cell}({t}) is not S's "
                                 f"claims({t}, {kind!r})")
    assert not found, found[:20]


# The month at which the sign test sets the three kinds on the anchor cell's twin, in force
# at S's month 108: in cover, where the death claim is nonzero.
ZERO_MONTH = 5


def test_three_negative_zero_kinds_total_a_positive_zero_as_s_sum_does():
    """``claims(t)`` is ``0.0``, not ``-0.0``, where all three kinds are ``-0.0``, as S's.

    S's total is ``sum`` of the three kinds, which starts at the int 0, and ``0 + -0.0`` is
    ``0.0``, so S's total of three negative zeros is a positive zero.  ``claims(t)`` starts
    its sum at ``0.0`` for that reason, and the claims test cannot hold it: no committed
    month has three zero kinds, the death claim being nonzero in cover.  So here, on a read
    of each model of their own, the three kinds of the anchor cell's twin at
    :data:`ZERO_MONTH` are set to ``-0.0`` as modelx input values, and so are S's
    ``claims(t, kind)`` of point 1 in the same month, S's month 108 later, and the totals
    must be S's: ``0.0``, a float, with a positive sign.  A total written without its
    ``0.0`` start gives ``-0.0`` and fails.
    """
    s = mx.read_model(model_path(TWIN), name=_name("s_zeros"))
    sec = mx.read_model(model_path(SEC), name=_name("zeros"))
    try:
        theirs, mine = _point(s, 1), _row(sec, "twin", 1, 108)
        month = 108 + ZERO_MONTH
        assert mine.claims_death(ZERO_MONTH) == theirs.claims(month, "DEATH") != 0.0
        for kind in ("DEATH", "LAPSE", "MATURITY"):
            theirs.claims[month, kind] = -0.0
        for cell in ("claims_death", "claims_lapse", "claims_maturity"):
            mine.cells[cell][ZERO_MONTH] = -0.0
        totals = (theirs.claims(month), mine.claims(ZERO_MONTH))
    finally:
        sec.close()
        s.close()
    for total in totals:
        assert type(total) is float and total == 0.0, totals
        assert math.copysign(1.0, total) == 1.0, totals


# The premium periods and the issue ages the decoding test reads them at: two ages, so that
# TO_65 and PAY_20, both twenty years at 45, are told apart, and TO_100 at both.
PERIODS = ("TO_100", "PAY_10", "PAY_20", "TO_65")
PERIOD_AGES = (30, 50)


def test_every_premium_period_decodes_as_wholelife_us_s_reads_it(tmp_path):
    """Each premium period decodes to the code that selects S's premium-paying years.

    ``Data.premium_period_code`` turns the text into a code, and ``policy_term`` and
    ``mec_flag`` branch on it where ``WholeLife_US_S`` compares the text.  No committed
    point is PAY_20 or TO_65, and at issue age 45, the splice's, both pay for twenty
    years, so a decoding that swapped them would pass every comparison there.  So S point
    9 is restated at issue ages 30 and 50 on each period, in a table of S's and one of
    this model's, and ``policy_term()`` and ``mec_flag()`` must be S's on every row, each
    of the right type; neither reads a table, so no table needs a row at those ages.
    """
    s_base = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                         index_col="point_id").loc[[9]]
    sec_base = _committed().loc[[_label(_committed(), "twin", 9, 0)]]
    cases = [(q, age) for q in PERIODS for age in PERIOD_AGES]
    labels = pd.Index(range(1, len(cases) + 1), name="point_id")

    def restated(base):
        rows = pd.concat([base.assign(premium_period=q, issue_age=age) for q, age in cases])
        return rows.set_axis(labels)

    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN),
                                  model_points=restated(s_base)), name=_name("s_periods"))
    sec = mx.read_model(_sec_inputs(tmp_path / "sec", restated(sec_base)),
                        name=_name("periods"))
    try:
        found = []
        for (q, age), label in zip(cases, labels):
            mine, theirs = _point(sec, label), _point(s, label)
            assert mine.premium_period_code() == mine.refs[q], (q, age)
            for cell in ("policy_term", "mec_flag"):
                got, want = mine.cells[cell](), theirs.cells[cell]()
                if got != want or type(got) is not type(want):
                    found.append(f"{q} at {age}: {cell} {got!r}, S's {want!r}")
    finally:
        sec.close()
        s.close()
    assert not found, found


def test_an_unknown_dividend_option_is_read_as_wholelife_us_s_reads_it(tmp_path):
    """A dividend option none of the four is ``NONE``, as ``WholeLife_US_S`` reads it.

    ``WholeLife_US_S`` compares the option's text with PUA, CASH, ACCUM and REDUCE_PREM
    and reads any other text as none of them, so a participating point whose option is
    misspelt earns its dividend and applies it nowhere.  ``Data.dividend_option_code``
    decodes such text to ``NONE`` rather than refuse it (R6).  On S point 2 with its option
    written ``PAU``, in a table of S's and in this model's, the twin must decode to
    ``NONE`` and be S's point in every cell, as T1 compares a twin, and its dividend must
    reach no option: a decoding that read the text as any of the four would apply it.
    """
    s_base = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                         index_col="point_id").loc[[2]].assign(dividend_option="PAU")
    sec_base = _committed().loc[[_label(_committed(), "twin", 2, 0)]].assign(
        dividend_option="PAU")
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=s_base),
                      name=_name("s_pau"))
    sec = mx.read_model(_sec_inputs(tmp_path / "sec", sec_base), name=_name("pau"))
    try:
        theirs, mine = _point(s, 2), _point(sec, 2)
        assert (mine.dividend_option(), mine.dividend_option_code()) == ("PAU", mine.NONE)
        _sweep_s(theirs)
        assert twin_mismatches(theirs, mine, exempt=TWIN_EXEMPT_DEFAULT | SPEC.exempt,
                               codes=codes(mine)) == []
        months = range(mine.proj_len())
        assert sum(mine.div_credited(t) for t in months) > 0.0
        applied = ("div_to_pua", "div_cash", "div_accum", "pua_face_offset")
        assert [name for name in applied
                if any(mine.cells[name](t) != 0.0 for t in months)] == []
    finally:
        sec.close()
        s.close()


# The digit counts the rounding test sets, each beside WholeLife_US_S's own setting: the
# sentinel, -1,000, and the count just below -400 turn rounding off, S's None; -400, the
# lowest count that rounds, and the negative counts S rounds a dividend to tens and
# hundreds with, round as S rounds, and so does 0.
ROUNDINGS = ((-1000, None), (-401, None), (-400, -400), (-2, -2), (-1, -1), (0, 0))


def test_rounding_off_is_a_digit_count_below_minus_400():
    """``div_round_digits`` is an int: below -400 it turns rounding off, as
    ``WholeLife_US_S``'s ``None`` does, and every other count rounds as S rounds.

    ``WholeLife_US_S`` turns rounding off with ``None``, which no C int holds, so here a
    count below -400 turns it off (R16).  S's ``round`` gives 0.0 for every float from -309
    digits down, so no count that leaves S a dividend turns rounding off here: -1 rounds
    to tens, -2 to hundreds, 0 to the dollar, in both.  C2 holds the shipped two
    decimals.  On the anchor cell's twin, in force at S's month 108, each count of
    :data:`ROUNDINGS` against S's setting beside it, the twin must be S's point from that
    month on in every cell, as the splice compares it (:func:`_continues_s`), so a
    sentinel that caught a count S rounds with, or a count below -400 handed to ``round``,
    fails here.  And the dividends are what each setting names: the unrounded amount at
    the sentinel and at -401, 0.0 at -400, and ``round`` of it at -2, -1, 0 and 2, six
    distinct amounts in all, so each comparison reaches the branch it names.
    """
    s = mx.read_model(model_path(TWIN), name=_name("s_round"))
    sec = mx.read_model(model_path(SEC), name=_name("round"))
    try:
        mine = _row(sec, "twin", 1, 108)
        anniversary = mine.anniv_mth(0)
        dividends = {2: mine.div_base(anniversary)}
        for digits, s_digits in ROUNDINGS:
            # Setting a Reference makes every ItemSpace afresh.
            sec.Projection.div_round_digits = digits
            s.Projection.div_round_digits = s_digits
            theirs, mine = _point(s, 1), _row(sec, "twin", 1, 108)
            _sweep_s(theirs)
            assert _continues_s(theirs, mine, 108) == [], digits
            dividends[digits] = mine.div_base(anniversary)
    finally:
        sec.close()
        s.close()
    unrounded = dividends[-1000]
    assert dividends[-401] == unrounded and dividends[-400] == 0.0, dividends
    assert [dividends[d] for d in (-2, -1, 0, 2)] == [
        round(unrounded, d) for d in (-2, -1, 0, 2)], dividends
    assert len(set(dividends.values())) == 6, dividends


# What T4 multiplies policy_count by: not a whole number, because a count of policies need
# not be one, so that a flow which read the count as whole policies would not follow it.
COUNT_FACTOR = 2.5


def test_scaling_the_count_scales_every_flow_and_no_per_policy_value(tmp_path):
    """``policy_count`` is a weight: 2.5 times the count, 2.5 times every flow, the same per
    policy.

    The committed table, and a copy with every count multiplied by :data:`COUNT_FACTOR`,
    are each read with :data:`SWITCHED_ON` set before either computes anything: the
    switches that ship off, and the two rates that ship where what they drive is 0, at the
    splice's values, so that every flow is nonzero on some point and the PUA-block
    dividend, the premium offset, the dynamic lapse and direct recognition reach every
    count.  On every point ``result_cf``, ``result_cf_annual`` and the counts of
    ``result_pols`` are 2.5 times the committed table's, element by element, to 1e-12
    relative: a scaled count is a computed float, which may come back from the CSV within
    two ulps (``sec_support``'s module docstring).  ``result_pols``'s four rates are the
    committed table's exactly.  So is every other cell of :data:`COUNTED`, at every argument
    the sweep of the committed table's point cached: the count at each timing and the
    claims of each kind, which no report shows, among them, and the count's roll-forward
    residual, a rounding about 0 on that many policies, to the residuals' floor of 1e-9.
    And every cell outside :data:`COUNTED` (the premium, the cash value, the paid-up
    additions, the dividend, the loan, the opening state, the rates, both clocks, the
    flags) agrees bit for bit at every argument that sweep cached.  So a flow that dropped
    the count, or read it as whole policies, which a table of counts of 1 hides from every
    comparison with S and a count doubled hides here, fails (USLIB-SEC-PLAN.md §5.2, T4,
    precised at M11).  Each counted cell but the residual is nonzero on some point.  Each
    point is released once compared (:func:`_release`).
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
            for ref, value in SWITCHED_ON.items():
                setattr(model.Projection, ref, value)
        for key, scaled_key in zip(point_keys(base), point_keys(scaled)):
            one, many = projection(base, key), projection(scaled, scaled_key)
            sweep(one)
            for report in reports:
                b, d = one.cells[report](), many.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                flows = [c for c in b.columns if c not in RATES]
                want = COUNT_FACTOR * b[flows]
                bad = ((d[flows] - want).abs() > 1e-12 * want.abs()).any()
                assert not bad.any(), (key, report, list(bad[bad].index))
                rates = [c for c in b.columns if c in RATES]
                assert d[rates].equals(b[rates]), (key, report)
            for name in counted:
                floor = 1e-9 if name in RESIDUALS else 0.0
                for args in _cached_args(one.cells[name]):
                    want = COUNT_FACTOR * one.cells[name](*args)
                    got = many.cells[name](*args)
                    assert abs(got - want) <= floor + 1e-12 * abs(want), (
                        key, name, args, got, want)
                    if want != 0.0 and name not in RESIDUALS:
                        nonzero.add(name)
            assert twin_mismatches(one, many, exempt=TWIN_EXEMPT_DEFAULT | COUNTED,
                                   rtol=0.0, atol=0.0) == []
            _release(base, key)
            _release(scaled, scaled_key)
    finally:
        scaled.close()
        base.close()
    want = set(counted) - RESIDUALS
    assert want <= nonzero, f"0 on every point: {sorted(want - nonzero)}"


def test_the_count_check_closes_on_a_million_policies(tmp_path):
    """``check_pols_roll_fwd`` scales its tolerance with the count, and closes at 1e6.

    A residual is rounding on that many policies, so the check holds it to 1e-10 times
    ``max(policy_count(), 1)``, where its tolerance unscaled would be 1e-10: at the counts
    the other tests use, one policy or less, the two are one.  So every committed point is
    projected from a copy where each counts a million policies: the check closes on each,
    and on some point the largest residual exceeds the unscaled 1e-10, so the scaling is
    what closes it (USLIB-SEC-PLAN.md §5.2, T4, precised at M10).  The paid-up additions'
    check is per policy, its tolerance relative to the block, and closes as it does on one.
    Each point is released once checked (:func:`_release`).
    """
    table = _committed()
    model = mx.read_model(_sec_inputs(tmp_path, table.assign(policy_count=1e6)),
                          name=_name("million"))
    past = []
    try:
        for key, point_id in zip(point_keys(model), table.index):
            p = projection(model, key)
            assert p.policy_count() == 1e6
            assert p.check_pols_roll_fwd() and p.check_pua_roll_fwd(), point_id
            worst = max(abs(p.check_pols_roll_fwd_resid(t)) for t in range(p.proj_len()))
            if worst > 1e-10:
                past.append(point_id)
            _release(model, key)
    finally:
        model.close()
    assert past, "no residual passes the unscaled 1e-10 at a million policies"


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault.  The checks run over the whole
# table as it is read, in Data, and the message names the file it read and the column or
# every point at fault.  A blank cell reads as NaN, and so does a text cell once the checks
# coerce the column to numbers, so each is refused as a count, a duration or a balance
# that is not a number.  The repeated point_id holds another policy under the same label,
# as a bad extract would, so that the check must look at the labels and not at whole rows.
# The point_ids are the committed table's: 16 and 17, REDUCE_PREM and ACCUM valued on the
# anniversary at 108; 18, the funded blend mid-year at 78; 19, the loan mid-year at 114;
# 20, the graded plan at 18; 21, REDUCE_PREM in its last month; 22, issued 3 months on.
# The two checks that turn on the policy year are tested at their edges, where an
# off-by-one would let a row through: a row moved to months 1 and 11, the ends of the
# first policy year, and to month 12, the first anniversary, where the anniversary columns
# are the ones entering month 0.  The edges test reads the months either side, 11, 12 and
# 13, and month 1, the first after a policy not yet in force, which holds no state
# (USLIB-SEC-PLAN.md §5.2, T5, precised at M10).  The anniversary's columns hold one
# amount at one instant, so the check is exact (D6): it refuses them a cent apart either
# way, the least an extract carrying cents can show, and an ulp apart either way, the least
# two doubles can be, which the CSV keeps, as well as further.  A {file} in a message is
# the table's filename: every case is read by one model, from a file of its own (the
# malformed fixture).


# The columns Data holds at 0 in the first policy year, which opened at issue and has
# credited no dividend yet: the three anniversary columns and the accumulation balance.
FIRST_YEAR = ("pua_face_prev_anniv_init", "loan_bal_prev_anniv_init", "div_accum_init",
              "div_prev_anniv_init")


def _moved(point, month, **columns):
    """An edit that moves row ``point`` to policy month ``month`` and sets ``columns``."""
    def edit(table):
        table = _set("duration_mth", [point], month)(table)
        for column, value in columns.items():
            table = _set(column, [point], value)(table)
        return table
    return edit


def _first_year_point(column):
    """The row a first-year case moves: 17, the ACCUM point, for the balance; else 18."""
    return 17 if column == "div_accum_init" else 18


def _in_first_year(column, month):
    """A row moved into its first policy year, at policy month ``month``, ``column`` set.

    The committed table has no point in its first policy year, so this makes one, at either
    end of it, month 1 or month 11, where an off-by-one check would let the row through:
    the four :data:`FIRST_YEAR` columns are zeroed, and ``column`` alone is set.  The
    accumulation balance is set on the ACCUM point, the one option allowed a balance at
    all.  Every other check still passes, so the one under test is the first to fail.
    """
    zeros = dict.fromkeys(FIRST_YEAR, 0.0)
    return _moved(_first_year_point(column), month, **{**zeros, column: 50.0})


def _drop(column):
    return lambda table: table.drop(columns=column)


MALFORMED = [
    ("a negative count", _set("policy_count", [16], -0.1),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [16]"),
    ("a blank count", _set("policy_count", [17], float("nan")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [17]"),
    ("two bad counts", _set("policy_count", [16, 18], -1.0),
     "{file}: policy_count must be a number, zero or more; it is not at point_id "
     "[16, 18]"),
    ("a text count", _set("policy_count", [19], "abc"),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [19]"),
    ("an infinite count", _set("policy_count", [19], float("inf")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [19]"),
    ("a fractional duration", _set("duration_mth", [18], 78.5),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [18]"),
    ("a blank duration", _set("duration_mth", [22], float("nan")),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [22]"),
    ("a text duration", _set("duration_mth", [19], "x114"),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [19]"),
    # numpy casts a float past int64 to the least int64, a policy issued 2**63 months on,
    # without a word: the table refuses it first.
    ("a duration past int64", _set("duration_mth", [16], 1e19),
     "{file}: duration_mth must be below 2**53 months; it is not at point_id [16]"),
    ("durations of 2**53 months at two points", _set("duration_mth", [16, 18], 2.0 ** 53),
     "{file}: duration_mth must be below 2**53 months; it is not at point_id [16, 18]"),
    ("issued beyond the horizon", _set("duration_mth", [22], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [22]"),
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("policy_count", "duration_mth", *STATE)],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[16]].assign(policy_id="WLPAR-900099")]),
     "{file}: point_id [16] appears more than once"),
    *[(f"a negative {column}", _set(column, [point], -1.0),
       f"{{file}}: {column} must be a number, zero or more; it is not at point_id "
       f"[{point}]")
      for column, point in zip(STATE, (18, 18, 19, 19, 17, 16, 20))],
    ("a blank div_accum_init", _set("div_accum_init", [17], float("nan")),
     "{file}: div_accum_init must be a number, zero or more; it is not at point_id [17]"),
    ("a text loan_bal_init", _set("loan_bal_init", [19], "x"),
     "{file}: loan_bal_init must be a number, zero or more; it is not at point_id [19]"),
    ("an infinite pua_face_init", _set("pua_face_init", [18], float("inf")),
     "{file}: pua_face_init must be a number, zero or more; it is not at point_id [18]"),
    ("state on new business", _set("pua_face_init", [2], 100.0),
     "{file}: pua_face_init must be 0 on a policy not yet in force, duration_mth 0 or "
     "less; it is not at point_id [2]"),
    ("state on future business", _set("prem_cum_init", [22], 100.0),
     "{file}: prem_cum_init must be 0 on a policy not yet in force, duration_mth 0 or "
     "less; it is not at point_id [22]"),
    *[(f"{what} on final expense", _set(column, [20], 5.0),
       f"{{file}}: {column} must be 0 on a non-participating product, which pays no "
       f"dividend; it is not at point_id [20]")
      for what, column in (("additions", "pua_face_init"),
                           ("additions at the anniversary", "pua_face_prev_anniv_init"),
                           ("a dividend", "div_prev_anniv_init"))],
    ("an accumulation off ACCUM", _set("div_accum_init", [16], 5.0),
     "{file}: div_accum_init must be 0 unless dividend_option is ACCUM; it is not at "
     "point_id [16]"),
    ("anniversary values apart, the loan", _set("loan_bal_prev_anniv_init", [16], 3.0),
     "{file}: on a point valued on a policy anniversary, duration_mth a multiple of 12, "
     "loan_bal_prev_anniv_init must equal loan_bal_init; it does not at point_id [16]"),
    ("anniversary values apart, the additions", _set("pua_face_prev_anniv_init", [17], 3.0),
     "{file}: on a point valued on a policy anniversary, duration_mth a multiple of 12, "
     "pua_face_prev_anniv_init must equal pua_face_init; it does not at point_id [17]"),
    *[(f"{what} apart on the first anniversary", _moved(16, 12, **{anniv: 3.0}),
       f"{{file}}: on a point valued on a policy anniversary, duration_mth a multiple of "
       f"12, {anniv} must equal {now}; it does not at point_id [16]")
      for what, anniv, now in (
          ("the additions", "pua_face_prev_anniv_init", "pua_face_init"),
          ("the loan", "loan_bal_prev_anniv_init", "loan_bal_init"))],
    *[(f"{what} {gap} {side} on the anniversary",
       _moved(16, 108, **{now: 500.0, anniv: apart}),
       f"{{file}}: on a point valued on a policy anniversary, duration_mth a multiple of "
       f"12, {anniv} must equal {now}; it does not at point_id [16]")
      for what, anniv, now in (
          ("the additions", "pua_face_prev_anniv_init", "pua_face_init"),
          ("the loan", "loan_bal_prev_anniv_init", "loan_bal_init"))
      for gap, side, apart in (
          ("a cent", "above", 500.01), ("a cent", "below", 499.99),
          ("an ulp", "above", float(np.nextafter(500.0, np.inf))),
          ("an ulp", "below", float(np.nextafter(500.0, -np.inf))))],
    *[(f"{column} in the first policy year, month {month}", _in_first_year(column, month),
       f"{{file}}: {column} must be 0 in the first policy year, duration_mth 1 to 11, "
       f"which opened at issue and has credited no dividend yet; it is not at point_id "
       f"[{_first_year_point(column)}]")
      for column in FIRST_YEAR for month in (1, 11)],
]


@pytest.fixture(scope="module")
def malformed(tmp_path_factory):
    """One model, and beside it every table of :data:`MALFORMED`, each a file of its own.

    Reading the model costs more than every check it makes, so the cases share one read:
    each case points ``Data.model_point_file`` at its own file, which clears the table, and
    reads it afresh.  Returns ``(model, {case: filename})``.
    """
    root = tmp_path_factory.mktemp("malformed")
    files = {}
    for number, (case, edit, _) in enumerate(MALFORMED):
        files[case] = f"malformed_{number:02d}_sec.csv"
        temp_inputs(root, model_path(SEC), model_points=edit(_committed()),
                    model_point_file=files[case])
    model = mx.read_model(root / SEC, name=_name("malformed"))
    yield model, files
    model.close()


@pytest.mark.parametrize("case, edit, message", MALFORMED, ids=[c[0] for c in MALFORMED])
def test_a_malformed_in_force_row_is_refused_naming_its_point(malformed, case, edit,
                                                               message):
    """``Data.model_point_table()`` refuses the table, naming the fault (D6, T5)."""
    model, files = malformed
    model.Data.model_point_file = files[case]
    _refused(model.Data.model_point_table, message.format(file=files[case]))


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses a policy issued later than it, and 0 refuses all.

    The committed table's one future point is issued three months on.  It reads at the
    shipped 120 months and at 3, the shortest horizon that admits it, and is refused at 2,
    by name.  At 0 the model takes no future new business, D4's fallback for a product
    that cannot support it, and the message says so.  A negative horizon is itself
    refused.  Setting the Reference clears the table, so each value is read afresh.
    """
    future = _label(_committed(), "future", 2, -3)
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

    The REDUCE_PREM point valued on the anniversary at 108 is moved on to ``duration_mth``
    660, the month its cover ends at attained age 100.  That is a rule of the product, not
    of the table: it needs ``maturity_age``, a Projection Reference, so the table reads,
    and the point is refused where its frame is defined, on its first projection, rather
    than projecting nothing.  An anniversary row is moved because its anniversary columns
    equal its current ones, as ``Data`` requires at a multiple of 12, so that ``Data`` has
    nothing to refuse.  A loop over the block would meet the point only when it reached it,
    after projecting the points before it, so ``run_sec.py --block``, run beside the table,
    asks every point for its frame first: it fails naming the point, and prints nothing
    before.
    """
    moved = _label(_committed(), "derived", 5, 108)
    model = _read_edited(tmp_path, _set("duration_mth", [moved], 660))
    message = (f"point_id {moved}: duration_mth 660 is at or past maturity, "
               f"policy month 660")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_row(model, "derived", 5, 108).result_cf, message)
    finally:
        model.close()
    runner = tmp_path / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert message in done.stderr.decode(errors="replace")


def test_the_edges_of_the_in_force_interface_are_accepted(sec_model, tmp_path):
    """A zero count, whole numbers in any type, the horizon and the year's edges are read.

    A count of 0 is a point that projects zeros; ``114.0`` is a whole number of months,
    read back as the int the policy clock counts in; a balance written without a decimal
    point, as an extract that holds whole dollars writes it, reads as the float every
    per-policy value is, and projects what the committed table projects; and a policy
    issued 120 months after the valuation date, the shipped ``future_horizon_mth``, is the
    last one the table admits, with a frame of 780 months, 660 of cover after 120 before
    issue.

    Either side of the first anniversary, where ``Data``'s first-year check ends and its
    anniversary check begins: a row valued on it, month 12, holding paid-up additions and
    a loan, each equal to its anniversary value, a row valued the month after, 13, whose
    additions and loan have moved since the anniversary, and a row valued the month before,
    11, whose additions and loan have moved since issue, apart from their anniversary
    values, which the first year holds at 0.  And a row valued in its first month, 1,
    holding additions, a loan and the premium paid, the state the first year allows, where
    a policy not yet in force holds none (USLIB-SEC-PLAN.md §5.2, T5, precised at M10).
    And a row whose additions at the anniversary exceed those entering month 0, which
    records a partial surrender of additions the model does not implement: it reads, as
    ``Data``'s docstring says, and is projected from the values it gives, its term-blend
    gap sized on the anniversary's additions, which leave none, and its death benefit on
    those entering month 0.
    """
    committed = _committed()
    last = _label(committed, "derived", 5, 659)
    future = _label(committed, "future", 2, -3)
    on_anniv = _label(committed, "derived", 5, 108)
    after = _label(committed, "derived", 4, 108)
    before = _label(committed, "twin", 2, 0)
    first = _label(committed, "twin", 7, 0)
    partial = _label(committed, "derived", 8, 78)
    whole = ("loan_bal_init", "loan_bal_prev_anniv_init", "prem_cum_init")

    def edit(table):
        table = _moved(on_anniv, 12, pua_face_init=500.0, pua_face_prev_anniv_init=500.0,
                       loan_bal_init=100.0, loan_bal_prev_anniv_init=100.0)(table)
        table = _moved(after, 13, pua_face_init=50.0, loan_bal_init=30.0,
                       loan_bal_prev_anniv_init=20.0)(table)
        table = _moved(before, 11, pua_face_init=40.0, loan_bal_init=15.0)(table)
        table = _moved(first, 1, pua_face_init=25.0, loan_bal_init=10.0,
                       prem_cum_init=1800.0)(table)
        table = _set("pua_face_prev_anniv_init", [partial], 110000.0)(table)
        table = _set("policy_count", [last], 0.0)(table)
        table = table.assign(duration_mth=table["duration_mth"].astype(float))
        table = table.assign(**{c: table[c].astype("int64") for c in whole})
        return _set("duration_mth", [future], -120.0)(table)

    assert all((committed[c] % 1 == 0).all() for c in whole)
    model = _read_edited(tmp_path, edit)
    try:
        read = model.Data.model_point_table()
        assert read["duration_mth"].dtype == float
        assert all(read[c].dtype == "int64" for c in whole)
        assert read.loc[on_anniv, ["duration_mth", "pua_face_prev_anniv_init",
                                   "loan_bal_prev_anniv_init"]].tolist() == [12, 500, 100]
        assert read.loc[after, ["duration_mth", "pua_face_init", "pua_face_prev_anniv_init",
                                "loan_bal_init", "loan_bal_prev_anniv_init"]].tolist() == [
            13, 50, 0, 30, 20]
        assert read.loc[before, ["duration_mth", "pua_face_init",
                                 "pua_face_prev_anniv_init", "loan_bal_init",
                                 "loan_bal_prev_anniv_init"]].tolist() == [11, 40, 0, 15, 0]
        assert read.loc[first, ["duration_mth", "pua_face_init", "loan_bal_init",
                                "prem_cum_init", *FIRST_YEAR]].tolist() == [
            1, 25, 10, 1800, 0, 0, 0, 0]
        frames = (_point(model, before).proj_len(), _point(model, first).proj_len())
        assert frames == (649, 659)
        df = _row(model, "derived", 5, 659).result_cf()
        assert len(df) == 1 and (df == 0.0).all().all()
        loan = _row(model, "derived", 6, 114)
        assert loan.duration_mth(0) == 114 and type(loan.duration_mth(0)) is int
        assert loan.loan_bal_init() == 2070.0 and type(loan.loan_bal_init()) is float
        graded = _row(model, "derived", 12, 18)
        assert graded.prem_cum_init() == 3162.0 and type(graded.prem_cum_init()) is float
        for p, kind, s_point, month in ((loan, "derived", 6, 114),
                                        (graded, "derived", 12, 18)):
            assert frame_mismatches(_row(sec_model, kind, s_point, month).result_cf(),
                                    p.result_cf(), rtol=0, atol=0) == []
        late = _row(model, "future", 2, -3)
        assert (late.t_entry(), late.proj_len(), late.pols_new_biz(120)) == (120, 780, 1.0)
        blend = _row(model, "derived", 8, 78)
        assert blend.pua_face_prev_anniv_init() > blend.pua_face_init()
        assert blend.oyt_face(0) == 0.0
        assert blend.claim_pp(0, blend.DEATH) == pytest.approx(
            blend.sum_assured() + blend.pua_face_init(), rel=1e-12)
    finally:
        model.close()


def _every_state_months(start, end):
    """The S months a point whose S frame runs from ``start`` to ``end`` is restated at.

    By default the edges of its windows (USLIB-SEC-PLAN.md §5.2, T5): every month of the
    first policy year, where ``Data``'s first-year rule holds, each anniversary, where its
    anniversary rule holds, and the month before it, which credits the year's dividend,
    and the last month of the frame, before maturity.  With ``USLIB_SEC_FULL=1``, every
    month.  Each after ``start``, the twin's month.
    """
    if SEC_FULL:
        return list(range(start + 1, end))
    months = {*range(1, 12), end - 1, *(m for a in range(12, end, 12) for m in (a - 1, a))}
    return sorted(m for m in months if start < m < end)


def _states(s):
    """Each ``(S point, month)`` of :func:`_every_state_months` on every point of ``s``."""
    labels = s.Data.model_point_table().index
    return [(point_id, d) for key, point_id in zip(point_keys(s), labels)
            for d in _every_state_months(projection(s, key).proj_start(),
                                         projection(s, key).proj_len())]


def _restated(root, s, states):
    """The twins of ``s``'s points and a row in force at each of ``states``, ``(S point,
    month)``, built by the generator out of ``s`` into a copy of the product directory:
    ``(folder, table)``."""
    spec = dataclasses.replace(SPEC, derived=tuple(states), future=())
    table, companions = build_sec_table(spec, s)
    assert companions == {}
    return _sec_inputs(root, table), table


def _states_apart(a, b):
    """The state columns, the count's among them, in which two tables of :func:`_restated`
    differ on the states, ``(S policy, month)``, they share, of which there must be some."""
    both = a.index.intersection(b.index)
    assert len(both), "the two tables share no state"
    return {c for c in ("policy_count", *STATE) if (a.loc[both, c] != b.loc[both, c]).any()}


def _refused_in_force(folder, refs):
    """What ``Data`` and ``proj_len()`` refuse of the table in ``folder``, read with
    ``refs`` set first: ``Data``'s refusal, or each row's ``proj_len()``'s, each by the line
    that names it.  Each row is released once asked (:func:`_release`)."""
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
            _release(model, key)
        return refused
    finally:
        model.close()


def test_every_state_s_reaches_is_accepted_in_force(s_model, spliced, tmp_path):
    """Every state ``WholeLife_US_S`` reaches is a valid opening state (T5).

    ``Data``'s rules and ``proj_len()``'s hold an opening state to what a policy in force
    can be, so they must accept each state the S model reaches: a rule exercised only on
    the rows the other tests choose could refuse a state S reaches elsewhere (D6).  So each
    point of S is restated in force by the generator at the edges of its windows, or with
    ``USLIB_SEC_FULL=1`` at every month of its frame (:func:`_every_state_months`), into
    one table beside the twins: ``Data`` reads it, and no row's ``proj_len()`` refuses it
    (USLIB-SEC-PLAN.md §5.2, T5, precised at M10).  The splice's overlays move four of the
    states S reaches: the count, the paid-up additions at both instants and the dividend
    credited at the anniversary.  They leave alone the loan, which its utilization holds
    to a share of the cash value whatever the loan rate, the accumulation and the premiums
    paid.  The cap's References, the splice's with an A/E of 5, move the count alone.
    Expense inflation moves no state.  So the test runs on each set of inputs on which
    those states differ (precised at M9), and asserts which states each moves:

    * S as shipped, its fifteen points under its own References, the overlays off, as T1
      and the committed rows read it (``s_model``);
    * the splice's, its points and three variants under :data:`SPLICED_REFS`, the overlays
      on (``spliced``);
    * the cap's, its point under :data:`CAPPED_REFS`, whose count falls below 1e-7 before
      the cap binds and is exactly 0 from it, which neither other set reaches.

    ``WholeLife_US_SEC`` refuses no state ``WholeLife_US_S`` reaches, so none is set aside.
    """
    table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                        index_col="point_id")
    capped = mx.read_model(temp_inputs(tmp_path / "capped", model_path(TWIN),
                                       model_points=table.loc[[CAPPED_POINT]]),
                           name=_name("every_capped"))
    try:
        for ref, value in CAPPED_REFS.items():
            setattr(capped.Projection, ref, value)
        sets = {"shipped": (s_model, {}), "spliced": (spliced[0], SPLICED_REFS),
                "capped": (capped, CAPPED_REFS)}
        found, states = {}, {}
        for tag, (s, refs) in sets.items():
            reached = _states(s)
            folder, rows = _restated(tmp_path / tag, s, reached)
            assert len(rows) == len(s.Data.model_point_table()) + len(reached)
            states[tag] = rows.set_index(["source_policy_id", "source_mth"])
            refused = _refused_in_force(folder, refs)
            if refused:
                found[tag] = f"{len(refused)} refused, first: {refused[:5]}"
    finally:
        capped.close()
    assert not found, found
    shipped, splice, cap = states["shipped"], states["spliced"], states["capped"]
    apart = _states_apart(shipped, splice)
    assert apart == {"policy_count", "pua_face_init", "pua_face_prev_anniv_init",
                     "div_prev_anniv_init"}, apart
    apart = _states_apart(splice, cap)
    assert apart == {"policy_count"}, apart
    count = cap["policy_count"]
    assert (count == 0.0).any() and ((count > 0.0) & (count < 1e-7)).any()


# What the contract does not issue, refused by proj_len() as a point past its cover is, as
# (case, the table's edit, the References set, the point, the message, and the frame the
# point projects at the shipped References, or None).  Data reads an issue age as
# WholeLife_US_S does, any finite number, so each reads.  product-spec.md issues level pay
# from age 0, issue_age_min, from which spec_sec.py sizes the compiled caches, so the bound
# is refused just inside it, at -1; and, raised to 46, it refuses the anchor cell's twin,
# issued at 45, which at the shipped 0 projects its 660 months: the Reference is what
# refuses it.  A bound lowered below 0 lets no point project, since no age-keyed table can
# hold a negative age (Data refuses one), so the case that projects is the shipped bound's.
NOT_ISSUED = [
    ("an issue age below 0", _set("issue_age", [2], -1), {}, 2,
     "point_id 2: issue age -1 is below issue_age_min, 0", None),
    ("an issue age below a bound raised to 46", None, {"issue_age_min": 46}, 2,
     "point_id 2: issue age 45 is below issue_age_min, 46", 660),
]


@pytest.mark.parametrize("case, edit, refs, point, message, frame", NOT_ISSUED,
                         ids=[c[0] for c in NOT_ISSUED])
def test_a_point_the_contract_does_not_issue_is_refused_by_proj_len(tmp_path, case, edit,
                                                                    refs, point, message,
                                                                    frame):
    """``proj_len()`` refuses a point issued below ``issue_age_min``, naming it (§6.1).

    ``WholeLife_US_S`` projects a point issued at any age its tables hold, and so would
    modelx here, but the compiled model's caches are sized from the contract, cover from
    ``issue_age_min``, 0, to ``maturity_age`` and the shipped horizon (``spec_sec.py``),
    and a younger point runs past them.  So the frame refuses such a point, naming it, as
    it refuses a point past its cover, and every report with it, in modelx as compiled
    (:data:`NOT_ISSUED`): an issue age of -1, just inside the bound, and the anchor cell's
    twin at 45 once the bound is raised to 46, which projects again at the shipped 0.  A
    bound off by one, or a refusal lost, lets a point through.
    """
    model = _faulty(tmp_path, edit)
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        _refused(_point(model, point).result_cf, message)
        if frame is not None:
            model.Projection.issue_age_min = 0
            assert len(_point(model, point).result_cf()) == frame
    finally:
        model.close()


def test_the_edges_of_each_range_are_accepted(tmp_path):
    """Each value at the edge of the range ``Data`` holds it to reads and projects.

    ``Data`` refuses an amount below 0, a share or a probability outside 0 to 1 and a net
    single premium of 0 or less (:data:`NOT_FINITE`), so the edges themselves must read: a
    face, a participating premium, a cash value, a net level premium and a final-expense
    rate of 0, a loan share of 1, a guaranteed mortality rate of 0 and of 1, and a net
    single premium above 1, a price per unit of face that a negative interest rate gives
    and the purchases divide by, with no upper bound to read.  Each is written at a key a
    committed point reads, and each such point projects finite numbers, reading the value
    written: a range checked with a strict comparison where it should not be, or an upper
    bound on the net single premium, refuses one of them.  The shipped table holds the
    rest of the edges already, a rider premium, a blend target and a loan share of 0.
    """
    def edit(table):
        table = _set("face_amount", [3], 0.0)(table)
        table = _set("annual_premium", [5], 0.0)(table)
        return _set("loan_utilization", [6], 1.0)(table)

    edits = {**_written("mort_table.csv", "mort_rate", 0.0, sex="M", age=54),
             **_written("nsp_table.csv", "nsp", 1.01, sex="M", age=99),
             **_written("cv_table.csv", "cv_per_1000", 0.0, premium_period="TO_100",
                        sex="M", issue_age=45, policy_year=30),
             **_written("np_guar_table.csv", "np_guar_per_1000", 0.0,
                        premium_period="TO_100", sex="F", issue_age=45),
             **_written("premium_rates.csv", "rate_per_1000", 0.0, product="WL_FE_LEVEL",
                        sex="F", issue_age=65)}
    edits["mort_table.csv"] = _then(edits["mort_table.csv"], _written(
        "mort_table.csv", "mort_rate", 1.0, sex="M", age=99)["mort_table.csv"])
    model = _faulty(tmp_path, edit, edits)
    try:
        anchor = _point(model, 1)
        read = {"mort_rate_guar_at(54)": (anchor.mort_rate_guar_at(54), 0.0),
                "mort_rate_guar_at(99)": (anchor.mort_rate_guar_at(99), 1.0),
                "nsp(99)": (anchor.nsp(99), 1.01),
                "cv_pp_anniv(30)": (anchor.cv_pp_anniv(30), 0.0),
                "np_guar()": (_point(model, 10).np_guar(), 0.0),
                "premium_rate()": (_point(model, 13).premium_rate(), 0.0),
                "sum_assured()": (_point(model, 3).sum_assured(), 0.0),
                "annual_premium()": (_point(model, 5).annual_premium(), 0.0),
                "loan_utilization()": (_point(model, 6).loan_utilization(), 1.0)}
        assert {k: v for k, v in read.items() if v[0] != v[1]} == {}
        for label in (1, 3, 5, 6, 10, 13):
            for report in ("result_cf", "result_pols"):
                frame = _point(model, label).cells[report]()
                assert np.isfinite(frame.to_numpy()).all(), (label, report)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Phase 2's decoding, and the reads beyond a table
#
# Data decodes the model point's text into the numbers the projection reads, and turns each
# table into an integer-indexed array or a join (USLIB-SEC-PLAN.md R6, R7).  So Data must
# refuse what it cannot decode, and every value a capped rate, a min or a max reads that is
# not a number in its range, and no read of an array's padding may go unrefused: a numpy
# read beyond a table's extent returns NaN, or, at -1, the last element, where
# WholeLife_US_S's lookup raised KeyError.  Each case is the committed inputs with one
# fault, read from a copy.  The points named are the committed table's: 1, the anchor
# cell, the first point, which reads every table but the final-expense rates; 4, a
# participating point; 11, final expense level, the first point that reads a rate.


def _faulty(tmp_path, table_edit=None, edits=None):
    """WholeLife_US_SEC read from a copy whose table is ``table_edit(_committed())`` and
    whose other inputs ``edits`` changes, as :func:`sec_support.temp_inputs` takes them."""
    table = _committed() if table_edit is None else table_edit(_committed())
    folder = temp_inputs(tmp_path, model_path(SEC), model_points=table,
                         model_point_file=TABLE, edits=edits)
    return mx.read_model(folder, name=_name("faulty"))


def _value_written(column, rows, value):
    """An edit of an input table that writes ``value``, text or a number, into ``column``
    on the rows ``rows(table)`` selects; pandas then reads a column holding text as text."""
    def edit(table):
        cells = table[column].astype(object)
        return table.assign(**{column: cells.where(~rows(table), value)})
    return edit


def _written(file, column, value, **match):
    """``{file: edit}``, the edit writing ``value`` into ``column`` on the rows of ``file``
    whose columns hold what ``match`` gives each, a value or a list of values."""
    def rows(table):
        at = pd.Series(True, index=table.index)
        for name, want in match.items():
            at &= table[name].isin(want if isinstance(want, list) else [want])
        return at
    return {file: _value_written(column, rows, value)}


def _then(first, second):
    """An edit that applies ``first`` and then ``second``."""
    return lambda table: second(first(table))


def _rows_added(file, rows):
    """``{file: edit}``, the edit appending what ``rows(table)`` returns to the table."""
    return {file: lambda table: pd.concat([table, rows(table)], ignore_index=True)}


def _dropped(file, **match):
    """``{file: edit}``, the edit dropping the rows whose columns hold what ``match``
    gives each, as :func:`_written` selects them."""
    def edit(table):
        at = pd.Series(True, index=table.index)
        for name, want in match.items():
            at &= table[name] == want
        return table[~at]
    return {file: edit}


def _repeated(file, **match):
    """``{file: edit}``, the edit appending a second copy of the rows ``match`` selects."""
    return _rows_added(file, lambda table: table[np.logical_and.reduce(
        [table[name] == want for name, want in match.items()])])


def _below(file, sex, value):
    """``{file: edit}``, the edit adding rows for ``sex`` from age -1 to the table's first
    age, each holding ``value``: a schedule that starts below 0 without a gap."""
    def rows(table):
        first = int(table["age"].min())
        column = "nsp" if file == "nsp_table.csv" else "mort_rate"
        return pd.DataFrame({"sex": sex, "age": range(-1, first), column: value,
                             "provenance": "test copy"})
    return _rows_added(file, rows)


CV_SCHEDULE = ("cv_table.csv: the schedule of premium_period TO_100, sex M, issue_age 45 "
               "must run in whole policy years from 1 or more, without a gap or a repeat")
CV_YEAR = {"premium_period": "TO_100", "sex": "M", "issue_age": 45, "policy_year": 30}


def _ages(file):
    """A table's message: the ages of sex M must run without a gap from 18 to 100."""
    return (f"{file}: the ages of sex M must run from 18 to 100 without a gap or a repeat, "
            f"none negative")


# A model point's issue age of 2**53 or more in size, which numpy would read as the least
# int64 once past int64.  A fraction is not refused: it truncates as S's int truncates it
# (test_a_fractional_issue_age_truncates_as_wholelife_us_s_truncates_it).
HUGE_AGE = f"{TABLE}: issue_age must be below 2**53 in size; it is not at point_id "


# What Data cannot decode, or cannot turn into an array, as (case, the table's edit, the
# other inputs' edits, the Data cell that refuses it, its message, and the point whose
# projection meets it, or None).  A projection reads every Data vector it decodes on its
# first month, and each table at its first read of it, so the first point meets every
# refusal but the label's, which only a refusal or a report reads, and the final-expense
# rates', which final expense alone reads.  A key written as text makes pandas read its
# whole column as text, which each check reads by value, refusing the text alone.
UNDECODABLE = [
    ("an issue age past int64", _set("issue_age", [3], 1e30), None, "issue_age",
     HUGE_AGE + "[3]", 1),
    ("issue ages of 2**53 at two points", _set("issue_age", [3, 7], -(2.0 ** 53)), None,
     "issue_age", HUGE_AGE + "[3, 7]", 1),
    ("a label that is not whole", lambda t: t.rename(index={3: 3.5}), None, "point_id",
     f"{TABLE}: point_id must be a whole number; [3.5] is not", None),
    ("a label written as text", lambda t: t.rename(index={3: "3x"}), None, "point_id",
     f"{TABLE}: point_id must be a whole number; ['3x'] is not", None),
    ("an unknown premium period", _set("premium_period", [4], "PAY_15"), None,
     "premium_period_code", f"{TABLE}: premium_period must be TO_100, PAY_10, PAY_20 or "
     f"TO_65; it is not at point_id [4]", 1),
    ("an unknown premium mode", _set("premium_mode", [4, 6], "W"), None, "prem_cycle",
     f"{TABLE}: premium_mode must be A, SA, Q or M; it is not at point_id [4, 6]", 1),
    ("a gap in a cash value schedule", None, _dropped("cv_table.csv", **CV_YEAR),
     "cv_schedules", CV_SCHEDULE, 1),
    ("a repeated policy year", None, _repeated("cv_table.csv", **CV_YEAR),
     "cv_schedules", CV_SCHEDULE, 1),
    ("a policy year that is not whole", None,
     _written("cv_table.csv", "policy_year", 30.5, **CV_YEAR), "cv_schedules",
     CV_SCHEDULE, 1),
    ("a policy year written as text", None,
     _written("cv_table.csv", "policy_year", "30x", **CV_YEAR), "cv_schedule",
     CV_SCHEDULE, 1),
    ("a policy year of 0", None, _rows_added("cv_table.csv", lambda cv: cv[
        (cv["premium_period"] == "TO_100") & (cv["sex"] == "M") & (cv["issue_age"] == 45)
        & (cv["policy_year"] == 1)].assign(policy_year=0)), "cv_year_first",
     CV_SCHEDULE, 1),
    ("a cash value issue age that is not whole", None,
     _written("cv_table.csv", "issue_age", 45.5, **CV_YEAR), "cv_array",
     "cv_table.csv: issue_age must be a whole number; [45.5] is not", 1),
    ("a cash value issue age written as text", None,
     _written("cv_table.csv", "issue_age", "45x", **CV_YEAR), "cv_year_last",
     "cv_table.csv: issue_age must be a whole number; ['45x'] is not", 1),
    ("a gap in the mortality table", None, _dropped("mort_table.csv", sex="M", age=60),
     "mort_schedules", _ages("mort_table.csv"), 1),
    ("a repeated mortality age", None, _repeated("mort_table.csv", sex="M", age=60),
     "mort_table_array", _ages("mort_table.csv"), 1),
    ("a mortality age that is not whole", None,
     _written("mort_table.csv", "age", 54.5, sex="M", age=54), "mort_schedule",
     "mort_table.csv: an age must be a whole number; [54.5] is not", 1),
    ("a mortality age written as text", None,
     _written("mort_table.csv", "age", "54x", sex="M", age=54), "mort_age_first",
     "mort_table.csv: an age must be a whole number; ['54x'] is not", 1),
    ("a negative mortality age", None, _below("mort_table.csv", "M", 0.0003),
     "mort_age_last", "mort_table.csv: the ages of sex M must run from -1 to 100 without "
     "a gap or a repeat, none negative", 1),
    ("a gap in the net single premiums", None, _dropped("nsp_table.csv", sex="M", age=60),
     "nsp_schedules", _ages("nsp_table.csv"), 1),
    ("a repeated net single premium age", None,
     _repeated("nsp_table.csv", sex="M", age=60), "nsp_array", _ages("nsp_table.csv"), 1),
    ("a net single premium age that is not whole", None,
     _written("nsp_table.csv", "age", 54.5, sex="M", age=54), "nsp_schedule",
     "nsp_table.csv: an age must be a whole number; [54.5] is not", 1),
    ("a net single premium age written as text", None,
     _written("nsp_table.csv", "age", "54x", sex="M", age=54), "nsp_age_first",
     "nsp_table.csv: an age must be a whole number; ['54x'] is not", 1),
    ("a negative net single premium age", None, _below("nsp_table.csv", "M", 0.03),
     "nsp_age_last", "nsp_table.csv: the ages of sex M must run from -1 to 100 without a "
     "gap or a repeat, none negative", 1),
    ("a net level premium issue age that is not whole", None,
     _written("np_guar_table.csv", "issue_age", 45.5, premium_period="TO_100", sex="M",
              issue_age=45), "np_guar_rows",
     "np_guar_table.csv: issue_age must be a whole number; [45.5] is not", 1),
    ("a net level premium issue age written as text", None,
     _written("np_guar_table.csv", "issue_age", "45x", premium_period="TO_100", sex="M",
              issue_age=45), "has_np_guar",
     "np_guar_table.csv: issue_age must be a whole number; ['45x'] is not", 1),
    ("a repeated net level premium", None,
     _repeated("np_guar_table.csv", premium_period="TO_100", sex="M", issue_age=45),
     "np_guar_per_1000", "np_guar_table.csv: a net level premium appears more than once "
     "for the premium_period, sex and issue_age [('TO_100', 'M', 45)]", 1),
    ("a rate issue age that is not whole", None,
     _written("premium_rates.csv", "issue_age", 65.5, product="WL_FE_LEVEL", sex="M",
              issue_age=65), "premium_rate_rows",
     "premium_rates.csv: issue_age must be a whole number; [65.5] is not", 11),
    ("a rate issue age written as text", None,
     _written("premium_rates.csv", "issue_age", "65x", product="WL_FE_LEVEL", sex="M",
              issue_age=65), "has_premium_rate",
     "premium_rates.csv: issue_age must be a whole number; ['65x'] is not", 11),
    ("a repeated rate", None,
     _repeated("premium_rates.csv", product="WL_FE_LEVEL", sex="M", issue_age=65),
     "premium_rate_per_1000", "premium_rates.csv: a rate appears more than once for the "
     "product, sex, risk_class and issue_age [('WL_FE_LEVEL', 'M', 'STD_NT', 65)]", 11),
]


@pytest.mark.parametrize("case, table_edit, edits, cell, message, point", UNDECODABLE,
                         ids=[c[0] for c in UNDECODABLE])
def test_what_data_cannot_decode_is_refused_naming_it(tmp_path, case, table_edit, edits,
                                                     cell, message, point):
    """``Data`` refuses a value it cannot decode, or a table its array cannot hold (R6, R7).

    Each case of :data:`UNDECODABLE` is the committed inputs with one fault, read from a
    copy, and the ``Data`` cell refuses it with ``ValueError``, naming every point or the
    schedule at fault, the first time it is read; and the projection of the point named,
    which reads the cell, meets the same refusal.  ``WholeLife_US_S`` met each of these
    only when a projection reached the point or the year: an unknown period in
    ``policy_term``, an unknown mode in ``modal_factor``, and a gap, a repeat or a key
    written otherwise at ``.loc``, as a ``KeyError``, or a second row where one was
    meant.  Each table's check is one ``Data`` cell, which its array, its extents and its
    schedule numbers or join read first, so whichever of them a projection reads first, it
    meets the table's own refusal; the cases name a different one of them each.  And a
    model point's issue age of ``2**53`` or more in size is refused before the cast, which
    would read an age past int64 as the least int64; a fraction is not refused, but
    truncates as ``WholeLife_US_S``'s ``int`` truncates it.  A value that is not a number
    in its range is :data:`NOT_FINITE`'s.
    """
    model = _faulty(tmp_path, table_edit, edits)
    try:
        _refused(model.Data.cells[cell], message)
        if point is not None:
            _refused(_point(model, point).result_cf, message)
    finally:
        model.close()


NAN, INF = float("nan"), float("inf")
POINTS = f"{TABLE}: {{}} must be a number, zero or more; it is not at point_id "
PREMIUM = (f"{TABLE}: annual_premium must be a number, zero or more, or blank off the "
           f"participating design; it is not at point_id ")
SHARE = f"{TABLE}: loan_utilization must be a number from 0 to 1; it is not at point_id "
AGE = f"{TABLE}: issue_age must be a finite number; it is not at point_id "
CV = "cv_table.csv: cv_per_1000 must be a number, zero or more; it is not in "
IN_SCHEDULE = "the schedule of premium_period {}, sex {}, issue_age {}, at policy year {}"
NNLP = ("np_guar_table.csv: np_guar_per_1000 must be a number, zero or more; it is not at "
        "the premium_period, sex and issue_age ")
RATE = ("premium_rates.csv: rate_per_1000 must be a number, zero or more; it is not at the "
        "product, sex, risk_class and issue_age ")
MORT = "mort_table.csv: mort_rate must be a number from 0 to 1; it is not at "
NSP = "nsp_table.csv: nsp must be a number above 0; it is not at "


def _cv(value, years=(30,), period="TO_100", sex="M", ages=(45,)):
    """The edit of *cv_table.csv* writing ``value`` as the cash value at ``years`` of the
    schedules of ``period`` and ``sex`` at each issue age of ``ages``."""
    return _written("cv_table.csv", "cv_per_1000", value, premium_period=period, sex=sex,
                    issue_age=list(ages), policy_year=list(years))


def _nnlp(value, period="TO_100", ages=(45,)):
    """The edit of *np_guar_table.csv* writing ``value`` as the male premium of ``period``
    at each issue age of ``ages``."""
    return _written("np_guar_table.csv", "np_guar_per_1000", value, premium_period=period,
                    sex="M", issue_age=list(ages))


def _rate(value, ages=(65,)):
    """The edit of *premium_rates.csv* writing ``value`` as the male level final-expense
    rate at each issue age of ``ages``."""
    return _written("premium_rates.csv", "rate_per_1000", value, product="WL_FE_LEVEL",
                    sex="M", issue_age=list(ages))


def _q(value, ages=(54,), sexes=("M",)):
    """The edit of *mort_table.csv* writing ``value`` as the rate at ``ages`` of
    ``sexes``."""
    return _written("mort_table.csv", "mort_rate", value, sex=list(sexes), age=list(ages))


def _nsp(value, ages=(55,), sexes=("M",)):
    """The edit of *nsp_table.csv* writing ``value`` as the premium at ``ages`` of
    ``sexes``."""
    return _written("nsp_table.csv", "nsp", value, sex=list(sexes), age=list(ages))


def _amounts(column):
    """:data:`NOT_FINITE`'s five cases of a column of amounts of the model point table."""
    message = POINTS.format(column)
    return [(f"a blank {column}", _set(column, [3], NAN), None, column, message + "[3]",
             1),
            (f"a {column} written as text", _set(column, [3], "x"), None, column,
             message + "[3]", 1),
            (f"an infinite {column}", _set(column, [3], INF), None, column,
             message + "[3]", 1),
            (f"a negative {column}", _set(column, [3], -1.0), None, column,
             message + "[3]", 1),
            (f"a blank {column} at two points", _set(column, [3, 7], NAN), None, column,
             message + "[3, 7]", 1)]


# A value a cap, a min or a max reads that is not a number in its range, as (case, the
# table's edit, the other inputs' edits, the Data cell that refuses it, its message, and
# the point whose projection meets it).  mort_rate caps the annual rate with min, and the
# dividend's floor, the REDUCE_PREM offset, the term-blend gap and its cap and the
# paid-up-additions purchases bound theirs with min and max, which through the dividend
# reach every amount and rate below.  Each column is checked whole when its array is first
# read, so a value no point reads, the cash value of a schedule no point carries, the net
# level premium of a period none pays or the rate at an age none is issued at, is refused
# at the first read of the table, by the first point that reads it.  Each refusal names
# every point, line or schedule at fault, so each column has a case that faults two: a
# refusal that named the first alone, or checked only what a point reads, would fail one.
# Each range is read at its edges: a value just outside each bound here, the bounds
# themselves in test_the_edges_of_each_range_are_accepted.
NOT_FINITE = [
    ("a blank issue age", _set("issue_age", [3], NAN), None, "issue_age", AGE + "[3]", 1),
    ("an issue age written as text", _set("issue_age", [3], "x"), None, "issue_age",
     AGE + "[3]", 1),
    ("an infinite issue age", _set("issue_age", [3], INF), None, "issue_age", AGE + "[3]",
     1),
    ("blank issue ages at two points", _set("issue_age", [3, 7], NAN), None, "issue_age",
     AGE + "[3, 7]", 1),
    *_amounts("face_amount"),
    ("a blank participating premium", _set("annual_premium", [3], NAN), None,
     "annual_premium", PREMIUM + "[3]", 1),
    ("a participating premium written as text", _set("annual_premium", [3], "x"), None,
     "annual_premium", PREMIUM + "[3]", 1),
    ("an infinite participating premium", _set("annual_premium", [3], INF), None,
     "annual_premium", PREMIUM + "[3]", 1),
    ("a negative participating premium", _set("annual_premium", [3], -1.0), None,
     "annual_premium", PREMIUM + "[3]", 1),
    ("a final-expense premium written as text", _set("annual_premium", [11], "x"), None,
     "annual_premium", PREMIUM + "[11]", 1),
    ("an infinite final-expense premium", _set("annual_premium", [11], INF), None,
     "annual_premium", PREMIUM + "[11]", 1),
    ("blank participating premiums at two points", _set("annual_premium", [3, 7], NAN),
     None, "annual_premium", PREMIUM + "[3, 7]", 1),
    *_amounts("pua_rider_premium"),
    *_amounts("term_blend_target"),
    ("a blank loan share", _set("loan_utilization", [3], NAN), None, "loan_utilization",
     SHARE + "[3]", 1),
    ("a loan share written as text", _set("loan_utilization", [3], "x"), None,
     "loan_utilization", SHARE + "[3]", 1),
    ("an infinite loan share", _set("loan_utilization", [3], INF), None,
     "loan_utilization", SHARE + "[3]", 1),
    ("a loan share below 0", _set("loan_utilization", [3], -0.01), None,
     "loan_utilization", SHARE + "[3]", 1),
    ("a loan share above 1", _set("loan_utilization", [6], 1.01), None,
     "loan_utilization", SHARE + "[6]", 1),
    ("loan shares above 1 at two points", _set("loan_utilization", [3, 6], 1.01), None,
     "loan_utilization", SHARE + "[3, 6]", 1),
    ("a blank cash value", None, _cv(NAN), "cv_schedules",
     CV + IN_SCHEDULE.format("TO_100", "M", 45, [30]), 1),
    ("a cash value written as text", None, _cv("x"), "cv_array",
     CV + IN_SCHEDULE.format("TO_100", "M", 45, [30]), 1),
    ("an infinite cash value", None, _cv(INF), "cv_year_first",
     CV + IN_SCHEDULE.format("TO_100", "M", 45, [30]), 1),
    ("a negative cash value", None, _cv(-1.0), "cv_schedule",
     CV + IN_SCHEDULE.format("TO_100", "M", 45, [30]), 1),
    ("blank cash values in two policy years", None, _cv(NAN, years=(30, 40)),
     "cv_year_last", CV + IN_SCHEDULE.format("TO_100", "M", 45, [30, 40]), 1),
    ("a blank cash value of a schedule no point carries", None,
     _cv(NAN, period="PAY_20", sex="F"), "cv_schedules",
     CV + IN_SCHEDULE.format("PAY_20", "F", 45, [30]), 1),
    ("blank cash values in two schedules", None, _cv(NAN, years=(10,), ages=(45, 65)),
     "cv_schedules", CV + IN_SCHEDULE.format("TO_100", "M", 45, [10]) + ", nor in "
     + IN_SCHEDULE.format("TO_100", "M", 65, [10]), 1),
    ("a blank net level premium", None, _nnlp(NAN), "np_guar_rows",
     NNLP + "[('TO_100', 'M', 45)]", 1),
    ("a net level premium written as text", None, _nnlp("x"), "np_guar_per_1000",
     NNLP + "[('TO_100', 'M', 45)]", 1),
    ("an infinite net level premium", None, _nnlp(INF), "has_np_guar",
     NNLP + "[('TO_100', 'M', 45)]", 1),
    ("a negative net level premium", None, _nnlp(-1.0), "np_guar_rows",
     NNLP + "[('TO_100', 'M', 45)]", 1),
    ("a blank net level premium of a period no point pays", None, _nnlp(NAN, "PAY_20"),
     "np_guar_rows", NNLP + "[('PAY_20', 'M', 45)]", 1),
    ("blank net level premiums at two issue ages", None, _nnlp(NAN, ages=(45, 65)),
     "np_guar_rows", NNLP + "[('TO_100', 'M', 45), ('TO_100', 'M', 65)]", 1),
    ("a blank rate", None, _rate(NAN), "premium_rate_rows",
     RATE + "[('WL_FE_LEVEL', 'M', 'STD_NT', 65)]", 11),
    ("a rate written as text", None, _rate("x"), "premium_rate_per_1000",
     RATE + "[('WL_FE_LEVEL', 'M', 'STD_NT', 65)]", 11),
    ("an infinite rate", None, _rate(INF), "has_premium_rate",
     RATE + "[('WL_FE_LEVEL', 'M', 'STD_NT', 65)]", 11),
    ("a negative rate", None, _rate(-1.0), "premium_rate_rows",
     RATE + "[('WL_FE_LEVEL', 'M', 'STD_NT', 65)]", 11),
    ("a blank rate at an age no point is issued at", None, _rate(NAN, (85,)),
     "premium_rate_rows", RATE + "[('WL_FE_LEVEL', 'M', 'STD_NT', 85)]", 11),
    ("blank rates at two issue ages", None, _rate(NAN, (65, 85)), "premium_rate_rows",
     RATE + "[('WL_FE_LEVEL', 'M', 'STD_NT', 65), ('WL_FE_LEVEL', 'M', 'STD_NT', 85)]",
     11),
    ("a blank mortality rate", None, _q(NAN), "mort_schedules", MORT + "sex M, age [54]",
     1),
    ("a mortality rate written as text", None, _q("x"), "mort_table_array",
     MORT + "sex M, age [54]", 1),
    ("an infinite mortality rate", None, _q(INF), "mort_schedule",
     MORT + "sex M, age [54]", 1),
    ("a mortality rate below 0", None, _q(-0.01), "mort_age_first",
     MORT + "sex M, age [54]", 1),
    ("a mortality rate above 1", None, _q(1.01, (100,)), "mort_age_last",
     MORT + "sex M, age [100]", 1),
    ("blank mortality rates at two ages", None, _q(NAN, (54, 60)), "mort_schedules",
     MORT + "sex M, age [54, 60]", 1),
    ("blank mortality rates of both sexes", None, _q(NAN, sexes=("F", "M")),
     "mort_schedules", MORT + "sex F, age [54], nor at sex M, age [54]", 1),
    ("a blank net single premium", None, _nsp(NAN), "nsp_schedules",
     NSP + "sex M, age [55]", 1),
    ("a net single premium written as text", None, _nsp("x"), "nsp_array",
     NSP + "sex M, age [55]", 1),
    ("an infinite net single premium", None, _nsp(INF), "nsp_schedule",
     NSP + "sex M, age [55]", 1),
    ("a net single premium of 0", None, _nsp(0.0), "nsp_age_first",
     NSP + "sex M, age [55]", 1),
    ("a negative net single premium", None, _nsp(-0.5), "nsp_age_last",
     NSP + "sex M, age [55]", 1),
    ("blank net single premiums at two ages", None, _nsp(NAN, (55, 60)), "nsp_schedules",
     NSP + "sex M, age [55, 60]", 1),
    ("blank net single premiums of both sexes", None, _nsp(NAN, sexes=("F", "M")),
     "nsp_schedules", NSP + "sex F, age [55], nor at sex M, age [55]", 1),
]


@pytest.mark.parametrize("case, table_edit, edits, cell, message, point", NOT_FINITE,
                         ids=[c[0] for c in NOT_FINITE])
def test_a_value_a_bound_reads_is_refused_unless_it_is_a_number_in_its_range(
        tmp_path, case, table_edit, edits, cell, message, point):
    """``Data`` refuses a value a cap, a ``min`` or a ``max`` reads outside its range.

    Each case of :data:`NOT_FINITE` is the committed inputs with one such value, or two in
    one column, read from a copy: blank, text or infinite, or outside its range, an amount
    below 0, a share or a probability outside 0 to 1, a net single premium of 0 or less.
    The ``Data`` cell refuses it with ``ValueError`` the first time it is read, naming the
    file, the column and every line, schedule or point at fault, and the projection of the
    point named, which reads the cell, meets the same refusal.  No other rule refuses the
    copy: every other ``Data`` cell reads, or meets this refusal through the check it
    reads.

    Without these refusals the cap reads an infinite rate as certain death, the ``max``
    and ``min`` bounds read an infinite amount as their bound, a blank or infinite issue
    age reads as the least int64, and a text value raises numpy's error, or ``int``'s,
    naming nothing.  ``WholeLife_US_S`` met each only when a projection reached it, and
    projected NaN, an infinity or a bound from the rest, without a word.
    """
    model = _faulty(tmp_path, table_edit, edits)
    try:
        _refused(model.Data.cells[cell], message)
        for name, cells in model.Data.cells.items():
            try:
                cells()
            except Exception as err:            # this case's refusal alone may be met
                assert message in str(err), f"Data.{name}: {_raised(err)}"
        _refused(_point(model, point).result_cf, message)
    finally:
        model.close()


def _beyond():
    """A table and edits whose points read beyond the tables, as (table, edits).

    The committed table with point 2, participating, issued at 46, which no cash value
    schedule and no net level premium is priced at; point 11, final expense level, at 66,
    which no rate is priced at; and point 3 of a sex the mortality and net single premium
    tables lack; and the anchor cell's cash value schedule, TO_100, M, 45, cut at policy
    year 50.
    """
    table = _set("issue_age", [2], 46)(_committed())
    table = _set("issue_age", [11], 66)(table)
    table = _set("sex", [3], "X")(table)
    cut = {"cv_table.csv": lambda cv: cv[~(
        (cv["premium_period"] == "TO_100") & (cv["sex"] == "M") & (cv["issue_age"] == 45)
        & (cv["policy_year"] > 50))]}
    return table, cut


# The reads beyond a table in _beyond's copy, as (point, cell, arguments, the message after
# the point's label, or None for a value read inside the guard).  A cell that reads a padded
# array checks the key against both ends of the point's schedule first.
BEYOND = [
    (1, "mort_rate_guar_at", (101,), "mort_table.csv has no rate at attained age 101"),
    (1, "mort_rate_guar_at", (17,), "mort_table.csv has no rate at attained age 17"),
    (1, "nsp", (101,), "nsp_table.csv has no net single premium at attained age 101"),
    (1, "nsp", (17,), "nsp_table.csv has no net single premium at attained age 17"),
    (1, "cv_pp_anniv", (51,), "cv_table.csv has no cash value for policy year 51"),
    (2, "cv_pp_anniv", (1,), "cv_table.csv has no cash value for policy year 1"),
    (2, "np_guar", (), "np_guar_table.csv has no np_guar_per_1000 for its premium_period, "
     "sex and issue_age"),
    (11, "premium_rate", (), "premium_rates.csv has no rate_per_1000 for its product, sex, "
     "risk_class and issue_age"),
    (3, "mort_rate_guar_at", (54,), "mort_table.csv has no rate at attained age 54"),
    (3, "nsp", (54,), "nsp_table.csv has no net single premium at attained age 54"),
]


def test_a_read_beyond_a_table_is_refused_naming_its_point(tmp_path):
    """The one cell that reads each padded array or join refuses a key the table lacks.

    ``mort_rate_guar_at``, ``nsp`` and ``cv_pp_anniv`` check the age or the policy year
    against both ends of the point's schedule first, and ``premium_rate`` and ``np_guar``
    the flag beside their join, and each raises ``ValueError`` naming the point and the
    key, where ``WholeLife_US_S``'s lookup raised ``KeyError`` (:data:`BEYOND`, on
    :func:`_beyond`'s copy): ages either side of the guaranteed mortality and the net
    single premiums; a year past a cash value schedule cut short; a participating point
    issued at an age with no schedule and no net level premium, a final-expense point at
    an age with no rate, and a point of a sex with no schedule; and each such point's
    projection meets a refusal, naming it.  Without the checks each read would return
    the array's padding, or a join's NaN.  ``cv_pp_anniv`` returns 0.0 at policy year 0
    and below, where there is no cash value, before it reads.

    The padding is NaN, as the ``Data`` docstrings say, so that a read past a check, were
    one lost, would make every number after it NaN rather than another schedule's value:
    row 0 of each array, the column of policy year 0, the ages below each schedule's first
    and every key outside its extents; and nothing inside them.
    """
    table, edits = _beyond()
    model = _faulty(tmp_path, lambda _: table, edits)
    try:
        found = []
        for label, cell, args, message in BEYOND:
            proj = _point(model, label)
            with pytest.raises(Exception) as excinfo:
                proj.cells[cell](*args)
            text = str(excinfo.value)
            if f"ValueError: point_id {label}: {message}" not in text:
                found.append(f"{cell}{args} on point {label}: {_raised(excinfo.value)}")
        assert not found, found
        anchor = _point(model, 1)
        assert [anchor.cv_pp_anniv(y) for y in (-1, 0)] == [0.0, 0.0]
        for label in (2, 3, 11):
            _refused(_point(model, label).result_cf, f"point_id {label}: ")
        data = model.Data
        for array, first, last, schedule in (
                (data.mort_table_array(), data.mort_age_first(), data.mort_age_last(),
                 anchor.mort_schedule()),
                (data.nsp_array(), data.nsp_age_first(), data.nsp_age_last(),
                 anchor.nsp_schedule()),
                (data.cv_array(), data.cv_year_first(), data.cv_year_last(),
                 anchor.cv_schedule())):
            assert np.isnan(array[0]).all() and len(array) == len(first) == len(last)
            for s in range(1, len(array)):
                inside = range(first[s], last[s] + 1)
                outside = [k for k in range(array.shape[1]) if k not in inside]
                assert np.isnan(array[s, outside]).all(), s
                assert not np.isnan(array[s, first[s]:last[s] + 1]).any(), s
            assert schedule > 0
        assert np.isnan(data.cv_array()[:, 0]).all()
        assert data.cv_year_last()[anchor.cv_schedule()] == 50
        assert data.mort_table_array().shape == data.nsp_array().shape == (3, 101)
        assert (data.mort_age_first()[1:] == 18).all()
    finally:
        model.close()


def test_a_key_written_as_a_float_reads_as_wholelife_us_s_reads_it(sec_model, tmp_path):
    """A table's key written ``45.0`` is the key 45, as ``WholeLife_US_S``'s lookups match.

    pandas reads a column as floats as soon as one of its cells is written so, or is
    blank, and ``WholeLife_US_S``'s ``.loc`` matches 45 against 45.0, so its tables project
    the same with their keys written either way.  ``Data`` reads every key by its value
    too: with the cash values' issue ages and policy years, the mortality and net single
    premium ages, the net level premiums' and the rates' issue ages and the model points'
    issue ages all written as floats, and so read, the anchor cell, final expense level
    and graded and the loan point in force each project exactly the committed model's
    ``result_cf`` and ``result_pols``.  A key that is not a whole number is refused
    (:data:`UNDECODABLE`).
    """
    def floats(*columns):
        return lambda df: df.assign(**{c: df[c].astype(float) for c in columns})

    edits = {"cv_table.csv": floats("issue_age", "policy_year"),
             "mort_table.csv": floats("age"), "nsp_table.csv": floats("age"),
             "np_guar_table.csv": floats("issue_age"),
             "premium_rates.csv": floats("issue_age")}
    model = _faulty(tmp_path, floats("issue_age"), edits)
    try:
        data = model.Data
        assert data.model_point_table()["issue_age"].dtype == float
        for table, level in ((data.cv_table(), "policy_year"),
                             (data.cv_table(), "issue_age"), (data.mort_table(), "age"),
                             (data.nsp_table(), "age"), (data.np_guar_table(), "issue_age"),
                             (data.premium_rates(), "issue_age")):
            assert table.index.get_level_values(level).dtype == float, level
        for label in (1, 11, 12, _label(_committed(), "derived", 6, 114)):
            mine, base = _point(model, label), _point(sec_model, label)
            for report in ("result_cf", "result_pols"):
                pd.testing.assert_frame_equal(mine.cells[report](), base.cells[report](),
                                              check_exact=True)
    finally:
        model.close()


def test_a_fractional_issue_age_truncates_as_wholelife_us_s_truncates_it(tmp_path):
    """A model point's issue age of 45.5 is 45, and -0.5 is 0, as ``WholeLife_US_S`` reads.

    ``WholeLife_US_S`` and Phase 1 take ``int`` of the issue age, which truncates a
    fraction toward zero, and Phase 2 changes no number (D2), so ``Data.issue_age``
    truncates too; it refuses only an age of ``2**53`` or more, which numpy would read as
    the least int64 (:data:`UNDECODABLE`).  On a copy whose anchor-cell twin, in force at
    S's month 108, is issued at 45.5, the twin reads 45 and must be S's point 1, issued at
    45, from that month on in every cell, as the splice compares it
    (:func:`_continues_s`).  And a point issued at -0.5 reads 0, the youngest issue age
    the contract admits, and ``proj_len()`` issues it, a 1,200-month cover issued now, as
    ``WholeLife_US_S`` would project it at 0.
    """
    committed = _committed()
    twin = _label(committed, "twin", 1, 108)
    born = _label(committed, "twin", 4, 0)
    table = _set("issue_age", [born], -0.5)(_set("issue_age", [twin], 45.5)(committed))
    s = mx.read_model(model_path(TWIN), name=_name("s_fraction"))
    sec = mx.read_model(_sec_inputs(tmp_path, table), name=_name("fraction"))
    try:
        theirs, mine = _point(s, 1), _point(sec, twin)
        assert mine.age_at_entry() == 45
        _sweep_s(theirs)
        assert _continues_s(theirs, mine, 108) == []
        young = _point(sec, born)
        assert (young.age_at_entry(), young.proj_len()) == (0, 1200)
    finally:
        sec.close()
        s.close()


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_table_is_what_s_generates(s_model):
    """``model_point_table_sec.csv`` is what WholeLife_US_S and its table generate today.

    Every row and column, the text cells and the seven opening-state columns included: an
    edit to an S row the table copies or derives from, or to an S formula a row's state is
    read from, fails here until ``python tools/gen_sec_points.py WholeLife_US_SEC``
    regenerates it, in the same commit.  Text and integers compare exactly, and a float by
    its value, to 1e-12, because the text the writer picks for a computed float depends on
    the platform's parser (§5.2).
    """
    assert check_generated(SEC, s_model=s_model) == []


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_two_clocks_on_the_shipped_points(sec_model):
    """``t`` counts from the valuation date; ``duration_mth(t)`` from issue (D3, D4).

    On a twin of S's new business the two coincide, and its policies enter as new business
    at ``t = 0``.  The worked example's point, in force 108 months, is in policy year 10 at
    attained age 54 at ``t = 0``, reaches its tenth anniversary at ``t = 11``, S's month
    119, and has 552 months of cover left.  The loan point valued six months into its tenth
    year pays nothing until its next anniversary, ``t = 6``.  The point issued three months
    on has nothing in force and nothing to do before ``t = 3``, and a frame of 663 months.
    The point in its last covered month has a one-month frame, on an anniversary, in which
    its survivors mature.

    ``pols_if_at``'s ``BEF_MAT`` is ``WholeLife_US_S``'s: the count after the month's
    surrenders, at its end, and not ``basiclife.BasicTerm_SE``'s count at its start, before
    the month's maturities, which a formula ported from it might read the name as (D5).
    And a timing neither model knows is refused rather than answered with another count.
    """
    twin = _row(sec_model, "twin", 2, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 659)] == [0, 1, 659]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0), twin.pols_if(0)) == (
        0, 0.0, 1.0, 1.0)
    assert (twin.anniv_mth(0), twin.maturity_mth(), twin.proj_len()) == (11, 660, 660)
    anchor = _row(sec_model, "twin", 1, 108)
    assert (anchor.duration_mth(0), anchor.duration(0), anchor.policy_year(0),
            anchor.age(0)) == (108, 9, 10, 54)
    assert (anchor.anniv_mth(0), anchor.maturity_mth(), anchor.proj_len()) == (11, 660, 552)
    assert anchor.is_active(551) and not anchor.is_active(552)
    assert anchor.pols_if(0) == anchor.pols_if_init() == anchor.policy_count() == 1.0
    assert (anchor.premium_pp(0), anchor.is_anniv(11), anchor.age_anniv(11)) == (
        1800.0, True, 55)
    loan = _row(sec_model, "derived", 6, 114)
    assert (loan.duration_mth(0), loan.policy_year(0), loan.age(0), loan.anniv_mth(0)) == (
        114, 10, 54, 5)
    assert [loan.premium_pp(t) for t in range(7)] == [0.0] * 6 + [1800.0]
    assert (loan.is_anniv(5), loan.policy_year(6), loan.age(6)) == (True, 11, 55)
    fut = _row(sec_model, "future", 2, -3)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-3, 3, 663)
    assert not fut.is_active(2) and fut.is_active(3)
    assert (fut.pols_if_init(), fut.pols_new_biz(3), fut.pols_if(3)) == (0.0, 1.0, 1.0)
    assert (fut.anniv_mth(3), fut.premium_pp(3)) == (14, 1800.0)
    last = _row(sec_model, "derived", 5, 659)
    assert (last.proj_len(), last.age(0), last.policy_year(0), last.is_anniv(0)) == (
        1, 99, 55, True)
    assert last.pols_maturity(0) > 0.0 and last.pols_if_at(1, last.BEF_NB) == 0.0
    surr = anchor.pols_if_at(0, anchor.BEF_SURR)
    assert anchor.pols_if_at(0, anchor.BEF_MAT) == surr * (1 - anchor.lapse_rate_mth(0))
    assert anchor.pols_if_at(0, anchor.BEF_MAT) < surr < anchor.pols_if(0)
    _refused(lambda: anchor.pols_if_at(0, anchor.AFT_DECR + 1), "invalid timing")


def test_the_worked_examples_pre_frame_values_are_the_opening_state(sec_model, s_model):
    """S's worked example reads four values before its frame; here they are opening state.

    ``WholeLife_US_S`` opens its point 1 at month 108, and its goldens read the paid-up
    additions, the loan, the cash value and the paid-up-additions cash value entering it
    at month 107, before its frame.  On the twin those are the model point's opening
    state at ``t = 0``: ``pua_face_init`` and ``pua_face_prev_anniv_init``, the notes'
    prior 4,100, one value on an anniversary; ``loan_bal_init``, 0; the schedule's
    ``cv_pp_anniv(9)``, 9,500, the cash value entering policy year 10; and the additions
    at the anniversary valued at ``NSP_54``.  From the valuation date on the twin is S's
    point from month 108, at the shipped assumptions, in every cell but those expense
    inflation moves, which carries the rest of the worked example over: the dividend steps,
    the purchase, the death benefit and the surrender value.

    With the PUA-block dividend on, the first anniversary's block dividend reads the
    additions at the anniversary that opened the year, and is the notes' parenthetical,
    ``0.02 PUACV + 0.00096 (PUAF - PUACV)``, 35.331623.
    """
    p, s = _row(sec_model, "twin", 1, 108), _point(s_model, 1)
    assert p.pua_face_init() == 4100.0 == s.pua_face(107)
    assert p.pua_face_prev_anniv_init() == 4100.0
    assert p.loan_bal_init() == 0.0 == s.loan_bal(107)
    assert p.loan_bal_prev_anniv_init() == 0.0
    assert p.cv_pp_anniv(p.duration(0)) == 9500.0 == pytest.approx(s.cv_pp(107), rel=1e-12)
    assert p.pua_face_prev_anniv_init() * p.nsp(p.age(0)) == pytest.approx(
        s.pua_cv(107), rel=1e-12)
    assert _continues_s(s, p, 108) == []
    fresh = mx.read_model(model_path(SEC), name=_name("pua_div"))
    try:
        fresh.Projection.pua_div_on = True
        a = _row(fresh, "twin", 1, 108)
        puaf = a.pua_face_prev_anniv_init()
        puacv = puaf * a.nsp(a.age(0))
        assert a.div_pua(11) == pytest.approx(0.02 * puacv + 0.00096 * (puaf - puacv),
                                              rel=1e-12)
        assert a.div_pua(11) == pytest.approx(35.331623, abs=1e-6)
    finally:
        fresh.close()


def test_a_policy_valued_mid_year_reads_the_anniversary_before_it(sec_model, s_model):
    """Valued mid-year, a policy's annual quantities read the year's anniversary values.

    The loan point valued at 114 owes 2,070.00 at the valuation date and owed 1,900.00 at
    the anniversary that opened its tenth year, six months before.  The interest that
    capitalizes at the next anniversary, ``t = 5``, is the year's rate on the 1,900.00,
    114.00, and month 0's advance closes the gap between the 2,070.00 and the loan the
    model holds at 20% of the cash value from then on, as S's month 114 does.  With a loan
    rate apart from the dividend rate, the year's interest margin credits the anniversary
    loan at the loan rate, which the shipped rates hide, and it is the anniversary's
    alone: in the months either side it is zero, as the dividend it is a margin of is.

    The funded blend valued at 78, before its crossover, carries 106,074.52 of paid-up
    additions at the valuation date against 93,241.47 at the anniversary.  The one-year-term
    layer of the year under way was bought on the anniversary value: 6,758.53, the whole
    gap to the target face, the dividend covering it, where the current value would leave
    none.  Its death benefit is the face, the additions entering the month and the layer,
    S's at month 78.

    Both rows are S's points from their months on in every cell but those inflation moves.
    Summed into policy years, the loan point's table opens at year 10 with the rest of that
    year, ``t = 0 .. 5``, counting the policies in force at the valuation date, and from
    year 11 on it is S's.  Each compares to 1e-9 relative with no absolute floor but on the
    residuals, as the splice does (:func:`_compare`).
    """
    loan, s6 = _row(sec_model, "derived", 6, 114), _point(s_model, 6)
    assert (loan.loan_bal_prev_anniv_init(), loan.loan_bal_init()) == (1900.0, 2070.0)
    assert loan.loan_int(5) == pytest.approx(114.0, rel=1e-12)
    assert loan.loan_draw(0) == pytest.approx(loan.loan_bal(0) - loan.loan_bal_init(),
                                              rel=1e-12)
    assert loan.loan_draw(0) == pytest.approx(s6.loan_draw(114), rel=1e-12)
    assert _continues_s(s6, loan, 114) == []
    blend, s8 = _row(sec_model, "derived", 8, 78), _point(s_model, 8)
    gap = blend.term_blend_target() - blend.sum_assured() - blend.pua_face_prev_anniv_init()
    assert blend.pua_face_init() == pytest.approx(106074.52, abs=0.005)
    assert blend.pua_face_prev_anniv_init() == pytest.approx(93241.47, abs=0.005)
    assert blend.oyt_face(0) == gap == pytest.approx(6758.53, abs=0.005)
    assert blend.term_blend_target() - blend.sum_assured() - blend.pua_face_init() < 0.0
    assert blend.claim_pp(0, blend.DEATH) == pytest.approx(
        blend.sum_assured() + blend.pua_face_init() + gap, rel=1e-12)
    assert blend.claim_pp(0, blend.DEATH) == pytest.approx(s8.claim_pp(78, "DEATH"),
                                                           rel=1e-12)
    assert _continues_s(s8, blend, 78) == []
    ann, s_ann = loan.result_cf_annual(), s6.result_cf_annual()
    assert list(ann.index) == list(range(10, 56))
    rest = loan.result_cf().loc[0:5].drop(columns="pols_if").sum()
    pd.testing.assert_series_equal(ann.loc[10].drop("pols_if"), rest, check_names=False)
    assert ann.loc[10, "pols_if"] == loan.pols_if(0)
    cols = [c for c in ann.columns if c not in INFLATED]
    pd.testing.assert_frame_equal(ann.loc[11:, cols], s_ann.loc[11:, cols],
                                  rtol=1e-9, atol=0.0)
    fresh = mx.read_model(model_path(SEC), name=_name("loan_rate"))
    try:
        fresh.Projection.int_rate_loan = 0.08
        f = _row(fresh, "derived", 6, 114)
        fund = f.cv_pp_anniv(9) + f.np_guar()
        assert f.div_int(5) == pytest.approx(0.02 * (fund - 1900.0) + 0.04 * 1900.0,
                                             rel=1e-12)
        assert f.div_int(0) == f.div_int(4) == f.div_int(6) == 0.0
        assert f.loan_int(5) == pytest.approx(0.08 * 1900.0, rel=1e-12)
    finally:
        fresh.close()


def test_the_dividend_options_carry_their_state_in_force(sec_model, s_model, tmp_path):
    """REDUCE_PREM reads last year's dividend, and ACCUM carries its balance (§7.2).

    The two S points that do not reproduce from S's own in-force state, valued on the
    anniversary that opens policy year 10.  The REDUCE_PREM point's premium at ``t = 0`` is
    net of the dividend credited at the anniversary before the valuation date,
    1,800.00 - 288.66 = 1,511.34, and the ACCUM point's balance of 1,766.74 accrues a
    month's interest at ``t = 0``.  Both are then S's points from month 108 on, in every
    cell but those inflation moves.  Zeroed, as ``WholeLife_US_S`` assumes for its in-force
    point, the premium is the whole 1,800.00 and the maturity claim falls by 1,060.82: the
    re-opening experiment's two findings.
    """
    rpd, accum = _row(sec_model, "derived", 5, 108), _row(sec_model, "derived", 4, 108)
    assert rpd.div_prev_anniv_init() == 288.66
    assert rpd.premium_net_pp(0) == pytest.approx(1511.34, abs=1e-9)
    assert accum.div_accum_init() == pytest.approx(1766.737522, abs=1e-6)
    assert accum.div_accum(0) == pytest.approx(accum.div_accum_init() * 1.06 ** (1 / 12),
                                               rel=1e-12)
    for p, row in ((5, rpd), (4, accum)):
        assert _continues_s(_point(s_model, p), row, 108) == []
    zeroed = _committed()
    zeroed.loc[_label(zeroed, "derived", 5, 108), "div_prev_anniv_init"] = 0.0
    zeroed.loc[_label(zeroed, "derived", 4, 108), "div_accum_init"] = 0.0
    model = mx.read_model(_sec_inputs(tmp_path, zeroed), name=_name("zeroed"))
    try:
        assert _row(model, "derived", 5, 108).premium_net_pp(0) == 1800.0
        last = accum.proj_len() - 1
        gap = (accum.claims_maturity(last)
               - _row(model, "derived", 4, 108).claims_maturity(last))
        assert gap == pytest.approx(1060.82, abs=0.005)
    finally:
        model.close()


def test_the_graded_benefit_reads_the_premiums_paid_before_the_valuation_date(
        sec_model, s_model, tmp_path):
    """Inside the graded years the death benefit is 110% of every premium paid since issue.

    The graded final-expense point valued 18 months after issue has paid two annual
    premiums of 1,581.00, at months 0 and 12, which is its ``prem_cum_init``, and owes none
    at ``t = 0``.  A natural-cause death then pays 110% of the 3,162.00 and an accidental
    one the face, blended by the 3% accidental share: 0.97 x 1.1 x 3,162 + 0.03 x 15,000 =
    3,823.854.  From ``t = 6``, policy year 3, the benefit is the face.  The row is S's
    point from month 18 on, in every cell but those inflation moves.  Zeroed, the premiums
    paid before the valuation date are lost and the benefit is the accidental share alone,
    450.00.
    """
    p = _row(sec_model, "derived", 12, 18)
    assert p.prem_cum_init() == 3162.0 == 2 * p.premium_pp_ann(0)
    assert p.prem_cum(0) == 3162.0 and p.premium_pp(0) == 0.0
    assert p.claim_pp(0, p.DEATH) == pytest.approx(3823.854, abs=1e-9)
    assert (p.policy_year(5), p.policy_year(6)) == (2, 3)
    assert p.claim_pp(5, p.DEATH) < p.claim_pp(6, p.DEATH) == 15000.0
    assert _continues_s(_point(s_model, 12), p, 18) == []
    zeroed = _set("prem_cum_init", [_label(_committed(), "derived", 12, 18)], 0.0)
    model = _read_edited(tmp_path, zeroed)
    try:
        graded = _row(model, "derived", 12, 18)
        assert graded.claim_pp(0, graded.DEATH) == pytest.approx(450.0, abs=1e-9)
    finally:
        model.close()


def test_the_last_dividend_reaches_maturity_in_force(sec_model, s_model):
    """Valued in its last covered month, a REDUCE_PREM policy still delivers its dividend.

    The frame is one row.  The dividend credited at ``t = 0``, the final anniversary, is
    S's 2,030.14 at its month 659: there is no next premium to offset, so it buys paid-up
    additions at ``NSP_100 = 1`` and reaches the maturity benefit, face plus additions.
    Nobody surrenders in the final policy year, every survivor matures, and nothing is
    carried past the frame.
    """
    p, s = _row(sec_model, "derived", 5, 659), _point(s_model, 5)
    assert p.proj_len() == 1 and list(p.result_cf().index) == [0]
    assert p.div_credited(0) == pytest.approx(2030.14, abs=0.005)
    assert p.div_credited(0) == pytest.approx(s.div_credited(659), rel=1e-12)
    assert p.nsp(p.age_anniv(0)) == 1.0 and p.pua_face_purch(0) == p.div_credited(0)
    assert p.pua_face(0) == pytest.approx(p.pua_face_init() + p.div_credited(0), rel=1e-12)
    assert p.claim_pp(0, p.MATURITY) == pytest.approx(p.sum_assured() + p.pua_face(0),
                                                      rel=1e-12)
    assert p.lapse_rate(0) == 0.0 and p.pols_maturity(0) == p.pols_if_at(0, p.BEF_MAT)
    assert p.pols_if_at(0, p.AFT_DECR) == 0.0
    assert _continues_s(s, p, 659) == []


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date dollars, for every point alike (D7).

    At the shipped 2%, the factor at ``t`` is ``1.02^(t/12)`` on every point, whatever its
    duration.  So the worked example's point and the REDUCE_PREM point, both in force 108
    months, pay S's month-``108 + t`` expenses deflated by ``1.02^9``, the inflation S had
    already applied since issue, and the point issued three months on pays S's month-``t``
    maintenance inflated by ``1.02^(3/12)``, the inflation of the months before its issue.
    Acquisition is not inflated on either.  This is the only test that sees inflation run
    on the policy clock: the splice sets the rate to 0, and on a point issued at ``t = 0``
    the clocks agree.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    fut = _row(sec_model, "future", 2, -3)
    for kind, s_point, month in (("twin", 1, 108), ("derived", 5, 108)):
        p, s = _row(sec_model, kind, s_point, month), _point(s_model, s_point)
        for t in (0, 6, 12):
            assert p.inflation_factor(t) == fut.inflation_factor(t) == (
                (1 + INFLATION) ** (t / 12))
        for t in range(p.proj_len()):
            assert p.expenses(t) == pytest.approx(
                s.expenses(month + t) / (1 + INFLATION) ** (month / 12), rel=1e-12), t
    s = _point(s_model, 2)
    acq = s.expense_acq_prem_rate * s.premium_pp_ann(0) + s.expense_acq
    for t in range(s.proj_len()):
        issued = acq if t == 0 else 0.0
        assert fut.expenses(3 + t) - issued == pytest.approx(
            (s.expenses(t) - issued) * (1 + INFLATION) ** (3 / 12), rel=1e-12), t


def test_acquisition_is_charged_on_new_business_only(sec_model):
    """0.9 G + 250 per policy issued, in the issue month, never on a policy in force.

    On every committed point, what ``expenses(t)`` holds beyond its maintenance part is
    ``(0.9 G + 250) * policy_count()`` in the issue month, ``t = -duration_mth``, where G
    is the first policy year's annual premium, and 0 in every other month, to 1e-9: the
    twins of S's new business bear it at ``t = 0``, the point issued three months on at
    ``t = 3``, and the points already in force never, though on the valuation clock their
    row 0 is ``t = 0``.

    ``WholeLife_US_S`` charges acquisition at ``t = 0`` on the count in force there, which
    on a point issued at the valuation date is the issued count, so the twins agree with S
    at any count, and T1 needs no S point to count one policy.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        ts = range(p.proj_len())
        acq = [p.expenses(t) - p.expense_maint / 12 * p.inflation_factor(t) * p.pols_if(t)
               for t in ts]
        issue = -table.at[point_id, "duration_mth"]
        expected = [(p.expense_acq_prem_rate * p.premium_pp_ann(t) + p.expense_acq)
                    * p.policy_count() if t == issue else 0.0 for t in ts]
        assert acq == pytest.approx(expected, abs=1e-9), point_id
        assert (issue in ts) == (sum(expected) > 0.0), point_id


def _outside_cover_faults(p, where):
    """Where ``p``, an ItemSpace that has evaluated nothing, departs from OUTSIDE_COVER.

    Every cell of :data:`OUTSIDE_COVER`, ``pols_if_at`` at each timing and ``claim_pp`` at
    each kind, in every month before issue and at ``t = proj_len()``, the
    first month after cover, which the count's look-ahead reads, against
    :data:`OUTSIDE_COVER`; then whether any of :data:`IN_COVER_ONLY` was evaluated on the
    way, which only a fresh ItemSpace can say.  A cell that raises is reported as a fault
    too, so the scan goes on.
    """
    faults = []
    for t in [*range(p.t_entry()), p.proj_len()]:
        calls = [(name, (t,), want) for name, want in OUTSIDE_COVER.items()]
        calls += [("pols_if_at", (t, p.refs[timing]), 0.0) for timing in TIMINGS]
        calls += [("claim_pp", (t, p.refs[kind]), 0.0) for kind in KINDS]
        for name, args, want in calls:
            try:
                got = p.cells[name](*args)
            except Exception as err:        # reported, so the scan goes on
                faults.append(f"{where}: {name}{args} raised {_raised(err)}")
                continue
            if got != want or type(got) is not type(want):
                faults.append(f"{where}: {name}{args} = {got!r}, not {want!r}")
    read = {name: sorted(p.cells[name].keys()) for name in IN_COVER_ONLY
            if len(p.cells[name].keys())}
    if read:
        faults.append(f"{where}: evaluated outside cover: {read}")
    return faults


# ---------------------------------------------------------------------------
# The cap on mortality
#
# mort_rate caps the annual rate at 1, as WholeLife_US_S's does.  At the shipped A/E of 0.7
# the rate stays below 0.18 to the end of every frame, so neither the committed points nor
# the splice grid come near the cap.  One point is made to pass it: S's point 2, a male
# non-tobacco cell issued at 45, alone in a copy of S's table, under the splice's
# References with the A/E at 5.0 (CAPPED_REFS).  The product, 5.0 times the guaranteed
# table's rate, first passes 1 at attained age 97, at 1.027, and stays past it to the end
# of the frame.
CAPPED_POINT = 2
CAPPED_REFS = {**SPLICED_REFS, "ae_best_est": 5.0}
CAPPED_MTH = 12 * (97 - 45)     # the first month at attained age 97, where it passes 1


def _capped_s(tmp_path):
    """WholeLife_US_S on :data:`CAPPED_POINT` alone, under :data:`CAPPED_REFS`, read from a
    copy of S's table; the caller closes it."""
    table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                        index_col="point_id")
    s = mx.read_model(temp_inputs(tmp_path, model_path(TWIN),
                                  model_points=table.loc[[CAPPED_POINT]]),
                      name=_name("capped_s"))
    for ref, value in CAPPED_REFS.items():
        setattr(s.Projection, ref, value)
    return s


def _capped_rows(s, cap):
    """The cap's four SEC rows, built from ``s`` (:func:`_capped_s`) by the generator: the
    twin, the point issued 12 months on, and the point restated in force in the month
    before ``cap``, its first capped month, and five months after it, with one policy."""
    spec = dataclasses.replace(
        SPEC, derived=((CAPPED_POINT, cap - 1), (CAPPED_POINT, cap + 5)),
        future=((CAPPED_POINT, 12),))
    rows, companions = build_sec_table(spec, s)
    assert companions == {}
    rows.loc[rows["source_mth"] == cap + 5, "policy_count"] = 1.0
    return rows


def test_an_annual_mortality_past_1_is_capped_in_both_models(tmp_path):
    """Where the annual mortality product passes 1, both models' rate is 1.

    On the point of :data:`CAPPED_POINT`, under :data:`CAPPED_REFS`, ``WholeLife_US_S``'s
    product of the A/E and the guaranteed table's rate passes 1 in month
    :data:`CAPPED_MTH` and stays past it to the end of the frame.  Both models cap it:
    ``mort_rate`` and the monthly rate, ``1 - (1 - q)^(1/12)``, are 1.0 in every one of
    those months, the float, not the int 1, which compares equal to it, and S's are floats
    below 1 in every month before.  So every policy in force at the start of the first
    capped month dies in it, and none is in force after it, and every report holds finite
    floats alone.

    Four rows of the point, built from S by the generator: issued at the valuation date
    and 12 months after it, and restated in force in the month before the cap, opened with
    S's count and state there, each compared with S in every cell, the capped months
    included, as T1, T3 and the splice compare them, to 1e-9 relative with no absolute
    floor, since the count before the cap falls to 8e-8, but for the roll-forward
    residuals, rounding around 0, which keep the floor of 1e-9 (USLIB-SEC-PLAN.md §5.2);
    and restated five months into the capped year, opened with S's state there and one
    policy, since S's count there is 0.  On each, the rate is 1.0 from its first capped
    month, every policy in force there dies in it, and the count is 0.0 after it.
    """
    s = _capped_s(tmp_path / "s")
    sec = None
    try:
        sp = _point(s, CAPPED_POINT)
        end, ae = sp.proj_len(), CAPPED_REFS["ae_best_est"]
        cap = next(t for t in range(end) if ae * sp.mort_rate_guar(t) > 1)
        assert (cap, sp.age(cap)) == (CAPPED_MTH, 97)
        after = range(cap, end)
        assert all(ae * sp.mort_rate_guar(t) > 1 for t in after)
        for rate in (sp.mort_rate, sp.mort_rate_mth):
            assert all(type(rate(t)) is float and rate(t) < 1.0 for t in range(cap))
            assert [(type(rate(t)), rate(t)) for t in after] == [(float, 1.0)] * len(after)
        _sweep_s(sp)
        assert sp.pols_if(cap) > 0.0 and sp.pols_death(cap) == sp.pols_if(cap)
        assert [sp.pols_if(t) for t in range(cap + 1, end)] == [0.0] * (len(after) - 1)
        rows = _capped_rows(s, cap)
        sec = mx.read_model(_sec_inputs(tmp_path / "sec", rows), name=_name("capped"))
        for ref, value in CAPPED_REFS.items():
            setattr(sec.Projection, ref, value)
        # Each row with the month its rate is first capped, on its own clock, and the
        # exemptions of its comparison with S: none for the row S's count does not open.
        cases = ((("twin", CAPPED_POINT, 0), cap, TWIN_EXEMPT_DEFAULT | SPEC.exempt),
                 (("future", CAPPED_POINT, -12), cap + 12, FUTURE_EXEMPT),
                 (("derived", CAPPED_POINT, cap - 1), 1, SPLICE_EXEMPT),
                 (("derived", CAPPED_POINT, cap + 5), 0, None))
        residuals = frozenset(name for name in sp.cells if name.endswith("_resid"))
        for case, first, exempt in cases:
            p = _row(sec, *case)
            if exempt is not None:
                assert twin_mismatches(sp, p, t_offset=case[2], exempt=exempt | residuals,
                                       atol=0.0, codes=codes(p)) == [], case
                others = exempt | (set(sp.cells) - residuals)
                assert twin_mismatches(sp, p, t_offset=case[2], exempt=others,
                                       codes=codes(p)) == [], case
            capped, later = range(first, p.proj_len()), range(first + 1, p.proj_len())
            for rate in (p.mort_rate, p.mort_rate_mth):
                assert [(type(rate(t)), rate(t)) for t in capped] == (
                    [(float, 1.0)] * len(capped)), case
            assert p.pols_if(first) > 0.0 and p.pols_death(first) == p.pols_if(first), case
            assert [p.pols_if(t) for t in later] == [0.0] * len(later), case
            for report in REPORTS:
                frame = p.cells[report]()
                assert (frame.dtypes == "float64").all(), (case, report)
                assert np.isfinite(frame.to_numpy()).all(), (case, report)
    finally:
        if sec is not None:
            sec.close()
        s.close()


def _nan_in_month(t):
    """NaN, what a blank rate carries: the formula a test puts in place of a cell's."""
    return float("nan")


def test_a_nan_that_reaches_the_cap_stays_nan():
    """A NaN that reaches the cap on mortality stays NaN, and is not read as 1.

    ``min`` keeps its first argument unless a later one compares smaller, in modelx and
    compiled alike, and no comparison with NaN holds, so with its bound first the cap would
    turn a NaN into 1.0: a blank rate read as certain death, every flow finite.  It is
    written ``min(q, 1.0)``, as ``WholeLife_US_S`` writes it.  To send it a NaN, the
    formula of ``mort_rate_guar``, which feeds it, is replaced by one returning NaN, in a
    model read for the test, which modelx allows.  ``mort_rate`` must then be the float
    NaN in the first month and the last, and so must the monthly rate and the count after
    the first month.
    """
    model = mx.read_model(model_path(SEC), name=_name("nan"))
    try:
        model.Projection.cells["mort_rate_guar"].formula = _nan_in_month
        p = _row(model, "twin", CAPPED_POINT, 0)
        calls = [("mort_rate", (0,)), ("mort_rate", (p.proj_len() - 1,)),
                 ("mort_rate_mth", (0,)), ("pols_if", (1,))]
        lost = [f"{name}{args} = {value!r}" for name, args in calls
                for value in [p.cells[name](*args)]
                if not (type(value) is float and math.isnan(value))]
        assert not lost, f"the cap loses a NaN mort_rate_guar(): {lost}"
    finally:
        model.close()


def test_every_guarded_cell_holds_its_outside_cover_value(spliced):
    """Outside cover each cell holds :data:`OUTSIDE_COVER`'s value, and reads no rate.

    On every committed point, in every month before issue and in the first month after
    cover, ``t = proj_len()``, which the count's look-ahead reads, on a model that evaluates
    nothing else.  So afterwards none of :data:`IN_COVER_ONLY` may hold a value at all:
    ``is_active``'s docstring promises that outside cover no count evaluates a rate, and no
    table is read at a policy year or an attained age the policy does not have.

    The committed table's one point issued after the valuation date is S's point 2, which
    has no rider, no blend, no loan and neither ACCUM nor REDUCE_PREM, so on it a cell tied
    to one of those would hold zero before issue, guarded or not.  So the same scan runs on
    the splice's future rows, the core's or, with ``USLIB_SEC_FULL=1``, all of them: the
    rider and the funded blend (S points 8 and 16), ACCUM, REDUCE_PREM and the graded plan
    among them.  Each row is made afresh first and released after.

    Several of these guards change no number the frame shows: once the counts are zero
    outside cover, every cash flow is too, and an unguarded value multiplies a zero count.
    They are held here because they are what the docstrings promise a caller, and because
    Phase 2 needs them: a table read at a policy year or an age the policy does not have
    would wrap round in a compiled model rather than fail (USLIB-SEC-PLAN.md F4, R1).
    """
    faults = []
    model = mx.read_model(model_path(SEC), name=_name("cover"))
    try:
        table = model.Data.model_point_table()
        for key, point_id in zip(point_keys(model), table.index):
            faults += _outside_cover_faults(projection(model, key), f"point {point_id}")
    finally:
        model.close()
    sec = spliced[1]
    futures = _selected(FUTURES, CORE_FUTURES)
    for s_point, k in futures:
        key = _row_key(sec, "future", s_point, -k)
        if key in sec.Projection.itemspaces:
            _release(sec, key)
        try:
            faults += _outside_cover_faults(projection(sec, key),
                                            _case_id("future", s_point, -k))
        finally:
            _release(sec, key)
    assert futures and not faults, (
        f"{len(faults)} faults outside cover, first:\n  " + "\n  ".join(faults[:20]))


def test_the_points_sum_row_by_row_into_a_block(spliced):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    S point 2's twin, the point restated at month 12 and the point issued 12 months on,
    summed as ``run_sec.py --block`` sums them, are indexed 0..671 and equal S's frame added
    to itself moved 12 months earlier and 12 months later.  A model whose frames sat on the
    policy clock would fail it.
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
    assert list(block.index) == list(range(672))
    assert frame_mismatches(expected, block) == []


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


# The labels an extract carries in the test below: the committed points' in reverse, from
# 122 down, so that a label is neither a position plus one nor in the order of the rows.
EXTRACT_LABELS = tuple(range(122, 100, -1))


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
    without saying where it came from.  On every shipped row ``source_mth`` equals
    ``duration_mth``, 108 on the in-force twin as on the rows restated at 108, so a formula
    that read the one for the other would pass every test that leaves ``duration_mth`` as
    generated.

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
            _release(model, key)
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    out = _run_sec(runner, "104")
    count = _row(sec_model, "derived", 6, 114).pols_if(0)
    assert out.splitlines()[:2] == [
        "model point 104: WLPAR-000006-M114 - WL_PAR M45 STD_NT face 100,000, A mode, "
        "dividend option PUA",
        f"at the valuation date: in force 114 months: policy year 10, attained age 54, "
        f"{count:.6f} in force, next anniversary at t = 5"]
    last = extract.index[extract["policy_id"] == "WLPAR-000005-M659"][0]
    moved = _set("duration_mth", [last], 661)(extract)
    model = mx.read_model(_sec_inputs(tmp_path / "moved", moved), name=_name("moved"))
    try:
        _refused(_point(model, last).result_cf,
                 f"point_id {last}: duration_mth 661 is at or past maturity, "
                 f"policy month 660")
    finally:
        model.close()


def _standing(p):
    """What ``run_sec.py`` says of point ``p`` at the valuation date, stated here."""
    d = p.duration_mth_init()
    if d < 0:
        return f"to be issued at t = {-d}, {-d} months after the valuation date"
    if d == 0:
        return "issued at the valuation date, t = 0"
    return (f"in force {d} months: policy year {p.policy_year(0)}, attained age "
            f"{p.age(0)}, {p.pols_if(0):.6f} in force, next anniversary at t = "
            f"{p.anniv_mth(0)}")


def test_run_sec_prints_a_point_and_the_block(sec_model):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  The worked example's point, the runner's default, with its lines at the
    valuation date, each asserted whole, so that a longer number cannot pass for the one
    asserted, and its first twelve rows of cash flows and counts.  Point 19, restated in
    force at S's month 114, and point 22, to be issued three months on, each with the two
    lines that say where its row came from and where it stands, which only the committed
    table's generator columns can say.  And the block: a line for each of the 22 points, in
    table order, its first twelve rows, which must be the committed points' frames summed
    row by row, as this test sums them, and those frames summed into projection years,
    each year's count the one in force in its first month.  Nothing else runs the runner on
    the committed table.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    out = _run_sec(runner)
    assert out.splitlines()[:3] == [
        "model point 1: WLPAR-000001 (S's WLPAR-000001) - WL_PAR M45 STD_NT face 100,000, "
        "A mode, dividend option PUA",
        "at the valuation date: in force 108 months: policy year 10, attained age 54, "
        "1.000000 in force, next anniversary at t = 11",
        "proj_len = 552 months from the valuation date (t = 0..551); maturity at policy "
        "month 660, attained age 100"]
    anchor = _row(sec_model, "twin", 1, 108)
    assert anchor.result_cf().head(12).round(2).to_string() in out
    assert anchor.result_pols().head(12).round(6).to_string() in out
    count = _row(sec_model, "derived", 6, 114).pols_if(0)
    for point_id, lines in (
            ("19", ["model point 19: WLPAR-000006-M114 (S's WLPAR-000006 at its month 114) "
                    "- WL_PAR M45 STD_NT face 100,000, A mode, dividend option PUA",
                    f"at the valuation date: in force 114 months: policy year 10, attained "
                    f"age 54, {count:.6f} in force, next anniversary at t = 5"]),
            ("22", ["model point 22: WLPAR-000002-F3 (S's WLPAR-000002, issued 3 months "
                    "on) - WL_PAR M45 STD_NT face 100,000, A mode, dividend option PUA",
                    "at the valuation date: to be issued at t = 3, 3 months after the "
                    "valuation date"])):
        assert _run_sec(runner, point_id).splitlines()[:2] == lines, point_id
    out = _run_sec(runner, "--block")
    table = sec_model.Data.model_point_table()
    points = [projection(sec_model, key) for key in point_keys(sec_model)]
    assert out.splitlines()[:len(points) + 1] == [
        "model points, t = 0 the valuation date for each:",
        *("  {:>2}  {:<18} {}; proj_len {}".format(
            point_id, table.at[point_id, "policy_id"], _standing(p), p.proj_len())
          for point_id, p in zip(table.index, points))]
    assert ("  22  WLPAR-000002-F3    to be issued at t = 3, 3 months after the valuation "
            "date; proj_len 663") in out
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
    ``t``, as the runner did before it released its points, to the last bit.  The printed
    block, to two decimals, cannot show a last bit, so ``add`` itself is read from the
    runner, which runs the model when imported, and run here on the committed points'
    frames.  A plain running sum differs from ``groupby``'s on them, so the comparison can
    fail.
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


# run_sec.py run as though it sat at /m/products/whole_life, a copy too shallow to have a
# repository above it: the source compiled under that name, so that its own __file__ is it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/whole_life/run_sec.py"
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
    the longest frame needs a limit of 2,448 in the export, the reports the sample runs in
    ascending ``t`` 128.  The limit is four times the first, rounded up to the thousand.
    No build can tell a lower limit: the reports alone need 128, so a limit of 1,000
    builds the same model.  So this holds the limit, read from the sample's code, to the
    value derived from its comment's need, and holds the call before the import of the
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


# What only WholeLife_US_S's docstrings may say: a reference into its Spaces, which the
# SEC pages would link to the wrong model; its clock, "t = 0 is the issue month" and t
# counting policy months from issue; a call of a cell this model does not have; and
# "pols_if_at(t, "AFT_DECR") == pols_if(t + 1)", which here fails in every issue month,
# where pols_if(t + 1) holds new business the end-of-month count does not.
STALE = re.compile(r"~\.WholeLife_US_S\.|``t = 0`` is the issue month"
                   r"|``t`` counts \*\*policy months\*\* from issue"
                   r"|\b(?:proj_start|duration_inforce|puaf_inforce|loan_inforce)\(\)"
                   r'|AFT_DECR"?\)[` ]*==[` ]*pols_if\(t \+ 1\)')


def test_the_docstrings_describe_the_valuation_clock(sec_model):
    """The docstrings say what this model is, and none says what only WholeLife_US_S is.

    Whitespace is collapsed first, as ``test_model_conventions`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock, the SEC table and the product.  The
    symbol map in the Projection docstring maps every cell running in force adds or
    renames, and names nothing the model lacks: every name in it is a cell, or a Reference
    the notes give a symbol to, as the interest rates are in ``WholeLife_US_S``'s map.  And
    no docstring says what :data:`STALE` matches.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE,
                   "participating whole life insurance"):
        assert phrase in flat["model"], phrase
    mapped = _mapped_cells(sec_model.Projection.doc)
    missing = [cells for cells in NEW_CELLS if cells not in mapped]
    assert not missing, f"the symbol map does not map {missing}"
    known = set(sec_model.Projection.cells) | set(sec_model.Projection.refs)
    unknown = sorted(mapped - known)
    assert not unknown, f"the symbol map names what the model lacks: {unknown}"
    stale = sorted(where for where, doc in flat.items() if STALE.search(doc))
    assert not stale, f"docstrings that describe WholeLife_US_S: {stale}"


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
    the variants, each property below holds of some core case: every dividend option, the
    loan, the rider on annual mode and on another, a funded and an unfunded blend, limited
    pay, every premium period, final expense level and graded, inside the graded years
    and after them, the female cell, each premium mode, S's in-force row as its twin and
    restated, and each
    kind of valuation month: on an anniversary, the first among them with additions
    already bought, mid-year, in the anniversary month with years still to run, in the last
    five policy years, and in the last covered month.  And
    of some core future case: issued off the valuation anniversaries and on them, more than
    a year on, final expense, monthly mode, the rider.

    Then, on the splice's model, of some core row, each of :data:`AT_VALUATION` and
    :data:`IN_FRAME`, what no column of the table shows:

    * every opening-state column is non-zero, and each anniversary column differs from its
      current one, so that a column read in its pair's place would show;
    * a row valued on its first anniversary holds additions there, so that a first-year
      check that ran a month too long would refuse it;
    * every read of the state at the anniversary before the valuation date is taken, with
      that value apart from the current one: the PUA-block dividend, the loan interest and
      the term-blend gap of the year under way, a premium net of ``div_prev_anniv_init``,
      and the graded death benefit on ``prem_cum_init``;
    * every branch the dividend drives later in the frame is taken: the REDUCE_PREM excess
      buying additions, the premium-offset overlay, the blend's cap binding, a blend past
      its crossover, and the last dividend buying additions at maturity.

    Each core row's branches were recorded by the T2 case that compared it
    (:func:`_settle`), and a row no case has recorded is evaluated here.
    """
    s_table = _s_table_with_variants()

    def at(p, column):
        return s_table.at[p, column]

    def frame(p):
        return 12 * (100 - int(at(p, "issue_age")))

    def par(p, option):
        return at(p, "product") == "WL_PAR" and at(p, "dividend_option") == option

    def blend(p):
        return at(p, "term_blend_target") > at(p, "face_amount")

    rider = {p: at(p, "pua_rider_premium") > 0.0 for p in s_table.index}
    splices = {
        **{f"the {o} option": (lambda k, p, d, o=o: par(p, o))
           for o in ("PUA", "CASH", "ACCUM", "REDUCE_PREM")},
        "a loan": lambda k, p, d: at(p, "loan_utilization") > 0.0,
        "the rider, annual": lambda k, p, d: rider[p] and at(p, "premium_mode") == "A",
        "the rider, another mode": lambda k, p, d: (
            rider[p] and at(p, "premium_mode") != "A"),
        "a funded blend": lambda k, p, d: blend(p) and rider[p],
        "an unfunded blend": lambda k, p, d: blend(p) and not rider[p],
        "limited pay": lambda k, p, d: at(p, "premium_period") != "TO_100",
        **{f"the {q} premium period": (lambda k, p, d, q=q: at(p, "premium_period") == q)
           for q in ("TO_100", "PAY_10", "PAY_20", "TO_65")},
        "final expense level": lambda k, p, d: at(p, "product") == "WL_FE_LEVEL",
        "graded, in the graded years": lambda k, p, d: (
            at(p, "product") == "WL_FE_GRADED" and d < 24),
        "graded, after them": lambda k, p, d: (
            at(p, "product") == "WL_FE_GRADED" and d >= 24),
        "the female cell": lambda k, p, d: at(p, "sex") == "F",
        **{f"{m} mode": (lambda k, p, d, m=m: at(p, "premium_mode") == m)
           for m in ("A", "SA", "Q", "M")},
        "S's in-force row as its twin": lambda k, p, d: (k, p) == ("twin", 1),
        "S's in-force row restated": lambda k, p, d: (k, p) == ("derived", 1),
        "on an anniversary": lambda k, p, d: k == "derived" and d % 12 == 0,
        "on the first anniversary, with additions": lambda k, p, d: d == 12 and rider[p],
        "mid-year": lambda k, p, d: d % 12 not in (0, 11),
        "in an anniversary month, years to run": lambda k, p, d: (
            d % 12 == 11 and d + 12 < frame(p)),
        "in the last five policy years": lambda k, p, d: frame(p) - 60 <= d < frame(p) - 1,
        "in the last covered month": lambda k, p, d: d == frame(p) - 1,
    }
    futures = {
        "issued off the anniversaries": lambda p, k: k % 12 != 0,
        "issued on them": lambda p, k: k % 12 == 0,
        "issued more than a year on": lambda p, k: k > 12,
        "final expense": lambda p, k: at(p, "product") != "WL_PAR",
        "monthly mode": lambda p, k: at(p, "premium_mode") == "M",
        "the rider": lambda p, k: rider[p],
    }
    missing = [what for what, holds in splices.items()
               if not any(holds(*case) for case in CORE_SPLICES)]
    missing += [what for what, holds in futures.items()
                if not any(holds(*case) for case in CORE_FUTURES)]
    assert not missing, f"no core case reaches: {missing}"

    reached = set()
    for case in CORE_SPLICES:
        reached |= _record_of(spliced, splice_records, case)["branches"]
    missing = [what for what in (*AT_VALUATION, *IN_FRAME) if what not in reached]
    assert not missing, f"no core row reaches: {missing}"


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
    exactly.  ``python tools/gen_sec_fingerprint.py WholeLife_US_SEC --check`` runs the same
    comparison from the command line.
    """
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# WholeLife_US_SEC's fingerprint, frozen at M13 from the model as Phase 1 left it and
# committed alone, before Phase 2 changed anything.  Each point is keyed by its point_id;
# each column holds (its sum over the frame, its largest absolute value, (its values at the
# months)).  The block is written by tools/gen_sec_fingerprint.py, and is never edited by
# hand: a refreeze goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: WholeLife_US_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 552, "months": (0, 137, 275, 413, 551),
        "result_cf": {
            "pols_if": (288.0404045652642, 1.0, (
                1.0, 0.760561902629876, 0.5295780643453551, 0.2791988590875926,
                0.05935480163141163)),
            "premiums": (43991.15064787228, 1800.0, (
                1800.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2025.341065323912, 5.0, (
                5.0, 4.7674908253791815, 4.168571565137779, 2.7597699939916587,
                0.7367448051415579)),
            "premium_taxes": (879.8230129574457, 36.0, (
                36.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (68469.94412781468, 254.5763609339235, (
                19.45197878431436, 45.31639132530343, 106.3190518932221, 221.30513574187242,
                171.851176121529)),
            "claims_lapse": (30655.05412621968, 80.51388378294082, (
                18.999084831165487, 55.057609103912824, 79.60353818378535,
                65.08247119102329, 0.0)),
            "claims_maturity": (10719.818960753017, 10719.818960753017, (
                0.0, 0.0, 0.0, 0.0, 10719.818960753017)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-68758.83064519645, 10892.406881679686, (
                1720.5489363845202, -105.14149125459544, -190.0911616421452,
                -289.1473769268874, -10892.406881679686)),
            "liability_cf": (68758.83064519645, 10892.406881679686, (
                -1720.5489363845202, 105.14149125459544, 190.0911616421452,
                289.1473769268874, 10892.406881679686)),
        },
        "result_pols": {
            "pols_if": (288.0404045652642, 1.0, (
                1.0, 0.760561902629876, 0.5295780643453551, 0.2791988590875926,
                0.05935480163141163)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.4591293356952477, 0.0015214595507907977, (
                0.00018685858582434545, 0.00039141107965164795, 0.0007969110814262248,
                0.0014039714481354725, 0.0009468210986315496)),
            "pols_lapse": (0.4824626837719714, 0.001681828229961014, (
                0.001681828229961014, 0.001278715131173591, 0.0008894852789919613,
                0.00046729060143183953, 0.0)),
            "pols_maturity": (0.05840798053278008, 0.05840798053278008, (
                0.0, 0.0, 0.0, 0.0, 0.05840798053278008)),
            "mort_rate": (22.057064316, 0.175489874, (
                0.00224, 0.006158159, 0.017908939999999998, 0.05870160799999999,
                0.175489874)),
            "mort_rate_mth": (1.923103673311545, 0.015951887170160717, (
                0.00018685858582434545, 0.0005146340860595622, 0.0015048037958508287,
                0.005028571580570129, 0.015951887170160717)),
            "lapse_rate": (10.799999999999999, 0.02, (
                0.02, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (0.9083569784793699, 0.001682142552739574, (
                0.001682142552739574, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    2: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "premiums": (44630.848227513656, 1800.0, (
                1800.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (4061.034370466994, 1875.0, (
                1875.0, 4.1503830162368525, 3.7649622696887732, 2.62488208653986,
                0.6203640007289675)),
            "premium_taxes": (892.6169645502731, 36.0, (
                36.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (49405.73966005118, 179.51920609875012, (
                8.987658125847453, 18.226675479238818, 56.162557141531764,
                146.25138701024576, 121.17678099043871)),
            "claims_lapse": (22547.154458812387, 56.79786646637751, (
                0.1155086677682963, 23.5496931639529, 51.33403984000449, 50.661702451994735,
                0.0)),
            "claims_maturity": (7558.760866104, 7558.760866104, (
                0.0, 0.0, 0.0, 0.0, 7558.760866104)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-39834.45809247118, 7680.558011095168, (
                -120.10316679361574, -45.92675165942857, -111.26155925122504,
                -199.53797154878035, -7680.558011095168)),
            "liability_cf": (39834.45809247118, 7680.558011095168, (
                120.10316679361574, 45.92675165942857, 111.26155925122504,
                199.53797154878035, 7680.558011095168)),
        },
        "result_pols": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.334497367909002, 0.0010719841664289626, (
                8.987658125847453e-05, 0.00016923259012394307, 0.0004437966486207595,
                0.0009529614030912094, 0.000667107597863083)),
            "pols_lapse": (0.6243497599744268, 0.0042649354252909406, (
                0.0042649354252909406, 0.0010649499879420256, 0.0007352323963559219,
                0.0003892038513884535, 0.0)),
            "pols_maturity": (0.04115287211657229, 0.04115287211657229, (
                0.0, 0.0, 0.0, 0.0, 0.04115287211657229)),
            "mort_rate": (22.220105964, 0.175489874, (
                0.001077986, 0.003202171, 0.012104343999999998, 0.048126365000000004,
                0.175489874)),
            "mort_rate_mth": (1.9367002972291485, 0.015951887170160717, (
                8.987658125847453e-05, 0.0002672400284223775, 0.0010143350596846235,
                0.004101813599558191, 0.015951887170160717)),
            "lapse_rate": (14.759999999999998, 0.05, (
                0.05, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (1.244364561142016, 0.004265318777560645, (
                0.004265318777560645, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    3: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "premiums": (44630.848227513656, 1800.0, (
                1800.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (4061.034370466994, 1875.0, (
                1875.0, 4.1503830162368525, 3.7649622696887732, 2.62488208653986,
                0.6203640007289675)),
            "premium_taxes": (892.6169645502731, 36.0, (
                36.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (33449.7367909002, 107.19841664289626, (
                8.987658125847453, 16.923259012394308, 44.379664862075956,
                95.29614030912094, 66.7107597863083)),
            "claims_lapse": (15582.837980416045, 37.91630059845029, (
                0.1155086677682963, 19.53783871628139, 36.74066569449995, 31.11246937517874,
                0.0)),
            "claims_maturity": (4115.287211657229, 4115.287211657229, (
                0.0, 0.0, 0.0, 0.0, 4115.287211657229)),
            "div_cash_paid": (19553.989990796275, 565.6231726916081, (
                0.0, 0.0, 0.0, 0.0, 83.54609179873806)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-33024.65508127336, 4266.164427243005, (
                -120.10316679361574, -40.61148074491255, -84.88529282626467,
                -129.03349177083953, -4266.164427243005)),
            "liability_cf": (33024.65508127336, 4266.164427243005, (
                120.10316679361574, 40.61148074491255, 84.88529282626467,
                129.03349177083953, 4266.164427243005)),
        },
        "result_pols": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.334497367909002, 0.0010719841664289626, (
                8.987658125847453e-05, 0.00016923259012394307, 0.0004437966486207595,
                0.0009529614030912094, 0.000667107597863083)),
            "pols_lapse": (0.6243497599744268, 0.0042649354252909406, (
                0.0042649354252909406, 0.0010649499879420256, 0.0007352323963559219,
                0.0003892038513884535, 0.0)),
            "pols_maturity": (0.04115287211657229, 0.04115287211657229, (
                0.0, 0.0, 0.0, 0.0, 0.04115287211657229)),
            "mort_rate": (22.220105964, 0.175489874, (
                0.001077986, 0.003202171, 0.012104343999999998, 0.048126365000000004,
                0.175489874)),
            "mort_rate_mth": (1.9367002972291485, 0.015951887170160717, (
                8.987658125847453e-05, 0.0002672400284223775, 0.0010143350596846235,
                0.004101813599558191, 0.015951887170160717)),
            "lapse_rate": (14.759999999999998, 0.05, (
                0.05, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (1.244364561142016, 0.004265318777560645, (
                0.004265318777560645, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    4: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "premiums": (44630.848227513656, 1800.0, (
                1800.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (4061.034370466994, 1875.0, (
                1875.0, 4.1503830162368525, 3.7649622696887732, 2.62488208653986,
                0.6203640007289675)),
            "premium_taxes": (892.6169645502731, 36.0, (
                36.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (65029.006313687976, 285.1085672083559, (
                8.987658125847453, 17.61223122931539, 55.99641505470967, 183.21372956126808,
                232.02577940556296)),
            "claims_lapse": (27243.928662133072, 68.91372926711423, (
                0.1155086677682963, 23.89451952703695, 56.07966906911336, 67.19412117671993,
                0.0)),
            "claims_maturity": (14446.509606587364, 14446.509606587364, (
                0.0, 0.0, 0.0, 0.0, 14446.509606587364)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-67042.24768991201, 14679.155749993657, (
                -120.10316679361574, -45.6571337725892, -115.84104639351179,
                -253.03273282452787, -14679.155749993657)),
            "liability_cf": (67042.24768991201, 14679.155749993657, (
                120.10316679361574, 45.6571337725892, 115.84104639351179,
                253.03273282452787, 14679.155749993657)),
        },
        "result_pols": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.334497367909002, 0.0010719841664289626, (
                8.987658125847453e-05, 0.00016923259012394307, 0.0004437966486207595,
                0.0009529614030912094, 0.000667107597863083)),
            "pols_lapse": (0.6243497599744268, 0.0042649354252909406, (
                0.0042649354252909406, 0.0010649499879420256, 0.0007352323963559219,
                0.0003892038513884535, 0.0)),
            "pols_maturity": (0.04115287211657229, 0.04115287211657229, (
                0.0, 0.0, 0.0, 0.0, 0.04115287211657229)),
            "mort_rate": (22.220105964, 0.175489874, (
                0.001077986, 0.003202171, 0.012104343999999998, 0.048126365000000004,
                0.175489874)),
            "mort_rate_mth": (1.9367002972291485, 0.015951887170160717, (
                8.987658125847453e-05, 0.0002672400284223775, 0.0010143350596846235,
                0.004101813599558191, 0.015951887170160717)),
            "lapse_rate": (14.759999999999998, 0.05, (
                0.05, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (1.244364561142016, 0.004265318777560645, (
                0.004265318777560645, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    5: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "premiums": (25845.575597967305, 1800.0, (
                1800.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (4061.034370466994, 1875.0, (
                1875.0, 4.1503830162368525, 3.7649622696887732, 2.62488208653986,
                0.6203640007289675)),
            "premium_taxes": (516.9115119593462, 36.0, (
                36.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (33848.829315202616, 109.35374983431213, (
                8.987658125847453, 16.923259012394308, 44.379664862075956,
                95.78105875506569, 69.92846728414244)),
            "claims_lapse": (15652.693377892856, 37.91630059845029, (
                0.1155086677682963, 19.53783871628139, 36.74066569449995,
                31.298510741608077, 0.0)),
            "claims_maturity": (4397.328876870319, 4397.328876870319, (
                0.0, 0.0, 0.0, 0.0, 4397.328876870319)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-32631.22185442483, 4467.87770815519, (
                -120.10316679361574, -40.61148074491255, -84.88529282626467,
                -129.70445158321363, -4467.87770815519)),
            "liability_cf": (32631.22185442483, 4467.87770815519, (
                120.10316679361574, 40.61148074491255, 84.88529282626467,
                129.70445158321363, 4467.87770815519)),
        },
        "result_pols": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.334497367909002, 0.0010719841664289626, (
                8.987658125847453e-05, 0.00016923259012394307, 0.0004437966486207595,
                0.0009529614030912094, 0.000667107597863083)),
            "pols_lapse": (0.6243497599744268, 0.0042649354252909406, (
                0.0042649354252909406, 0.0010649499879420256, 0.0007352323963559219,
                0.0003892038513884535, 0.0)),
            "pols_maturity": (0.04115287211657229, 0.04115287211657229, (
                0.0, 0.0, 0.0, 0.0, 0.04115287211657229)),
            "mort_rate": (22.220105964, 0.175489874, (
                0.001077986, 0.003202171, 0.012104343999999998, 0.048126365000000004,
                0.175489874)),
            "mort_rate_mth": (1.9367002972291485, 0.015951887170160717, (
                8.987658125847453e-05, 0.0002672400284223775, 0.0010143350596846235,
                0.004101813599558191, 0.015951887170160717)),
            "lapse_rate": (14.759999999999998, 0.05, (
                0.05, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (1.244364561142016, 0.004265318777560645, (
                0.004265318777560645, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    6: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "premiums": (44630.848227513656, 1800.0, (
                1800.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (4061.034370466994, 1875.0, (
                1875.0, 4.1503830162368525, 3.7649622696887732, 2.62488208653986,
                0.6203640007289675)),
            "premium_taxes": (892.6169645502731, 36.0, (
                36.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (44707.548162767576, 160.09267948890124, (
                8.987658125847453, 17.61143603892956, 51.74471683333912, 131.04533132030048,
                107.8462255869199)),
            "claims_lapse": (19430.58686272918, 49.3546431254452, (
                0.09240693421463704, 19.64212542069662, 43.985906701104504,
                44.43920857695899, 0.0)),
            "claims_maturity": (6735.703423772555, 6735.703423772555, (
                0.0, 0.0, 0.0, 0.0, 6735.703423772555)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (-24.879056101021433, 245.88263058304548, (
                5.393078101631191, 21.351960321164917, 17.301106085276114,
                7.187473214407817, -48.153003098849396)),
            "net_cf": (-31171.762500671895, 6796.017010261354, (
                -125.47314316169327, -62.75590479702795, -116.7966918894085,
                -185.29689519820715, -6796.017010261354)),
            "liability_cf": (31171.762500671895, 6796.017010261354, (
                125.47314316169327, 62.75590479702795, 116.7966918894085,
                185.29689519820715, 6796.017010261354)),
        },
        "result_pols": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.334497367909002, 0.0010719841664289626, (
                8.987658125847453e-05, 0.00016923259012394307, 0.0004437966486207595,
                0.0009529614030912094, 0.000667107597863083)),
            "pols_lapse": (0.6243497599744268, 0.0042649354252909406, (
                0.0042649354252909406, 0.0010649499879420256, 0.0007352323963559219,
                0.0003892038513884535, 0.0)),
            "pols_maturity": (0.04115287211657229, 0.04115287211657229, (
                0.0, 0.0, 0.0, 0.0, 0.04115287211657229)),
            "mort_rate": (22.220105964, 0.175489874, (
                0.001077986, 0.003202171, 0.012104343999999998, 0.048126365000000004,
                0.175489874)),
            "mort_rate_mth": (1.9367002972291485, 0.015951887170160717, (
                8.987658125847453e-05, 0.0002672400284223775, 0.0010143350596846235,
                0.004101813599558191, 0.015951887170160717)),
            "lapse_rate": (14.759999999999998, 0.05, (
                0.05, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (1.244364561142016, 0.004265318777560645, (
                0.004265318777560645, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    7: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "premiums": (44630.848227513656, 1800.0, (
                1800.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (24794.915681952032, 1000.0, (
                1000.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (4061.034370466994, 1875.0, (
                1875.0, 4.1503830162368525, 3.7649622696887732, 2.62488208653986,
                0.6203640007289675)),
            "premium_taxes": (1388.515278189314, 56.0, (
                56.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (71507.76427269593, 261.6646873091647, (
                8.987658125847453, 24.33177510253132, 81.37186257075561, 214.49787599602726,
                176.9104276025446)),
            "claims_lapse": (36572.26270257556, 88.52398623681002, (
                3.9717090002291866, 42.340902037106915, 82.55632528161875, 76.8448063761672,
                0.0)),
            "claims_maturity": (10996.88634835786, 10996.88634835786, (
                0.0, 0.0, 0.0, 0.0, 10996.88634835786)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-55100.69906281997, 11174.417139961135, (
                856.0406328739234, -70.8230601558751, -167.69315012206314,
                -293.96756445873433, -11174.417139961135)),
            "liability_cf": (55100.69906281997, 11174.417139961135, (
                -856.0406328739234, 70.8230601558751, 167.69315012206314,
                293.96756445873433, 11174.417139961135)),
        },
        "result_pols": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.334497367909002, 0.0010719841664289626, (
                8.987658125847453e-05, 0.00016923259012394307, 0.0004437966486207595,
                0.0009529614030912094, 0.000667107597863083)),
            "pols_lapse": (0.6243497599744268, 0.0042649354252909406, (
                0.0042649354252909406, 0.0010649499879420256, 0.0007352323963559219,
                0.0003892038513884535, 0.0)),
            "pols_maturity": (0.04115287211657229, 0.04115287211657229, (
                0.0, 0.0, 0.0, 0.0, 0.04115287211657229)),
            "mort_rate": (22.220105964, 0.175489874, (
                0.001077986, 0.003202171, 0.012104343999999998, 0.048126365000000004,
                0.175489874)),
            "mort_rate_mth": (1.9367002972291485, 0.015951887170160717, (
                8.987658125847453e-05, 0.0002672400284223775, 0.0010143350596846235,
                0.004101813599558191, 0.015951887170160717)),
            "lapse_rate": (14.759999999999998, 0.05, (
                0.05, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (1.244364561142016, 0.004265318777560645, (
                0.004265318777560645, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    8: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "premiums": (44630.848227513656, 1800.0, (
                1800.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (123974.57840976017, 5000.0, (
                5000.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (4061.034370466994, 1875.0, (
                1875.0, 4.1503830162368525, 3.7649622696887732, 2.62488208653986,
                0.6203640007289675)),
            "premium_taxes": (3372.1085327454766, 136.0, (
                136.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (159833.48598096892, 589.0258765391588, (
                8.987658125847453, 48.55799483823019, 181.69986864699956,
                486.39039679740677, 399.07956973342993)),
            "claims_lapse": (92352.11228651341, 216.30216773359595, (
                19.396510330072743, 116.90806446695288, 206.81479215191928,
                181.15772025853443, 0.0)),
            "claims_maturity": (24702.16915977831, 24702.16915977831, (
                0.0, 0.0, 0.0, 0.0, 24702.16915977831)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-115715.48369319928, 25101.86909351247, (
                4760.61583154408, -169.61644232141992, -392.27962306860763,
                -670.1729991424811, -25101.86909351247)),
            "liability_cf": (115715.48369319928, 25101.86909351247, (
                -4760.61583154408, 169.61644232141992, 392.27962306860763,
                670.1729991424811, 25101.86909351247)),
        },
        "result_pols": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.334497367909002, 0.0010719841664289626, (
                8.987658125847453e-05, 0.00016923259012394307, 0.0004437966486207595,
                0.0009529614030912094, 0.000667107597863083)),
            "pols_lapse": (0.6243497599744268, 0.0042649354252909406, (
                0.0042649354252909406, 0.0010649499879420256, 0.0007352323963559219,
                0.0003892038513884535, 0.0)),
            "pols_maturity": (0.04115287211657229, 0.04115287211657229, (
                0.0, 0.0, 0.0, 0.0, 0.04115287211657229)),
            "mort_rate": (22.220105964, 0.175489874, (
                0.001077986, 0.003202171, 0.012104343999999998, 0.048126365000000004,
                0.175489874)),
            "mort_rate_mth": (1.9367002972291485, 0.015951887170160717, (
                8.987658125847453e-05, 0.0002672400284223775, 0.0010143350596846235,
                0.004101813599558191, 0.015951887170160717)),
            "lapse_rate": (14.759999999999998, 0.05, (
                0.05, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (1.244364561142016, 0.004265318777560645, (
                0.004265318777560645, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    9: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "premiums": (39743.91533168908, 4800.0, (
                4800.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (6761.034370466993, 4575.0, (
                4575.0, 4.1503830162368525, 3.7649622696887732, 2.62488208653986,
                0.6203640007289675)),
            "premium_taxes": (794.8783066337817, 96.0, (
                96.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (57351.20433555746, 207.4338941026885, (
                8.987658125847453, 20.154512614141783, 66.37655591891097,
                171.63272359750746, 138.33400383275108)),
            "claims_lapse": (39142.12314460137, 83.33592965839237, (
                0.6560892329239231, 62.03421385192725, 82.20887751488591, 65.8476482098511,
                0.0)),
            "claims_maturity": (8618.007148519237, 8618.007148519237, (
                0.0, 0.0, 0.0, 0.0, 8618.007148519237)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-72923.33197408976, 8756.961516352718, (
                119.35625264122862, -86.33910948230589, -152.35039570348565,
                -240.1052538938984, -8756.961516352718)),
            "liability_cf": (72923.33197408976, 8756.961516352718, (
                -119.35625264122862, 86.33910948230589, 152.35039570348565,
                240.1052538938984, 8756.961516352718)),
        },
        "result_pols": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.334497367909002, 0.0010719841664289626, (
                8.987658125847453e-05, 0.00016923259012394307, 0.0004437966486207595,
                0.0009529614030912094, 0.000667107597863083)),
            "pols_lapse": (0.6243497599744268, 0.0042649354252909406, (
                0.0042649354252909406, 0.0010649499879420256, 0.0007352323963559219,
                0.0003892038513884535, 0.0)),
            "pols_maturity": (0.04115287211657229, 0.04115287211657229, (
                0.0, 0.0, 0.0, 0.0, 0.04115287211657229)),
            "mort_rate": (22.220105964, 0.175489874, (
                0.001077986, 0.003202171, 0.012104343999999998, 0.048126365000000004,
                0.175489874)),
            "mort_rate_mth": (1.9367002972291485, 0.015951887170160717, (
                8.987658125847453e-05, 0.0002672400284223775, 0.0010143350596846235,
                0.004101813599558191, 0.015951887170160717)),
            "lapse_rate": (14.759999999999998, 0.05, (
                0.05, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (1.244364561142016, 0.004265318777560645, (
                0.004265318777560645, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    10: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (302.5994713781298, 1.0, (
                1.0, 0.6369133793247594, 0.45022790463775986, 0.26209597664291073,
                0.0699139479856291)),
            "premiums": (40009.20494606354, 1560.0, (
                1560.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3961.5600893231203, 1659.0, (
                1659.0, 4.174323060408968, 3.8742751004957747, 2.9612206059874366,
                1.0371142400184061)),
            "premium_taxes": (800.1840989212709, 31.2, (
                31.2, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (42893.36787018587, 172.09075656137603, (
                7.264877111334833, 13.978515986908889, 42.826277306423876,
                120.16874301714059, 144.21634263174315)),
            "claims_lapse": (23383.16523337723, 58.697284858500694, (
                0.09454103078054592, 21.15283029577274, 50.0599293431046,
                55.818160653628425, 0.0)),
            "claims_maturity": (12480.613928103172, 12480.613928103172, (
                0.0, 0.0, 0.0, 0.0, 12480.613928103172)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-43509.686273847125, 12625.867384974934, (
                -137.55941814211536, -39.3056693430906, -96.76048175002425,
                -178.94812427675646, -12625.867384974934)),
            "liability_cf": (43509.686273847125, 12625.867384974934, (
                137.55941814211536, 39.3056693430906, 96.76048175002425, 178.94812427675646,
                12625.867384974934)),
        },
        "result_pols": {
            "pols_if": (302.5994713781298, 1.0, (
                1.0, 0.6369133793247594, 0.45022790463775986, 0.26209597664291073,
                0.0699139479856291)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.2894764004467829, 0.0010061133225686494, (
                7.264877111334833e-05, 0.00012995930964542117, 0.0003407272215229227,
                0.0007937391284339181, 0.000807593149198401)),
            "pols_lapse": (0.6414172447167874, 0.0042650089073930485, (
                0.0042650089073930485, 0.0010711604876864603, 0.0007567743650637504,
                0.0004395476128491644, 0.0)),
            "pols_maturity": (0.0691063548364307, 0.0691063548364307, (
                0.0, 0.0, 0.0, 0.0, 0.0691063548364307)),
            "mort_rate": (16.516532339999998, 0.130138911, (
                0.0008714369999999999, 0.0024458, 0.009043754999999999,
                0.035741908999999995, 0.130138911)),
            "mort_rate_mth": (1.42213071586005, 0.011551245101541152, (
                7.264877111334833e-05, 0.00020404550110597608, 0.000756788324342228,
                0.003028429274652078, 0.011551245101541152)),
            "lapse_rate": (14.759999999999998, 0.05, (
                0.05, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (1.244364561142016, 0.004265318777560645, (
                0.004265318777560645, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    11: {"rows": 420, "months": (0, 104, 209, 314, 419),
        "result_cf": {
            "pols_if": (124.52901560745013, 1.0, (
                1.0, 0.46359543244043444, 0.2229838014358708, 0.08192176329059586,
                0.016068478377314514)),
            "premiums": (9988.83677048322, 921.75, (
                921.75, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1836.9128992132455, 1084.575, (
                1084.575, 2.7519717710269087, 1.5740903056766147, 0.6877128252395103,
                0.16041097839732563)),
            "premium_taxes": (199.77673540966438, 18.435, (
                18.435, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (3261.643831210079, 9.609363501561424, (
                7.719511290893433, 7.781586699897034, 9.159817268334576, 8.40990598190169,
                3.8448383110663245)),
            "claims_lapse": (2243.679193594651, 8.750699732369691, (
                0.08472630278798478, 6.557433473230676, 8.572277330812854,
                5.016979179370037, 0.0)),
            "claims_maturity": (237.1823373486514, 237.1823373486514, (
                0.0, 0.0, 0.0, 0.0, 237.1823373486514)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (2209.641773706928, 777.283078443377, (
                -189.06423759368147, -17.09099194415462, -19.306184904824043,
                -14.114597986511237, -241.18758663811505)),
            "liability_cf": (-2209.641773706928, 777.283078443377, (
                189.06423759368147, 17.09099194415462, 19.306184904824043,
                14.114597986511237, 241.18758663811505)),
        },
        "result_pols": {
            "pols_if": (124.52901560745013, 1.0, (
                1.0, 0.46359543244043444, 0.2229838014358708, 0.08192176329059586,
                0.016068478377314514)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.21744292208067192, 0.0006406242334374283, (
                0.0005146340860595622, 0.0005187724466598023, 0.0006106544845556384,
                0.000560660398793446, 0.0002563225540710883)),
            "pols_lapse": (0.7667449220960848, 0.010590787848498097, (
                0.010590787848498097, 0.0023816092044656946, 0.0011436679482234636,
                0.00041844119618380686, 0.0)),
            "pols_maturity": (0.015812155823243426, 0.015812155823243426, (
                0.0, 0.0, 0.0, 0.0, 0.015812155823243426)),
            "mort_rate": (21.572314931999998, 0.175489874, (
                0.006158159, 0.013345899, 0.032372228, 0.07910434, 0.175489874)),
            "mort_rate_mth": (1.8826340320375885, 0.015951887170160717, (
                0.0005146340860595622, 0.0011190197537730429, 0.0027385598443627757,
                0.006843851697926118, 0.015951887170160717)),
            "lapse_rate": (26.160000000000007, 0.12, (
                0.12, 0.06, 0.06, 0.06, 0.0)),
            "lapse_rate_mth": (2.2497718284312316, 0.010596241035318976, (
                0.010596241035318976, 0.005143012831822946, 0.005143012831822946,
                0.005143012831822946, 0.0)),
        },
    },
    12: {"rows": 420, "months": (0, 104, 209, 314, 419),
        "result_cf": {
            "pols_if": (124.52901560745013, 1.0, (
                1.0, 0.46359543244043444, 0.2229838014358708, 0.08192176329059586,
                0.016068478377314514)),
            "premiums": (17133.008878908564, 1581.0, (
                1581.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2430.2378992132453, 1677.9, (
                1677.9, 2.7519717710269087, 1.5740903056766147, 0.6877128252395103,
                0.16041097839732563)),
            "premium_taxes": (342.66017757817133, 31.62, (
                31.62, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (3123.747256871893, 9.609363501561424, (
                1.0997354736210019, 7.781586699897034, 9.159817268334576, 8.40990598190169,
                3.8448383110663245)),
            "claims_lapse": (2243.679193594651, 8.750699732369691, (
                0.08472630278798478, 6.557433473230676, 8.572277330812854,
                5.016979179370037, 0.0)),
            "claims_maturity": (237.1823373486514, 237.1823373486514, (
                0.0, 0.0, 0.0, 0.0, 237.1823373486514)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (8755.502014301952, 1347.85513166166, (
                -129.7044617764091, -17.09099194415462, -19.306184904824043,
                -14.114597986511237, -241.18758663811505)),
            "liability_cf": (-8755.502014301952, 1347.85513166166, (
                129.7044617764091, 17.09099194415462, 19.306184904824043,
                14.114597986511237, 241.18758663811505)),
        },
        "result_pols": {
            "pols_if": (124.52901560745013, 1.0, (
                1.0, 0.46359543244043444, 0.2229838014358708, 0.08192176329059586,
                0.016068478377314514)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.21744292208067192, 0.0006406242334374283, (
                0.0005146340860595622, 0.0005187724466598023, 0.0006106544845556384,
                0.000560660398793446, 0.0002563225540710883)),
            "pols_lapse": (0.7667449220960848, 0.010590787848498097, (
                0.010590787848498097, 0.0023816092044656946, 0.0011436679482234636,
                0.00041844119618380686, 0.0)),
            "pols_maturity": (0.015812155823243426, 0.015812155823243426, (
                0.0, 0.0, 0.0, 0.0, 0.015812155823243426)),
            "mort_rate": (21.572314931999998, 0.175489874, (
                0.006158159, 0.013345899, 0.032372228, 0.07910434, 0.175489874)),
            "mort_rate_mth": (1.8826340320375885, 0.015951887170160717, (
                0.0005146340860595622, 0.0011190197537730429, 0.0027385598443627757,
                0.006843851697926118, 0.015951887170160717)),
            "lapse_rate": (26.160000000000007, 0.12, (
                0.12, 0.06, 0.06, 0.06, 0.0)),
            "lapse_rate_mth": (2.2497718284312316, 0.010596241035318976, (
                0.010596241035318976, 0.005143012831822946, 0.005143012831822946,
                0.005143012831822946, 0.0)),
        },
    },
    13: {"rows": 420, "months": (0, 104, 209, 314, 419),
        "result_cf": {
            "pols_if": (129.7143001866972, 1.0, (
                1.0, 0.4730292273692644, 0.238969071302375, 0.09907560807509673,
                0.026527687144528786)),
            "premiums": (7582.648860929991, 673.1999999999999, (
                673.1999999999999, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1652.584993523375, 860.88, (
                860.88, 2.8079721875994608, 1.6869337416951065, 0.8317150852814806,
                0.26482484212566765)),
            "premium_taxes": (151.65297721859983, 13.463999999999999, (
                13.463999999999999, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (2708.2047839647457, 7.859648247683838, (
                5.8081873130821915, 5.918625793115485, 7.269181077873211, 7.473131806412038,
                4.596417242751815)),
            "claims_lapse": (2421.495952729263, 9.088544790921643, (
                0.07891142838659503, 6.428616671503887, 9.043778219678298,
                6.0571442142509015, 0.0)),
            "claims_maturity": (393.31888992518, 393.31888992518, (
                0.0, 0.0, 0.0, 0.0, 393.31888992518)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (255.39126356882798, 567.0259169413235, (
                -207.03109874146884, -15.155214652218833, -17.999893039246615,
                -14.36199110594442, -398.1801320100575)),
            "liability_cf": (-255.39126356882798, 567.0259169413235, (
                207.03109874146884, 15.155214652218833, 17.999893039246615,
                14.36199110594442, 398.1801320100575)),
        },
        "result_pols": {
            "pols_if": (129.7143001866972, 1.0, (
                1.0, 0.4730292273692644, 0.238969071302375, 0.09907560807509673,
                0.026527687144528786)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.1805469855976497, 0.0005239765498455892, (
                0.00038721248753881277, 0.0003945750528743657, 0.00048461207185821403,
                0.0004982087870941358, 0.00030642781618345433)),
            "pols_lapse": (0.7932317550740048, 0.01059213803846913, (
                0.01059213803846913, 0.0024307660816273707, 0.001226528634012904,
                0.0005069848294659315, 0.0)),
            "pols_maturity": (0.02622125932834533, 0.02622125932834533, (
                0.0, 0.0, 0.0, 0.0, 0.02622125932834533)),
            "mort_rate": (16.019020247999997, 0.130138911, (
                0.004636667, 0.009963946999999999, 0.024065538, 0.05870160799999999,
                0.130138911)),
            "mort_rate_mth": (1.3806227255039905, 0.011551245101541152, (
                0.00038721248753881277, 0.000834145186057067, 0.0020279280043107306,
                0.005028571580570129, 0.011551245101541152)),
            "lapse_rate": (26.160000000000007, 0.12, (
                0.12, 0.06, 0.06, 0.06, 0.0)),
            "lapse_rate_mth": (2.2497718284312316, 0.010596241035318976, (
                0.010596241035318976, 0.005143012831822946, 0.005143012831822946,
                0.005143012831822946, 0.0)),
        },
    },
    14: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "premiums": (44630.848227513656, 1800.0, (
                1800.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (4061.034370466994, 1875.0, (
                1875.0, 4.1503830162368525, 3.7649622696887732, 2.62488208653986,
                0.6203640007289675)),
            "premium_taxes": (892.6169645502731, 36.0, (
                36.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (52619.56156868959, 143.5606870219553, (
                8.987658125847453, 33.846518024788615, 88.75932972415191,
                139.26820111034962, 78.31985086830306)),
            "claims_lapse": (16738.024155095125, 41.31790041112039, (
                0.1155086677682963, 20.38208717592832, 40.25123585783993,
                33.493513695302916, 0.0)),
            "claims_maturity": (4383.297522726723, 4383.297522726723, (
                0.0, 0.0, 0.0, 0.0, 4383.297522726723)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-34063.68635401506, 4462.237737595755, (
                -120.10316679361574, -58.378988216953786, -132.7755278516806,
                -175.3865968921924, -4462.237737595755)),
            "liability_cf": (34063.68635401506, 4462.237737595755, (
                120.10316679361574, 58.378988216953786, 132.7755278516806,
                175.3865968921924, 4462.237737595755)),
        },
        "result_pols": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.334497367909002, 0.0010719841664289626, (
                8.987658125847453e-05, 0.00016923259012394307, 0.0004437966486207595,
                0.0009529614030912094, 0.000667107597863083)),
            "pols_lapse": (0.6243497599744268, 0.0042649354252909406, (
                0.0042649354252909406, 0.0010649499879420256, 0.0007352323963559219,
                0.0003892038513884535, 0.0)),
            "pols_maturity": (0.04115287211657229, 0.04115287211657229, (
                0.0, 0.0, 0.0, 0.0, 0.04115287211657229)),
            "mort_rate": (22.220105964, 0.175489874, (
                0.001077986, 0.003202171, 0.012104343999999998, 0.048126365000000004,
                0.175489874)),
            "mort_rate_mth": (1.9367002972291485, 0.015951887170160717, (
                8.987658125847453e-05, 0.0002672400284223775, 0.0010143350596846235,
                0.004101813599558191, 0.015951887170160717)),
            "lapse_rate": (14.759999999999998, 0.05, (
                0.05, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (1.244364561142016, 0.004265318777560645, (
                0.004265318777560645, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    15: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "premiums": (45146.92363192646, 154.4994, (
                154.4994, 97.83838816717382, 67.59730453883432, 35.89435780714376,
                6.461161773892437)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (4061.034370466994, 1875.0, (
                1875.0, 4.1503830162368525, 3.7649622696887732, 2.62488208653986,
                0.6203640007289675)),
            "premium_taxes": (902.9384726385292, 3.0899880000000004, (
                3.0899880000000004, 1.9567677633434764, 1.3519460907766865,
                0.7178871561428752, 0.12922323547784875)),
            "claims_death": (49405.73966005118, 179.51920609875012, (
                8.987658125847453, 18.226675479238818, 56.162557141531764,
                146.25138701024576, 121.17678099043871)),
            "claims_lapse": (22547.154458812387, 56.79786646637751, (
                0.1155086677682963, 23.5496931639529, 51.33403984000449, 50.661702451994735,
                0.0)),
            "claims_maturity": (7558.760866104, 7558.760866104, (
                0.0, 0.0, 0.0, 0.0, 7558.760866104)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-39328.70419614663, 7674.226072556753, (
                -1732.6937547936159, 49.954868744401765, -45.01620080316739,
                -164.36150089777948, -7674.226072556753)),
            "liability_cf": (39328.70419614663, 7674.226072556753, (
                1732.6937547936159, -49.954868744401765, 45.01620080316739,
                164.36150089777948, 7674.226072556753)),
        },
        "result_pols": {
            "pols_if": (292.21423275382597, 1.0, (
                1.0, 0.6332606351039151, 0.43752470584891795, 0.23232684273947835,
                0.04181997971443537)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.334497367909002, 0.0010719841664289626, (
                8.987658125847453e-05, 0.00016923259012394307, 0.0004437966486207595,
                0.0009529614030912094, 0.000667107597863083)),
            "pols_lapse": (0.6243497599744268, 0.0042649354252909406, (
                0.0042649354252909406, 0.0010649499879420256, 0.0007352323963559219,
                0.0003892038513884535, 0.0)),
            "pols_maturity": (0.04115287211657229, 0.04115287211657229, (
                0.0, 0.0, 0.0, 0.0, 0.04115287211657229)),
            "mort_rate": (22.220105964, 0.175489874, (
                0.001077986, 0.003202171, 0.012104343999999998, 0.048126365000000004,
                0.175489874)),
            "mort_rate_mth": (1.9367002972291485, 0.015951887170160717, (
                8.987658125847453e-05, 0.0002672400284223775, 0.0010143350596846235,
                0.004101813599558191, 0.015951887170160717)),
            "lapse_rate": (14.759999999999998, 0.05, (
                0.05, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (1.244364561142016, 0.004265318777560645, (
                0.004265318777560645, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    16: {"rows": 552, "months": (0, 137, 275, 413, 551),
        "result_cf": {
            "pols_if": (202.9464094692924, 0.7045761853292647, (
                0.7045761853292647, 0.5358738040617266, 0.37312809241050726,
                0.19671686708421995, 0.04181997971443537)),
            "premiums": (13156.087911963028, 1064.8541719355308, (
                1064.8541719355308, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1427.0070817966346, 3.5228809266463235, (
                3.5228809266463235, 3.3590604993379367, 2.937076251636827,
                1.9444682147528207, 0.5190928443677931)),
            "premium_taxes": (263.12175823926054, 21.297083438710615, (
                21.297083438710615, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (32748.25211599424, 109.35374983431213, (
                13.165610959613833, 27.577892539656755, 56.148456979791014,
                99.93040994080674, 69.92846728414244)),
            "claims_lapse": (14844.293814257278, 37.91630059845029, (
                11.425144743935547, 30.00621399500808, 37.91533704896624, 27.98681982183231,
                0.0)),
            "claims_maturity": (4397.328876870319, 4397.328876870319, (
                0.0, 0.0, 0.0, 0.0, 4397.328876870319)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-40523.91573519471, 4467.776436998829, (
                1015.4434518666244, -60.94316703400277, -97.00087028039408,
                -129.86169797739188, -4467.776436998829)),
            "liability_cf": (40523.91573519471, 4467.776436998829, (
                -1015.4434518666244, 60.94316703400277, 97.00087028039408,
                129.86169797739188, 4467.776436998829)),
        },
        "result_pols": {
            "pols_if": (202.9464094692924, 0.7045761853292647, (
                0.7045761853292647, 0.5358738040617266, 0.37312809241050726,
                0.19671686708421995, 0.04181997971443537)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.32349159591691823, 0.0010719841664289626, (
                0.00013165610959613833, 0.00027577892539656755, 0.0005614845697979101,
                0.0009892048472384999, 0.000667107597863083)),
            "pols_lapse": (0.33993171729577565, 0.0011849761186450006, (
                0.0011849761186450006, 0.0009009522292451007, 0.0006267101447786945,
                0.0003292418293970651, 0.0)),
            "pols_maturity": (0.04115287211657229, 0.04115287211657229, (
                0.0, 0.0, 0.0, 0.0, 0.04115287211657229)),
            "mort_rate": (22.057064316, 0.175489874, (
                0.00224, 0.006158159, 0.017908939999999998, 0.05870160799999999,
                0.175489874)),
            "mort_rate_mth": (1.923103673311545, 0.015951887170160717, (
                0.00018685858582434545, 0.0005146340860595622, 0.0015048037958508287,
                0.005028571580570129, 0.015951887170160717)),
            "lapse_rate": (10.799999999999999, 0.02, (
                0.02, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (0.9083569784793699, 0.001682142552739574, (
                0.001682142552739574, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    17: {"rows": 552, "months": (0, 137, 275, 413, 551),
        "result_cf": {
            "pols_if": (202.9464094692924, 0.7045761853292647, (
                0.7045761853292647, 0.5358738040617266, 0.37312809241050726,
                0.19671686708421995, 0.04181997971443537)),
            "premiums": (30995.11711172293, 1268.2371335926764, (
                1268.2371335926764, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1427.0070817966346, 3.5228809266463235, (
                3.5228809266463235, 3.3590604993379367, 2.937076251636827,
                1.9444682147528207, 0.5190928443677931)),
            "premium_taxes": (619.9023422344586, 25.364742671853527, (
                25.364742671853527, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (63922.08033848633, 285.1085672083559, (
                13.398212748383813, 30.75692245583477, 78.78998270058797,
                207.23171475383546, 232.02577940556296)),
            "claims_lapse": (26326.017514983316, 68.91372926711423, (
                13.528876935363998, 40.44245563507499, 64.26151475802185,
                63.889768774892424, 0.0)),
            "claims_maturity": (14446.509606587364, 14446.509606587364, (
                0.0, 0.0, 0.0, 0.0, 14446.509606587364)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-75746.39977236517, 14679.054478837295, (
                1212.4224203104286, -74.5584385902477, -145.98857371024664,
                -273.0659517434807, -14679.054478837295)),
            "liability_cf": (75746.39977236517, 14679.054478837295, (
                -1212.4224203104286, 74.5584385902477, 145.98857371024664,
                273.0659517434807, 14679.054478837295)),
        },
        "result_pols": {
            "pols_if": (202.9464094692924, 0.7045761853292647, (
                0.7045761853292647, 0.5358738040617266, 0.37312809241050726,
                0.19671686708421995, 0.04181997971443537)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.32349159591691823, 0.0010719841664289626, (
                0.00013165610959613833, 0.00027577892539656755, 0.0005614845697979101,
                0.0009892048472384999, 0.000667107597863083)),
            "pols_lapse": (0.33993171729577565, 0.0011849761186450006, (
                0.0011849761186450006, 0.0009009522292451007, 0.0006267101447786945,
                0.0003292418293970651, 0.0)),
            "pols_maturity": (0.04115287211657229, 0.04115287211657229, (
                0.0, 0.0, 0.0, 0.0, 0.04115287211657229)),
            "mort_rate": (22.057064316, 0.175489874, (
                0.00224, 0.006158159, 0.017908939999999998, 0.05870160799999999,
                0.175489874)),
            "mort_rate_mth": (1.923103673311545, 0.015951887170160717, (
                0.00018685858582434545, 0.0005146340860595622, 0.0015048037958508287,
                0.005028571580570129, 0.015951887170160717)),
            "lapse_rate": (10.799999999999999, 0.02, (
                0.02, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (0.9083569784793699, 0.001682142552739574, (
                0.001682142552739574, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    18: {"rows": 582, "months": (0, 145, 290, 435, 581),
        "result_cf": {
            "pols_if": (224.83866606689017, 0.756176306210982, (
                0.756176306210982, 0.561860800723439, 0.3911910784589998,
                0.20728485147959066, 0.04181997971443537)),
            "premiums": (33635.7090500399, 1339.3832563179271, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (93432.5251389997, 3720.509045327575, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1611.5221326837504, 3.7808815310549098, (
                3.7808815310549098, 3.5687611316422454, 3.156431946413347,
                2.1246812993629636, 0.5454381007265446)),
            "premium_taxes": (2541.364683780792, 101.19784603291006, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (158336.13236635036, 589.0258765391588, (
                23.256434933919262, 80.07691609296629, 230.37951424665587,
                486.90776441748096, 399.07956973342993)),
            "claims_lapse": (87918.19876274954, 216.30216773359595, (
                84.47404329691783, 156.84494608943837, 212.97976269444774,
                166.85608177543224, 0.0)),
            "claims_maturity": (24702.16915977831, 24702.16915977831, (
                0.0, 0.0, 0.0, 0.0, 24702.16915977831)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-148041.15291630314, 25101.794167612465, (
                -111.51135976189201, -240.4906233140469, -446.515708887517,
                -655.8885274922761, -25101.794167612465)),
            "liability_cf": (148041.15291630314, 25101.794167612465, (
                111.51135976189201, 240.4906233140469, 446.515708887517, 655.8885274922761,
                25101.794167612465)),
        },
        "result_pols": {
            "pols_if": (224.83866606689017, 0.756176306210982, (
                0.756176306210982, 0.561860800723439, 0.3911910784589998,
                0.20728485147959066, 0.04181997971443537)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.32699712103050727, 0.0010719841664289626, (
                0.0001092707855490226, 0.0002390740938307411, 0.000533188422792015,
                0.0009412589073682604, 0.000667107597863083)),
            "pols_lapse": (0.38802631306390395, 0.0019166666901228578, (
                0.0019166666901228578, 0.0009447278049067364, 0.0006571422603933622,
                0.00034709933755089275, 0.0)),
            "pols_maturity": (0.04115287211657229, 0.04115287211657229, (
                0.0, 0.0, 0.0, 0.0, 0.04115287211657229)),
            "mort_rate": (22.114728006, 0.175489874, (
                0.001732675, 0.005094117, 0.016233791, 0.053150236999999996, 0.175489874)),
            "mort_rate_mth": (1.9279132362167988, 0.015951887170160717, (
                0.00014450437636237545, 0.0004255041346947763, 0.0013629871746880795,
                0.004540895780128618, 0.015951887170160717)),
            "lapse_rate": (11.579999999999998, 0.030000000000000002, (
                0.030000000000000002, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (0.9741521806350675, 0.002535048613836688, (
                0.002535048613836688, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    19: {"rows": 546, "months": (0, 136, 272, 408, 545),
        "result_cf": {
            "pols_if": (198.73865270218818, 0.6967132057345454, (
                0.6967132057345454, 0.5300159315768095, 0.3694586607297134,
                0.1953984204075844, 0.04181997971443537)),
            "premiums": (29726.87997813025, 1240.0883567651597, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1392.0300421098882, 3.483566028672727, (
                3.483566028672727, 3.316863061091073, 2.8938304526649126,
                1.9155649979405616, 0.5139785044275436)),
            "premium_taxes": (594.537599562605, 24.801767135303194, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (43518.30690781583, 160.09267948890124, (
                13.301412322522907, 29.759004492807904, 75.65549526042467,
                138.50833764125463, 107.8462255869199)),
            "claims_lapse": (18607.922471152757, 49.3546431254452, (
                11.885493201492997, 33.31933088746682, 48.45675057558018, 40.14726861082446,
                0.0)),
            "claims_maturity": (6735.703423772555, 6735.703423772555, (
                0.0, 0.0, 0.0, 0.0, 6735.703423772555)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (-1390.6930896265349, 245.88263058304548, (
                19.703319230323935, 20.64285888987874, 13.925013961142753,
                5.667393260679928, -48.153003098849396)),
            "net_cf": (-39730.92737665686, 6795.9106247650525, (
                -48.373790783012566, -87.03805733124453, -140.93109024981254,
                -186.23856451069955, -6795.9106247650525)),
            "liability_cf": (39730.92737665686, 6795.9106247650525, (
                48.373790783012566, 87.03805733124453, 140.93109024981254,
                186.23856451069955, 6795.9106247650525)),
        },
        "result_pols": {
            "pols_if": (198.73865270218818, 0.6967132057345454, (
                0.6967132057345454, 0.5300159315768095, 0.3694586607297134,
                0.1953984204075844, 0.04181997971443537)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.3227053404379243, 0.0010719841664289626, (
                0.0001301868443487034, 0.0002727642645440388, 0.0006139550002535399,
                0.0009825749437498733, 0.000667107597863083)),
            "pols_lapse": (0.3328549931800503, 0.0011717519375909944, (
                0.0011717519375909944, 0.0008911035237590014, 0.0006204493748602306,
                0.00032703516658155713, 0.0)),
            "pols_maturity": (0.04115287211657229, 0.04115287211657229, (
                0.0, 0.0, 0.0, 0.0, 0.04115287211657229)),
            "mort_rate": (22.043624316000002, 0.175489874, (
                0.00224, 0.006158159, 0.019759977999999997, 0.05870160799999999,
                0.175489874)),
            "mort_rate_mth": (1.921982521796599, 0.015951887170160717, (
                0.00018685858582434545, 0.0005146340860595622, 0.0016617691382330158,
                0.005028571580570129, 0.015951887170160717)),
            "lapse_rate": (10.68, 0.02, (
                0.02, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (0.8982641231629325, 0.001682142552739574, (
                0.001682142552739574, 0.001682142552739574, 0.001682142552739574,
                0.001682142552739574, 0.0)),
        },
    },
    20: {"rows": 402, "months": (0, 100, 200, 300, 401),
        "result_cf": {
            "pols_if": (108.10856244402258, 0.8268846795529393, (
                0.8268846795529393, 0.42410866155645177, 0.20756204609992948,
                0.07807501052806189, 0.016068478377314514)),
            "premiums": (14169.296602362083, 1236.0095090534894, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (654.3833292571369, 4.134423397764697, (
                4.134423397764697, 2.501008941955446, 1.4436241664389584,
                0.6404516514511764, 0.15571621188881993)),
            "premium_taxes": (283.3859320472417, 24.72019018106979, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (3100.223789017751, 9.609363501561424, (
                1.7908119162642355, 7.855577723162393, 9.428804650735659, 8.015006900521138,
                3.8448383110663245)),
            "claims_lapse": (2230.9477367324134, 8.750699732369691, (
                1.4539626145442102, 7.253080210785604, 8.423243468036816, 4.83964346871376,
                0.0)),
            "claims_maturity": (237.1823373486514, 237.1823373486514, (
                0.0, 0.0, 0.0, 0.0, 237.1823373486514)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (7663.17347795889, 1198.2847772547161, (
                -7.379197928573142, -17.609666875903443, -19.29567228521143,
                -13.495102020686074, -241.18289187160656)),
            "liability_cf": (-7663.17347795889, 1198.2847772547161, (
                7.379197928573142, 17.609666875903443, 19.29567228521143,
                13.495102020686074, 241.18289187160656)),
        },
        "result_pols": {
            "pols_if": (108.10856244402258, 0.8268846795529393, (
                0.8268846795529393, 0.42410866155645177, 0.20756204609992948,
                0.07807501052806189, 0.016068478377314514)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.20872712670537352, 0.0006406242334374283, (
                0.00046832643617257237, 0.0005237051815441595, 0.0006285869767157106,
                0.0005343337933680759, 0.0002563225540710883)),
            "pols_lapse": (0.6023453970243225, 0.007224210245546042, (
                0.007224210245546042, 0.0021785028660033126, 0.0010642614356041974,
                0.00039879269543476525, 0.0)),
            "pols_maturity": (0.015812155823243426, 0.015812155823243426, (
                0.0, 0.0, 0.0, 0.0, 0.015812155823243426)),
            "mort_rate": (21.457764846, 0.175489874, (
                0.0067753629999999995, 0.014717821999999998, 0.035741908999999995,
                0.07910434, 0.175489874)),
            "mort_rate_mth": (1.8730601757201923, 0.015951887170160717, (
                0.0005663745474469017, 0.001234837269350253, 0.003028429274652078,
                0.006843851697926118, 0.015951887170160717)),
            "lapse_rate": (24.120000000000005, 0.1, (
                0.1, 0.06, 0.06, 0.06, 0.0)),
            "lapse_rate_mth": (2.0701672702792235, 0.008741610954696721, (
                0.008741610954696721, 0.005143012831822946, 0.005143012831822946,
                0.005143012831822946, 0.0)),
        },
    },
    21: {"rows": 1, "months": (0,),
        "result_cf": {
            "pols_if": (0.041819979714435365, 0.041819979714435365, (
                0.041819979714435365,)),
            "premiums": (0.0, 0.0, (
                0.0,)),
            "rider_premiums": (0.0, 0.0, (
                0.0,)),
            "expenses": (0.2090998985721768, 0.2090998985721768, (
                0.2090998985721768,)),
            "premium_taxes": (0.0, 0.0, (
                0.0,)),
            "claims_death": (69.92846728414243, 69.92846728414243, (
                69.92846728414243,)),
            "claims_lapse": (0.0, 0.0, (
                0.0,)),
            "claims_maturity": (4397.328876870319, 4397.328876870319, (
                4397.328876870319,)),
            "div_cash_paid": (0.0, 0.0, (
                0.0,)),
            "loan_draws": (0.0, 0.0, (
                0.0,)),
            "net_cf": (-4467.466444053033, 4467.466444053033, (
                -4467.466444053033,)),
            "liability_cf": (4467.466444053033, 4467.466444053033, (
                4467.466444053033,)),
        },
        "result_pols": {
            "pols_if": (0.041819979714435365, 0.041819979714435365, (
                0.041819979714435365,)),
            "pols_new_biz": (0.0, 0.0, (
                0.0,)),
            "pols_death": (0.0006671075978630829, 0.0006671075978630829, (
                0.0006671075978630829,)),
            "pols_lapse": (0.0, 0.0, (
                0.0,)),
            "pols_maturity": (0.04115287211657228, 0.04115287211657228, (
                0.04115287211657228,)),
            "mort_rate": (0.175489874, 0.175489874, (
                0.175489874,)),
            "mort_rate_mth": (0.015951887170160717, 0.015951887170160717, (
                0.015951887170160717,)),
            "lapse_rate": (0.0, 0.0, (
                0.0,)),
            "lapse_rate_mth": (0.0, 0.0, (
                0.0,)),
        },
    },
    22: {"rows": 663, "months": (0, 165, 331, 496, 662),
        "result_cf": {
            "pols_if": (292.21423275382597, 1.0, (
                0.0, 0.6357362350748469, 0.4387069206925923, 0.23367680681243352,
                0.04181997971443537)),
            "premiums": (44630.848227513656, 1800.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "rider_premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (4071.9083241221592, 1875.024814657866, (
                0.0, 4.1734895623346855, 3.787615580002266, 2.648862285432246,
                0.6234428248150643)),
            "premium_taxes": (892.6169645502731, 36.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (49405.739660051186, 179.51920609875012, (
                0.0, 18.29792885389266, 56.31431133466379, 147.1011989207235,
                121.17678099043871)),
            "claims_lapse": (22547.154458812387, 56.79786646637751, (
                0.0, 23.254808791491044, 51.29797563082107, 50.87897885102781, 0.0)),
            "claims_maturity": (7558.760866104, 7558.760866104, (
                0.0, 0.0, 0.0, 0.0, 7558.760866104)),
            "div_cash_paid": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "loan_draws": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-39845.33204612634, 7680.561089919254, (
                -0.0, -45.72622720771839, -111.39990254548712, -200.62904005718354,
                -7680.561089919254)),
            "liability_cf": (39845.33204612634, 7680.561089919254, (
                0.0, 45.72622720771839, 111.39990254548712, 200.62904005718354,
                7680.561089919254)),
        },
        "result_pols": {
            "pols_if": (292.21423275382597, 1.0, (
                0.0, 0.6357362350748469, 0.4387069206925923, 0.23367680681243352,
                0.04181997971443537)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.334497367909002, 0.0010719841664289626, (
                0.0, 0.00016989416953053734, 0.000444995810584778, 0.0009584987040845719,
                0.000667107597863083)),
            "pols_lapse": (0.6243497599744269, 0.0042649354252909406, (
                0.0, 0.0010691131871258192, 0.0007372190330895796, 0.0003914653688706128,
                0.0)),
            "pols_maturity": (0.04115287211657229, 0.04115287211657229, (
                0.0, 0.0, 0.0, 0.0, 0.04115287211657229)),
            "mort_rate": (22.220105964, 0.175489874, (
                0.0, 0.003202171, 0.012104343999999998, 0.048126365000000004, 0.175489874)),
            "mort_rate_mth": (1.9367002972291485, 0.015951887170160717, (
                0.0, 0.0002672400284223775, 0.0010143350596846235, 0.004101813599558191,
                0.015951887170160717)),
            "lapse_rate": (14.76, 0.05, (
                0.0, 0.02, 0.02, 0.02, 0.0)),
            "lapse_rate_mth": (1.244364561142016, 0.004265318777560645, (
                0.0, 0.001682142552739574, 0.001682142552739574, 0.001682142552739574,
                0.0)),
        },
    },
}
# END generated fingerprint: WholeLife_US_SEC


# ---------------------------------------------------------------------------
# Compiled (USLIB-SEC-PLAN.md Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython CI job, which sets USLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is
# WholeLife's own: the comparison on the splice grid, at the contract's extremes and where
# the cap on mortality binds, the refusals, the deepest call, a Reference set late and the
# runner.  None asks for sec_read, sec_model or s_model, which sweep every committed point;
# the grid test alone asks for spliced.


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)


# How many rows of the splice grid C4 compares at once.  compiled_mismatches sweeps every
# row of its case in one modelx read, and keeps every value of every row, in the parent
# and in the child, until it compares them: the full grid's 153 rows at once peak at about
# 9.3 GiB, parent and child together (M15).  Twenty rows at a time hold the comparison
# near the module's own peak, for one modelx read and one child more a chunk.
C4_CHUNK = 20


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_the_splice_grid(spliced,
                                                                             sec_build,
                                                                             tmp_path):
    """C4 on the branches: compiled, every cell of the splice grid is modelx's.

    The sample traces the committed points alone, and they leave branches untaken, which
    are typed all the same, because every branch of a cell returns the one type the
    others return (sample_sec.py).  What the compiled model computes on them is held
    here: the splice grid's points, S's restated in force at T2's months and issued
    later, and the variants, the rider paid monthly, REDUCE_PREM semi-annually, the graded
    plan quarterly, and the twenty-year and to-65 premium periods, with the three overlays
    that ship off and the dividend on the paid-up additions switched on
    (:data:`SPLICED_REFS`).  The grid is the one this run's ``spliced`` selects, the core
    by default and the full grid under ``USLIB_SEC_FULL=1``, and the test carries no
    ``sec_full`` mark, since a skipped compile test fails the cython job.  The grid's SEC
    table goes beside the build :data:`C4_CHUNK` rows at a time; modelx sweeps every row
    fully, and the compiled model must agree at every argument modelx caches, identically
    on x86-64 and to 1e-12 relative elsewhere, with every raise and every ``Data`` array
    (``sec_support.compiled_mismatches``).
    """
    build = sec_build(SEC)
    table = pd.read_csv(spliced[1].Data.input_dir() / TABLE, index_col="point_id")
    assert len(table) == len(spliced[1].Data.model_point_table())
    chunks = [table.iloc[i:i + C4_CHUNK] for i in range(0, len(table), C4_CHUNK)]
    assert sum(len(chunk) for chunk in chunks) == len(table) and len(chunks) > 1
    found = []
    for i, chunk in enumerate(chunks):
        folder = compiled_case(build, tmp_path / f"grid{i}", model_points=chunk)
        found += compiled_mismatches(build, folder, refs=SPLICED_REFS)
        shutil.rmtree(tmp_path / f"grid{i}")
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


def _contract_extremes():
    """Inputs for the contract's longest frames and oldest issue ages: a table and edits.

    Seven points made from the committed twins.  Five are issued at 0, the youngest age
    the contract issues at (:data:`YOUNGEST`), so cover runs 1,200 months, 100 policy
    years, the longest: ACCUM issued 120 months on, the shipped ``future_horizon_mth``, a
    frame of 1,320 months, the longest the contract allows, which reads every cache as far
    as ``spec_sec.py`` sizes it, ``t`` to 1,321 in C4's sweep of the month after it, and
    the policy year and the attained age to 100; PUA issued now; premiums paid for twenty
    years, issued 120 months on; to attained age 65, female and quarterly, 120 months on;
    and for ten years, semi-annually, now.  And the oldest final-expense issue ages, level
    at 85 and graded at 80, 120 months on.

    The shipped tables stop short of such policies, so the copies extend them: mortality
    and the net single premiums down to age 0, falling 3% and 1.5% a year below age 18's
    value of each sex; a cash value schedule for every period and sex at 0, and final
    expense's at 85 and 80, each rising by its own step a year; a net level premium for
    every period and sex at 0; and a graded rate at 80.  The numbers mean nothing, but each
    key the copies add reads a value of its own, so that a read of the key beside the
    right one, which a padded array allows, changes a number the compiled comparison sees.
    """
    committed = _committed()

    def twin(s_point, **columns):
        return committed.loc[[_label(committed, "twin", s_point, 0)]].assign(**columns)

    later = -120
    rows = pd.concat([
        twin(4, issue_age=YOUNGEST, duration_mth=later),
        twin(2, issue_age=YOUNGEST),
        twin(2, issue_age=YOUNGEST, premium_period="PAY_20", duration_mth=later),
        twin(10, issue_age=YOUNGEST, premium_period="TO_65", premium_mode="Q",
             duration_mth=later),
        twin(9, issue_age=YOUNGEST, premium_mode="SA"),
        twin(11, issue_age=85, duration_mth=later),
        twin(12, issue_age=80, duration_mth=later)])
    rows.index = pd.Index(range(1, len(rows) + 1), name="point_id")

    def down_to_0(column, fall):
        def edit(table):
            low = []
            for sex, rows_of in table.groupby("sex"):
                first = rows_of[rows_of["age"] == rows_of["age"].min()].iloc[0]
                low.append(pd.DataFrame({
                    "sex": sex, "age": range(YOUNGEST, int(first["age"])),
                    column: [first[column] * (1 - fall) ** (first["age"] - a)
                             for a in range(YOUNGEST, int(first["age"]))],
                    "provenance": "extended"}))
            return pd.concat([*low, table], ignore_index=True)
        return edit

    periods = ("TO_100", "PAY_10", "PAY_20", "TO_65")

    def cash_values(cv):
        keys = [(q, sex, YOUNGEST) for q in periods for sex in ("M", "F")]
        keys += [("TO_100", "M", 85), ("TO_100", "M", 80)]
        added = [pd.DataFrame({"premium_period": q, "sex": sex, "issue_age": age,
                               "policy_year": range(1, 101 - age),
                               "cv_per_1000": [(9.0 + k / 8) * y
                                               for y in range(1, 101 - age)],
                               "provenance": "extended"})
                 for k, (q, sex, age) in enumerate(keys)]
        return pd.concat([cv, *added], ignore_index=True)

    def net_level_premiums(nnlp):
        added = pd.DataFrame([{"premium_period": q, "sex": sex, "issue_age": YOUNGEST,
                               "np_guar_per_1000": 2.0 + k / 4, "provenance": "extended"}
                              for k, (q, sex) in enumerate(
                                  (q, sex) for q in periods for sex in ("M", "F"))])
        return pd.concat([nnlp, added], ignore_index=True)

    def rates(r):
        graded = r[(r["product"] == "WL_FE_GRADED") & (r["sex"] == "M")].assign(
            issue_age=80, rate_per_1000=180.0, provenance="extended")
        return pd.concat([r, graded], ignore_index=True)

    return rows, {"mort_table.csv": down_to_0("mort_rate", 0.03),
                  "nsp_table.csv": down_to_0("nsp", 0.015), "cv_table.csv": cash_values,
                  "np_guar_table.csv": net_level_premiums, "premium_rates.csv": rates}


# The References the extremes run under: the splice's switches, at the shipped inflation,
# and rounding switched off, at the sentinel, so that the branch of div_base the sample
# leaves untaken runs compiled too.
EXTREME_REFS = {**SWITCHED_ON, "div_round_digits": -1000}


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_contract_extremes(
        sec_build, tmp_path):
    """C4 where the caches end: the contract's longest frames, every cell compiled.

    The seven points of :func:`_contract_extremes`, the longest frames the contract allows
    and its oldest final-expense issue ages, read every cache as far as ``spec_sec.py``
    sizes it: ``t`` to 1,321, the month after the 1,320-month frame and the count the
    roll-forward check's residual reads in it, and the policy year and the attained age to
    100.  They run every premium period and every mode, under :data:`EXTREME_REFS`, with
    rounding off.  modelx sweeps each fully, and the compiled model must agree everywhere.
    A cache one too small for the contract raises ``IndexError`` compiled where modelx
    reads on, and fails here, though the spec check passes it, which holds the caches to
    the spec and not the spec to the contract.
    """
    build = sec_build(SEC)
    rows, edits = _contract_extremes()
    folder = compiled_case(build, tmp_path / "extremes", model_points=rows, edits=edits)
    model = mx.read_model(folder, name=_name("extremes_frames"))
    try:
        frames = [projection(model, key).proj_len() for key in point_keys(model)]
    finally:
        model.close()
    assert frames == [1320, 1200, 1320, 1320, 1200, 300, 360], frames
    found = compiled_mismatches(build, folder, refs=EXTREME_REFS)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_where_the_cap_binds(sec_build,
                                                                              tmp_path):
    """C4 where ``mort_rate`` caps the annual rate at 1, and where it meets a NaN.

    The four rows of the cap's test (:func:`_capped_rows`), on whose frames the annual
    rate passes 1 from attained age 97, go beside the build, under :data:`CAPPED_REFS`.
    modelx sweeps them fully, and the compiled model must agree at every argument modelx
    caches, identically on x86-64 and to 1e-12 relative elsewhere.  No other compiled test
    reaches the side of ``min(q, 1.0)`` that returns 1.

    And the twin of S's point 2 under an A/E of NaN, a Reference, which the compiled
    model reads as modelx does, so that a NaN reaches the cap compiled: ``min`` keeps its
    first argument there as in modelx, and C4 holds the compiled NaN to modelx's, in
    every cell it reaches.
    """
    build = sec_build(SEC)
    s = _capped_s(tmp_path / "s")
    try:
        rows = _capped_rows(s, CAPPED_MTH)
    finally:
        s.close()
    folder = compiled_case(build, tmp_path / "capped", model_points=rows)
    found = compiled_mismatches(build, folder, refs=CAPPED_REFS)
    committed = _committed()
    twin = committed.loc[[_label(committed, "twin", CAPPED_POINT, 0)]]
    folder = compiled_case(build, tmp_path / "nan", model_points=twin)
    model = mx.read_model(folder, name=_name("nan_ref"))
    try:
        model.Projection.ae_best_est = float("nan")
        assert math.isnan(_point(model, CAPPED_POINT).mort_rate(0))
    finally:
        model.close()
    found += compiled_mismatches(build, folder, refs={"ae_best_est": float("nan")})
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


# The cases of MALFORMED whose duration_mth no int64 holds exactly, which the compiled
# refusals test reads compiled.
PAST_INT64 = ("a duration past int64", "durations of 2**53 months at two points")


# The compiled model's own refusals: what it does with a key past the caches spec_sec.py
# sizes, which no projection the contract allows reaches, as (cell, arguments, what modelx
# does).  modelx answers a month and a policy year outside cover with a zero, as the cells
# say, and refuses a code past the timings and the kinds; compiled, each is past a cache,
# and raises IndexError rather than read or write beyond it.  claim_pp's cache is five
# kinds wide, timing's width (spec_sec.py), so its first key past the cache is 5.
COMPILED_ONLY = [
    ("net_cf", (1322,), ("ok", 0.0)),
    ("cv_pp_anniv", (-1,), ("ok", 0.0)),
    ("pols_if_at", (0, 5), ("raised", "ValueError: invalid timing")),
    ("claim_pp", (0, 5), ("raised", "ValueError: invalid kind")),
]

# The kinds past MATURITY that claim_pp's cache still holds, since it is as wide as
# timing's (spec_sec.py): there the cell itself refuses the code, compiled as in modelx.
KINDS_IN_CACHE = [(0, 3), (0, 4)]


# The label accessors, which return the point's column as read (sample_sec.py).
LABELS = ("product", "premium_period", "sex", "risk_class", "dividend_option",
          "premium_mode")
DIVIDEND_STATE = ("pua_rider_premium", "pua_face_init", "pua_face_prev_anniv_init",
                  "div_accum_init", "div_prev_anniv_init")


@pytest.mark.cython
def test_the_compiled_model_returns_a_label_that_is_not_text_as_modelx_does(sec_build,
                                                                             tmp_path):
    """C4 on labels that are not text: the compiled accessors return what modelx returns.

    ``Data`` accepts a table whose labels are blank, which pandas reads as NaN, or a
    number, on the first committed point with its paid-up additions, dividends and rider
    premium 0, which a product other than WL_PAR may not carry.  modelx returns each
    label as pandas reads it, and an accessor typed ``str`` would raise ``TypeError``
    compiled; the sample types the labels as Python objects from a blank copy
    (sample_sec.py, M26).  So on a copy of that point with every label blank, and on one
    with every label the number 7, after checking that modelx returns NaN and 7, each
    label is called compiled and must return what modelx returns
    (``sec_support.label_mismatches``).
    """
    clear = {column: 0.0 for column in DIVIDEND_STATE}
    build = sec_build(SEC)
    first = _committed().iloc[[0]]
    found = []
    for case, value in (("blank", None), ("numeric", 7)):
        rows = first.assign(**{label: value for label in LABELS}, **clear)
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
    the compiled model as out of modelx.  So ``proj_len()`` refuses a point past its
    cover, naming it by ``point_id()``, on the committed table and on the extract whose
    labels are not its positions plus one (:func:`_extract`), and a point the contract
    does not issue, which the compiled caches are not sized for (:data:`NOT_ISSUED`), each
    on its own inputs and References.  The one reader of each padded table or join
    refuses a key beyond it (:data:`BEYOND`); a premium period and a mode ``Data`` cannot
    decode are refused when another point first reads its premium; and every case of
    :data:`UNDECODABLE` a projection meets, the text keys of the five tables among them,
    and every case of :data:`NOT_FINITE`, each a value a cap, a ``min`` or a ``max`` reads
    outside its range, are refused by the point's ``result_cf()``, on its own inputs,
    compiled as in modelx, so a compiled ``Data`` cell refuses each value its modelx cell
    refuses.

    And a ``duration_mth`` past what an int64 holds exactly (:data:`PAST_INT64`), which
    the table's own check refuses before ``Data.duration_mth`` casts it: there no point's
    key can be taken from the table, so it is read through that vector, compiled as in
    modelx.  The issue age's, of ``2**53`` or more, are :data:`UNDECODABLE`'s, above.

    And a kind past ``MATURITY`` inside ``claim_pp``'s cache (:data:`KINDS_IN_CACHE`),
    which the cell refuses, ``invalid kind``, compiled as in modelx.

    And the refusals that are the compiled model's alone (:data:`COMPILED_ONLY`): a month
    past the ``t`` cache, a policy year below the ``y`` cache, and a timing and a kind past
    their caches, each raising ``IndexError`` compiled, beside what modelx does.

    The cases share one directory, which each case's inputs overwrite in turn, and one
    copy of the compiled package: each child reads its inputs afresh, as the compiled
    ``Data`` reads its files once an import.
    """
    build = sec_build(SEC)
    committed, extract = _committed(), _extract()
    moved = _label(committed, "derived", 5, 108)
    last = extract.index[extract["policy_id"] == "WLPAR-000005-M659"][0]
    beyond, beyond_edits = _beyond()
    # Each case: (case, table, edits, References, [(label, cell, args)], compiled only).
    cases = [
        ("past its cover", _set("duration_mth", [moved], 660)(committed), None, {},
         [(moved, "proj_len", ())]),
        (f"past its cover, labelled {last}", _set("duration_mth", [last], 661)(extract),
         None, {}, [(last, "proj_len", ())]),
        *((case, committed if edit is None else edit(committed), None, refs,
           [(point, "proj_len", ())]) for case, edit, refs, point, _, _ in NOT_ISSUED),
        ("beyond the tables", beyond, beyond_edits, {},
         [(label, cell, args) for label, cell, args, _ in BEYOND]),
        ("an unknown mode, at another point's first premium",
         _set("premium_mode", [4], "W")(committed), None, {}, [(1, "premiums", (0,))]),
        ("an unknown premium period, at another point's first premium",
         _set("premium_period", [4], "PAY_15")(committed), None, {},
         [(1, "premiums", (0,))]),
        *((case, committed if edit is None else edit(committed), edits, {},
           [(point, "result_cf", ())])
          for case, edit, edits, _, _, point in UNDECODABLE + NOT_FINITE
          if point is not None),
        ("a kind past MATURITY, inside claim_pp's cache", committed, None, {},
         [(1, "claim_pp", args) for args in KINDS_IN_CACHE]),
    ]
    dest = tmp_path / "refused"
    folder = compiled_case(build, dest)
    found, refused = [], 0
    for case, table, edits, refs, calls in [*cases, ("compiled only", committed, None, {},
                                                     [(1, c, a) for c, a, _ in
                                                      COMPILED_ONLY])]:
        temp_inputs(dest, model_path(SEC), model_points=table, model_point_file=TABLE,
                    edits=edits)
        model = mx.read_model(folder, name=_name("refused"))
        try:
            for ref, value in refs.items():
                setattr(model.Projection, ref, value)
            keys = dict(zip(model.Data.model_point_table().index, point_keys(model)))
            job, want = {"refs": refs, "calls": {}}, []
            for label, cell, args in calls:
                job["calls"].setdefault(keys[label], []).append((cell, args))
                try:
                    value = projection(model, keys[label]).cells[cell](*args)
                    want.append(("ok", value))
                except Exception as err:        # what modelx raised is what compiled must
                    want.append(("raised", _raised(err)))
        finally:
            model.close()
        got = run_compiled(dest, build.package.name, job)
        assert got["exit"] == 0, f"{case}: the compiled run failed:\n{got['stderr']}"
        assert all(got["compiled"].values()), got["compiled"]
        have = {key: iter(values) for key, values in got["values"].items()}
        for (label, cell, args), modelx_did in zip(calls, want):
            status, text = next(have[keys[label]])
            where = f"{case}: point {label}: {cell}{args}"
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
    for case, edit, _ in MALFORMED:
        if case not in PAST_INT64:
            continue
        temp_inputs(dest, model_path(SEC), model_points=edit(committed),
                    model_point_file=TABLE)
        model = mx.read_model(folder, name=_name("refused"))
        try:
            model.Data.duration_mth()
            modelx_did = ("ok", None)
        except Exception as err:                # what modelx raised is what compiled must
            modelx_did = ("raised", _raised(err))
        finally:
            model.close()
        got = run_compiled(dest, build.package.name,
                           {"refs": {}, "calls": {}, "data": ["duration_mth"]})
        assert got["exit"] == 0, f"{case}: the compiled run failed:\n{got['stderr']}"
        assert all(got["compiled"].values()), got["compiled"]
        status, text = got["data"]["duration_mth"]
        if modelx_did[0] != "raised":
            found.append(f"{case}: Data.duration_mth: modelx returned, where a refusal was "
                         f"meant")
        elif (status, text) != modelx_did:
            found.append(f"{case}: Data.duration_mth: compiled {status} {text!r}, modelx "
                         f"{modelx_did}")
        refused += 1
    assert not found, "\n".join(found)
    assert refused == sum(len(calls) for *_, calls in cases) + len(PAST_INT64)


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

    On the five points of :func:`_contract_extremes` issued at age 0, whose cover runs
    1,200 months, a cold ``net_cf`` in the last month runs the count chain from the end
    of the frame back to ``t_entry``, 1,211 cells deep in modelx on a model just read
    (:func:`test_every_chain_runs_one_cell_a_month_from_a_cold_start`), and compiled it
    runs on the C stack, which the interpreter's recursion limit does not count.  1 MiB
    is the stack MSVC gives an executable's main thread unless the executable asks for
    more: a host that embeds Python, where python.exe itself asks for 2,000,000 bytes.  A
    thread whose stack is reserved at 1 MiB stands in for it on every platform
    (``sec_support.run_compiled``), and in one each call runs cold and returns modelx's
    number, identically on x86-64 (``sec_support.exact_here``) and to 1e-12 elsewhere.
    With gcc the calls need about 290 KiB.  A stack too small kills the child, and the
    test fails naming the stack.  The thread's stack is read back too, from Windows or
    from glibc, and must be at most 1 MiB and a page: a stand-in larger than asked for
    would stand for nothing.  And the calls run again on the child's main thread, which is
    what ``run_sec.py --cython`` runs on.

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
    rows, edits = _contract_extremes()
    rows = rows[rows["issue_age"] == YOUNGEST]
    folder = compiled_case(build, tmp_path / "extremes", model_points=rows, edits=edits)
    model = mx.read_model(folder, name=_name("extremes"))
    try:
        calls, want = {}, {}
        for key in point_keys(model):
            proj = projection(model, key)
            last = proj.proj_len() - 1
            assert last - proj.t_entry() == 12 * (100 - YOUNGEST) - 1
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
STALE_CHILD = """\
import json, sys
sys.path.insert(0, sys.argv[1])
model = __import__(sys.argv[2]).mx_model
p = model.Projection
early = p[1]
values = [p.expenses(12), early.expenses(12)]
p.inflation_rate = 0.0
values += [p.expenses(12), early.expenses(12), p[2].expenses(12)]
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
    the anchor cell, and the twins of S's points 2 and 3, made before and after, so that a
    modelx-cython that began to clear caches would be seen here, and the advice changed
    with it.  A compiled value meets modelx's as C4 holds it (:func:`_as_modelx`), and one
    the compiled model kept, its own value of before, identically.
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
        before = (p.expenses(12), p[1].expenses(12))
        p.inflation_rate = 0.0
        fresh = (p.expenses(12), p[1].expenses(12), p[2].expenses(12))
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
    modelx's: point 19's description, the loan point in force mid-year, and its first
    twelve rows and counts, and the block's lines for each point, its first twelve rows
    and its first twelve projection years.

    The same output is what a runner that ignored ``--build`` and ran modelx would print,
    so the runner is also given a directory that holds no build, and must refuse it,
    saying so, rather than print anything.
    """
    build = sec_build(SEC)
    runner = model_path(SEC).parent / "run_sec.py"
    for args in (("19",), ("--block",)):
        expected = _run_sec(runner, *args)
        assert _run_sec(runner, *args, "--cython", "--build", str(build.out)) == expected
    empty = tmp_path / "no_build"
    empty.mkdir()
    done = _run_sec(runner, "19", "--build", str(empty), check=False)
    stderr = done.stderr.decode(errors="replace")
    assert done.returncode != 0 and done.stdout == b"", stderr
    assert f"holds no build of {SEC} for this interpreter" in stderr, stderr
