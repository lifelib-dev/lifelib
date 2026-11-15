"""In-force tests for MYGA_US_SEC: the splice, future business, counts, regeneration.

``MYGA_US_SEC`` is ``MYGA_US_S`` taught to run in force at a valuation date
(USLIB-SEC-PLAN.md, milestone M7).  It runs on two clocks: ``t`` counts months from the
valuation date, the same month for every model point, and ``duration_mth(t)`` counts the
months the contract has been in force, ``duration_mth_init() + t``.  A model point may be a
contract already in force at the valuation date, in any month of its contract year, one
issued at it, or one to be issued after it, as in ``basiclife/BasicTerm_SE``.  A contract in
force opens with ten columns of state beside its count: the account value, the Model #805
floor and ``P_accum@GMIR`` entering month 0; the interest credited to date, and to the
anniversary that opened the contract year under way; that year's free-withdrawal allowance
and the part of it unused; the IRC 72 basis; and the declared rate and the MVA reference
yield ``i0`` in force.

The worked example is not restated here.  On a point issued at the valuation date the two
clocks coincide and the model is ``MYGA_US_S``, and ``test_model_conventions.py`` asserts
that cell by cell on the twins of S's seven points (T1), so every golden of
``test_fixed_deferred_annuity_us.py`` on a cell S's sweep reaches holds on this model with
no number copied: the worked example's table, both surrender traces line by line and the
roll-forwards.  The statutory nonforfeiture rate and its compliance test, which no report
reads, and the geometric factor at the specimen's arguments are evaluated on S's points by
the splice's own sweep (``_sweep_s``) and compared on every restated row.  The conventions
also hold the SEC family's other
rules: every frame opens at ``t = 0``, ``pols_if`` is the ``BEF_DECR`` count, ``BEF_DECR``
is ``BEF_NB`` plus the month's new business, new business enters once, and nothing happens
before issue.  This module holds the rest of the plan's tests (its §5.2) and the product's
own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's and in
  ``result_pols``.  The months straddle the contract year and the guarantee period: the
  first year's last month and the first anniversary, the month after the excess
  withdrawal, the last month of the initial term, the window, which is the first renewal
  month, the month after it and a renewal period well under way, and the last covered
  month.  They run on every renewal
  architecture, free-withdrawal rule, floor convention, MVA family and cap, on stepped
  rate scenarios, and four variants of S's points, in a copy of S's table, add the female
  cell, the GMIR's other two bands, a zero basis, premium tax, the floor's charge, a
  seven-year guarantee period and issue age 85.
* T3, future new business: a point issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before issue, no decrement rate evaluated there,
  and no age or contract year read before the contract's first.
* D11's R1, R1a and R2, and D3's clock: on the splice's grid no cell is called at a
  negative month, none evaluated on the books reads a month before them, none reads
  beyond ``t + 1``, and no state keyed by contract year is asked about a year that closed
  before the valuation date; on the committed points no recursion runs backward over the
  frame, the deepest cold call runs one cell a month, and the policy clock is a closed
  form.
* T4, the count algebra: the count rolls forward through new business and decrements,
  ``result_pols`` is S's report with the new business beside it, and multiplying
  ``policy_count`` by 2.5, with every assumption that ships at zero switched on,
  multiplies every flow and moves no per-contract value.
* T5, validation: each malformed in-force row is refused as the table is read, naming its
  point, a key that the table it joins lacks among them, and each assumption table whose
  keys cannot be read is refused, naming the file and the lines, before a projection reads
  a value from it; the future horizon is a Reference that bounds future business, and at
  0 refuses it; a point past maturity is refused by ``proj_len()``; the edges of the
  interface are accepted, and each rule just outside its window of months or ages and
  its cent; and every state S reaches, restated in force, is accepted on each set of
  inputs S runs on.
* T6, regeneration: the committed ``model_point_table_sec.csv`` is what the generator makes
  of ``MYGA_US_S`` and its table as they stand.
* Then the two clocks on the shipped points, the opening state as S carries it, each
  column shown on a committed row, the rate and ``i0`` on a renewal valuation, the
  free-withdrawal state of the year under way, the scenario on the valuation clock,
  withdrawals on the policy clock, expense inflation on the valuation clock, the premium
  and acquisition on new business, per contract issued, the checks' tolerance on a point
  of a million contracts, the values outside cover, the block, an in-force extract, the
  runner, the docstrings, the shared input tables, and what the default grid reaches.
* C2, the fingerprint: every committed point computes what the model computed when Phase 1
  ended, frozen at the end of this module before Phase 2 changed anything (§5.4).

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``, ``-k``
for one issued ``k`` months on.

**The core grid and the full one** (USLIB-SEC-PLAN.md K6).  A MYGA projection costs about
five times a Term one, and T2 and T3 over every point at every month, 72 cases and 18,
would more than double this module's run time in every run.  By default they run a core
of 17 and 7 cases, chosen so that between them they reach every branch, every
opening-state column, every kind of valuation month and every product switch the full
grid reaches, which ``test_the_core_grid_reaches_every_branch`` asserts, and so that each
fault in how the opening state is read fails at least one of them.  The other cases, and
the rules test's scan of their rows, carry the ``sec_full`` marker and are skipped, with
the reason shown, unless ``USLIB_SEC_FULL=1`` is set.  They are never dropped: one leg of
the CI matrix sets it, so every CI run runs the full grid, and ``USLIB_SEC_FULL=1 python
-m pytest -m sec_full`` on this module runs them alone.  Memory is the other cost: a
projected point holds its cached values and their dependency graph, so a row read once, a
splice case's or a point of a temporary copy, is released as soon as it has been read
(``_release``), and the splice's rows are held one at a time, however large the grid.

Every test keeps five rules.  Each model is read under a name of its own and closed:
``test_fixed_deferred_annuity_us.py`` reads S under its default name, and reading a model
under a name in use renames the open one.  No test writes inside the library tree: every
changed input goes through ``sec_support.temp_inputs`` into a temporary directory, because
a CSV added beside the models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``us_registry.point_keys`` and the ItemSpaces from
``us_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor Phase 2's positions can
point a test at the wrong row; a table the model refuses has no keys, and a row's is
taken from the file as ``run_sec.py`` takes one (``_file_key``).  Every Reference a
test changes is set on a model read afresh, before it computes anything, because a
compiled model never clears a cache.  And a timing or a kind is passed through
``_timing``, which hands the model its own Reference where it defines one and the string
otherwise, and every twin comparison goes through ``_mismatches``, which passes the SEC
Space's codes, so that the same calls serve Phase 2's int codes (C1).
"""
import ast
import dataclasses
import importlib.machinery
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
import warnings

import modelx as mx
import numpy as np
import pandas as pd
import pytest

from sec_support import (
    GENERATED_COLUMNS, SEC_SPECS, TWIN_EXEMPT_DEFAULT, build_sec_table,
    check_generated, codes, compiled_case, compiled_mismatches, exact_here,
    fingerprint_mismatches, frame_mismatches, run_compiled, shift_months, sweep,
    temp_inputs, twin_mismatches)
from us_registry import model_path, point_keys, projection

SEC, TWIN, TABLE = "MYGA_US_SEC", "MYGA_US_S", "model_point_table_sec.csv"
SPEC = SEC_SPECS[SEC]

# S's seven points, all issued at t = 0: the worked example's anchor and its six variants on
# the switches the technical notes make first-class parameters.
S_POINTS = (1, 2, 3, 4, 5, 6, 7)

# T2's months (USLIB-SEC-PLAN.md §7.10): 11, the last month of the first contract year, its
# anniversary at t = 1, where year 2's allowance is fixed from inside the frame; 12, the
# first anniversary, the year's allowance read at t = 0 and the anchor's $4,000 there; 30,
# mid-year after point 5's excess withdrawal at 29; 59, the last month of the initial term,
# with the window and the redeclaration at t = 1; 60, the window, the rate redeclared and
# i0 re-locked from the scenario at t = 0; 61 and 89, inside the first renewal period, its
# rate and i0 fixed before the valuation date (point 3, Camp B, redeclares every
# anniversary, at 60 and at 84); and 479, the last covered month.
SPLICE_MTHS = (11, 12, 30, 59, 60, 61, 89, 479)

# Four more S points, in the splice's copy of S's table and never in the committed one, for
# the branches and the categories S's own points do not reach:
#
# 8, S point 1, female, at a GMIR of 2%, the factor's middle band, with the statutory $50
#   charge on the floor and 2% premium tax: the female mortality rows, the charge c(t) and
#   the premium tax, all zero or absent on S's points;
# 9, S point 3 at a GMIR of 3%, the high band, as an IRA with no basis: every withdrawal
#   all gain, and Camp B's renewal rate floored at the GMIR;
# 10, S point 5 with a seven-year guarantee period: a renewal schedule that runs out before
#   the period does, a window at policy month 84, and the interest-only rule over it;
# 11, S point 4 issued at 85: the attained-age cap on the surrender charge, and cover that
#   ends fifteen years on, with its third guarantee period.
#
# Each variant is (the S point it changes, the columns it changes); the policy_id keeps the
# generated ids apart.
VARIANTS = {
    8: (1, {"policy_id": "MYGA-900008", "sex": "F", "gmir": 0.02,
            "mgsv_annual_charge": 50.0, "premium_tax_rate": 0.02}),
    9: (3, {"policy_id": "MYGA-900009", "gmir": 0.03, "tax_status": "IRA",
            "tax_basis_initial": 0.0}),
    10: (5, {"policy_id": "MYGA-900010", "guar_period": 7}),
    11: (4, {"policy_id": "MYGA-900011", "age_at_entry": 85}),
}
VARIANT_MTHS = {8: (12, 30, 61), 9: (61, 72, 89), 10: (30, 83, 84, 85, 100),
                11: (59, 60, 61, 125, 179)}

# T2's cases, as (row_kind, S point, source_mth): each S point restated in force at each of
# the months above, then each variant at its own.  MYGA_US_S has no in-force point, so no
# twin of one is a splice case (§5.2).  T3's cases, as (S point, k): issued a month on,
# which puts the contract anniversaries a month off the valuation years, and 15 months
# on, more than a year, so that a missing guard reads contract year -1 before issue.
SPLICES = (tuple(("derived", p, d) for p in S_POINTS for d in SPLICE_MTHS)
           + tuple(("derived", p, d) for p, mths in VARIANT_MTHS.items() for d in mths))
IN_FORCE_TWINS = ()
FUTURE_MTHS = (1, 15)
FUTURES = (tuple((p, k) for p in S_POINTS for k in FUTURE_MTHS)
           + tuple((p, 1) for p in VARIANTS))

# The default run's cases (the module docstring), each with what it is there for.  The
# rest of SPLICES and FUTURES run with USLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("derived", 1, 11): "the first contract year, its anniversary at t = 1",
    ("derived", 1, 12): "an anniversary: the year's allowance read at t = 0, the $4,000",
    ("derived", 5, 11): "interest_only, a year's last month: year 3's from frame month 0",
    ("derived", 5, 12): "interest_only on an anniversary: last year's interest allowed",
    ("derived", 5, 30): "after the excess withdrawal: the interest cap, the net floor",
    ("derived", 3, 30): "Camp B in its initial term: the GMIR-floored cap reads P_accum",
    ("derived", 2, 59): "the last month of the initial term: the window at t = 1",
    ("derived", 4, 60): "the window at t = 0: geometric, no exemption, i0 re-locked",
    ("derived", 2, 61): "a renewal period: the rate and i0 from the opening state",
    ("derived", 4, 89): "a renewal period under way: i0 apart from the yield at t = 0",
    ("derived", 6, 30): "the asymmetric cap binding",
    ("derived", 7, 61): "the declared differential renewed at 6% or more; both factors",
    ("derived", 3, 89): "Camp B past its initial term: the rate declared at 84",
    ("derived", 3, 479): "the last covered month: the deemed maturity",
    ("derived", 8, 30): "female, the GMIR's middle band, the floor's charge",
    ("derived", 9, 72): "the GMIR's high band, a zero basis, a redeclaration at t = 0",
    ("derived", 10, 84): "a seven-year period: its window at t = 0, its schedule run out",
}
CORE_FUTURES = {
    (1, 1): "issued a month off the valuation anniversaries",
    (1, 15): "issued more than a year on: contract year -1 before issue",
    (3, 1): "Camp B",
    (5, 15): "interest_only, its excess withdrawal at t = 44",
    (7, 1): "the declared differential",
    (8, 1): "premium tax and the floor's charge on new business",
    (10, 1): "a seven-year period",
}

SEC_FULL = os.environ.get("USLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "USLIB_SEC_FULL=1 (USLIB-SEC-PLAN.md K6)"))

# What the splice sets in both models, S and SEC alike, before either evaluates anything.
# Expense inflation is read on the valuation clock in SEC and on the policy clock in S
# (D7), so at the shipped 2.5% the expenses of a point opened at d differ by 1.025 to the
# completed years, by design, and at 0 both factors are 1; the clock itself is asserted on
# its own, at the shipped rate.  The rest are assumptions that ship at a value that hides
# some of the state from any comparison:
#   free_wd_util 0.5, the utilization withdrawal at each contract-year start, without which
#     the allowance, the remainder, the floor, P_accum and the basis move on the anchor's
#     $4,000 and point 5's $20,000 alone;
#   renewal_spread 0.75%, so that the renewal rate parts from the market rate beyond the
#     50 bp buffer, the dynamic lapse is live, and a rate declared at the wrong month
#     reads a different market;
#   expense_acq 150, acquisition on new business, per contract issued;
#   load_prem_rate 1%, so that the premium credited is not the premium, and a formula that
#     credits P where it should credit P (1 - load) shows.  It also wakes MYGA_US_S's
#     gmir_floor quirk, a payment on a withdrawal of 0, alike in both models.
# The identity does not depend on the values, only on both models having the same ones.
SPLICED_REFS = {"inflation_rate": 0.0, "free_wd_util": 0.5, "renewal_spread": 0.0075,
                "expense_acq": 150.0, "load_prem_rate": 0.01}

# Every assumption that ships at zero, switched on in T4 at the value T2 gives it, in the
# SEC model itself, so that every flow is nonzero on some point (§5.2, T4, precised at
# M11): the four References above but the inflation, which ships at 2.5%; and the premium
# tax and the floor's annual charge, columns at 0 on every S point, at variant 8's 2% and
# $50 on every committed row.
SWITCHED_ON = {ref: value for ref, value in SPLICED_REFS.items() if ref != "inflation_rate"}
SWITCHED_ON_COLUMNS = {column: VARIANTS[8][1][column]
                       for column in ("premium_tax_rate", "mgsv_annual_charge")}

# Each shipped scenario replaced, in the splice's copies alone, by a stepped one under the
# same id, at levels of its own: the market moves within the initial term, from a
# competitive rate to an uncompetitive one, and within each renewal period, so that a rate
# read at the current month rather than at the declaration differs; at the base
# scenario's second renewal, month 120, it falls to 0.90%, where the renewal rate floors at
# the GMIR; and the yield moves within each period, so that i0 locked at its start differs
# from the current yield.  The months are S's; each spliced row reads a copy re-based to its
# own month (_rebase).
STEPPED = pd.DataFrame(
    [("base", 0, 0.0650, 0.0445), ("base", 25, 0.0550, 0.0350),
     ("base", 60, 0.0700, 0.0520), ("base", 67, 0.0600, 0.0470),
     ("base", 95, 0.0450, 0.0300), ("base", 120, 0.0300, 0.0090),
     ("base", 150, 0.0500, 0.0400),
     ("stress", 0, 0.1000, 0.0445), ("stress", 40, 0.0800, 0.0500),
     ("stress", 60, 0.0900, 0.0600), ("stress", 73, 0.0700, 0.0550),
     ("stress", 88, 0.0850, 0.0450), ("stress", 120, 0.0600, 0.0300),
     ("stress", 200, 0.0750, 0.0500),
     ("differential", 0, 0.1000, 0.0600), ("differential", 30, 0.0900, 0.0650),
     ("differential", 60, 0.0950, 0.0700), ("differential", 70, 0.0800, 0.0500),
     ("differential", 125, 0.0700, 0.0450)],
    columns=["scenario_id", "t", "mva_ref_yield", "market_rate"]).assign(
        provenance="stepped for a test")


def _stepped(_):
    """The stepped scenarios, in place of the shipped flat ones (:data:`STEPPED`)."""
    return STEPPED.copy()


def _renewal_apart(table):
    """The renewal schedule raised by 0.5%, so that no renewal rate equals an initial one.

    The shipped renewal year 1 and initial year 5 are both 5%, so a schedule joined on the
    wrong key would read the same number there, and no comparison with S could see it.
    """
    renewal = table["schedule"] == "renewal"
    out = table.copy()
    out.loc[renewal, "surr_charge_rate"] = out.loc[renewal, "surr_charge_rate"] + 0.005
    return out


def _factors_cut(table):
    """The declared-differential factors cut to 0-3 years, so the flat branch is reached.

    Beyond the table's last row the factor is flat; no shipped period is long enough to
    get there on the full table, and a five-year period does on this one.
    """
    return table[table["years_remaining"] <= 3].copy()


# The input files the splice's copies change, S's and SEC's alike.  SEC's scenario file is
# then replaced by its re-based copies (_rebase).
SPLICED_EDITS = {"rate_scenario.csv": _stepped, "surr_charge_table.csv": _renewal_apart,
                 "mva_factor_table.csv": _factors_cut}

# The cells T2 and T3 skip beyond T1's, which already drop av_pp_init, mgsv_pp_init and
# result_pols as a whole (the spec's exempt).  proj_len counts from the valuation date on
# SEC and from issue on S, so it differs by d, or by -k, by design; frame_mismatches
# asserts what it must get right, that both frames end at the same instant.  scenario_id
# names a spliced row's own re-based copy of its S scenario (_rebase), so it differs by
# design; every cell the scenario drives is compared.  And on a row restated in force,
# tax_basis_pp_init is the basis entering the valuation month, where S's is the basis at
# issue, the opening of S's frame; tax_basis_pp and taxable_wd_pp, which open from it, are
# compared from month 0 on.  A future row's is the basis at issue, as S's is, and T3
# compares it.
SPLICE_EXEMPT = (TWIN_EXEMPT_DEFAULT | SPEC.exempt
                 | {"proj_len", "scenario_id", "tax_basis_pp_init"})
FUTURE_EXEMPT = TWIN_EXEMPT_DEFAULT | SPEC.exempt | {"proj_len", "scenario_id"}

# The roll-forward residuals, whose exact value is 0 and whose computed value is rounding
# around it: an opening state that comes back from the CSV an ulp off moves each by an ulp
# of what it closes.  T2 and T3 compare them at the harness's absolute floor of 1e-9, and
# every other cell and column with none (_compare), since a count late in a long frame, or
# an expense on it, falls far below 1e-7, where a floor of 1e-9 would pass any error (§5.2,
# precised at M11).
RESIDUALS = frozenset({"check_av_roll_fwd_resid", "check_pols_roll_fwd_resid"})

# The cells keyed by contract year whose value is the state of that year.  A year that
# closed before the valuation date is no year of an SEC row's frame, as a month before it
# is none, so T2 skips those keys (_on_the_books), and the rules test asserts that the
# model asks about none of them.
YEAR_STATE = ("free_wd_base", "free_wd_allow")

# The result_cf columns that expense inflation moves, and the cells they are made of: on
# the committed points, at the shipped 2.5%, the only places an in-force row departs from S.
INFLATED = ("expenses", "net_cf")
INFLATION_CELLS = frozenset({"inflation_factor", "expenses", "net_cf", "result_cf"})

# The decrement rates, none of which may be evaluated before issue (R1, D4).
DECREMENT_RATES = ("annuitization_rate", "mort_rate", "mort_rate_mth", "lapse_rate",
                   "lapse_rate_mth")

# The cells that scale with policy_count.  Every other cell is a per-contract amount, a
# rate, a clock or a flag, and must not move when the count does.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz",
    "pols_annuitization", "pols_death", "pols_lapse", "pols_maturity", "pols_decr",
    "premiums", "prem_to_av", "withdrawals", "claims", "claims_from_av", "claims_over_av",
    "commissions", "premium_taxes", "expenses", "net_cf", "av_at", "inv_income",
    "wd_from_av", "av_change", "check_av_roll_fwd_resid", "check_pols_roll_fwd_resid",
    "result_cf", "result_pols"})

# What T4 multiplies policy_count by: not a whole number, because a count of contracts need
# not be one, so that a flow which read the count as whole contracts would not follow it.
COUNT_FACTOR = 2.5

# The counted cells T4 holds otherwise than to 1e-12 of themselves, value by value (§5.2,
# T4, precised at M4 and M10): the change in the account value in force, a difference of
# two counted balances, whose sides round apart where they nearly cancel, as on point 7 at
# t = 236 by 5.1e-12 of itself, to 1e-12 of its largest magnitude on the point; and the
# roll-forward residuals, whose exact value is 0 (RESIDUALS), to their floor of 1e-9.
CANCELLING = frozenset({"av_change"})

# result_pols' columns, in its order: the count, the new business within it, the month's
# annuitizations, deaths and surrenders in processing order, the deemed maturities of the
# last covered month, and the notes' end-of-month l(t), as MYGA_US_S reports it.
RESULT_POLS = ["pols_if", "pols_new_biz", "pols_annuitization", "pols_death",
               "pols_lapse", "pols_maturity", "pols_if_aft_decr"]
OUTFLOWS = RESULT_POLS[2:6]

# The five count timings, BEF_NB the one running in force adds; the account value's three;
# and the four benefit kinds.  Each is passed through _timing.
TIMINGS = ("BEF_NB", "BEF_DECR", "BEF_MORT", "BEF_LAPSE", "AFT_DECR")
AV_TIMINGS = ("BEF_WD", "BEF_INV", "EOM")
KINDS = ("DEATH", "LAPSE", "ANNUITIZATION", "MATURITY")
KINDED = ("pols_decr", "claim_pp", "claim_from_av_pp", "claims", "claims_from_av",
          "claims_over_av")
# The two of them that take the four kinds' total too, MYGA_US_S's kind=None, which is
# the code ALL at stage "EC" (R12).
TOTALLED = ("claims", "claims_over_av")

# What each cell holds outside cover, before issue and from the month cover has ended, as
# its docstring says: no count, so no cash flow; no account value, floor, allowance or
# basis; no rate, scale or charge; and no question about the contract answered yes.  The
# MVA factor gating the dynamic lapse is 1.0, its "no MVA in force".  The type is part of
# the value: a count or an amount is a float in every branch and a flag a bool, because
# Phase 2 types a cell by the values it returns (USLIB-SEC-PLAN.md F3).  The guard test
# also calls pols_if_at, av_pp_at and av_at at each timing and the KINDED cells at each
# kind, ALL among them where a cell takes it, all 0.0: the totals, claims(t, ALL) and
# claims_over_av(t, ALL), which take no kind=None at stage "EC", among them.  The whole
# years of the MVA term are an int, 0.
OUTSIDE_COVER = {
    "is_active": False, "in_gp_window": False, "mva_in_force": False,
    "pols_if": 0.0, "pols_new_biz": 0.0, "pols_annuitization": 0.0, "pols_death": 0.0,
    "pols_lapse": 0.0, "pols_maturity": 0.0,
    "credit_rate": 0.0, "credit_rate_mth": 0.0, "mort_rate": 0.0, "mort_rate_mth": 0.0,
    "annuitization_rate": 0.0, "surr_charge_rate": 0.0, "mva_rate": 0.0,
    "surr_charge_age_cap": 0.0, "mva_term": 0.0, "mva_term_years": 0,
    "mva_ref_yield_locked": 0.0,
    "mva_duration_factor": 0.0, "lapse_rate_base": 0.0, "lapse_dyn_exponent": 0.0,
    "lapse_dyn_market": 0.0, "lapse_dyn_rate": 0.0, "mva_lapse_factor_at": 1.0,
    "lapse_rate": 0.0, "lapse_rate_mth": 0.0,
    "av_pp": 0.0, "prem_to_av_pp": 0.0, "prem_to_mgsv_pp": 0.0, "wd_scheduled_pp": 0.0,
    "wd_pp": 0.0, "inv_income_pp": 0.0, "interest_credited_pp": 0.0,
    "prem_accum_gmir_pp": 0.0, "free_wd_avail": 0.0, "wd_free_pp": 0.0,
    "free_wd_remain": 0.0, "wd_excess_pp": 0.0, "surr_excess_pp": 0.0,
    "surr_charge_pp": 0.0, "mva_pp": 0.0, "wd_charge_pp": 0.0, "wd_mva_pp": 0.0,
    "wd_payment_pp": 0.0, "surr_value_pp": 0.0, "surr_benefit_pp": 0.0,
    "mgsv_charge_pp": 0.0, "mgsv_wd_deduct_pp": 0.0, "mgsv_pp": 0.0,
    "taxable_wd_pp": 0.0, "tax_basis_pp": 0.0, "annuitization_pp": 0.0,
    "premiums": 0.0, "prem_to_av": 0.0, "withdrawals": 0.0,
    "commissions": 0.0, "premium_taxes": 0.0, "expenses": 0.0,
    "net_cf": 0.0, "inv_income": 0.0, "wd_from_av": 0.0, "av_change": 0.0,
    "check_av_roll_fwd_resid": 0.0, "check_pols_roll_fwd_resid": 0.0}

# The cells a month outside cover may not reach: every read keyed by a contract year, a
# guarantee period, a surrender-charge year or an attained age, the rate scenario, the two
# cells keyed by contract year and the two keyed by age, which no month outside cover
# has.  None has a guard of its own:
# the clock cells are arithmetic and would answer harmlessly, and the scenario readers are
# inputs, defined at every month of a shipped path, left unguarded so that a pre-issue read
# of a future row's re-based scenario fails loudly (T3).  No formula reaches them outside
# cover, and a caller must not either (USLIB-SEC-PLAN.md F4).
IN_COVER_ONLY = ("age", "policy_year", "duration", "gp_index", "redeclare_month",
                 "gp_start_month", "gp_end", "surr_charge_id", "surr_charge_year",
                 "scenario_rate", "market_rate", "mva_ref_yield", "free_wd_base",
                 "free_wd_allow", "surr_charge_age_cap_at", "mort_rate_at")
SCENARIO_READERS = ("scenario_rate", "market_rate", "mva_ref_yield")

# The two monthly cells defined at every month, inside cover or out: the policy clock, and
# expense inflation, an input on the valuation clock (D7).
EVERY_MONTH = ("duration_mth", "inflation_factor")

# The bools each text column S branches on is decoded into, once a point, so that no
# monthly cell compares a column's text or calls a label accessor (USLIB-SEC-PLAN.md
# §7.1, *Record — M14*), each read where S asks its question.  At stage "EC" no monthly
# cell compares text at all: S's timing and kind strings and the schedule surr_charge_id
# names are int codes (R9, R10), and Data decodes the columns into the vectors these read
# (R6).
DECODES = ("is_rollover", "is_annual_redeclare", "is_pct_av", "is_interest_only",
           "is_linear_duration", "is_geometric", "is_declared_differential", "is_cap_none",
           "is_cap_sym_sc", "is_cap_min_sc_interest", "is_cap_asym_sc_snfl",
           "is_cap_gmir_floor", "is_wd_gross", "is_wd_net_of_charges")

# The opening state, in Data's order, and the cells running in force adds to MYGA_US_S's,
# each of which the symbol map must name.
STATE = ("av_pp_init", "mgsv_pp_init", "prem_accum_gmir_pp_init",
         "interest_credited_pp_init", "interest_credited_pp_prev_anniv_init",
         "free_wd_allow_init", "free_wd_remain_init", "tax_basis_pp_init",
         "credit_rate_init", "mva_ref_yield_locked_init")
NEW_CELLS = ("policy_count", "duration_mth_init", "maturity_mth", "t_entry", "is_active",
             "pols_new_biz", "prem_to_mgsv_pp", "surr_charge_age_cap_at", "mort_rate_at",
             "mva_term_years", "point_id", "scenario_number", "wd_schedule_number",
             "mort_schedule",
             "prem_accum_gmir_pp_init", "interest_credited_pp_init",
             "interest_credited_pp_prev_anniv_init", "free_wd_allow_init",
             "free_wd_remain_init", "credit_rate_init", "mva_ref_yield_locked_init",
             *DECODES)

INFLATION = 0.025       # the shipped inflation_rate, which the inflation test reads

REPORTS = ("result_cf", "result_pols", "result_av")

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A report evaluates each column in ascending t, so a forward
# recursion, through t - 1, finds the month before already cached: the committed points'
# sweep runs under a limit of 15 and not under 14 (measured at M20).  A backward recursion
# over the frame, through t + 1, opens a chain as long as the frame, and the shortest frame
# longer than a month is 419.
CALL_DEPTH = 40

# The frames a cold call may hold on modelx's stack beyond one a month back to t_entry()
# (asserted as a bound, as Term's is).  Measured at M20: 14 on a cold last-month net_cf at
# the shipped covers and at the contract's longest, from issue age 0, and 15 on a model
# just read, whose deepest frames are Data's first reads; 16, the bound itself, on the
# account value's residual cold at the longest cover on an interest-only, GMIR-floored
# point, with or without withdrawals (DEEPEST_HEAD); 4 and 5 on the floor's and the
# basis's chains called alone.  A chain of two cells a month doubles the depth, and fails
# here, where every comparison passes.
CHAIN_OVERHEAD = 16

# The head that reaches CHAIN_OVERHEAD exactly, cold in the last month of the longest
# cover on an interest-only, GMIR-floored point (measured at M20): the depth test holds it.
DEEPEST_HEAD = "check_av_roll_fwd_resid"

# What only MYGA_US_S's docstrings may say: a reference into its Spaces, which the SEC pages
# would link to the wrong model; its clock, t counting policy months from 0, t = 0 the first
# policy month, the scenario's and the withdrawals' t a 0-based policy month, a month t a
# policy month, the issue flows at BOM of t = 0; pols_if(0) as pols_if_init(), which here
# holds for no point issued at t = 0; "then clear the cache", modelx-only advice that a
# compiled model cannot follow; and S's account of tax_basis_initial as the one model
# point column left.  Each is a phrase of MYGA_US_S's own, which the docstring test
# checks.
STALE_PHRASES = (r"~\.MYGA_US_S\.", r"``t`` counts \*\*policy months\*\* from 0",
                 r"``t = 0`` is the first policy month", r"0-based policy month",
                 r"\bpolicy month t\b", r"at BOM of t = 0", r"pols_if\(0\) == pols_if_init",
                 r"then clear the cache", r"Only ``tax_basis_initial`` stays")
STALE = re.compile("|".join(STALE_PHRASES))


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

    ``month`` is the row's ``source_mth``: 0 for a twin, ``d`` for a derived row, ``-k`` for
    a future one.  The twins keep S's ``point_id`` and ``policy_id``, so the S policy is the
    twin's.
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

    The splice's rows and the points of the temporary copies are each needed once, so each
    is released when read, as ``run_sec.py --block`` releases its points
    (USLIB-SEC-PLAN.md F5): held together they would raise this module's memory several
    times over.  Asked for again, the ItemSpace is made afresh and recomputes.
    """
    del model.Projection[key]


def _committed():
    """The committed SEC table as the file holds it, unvalidated, indexed by point_id."""
    return pd.read_csv(model_path(SEC).parent / TABLE, index_col="point_id")


def _relabeled(table):
    """``table`` relabeled ``100 + point_id`` and written in reverse order.

    Every generated table numbers its points from 1 in table order, so on it no test can
    tell a label from a position; on this one none is the other.
    """
    return table.set_axis(table.index + 100).iloc[::-1]


def _sec_inputs(tmp_path, table, edits=None):
    """A copy of the product directory whose SEC table is ``table``; its SEC folder."""
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=edits)


def _read_edited(tmp_path, edit):
    """MYGA_US_SEC read from a copy whose SEC table is ``edit(_committed())``."""
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


def _plus(column, points, amount):
    """An edit that adds ``amount`` to ``column`` at ``points`` alone."""
    def edit(table):
        moved = table[column].where(~table.index.isin(points), table[column] + amount)
        return table.assign(**{column: moved})
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


def _timing(model, label):
    """The argument that selects timing or kind ``label``: at stage "E", the string itself.

    Phase 2 turns the timing and kind strings into int References of the same names (R9:
    ``pols_if_at(t, BEF_DECR)``, ``claims(t, DEATH)``), and this passes whichever the
    model defines, so that every call in this module reads the same at both stages.
    """
    value = model.Projection.refs.get(label)
    return value if isinstance(value, int) and not isinstance(value, bool) else label


def _mismatches(s_proj, sec_proj, *, arg_map=None, **kwargs):
    """Every twin comparison of this module, through one place.

    :func:`sec_support.twin_mismatches` with the SEC Space's :func:`sec_support.codes`,
    which map S's timing and kind strings to the int codes Phase 2 gives them, and the
    spec's ``twin_arg_map``, which maps S's ``kind=None`` totals onto the code ``ALL`` and
    S's scenario columns onto their codes' names (R9, R12).  The spec's map runs first,
    then the caller's ``arg_map``, on S's arguments.  At stage ``"E"`` there were no codes;
    every comparison goes through here, so each took Phase 2's codes when they came.
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


def _sweep_s(proj):
    """Evaluate on an S point what the splice compares: the sweep, and the cells it misses.

    :func:`sec_support.sweep` reaches neither ``tax_status``, ``duration_mth``, ``gp_end``,
    ``taxable_wd_pp`` and ``tax_basis_pp``, through which ``tax_basis_pp_init``, nor
    ``claims_over_av``, ``mgsv_rate_statutory``, ``mgsv_rate_is_compliant`` and
    ``mva_ref_term_years`` on ``MYGA_US_S``, because no result column or check reads them,
    and a cell S never evaluates is compared nowhere (USLIB-SEC-PLAN.md §7.10, *never
    reached*).  They are evaluated here, the monthly ones over the
    frame and the others at arguments of their own: the statutory rate at CMT levels either
    side of its 15 bp floor, at it and at its 3% cap, the term rounded up from a fraction of
    a year, and the geometric factor above, below and at 1, which S reaches on one point
    only.  ``policy_id`` is left out: a generated row's is its own, which the clocks test
    asserts.
    """
    sweep(proj)
    proj.tax_status()
    total = (proj.refs["ALL"],) if "ALL" in proj.refs else ()   # stage "EC"'s total
    for t in range(proj.proj_len()):
        proj.duration_mth(t)
        proj.gp_end(t)
        proj.taxable_wd_pp(t)
        proj.tax_basis_pp(t)
        proj.claims_over_av(t, *total)
    for cmt5 in (0.0, 0.01, 0.014, 0.02, 0.0405, 0.08):
        proj.mgsv_rate_statutory(cmt5)
        proj.mgsv_rate_is_compliant(cmt5)
    for tau in (0.1, 985 / 365.25, 9.0):
        proj.mva_ref_term_years(tau)
    if "mva_factor_geometric" in proj.cells:     # S's alone: SEC writes it in mva_rate
        for args in ((0.08, 0.07, 985 / 365.25), (0.08, 0.09, 985 / 365.25),
                     (0.08, 0.08, 9.0)):
            proj.mva_factor_geometric(*args)


def _on_the_books(d):
    """T2's ``arg_map`` for a row opened at S month ``d``: the contract years it holds.

    ``free_wd_allow`` of a year that closed before ``d``, and ``free_wd_base`` of a year
    that opened before ``d``, are skipped: the year under way takes its allowance from
    ``free_wd_allow_init`` and needs no base, and an earlier year is no year of the row's
    frame.  Every other key passes unchanged, its ``t`` moved by the comparison itself.
    """
    def arg_map(name, args):
        if name == "free_wd_allow" and 12 * args[0] <= d:
            return None
        if name == "free_wd_base" and 12 * (args[0] - 1) < d:
            return None
        return args
    return arg_map


def _compare(s_proj, sec_proj, month, exempt, arg_map=None, columns=None):
    """Where SEC's row departs from S's point from S month ``month`` on, in two passes.

    First the frames, ``result_cf`` (over ``columns``, or every column both hold) and
    ``result_pols``, SEC row ``t`` against S row ``t + month``, frames ending together;
    then every cell of S's but ``exempt`` and :data:`RESIDUALS`, at every argument S cached
    inside its frame from ``month`` on, through ``arg_map``, moved onto SEC's clock.  Both
    to 1e-9 relative with no absolute floor: on the committed points 12,927 of the numbers
    cached outside the reports and the checks are nonzero and below 1e-7, every one a count
    or an expense, and a floor of 1e-9 would pass a 1% error in any of them.  Then the
    cells of :data:`RESIDUALS` alone, at the floor of 1e-9: their exact value is 0, and the
    computed one is rounding of what they close (§5.2, precised at M11).  Returns the
    mismatch lines, empty when the row is S's.
    """
    found = []
    for report, keep in (("result_cf", columns), ("result_pols", None)):
        found += [f"{report}: {line}" for line in frame_mismatches(
            s_proj.cells[report](), sec_proj.cells[report](), t_offset=month,
            columns=keep, atol=0.0)]
    found += _mismatches(s_proj, sec_proj, t_offset=month, exempt=exempt | RESIDUALS,
                         arg_map=arg_map, atol=0.0)
    found += _mismatches(s_proj, sec_proj, t_offset=month, arg_map=arg_map,
                         exempt=(set(s_proj.cells) - RESIDUALS) | exempt)
    return found


def _continues_s(s_proj, sec_proj, month):
    """Where a committed row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison (:func:`_compare`), on the committed model at the shipped
    assumptions: frame by frame, ``result_cf`` and ``result_pols``, then cell by cell over
    every cell of S's but :data:`SPLICE_EXEMPT`, at every key S cached from ``month`` on.
    The shipped 2.5% expense inflation runs from issue in S and from the valuation date
    here (D7), so :data:`INFLATED`'s two columns, and :data:`INFLATION_CELLS`, differ by
    design and are left out; the inflation test holds them.  The shipped scenarios are
    flat, so nothing else moves with the clock, and every other column and cell must
    agree, to 1e-9 relative with no absolute floor but on the residuals.
    """
    keep = [c for c in s_proj.result_cf().columns if c not in INFLATED]
    return _compare(s_proj, sec_proj, month, SPLICE_EXEMPT | INFLATION_CELLS,
                    _on_the_books(month), keep)


def _rebase(table, scenarios):
    """Give each derived and future row of ``table`` its own copy of its S scenario.

    The rows of the splice's table share S's three scenarios, and each reads its scenario
    at its own valuation month: a row whose SEC ``t = 0`` is S month ``s`` reads S's month
    ``t + s``.  So each gets a copy re-based to its month, as a step function
    (:func:`sec_support.shift_months`), under an id of its own, the S id with the month,
    ``base_m30`` or ``base_f15``: the row in force at S month ``s`` becomes month 0, and for
    a future row, ``s = -k``, months ``0 .. k - 1`` hold no row, so that a read before issue
    fails loudly.  The twins keep S's scenarios.  Returns ``(table, scenarios)``.
    """
    copies, ids, made = [], [], set()
    for _, row in table.iterrows():
        month, sid = int(row["source_mth"]), row["scenario_id"]
        if month == 0:
            ids.append(sid)
            continue
        copy = f"{sid}_{'m' if month > 0 else 'f'}{abs(month)}"
        if copy not in made:
            path = scenarios[scenarios["scenario_id"] == sid]
            copies.append(shift_months(path, "t", month).assign(scenario_id=copy))
            made.add(copy)
        ids.append(copy)
    return table.assign(scenario_id=ids), pd.concat([scenarios, *copies], ignore_index=True)


def _case_id(kind, s_point, month):
    """A case's id: ``point2-d12`` for a derived row, ``point2-k3`` if issued later."""
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
    """MYGA_US_SEC read in place, as committed, and swept once, cold; what it met.

    The model is first asked for ``duration_mth(400)`` on the twin of S point 1, and the
    keys that call leaves in ``duration_mth`` are kept.  Then every committed point is
    swept (:func:`sec_support.sweep`: ``result_cf``, the other reports and the checks), in
    table order and each column in ascending ``t``, under a recursion limit lowered to
    :data:`CALL_DEPTH`, and whatever that raises is kept, point by point, rather than
    raised.  Last, the opening-state columns the sweep did not read are kept, point by
    point, before any test reads one.  So the record says what a cold model does, which
    the clock test and the tests of where each column is read assert (D3, R2), and every
    test on the committed model reads a model already swept: the sweep is paid once, not
    once for each.  Returns ``(model, record)``.
    """
    model = mx.read_model(model_path(SEC), name=_name("sec"))
    first = _row(model, "twin", 1, 0)
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
    yield model, record
    model.close()


@pytest.fixture(scope="module")
def sec_model(sec_read):
    """MYGA_US_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """MYGA_US_S read in place, as committed, with every point swept (:func:`_sweep_s`).

    T6 regenerates the SEC table from it, which would otherwise project every S point again
    (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the in-force tests read S's months
    off it, the cells its own sweep misses among them.
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
    and whose scenarios, renewal schedule and declared-differential factors are the
    splice's (:data:`SPLICED_EDITS`).  SEC runs on the same tables, and on a model point
    table of its own, built by the generator from the registered spec with its rows
    replaced by the cases this run selects, the core or the full grid (:func:`_selected`),
    out of this S model, so each row opens with the state of the very run it is compared
    with; then each row's scenario is a copy re-based to its own month (:func:`_rebase`).
    Every S point is then swept (:func:`_sweep_s`), and stays swept; each SEC row is
    projected by the case that compares it and released once compared (:func:`_settle`).
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
    table, scenarios = _rebase(table, pd.read_csv(s_folder.parent / "rate_scenario.csv"))
    sec_folder = temp_inputs(root / "sec", model_path(SEC), model_points=table,
                             model_point_file=spec.model_point_file,
                             edits={**SPLICED_EDITS, "rate_scenario.csv": scenarios})
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
# core grid's reach need of the row, and releases it (_settle).  So each of the two tests
# reads the records, and computes any case no earlier test has recorded, which keeps it
# whole when run alone.


def _cached_args(cells):
    """The argument tuple of every key ``cells`` has cached (:func:`sec_support._args`)."""
    n = len(cells.parameters)
    return [() if n == 0 else (key,) if n == 1 else tuple(key)
            for key in list(cells.keys())]


def _month(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _month_reads(proj, node, memo):
    """The calls keyed by a month that ``node``, a call keyed by none, makes or has made.

    ``node`` is a call of a cell of ``proj`` with no ``t``: one keyed by a contract year or
    an age, or by nothing.  Its precedents keyed by ``t`` are its own
    reads, and through each precedent of ``proj``'s keyed by no month, that precedent's,
    down every path to the first call keyed by ``t``.  So ``free_wd_avail(t)`` reads,
    through ``free_wd_allow(y)``, the interest that cell reads, and the reads are judged
    against the month that asked.  ``memo`` holds each call's reads, once, by cells and
    arguments.
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


def _rule_breaches(proj):
    """R1, R1a and R2 on one row, once its three reports have run.

    ``{"negative": [...], "early": [...], "ahead": [...], "year": [...]}``: every cached
    call with a negative argument, a month, a contract year or an age; every read keyed by
    a month before ``t_entry()`` of a call keyed by a month at or after it; every read
    keyed by a month beyond ``t + 1`` of a call keyed by ``t``; and every key of a
    :data:`YEAR_STATE` cell at a contract year before the one under way at ``t_entry()``.
    A read is a precedent of the call's, as modelx's dependency graph records it, keyed by
    a month, or one a precedent keyed by no month makes on the call's behalf
    (:func:`_month_reads`): ``free_wd_allow(y)`` reads the interest at the anniversaries
    either side of year ``y - 1`` for the month that asks for the allowance, and a read
    there before issue or past ``t + 1`` is the asking month's.
    """
    for report in REPORTS:
        proj.cells[report]()
    entry = proj.t_entry()
    negative, early, ahead = [], [], []
    memo = {}
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
                    if u > t + 1:
                        ahead.append(f"{name}{args} -> {via}{node.obj.name}{node.args}")
    first = proj.policy_year(entry)
    year = [f"{name}({y})" for name in YEAR_STATE for y in list(proj.cells[name].keys())
            if y < first]
    return {"negative": negative, "early": early, "ahead": ahead, "year": year}


def _redeclared(x):
    """Whether the rate in force at ``t = 0`` was declared after the initial term."""
    return x.duration_mth_init() >= 12 * x.guar_period()


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, every opening-state column is in use,
# the year under way is read in each of its states, and each rate fixed in the past is read
# from the opening state, and each fixed at the valuation date from the scenario.  Later in
# the frame, every branch of the rates, the MVA, the floor, the charges, the decrements, the
# withdrawals and their tax that the full grid reaches.  One branch it does not: the
# dynamic lapse term gated off by a surrender haircut of 20% or more, which on S's points
# the Model #805 floor and the caps keep below 20% wherever the market term is live.
AT_VALUATION = {
    **{f"{c} non-zero": (lambda x, c=c: x.cells[c]() != 0.0)
       for c in STATE if c != "tax_basis_pp_init"},
    "the first contract year": lambda x: 0 < x.duration_mth_init() < 12,
    "an anniversary: the year's allowance read at t = 0": (
        lambda x: x.duration_mth_init() % 12 == 0),
    "interest_only on an anniversary": lambda x: (
        x.duration_mth_init() % 12 == 0 and x.free_wd_rule() == "interest_only"),
    "interest_only in a year's last month: the year after next from frame month 0": (
        lambda x: x.duration_mth_init() % 12 == 11 and x.free_wd_rule() == "interest_only"),
    "part of the allowance used, mid-year": lambda x: (
        x.duration_mth_init() % 12 != 0
        and x.free_wd_remain_init() < x.free_wd_allow_init()),
    "credit_rate_init read": lambda x: (
        _redeclared(x) and x.redeclare_month(0) < x.duration_mth_init()),
    "a redeclaration at t = 0": lambda x: (
        _redeclared(x) and x.redeclare_month(0) == x.duration_mth_init()),
    "mva_ref_yield_locked_init read": lambda x: (
        x.mva_in_force(0) and x.gp_index(0) >= 2
        and x.gp_start_month(0) < x.duration_mth_init()),
    "i0 re-locked at t = 0": lambda x: (
        x.renewal_architecture() == "rollover" and _redeclared(x)
        and x.gp_start_month(0) == x.duration_mth_init()),
    "an annual redeclaration at t = 0": lambda x: (
        x.renewal_architecture() == "annual_redeclare"
        and x.duration_mth_init() > 12 * x.guar_period()
        and x.duration_mth_init() % 12 == 0),
    "P_accum read in force": lambda x: (
        x.mva_cap_rule() == "gmir_floor" and x.mva_in_force(0)),
    "the interest to date read in force": lambda x: (
        x.mva_cap_rule() == "min_sc_interest" and x.mva_in_force(0)),
    "a basis below the premium": lambda x: x.tax_basis_pp_init() < x.premium_pp(),
    "a zero basis": lambda x: x.tax_basis_pp_init() == 0.0,
    "the window at t = 0": lambda x: x.in_gp_window(0),
    "the last covered month": lambda x: x.proj_len() == 1,
    "the last month of the initial term": lambda x: (
        x.duration_mth_init() == 12 * x.guar_period() - 1),
}


def _mva_binds(x, t, rule):
    """Whether ``rule`` is the point's cap and changes its MVA on a surrender in month t."""
    return (x.mva_in_force(t) and x.mva_cap_rule() == rule
            and x.mva_pp(t) != x.mva_rate(t) * x.surr_excess_pp(t))


IN_FRAME = {
    "the GMIR flooring a renewal rate": lambda x, t: (
        x.duration_mth(t) >= 12 * x.guar_period() and x.credit_rate(t) == x.gmir()),
    "a competitive rate": lambda x, t: x.lapse_dyn_market(t) < 0.0,
    "a rate inside the lapse buffer": lambda x, t: (
        x.lapse_dyn_market(t) == 0.0 and x.credit_rate(t) < x.market_rate(t)),
    "an uncompetitive rate": lambda x, t: x.lapse_dyn_market(t) > 0.0,
    **{f"the {family} MVA in force": (
        lambda x, t, family=family: x.mva_in_force(t) and x.mva_family() == family)
       for family in ("linear_duration", "geometric", "declared_differential")},
    **{f"the {rule} cap binding": (lambda x, t, rule=rule: _mva_binds(x, t, rule))
       for rule in ("sym_sc", "min_sc_interest", "asym_sc_snfl", "gmir_floor")},
    "the flat duration factor": lambda x, t: (
        x.mva_in_force(t) and x.mva_family() == "declared_differential"
        and x.mva_term(t) >= 3.0),
    "the interpolated duration factor": lambda x, t: (
        x.mva_in_force(t) and x.mva_family() == "declared_differential"
        and x.mva_term(t) < 3.0),
    "Ic at 6% or more": lambda x, t: (
        x.mva_in_force(t) and x.mva_family() == "declared_differential"
        and x.credit_rate(t) >= 0.06),
    "the floor binding on a surrender": lambda x, t: (
        x.surr_benefit_pp(t) > x.surr_value_pp(t)),
    "a schedule that runs out": lambda x, t: (
        x.surr_charge_id(t) not in ("none", getattr(x, "NONE", "none"))
        and not x.in_gp_window(t)
        and x.surr_charge_rate(t) == 0.0 and x.surr_charge_age_cap(t) > 0.0),
    "the age cap binding": lambda x, t: (
        0.0 < x.surr_charge_age_cap(t) < 1.0
        and x.surr_charge_rate(t) == x.surr_charge_age_cap(t)),
    "an annuitization in a window": lambda x, t: x.pols_annuitization(t) > 0.0,
    "the deemed maturity": lambda x, t: x.pols_maturity(t) > 0.0,
    "a utilization withdrawal": lambda x, t: (
        x.duration_mth(t) % 12 == 0 and x.wd_pp(t) > x.wd_scheduled_pp(t)),
    "an excess withdrawal": lambda x, t: x.wd_excess_pp(t) > 0.0,
    "a withdrawal free of tax": lambda x, t: (
        x.wd_pp(t) > 0.0 and x.taxable_wd_pp(t) == 0.0),
    "a withdrawal partly from basis": lambda x, t: (
        0.0 < x.taxable_wd_pp(t) < x.wd_pp(t)),
    "a withdrawal all gain": lambda x, t: (
        x.wd_pp(t) > 0.0 and x.taxable_wd_pp(t) == x.wd_pp(t)),
    "the floor's charge": lambda x, t: x.mgsv_charge_pp(t) > 0.0,
    "premium tax": lambda x, t: x.premium_taxes(t) > 0.0,
    "acquisition": lambda x, t: (
        x.expenses(t) > x.expense_maint / 12.0 * x.inflation_factor(t) * x.pols_if(t)
        + 1e-9),
}


def _branches(x, kind):
    """The names in :data:`AT_VALUATION` and :data:`IN_FRAME` that hold of row ``x``.

    :data:`AT_VALUATION` asks about the state at the valuation date, which only a row in
    force holds; :data:`IN_FRAME` about the frame, which a future row has too, and which
    alone has the premium tax and the acquisition of new business.
    """
    reached = set()
    if kind != "future":
        reached = {what for what, holds in AT_VALUATION.items() if holds(x)}
    return reached | {what for what, holds in IN_FRAME.items()
                      if any(holds(x, t) for t in range(x.t_entry(), x.proj_len()))}


def _settle(records, case, model, key):
    """Record what the rules and the core grid's reach need of a row, and release it.

    ``case`` is the row's (row_kind, S point, source_mth) and ``key`` its registry key in
    ``model``, the splice's SEC model.  A T2 or T3 case calls this once it has compared
    the row, whatever the comparison found, so the row is released either way.  The record
    is :func:`_rule_breaches`'s, with the row's :func:`_branches`, and a row that raises is
    recorded as raising, which the rules test reports.
    """
    try:
        proj = projection(model, key)
        record = _rule_breaches(proj)
        record["branches"] = _branches(proj, case[0])
        record["raised"] = None
    except Exception as err:                    # recorded, and reported by the rules test
        record = {"negative": [], "early": [], "ahead": [], "year": [],
                  "branches": set(), "raised": _raised(err)}
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
    passed as ``t`` (R1a), a look-back that stops at the wrong month, and a scenario read on
    the wrong clock: each row reads its S scenario re-based to its own month, and the
    scenarios step within every period.  The frame comparisons read SEC row ``t`` against
    S row ``t + d`` in every column of ``result_cf`` and every column of ``result_pols``
    both reports hold, and fail frames that end apart.  The cell comparison then evaluates
    every cell of S's but :data:`SPLICE_EXEMPT`, at every argument S cached inside its own
    frame from month ``d`` on, moved onto SEC's clock, to 1e-9 relative with no absolute
    floor but on the residuals (:func:`_compare`): the account value and its timings, the
    floor, ``P_accum``, the interest, the allowance and its remainder, the basis, the
    declared rate and ``i0``, the surrender traces, the counts and ``result_av`` among
    them.  The contract years before the one under way are no years of the row's frame,
    and are skipped (:func:`_on_the_books`).  An S cell this model lacked would fail it.
    The row is then recorded for the rules test and released (:func:`_settle`).
    """
    s, sec = spliced
    key = _row_key(sec, kind, s_point, month)
    s_proj, sec_proj = _point(s, s_point), projection(sec, key)
    try:
        assert _compare(s_proj, sec_proj, month, SPLICE_EXEMPT, _on_the_books(month)) == []
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

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at the deemed maturity, in
    ``result_cf`` and in every column of ``result_pols`` S's has, and every cell of S's but
    :data:`FUTURE_EXEMPT` agrees at every argument S cached inside its own frame, moved
    ``k`` later, ``result_av`` and every contract year included, to 1e-9 relative with no
    absolute floor but on the residuals (:func:`_compare`).  An S cell this model
    lacked would fail it.  Before issue every column of the three reports is an exact
    zero, and the contracts arrive in month ``k`` as new business.  The row's scenario has
    no row before issue (:func:`_rebase`), so a scenario read there raises inside the
    comparison.

    The last assertions are R1 and D4's base rule made testable.  After every report, no
    decrement rate keyed by month has been evaluated at a month before issue, the age cap
    keyed by age has not been read below the issue age, and no allowance or base keyed by
    contract year below year 1.  A recursion based at ``t == 0`` rather than at
    ``t_entry()``, or a decrement count that evaluates its rate before asking whether the
    month is in cover, still gives the right numbers.  This is the only test that sees the
    first, and the guard test sees the second too.

    The pre-issue rows are asserted present before they are asserted zero, in each of the
    three reports: a frame that opened at issue would have none, its zeros would hold of
    nothing, and the comparisons with S, which start at issue, would not see it.  The row
    is then recorded for the rules test and released (:func:`_settle`).
    """
    s, sec = spliced
    key = _row_key(sec, "future", s_point, -k)
    s_proj, sec_proj = _point(s, s_point), projection(sec, key)
    try:
        frames = {report: sec_proj.cells[report]() for report in REPORTS}
        assert _compare(s_proj, sec_proj, -k, FUTURE_EXEMPT) == []
        for report, frame in frames.items():
            assert list(frame.index[:k]) == list(range(k)), report
            assert (frame.loc[:k - 1] == 0.0).all().all(), report
        assert sec_proj.pols_new_biz(k) == sec_proj.policy_count() == 1.0
        early = {name: sorted(t for t in sec_proj.cells[name].keys() if t < k)
                 for name in DECREMENT_RATES}
        assert not any(early.values()), f"rates evaluated before issue: {early}"
        ages = sorted(sec_proj.cells["surr_charge_age_cap_at"].keys())
        assert ages and ages[0] >= sec_proj.age_at_entry(), f"ages read: {ages[:5]}"
        years = sorted(y for name in YEAR_STATE for y in sec_proj.cells[name].keys())
        assert years and years[0] >= 1, f"contract years read: {years[:5]}"
    finally:
        _settle(splice_records, ("future", s_point, -k), sec, key)


# ---------------------------------------------------------------------------
# D11's R1, R1a and R2, and D3's closed-form clock


@pytest.mark.parametrize("grid", [pytest.param("core", id="core"),
                                  pytest.param("full", id="full", marks=FULL_ONLY)])
def test_no_cell_is_called_before_the_valuation_date_or_reads_far_ahead(spliced,
                                                                        splice_records,
                                                                        grid):
    """R1, its look-back, R1a and R2's look-ahead, on the rows T2 and T3 compare.

    Each is a rule of how the model computes, not of what, so no number shows a breach,
    and on a point issued at ``t = 0`` the two clocks coincide and hide it from T1 too.
    The splice's rows are points in force at every month T2 names, the variants among them,
    and points issued later, and on each the three reports are run first:

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and
      a compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  A policy
      month turned into ``t`` by subtracting ``duration_mth_init()`` (R1a) goes negative
      on a point in force past it, as ``MYGA_US_S``'s ``free_wd_base`` and
      ``free_wd_allow`` do at an anniversary before the valuation date, and so does a
      balance read a month back without the opening state's branch.  The keys of
      ``free_wd_base``, ``free_wd_allow`` and ``surr_charge_age_cap_at``, contract years
      and ages, are held to it too.
    * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
      ``t_entry()`` on read a month before it.  On a point issued later a recursion based
      at ``t == 0`` reads the pre-issue zeros, so no number shows it and no argument goes
      negative.
    * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month beyond
      ``t + 1``, as modelx's dependency graph records each cached call's precedents.  MYGA
      needs no exception: the anniversary reads, the allowance and its base, look back to
      the anniversary, never ahead.
    * Both are judged on what a call reads through a cell keyed by no month, too: the
      allowance of a contract year and its base, keyed by the year, read the interest and
      the account value at its anniversaries for the month that asks (:func:`_month_reads`),
      and a look-back based at 0 rather than at ``t_entry()`` reads a month before issue
      there, with no number to show it.
    * The contract year under way at the valuation date is the first the model asks about:
      no ``free_wd_base`` or ``free_wd_allow`` key is a year that closed before it, whose
      state is the opening state's, not the frame's.  ``MYGA_US_S``'s forms ask for the
      year before, and read its anniversary at a policy month passed as ``t``.

    Each row was scanned by the T2 or T3 case that compared it (:func:`_settle`), and a
    row no case has scanned is scanned here.  The core case covers the core's rows, the
    full case every other row of the full grid, with ``USLIB_SEC_FULL=1``.  The
    new-business twins in the splice's table are no case's, and are left out: on them the
    clocks coincide, T1 compares the committed twins with S cell by cell on the shipped
    inputs, and T3 compares every S point and variant issued a month on with S on the
    splice's.  The closed-form clock and the recursion depth are asserted on the committed
    model, in the tests after this one.
    """
    cases = [case for case in GRID if (case in CORE_GRID) == (grid == "core")]
    negative, early, ahead, year, raised = [], [], [], [], []
    for case in cases:
        record, where = _record_of(spliced, splice_records, case), _case_id(*case)
        negative += [f"{where}: {call}" for call in record["negative"]]
        early += [f"{where}: {read}" for read in record["early"]]
        ahead += [f"{where}: {read}" for read in record["ahead"]]
        year += [f"{where}: {call}" for call in record["year"]]
        if record["raised"]:
            raised.append(f"{where}: {record['raised']}")
    assert cases, f"the {grid} grid has no rows"
    assert not raised, f"rows that raised: {raised[:10]}"
    assert not negative, f"called before the valuation date: {negative[:10]}"
    assert not early, f"read before issue from the books: {early[:10]}"
    assert not ahead, f"read beyond t + 1: {ahead[:10]}"
    assert not year, (f"asked about a contract year closed before the valuation date: "
                      f"{year[:10]}")


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


def _cold_depth(proj, cell, t):
    """The frames on modelx's stack at the deepest point of ``cell(t)``, called cold.

    The deepest stack position modelx's trace records, plus one, on an ItemSpace that has
    evaluated nothing.  modelx warns as the trace starts and as it stops.
    """
    with pytest.warns(UserWarning, match="call stack trace"):
        mx.start_stacktrace(maxlen=None)
        try:
            proj.cells[cell](t)
            trace = mx.get_stacktrace()
        finally:
            mx.stop_stacktrace()
    return 1 + max(depth for event, depth, *_ in trace if event == "ENTER")


# The cold calls the depth test makes on the committed model, each on an ItemSpace of its
# own, and the chains each walks the length of: the last month's net cash flow walks the
# count, the account value and the free-withdrawal carry on every point, P_accum on the
# GMIR-floored point and the interest credited on the interest-only point; on the point
# issued 15 months on it walks them from issue, not from t = 0.  The floor's chain and the
# basis's are called alone: the count chain reaches the floor from below, and no report
# reads the basis.
COLD_CALLS = ((("twin", 1, 0), "net_cf"), (("twin", 3, 0), "net_cf"),
              (("twin", 5, 0), "net_cf"), (("future", 1, -15), "net_cf"),
              (("twin", 2, 0), "mgsv_pp"), (("twin", 4, 0), "tax_basis_pp"))


def _extended_mortality(table):
    """The mortality table extended below age 40 by a distinct rate per age and sex.

    ``q(40) x 0.97 ** (40 - x)``: geometric in age, never flat, so that a read at the wrong
    age reads another number, and an issue age of 0, the contract's
    youngest (product-spec), projects its whole cover.
    """
    rows = []
    for sex in ("M", "F"):
        q40 = float(table.loc[(table["age"] == 40) & (table["sex"] == sex),
                              "mort_rate"].iloc[0])
        rows += [{"age": x, "sex": sex, "mort_rate": q40 * 0.97 ** (40 - x),
                  "provenance": "extended below 40 for a test"} for x in range(40)]
    return pd.concat([pd.DataFrame(rows), table], ignore_index=True)


def test_the_deepest_cold_call_runs_one_cell_a_month(tmp_path):
    """A cold call holds one frame a month back to ``t_entry()``, and a few more (F7).

    Every recursion here is one cell a month: the count, the account value, the floor,
    ``P_accum``, the interest credited, the basis and the free-withdrawal carry, where
    ``MYGA_US_S``'s account value ran three cells a month and its carry two.  A compiled
    model runs each chain on the C stack, so the depth is what sizes it, and no comparison
    sees it: a chain of two cells a month gives the same numbers.  So each cold call of
    :data:`COLD_CALLS`, on an ItemSpace of the committed model that has evaluated nothing,
    holds at least one frame for each month back to ``t_entry()``, and so walked its chain,
    and at most :data:`CHAIN_OVERHEAD` more.  The point issued 15 months on walks from its
    issue: a chain that ran on through its months before issue, as one guarded by the frame
    rather than by cover would, walks 15 months further, and fails.

    The same holds at the contract's longest cover from issue, 1,200 months at issue age 0,
    which the shipped mortality, starting at 40, cannot price: on a copy whose mortality
    is extended below 40 (:func:`_extended_mortality`), the anchor issued at 0 at the
    valuation date and 120 months after it, the horizon, each cold, and the deepest head,
    the account value's residual (:data:`DEEPEST_HEAD`), cold on the anchor made
    interest-only and GMIR-floored, which reaches the bound exactly.  That is the depth
    Phase 2's stack is sized from (USLIB-SEC-PLAN.md §7.10).
    """
    model = mx.read_model(model_path(SEC), name=_name("depth"))
    try:
        for case, cell in COLD_CALLS:
            p = _row(model, *case)
            last = p.proj_len() - 1
            months = p.proj_len() - p.t_entry()
            depth = _cold_depth(p, cell, last)
            assert months <= depth <= months + CHAIN_OVERHEAD, (case, cell, months, depth)
    finally:
        model.close()
    committed = _committed()
    twin = _label(committed, "twin", 1, 0)
    table = committed.loc[[twin, _label(committed, "future", 1, -15), twin]].assign(
        age_at_entry=0)
    table.index = pd.Index([1, 2, 3], name="point_id")
    table = _set("duration_mth", [2], -120)(table)
    table = _set("free_wd_rule", [3], "interest_only")(table)
    table = _set("mva_cap_rule", [3], "gmir_floor")(table)
    folder = _sec_inputs(tmp_path, table, edits={"mort_table.csv": _extended_mortality})
    model = mx.read_model(folder, name=_name("depth0"))
    try:
        for key, head in zip(point_keys(model), ("net_cf", "net_cf", DEEPEST_HEAD)):
            p = projection(model, key)
            months = p.proj_len() - p.t_entry()
            assert months == 1200, (key, p.proj_len(), p.t_entry())
            depth = _cold_depth(p, head, p.proj_len() - 1)
            assert months <= depth <= months + CHAIN_OVERHEAD, (key, head, months, depth)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and is not repeated here.


def test_the_count_rolls_forward_through_new_business_and_decrements(sec_model):
    """The count leaves month t by its annuitizations, deaths, surrenders, maturities alone.

    On every committed point and at every ``t`` of its frame, the count weighting month
    ``t``, ``pols_if_at(t, "BEF_DECR")``, less the count carried into ``t + 1``,
    ``pols_if_at(t + 1, "BEF_NB")``, is the four outflows of month ``t``, to 1e-12.  The
    step from the last row to ``t = proj_len()`` is what catches cover that runs a month too
    long: the maturities would then leave a month late, and the count would carry over.
    And the notes' end-of-month ``l(t)``, ``pols_if_at(t, "AFT_DECR")``, is exactly the
    count carried into the next month before its new business, in every month but the last
    covered one, where it is what the deemed maturity annuitizes out and the next month
    opens empty: the two are one product in one order.

    ``result_pols()`` sets the same movement out row by row, in :data:`RESULT_POLS`'s
    columns, indexed by ``t`` over the frame: ``pols_if`` at ``t + 1`` is ``pols_if`` less
    the outflows at ``t``, plus the new business of ``t + 1``, and row 0 opens from
    ``pols_if_init()``.  A timing the model does not have, ``basiclife.BasicTerm_SE``'s
    ``"BEF_MAT"``, which a formula ported from it might ask for, is refused rather than
    answered with another count.
    """
    bef_nb, bef_decr, aft_decr = (_timing(sec_model, label)
                                  for label in ("BEF_NB", "BEF_DECR", "AFT_DECR"))
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        last = p.proj_len() - 1
        for t in range(p.proj_len()):
            out = (p.pols_annuitization(t) + p.pols_death(t) + p.pols_lapse(t)
                   + p.pols_maturity(t))
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
    anchor = _row(sec_model, "derived", 1, 12)
    _refused(lambda: anchor.pols_if_at(0, _timing(sec_model, "BEF_MAT")), "invalid timing")


def test_result_pols_is_s_report_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's, column for column, with ``pols_new_biz`` second (D5).

    T1 skips the report as a whole, because its frame has a column S's lacks (the spec's
    exempt), so it is compared here, on every twin, the seven issued at the valuation
    date: every column S's report has agrees, to 1e-9, frames ending together, and
    ``pols_new_biz`` holds the count in the issue month and 0 in every other.  The derived
    rows' reports are compared with S's from their months on by the opening-state test.
    """
    table = sec_model.Data.model_point_table()
    twins = table.index[table["row_kind"] == "twin"].tolist()
    assert twins == sorted(s_model.Data.model_point_table().index)
    for point_id in twins:
        p = _point(sec_model, point_id)
        mine, theirs = p.result_pols(), _point(s_model, point_id).result_pols()
        assert list(mine.columns) == [theirs.columns[0], "pols_new_biz",
                                      *theirs.columns[1:]], point_id
        assert frame_mismatches(theirs, mine) == [], point_id
        assert list(mine["pols_new_biz"]) == [
            p.policy_count() if t == 0 else 0.0 for t in mine.index], point_id


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


def test_scaling_the_count_scales_every_flow_and_no_per_contract_value(tmp_path):
    """``policy_count`` is a weight: 2.5 times the count, 2.5 times every flow, the same per
    contract.

    The committed table, with the premium tax and the floor's charge switched on
    (:data:`SWITCHED_ON_COLUMNS`), and a copy with every count multiplied by
    :data:`COUNT_FACTOR`, are each read with :data:`SWITCHED_ON` set before either
    computes anything: every assumption that ships at zero is on at the value the splice
    gives it, so that every flow is nonzero on some point, the acquisition, the premium
    tax and the utilization withdrawal among them, which the shipped zeros leave 0 on every
    point (§5.2, T4, precised at M11).  On every point ``result_cf`` and ``result_pols``
    are 2.5 times the committed table's, element by element, to 1e-12 relative: a scaled
    count is a computed float, which may come back from the CSV within two ulps
    (``sec_support``'s module docstring).  So is every other cell of :data:`COUNTED`, at
    every argument the sweep of the committed table's point cached (:func:`_sweep_s`),
    the account value in force and the counts at each timing, the claims at each kind and
    the claims less the account value they release among them, which no report shows;
    but the change in the account value in force, a difference of two counted balances
    (:data:`CANCELLING`), to 1e-12 of its largest magnitude on the point, and the
    residuals, :data:`RESIDUALS`, to their floor of 1e-9 (:func:`_scaled_apart`).  Every
    column of the two reports, and every cell of :data:`COUNTED`, is nonzero on some
    point.  And every cell outside it (the account value and its timings, the floor,
    ``P_accum``, the interest, the allowance, the basis, the rates, the opening state,
    both clocks, the flags, ``result_av``) is the committed table's exactly, at every
    argument that sweep cached, and both checks close, their tolerance scaled with the
    count.  So a flow that dropped the count, or read it as whole contracts, which a table
    of counts of 1 hides from every comparison with S, fails here.  Each point is
    released once compared.
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
            for report in ("result_cf", "result_pols"):
                b, d = one.cells[report](), many.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                for column in b.columns:
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
            assert many.check_av_roll_fwd() and many.check_pols_roll_fwd(), key
            assert _mismatches(one, many, exempt=TWIN_EXEMPT_DEFAULT | COUNTED, rtol=0.0,
                               atol=0.0) == []
            _release(base, key)
            _release(scaled, scaled_key)
    finally:
        scaled.close()
        base.close()
    zero = sorted({*counted, *columns} - nonzero)
    assert not zero, f"0 on every point: {zero}"


def test_the_roll_forward_checks_close_on_a_million_contracts(tmp_path):
    """Both roll-forward checks scale their tolerance with the count, and close at 1e6.

    A residual is rounding on that many contracts, so ``check_av_roll_fwd`` holds it to
    ``check_tol_av x max(policy_count(), 1)`` and ``check_pols_roll_fwd`` likewise, where
    ``MYGA_US_S``'s tolerance is fixed: at the counts the other tests use, one or two
    contracts, the residuals are far inside either.  So the anchor's twin is projected
    from a copy where it counts a million contracts: both checks close, and each residual
    somewhere exceeds the fixed tolerance it would have had, so the scaling is what closes
    them.
    """
    committed = _committed()
    twin = _label(committed, "twin", 1, 0)
    model = _read_edited(tmp_path, _set("policy_count", [twin], 1e6))
    try:
        p = _point(model, twin)
        assert p.policy_count() == 1e6
        assert p.check_av_roll_fwd() and p.check_pols_roll_fwd()
        av = max(abs(p.check_av_roll_fwd_resid(t)) for t in range(p.proj_len()))
        pols = max(abs(p.check_pols_roll_fwd_resid(t)) for t in range(p.proj_len()))
        assert av > p.check_tol_av and pols > p.check_tol_pols, (av, pols)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault.  The checks run over the whole
# table as it is read, in Data, and the message names the file it read and the column or
# every point at fault.  A blank cell reads as NaN, and so does a text cell once the checks
# coerce the column to numbers, so each is refused as a count, a duration or a balance
# that is not a number.  The repeated point_id holds another contract under the same
# label, as a bad extract would, so that the check must look at the labels and not at
# whole rows.  The point_ids are the committed table's: 8, the anchor on its first
# anniversary; 9, the interest-only point at 30, the month after its excess withdrawal;
# 10, Camp B at 30; 11, the registered-contract point in its window at 60; 12, the stress
# trace at 61, in its first renewal period; 13, Camp B in its last covered month; 14, the
# anchor issued 15 months on; and 1 and 2, twins.  Each check over a window of contract
# months is refused in the window's first month and its last, where an off-by-one would
# let a row through (§5.2, T5, precised at M10): a row moved to months 1 and 11, the ends
# of the first contract year; to months 12 and 23, the ends of the second, where an
# interest-only allowance is the first year's interest; to month 1 and the initial
# term's last month, 60, the first renewal month, where the rate entering it is still the
# initial one; to month 1 for the account value in force, and to months 1, 11 and 13 for
# the remainder off an anniversary; and the anniversary rules at the first anniversary,
# 12.  Each is read just outside its window, the second year's at month 24 by the edges
# test and the others by test_each_rule_reads_the_months_and_cents_just_outside_it,
# which also reads 0.95 of a cent where each check of an amount against another is
# refused at 1.05 cents.  Each case
# is built so that the check it names is the first to fail.  The last checks join each
# point's keys to the tables they key, a scenario, a withdrawal programme, and a sex and
# an attained age in the mortality table, a year below its first and past its last.  A
# {file} in a message is the table's filename: every case reads its own file (the
# malformed fixture).


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

    The committed table has no point in its first contract year, so this makes one, at
    either end of it, month 1 or month 11, where an off-by-one check would let the row
    through.  The year opened at issue, so its state is set as ``Data`` requires there,
    the interest at the anniversary 0 and the allowance the issue allowance,
    ``free_wd_rate x premium`` under ``pct_av`` and 0 under ``interest_only``, and then
    ``columns`` alone are set.  Every other check still passes, so the one under test is
    the first to fail.
    """
    def edit(table):
        row = table.loc[point]
        issue = (row["free_wd_rate"] * row["premium"] if row["free_wd_rule"] == "pct_av"
                 else 0.0)
        state = {"interest_credited_pp_prev_anniv_init": 0.0, "free_wd_allow_init": issue}
        return _moved(point, month, **{**state, **columns})(table)
    return edit


def _drop(column):
    return lambda table: table.drop(columns=column)


def _off(column, point, amount, base, by=None):
    """An edit that sets ``column`` at ``point`` ``amount`` off what its rule holds it to.

    That is the row's ``base`` column, times its ``by`` column if one is named, as the
    file holds them, so the case is ``amount`` off whatever the committed amounts are.
    """
    def edit(table):
        row = table.loc[point]
        return _set(column, [point], row[base] * (row[by] if by else 1.0) + amount)(table)
    return edit


# The six balances Data holds to zero or more, each with the committed row that carries it.
BALANCES = (("av_pp_init", 9), ("interest_credited_pp_init", 9),
            ("interest_credited_pp_prev_anniv_init", 9), ("free_wd_allow_init", 9),
            ("free_wd_remain_init", 10), ("tax_basis_pp_init", 12))
FIRST_YEAR_INTEREST = (
    "{file}: interest_credited_pp_prev_anniv_init must be 0 in the first policy year, "
    "duration_mth 1 to 11, which opened at issue with no interest credited; it is not at "
    "point_id [{point}]")
FIRST_YEAR_ALLOWANCE = (
    "{file}: free_wd_allow_init must be the issue allowance in the first policy year, "
    "duration_mth 1 to 11: free_wd_rate x premium under pct_av, 0 under interest_only, to "
    "a cent; it is not at point_id [{point}]")
INITIAL_TERM = (
    "{file}: entering a month of the initial guarantee period, duration_mth 1 to 12 x "
    "guar_period, {column} must equal {issued}; it does not at point_id [{point}]")
ANNIVERSARY_ALLOWANCE = (
    "{file}: on a point valued on a policy anniversary under pct_av, duration_mth a "
    "multiple of 12, free_wd_allow_init must be free_wd_rate x av_pp_init, to a cent, the "
    "allowance the anniversary fixes on the account value entering month 0; it is not at "
    "point_id [{point}]")
INTEREST_ONLY_ALLOWANCE = (
    "{file}: under interest_only, free_wd_allow_init, the interest credited over the "
    "contract year before the one under way, must not exceed "
    "interest_credited_pp_prev_anniv_init, the interest credited to the anniversary that "
    "opened the year; it does at point_id [{point}]")
SECOND_YEAR_ALLOWANCE = (
    "{file}: under interest_only in the second policy year, duration_mth 12 to 23, "
    "free_wd_allow_init must equal interest_credited_pp_prev_anniv_init, the interest "
    "credited over the first, to a cent; it does not at point_id [{point}]")
ANNIVERSARY_INTEREST = (
    "{file}: on a point valued on a policy anniversary, duration_mth a multiple of 12, "
    "interest_credited_pp_prev_anniv_init must equal interest_credited_pp_init, to a "
    "cent; it does not at point_id [{point}]")
INTEREST_TO_DATE = (
    "{file}: interest_credited_pp_prev_anniv_init, the interest credited to the "
    "anniversary, must not exceed interest_credited_pp_init, that credited to the "
    "valuation date; it does at point_id [{point}]")
REMAINDER = (
    "{file}: off an anniversary, free_wd_remain_init must not exceed free_wd_allow_init, "
    "the allowance of the contract year under way; it does at point_id [{point}]")
ZERO_AV = (
    "{file}: av_pp_init must be more than 0 on a policy in force, duration_mth 1 or more: "
    "a contract fully withdrawn is not in force; it is not at point_id [{point}]")
SCENARIO_KEY = (
    "{file}: scenario_id must be a scenario of rate_scenario.csv that sets its levels by "
    "the first month the point is on the books, t = 0 or its issue month if later; it is "
    "not at point_id [{point}]")
WITHDRAWAL_KEY = (
    "{file}: wd_schedule_id must be a programme of withdrawal_table.csv; it is not at "
    "point_id [{point}]")
MORTALITY_KEY = (
    "{file}: mort_table.csv must give a rate at the point's sex and its attained age in "
    "the first month it is on the books; it does not at point_id [{point}]")
NO_STATE_MESSAGE = (
    "{{file}}: {column} must be 0 on a policy not yet in force, duration_mth 0 or less; it "
    "is not at point_id [{point}]")

# The nine state columns a contract not yet in force must hold at 0, tax_basis_pp_init, its
# basis at issue, apart; each is set on a twin and on the future row, at a value that
# passes every check before the one under test.
NO_STATE = tuple(c for c in STATE if c != "tax_basis_pp_init")

# Each amount Data holds to another to a cent is pinned from both sides (§5.2, T5,
# precised at M10): refused at 1.05 cents off, and read at 0.95 of a cent off
# (test_each_rule_reads_the_months_and_cents_just_outside_it), a tenth of a cent either
# side of the cent, on both signs where the rule takes the size of the difference.
PAST_CENT, INSIDE_CENT = 0.0105, 0.0095


def _no_state_value(column):
    return 0.04 if column in ("credit_rate_init", "mva_ref_yield_locked_init") else 100.0

MALFORMED = [
    ("a negative count", _set("policy_count", [8], -0.1),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [8]"),
    ("a blank count", _set("policy_count", [9], float("nan")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [9]"),
    ("two bad counts", _set("policy_count", [8, 10], -1.0),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [8, 10]"),
    ("a text count", _set("policy_count", [11], "abc"),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [11]"),
    ("an infinite count", _set("policy_count", [11], float("inf")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [11]"),
    ("a fractional duration", _set("duration_mth", [9], 30.5),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [9]"),
    ("a blank duration", _set("duration_mth", [14], float("nan")),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [14]"),
    ("a text duration", _set("duration_mth", [12], "x61"),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [12]"),
    ("a fractional issue age", _set("age_at_entry", [9], 60.5),
     "{file}: age_at_entry must be a whole number of years; it is not at point_id [9]"),
    ("a text issue age", _set("age_at_entry", [12], "x60"),
     "{file}: age_at_entry must be a whole number of years; it is not at point_id [12]"),
    ("a fractional guarantee period", _set("guar_period", [12], 5.5),
     "{file}: guar_period must be a whole number of years; it is not at point_id [12]"),
    ("a blank guarantee period", _set("guar_period", [14], float("nan")),
     "{file}: guar_period must be a whole number of years; it is not at point_id [14]"),
    ("a guarantee period of 0", _set("guar_period", [9], 0),
     "{file}: guar_period must be 1 year or more; it is not at point_id [9]"),
    ("a negative guarantee period", _set("guar_period", [1], -5),
     "{file}: guar_period must be 1 year or more; it is not at point_id [1]"),
    ("issued beyond the horizon", _set("duration_mth", [14], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [14]"),
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("policy_count", "duration_mth", *STATE)],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[9]].assign(policy_id="MYGA-900099")]),
     "{file}: point_id [9] appears more than once"),
    *[(f"a negative {column}", _set(column, [point], -1.0),
       f"{{file}}: {column} must be a number, zero or more; it is not at point_id "
       f"[{point}]")
      for column, point in BALANCES],
    ("a text av_pp_init", _set("av_pp_init", [8], "x"),
     "{file}: av_pp_init must be a number, zero or more; it is not at point_id [8]"),
    ("a blank mgsv_pp_init", _set("mgsv_pp_init", [11], float("nan")),
     "{file}: mgsv_pp_init must be a number; it is not at point_id [11]"),
    ("a text prem_accum_gmir_pp_init", _set("prem_accum_gmir_pp_init", [10], "x"),
     "{file}: prem_accum_gmir_pp_init must be a number; it is not at point_id [10]"),
    ("a text credit_rate_init", _set("credit_rate_init", [12], "4.45%"),
     "{file}: credit_rate_init must be a number; it is not at point_id [12]"),
    ("an infinite mva_ref_yield_locked_init",
     _set("mva_ref_yield_locked_init", [12], float("inf")),
     "{file}: mva_ref_yield_locked_init must be a number; it is not at point_id [12]"),
    ("an infinite av_pp_init", _set("av_pp_init", [8], float("inf")),
     "{file}: av_pp_init must be a number, zero or more; it is not at point_id [8]"),
    ("a -inf mgsv_pp_init", _set("mgsv_pp_init", [9], -float("inf")),
     "{file}: mgsv_pp_init must be a number; it is not at point_id [9]"),
    *[(f"{column} on new business", _set(column, [2], _no_state_value(column)),
       NO_STATE_MESSAGE.format(column=column, point=2))
      for column in NO_STATE],
    *[(f"{column} on future business", _set(column, [14], _no_state_value(column)),
       NO_STATE_MESSAGE.format(column=column, point=14))
      for column in NO_STATE],
    ("a zero account value in force", _set("av_pp_init", [9], 0.0),
     ZERO_AV.replace("{point}", "9")),
    ("a zero account value on an anniversary, its allowance 0 to match",
     lambda t: _set("free_wd_allow_init", [8], 0.0)(_set("av_pp_init", [8], 0.0)(t)),
     ZERO_AV.replace("{point}", "8")),
    *[(f"interest at the anniversary in the first contract year, month {month}",
       _in_first_year(8, month, interest_credited_pp_prev_anniv_init=50.0),
       FIRST_YEAR_INTEREST.replace("{point}", "8"))
      for month in (1, 11)],
    *[(f"a stale allowance in the first contract year, month {month}",
       _in_first_year(8, month, free_wd_allow_init=10445.0),
       FIRST_YEAR_ALLOWANCE.replace("{point}", "8"))
      for month in (1, 11)],
    ("an interest-only allowance in the first contract year",
     _in_first_year(9, 11, free_wd_allow_init=100.0),
     FIRST_YEAR_ALLOWANCE.replace("{point}", "9")),
    ("the interest at the anniversary apart from that entering month 0",
     _set("interest_credited_pp_prev_anniv_init", [8], 4000.0),
     ANNIVERSARY_INTEREST.replace("{point}", "8")),
    ("more interest at the anniversary than to the valuation date",
     _set("interest_credited_pp_prev_anniv_init", [9], 12000.0),
     INTEREST_TO_DATE.replace("{point}", "9")),
    ("an interest-only allowance above the interest at its anniversary",
     _moved(8, 12, free_wd_rule="interest_only", free_wd_allow_init=99999.0),
     INTEREST_ONLY_ALLOWANCE.replace("{point}", "8")),
    ("an interest-only allowance above the interest at its anniversary, mid-year",
     _set("free_wd_allow_init", [9], 50000.0),
     INTEREST_ONLY_ALLOWANCE.replace("{point}", "9")),
    *[(f"an interest-only allowance in the second year apart from the first year's "
       f"interest, month {month}",
       _moved(8, month, free_wd_rule="interest_only", free_wd_allow_init=4000.0,
              free_wd_remain_init=4000.0),
       SECOND_YEAR_ALLOWANCE.replace("{point}", "8"))
      for month in (12, 23)],
    ("a remainder above the year's allowance", _set("free_wd_remain_init", [9], 5000.0),
     REMAINDER.replace("{point}", "9")),
    ("a renewal rate in the initial term", _set("credit_rate_init", [9], 0.05),
     INITIAL_TERM.replace("{column}", "credit_rate_init").replace(
         "{issued}", "declared_rate_initial").replace("{point}", "9")),
    ("a re-locked i0 entering the first renewal month",
     _set("mva_ref_yield_locked_init", [11], 0.06),
     INITIAL_TERM.replace("{column}", "mva_ref_yield_locked_init").replace(
         "{issued}", "mva_ref_yield_at_issue").replace("{point}", "11")),
    ("a renewal rate below the GMIR", _set("credit_rate_init", [12], 0.001),
     "{file}: credit_rate_init must be gmir or more, the guaranteed minimum interest "
     "rate; it is not at point_id [12]"),
    ("a stale allowance on an anniversary", _set("free_wd_allow_init", [8], 10000.0),
     ANNIVERSARY_ALLOWANCE.replace("{point}", "8")),
    ("an allowance a dollar over on an anniversary", _plus("free_wd_allow_init", [11], 1.0),
     ANNIVERSARY_ALLOWANCE.replace("{point}", "11")),
    ("a scenario the scenario table lacks", _set("scenario_id", [1], "Base"),
     SCENARIO_KEY.replace("{point}", "1")),
    ("a blank scenario", _set("scenario_id", [12], float("nan")),
     SCENARIO_KEY.replace("{point}", "12")),
    ("a withdrawal programme the withdrawal table lacks",
     _set("wd_schedule_id", [8], "Anchor"), WITHDRAWAL_KEY.replace("{point}", "8")),
    ("a sex the mortality table lacks", _set("sex", [1], "m"),
     MORTALITY_KEY.replace("{point}", "1")),
    ("an issue age below the mortality table's first", _set("age_at_entry", [2], 39),
     MORTALITY_KEY.replace("{point}", "2")),
    ("an attained age at the valuation date past the mortality table's last",
     _set("age_at_entry", [13], 82), MORTALITY_KEY.replace("{point}", "13")),
    # The first and last months of the windows not yet met at both ends above: the
    # account value above 0 from month 1, the initial term's rate and i0 from month 1 to
    # the first renewal month, and the remainder off an anniversary in the first contract
    # year's first and last months and the month after the first anniversary.
    ("a zero account value in force in its first month",
     _in_first_year(8, 1, av_pp_init=0.0), ZERO_AV.replace("{point}", "8")),
    ("a renewal rate entering the first month of the initial term",
     _in_first_year(8, 1, credit_rate_init=0.05),
     INITIAL_TERM.replace("{column}", "credit_rate_init").replace(
         "{issued}", "declared_rate_initial").replace("{point}", "8")),
    ("a re-locked i0 entering the first month of the initial term",
     _in_first_year(8, 1, mva_ref_yield_locked_init=0.06),
     INITIAL_TERM.replace("{column}", "mva_ref_yield_locked_init").replace(
         "{issued}", "mva_ref_yield_at_issue").replace("{point}", "8")),
    ("a renewal rate entering the first renewal month",
     _set("credit_rate_init", [11], 0.05),
     INITIAL_TERM.replace("{column}", "credit_rate_init").replace(
         "{issued}", "declared_rate_initial").replace("{point}", "11")),
    *[(f"a remainder above the year's allowance in the first contract year, month {month}",
       _in_first_year(8, month, free_wd_remain_init=10001.0),
       REMAINDER.replace("{point}", "8"))
      for month in (1, 11)],
    ("a remainder above the year's allowance the month after an anniversary",
     _moved(8, 13, free_wd_remain_init=10446.0), REMAINDER.replace("{point}", "8")),
    # Each rule's cent, 1.05 cents past it (PAST_CENT), on both signs where the rule takes
    # the size of the difference: the anchor's issue allowance in its first year, its
    # interest at the anniversary and its allowance on the anniversary, and the same
    # allowance under interest_only in the second year; on the interest-only point at 30,
    # its interest at the anniversary and its allowance; and on Camp B at 30, whose
    # remainder is its allowance, the remainder.
    *[(f"an issue allowance {what} in the first contract year",
       _in_first_year(8, 6, free_wd_allow_init=10000.0 + sign * PAST_CENT),
       FIRST_YEAR_ALLOWANCE.replace("{point}", "8"))
      for what, sign in (("1.05 cents over", 1), ("1.05 cents under", -1))],
    *[(f"the interest at the anniversary {what} that entering month 0",
       _off("interest_credited_pp_prev_anniv_init", 8, sign * PAST_CENT,
            "interest_credited_pp_init"),
       ANNIVERSARY_INTEREST.replace("{point}", "8"))
      for what, sign in (("1.05 cents over", 1), ("1.05 cents under", -1))],
    *[(f"an allowance {what} free_wd_rate x av_pp_init on an anniversary",
       _off("free_wd_allow_init", 8, sign * PAST_CENT, "av_pp_init", by="free_wd_rate"),
       ANNIVERSARY_ALLOWANCE.replace("{point}", "8"))
      for what, sign in (("1.05 cents over", 1), ("1.05 cents under", -1))],
    ("an interest-only allowance in the second year 1.05 cents under the first year's "
     "interest",
     lambda t: _off("free_wd_allow_init", 8, -PAST_CENT,
                    "interest_credited_pp_prev_anniv_init")(
         _set("free_wd_rule", [8], "interest_only")(t)),
     SECOND_YEAR_ALLOWANCE.replace("{point}", "8")),
    ("the interest at the anniversary 1.05 cents over that to the valuation date",
     _off("interest_credited_pp_prev_anniv_init", 9, PAST_CENT,
          "interest_credited_pp_init"),
     INTEREST_TO_DATE.replace("{point}", "9")),
    ("an interest-only allowance 1.05 cents over the interest at its anniversary",
     _off("free_wd_allow_init", 9, PAST_CENT, "interest_credited_pp_prev_anniv_init"),
     INTEREST_ONLY_ALLOWANCE.replace("{point}", "9")),
    ("a remainder 1.05 cents over the year's allowance",
     _off("free_wd_remain_init", 10, PAST_CENT, "free_wd_allow_init"),
     REMAINDER.replace("{point}", "10")),
]


@pytest.fixture(scope="module")
def malformed(tmp_path_factory):
    """Every table of :data:`MALFORMED`, each a file of its own, beside one model folder.

    Returns ``(folder, {case: filename})``.  Each case reads the model afresh and points
    ``Data.model_point_file`` at its own file before the model computes anything
    (a Reference set after a Space has computed does not reach a compiled model), so the
    files share one copy of the product directory, and no read.
    """
    root = tmp_path_factory.mktemp("malformed")
    files = {}
    for number, (case, edit, _) in enumerate(MALFORMED):
        files[case] = f"malformed_{number:02d}_sec.csv"
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

    And a projection meets the same refusal: the first point's ``result_cf()``, which
    reads the table through its model point, raises the table's own message, so that no
    point projects from a table the model refuses, compiled or not.
    """
    folder, files = malformed
    model = mx.read_model(folder, name=_name("malformed"))
    try:
        model.Data.model_point_file = files[case]
        _refused(model.Data.model_point_table, message.format(file=files[case]))
        table = pd.read_csv(folder.parent / files[case], index_col="point_id")
        _refused(model.Projection[_file_key(model, table, table.index[0])].result_cf,
                 message.format(file=files[case]))
    finally:
        model.close()


# The six assumption tables, each with the Data Reference naming its file and the cell that
# checks it, which is the only way the projection reads the table (Data's docstring).
CHECKED = {"mort_table.csv": ("mort_table_file", "mort_rates"),
           "surr_charge_table.csv": ("surr_charge_file", "surr_charge_scales"),
           "surr_charge_age_cap.csv": ("surr_charge_age_cap_file", "surr_charge_age_caps"),
           "rate_scenario.csv": ("rate_scenario_file", "rate_scenario_steps"),
           "withdrawal_table.csv": ("withdrawal_file", "wd_schedules"),
           "mva_factor_table.csv": ("mva_factor_file", "mva_factors")}


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


# Each assumption table with one fault: (case, file, edit, message, S point).  The message
# names the faulty file by {file}, the column and the file's lines; the S point is a twin
# whose projection reads the table, the anchor for every table but the duration factors',
# which only the declared-differential point reads.  A key written as text is refused in
# every table; then a blank and a fractional key, a blank text key, a value out of its
# range or blank, a repeated key, keys that leave a gap where the projection reads every
# year or age between the first and the last, a schedule the projection names that the
# table lacks, and in every table a whole key of 2**53 or more in size, which the int64 key
# would not hold.
TABLE_FAULTS = [
    ("mortality, an age written as text", "mort_table.csv", _cell("age", 42, "61x"),
     "{file}: age must be a whole number; it is not on line [44]", 1),
    ("surrender charges, a contract year written as text", "surr_charge_table.csv",
     _cell("contract_year", 0, "1x"),
     "{file}: contract_year must be a whole number; it is not on line [2]", 1),
    ("the age cap, an age written as text", "surr_charge_age_cap.csv",
     _cell("age", 0, "94x"), "{file}: age must be a whole number; it is not on line [2]",
     1),
    ("the scenarios, a month written as text", "rate_scenario.csv", _cell("t", 1, "0x"),
     "{file}: t must be a whole number; it is not on line [3]", 1),
    ("the withdrawals, a month written as text", "withdrawal_table.csv",
     _cell("t", 0, "12x"), "{file}: t must be a whole number; it is not on line [2]", 1),
    ("the duration factors, a year written as text", "mva_factor_table.csv",
     _cell("years_remaining", 3, "3x"),
     "{file}: years_remaining must be a whole number; it is not on line [5]", 7),
    ("the withdrawals, a blank month", "withdrawal_table.csv", _cell("t", 2, None),
     "{file}: t must be a whole number; it is not on line [4]", 1),
    ("surrender charges, a fractional contract year", "surr_charge_table.csv",
     _cell("contract_year", 6, 2.5),
     "{file}: contract_year must be a whole number; it is not on line [8]", 1),
    ("surrender charges, a blank schedule", "surr_charge_table.csv",
     _cell("schedule", 5, None), "{file}: schedule must not be blank; it is on line [7]",
     1),
    ("surrender charges, 9 for 9%", "surr_charge_table.csv",
     _cell("surr_charge_rate", 0, 9.0),
     "{file}: surr_charge_rate must be a number from 0 to 1; it is not on line [2]", 1),
    ("surrender charges, a renewal schedule from year 2", "surr_charge_table.csv",
     _drop_row(5),
     "{file}: the contract years of schedule renewal must run from 1, one row a year, "
     "without a gap or a repeat", 1),
    ("surrender charges, the renewal schedule spelt Renewal", "surr_charge_table.csv",
     lambda table: table.assign(schedule=table["schedule"].replace("renewal", "Renewal")),
     "{file}: schedule renewal must be in the table, one of the two the projection reads, "
     "initial and renewal; it is not", 1),
    ("mortality, a blank rate", "mort_table.csv", _cell("mort_rate", 3, None),
     "{file}: mort_rate must be a number from 0 to 1; it is not on line [5]", 1),
    ("mortality, a male age missing", "mort_table.csv", _drop_row(60),
     "{file}: the ages of sex M must run one row an age, without a gap or a repeat", 1),
    ("the age cap, an age missing", "surr_charge_age_cap.csv", _drop_row(2),
     "{file}: the ages must run one row an age, without a gap or a repeat", 1),
    ("the duration factors, a year missing", "mva_factor_table.csv", _drop_row(4),
     "{file}: the years remaining must run from 0, one row a year, without a gap or a "
     "repeat", 7),
    ("the scenarios, two levels at one month", "rate_scenario.csv",
     _append("base", 0, 0.07, 0.05, "a second row at t = 0"),
     "{file}: a scenario must set one level a month; one sets two on lines [2, 5]", 1),
    ("the withdrawals, two at one month", "withdrawal_table.csv",
     _append("anchor", 12, 1000.0, "a second withdrawal at t = 12"),
     "{file}: a programme must withdraw once a month at most; one withdraws twice on lines "
     "[2, 5]", 1),
    ("mortality, an age of 1e20", "mort_table.csv", _cell("age", 42, 1e20),
     "{file}: age must be below 2**53 in size; it is not on line [44]", 1),
    ("surrender charges, a contract year of 1e20", "surr_charge_table.csv",
     _cell("contract_year", 0, 1e20),
     "{file}: contract_year must be below 2**53 in size; it is not on line [2]", 1),
    ("the age cap, an age of 1e20", "surr_charge_age_cap.csv", _cell("age", 0, 1e20),
     "{file}: age must be below 2**53 in size; it is not on line [2]", 1),
    ("the scenarios, a month of 1e20", "rate_scenario.csv", _cell("t", 1, 1e20),
     "{file}: t must be below 2**53 in size; it is not on line [3]", 1),
    ("the withdrawals, a month of 1e20", "withdrawal_table.csv", _cell("t", 0, 1e20),
     "{file}: t must be below 2**53 in size; it is not on line [2]", 1),
    ("the duration factors, a year of 1e20", "mva_factor_table.csv",
     _cell("years_remaining", 3, 1e20),
     "{file}: years_remaining must be below 2**53 in size; it is not on line [5]", 7),
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

    ``MYGA_US_S`` reads each assumption table's keys as pandas reads them: one key written
    as text turns its column to text, and then every surrender charge or withdrawal is
    silently zero, the age cap vanishes, or a lookup raises an error that names no file.
    Here the table's checked cell, the one way the projection reads it, refuses the table,
    and so does a projection that reads it, the twin's ``result_cf()``, with the same
    message, before it reads a value from the table.  The twin's key is taken from the file
    (:func:`_file_key`): the model point table checks each point's keys against the
    scenarios, the withdrawals and the mortality, so it reads those three tables and is
    refused with them.
    """
    folder, files = malformed_tables
    reference, checked = CHECKED[source]
    committed = _committed()
    model = mx.read_model(folder, name=_name("table"))
    try:
        setattr(model.Data, reference, files[case])
        text = message.format(file=files[case])
        _refused(model.Data.cells[checked], text)
        key = _file_key(model, committed, _label(committed, "twin", s_point, 0))
        _refused(model.Projection[key].result_cf, text)
    finally:
        model.close()


def test_a_points_scenario_must_set_its_levels_by_its_first_month_on_the_books(tmp_path):
    """A scenario may start after ``t = 0``, but not after a point that runs on it starts.

    The scenario is a step function of the valuation month, and a point reads it from the
    first month it is on the books, ``t = 0`` or its issue month if later, so the table may
    hold a scenario for business issued later that sets no level before then; the splice's
    future rows run on such scenarios.  Moved to ``t = 3``, the base scenario is refused
    for the anchor's twin and the anchor at 12, both on the books from ``t = 0``, by
    ``Data`` and by the twin's projection, where ``MYGA_US_S``'s step function finds no
    level and raises Python's own error; the anchor issued 15 months on, on the same
    scenario, is not named.  At ``t = 15`` the scenario holds for that point alone, which
    projects its frame, reading its first level in its issue month, and at ``t = 16`` it is
    refused.  Each table is read on a model of its own.
    """
    committed = _committed()
    twin, anchor = _label(committed, "twin", 1, 0), _label(committed, "derived", 1, 12)
    future = _label(committed, "future", 1, -15)

    def base_from(month):
        def edit(table):
            table = table.copy()
            table.loc[table["scenario_id"] == "base", "t"] = month
            return table
        return {"rate_scenario.csv": edit}

    late = committed.drop(index=[twin, anchor])
    for month, table, refused in ((3, committed, [twin, anchor]), (15, late, None),
                                  (16, late, [future])):
        folder = _sec_inputs(tmp_path / f"base_{month}", table, edits=base_from(month))
        model = mx.read_model(folder, name=_name("scenario"))
        try:
            if refused is None:
                assert len(model.Data.model_point_table()) == len(table)
                p = _point(model, future)
                assert p.market_rate(15) == 0.0445 and len(p.result_cf()) == 495
                assert np.isfinite(p.result_cf().to_numpy()).all()
            else:
                text = SCENARIO_KEY.replace("{file}", TABLE).replace("[{point}]",
                                                                     str(refused))
                _refused(model.Data.model_point_table, text)
                key = _file_key(model, table, refused[0])
                _refused(model.Projection[key].result_cf, text)
        finally:
            model.close()


def test_table_keys_written_as_floats_are_read_by_value(sec_model, tmp_path):
    """A key written ``1.0`` is the whole number it holds, in every table, as in S.

    On a copy whose six assumption tables carry every numeric key as a float, the age, the
    contract year, the month and the year remaining, the anchor's twin and the
    declared-differential point project exactly what the committed model projects, which
    together read all six tables.
    """
    def floats(column):
        return lambda table: table.assign(**{column: table[column].astype(float)})

    edits = {"mort_table.csv": floats("age"),
             "surr_charge_table.csv": floats("contract_year"),
             "surr_charge_age_cap.csv": floats("age"), "rate_scenario.csv": floats("t"),
             "withdrawal_table.csv": floats("t"),
             "mva_factor_table.csv": floats("years_remaining")}
    model = mx.read_model(temp_inputs(tmp_path, model_path(SEC), edits=edits),
                          name=_name("floats"))
    try:
        written = pd.read_csv(tmp_path / "surr_charge_table.csv")
        assert written["contract_year"].dtype == float
        for s_point in (1, 7):
            mine = _row(model, "twin", s_point, 0)
            base = _row(sec_model, "twin", s_point, 0)
            for report in REPORTS:
                assert frame_mismatches(base.cells[report](), mine.cells[report](), rtol=0,
                                        atol=0) == [], (s_point, report)
    finally:
        model.close()


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses a contract issued later than it; 0 refuses all.

    The committed table's one future point is issued 15 months on.  It reads at the
    shipped 120 months and at 15, the shortest horizon that admits it, and is refused at
    14, by name, and at 15 it projects its 495 months.  At 0 the model takes no future new
    business, D4's fallback for a product that cannot support it, and the message says so.
    A negative horizon is itself refused.  Each value is set on a model read afresh, before
    it computes anything.
    """
    future = _label(_committed(), "future", 1, -15)
    later = (f"{TABLE}: duration_mth must be -14 or more, a policy issued at most 14 "
             f"months after the valuation date; it is not at point_id [{future}]")
    no_future = (f"{TABLE}: duration_mth must be 0 or more: this model takes no future new "
                 f"business; it is not at point_id [{future}]")
    negative = "future_horizon_mth must be 0 months or more, not -1"
    folder = _sec_inputs(tmp_path, _committed())
    for horizon, refusal in ((None, None), (15, None), (14, later), (0, no_future),
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
            if horizon == 15:
                assert len(_point(model, future).result_cf()) == 495
        finally:
            model.close()


def test_a_point_past_its_cover_is_refused_by_proj_len(tmp_path):
    """A point whose cover has ended has no frame, and ``proj_len()`` refuses it by name.

    Camp B in its last covered month is moved on to ``duration_mth`` 480, the month its
    cover ends at attained age 100.  That is a rule of the product, not of the table: it
    needs ``maturity_age``, a Projection Reference, so the table reads, and the point is
    refused where its frame is defined, on its first projection, rather than projecting
    nothing.  480 is an anniversary, so the year-opening interest and the allowance are
    set to what ``Data`` requires there, the interest entering month 0 and ``free_wd_rate``
    times the account value, and ``Data`` has nothing to refuse.  The table is relabeled
    ``100 + point_id`` and written in reverse order, so that the label named is no
    position.  A loop over the block would meet the point only when it
    reached it, after projecting the points before it, so ``run_sec.py --block``, run
    beside the table, asks every point for its frame first: it fails naming the point, and
    prints nothing before.
    """
    committed = _committed()
    moved = 100 + _label(committed, "derived", 3, 479)

    def edit(table):
        row = table.loc[moved]
        return _moved(moved, 480,
                      interest_credited_pp_prev_anniv_init=row["interest_credited_pp_init"],
                      free_wd_allow_init=row["free_wd_rate"] * row["av_pp_init"])(table)

    folder = _sec_inputs(tmp_path, edit(_relabeled(committed)))
    model = mx.read_model(folder, name=_name("past"))
    message = f"point_id {moved}: duration_mth 480 is at or past maturity, policy month 480"
    try:
        assert len(model.Data.model_point_table()) == len(committed)
        _refused(_point(model, moved).result_cf, message)
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert message in done.stderr.decode(errors="replace")


def test_the_edges_of_the_in_force_interface_are_accepted(sec_model, s_model, tmp_path):
    """A zero count, whole numbers in any type, signed floors and the year's edges are read.

    A count of 0 is a point that projects zeros; ``30.0`` is a whole number of months, read
    back as the int the policy clock counts in, and an issue age and a guarantee period
    written as floats are read as the ints they hold; and a contract issued 120 months
    after the valuation date, the shipped ``future_horizon_mth``, is the last one the
    table admits, with a frame of 600 months, 480 of cover after 120 before issue.
    Neither the floor nor
    ``P_accum`` is floored at zero, in either model, so a point opening below zero on both
    projects, its floor and ``P_accum`` rolling on from there.  A basis of 0 on a contract
    issued at the valuation date is a qualified contract, every withdrawal all gain.  And
    on a point valued on an anniversary, a remainder above the year's allowance is last
    year's, which lapses there unread: the year opens on its own allowance, as committed.

    Amounts of money are held to their rules to a cent, so an extract may carry each to
    the cent.  Copies of committed rows, appended under ids of their own, say so: the
    anchor on its anniversary with an account value of 104,449.99 and the year's allowance
    at 10,445.00, where 10% of the one is 10,444.999 in floating point; the anchor moved to
    policy month 6 at a ``free_wd_rate`` of 7%, carrying the issue allowance as 7,000.00,
    which in floating point is 7,000.000000000001; the anchor on its anniversary under
    ``interest_only``, its allowance year 1's interest carried as 4,450.00; and the two
    ties, where half a cent left the floating-point error to decide: point 11, valued on
    its anniversary at 60, its account value and allowance carried as 124,320.35 and
    12,432.03, which are 0.005 apart, and the anchor at month 6 on a premium of 12,345.50
    at 7%, 864.185, carrying the issue allowance as 864.18.  Each is read and projects,
    from the allowance as carried.

    And S point 5, interest-only, restated on its second anniversary, month 24, with the
    state S carries into it, where the year's allowance is year 2's interest and no longer
    the first year's, below the interest at the anniversary: read, and S's projection from
    month 24 on (:func:`_continues_s`).  With month 23's refusal (the malformed table),
    it pins both ends of the second year, where the allowance must be the first year's
    interest.  The copies' ``row_kind`` says what they are, which no formula reads, so the
    rows they copy are still found as the ones they are.
    """
    committed = _committed()
    last = _label(committed, "derived", 3, 479)
    future = _label(committed, "future", 1, -15)
    camp_b = _label(committed, "derived", 3, 30)
    on_anniv = _label(committed, "derived", 1, 12)
    window = _label(committed, "derived", 4, 60)
    s5 = _point(s_model, 5)
    year3 = {**_carried(s5, 24), "duration_mth": 24, "policy_count": s5.pols_if(24)}
    month6 = {"duration_mth": 6, "free_wd_rate": 0.07,
              "interest_credited_pp_prev_anniv_init": 0.0}
    cents = {101: (on_anniv, {"av_pp_init": 104449.99, "free_wd_allow_init": 10445.0}),
             102: (on_anniv, {**month6, "free_wd_allow_init": 7000.0,
                              "free_wd_remain_init": 7000.0}),
             103: (on_anniv, {"free_wd_rule": "interest_only",
                              "free_wd_allow_init": 4450.0}),
             104: (window, {"av_pp_init": 124320.35, "free_wd_allow_init": 12432.03}),
             105: (on_anniv, {**month6, "premium": 12345.5, "free_wd_allow_init": 864.18,
                              "free_wd_remain_init": 864.18}),
             106: (_label(committed, "derived", 5, 30), year3)}

    def edit(table):
        table = _set("policy_count", [last], 0.0)(table)
        table = _set("mgsv_pp_init", [camp_b], -1000.0)(table)
        table = _set("prem_accum_gmir_pp_init", [camp_b], -2000.0)(table)
        table = _set("tax_basis_pp_init", [1], 0.0)(table)
        table = _set("free_wd_remain_init", [on_anniv], 20000.0)(table)
        rows = [table.loc[[row]].assign(**changes, row_kind="copy").set_axis([label])
                for label, (row, changes) in cents.items()]
        table = pd.concat([table, *rows]).rename_axis("point_id")
        table = table.assign(duration_mth=table["duration_mth"].astype(float),
                             age_at_entry=table["age_at_entry"].astype(float),
                             guar_period=table["guar_period"].astype(float))
        return _set("duration_mth", [future], -120.0)(table)

    model = _read_edited(tmp_path, edit)
    try:
        assert 0.1 * 104449.99 != 10445.0 and 0.07 * 100000.0 != 7000.0
        assert abs(12432.03 - 0.1 * 124320.35) > 0.005
        assert abs(864.18 - 0.07 * 12345.5) > 0.005
        for label, (_, changes) in cents.items():
            p = _point(model, label)
            assert np.isfinite(p.result_cf().to_numpy()).all(), label
            opening = (p.free_wd_remain_init() if label in (102, 105)
                       else p.free_wd_allow_init())
            assert p.free_wd_avail(0) == opening == changes["free_wd_allow_init"], label
        third = _point(model, 106)
        assert third.is_interest_only() and third.policy_year(0) == 3
        assert third.free_wd_allow_init() == pytest.approx(
            s5.interest_credited_pp(23) - s5.interest_credited_pp(11), rel=1e-12)
        gap = third.interest_credited_pp_prev_anniv_init() - third.free_wd_allow_init()
        assert gap > 4000.0 and gap == pytest.approx(s5.interest_credited_pp(11), rel=1e-9)
        assert _continues_s(s5, third, 24) == []
        read = model.Data.model_point_table()
        assert read["duration_mth"].dtype == float
        df = _row(model, "derived", 3, 479).result_cf()
        assert len(df) == 1 and (df == 0.0).all().all()
        mid = _row(model, "derived", 5, 30)
        assert mid.duration_mth(0) == 30 and type(mid.duration_mth(0)) is int
        assert type(mid.age_at_entry()) is int and type(mid.guar_period()) is int
        assert (mid.age_at_entry(), mid.guar_period()) == (
            _row(sec_model, "derived", 5, 30).age_at_entry(),
            _row(sec_model, "derived", 5, 30).guar_period())
        late = _row(model, "future", 1, -15)
        assert (late.t_entry(), late.proj_len(), late.pols_new_biz(120)) == (120, 600, 1.0)
        floor = _row(model, "derived", 3, 30)
        assert floor.mgsv_pp(0) < 0.0 and floor.prem_accum_gmir_pp(0) < 0.0
        assert floor.mgsv_pp(0) == pytest.approx(-1000.0 * (1 + floor.mgsv_rate_mth()),
                                                 rel=1e-12)
        assert np.isfinite(floor.result_cf().to_numpy()).all()
        qualified = _row(model, "twin", 1, 0)
        assert qualified.tax_basis_pp_init() == 0.0
        assert qualified.taxable_wd_pp(12) == qualified.wd_pp(12) == 4000.0
        anniv, base = _row(model, "derived", 1, 12), _row(sec_model, "derived", 1, 12)
        assert anniv.free_wd_remain_init() > anniv.free_wd_allow_init()
        assert anniv.free_wd_avail(0) == anniv.free_wd_allow_init() == base.free_wd_avail(0)
        assert frame_mismatches(base.result_cf(), anniv.result_cf(), rtol=0, atol=0) == []
    finally:
        model.close()


def test_each_rule_reads_the_months_and_cents_just_outside_it(s_model, tmp_path):
    """Each window of months or ages, and each cent, is read just outside its rule (T5).

    The malformed table refuses each rule over a window of contract months in the window's
    first month and its last, each rule over a window of ages a year past each end, and
    each amount held to another to a cent at 1.05 cents off.  Here each is read just
    outside, so that a window moved a month, or a cent a tenth of a cent, either way fails
    the one test or the other (§5.2, T5, precised at M10).  Rows appended to the committed
    table under ids of their own:

    * the anchor restated with S's state at months 1, 11 and 13: one month in force it
      holds a state, which a contract not yet in force may not; and either side of the
      first anniversary its interest at the anniversary is not the interest to date, nor
      its allowance 10% of its account value, which the anniversary rules require on the
      anniversary alone;
    * the stress trace at 61, the month after the initial term, entering it at 5%, apart
      from the initial term's 4.45%;
    * the point valued in its window at 60, the initial term's last month, entering it at
      the initial 4.45% under a GMIR raised to 5%, which binds only from 61;
    * the anchor's twin issued at 40, the mortality table's first age, and Camp B in its
      last covered month issued at 81, at attained age 120, the table's last, read with
      ``maturity_age`` raised to 121, so that the contract is in cover there;
    * 0.95 of a cent off (:data:`INSIDE_CENT`) on both signs: the anchor's issue allowance
      at month 6, its interest at the anniversary and its allowance at 12, and the same
      allowance under ``interest_only`` in the second year; and over, the one sign each
      rule bounds: the interest-only point's interest at the anniversary over that to the
      valuation date, and its allowance over that interest, and Camp B's remainder at 30
      over its allowance.

    ``Data`` reads the table, and no row's ``proj_len()`` refuses it.  The committed rows
    and the edges test read the other sides: month 0 for the account value above 0 and
    the first year's and the initial term's rules, where a contract not in force holds no
    state; 12 for the first year's rules and the remainder's; 24 for the second year's;
    the last covered month, 479, for ``proj_len()``; and 120 months on for the horizon.
    """
    committed = _committed()
    s1 = _point(s_model, 1)
    on_anniv, interest_only, camp_b, window, renewal, last = (
        _label(committed, "derived", s_point, month) for s_point, month
        in ((1, 12), (5, 30), (3, 30), (4, 60), (2, 61), (3, 479)))
    row, io = committed.loc[on_anniv], committed.loc[interest_only]
    issue, base = (row["free_wd_rate"] * row[c] for c in ("premium", "av_pp_init"))
    first_year = {"duration_mth": 6, "interest_credited_pp_prev_anniv_init": 0.0}
    copies = {
        **{101 + i: (on_anniv, {**_carried(s1, d), "duration_mth": d,
                                "policy_count": s1.pols_if(d)})
           for i, d in enumerate((1, 11, 13))},
        104: (renewal, {"credit_rate_init": 0.05}),
        105: (window, {"gmir": 0.05}),
        106: (_label(committed, "twin", 1, 0), {"age_at_entry": 40}),
        107: (last, {"age_at_entry": 81}),
        108: (interest_only, {"interest_credited_pp_prev_anniv_init":
                              io["interest_credited_pp_init"] + INSIDE_CENT}),
        109: (interest_only, {"free_wd_allow_init":
                              io["interest_credited_pp_prev_anniv_init"] + INSIDE_CENT}),
        110: (camp_b, {"free_wd_remain_init": committed.at[camp_b, "free_wd_allow_init"]
                      + INSIDE_CENT}),
    }
    for i, sign in enumerate((1, -1)):
        off = sign * INSIDE_CENT
        copies.update({
            111 + i: (on_anniv, {**first_year, "free_wd_allow_init": issue + off}),
            113 + i: (on_anniv, {"interest_credited_pp_prev_anniv_init":
                                 row["interest_credited_pp_init"] + off}),
            115 + i: (on_anniv, {"free_wd_allow_init": base + off}),
            117 + i: (on_anniv, {"free_wd_rule": "interest_only", "free_wd_allow_init":
                                 row["interest_credited_pp_prev_anniv_init"] + off})})
    rows = [committed.loc[[point]].assign(**changes, row_kind="copy").set_axis([label])
            for label, (point, changes) in copies.items()]
    table = pd.concat([committed, *rows]).rename_axis("point_id")
    model = mx.read_model(_sec_inputs(tmp_path, table), name=_name("outside"))
    try:
        model.Projection.maturity_age = 121
        assert len(model.Data.model_point_table()) == len(table)
        assert _point(model, 107).age(0) == 120 and _point(model, 106).age(0) == 40
        refused = []
        for label in copies:
            try:
                _point(model, label).proj_len()
            except Exception as err:            # reported, so every row is asked
                refused.append(f"{label}: {_raised(err)}")
        assert not refused, refused
    finally:
        model.close()


def _every_state_months(n):
    """The months of a frame of ``n`` the every-state test restates an S point at, from 1.

    By default the edges of the windows ``Data``'s rules turn on (USLIB-SEC-PLAN.md §5.2,
    T5): every month of the first contract year, and each anniversary with the months
    either side of it, where the first and second years, the initial term and each
    renewal, the anniversary rules and the remainder's open and close, and the last
    covered month.  With ``USLIB_SEC_FULL=1``, every month of the frame.
    """
    if SEC_FULL:
        return list(range(1, n))
    return sorted({*range(1, min(12, n)), n - 1,
                   *(d for d in range(12, n) if d % 12 in (0, 1, 11))})


def _refused_in_force(s, states, root, refs, edits):
    """What ``Data`` and ``proj_len()`` refuse of ``states`` of ``s``, restated in force.

    ``states`` are ``(S point, month)`` pairs of ``s``, an S model.  The generator builds
    from ``s`` one table of every S point's twin and a derived row at each state; a model
    read on ``edits``, with ``refs`` set first, reads it through ``Data`` and then asks
    every row for its frame, releasing each.  Returns each refusal, the line naming it:
    ``Data``'s, or each row's ``proj_len()``'s.
    """
    spec = dataclasses.replace(SPEC, derived=tuple(states), future=())
    table, _ = build_sec_table(spec, s)
    model = mx.read_model(temp_inputs(root, model_path(SEC), model_points=table,
                                      model_point_file=TABLE, edits=edits),
                          name=_name("every"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        try:
            read = model.Data.model_point_table()
        except Exception as err:                # reported, with the rows' states
            return [f"Data: {_raised(err)}"]
        assert len(read) == len(table)
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
    """Every state ``MYGA_US_S`` reaches is a valid opening state, on each set of inputs.

    ``Data``'s rules and ``proj_len()``'s hold an opening state to what a contract in force
    can be, so they must accept each state the S model reaches: a rule exercised only on
    the rows the other tests choose could refuse a state S reaches elsewhere (D6).  So
    every S point is restated in force by the generator at the edges of the windows those
    rules turn on, or with ``USLIB_SEC_FULL=1`` at every month of its frame
    (:func:`_every_state_months`), into one table beside the twins: ``Data`` reads it,
    and no row's ``proj_len()`` refuses it (:func:`_refused_in_force`).  It runs on each
    set of inputs the module runs S on, the states S reaches differing on each (§5.2, T5,
    precised at M9): S's shipped References and inputs, on S's seven points, about 900
    states; the splice's (:data:`SPLICED_REFS`, :data:`SPLICED_EDITS`), on those and the
    four variants, about 1,300, where the utilization withdrawal, the renewal spread, the
    premium load and the stepped scenarios move every balance and rate; and the scenario
    test's, the base scenario stepped at month 6 (:func:`_base_stepped`), on the one S
    point it moves, the anchor, which renews at 3.50% on an ``i0`` of 5.50%, about 130.

    The one state the product refuses by name, a contract fully withdrawn, which ``Data``
    refuses in force as holding nothing, would be set aside first and shown refused; but
    ``MYGA_US_S`` reaches none on any of the three, every withdrawal leaving an account
    value above 0, so none is set aside, which the test asserts, and the malformed table
    shows it refused, at month 1 and mid-year.
    """
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    step, base = {"rate_scenario.csv": _base_stepped}, s_table["scenario_id"] == "base"
    stepped = mx.read_model(temp_inputs(tmp_path / "s_stepped", model_path(TWIN),
                                        model_points=s_table[base], edits=step),
                            name=_name("s_stepped"))
    try:
        for label, s, refs, edits in (
                ("shipped", s_model, {}, None),
                ("spliced", spliced[0], SPLICED_REFS, SPLICED_EDITS),
                ("stepped", stepped, {}, step)):
            kept, withdrawn = [], []
            for key, point_id in zip(point_keys(s), s.Data.model_point_table().index):
                p = projection(s, key)
                for d in _every_state_months(p.proj_len()):
                    (kept if p.av_pp(d - 1) > 0.0 else withdrawn).append((point_id, d))
            assert not withdrawn, (label, withdrawn[:5])
            assert len(kept) >= 100 * len(s.Data.model_point_table()), (label, len(kept))
            refused = _refused_in_force(s, kept, tmp_path / label, refs, edits)
            assert not refused, f"{label}: {len(refused)} refused, first: {refused[:5]}"
    finally:
        stepped.close()


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_table_is_what_s_generates(s_model):
    """``model_point_table_sec.csv`` is what MYGA_US_S and its table generate today.

    Every row and column, the text cells and the ten opening-state columns included: an
    edit to an S row the table copies or derives from, or to an S formula a row's state is
    read from, fails here until ``python tools/gen_sec_points.py MYGA_US_SEC``
    regenerates it, in the same commit.  Text and integers compare exactly, and a float by
    its value, to 1e-12, because the text the writer picks for a computed float depends on
    the platform's parser (§5.2).
    """
    assert check_generated(SEC, s_model=s_model) == []


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_two_clocks_on_the_shipped_points(sec_model):
    """``t`` counts from the valuation date; ``duration_mth(t)`` from issue (D3, D4).

    On a twin the two coincide, and its contracts enter as new business at ``t = 0``.  The
    anchor in force 12 months is in contract year 2 at attained age 61 at ``t = 0``, in
    the second year of its initial term and of its surrender-charge schedule, and has 468
    months of cover left, to its deemed maturity at policy month 480.  The point valued in
    its window is in its second guarantee period, whose rate was declared at policy month
    60, the valuation month: no surrender charge applies, and 1% annuitize.  Camp B in its
    last covered month has a one-month frame, in which its survivors mature.  The anchor
    issued 15 months on has nothing in force and nothing to do before ``t = 15``, and
    contract year -1, then 0, before issue, which no schedule is read at.
    """
    twin = _row(sec_model, "twin", 1, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 479)] == [0, 1, 479]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0), twin.pols_if(0)) == (
        0, 0.0, 1.0, 1.0)
    assert twin.policy_id() == "MYGA-000001"
    anchor = _row(sec_model, "derived", 1, 12)
    assert (anchor.duration_mth(0), anchor.policy_year(0), anchor.age(0),
            anchor.gp_index(0), anchor.surr_charge_year(0)) == (12, 2, 61, 1, 2)
    assert (anchor.maturity_mth(), anchor.proj_len(), anchor.policy_id()) == (
        480, 468, "MYGA-000001-M12")
    assert anchor.is_active(467) and not anchor.is_active(468)
    window = _row(sec_model, "derived", 4, 60)
    assert window.in_gp_window(0) and (window.gp_index(0), window.redeclare_month(0)) == (
        2, 60)
    assert (window.surr_charge_rate(0), window.annuitization_rate(0)) == (0.0, 0.01)
    assert not window.in_gp_window(1) and window.surr_charge_rate(1) > 0.0
    last = _row(sec_model, "derived", 3, 479)
    assert (last.proj_len(), last.age(0), last.policy_year(0)) == (1, 99, 40)
    assert last.pols_maturity(0) > 0.0
    assert last.pols_if_at(1, _timing(sec_model, "BEF_NB")) == 0.0
    fut = _row(sec_model, "future", 1, -15)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-15, 15, 495)
    assert [fut.policy_year(t) for t in range(16)] == [-1] * 3 + [0] * 12 + [1]
    assert not fut.is_active(14) and fut.is_active(15)
    assert (fut.pols_if_init(), fut.pols_new_biz(15), fut.pols_if(15)) == (0.0, 1.0, 1.0)
    assert (fut.premiums(14), fut.premiums(15)) == (0.0, 100000.0)


def _carried(s, d):
    """What ``MYGA_US_S`` point ``s`` carries into its month ``d``, column by column.

    Each as S's own formulas read it, the D6 instants spelled out: a balance or a rate
    entering month ``d`` is its value in month ``d - 1``; the interest at the anniversary
    that opened the contract year of ``d`` is the close of the month before that
    anniversary, nothing in the first year; and the year's allowance is S's for that year.
    """
    anniv = 12 * (d // 12)
    return {
        "av_pp_init": s.av_pp(d - 1),
        "mgsv_pp_init": s.mgsv_pp(d - 1),
        "prem_accum_gmir_pp_init": s.prem_accum_gmir_pp(d - 1),
        "interest_credited_pp_init": s.interest_credited_pp(d - 1),
        "interest_credited_pp_prev_anniv_init": (
            s.interest_credited_pp(anniv - 1) if anniv > 0 else 0.0),
        "free_wd_allow_init": s.free_wd_allow(d // 12 + 1),
        "free_wd_remain_init": s.free_wd_remain(d - 1),
        "tax_basis_pp_init": s.tax_basis_pp(d - 1),
        "credit_rate_init": s.credit_rate(d - 1),
        "mva_ref_yield_locked_init": s.mva_ref_yield_locked(d - 1),
    }


def test_the_opening_state_is_what_s_carries_into_the_valuation_month(sec_model, s_model):
    """Each committed in-force row opens with S's state at its month, and continues S.

    For each derived row, restated from S point ``p`` at its month ``d``, each of the ten
    opening-state columns is what S carries into month ``d`` (:func:`_carried`), to 1e-12
    relative, because a computed float may come back from the CSV within two ulps.  Then
    the row is S's point from month ``d`` on, at the shipped assumptions, in every cell but
    those expense inflation moves (:func:`_continues_s`): the committed rows themselves are
    splices, on the shipped inputs, as T2's rows are on the splice's.
    """
    table = sec_model.Data.model_point_table()
    derived = table[table["row_kind"] == "derived"]
    assert len(derived) == 6
    s_table = s_model.Data.model_point_table()
    s_of = {policy: point_id for point_id, policy in s_table["policy_id"].items()}
    for point_id, row in derived.iterrows():
        s, d = _point(s_model, s_of[row["source_policy_id"]]), int(row["source_mth"])
        p = _point(sec_model, point_id)
        assert p.duration_mth_init() == d, point_id
        for column, value in _carried(s, d).items():
            assert p.cells[column]() == pytest.approx(value, rel=1e-12, abs=1e-12), (
                point_id, column)
        assert _continues_s(s, p, d) == [], point_id


def test_each_opening_state_column_shows_on_a_committed_row(sec_model, tmp_path):
    """Each column, changed alone, changes what its committed row gives in its first months.

    A column the projection never read, or read where another belongs, would pass every
    test that leaves the column as generated.  So each is changed on a copy of a committed
    row that reads it, appended to the committed table under an id of its own, and the
    copy's first months are asserted against the row's, to the cent:

    * the account value, on the interest-only point at 30: halved, to 45,713.17, the
      contract credits a month's interest on that, 45,879.33 at the end of month 0, and
      still projects its whole frame;
    * the floor, on the same point: zeroed, the contract has no floor at the end of
      month 0;
    * ``P_accum`` on Camp B at 30: zeroed, the GMIR-floored cap no longer holds ``AV + M``
      above the premium accumulated at the GMIR, and the MVA on a surrender falls to its
      raw value;
    * the interest credited to date, with that at the anniversary, on the interest-only
      point: zeroed, with year 3's allowance, which cannot exceed the interest to its
      anniversary, the interest-credited cap limits the MVA on a surrender at ``t = 0`` to
      the month's interest, where the surrender charge limits it on the row;
    * the interest at the anniversary alone, with year 3's allowance as before: zeroed,
      year 4's interest-only allowance, at ``t = 6``, is the whole interest since issue
      rather than year 3's;
    * the year's allowance, on the anchor valued on its anniversary: ``Data`` holds it to
      10% of the account value to a cent, and moved by 0.4 of a cent within that, the
      allowance at ``t = 0`` is the column's, not the product, and so is what the $4,000
      leaves of it;
    * the remainder, on the interest-only point, whose allowance its excess withdrawal used
      up: restored to the year's allowance, it shelters part of a surrender at ``t = 0``;
    * the basis, on the anchor at 12: set to the account value, the $4,000 is no gain;
    * the declared rate, on the stress trace at 61 and on Camp B at 479, declared before
      the valuation date: set to the GMIR, each credits the GMIR at ``t = 0``;
    * ``i0``, on the stress trace at 61: locked at 8% rather than 10%, a surrender at
      ``t = 0`` takes a negative MVA, capped at the charge, where the row's is 0.
    """
    committed = _committed()
    p8, p9, p10, p12, p13 = (_label(committed, "derived", s_point, month) for s_point, month
                             in ((1, 12), (5, 30), (3, 30), (2, 61), (3, 479)))
    copies = {
        "av": (p9, {"av_pp_init": committed.at[p9, "av_pp_init"] / 2}),
        "floor": (p9, {"mgsv_pp_init": 0.0}),
        "p_accum": (p10, {"prem_accum_gmir_pp_init": 0.0}),
        "interest": (p9, {"interest_credited_pp_init": 0.0,
                          "interest_credited_pp_prev_anniv_init": 0.0,
                          "free_wd_allow_init": 0.0}),
        "interest_anniv": (p9, {"interest_credited_pp_prev_anniv_init": 0.0,
                                "free_wd_allow_init": 0.0}),
        "allowance": (p8, {"free_wd_allow_init": committed.at[p8, "free_wd_allow_init"]
                           + 0.004}),
        "remainder": (p9, {"free_wd_remain_init": committed.at[p9, "free_wd_allow_init"]}),
        "basis": (p8, {"tax_basis_pp_init": committed.at[p8, "av_pp_init"]}),
        "rate": (p12, {"credit_rate_init": committed.at[p12, "gmir"]}),
        "rate_camp_b": (p13, {"credit_rate_init": committed.at[p13, "gmir"]}),
        "i0": (p12, {"mva_ref_yield_locked_init": 0.08}),
    }
    labels = {what: 100 + i for i, what in enumerate(copies, start=1)}
    rows = [committed.loc[[point]].assign(**changes).set_axis([labels[what]])
            for what, (point, changes) in copies.items()]
    table = pd.concat([committed, *rows]).rename_axis("point_id")
    model = mx.read_model(_sec_inputs(tmp_path, table), name=_name("shown"))
    try:
        c = {what: _point(model, label) for what, label in labels.items()}
        r8, r9, r10, r12, r13 = (_point(sec_model, p) for p in (p8, p9, p10, p12, p13))
        cent = 0.005
        assert r9.av_pp(0) == pytest.approx(91758.65, abs=cent)
        half = c["av"]
        assert half.av_pp(0) == half.av_pp_init() * (1.0 + half.credit_rate_mth(0))
        assert half.av_pp(0) == pytest.approx(45879.33, abs=cent)
        assert np.isfinite(half.result_cf().to_numpy()).all()
        assert r9.mgsv_pp(0) == pytest.approx(76037.15, abs=cent)
        assert c["floor"].mgsv_pp(0) == 0.0
        assert r10.mva_pp(0) == pytest.approx(-11257.20, abs=cent)
        assert c["p_accum"].mva_pp(0) == pytest.approx(-12203.50, abs=cent)
        assert c["p_accum"].mva_pp(0) == c["p_accum"].mva_rate(0) * c[
            "p_accum"].surr_excess_pp(0)
        assert r9.mva_pp(0) == -r9.surr_charge_pp(0) == pytest.approx(-6423.11, abs=cent)
        assert c["interest"].mva_pp(0) == -c["interest"].interest_credited_pp(0)
        assert c["interest"].mva_pp(0) == pytest.approx(-332.31, abs=cent)
        assert r9.free_wd_avail(6) == pytest.approx(4340.41, abs=cent)
        anniv = c["interest_anniv"]
        assert anniv.free_wd_avail(6) == anniv.interest_credited_pp(5)
        assert anniv.free_wd_avail(6) == pytest.approx(13438.44, abs=cent)
        assert r8.wd_payment_pp(0) == r8.wd_free_pp(0) == 4000.0
        allow = c["allowance"]
        assert allow.free_wd_avail(0) == allow.free_wd_allow_init() != r8.free_wd_avail(0)
        assert allow.free_wd_avail(0) == pytest.approx(10445.004, abs=1e-9)
        assert allow.free_wd_remain(0) == allow.free_wd_avail(0) - 4000.0
        assert r9.free_wd_remain_init() == 0.0
        assert r9.surr_charge_pp(0) == pytest.approx(6423.11, abs=cent)
        assert c["remainder"].surr_charge_pp(0) == pytest.approx(6097.74, abs=cent)
        assert r8.taxable_wd_pp(0) == 4000.0 and c["basis"].taxable_wd_pp(0) == 0.0
        assert r12.credit_rate(0) == r13.credit_rate(0) == 0.0445
        assert c["rate"].credit_rate(0) == c["rate_camp_b"].credit_rate(0) == 0.0025
        assert (r12.mva_ref_yield_locked(0), r12.mva_pp(0)) == (0.10, 0.0)
        assert c["i0"].mva_ref_yield_locked(0) == 0.08
        assert c["i0"].mva_pp(0) == -c["i0"].surr_charge_pp(0)
        assert c["i0"].mva_pp(0) == pytest.approx(-5639.69, abs=cent)
    finally:
        model.close()


def test_the_declared_rate_and_i0_on_a_renewal_valuation(sec_model, sec_read):
    """A rate fixed in the past is the opening state's; one fixed at t = 0, the scenario's.

    The point valued in its window, at policy month 60, redeclares its rate and re-locks
    ``i0`` at the valuation month itself, so both come from the scenario at ``t = 0``:
    ``max(GMIR, MR(0) - s_ren)`` and the reference yield, 10% on the stress path, where the
    two columns hold the rate and ``i0`` entering month 0, the initial term's 4.45% and 5%,
    which the cold sweep read nowhere.  The stress trace valued at 61 is a month into its
    period: the rate declared at 60 and ``i0`` locked there are facts of the past, and both
    come from the columns, which the sweep read.  Camp B valued in its last covered month,
    479, redeclared at 468, before the valuation date, so its rate is the column's too; its
    MVA ran out with its initial term, and its ``i0`` column is read nowhere.
    """
    unread = sec_read[1]["unread"]
    window = _row(sec_model, "derived", 4, 60)
    label = _label(sec_model.Data.model_point_table(), "derived", 4, 60)
    assert window.credit_rate(0) == max(window.gmir(),
                                        window.market_rate(0) - window.renewal_spread)
    assert window.mva_ref_yield_locked(0) == window.mva_ref_yield(0) == 0.10
    assert (window.credit_rate_init(), window.mva_ref_yield_locked_init()) == (0.0445, 0.05)
    assert {"credit_rate_init", "mva_ref_yield_locked_init"} <= unread[label]
    renewal = _row(sec_model, "derived", 2, 61)
    label = _label(sec_model.Data.model_point_table(), "derived", 2, 61)
    assert (renewal.redeclare_month(0), renewal.gp_start_month(0)) == (60, 60)
    assert renewal.credit_rate(0) == renewal.credit_rate_init() == 0.0445
    assert renewal.mva_ref_yield_locked(0) == renewal.mva_ref_yield_locked_init() == 0.10
    assert not {"credit_rate_init", "mva_ref_yield_locked_init"} & unread[label]
    camp_b = _row(sec_model, "derived", 3, 479)
    label = _label(sec_model.Data.model_point_table(), "derived", 3, 479)
    assert (camp_b.redeclare_month(0), camp_b.duration_mth_init()) == (468, 479)
    assert camp_b.credit_rate(0) == camp_b.credit_rate_init() == 0.0445
    assert not camp_b.mva_in_force(0)
    assert "credit_rate_init" not in unread[label]
    assert "mva_ref_yield_locked_init" in unread[label]


def test_the_year_under_way_reads_its_free_withdrawal_state(sec_model, sec_read):
    """The allowance of the year under way, and what is left of it, are opening state.

    Valued on its first anniversary, the anchor opens contract year 2 at ``t = 0``: the
    year's allowance is the column's, 10% of the account value at the anniversary,
    10,445.00, so the $4,000 there is free, and 6,445.00 of the allowance is left for a
    surrender at the end of month 0.  Last year's remainder lapses there, and the cold
    sweep did not read it.  The interest-only point valued at 30, mid-year, the month after
    its $20,000 excess withdrawal used up year 3's allowance, opens from the remainder, 0,
    through month 5; at ``t = 6`` year 4 opens, and its allowance is the interest credited
    over year 3, from the anniversary at policy month 24,
    ``interest_credited_pp_prev_anniv_init``, to the end of ``t = 5``.  Off an anniversary
    the sweep read the year's allowance column nowhere: the year's remainder carries the
    year.
    """
    unread = sec_read[1]["unread"]
    table = sec_model.Data.model_point_table()
    anchor = _row(sec_model, "derived", 1, 12)
    assert anchor.free_wd_avail(0) == anchor.free_wd_allow_init()
    assert anchor.free_wd_allow_init() == pytest.approx(10445.0, abs=0.005)
    assert anchor.free_wd_allow_init() == pytest.approx(0.1 * anchor.av_pp_init(),
                                                        rel=1e-12)
    assert anchor.wd_pp(0) == anchor.wd_free_pp(0) == 4000.0
    assert anchor.free_wd_remain(0) == pytest.approx(6445.0, abs=0.005)
    assert "free_wd_remain_init" in unread[_label(table, "derived", 1, 12)]
    mid = _row(sec_model, "derived", 5, 30)
    assert mid.free_wd_avail(0) == mid.free_wd_remain_init() == 0.0
    assert [mid.free_wd_avail(t) for t in range(6)] == [0.0] * 6
    assert mid.free_wd_avail(6) == (mid.interest_credited_pp(5)
                                    - mid.interest_credited_pp_prev_anniv_init())
    assert mid.free_wd_avail(6) == pytest.approx(4340.41, abs=0.005)
    for s_point, month in ((5, 30), (3, 30), (2, 61), (3, 479)):
        assert "free_wd_allow_init" in unread[_label(table, "derived", s_point, month)], (
            s_point, month)


def _base_stepped(table):
    """The scenarios with the base one stepped at ``t = 6`` to MR 3.50% and a 5.50% yield.

    The scenario test's input, and one the every-state test restates S's states on.
    """
    row = table[table["scenario_id"] == "base"].assign(
        t=6, mva_ref_yield=0.0550, market_rate=0.0350)
    return pd.concat([table, row], ignore_index=True)


def test_the_rate_scenario_runs_on_the_valuation_clock(tmp_path):
    """The rate scenario is a path in calendar time, read at ``t`` on every point (D7).

    The three shipped scenarios are each one row at ``t = 0``, the premise under which the
    committed in-force rows continue S without a re-based scenario.  On a copy whose base
    scenario steps at ``t = 6``, the anchor's twin and the anchor in force 12 months both
    see the new market rate and yield from ``t = 6``, their policy months 6 and 18, and the
    anchor issued 15 months on from ``t = 6`` too, before its issue.  The anchor in force,
    still crediting its initial 4.45%, is competitive against the lower market from there,
    and its dynamic lapse moves at ``t = 6``, not before.  S's anchor, on its policy clock,
    sees the step at its month 6, so at its month 12, where the in-force anchor's frame
    opens, it reads the new rate; on the valuation clock that month is ``t = 0``, before
    the step.  Each model is read afresh.
    """
    shipped = pd.read_csv(model_path(SEC).parent / "rate_scenario.csv")
    assert sorted(shipped["scenario_id"]) == ["base", "differential", "stress"]
    assert (shipped["t"] == 0).all()
    edits = {"rate_scenario.csv": _base_stepped}
    sec_folder = temp_inputs(tmp_path, model_path(SEC), edits=edits)
    s_folder = temp_inputs(tmp_path, model_path(TWIN), edits=edits)
    sec = mx.read_model(sec_folder, name=_name("scenario"))
    s = mx.read_model(s_folder, name=_name("scenario_s"))
    try:
        for case in (("twin", 1, 0), ("derived", 1, 12), ("future", 1, -15)):
            p = _row(sec, *case)
            assert [p.market_rate(t) for t in (0, 5, 6, 7)] == [0.0445] * 2 + [0.0350] * 2
            assert [p.mva_ref_yield(t) for t in (5, 6)] == [0.0650, 0.0550], case
        anchor = _row(sec, "derived", 1, 12)
        assert [anchor.lapse_dyn_market(t) for t in range(6)] == [0.0] * 6
        assert anchor.lapse_dyn_market(6) < 0.0
        s1 = _point(s, 1)
        assert [s1.market_rate(t) for t in (5, 6, 12)] == [0.0445, 0.0350, 0.0350]
        assert anchor.market_rate(0) == 0.0445 != s1.market_rate(12)
    finally:
        s.close()
        sec.close()


def test_withdrawals_stay_on_the_policy_clock(sec_model):
    """A withdrawal programme falls where the contract has it, however old the contract.

    *withdrawal_table.csv*'s month is a policy month (D7): the anchor's $4,000 at policy
    month 12 falls at ``t = 12`` on its twin, at ``t = 0`` on the anchor valued on its
    first anniversary, and at ``t = 27`` on the anchor issued 15 months on.  Point 5's
    $20,000 at policy month 29 falls at ``t = 29`` on its twin and nowhere on the point
    valued at 30, whose opening state carries it.  No other month withdraws.
    """
    def taken(case):
        p = _row(sec_model, *case)
        return [(t, p.wd_pp(t)) for t in range(p.proj_len()) if p.wd_pp(t) != 0.0]

    assert taken(("twin", 1, 0)) == [(12, 4000.0)]
    assert taken(("derived", 1, 12)) == [(0, 4000.0)]
    assert taken(("future", 1, -15)) == [(27, 4000.0)]
    assert taken(("twin", 5, 0)) == [(29, 20000.0)]
    assert taken(("derived", 5, 30)) == []


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date dollars, for every point alike (D7).

    At the shipped 2.5%, on every committed point and in every month, ``expenses(t)`` is
    the acquisition on the contracts issued that month plus ``50 / 12 x 1.025 ** (t // 12)``
    per contract in force, whatever the contract's age: ``MYGA_US_S``'s annual step, taken
    every twelve months from the valuation date.  So the anchor in force 12 months, on its
    anniversary at ``t = 0``, steps at ``t = 12``, its policy month 24, and pays S's
    month-``12 + t`` expenses deflated by 1.025, the step S took at its first anniversary,
    before the valuation date; the anchor issued 15 months on steps at ``t = 12``, before
    its issue; and on a twin the two clocks give S's expenses in every month.  This is the
    only test that sees inflation on the valuation clock: the splice sets the rate to 0,
    and on a point issued at ``t = 0`` the clocks agree.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            want = (p.expense_acq * p.pols_new_biz(t)
                    + p.expense_maint / 12 * (1 + INFLATION) ** (t // 12) * p.pols_if(t))
            assert p.expenses(t) == pytest.approx(want, rel=1e-12, abs=1e-12), (
                point_id, t)
    s1 = _point(s_model, 1)
    anchor, twin = _row(sec_model, "derived", 1, 12), _row(sec_model, "twin", 1, 0)
    assert [anchor.inflation_factor(t) for t in (0, 11, 12)] == [1.0, 1.0, 1 + INFLATION]
    for t in range(anchor.proj_len()):
        assert anchor.expenses(t) == pytest.approx(s1.expenses(12 + t) / (1 + INFLATION),
                                                   rel=1e-12), t
    assert [twin.expenses(t) for t in range(480)] == pytest.approx(
        [s1.expenses(t) for t in range(480)], rel=1e-12)
    fut = _row(sec_model, "future", 1, -15)
    assert [fut.inflation_factor(t) for t in (11, 12, 15)] == [1.0] + [1 + INFLATION] * 2


def test_acquisition_and_the_premium_fall_on_new_business_only(sec_model, tmp_path):
    """The premium, its commission and acquisition, per contract issued, in the issue month.

    On every committed point the premium is ``premium x policy_count()`` in the issue
    month, ``t = -duration_mth``, the commission 2% of it, the premium credited to the
    account value the same, and each is 0 in every other month: ``t = 0`` on the twins,
    ``t = 15`` on the anchor issued 15 months on, and never on a point already in force,
    though on the valuation clock its row 0 is ``t = 0``.  Acquisition ships at 0, so it is
    asserted on a model read afresh with ``expense_acq`` set to 150 before it computes
    anything, from a copy whose twin and future anchor each count 2.5 contracts: what
    ``expenses(t)`` holds beyond maintenance is ``150 x policy_count()``, 375, in the issue
    month and 0 in every other, on the twin, the anchor in force and the anchor issued
    later.  Every shipped point counts one contract, at which a charge per model point,
    150, would pass.  ``MYGA_US_S`` charges both on the count at issue, so the twins agree
    with S at any count, and T1 needs no S point to count one contract.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        issue = -int(table.at[point_id, "duration_mth"])
        issued = [p.policy_count() if t == issue else 0.0 for t in range(p.proj_len())]
        assert [p.premiums(t) for t in range(p.proj_len())] == [
            p.premium_pp() * n for n in issued], point_id
        assert [p.commissions(t) for t in range(p.proj_len())] == pytest.approx(
            [p.comm_rate_acq * p.premium_pp() * n for n in issued], abs=1e-9), point_id
        assert [p.prem_to_av(t) for t in range(p.proj_len())] == [
            p.premium_pp() * (1 - p.load_prem_rate) * n for n in issued], point_id
    committed = _committed()
    issued = [_label(committed, "twin", 1, 0), _label(committed, "future", 1, -15)]
    fresh = _read_edited(tmp_path, _set("policy_count", issued, 2.5))
    try:
        fresh.Projection.expense_acq = 150.0
        for case in (("twin", 1, 0), ("derived", 1, 12), ("future", 1, -15)):
            p = _row(fresh, *case)
            ts = range(p.proj_len())
            maintenance = [p.expense_maint / 12 * p.inflation_factor(t) * p.pols_if(t)
                           for t in ts]
            acq = [p.expenses(t) - m for t, m in zip(ts, maintenance)]
            issue = -p.duration_mth_init()
            expected = [150.0 * p.policy_count() if t == issue else 0.0 for t in ts]
            assert acq == pytest.approx(expected, abs=1e-9), case
            if case[0] != "derived":
                assert (p.policy_count(), acq[issue]) == (2.5, pytest.approx(375.0)), case
    finally:
        fresh.close()


def _monthly_args(model, name, cells, t):
    """Every argument tuple Phase 2's full sweep calls monthly cell ``name`` with at ``t``.

    ``t`` alone, or ``t`` with each timing, each kind, the total where the cell takes it,
    or each scenario column, each passed through :func:`_timing`.
    """
    if len(cells.parameters) == 1:
        return [(t,)]
    if name == "pols_if_at":
        return [(t, _timing(model, x)) for x in TIMINGS]
    if name in ("av_pp_at", "av_at"):
        return [(t, _timing(model, x)) for x in AV_TIMINGS]
    if name in KINDED:
        return [(t, _timing(model, k)) for k in _kinds(model, name)]
    if name == "scenario_rate":
        return [(t, _timing(model, "MARKET_RATE")), (t, _timing(model, "MVA_REF_YIELD"))]
    raise AssertionError(f"{name}{cells.parameters}: a monthly cell _monthly_args lacks")


def _kinds(model, name):
    """The kinds cell ``name`` takes: :data:`KINDS`, and ``ALL`` too in :data:`TOTALLED`
    at stage "EC"."""
    if name in TOTALLED and "ALL" in model.Projection.refs:
        return (*KINDS, "ALL")
    return KINDS


def _outside_cover_faults(model, p, where, scenario=True):
    """Where ``p``, an ItemSpace that has evaluated nothing, answers wrongly outside cover.

    In every month before issue and at ``t = proj_len()``, the first month after cover,
    which the count's and the account value's look-ahead reads: first every cell of
    :data:`OUTSIDE_COVER`, ``pols_if_at``, ``av_pp_at`` and ``av_at`` at each timing and
    the :data:`KINDED` cells at each kind they take, against its value and its type; then
    whether any of :data:`IN_COVER_ONLY` was evaluated at a month,
    a contract year or an age outside cover on the way, which only a fresh ItemSpace can
    say.  Then every monthly cell is called at those months, as Phase 2's full sweep will
    call it, with each of its arguments (:func:`_monthly_args`): none may
    raise or return a numpy type, and afterwards no contract-year state cell may hold a key
    at a year outside the contract's.  With ``scenario=False`` the scenario readers are left
    out of that last call, on a row whose scenario has no month before issue.  A cell that
    raises is reported as a fault too, so the scan goes on.
    """
    faults = []
    months = [*range(p.t_entry()), p.proj_len()]

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
        for timing in TIMINGS:
            call("pols_if_at", (t, _timing(model, timing)), 0.0)
        for name in ("av_pp_at", "av_at"):
            for timing in AV_TIMINGS:
                call(name, (t, _timing(model, timing)), 0.0)
        for name in KINDED:
            for kind in _kinds(model, name):
                call(name, (t, _timing(model, kind)), 0.0)

    def outside(name, key):
        params = p.cells[name].parameters
        if "t" in params:
            return not p.is_active(key if len(params) == 1 else key[params.index("t")])
        if name in ("surr_charge_age_cap_at", "mort_rate_at"):
            return not p.age_at_entry() <= key < p.age_at_entry() + p.policy_term()
        return not 1 <= key <= p.policy_term()

    read = {name: [k for k in p.cells[name].keys() if outside(name, k)][:5]
            for name in IN_COVER_ONLY}
    read = {name: keys for name, keys in read.items() if keys}
    if read:
        faults.append(f"{where}: evaluated outside cover: {read}")
    for name, cells in p.cells.items():
        if "t" not in cells.parameters or (not scenario and name in SCENARIO_READERS):
            continue
        for t in months:
            for args in _monthly_args(model, name, cells, t):
                call(name, args)
    years = {name: [y for y in p.cells[name].keys() if outside(name, y)][:5]
             for name in YEAR_STATE}
    years = {name: keys for name, keys in years.items() if keys}
    if years:
        faults.append(f"{where}: asked about a contract year outside cover: {years}")
    return faults


def test_every_guarded_cell_holds_its_outside_cover_value(spliced):
    """Outside cover each cell holds :data:`OUTSIDE_COVER`'s value, and reads no rate.

    On every committed point, in every month before issue and in the first month after
    cover, ``t = proj_len()``, which the count's look-ahead reads, on a model that evaluates
    nothing else (:func:`_outside_cover_faults`).  ``is_active``'s docstring promises that
    outside cover no count evaluates a rate, and no table is read at a contract year or an
    attained age the contract does not have, so afterwards none of :data:`IN_COVER_ONLY`
    may hold a key outside cover.  Then every monthly cell, guarded or not, is called
    there, as Phase 2's full sweep will call it: each answers, with a Python value.  Every
    monthly cell is one of those lists, or :data:`EVERY_MONTH`'s, so that a cell added to
    the model is placed in one.

    The committed table's one point issued after the valuation date is the anchor, which
    has the base scenario, no interest-only rule, no floor charge and no premium tax, so
    on it a cell tied to one of those would hold zero before issue, guarded or not.  So
    the same scan runs on the splice's future rows, the core's or, with
    ``USLIB_SEC_FULL=1``, all of them, with the splice's assumptions switched on: Camp B,
    the interest-only point, the declared differential, the floor's charge and premium
    tax, and the seven-year period among them.  Their scenarios have no month before issue
    (:func:`_rebase`), and a scenario reader there raises, which is asserted, rather than
    answering with a rate the path does not hold.  Each row is made afresh first and
    released after.

    Several of these guards change no number the frame shows: once the counts are zero
    outside cover, every cash flow is too, and an unguarded value multiplies a zero count.
    They are held here because they are what the docstrings promise a caller, and because
    Phase 2 needs them: a table read at a contract year or an age the contract does not
    have would wrap round in a compiled model rather than fail (USLIB-SEC-PLAN.md F4, R1).
    """
    faults = []
    model = mx.read_model(model_path(SEC), name=_name("cover"))
    try:
        monthly = {n for n, c in model.Projection.cells.items() if "t" in c.parameters}
        placed = {*OUTSIDE_COVER, *IN_COVER_ONLY, *EVERY_MONTH, *KINDED, "pols_if_at",
                  "av_pp_at", "av_at"}
        assert monthly <= placed, f"monthly cells unplaced: {sorted(monthly - placed)}"
        table = model.Data.model_point_table()
        for key, point_id in zip(point_keys(model), table.index):
            faults += _outside_cover_faults(model, projection(model, key),
                                            f"point {point_id}")
    finally:
        model.close()
    sec = spliced[1]
    futures = _selected(FUTURES, CORE_FUTURES)
    for s_point, k in futures:
        key = _row_key(sec, "future", s_point, -k)
        if key in sec.Projection.itemspaces:
            _release(sec, key)
        try:
            p = projection(sec, key)
            where = _case_id("future", s_point, -k)
            faults += _outside_cover_faults(sec, p, where, scenario=False)
            for reader, args in (("market_rate", (0,)), ("mva_ref_yield", (k - 1,)),
                                 ("scenario_rate", (0, _timing(sec, "MARKET_RATE")))):
                with pytest.raises(Exception):
                    p.cells[reader](*args)
        finally:
            _release(sec, key)
    assert futures and not faults, (
        f"{len(faults)} faults outside cover, first:\n  " + "\n  ".join(faults[:20]))


def test_the_points_sum_row_by_row_into_a_block(sec_model, s_model):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    The anchor's twin, the anchor restated at month 12 and the anchor issued 15 months on,
    summed as ``run_sec.py --block`` sums them, are indexed 0..494 and equal S's frame
    added to itself moved 12 months earlier and 15 months later, in every column but the
    two expense inflation moves (:data:`INFLATED`).  A model whose frames sat on the
    policy clock would fail it.  The committed rows are already swept, so it costs a sum.
    """
    cases = (("twin", 1, 0), ("derived", 1, 12), ("future", 1, -15))
    block = pd.concat([_row(sec_model, *case).result_cf() for case in cases]).groupby(
        level="t").sum()
    sdf = _point(s_model, 1).result_cf()
    expected = pd.concat([sdf, sdf.set_axis(sdf.index - 12).loc[0:],
                          sdf.set_axis(sdf.index + 15)]).groupby(level=0).sum()
    assert list(block.index) == list(range(495))
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

    The runner test and the extract test both read ``run_sec.py 8``, and an interpreter
    that reads the model and projects a point costs seconds.
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
    position, every point projects what the committed point it was made from
    projects, in ``result_cf`` and ``result_pols``, to 1e-12.  On every shipped row
    ``source_mth`` equals ``duration_mth``, so a formula that read the one for the other
    would pass every test that leaves ``duration_mth`` as generated.  And ``run_sec.py``,
    run beside the extract, finds point 108 by its label and prints it without saying where
    it came from, every later line as it prints committed point 8, and refuses point 8,
    which the extract does not have, naming the labels it does.
    """
    committed = _committed()
    extract = _relabeled(committed.drop(columns=list(GENERATED_COLUMNS)))
    folder = _sec_inputs(tmp_path, extract)
    model = mx.read_model(folder, name=_name("extract"))
    try:
        table = model.Data.model_point_table()
        assert not set(GENERATED_COLUMNS) & set(table.columns)
        assert list(table.index) == [100 + p for p in reversed(committed.index)]
        for label in table.index:
            mine, base = _point(model, label), _point(sec_model, label - 100)
            for report in ("result_cf", "result_pols"):
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=1e-12, atol=1e-12) == [], (label, report)
            _release(model, _key(model, label))
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    out, base = _run_sec(runner, "108").splitlines(), committed_runs("8").splitlines()
    assert out[0] == ("model point 108: MYGA-000001-M12 - M60 NQ premium 100,000, 5-year "
                      "guarantee period")
    assert out[1:] == base[1:]
    refused = _run_sec(runner, "8", check=False)
    assert refused.returncode == 1 and refused.stdout == b""
    labels = [100 + p for p in reversed(committed.index)]
    assert refused.stderr.decode(errors="replace").strip() == (
        f"no model point 8 in the table: {labels}")


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
            f"contract")


def test_run_sec_prints_a_point_and_the_block(sec_model, committed_runs):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  The anchor's twin, the runner's default, the anchor restated at its
    first anniversary and Camp B in its last covered month, each with its lines at the
    valuation date asserted whole, so that a longer number cannot pass for the one
    asserted: where its row came from, which only the committed table's generator columns
    can say, where it stands, its frame, and the shock lapse of its first renewal year, at
    the valuation month that year opens in, or, on Camp B, that it opened before the
    valuation date.  Then each point's first twelve rows of account value and cash flows.
    And the block: a line for each of the 14 points, in table order, its first twelve rows,
    which must be the committed points' frames summed row by row, as this test sums them,
    and those frames summed into projection years, each year's count the one in force in
    its first month.  Nothing else runs the runner on the committed table.
    """
    twin, anchor = _row(sec_model, "twin", 1, 0), _row(sec_model, "derived", 1, 12)
    last = _row(sec_model, "derived", 3, 479)
    rate = ("declared rate = 4.45%  GMIR = 0.25%  GMSV rate = 2.80%  renewal = {}  MVA = "
            "linear_duration / {}")
    frame = ("proj_len = {} from the valuation date (t = 0..{}); deemed maturity at policy "
             "month 480, attained age 100")
    for args, p, lines in (
            ((), twin, [
                "model point 1: MYGA-000001 (S's MYGA-000001) - M60 NQ premium 100,000, "
                "5-year guarantee period",
                rate.format("rollover", "sym_sc"),
                "at the valuation date: issued at the valuation date, t = 0",
                frame.format(_months(480), 479),
                f"shock lapse at contract year 6, t = 60: {twin.lapse_rate(60):.2%} p.a."]),
            (("8",), anchor, [
                "model point 8: MYGA-000001-M12 (S's MYGA-000001 at its month 12) - M60 NQ "
                "premium 100,000, 5-year guarantee period",
                rate.format("rollover", "sym_sc"),
                f"at the valuation date: {_standing(anchor)}",
                frame.format(_months(468), 467),
                f"shock lapse at contract year 6, t = 48: {anchor.lapse_rate(48):.2%} "
                f"p.a."]),
            (("13",), last, [
                "model point 13: MYGA-000003-M479 (S's MYGA-000003 at its month 479) - M60 "
                "NQ premium 100,000, 5-year guarantee period",
                rate.format("annual_redeclare", "gmir_floor"),
                f"at the valuation date: {_standing(last)}",
                frame.format(_months(1), 0),
                "the first renewal year, contract year 6, opened before the valuation "
                "date"])):
        out = committed_runs(*args)
        assert out.splitlines()[:5] == lines, args
        assert p.result_av().iloc[:12, :5].round(2).to_string() in out, args
        assert p.result_cf().head(12).round(2).to_string() in out, args
    assert "in force 12 months: contract year 2, attained age 61, " in _standing(anchor)
    assert _standing(anchor).endswith("AV 104,450.00 per contract")
    out = committed_runs("--block")
    table = sec_model.Data.model_point_table()
    points = [projection(sec_model, key) for key in point_keys(sec_model)]
    assert out.splitlines()[:len(points) + 1] == [
        "model points, t = 0 the valuation date for each:",
        *("  {:>2}  {:<16} {}; proj_len {}".format(
            point_id, table.at[point_id, "policy_id"], _standing(p), p.proj_len())
          for point_id, p in zip(table.index, points))]
    assert ("  14  MYGA-000001-F15  to be issued at t = 15, 15 months after the valuation "
            "date; proj_len 495") in out
    block = pd.concat([p.result_cf() for p in points]).groupby(level="t").sum()
    assert block.head(12).round(2).to_string() in out
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", [block.at[12 * (y - 1), "pols_if"] for y in annual.index])
    assert annual.head(12).round(2).to_string() in out


def test_run_sec_says_one_month_where_a_point_is_a_month_from_the_valuation_date(tmp_path):
    """The runner writes "1 month", not "1 months", on both sides of the valuation date.

    No committed point is in force one month or issued one month on, so the runner is run,
    with ``--block``, beside a table of two: the anchor moved back to policy month 1, its
    first-year state as ``Data`` requires it, the interest at the anniversary 0 and the
    issue allowance, and the anchor issued a month on.  Each block line is asserted whole.
    """
    committed = _committed()
    anchor = _label(committed, "derived", 1, 12)
    future = _label(committed, "future", 1, -15)
    issue = committed.at[anchor, "free_wd_rate"] * committed.at[anchor, "premium"]
    table = _in_first_year(anchor, 1)(_set("duration_mth", [future], -1)(committed))
    folder = _sec_inputs(tmp_path, table.loc[[anchor, future]])
    assert table.at[anchor, "free_wd_allow_init"] == issue
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    out = _run_sec(runner, "--block").splitlines()
    assert out[:3] == [
        "model points, t = 0 the valuation date for each:",
        f"  {anchor:>2}  MYGA-000001-M12  in force 1 month: contract year 1, attained age "
        f"60, {committed.at[anchor, 'policy_count']:.6f} in force, AV 104,450.00 per "
        f"contract; proj_len 479",
        f"  {future:>2}  MYGA-000001-F15  to be issued at t = 1, 1 month after the "
        f"valuation date; proj_len 481"]


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


def test_the_docstrings_describe_the_valuation_clock(sec_model, s_model):
    """The docstrings say what this model is, and none says what only MYGA_US_S is.

    Whitespace is collapsed first, as ``test_model_conventions`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock, the SEC table and the product.  The
    symbol map in the Projection docstring maps every cell running in force adds, which are
    exactly the cells ``MYGA_US_S`` lacks, and the three opening-state accessors whose
    meaning changed, and names nothing the model lacks: every name in it is a cell, or a
    Reference the notes give a symbol to, as the renewal spread is.  And no docstring says
    what :data:`STALE` matches, each of whose phrases ``MYGA_US_S``'s docstrings say.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE,
                   "multi-year guaranteed annuity"):
        assert phrase in flat["model"], phrase
    assert set(NEW_CELLS) == set(sec_model.Projection.cells) - set(s_model.Projection.cells)
    mapped = _mapped_cells(sec_model.Projection.doc)
    missing = [cells for cells in (*NEW_CELLS, *STATE) if cells not in mapped]
    assert not missing, f"the symbol map does not map {missing}"
    known = set(sec_model.Projection.cells) | set(sec_model.Projection.refs)
    unknown = sorted(mapped - known)
    assert not unknown, f"the symbol map names what the model lacks: {unknown}"
    stale = sorted(where for where, doc in flat.items() if STALE.search(doc))
    assert not stale, f"docstrings that describe MYGA_US_S: {stale}"
    s_flat = [re.sub(r"\s+", " ", doc) for _, doc in _docs(s_model)]
    unsaid = [phrase for phrase in STALE_PHRASES
              if not any(re.search(phrase, doc) for doc in s_flat)]
    assert not unsaid, f"phrases MYGA_US_S does not say, so STALE holds nothing: {unsaid}"


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
    the variants, each property below holds of some core case: each renewal architecture,
    free-withdrawal rule, floor convention, MVA family and cap rule, the free amount exempt
    from the MVA and not, the female cell, each band of the GMIR factor, a guarantee period
    other than five, each withdrawal programme and each scenario, a zero basis, the floor's
    charge, and each kind of valuation month: the first contract year, an anniversary,
    mid-year, the last month of the initial term, the window, inside a renewal period,
    an annual redeclaration month, past the initial term under Camp B, and the last covered
    month.  And of some core future case: issued off the valuation anniversaries and more
    than a year on, Camp B, the interest-only rule, the declared differential, premium tax
    and a seven-year period.

    Then, on the splice's model, of some core row, each of :data:`AT_VALUATION` and
    :data:`IN_FRAME`, what no column of the table shows:

    * every opening-state column is non-zero, the year under way is valued in its first
      year, on an anniversary under each rule and mid-year with part of its allowance used,
      and each rate fixed in the past is read from its column, the rate under each
      architecture and ``i0``, while each fixed at the valuation date, a redeclaration, an
      annual one and a re-lock, is read from the scenario; ``P_accum`` and the interest to
      date are read by their caps in force; a basis below the premium and a zero one; and
      the window, the last covered month and the initial term's last month at ``t = 0``;
    * later in the frame, every branch of the renewal rate and of the competitor-rate
      response that the full grid reaches, each MVA family in force and each cap binding,
      both duration factors and the factor's 6% column, the floor binding on a surrender, a
      schedule that runs out and the age cap, an annuitization, the deemed maturity, a
      utilization and an excess withdrawal, each tax treatment of a withdrawal, and the
      floor's charge, premium tax and acquisition.

    Each core row's branches were recorded by the T2 or T3 case that compared it
    (:func:`_settle`), and a row no case has recorded is evaluated here.
    """
    s_table = _s_table_with_variants()

    def at(p, column):
        return s_table.at[p, column]

    def n12(p):
        return 12 * int(at(p, "guar_period"))

    def camp_b(p):
        return at(p, "renewal_architecture") == "annual_redeclare"

    def choices(column, values):
        return {f"{column} {v}": (lambda k, p, d, v=v, column=column: at(p, column) == v)
                for v in values}

    splices = {
        **choices("renewal_architecture", ("rollover", "annual_redeclare")),
        **choices("free_wd_rule", ("pct_av", "interest_only")),
        **choices("mgsv_wd_convention", ("gross", "net_of_charges")),
        **choices("mva_family", ("linear_duration", "geometric", "declared_differential")),
        **choices("mva_cap_rule", ("sym_sc", "min_sc_interest", "asym_sc_snfl",
                                   "gmir_floor", "none")),
        **choices("free_wd_mva_exempt", (True, False)),
        **choices("sex", ("M", "F")),
        **choices("gmir", (0.0025, 0.02, 0.03)),
        **choices("wd_schedule_id", ("anchor", "none", "charged")),
        **choices("scenario_id", ("base", "stress", "differential")),
        "a guarantee period other than five": lambda k, p, d: at(p, "guar_period") != 5,
        "a zero basis": lambda k, p, d: at(p, "tax_basis_initial") == 0.0,
        "the floor's charge": lambda k, p, d: at(p, "mgsv_annual_charge") > 0.0,
        "the first contract year": lambda k, p, d: 0 < d < 12,
        "an anniversary": lambda k, p, d: d % 12 == 0,
        "mid-year": lambda k, p, d: d > 12 and d % 12 != 0,
        "the last month of the initial term": lambda k, p, d: d == n12(p) - 1,
        "the window": lambda k, p, d: (
            d == n12(p) if camp_b(p) else d > 0 and d % n12(p) == 0),
        "inside a renewal period": lambda k, p, d: (
            not camp_b(p) and d > n12(p) and d % n12(p) != 0),
        "an annual redeclaration month": lambda k, p, d: (
            camp_b(p) and d > n12(p) and d % 12 == 0),
        "past the initial term under Camp B": lambda k, p, d: camp_b(p) and d > n12(p),
        "the last covered month": lambda k, p, d: (
            d == 12 * (100 - int(at(p, "age_at_entry"))) - 1),
    }
    futures = {
        "issued off the anniversaries": lambda p, k: k % 12 != 0,
        "issued more than a year on": lambda p, k: k > 12,
        "Camp B": lambda p, k: camp_b(p),
        "the interest-only rule": lambda p, k: at(p, "free_wd_rule") == "interest_only",
        "the declared differential": lambda p, k: (
            at(p, "mva_family") == "declared_differential"),
        "premium tax": lambda p, k: at(p, "premium_tax_rate") > 0.0,
        "a seven-year period": lambda p, k: at(p, "guar_period") == 7,
    }
    missing = [what for what, holds in splices.items()
               if not any(holds(*case) for case in CORE_SPLICES)]
    missing += [what for what, holds in futures.items()
                if not any(holds(*case) for case in CORE_FUTURES)]
    assert not missing, f"no core case reaches: {missing}"

    reached = set()
    for case in sorted(CORE_GRID):
        reached |= _record_of(spliced, splice_records, case)["branches"]
    missing = [what for what in (*AT_VALUATION, *IN_FRAME) if what not in reached]
    assert not missing, f"no core row reaches: {missing}"


# ---------------------------------------------------------------------------
# Stage EC -- what compiling changed, held in modelx (USLIB-SEC-PLAN.md Phase 2)


def test_the_all_totals_are_s_totals_bit_for_bit(sec_model, s_model):
    """``claims(t, ALL)`` and ``claims_over_av(t, ALL)`` are ``MYGA_US_S``'s totals, bit
    for bit (R12).

    S's ``claims(t, kind=None)`` and ``claims_over_av(t, kind=None)`` are the four kinds'
    total, written as a chain of ``+`` in the kinds' order, and here they are the code
    ``ALL``, the same chain.  T1 reaches S's totals through the spec's ``twin_arg_map``
    to its tolerance; here they are held exactly, on the twins of S's seven points, in
    every month of the frame: each total S's float, its type and the sign of a zero
    included, and each kind S's at the kind's name.  A total summed in another order, or
    one that sums a kind twice and another not at all, moves a last bit or a number in a
    month where three kinds are paid, and fails.
    """
    found = []
    for point in S_POINTS:
        mine, theirs = _row(sec_model, "twin", point, 0), _point(s_model, point)
        assert mine.proj_len() == theirs.proj_len()
        for t in range(mine.proj_len()):
            for cell in TOTALLED:
                got, want = mine.cells[cell](t, mine.ALL), theirs.cells[cell](t, None)
                if (got != want or type(got) is not type(want)
                        or math.copysign(1.0, got) != math.copysign(1.0, want)):
                    found.append(f"point {point}: {cell}({t}, ALL) {got!r}, S's {want!r}")
                for kind in KINDS:
                    if mine.cells[cell](t, _timing(sec_model, kind)) != theirs.cells[cell](
                            t, kind):
                        found.append(f"point {point}: {cell}({t}, {kind}) is not S's")
    assert not found, found[:20]


# The month at which the sign test sets the kinds on the worked example's twin: policy
# month 60, the window, where death, lapse and annuitization are all paid.
ZERO_MONTH = 60


def test_negative_zero_kinds_total_a_negative_zero_as_s_chain_does():
    """Each ``ALL`` total is ``-0.0`` where every kind is ``-0.0``, as S's chain gives.

    S's totals add the four kinds with ``+``, starting at the first, and ``-0.0 + -0.0``
    is ``-0.0``, so S's total of negative zeros keeps its sign.  The split test cannot
    hold it: no committed month has negative zero kinds.  So here, on a read of each
    model of its own, the four kinds of ``claims`` and of ``claims_over_av`` at
    :data:`ZERO_MONTH` on the worked example's twin are set to ``-0.0`` as modelx input
    values, in both models, and each total must be S's: ``-0.0``, a float.  A total
    started at ``0.0``, as a ``sum`` from ``0.0`` is, gives ``0.0`` and fails.
    """
    s = mx.read_model(model_path(TWIN), name=_name("s_zeros"))
    sec = mx.read_model(model_path(SEC), name=_name("zeros"))
    try:
        theirs, mine = _point(s, 1), _row(sec, "twin", 1, 0)
        paid = [kind for kind in KINDS if theirs.claims(ZERO_MONTH, kind) != 0.0]
        assert paid == ["DEATH", "LAPSE", "ANNUITIZATION"], paid
        for cell in TOTALLED:
            for kind in KINDS:
                theirs.cells[cell][ZERO_MONTH, kind] = -0.0
                mine.cells[cell][ZERO_MONTH, _timing(sec, kind)] = -0.0
        totals = [proj.cells[cell](ZERO_MONTH, total) for cell in TOTALLED
                  for proj, total in ((theirs, None), (mine, mine.ALL))]
    finally:
        sec.close()
        s.close()
    for total in totals:
        assert type(total) is float and total == 0.0, totals
        assert math.copysign(1.0, total) == -1.0, totals


def test_the_schedule_code_is_s_schedule_in_every_month(sec_model, s_model):
    """``surr_charge_id(t)`` is S's schedule, as its code, in every month of every twin.

    S returns the schedule's key in lower case, ``"initial"``, ``"renewal"`` or
    ``"none"``, and SEC its code, ``INITIAL``, ``RENEWAL`` or ``NONE``, which T1 cannot
    map, since a code is named in upper case; T1 skips S's cell (the spec's ``exempt``),
    and the rate it selects is compared in every month.  So the code is held to S's key
    here, on the twins of S's seven points, which between them reach all three, in every
    month of the frame, each an int.  The codes are 0, 1 and 2, and each is the row of
    ``Data.surr_charge_array`` that holds its schedule's rates, at their contract years,
    as *surr_charge_table.csv* holds them: a code swapped with another reads another
    schedule, and on an annual-redeclare point ``NONE`` read as ``RENEWAL`` charges past
    the initial term, where the shipped rates of the two schedules may agree.
    """
    proj = sec_model.Projection
    names = {"none": proj.NONE, "initial": proj.INITIAL, "renewal": proj.RENEWAL}
    assert list(names.values()) == [0, 1, 2]
    rates = pd.read_csv(model_path(SEC).parent / "surr_charge_table.csv")
    held = sec_model.Data.surr_charge_array()
    for schedule in ("initial", "renewal"):
        rows = rates[rates["schedule"] == schedule]
        assert held[names[schedule], rows["contract_year"].to_numpy()].tolist() == (
            rows["surr_charge_rate"].tolist()), schedule
    found, seen = [], set()
    for point in S_POINTS:
        mine, theirs = _row(sec_model, "twin", point, 0), _point(s_model, point)
        for t in range(mine.proj_len()):
            want, got = theirs.surr_charge_id(t), mine.surr_charge_id(t)
            seen.add(want)
            if type(got) is not int or got != names[want]:
                found.append(f"point {point}: surr_charge_id({t}) {got!r}, S's {want!r}")
    assert seen == set(names), seen
    assert not found, found[:20]


# Where the three cells MYGA_US_SEC keeps as S wrote them (the registry's "engine") cannot
# answer: a CMT level or a term that is not a number, or not finite.  And below 0, which
# the arguments T1 compares, all 0 or more, do not reach.
NOT_FINITE = (float("nan"), float("inf"), float("-inf"))
NEGATIVE = (-0.0123, -0.0004, -2.5)


def test_the_engine_cells_raise_where_s_raises():
    """The three engine cells refuse what ``MYGA_US_S``'s refuse, with S's error.

    ``mgsv_rate_statutory``, ``mgsv_rate_is_compliant`` and ``mva_ref_term_years`` are
    S's formulas, ``math`` included, kept as Python cells beside the compiled ones (R14):
    no projection cell calls them, and T1 compares them at the arguments S's own tests
    use.  Rounded by ``math.floor`` and ``math.ceil``, a level that is not a number raises
    ``ValueError`` and an infinite one ``OverflowError``, where integer arithmetic would
    answer the statutory cap.  So each is called at NaN and at either infinity, on the
    worked example in each model, and each must raise S's error and message; and at
    arguments below 0 (:data:`NEGATIVE`) each must return S's value.
    """
    s = mx.read_model(model_path(TWIN), name=_name("s_engine"))
    sec = mx.read_model(model_path(SEC), name=_name("engine"))
    try:
        theirs, mine = _point(s, 1), _row(sec, "twin", 1, 0)
        found = []
        for cell in ("mgsv_rate_statutory", "mgsv_rate_is_compliant",
                     "mva_ref_term_years"):
            for value in NOT_FINITE:
                did = []
                for proj in (theirs, mine):
                    try:
                        did.append(("ok", proj.cells[cell](value)))
                    except Exception as err:    # what S raised is what SEC must
                        did.append(("raised", _raised(err)))
                if did[0][0] != "raised" or did[1] != did[0]:
                    found.append(f"{cell}({value}): S {did[0]}, SEC {did[1]}")
            for value in NEGATIVE:
                want, got = theirs.cells[cell](value), mine.cells[cell](value)
                if got != want or type(got) is not type(want):
                    found.append(f"{cell}({value}): S {want!r}, SEC {got!r}")
    finally:
        sec.close()
        s.close()
    assert not found, found

def _drain(table):
    """An edit of the withdrawals that adds ``drain``: the anchor's whole premium,
    $100,000, withdrawn in its issue month, policy month 0."""
    added = pd.DataFrame([("drain", 0, 100000.0, "test copy")],
                         columns=["wd_schedule_id", "t", "wd_amount", "provenance"])
    return pd.concat([table, added], ignore_index=True)


def _minus_one(table):
    """An edit of the scenarios that adds ``minus1``, a reference yield of -1 from t = 0."""
    added = pd.DataFrame([("minus1", 0, -1.0, 0.0445, "test copy")],
                         columns=["scenario_id", "t", "mva_ref_yield", "market_rate",
                                  "provenance"])
    return pd.concat([table, added], ignore_index=True)


# The three divisors a cell tests before it divides, each brought to zero by S's own inputs
# or References, as (case, S point, its columns written, the input edits, the References,
# the calls): the account value in cover, where the anchor withdraws its whole premium in
# its issue month, which every report reaches through the dynamic lapse; the geometric
# MVA's 1 + it + s_adm, at a reference yield of -1 with no spread; and the statute's
# rounding step, in an engine cell.
ZERO_DIVISORS = [
    ("the whole account value withdrawn", 1, {"wd_schedule_id": "drain"},
     {"withdrawal_table.csv": _drain}, {}, [("lapse_dyn_rate", (0,)), ("net_cf", (0,))]),
    ("a geometric MVA's divisor at zero", 4, {"scenario_id": "minus1"},
     {"rate_scenario.csv": _minus_one}, {"mva_admin_spread": 0.0}, [("mva_rate", (1,))]),
    ("a statutory rounding step of zero", 1, {}, None, {"mgsv_stat_step": 0.0},
     [("mgsv_rate_statutory", (0.03,))]),
]
ZERO_DIVISION = "ZeroDivisionError: float division by zero"


def _zero_divisor_tables(s_point, columns):
    """S's table and the committed SEC table, with ``columns`` written on ``s_point`` and
    on its twin."""
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    committed = _committed()
    twin = _label(committed, "twin", s_point, 0)
    for column, value in columns.items():
        s_table = _set(column, [s_point], value)(s_table)
        committed = _set(column, [twin], value)(committed)
    return s_table, committed


def test_a_zero_divisor_raises_s_error_with_s_message(tmp_path):
    """A divisor of zero raises S's ``ZeroDivisionError``, with S's message, in each model.

    Compiled division words it ``float division``, so each cell whose divisor its inputs
    can bring to zero tests the divisor and raises Python's own error and message first,
    ``float division by zero``; the compiled model is held to it by
    :func:`test_the_compiled_model_divides_by_zero_as_modelx_does`.  Here, in modelx, each
    case of :data:`ZERO_DIVISORS` is S's own inputs, read by ``MYGA_US_S`` on its point and
    by this model on the twin, and each call must raise that error in both.  The anchor
    that withdraws its whole premium closes its issue month with an account value of
    exactly 0.0.
    """
    found = []
    for number, (case, s_point, columns, edits, refs, calls) in enumerate(ZERO_DIVISORS):
        s_table, table = _zero_divisor_tables(s_point, columns)
        s = mx.read_model(temp_inputs(tmp_path / f"s{number}", model_path(TWIN),
                                      model_points=s_table, edits=edits),
                          name=_name("s_zero"))
        sec = mx.read_model(_sec_inputs(tmp_path / f"sec{number}", table, edits=edits),
                            name=_name("zero"))
        try:
            for model in (s, sec):
                for ref, value in refs.items():
                    setattr(model.Projection, ref, value)
            theirs, mine = _point(s, s_point), _row(sec, "twin", s_point, 0)
            if "wd_schedule_id" in columns:
                assert mine.av_pp(0) == 0.0 and mine.is_active(0)
            for cell, args in calls:
                did = []
                for proj in (theirs, mine):
                    try:
                        did.append(("ok", proj.cells[cell](*args)))
                    except Exception as err:    # what S raised is what SEC must
                        did.append(("raised", _raised(err)))
                if did != [("raised", ZERO_DIVISION)] * 2:
                    found.append(f"{case}: {cell}{args}: S {did[0]}, SEC {did[1]}")
        finally:
            sec.close()
            s.close()
    assert not found, found


def test_every_parameterless_cell_returns_a_python_number(sec_model):
    """Every parameterless cell but the reporting ones returns a Python int, float or bool.

    R11: a ``Projection`` cell that reads a ``Data`` vector converts the element, ``int()``
    or ``float()``, so that modelx returns a Python number, as the compiled cell does, and
    not a numpy scalar, whose arithmetic and printing differ.  A conversion left out moves
    no number and still compiles, so it is asserted here: on every committed point, each
    parameterless cell outside :func:`sec_support.reporting_cells` returns exactly an
    ``int``, a ``float`` or a ``bool``.
    """
    from sec_support import reporting_cells
    space = sec_model.Projection
    reporting = reporting_cells(SEC, space)
    names = sorted(name for name, cell in space.cells.items()
                   if not cell.parameters and name not in reporting)
    assert "mort_schedule" in names and "point_id" in names
    found = []
    for key in point_keys(sec_model):
        proj = projection(sec_model, key)
        found += [f"{key}: {name} {type(value).__name__}" for name in names
                  if type(value := proj.cells[name]()) not in (int, float, bool)]
    assert not found, found


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


def _mortality_to(last):
    """An edit of the mortality table that ends each sex's rows at age ``last``."""
    return lambda table: table[table["age"] <= last].reset_index(drop=True)


def _not_issued_cases():
    """:data:`NOT_ISSUED`'s inputs, as (case, the table, the edits, the label, the
    message, the References that let it project or None, its frame then).

    Each on the committed table relabeled ``100 + point_id`` and written in reverse
    (:func:`_relabeled`), so that the label named is no position.
    """
    committed = _committed()
    table = _relabeled(committed)
    twin = 100 + _label(committed, "twin", 1, 0)
    in_force = 100 + _label(committed, "derived", 5, 30)
    above = f"point_id {twin}: issue age 86 is above issue_age_max, 85"
    # Camp B in its last covered month is at attained age 99, which Data refuses on a
    # mortality table that ends at 98, and is left out of those cases.
    short = table.drop(index=[100 + _label(committed, "derived", 3, 479)])
    return [
        ("an issue age of 86", _set("age_at_entry", [twin], 86)(table), None, twin, above,
         {"issue_age_max": 86}, 12 * (100 - 86)),
        ("an issue age of -1, in force 30 months",
         _set("age_at_entry", [in_force], -1)(table),
         {"mort_table.csv": _extended_mortality}, in_force,
         f"point_id {in_force}: issue age -1 is below issue_age_min, 0",
         {"issue_age_min": -1}, 12 * (100 + 1) - 30),
        ("a mortality table that ends at 98", short, {"mort_table.csv": _mortality_to(98)},
         twin, f"point_id {twin}: the mortality table gives no rate at attained age 99, "
         f"the last before the deemed maturity", {"maturity_age": 99}, 12 * (99 - 60)),
        ("an issue age of 86 on a table that ends at 98: the bound's rule before the "
         "table's", _set("age_at_entry", [twin], 86)(short),
         {"mort_table.csv": _mortality_to(98)}, twin, above, None, None),
    ]


NOT_ISSUED = _not_issued_cases()


@pytest.mark.parametrize("case, table, edits, label, message, issue, frame", NOT_ISSUED,
                         ids=[c[0] for c in NOT_ISSUED])
def test_a_point_the_contract_does_not_issue_is_refused_by_proj_len(tmp_path, case, table,
                                                                    edits, label, message,
                                                                    issue, frame):
    """``proj_len()`` refuses a point the contract does not issue, naming it (§6.1).

    ``MYGA_US_S`` projects a point issued at any age its mortality rates to maturity, but
    the compiled caches are sized from the contract, cover from ``issue_age_min``, 0, to
    ``maturity_age``, 100, and the shipped horizon (``spec_sec.py``), and a point past
    them runs past the caches.  So the frame refuses such a point, naming it by its label:
    issued above ``issue_age_max``, 85, the oldest age ``product-spec.md`` issues at,
    which no cache needs; issued below ``issue_age_min``, on mortality extended below 40
    so that ``Data`` reads it; or on a mortality table whose last age falls short of the
    last covered month's, 99, which ``Data`` cannot check, ``maturity_age`` being a
    ``Projection`` Reference.  Each by the rule asked first (:data:`NOT_ISSUED`).  The
    table reads, since these are rules of the product, and every report is refused with
    the frame.  Each projects once the Reference that refuses it is moved: the issue age
    of 86 once ``issue_age_max`` is 86, the issue age of -1 once ``issue_age_min`` is
    -1, and the table ending at 98 once ``maturity_age`` is 99, each its whole frame and
    both checks closing.  A bound off by one, or a refusal lost or asked in another
    order, lets a point through or names the wrong rule.
    """
    model = mx.read_model(_sec_inputs(tmp_path, table, edits), name=_name("not_issued"))
    try:
        assert len(model.Data.model_point_table()) == len(table)
        p = _point(model, label)
        assert p.point_id() == label != list(table.index).index(label)
        for report in REPORTS:
            _refused(p.cells[report], message)
    finally:
        model.close()
    if issue is None:
        return
    model = mx.read_model(_sec_inputs(tmp_path / "issued", table, edits),
                          name=_name("issued"))
    try:
        for ref, value in issue.items():
            setattr(model.Projection, ref, value)
        p = _point(model, label)
        assert p.proj_len() == len(p.result_cf()) == frame, (p.proj_len(), frame)
        assert p.check_av_roll_fwd() and p.check_pols_roll_fwd()
    finally:
        model.close()


# The five columns MYGA_US_S branches on, each value it tests, which Data decodes into a
# flag a value (R6), and the variants of a value it does not know: upper case, and a
# leading space.  S compares each by ==, so each variant is no value S knows.
DECODED = {"mgsv_wd_convention": ("gross", "net_of_charges"),
           "renewal_architecture": ("rollover", "annual_redeclare"),
           "free_wd_rule": ("pct_av", "interest_only"),
           "mva_family": ("linear_duration", "geometric", "declared_differential"),
           "mva_cap_rule": ("none", "sym_sc", "min_sc_interest", "asym_sc_snfl",
                            "gmir_floor")}
VARIANT_OF = {"upper": str.upper, "space": lambda value: " " + value}

# The default run's variant of each column; the other 23 run with USLIB_SEC_FULL=1.
CORE_DECODES = {("mgsv_wd_convention", "net_of_charges", "space"),
                ("renewal_architecture", "annual_redeclare", "upper"),
                ("free_wd_rule", "interest_only", "space"),
                ("mva_family", "geometric", "upper"),
                ("mva_cap_rule", "gmir_floor", "space")}
UNDECODABLE = [pytest.param(column, value, how, id=f"{column}-{value}-{how}",
                            marks=() if (column, value, how) in CORE_DECODES
                            else FULL_ONLY)
               for column, values in DECODED.items() for value in values
               for how in VARIANT_OF]


@pytest.mark.parametrize("column, value, how", UNDECODABLE)
def test_each_decode_is_s_exact_comparison(tmp_path, column, value, how):
    """A value S does not know is answered as S answers it: refused alike, or projected.

    ``Data`` decodes each of the five columns ``MYGA_US_S`` branches on into a flag a
    value, set where the column is exactly that value, S's ``==`` (R6), so a value written
    otherwise is no value: under ``mgsv_wd_convention``, ``free_wd_rule``, ``mva_family``
    and ``mva_cap_rule`` S's projection refuses it, ``invalid ...``, and so must SEC's,
    with S's message; under ``renewal_architecture`` S projects it, as neither
    architecture, and so must SEC, every cell S computes, under T1.  Each variant of each
    value (:data:`DECODED`, upper case and a leading space) is written on the S point that
    carries the value, in a copy of S's table, and on its twin, in a copy of the committed
    table, each read on a model of its own.  A decode that stripped a space or ignored
    case would read the value S refuses, and fail.
    """
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    point = s_table.index[s_table[column] == value][0]
    variant = VARIANT_OF[how](value)
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN),
                                  model_points=_set(column, [point], variant)(s_table)),
                      name=_name("s_decode"))
    sec = mx.read_model(_sec_inputs(tmp_path / "sec",
                                    _set(column, [point], variant)(_committed())),
                        name=_name("decode"))
    try:
        theirs, mine = _point(s, point), _row(sec, "twin", point, 0)
        assert theirs.cells[column]() == mine.cells[column]() == variant
        did = []
        for proj in (theirs, mine):
            try:
                did.append(("ok", [proj.cells[report]() is not None
                                   for report in REPORTS]))
            except Exception as err:            # what S raised is what SEC must
                did.append(("raised", _raised(err)))
        assert did[1] == did[0], did
        if did[0][0] == "ok":
            assert column == "renewal_architecture", did
            _sweep_s(theirs)
            assert _mismatches(theirs, mine,
                               exempt=TWIN_EXEMPT_DEFAULT | SPEC.exempt) == []
        else:
            assert did[0][1] == f"ValueError: invalid {column}", did
    finally:
        sec.close()
        s.close()


# Each Data vector of a point, with what MYGA_US_S's own expression gives for the point's
# row as read_csv reads it, which is how S reads its table: by float(), int(), bool() and
# ==.  The flags are S's == on the column, and free_wd_mva_exempt S's bool(), as ints.
FLAGS = {"is_wd_gross": ("mgsv_wd_convention", "gross"),
         "is_wd_net_of_charges": ("mgsv_wd_convention", "net_of_charges"),
         "is_rollover": ("renewal_architecture", "rollover"),
         "is_annual_redeclare": ("renewal_architecture", "annual_redeclare"),
         "is_pct_av": ("free_wd_rule", "pct_av"),
         "is_interest_only": ("free_wd_rule", "interest_only"),
         "is_linear_duration": ("mva_family", "linear_duration"),
         "is_geometric": ("mva_family", "geometric"),
         "is_declared_differential": ("mva_family", "declared_differential"),
         "is_cap_none": ("mva_cap_rule", "none"),
         "is_cap_sym_sc": ("mva_cap_rule", "sym_sc"),
         "is_cap_min_sc_interest": ("mva_cap_rule", "min_sc_interest"),
         "is_cap_asym_sc_snfl": ("mva_cap_rule", "asym_sc_snfl"),
         "is_cap_gmir_floor": ("mva_cap_rule", "gmir_floor")}
WHOLE = ("age_at_entry", "duration_mth", "guar_period")
REAL = ("policy_count", "premium", "declared_rate_initial", "gmir", "mgsv_rate",
        "mgsv_annual_charge", "free_wd_rate", "mva_ref_yield_at_issue", "premium_tax_rate",
        *STATE)

# What the vectors test writes into a copy of the committed table, as (column, the
# twin of S's point, the value): a flag's value in upper case and with a space, which no
# flag may read; a 0 among the exemption's True and False, which makes the column text,
# where S's bool() reads every value, "False" among them, as True; and an amount written
# 1_000, which S's float() reads as 1000.0 and pandas' parsing as no number.
WRITTEN_OTHERWISE = (("mgsv_wd_convention", 1, "Gross"),
                     ("renewal_architecture", 2, " rollover"),
                     ("free_wd_mva_exempt", 4, "0"), ("premium", 6, "1_000"))


def _data_mismatches(model, table):
    """Where ``model``'s ``Data`` vectors depart from S's reading of ``table``'s rows."""
    data, found = model.Data, []
    rows = [table.loc[label] for label in table.index]
    expected = {"point_id": ("int64", [int(label) for label in table.index]),
                "free_wd_mva_exempt": ("int64", [int(bool(r["free_wd_mva_exempt"]))
                                                 for r in rows])}
    expected.update((name, ("int64", [int(r[name]) for r in rows])) for name in WHOLE)
    expected.update((name, ("float64", [float(r[name]) for r in rows])) for name in REAL)
    expected.update((name, ("int64", [int(r[column] == value) for r in rows]))
                    for name, (column, value) in FLAGS.items())
    for name, (dtype, want) in expected.items():
        have = data.cells[name]()
        if have.dtype != dtype or have.shape != (len(rows),):
            found.append(f"{name}: {have.dtype} {have.shape}, not {dtype}")
        elif [x for x in have.tolist()] != want:
            found.append(f"{name}: {have.tolist()}, S reads {want}")
    for name, column, file in (("scenario_number", "scenario_id", data.rate_scenario_file),
                               ("wd_schedule_number", "wd_schedule_id",
                                data.withdrawal_file),
                               ("mort_schedule", "sex", data.mort_table_file)):
        ids = sorted(set(pd.read_csv(data.input_dir() / file)[column]))
        want = [ids.index(r[column]) + 1 for r in rows]
        if data.cells[name]().tolist() != want:
            found.append(f"{name}: {data.cells[name]().tolist()}, by sorted key {want}")
    return found


def test_the_data_vectors_hold_the_table_as_s_reads_it(sec_model, tmp_path):
    """Each ``Data`` vector holds its column as ``MYGA_US_S`` reads it, point by point.

    ``Projection`` reads a point's values as elements of ``Data`` vectors, ``[idx]``,
    where ``MYGA_US_S`` reads its model point's row.  So each vector is held to S's own
    expression on the row as ``read_csv`` gives it: ``int()`` of the label and of the
    three whole numbers, ``float()`` of the count and of the eighteen amounts and rates,
    S's ``bool()`` of ``free_wd_mva_exempt`` and S's ``==`` of each of the fourteen
    flags, int64 and float64 one element a point; and each join's number to its key's
    place among the table's sorted keys, from 1.  On the committed table, and on a copy
    with values S reads otherwise than pandas would (:data:`WRITTEN_OTHERWISE`): a flag's
    value in another case or with a space, which S's ``==`` does not match, a ``0`` that
    makes the exemption's column text, where S's ``bool()`` reads ``"False"`` as true,
    and an amount written ``1_000``,
    which S's ``float()`` reads and pandas' parsing does not.  A vector built by pandas'
    parsing, or a decode that strips or folds case, reads one of them otherwise, and
    fails.
    """
    found = [f"committed: {line}" for line in _data_mismatches(sec_model, _committed())]
    table = _committed()
    for column, s_point, value in WRITTEN_OTHERWISE:
        table = _set(column, [_label(table, "twin", s_point, 0)], value)(table)
    folder = _sec_inputs(tmp_path, table)
    written = pd.read_csv(folder.parent / TABLE, index_col="point_id")
    assert not any(pd.api.types.is_numeric_dtype(written[column])
                   or pd.api.types.is_bool_dtype(written[column])
                   for column in ("premium", "free_wd_mva_exempt"))
    model = mx.read_model(folder, name=_name("vectors"))
    try:
        found += [f"written otherwise: {line}" for line in _data_mismatches(model, written)]
        assert model.Data.premium()[list(written.index).index(6)] == 1000.0
    finally:
        model.close()
    assert not found, found


def _reversed(*columns):
    """An edit that writes a table's rows in reverse order, ``columns`` as floats."""
    return lambda table: table.iloc[::-1].assign(
        **{column: table.iloc[::-1][column].astype(float) for column in columns})


def _scenarios_apart(table):
    """The shipped scenarios, ``base`` keyed at months -5, -2 and 3, and ``late``, which
    no point names, from month 7, each level its own."""
    held = table[table["scenario_id"] != "base"]
    rows = [("base", -5, 0.071, 0.041), ("base", -2, 0.062, 0.042),
            ("base", 3, 0.053, 0.043), ("late", 7, 0.044, 0.034),
            ("late", 30, 0.035, 0.025)]
    added = pd.DataFrame(rows, columns=["scenario_id", "t", "mva_ref_yield",
                                        "market_rate"]).assign(provenance="test copy")
    return pd.concat([held, added], ignore_index=True)


def _withdrawals_apart(table):
    """The shipped programmes, ``anchor`` with rows at policy months -3 and 0 and at its
    last covered month, 479, beside its 12, each amount its own."""
    rows = [("anchor", -3, 700.0), ("anchor", 0, 300.0), ("anchor", 479, 900.0)]
    added = pd.DataFrame(rows, columns=["wd_schedule_id", "t", "wd_amount"]).assign(
        provenance="test copy")
    return pd.concat([table, added], ignore_index=True)


# The numeric key of each assumption table.
KEY_COLUMNS = {"mort_table.csv": "age", "surr_charge_table.csv": "contract_year",
               "surr_charge_age_cap.csv": "age", "rate_scenario.csv": "t",
               "withdrawal_table.csv": "t", "mva_factor_table.csv": "years_remaining"}

# The keys test's copy: every assumption table written in reverse key order, its numeric
# keys as floats, and the scenarios and withdrawals with keys at and below 0.
KEYS_APART = {"mort_table.csv": _reversed("age"),
              "surr_charge_table.csv": _reversed("contract_year"),
              "surr_charge_age_cap.csv": _reversed("age"),
              "rate_scenario.csv": lambda t: _reversed("t")(_scenarios_apart(t)),
              "withdrawal_table.csv": lambda t: _reversed("t")(_withdrawals_apart(t)),
              "mva_factor_table.csv": _reversed("years_remaining")}


def _step_levels(rows, column, last):
    """A scenario's level in each month 0 .. ``last``, the latest key at or before it, as
    ``MYGA_US_S``'s step function reads it; NaN before its first key."""
    pairs = sorted(zip(rows["t"].astype(int), rows[column]))
    levels = []
    for month in range(last + 1):
        held = [level for key, level in pairs if key <= month]
        levels.append(held[-1] if held else float("nan"))
    return levels


def test_the_arrays_hold_each_table_at_its_keys_and_pad_with_nan(sec_model, tmp_path):
    """Each ``Data`` array holds its table's values at their keys, and NaN where none is.

    Each table a cell reads by key becomes an array indexed by the key (R7), read by
    element.  So on a copy of every table written in reverse key order, its numeric keys
    as floats, ``1.0`` (:data:`KEYS_APART`), each array holds each row's value at the
    row's key, read from the file, a schedule's at its code and a sex's, a scenario's and
    a programme's at its number, the sorted keys' place from 1: so a numbering by file
    order, or a value read by position, is seen.  Each scenario is its step function,
    month by month, as ``MYGA_US_S``'s ``max()`` of the months at or before reads it:
    ``base``'s keys at -5, -2 and 3 give month 0 the level of -2, not the first, and
    ``late``, from month 7, is NaN before it, its first month 7.  Withdrawals are a
    value: 0.0 in every month a programme has no row, the row at month -3 nowhere, and
    the last covered month's at its month, not wrapped into the array from its end.

    The padding is NaN, as ``Data``'s docstring says, so that a read past a check, were
    one lost, would make every number after it NaN rather than another key's value: row
    0 of every array numbered from 1, column 0 of the surrender charges, each sex's ages
    below its first, the age cap's below its first; and on the committed model, no value
    any cell has cached on any committed point, after the full sweep, is NaN, so no
    projection reads padding.
    """
    model = mx.read_model(temp_inputs(tmp_path, model_path(SEC), edits=KEYS_APART),
                          name=_name("keys_apart"))
    try:
        data, here = model.Data, model.Data.input_dir()
        read = {name: pd.read_csv(here / name) for name in KEYS_APART}
        for name, key in KEY_COLUMNS.items():
            assert read[name][key].dtype == float, name
        mort, sexes = data.mort_table_array(), sorted(set(read["mort_table.csv"]["sex"]))
        for _, row in read["mort_table.csv"].iterrows():
            assert mort[sexes.index(row["sex"]) + 1, int(row["age"])] == row["mort_rate"]
        codes = {"initial": model.Projection.INITIAL, "renewal": model.Projection.RENEWAL}
        charges = data.surr_charge_array()
        for _, row in read["surr_charge_table.csv"].iterrows():
            assert charges[codes[row["schedule"]], int(row["contract_year"])] == row[
                "surr_charge_rate"]
        caps = data.surr_charge_age_cap_array()
        for _, row in read["surr_charge_age_cap.csv"].iterrows():
            assert caps[int(row["age"])] == row["surr_charge_cap"]
        factors = data.mva_factor_array()
        for _, row in read["mva_factor_table.csv"].iterrows():
            assert factors[int(row["years_remaining"])].tolist() == [row["factor_lo"],
                                                                     row["factor_hi"]]
        steps = read["rate_scenario.csv"]
        ids, last = sorted(set(steps["scenario_id"])), data.scenario_last_mth()
        assert ids == ["base", "differential", "late", "stress"] and last == 30
        for column, array in (("mva_ref_yield", data.mva_ref_yield_array()),
                              ("market_rate", data.market_rate_array())):
            assert np.isnan(array[0]).all()
            for s, scenario in enumerate(ids, start=1):
                want = _step_levels(steps[steps["scenario_id"] == scenario], column, last)
                assert np.array_equal(array[s], want, equal_nan=True), (column, scenario)
        assert data.scenario_first_mths().tolist() == [0, 0, 0, 7, 0]
        assert data.market_rate_array()[1, :4].tolist() == [0.042, 0.042, 0.042, 0.043]
        programmes = read["withdrawal_table.csv"]
        ids, amounts = sorted(set(programmes["wd_schedule_id"])), data.wd_amount_array()
        assert data.wd_last_mth() == 479 and amounts.shape == (len(ids) + 1, 480)
        assert np.isnan(amounts[0]).all() and not np.isnan(amounts[1:]).any()
        want = np.zeros((len(ids) + 1, 480))
        for _, row in programmes.iterrows():
            if row["t"] >= 0:
                want[ids.index(row["wd_schedule_id"]) + 1, int(row["t"])] = row["wd_amount"]
        assert np.array_equal(amounts[1:], want[1:])
        assert 700.0 not in amounts[1:]
    finally:
        model.close()
    data = sec_model.Data
    assert data.mort_age_firsts().tolist() == [0, 40, 40]
    mort = data.mort_table_array()
    assert np.isnan(mort[0]).all() and np.isnan(mort[1:, :40]).all()
    assert not np.isnan(mort[1:, 40:]).any()
    charges, last = data.surr_charge_array(), data.surr_charge_last_years()
    assert np.isnan(charges[0]).all() and np.isnan(charges[:, 0]).all() and last[0] == 0
    for code in (1, 2):
        assert not np.isnan(charges[code, 1:last[code] + 1]).any()
        assert np.isnan(charges[code, last[code] + 1:]).all()
    caps, first = data.surr_charge_age_cap_array(), data.surr_charge_age_cap_first()
    assert first == 94 and np.isnan(caps[:first]).all() and not np.isnan(caps[first:]).any()
    for array in (data.mva_ref_yield_array(), data.market_rate_array(),
                  data.wd_amount_array()):
        assert np.isnan(array[0]).all() and not np.isnan(array[1:]).any()
    assert not np.isnan(data.mva_factor_array()).any()
    found = []
    for key in point_keys(sec_model):
        proj = projection(sec_model, key)
        for name, cells in proj.cells.items():
            for args in list(cells.keys()):
                args = args if isinstance(args, tuple) else (args,)
                value = cells(*args)
                if isinstance(value, float) and math.isnan(value):
                    found.append(f"point {proj.point_id()}: {name}{args}")
                elif isinstance(value, pd.DataFrame) and value.isna().any().any():
                    found.append(f"point {proj.point_id()}: {name}")
    assert not found, found[:20]


def test_scenario_keys_at_or_below_0_and_withdrawals_before_issue_read_as_s_reads_them(
        tmp_path):
    """A scenario keyed before ``t = 0`` and a withdrawal at a negative month are S's.

    ``MYGA_US_S`` reads a scenario's level at month ``t`` as the latest key at or before
    it, a negative key among them, and a withdrawal by its month's key, which no month of
    cover reaches below 0.  ``Data`` fills the scenario into an array from month 0 and
    drops a withdrawal row before month 0, so a fill that took the first negative level,
    or wrote the row at -3 into the array's third column from the end, would part from
    S.  So on copies of S's and SEC's inputs whose ``base`` scenario is keyed at -5, -2
    and 3 and whose ``anchor`` programme has rows at -3, 0 and 479, its last covered month
    (:func:`_scenarios_apart`, :func:`_withdrawals_apart`), the anchor's twin, which runs
    on both, computes S's every cell under T1, and the anchor issued 15 months on reads
    the level of month 3 in its issue month.
    """
    edits = {"rate_scenario.csv": _scenarios_apart,
             "withdrawal_table.csv": _withdrawals_apart}
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), edits=edits),
                      name=_name("s_keys"))
    sec = mx.read_model(_sec_inputs(tmp_path / "sec", _committed(), edits),
                        name=_name("keys"))
    try:
        theirs, mine = _point(s, 1), _row(sec, "twin", 1, 0)
        _sweep_s(theirs)
        assert [theirs.market_rate(t) for t in range(4)] == [0.042, 0.042, 0.042, 0.043]
        assert [theirs.wd_scheduled_pp(t) for t in (0, 12, 479)] == [300.0, 4000.0, 900.0]
        assert _mismatches(theirs, mine, exempt=TWIN_EXEMPT_DEFAULT | SPEC.exempt) == []
        late = _row(sec, "future", 1, -15)
        assert late.market_rate(15) == 0.043 and late.wd_scheduled_pp(15) == 300.0
    finally:
        sec.close()
        s.close()


def _far(row, columns):
    """An edit that adds ``row`` to a plain table of ``columns``, provenance last."""
    def edit(table):
        added = pd.DataFrame([(*row, "test copy")], columns=[*columns, "provenance"])
        return pd.concat([table, added], ignore_index=True)
    return edit


# A key far past every frame, below 2**53, in each table read by month: a level of the
# base scenario and a withdrawal of the anchor programme at month 1e10, which MYGA_US_S
# looks up and never reaches, and which no read of this model reaches either.
FAR_KEYS = {"rate_scenario.csv": _far(("base", 1e10, 0.5, 0.5),
                                      ("scenario_id", "t", "mva_ref_yield", "market_rate")),
            "withdrawal_table.csv": _far(("anchor", 1e10, 777.0),
                                         ("wd_schedule_id", "t", "wd_amount"))}


def test_a_key_far_past_every_frame_is_held_nowhere_and_projects_as_without_it(
        sec_model, tmp_path):
    """A row at month 1e10 widens no array, and every point projects as without it.

    ``Data`` holds the scenario and withdrawal arrays to ``read_last_mth``, the last month
    any read reaches, 1,321 as shipped, the last ``t`` ``spec_sec.py`` derives; were they as
    wide as the largest key, a row at 1e10 would ask for 373 GiB, where ``MYGA_US_S``
    projects the table.  So on copies whose ``base`` scenario and ``anchor`` programme each
    have a row at 1e10 (:data:`FAR_KEYS`): ``MYGA_US_S`` projects the anchor; the arrays
    end at month 1,321; and every committed point's three reports are the committed
    model's, value for value, as though the rows were not there.  Compiled, the same holds
    against modelx (:func:`test_the_compiled_model_holds_a_far_key_as_modelx_does`).
    """
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), edits=FAR_KEYS),
                      name=_name("s_far"))
    try:
        assert _point(s, 1).result_cf() is not None
    finally:
        s.close()
    model = mx.read_model(_sec_inputs(tmp_path / "sec", _committed(), FAR_KEYS),
                          name=_name("far"))
    try:
        data = model.Data
        assert 1e10 in set(pd.read_csv(data.input_dir() / "rate_scenario.csv")["t"])
        assert data.read_last_mth == 1321
        assert data.scenario_last_mth() == data.wd_last_mth() == 1321
        for array in (data.mva_ref_yield_array(), data.market_rate_array(),
                      data.wd_amount_array()):
            assert array.shape[1] == 1322, array.shape
        assert 777.0 not in data.wd_amount_array() and 0.5 not in data.market_rate_array()
        for key in point_keys(model):
            mine, theirs = projection(model, key), projection(sec_model, key)
            for report in REPORTS:
                assert mine.cells[report]().equals(theirs.cells[report]()), (key, report)
            _release(model, key)
    finally:
        model.close()


# run_sec.py run as though it sat at /m/products/fixed_deferred_annuity, a copy too
# shallow to have a repository above it: the source compiled under that name, so that its
# own __file__ is it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/fixed_deferred_annuity/run_sec.py"
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
    the longest frame, issue age 0, needs a limit of 2,444 in the export, and the reports
    the sample runs in ascending ``t``, the export's import among the frames they run
    under, 128.  The limit is four times the first, rounded up to the thousand.  No build
    can tell a lower limit above the reports' need: a limit of 2,000 builds the same
    model.  So this holds the limit, read from the sample's code, to the value derived
    from its comment's need, and holds the call before the import of the export.  A
    change to the need is measured again and written in the comment.
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


# The codes, each family in its numbering's order: the timings, the count's five and the
# account value's three, one numbering; the kinds and their total; the scenario's columns;
# and the surrender-charge schedules.
TIMING_CODES = ("BEF_NB", "BEF_DECR", "BEF_MORT", "BEF_LAPSE", "AFT_DECR", "BEF_WD",
                "BEF_INV", "EOM")
KIND_CODES = ("DEATH", "LAPSE", "ANNUITIZATION", "MATURITY", "ALL")
NAME_CODES = ("MVA_REF_YIELD", "MARKET_RATE")
SCHEDULE_CODES = ("NONE", "INITIAL", "RENEWAL")


def test_the_spec_sizes_each_cache_as_its_comment_derives():
    """``spec_sec.py`` gives each cache the size its comment derives from the contract.

    The spec check, C3, holds the compiled caches to the spec, and C4 at the contract's
    extremes holds the spec to the largest argument a projection reads; neither sees a
    size one above the comment's, which only adds headroom, and C4 sees one below only on
    a point that reaches it.  So this reads the spec as mx2cy does, and the bounds of the
    contract from the model's own References, and holds each size to the comment's
    derivation from them: ``t`` to ``12 * (maturity_age - issue_age_min) + the horizon +
    2``, ``y`` to ``maturity_age - issue_age_min + 2`` and ``a`` to ``maturity_age + 1``;
    every 2-D cache to ``(t, width)``, one width, the widest of the timings' count, the
    kinds' and the scenario columns' (§7.2, *For M16 and later*, item 16); each family
    of codes dense from 0; and ``Data.read_last_mth``, the last month the scenario and
    withdrawal arrays hold, to the last ``t``.  A change to a bound or a size is derived
    again in the comment and here.
    """
    source = (model_path(SEC).parent / "spec_sec.py").read_text(encoding="utf-8")
    comment = " ".join(line.lstrip("# ") for line in source.splitlines()
                       if line.startswith("#"))
    for formula in ("needs t raised to 12 * (maturity_age - issue_age_min) + the horizon "
                    "+ 2", "needs y raised to maturity_age - issue_age_min + 2",
                    "needs a raised to maturity_age + 1"):
        assert formula in comment, formula
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    proj, data = _references("Projection"), _references("Data")
    low, top, horizon = (proj["issue_age_min"], proj["maturity_age"],
                         data["future_horizon_mth"])
    families = [[proj[code] for code in family]
                for family in (TIMING_CODES, KIND_CODES, NAME_CODES, SCHEDULE_CODES)]
    for family in families:
        assert family == list(range(len(family))), family
    t = 12 * (top - low) + horizon + 2
    width = max(len(family) for family in families[:3])
    assert sizes == {"t": t, ("t", "timing"): (t, width), ("t", "kind"): (t, width),
                     ("t", "name"): (t, width), "y": top - low + 2, "a": top + 1}, sizes
    assert data["read_last_mth"] == t - 1 == 1321
    assert "Data.read_last_mth" in comment and "is the last t, 1,321" in comment


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
    exactly.  ``python tools/gen_sec_fingerprint.py MYGA_US_SEC --check`` runs the same
    comparison from the command line.
    """
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# MYGA_US_SEC's fingerprint, frozen at M13 from the model as Phase 1 left it and committed
# alone, before Phase 2 changed anything.  Each point is keyed by its point_id; each column
# holds (its sum over the frame, its largest absolute value, (its values at the months)).
# The block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a
# refreeze goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: MYGA_US_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 480, "months": (0, 119, 239, 359, 479),
        "result_cf": {
            "pols_if": (66.8595111187876, 1.0, (
                1.0, 0.08096076322939195, 0.0005597324760138211, 2.4642251005282056e-06,
                3.0118716619398657e-09)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (3928.294749999998, 3928.294749999998, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (4707.2210197146305, 81.56075344370839, (
                46.07426478061503, 13.65900488282683, 0.40810622601464314,
                0.00782181827883033, 4.1536506698748663e-05)),
            "claims_lapse": (112522.88008859924, 18812.27725669592, (
                91.84125528145942, 12.47935208564064, 0.13307456594698516,
                0.0009002433676992364, 1.6880745714159825e-06)),
            "claims_annuitization": (1219.5153536729047, 1085.2386771418999, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0016095580174365265, 0.0016095580174365265, (
                0.0, 0.0, 0.0, 0.0, 0.0016095580174365265)),
            "commissions": (2000.0, 2000.0, (
                2000.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (297.7353941274238, 4.27907235661803, (
                4.166666666666667, 0.4212870800662007, 0.003728401777889009,
                2.1011701944827316e-05, 3.28742588835212e-08)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-24675.648215672267, 97857.91781327125, (
                97857.91781327125, -26.55964404853367, -0.5449091937395173,
                -0.008743073348474392, -0.0016528154729655747)),
        },
        "result_pols": {
            "pols_if": (66.8595111187876, 1.0, (
                1.0, 0.08096076322939195, 0.0005597324760138211, 2.4642251005282056e-06,
                3.0118716619398657e-09)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_annuitization": (0.009960081010576393, 0.009076983478531697, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.04105291560669626, 0.0006797071008948576, (
                0.00045907401398581626, 9.189526200906856e-05, 1.7764902868012336e-06,
                2.2029918764323746e-08, 7.569212524371312e-11)),
            "pols_lapse": (0.9489870004496239, 0.156776855233495, (
                0.0010472016836012025, 8.472490969074303e-05, 5.84560804303554e-07,
                2.5586455136922192e-09, 3.0761843504811453e-12)),
            "pols_maturity": (2.9331033523456716e-09, 2.9331033523456716e-09, (
                0.0, 0.0, 0.0, 0.0, 2.9331033523456716e-09)),
            "pols_if_aft_decr": (65.85951112172069, 0.998493724302413, (
                0.998493724302413, 0.08078414305769215, 0.0005573714249227162,
                2.4396365362501897e-06, 2.9331033523456716e-09)),
        },
    },
    2: {"rows": 480, "months": (0, 119, 239, 359, 479),
        "result_cf": {
            "pols_if": (66.8595111187876, 1.0, (
                1.0, 0.08096076322939195, 0.0005597324760138211, 2.4642251005282056e-06,
                3.0118716619398657e-09)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (4872.390875687495, 84.80856841409002, (
                46.07426478061503, 14.202917471490926, 0.4243573450197068,
                0.008133289389983376, 4.3190523889341025e-05)),
            "claims_lapse": (116827.11601709104, 19561.397306738567, (
                91.84125528145942, 12.976289948682588, 0.13837370247050892,
                0.0009360917845314635, 1.755295062064706e-06)),
            "claims_annuitization": (1268.0774384383765, 1128.4537563710448, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0016736519155922899, 0.0016736519155922899, (
                0.0, 0.0, 0.0, 0.0, 0.0016736519155922899)),
            "commissions": (2000.0, 2000.0, (
                2000.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (297.7353941274238, 4.27907235661803, (
                4.166666666666667, 0.4212870800662007, 0.003728401777889009,
                2.1011701944827316e-05, 3.28742588835212e-08)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-25265.32139899628, 97857.91781327125, (
                97857.91781327125, -27.600494500239712, -0.5664594492681048,
                -0.009090392876459666, -0.0017186306088025792)),
        },
        "result_pols": {
            "pols_if": (66.8595111187876, 1.0, (
                1.0, 0.08096076322939195, 0.0005597324760138211, 2.4642251005282056e-06,
                3.0118716619398657e-09)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_annuitization": (0.009960081010576393, 0.009076983478531697, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.04105291560669626, 0.0006797071008948576, (
                0.00045907401398581626, 9.189526200906856e-05, 1.7764902868012336e-06,
                2.2029918764323746e-08, 7.569212524371312e-11)),
            "pols_lapse": (0.9489870004496239, 0.156776855233495, (
                0.0010472016836012025, 8.472490969074303e-05, 5.84560804303554e-07,
                2.5586455136922192e-09, 3.0761843504811453e-12)),
            "pols_maturity": (2.9331033523456716e-09, 2.9331033523456716e-09, (
                0.0, 0.0, 0.0, 0.0, 2.9331033523456716e-09)),
            "pols_if_aft_decr": (65.85951112172069, 0.998493724302413, (
                0.998493724302413, 0.08078414305769215, 0.0005573714249227162,
                2.4396365362501897e-06, 2.9331033523456716e-09)),
        },
    },
    3: {"rows": 480, "months": (0, 119, 239, 359, 479),
        "result_cf": {
            "pols_if": (74.26169744942888, 1.0, (
                1.0, 0.06267751304574128, 0.033362441568380044, 0.011308313910841347,
                0.0010641285598625447)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (14564.052675913428, 84.80856841409002, (
                46.07426478061503, 10.995493490898566, 25.29350669119166, 37.32361525330328,
                15.259703979707927)),
            "claims_lapse": (117554.49313754628, 19561.397306738567, (
                96.22536932069687, 30.77051284513463, 25.262592300218902,
                13.157789787622614, 1.882390760977174)),
            "claims_annuitization": (1128.4537563710448, 1128.4537563710448, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (590.0580576938073, 590.0580576938073, (
                0.0, 0.0, 0.0, 0.0, 590.0580576938073)),
            "commissions": (2000.0, 2000.0, (
                2000.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (348.4090072333657, 4.27907235661803, (
                4.166666666666667, 0.3261484378801583, 0.22222863919583413,
                0.09642257168073322, 0.011614850062946783)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-36185.46663475791, 97853.53369923202, (
                97853.53369923202, -42.09215477391335, -50.7783276306064,
                -50.577827612606626, -607.2117672845554)),
        },
        "result_pols": {
            "pols_if": (74.26169744942888, 1.0, (
                1.0, 0.06267751304574128, 0.033362441568380044, 0.011308313910841347,
                0.0010641285598625447)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_annuitization": (0.009076983478531697, 0.009076983478531697, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.07245246529352063, 0.0006797071008948576, (
                0.00045907401398581626, 7.114269003487092e-05, 0.00010588639382206831,
                0.00010109516243621901, 2.674288989347248e-05)),
            "pols_lapse": (0.9174364644796958, 0.156776855233495, (
                0.0010472016836012025, 0.00019909038729070552, 0.00010575697667887517,
                3.5639336834167074e-05, 3.2989217172393645e-06)),
            "pols_maturity": (0.001034086748251833, 0.001034086748251833, (
                0.0, 0.0, 0.0, 0.0, 0.001034086748251833)),
            "pols_if_aft_decr": (73.26273153617716, 0.998493724302413, (
                0.998493724302413, 0.0624072799684157, 0.0331507981978791,
                0.01117157941157096, 0.001034086748251833)),
        },
    },
    4: {"rows": 480, "months": (0, 119, 239, 359, 479),
        "result_cf": {
            "pols_if": (66.8595111187876, 1.0, (
                1.0, 0.08096076322939195, 0.0005597324760138211, 2.4642251005282056e-06,
                3.0118716619398657e-09)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (4872.390875687495, 84.80856841409002, (
                46.07426478061503, 14.202917471490926, 0.4243573450197068,
                0.008133289389983376, 4.3190523889341025e-05)),
            "claims_lapse": (115330.30200584415, 19561.397306738567, (
                91.84125528145942, 12.963753136678703, 0.13824001517614243,
                0.0009351873960839591, 1.755295062064706e-06)),
            "claims_annuitization": (1268.0774384383765, 1128.4537563710448, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0016736519155922899, 0.0016736519155922899, (
                0.0, 0.0, 0.0, 0.0, 0.0016736519155922899)),
            "commissions": (2000.0, 2000.0, (
                2000.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (297.7353941274238, 4.27907235661803, (
                4.166666666666667, 0.4212870800662007, 0.003728401777889009,
                2.1011701944827316e-05, 3.28742588835212e-08)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-23768.507387749396, 97857.91781327125, (
                97857.91781327125, -27.58795768823583, -0.5663257619737382,
                -0.009089488488012162, -0.0017186306088025792)),
        },
        "result_pols": {
            "pols_if": (66.8595111187876, 1.0, (
                1.0, 0.08096076322939195, 0.0005597324760138211, 2.4642251005282056e-06,
                3.0118716619398657e-09)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_annuitization": (0.009960081010576393, 0.009076983478531697, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.04105291560669626, 0.0006797071008948576, (
                0.00045907401398581626, 9.189526200906856e-05, 1.7764902868012336e-06,
                2.2029918764323746e-08, 7.569212524371312e-11)),
            "pols_lapse": (0.9489870004496239, 0.156776855233495, (
                0.0010472016836012025, 8.472490969074303e-05, 5.84560804303554e-07,
                2.5586455136922192e-09, 3.0761843504811453e-12)),
            "pols_maturity": (2.9331033523456716e-09, 2.9331033523456716e-09, (
                0.0, 0.0, 0.0, 0.0, 2.9331033523456716e-09)),
            "pols_if_aft_decr": (65.85951112172069, 0.998493724302413, (
                0.998493724302413, 0.08078414305769215, 0.0005573714249227162,
                2.4396365362501897e-06, 2.9331033523456716e-09)),
        },
    },
    5: {"rows": 480, "months": (0, 119, 239, 359, 479),
        "result_cf": {
            "pols_if": (66.8595111187876, 1.0, (
                1.0, 0.08096076322939195, 0.0005597324760138211, 2.4642251005282056e-06,
                3.0118716619398657e-09)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (17068.79416613149, 17068.79416613149, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (4263.35491096676, 69.54084369679913, (
                46.07426478061503, 11.646026838950801, 0.3479621028091926,
                0.006669088003561908, 3.541511815535524e-05)),
            "claims_lapse": (96073.53954236677, 16039.842412584487, (
                95.26109606216296, 10.634323617106856, 0.11339995776820963,
                0.0007671455409358565, 1.4392967813913133e-06)),
            "claims_annuitization": (1039.79086772593, 925.3030414062164, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0013723515022299934, 0.0013723515022299934, (
                0.0, 0.0, 0.0, 0.0, 0.0013723515022299934)),
            "commissions": (2000.0, 2000.0, (
                2000.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (297.7353941274238, 4.27907235661803, (
                4.166666666666667, 0.4212870800662007, 0.003728401777889009,
                2.1011701944827316e-05, 3.28742588835212e-08)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-20743.216253669867, 97854.49797249056, (
                97854.49797249056, -22.701637536123858, -0.4650904623552913,
                -0.0074572452464425915, -0.0014092387914256235)),
        },
        "result_pols": {
            "pols_if": (66.8595111187876, 1.0, (
                1.0, 0.08096076322939195, 0.0005597324760138211, 2.4642251005282056e-06,
                3.0118716619398657e-09)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_annuitization": (0.009960081010576393, 0.009076983478531697, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.04105291560669626, 0.0006797071008948576, (
                0.00045907401398581626, 9.189526200906856e-05, 1.7764902868012336e-06,
                2.2029918764323746e-08, 7.569212524371312e-11)),
            "pols_lapse": (0.9489870004496239, 0.156776855233495, (
                0.0010472016836012025, 8.472490969074303e-05, 5.84560804303554e-07,
                2.5586455136922192e-09, 3.0761843504811453e-12)),
            "pols_maturity": (2.9331033523456716e-09, 2.9331033523456716e-09, (
                0.0, 0.0, 0.0, 0.0, 2.9331033523456716e-09)),
            "pols_if_aft_decr": (65.85951112172069, 0.998493724302413, (
                0.998493724302413, 0.08078414305769215, 0.0005573714249227162,
                2.4396365362501897e-06, 2.9331033523456716e-09)),
        },
    },
    6: {"rows": 480, "months": (0, 119, 239, 359, 479),
        "result_cf": {
            "pols_if": (66.8595111187876, 1.0, (
                1.0, 0.08096076322939195, 0.0005597324760138211, 2.4642251005282056e-06,
                3.0118716619398657e-09)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (4872.390875687495, 84.80856841409002, (
                46.07426478061503, 14.202917471490926, 0.4243573450197068,
                0.008133289389983376, 4.3190523889341025e-05)),
            "claims_lapse": (116763.59665074722, 19561.397306738567, (
                91.84125528145942, 12.976289948682588, 0.13837370247050892,
                0.0009360917845314635, 1.755295062064706e-06)),
            "claims_annuitization": (1268.0774384383765, 1128.4537563710448, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0016736519155922899, 0.0016736519155922899, (
                0.0, 0.0, 0.0, 0.0, 0.0016736519155922899)),
            "commissions": (2000.0, 2000.0, (
                2000.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (297.7353941274238, 4.27907235661803, (
                4.166666666666667, 0.4212870800662007, 0.003728401777889009,
                2.1011701944827316e-05, 3.28742588835212e-08)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-25201.802032652482, 97857.91781327125, (
                97857.91781327125, -27.600494500239712, -0.5664594492681048,
                -0.009090392876459666, -0.0017186306088025792)),
        },
        "result_pols": {
            "pols_if": (66.8595111187876, 1.0, (
                1.0, 0.08096076322939195, 0.0005597324760138211, 2.4642251005282056e-06,
                3.0118716619398657e-09)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_annuitization": (0.009960081010576393, 0.009076983478531697, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.04105291560669626, 0.0006797071008948576, (
                0.00045907401398581626, 9.189526200906856e-05, 1.7764902868012336e-06,
                2.2029918764323746e-08, 7.569212524371312e-11)),
            "pols_lapse": (0.9489870004496239, 0.156776855233495, (
                0.0010472016836012025, 8.472490969074303e-05, 5.84560804303554e-07,
                2.5586455136922192e-09, 3.0761843504811453e-12)),
            "pols_maturity": (2.9331033523456716e-09, 2.9331033523456716e-09, (
                0.0, 0.0, 0.0, 0.0, 2.9331033523456716e-09)),
            "pols_if_aft_decr": (65.85951112172069, 0.998493724302413, (
                0.998493724302413, 0.08078414305769215, 0.0005573714249227162,
                2.4396365362501897e-06, 2.9331033523456716e-09)),
        },
    },
    7: {"rows": 480, "months": (0, 119, 239, 359, 479),
        "result_cf": {
            "pols_if": (66.85511257544857, 1.0, (
                1.0, 0.08094962301349186, 0.0005596554567222492, 2.463886022701474e-06,
                3.0114572278456314e-09)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (4929.738155992021, 84.90105513124581, (
                46.07426478061503, 15.28638893150808, 0.5292163762879135,
                0.011752817320786936, 7.231667370882223e-05)),
            "claims_lapse": (118658.46216395259, 19582.729696303813, (
                91.97285491771423, 13.965990657970874, 0.17256351447605642,
                0.0013526581664411678, 2.939003485840258e-06)),
            "claims_annuitization": (1279.9308965881955, 1128.2984809267712, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0028023031114911426, 0.0028023031114911426, (
                0.0, 0.0, 0.0, 0.0, 0.0028023031114911426)),
            "commissions": (2000.0, 2000.0, (
                2000.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (297.7151161159343, 4.278483555475314, (
                4.166666666666667, 0.4212291108865555, 0.0037278887491191334,
                2.1008810730777975e-05, 3.286973537945687e-08)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-27165.84913495185, 97857.786213635, (
                97857.786213635, -29.673608700365513, -0.7055077795130891,
                -0.013126484297958882, -0.0028775916584211844)),
        },
        "result_pols": {
            "pols_if": (66.85511257544857, 1.0, (
                1.0, 0.08094962301349186, 0.0005596554567222492, 2.463886022701474e-06,
                3.0114572278456314e-09)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_annuitization": (0.009958710501598786, 0.009075734483936804, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.041049804979467995, 0.0006796135730728519, (
                0.00045907401398581626, 9.188261720412674e-05, 1.7762458414112711e-06,
                2.2026887443452906e-08, 7.568170999336814e-11)),
            "pols_lapse": (0.9489914815862336, 0.156755282709401, (
                0.0010487022223321357, 8.471325152759804e-05, 5.844803686294464e-07,
                2.5582934435992828e-09, 3.0757610669491477e-12)),
            "pols_maturity": (2.9326997567853137e-09, 2.9326997567853137e-09, (
                0.0, 0.0, 0.0, 0.0, 2.9326997567853137e-09)),
            "pols_if_aft_decr": (65.85511257838127, 0.9984922237636821, (
                0.9984922237636821, 0.08077302714476013, 0.0005572947305122085,
                2.439300841814422e-06, 2.9326997567853137e-09)),
        },
    },
    8: {"rows": 468, "months": (0, 116, 233, 350, 467),
        "result_cf": {
            "pols_if": (54.958427851815024, 0.9820736874999996, (
                0.9820736874999996, 0.017057842293690405, 0.00020770983354851584,
                1.6130135021140294e-06, 3.0118716619398657e-09)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (3928.294749999998, 3928.294749999998, (
                3928.294749999998, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (4147.828008118528, 81.56075344370839, (
                50.179870727442115, 3.293218730384871, 0.171638029800507,
                0.005740945196115319, 4.1536506698748663e-05)),
            "claims_lapse": (111415.51263155772, 18812.27725669592, (
                90.21079742472097, 436.16337460831653, 8.101746740411262,
                0.09557508609326262, 1.6880745714159825e-06)),
            "claims_annuitization": (1219.5153536729047, 1085.2386771418999, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0016095580174365265, 0.0016095580174365265, (
                0.0, 0.0, 0.0, 0.0, 0.0016095580174365265)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (242.09516798215097, 4.174704738163932, (
                4.091973697916665, 0.08876211494915456, 0.0013835640165145505,
                1.3753678157136418e-05, 3.20724476912402e-08)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-120953.2475208893, 19983.251392019694, (
                -4072.777391850078, -439.54535545365053, -8.274768334228282,
                -0.10132978496753507, -0.0016528146711543823)),
        },
        "result_pols": {
            "pols_if": (54.958427851815024, 0.9820736874999996, (
                0.9820736874999996, 0.017057842293690405, 0.00020770983354851584,
                1.6130135021140294e-06, 3.0118716619398657e-09)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_annuitization": (0.009960081010576393, 0.009076983478531697, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.035589437540547726, 0.0006797071008948576, (
                0.0004977415471321419, 2.1444370579855675e-05, 7.310530872010167e-07,
                1.5994161012021346e-08, 7.569212524371312e-11)),
            "pols_lapse": (0.936524166015772, 0.156776855233495, (
                0.0010283800857581577, 0.0029744837754837254, 3.613762880687522e-05,
                2.788328930024375e-07, 3.0761843504811453e-12)),
            "pols_maturity": (2.9331033523456716e-09, 2.9331033523456716e-09, (
                0.0, 0.0, 0.0, 0.0, 2.9331033523456716e-09)),
            "pols_if_aft_decr": (53.97635416724812, 0.9805475658671093, (
                0.9805475658671093, 0.014061914147626822, 0.0001708411516544396,
                1.3181864480995705e-06, 2.9331033523456716e-09)),
        },
    },
    9: {"rows": 450, "months": (0, 112, 224, 336, 449),
        "result_cf": {
            "pols_if": (37.513436075098525, 0.9546596989821345, (
                0.9546596989821345, 0.007687783840336947, 5.2371821987197326e-05,
                7.194379809088407e-07, 3.0118716619398657e-09)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (2725.0746315223773, 69.54084369679913, (
                49.037847741518476, 1.4747975028612765, 0.042278980565509626,
                0.0022151355192442566, 3.541511815535524e-05)),
            "claims_lapse": (93257.80638213185, 16039.842412584487, (
                78.8824954637798, 1.06552332588136, 0.010870932619142399,
                0.036766714089249704, 1.4392967813913133e-06)),
            "claims_annuitization": (1039.79086772593, 925.3030414062164, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0013723515022299934, 0.0013723515022299934, (
                0.0, 0.0, 0.0, 0.0, 0.0013723515022299934)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (162.81723003599046, 4.015061254609861, (
                3.9777487457588943, 0.04000411899649528, 0.00034034236968543926,
                5.984809771621835e-06, 3.129019286950264e-08)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-97185.49048376761, 17038.65984175714, (
                -131.89809195105718, -2.580324947739132, -0.053490255554337465,
                -0.03898783441826559, -0.0014092372073596096)),
        },
        "result_pols": {
            "pols_if": (37.513436075098525, 0.9546596989821345, (
                0.9546596989821345, 0.007687783840336947, 5.2371821987197326e-05,
                7.194379809088407e-07, 3.0118716619398657e-09)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_annuitization": (0.009960081010576393, 0.009076983478531697, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.02644268129477285, 0.0006797071008948576, (
                0.0005344220433947771, 1.0705489808324539e-05, 2.0441833291203445e-07,
                7.133732538344295e-09, 7.569212524371312e-11)),
            "pols_lapse": (0.9182569337436818, 0.156776855233495, (
                0.0009996204961703512, 8.043141771189873e-06, 5.465488357265671e-08,
                1.243653405812986e-07, 3.0761843504811453e-12)),
            "pols_maturity": (2.9331033523456716e-09, 2.9331033523456716e-09, (
                0.0, 0.0, 0.0, 0.0, 2.9331033523456716e-09)),
            "pols_if_aft_decr": (36.5587763790495, 0.9531256564425694, (
                0.9531256564425694, 0.007669035208757433, 5.2112748770712634e-05,
                5.879389077891979e-07, 2.9331033523456716e-09)),
        },
    },
    10: {"rows": 450, "months": (0, 112, 224, 336, 449),
        "result_cf": {
            "pols_if": (44.91562240573983, 0.9546596989821345, (
                0.9546596989821345, 0.0565191385600252, 0.030154800222476907,
                0.010323999724259387, 0.0010641285598625447)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (13015.027840025712, 84.80856841409002, (
                59.80413011954476, 13.222894738229172, 29.688144587453213,
                38.76633108611194, 15.259703979707927)),
            "claims_lapse": (114711.58938147245, 19561.397306738567, (
                93.93456276052434, 30.154194842347636, 24.093184276301972,
                12.309351632984047, 1.882390760977174)),
            "claims_annuitization": (1128.4537563710448, 1128.4537563710448, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (590.0580576938073, 590.0580576938073, (
                0.0, 0.0, 0.0, 0.0, 590.0580576938073)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (210.45741566448817, 4.015061254609861, (
                3.9777487457588943, 0.2941027468373195, 0.1959633210320171,
                0.08588255842972753, 0.011055181499532931)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-129655.5864512275, 20778.63317559334, (
                -157.716441625828, -43.671192327414126, -53.9772921847872,
                -51.16156527752572, -607.211207615992)),
        },
        "result_pols": {
            "pols_if": (44.91562240573983, 0.9546596989821345, (
                0.9546596989821345, 0.0565191385600252, 0.030154800222476907,
                0.010323999724259387, 0.0010641285598625447)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_annuitization": (0.009076983478531697, 0.009076983478531697, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.05784223098159723, 0.0006797071008948576, (
                0.0005344220433947771, 7.870474435752515e-05, 0.00011770058319302042,
                0.00010236970345347763, 2.674288989347248e-05)),
            "pols_lapse": (0.8867063977737538, 0.156776855233495, (
                0.0009996204961703512, 0.00017948249935866966, 9.551899856672446e-05,
                3.250513115554004e-05, 3.2989217172393645e-06)),
            "pols_maturity": (0.001034086748251833, 0.001034086748251833, (
                0.0, 0.0, 0.0, 0.0, 0.001034086748251833)),
            "pols_if_aft_decr": (43.96199679350595, 0.9531256564425694, (
                0.9531256564425694, 0.05626095131630901, 0.029941580640717162,
                0.01018912488965037, 0.001034086748251833)),
        },
    },
    11: {"rows": 420, "months": (0, 104, 209, 314, 419),
        "result_cf": {
            "pols_if": (9.5499785887727, 0.9076983478531697, (
                0.9076983478531697, 0.00725409583421611, 4.851364497805438e-05,
                2.0917536805200732e-07, 3.0118716619398657e-09)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (1233.0925590536413, 84.80856841409, (
                84.80856841409, 2.2568543606125426, 0.055935085269708244,
                0.0008968097648583628, 4.3190523889341025e-05)),
            "claims_lapse": (109477.74219082606, 19561.397306738567, (
                19561.397306738567, 1.3490544585831996, 0.012998104999714542,
                8.03981055085476e-05, 1.755295062064706e-06)),
            "claims_annuitization": (1268.0774384383762, 1128.4537563710446, (
                1128.4537563710446, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0016736519155922899, 0.0016736519155922899, (
                0.0, 0.0, 0.0, 0.0, 0.0016736519155922899)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (41.49096799829576, 3.7820764493882075, (
                3.7820764493882075, 0.03682671409676471, 0.00030758020047862123,
                1.656226771217677e-06, 2.9056054666185477e-08)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-112020.40482996825, 20778.44170797309, (
                -20778.44170797309, -3.642735533292507, -0.0692407704699014,
                -0.0009788640971381281, -0.001718626790598362)),
        },
        "result_pols": {
            "pols_if": (9.5499785887727, 0.9076983478531697, (
                0.9076983478531697, 0.00725409583421611, 4.851364497805438e-05,
                2.0917536805200732e-07, 3.0118716619398657e-09)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_annuitization": (0.009960081010576393, 0.009076983478531697, (
                0.009076983478531697, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.008759633115031818, 0.0006797071008948576, (
                0.0006797071008948576, 1.2402591071791859e-05, 2.100120950234593e-07,
                2.300442823398254e-09, 7.569212524371312e-11)),
            "pols_lapse": (0.8889786307944583, 0.156776855233495, (
                0.156776855233495, 7.58699634921231e-06, 5.060687798177476e-08,
                2.1673926936064605e-10, 3.0761843504811453e-12)),
            "pols_maturity": (2.9331033523456716e-09, 2.9331033523456716e-09, (
                0.0, 0.0, 0.0, 0.0, 2.9331033523456716e-09)),
            "pols_if_aft_decr": (8.642280243852634, 0.7411648020402483, (
                0.7411648020402483, 0.007234106246795105, 4.825302600504914e-05,
                2.0665818595924843e-07, 2.9331033523456716e-09)),
        },
    },
    12: {"rows": 419, "months": (0, 104, 209, 313, 418),
        "result_cf": {
            "pols_if": (8.64228024091953, 0.7411648020402483, (
                0.7411648020402483, 0.007234106246795105, 4.825302600504914e-05,
                2.0917536805200732e-07, 3.0118716619398657e-09)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (1148.2839906395511, 70.2026462434004, (
                70.2026462434004, 2.2588158782372, 0.05583681737495244,
                0.0008968097648583628, 4.3190523889341025e-05)),
            "claims_lapse": (91326.82529596993, 15463.24212229047, (
                15463.24212229047, 1.3568075526085042, 0.013090768831675271,
                8.144867340794163e-05, 1.755295062064706e-06)),
            "claims_annuitization": (139.62368206733157, 124.85633010549458, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0016736519155922899, 0.0016736519155922899, (
                0.0, 0.0, 0.0, 0.0, 0.0016736519155922899)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (37.65737315484715, 3.088186675167701, (
                3.088186675167701, 0.036725233383290624, 0.00030592785635972966,
                1.656226771217677e-06, 2.9056054666185477e-08)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-92652.39201548357, 15536.532955209039, (
                -15536.532955209039, -3.652348664228995, -0.06923351406298744,
                -0.0009799146650375221, -0.001718626790598362)),
        },
        "result_pols": {
            "pols_if": (8.64228024091953, 0.7411648020402483, (
                0.7411648020402483, 0.007234106246795105, 4.825302600504914e-05,
                2.0917536805200732e-07, 3.0118716619398657e-09)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_annuitization": (0.0008830975320446957, 0.0008078414305769215, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.00807992601413696, 0.0005606087267140277, (
                0.0005606087267140277, 1.2368414148279606e-05, 2.0888389415237548e-07,
                2.300442823398254e-09, 7.569212524371312e-11)),
            "pols_lapse": (0.7322017755609633, 0.1293063925254985, (
                0.1293063925254985, 7.566089411910756e-06, 5.033501400262874e-08,
                2.1673926936064605e-10, 3.0761843504811453e-12)),
            "pols_maturity": (2.9331033523456716e-09, 2.9331033523456716e-09, (
                0.0, 0.0, 0.0, 0.0, 2.9331033523456716e-09)),
            "pols_if_aft_decr": (7.901115441812386, 0.6112978007880358, (
                0.6112978007880358, 0.007214171743234915, 4.799380709689413e-05,
                2.0665818595924843e-07, 2.9331033523456716e-09)),
        },
    },
    13: {"rows": 1, "months": (0,),
        "result_cf": {
            "pols_if": (0.0010641285598625447, 0.0010641285598625447, (
                0.0010641285598625447,)),
            "premiums": (0.0, 0.0, (
                0.0,)),
            "withdrawals": (0.0, 0.0, (
                0.0,)),
            "claims_death": (15.259703979707927, 15.259703979707927, (
                15.259703979707927,)),
            "claims_lapse": (1.882390760977174, 1.882390760977174, (
                1.882390760977174,)),
            "claims_annuitization": (0.0, 0.0, (
                0.0,)),
            "claims_maturity": (590.0580576938073, 590.0580576938073, (
                590.0580576938073,)),
            "commissions": (0.0, 0.0, (
                0.0,)),
            "expenses": (0.00443386899942727, 0.00443386899942727, (
                0.00443386899942727,)),
            "premium_taxes": (0.0, 0.0, (
                0.0,)),
            "net_cf": (-607.2045863034919, 607.2045863034919, (
                -607.2045863034919,)),
        },
        "result_pols": {
            "pols_if": (0.0010641285598625447, 0.0010641285598625447, (
                0.0010641285598625447,)),
            "pols_new_biz": (0.0, 0.0, (
                0.0,)),
            "pols_annuitization": (0.0, 0.0, (
                0.0,)),
            "pols_death": (2.674288989347248e-05, 2.674288989347248e-05, (
                2.674288989347248e-05,)),
            "pols_lapse": (3.2989217172393645e-06, 3.2989217172393645e-06, (
                3.2989217172393645e-06,)),
            "pols_maturity": (0.001034086748251833, 0.001034086748251833, (
                0.001034086748251833,)),
            "pols_if_aft_decr": (0.001034086748251833, 0.001034086748251833, (
                0.001034086748251833,)),
        },
    },
    14: {"rows": 495, "months": (0, 123, 247, 370, 494),
        "result_cf": {
            "pols_if": (66.85951111878761, 1.0, (
                0.0, 0.08292925757760036, 0.0005765422614039996, 2.5650826890191205e-06,
                3.0118716619398657e-09)),
            "premiums": (100000.0, 100000.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (3928.294749999998, 3928.294749999998, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (4707.22101971463, 81.56075344370839, (
                0.0, 13.443721386041036, 0.4098207427364488, 0.008024646313580807,
                4.1536506698748663e-05)),
            "claims_lapse": (112522.88008859925, 18812.27725669592, (
                0.0, 12.283144613235022, 0.1336369535551048, 0.0009236006762619381,
                1.6880745714159825e-06)),
            "claims_annuitization": (1219.5153536729047, 1085.2386771418999, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0016095580174365265, 0.0016095580174365265, (
                0.0, 0.0, 0.0, 0.0, 0.0016095580174365265)),
            "commissions": (2000.0, 2000.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (306.9711105671617, 4.408903225535521, (
                0.0, 0.44231858702818677, 0.003936381783578315, 2.2418476192293474e-05,
                3.4538518239499454e-08)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-24684.883932111978, 97857.8136466046, (
                0.0, -26.169184586304244, -0.547394078075132, -0.00897066546603504,
                -0.0016528171372249306)),
        },
        "result_pols": {
            "pols_if": (66.85951111878761, 1.0, (
                0.0, 0.08292925757760036, 0.0005765422614039996, 2.5650826890191205e-06,
                3.0118716619398657e-09)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_annuitization": (0.009960081010576393, 0.009076983478531697, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.04105291560669626, 0.0006797071008948576, (
                0.0, 9.412961969884773e-05, 1.8298415246667457e-06, 2.293157522450029e-08,
                7.569212524371312e-11)),
            "pols_lapse": (0.9489870004496238, 0.156776855233495, (
                0.0, 8.678492616324272e-05, 6.021162295985663e-07, 2.6633676091934708e-09,
                3.0761843504811453e-12)),
            "pols_maturity": (2.9331033523456716e-09, 2.9331033523456716e-09, (
                0.0, 0.0, 0.0, 0.0, 2.9331033523456716e-09)),
            "pols_if_aft_decr": (65.85951112172069, 0.998493724302413, (
                0.0, 0.08274834303173828, 0.0005741103036497342, 2.5394877461854267e-06,
                2.9331033523456716e-09)),
        },
    },
}
# END generated fingerprint: MYGA_US_SEC


# ---------------------------------------------------------------------------
# Compiled (USLIB-SEC-PLAN.md Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython CI job, which sets USLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is MYGA's
# own: the comparison on the splice grid, at the contract's extremes, where the caps bind,
# on labels that are not text and on keys written as floats, the refusals, the deepest
# call, a Reference set late and the runner.  Each comparison adds _myga_c4_also's calls,
# the codes and the cells no swept cell reaches.  None asks for sec_read, sec_model or
# s_model, which sweep every committed point; the grid test alone asks for spliced.


def _myga_c4_also(proj):
    """What C4 compares of a ``MYGA_US_SEC`` point beyond its full sweep (M20).

    ``sec_support.full_sweep`` reaches a cell of more than ``t`` only at the keys some
    swept cell asks of it, and an engine cell at none.  So, as ``sample_sec.py`` does, this
    calls ``av_pp_at`` at ``EOM``, ``av_at`` at ``BEF_WD`` and ``claims_over_av`` at every
    kind and ``ALL``, at ``t = 0 .. proj_len()``, and the three engine cells at the
    arguments this module sweeps ``MYGA_US_S``'s at: the statutory rate at CMT levels
    either side of its 15 bp floor, at it and at its 3% cap, and the term rounded up from
    a fraction of a year.  Passed to ``sec_support.compiled_mismatches`` as ``also``; it
    lives here, as M18's module keeps its own, so that the shared module holds only shared
    machinery.
    """
    kinds = (proj.DEATH, proj.LAPSE, proj.ANNUITIZATION, proj.MATURITY, proj.ALL)
    for t in range(proj.proj_len() + 1):
        proj.av_pp_at(t, proj.EOM)
        proj.av_at(t, proj.BEF_WD)
        for kind in kinds:
            proj.claims_over_av(t, kind)
    for cmt5 in (0.0, 0.01, 0.014, 0.02, 0.0405, 0.08):
        proj.mgsv_rate_statutory(cmt5)
        proj.mgsv_rate_is_compliant(cmt5)
    for tau in (0.1, 985 / 365.25, 9.0):
        proj.mva_ref_term_years(tau)


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)


def _copied(folder, file):
    """An edit that replaces ``file`` with the copy in ``folder``, as written there."""
    return lambda _: pd.read_csv(pathlib.Path(folder) / file)


# How many rows of the splice grid C4 compares at once.  compiled_mismatches sweeps every
# row of its case in one modelx read, _myga_c4_also's calls with it, and keeps every value
# of every row, in the parent and in the child, until it compares them.  A MYGA row runs at
# most 495 months on the grid, against UL's 1,236 and WholeLife's 660; on the core grid's
# 24 rows, twenty at a time peaked at 2.27 GB in the comparison's process, ten at 1.58 GB,
# for 52 s against 57 (measured at M20, under load), so MYGA compares twenty rows at a
# time, WholeLife's chunk, two chunks on the core grid and five on the full
# (USLIB-SEC-PLAN.md §7.2, *For M16 and later*, item 7).
C4_CHUNK = 20


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_the_splice_grid(spliced,
                                                                             sec_build,
                                                                             tmp_path):
    """C4 on the branches: compiled, every cell of the splice grid is modelx's.

    The sample traces the committed points alone, and they leave branches untaken, which
    are typed all the same, because every branch of a cell returns the one type the
    others return (sample_sec.py).  What the compiled model computes on them is held
    here: the splice grid's points, S's restated in force at T2's months and issued later,
    and the variants, the female mortality, the GMIR's other two bands, a zero basis,
    premium tax, the floor's charge, a seven-year guarantee period on the five-year
    schedules and issue age 85, under the splice's References, with utilization
    withdrawals, the renewal spread and acquisition (:data:`SPLICED_REFS`), on the
    splice's stepped scenarios, re-based to each row's month, its renewal schedule apart
    and its cut duration factors (:data:`SPLICED_EDITS`).  The grid is the one this run's
    ``spliced`` selects, the core by default and the full grid under
    ``USLIB_SEC_FULL=1``, and the test carries no ``sec_full`` mark, since a skipped
    compile test fails the cython job.  The grid's SEC table goes beside the build
    :data:`C4_CHUNK` rows at a time; modelx sweeps every row fully, with
    :func:`_myga_c4_also`'s calls, and the compiled model must agree at every
    argument modelx caches, identically on x86-64 and to 1e-12 relative elsewhere, with
    every raise and every ``Data`` array (``sec_support.compiled_mismatches``).
    """
    build = sec_build(SEC)
    here = spliced[1].Data.input_dir()
    table = pd.read_csv(here / TABLE, index_col="point_id")
    assert len(table) == len(spliced[1].Data.model_point_table())
    edits = {file: _copied(here, file) for file in SPLICED_EDITS}
    chunks = [table.iloc[i:i + C4_CHUNK] for i in range(0, len(table), C4_CHUNK)]
    assert sum(len(chunk) for chunk in chunks) == len(table) and len(chunks) > 1
    found = []
    for i, chunk in enumerate(chunks):
        folder = compiled_case(build, tmp_path / f"grid{i}", model_points=chunk,
                               edits=edits)
        found += compiled_mismatches(build, folder, refs=SPLICED_REFS, also=_myga_c4_also)
        shutil.rmtree(tmp_path / f"grid{i}")
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


def _late_scenario(table):
    """The shipped scenarios and ``late``, which sets its first level at month 120, the
    shipped horizon, each later level its own."""
    rows = [("late", 120, 0.058, 0.041), ("late", 600, 0.049, 0.036),
            ("late", 1300, 0.067, 0.052)]
    added = pd.DataFrame(rows, columns=["scenario_id", "t", "mva_ref_yield",
                                        "market_rate"]).assign(provenance="test copy")
    return pd.concat([table, added], ignore_index=True)


def _far_withdrawals(table):
    """The shipped programmes and ``far``, with withdrawals at policy months 0, 600 and
    1,199, the last covered month from issue age 0, each its own amount."""
    rows = [("far", 0, 1100.0), ("far", 600, 1600.0), ("far", 1199, 1900.0)]
    added = pd.DataFrame(rows, columns=["wd_schedule_id", "t", "wd_amount"]).assign(
        provenance="test copy")
    return pd.concat([table, added], ignore_index=True)


EXTREME_EDITS = {"mort_table.csv": _extended_mortality, "rate_scenario.csv": _late_scenario,
                 "withdrawal_table.csv": _far_withdrawals}

# The state of the anchor at issue age 0 in force in its last covered month, policy month
# 1,199, each column a value Data accepts there: off an anniversary, past the initial term.
LAST_MONTH_STATE = {"policy_count": 0.5, "av_pp_init": 150000.0, "mgsv_pp_init": 120000.0,
                    "prem_accum_gmir_pp_init": 110000.0,
                    "interest_credited_pp_init": 60000.0,
                    "interest_credited_pp_prev_anniv_init": 59000.0,
                    "free_wd_allow_init": 14000.0, "free_wd_remain_init": 14000.0,
                    "tax_basis_pp_init": 100000.0, "credit_rate_init": 0.03,
                    "mva_ref_yield_locked_init": 0.05}

# The frames of the contract's extremes, in _contract_extremes' order.
EXTREME_FRAMES = [1200, 1320, 180, 300, 1, 480, 480, 1]


def _contract_extremes():
    """The table for the contract's longest frames, its oldest issue age and the bounds of
    its tables, made from the committed points.

    Issued at 0, the youngest age the contract issues at, cover runs 1,200 months: the
    anchor issued now, withdrawing on ``far``'s programme to its last covered month; and
    issued 120 months on, the shipped ``future_horizon_mth``, a frame of 1,320 months, the
    longest the contract allows, which reads every cache as far as ``spec_sec.py`` sizes
    it, ``t`` to 1,320 in C4's sweep of the month after it and 1,321 in its look-ahead,
    the contract year to 100 and the attained age to 99, on ``late``, a scenario that sets
    its first level in the point's issue month, 120.  Then at 85, the oldest issue age:
    S's asymmetric cap issued now and its geometric MVA issued 120 months on, attained ages
    85 to 99, through the age cap's band, 94 to 99.  Camp B in its last covered month, a
    frame of one row; the declared differential on a twelve-year guarantee period, whose
    whole years remaining pass the duration factors' last, 10; the anchor on a seven-year
    period, which outruns the five-year surrender schedules; and the anchor at issue age
    0 in force in its last covered month, policy month 1,199 (:data:`LAST_MONTH_STATE`).

    The shipped tables stop short of such policies, so the copies extend them
    (:data:`EXTREME_EDITS`), each added key with values of its own: the mortality below 40
    geometric in age (:func:`_extended_mortality`), so that a read of the age beside the
    right one, which a padded array allows, changes a number the compiled comparison sees.
    """
    committed = _committed()

    def twin(s_point, **columns):
        return committed.loc[[_label(committed, "twin", s_point, 0)]].assign(**columns)

    rows = pd.concat([
        twin(1, age_at_entry=0, wd_schedule_id="far"),
        twin(1, age_at_entry=0, duration_mth=-120, scenario_id="late",
             wd_schedule_id="far"),
        twin(6, age_at_entry=85),
        twin(4, age_at_entry=85, duration_mth=-120),
        committed.loc[[_label(committed, "derived", 3, 479)]],
        twin(7, guar_period=12),
        twin(1, guar_period=7),
        twin(1, age_at_entry=0, duration_mth=1199, **LAST_MONTH_STATE)])
    rows.index = pd.Index(range(1, len(rows) + 1), name="point_id")
    return rows


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_contract_extremes(
        sec_build, tmp_path):
    """C4 where the caches end: the contract's longest frames, every cell compiled.

    The eight points of :func:`_contract_extremes`, the longest frames the contract
    allows, its oldest issue age and the bounds of its tables, read every cache as far as
    ``spec_sec.py`` sizes it: ``t`` to 1,320, the month after the 1,320-month frame, and
    1,321, which the roll-forwards read there, the contract year to 100 and the attained
    age to 99; the scenario from a first month above 0, a withdrawal programme to the
    last covered month, the duration factors past their last year and the surrender
    schedules past theirs.  modelx sweeps each fully, with
    :func:`_myga_c4_also`'s calls, and the compiled model must agree everywhere,
    every raise included.  A cache one too small for the contract raises ``IndexError``
    compiled where modelx reads on, and fails here, though the spec check passes it,
    which holds the caches to the spec and not the spec to the contract.  Under the
    shipped References, and with ``USLIB_SEC_FULL=1`` again under :data:`SPLICED_REFS`,
    with utilization withdrawals at every anniversary to the last.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "extremes", model_points=_contract_extremes(),
                           edits=EXTREME_EDITS)
    model = mx.read_model(folder, name=_name("extremes_frames"))
    try:
        frames = [projection(model, key).proj_len() for key in point_keys(model)]
        data = model.Data
        assert data.scenario_first_mths().max() == 120 and data.wd_last_mth() == 1199
        declared = projection(model, point_keys(model)[5])
        assert max(declared.mva_term_years(t) for t in range(declared.proj_len())) > (
            data.mva_factor_last_year())
    finally:
        model.close()
    assert frames == EXTREME_FRAMES, frames
    found = []
    for refs in ({}, SPLICED_REFS) if SEC_FULL else ({},):
        found += compiled_mismatches(build, folder, refs=refs, also=_myga_c4_also)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


# The cap test's points: the twins of S's six points that cap the MVA, every cap rule,
# issued at 85, so that the age cap binds on the surrender charge from attained age 95,
# and the anchor, which does not, at 60.
CAPPED_POINTS = (1, 2, 3, 4, 5, 6)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_where_the_caps_bind(sec_build,
                                                                              tmp_path):
    """C4 where a cap binds: the surrender charge's age cap and each MVA cap rule.

    MYGA's caps are ``min``s and ``max``es whose other side the committed points rarely
    reach: ``surr_charge_rate`` is the schedule's rate capped by the attained age's
    (``surr_charge_age_cap``), which binds from attained age 95 on the shipped tables,
    and ``mva_pp`` and ``wd_mva_pp`` cap the MVA by one of four rules, or none.  So the
    twins of S's points 1 to 6, every rule among them, issued at 85, run on the splice's
    stepped scenarios and renewal schedule under :data:`SPLICED_REFS`, where utilization
    withdrawals reach the excess and the yields move: in modelx the age cap binds, and
    under each of the four rules the MVA is capped in some month.  modelx sweeps each
    point fully, and the compiled model must agree at every argument modelx caches,
    identically on x86-64 and to 1e-12 relative elsewhere, on both sides of every cap.
    """
    build = sec_build(SEC)
    committed = _committed()
    rows = committed.loc[[_label(committed, "twin", p, 0) for p in CAPPED_POINTS]].assign(
        age_at_entry=85)
    folder = compiled_case(build, tmp_path / "capped", model_points=rows,
                           edits=SPLICED_EDITS)
    model = mx.read_model(folder, name=_name("capped"))
    try:
        for ref, value in SPLICED_REFS.items():
            setattr(model.Projection, ref, value)
        aged, capped = False, set()
        for key in point_keys(model):
            p = projection(model, key)
            for t in range(p.proj_len()):
                cap = p.surr_charge_age_cap(t)
                aged |= 0 < p.surr_charge_rate(t) == cap < 1.0
                raw = p.mva_rate(t) * p.surr_excess_pp(t)
                if p.mva_pp(t) != raw:
                    capped.add(p.mva_cap_rule())
    finally:
        model.close()
    assert aged and capped == {"sym_sc", "min_sc_interest", "asym_sc_snfl",
                               "gmir_floor"}, (aged, capped)
    found = compiled_mismatches(build, folder, refs=SPLICED_REFS, also=_myga_c4_also)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


# The labels Data accepts that are not text: the seven a projection does not join on,
# blank, read by pandas as NaN; and the three it joins on, sex, scenario_id and
# wd_schedule_id, as numbers, which pandas reads as ints, on tables keyed by numbers.
NUMBERED = {"sex": {"M": 1, "F": 2},
            "scenario_id": {"base": 1, "stress": 2, "differential": 3},
            "wd_schedule_id": {"anchor": 1, "none": 2, "charged": 3}}
NUMBERED_FILES = {"sex": "mort_table.csv", "scenario_id": "rate_scenario.csv",
                  "wd_schedule_id": "withdrawal_table.csv"}


def _numbered(column):
    """An edit of a table keyed by ``column`` that keys it by :data:`NUMBERED`'s ints."""
    return lambda table: table.assign(**{column: table[column].map(NUMBERED[column])})


def _labels_not_text():
    """The labels ``Data`` accepts that are not text, as (case, the table, the edits).

    ``blank``: the anchor's twin; the stress twin with a blank ``policy_id`` and
    ``tax_status``, which no cell reads, so that it projects; and Camp B in its last
    covered month, a frame of one month, since modelx sweeps a raise in every cell of every
    month, five times, each with one of the five decoded labels blank, which its
    projection refuses where it asks for the value, as S's does, and a blank
    ``renewal_architecture``, which S reads as neither architecture, it projects; and once
    more with both ``mva_cap_rule`` and ``mgsv_wd_convention`` blank, so that the surrender
    benefit, ``max`` of the surrender value and the floor, reaches two refusals.  Compiled,
    ``max`` and ``min`` of two cells would evaluate the second first, so each cell that
    takes two binds them first in ``MYGA_US_S``'s order, and this point is refused with
    ``invalid mva_cap_rule`` in both engines.  ``numeric``: the committed table with
    its sex, scenario and withdrawal keys numbers, on tables keyed by the same numbers
    (:data:`NUMBERED`).
    """
    committed = _committed()
    last = committed.loc[[_label(committed, "derived", 3, 479)]]
    blank = pd.concat([
        committed.loc[[_label(committed, "twin", 1, 0)]],
        committed.loc[[_label(committed, "twin", 2, 0)]].assign(policy_id=None,
                                                                 tax_status=None),
        *[last.assign(**{label: None}) for label in DECODED],
        last.assign(mva_cap_rule=None, mgsv_wd_convention=None)])
    blank.index = pd.Index(range(1, len(blank) + 1), name="point_id")
    numeric = committed.assign(**{column: committed[column].map(numbers)
                                  for column, numbers in NUMBERED.items()})
    return [("blank", blank, None),
            ("numeric", numeric, {NUMBERED_FILES[c]: _numbered(c) for c in NUMBERED})]


@pytest.mark.cython
def test_the_compiled_model_returns_a_label_that_is_not_text_as_modelx_does(sec_build,
                                                                             tmp_path):
    """C4 on labels that are not text: the compiled accessors return what modelx returns.

    ``Data`` accepts a blank label where no cell reads it, and keys that are numbers on
    tables keyed by numbers, since ``MYGA_US_S`` projects such a point; and it accepts
    blank decoded labels, which the point's first projection refuses.  modelx returns each
    label as pandas reads it, NaN or an int, and an accessor typed ``str`` would raise
    ``TypeError`` compiled; the sample types the ten as Python objects (sample_sec.py).
    So on each case of :func:`_labels_not_text`, after checking that the file reads as the
    case says, modelx sweeps every point fully, with every code where no cell raises
    (:func:`_myga_c4_also`), and the compiled model must agree everywhere, the
    label accessors and every raise included.
    """
    build = sec_build(SEC)
    found = []
    for case, rows, edits in _labels_not_text():
        folder = compiled_case(build, tmp_path / case, model_points=rows, edits=edits)
        model = mx.read_model(folder, name=_name(f"labels_{case}"))
        try:
            points = [projection(model, key) for key in point_keys(model)]
            if case == "blank":
                assert math.isnan(points[1].policy_id()) and math.isnan(
                    points[1].tax_status())
                assert points[1].result_cf() is not None
                for p, label in zip(points[2:], DECODED):
                    assert math.isnan(p.cells[label]()), label
                _refused(points[-2].result_cf, "invalid mva_cap_rule")
                two = points[-1]
                _refused(lambda: two.surr_value_pp(0), "invalid mva_cap_rule")
                _refused(lambda: two.mgsv_pp(0), "invalid mgsv_wd_convention")
                _refused(lambda: two.surr_benefit_pp(0), "invalid mva_cap_rule")
            else:
                for column, numbers in NUMBERED.items():
                    got = [p.cells[column]() for p in points]
                    assert all(isinstance(v, (int, np.integer)) for v in got), got
                    assert set(got) <= set(numbers.values()), got
        finally:
            model.close()
        also = _myga_c4_also if case == "numeric" else None
        found += [f"{case}: {line}" for line in compiled_mismatches(build, folder,
                                                                     also=also)]
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


@pytest.mark.cython
def test_the_compiled_model_reads_keys_written_as_floats_as_modelx_does(sec_build,
                                                                        tmp_path):
    """C4 on tables written out of key order, with keys as floats, at and below 0.

    ``Data`` numbers each table's keys by their sorted order and reads each row's value
    at its key, read by value; the modelx tests hold the arrays to the files, and the
    keys at and below 0 to S.  This holds the compiled ``Data``, and every projection on
    it, to modelx, on :data:`KEYS_APART`'s copy: every assumption table in reverse key
    order with its keys as floats, ``1.0``, a scenario keyed at -5, -2 and 3 beside one
    from month 7, and withdrawals at -3, 0 and the anchor's last covered month.  modelx
    sweeps every committed point fully, and every ``Data`` array and every cell compiled
    must agree.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "keys", edits=KEYS_APART)
    found = compiled_mismatches(build, folder, also=_myga_c4_also)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


@pytest.mark.cython
def test_the_compiled_model_holds_a_far_key_as_modelx_does(sec_build, tmp_path):
    """C4 with a scenario level and a withdrawal at month 1e10 (:data:`FAR_KEYS`).

    The compiled ``Data`` holds the arrays to ``read_last_mth``, as modelx does, and
    projects as though the rows were not there
    (:func:`test_a_key_far_past_every_frame_is_held_nowhere_and_projects_as_without_it`):
    every committed point, swept fully, and every ``Data`` array, compiled as in modelx.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "far", edits=FAR_KEYS)
    found = compiled_mismatches(build, folder, also=_myga_c4_also)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


# The compiled model's own refusals: what it does with a key past the caches spec_sec.py
# sizes, which no projection the contract allows reaches, as (position, cell, arguments,
# what modelx does).  modelx answers a month outside cover with a zero, a contract year past
# cover from the account value outside it, and an age past a table from its last row or by
# its refusal, as the cells say, and refuses a code past the timings, the kinds and the
# names; compiled, each is past a cache, and raises IndexError rather than read or write
# beyond it.  The timing, kind and name caches are eight wide (spec_sec.py), so their first
# code past the cache is 8.  And the free-withdrawal base of a year that opened before the
# valuation date, on the point in force 30 months, reads the account value at a month
# before t = 0: modelx answers with the opening account value, compiled it is past the t
# cache.  free_wd_allow, its one caller, takes such a year's allowance from the opening
# state, so no projection asks for it.
COMPILED_ONLY = [
    (0, "net_cf", (1322,), ("ok", 0.0)),
    (0, "net_cf", (-1,), ("ok", 0.0)),
    (0, "pols_if_at", (0, 8), ("raised", "ValueError: invalid timing")),
    (0, "av_at", (0, 8), ("raised", "ValueError: invalid timing")),
    (0, "claims", (0, 8), ("raised", "ValueError: invalid kind")),
    (0, "claims_over_av", (0, 8), ("raised", "ValueError: invalid kind")),
    (0, "scenario_rate", (0, 8), ("raised", "ValueError: invalid name")),
    (0, "free_wd_allow", (102,), ("ok", 0.0)),
    (0, "free_wd_allow", (-1,), ("ok", 10000.0)),
    (0, "surr_charge_age_cap_at", (101,), ("ok", 0.0)),
    (0, "surr_charge_age_cap_at", (-1,), ("ok", 1.0)),
    (0, "mort_rate_at", (101,), ("ok", 0.313569)),
    (0, "mort_rate_at", (-1,), ("raised", "ValueError: point_id 1: the mortality table "
                                "gives no rate at attained age -1")),
    (8, "free_wd_base", (2,), ("ok", 91426.33990921354)),
    (8, "free_wd_base", (3,), ("ok", 91426.33990921354)),
]

# The codes inside the timing, kind and name caches that a cell does not take, since one
# numbering serves both timing families and every 2-D cache is timing's width
# (spec_sec.py): there the cell itself refuses the code, compiled as in modelx.  As
# (cell, the code's name or number).
CODES_IN_CACHE = [("pols_if_at", "BEF_WD"), ("pols_if_at", "EOM"), ("av_pp_at", "BEF_NB"),
                  ("av_pp_at", "AFT_DECR"), ("av_at", "BEF_MORT"), ("claim_pp", "ALL"),
                  ("claim_pp", 7), ("pols_decr", "ALL"), ("claim_from_av_pp", "ALL"),
                  ("claims_from_av", "ALL"), ("claims", 5), ("claims_over_av", 7),
                  ("scenario_rate", 2), ("scenario_rate", 7)]

# The eight contract columns Data reads as numbers through model_point_numbers alone, which
# no rule of model_point_table reads on a point issued at the valuation date.
NUMBER_COLUMNS = ("premium", "declared_rate_initial", "gmir", "mgsv_rate",
                  "mgsv_annual_charge", "free_wd_rate", "mva_ref_yield_at_issue",
                  "premium_tax_rate")


def _first_from(month):
    """An edit that adds ``from15``, a scenario whose first level is at ``month``."""
    def edit(table):
        added = pd.DataFrame([("from15", month, 0.061, 0.043)],
                             columns=["scenario_id", "t", "mva_ref_yield", "market_rate"])
        return pd.concat([table, added.assign(provenance="test copy")], ignore_index=True)
    return edit


def _at_age_minus_1(table):
    """An edit that adds a row at age -1 to a table keyed by age, the first row's copy."""
    return pd.concat([table.iloc[[0]].assign(age=-1), table], ignore_index=True)


def _past_cover(table, label):
    """``table`` with row ``label``, Camp B in its last covered month, moved on to 480,
    the month its cover ends, its anniversary state as ``Data`` requires it there."""
    row = table.loc[label]
    return _moved(label, 480,
                  interest_credited_pp_prev_anniv_init=row["interest_credited_pp_init"],
                  free_wd_allow_init=row["free_wd_rate"] * row["av_pp_init"])(table)


def _refusal_cases():
    """Every refusal the compiled model must make as modelx does, as (case, the table, the
    edits, [(position, cell, arguments)], the Data cells to read).

    A position, not a label, since a table ``Data`` refuses has no keys to give: each is
    the row's place in the table written, ``Projection``'s ``idx``, which the test indexes
    ``Projection`` by in modelx too.
    """
    committed, relabeled = _committed(), _relabeled(_committed())

    def at(table, label):
        return list(table.index).index(label)

    last = _label(committed, "derived", 3, 479)
    future = _label(committed, "future", 1, -15)
    short = committed.drop(index=[last])
    cases = [
        ("past its cover", _past_cover(committed, last), None,
         [(at(committed, last), "proj_len", ())], ()),
        ("past its cover, relabeled", _past_cover(relabeled, 100 + last), None,
         [(at(relabeled, 100 + last), "proj_len", ())], ()),
        ("the scenario read before its first month",
         _set("scenario_id", [future], "from15")(committed),
         {"rate_scenario.csv": _first_from(15)},
         [(at(committed, future), "scenario_rate", (0, "MARKET_RATE")),
          (at(committed, future), "scenario_rate", (14, "MVA_REF_YIELD"))], ()),
        ("an age below the mortality table", committed, None,
         [(0, "mort_rate_at", (39,))], ()),
        ("an age past a mortality table that ends at 98", short,
         {"mort_table.csv": _mortality_to(98)},
         [(0, "mort_rate_at", (99,)), (0, "proj_len", ()), (0, "result_cf", ())], ()),
        ("a mortality row at age -1", committed,
         {"mort_table.csv": _at_age_minus_1},
         [(0, "result_cf", ())], ("mort_rates",)),
        ("an age cap row at age -1", committed,
         {"surr_charge_age_cap.csv": _at_age_minus_1},
         [(0, "result_cf", ())], ("surr_charge_age_caps",)),
        ("codes no cell of the family takes, inside the caches", committed, None,
         [(0, cell, (0, code)) for cell, code in CODES_IN_CACHE], ()),
        ("a label at 2**53, relabeled", relabeled.rename(index={101: 2 ** 53}), None,
         [(at(relabeled, 101), "point_id", ())], ("point_id",)),
        ("a label written as text, relabeled", relabeled.rename(index={107: "7x"}), None,
         [(at(relabeled, 107), "point_id", ())], ("point_id",)),
    ]
    for column in ("age_at_entry", "duration_mth", "guar_period"):
        cases.append((f"{column} at 2**53", _set(column, [2], 2 ** 53)(committed), None,
                      [(1, "result_cf", ())], ("model_point_table",)))
    for column in NUMBER_COLUMNS:
        cases.append((f"{column} written as text", _set(column, [3], "1e5x")(committed),
                      None, [(2, "result_cf", ())], ("model_point_numbers", column)))
    for case, table, edits, label, *_ in NOT_ISSUED:
        cases.append((case, table, edits, [(at(table, label), "result_cf", ())], ()))
    for column, values in DECODED.items():
        if column == "renewal_architecture":
            continue                            # S projects every value of it
        for value in values:
            point = next(p for p in S_POINTS
                         if committed.at[_label(committed, "twin", p, 0), column] == value)
            for how, variant in VARIANT_OF.items():
                cases.append((f"{column} {variant(value)!r}",
                              _set(column, [point], variant(value))(committed), None,
                              [(at(committed, point), "result_cf", ())], ()))
    for case, edit, _ in MALFORMED:
        cases.append((case, edit(committed), None, [(0, "result_cf", ())],
                      ("model_point_table",)))
    for case, source, edit, _, s_point in TABLE_FAULTS:
        twin = at(committed, _label(committed, "twin", s_point, 0))
        cases.append((case, committed, {source: edit}, [(twin, "net_cf", (0,))],
                      (CHECKED[source][1],)))
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
    the compiled model as out of modelx.  So, each on its own inputs
    (:func:`_refusal_cases`): ``proj_len()`` refuses a point past its cover, naming it by
    ``point_id()``, on the committed table and relabeled ``100 + point_id`` in reverse
    order, where a label is no position, and a point the contract does not issue, which
    the compiled caches are not sized for (:data:`NOT_ISSUED`), relabeled too; the
    scenario read before its first month and the mortality outside its ages are refused
    by name; a table with a negative age, which no array from 0 can hold, is refused by
    its check; a label at ``2**53`` or written as text by ``Data.point_id``, a whole
    number at ``2**53`` by the table, and text in each of the eight contract amounts and
    rates by ``model_point_numbers`` and the amount's vector; each variant of a decoded
    value S refuses (:data:`DECODED`), by the projection, with S's message; and every case
    of :data:`MALFORMED` and of :data:`TABLE_FAULTS` is refused by a projection, and by the
    ``Data`` cell that checks it, compiled as in modelx, so a compiled ``Data`` cell
    refuses each value its modelx cell refuses; and a code a cell does not take, inside
    its cache, is refused by the cell (:data:`CODES_IN_CACHE`).

    And the refusals that are the compiled model's alone (:data:`COMPILED_ONLY`): a month
    past the ``t`` cache either side, a code past the timing, kind and name caches, a
    contract year past the ``y`` cache either side and an age past the ``a`` cache, each
    raising ``IndexError`` compiled, beside what modelx does, and the free-withdrawal base
    of a year that opened before the valuation date, a month before ``t = 0``.

    The cases share one directory, which each case's inputs overwrite in turn, and one
    copy of the compiled package: each child reads its inputs afresh, as the compiled
    ``Data`` reads its files once an import.
    """
    build = sec_build(SEC)
    cases = _refusal_cases()
    cases.append(("compiled only", _committed(), None,
                  [(idx, cell, args) for idx, cell, args, _ in COMPILED_ONLY], ()))
    dest = tmp_path / "refused"
    folder = compiled_case(build, dest)
    found, refused = [], 0
    for case, table, edits, calls, data in cases:
        temp_inputs(dest, model_path(SEC), model_points=table, model_point_file=TABLE,
                    edits=edits)
        model = mx.read_model(folder, name=_name("refused"))
        try:
            calls = [(idx, cell, tuple(_timing(model, a) if isinstance(a, str) else a
                                       for a in args))
                     for idx, cell, args in calls]
            want = [_modelx_did(lambda: model.Projection[idx].cells[cell](*args))
                    for idx, cell, args in calls]
            want_data = {name: _modelx_did(model.Data.cells[name]) for name in data}
        finally:
            model.close()
        job = {"refs": {}, "calls": {}, "data": list(data)}
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
                expected = next(w for i, c, a, w in COMPILED_ONLY
                                if (i, c, a) == (idx, cell, args))
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
def test_the_compiled_model_divides_by_zero_as_modelx_does(sec_build, tmp_path):
    """Compiled, a divisor of zero raises modelx's ``ZeroDivisionError``, word for word.

    Cython's division of C doubles raises ``ZeroDivisionError("float division")``, where
    Python says ``float division by zero``; so each cell whose divisor its inputs can bring
    to zero tests it and raises Python's own message.  On each case of
    :data:`ZERO_DIVISORS`, S's inputs, with which ``MYGA_US_S`` raises the same
    (:func:`test_a_zero_divisor_raises_s_error_with_s_message`), the compiled model,
    with the case's References set, must raise what modelx raises on the same copy, and
    that is the error asserted there.
    """
    build = sec_build(SEC)
    found = []
    for number, (case, s_point, columns, edits, refs, calls) in enumerate(ZERO_DIVISORS):
        _, table = _zero_divisor_tables(s_point, columns)
        idx = list(table.index).index(_label(table, "twin", s_point, 0))
        dest = tmp_path / f"zero{number}"
        folder = compiled_case(build, dest, model_points=table, edits=edits)
        model = mx.read_model(folder, name=_name("zero_cy"))
        try:
            for ref, value in refs.items():
                setattr(model.Projection, ref, value)
            want = [_modelx_did(lambda: model.Projection[idx].cells[cell](*args))
                    for cell, args in calls]
        finally:
            model.close()
        got = run_compiled(dest, build.package.name,
                           {"refs": refs, "calls": {idx: calls}})
        assert got["exit"] == 0, f"{case}: the compiled run failed:\n{got['stderr']}"
        assert all(got["compiled"].values()), got["compiled"]
        for (cell, args), modelx_did, compiled_did in zip(calls, want, got["values"][idx]):
            if modelx_did != ("raised", ZERO_DIVISION) or tuple(compiled_did) != modelx_did:
                found.append(f"{case}: {cell}{args}: modelx {modelx_did}, compiled "
                             f"{compiled_did}")
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

# The two cold calls the stack test makes on each point: the last month's net cash flow,
# and the account value's residual there, the deepest head (STACK_HEADS).
STACK_HEADS = ("net_cf", "check_av_roll_fwd_resid")


@pytest.mark.cython
def test_the_longest_cover_runs_cold_on_a_one_megabyte_stack(sec_build, tmp_path):
    """The deepest call the contract allows runs compiled on a 1 MiB stack (F7).

    On the anchor at issue age 0, issued now and 120 months on, whose cover runs 1,200
    months, on mortality extended below 40 (:func:`_extended_mortality`), a cold
    ``net_cf`` and a cold ``check_av_roll_fwd_resid`` in the last month each run the
    count's and the account value's chains from the end of the frame back to
    ``t_entry``, 1,199 months and the cells above and below them deep in modelx on a model
    just read (:func:`test_the_deepest_cold_call_runs_one_cell_a_month`), and compiled
    they run on the C stack, which the interpreter's recursion limit does not count.
    1 MiB is the stack MSVC gives an executable's main thread unless the executable asks
    for more: a host that embeds Python, where python.exe itself asks for 2,000,000
    bytes.  A thread whose stack is reserved at 1 MiB stands in for it on every platform
    (``sec_support.run_compiled``), and in one each call runs cold and returns modelx's
    number, identically on x86-64 (``sec_support.exact_here``) and to 1e-12 elsewhere.
    With gcc the calls need between 256 and 384 KiB.  A stack too small kills the child, and
    the test fails naming the stack.  The thread's stack is read back too, from Windows or
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
    committed = _committed()
    rows = committed.loc[[_label(committed, "twin", 1, 0)] * 2].assign(age_at_entry=0)
    rows = rows.assign(duration_mth=[0, -120])
    rows.index = pd.Index([1, 2], name="point_id")
    folder = compiled_case(build, tmp_path / "longest", model_points=rows,
                           edits={"mort_table.csv": _extended_mortality})
    calls, want = {}, {}
    for key in (0, 1):
        model = mx.read_model(folder, name=_name("longest"))
        try:
            proj = projection(model, key)
            last = proj.proj_len() - 1
            assert last - proj.t_entry() == 12 * 100 - 1, key
            calls[key] = [(head, (last,)) for head in STACK_HEADS]
            want[key] = [proj.cells[head](last) for head in STACK_HEADS]
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
# expenses(12), before inflation_rate is set to 0 and after.
STALE_CHILD = """\\
import json, sys
sys.path.insert(0, sys.argv[1])
model = __import__(sys.argv[2]).mx_model
p = model.Projection
early = p[7]
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
    the worked example's twin at ``idx`` 0, the anchor restated at its month 12, at
    ``idx`` 7, made before, and Camp B's twin, at ``idx`` 2, made after, so that a
    modelx-cython that began to clear caches would be seen here, and the advice changed
    with it.  A compiled value meets modelx's as C4 holds it (:func:`_as_modelx`), and
    one the compiled model kept, its own value of before, identically.
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
        before = (p.expenses(12), projection(model, 7).expenses(12))
        p.inflation_rate = 0.0
        fresh = (p.expenses(12), projection(model, 7).expenses(12),
                 projection(model, 2).expenses(12))
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
    modelx's: point 8's description, the anchor restated at its first anniversary, and
    its first twelve rows of account value and cash flows, and the block's lines for each
    point, its first twelve rows and its first twelve projection years.

    The same output is what a runner that ignored ``--build`` and ran modelx would print,
    so the runner is also given a directory that holds no build, and must refuse it,
    saying so, rather than print anything.
    """
    build = sec_build(SEC)
    runner = model_path(SEC).parent / "run_sec.py"
    for args in (("8",), ("--block",)):
        expected = _run_sec(runner, *args)
        assert _run_sec(runner, *args, "--cython", "--build", str(build.out)) == expected
    empty = tmp_path / "no_build"
    empty.mkdir()
    done = _run_sec(runner, "8", "--build", str(empty), check=False)
    stderr = done.stderr.decode(errors="replace")
    assert done.returncode != 0 and done.stdout == b"", stderr
    assert f"holds no build of {SEC} for this interpreter" in stderr, stderr
