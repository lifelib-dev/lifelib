"""In-force tests for DIA_US_SEC: the splice, future business, counts, regeneration.

``DIA_US_SEC`` is ``DIA_US_S`` taught to run in force at a valuation date
(USLIB-SEC-PLAN.md, milestone M12).  It runs on two clocks: ``t`` counts months from the
valuation date, the same month for every model point, and ``duration_mth(t)`` counts the
months from issue, ``duration_mth_init() + t``.  A model point may be a contract already in
force at the valuation date, in its deferral or in its income phase, one issued at it, or
one issued up to ten years after it, as in ``basiclife/BasicTerm_SE``.  A contract in force
opens with eight columns of state beside its count: each covered life's probability of
being alive at the valuation date; the premiums paid and the income they bought; on a cash
or installment refund, the guarantee period the pricing kernel prices every slice with, a
fixed point over the whole premium schedule; the cohort that reached the income phase,
``l_last(T)``, past the income start month, and the cohort that commuted, ``l_last(t_c)``,
past a commutation; and the reference rate's change since issue, which moves the
commutation discount rate.  Its premiums still due are in its own premium schedule,
``premium_schedule_sec.csv``.  Pricing stays at issue and at the premium dates, on a
survival curve of its own from issue, and the payout schedule is fixed at the income start
month and read by policy month, so neither needs a column.

The worked example is not restated here.  On a point issued at the valuation date the two
clocks coincide and the model is ``DIA_US_S``, and ``test_model_conventions.py`` asserts
that cell by cell on the twins of S's seventeen points (T1), so every golden of
``test_deferred_income_annuity_us.py`` holds on this model with no number copied.  The
conventions also hold the SEC family's other rules: every frame opens at ``t = 0``,
``BEF_DECR`` is ``BEF_NB`` plus the month's new business, new business enters once, and
nothing happens before issue.  ``pols_if`` here is the count on the books weighted by the
probability that a covered life is alive, as ``DIA_US_S`` weights its constant count, so
the model is registered ``survival_pols_if`` and skips the convention that ``pols_if`` is
the ``BEF_DECR`` count; this module asserts what it is instead.  It holds the rest of the
plan's tests (its §5.2) and the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's and in
  ``result_pols``.  The months are the ones S's events need: either side of the second
  premium, of the income start month and of each option month, the last month of each
  refund, derived and certain period and the first after it, the month before mortality's
  cap binds and the months after a life dies with certainty, the anniversaries and the
  last month of a frame.  Eighteen variants of S's points, in a copy of S's table, reach
  what S's own points cannot.
* T3, future new business: a contract issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before it and no rate evaluated there.
* D11's R1, R1a and R2, and D3's clock: on the splice's grid no cell is called at a
  negative argument, nor at a policy month, a policy year or an age the contract does not
  have, none evaluated on the books reads a month before them, and none reads beyond
  ``t + 1``; on the committed points no recursion runs backward over the frame, a cold
  call runs one cell a month, a cold first month a handful of cells, and the policy clock
  is a closed form.
* T4, the count algebra: the count is on the books from issue to the stop rule,
  ``pols_if`` is that count weighted by survival, ``result_pols`` is S's report with the
  new business beside it, and multiplying ``policy_count`` by 2.5, with the reference
  rate's change switched on, multiplies every flow and moves no per-contract value.
* T5, validation: each malformed in-force row and each malformed premium schedule is
  refused as its table is read, naming its point, and each malformed assumption table, a
  key or a value, by the count cell beside its reader, naming the file's lines, and each
  again through a projection; a point at or past the stop rule, owing nothing, or
  accelerating inside a commuted guarantee, is refused by ``proj_len()``; the future
  horizon is a Reference that bounds future business, and at 0 refuses it; the edges of
  the interface, and assumption keys written as floats, are accepted, each check over a
  window of contract months refused just inside each end and read just outside it; and
  every state S reaches, restated in force, is accepted, but a contract owing nothing,
  which is refused by name.
* T6, regeneration: the committed ``model_point_table_sec.csv`` and
  ``premium_schedule_sec.csv`` are what the generator makes of ``DIA_US_S`` and its inputs
  as they stand, and each derived and future row in them is its S point from its month on,
  frame by frame.
* Then the product's own facts: the worked example's derived rows, pricing at issue and
  the premium dates, the payout schedule fixed at the income start month, survival per
  life, the contract open after the last death in a guarantee, a commutation and an
  acceleration before the valuation date, the commutation residual where its guarantee
  ends, the reference rate's change since each contract's own issue, improvement on the
  policy clock and inflation on the valuation clock, the capped mortality rate, the checks
  failing a residual that is not a number, new business with its premiums and no
  acquisition, no lapse, the stop rule, the values outside cover, the block, the annual
  display, an in-force extract, the runner, the docstrings, the shared input tables,
  invalid values, and what the default grid reaches.
* Phase 2's representation, held in modelx in every run (M24): a value a point cannot use
  refused by the point alone, and a fraction in an int column as the table is read; the
  contract the compiled caches are sized for, refused by ``stop_mth()``; every form from
  issue age 0 continuing S, to the last bit of its pricing; the total ``ALL`` with S's sign
  of zero, and ``claims_ann``'s plain sum an ulp or two from S's; the premium table and
  the pricing guarantee's sum S's to the last bit, a premium of 0.0 priced as S prices it,
  and the ROP deferral rounded as S rounds it; each decode S's exact comparison; the tables
  numbered by their own sexes and their padding never read; the vectors' dtypes and the
  cells' Python numbers; the spec and the sample held to their comments; and the runner's
  block sum and build decision.
* C2, the fingerprint: every committed point computes what the model computed when Phase 1
  ended, frozen at the end of this module before Phase 2 changed anything (§5.4).
* The compiled model, marked ``cython``, after the fingerprint: C4 on the splice grid, at
  the contract's extremes, where the cap on mortality and the reference rate's floor bind,
  on keys written as floats and on a label that is not text; the refusals, compiled as in
  modelx, on an extract labelled otherwise than by position; the total's sign of zero; the
  deepest call on a 1 MiB stack and on the main thread; a Reference set late; and the
  runner.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``, ``-k``
for one issued ``k`` months on.  ``DIA_US_S`` has no point in force, so every twin is new
business, compared by T1, and every splice case is a derived row.

**The core grid and the full one** (USLIB-SEC-PLAN.md K6).  T2 and T3 over every month the
product's events need, 112 splices and 21 future points, would take this module well past
three minutes in every run.  By default they run a core of 36 and 8, chosen so that between
them they reach every form, trigger, basis, timing and frequency, every market type and
option, every opening-state column, every kind of valuation month and every branch the full
grid reaches, which ``test_the_core_grid_reaches_every_branch`` asserts; measured line by
line when the module was written, the core's cases execute every line of ``Projection`` the
full grid's execute.  The other cases, and the rules test's scan of their rows, carry the
``sec_full`` marker and are skipped, with the reason shown, unless ``USLIB_SEC_FULL=1`` is
set.  They are never dropped: one leg of the CI matrix sets it, and ``USLIB_SEC_FULL=1
python -m pytest -m sec_full`` on this module runs them alone.  The every-state test
restates S's states at the edges of the product's windows by default, and at every month
of every frame with ``USLIB_SEC_FULL=1``.  Memory is the other cost.  A projected point
holds its cached values and their dependency graph, so a row read once, a splice case's
or a point of a temporary copy, is released as soon as it has been read (``_release``),
and the splice's rows are held one at a time, however large the grid.  The three models
the module sweeps once and holds, the splice's S model and the committed S and SEC models,
are frozen out of the collector (``gc.freeze``), so that a collection scans only what a
test has made since, and the freeze is undone as the module ends (:func:`_freeze`).

Every test keeps four rules.  Each model is read under a name of its own and closed:
``test_deferred_income_annuity_us.py`` reads S under its default name, and reading a model
under a name in use renames the open one.  No test writes inside the library tree: every
changed input goes through ``sec_support.temp_inputs`` into a temporary directory, because
a CSV added beside the models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``us_registry.point_keys`` and the ItemSpaces from
``us_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor Phase 2's positions can
point a test at the wrong row.  And every Reference a test changes, ``Data``'s included, is
set on a model just read, before it computes anything, because a compiled model never
clears a cache; timings and kinds pass through :func:`_code`, so that the same calls serve
Phase 2's int codes (C1).
"""
import ast
import dataclasses
import gc
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
    GENERATED_COLUMNS, SEC_SPECS, TWIN_EXEMPT_DEFAULT, build_sec_table, check_generated,
    codes, compiled_case, compiled_mismatches, exact_here, fingerprint_mismatches,
    frame_mismatches, run_compiled, temp_inputs, twin_mismatches)
from us_registry import model_path, point_keys, projection

SEC, TWIN = "DIA_US_SEC", "DIA_US_S"
TABLE, SCHEDULE = "model_point_table_sec.csv", "premium_schedule_sec.csv"
SPEC = SEC_SPECS[SEC]
NAN = float("nan")

# Eighteen more S points, in the splice's copy of S's table and never in the committed
# one, each one of S's points changed so as to reach what S's own points cannot.  S's
# points are the female anchor life at 60, paying monthly in arrears from policy month 240
# but for one in advance, nonqualified but for the two QLACs, on the anchor mortality basis
# but for one, and each exercises at most one option.  Each variant is (the S point it
# changes, the columns it changes), and takes its base's premium rows; the policy_id keeps
# the generated ids apart.
#
# 18, the anchor on the table basis on a male life, TradIRA, its purchase rate rounded to 4
#   places: both factor tables read on their male rows, and the cap on a male life;
# 19, the death-benefit fork as life only on the table basis, RothIRA: the life-only payout
#   factor and a pricing guarantee of 0;
# 20, life only with the return-of-premium death benefit, LO_ROP: ROP in deferral and a
#   pure life annuity in payout;
# 21, the installment refund paying quarterly in arrears on a 2% COLA, half of its derived
#   period commuted at policy month 252;
# 22, the installment refund paying semi-annually in advance: the refund-period search in
#   advance;
# 23, the cash refund on computed factors paying semi-annually in arrears;
# 24, the 10-year period certain paying annually in arrears;
# 25, the period certain accelerated at policy month 357, so that the five instalments the
#   lump sum pulls forward straddle the guarantee's end: floors 1, 1, 0, 0, 0;
# 26, the commuting period certain paying quarterly in advance, half of it commuted;
# 27, the cash refund with a commutation at policy month 252 and nothing guaranteed to
#   commute;
# 28, the joint point with a female joint annuitant at 57, the younger life;
# 29, the joint point on the primary trigger, generational: improvement on both sexes;
# 30, the 10-year period certain bought at 80 with a 30-year guarantee: the life dies with
#   certainty at 120 inside it;
# 31, the joint point bought at 80 and 85 as a 30-year period certain: both lives dead
#   inside the guarantee;
# 32, the QLAC breaching its limit turned installment refund on a 1% COLA from policy month
#   360, with 20,000 of other QLAC premium, a half commutation at 365 inside its derived
#   period and an acceleration at 390 on life-contingent instalments: a QLAC failing all
#   six of its conditions;
# 33, the start-date adjustment advancing the income start to policy month 180 at policy
#   month 30, before the second premium, which is then priced to the new date;
# 34, the advance cash refund paying annually;
# 35, the commuting period certain half commuted at policy month 252 and accelerating in
#   its guarantee's last month, 359, so that its lump sum pulls forward only the life tail
#   (proj_len() refuses a lump sum that pulls forward instalments of the commuted
#   guarantee), and the commutation residual adds the lump sum back.
VARIANTS = {
    18: (1, {"policy_id": "DIA-900018", "sex": "M", "market_type": "TradIRA",
             "purchase_rate_dp": 4}),
    19: (4, {"policy_id": "DIA-900019", "income_form": "LO", "market_type": "RothIRA"}),
    20: (6, {"policy_id": "DIA-900020", "income_form": "LO_ROP", "db_form": "ROP"}),
    21: (5, {"policy_id": "DIA-900021", "frequency": 4, "cola_rate": 0.02,
             "commute_mth": 252, "commute_frac": 0.5}),
    22: (5, {"policy_id": "DIA-900022", "frequency": 2, "timing": "advance"}),
    23: (3, {"policy_id": "DIA-900023", "frequency": 2}),
    24: (7, {"policy_id": "DIA-900024", "frequency": 1}),
    25: (7, {"policy_id": "DIA-900025", "accel_mth": 357}),
    26: (15, {"policy_id": "DIA-900026", "frequency": 4, "timing": "advance",
              "commute_frac": 0.5}),
    27: (3, {"policy_id": "DIA-900027", "commute_mth": 252, "commute_frac": 1.0}),
    28: (8, {"policy_id": "DIA-900028", "joint_sex": "F", "joint_age": 57}),
    29: (9, {"policy_id": "DIA-900029", "mort_basis": "generational"}),
    30: (7, {"policy_id": "DIA-900030", "issue_age": 80, "certain_period": 30}),
    31: (8, {"policy_id": "DIA-900031", "issue_age": 80, "joint_age": 85,
             "income_form": "PC", "certain_period": 30}),
    32: (12, {"policy_id": "DIA-900032", "income_form": "IR", "cola_rate": 0.01,
              "income_start_mth": 360, "commute_mth": 365, "commute_frac": 0.5,
              "accel_mth": 390, "other_qlac_premium": 20000.0}),
    33: (13, {"policy_id": "DIA-900033", "adjust_mth": 30, "adjust_start_mth": 180}),
    34: (17, {"policy_id": "DIA-900034", "frequency": 1}),
    35: (15, {"policy_id": "DIA-900035", "commute_frac": 0.5, "accel_mth": 359}),
}

# T2's months, by S point or variant: every month S's events need, chosen on the splice's
# edited inputs, where the set-apart tables and the A/E move some events from where the
# shipped inputs put them (below).  12 and 24, anniversaries in deferral; 59, 60 and 61,
# either side of the second premium; 239, 240 and 241, either side of the income start
# month T, and 299, 300 and 301 where T is 300; 270, 279 and 280 on the installment refund,
# inside its derived period, its last certain month and the first after; 279 and 280 on
# the anchor, the refund's last month and the first without; 359 and 360, the end of a
# 10-year guarantee; 251, 252 and 253 around the COLA's first step, the acceleration and
# the commutation, and 257 and 258, the blackout's end; 119, 120 and 121 around the
# start-date adjustment, and 179 and 180 around its advanced start; 647 and 683, the month
# before the cap binds on a male life of 117, and 649, the joint annuitant dead from it;
# 479, 480, 500 and 599, around omega inside a 30-year guarantee; 384 and 500, both lives
# dead inside one; 356 to 362 around an acceleration straddling a guarantee's end, and 240,
# its income start month, where l_last(T) is derived and the lump sum's floor reads it; 365
# and 390, a commutation inside a derived period and an acceleration after it; 252 and 359,
# a half commutation and an acceleration in the guarantee's last month; months off the
# payment step of each frequency below monthly; and 719, the last month of a frame.
SPLICE_MTHS = {
    1: (12, 24, 59, 60, 61, 239, 240, 241, 279, 280, 719),
    2: (60, 241), 3: (59, 241), 4: (59, 240), 5: (239, 240, 270, 279, 280),
    6: (60, 240), 7: (239, 300, 359, 360), 8: (12, 240, 300, 647, 649), 9: (240, 649),
    10: (251, 252), 11: (299, 300), 12: (300,), 13: (59, 119, 120, 121, 299, 300, 301),
    14: (59, 60, 61, 251, 252, 253, 257, 258), 15: (59, 251, 252, 253, 359, 360),
    16: (24, 240), 17: (239, 240, 241), 18: (60, 241, 683), 19: (240,), 20: (59, 240),
    21: (241, 252, 253), 22: (241, 250), 23: (243, 245), 24: (250, 251, 359),
    25: (240, 356, 357, 358, 362), 26: (250, 252, 253), 27: (252,), 28: (240, 300),
    29: (24, 240, 649), 30: (479, 480, 500, 599), 31: (384, 500), 32: (365, 390),
    33: (29, 30, 31, 179, 180), 34: (245,), 35: (252, 359)}

# T2's cases, as (row_kind, S point, source_mth), and T3's, as (S point, k).  DIA_US_S has
# no point in force, so there is no twin to splice (§5.2's IN_FORCE_TWINS).  The future
# offset is 13: more than a year, so that a read before issue lands at policy year -1, and
# off every payment step, so that the payment months fall apart on the two clocks.  12
# puts the anniversaries back on the valuation years, and 1 puts them a month off; 120 is
# the horizon itself, the commutation of point 15 falling 372 months on.
SPLICES = tuple(("derived", p, d) for p, ds in SPLICE_MTHS.items() for d in ds)
IN_FORCE_TWINS = ()
FUTURES = (((1, 1), (8, 12), (15, 120))
           + tuple((p, 13) for p in (1, 3, 5, 7, 9, 11, 13, 14, 15, 16, 17, 21, 22, 25,
                                     26, 30, 32, 33)))

# The default run's cases (the module docstring), each with what it is there for.  The
# rest of SPLICES and FUTURES run with USLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("derived", 1, 59): "the table basis in deferral: the second slice at t = 1, dp 6",
    ("derived", 1, 240): "the income start at t = 0: the refund of the whole CP(T)",
    ("derived", 1, 719): "the last month: a one-row frame",
    ("derived", 5, 240): "the installment refund at T: l_last(T) derived at t = 0",
    ("derived", 5, 279): "the installment refund's last certain month",
    ("derived", 7, 239): "the period certain the month before T: l_last(T) at t = 1",
    ("derived", 7, 300): "inside the guarantee: the contract open above the life alive",
    ("derived", 8, 300): "joint: two fractional lives",
    ("derived", 9, 649): "the primary trigger, the joint annuitant dead with certainty",
    ("derived", 11, 300): "a QLAC at its income start, at its limit",
    ("derived", 13, 120): "the start-date adjustment at t = 0",
    ("derived", 14, 60): "the second slice at t = 0, priced with the n_g column",
    ("derived", 14, 252): "the acceleration's lump sum at t = 0",
    ("derived", 14, 253): "inside the blackout, the lump sum paid before t = 0",
    ("derived", 15, 252): "the commutation at t = 0, with the rate change in its column",
    ("derived", 17, 240): "advance timing at T: the balance at G(m)",
    ("derived", 18, 683): "the table basis on a male life, dp 4: the month before the cap",
    ("derived", 19, 240): "life only on the table basis, RothIRA, at T",
    ("derived", 20, 59): "LO_ROP in deferral",
    ("derived", 21, 253): "the installment refund quarterly in arrears, COLA, commuted",
    ("derived", 22, 250): "the installment refund semi-annual in advance, off its period",
    ("derived", 23, 243): "the cash refund semi-annual in arrears, off its period",
    ("derived", 24, 250): "the period certain annual in arrears, off its period",
    ("derived", 25, 240): "an acceleration in a guarantee, l_last(T) derived at t = 0",
    ("derived", 25, 357): "an acceleration straddling the guarantee's end at t = 0",
    ("derived", 26, 252): "half commuted at t = 0, quarterly in advance, a payment month",
    ("derived", 26, 253): "after it, off its period: the frozen weight, quarterly",
    ("derived", 27, 252): "a commutation month with nothing to commute",
    ("derived", 28, 300): "a female joint annuitant, the younger life",
    ("derived", 29, 649): "the primary trigger, generational, the joint annuitant dead",
    ("derived", 30, 479): "the month before the cap at omega, inside a guarantee",
    ("derived", 31, 500): "both lives dead in a guarantee",
    ("derived", 32, 365): "a QLAC failing every condition, commuting in its derived period",
    ("derived", 33, 31): "after an advancing adjustment: the second slice priced to T'",
    ("derived", 34, 245): "the advance cash refund annual, off its period",
    ("derived", 35, 252): "half commuted at t = 0, accelerating at its guarantee's end",
}
CORE_FUTURES = {
    (1, 1): "the table basis, a month off the valuation anniversaries",
    (8, 12): "joint, on the valuation anniversaries",
    (13, 13): "the start-date adjustment from its own issue",
    (14, 13): "an acceleration from its own issue",
    (15, 13): "a commutation from its own issue, on no rate change",
    (21, 13): "a commuting installment refund, quarterly, COLA",
    (25, 13): "an acceleration in a guarantee from its own issue, l_last(T) derived",
    (30, 13): "a guarantee past the age stop",
}

SEC_FULL = os.environ.get("USLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "USLIB_SEC_FULL=1 (USLIB-SEC-PLAN.md K6)"))

# What the splice sets in S as it is read, before it computes anything, and in SEC alike
# but for the reference rate's change (below).  Expense inflation is the one input DIA
# reads on the valuation clock (D7): S inflates by policy year and SEC by valuation year,
# so at the shipped 2.5% the expenses of a point opened at d differ by design, and at 0
# both factors are 1.  The clock itself is then asserted on its own, at the shipped rate.
# Mortality improvement is calendar-dated, from each contract's issue year, so it moves
# with no clock and is not neutralized.  The rest ship at a value that hides some of the
# state from any comparison, and are set apart: ref_rate_shift ships at 0, which hides the
# change in the commutation discount rate (SWITCHED_ON, the one assumption that ships at
# zero); baa_yield ships so that the repricing rate equals the pricing rate, which would
# hide a mix-up of the two; and mort_ae_factor ships at 1, which hides a dropped factor
# and leaves the cap on mortality idle below the limiting age.  The identity does not
# depend on the values, only on the two models describing the same contract.
SWITCHED_ON = {"ref_rate_shift": 0.005}
SPLICED_REFS = {"inflation_rate": 0.0, "baa_yield": 0.0625, "mort_ae_factor": 1.05,
                **SWITCHED_ON}

# The reference rate's change is S's ref_rate_shift, the change since each S contract's
# own issue, which S applies from month 0 on.  SEC reads the splice's table once, as a
# block is read, on one path of the reference rate, which every point shares (D7).
# Restated in force at d, a point has seen all of S's change by the valuation date and
# carries it in ref_rate_shift_init (the spec's state), and on that path nothing changes
# after it, so SEC's own ref_rate_shift, the change made at the valuation date, is 0
# (SEC_REFS).  Restated to be issued k months on, a point has seen no change by its issue
# date, its column is 0, and sees none after it, so its S twin, the same contract on that
# path, is S read with its ref_rate_shift at 0 (LATER_REFS): the splice reads S twice,
# once for each kind of row.  What SEC's ref_rate_shift moves, each contract on the books
# at the valuation date and no contract issued later, the reference-rate test asserts, on
# one table read at two values, and with the column and the Reference of opposite signs.
SEC_REFS = {**SPLICED_REFS, "ref_rate_shift": 0.0}
LATER_REFS = {**SPLICED_REFS, "ref_rate_shift": 0.0}


def _mortality_apart(df):
    """Every ``(age, sex)`` row of the mortality table apart from every other.

    The shipped rates are band-constant over ages 60 to 84 and the male rates are the
    female rates three years on, so a join on the wrong age or the wrong sex would read
    the same number there, and no comparison with S could see it.  Scaled a little by age
    and by sex.  The factor is kept small on purpose: a steeper one takes the female rate
    past 1 at 118 under the splice's A/E, kills the anchor with certainty before its last
    months, and leaves every row valued after it a contract owing nothing, which
    ``proj_len()`` refuses.
    """
    age, male = df["age"], df["sex"] == "M"
    return df.assign(mort_rate=df["mort_rate"] * (1 + 0.0001 * (age - 40))
                     * male.map({True: 1.004, False: 1.0}))


def _improvement_apart(df):
    """Every ``(age, sex)`` row of the improvement scale apart from every other.

    The shipped scale is the same for both sexes at every age and flat at 0.01 below 86,
    so a join on the wrong sex or the wrong age would read the same number there.  Scaled
    by age and sex, plus a small offset that keeps the scale's zero tail apart without
    lowering old-age mortality enough to move the cap.
    """
    age, female = df["age"], df["sex"] == "F"
    scale = female.map({True: 1.25, False: 1.0})
    offset = female.map({True: 1.5, False: 1.0})
    return df.assign(improvement_rate=df["improvement_rate"] * (1 + 0.004 * (age - 40))
                     * scale + 0.000001 * (age - 39) * offset)


# The edits both copies, S's and SEC's, carry.
SPLICED_EDITS = {"mort_table.csv": _mortality_apart,
                 "improvement_scale.csv": _improvement_apart}

# The opening state, in Data's order, and the cells running in force adds to DIA_US_S's,
# each of which the symbol map must name.
STATE = ("lives_if_init_1", "lives_if_init_2", "cum_premium_pp_init", "annual_income_init",
         "guarantee_mths_pricing_init", "surv_to_payout_init", "commute_weight_init",
         "ref_rate_shift_init")
NEW_CELLS = (
    "policy_count", "duration_mth_init", "t_entry", "stop_mth", "is_active", "pols_if_at",
    "pols_new_biz", "lives_if_init", "cum_premium_pp_init", "annual_income_init",
    "guarantee_mths_pricing_init", "surv_to_payout_init", "commute_weight_init",
    "ref_rate_shift_init", "lives_if_pm", "lives_if_last_pm", "mort_rate_py",
    "mort_rate_mth_py", "mort_rate_base_at", "improvement_rate_at", "premium_pm",
    "cum_premium_payout", "annual_income_payout", "is_payment_pm", "cola_factor_pm",
    "annuity_pp_sched_pm", "certain_floor_pm", "is_trigger_either", "is_life_only",
    "is_cash_refund", "is_installment_refund", "is_period_certain", "is_rop", "is_arrears",
    "is_generational", "is_formula_basis",
    # Phase 2's (M24): the label by position, the schedules the sexes select, the pricing
    # kernel keyed by ints, and the ROP table's deferral key.
    "point_id", "mort_schedule", "improvement_schedule", "annuity_factor_at",
    "rop_deferral_yrs")

# The four roll-forward residuals.  Each is 0 exactly or rounding around 0, and an opening
# state the CSV gives back an ulp off moves one by an ulp of what it closes, so T2 and T3
# compare them at the default absolute floor of 1e-9, in a pass of their own, and every
# other cell with no floor (§5.2).
RESIDUALS = frozenset({"check_lives_roll_fwd_resid", "check_income_roll_fwd_resid",
                       "check_payment_factor_resid", "check_commutation_value_resid"})

# The cells T2 skips beyond T1's, which already drop result_pols (the spec's exempt).
# proj_len counts from the valuation date on SEC and from issue on S, so it differs by d by
# design; frame_mismatches asserts what it must get right, that both frames end at the
# same instant.  payment_surv_mth returns a time point, which on SEC's clock is S's less
# d: payment_factor_life, which reads it, is compared, so a wrong survival point still
# fails.  premium_by_mth and premium_schedule hold the premiums still due, and the
# companion's own row labels, where S's hold the whole schedule: the slices still due are
# compared through premium_pp, purchase_rate and annual_income, and the slices paid through
# the opening state.  result_annual's first row on a row restated mid-year holds part of
# a policy year, and its later rows are compared through the year-keyed cells it reads
# (and by test_result_annual_keeps_the_policy_year_key).  The cells keyed by policy month
# are compared at S's keys unshifted, which are policy months on both sides.  Per case,
# accel_payment_factor too, on a row valued after its acceleration month
# (:func:`_after_the_exercise`).
SPLICE_EXEMPT = (TWIN_EXEMPT_DEFAULT | SPEC.exempt
                 | {"proj_len", "payment_surv_mth", "premium_by_mth", "premium_schedule",
                    "result_annual"})
# A future row holds its whole schedule and whole policy years, which T3 compares; the
# schedule's row labels are still the companion's.
FUTURE_EXEMPT = SPLICE_EXEMPT - {"premium_by_mth", "result_annual"}

# The result_cf columns that expense inflation moves, and the cells they are made of: on
# the committed rows, at the shipped 2.5%, the only places a row in force departs from S.
INFLATED = ("expenses", "liability_cf", "net_cf")
INFLATION_CELLS = frozenset({"inflation_factor", "expenses", "liability_outgo",
                             "liability_cf", "net_cf", "result_cf"})

# The decrement rates keyed by month, none of which may be evaluated before issue (R1,
# D4), and the two age-keyed table readers, which may not be read below an issue age.
DECREMENT_RATES = ("mort_rate", "mort_rate_mth", "mort_rate_base", "improvement_rate")
AGE_READERS = ("mort_rate_base_at", "improvement_rate_at")

# The label accessors, DIA_US_S's, which no projection cell calls and the sweep calls, so
# that T2 compares them with S's.
LABELS = ("reduction_trigger", "market_type", "income_form", "payout_form", "db_form",
          "payment_timing", "mort_basis", "factor_basis")

# The cells that scale with policy_count.  Every other cell is a per-contract amount, a
# probability, a rate, a clock or a flag, and must not move when the count does.
# result_annual is both: its claims and income columns are counted, its age, premium,
# CP, B and survival columns are per contract.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz", "premiums",
    "annuity_payments", "claims", "commutations", "expenses", "liability_outgo",
    "liability_cf", "net_cf", "claims_ann", "annuity_payments_ann", "result_cf",
    "result_pols", "result_annual", "check_commutation_value_resid"})
ANNUAL_COUNTED = ("claims_death", "claims_refund", "annuity_payments")

# result_pols' columns, in its order: the count on the books weighted by survival and the
# contracts issued in the month, then S's other seven columns in S's order, which no count
# moves.
RESULT_POLS = ["pols_if", "pols_new_biz", "lives_if_1", "lives_if_2", "lives_if_last",
               "lives_death_last", "certain_floor", "payment_factor_life", "payment_factor"]
RATES = RESULT_POLS[2:]

# BasicTerm_SE's two timings, which running in force adds (S has none), and the two kinds.
TIMINGS = ("BEF_NB", "BEF_DECR")
KINDS = ("DEATH", "REFUND")

# What each monthly cell holds outside cover, before issue and from the stop rule on, as
# its docstring says: no count, so no cash flow; no premium, no instalment, no payment
# factor, no refund and no commutation; no question about the contract answered yes; and a
# COLA factor that moves nothing.  The type is part of the value: an amount, a probability
# or a rate is a float in every branch and a flag a bool, because Phase 2 types a cell by
# the values it returns (USLIB-SEC-PLAN.md F3).  The guard test also calls each of
# PER_LIFE for every covered life, pols_if_at at each timing, and claim_pp and claims at
# each kind, all 0.0, and before issue the time-point cells of BEFORE_ISSUE, lives_if for
# both lives among them; and phase, PRE_ISSUE before issue and TERMINATED from the stop
# rule on, each label passed through _code, as Phase 2's int codes will be.
OUTSIDE_COVER = {
    "is_active": False, "is_payout": False, "is_payment_mth": False,
    "accel_blackout": False, "premium_pp": 0.0, "cum_premium_pp": 0.0,
    "annual_income": 0.0, "annuity_pp_sched": 0.0, "annuity_pp": 0.0,
    "annuity_pp_paid": 0.0, "lives_death_last": 0.0, "certain_floor": 0.0,
    "payment_factor_life": 0.0, "payment_factor": 0.0, "refund_balance": 0.0,
    "accel_payment_factor": 0.0, "commute_frac_cum": 0.0, "commute_weight": 0.0,
    "commuted_value": 0.0, "commutations": 0.0, "annuity_payments": 0.0,
    "premiums": 0.0, "pols_if": 0.0, "pols_new_biz": 0.0, "expenses": 0.0,
    "liability_outgo": 0.0, "liability_cf": 0.0, "net_cf": 0.0,
    "check_payment_factor_resid": 0.0, "check_income_roll_fwd_resid": 0.0,
    "check_commutation_value_resid": 0.0, "cola_factor": 1.0}
PER_LIFE = ("mort_rate_base", "improvement_rate", "mort_rate", "mort_rate_mth",
            "lives_death")
BEFORE_ISSUE = {"lives_if_last": 0.0, "check_lives_roll_fwd_resid": 0.0}

# The valuation-clock cells a month outside cover may not reach: the attained age and the
# calendar year.  The rates that read them hold 0.0 outside cover by their own guards,
# which the guard test asserts first; these have none, and no formula may reach them
# there, nor a caller (USLIB-SEC-PLAN.md F4).  The age readers and the annual rate by
# policy year are not among them: an installment refund's stop rule searches its payout
# schedule, which prices its premiums, so they are read on the policy clock from issue on
# every point, in cover or not, and :func:`_contract` bounds their keys instead.
IN_COVER_ONLY = ("age", "calendar_year")

INFLATION = 0.025       # the shipped inflation_rate, which the inflation test reads

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A limit of n admits a call n + 1 cells deep, counted as modelx's
# stack trace counts them.  A report evaluates each column in ascending t, so a forward
# recursion, through t - 1, finds the month before already cached: the committed points'
# sweep needs a limit of 16, and 15 fails on the installment refund's twin, whose refund
# period is searched over its payout schedule (measured at M24, one more than at M12, the
# first rate reading the life's schedule through Data).  The instalments scheduled
# to date are based at the valuation date's policy month, so the anchor in its last month
# reads them without recursing back to its income start month, 478 months earlier; and a
# backward recursion over a frame longer than a month needs a limit of hundreds.
CALL_DEPTH = 40

# How deep a cold call may run beyond its chain, one cell a month from its month back to
# t_entry (D5).  Three cells recurse a month at a time, each life's survival on every
# point, the premiums paid and the income bought, and the longest of them, survival, sets
# the depth: 726 to 731 levels on the 720-month twins.  Beyond the chain are the cells
# above it, from net_cf down, and below it the first month's rates, the age readers, the
# schedules, the count cells that check their tables and Data's first reads of its tables:
# measured by modelx's stack trace at 7 to 12 levels on the committed points, 15 on the
# anchor's one-row frame in its last month, and 12 at the contract's longest cover, 1,440
# months from issue age 0, where the cash refund runs 1,451 cells deep issued at the
# valuation date and 120 months on (M24, three more than at M12, where the first rate read
# no schedule).  A chain of two cells a month doubles the depth, and needs twice the stack
# compiled.
CHAIN_OVERHEAD = 16

# How deep a cold net_cf(0) may run.  The first month reads the cohort that reaches the
# income phase, l_last(T), only where a certain floor pays it, and on the installment
# refund prices its premiums and searches its payout schedule for its stop rule, by loops
# (lives_if_pm, annuity_factor, the payout income); so a cold first month runs 12 or 13
# cells deep on the committed points, 21 on the installment refund's twin and 8 on the
# point issued later (10 before Data's table is read, where this test reads it first),
# where DIA_US_S's runs 251 on point 1 and 311 on point 13, reading l_last(T) in every
# month through its survival recursion to the income start month (M12).
FIRST_MONTH_DEPTH = 32

# The contract's youngest issue age, issue_age_min, on every form and every life, from
# which the longest cover runs to the age stop.  DIA_US_S projects every form from 0 on
# tables extended below their first age, 20 (M24), so the depth test reads such tables.
CONTRACT_MIN_AGE = 0

REPORTS = ("result_cf", "result_pols")


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
    F5): held together they would raise this module's memory by a gigabyte.  Asked for
    again, the ItemSpace is made afresh and recomputes.  With ``collect``, the collector
    runs at once, as it does for each splice row.  That costs little, because the swept
    models the module holds are frozen out of the collector (:func:`_freeze`), so the
    collection scans only what the row made.
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


def _committed_schedule():
    """The committed premium schedule as the file holds it, unvalidated, on a default
    index."""
    return pd.read_csv(model_path(SEC).parent / SCHEDULE)


def _sec_inputs(tmp_path, table, edits=None, schedule=None):
    """A copy of the product directory whose SEC table is ``table``; its SEC folder.

    ``schedule``, a premium schedule on a default index, is written over the copy's
    ``premium_schedule_sec.csv``; without it the copy holds the committed one, which names
    the committed table's points.  ``edits`` go to ``sec_support.temp_inputs``.
    """
    edits = dict(edits or {})
    if schedule is not None:
        edits[SCHEDULE] = schedule
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=edits)


def _read_edited(tmp_path, edit=None, tag="edited", refs=None, schedule_edit=None):
    """DIA_US_SEC read from a copy whose SEC table is ``edit(_committed())``, and whose
    premium schedule is ``schedule_edit(_committed_schedule())``."""
    table = (edit or (lambda t: t))(_committed())
    schedule = schedule_edit(_committed_schedule()) if schedule_edit else None
    return _read(_sec_inputs(tmp_path, table, schedule=schedule), tag, refs)


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
    """The argument that selects timing or kind ``label``: at stage ``"E"``, the string.

    The conventions' lookup (``test_model_conventions._timing``), on ``Projection`` or any
    of its ItemSpaces, which see its References: Phase 2 turns the timing and kind strings
    into int References of the same names (R9), and this passes whichever the model
    defines, so the calls below read the same at both stages.
    """
    value = space.refs.get(label)
    return value if isinstance(value, int) else label


def _mismatches(s_proj, sec_proj, **kwargs):
    """:func:`sec_support.twin_mismatches`, the one place this module calls it.

    It passes the SEC Space's :func:`sec_support.codes`, which map S's timing, kind and
    phase strings to the int codes Phase 2 gives them, and composes the spec's
    ``twin_arg_map`` before any ``arg_map`` it is given, which maps S's
    ``claims(t, None)`` and ``claims_ann(y, None)`` onto SEC's ``ALL`` and passes SEC's own
    keys unchanged.  Every comparison goes through here, so each takes Phase 2's codes and
    map.
    """
    given = kwargs.pop("arg_map", None)
    spec_map = SPEC.twin_arg_map

    def arg_map(name, args):
        mapped = spec_map(name, args) if spec_map is not None else args
        return mapped if given is None or mapped is None else given(name, mapped)

    return twin_mismatches(s_proj, sec_proj, codes=codes(sec_proj), arg_map=arg_map,
                           **kwargs)


def _lives(x):
    return (1, 2) if x.is_joint() else (1,)


def _sweep(proj):
    """Evaluate on an S point or an SEC row what the splice compares: the reports and more.

    ``result_cf()``, ``result_pols()`` and ``result_annual()``, and every ``check_*``, the
    survival check among them, which here restates the recursion a month at a time and so
    costs a cell a month.  Then the cells no report or check reaches, so that the
    comparisons see them too: ``guarantee_yrs``, ``qlac_flags``, ``accel_cost``,
    ``payout_factor_calc``, ``other_qlac_premium``, ``is_qlac`` and the label accessors,
    each covered life's ``sex``; over the frame ``phase``, ``duration_mth``,
    ``cola_factor`` and, in a blackout month, ``accel_payment_factor``; and over the months
    on the books, where a contract has an attained age, the calendar year and, for each
    covered life, the attained age, the base-table rate, the improvement rate and the
    deaths.  An S point is swept the same way, so what it caches is what T2 compares.
    """
    proj.result_cf()
    proj.result_pols()
    proj.result_annual()
    for name in proj.cells:
        if name.startswith("check_") and not name.endswith("_resid"):
            proj.cells[name]()
    for name in ("guarantee_yrs", "qlac_flags", "accel_cost", "payout_factor_calc",
                 "other_qlac_premium", "is_qlac", *LABELS):
        proj.cells[name]()
    lives = _lives(proj)
    for life in lives:
        proj.sex(life)
    entry = proj.t_entry() if "t_entry" in proj.cells else 0
    for t in range(proj.proj_len()):
        proj.phase(t)
        proj.duration_mth(t)
        proj.cola_factor(t)
        if proj.accel_blackout(t):
            proj.accel_payment_factor(t)
        if t < entry:
            continue
        proj.calendar_year(t)
        for life in lives:
            proj.age(t, life)
            proj.mort_rate_base(t, life)
            proj.improvement_rate(t, life)
            proj.lives_death(t, life)


def _after_the_exercise(p):
    """``{"accel_payment_factor"}`` on a row valued after its acceleration month, else
    nothing: the cell T2 exempts on that row.

    ``DIA_US_S`` reads the factor only in the exercise month, for the five instalments the
    lump sum pulls forward, and caches it at their months.  A row valued after the exercise
    paid the lump sum before the valuation date, its blackout months pay nothing, and from
    the valuation date on nothing reads the factor, which is 0.0 there; so S's cached
    values have no counterpart (``test_an_acceleration_needs_no_column``).
    """
    a = p.accel_mth()
    return {"accel_payment_factor"} if 0 <= a < p.duration_mth_init() else set()


def _years_on_the_books(month):
    """The ``arg_map`` for S's year-keyed display cells on a row restated at S month
    ``month``.

    ``lives_if_ann(y)`` and ``annuity_payments_ann(y)`` read the survival at the end of
    policy year ``y``, which a year that ended before the valuation date does not have on
    the valuation clock, so those keys are skipped; ``claims_ann(y, kind)`` sums the months
    of policy year ``y`` on the books, so a year begun before the valuation date is a part
    year here and skipped too.  Every other key, and every key of a future row, is a whole
    year on the books and compared.
    """
    def arg_map(name, args):
        if name in ("lives_if_ann", "annuity_payments_ann") and 12 * args[0] < month:
            return None
        if name == "claims_ann" and 12 * (args[0] - 1) < month:
            return None
        return args
    return arg_map


def _compared(s_proj, sec_proj, month, exempt):
    """Where row ``sec_proj``, restated at S month ``month``, departs from S cell by cell.

    In two passes (§5.2): every cell of S's but ``exempt``, :data:`RESIDUALS` and the cell
    :func:`_after_the_exercise` names, at every argument S cached inside its frame from
    month ``month`` on, to 1e-9 relative with no absolute floor; then the residuals alone,
    at the default floor of 1e-9.  The year-keyed display cells are compared on the years
    on the books (:func:`_years_on_the_books`).
    """
    exempt = exempt | _after_the_exercise(sec_proj)
    arg_map = _years_on_the_books(month)
    found = _mismatches(s_proj, sec_proj, t_offset=month, exempt=exempt | RESIDUALS,
                        arg_map=arg_map, atol=0.0)
    return found + _mismatches(s_proj, sec_proj, t_offset=month,
                               exempt=exempt | (set(s_proj.cells) - RESIDUALS),
                               arg_map=arg_map)


def _continues_s(s_proj, sec_proj, month, exempt=SPLICE_EXEMPT):
    """Where a committed row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison, on the committed model at the shipped assumptions: frame by
    frame, ``result_cf`` and ``result_pols``, then cell by cell over every cell of S's but
    ``exempt`` (:func:`_compared`), :data:`SPLICE_EXEMPT` on a row restated in force and
    :data:`FUTURE_EXEMPT` on one issued later.  The shipped 2.5% expense inflation steps by
    policy year in S and by valuation year here (D7), so :data:`INFLATED`'s three columns,
    and :data:`INFLATION_CELLS`, differ by design and are left out; the inflation test holds
    them.  Every other column and cell must agree, to 1e-9 with no absolute floor.
    """
    s_df = s_proj.result_cf()
    keep = [c for c in s_df.columns if c not in INFLATED]
    found = frame_mismatches(s_df, sec_proj.result_cf(), t_offset=month, columns=keep,
                             atol=0.0)
    found += frame_mismatches(s_proj.result_pols(), sec_proj.result_pols(),
                              t_offset=month, atol=0.0)
    return found + _compared(s_proj, sec_proj, month, exempt | INFLATION_CELLS)


def _case_id(kind, s_point, month):
    """A case's id: ``point14-d59``, or ``point8-k13`` if it is issued later."""
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
# releases left is collected (:func:`_refreeze`).
T2_CASES = tuple(_selected(SPLICES + IN_FORCE_TWINS, CORE_SPLICES))
LAST_OF_POINT = {case[1]: case for case in T2_CASES}


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


def _s_schedule_with_variants(schedule):
    """S's premium schedule with each variant's premiums, its base's rows under its own
    point_id."""
    rows = [schedule[schedule["point_id"] == base].assign(point_id=point_id)
            for point_id, (base, _) in VARIANTS.items()]
    return pd.concat([schedule, *rows], ignore_index=True)


def _s_copy(root):
    """A copy of S's product directory with the variants and the splice's edits; S's
    folder in it."""
    return temp_inputs(root, model_path(TWIN), model_points=_s_table_with_variants(),
                       edits={**SPLICED_EDITS,
                              "premium_schedule.csv": _s_schedule_with_variants})


def _sec_built(root, s, derived=(), future=(), edits=None):
    """SEC's inputs for a table the generator builds from S model ``s``: its folder.

    The registered spec with its rows replaced by ``derived`` and ``future``, built from
    ``s`` (``sec_support.build_sec_table``), written with its premium schedule into a copy
    of the product directory, with ``edits`` beside them.
    """
    spec = dataclasses.replace(SPEC, derived=tuple(derived), future=tuple(future))
    table, companions = build_sec_table(spec, s)
    assert set(companions) == {SCHEDULE}
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
    """DIA_US_SEC read in place, as committed, and swept once, cold; what it met.

    The model is first asked for ``duration_mth(500)`` on the twin of S point 2, and the
    keys that call leaves in ``duration_mth`` are kept.  Then every committed point is
    swept (:func:`_sweep`), in table order and each column in ascending ``t``, under a
    recursion limit lowered to :data:`CALL_DEPTH`, and whatever that raises is kept, point
    by point, rather than raised.  So the record says what a cold model does, which the
    clock and depth test asserts (D3, R2), and every test on the committed model reads a
    model already swept: the sweep is paid once, not once for each.  The swept model is
    then frozen out of the collector (:func:`_freeze`).  Returns ``(model, record)``.
    """
    model = _read(model_path(SEC), "sec")
    first = _row(model, "twin", 2, 0)
    record = {"duration_mth(500)": first.duration_mth(500),
              "keys": list(first.cells["duration_mth"].keys()), "deep": []}
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
    _freeze()
    yield model, record
    model.close()


@pytest.fixture(scope="module")
def sec_model(sec_read):
    """DIA_US_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """DIA_US_S read in place, as committed, with every point swept (:func:`_sweep`).

    T6 regenerates the SEC table and its premium schedule from it, which would otherwise
    project every S point again (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the
    in-force tests read S's months off it.  The swept model is then frozen out of the
    collector (:func:`_freeze`).
    """
    model = mx.read_model(model_path(TWIN), name=_name("s"))
    for key in point_keys(model):
        _sweep(projection(model, key))
    _freeze()
    yield model
    model.close()


@pytest.fixture(scope="module")
def spliced(tmp_path_factory):
    """S and SEC on the splice's inputs: ``(s, sec, s_later, events, every)``.

    S is read from a copy of the product directory whose table has the variants appended,
    whose premium schedule has their premiums, and whose mortality table and improvement
    scale are set apart (:data:`SPLICED_EDITS`), under :data:`SPLICED_REFS`, and every S
    point is swept (:func:`_sweep`) and stays swept.  SEC runs on the same assumption
    tables, and on a model point table and a premium schedule of its own, built by the
    generator from the registered spec with its rows replaced by the cases this run
    selects, the core or the full grid (:func:`_selected`), out of this S model, so each
    row opens with the state of the very run it is compared with.  SEC reads the table
    once, under :data:`SEC_REFS`, as a block is read, on one path of the reference rate,
    and each SEC row is projected by the case that compares it and released once compared.
    A row issued later is compared with ``s_later``, S read again from the same copy under
    :data:`LATER_REFS`, the same contract on that path; each of its points is swept by the
    T3 case that compares it and released with the row, so that ``s_later`` holds at most
    one swept point at a time.  The rows the product's own tests read on the splice's inputs
    (:data:`EVENT_ROWS`) are built into a table of their own from the same swept S model, in
    the folder ``events``, which the ``events`` fixture reads, so that no S point is
    projected again for them; and so are the states the every-state test restates,
    ``every`` (:func:`_every_state_table`), whose S points T2 releases before that test
    runs.

    Everything alive once S is swept, S's points among them, is then frozen out of the
    collector (:func:`_freeze`), so that the collection after each row's release scans only
    what the row made, not the swept S model the module holds.  Each S point is held swept
    until the last T2 case that compares a row of it, and released then, and once the last
    T2 case has run, what the releases left is returned to the collector and collected
    (:func:`_refreeze`): held to the end of the module, the swept S model would add 1.5 GB
    to it, under the two committed models' sweeps (measured at M12).
    """
    root = tmp_path_factory.mktemp("spliced")
    s_folder = _s_copy(root / "s")
    s = _read(s_folder, "s_spliced", SPLICED_REFS)
    for key in point_keys(s):
        _sweep(projection(s, key))
    derived = [(p, d) for kind, p, d in _selected(SPLICES, CORE_SPLICES)]
    sec_folder = _sec_built(root / "sec", s, derived, _selected(FUTURES, CORE_FUTURES),
                            SPLICED_EDITS)
    events = _sec_built(root / "events", s, EVENT_ROWS, EVENT_FUTURES, SPLICED_EDITS)
    every = _every_state_table(root / "every", s, SPLICED_EDITS)
    sec = _read(sec_folder, "sec_spliced", SEC_REFS)
    s_later = _read(s_folder, "s_spliced_later", LATER_REFS)
    _freeze()
    yield s, sec, s_later, events, every
    s_later.close()
    sec.close()
    s.close()


@pytest.fixture(scope="module")
def splice_records():
    """What each splice row was found to do, by case (:func:`_record`)."""
    return {}


# The rows the product's own tests read on the splice's inputs, whatever the grid: around
# the acceleration of point 14 and the commutation of point 15 and its variants, the income
# start of point 7, the month before each cap binds, the generational point in payout, the
# COLA cash refund past its first COLA anniversary, its refund still running, the anchor on
# an anniversary, and the anchor issued 13 months on.
EVENT_ROWS = ((1, 12), (7, 240), (8, 647), (10, 265), (14, 251), (14, 252), (14, 253),
              (15, 240), (15, 251), (15, 252), (15, 253), (15, 360), (16, 240), (18, 683),
              (21, 252), (26, 250), (26, 252), (30, 479), (32, 365), (32, 390), (35, 252))
EVENT_FUTURES = ((1, 13),)


@pytest.fixture(scope="module")
def events(spliced):
    """SEC on the splice's inputs, its table the generator's for :data:`EVENT_ROWS`.

    Built by the ``spliced`` fixture from the splice's S model, swept, and read under
    :data:`SEC_REFS`, as the splice's own table is, so each row opens with the state of the
    very run it is compared with.  Each test projects the rows it reads and releases them.
    """
    sec = _read(spliced[3], "events", SEC_REFS)
    yield sec
    sec.close()


# ---------------------------------------------------------------------------
# The splice's records
#
# Each T2 and T3 case sweeps its row, records what the rules test and the core grid's reach
# need of it, compares it with S, and releases it: held together, the rows of the full grid
# would hold several gigabytes.  The record is made before the comparison, because the
# comparison evaluates SEC's cells at S's own cached arguments, and those include keys SEC
# never reads itself: S's instalments scheduled to date from policy month 0, S's pricing at
# the premium months already paid, S's survival from issue.  Comparing them would plant
# those keys in SEC's cache, for the rules test to report as SEC's.  So each of the two
# tests reads the records, and computes any case no earlier test has recorded, which keeps
# it whole when run alone.


def _cached_args(cells):
    """The argument tuple of every key ``cells`` has cached (:func:`sec_support._args`)."""
    n = len(cells.parameters)
    return [() if n == 0 else (key,) if n == 1 else tuple(key)
            for key in list(cells.keys())]


def _month(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _contract(p):
    """The arguments each policy-clock and age-keyed cell may take on row ``p``.

    ``({cell: (lowest, highest)}, {life: (lowest age, highest age)})``.  The policy clock
    runs from issue to the stop rule, ``stop_mth()``, and a little past it, where an
    acceleration in a contract's last months pulls five instalments forward, and the
    pricing kernel reads survival to the mortality horizon, ``horizon_mths()``: so the
    pricing survival, the schedule by policy month, its payment months, COLA and certain
    floor are read at policy months 0 to the later of the two, ``reach``, and the annual
    rate at policy years 1 to ``reach``'s.  The premiums and the pricing of each premium
    at policy months 0 to ``stop_mth() - 1``, the pricing curve's last-survivor exposure
    from issue to the later income start month, and the instalments scheduled to date from
    the month before the income start month in force to the later of the horizon and the
    last month.  The year-keyed display cells at the policy years of the frame, from the
    valuation date's.  The age readers are read for a covered life at ages from its issue
    age to the last below omega: at and above it the rate cells answer without them.  Each
    is a function of the point, so the ranges hold on every row, in force or not.
    """
    stop, horizon = p.stop_mth(), p.horizon_mths()
    start = p.income_start_mth()
    reach = max(horizon, stop + p.accel_months - 1)
    years = (reach - 1) // 12 + 1
    first = p.duration_mth(p.t_entry()) // 12 + 1
    lives = (1, 2) if p.is_joint() else (1,)
    ages = {life: (p.age_at_entry(life), p.omega_age - 1) for life in lives}
    ranges = {name: (0, stop - 1) for name in (
        "premium_pm", "income_start_mth_at", "deferral_yrs", "surv_to_income_start",
        "rop_factor_calc", "rop_factor", "annuity_factor_def", "purchase_rate",
        "rop_deferral_yrs")}
    ranges["annuity_factor_at"] = (0, max(stop - 1, start, p.income_start_mth_init()))
    ranges.update({name: (0, reach) for name in (
        "lives_if_pm", "is_payment_pm", "cola_factor_pm", "annuity_pp_sched_pm",
        "certain_floor_pm")})
    ranges.update({"mort_rate_py": (1, years), "mort_rate_mth_py": (1, years),
                   "lives_if_last_pm": (0, max(start, p.income_start_mth_init())),
                   "cum_annuity_pp": (start - 1, max(horizon, stop - 1))})
    ranges.update({name: (first, stop // 12) for name in (
        "lives_if_ann", "claims_ann", "annuity_payments_ann")})
    return ranges, ages


def _outside_contract(p):
    """Each cached argument of a policy-clock or age-keyed cell not in :func:`_contract`."""
    ranges, ages = _contract(p)
    found = []
    for name, (lo, hi) in ranges.items():
        found += [f"{name}{args}, outside {lo}..{hi}"
                  for args in _cached_args(p.cells[name])
                  if not (_month(args[0]) and lo <= args[0] <= hi)]
    for name in AGE_READERS:
        for args in _cached_args(p.cells[name]):
            x, life = args
            if life not in ages or not ages[life][0] <= x <= ages[life][1]:
                found.append(f"{name}{args}, outside ages {ages}")
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
    ``surv_to_payout()`` or ``certain_mths_refund()``, as far as the dependency graph
    goes: so a read that looks ahead through a cell taking no ``t`` is the reader's.
    ``reach`` holds what each call keyed by no month reads, so that each is walked once a
    row, and the walk is a loop, not a recursion, since a schedule summed by policy month
    can be hundreds of calls deep.
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
                    found |= reach[(id(pred.obj), pred.args)]
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
    call keyed by a month at or after it reads; every call keyed by a month beyond ``t + 1``
    that a call keyed by ``t`` reads; and every policy-clock or age argument the contract
    does not have (:func:`_contract`).  A call reads its precedents, as modelx's dependency
    graph records them, and, through a precedent keyed by no month, whatever that
    precedent reads in turn (:func:`_months_read`): ``payment_factor(t)`` reading
    ``surv_to_payout()``, which reads ``lives_if_last`` at the income start month, reads
    that month.  DIA admits no look-ahead at all.
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


def _step(x):
    """The months from one instalment to the next on row ``x``."""
    return 12 // x.payment_freq()


def _off_period(x):
    """Whether row ``x`` is valued between two of its instalment dates, off its period:
    its months from the income start month to the valuation date are not a whole number of
    payment steps."""
    return (x.duration_mth_init() - x.income_start_mth()) % _step(x) != 0


def _refund_form(x):
    return x.is_cash_refund() or x.is_installment_refund()


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, every opening-state column in use, at
# every value it takes: two fractional lives, one life of a joint contract dead, every life
# dead inside a guarantee, the guarantee-period column pricing a premium still due and an
# adjustment still to come, each frozen weight read where it weighs an instalment, and a
# change in the reference rate already seen, on a point whose commutation it discounts;
# then what falls at t = 0 because of where the contract stands: a premium, the
# adjustment, the lump sum, a blackout month, the commutation and one with nothing to
# commute, the income start, a refund, the advance refund balance, a payment month off
# monthly and a month between instalments.  Later in the frame, every branch of the refund,
# the derived and elected guarantees, the commutation and the acceleration, each valued
# off its period where its frequency is below monthly (a row valued on its period would
# hide a payment month counted from the wrong clock), the cap below omega, omega inside a
# guarantee, a QLAC complying and each of the six conditions a QLAC fails, and a slice
# priced to an adjusted income start month.
AT_VALUATION = {
    "two fractional lives": lambda x: (
        x.is_joint() and 0.0 < x.lives_if_init(1) < 1.0 and 0.0 < x.lives_if_init(2) < 1.0),
    "one life of a joint contract dead": lambda x: (
        x.is_joint() and (x.lives_if_init(1) == 0.0) != (x.lives_if_init(2) == 0.0)),
    "every life dead in a guarantee": lambda x: (
        x.lives_if_last(0) == 0.0 and x.certain_floor(0) == 1.0),
    "the n_g column pricing a premium still due": lambda x: (
        _refund_form(x) and x.is_formula_basis() and x.duration_mth_init() > 0
        and any(k >= x.duration_mth_init() for k in x.premium_by_mth())),
    "the n_g column pricing an adjustment still to come": lambda x: (
        _refund_form(x) and 0 < x.duration_mth_init() <= x.adjust_mth()),
    "l_last(T) from the column weighting a guarantee": lambda x: (
        x.duration_mth_init() > x.income_start_mth() and x.certain_floor(0) == 1.0),
    "l_last(T) derived at t = 0, weighting a guarantee": lambda x: (
        x.duration_mth_init() == x.income_start_mth() and x.certain_mths_eff() > 0),
    "l_last(T) derived ahead of t = 0, weighting a guarantee": lambda x: (
        0 < x.duration_mth_init() < x.income_start_mth() and x.certain_mths_eff() > 0),
    "l_last(t_c) from the column": lambda x: (
        0 <= x.commute_mth() < x.duration_mth_init() and x.commute_weight(0) > 0.0),
    "a rate change seen, on a commuting point": lambda x: (
        x.ref_rate_shift_init() != 0.0 and x.duration_mth_init() <= x.commute_mth()
        and x.commuted_value(x.commute_mth() - x.duration_mth_init()) > 0.0),
    "a premium at t = 0": lambda x: x.duration_mth_init() > 0 and x.premium_pp(0) > 0.0,
    "the adjustment at t = 0": lambda x: x.duration_mth(0) == x.adjust_mth(),
    "the lump sum at t = 0": lambda x: x.duration_mth(0) == x.accel_mth(),
    "a blackout month at t = 0": lambda x: x.accel_blackout(0),
    "the commutation at t = 0": lambda x: (
        x.duration_mth(0) == x.commute_mth() and x.commuted_value(0) > 0.0),
    "a commutation month with nothing to commute": lambda x: (
        x.duration_mth(0) == x.commute_mth() and x.commuted_value(0) == 0.0),
    "the income start month at t = 0": lambda x: (
        x.duration_mth(0) == x.income_start_mth()),
    "a refund at t = 0": lambda x: x.claims(0, _code(x, "REFUND")) > 0.0,
    "the advance refund balance at t = 0": lambda x: (
        not x.is_arrears() and x.is_payment_mth(0)
        and x.claims(0, _code(x, "REFUND")) > 0.0),
    "a payment month at t = 0, off monthly": lambda x: (
        x.payment_freq() != 12 and x.is_payment_mth(0)),
    "a month between instalments at t = 0": lambda x: (
        x.is_payout(0) and not x.is_payment_mth(0)),
}
IN_FRAME = {
    "a premium in the frame": lambda x, t: t > 0 and x.premium_pp(t) > 0.0,
    "the deferral death benefit": lambda x, t: x.claims(t, _code(x, "DEATH")) > 0.0,
    "the refund running out": lambda x, t: (
        x.is_cash_refund() and x.refund_balance(t) > 0.0 and x.is_active(t + 1)
        and x.refund_balance(t + 1) == 0.0),
    "the derived period ending": lambda x, t: (
        x.is_installment_refund() and x.certain_floor(t) == 1.0
        and x.certain_floor(t + 1) == 0.0),
    "an elected guarantee ending": lambda x, t: (
        x.is_period_certain() and x.certain_floor(t) == 1.0
        and x.certain_floor(t + 1) == 0.0),
    "the life tail resuming after a commutation": lambda x, t: (
        x.commute_frac_cum(t) > 0.0 and x.certain_floor(t) == 0.0
        and x.annuity_payments(t) > 0.0),
    "an acceleration straddling a guarantee's end": lambda x, t: (
        x.duration_mth(t) == x.accel_mth() and x.certain_floor(t) == 1.0
        and x.certain_floor_pm(x.accel_mth() + x.accel_months - 1) == 0.0),
    "an acceleration on life-contingent instalments": lambda x, t: (
        x.duration_mth(t) == x.accel_mth() and x.certain_floor(t) == 0.0
        and x.annuity_payments(t) > 0.0),
    "an acceleration on guaranteed instalments, l_last(T) derived": lambda x, t: (
        x.duration_mth(t) == x.accel_mth() and x.certain_floor_pm(x.accel_mth() + 1) == 1.0
        and x.duration_mth_init() <= x.income_start_mth()),
    "an acceleration in a commuted guarantee's last month": lambda x, t: (
        x.duration_mth(t) == x.accel_mth() and x.commute_frac_cum(t) > 0.0
        and x.certain_floor(t) == 1.0 and x.certain_floor(t + 1) == 0.0),
    "a commutation inside a derived period": lambda x, t: (
        x.is_installment_refund() and x.commuted_value(t) > 0.0),
    "a refund, valued off its period": lambda x, t: (
        _off_period(x) and x.claims(t, _code(x, "REFUND")) > 0.0),
    "a certain instalment, valued off its period": lambda x, t: (
        _off_period(x) and x.certain_floor(t) == 1.0 and x.annuity_payments(t) > 0.0),
    "the cap below omega": lambda x, t: any(
        x.mort_rate(t, life) == 1.0 and x.age(t, life) < x.omega_age for life in _lives(x)),
    "omega inside a guarantee": lambda x, t: (
        x.certain_floor(t) == 1.0 and x.age(t, 1) >= x.omega_age
        and x.mort_rate(t, 1) == 1.0),
    "a QLAC complying": lambda x, t: x.is_qlac() and x.qlac_flags() == [],
    **{f"the QLAC condition: {flag}": (lambda x, t, flag=flag: flag in x.qlac_flags())
       for flag in ("premium limit exceeded", "income start after the age limit",
                    "cost-of-living adjustment on a QLAC", "commutation on a QLAC",
                    "payment acceleration on a QLAC",
                    "income form not permitted on a QLAC")},
    "a slice priced to an adjusted start": lambda x, t: (
        x.premium_pp(t) > 0.0 and 0 <= x.adjust_mth() <= x.duration_mth(t)),
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
    opening state is each life alive, nothing paid or bought, nothing frozen and no change
    in the reference rate.  The row is read in the splice's one read of its table, with
    SEC's ``ref_rate_shift`` at 0 (:data:`SEC_REFS`), so its commutation discount rate is
    S's only if it reads the change it carries.  For the same reason it is the test that
    catches a policy month passed as ``t`` (R1a): the premium months, the income start
    month, the payment months, the certain period, the option months and the refund balance
    all read the policy clock.  The frame comparisons read SEC row ``t`` against S row
    ``t + d`` in every column of ``result_cf`` and every column of ``result_pols`` both
    reports hold, and fail frames that end apart.  The cell comparison then evaluates every
    cell of S's but :data:`SPLICE_EXEMPT`, at every argument S cached inside its own frame
    from month ``d`` on, moved onto SEC's clock, to 1e-9 relative with no absolute floor
    (:func:`_compared`): each life's survival, the premiums paid and the income bought, the
    pricing of each premium still due at its policy month, the instalments scheduled to
    date at every policy month S read them, the counts and the payment factors among them.
    The floor would hide what matters near the limiting age, where a capped rate kills
    lives whose survival is near 1e-8.  The four roll-forward residuals are compared at the
    floor, since they are rounding around 0.  An S cell this model lacked would fail it.

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
        for report in REPORTS:
            assert frame_mismatches(s_proj.cells[report](), sec_proj.cells[report](),
                                    t_offset=month, atol=0.0) == [], report
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

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at the stop rule, in
    ``result_cf`` and in every column of ``result_pols`` S's has, and every cell of S's but
    :data:`FUTURE_EXEMPT` agrees at every argument S cached inside its own frame, moved
    ``k`` later, to 1e-9 relative with no absolute floor, the residuals at the floor.  A
    future row holds its whole premium schedule and whole policy years, so its premiums by
    month and its annual display are compared too.  The row is read in the splice's one
    read of its table (:data:`SEC_REFS`) and compared with S read with its
    ``ref_rate_shift`` at 0 (:data:`LATER_REFS`): bought after the valuation date, the
    contract has seen no change in the reference rate on the block's path, and S's point is
    the same contract on it.  An S cell this model lacked would fail it.  Before issue
    every column of ``result_cf`` and ``result_pols`` is an exact zero, and the contracts
    arrive in month ``k`` as new business, bringing the first premium.

    The last assertions are R1 and D4's base rule made testable.  After every report, no
    decrement rate keyed by month has been evaluated at a month before issue, and neither
    age reader has been read below an issue age.  A survival recursion based at ``t == 0``
    rather than at ``t_entry()``, which carries each life at 1 through the months before,
    or a rate that evaluates its table before asking whether the month is in cover, still
    gives the right numbers.  The rules test's look-back and the guard test see the first
    too, and the guard test the second.

    The pre-issue rows are asserted present before they are asserted zero: a frame that
    opened at issue would have none, its zeros would hold of nothing, and the comparisons
    with S, which start there, would not see it.  The row is swept and recorded for the
    rules test first (:func:`_record`), and released after, with the S point it was
    compared with, swept here.
    """
    s_later, sec = spliced[2], spliced[1]
    case = ("future", s_point, -k)
    key, s_key = _row_key(sec, *case), _key(s_later, s_point)
    try:
        sec_proj = projection(sec, key)
        splice_records[case] = _record(case, sec_proj)
        s_proj = projection(s_later, s_key)
        _sweep(s_proj)
        df, pols = sec_proj.result_cf(), sec_proj.result_pols()
        assert frame_mismatches(s_proj.result_cf(), df, t_offset=-k, atol=0.0) == []
        assert frame_mismatches(s_proj.result_pols(), pols, t_offset=-k, atol=0.0) == []
        assert _compared(s_proj, sec_proj, -k, FUTURE_EXEMPT) == []
        for report, frame in (("result_cf", df), ("result_pols", pols)):
            assert list(frame.index[:k]) == list(range(k)), report
            assert (frame.loc[:k - 1] == 0.0).all().all(), report
        assert sec_proj.pols_new_biz(k) == sec_proj.policy_count() == 1.0
        assert sec_proj.premiums(k) == s_proj.premiums(0) > 0.0
        early = {name: sorted(args for args in _cached_args(sec_proj.cells[name])
                              if args[0] < k)
                 for name in DECREMENT_RATES}
        assert not any(early.values()), f"rates evaluated before issue: {early}"
        for name in AGE_READERS:
            low = [(x, life) for x, life in _cached_args(sec_proj.cells[name])
                   if x < sec_proj.age_at_entry(life)]
            assert not low, f"{name} read below an issue age: {low[:5]}"
    finally:
        _release(sec, key)
        if s_key in s_later.Projection.itemspaces:
            _release(s_later, s_key)
        gc.collect()


# ---------------------------------------------------------------------------
# D11's R1, R1a and R2, and D3's closed-form clock


@pytest.mark.parametrize("grid", [pytest.param("core", id="core"),
                                  pytest.param("full", id="full", marks=FULL_ONLY)])
def test_no_cell_is_called_before_the_valuation_date_or_reads_far_ahead(spliced,
                                                                        splice_records,
                                                                        grid):
    """R1, its look-back, R1a's ranges and R2's look-ahead, on the rows T2 and T3 compare.

    Each is a rule of how the model computes, not of what, so no number shows a breach,
    and on a point issued at ``t = 0`` the two clocks coincide and hide it from T1 too.
    The splice's rows are points in force at every month T2 names, the variants among
    them, and points issued later, and each was swept first:

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and
      a compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  A policy
      month turned into ``t`` by subtracting ``duration_mth_init()`` (R1a) goes negative on
      a point past it: the income start month, a premium month or an option month on a
      contract valued after it, and the ``-1`` an option accessor returns for "never".  So
      does a survival, premium or income recursion based at ``t == 0`` but read a month
      back from it.
    * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
      ``t_entry()`` on read a month before it.  On a point issued later a recursion based
      at ``t == 0`` reads the months before, where each life is carried at 1 and nothing
      is paid, so no number shows it and no argument goes negative.
    * R1a's ranges: every argument of a cell keyed by the policy clock, a policy year or an
      age is one the contract has (:func:`_contract`): the premiums and their pricing, the
      pricing survival and the annual rate by policy year, the payout schedule by policy
      month and the instalments scheduled to date, the display years from the valuation
      date's, and the two age readers from each life's issue age to the last below omega.
      A schedule read at a policy month before issue, an age table read past omega, or a
      cache sized from the contract read beyond it would wrap round in a compiled model.
    * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month beyond
      ``t + 1``, as modelx's dependency graph records each cached call's precedents, read
      directly or through a precedent keyed by no month, which is followed to the
      month-keyed calls it reads (:func:`_months_read`): ``surv_to_payout()``, read in
      every month, would read ``lives_if_last`` at the income start month from the
      deferral.  ``DIA_US_S``'s refund, commuted value and acceleration read the schedule
      at months ahead of ``t`` as ``annuity_pp_sched(s)``, and its commutation residual
      reads every guaranteed month still to come; here they read the schedule by policy
      month, which no frame index ahead of ``t`` keys, and the residual is measured where
      the guarantee ends, reading back.  DIA admits no look-ahead.

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

    * D3: the policy clock is the closed form.  Called first, ``duration_mth(500)``
      evaluates ``duration_mth`` once, where ``BasicTerm_SE``'s recursion would evaluate
      it at all 501 months from 0.
    * R2's recursions run forward: under modelx's recursion limit lowered to
      :data:`CALL_DEPTH`, every committed point is swept, each column in ascending ``t``.
      A forward recursion, through ``t - 1``, finds the month before already cached and
      stays shallow, which is why D3 is asserted on its own.  So do the schedules read by
      policy month, because each is based where it is first read: the instalments scheduled
      to date at the valuation date's policy month, by one loop over the payout months
      before it, so the anchor in its last month reads them without recursing back 478
      months to its income start month; and the pricing survival and the payout income by
      a loop from issue and from the valuation date.  A backward recursion over the frame,
      through ``t + 1``, keeps every step within the look-ahead but opens a chain as long
      as the frame, which a compiled model would run on the C stack (F7), and fails here.
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


def _extended(column, low=CONTRACT_MIN_AGE):
    """An edit of an age table that adds the ages from ``low``, 0 unless given, to 19,
    below its first.

    The shipped tables start at 20.  The added rows are geometric in age and apart by sex,
    a distinct value at every ``(age, sex)``, so that a read at the wrong age or sex
    changes a number.
    """
    def edit(df):
        rows = []
        for sex, scale in (("M", 1.0), ("F", 0.97)):
            first = float(df.loc[(df["age"] == 20) & (df["sex"] == sex), column].iloc[0])
            rows += [{"age": age, "sex": sex, column: first * 0.94 ** (20 - age) * scale,
                      "provenance": "[std] extended below 20 for a depth test"}
                     for age in range(low, 20)]
        return pd.concat([pd.DataFrame(rows), df], ignore_index=True)
    return edit


# The age tables from age 0, the contract's youngest issue age, issue_age_min, which the
# longest cover reads.
FROM_AGE_0 = {"mort_table.csv": _extended("mort_rate"),
              "improvement_scale.csv": _extended("improvement_rate")}


def _longest_cover():
    """The two points at the contract's longest cover from issue, their premiums, and the
    tables they need.

    S point 5's twin, the installment refund, at the contract's youngest issue age,
    :data:`CONTRACT_MIN_AGE`, 0, with its income from policy month 360: 1,440 months to
    the age stop, through which each life's survival runs, and the refund-period search
    over its payout schedule from issue.  Once issued at the valuation date and once 120
    months on, the longest frame, 1,560 months.  Each takes point 5's premiums, and both
    read the age tables from age 0 (:data:`FROM_AGE_0`).
    """
    row = _committed().loc[[5]].assign(issue_age=CONTRACT_MIN_AGE, income_start_mth=360)
    rows = pd.concat([row, row.assign(duration_mth=-120, policy_id="DIA-000005-F120",
                                      row_kind="future", source_mth=-120)])
    rows.index = pd.Index([1, 2], name="point_id")
    premiums = _committed_schedule()
    premiums = premiums[premiums["point_id"] == 5]
    schedule = pd.concat([premiums.assign(point_id=1), premiums.assign(point_id=2)],
                         ignore_index=True)
    return rows, schedule, FROM_AGE_0


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_the_deepest_cold_call_runs_one_cell_a_month(tmp_path):
    """A cold ``net_cf`` in the last month runs one cell a month back to ``t_entry`` (D5),
    and a cold first month runs a handful of cells deep.

    On a model just read, nothing is cached, so ``net_cf(proj_len() - 1)`` runs each chain
    from the end of the frame back to the first month on the books, each life's survival,
    the premiums paid and the income bought, and modelx's stack trace counts how deep.
    Each chain may be one cell a month and no more, plus at most :data:`CHAIN_OVERHEAD`
    cells above and below it: on the twins of the anchor, the installment refund and the
    joint point, 720 months; on the anchor a month into its income phase, whose refund
    reads the instalments scheduled to date back to the valuation date's policy month, and
    no further; on the joint point issued 13 months on; and at the contract's longest cover
    from issue (:func:`_longest_cover`), 1,440 months from issue age 0, issued at the
    valuation date and 120 months on.  No number shows the depth, and a compiled model runs
    the chain on the C stack, so a chain of two cells a month, which gives the same
    numbers, needs twice the stack (F7).  A future point's chain stops at ``t_entry()``, so
    the longest frame, 1,560 months, runs no deeper than the cover it holds.

    And a cold ``net_cf(0)`` runs at most :data:`FIRST_MONTH_DEPTH` cells deep on the twins
    of the anchor, the installment refund and the start-date adjustment and on the point in
    deferral with a premium due: the first month reads ``l_last(T)`` only where a certain
    floor pays it, and the installment refund prices its premiums for its stop rule by
    loops from issue (R2, F7), where ``DIA_US_S``'s first month recurses through its
    survival to the income start month, 251 cells on the anchor and 311 on the adjustment.
    A floor weight read in deferral, or a pricing survival written as a recursion, gives the
    same numbers, and fails here.
    """
    rows, schedule, tables = _longest_cover()
    refund = _label(_committed(), "derived", 1, 241)
    later = _label(_committed(), "future", 8, -13)
    reads = [("committed", model_path(SEC), [1, 5, 8, refund, later]),
             ("longest", _sec_inputs(tmp_path, rows, tables, schedule), [1, 2])]
    found, depths = [], {}
    for where, folder, labels in reads:
        for label in labels:
            fresh = _read(folder, "depth")
            try:
                p = _point(fresh, label)
                last = p.proj_len() - 1
                depth = _cold_depth(p, "net_cf", (last,))
                depths[where, label] = depth
                allowed = last - p.t_entry() + CHAIN_OVERHEAD
                if depth > allowed:
                    found.append(f"{where} point {label}: net_cf({last}) cold runs {depth} "
                                 f"cells deep, beyond {allowed}, one a month back to "
                                 f"t_entry() {p.t_entry()} and {CHAIN_OVERHEAD} more")
            finally:
                fresh.close()
    deferred = _label(_committed(), "derived", 14, 59)
    for label in (1, 5, 13, deferred):
        fresh = _read(model_path(SEC), "first")
        try:
            depth = _cold_depth(_point(fresh, label), "net_cf", (0,))
            if depth > FIRST_MONTH_DEPTH:
                found.append(f"point {label}: net_cf(0) cold runs {depth} cells deep, "
                             f"beyond {FIRST_MONTH_DEPTH}")
        finally:
            fresh.close()
    assert not found, found
    assert depths["longest", 1] > 1440 - CHAIN_OVERHEAD, (
        f"the longest cover ran {depths['longest', 1]} cells deep: the depth test did not "
        f"reach it")


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and so is the new business
# entering once at its policy_count; neither is repeated here.


def test_the_count_is_on_the_books_from_issue_to_the_stop_rule(sec_model):
    """The count weights every month from issue to the stop rule, undecremented.

    DIA_US_S weights every flow by its constant ``pols_if_init`` and carries mortality in
    each life's survival, and so does this model: under independence the two lives'
    probabilities are the whole survival state, which a count weighted by survival could
    not carry.  So on every committed point ``pols_if_at(t, "BEF_DECR")``, the count
    weighting month ``t``, is ``policy_count()`` at every ``t`` from ``t_entry()`` to the
    last row and 0 before, and ``"BEF_NB"`` opens at ``t_entry()`` at ``pols_if_init()``,
    the count in force at the valuation date, 0 on a point not yet in force.  The count
    leaves the books once, at the stop rule: ``BEF_DECR(t) - BEF_NB(t + 1)`` is 0 inside
    the frame and the whole count at the last row, whose next month, ``t = proj_len()``,
    is outside cover.  No maturity cell is needed for it, since nothing decrements the
    count.  ``result_pols()`` puts its columns in :data:`RESULT_POLS`'s order, over the
    frame.  And a timing neither model knows is refused rather than answered with another
    count.
    """
    nb = _code(sec_model.Projection, "BEF_NB")
    decr = _code(sec_model.Projection, "BEF_DECR")
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        entry, n, count = p.t_entry(), p.proj_len(), p.policy_count()
        assert [p.pols_if_at(t, decr) for t in range(n)] == (
            [0.0] * entry + [count] * (n - entry)), point_id
        assert p.pols_if_at(entry, nb) == p.pols_if_init(), point_id
        assert p.pols_if_init() == (count if p.duration_mth_init() > 0 else 0.0), point_id
        moved = [p.pols_if_at(t, decr) - p.pols_if_at(t + 1, nb) for t in range(entry, n)]
        assert moved == [0.0] * (n - 1 - entry) + [count], point_id
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(n)), point_id
    _refused(lambda: projection(sec_model, point_keys(sec_model)[0]).pols_if_at(
        0, "BEF_MAT"), "invalid timing")


def test_pols_if_is_the_count_weighted_by_survival(sec_model):
    """``pols_if(t)`` is the count on the books weighted by survival, not ``BEF_DECR``.

    On every committed point and at every ``t`` of its frame, ``pols_if(t)`` is exactly
    ``pols_if_at(t, "BEF_DECR") * lives_if_last(t)``: the contracts on the books weighted
    by the probability that a covered life is alive at the start of month ``t``,
    ``DIA_US_S``'s ``pols_if_init * l_last(t)`` on the count on the books, which carries
    the maintenance expense.  It differs from the count that weights the row wherever
    survival is below 1: on the period certain in force 300 months, ``pols_if(0)`` is 0.5577
    against a count of 1, on the commuting contract a month after its commutation 0.677527,
    and on the joint point with its joint annuitant dead 4.25e-05.  That is why the
    registry marks the model ``survival_pols_if`` and the convention that ``pols_if`` is
    ``BEF_DECR`` skips it (D5).
    """
    decr = _code(sec_model.Projection, "BEF_DECR")
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            assert p.pols_if(t) == p.pols_if_at(t, decr) * p.lives_if_last(t), (point_id, t)
    for s_point, month, value in ((7, 300, 0.5577), (15, 253, 0.677527),
                                  (8, 672, 4.245667e-05)):
        p = _row(sec_model, "derived", s_point, month)
        assert p.pols_if(0) == pytest.approx(value, rel=1e-6, abs=0.0), (s_point, month)
        assert p.pols_if_at(0, decr) == p.policy_count() == 1.0
        assert p.pols_if(0) < p.pols_if_at(0, decr)


def test_result_pols_is_s_report_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's, column for column, with ``pols_new_biz`` beside it (D5).

    T1 skips the report as a whole, because its frame has a column S's lacks (the spec's
    exempt), so it is compared here, on every twin, at offset 0.  Its columns are
    :data:`RESULT_POLS`: ``pols_if`` first, as ``BasicTerm_SE`` sets its counts out, where
    ``DIA_US_S`` has it last, then ``pols_new_biz``, the contracts issued in the month, then
    S's other seven in S's order.  Every column S's report has agrees, to 1e-9 with no
    absolute floor, frames ending together, and ``pols_new_biz`` holds the count in the
    month the contract is issued and 0 in every other.  Counts and survival carry no
    inflation, so the shipped assumptions serve.
    """
    table = sec_model.Data.model_point_table()
    twins = table.index[table["row_kind"] == "twin"].tolist()
    assert twins == sorted(s_model.Data.model_point_table().index)
    for point_id in twins:
        p = _point(sec_model, point_id)
        mine, theirs = p.result_pols(), _point(s_model, point_id).result_pols()
        assert list(mine.columns) == RESULT_POLS, point_id
        assert sorted(theirs.columns) == sorted(c for c in RESULT_POLS
                                                if c != "pols_new_biz"), point_id
        assert frame_mismatches(theirs, mine, atol=0.0) == [], point_id
        assert list(mine["pols_new_biz"]) == [
            p.policy_count() if t == 0 else 0.0 for t in mine.index], point_id


# What T4 multiplies policy_count by: not a whole number, because a count of contracts need
# not be one, so that a flow which read the count as whole contracts would not follow it.
COUNT_FACTOR = 2.5

# The twins T4 and the extract test project beside every row in force or issued later: the
# anchor on the table basis, the installment refund, the joint point and the commuting
# point.  Between them those rows carry every flow (the premiums, the death benefit, the
# refund, the instalments, an acceleration's lump sum and a commutation), every
# opening-state column, the count in force and new business.  The other twins are T1's.
FLOW_TWINS = (1, 5, 8, 15)


def _flow_points(table):
    """The labels of ``table``'s rows that T4 and the extract test project."""
    return [p for p in table.index
            if table.at[p, "row_kind"] != "twin" or p in FLOW_TWINS]


def test_scaling_the_count_scales_every_flow_and_no_per_contract_value(tmp_path):
    """``policy_count`` is a weight: 2.5 times the count, 2.5 times every flow, the same per
    contract.

    The committed table, and a copy with every count multiplied by :data:`COUNT_FACTOR`,
    are each read with :data:`SWITCHED_ON` set before either computes anything: the one
    assumption that ships at zero, the reference rate's change, switched on at the
    splice's value, so that the commutation is discounted at a moved rate on every point
    on the books.  On every point ``result_cf`` and the counts of ``result_pols`` are 2.5
    times the committed table's, element by element, to 1e-12 relative: a scaled count is a
    computed float, which may come back from the CSV within two ulps (``sec_support``'s
    module docstring).  So is every other cell of :data:`COUNTED`, at every argument the
    sweep of the committed table's point cached: the gross outgo, the annual claims and
    income, the counts at each timing and the commutation residual among them, the
    residual, rounding around 0, at a floor of 1e-9.  ``result_pols``'s seven probabilities
    and factors are the committed table's exactly, and so are ``result_annual``'s age,
    premium, CP, B and survival, its claims and income 2.5 times.  And every cell outside
    :data:`COUNTED` (the instalment, the refund, the commuted value per contract, the
    instalments scheduled to date, each life's survival, the opening state, the pricing,
    the rates, both clocks, the flags) agrees at every argument that sweep cached.  So a
    flow that dropped the count, or read it as whole contracts, which a table of counts of
    1 hides from every comparison with S, fails here.  Each counted cell is nonzero on some
    point: the premiums, the death benefit and the refund, the instalments, the lump sum
    of an acceleration and a commutation among them.  The points are every row in force or
    issued later and the twins that carry each flow beside them (:data:`FLOW_TWINS`), each
    released once compared.
    """
    table = _committed()
    base = _read(_sec_inputs(tmp_path / "base", table), "counted", SWITCHED_ON)
    scaled = _read(_sec_inputs(tmp_path / "scaled", table.assign(
        policy_count=COUNT_FACTOR * table["policy_count"])), "scaled", SWITCHED_ON)
    counted = sorted(COUNTED - set(REPORTS) - {"result_annual"})
    nonzero = set()
    try:
        for point_id in _flow_points(table):
            key, scaled_key = _key(base, point_id), _key(scaled, point_id)
            one, many = projection(base, key), projection(scaled, scaled_key)
            _sweep(one)
            for report in REPORTS:
                b, d = one.cells[report](), many.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                flows = [c for c in b.columns if c not in RATES]
                bad = ((d[flows] - COUNT_FACTOR * b[flows]).abs()
                       > 1e-12 * (COUNT_FACTOR * b[flows]).abs()).any()
                assert not bad.any(), (key, report, list(bad[bad].index))
                nonzero |= {c for c in flows if (b[c] != 0.0).any()}
                rates = [c for c in b.columns if c in RATES]
                assert d[rates].equals(b[rates]), (key, report)
            b, d = one.result_annual(), many.result_annual()
            assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
            for c in b.columns:
                want = COUNT_FACTOR * b[c] if c in ANNUAL_COUNTED else b[c]
                bad = (d[c] - want).abs() > 1e-12 * want.abs()
                assert not bad.any(), (key, "result_annual", c, list(bad[bad].index))
            for name in counted:
                for args in _cached_args(one.cells[name]):
                    want = COUNT_FACTOR * one.cells[name](*args)
                    got = many.cells[name](*args)
                    floor = 1e-9 if name in RESIDUALS else 0.0
                    assert abs(got - want) <= floor + 1e-12 * abs(want), (
                        key, name, args, got, want)
                    if want != 0.0 and name not in RESIDUALS:
                        nonzero.add(name)
            assert _mismatches(one, many, exempt=TWIN_EXEMPT_DEFAULT | COUNTED) == []
            _release(base, key)
            _release(scaled, scaled_key)
    finally:
        scaled.close()
        base.close()
    want = set(counted) - RESIDUALS
    assert want <= nonzero, f"0 on every point: {sorted(want - nonzero)}"


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault, and only the rule under test
# refuses it.  The checks run over the whole table as it is read, in Data, and the message
# names the file it read and the column or every point at fault.  A blank cell reads as
# NaN, and so does a text cell once the checks coerce the column to numbers, so each is
# refused as a count, a duration, a month, a probability, an amount, a rate or a change in
# the reference rate that is not a number.  The repeated point_id holds another contract
# under the same label, as a bad extract would, so that the check must look at the labels
# and not at whole rows.  The point_ids are the committed table's: 18, the acceleration
# contract in deferral 59 months, with a premium due and its guarantee-period column; 19,
# the anchor on the table basis a month into its income phase, its cash refund running;
# 20, the period certain inside its guarantee at 300; 21, the commuting period certain a
# month after its commutation, with both frozen weights; 22, the start-date adjustment a
# month after it; 23, the joint point at 672, its joint annuitant dead; 26, the joint point
# issued 13 months on; and the twins 1, the anchor, 5, the installment refund, 8, joint, 13,
# the start-date adjustment, and 15, the commuting point.  A frozen weight of 0 is refused
# on a contract whose lives have all died, rows 20 and 21 with life 1 at 0, where it would
# otherwise pass every other rule.
#
# Where the docs say a check runs before another, its case sits on a row the later check
# would refuse differently, so that a check moved after it fails its case: a fractional
# income start month on point 20, whose frozen weight's presence rule reads the start
# month; the broken adjustment pair on point 19, past its income start month, where the
# start month in force it gives is blank; the life probabilities on point 18, which
# carries no frozen weight to break as well.
#
# Each check over a window of contract months is refused just inside each end of its
# window, its first month as well as its last, and read just outside it (the edges test),
# where an off-by-one would let a row through (USLIB-SEC-PLAN.md §5.2, T5, precised at
# M10).  An income start month is refused at -1 and read at 0.  An acceleration or a
# commutation, payout-phase options, are refused at policy months 0 and 239 and read at
# 240, the income start month, and at -1, never; on the adjustment's twin, deferred to 300,
# an acceleration is refused at 299 and read at 300.  The interlock is refused five months
# either side of the commutation and read six months either side: six before by the edges
# test, and six after in REFUSED, where proj_len() refuses it instead.  The at-issue
# check and the guarantee-period column's are refused at -120, the horizon, and at 0, and
# read at 1, a contract a month in force.  The frozen weights are refused given at -120
# and at their month, the income start month and the commutation month, and blank the
# month after, and read blank at their month and given after it.  The two checks on the
# adjustment's months, its new start month after the exercise and the exercise before the
# income start month, are refused where the months meet and read a month apart.  The two
# bounds between the frozen weights and the lives are held exactly, with no tolerance:
# each is read at equality and refused an ulp past it, l_last(t_c) above l_last(T) and
# either weight below the life alive, so that neither a floating-point slack nor a strict
# inequality passes.  Each case is read by a model of its own, its file named by a
# Reference set before the model computes anything (the malformed fixture), so a {file}
# in a message is the case's own filename.

_INTEGER = "{file}: {c} must be {what}; it is not at point_id [{p}]"
_LIFE = ("{file}: lives_if_init_{n} must be a probability, 0 to 1; it is not at "
         "point_id [{p}]")
_AMOUNT = "{file}: {c} must be a number, zero or more; it is not at point_id [{p}]"
_OPTION = ("{file}: {c} must be blank or a whole number of months, a policy month; it is "
           "not at point_id [{p}]")
_PAYOUT_OPTION = ("{file}: {c} must be blank or the income start month in force or later: "
                  "{option} is a payout-phase option; it is not at point_id [{p}]")
_START = ("{file}: income_start_mth must be a whole number of months, 0 or more, a policy "
          "month; it is not at point_id [{p}]")
_GUARANTEE = ("{file}: guarantee_mths_pricing_init must be blank or a number of months, "
              "zero or more; it is not at point_id [{p}]")
_WEIGHT = ("{file}: {c} must be blank or a probability, 0 to 1; it is not at point_id "
           "[{p}]")
_CHANGE = ("{file}: ref_rate_shift_init must be a number, the change in the reference rate "
           "since issue; it is not at point_id [{p}]")
_SINGLE = ("{file}: lives_if_init_2 must be 0 on a single-life contract, which covers no "
           "second life; it is not at point_id [{p}]")
_AT_ISSUE = ("{file}: {c} must hold its value at issue on a contract not yet in force, "
             "duration_mth 0 or less: each covered life alive, no premium paid, no income "
             "bought and no change in the reference rate; it does not at point_id [{p}]")
_NG_GIVEN = ("{file}: guarantee_mths_pricing_init must be given on a contract in force on "
             "a refund form, income_form CR or IR, whose premiums still due the kernel "
             "prices with it; it is blank at point_id [{p}]")
_NG_BLANK = ("{file}: guarantee_mths_pricing_init must be blank unless the contract is in "
             "force on a refund form: on new business the kernel derives it from the "
             "premium schedule, and the other forms fix it; it is not at point_id [{p}]")
_S2P_GIVEN = ("{file}: surv_to_payout_init must be given on a contract past its income "
              "start month in force; it is blank at point_id [{p}]")
_S2P_BLANK = ("{file}: surv_to_payout_init must be blank unless duration_mth is after the "
              "income start month in force, where the projection derives it; it is not at "
              "point_id [{p}]")
_CW_GIVEN = ("{file}: commute_weight_init must be given on a contract whose commutation "
             "month precedes the valuation date; it is blank at point_id [{p}]")
_CW_BLANK = ("{file}: commute_weight_init must be blank unless the commutation month "
             "precedes the valuation date, where the projection derives it; it is not at "
             "point_id [{p}]")
_ORDER = ("{file}: commute_weight_init must be at most surv_to_payout_init: a commutation "
          "is taken in the income phase, by part of the cohort that reached it; it is not "
          "at point_id [{p}]")
_FLOOR = ("{file}: {c} must be at least the probability that a covered life is alive at "
          "the valuation date: the cohort it weighs includes every life still alive; it "
          "is not at point_id [{p}]")
_EMPTY = ("{file}: {c} must be above 0 where it is given: {why}, so the cohort it weighs "
          "is not empty; it is not at point_id [{p}]")
_SEX = ("{file}: sex must be M or F, and so must joint_sex on a joint contract; it is not "
        "at point_id [{p}]")


def _m(template, **values):
    """A message of the templates above, ``{file}`` left for the case to fill."""
    return template.format(file="{file}", **values)


_YEARS = "a whole number of years, 0 or more"

MALFORMED = [
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("policy_count", "duration_mth", *STATE)],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[18]].assign(policy_id="DIA-900099")]),
     "{file}: point_id [18] appears more than once"),
    ("a negative count", _set("policy_count", [18], -0.1),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [18]"),
    ("a count written as text", _set("policy_count", [19], "abc"),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [19]"),
    ("a blank count", _set("policy_count", [20], NAN),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [20]"),
    ("an infinite count", _set("policy_count", [21], float("inf")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [21]"),
    ("two bad counts", _both(_set("policy_count", [18], -1.0),
                             _set("policy_count", [26], "x")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id "
     "[18, 26]"),
    ("a fractional duration", _set("duration_mth", [18], 59.5),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [18]"),
    ("a blank duration", _set("duration_mth", [18], NAN),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [18]"),
    ("a duration written as text", _set("duration_mth", [18], "ten"),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [18]"),
    ("issued beyond the horizon", _set("duration_mth", [26], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [26]"),
    ("a fractional income start month", _set("income_start_mth", [20], 300.5),
     _m(_START, p=20)),
    ("an income start month written as text", _set("income_start_mth", [20], "x"),
     _m(_START, p=20)),
    ("a negative income start month", _set("income_start_mth", [1], -12),
     _m(_START, p=1)),
    ("an income start month of -1", _set("income_start_mth", [1], -1), _m(_START, p=1)),
    ("an adjustment month written as text", _set("adjust_mth", [22], "x"),
     _m(_OPTION, c="adjust_mth", p=22)),
    ("a fractional adjustment month", _set("adjust_mth", [22], 120.5),
     _m(_OPTION, c="adjust_mth", p=22)),
    ("a new start month written as text", _set("adjust_start_mth", [22], "x"),
     _m(_OPTION, c="adjust_start_mth", p=22)),
    ("a fractional new start month", _set("adjust_start_mth", [22], 300.5),
     _m(_OPTION, c="adjust_start_mth", p=22)),
    ("an acceleration month written as text", _set("accel_mth", [18], "x"),
     _m(_OPTION, c="accel_mth", p=18)),
    ("a fractional acceleration month", _set("accel_mth", [18], 252.5),
     _m(_OPTION, c="accel_mth", p=18)),
    ("a commutation month written as text", _set("commute_mth", [21], "x"),
     _m(_OPTION, c="commute_mth", p=21)),
    ("a fractional commutation month", _set("commute_mth", [21], 252.5),
     _m(_OPTION, c="commute_mth", p=21)),
    ("an adjustment without its new start month, past T",
     _set("adjust_mth", [19], 120),
     "{file}: adjust_mth and adjust_start_mth go together, both blank or both a policy "
     "month; they do not at point_id [19]"),
    ("a new start month without its adjustment, past T",
     _set("adjust_start_mth", [19], 300),
     "{file}: adjust_mth and adjust_start_mth go together, both blank or both a policy "
     "month; they do not at point_id [19]"),
    ("a new start month at the exercise", _set("adjust_start_mth", [22], 120),
     "{file}: adjust_start_mth must follow adjust_mth: an income start date moves to a "
     "month after the exercise; it does not at point_id [22]"),
    ("an adjustment at the income start month", _set("adjust_mth", [13], 240),
     "{file}: adjust_mth must precede income_start_mth: a start-date adjustment is a "
     "deferral option; it does not at point_id [13]"),
    ("an acceleration in deferral", _set("accel_mth", [18], 200),
     _m(_PAYOUT_OPTION, c="accel_mth", option="payment acceleration", p=18)),
    ("an acceleration at issue", _set("accel_mth", [14], 0),
     _m(_PAYOUT_OPTION, c="accel_mth", option="payment acceleration", p=14)),
    ("an acceleration the month before the income start month",
     _set("accel_mth", [14], 239),
     _m(_PAYOUT_OPTION, c="accel_mth", option="payment acceleration", p=14)),
    ("an acceleration the month before an adjusted income start month",
     _set("accel_mth", [13], 299),
     _m(_PAYOUT_OPTION, c="accel_mth", option="payment acceleration", p=13)),
    ("a commutation in deferral", _set("commute_mth", [15], 200),
     _m(_PAYOUT_OPTION, c="commute_mth", option="commutation", p=15)),
    ("a commutation at issue", _set("commute_mth", [15], 0),
     _m(_PAYOUT_OPTION, c="commute_mth", option="commutation", p=15)),
    ("a commutation the month before the income start month",
     _set("commute_mth", [15], 239),
     _m(_PAYOUT_OPTION, c="commute_mth", option="commutation", p=15)),
    ("an acceleration five months after a commutation", _set("accel_mth", [15], 257),
     "{file}: accel_mth and commute_mth must fall six months apart or more, the product's "
     "interlock between its two payout options; they do not at point_id [15]"),
    ("an acceleration five months before a commutation", _set("accel_mth", [15], 247),
     "{file}: accel_mth and commute_mth must fall six months apart or more, the product's "
     "interlock between its two payout options; they do not at point_id [15]"),
    ("a joint flag written as text", _set("joint", [19], "no"),
     "{file}: joint must be True or False, a flag; it is not at point_id [19]"),
    ("a sex neither M nor F", _set("sex", [18], "X"), _m(_SEX, p=18)),
    ("no joint sex on a joint contract", _set("joint_sex", [23], NAN), _m(_SEX, p=23)),
    ("a fractional issue age", _set("issue_age", [18], 60.5),
     _m(_INTEGER, c="issue_age", what=_YEARS, p=18)),
    ("an issue age written as text", _set("issue_age", [19], "sixty"),
     _m(_INTEGER, c="issue_age", what=_YEARS, p=19)),
    ("a joint age written as text", _set("joint_age", [23], "x"),
     _m(_INTEGER, c="joint_age", what=_YEARS + ", on a joint contract", p=23)),
    ("a negative certain period", _set("certain_period", [20], -1),
     _m(_INTEGER, c="certain_period", what=_YEARS, p=20)),
    ("a fractional frequency", _set("frequency", [19], 12.5),
     _m(_INTEGER, c="frequency", what="a whole number of payments a year", p=19)),
    ("a fractional issue year", _set("issue_year", [18], 2026.5),
     _m(_INTEGER, c="issue_year", what="a whole number, a calendar year", p=18)),
    ("a negative rounding", _set("purchase_rate_dp", [19], -1),
     "{file}: purchase_rate_dp must be blank, for full precision, or a whole number of "
     "decimal places, 0 or more; it is not at point_id [19]"),
    ("a rounding written as text", _set("purchase_rate_dp", [19], "six"),
     "{file}: purchase_rate_dp must be blank, for full precision, or a whole number of "
     "decimal places, 0 or more; it is not at point_id [19]"),
    ("a blank survivor percentage", _set("survivor_pct", [23], NAN),
     _m(_INTEGER, c="survivor_pct", what="a probability, 0 to 1", p=23)),
    ("a survivor percentage above 1", _set("survivor_pct", [23], 1.5),
     _m(_INTEGER, c="survivor_pct", what="a probability, 0 to 1", p=23)),
    ("a blank COLA", _set("cola_rate", [18], NAN),
     _m(_INTEGER, c="cola_rate", what="a number, zero or more", p=18)),
    ("a negative COLA", _set("cola_rate", [18], -0.01),
     _m(_INTEGER, c="cola_rate", what="a number, zero or more", p=18)),
    ("an infinite other QLAC premium", _set("other_qlac_premium", [18], float("inf")),
     _m(_INTEGER, c="other_qlac_premium", what="a number, zero or more", p=18)),
    ("a commuted fraction above 1", _set("commute_frac", [21], 1.5),
     "{file}: commute_frac must be blank or a fraction, 0 to 1; it is not at point_id "
     "[21]"),
    ("a commuted fraction written as text", _set("commute_frac", [21], "all"),
     "{file}: commute_frac must be blank or a fraction, 0 to 1; it is not at point_id "
     "[21]"),
    ("a joint contract on the table basis", _set("factor_basis", [23], "table"),
     "{file}: factor_basis must be formula on a joint contract: the table basis, equation "
     "(1), factors a single life's survival out of the payout factor; it is not at "
     "point_id [23]"),
    ("life 1 above 1", _set("lives_if_init_1", [18], 1.5), _m(_LIFE, n=1, p=18)),
    ("life 1 below 0", _set("lives_if_init_1", [18], -0.1), _m(_LIFE, n=1, p=18)),
    ("life 1 blank", _set("lives_if_init_1", [18], NAN), _m(_LIFE, n=1, p=18)),
    ("life 1 written as text", _set("lives_if_init_1", [18], "alive"),
     _m(_LIFE, n=1, p=18)),
    ("life 2 below 0 on future business", _set("lives_if_init_2", [26], -0.1),
     _m(_LIFE, n=2, p=26)),
    ("life 2 written as text", _set("lives_if_init_2", [23], "0.0x"),
     _m(_LIFE, n=2, p=23)),
    ("negative premiums paid", _set("cum_premium_pp_init", [18], -1.0),
     _m(_AMOUNT, c="cum_premium_pp_init", p=18)),
    ("premiums paid written as text", _set("cum_premium_pp_init", [18], "x"),
     _m(_AMOUNT, c="cum_premium_pp_init", p=18)),
    ("a negative income bought", _set("annual_income_init", [18], -1.0),
     _m(_AMOUNT, c="annual_income_init", p=18)),
    ("an income bought written as text", _set("annual_income_init", [18], "x"),
     _m(_AMOUNT, c="annual_income_init", p=18)),
    ("a guarantee period written as text", _set("guarantee_mths_pricing_init", [18], "x"),
     _m(_GUARANTEE, p=18)),
    ("a negative guarantee period", _set("guarantee_mths_pricing_init", [18], -1.0),
     _m(_GUARANTEE, p=18)),
    ("l_last(T) written as text", _set("surv_to_payout_init", [19], "x"),
     _m(_WEIGHT, c="surv_to_payout_init", p=19)),
    ("l_last(T) above 1", _set("surv_to_payout_init", [19], 1.5),
     _m(_WEIGHT, c="surv_to_payout_init", p=19)),
    ("l_last(t_c) written as text", _set("commute_weight_init", [21], "x"),
     _m(_WEIGHT, c="commute_weight_init", p=21)),
    ("a rate change written as text", _set("ref_rate_shift_init", [19], "up"),
     _m(_CHANGE, p=19)),
    ("a blank rate change", _set("ref_rate_shift_init", [20], NAN), _m(_CHANGE, p=20)),
    ("an infinite rate change", _set("ref_rate_shift_init", [21], float("inf")),
     _m(_CHANGE, p=21)),
    ("a second life on a single-life contract", _set("lives_if_init_2", [19], 0.5),
     _m(_SINGLE, p=19)),
    ("a life not alive on future business", _set("lives_if_init_1", [26], 0.9),
     _m(_AT_ISSUE, c="lives_if_init_1", p=26)),
    ("a joint life not alive at issue", _set("lives_if_init_2", [8], 0.5),
     _m(_AT_ISSUE, c="lives_if_init_2", p=8)),
    ("premiums paid at issue", _set("cum_premium_pp_init", [1], 100.0),
     _m(_AT_ISSUE, c="cum_premium_pp_init", p=1)),
    ("income bought at issue", _set("annual_income_init", [5], 10.0),
     _m(_AT_ISSUE, c="annual_income_init", p=5)),
    ("a rate change at issue", _set("ref_rate_shift_init", [15], 0.005),
     _m(_AT_ISSUE, c="ref_rate_shift_init", p=15)),
    ("a rate change on future business", _set("ref_rate_shift_init", [26], -0.005),
     _m(_AT_ISSUE, c="ref_rate_shift_init", p=26)),
    ("a life not alive on business issued at the horizon",
     _moved(26, -120, lives_if_init_1=0.9), _m(_AT_ISSUE, c="lives_if_init_1", p=26)),
    ("no guarantee period on a refund form in force",
     _set("guarantee_mths_pricing_init", [18], NAN), _m(_NG_GIVEN, p=18)),
    ("a guarantee period at issue", _set("guarantee_mths_pricing_init", [1], 40.0),
     _m(_NG_BLANK, p=1)),
    ("a guarantee period on a period certain",
     _set("guarantee_mths_pricing_init", [20], 120.0), _m(_NG_BLANK, p=20)),
    ("no guarantee period a month in force",
     _moved(18, 1, guarantee_mths_pricing_init=NAN), _m(_NG_GIVEN, p=18)),
    ("a guarantee period on business issued at the horizon",
     _moved(26, -120, guarantee_mths_pricing_init=40.0), _m(_NG_BLANK, p=26)),
    ("no l_last(T) past the income start month", _set("surv_to_payout_init", [19], NAN),
     _m(_S2P_GIVEN, p=19)),
    ("l_last(T) in deferral", _set("surv_to_payout_init", [18], 0.99),
     _m(_S2P_BLANK, p=18)),
    ("l_last(T) at the income start month", _set("duration_mth", [19], 240),
     _m(_S2P_BLANK, p=19)),
    ("l_last(T) on business issued at the horizon",
     _moved(26, -120, surv_to_payout_init=0.9), _m(_S2P_BLANK, p=26)),
    ("no l_last(t_c) past the commutation", _set("commute_weight_init", [21], NAN),
     _m(_CW_GIVEN, p=21)),
    ("l_last(t_c) with no commutation", _set("commute_weight_init", [20], 0.6),
     _m(_CW_BLANK, p=20)),
    ("l_last(t_c) at the commutation month", _set("duration_mth", [21], 252),
     _m(_CW_BLANK, p=21)),
    ("l_last(t_c) on business issued at the horizon",
     _moved(26, -120, commute_mth=252, commute_frac=1.0, commute_weight_init=0.5),
     _m(_CW_BLANK, p=26)),
    ("l_last(t_c) above l_last(T)", _set("commute_weight_init", [21], 0.9),
     _m(_ORDER, p=21)),
    ("l_last(t_c) an ulp above l_last(T)",
     _both(_set("surv_to_payout_init", [21], 0.75),
           _set("commute_weight_init", [21], math.nextafter(0.75, 1.0))),
     _m(_ORDER, p=21)),
    ("l_last(T) below the life alive", _set("surv_to_payout_init", [19], 0.5),
     _m(_FLOOR, c="surv_to_payout_init", p=19)),
    ("l_last(t_c) below the life alive", _set("commute_weight_init", [21], 0.6),
     _m(_FLOOR, c="commute_weight_init", p=21)),
    ("l_last(T) an ulp below the life alive",
     _both(_set("lives_if_init_1", [19], 0.5),
           _set("surv_to_payout_init", [19], math.nextafter(0.5, 0.0))),
     _m(_FLOOR, c="surv_to_payout_init", p=19)),
    ("l_last(t_c) an ulp below the life alive",
     _both(_set("lives_if_init_1", [21], 0.5),
           _set("commute_weight_init", [21], math.nextafter(0.5, 0.0))),
     _m(_FLOOR, c="commute_weight_init", p=21)),
    ("l_last(T) below two joint lives' last survivor",
     _both(_set("lives_if_init_1", [23], 0.5), _set("lives_if_init_2", [23], 0.5),
           _set("surv_to_payout_init", [23], 0.7)),
     _m(_FLOOR, c="surv_to_payout_init", p=23)),
    ("l_last(T) of 0, every life dead in the guarantee",
     _both(_set("lives_if_init_1", [20], 0.0), _set("surv_to_payout_init", [20], 0.0)),
     _m(_EMPTY, c="surv_to_payout_init", p=20,
        why="a contract in force past its income start month reached it")),
    ("l_last(t_c) of 0, every life dead after the commutation",
     _both(_set("lives_if_init_1", [21], 0.0), _set("commute_weight_init", [21], 0.0)),
     _m(_EMPTY, c="commute_weight_init", p=21,
        why="a commutation is exercised by an owner alive to exercise it")),
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


def _premium(point_id, column, value):
    """An edit of the premium schedule that writes ``value`` into ``column`` on the rows of
    point ``point_id``, the column made ``object`` first, as :func:`_set` makes it."""
    def edit(schedule):
        cells = schedule[column].astype(object)
        return schedule.assign(**{column: cells.where(schedule["point_id"] != point_id,
                                                      value)})
    return edit


def _added(point_id, month, amount=1000.0):
    """An edit of the premium schedule that adds a premium of ``amount`` to point
    ``point_id`` at policy month ``month``."""
    def edit(schedule):
        row = {"point_id": point_id, "slice": 9, "premium_mth": month,
               "premium_amt": amount, "provenance": "[std] a test case"}
        return pd.concat([schedule, pd.DataFrame([row])], ignore_index=True)
    return edit


_PREMIUM_MTH = ("{file}: premium_mth must be a whole number of months, 0 or more, a policy "
                "month; it is not at point_id [{p}]")
_PREMIUM_AMT = ("{file}: premium_amt must be a number, zero or more; it is not at "
                "point_id [{p}]")

# The malformed premium schedules, as (case, the edit of premium_schedule_sec.csv, the
# message): what Data.premium_schedule_table refuses, naming the file and the point.  The
# committed schedule holds S's schedule as it stands, then row 18's premium still due, at
# policy month 60, and row 26's two.  DIA_US_S takes int() of the raw month, so that 60.5
# is 60 and text raises Python's own message, and a point with no premium row projects
# silently, buying no income; here the months and amounts are read by value, each checked
# against the point it names, and a point that buys nothing is refused.  The two checks
# over a window of policy months are refused at each end and read just outside it (the
# edges test), USLIB-SEC-PLAN.md §5.2's T5 (precised at M10): a premium before the
# valuation date, on row 18 at 59, at policy months 0 and 58, and read at 59, due in the
# valuation month; and one at or after the income start month, at 240 and at the adjusted
# 300, and read at 239.
SCHEDULES = [
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("point_id", "premium_mth", "premium_amt")],
    ("a point_id written as text", _premium(18, "point_id", "x"),
     "{file}: point_id must be a whole number, a model point's label; ['x'] is not"),
    ("a fractional point_id", _premium(18, "point_id", 18.5),
     "{file}: point_id must be a whole number, a model point's label; [18.5] is not"),
    ("a point the table lacks", _premium(18, "point_id", 99),
     "{file}: point_id [99] is no model point of model_point_table_sec.csv"),
    ("a fractional premium month", _premium(18, "premium_mth", 60.5),
     _m(_PREMIUM_MTH, p=18)),
    ("a premium month written as text", _premium(18, "premium_mth", "sixty"),
     _m(_PREMIUM_MTH, p=18)),
    ("a negative premium month", _premium(26, "premium_mth", -1), _m(_PREMIUM_MTH, p=26)),
    ("a premium written as text", _premium(18, "premium_amt", "x"),
     _m(_PREMIUM_AMT, p=18)),
    ("a negative premium", _premium(18, "premium_amt", -1.0), _m(_PREMIUM_AMT, p=18)),
    ("a blank premium", _premium(26, "premium_amt", NAN), _m(_PREMIUM_AMT, p=26)),
    ("a premium before the valuation date", _added(18, 58),
     "{file}: a premium falls before the valuation date at point_id [18]: those paid "
     "before it are in cum_premium_pp_init and annual_income_init, and the schedule holds "
     "the premiums still due"),
    ("a premium at issue on a contract in force", _added(18, 0),
     "{file}: a premium falls before the valuation date at point_id [18]: those paid "
     "before it are in cum_premium_pp_init and annual_income_init, and the schedule holds "
     "the premiums still due"),
    ("a premium at the income start month", _added(1, 240),
     "{file}: a premium falls at or after the income start month in force at point_id "
     "[1]: the income is level in payout"),
    ("a premium at an adjusted income start month", _added(13, 300),
     "{file}: a premium falls at or after the income start month in force at point_id "
     "[13]: the income is level in payout"),
    ("a point with no premium row", lambda s: s[s["point_id"] != 6],
     "{file}: point_id [6] buys no income: annual_income_init is 0 and no premium is due"),
    ("a point whose premiums are all 0", _premium(6, "premium_amt", 0.0),
     "{file}: point_id [6] buys no income: annual_income_init is 0 and no premium is due"),
]


@pytest.mark.parametrize("case, edit, message", SCHEDULES, ids=[c[0] for c in SCHEDULES])
def test_a_malformed_premium_schedule_is_refused_naming_its_point(tmp_path, case, edit,
                                                                  message):
    """``Data.premium_schedule_table()`` refuses the schedule, and a projection meets the
    refusal (D8, T5).

    The schedule is the model's own companion, checked against the model point table as
    that table is checked, so each case is the committed schedule with one fault, read by a
    model of its own from a copy of the inputs, its file named by a Reference set before
    the model computes anything.  The base ``Projection``'s default point, the anchor's
    twin, reads its premiums in its first month, so its ``result_cf()`` meets the same
    refusal before it computes a number, whichever point the fault is on.
    """
    folder = _sec_inputs(tmp_path, _committed())
    name = "malformed_premiums_sec.csv"
    edit(_committed_schedule()).to_csv(folder.parent / name, index=False)
    model = _read(folder, "schedule", data={"premium_schedule_file": name})
    try:
        _refused(model.Data.premium_schedule_table, message.format(file=name))
        _refused(model.Projection.result_cf, message.format(file=name))
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


# Where the cases below write: the female rate at 70 is line 103 of each age-keyed table,
# which the anchor's life reads, and the female row at 120, its last line, 203, which no
# join reads, so that a fault in its key leaves no gap in the female ages; the factor
# tables' first line, 2, is the anchor's key, and their last, 5, a male row no point reads.
_MORT_KEY, _MORT_LAST = (70, "F"), (120, "F")
_PAYOUT_KEY, _PAYOUT_LAST = (80, "F", "CR"), (80, "M", "LO")
_ROP_KEY, _ROP_LAST = (60, "F", 20), (65, "M", 15)
_AGE_SEX = ("age", "sex")
_PAYOUT_KEYS = ("income_start_age", "sex", "payout_form")
_ROP_KEYS = ("issue_age", "sex", "deferral_years")


def _tables(file, keys, key, column, message, values):
    return [(f"{file}: {what}", file, _cell(file, keys, key, column, value), message)
            for what, value in values]


_BAD = (("blank", NAN), ("written as text", "x"), ("infinite", float("inf")))
_KEY_BAD = (("blank", NAN), ("written as text", "x"), ("fractional", 120.5))


def _age_keyed(file, column, what, out_of_range):
    """The cases of an assumption table keyed by age and sex, ``file``, rate ``column``."""
    cases = _tables(file, _AGE_SEX, _MORT_KEY, column,
                    f"{file}: {column} must be {what}; it is not on line [103]",
                    (*_BAD, out_of_range))
    cases += [(f"{file}: an age {how}", file, _cell(file, _AGE_SEX, _MORT_LAST, "age", v),
               f"{file}: age must be a whole number; it is not on line [203]")
              for how, v in _KEY_BAD]
    cases += [(f"{file}: a sex {how}", file, _cell(file, _AGE_SEX, _MORT_LAST, "sex", v),
               f"{file}: sex must be M or F; it is not on line [203]")
              for how, v in (("blank", NAN), ("neither M nor F", "X"))]
    cases += [(f"{file}: an age and sex on two rows", file,
               _row_again(file, _AGE_SEX, _MORT_KEY),
               f"{file}: each age and sex must have one row; age 70, sex F is on line "
               f"[103, 204]"),
              (f"{file}: an age missing", file, _row_gone(file, _AGE_SEX, _MORT_KEY),
               f"{file}: the ages of each sex must run one row an age, without a gap; no "
               f"line holds age 70 of sex F")]
    return cases


# The malformed assumption tables, as (case, the file, its edit, the message): what the
# count cell beside each of Data's four readers of DIA_US_S's tables refuses, naming the
# file, the column and the lines.  Each value reaches a floor through survival or the
# purchase rates, where a blank would be lost without a word, so each is refused blank,
# written as text, infinite, and outside its table's range: a negative rate or factor, a
# payout factor of 0, which divides the purchase rate, and an improvement rate of 1, which
# makes 1 - G2 zero.  A negative improvement rate, a deterioration, is accepted
# (test_a_negative_improvement_rate_projects_as_s_projects_it).  Each key is read by value:
# an age or a year that is blank, text or not whole is refused, and so is a sex or a payout
# form no join reads, a key on two rows, and, where a join reads every age, a gap.
TABLES = [
    *_age_keyed("mort_table.csv", "mort_rate", "a finite number, zero or more",
                ("negative", -0.001)),
    *_age_keyed("improvement_scale.csv", "improvement_rate", "a finite number below 1",
                ("of 1", 1.0)),
    *_tables("payout_factor_table.csv", _PAYOUT_KEYS, _PAYOUT_KEY, "payout_factor",
             "payout_factor_table.csv: payout_factor must be a finite number above zero; "
             "it is not on line [2]", (*_BAD, ("of 0", 0.0))),
    ("payout_factor_table.csv: an income start age written as text",
     "payout_factor_table.csv",
     _cell("payout_factor_table.csv", _PAYOUT_KEYS, _PAYOUT_LAST, "income_start_age", "x"),
     "payout_factor_table.csv: income_start_age must be a whole number; it is not on line "
     "[5]"),
    ("payout_factor_table.csv: a blank sex", "payout_factor_table.csv",
     _cell("payout_factor_table.csv", _PAYOUT_KEYS, _PAYOUT_LAST, "sex", NAN),
     "payout_factor_table.csv: sex must be M or F; it is not on line [5]"),
    ("payout_factor_table.csv: a payout form no join reads", "payout_factor_table.csv",
     _cell("payout_factor_table.csv", _PAYOUT_KEYS, _PAYOUT_LAST, "payout_form", "LO_ROP"),
     "payout_factor_table.csv: payout_form must be LO, CR, IR or PC; it is not on line "
     "[5]"),
    ("payout_factor_table.csv: a key on two rows", "payout_factor_table.csv",
     _row_again("payout_factor_table.csv", _PAYOUT_KEYS, _PAYOUT_LAST),
     "payout_factor_table.csv: each income_start_age, sex and payout_form must have one "
     "row; income_start_age 80, sex M, payout_form LO is on line [5, 6]"),
    *_tables("rop_factor_table.csv", _ROP_KEYS, _ROP_KEY, "rop_factor",
             "rop_factor_table.csv: rop_factor must be a finite number, zero or more; it "
             "is not on line [2]", (*_BAD, ("negative", -0.1))),
    ("rop_factor_table.csv: an issue age written as text", "rop_factor_table.csv",
     _cell("rop_factor_table.csv", _ROP_KEYS, _ROP_LAST, "issue_age", "x"),
     "rop_factor_table.csv: issue_age must be a whole number; it is not on line [5]"),
    ("rop_factor_table.csv: a fractional deferral", "rop_factor_table.csv",
     _cell("rop_factor_table.csv", _ROP_KEYS, _ROP_LAST, "deferral_years", 15.5),
     "rop_factor_table.csv: deferral_years must be a whole number; it is not on line [5]"),
    ("rop_factor_table.csv: a sex neither M nor F", "rop_factor_table.csv",
     _cell("rop_factor_table.csv", _ROP_KEYS, _ROP_LAST, "sex", "m"),
     "rop_factor_table.csv: sex must be M or F; it is not on line [5]"),
    ("rop_factor_table.csv: a key on two rows", "rop_factor_table.csv",
     _row_again("rop_factor_table.csv", _ROP_KEYS, _ROP_LAST),
     "rop_factor_table.csv: each issue_age, sex and deferral_years must have one row; "
     "issue_age 65, sex M, deferral_years 15 is on line [5, 6]"),
]

# Each table's reader, DIA_US_S's and unchanged, its count cell, which checks it, and the
# point its refusal is read through, one whose projection reads the table: the anchor's
# twin reads the mortality table and, on the table basis, both factor tables; the
# generational twin reads the improvement scale.
TABLE_READERS = {"mort_table.csv": ("mort_table", "mort_table_count", 1),
                 "improvement_scale.csv": ("improvement_scale", "improvement_scale_count",
                                           16),
                 "payout_factor_table.csv": ("payout_factor_table", "payout_factor_count",
                                             1),
                 "rop_factor_table.csv": ("rop_factor_table", "rop_factor_count", 1)}


@pytest.mark.parametrize("case, file, edit, message", TABLES, ids=[c[0] for c in TABLES])
def test_a_malformed_assumption_table_is_refused_naming_the_file(tmp_path, case, file,
                                                                 edit, message):
    """Each assumption table's count cell refuses a key or a value the joins cannot use,
    and a projection meets the refusal.

    The four tables are ``DIA_US_S``'s files, read in place by both models, so each case is
    read by a model of its own from a copy of the inputs with the one fault.
    ``DIA_US_S``'s reader, unchanged, reads the table as it stands; the count cell beside
    it refuses it, naming the file, the column and the lines at fault (§7.1, *Precised at
    M3*, item 9); and the point named in :data:`TABLE_READERS`, whose projection reads that
    table, meets the same refusal in its ``result_cf()`` before it computes a number,
    because the join asks the count before it reads a value.
    """
    model = _read(_sec_inputs(tmp_path, _committed(), {file: edit}), "table")
    reader, count, point_id = TABLE_READERS[file]
    try:
        assert len(model.Data.cells[reader]()) > 0
        _refused(model.Data.cells[count], message)
        _refused(_point(model, point_id).result_cf, message)
    finally:
        model.close()


def test_a_negative_improvement_rate_projects_as_s_projects_it(tmp_path):
    """An improvement rate below 0 is a deterioration, which both models project alike, and
    a scale of whole zeros is read by value.

    The generational basis improves the base rate by ``(1 - G2) ** k``, so a negative rate
    raises it year on year, which ``DIA_US_S`` projects without complaint and this model's
    reader accepts: on a copy of both models' inputs whose scale is -0.01 at every age, the
    generational twin's ``result_cf`` is S's point 16's, to 1e-9, and its rate at the
    income start month is above the anchor basis's.  And a scale written as the integer 0
    throughout, read as int64, is read by value: the generational twin then projects what
    the twin on the anchor basis, point 3, projects, in every column.
    """
    worse = {"improvement_scale.csv": lambda df: df.assign(improvement_rate=-0.01)}
    sec = _read(_sec_inputs(tmp_path / "sec", _committed(), worse), "worse")
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN), edits=worse), "s_worse")
    try:
        p, s16 = _point(sec, 16), _point(s, 16)
        assert frame_mismatches(s16.result_cf(), p.result_cf()) == []
        assert p.mort_rate(240, 1) > _point(sec, 3).mort_rate(240, 1)
    finally:
        s.close()
        sec.close()
    zero = {"improvement_scale.csv": lambda df: df.assign(improvement_rate=0)}
    folder = _sec_inputs(tmp_path / "zero", _committed(), zero)
    flat = _read(folder, "flat")
    try:
        assert flat.Data.improvement_scale()["improvement_rate"].dtype == "int64"
        assert frame_mismatches(_point(flat, 3).result_cf(), _point(flat, 16).result_cf(),
                                rtol=0.0, atol=0.0) == []
    finally:
        flat.close()


# The four assumption tables with every age and year written as a float, as one blank or
# one 70.0 in a key column makes pandas read it.
FLOAT_KEYS = {
    "mort_table.csv": lambda df: df.assign(age=df["age"].astype(float)),
    "improvement_scale.csv": lambda df: df.assign(age=df["age"].astype(float)),
    "payout_factor_table.csv": lambda df: df.assign(
        income_start_age=df["income_start_age"].astype(float)),
    "rop_factor_table.csv": lambda df: df.assign(
        issue_age=df["issue_age"].astype(float),
        deferral_years=df["deferral_years"].astype(float)),
}


def test_an_assumption_tables_keys_written_as_floats_are_read_by_value(sec_model,
                                                                       tmp_path):
    """An assumption table whose keys are written as floats is read as the same table.

    The joins match each key by value, as ``DIA_US_S``'s do, and each count cell reads the
    keys by value too.  On a copy of the inputs whose four tables carry every age and every
    year written as a float (:data:`FLOAT_KEYS`), ``DIA_US_S``'s readers read the keys as
    floats, each count cell counts what it counts on the committed tables, and the
    anchor's twin, which reads the mortality table and both factor tables on the table
    basis, and the generational twin, which reads the improvement scale, project exactly
    what the committed model projects.
    """
    model = _read(_sec_inputs(tmp_path, _committed(), FLOAT_KEYS), "float_keys")
    try:
        assert model.Data.mort_table().index.levels[0].dtype == "float64"
        for name in ("mort_table_count", "improvement_scale_count", "payout_factor_count",
                     "rop_factor_count"):
            assert model.Data.cells[name]() == sec_model.Data.cells[name](), name
        for point_id in (1, 16):
            assert frame_mismatches(_point(sec_model, point_id).result_cf(),
                                    _point(model, point_id).result_cf(), rtol=0.0,
                                    atol=0.0) == [], point_id
    finally:
        model.close()


# The points a rule of the product refuses, each in proj_len() and each by name, with the
# reason by form: a point at or past the stop rule, and a contract that owes nothing after
# the valuation date, every covered life having died before its income start month, whose
# death benefit was paid, or after it, its certain period over or the form having none,
# the refund, if any, having been paid at the last death.  The table reads in each: the
# rules need the certain period, which an installment refund derives in Projection.  Each
# window is refused at its first month and at its last and read just outside it (the
# edges test), USLIB-SEC-PLAN.md §5.2's T5 (precised at M10): every life dead in deferral
# at 1, the first month in force, and at 240, the income start month, where the at-issue
# check refuses 0, and read inside the guarantee at 241; after the period certain's
# guarantee at 360 and 719, the frame's last month, and read at 359; and on a form with
# no certain period at 241 and 719.  The stop rule is refused at 720 and read at 719, the
# committed row 25; past each frame's last month the stop rule refuses first.  As (case,
# point_id, edit, message).
_OWED = "point_id {p}: duration_mth {d}: no payment is owed after the valuation date: "
# Row 21, a month after its full commutation at policy month 252, accelerating inside the
# guarantee that runs to 359: six months after the commutation, the least the interlock
# allows, so that Data reads the table and only proj_len() refuses it; and at 358, where
# the lump sum pulls forward 359, the guarantee's last month, valued before the exercise
# and at it.  The commuting twin, point 15, accelerating at 258 on the books from issue,
# at the valuation date and issued 120 months on, the window's first month.  An
# acceleration at 359, which pulls forward the life tail alone, and one valued a month
# after it, its lump sum paid, are read (the edges test).
_ACCEL = ("point_id {p}: accel_mth {a} pulls forward guaranteed instalments that the "
          "commutation at policy month 252 reduced, the guarantee running to policy month "
          "359: the lump sum would pay the cohort that commuted its instalments again")
REFUSED = [
    ("past the stop rule", 25, _set("duration_mth", [25], 720),
     "point_id 25: duration_mth 720 is at or past the end of the projection, policy "
     "month 720"),
    ("every life dead in deferral", 18, _set("lives_if_init_1", [18], 0.0),
     _OWED.format(p=18, d=59) + "every covered life has died before the income start "
     "month, 240"),
    ("every life dead at the income start month", 20,
     _moved(20, 240, lives_if_init_1=0.0, surv_to_payout_init=NAN),
     _OWED.format(p=20, d=240) + "every covered life has died before the income start "
     "month, 240"),
    ("every life dead after the certain period", 20,
     _moved(20, 360, lives_if_init_1=0.0),
     _OWED.format(p=20, d=360) + "every covered life has died, and the certain period "
     "ended at policy month 360"),
    ("every life dead, no certain period", 19, _set("lives_if_init_1", [19], 0.0),
     _OWED.format(p=19, d=241) + "every covered life has died, and the form has no "
     "certain period"),
    ("both joint lives dead, no certain period", 23, _set("lives_if_init_1", [23], 0.0),
     _OWED.format(p=23, d=672) + "every covered life has died, and the form has no "
     "certain period"),
    ("an acceleration six months after a commutation, inside its guarantee", 21,
     _set("accel_mth", [21], 258), _ACCEL.format(p=21, a=258)),
    ("an acceleration pulling forward a guarantee's last month", 21,
     _set("accel_mth", [21], 358), _ACCEL.format(p=21, a=358)),
    ("an acceleration inside a commuted guarantee at the valuation date", 21,
     _moved(21, 358, accel_mth=358), _ACCEL.format(p=21, a=358)),
    ("an acceleration inside a commuted guarantee at issue", 15,
     _set("accel_mth", [15], 258), _ACCEL.format(p=15, a=258)),
    ("an acceleration inside a commuted guarantee issued at the horizon", 15,
     _moved(15, -120, accel_mth=258), _ACCEL.format(p=15, a=258)),
    ("every life dead in the first month in force", 18,
     _moved(18, 1, lives_if_init_1=0.0),
     _OWED.format(p=18, d=1) + "every covered life has died before the income start "
     "month, 240"),
    ("every life dead in the last month, after the certain period", 20,
     _moved(20, 719, lives_if_init_1=0.0),
     _OWED.format(p=20, d=719) + "every covered life has died, and the certain period "
     "ended at policy month 360"),
    ("every life dead in the last month, no certain period", 25,
     _set("lives_if_init_1", [25], 0.0),
     _OWED.format(p=25, d=719) + "every covered life has died, and the form has no "
     "certain period"),
]


@pytest.mark.parametrize("case, point_id, edit, message", REFUSED,
                         ids=[c[0] for c in REFUSED])
def test_a_point_owing_nothing_is_refused_by_proj_len(tmp_path, case, point_id, edit,
                                                      message):
    """A point with no frame left is read, and refused by ``proj_len()`` by name (D6, T5).

    The rules need ``stop_mth()`` and the certain period, which an installment refund
    derives from its payout schedule in ``Projection``, so they are rules of the product,
    not of the table: the table reads, and the point is refused where its frame is defined,
    on its first projection, rather than projecting nothing.  An in-force extract should
    carry neither kind of point: a contract that owes nothing has paid its death benefit,
    its last instalment or its refund before the valuation date, as ``Term_US_SEC``'s point
    past its cover has ended.  The other points of the same table project.
    """
    model = _read_edited(tmp_path, edit, "refused")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_point(model, point_id).result_cf, message)
        assert len(_point(model, 24).result_cf()) > 0
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
    future = _label(_committed(), "future", 8, -13)
    later = (f"model_point_table_sec.csv: duration_mth must be -12 or more, a policy "
             f"issued at most 12 months after the valuation date; it is not at point_id "
             f"[{future}]")
    no_future = (f"model_point_table_sec.csv: duration_mth must be 0 or more: this model "
                 f"takes no future new business; it is not at point_id [{future}]")
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
                    assert (late.proj_len(), late.pols_new_biz(13)) == (733, 1.0)
                    assert late.result_cf()["premiums"].iloc[13] == 100000.0
            else:
                _refused(model.Data.model_point_table, refusal)
        finally:
            model.close()


# The integer and state columns the edges test writes as floats, as one blank or one 1.0 in
# a column makes pandas read it.
_WHOLE = ("duration_mth", "income_start_mth", "certain_period", "frequency", "issue_age",
          "joint_age", "issue_year", "purchase_rate_dp", "policy_count", "adjust_mth",
          "adjust_start_mth", "accel_mth", "commute_mth", *STATE)

# The columns Data reads by value and returns as the numbers it checked them as.
_CHECKED = ("income_start_mth", "adjust_mth", "adjust_start_mth", "accel_mth",
            "commute_mth", "issue_age", "joint_age", "certain_period", "frequency",
            "issue_year", "purchase_rate_dp", "survivor_pct", "cola_rate",
            "other_qlac_premium", "commute_frac")


def test_the_edges_of_the_in_force_interface_are_accepted(sec_model, tmp_path):
    """A zero count, whole numbers in any type, the horizon and the checks' edges are read.

    A count of 0 is a point that projects zeros.  The integer columns written as floats,
    as one blank or one ``1.0`` in a column makes pandas read it, and the premium months of
    the schedule likewise, are read by value, and the other rows in force or issued later
    and the twins that carry each flow (:data:`FLOW_TWINS`) project exactly what the
    committed table projects: ``12.0`` is the int the policy clock counts in.  ``Data``
    returns the columns it read by value as the numbers it checked them as.  A contract
    issued 120 months after the valuation date, the shipped ``future_horizon_mth``, is the
    last one the table admits, with a frame of 840 months, 720 to the stop rule after 120
    before it.  An option month written -1, on a contract that never exercises it, is never,
    as ``DIA_US_S`` reads one, and changes no number.  A fall in the reference rate since
    issue is a change like any other: 25 basis points down on the commuted contract.  A
    premium after the elected income start month but before the adjusted one, at policy
    month 250 on the adjustment's twin, deferred to 300, is a premium of the deferral,
    priced to the new start month.  And a contract with every life dead inside its
    guarantee pays its beneficiary, through the frozen ``l_last(T)``: the period certain at
    300 with its life dead pays 0.715 of each instalment until its guarantee ends at policy
    month 360, ``t = 60``, and nothing after.

    Each window of contract months is read just outside it (USLIB-SEC-PLAN.md §5.2, T5,
    precised at M10), by copies of committed rows appended under ids of their own, each
    with its source's premiums still due, and each reading and projecting its whole frame
    in finite numbers: an income start month of 0, the least a policy month can be; the
    adjustment exercised the month before the income start month, and the new start month
    the month after the exercise; an acceleration and a commutation at the income start
    month, 240, and an acceleration at the adjustment's 300; a commutation at -1, never; an
    acceleration six months before a commutation; the deferral row a month in force, its
    guarantee-period column given; the anchor at its income start month and the commuting
    point at its commutation month, each frozen weight blank and derived; a premium due in
    the valuation month and one the month before the income start month; the period
    certain with its life dead at 241 and 359, inside its guarantee, paying its
    beneficiary; and an acceleration inside a commuted guarantee valued the month after
    it, its lump sum paid, and one in the guarantee's last month, which pulls forward the
    life tail alone.  And each bound between the frozen weights and the lives is read at
    equality: ``l_last(t_c)`` at ``l_last(T)``, and each weight at the life alive.
    """
    committed = _committed()
    zero = _label(committed, "derived", 1, 241)
    later = _label(committed, "future", 8, -13)
    dead = _label(committed, "derived", 7, 300)
    fall = _label(committed, "derived", 15, 253)
    deferral = _label(committed, "derived", 14, 59)
    copies = {101: (zero, {"income_start_mth": 0.0}),
              102: (13, {"adjust_mth": 239.0}),
              103: (13, {"adjust_start_mth": 121.0}),
              104: (14, {"accel_mth": 240.0}),
              105: (13, {"accel_mth": 300.0}),
              106: (15, {"commute_mth": 240.0}),
              107: (15, {"commute_mth": -1.0}),
              108: (15, {"accel_mth": 246.0}),
              109: (deferral, {"duration_mth": 1.0}),
              110: (zero, {"duration_mth": 240.0, "surv_to_payout_init": NAN}),
              111: (fall, {"duration_mth": 252.0, "commute_weight_init": NAN}),
              112: (fall, {"surv_to_payout_init": 0.75, "commute_weight_init": 0.75}),
              113: (zero, {"lives_if_init_1": 0.5, "surv_to_payout_init": 0.5}),
              114: (fall, {"lives_if_init_1": 0.5, "commute_weight_init": 0.5}),
              115: (deferral, {}),
              116: (17, {}),
              117: (dead, {"duration_mth": 241.0, "lives_if_init_1": 0.0}),
              118: (dead, {"duration_mth": 359.0, "lives_if_init_1": 0.0}),
              119: (fall, {"duration_mth": 359.0, "accel_mth": 358.0}),
              120: (fall, {"accel_mth": 359.0})}

    def edit(table):
        table = table.assign(**{c: table[c].astype(float) for c in _WHOLE})
        rows = [table.loc[[row]].assign(**changes).set_axis([label])
                for label, (row, changes) in copies.items()]
        table = pd.concat([table, *rows]).rename_axis("point_id")
        table = _set("policy_count", [zero], 0.0)(table)
        table = _set("duration_mth", [later], -120.0)(table)
        table = _set("accel_mth", [1], -1.0)(table)
        table = _set("ref_rate_shift_init", [fall], -0.0025)(table)
        return _set("lives_if_init_1", [dead], 0.0)(table)

    def schedule_edit(schedule):
        rows = [schedule[schedule["point_id"] == row].assign(point_id=label)
                for label, (row, _) in copies.items()]
        schedule = pd.concat([schedule, *rows], ignore_index=True)
        schedule = _added(115, 59)(_added(116, 239)(_added(13, 250)(schedule)))
        return schedule.assign(premium_mth=schedule["premium_mth"].astype(float))

    model = _read_edited(tmp_path, edit, schedule_edit=schedule_edit)
    try:
        read = model.Data.model_point_table()
        assert all(read[c].dtype == float for c in (*_WHOLE, *_CHECKED)), read.dtypes
        assert len(read) == len(committed) + len(copies)
        for label in copies:
            key = _key(model, label)
            frame = projection(model, key).result_cf()
            assert len(frame) == projection(model, key).proj_len() > 0, label
            assert all(math.isfinite(v) for v in frame.to_numpy().ravel()), label
            _release(model, key)
        at = {label: _point(model, label) for label in copies}
        assert at[101].income_start_mth() == 0
        assert (at[102].adjust_mth(), at[102].income_start_mth()) == (239, 300)
        assert (at[103].adjust_mth(), at[103].income_start_mth()) == (120, 121)
        assert at[104].accel_mth() == at[104].income_start_mth() == 240
        assert at[105].accel_mth() == at[105].income_start_mth() == 300
        assert at[106].commute_mth() == at[106].income_start_mth() == 240
        assert (at[107].commute_mth(), at[108].accel_mth()) == (-1, 246)
        assert at[109].duration_mth(0) == 1 and at[109].guarantee_mths_pricing_init() > 0
        assert at[110].duration_mth(0) == at[110].income_start_mth() == 240
        assert at[111].duration_mth(0) == at[111].commute_mth() == 252
        assert at[111].commutations(0) > 0.0
        assert at[112].commute_weight_init() == at[112].surv_to_payout_init() == 0.75
        assert at[113].surv_to_payout_init() == at[113].lives_if_init(1) == 0.5
        assert at[114].commute_weight_init() == at[114].lives_if_init(1) == 0.5
        assert (at[115].premium_pp(0), at[116].premium_pp(239)) == (1000.0, 1000.0)
        for label in (117, 118):
            paid = [at[label].annuity_payments(t) for t in range(at[label].proj_len())]
            last = 360 - at[label].duration_mth_init()
            assert at[label].lives_if_last(0) == 0.0 and all(paid[:last]), label
            assert paid[last:] == [0.0] * (len(paid) - last), label
        assert at[119].accel_mth() == at[119].duration_mth_init() - 1
        assert at[120].accel_mth() == 359
        assert model.Data.premium_schedule_table()["premium_mth"].dtype == "int64"
        df = _point(model, zero).result_cf()
        assert len(df) == 479 and (df == 0.0).all().all()
        deferred = _point(model, 13)
        assert deferred.income_start_mth() == deferred.income_start_mth_at(250) == 300
        assert deferred.premium_pp(250) == 1000.0
        assert deferred.annual_income(250) == pytest.approx(
            deferred.annual_income(249) + 1000.0 * deferred.purchase_rate(250), rel=1e-15)
        assert deferred.annual_income_payout() == deferred.annual_income(250)
        for point_id in sorted(set(_flow_points(committed)) - {zero, later, dead}):
            key = _key(model, point_id)
            assert frame_mismatches(_point(sec_model, point_id).result_cf(),
                                    projection(model, key).result_cf(), rtol=0,
                                    atol=0) == [], point_id
            _release(model, key)
        p = _point(model, 18)
        assert p.duration_mth(0) == 59 and type(p.duration_mth(0)) is int
        assert p.income_start_mth() == 240 and type(p.income_start_mth()) is int
        assert p.accel_mth() == 252 and type(p.accel_mth()) is int
        assert _point(model, 1).accel_mth() == -1
        late = _point(model, later)
        assert (late.t_entry(), late.proj_len(), late.pols_new_biz(120)) == (120, 840, 1.0)
        assert late.result_cf().loc[:119].eq(0.0).all().all()
        assert late.premiums(120) == 100000.0
        moved = _point(model, fall)
        assert moved.ref_rate_shift_init() == -0.0025
        assert moved.commute_disc_rate(0) == pytest.approx(0.0525, rel=1e-12)
        gone = _point(model, dead)
        assert gone.lives_if_last(0) == 0.0 and gone.pols_if(0) == 0.0
        paid = [gone.annuity_payments(t) for t in range(gone.proj_len())]
        assert paid[:60] == [gone.annuity_pp_sched(t) * gone.surv_to_payout()
                             for t in range(60)]
        assert gone.surv_to_payout() == pytest.approx(0.715, rel=1e-9)
        assert paid[60:] == [0.0] * (len(paid) - 60)
    finally:
        model.close()


# Every state DIA_US_S reaches, restated in force at its month, is an opening state Data's
# checks and proj_len()'s accept, but a state the product refuses by name: a check
# exercised only on the rows the tests above choose could refuse a state S reaches
# elsewhere (D6).  DIA_US_S keeps a contract on its books after it owes nothing, every
# covered life dead before its income start month or after its certain period, or on a
# form with none, and projects it as zeros to its stop rule, where proj_len() refuses it by
# name (REFUSED): the every-state test sets each such state aside and shows it refused.


def _every_state_months(sp):
    """The months S point ``sp``, projected, is restated at by the every-state test.

    By default the edges of each window a check of ``Data`` or ``proj_len()`` reads a
    month against (USLIB-SEC-PLAN.md §5.2, T5, precised at M10): policy month 1, the first
    past the at-issue check's window and inside the guarantee-period column's; each
    premium month and the month after it, where the premium leaves the schedule for the
    premiums paid; the income start month in force and the month either side, where the
    deferral ends and ``l_last(T)`` becomes a column; the month of the first instalment and
    the month after it, below monthly in arrears a payment step after the income start
    month; each option month and the month after it, where ``l_last(t_c)`` becomes a
    column and an acceleration leaves the books; the guarantee's last month and the first
    after it; the month before each covered life's survival reaches 0, and the month it
    does; and the frame's last month, before the stop rule.  With ``USLIB_SEC_FULL=1``,
    every month of its frame.
    """
    n = sp.proj_len()
    if SEC_FULL:
        return list(range(1, n))
    start = sp.income_start_mth()
    end = start + sp.certain_mths_eff()
    first = next(t for t in range(start, n) if sp.is_payment_mth(t))
    months = {1, start - 1, start, start + 1, first, first + 1, end - 1, end, n - 1}
    for m in (*sp.premium_by_mth(), sp.adjust_mth(), sp.accel_mth(), sp.commute_mth()):
        if m >= 0:
            months |= {m, m + 1}
    for life in _lives(sp):
        zero = next((d for d in range(n) if sp.lives_if(d, life) == 0.0), None)
        if zero is not None:
            months |= {zero - 1, zero}
    return sorted(d for d in months if 1 <= d < n)


def _owing(sp, d):
    """Why S point ``sp`` restated at month ``d`` owes nothing after it, as ``proj_len()``
    says it, or None where it owes a payment.

    As ``proj_len()`` reads a contract in force with every covered life dead,
    ``DIA_US_S``'s survival exactly 0: valued at or before its income start month in
    force, or at or after the end of its certain period, or on a form with none.  Inside a
    guarantee the beneficiary is paid.
    """
    if any(sp.lives_if(d, life) > 0.0 for life in _lives(sp)):
        return None
    start = sp.income_start_mth()
    end = start + sp.certain_mths_eff()
    if d <= start:
        return f"every covered life has died before the income start month, {start}"
    if d < end:
        return None
    if end > start:
        return (f"every covered life has died, and the certain period ended at policy "
                f"month {end}")
    return "every covered life has died, and the form has no certain period"


def _every_state_table(root, s, edits):
    """The states ``s``'s points reach, restated in force: ``(folder, rows, owing)``.

    Each month of :func:`_every_state_months` of each point of ``s``, an S model already
    swept, a derived row of a table the generator builds beside every point's twin, with
    its premium schedule, written into ``folder`` under ``root`` with ``edits`` beside
    them, the inputs S read (:func:`_sec_built`).  ``rows`` is the table's length, and
    ``owing`` holds ``{(S point, month): why}`` for each state owing nothing
    (:func:`_owing`).
    """
    states, owing = [], {}
    for key, point_id in zip(point_keys(s), s.Data.model_point_table().index):
        sp = projection(s, key)
        for d in _every_state_months(sp):
            states.append((point_id, d))
            why = _owing(sp, d)
            if why is not None:
                owing[(point_id, d)] = why
    folder = _sec_built(root, s, states, (), edits)
    return folder, len(s.Data.model_point_table()) + len(states), owing


def _departures(model, rows, owing):
    """Where ``Data`` and ``proj_len()`` depart from what the every-state test expects.

    ``model`` holds a table of ``rows`` rows (:func:`_every_state_table`), which ``Data``
    must read, and its premium schedule.  Each row's ``proj_len()`` must give a frame, but
    a state of ``owing``, ``{(S point, month): why}``, which it must refuse, naming the
    row, its month and why.  Each row is released once asked, the collector run every
    500.  Returns each departure, the line that names it.
    """
    try:
        table = model.Data.model_point_table()
        model.Data.premium_schedule_table()
    except Exception as err:                    # reported, with the rows' states
        return [f"Data: {_raised(err)}"]
    assert len(table) == rows
    twins = table.index[table["row_kind"] == "twin"]
    point_of = dict(zip(table.loc[twins, "policy_id"], twins))
    found = []
    for i, (key, label) in enumerate(zip(point_keys(model), table.index)):
        state = (point_of[table.at[label, "source_policy_id"]],
                 int(table.at[label, "source_mth"]))
        why = owing.get(state) if table.at[label, "row_kind"] == "derived" else None
        try:
            projection(model, key).proj_len()
            if why is not None:
                found.append(f"point_id {label}, S point {state}: it has a frame")
        except Exception as err:                # reported, so every row is asked
            text = str(err)
            if why is None or not ("ValueError" in text
                                   and _OWED.format(p=label, d=state[1]) + why in text):
                found.append(_raised(err))
        _release(model, key, collect=i % 500 == 499)
    return found


def test_every_state_s_reaches_is_accepted_in_force(s_model, spliced, tmp_path):
    """Every state ``DIA_US_S`` reaches is a valid opening state, but one owing nothing.

    ``Data``'s checks and ``proj_len()``'s hold an opening state to what a contract in
    force can be, so they must accept each state the S model reaches (D6).  So every S
    point, swept, is restated in force by the generator at the edges of its windows, or
    with ``USLIB_SEC_FULL=1`` at every month of its frame (:func:`_every_state_months`),
    into one table beside the twins, with its premiums still due: ``Data`` reads the table
    and the schedule, and every row's ``proj_len()`` gives a frame.  But for the states set
    aside, which ``DIA_US_S`` keeps on its books, projecting zeros to its stop rule, and
    ``proj_len()`` refuses, each by name, its row, its month and why it owes nothing
    (:func:`_owing`): on the splice, variant 18, the anchor on a male life on the table
    basis, dead from policy month 685, after mortality's cap at 117, its form a cash refund
    with no certain period (USLIB-SEC-PLAN.md §5.2, T5, precised at M10).  No state S
    reaches is an acceleration ``proj_len()`` refuses: no point accelerates inside a
    guarantee a commutation before it reduced.

    It runs under each set of inputs on which the states S reaches differ (§5.2, T5,
    precised at M9).  S's shipped References, on S's own table: the committed S model,
    whose points see no change in the reference rate, price at the shipped A/E of 1 and
    reprice at the pricing rate, and none of whose contracts has every covered life dead
    before its stop rule, so that none owes nothing.  And the splice's References,
    set-apart tables and variants (:data:`SPLICED_REFS`): the reference rate up 50 basis
    points in every state, and the A/E at 1.05, under which variant 18's male life reaches
    mortality's cap at 117 and dies with certainty.  Under :data:`LATER_REFS`, under which
    the splice reads S a second time, S's states are the splice's but for the reference
    rate's change, 0 as under the shipped References, which ``Data`` holds only to be a
    number.  The splice's table is built while its S model is swept, in the ``spliced``
    fixture, before T2 releases its points.
    """
    sets = (("shipped", _every_state_table(tmp_path / "shipped", s_model, None), {},
             set()),
            ("spliced", spliced[4], SEC_REFS, {18}))
    for name, (folder, rows, owing), refs, owing_points in sets:
        assert {p for p, _ in owing} == owing_points, (name, sorted(owing)[:5])
        model = _read(folder, "every", refs)
        try:
            found = _departures(model, rows, owing)
        finally:
            model.close()
        assert not found, f"{name}: {len(found)} departures, first: {found[:5]}"


# What the decodes refuse, as (case, the table's edit, the point, the cell it is read
# through, its message): each text value a projection branches on, and the frequency,
# which picks its payment months.  The decodes read the model point's columns and validate
# them as DIA_US_S's label accessors do, so an invalid value raises S's own message
# wherever the projection first meets it, and only the rule under test refuses each case:
# the form on a twin, whose guarantee-period column is blank whatever its form; the trigger
# on a joint point, where the payment factor and the pricing kernel read it.  The market
# type is read by the QLAC overlay alone, as in S, so its refusal is met there, and every
# cash flow of the point projects.
UNDECODABLE = [
    ("an unknown reduction trigger", _set("reduction_trigger", [8], "first"), 8,
     "result_cf", "invalid reduction_trigger"),
    ("an unknown income form", _set("income_form", [3], "LCR"), 3, "result_cf",
     "invalid income_form"),
    ("an unknown death-benefit form", _set("db_form", [3], "RCP"), 3, "result_cf",
     "invalid db_form"),
    ("an unknown payment timing", _set("timing", [17], "middle"), 17, "result_cf",
     "invalid timing"),
    ("an unknown mortality basis", _set("mort_basis", [16], "select"), 16, "result_cf",
     "invalid mort_basis"),
    ("an unknown factor basis", _set("factor_basis", [3], "tabular"), 3, "result_cf",
     "invalid factor_basis"),
    ("an unknown frequency", _set("frequency", [1], 5), 1, "result_cf",
     "invalid frequency"),
    ("an unknown market type", _set("market_type", [11], "IRA"), 11, "qlac_flags",
     "invalid market_type"),
]


@pytest.mark.parametrize("case, edit, point_id, cell, message", UNDECODABLE,
                         ids=[c[0] for c in UNDECODABLE])
def test_an_undecodable_value_is_refused_where_the_projection_meets_it(tmp_path, case,
                                                                        edit, point_id,
                                                                        cell, message):
    """An invalid switch raises ``ValueError`` with S's message, not a quiet default.

    Each case is read by a model of its own, from a copy of the inputs with the one fault.
    The table reads, because these are rules of the projection, not of the in-force
    interface, and the point's projection meets the fault on its way to its first number.
    A decode that read an unknown form as a life annuity, or an unknown trigger as the
    primary's, would project a contract no one wrote.  The market type is read only by the
    QLAC overlay, which refuses it, while the cash flows, which it does not reach, project.
    """
    model = _read_edited(tmp_path, edit, "undecodable")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        p = _point(model, point_id)
        _refused(p.cells[cell], message)
        if cell != "result_cf":
            assert len(p.result_cf()) == p.proj_len()
    finally:
        model.close()


def test_a_life_a_kind_or_a_timing_neither_model_knows_is_refused(sec_model):
    """A third life, an unknown claim kind or timing raises, rather than answers.

    The opening state, the issue ages, the two age-keyed table readers, the pricing
    survival and the projection's take a life, 1 or 2, as ``DIA_US_S``'s ``age_at_entry``
    does; ``claim_pp`` takes the two kinds, ``"DEATH"`` and ``"REFUND"``; and ``pols_if_at``
    the two timings, ``BasicTerm_SE``'s ``"BEF_NB"`` and ``"BEF_DECR"`` (the count test asks
    for ``"BEF_MAT"``).  Each refuses anything else with ``ValueError`` instead of
    answering with another life's, kind's or timing's number.
    """
    p = _row(sec_model, "derived", 1, 241)
    for call, message in ((lambda: p.lives_if_init(3), "invalid life"),
                          (lambda: p.age_at_entry(3), "invalid life"),
                          (lambda: p.mort_rate_base_at(70, 3), "invalid life"),
                          (lambda: p.improvement_rate_at(70, 3), "invalid life"),
                          (lambda: p.lives_if_pm(12, 3), "invalid life"),
                          (lambda: p.lives_if(0, 3), "invalid life"),
                          (lambda: p.claim_pp(0, "LAPSE"), "invalid kind"),
                          (lambda: p.pols_if_at(0, "AFT_DECR"), "invalid timing")):
        _refused(call, message)


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_files_are_what_s_generates(s_model):
    """``model_point_table_sec.csv`` and ``premium_schedule_sec.csv`` are what DIA_US_S and
    its inputs generate today.

    Every row and column of both files, the text cells and the opening-state columns
    included: an edit to an S row or a premium the files copy or derive from, or to an S
    formula a row's state is read from, fails here until ``python tools/gen_sec_points.py
    DIA_US_SEC`` regenerates them, in the same commit.  Text and integers compare exactly,
    and a float by its value, to 1e-12, because the text the writer picks for a computed
    float depends on the platform's parser (§5.2).  The premium schedule is the spec's one
    companion, so both files are checked.
    """
    assert set(SPEC.companions) == {SCHEDULE}
    assert check_generated(SEC, s_model=s_model) == []


def test_every_committed_row_continues_its_s_point(sec_model, s_model):
    """Each derived and future row of the committed table is its S point from its month on.

    T6 holds the committed table to what the generator makes of ``DIA_US_S``, each float to
    1e-12 absolute and relative, which pins a probability as small as the anchor's survival
    in its last month, 6.1e-08, only to about 1.6e-5 of itself, and says nothing of what the
    model makes of a row.  So each derived and future row is projected too, at the shipped
    assumptions, and compared with its S point from the row's ``source_mth`` on
    (:func:`_continues_s`): ``result_cf`` and ``result_pols`` frame by frame, and every
    other cell of S's at every argument S cached, to 1e-9 relative with no absolute floor,
    the roll-forward residuals at the floor.  The eight rows restated in force skip what
    the splice skips.  The joint point issued 13 months on, its ``source_mth`` -13, holds
    its whole premium schedule and whole policy years, so its premiums by month and its
    annual display are compared too, as T3 compares future business on the splice's
    inputs.  The shipped expense inflation runs from issue in S and from the valuation date
    here (D7), so the cells it moves are left out; the inflation test holds them.
    """
    table = sec_model.Data.model_point_table()
    rows = table.index[table["row_kind"] != "twin"]
    assert set(table.loc[rows, "row_kind"]) == {"derived", "future"}
    for point_id in rows:
        month = int(table.at[point_id, "source_mth"])
        later = table.at[point_id, "row_kind"] == "future"
        p, s = _point(sec_model, point_id), _source(s_model, table, point_id)
        found = _continues_s(s, p, month, FUTURE_EXEMPT if later else SPLICE_EXEMPT)
        assert found == [], point_id


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_worked_example_carries_over_at_the_valuation_date(sec_model, s_model):
    """S's worked example and its traces, restated in force, continue S's months.

    At the shipped assumptions, on the three rows derived from the worked example's points:

    * the anchor a month into its income phase, at policy month 241, pays the instalment
      3,688.30, ``B(T) / 12`` on the 44,259.65 the two slices bought, from ``t = 0``, and
      its refund balance at ``t = 0`` is ``CP(T) - G(240) = 150,000 - 3,688.30``,
      146,311.70, the cash refund of a death in the month, read off the instalments
      scheduled to date on the policy clock; the balance runs out in the fourth payment
      year and stays at the float 0.0 from then on, where ``max(0.0, CP(T) - G)`` floors
      it;
    * the acceleration contract in deferral at policy month 59, the month before its second
      premium, carries the 100,000 paid and the 32,024.03 it bought, and buys the second
      slice at ``t = 1``, 50,000 at ``DIA_US_S``'s ``purchase_rate(60)``, its income rising
      to 44,106.53 and its premium income 48,750.00, the premium weighted by survival to
      policy month 60;
    * the start-date adjustment a month after its exercise, at policy month 121, carries the
      repriced income, 82,907.43, the 44,106.53 the slices bought times the factor 1.8797,
      and pays it from policy month 300, its first instalment at ``t = 179``, the end of the
      adjusted income start month.

    Each row is S's point from its month on in every cell but those expense inflation moves
    (:func:`_continues_s`).
    """
    anchor = _row(sec_model, "derived", 1, 241)
    assert anchor.annuity_pp_sched(0) == pytest.approx(3688.30, abs=0.005)
    assert anchor.annual_income_payout() == pytest.approx(44259.65, abs=0.005)
    assert anchor.refund_balance(0) == pytest.approx(150000.0 - 3688.30, abs=0.005)
    assert anchor.claim_pp(0, _code(anchor, "REFUND")) == anchor.refund_balance(0)
    assert anchor.cum_annuity_pp(240) == anchor.annuity_pp_sched_pm(240)
    balances = [anchor.refund_balance(t) for t in range(anchor.proj_len())]
    out = balances.index(0.0)
    assert 24 < out + 1 <= 48 and balances[out - 1] > 0.0
    floored = [(type(b), b) for b in balances[out:]]
    assert floored == [(float, 0.0)] * len(floored)
    deferred = _row(sec_model, "derived", 14, 59)
    s14 = _point(s_model, 14)
    assert (deferred.cum_premium_pp_init(), deferred.premium_pp(1)) == (100000.0, 50000.0)
    assert deferred.annual_income(0) == pytest.approx(32024.03, abs=0.005)
    assert deferred.purchase_rate(60) == s14.purchase_rate(60)
    assert deferred.annual_income(1) == pytest.approx(
        deferred.annual_income(0) + 50000.0 * s14.purchase_rate(60), rel=1e-15)
    assert deferred.annual_income(1) == pytest.approx(44106.53, abs=0.005)
    assert deferred.premiums(1) == pytest.approx(48750.00, abs=0.005)
    adjusted = _row(sec_model, "derived", 13, 121)
    assert adjusted.income_start_mth() == 300
    assert adjusted.annual_income_init() == pytest.approx(82907.43, abs=0.005)
    assert adjusted.annual_income_init() == pytest.approx(
        44106.53 * 1.8797, rel=1e-4)
    paid = [adjusted.annuity_payments(t) for t in range(adjusted.proj_len())]
    assert paid[:179] == [0.0] * 179 and paid[179] > 0.0
    assert paid[179] == pytest.approx(
        adjusted.annual_income_init() / 12 * adjusted.lives_if(180, 1), rel=1e-12)
    for (s_point, month), p in (((1, 241), anchor), ((14, 59), deferred),
                                ((13, 121), adjusted)):
        assert _continues_s(_point(s_model, s_point), p, month) == [], (s_point, month)


def test_pricing_stays_at_issue_and_premium_dates(sec_model, s_model, tmp_path):
    """Each premium still due is priced at its own date on survival from issue, as S
    prices it.

    The pricing survival, ``lives_if_pm(k, life)``, is one explicit loop from issue, S's
    recursion unrolled, so it is ``DIA_US_S``'s ``lives_if(k, life)`` bit for bit at every
    time point from issue to the horizon, on the anchor's twin, the joint twin for both
    lives, and the generational and adjustment twins.  On the contract in deferral at
    policy month 59, the slice still due, at policy month 60, is priced with
    ``guarantee_mths_pricing_init``, ``DIA_US_S``'s fixed point over the whole schedule, the
    slice already bought included, and its purchase rate is ``DIA_US_S``'s bit for bit; on
    a fresh read its projection prices that one premium and no other, the first slice
    being in the opening state.  Set to 0, the column gives the slice another price and
    the contract another income: the schedule of premiums still due cannot recover it.  And
    on the adjustment a month after its exercise, the repriced income is in the opening
    state, and nothing in its projection evaluates the repricing factor again.
    """
    deferred = _row(sec_model, "derived", 14, 59)
    s14 = _point(s_model, 14)
    assert deferred.guarantee_mths_pricing() == deferred.guarantee_mths_pricing_init()
    assert deferred.guarantee_mths_pricing() == pytest.approx(
        s14.guarantee_mths_pricing(), rel=1e-15)
    assert deferred.purchase_rate(60) == s14.purchase_rate(60)
    label = _label(_committed(), "derived", 14, 59)
    adjusted = _label(_committed(), "derived", 13, 121)
    fresh = _read(model_path(SEC), "pricing")
    try:
        for point_id, lives in ((1, (1,)), (8, (1, 2)), (13, (1,)), (16, (1,))):
            p, s = _point(fresh, point_id), _point(s_model, point_id)
            for life in lives:
                mine = [p.lives_if_pm(k, life) for k in range(p.horizon_mths() + 1)]
                assert mine == [s.lives_if(k, life)
                                for k in range(p.horizon_mths() + 1)], (point_id, life)
        p = _point(fresh, label)
        p.result_cf()
        assert sorted(p.cells["purchase_rate"].keys()) == [60]
        q = _point(fresh, adjusted)
        q.result_cf()
        assert len(q.cells["adjust_income_factor"].keys()) == 0
        assert len(q.cells["purchase_rate"].keys()) == 0
    finally:
        fresh.close()
    zeroed = _read_edited(tmp_path, _set("guarantee_mths_pricing_init", [label], 0.0),
                          "zeroed")
    try:
        z = _point(zeroed, label)
        assert z.purchase_rate(60) != s14.purchase_rate(60)
        assert abs(z.annual_income(1) - deferred.annual_income(1)) > 1.0
    finally:
        zeroed.close()


def test_the_payout_schedule_is_fixed_at_the_income_start(sec_model, s_model, events,
                                                          spliced):
    """The income, the refund base and the instalments scheduled to date are S's, read by
    policy month and based at the valuation date's.

    On every twin, ``annual_income_payout()``, ``cum_premium_payout()`` and
    ``cum_annuity_pp(k)`` at every policy month from issue to the stop rule are
    ``DIA_US_S``'s ``annual_income(T)``, ``cum_premium_pp(T)`` and ``cum_annuity_pp(k)``,
    bit for bit.  On every row restated in force they are S's to the last ulp of the opening
    state, which the CSV gives back exactly or within two ulps, and bit for bit where it
    gives it back exactly, as on the cash refund a month into its income phase: the loop
    that sums the instalments before the valuation date's policy month adds them in S's
    order.  The committed rows' instalments are level before their valuation dates, where
    any order of addition gives one float, so the order is asserted on a row whose
    instalments step: the COLA cash refund restated at policy month 265, past its first COLA
    anniversary, its refund still running, on the splice's inputs, whose ``G`` at the
    valuation date's key is the instalments added one by one from the income start month,
    in S's order, to the last bit.  On a model just read, the cash refunds in payout, a
    month in, 432 months in and in the last month, read ``G`` from the valuation date's
    policy month on and never below, keys ``d - 1`` to the last month's (R2's static
    schedule): the refund of a contract long in payout does not recurse back to its income
    start month.  An installment refund's derived period, ``n_R``, is a fixed point of the
    whole payout schedule, which its stop rule needs, so the installment refund valued 30
    months into its income phase reads ``G`` at every payment point from the income start
    month to the end of its derived period, in ascending order, a cell deep each, and at no
    other key.
    """
    table = sec_model.Data.model_point_table()
    exact = set()
    for point_id in table.index[table["row_kind"] != "future"]:
        p, s = _point(sec_model, point_id), _source(s_model, table, point_id)
        start = p.income_start_mth()
        keys = range(p.stop_mth() + 1)
        mine = [p.annual_income_payout(), p.cum_premium_payout(),
                *(p.cum_annuity_pp(k) for k in keys)]
        theirs = [s.annual_income(start), s.cum_premium_pp(start),
                  *(s.cum_annuity_pp(k) for k in keys)]
        if table.at[point_id, "row_kind"] == "twin" or mine[0] == theirs[0]:
            assert mine == theirs, point_id
            exact.add(point_id)
        else:
            assert mine == pytest.approx(theirs, rel=1e-15, abs=0.0), point_id
    assert _label(table, "derived", 1, 241) in exact
    key = _row_key(events, "derived", 10, 265)
    try:
        p = projection(events, key)
        start, base = p.income_start_mth(), p.duration_mth_init() - 1
        steps = [p.annuity_pp_sched_pm(j) for j in range(start, base + 1)]
        assert len(set(steps) - {0.0}) > 1, sorted(set(steps))
        total = 0.0
        for inst in steps:
            total += inst
        assert p.cum_annuity_pp(base) == total
        assert p.cum_annuity_pp(base) == pytest.approx(
            _point(spliced[0], 10).cum_annuity_pp(base), rel=1e-15, abs=0.0)
        assert p.refund_balance(0) > 0.0
    finally:
        _release(events, key, collect=True)
    fresh = _read(model_path(SEC), "g_keys")
    try:
        for s_point, month in ((1, 241), (8, 672), (1, 719)):
            p = _row(fresh, "derived", s_point, month)
            p.result_cf()
            keys = sorted(p.cells["cum_annuity_pp"].keys())
            assert keys == list(range(month - 1, keys[-1] + 1)), (month, keys[:5])
            assert keys[-1] == p.stop_mth() - 2, (month, keys[-3:])
        p = _row(fresh, "derived", 5, 270)
        p.result_cf()
        start = p.income_start_mth()
        assert sorted(p.cells["cum_annuity_pp"].keys()) == list(
            range(start, start + p.certain_mths_refund()))
    finally:
        fresh.close()


def test_survival_opens_per_life_at_the_valuation_date(sec_model, s_model):
    """Each life's survival opens at ``t_entry()`` at its column, and runs on from there.

    On every committed point ``lives_if(t, life)`` is 0 before the contract is on the
    books and ``lives_if_init(life)`` at ``t_entry()``, for each life separately: 1 for
    each covered life at issue, and on a row restated from S at its month ``d``, S's
    ``lives_if(d, life)``, read back from the CSV to 1e-12.  On the joint point at 672 the
    joint annuitant died with certainty at 118, so that life is exactly 0 and the primary a
    fraction, and the payment factor is the survivor percentage times the primary's
    survival from ``t = 0``, read at the end of each month, arrears; on the anchor in its
    last month the life is 6.1e-08.  That each life then runs on from its opening value as
    S's does is asserted with the rest of each derived row's projection, by
    :func:`test_every_committed_row_continues_its_s_point`.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        entry = p.t_entry()
        for life in (1, 2):
            assert [p.lives_if(t, life) for t in range(entry)] == [0.0] * entry
            covered = life == 1 or p.is_joint()
            assert p.lives_if(entry, life) == (p.lives_if_init(life) if covered else 0.0)
        if table.at[point_id, "row_kind"] != "derived":
            assert (p.lives_if_init(1), p.lives_if_init(2)) == (
                1.0, 1.0 if p.is_joint() else 0.0), point_id
    for point_id in table.index[table["row_kind"] == "derived"]:
        month = int(table.at[point_id, "source_mth"])
        p, s = _point(sec_model, point_id), _source(s_model, table, point_id)
        for life in _lives(p):
            assert p.lives_if_init(life) == pytest.approx(s.lives_if(month, life),
                                                          rel=1e-12, abs=0.0), point_id
    joint = _row(sec_model, "derived", 8, 672)
    assert joint.lives_if_init(2) == 0.0 < joint.lives_if_init(1) < 1e-4
    for t in range(joint.proj_len()):
        assert joint.payment_factor(t) == joint.payment_factor_life(t) == (
            joint.survivor_pct() * joint.lives_if(t + 1, 1)), t
    assert _row(sec_model, "derived", 1, 719).lives_if_init(1) == pytest.approx(
        6.132e-08, rel=1e-3)


def test_contract_open_is_not_life_alive_in_a_guarantee(sec_model, events, spliced,
                                                        tmp_path):
    """In a certain period the guarantee pays the cohort that reached the income phase,
    ``l_last(T)``, which the lives alive cannot say.

    On the period certain in force 300 months, inside its guarantee, the payment factor is
    ``surv_to_payout_init``, 0.715, ``DIA_US_S``'s ``l_last(240)``, while the probability
    that the life is alive, ``lives_if_last(0)``, is 0.5577: the guarantee runs on to a
    beneficiary after the last death, and the contract open exceeds the life alive.  Set to
    the life alive, the column cuts the guaranteed instalments to 0.5577 of each, which
    nothing else on the row could restore: only the column carries the continuation.  And
    on the same contract valued on its income start month, where the column is blank, the
    weight is derived from the projection at ``t = 0``, ``lives_if_last(0)``, bit for bit
    ``DIA_US_S``'s ``surv_to_payout()``, read only where the certain floor is positive.
    """
    p = _row(sec_model, "derived", 7, 300)
    assert p.certain_floor(0) == 1.0
    assert p.surv_to_payout_init() == pytest.approx(0.715, rel=1e-9)
    assert p.payment_factor(0) == p.surv_to_payout_init()
    assert p.lives_if_last(0) == pytest.approx(0.5577, rel=1e-9)
    assert p.payment_factor_life(0) < p.payment_factor(0)
    label = _label(_committed(), "derived", 7, 300)
    alive = _read_edited(tmp_path, _set("surv_to_payout_init", [label],
                                        p.lives_if_last(0)), "alive")
    try:
        q = _point(alive, label)
        for t in (0, 30, 59):
            assert q.annuity_payments(t) < p.annuity_payments(t)
            assert q.annuity_payments(t) == pytest.approx(
                p.annuity_payments(t) * p.lives_if_last(0) / p.surv_to_payout_init(),
                rel=1e-12)
        assert q.annuity_payments(60) == p.annuity_payments(60)
    finally:
        alive.close()
    s7 = _point(spliced[0], 7)
    key = _row_key(events, "derived", 7, 240)
    try:
        r = projection(events, key)
        assert pd.isna(r.model_point()["surv_to_payout_init"])
        assert r.surv_to_payout() == r.lives_if_last(0) == r.payment_factor(0)
        assert r.surv_to_payout() == pytest.approx(s7.surv_to_payout(), rel=1e-15, abs=0.0)
        assert r.payment_factor(0) == pytest.approx(s7.payment_factor(240), rel=1e-15,
                                                    abs=0.0)
    finally:
        _release(events, key, collect=True)


def test_a_commutation_before_the_valuation_date_leaves_its_weight(sec_model, s_model,
                                                                   events, spliced,
                                                                   tmp_path):
    """A contract that commuted before the valuation date pays its beneficiaries'
    guarantee, and its life tail, through the frozen ``l_last(t_c)``.

    The commuting period certain a month after its commutation, at policy month 253,
    carries ``commute_weight_init``, 0.680338, ``DIA_US_S``'s ``l_last(252)``, the cohort
    alive to commute, beside ``surv_to_payout_init``, 0.715, the cohort that reached the
    income phase.  The commuted cohort's guaranteed instalments are gone, so through the
    end of the guarantee, policy month 359, ``t = 106``, it pays the rest of the cohort's,
    the beneficiaries' of contracts whose life died between the income start and the
    commutation: ``inst * (0.715 - 0.680338)``, 79.54 a month, S's months 253 to 359; and
    from policy month 360 the life tail, which a commutation does not reach, 919.16 at
    ``t = 107``.  Set to 0.715, the column extinguishes the beneficiaries' guarantee too:
    read from a copy of the table whose column is 0.715, the row pays nothing until the
    tail, which is unchanged, the fault ``DIA_US_S``'s ``model.md`` prices at 6,898.37 of
    present value.  And on the same contract valued on its
    commutation month, where the column is blank, the weight is derived at ``t = 0``,
    ``lives_if_last(0)``, bit for bit ``DIA_US_S``'s ``commute_weight(252)``.
    """
    p = _row(sec_model, "derived", 15, 253)
    assert p.commute_weight_init() == pytest.approx(0.680338, abs=5e-7)
    assert p.surv_to_payout_init() == pytest.approx(0.715, rel=1e-9)
    assert p.commute_weight(0) == p.commute_weight_init()
    residual = p.annuity_pp_sched(0) * (p.surv_to_payout() - p.commute_weight(0))
    assert residual == pytest.approx(79.54, abs=0.005)
    paid = [p.annuity_payments(t) for t in range(p.proj_len())]
    assert paid[:107] == pytest.approx([residual] * 107, rel=1e-12)
    assert p.certain_floor(106) == 1.0 and p.certain_floor(107) == 0.0
    assert paid[107] == pytest.approx(919.16, abs=0.005)
    assert paid[107] == pytest.approx(
        p.annuity_pp_sched(107) * p.lives_if(108, 1), rel=1e-12)
    s15 = _point(s_model, 15)
    assert sum(paid[:107]) == pytest.approx(sum(s15.annuity_payments(253 + t)
                                                for t in range(107)), rel=1e-12)
    label = _label(_committed(), "derived", 15, 253)
    whole = _read_edited(tmp_path, _set("commute_weight_init", [label],
                                        p.surv_to_payout_init()), "whole")
    try:
        q = _point(whole, label)
        assert q.commute_weight(0) == q.surv_to_payout() == p.surv_to_payout_init()
        later = [q.annuity_payments(t) for t in range(q.proj_len())]
        assert later[:107] == [0.0] * 107
        assert later[107:] == paid[107:]
    finally:
        whole.close()
    key = _row_key(events, "derived", 15, 252)
    try:
        r = projection(events, key)
        assert pd.isna(r.model_point()["commute_weight_init"])
        assert r.commute_weight(0) == r.lives_if_last(0)
        assert r.commute_weight(0) == pytest.approx(
            _point(spliced[0], 15).commute_weight(252), rel=1e-15, abs=0.0)
    finally:
        _release(events, key, collect=True)


# The rows of the commutation residual's test, on the splice's inputs: each commuting point
# valued before, at and after its commutation, as (S point, source_mth).
COMMUTED = ((15, 251), (15, 252), (15, 253), (15, 360), (21, 252), (26, 250), (26, 252),
            (32, 365), (32, 390), (35, 252))


def test_the_commutation_residual_closes_at_the_guarantees_last_month(events, spliced):
    """The exchange residual is measured where the guarantee ends, reading back to the
    commutation, and is ``DIA_US_S``'s residual at the exercise, bit for bit.

    ``DIA_US_S`` computes ``check_commutation_value_resid`` at the commutation month, over
    every guaranteed month still to come, a read R2 does not admit.  This model sums the
    same months, month by month, in the same order and discounted from the exercise at the
    rate of the exercise month, at the guarantee's last month, policy month
    ``T + n_eff - 1``, reading back.  So on every row valued at or before its commutation,
    on the splice's inputs, its residual there is S's at the exercise, to the last bit:
    rounding, 8.7e-11 on point 15, 2.9e-11 on its quarterly variant, and exactly 0 on the
    commuting installment refund.  It is 0.0 in every other month, and on every row valued
    after the commutation, where the exchange closed before the valuation date or the
    commutation fell after the guarantee.  Its precedents at that month include the
    commutation itself, ``commutations(t_c)``.  A residual moved to the wrong month, or
    measured on ``t`` where ``duration_mth(t)`` belongs, is 0 there and passes every
    comparison at the floor; only this equality sees it.
    """
    s = spliced[0]
    for s_point, month in COMMUTED:
        key = _row_key(events, "derived", s_point, month)
        try:
            p = projection(events, key)
            sp = _point(s, s_point)
            c, d = p.commute_mth(), p.duration_mth_init()
            end = p.income_start_mth() + p.certain_mths_eff()
            residuals = [p.check_commutation_value_resid(t) for t in range(p.proj_len())]
            if d <= c < end:
                at = end - 1 - d
                assert residuals[at] == sp.check_commutation_value_resid(c), (
                    s_point, month, residuals[at], sp.check_commutation_value_resid(c))
                others = residuals[:at] + residuals[at + 1:]
                preds = {(node.obj.name, node.args) for node in
                         p.cells["check_commutation_value_resid"].preds(at)}
                assert ("commutations", (c - d,)) in preds, (s_point, month)
                assert p.check_commutation_value() is True
            else:
                others = residuals
            assert others == [0.0] * len(others), (s_point, month)
        finally:
            _release(events, key, collect=True)


def test_an_acceleration_needs_no_column(events, spliced):
    """An acceleration is read only in its exercise month, so nothing of it is opening
    state.

    On the splice's inputs, the acceleration contract valued in its exercise month, policy
    month 252, pays at ``t = 0`` S's lump sum, the instalment and the five it pulls forward,
    each weighted by the survival at the lump sum's own date, and nothing in the five
    blackout months after it.  Valued a month later, at 253, inside the blackout, the lump
    sum was paid before the valuation date: the blackout pays nothing through policy month
    257, ``accel_payment_factor`` is 0.0 at every month from the valuation date on, since
    nothing reads it, and the instalments resume at 258 as S's.  Valued the month before
    the exercise, at 251, the factor in the blackout is S's, read back at the exercise
    month on the valuation clock.
    """
    s14 = _point(spliced[0], 14)
    for month in (251, 252, 253):
        key = _row_key(events, "derived", 14, month)
        try:
            p = projection(events, key)
            a = p.accel_mth() - month
            paid = [p.annuity_payments(t) for t in range(p.proj_len())]
            assert paid == pytest.approx([s14.annuity_payments(month + t)
                                          for t in range(p.proj_len())], rel=1e-12)
            blackout = [t for t in range(p.proj_len()) if p.accel_blackout(t)]
            assert blackout == [t for t in range(a + 1, a + 6) if t >= 0], month
            assert all(paid[t] == 0.0 for t in blackout), month
            factors = [p.accel_payment_factor(t) for t in blackout]
            if a >= 0:
                assert paid[a] == pytest.approx(s14.annuity_payments(252), rel=1e-12)
                assert paid[a] > 5.0 * p.annuity_pp_sched(a) * p.payment_factor(a)
                assert factors == pytest.approx([s14.accel_payment_factor(month + t)
                                                 for t in blackout], rel=1e-12)
            else:
                assert factors == [0.0] * len(blackout)
                assert all(p.accel_payment_factor(t) == 0.0 for t in range(p.proj_len()))
                assert paid[a + 6] > 0.0
        finally:
            _release(events, key, collect=True)
    _release(spliced[0], _key(spliced[0], 14), collect=True)


def test_each_contract_reads_the_reference_rate_change_since_its_own_issue(s_model,
                                                                         tmp_path):
    """Each contract reads the reference rate's change since its own issue, on one path,
    floored as a whole.

    The commutation discount rate moves one for one with the reference rate's change since
    issue, floored at 0, and every contract of a block reads that change on one path of the
    reference rate, which every point shares (D7, as precised at M11).  Contracts issued at
    different dates have seen different changes by the valuation date, which
    ``ref_rate_shift_init`` carries, and the Reference ``ref_rate_shift`` is the change made
    at the valuation date, which every contract on the books there sees and a contract
    issued later, bought after it, does not.  One table holds three contracts on S point
    15's terms, all of them commuting at policy month 252: the point in force at its income
    start month, 240, its column set to 0.005; its twin, issued at the valuation date; and
    the same contract issued 13 months on.  Read with the Reference at 0, the point in force
    discounts at 5.75%, ``i_p + 0.005 + m_c``, its commuted value S's with S's change at
    0.005, and the other two at 5.25%, S's on its shipped rate.  Read with the Reference at
    0.005, the rate 50 basis points up again at the valuation date, the point in force
    discounts at 6.25%, S's at 0.010, the twin at 5.75%, S's at 0.005, and the contract
    issued later at 5.25% still, its commuted value unmoved.  A Reference read as the change
    since each contract's own issue would move the last too, and one ignored would leave the
    twin at 5.25%.

    The floor is on the whole change since issue, column and Reference added first (§7.9,
    *Record — M11*): a column of -0.01 at the Reference 0.005, a fall before the valuation
    date that a rise at it only part offsets, discounts at ``i_p + m_c``, 5.25%, where a
    floor on each part would give 5.75%; and a column of 0.01 at -0.005 at ``i_p + 0.005 +
    m_c``, 5.75%, where a floor on each part would give 6.25%.  The contract issued later
    reads 5.25% at every value.  Each value is set on a model read for it, before the model
    computes anything.
    """
    spec = dataclasses.replace(SPEC, derived=((15, 240),), future=((15, 13),))
    table, companions = build_sec_table(spec, s_model)
    in_force = _label(table.set_index("point_id"), "derived", 15, 240)
    later = _label(table.set_index("point_id"), "future", 15, -13)
    twin = 15

    def with_change(change):
        edited = table.set_index("point_id")
        return _set("ref_rate_shift_init", [in_force], change)(edited)

    def rates(change, shift, tag):
        folder = _sec_inputs(tmp_path / tag, with_change(change),
                             schedule=companions[SCHEDULE])
        model = _read(folder, tag, {"ref_rate_shift": shift})
        try:
            p, t15, f = (_point(model, i) for i in (in_force, twin, later))
            assert (p.ref_rate_shift_init(), t15.ref_rate_shift_init(),
                    f.ref_rate_shift_init(), f.t_entry()) == (change, 0.0, 0.0, 13)
            return ((p.commute_disc_rate(12), t15.commute_disc_rate(252),
                     f.commute_disc_rate(265)),
                    (p.commuted_value(12), t15.commuted_value(252), f.commuted_value(265)))
        finally:
            model.close()

    up = _read(model_path(TWIN), "s_rate_up", {"ref_rate_shift": 0.005})
    up_twice = _read(model_path(TWIN), "s_rate_up_twice", {"ref_rate_shift": 0.01})
    try:
        s15, s15_up, s15_up_twice = (_point(m, 15) for m in (s_model, up, up_twice))
        flat_rates, flat_values = rates(0.005, 0.0, "flat")
        step_rates, step_values = rates(0.005, 0.005, "step")
        assert flat_rates == pytest.approx((0.0575, 0.0525, 0.0525), rel=1e-12)
        assert step_rates == pytest.approx((0.0625, 0.0575, 0.0525), rel=1e-12)
        assert flat_values == pytest.approx((s15_up.commuted_value(252),
                                             s15.commuted_value(252),
                                             s15.commuted_value(252)), rel=1e-12)
        assert step_values == pytest.approx((s15_up_twice.commuted_value(252),
                                             s15_up.commuted_value(252),
                                             s15.commuted_value(252)), rel=1e-12)
        assert step_values[2] == flat_values[2]
    finally:
        up_twice.close()
        up.close()
    fall_rates, _ = rates(-0.01, 0.005, "fall")
    rise_rates, _ = rates(0.01, -0.005, "rise")
    assert fall_rates == pytest.approx((0.0525, 0.0575, 0.0525), rel=1e-12)
    assert rise_rates == pytest.approx((0.0575, 0.0525, 0.0525), rel=1e-12)


def test_mortality_improvement_is_calendar_dated_on_the_policy_clock(sec_model, s_model,
                                                                    events, spliced):
    """Improvement reads each contract's own calendar years, whatever the valuation date.

    The exponent is the calendar year of the policy year less ``mort_table_year``, and the
    calendar year is ``issue_year() + duration(t)``, on the policy clock (D7): a contract in
    force at the valuation date reads the improvement of the calendar years it reaches,
    from its own issue year, so nothing is re-based onto the valuation clock and the splice
    need not neutralize it.  On the generational point in force at its income start month,
    on the splice's set-apart scale, ``calendar_year(0)`` is 2046, and its rates at every
    ``t`` are S point 16's at month ``240 + t``, the improvement rates by age S's too, with
    no input re-based.  On the joint point issued 13 months on, at the shipped assumptions,
    ``calendar_year(13)``, its issue month, is 2026, and its rates are S point 8's ``13``
    months earlier, for both lives.
    """
    s16 = _point(spliced[0], 16)
    key = _row_key(events, "derived", 16, 240)
    try:
        p = projection(events, key)
        assert p.is_generational() and (p.issue_year(), p.calendar_year(0)) == (2026, 2046)
        for t in range(p.proj_len()):
            assert p.mort_rate(t, 1) == s16.mort_rate(240 + t, 1), t
            assert p.improvement_rate(t, 1) == s16.improvement_rate(240 + t, 1), t
    finally:
        _release(events, key, collect=True)
    later, s8 = _row(sec_model, "future", 8, -13), _point(s_model, 8)
    assert (later.duration_mth(13), later.calendar_year(13)) == (0, 2026)
    for t in range(s8.proj_len()):
        for life in (1, 2):
            assert later.mort_rate(13 + t, life) == s8.mort_rate(t, life), (t, life)


# The cap on mortality
#
# DIA_US_S caps the annual rate, the bound second, min(mort_ae_factor * q, 1.0), so that
# its monthly rate stays real at any A/E and a lost rate stays NaN, and this model caps it
# as S does, in mort_rate_py (USLIB-SEC-PLAN.md §5.1, step 6).  On the shipped tables the
# male rate is 1.0 at 118 and 119, so the cap changes no value there; under the splice's
# A/E of 1.05 it binds with an effect at male 117, and at omega inside a guarantee that
# outlasts the age stop.  The S points on which it binds inside the frame, each with the
# life it binds on, the first S month it binds in and the month before it, at which a row is
# restated in force, on the splice's inputs; each point's twin is new business there.
CAPPED = {
    8: (2, 648, 647),     # the joint annuitant, male, at 117
    18: (1, 684, 683),    # the male life on the table basis, at 117
    30: (1, 480, 479),    # omega inside a 30-year guarantee
}


def _uncapped_mort_rate(s, m, life):
    """``DIA_US_S``'s annual mortality of ``life`` in month ``m`` before its cap, from S's
    own cells: the A/E times the base rate, improved on the generational basis."""
    q = s.mort_rate_base(m, life)
    if s.mort_basis() == "generational":
        q = q * (1.0 - s.improvement_rate(m, life)) ** (s.calendar_year(m)
                                                        - s.mort_table_year)
    return s.mort_ae_factor * q


def test_a_capped_annual_mortality_is_the_float_1_in_both_models(sec_model, events,
                                                                  spliced):
    """Where the annual mortality product passes 1, both models' rate is the float 1.0, and
    the life's survival is exactly 0 after it.

    On each S point of :data:`CAPPED`, on the splice's inputs, ``DIA_US_S``'s product of
    the A/E, the base rate and, on the generational basis, the improvement, computed from
    S's own cells (:func:`_uncapped_mort_rate`), passes 1 in every month from the point's
    first capped month to the end of its frame.  Both models cap it there: ``mort_rate`` and
    ``mort_rate_mth`` are ``(float, 1.0)`` in each of those months, the type asserted with
    the value, since ``1 == 1.0`` would let an int cap through, and below 1 in every month
    before.  The life alive at the start of the first capped month dies in it, so that its
    survival is exactly 0 at every time point after, in both models.  Two rows of each
    point are read, its twin and the point restated in force the month before the cap,
    opened with S's state there: on each, every report is float64 and finite, and every
    cell of S's agrees with S at every argument S cached, the capped months included, to
    1e-9 relative with no absolute floor (:func:`_compared`), since survival where the cap
    binds is near 1e-8.  A cap applied to new business alone fails on the rows in force.
    On the shipped tables the joint annuitant of the committed joint twin reaches 118,
    where the table's rate is 1, and its rate is ``(float, 1.0)`` too.

    And the cap's order: on a model read with ``mort_ae_factor`` set to NaN before it
    computes anything, the anchor's twin's ``mort_rate(0, 1)`` is NaN, not 1.0.  The cap
    with its bound second keeps a lost value a NaN, where ``min(1.0, nan)`` is 1.0 and would
    pass it as certain death in month 0 with every flow finite; so would a cap on the
    monthly rate.  No reader is patched, so the case runs compiled at Phase 2 too.
    """
    s = spliced[0]
    found = []
    for s_point, (life, first, month) in CAPPED.items():
        sp = _point(s, s_point)
        try:
            _sweep(sp)
            end = sp.proj_len()
            assert [m for m in range(end) if sp.mort_rate(m, life) == 1.0] == list(
                range(first, end)), s_point
            assert all(_uncapped_mort_rate(sp, m, life) > 1.0 for m in range(first, end))
            assert all(sp.mort_rate(m, life) < 1.0 for m in range(first))
            found += [("S", s_point, m, rate.name) for m in range(first, end)
                      for rate in (sp.cells["mort_rate"], sp.cells["mort_rate_mth"])
                      if (type(rate(m, life)), rate(m, life)) != (float, 1.0)]
            assert sp.lives_if(first, life) > 0.0, s_point
            assert [sp.lives_if(m, life) for m in range(first + 1, end + 1)] == (
                [0.0] * (end - first)), s_point
            for case in (("derived", s_point, month), ("twin", s_point, 0)):
                key = _row_key(events, *case)
                try:
                    p = projection(events, key)
                    n, at = p.proj_len(), first - case[2]
                    capped = [t for t in range(n) if p.mort_rate(t, life) == 1.0]
                    assert capped == list(range(at, n)), (case, capped[:3])
                    found += [(case, t, rate.name) for t in capped
                              for rate in (p.cells["mort_rate"], p.cells["mort_rate_mth"])
                              if (type(rate(t, life)), rate(t, life)) != (float, 1.0)]
                    assert p.lives_if(at, life) > 0.0, case
                    assert [p.lives_if(t, life) for t in range(at + 1, n + 1)] == (
                        [0.0] * (n - at)), case
                    for frame in (p.result_cf(), p.result_pols()):
                        assert (frame.dtypes == "float64").all(), (case, frame.dtypes)
                        assert (frame.abs() < float("inf")).all().all(), case
                    exempt = SPLICE_EXEMPT if case[0] == "derived" else FUTURE_EXEMPT
                    assert _compared(sp, p, case[2], exempt) == [], case
                finally:
                    _release(events, key)
        finally:
            _release(s, _key(s, s_point), collect=True)
    assert not found, f"a capped rate that is not the float 1.0: {found[:5]}"
    joint = _point(sec_model, 8)
    rate = joint.mort_rate(12 * (118 - 63), 2)
    assert (type(rate), rate) == (float, 1.0)
    lost = _read(model_path(SEC), "lost", {"mort_ae_factor": NAN})
    try:
        q = _point(lost, 1).mort_rate(0, 1)
        assert q != q, f"mort_rate(0, 1) is {q!r} with a lost A/E"
    finally:
        lost.close()


# The model's four checks, each a bool over its residual's months (RESIDUALS).
CHECKS = ("check_lives_roll_fwd", "check_income_roll_fwd", "check_payment_factor",
          "check_commutation_value")


def test_a_residual_that_is_not_a_number_fails_its_check():
    """A check whose residual is not a number fails, as ``DIA_US_S``'s does.

    Each check asks whether every month's residual is within its tolerance, or is 0.0,
    never whether one is beyond it, so a NaN fails it, where ``abs(r) > tol`` would pass
    it.  On a model read with ``mort_ae_factor`` set to NaN before it computes anything,
    each life's monthly mortality is NaN, and so is its survival from ``t = 1``.  On every
    committed twin the survival roll-forward's residual is 0.0 at ``t = 0`` and NaN in
    every month after, and ``check_lives_roll_fwd()`` is ``False``.  On the twin of S point
    15, a 10-year period certain commuted in full at policy month 252, each of the four
    residuals is NaN in some month and 0.0 in every other, and each check is ``False``: what
    each check fails is the NaN.

    The other three are not asserted on every twin, because they read survival through
    ``DIA_US_S``'s own comparisons and ``max``, which can lose a NaN: ``nan > 0.0`` is
    ``False``, and ``max(0.0, nan)`` is 0.0.  On the anchor's twin, with no certain floor,
    the payment factor in its income phase is ``max(0.0, nan)``, and its residual 0.0; on
    the installment refund's twin the guarantee search finds no income, so no instalment is
    certain, each is valued at 0.0 and every premium buys 0.0, which the income
    roll-forward closes.  No formula is replaced, so the case runs compiled at Phase 2 too.
    """
    assert {f"{check}_resid" for check in CHECKS} == RESIDUALS
    model = _read(model_path(SEC), "nan", {"mort_ae_factor": NAN})
    try:
        table = model.Data.model_point_table()
        twins = table.index[table["row_kind"] == "twin"].tolist()
        assert len(twins) == 17
        for point_id in twins:
            p = _point(model, point_id)
            lives = [p.check_lives_roll_fwd_resid(t) for t in range(p.proj_len())]
            assert lives[0] == 0.0 and all(r != r for r in lives[1:]), point_id
            assert p.check_lives_roll_fwd() is False, point_id
            for check in CHECKS if point_id == 15 else ():
                resid = [p.cells[f"{check}_resid"](t) for t in range(p.proj_len())]
                assert any(r != r for r in resid), check
                assert all(r != r or r == 0.0 for r in resid), check
                assert p.cells[check]() is False, check
            _release(model, _key(model, point_id))
    finally:
        model.close()


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date dollars, for every point alike (D7).

    At the shipped 2.5%, the factor at ``t`` is ``1.025 ** (t // 12)`` on every point,
    whatever its duration: S's annual steps, moved onto the valuation clock.  So the period
    certain in force 300 months, valued on its anniversary, pays S's month ``300 + t``
    expenses deflated by ``1.025 ** 25``, the inflation S had already applied since issue;
    the anchor a month into its income phase, valued a month off its anniversary, pays S's
    month ``241 + t`` expenses divided by ``1.025 ** 20`` or ``1.025 ** 21``, as its policy
    years and the valuation years step apart; and the joint point issued 13 months on pays
    S's month ``t - 13`` maintenance times 1.025 or 1.025 squared, valuation years against
    policy years.  This is the only test that sees inflation run on the valuation clock:
    the splice sets the rate to 0, and on a point issued at ``t = 0`` the clocks agree.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    for key in point_keys(sec_model):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            assert p.inflation_factor(t) == (1.0 + INFLATION) ** (t // 12), (key, t)
    p, s = _row(sec_model, "derived", 7, 300), _point(s_model, 7)
    for t in range(p.proj_len()):
        assert p.expenses(t) == pytest.approx(
            s.expenses(300 + t) / (1.0 + INFLATION) ** 25, rel=1e-12), t
    for (kind, s_point, month), steps in ((("derived", 1, 241), {20, 21}),
                                          (("future", 8, -13), {-1, -2})):
        p, s = _row(sec_model, kind, s_point, month), _point(s_model, s_point)
        ratios = set()
        for t in range(max(0, -month), p.proj_len()):
            if p.expenses(t):
                ratio = s.expenses(month + t) / p.expenses(t)
                ratios |= {n for n in steps
                           if ratio == pytest.approx((1.0 + INFLATION) ** n, rel=1e-12)}
                assert any(ratio == pytest.approx((1.0 + INFLATION) ** n, rel=1e-12)
                           for n in steps), (s_point, t, ratio)
        assert ratios == steps, (s_point, ratios)


def test_new_business_brings_its_premiums_and_no_acquisition(sec_model):
    """A contract issued later brings its premium schedule into the frame, and no cost.

    ``DIA_US_S`` charges no acquisition cost, and neither does this model: on every point
    and in every month ``expenses(t)`` is the maintenance charge alone,
    ``expense_maint / 12 * inflation_factor(t) * pols_if(t)``, the issue month included,
    where ``Term_US_SEC`` charges acquisition per policy issued, and the gross outgo is the
    income, the claims, the commutations and that charge.  The joint point issued 13 months
    on brings its premiums as new business, weighted by its count and its survival from
    issue: the first, 100,000, at ``t = 13``, its issue month, and the second at policy
    month 60, ``t = 73``, ``50,000 * l_last(60)``; before issue there is none.
    """
    for key in point_keys(sec_model):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            assert p.expenses(t) == (
                p.expense_maint / 12.0 * p.inflation_factor(t) * p.pols_if(t)), (key, t)
            assert p.liability_outgo(t) == (p.annuity_payments(t)
                                            + p.claims(t, _code(p, "ALL"))
                                            + p.commutations(t) + p.expenses(t)), (key, t)
    later = _row(sec_model, "future", 8, -13)
    premiums = [later.premiums(t) for t in range(later.proj_len())]
    assert [t for t, x in enumerate(premiums) if x] == [13, 73]
    assert premiums[13] == 100000.0 == later.policy_count() * later.premium_pm(0)
    assert premiums[73] == 50000.0 * later.lives_if_last(73)
    assert later.pols_new_biz(13) == 1.0


def test_there_is_no_lapse_decrement_and_no_account_value(sec_model):
    """``pols_new_biz`` exists, meaning contracts issued; a lapse still does not.

    ``DIA_US_S``'s tests forbid every name that would make a DIA a deferred annuity with a
    balance: "A nonzero lapse assumption in a DIA model is a defect, not a margin", and the
    liability is a schedule of income slices, not a balance.  Running in force adds the
    count's names, ``pols_new_biz`` and ``pols_if_at`` among them, none of which is a lapse
    (``pols_if_at`` holds ``if_at``, not ``av_at``), and the same ban holds over every cell
    and Reference of both Spaces.  ``result_cf()`` keeps ``DIA_US_S``'s columns.
    """
    names = set(sec_model.Projection.cells) | set(sec_model.Projection.refs)
    names |= set(sec_model.Data.cells)
    assert {"pols_new_biz", "pols_if_at"} <= names
    forbidden = ("lapse", "surr_charge", "surrender", "av_pp", "av_at", "account_value",
                 "crediting", "credit_rate", "interim_value", "benefit_base",
                 "annuitization_rate", "free_withdrawal", "market_value_adj")
    bad = sorted((n, word) for n in names for word in forbidden if word in n)
    assert not bad, bad
    assert set(_point(sec_model, 1).result_cf().columns) == {
        "pols_if", "premiums", "annuity_payments", "claims", "commutations", "expenses",
        "liability_cf", "net_cf"}


def test_the_stop_rule_ends_every_frame(sec_model, s_model):
    """Every frame ends at the stop rule, S's frame from issue (D3).

    ``stop_mth()`` is S's frame length from issue, the age stop on the youngest covered
    life or the end of the guarantee if later, so it is S's ``proj_len()`` on every twin,
    and the frame runs from the valuation date to it: 661, 479, 420, 467, 599, 48, 450, 1
    and 733 months on the rows restated at policy months 59, 241, 300, 253, 121, 672, 270
    and 719 and the row issued 13 months on.  Its last month is policy month
    ``stop_mth() - 1`` on every point, inside cover, and the next is outside.  A contract's
    own end is no end of the frame: the anchor in its last month still carries a life,
    6.13e-08, and pays its instalment weighted by it.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        n = p.proj_len()
        assert n == p.stop_mth() - p.duration_mth_init(), point_id
        assert p.duration_mth(n - 1) == p.stop_mth() - 1, point_id
        assert p.is_active(n - 1) and not p.is_active(n), point_id
        if table.at[point_id, "row_kind"] == "twin":
            assert p.stop_mth() == _point(s_model, point_id).proj_len(), point_id
    rows = table.index[table["row_kind"] != "twin"]
    assert [_point(sec_model, i).proj_len() for i in rows] == [
        661, 479, 420, 467, 599, 48, 450, 1, 733]
    last = _row(sec_model, "derived", 1, 719)
    assert last.annuity_payments(0) == pytest.approx(
        _point(s_model, 1).annuity_payments(719), rel=1e-12)
    assert last.annuity_payments(0) > 0.0


def _outside_cover_faults(p, where):
    """Where ``p``, an ItemSpace that has evaluated nothing, departs from OUTSIDE_COVER.

    Every cell of :data:`OUTSIDE_COVER`, each of :data:`PER_LIFE` for every covered life,
    ``pols_if_at`` at each timing, ``claim_pp`` and ``claims`` at each kind and ``claims``
    at the total, ``ALL``, a float as each kind's is, in every
    month before issue and at ``t = proj_len()``, the month after the stop rule, which the
    closing time points read; and before issue :data:`BEFORE_ISSUE`'s time points and
    ``lives_if`` for both lives, all 0.0.  And ``phase``, ``PRE_ISSUE`` before issue and
    ``TERMINATED`` at ``t = proj_len()``, through :func:`_code`.  Then whether any of
    :data:`IN_COVER_ONLY` was evaluated on the way, which only a fresh ItemSpace can say.
    A cell that raises is reported as a fault too, so the scan goes on.
    """
    faults = []
    for t in [*range(p.t_entry()), p.proj_len()]:
        calls = [(name, (t,), want) for name, want in OUTSIDE_COVER.items()]
        calls += [(name, (t, life), 0.0) for name in PER_LIFE for life in _lives(p)]
        calls += [("pols_if_at", (t, _code(p, timing)), 0.0) for timing in TIMINGS]
        calls += [(name, (t, _code(p, kind)), 0.0) for name in ("claim_pp", "claims")
                  for kind in KINDS]
        calls.append(("claims", (t, _code(p, "ALL")), 0.0))
        if t < p.t_entry():
            calls += [(name, (t,), want) for name, want in BEFORE_ISSUE.items()]
            calls += [("lives_if", (t, life), 0.0) for life in (1, 2)]
        phase = "PRE_ISSUE" if t < p.t_entry() else "TERMINATED"
        calls.append(("phase", (t,), _code(p, phase)))
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


def _monthly_calls(p, t):
    """Every call of a monthly cell of ``p`` at ``t``: each life, kind and timing.

    A monthly cell is one whose first parameter is ``t``: each covered life for a
    ``(t, life)`` cell, and both lives for ``lives_if`` and ``lives_death``, which answer
    for a life the contract does not cover; each of :data:`KINDS` for a kind; each of
    :data:`TIMINGS` for a timing.
    """
    calls = []
    for name, cells in p.cells.items():
        params = cells.parameters
        if not params or params[0] != "t":
            continue
        if params == ("t",):
            calls.append((name, (t,)))
        elif params == ("t", "life"):
            lives = (1, 2) if name in ("lives_if", "lives_death") else _lives(p)
            calls += [(name, (t, life)) for life in lives]
        elif params == ("t", "kind"):
            calls += [(name, (t, _code(p, kind))) for kind in KINDS]
        elif params == ("t", "timing"):
            calls += [(name, (t, _code(p, timing))) for timing in TIMINGS]
        else:
            raise AssertionError(f"{name}{params}: a monthly cell the guard test does not "
                                 f"know how to call")
    return calls


def _guard_faults(p, where):
    """:func:`_outside_cover_faults`, then every monthly cell outside cover, and the keys.

    After the first scan, every monthly cell (:func:`_monthly_calls`) is called at the same
    months, as Phase 2's full sweep calls every cell of ``t`` from 0 to ``proj_len()``: none
    may raise, and afterwards every policy-clock and age-keyed cell's keys must lie inside
    the contract (:func:`_contract`).  Two kinds of key are reached on purpose: the closing
    time points at ``t = proj_len()``, which evaluate every covered month's rates, and
    ``is_active``, which on an installment refund searches its payout schedule, and so
    prices its premiums, for the refund period; neither may leave the contract.
    """
    faults = _outside_cover_faults(p, where)
    for t in [*range(p.t_entry()), p.proj_len()]:
        for name, args in _monthly_calls(p, t):
            try:
                p.cells[name](*args)
            except Exception as err:        # reported, so the scan goes on
                faults.append(f"{where}: {name}{args} raised {_raised(err)}")
    return faults + [f"{where}: {line}" for line in _outside_contract(p)]


def test_every_guarded_cell_holds_its_outside_cover_value(spliced):
    """Outside cover each cell holds :data:`OUTSIDE_COVER`'s value, and reads no rate.

    On every committed point, in every month before issue and in the month after the stop
    rule, ``t = proj_len()``, which the closing time points read, on a model that evaluates
    nothing else.  So afterwards none of :data:`IN_COVER_ONLY` may hold a value at all:
    ``is_active``'s docstring promises that outside cover no cell reads a rate, a policy
    year or an attained age the contract does not have.  Then every monthly cell is called
    at those months, as Phase 2's full sweep calls it, and the policy-clock and age keys it
    reaches must stay inside the contract (:func:`_guard_faults`).

    The committed table's one point issued after the valuation date is the joint cash
    refund, with no certain period, no option and no adjustment, so on it a cell tied to
    one of those would hold zero before issue, guarded or not.  So the same scan runs on the
    splice's future rows, the core's or, with ``USLIB_SEC_FULL=1``, all of them: the
    installment refund, the start-date adjustment, the acceleration, the commutation and a
    guarantee past the age stop among them, 13 months on, so that a read before issue lands
    at policy year -1.  Each row is made afresh first and released after.

    Several of these guards change no number the frame shows: once the counts are zero
    outside cover, every cash flow is too, and an unguarded value multiplies a zero count.
    They are held here because they are what the docstrings promise a caller, and because
    Phase 2 needs them: a table read at a policy year or an age the contract does not have
    would wrap round in a compiled model rather than fail (USLIB-SEC-PLAN.md F4, R1).
    """
    faults = []
    model = _read(model_path(SEC), "cover")
    try:
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


def test_the_points_sum_row_by_row_into_a_block(events, spliced):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    The anchor issued at the valuation date, in force 12 months and issued 13 months on,
    summed as ``run_sec.py --block`` sums them, are indexed 0..732 and equal S's frame added
    to itself moved 12 months earlier and 13 months later.  A model whose frames sat on the
    policy clock would fail it.  The three are read from one read of a table, on the
    splice's inputs (:data:`SEC_REFS`), as a block is read; the anchor holds no commutation,
    so the reference rate's change, which the splice's S reads 50 basis points up, moves no
    number of its frame.
    """
    keys = [_row_key(events, *case)
            for case in (("twin", 1, 0), ("derived", 1, 12), ("future", 1, -13))]
    try:
        frames = [projection(events, key).result_cf() for key in keys]
    finally:
        for key in keys:
            _release(events, key, collect=True)
    block = pd.concat(frames).groupby(level="t").sum()
    try:
        sdf = _point(spliced[0], 1).result_cf()
    finally:
        _release(spliced[0], _key(spliced[0], 1), collect=True)
    expected = pd.concat([sdf, sdf.set_axis(sdf.index - 12).loc[0:],
                          sdf.set_axis(sdf.index + 13)]).groupby(level=0).sum()
    assert list(block.index) == list(range(733))
    assert frame_mismatches(expected, block) == []


def test_result_annual_keeps_the_policy_year_key(sec_model, s_model):
    """The annual display is indexed by the policy year, from the valuation date's.

    ``result_annual`` keeps ``DIA_US_S``'s key, so a point in force shows the policy years
    from the one the valuation date falls in, and the years before it are left out, as
    ``Term_US_SEC``'s annual report leaves them out.  On the period certain in force 300
    months, valued on its anniversary, every row is S's year, policy years 26 to 60, in
    every column.  On the anchor a month into its income phase, valued a month after its
    anniversary, the first row, policy year 21, holds the months of that year on the books,
    policy months 241 to 251: its claims are those eleven months' and its CP, B and survival
    the year's closing values, S's; every later row is S's year.  The joint point issued 13
    months on starts at policy year 1, as S does.
    """
    on = _row(sec_model, "derived", 7, 300)
    mine, theirs = on.result_annual(), _point(s_model, 7).result_annual()
    assert list(mine.index) == list(range(26, 61))
    assert frame_mismatches(theirs.loc[26:], mine, atol=0.0) == []
    off = _row(sec_model, "derived", 1, 241)
    s1 = _point(s_model, 1)
    mine, theirs = off.result_annual(), s1.result_annual()
    assert list(mine.index) == list(range(21, 61))
    assert frame_mismatches(theirs.loc[22:], mine.loc[22:], atol=0.0) == []
    first, whole = mine.loc[21], theirs.loc[21]
    for c in ("age", "cum_premium_pp", "annual_income", "lives_if", "annuity_payments"):
        assert first[c] == pytest.approx(whole[c], rel=1e-12), c
    assert first["claims_refund"] == pytest.approx(
        sum(s1.claims(m, "REFUND") for m in range(241, 252)), rel=1e-12)
    assert first["claims_refund"] < whole["claims_refund"]
    later = _row(sec_model, "future", 8, -13).result_annual()
    assert list(later.index) == list(range(1, 61))


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


def _relabelled(table):
    """An administration extract of ``table``: no generator columns, labels moved by 100,
    the rows in reverse order.

    Every generated table numbers its points from 1, in table order, so on it a label and a
    position look alike; on this one they never agree.
    """
    extract = table.drop(columns=list(GENERATED_COLUMNS))
    extract.index = pd.Index(extract.index + 100, name="point_id")
    return extract.iloc[::-1]


def _relabelled_schedule(schedule):
    """The premium schedule of :func:`_relabelled`'s extract: each premium under its point's
    new label."""
    return schedule.assign(point_id=schedule["point_id"] + 100)


def test_an_in_force_extract_needs_none_of_the_generator_columns(sec_model, tmp_path):
    """The model reads the in-force interface and S's columns, never where a row came from.

    ``row_kind``, ``source_policy_id`` and ``source_mth`` record how the generator made each
    shipped row, and an administration extract carries none of them; nor does it number
    its points 1 to n in table order.  Read without them, relabelled 101..126 and reversed,
    its premium schedule relabelled with it (:func:`_relabelled`), each point projects what
    the committed row it was relabelled from projects, in ``result_cf`` and
    ``result_pols``, to 1e-12: every row in force or issued later, and the twins that carry
    each flow beside them (:data:`FLOW_TWINS`).  And ``run_sec.py``, run beside that
    extract, prints the point it was given by its label, 119, the anchor a month into its
    income phase, without saying where it came from.  On every shipped row ``source_mth``
    equals ``duration_mth``, so a formula that read the one for the other would pass every
    test that leaves ``duration_mth`` as generated.
    """
    extract = _relabelled(_committed())
    folder = _sec_inputs(tmp_path, extract,
                         schedule=_relabelled_schedule(_committed_schedule()))
    model = _read(folder, "extract")
    try:
        table = model.Data.model_point_table()
        assert not set(GENERATED_COLUMNS) & set(table.columns)
        assert list(table.index) == list(range(126, 100, -1))
        for point_id in (p + 100 for p in _flow_points(_committed())):
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
    out = _run_sec(runner, "119")
    assert out.splitlines()[:3] == [
        "model point 119: DIA-000001-M241 - NQ CR F60 - premiums due none",
        "deferral DB = ROP   income starts at policy month 240 (attained age 80)   m = 12 "
        "in arrears   COLA = 0%",
        "at the valuation date: in payout 1 month: policy year 21, lives 0.712045 alive, "
        "income 44,259.65/yr, 0 certain months left"]


def test_run_sec_block_refuses_before_printing(tmp_path):
    """``run_sec.py --block`` asks every point for its frame before it projects any.

    The point at or past the stop rule is refused in ``proj_len()`` when the block reaches
    it, which a loop over the block would do only after projecting the points before it.
    So the runner asks every point for its frame first: run beside the refused table, as an
    extract relabelled and reversed (:func:`_relabelled`) holds it, it exits non-zero,
    prints nothing, and names the point by its label, 125, not by its position.
    """
    extract = _relabelled(REFUSED[0][2](_committed()))
    folder = _sec_inputs(tmp_path, extract,
                         schedule=_relabelled_schedule(_committed_schedule()))
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert REFUSED[0][3].replace("point_id 25", "point_id 125") in done.stderr.decode(
        errors="replace")


def _shown(df):
    """A frame as ``run_sec.py`` prints it: to the cent, with no negative zero."""
    return (df.round(2) + 0.0).to_string()


def _standing(p):
    """What ``run_sec.py`` says of point ``p`` at the valuation date, stated here."""
    d = p.duration_mth_init()
    if d < 0:
        return f"to be issued at t = {-d}, {-d} months after the valuation date"
    if d == 0:
        return "issued at the valuation date, t = 0"
    alive = f"{p.lives_if_init(1):.6g}"
    if p.is_joint():
        alive += f" and {p.lives_if_init(2):.6g}"
    start = p.income_start_mth()
    if d < start:
        return (f"in deferral {d} month{'' if d == 1 else 's'}: policy year "
                f"{p.policy_year(0)}, lives {alive} alive, premiums paid "
                f"{p.cum_premium_pp_init():,.0f}, income bought "
                f"{p.annual_income_init():,.2f}/yr, the income starts at t = {start - d}")
    paid, left = d - start, max(start + p.certain_mths_eff() - d, 0)
    return (f"in payout {paid} month{'' if paid == 1 else 's'}: policy year "
            f"{p.policy_year(0)}, lives {alive} alive, income "
            f"{p.annual_income_init():,.2f}/yr, {left} certain month"
            f"{'' if left == 1 else 's'} left")


def test_run_sec_prints_a_point_and_the_block(sec_model):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  Point 1, the runner's default, the worked example's anchor issued at the
    valuation date, with its lines each asserted whole, so that a longer number cannot pass
    for the one asserted, and its first fifteen rows of cash flows and counts, as ``run.py``
    prints S's.  Point 19, the anchor a month into its income phase, point 26, the joint
    point issued 13 months on, and point 25, the anchor in its last month, each with the
    lines that say where its row came from and where it stands, which only the committed
    table's generator columns can say;
    point 25's frame has one row, and its headings say so, in the singular.  And the block:
    a line for each of the 26 points, in table order, its first fifteen rows, which must be
    the committed points' frames summed row by row, as this test sums them, and those frames
    summed into projection years, each year's ``pols_if`` its first month's.  Nothing else
    runs the runner on the committed table.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    head = ("proj_len = {} months from the valuation date (t = 0..{}); the stop rule at "
            "policy month 720")
    out = _run_sec(runner)
    assert out.splitlines()[:5] == [
        "model point 1: DIA-000001 (S's DIA-000001) - NQ CR F60 - premiums due 100,000 at "
        "month 0, 50,000 at month 60",
        "deferral DB = ROP   income starts at policy month 240 (attained age 80)   m = 12 "
        "in arrears   COLA = 0%",
        "at the valuation date: issued at the valuation date, t = 0",
        head.format(720, 719),
        "pricing factors = table   CP(T) = 150,000   B = 44,259.65/yr = 3,688.30/instalment"
        "   guarantee = 3.3891 yrs (0 certain months)"]
    assert "first 15 rows, t = 0..14 (months from the valuation date):" in out.splitlines()
    anchor = _point(sec_model, 1)
    assert _shown(anchor.result_cf().head(15)) in out
    assert (anchor.result_pols().head(15).round(6) + 0.0).to_string() in out
    for point_id, lines in (
            ("19", ["model point 19: DIA-000001-M241 (S's DIA-000001 at its month 241) - "
                    "NQ CR F60 - premiums due none",
                    "at the valuation date: in payout 1 month: policy year 21, lives "
                    "0.712045 alive, income 44,259.65/yr, 0 certain months left",
                    head.format(479, 478)]),
            ("26", ["model point 26: DIA-000008-F13 (S's DIA-000008, issued 13 months on) "
                    "- NQ CR F60 + M63 - premiums due 100,000 at month 0, 50,000 at month "
                    "60",
                    "at the valuation date: to be issued at t = 13, 13 months after the "
                    "valuation date",
                    head.format(733, 732)]),
            ("25", ["model point 25: DIA-000001-M719 (S's DIA-000001 at its month 719) - "
                    "NQ CR F60 - premiums due none",
                    "at the valuation date: in payout 479 months: policy year 60, lives "
                    "6.13203e-08 alive, income 44,259.65/yr, 0 certain months left",
                    "proj_len = 1 month from the valuation date (t = 0..0); the stop rule "
                    "at policy month 720"])):
        printed = _run_sec(runner, point_id).splitlines()
        assert [printed[0], *printed[2:4]] == lines, point_id
    for heading in ("the one row, t = 0 (months from the valuation date):",
                    "counts, survival and payment factors, the one row, t = 0:"):
        assert heading in printed, heading
    out = _run_sec(runner, "--block")
    table = sec_model.Data.model_point_table()
    points = [projection(sec_model, key) for key in point_keys(sec_model)]
    assert out.splitlines()[:len(points) + 1] == [
        "model points, t = 0 the valuation date for each:",
        *("  {:>2}  {:<16} {}; proj_len {}".format(
            point_id, table.at[point_id, "policy_id"], _standing(p), p.proj_len())
          for point_id, p in zip(table.index, points))]
    block = pd.concat([p.result_cf() for p in points]).groupby(level="t").sum()
    assert _shown(block.head(15)) in out
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", [block.at[12 * (y - 1), "pols_if"] for y in annual.index])
    assert _shown(annual.head(12)) in out


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
    opens the column, ``age`` of ``age(t, life)``.
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


# What only DIA_US_S's docstrings may say: a reference into its Spaces, which the SEC pages
# would link to the wrong model; its clock, t counting policy months from issue and t = 0
# the issue month; and "then clear the cache", modelx-only advice that a compiled model
# cannot follow.
STALE = re.compile(r"~\.DIA_US_S\.|``t`` counts \*\*policy months from issue"
                   r"|t counts months from issue|``t = 0`` is the issue month"
                   r"|then clear the cache")


def test_the_docstrings_describe_the_valuation_clock(sec_model, s_model):
    """The docstrings say what this model is, and none says what only DIA_US_S is.

    Whitespace is collapsed first, as ``test_model_conventions`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock, both SEC files and the product.  The
    cells running in force adds are exactly :data:`NEW_CELLS`, beside every cell of
    ``DIA_US_S``'s, and the symbol map in the Projection docstring maps each of them and
    names nothing the model lacks: every name in it is a cell, or a Reference the notes give
    a symbol to, as the A/E factor is in ``DIA_US_S``'s map.  And no docstring says what
    :data:`STALE` matches, which ``DIA_US_S``'s own docstrings say.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE, SCHEDULE,
                   "deferred income annuit"):
        assert phrase in flat["model"], phrase
    sec_cells, s_cells = set(sec_model.Projection.cells), set(s_model.Projection.cells)
    assert s_cells <= sec_cells, sorted(s_cells - sec_cells)
    assert sec_cells - s_cells == set(NEW_CELLS), sorted((sec_cells - s_cells)
                                                         ^ set(NEW_CELLS))
    mapped = _mapped_cells(sec_model.Projection.doc)
    missing = [cells for cells in NEW_CELLS if cells not in mapped]
    assert not missing, f"the symbol map does not map {missing}"
    known = set(sec_model.Projection.cells) | set(sec_model.Projection.refs)
    unknown = sorted(mapped - known)
    assert not unknown, f"the symbol map names what the model lacks: {unknown}"
    stale = sorted(where for where, doc in flat.items() if STALE.search(doc))
    assert not stale, f"docstrings that describe DIA_US_S: {stale}"
    s_flat = [re.sub(r"\s+", " ", doc) for _, doc in _docs(s_model)]
    assert all(any(re.search(part, doc) for doc in s_flat)
               for part in STALE.pattern.split("|")), "a STALE phrase S does not say"


def test_the_sec_model_reads_the_s_tables_in_place(sec_model, s_model):
    """One copy of each assumption table serves both models (D1).

    The two ``input_dir()`` s are one directory, and SEC's filename References are S's with
    ``model_point_file`` and ``premium_schedule_file`` alone changed, to
    ``model_point_table_sec.csv`` and ``premium_schedule_sec.csv``: an edit to an assumption
    table reaches both models, and the two can never drift apart.
    """
    assert sec_model.Data.input_dir() == s_model.Data.input_dir()
    files = {r: v for r, v in s_model.Data.refs.items() if r.endswith("_file")}
    assert {r: v for r, v in sec_model.Data.refs.items() if r.endswith("_file")} == {
        **files, "model_point_file": TABLE, "premium_schedule_file": SCHEDULE}


def test_the_core_grid_reaches_every_branch(spliced, splice_records):
    """What the default run's T2 and T3 cases reach, which the full grid only multiplies.

    The default run thins the splice to a core (the module docstring), and this test is
    what keeps the thinning from costing a branch.  First, statically, over S's table with
    the variants, each property below holds of some core case: each form; joint and single
    lives; each trigger on a joint contract; each mortality and factor basis; each timing
    and frequency, and each frequency below monthly with each timing valued off its period,
    where a payment month counted on the wrong clock shows; each market type and
    death-benefit form; each sex in each role; a COLA and none on a refund form; a rounding
    of the purchase rate to 6 and to 4 places and none; each option, the adjustment
    deferring and advancing; and each kind of valuation month: an anniversary, mid-year,
    the month before a premium and the premium's own, the income start month and the month
    before it, each option's month and a month after it, a guarantee's last month, and the
    last month of a frame.  Of some core future case: issued 1, 12 and more than 12
    months on, joint and single, each refund form, a guarantee, each option.  And the
    splice's two edited tables give every ``(age, sex)`` below omega a value of its own, so
    that a join on the wrong key changes a number.

    Then, on the splice's model, of some core row, each of :data:`AT_VALUATION` and
    :data:`IN_FRAME`, what no column of the table shows: every opening-state column at each
    value it takes, what falls at ``t = 0`` because of where the contract stands, and each
    branch of the refund, the guarantees, the options, the cap and the QLAC overlay later in
    the frame.  Each core row's branches were recorded by the case that compared it
    (:func:`_record`), and a row no case has recorded is evaluated here.
    """
    s = spliced[0]
    s_table = _s_table_with_variants()

    def at(p, column):
        return s_table.at[p, column]

    def option(p, column):
        value = at(p, column)
        return -1 if pd.isna(value) else int(value)

    def start(p):
        return option(p, "adjust_start_mth") if option(p, "adjust_mth") >= 0 else int(
            at(p, "income_start_mth"))

    def n_eff(p):
        return _point(s, p).certain_mths_eff()

    def premium_months(p):
        return set(_point(s, p).premium_by_mth())

    def step(p):
        return 12 // int(at(p, "frequency"))

    splices = {
        **{f"the {f} form": (lambda k, p, d, f=f: at(p, "income_form") == f)
           for f in ("LO", "LO_ROP", "CR", "IR", "PC")},
        "a joint contract": lambda k, p, d: at(p, "joint"),
        "a single life": lambda k, p, d: not at(p, "joint"),
        **{f"the {trig} trigger, joint": (lambda k, p, d, trig=trig: (
            at(p, "joint") and at(p, "reduction_trigger") == trig))
           for trig in ("either", "primary")},
        **{f"the {b} mortality basis": (lambda k, p, d, b=b: at(p, "mort_basis") == b)
           for b in ("anchor", "generational")},
        **{f"the {b} factor basis": (lambda k, p, d, b=b: at(p, "factor_basis") == b)
           for b in ("table", "formula")},
        **{f"{m} timing": (lambda k, p, d, m=m: at(p, "timing") == m)
           for m in ("arrears", "advance")},
        **{f"{m} payments a year": (lambda k, p, d, m=m: at(p, "frequency") == m)
           for m in (12, 4, 2, 1)},
        **{f"the {m} market": (lambda k, p, d, m=m: at(p, "market_type") == m)
           for m in ("NQ", "TradIRA", "RothIRA", "QLAC")},
        **{f"the {f} death benefit": (lambda k, p, d, f=f: at(p, "db_form") == f)
           for f in ("ROP", "NONE")},
        **{f"a {sex} {role}": (lambda k, p, d, sex=sex, c=c: (
            (c == "sex" or at(p, "joint")) and at(p, c) == sex))
           for sex in ("M", "F") for role, c in (("primary", "sex"),
                                                 ("joint annuitant", "joint_sex"))},
        "a COLA on a refund form": lambda k, p, d: (
            at(p, "income_form") in ("CR", "IR") and at(p, "cola_rate") > 0.0),
        "no COLA on a refund form": lambda k, p, d: (
            at(p, "income_form") in ("CR", "IR") and at(p, "cola_rate") == 0.0),
        **{f"a purchase rate rounded to {n} places": (
            lambda k, p, d, n=n: at(p, "purchase_rate_dp") == n) for n in (6, 4)},
        "a purchase rate at full precision": lambda k, p, d: pd.isna(
            at(p, "purchase_rate_dp")),
        "other QLAC premium": lambda k, p, d: at(p, "other_qlac_premium") > 0.0,
        "an adjustment deferring the start": lambda k, p, d: (
            option(p, "adjust_mth") >= 0 and start(p) > at(p, "income_start_mth")),
        "an adjustment advancing the start": lambda k, p, d: (
            option(p, "adjust_mth") >= 0 and start(p) < at(p, "income_start_mth")),
        "on an anniversary": lambda k, p, d: d % 12 == 0,
        "mid-year": lambda k, p, d: d % 12 not in (0, 11),
        "the month before a premium": lambda k, p, d: d + 1 in premium_months(p),
        "a premium month": lambda k, p, d: d in premium_months(p) and d > 0,
        "the month before the income start": lambda k, p, d: d == start(p) - 1,
        "the income start month": lambda k, p, d: d == start(p),
        **{f"valued in the {o} month": (
            lambda k, p, d, o=o: option(p, o) >= 0 and d == option(p, o))
           for o in ("adjust_mth", "accel_mth", "commute_mth")},
        **{f"valued after the {o} month": (
            lambda k, p, d, o=o: 0 <= option(p, o) < d)
           for o in ("adjust_mth", "accel_mth", "commute_mth")},
        "in a guarantee's last month": lambda k, p, d: n_eff(p) > 0 and (
            d == start(p) + n_eff(p) - 1),
        "in the last month of a frame": lambda k, p, d: d == _point(s, p).proj_len() - 1,
    }
    pairs = {(int(at(p, "frequency")), at(p, "timing")) for p in s_table.index
             if at(p, "frequency") != 12}
    for m, timing in sorted(pairs):
        splices[f"{m} a year in {timing}, off its period"] = (
            lambda k, p, d, m=m, timing=timing:
            (int(at(p, "frequency")), at(p, "timing")) == (m, timing)
            and (d - start(p)) % step(p) != 0)
    futures = {
        "issued a month on": lambda p, k: k == 1,
        "issued a year on": lambda p, k: k == 12,
        "issued more than a year on": lambda p, k: k > 12,
        "a joint contract": lambda p, k: at(p, "joint"),
        "a single life": lambda p, k: not at(p, "joint"),
        **{f"the {f} form": (lambda p, k, f=f: at(p, "income_form") == f)
           for f in ("CR", "IR", "PC")},
        **{f"the {o} option": (lambda p, k, o=o: option(p, o) >= 0)
           for o in ("adjust_mth", "accel_mth", "commute_mth")},
    }
    missing = [what for what, holds in splices.items()
               if not any(holds(*case) for case in CORE_SPLICES)]
    missing += [what for what, holds in futures.items()
                if not any(holds(*case) for case in CORE_FUTURES)]
    assert not missing, f"no core case reaches: {missing}"
    assert len(pairs) == 6, sorted(pairs)

    for name, column in (("mort_table", "mort_rate"),
                         ("improvement_scale", "improvement_rate")):
        rates = s.Data.cells[name]()[column]
        below = rates[rates.index.get_level_values("age") < s.Projection.omega_age]
        assert below.is_unique, f"{name}: two (age, sex) rows share a value"

    reached = set()
    for case in sorted(CORE_GRID, key=str):
        reached |= _record_of(spliced, splice_records, case)["branches"]
    missing = [what for what in (*AT_VALUATION, *IN_FRAME) if what not in reached]
    assert not missing, f"no core row reaches: {missing}"


# ---------------------------------------------------------------------------
# Phase 2's representation (USLIB-SEC-PLAN.md §6.1, M24)
#
# What the compiled representation changes, held in modelx, in every run: what a point
# cannot use is refused by the point alone; the contract the caches are sized for; every
# form from issue age 0; the totals, the schedule and the rounding as S computes them; the
# tables numbered by their own sexes; the vectors' dtypes; the spec and the sample against
# their comments; and the runner's block sum and build decision.  None needs modelx-cython.


INF = float("inf")

# What a Data vector holds that a point's projection cannot use, each refused by the
# point's own Projection accessor where it reads it, naming the point, and nowhere else,
# so that no point is refused for another's value, nor for a column its projection never
# reads (D2), as (case, column, point_id, value, whether the point is refused, the
# accessor, its arguments).  Each case is one point of one copy of the committed table,
# which holds them all.  Every value Data's checks let through and int() cannot read below
# 2**53 in size: a number of 2**53 or more, either sign, where the table's checks accept
# it, and a joint age written as text on a single life, whose joint_age no check reads.
# The points that project hold the value outside the accessor's scope: a certain period on
# a form without one, an issue year on the anchor basis, a single life's joint age.
_INT = "{} must be a number int() reads, below 2**53 in size; it is not"
_MONTHS = "{} must be blank or below 2**53 months in size; it is not"
NOT_DECODABLE = [
    ("a duration of 2**53 or more", "duration_mth", 19, 1e20, True, "duration_mth_init",
     (), _INT.format("duration_mth")),
    ("an issue age of 2**53 or more", "issue_age", 2, 1e20, True, "age_at_entry", (1,),
     _INT.format("issue_age")),
    ("a joint issue age of 2**53 or more", "joint_age", 9, 1e20, True, "age_at_entry",
     (2,), _INT.format("joint_age")),
    ("a certain period of 2**53 or more on a period certain", "certain_period", 7, 1e20,
     True, "certain_period", (), _INT.format("certain_period")),
    ("an income start month of 2**53 or more", "income_start_mth", 10, 1e20, True,
     "income_start_mth_init", (), _INT.format("income_start_mth")),
    ("a frequency of 2**53 or more", "frequency", 12, 1e20, True, "payment_freq", (),
     _INT.format("frequency")),
    ("an issue year of 2**53 or more on the generational basis", "issue_year", 16, 1e20,
     True, "issue_year", (), _INT.format("issue_year")),
    ("a rounding of 2**53 or more", "purchase_rate_dp", 1, 1e20, True, "purchase_rate_dp",
     (), "purchase_rate_dp must be blank or below 2**53 in size; it is not"),
    ("an adjustment month of -2**53 or less", "adjust_mth", 11, -1e20, True, "adjust_mth",
     (), _MONTHS.format("adjust_mth")),
    ("a new start month of 2**53 or more", "adjust_start_mth", 13, 1e20, True,
     "adjust_start_mth", (), _MONTHS.format("adjust_start_mth")),
    ("an acceleration month of 2**53 or more", "accel_mth", 14, 1e20, True, "accel_mth",
     (), _MONTHS.format("accel_mth")),
    ("a commutation month of 2**53 or more", "commute_mth", 15, 1e20, True, "commute_mth",
     (), _MONTHS.format("commute_mth")),
    ("a single life's joint age written as text", "joint_age", 3, "x", False,
     "age_at_entry", (2,), _INT.format("joint_age")),
    ("a certain period of 2**53 or more on a cash refund", "certain_period", 4, 1e20,
     False, "certain_period", (), _INT.format("certain_period")),
    ("an issue year of 2**53 or more on the anchor basis", "issue_year", 17, 1e20, False,
     "issue_year", (), _INT.format("issue_year")),
]


def _not_decodable_table():
    """The committed table with every value of :data:`NOT_DECODABLE` written in."""
    table = _committed()
    for _, column, point, value, *_ in NOT_DECODABLE:
        table = _set(column, [point], value)(table)
    return table


def _did(call):
    """``("ok", value)`` or ``("raised", "Type: message")``: what ``call()`` did."""
    try:
        return ("ok", call())
    except Exception as err:                    # what was raised is what is compared
        return ("raised", _raised(err))


def test_a_value_a_point_cannot_use_is_refused_by_the_point_alone(sec_model, tmp_path):
    """Each point is refused for its own value, where its projection reads it (D2, R7).

    ``Data`` holds each int column a projection reads in an int64 vector, read element by
    element through ``int()`` as stage ``E`` read the point's value, and beside it a 0/1
    ``_ok`` vector, 0 where ``int()`` raises or the value is ``2**53`` or more in size,
    which the int64 vector cannot be trusted to hold (USLIB-SEC-PLAN.md §7.10, *Record --
    M20*).  The point's own ``Projection`` accessor reads the flag and refuses the value,
    naming the point.  So, on one copy of the committed table holding every case of
    :data:`NOT_DECODABLE`: the table reads; each refused point's ``result_cf()`` is
    refused with its accessor's message, and so is a direct call of the accessor; every
    other point projects the committed model's numbers exactly, those holding a value
    outside its accessor's scope among them; and on those, a direct call of the accessor
    still refuses the value.  A refusal moved to ``Data`` would refuse the whole table, a
    scope widened would refuse a point the model projects, and a flag lost would project
    from 0, the vector's value there.
    """
    points = [case[2] for case in NOT_DECODABLE]
    assert len(set(points)) == len(points), "each case is a point of its own"
    model = _read(_sec_inputs(tmp_path, _not_decodable_table()), "not_decodable")
    try:
        table = model.Data.model_point_table()
        assert len(table) == len(_committed())
        found = []
        for case, _, point, _, is_refused, cell, args, what in NOT_DECODABLE:
            p = _point(model, point)
            want = ("raised", f"ValueError: point_id {point}: {what}")
            got = _did(lambda: p.cells[cell](*args))
            if got != want:
                found.append(f"{case}: {cell}{args} did {got}, not {want}")
            did = _did(p.result_cf)
            if is_refused and did != want:
                found.append(f"{case}: result_cf() did {did[0]} {did[1]!r:.120}")
            if not is_refused and did[0] != "ok":
                found.append(f"{case}: result_cf() raised {did[1]!r:.120}")
        assert not found, "\n".join(found)
        refused = {case[2] for case in NOT_DECODABLE if case[4]}
        for point in table.index:
            if point in refused:
                continue
            mine, base = _point(model, point), _point(sec_model, point)
            for report in REPORTS:
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=0, atol=0) == [], (point, report)
            _release(model, _key(model, point))
    finally:
        model.close()


# The int columns a projection reads, each written as a fraction on a point whose
# projection reads it, as (column, point_id, value): Data refuses each as the table is
# read, naming the column and the point, where DIA_US_S's int() truncates it (stage E's
# whole-number checks, M12).  joint_age is read on a joint contract alone, and checked
# there.  So no fraction reaches an int64 vector of a point that reads it, and there is
# no fraction to compare with DIA_US_S's truncation.
FRACTIONS = [
    ("duration_mth", 19, 241.5), ("issue_age", 2, 60.5), ("joint_age", 8, 63.5),
    ("certain_period", 7, 10.5), ("income_start_mth", 10, 240.5), ("frequency", 12, 12.5),
    ("issue_year", 16, 2026.5), ("purchase_rate_dp", 1, 6.5), ("adjust_mth", 13, 120.5),
    ("adjust_start_mth", 13, 300.5), ("accel_mth", 14, 252.5), ("commute_mth", 15, 252.5),
]


def test_a_fraction_in_an_int_column_is_refused_as_the_table_is_read(tmp_path):
    """No int column a projection reads holds a fraction: ``Data`` refuses it at load.

    ``Data``'s int64 vectors read each value through ``int()``, which would truncate a
    fraction as ``DIA_US_S``'s accessors do, so a fraction that reached one would be a
    number compared with S's truncation (USLIB-SEC-PLAN.md §7.9, *Record -- M23*).  Here
    there is none to compare: each case of :data:`FRACTIONS`, every int column of
    ``Data``'s table that has an ``_ok`` flag, is refused by ``model_point_table()``,
    naming the column and the point, as stage ``E`` refused it.  A whole-number check
    lost on any of them fails here, and the fraction would then project truncated.
    """
    assert {column for column, *_ in FRACTIONS} == {
        name[:-3] for name in _vector_kinds() if name.endswith("_ok")}
    found = []
    for number, (column, point, value) in enumerate(FRACTIONS):
        model = _read(_sec_inputs(tmp_path / f"f{number}",
                                  _set(column, [point], value)(_committed())), "fraction")
        try:
            did = _did(model.Data.model_point_table)
        finally:
            model.close()
        if (did[0] != "raised" or column not in did[1]
                or f"point_id [{point}]" not in did[1]):
            found.append(f"{column} {value} on point {point}: {did[0]} {did[1]!r:.150}")
    assert not found, "\n".join(found)


# A point the contract does not issue, refused by stop_mth() in its rules' order, naming
# the point, as (case, the table's edit, the label, the message, the References that issue
# it, its frame then): an issue age of a covered life below issue_age_min, raised here to
# 61 and 64, since Data refuses a negative age at load; an income start month, at issue
# and in force after an adjustment, past 12 * (omega_age - issue_age_min), 1,440; and a
# period certain ending past it.  DIA_US_S projects each, and so does this model once the
# bound is moved: issue_age_min lowered to 60 and 63, or to -1, which widens the latest
# month to 1,452.  The issue ages' rules come before the months'.
_PAST = ("past 12 * (omega_age - issue_age_min), 1440, the latest policy month the caches "
         "are sized for")
NOT_ISSUED = [
    ("an issue age below issue_age_min", None, 1,
     "point_id 1: issue age 60 is below issue_age_min, 61", {"issue_age_min": 61},
     {"issue_age_min": 60}, 720),
    ("a joint issue age below issue_age_min", _set("issue_age", [8], 65), 8,
     "point_id 8: joint issue age 63 is below issue_age_min, 64", {"issue_age_min": 64},
     {"issue_age_min": 63}, 684),
    ("an income start month of 1,441", _set("income_start_mth", [3], 1441), 3,
     f"point_id 3: income_start_mth 1441 is {_PAST}", {}, {"issue_age_min": -1}, 1441),
    ("a new start month of 1,441", _set("adjust_start_mth", [13], 1441), 13,
     f"point_id 13: adjust_start_mth 1441 is {_PAST}", {}, {"issue_age_min": -1}, 1441),
    ("a period certain ending at policy month 1,441",
     _set("income_start_mth", [7], 1321), 7,
     f"point_id 7: the certain period of 10 years from policy month 1321 ends {_PAST}", {},
     {"issue_age_min": -1}, 1441),
    ("an issue age and a month past the caches: the age's rule first",
     _set("income_start_mth", [3], 1441), 3,
     "point_id 3: issue age 60 is below issue_age_min, 61", {"issue_age_min": 61}, None,
     None),
]

# The months just inside: an income start month of 1,440 and a period certain ending at
# 1,440, each projecting its frame to the stop rule, as (the edit, the label, the frame).
JUST_ISSUED = [(_set("income_start_mth", [3], 1440), 3, 1440),
               (_set("income_start_mth", [7], 1320), 7, 1440)]


@pytest.mark.parametrize("case, edit, label, message, refs, issue, frame", NOT_ISSUED,
                         ids=[c[0] for c in NOT_ISSUED])
def test_a_point_the_contract_does_not_issue_is_refused_by_stop_mth(tmp_path, case, edit,
                                                                    label, message, refs,
                                                                    issue, frame):
    """``stop_mth()`` refuses a point the caches cannot hold, naming it (§6.1, F4).

    ``DIA_US_S`` projects a contract at any issue age, from any income start month, with
    any certain period, but the compiled caches are sized from the contract
    (``spec_sec.py``): every life from ``issue_age_min``, 0, since a frame runs to the age
    stop on its youngest life, and every month of the payout schedule to ``12 *
    (omega_age - issue_age_min)``, 1,440.  A point past them would run past a cache, so
    ``stop_mth()`` refuses it before the stop rule, which searches the installment
    refund's schedule: each case of :data:`NOT_ISSUED`, the joint annuitant's age among
    them, and in force the adjusted start month, by the rule asked first.  The table reads,
    since these are rules of the product, and every report is refused, with the frame and
    ``stop_mth()`` itself.  Each projects once its bound is moved, to the frame its stop
    rule gives, its checks passing: the Reference is what refuses each, and a bound off by
    one, a rule lost or asked in another order, lets a point through or names the wrong
    rule.  The months just inside (:data:`JUST_ISSUED`) project at the shipped bound.
    """
    model = _read_edited(tmp_path, edit, "not_issued", refs)
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        p = _point(model, label)
        for cell in (*REPORTS, "proj_len", "stop_mth"):
            _refused(p.cells[cell], message)
    finally:
        model.close()
    if issue is None:
        for number, (edit, label, frame) in enumerate(JUST_ISSUED):
            model = _read_edited(tmp_path / f"inside{number}", edit, "inside")
            try:
                p = _point(model, label)
                assert p.proj_len() == len(p.result_cf()) == frame, label
                assert p.check_lives_roll_fwd() and p.check_income_roll_fwd()
            finally:
                model.close()
        return
    model = _read_edited(tmp_path / "issued", edit, "issued", issue)
    try:
        p = _point(model, label)
        assert p.proj_len() == len(p.result_cf()) == frame
        assert p.check_lives_roll_fwd() and p.check_payment_factor()
        assert p.check_income_roll_fwd()
    finally:
        model.close()


def _s_and_sec(tmp_path, rows, schedule, edits=None):
    """S and SEC read on the same contracts: S's table ``rows`` and its premium
    ``schedule``, each point the twin of its S point, and the SEC twins of the same rows,
    with the same schedule under the same labels, both on the tables ``edits`` give."""
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    s_rows = pd.concat([s_table.loc[[point]].assign(**columns) for point, columns in rows])
    sec_rows = pd.concat([_committed().loc[[point]].assign(**columns)
                          for point, columns in rows])
    s_edits = {**(edits or {}), "premium_schedule.csv": schedule}
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=s_rows,
                          edits=s_edits), "s_on")
    sec = _read(_sec_inputs(tmp_path / "sec", sec_rows, edits, schedule), "sec_on")
    return s, sec


def _premiums(*rows):
    """A premium schedule of ``(point_id, premium_mth, premium_amt)`` rows, in order."""
    return pd.DataFrame([{"point_id": p, "slice": n, "premium_mth": m, "premium_amt": a,
                          "provenance": "[std] a test case"}
                         for n, (p, m, a) in enumerate(rows, 1)])


# Points DIA_US_S projects from issue age 0, on age tables extended to 0 (FROM_AGE_0), as
# (the S point, its columns): the joint cash refund on the primary's death at 0 and 0, the
# period certain at 0, and the joint cash refund on either death with its first life at
# 119 and its second at 0, its income at policy month 24, after premiums at 0 and 13: the
# first life is 10% alive at the second premium and dead by the income start month, so
# that the pricing guarantee's iteration runs on the second life alone (M24).
YOUNG = [(9, {"issue_age": 0, "joint_age": 0}), (7, {"issue_age": 0}),
         (8, {"issue_age": 119, "joint_age": 0, "income_start_mth": 24})]
YOUNG_PREMIUMS = ((9, 0, 100000.0), (9, 60, 50000.0), (7, 0, 100000.0), (7, 60, 50000.0),
                  (8, 0, 100000.0), (8, 13, 50000.0))


def test_every_form_from_issue_age_0_continues_s(tmp_path):
    """Every form projects from issue age 0, as ``DIA_US_S`` projects it, to the last bit
    of its pricing.

    ``DIA_US_S`` projects any issue age, and its frame runs to the age stop on its
    youngest life, so the contract the compiled caches are sized for starts every life at
    ``issue_age_min``, 0, below the 22 product-spec issues at.  Each case of :data:`YOUNG`,
    on tables extended to age 0 (:data:`FROM_AGE_0`), projects 1,440 months, its checks
    passing, and S's point and its twin are swept and compared cell by cell, as T1
    compares them, to 1e-9 relative with no floor.  On the joint point at 119 and 0, whose
    pricing guarantee iterates the kernel inline over a schedule whose first life dies in
    the deferral, ``guarantee_mths_pricing()`` and the purchase rate of each premium are
    S's to the last bit (``float.hex``): an inline copy of the kernel that returned from
    the outer cell, or shared a local with it, moves them.  The compiled model is held to
    modelx at these ages by the extremes' C4.
    """
    s, sec = _s_and_sec(tmp_path, YOUNG, _premiums(*YOUNG_PREMIUMS), FROM_AGE_0)
    try:
        for point, _ in YOUNG:
            theirs, mine = _point(s, point), _point(sec, point)
            assert mine.proj_len() == len(mine.result_cf()) == 1440, point
            assert mine.check_lives_roll_fwd() and mine.check_income_roll_fwd(), point
            _sweep(theirs)
            _sweep(mine)
            assert _mismatches(theirs, mine, exempt=TWIN_EXEMPT_DEFAULT | SPEC.exempt,
                               atol=0.0) == [], point
        theirs, mine = _point(s, 8), _point(sec, 8)
        assert theirs.lives_if(12, 1) < 0.1 and theirs.lives_if(24, 1) == 0.0
        assert mine.guarantee_mths_pricing().hex() == theirs.guarantee_mths_pricing().hex()
        for k in (0, 13):
            assert mine.purchase_rate(k).hex() == theirs.purchase_rate(k).hex(), k
    finally:
        sec.close()
        s.close()


# The exercise months of S point 14's acceleration, the anchor issued at 60 and
# accelerating, each a point of its own: the age stop, policy month 720, the month after
# it, the first month past the pricing survival's cache, 1,447, and a later one.  An A/E
# below 1 takes the rate past the limiting age off 1, so that S's survival there is
# positive (M24).
PAST_STOP = (720, 721, 1447, 1500)
BELOW_ONE_AE = 0.5


def test_an_acceleration_past_the_age_stop_costs_what_s_costs(tmp_path):
    """``accel_cost()`` is ``DIA_US_S``'s cost, to the last bit, for an exercise at or past
    the age stop, however late.

    ``Data`` bounds an exercise month from below alone, so a point may accelerate after its
    stop rule, and projects; the pricing survival's cache ends at policy month 1,446.  At
    the shipped A/E the rate is 1 from the limiting age on, and S's survival is 0 in every
    month after the stop, so its cost there is 0, which this model gives reading the
    survival a month after the stop alone (M24).  On S point 14 at each month of
    :data:`PAST_STOP`, each its own point, ``accel_cost()`` is S's by ``float.hex``,
    positive at the stop and 0 after it, where S's survival at the exercise is 0, and each
    frame is S's 720 months.  At :data:`BELOW_ONE_AE` S's survival past the stop is
    positive, and so is its cost, which this model reads on as S does: S's again, by
    ``float.hex``.  A shortcut that answered 0 past the stop whatever the A/E fails here;
    the compiled model is held to modelx at these months by the extremes' C4.
    """
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    s_due = pd.read_csv(model_path(TWIN).parent / "premium_schedule.csv")
    s_due = s_due[s_due["point_id"] == 14]
    labels = range(1, len(PAST_STOP) + 1)
    s_rows = pd.concat([s_table.loc[[14]].assign(accel_mth=a) for a in PAST_STOP])
    sec_rows = pd.concat([_committed().loc[[14]].assign(accel_mth=a) for a in PAST_STOP])
    s_rows.index = sec_rows.index = pd.Index(labels, name="point_id")
    schedule = _premiums(*((label, m, a) for label in labels
                           for m, a in zip(s_due["premium_mth"], s_due["premium_amt"])))
    s_inputs = temp_inputs(tmp_path / "s", model_path(TWIN), model_points=s_rows,
                           edits={"premium_schedule.csv": schedule})
    sec_inputs = _sec_inputs(tmp_path / "sec", sec_rows, None, schedule)
    for ae, months in ((1.0, PAST_STOP), (BELOW_ONE_AE, PAST_STOP[:3])):
        s = _read(s_inputs, "s_accel", {"mort_ae_factor": ae})
        sec = _read(sec_inputs, "accel", {"mort_ae_factor": ae})
        try:
            for label, a in zip(labels, months):
                theirs, mine = _point(s, label), _point(sec, label)
                assert mine.proj_len() == theirs.proj_len() == 720, (ae, a)
                want, got = theirs.accel_cost(), mine.accel_cost()
                assert type(got) is float and got.hex() == want.hex(), (ae, a, got, want)
                assert (want > 0.0) == (a == 720 or ae < 1.0), (ae, a, want)
                if ae == 1.0 and a > 720:
                    assert theirs.lives_if(a, 1) == 0.0, a
        finally:
            sec.close()
            s.close()


def _hex_faults(theirs, mine, months, cells):
    """Where ``mine``'s cells differ from ``theirs``' by ``float.hex``, sign of zero
    included: S's total under ``None``, SEC's under ``ALL``."""
    found = []
    for t in months:
        for cell, total in cells:
            want = theirs.cells[cell](t, None) if total else theirs.cells[cell](t)
            got = mine.cells[cell](t, mine.ALL) if total else mine.cells[cell](t)
            if type(got) is not float or got.hex() != want.hex():
                found.append(f"{cell}({t}): S {want.hex()}, SEC {got!r}")
    return found


# The A/E at which the kinds' claims are negative zeros: a negative rate kills no one, and
# the death benefit's claim is -0.0 times a count.
NEGATIVE_AE = -0.5


def test_the_all_total_is_s_total_with_its_sign_of_zero():
    """``claims(t, ALL)`` is ``DIA_US_S``'s ``claims(t)``, bit for bit, a negative zero
    included (R12).

    S's ``claims(t, kind=None)`` is ``claims(t, "DEATH") + claims(t, "REFUND")``, a
    ``+`` of the two kinds, and ``-0.0 + -0.0`` is ``-0.0``; here the code ``ALL`` is the
    same ``+``, where a total begun at ``0.0``, as a split's or a ``sum``'s is, would give
    ``0.0`` (§7.12, *C*).  T1 compares at its tolerance, which cannot see a sign.  So on
    the twin of S point 4, on a model of each read with ``mort_ae_factor`` at
    :data:`NEGATIVE_AE` before it computes anything, S's total is ``-0.0`` in most months,
    and in every month of the frame ``claims(t, ALL)`` and ``liability_outgo(t)`` are S's
    ``claims(t)`` and ``liability_outgo(t)`` by ``float.hex``.  The compiled model is held
    to the same by :func:`test_the_compiled_all_total_keeps_s_sign_of_zero`.
    """
    s = _read(model_path(TWIN), "s_negzero", {"mort_ae_factor": NEGATIVE_AE})
    sec = _read(model_path(SEC), "negzero", {"mort_ae_factor": NEGATIVE_AE})
    try:
        theirs, mine = _point(s, 4), _row(sec, "twin", 4, 0)
        months = range(theirs.proj_len())
        zeros = [t for t in months if math.copysign(1.0, theirs.claims(t)) < 0.0
                 and theirs.claims(t) == 0.0]
        assert len(zeros) > len(months) // 2, len(zeros)
        assert _hex_faults(theirs, mine, months, (("claims", True),
                                                   ("liability_outgo", False))) == []
    finally:
        sec.close()
        s.close()


def test_claims_ann_is_a_plain_sum_an_ulp_or_two_from_s(sec_model, s_model):
    """``claims_ann(y, kind)`` adds its months' claims left to right, as Phase 1 did, and
    is ``DIA_US_S``'s compensated ``sum`` to an ulp or two, at T1's tolerance.

    S's ``claims_ann`` is ``sum(claims(t, kind) for t ...)``, which CPython 3.12 and later
    compensates; this model's, since M12, a plain ``+=`` loop, kept so that no number
    moves from Phase 1 (ruled at M24).  So the two differ in the last bit or two of some
    years, which the module's comparisons hold at T1's 1e-9 relative.  This records the
    precision: on every twin, at the shipped A/E and at :data:`NEGATIVE_AE`, each kind and
    the total in each policy year are the plain left-to-right sum of the year's monthly
    claims, by ``float.hex``, and S's to 1e-15 relative and two ulps; some years differ
    from S.  How many depends on the platform's ``libm``, which rounds the monthly survival
    in the last bit as it will: at the shipped A/E the total differs in 154 of the twins'
    policy years on Windows and in 152 on Linux and macOS (Tests run 24), so the count is
    held to a band around both, and at :data:`NEGATIVE_AE` the twin of S point 4's total
    differs in some year (24 and 25 on Windows).  A loop made Neumaier's, or a sum of the
    wrong kind, fails here.
    """
    neg_s = _read(model_path(TWIN), "s_ann", {"mort_ae_factor": NEGATIVE_AE})
    neg = _read(model_path(SEC), "ann", {"mort_ae_factor": NEGATIVE_AE})
    try:
        found, apart = [], {}
        for ae, s, sec in ((1.0, s_model, sec_model), (NEGATIVE_AE, neg_s, neg)):
            for point in range(1, 18):
                theirs, mine = _point(s, point), _row(sec, "twin", point, 0)
                for y in range(1, theirs.proj_len() // 12 + 1):
                    for kind in ("DEATH", "REFUND", None):
                        code = mine.ALL if kind is None else _code(mine, kind)
                        got, want = mine.claims_ann(y, code), theirs.claims_ann(y, kind)
                        plain = 0.0
                        for t in range(12 * (y - 1), 12 * y):
                            plain += mine.claims(t, code)
                        if got.hex() != plain.hex():
                            found.append(f"{ae} point {point}: claims_ann({y}, {kind}) is "
                                         f"not the plain sum")
                        if (got != pytest.approx(want, rel=1e-15, abs=0)
                                or abs(got - want) > 2.0 * math.ulp(max(abs(got),
                                                                        abs(want)))):
                            found.append(f"{ae} point {point}: claims_ann({y}, {kind}) "
                                         f"{got!r}, S's {want!r}")
                        if got != want:
                            apart.setdefault((ae, point, kind), []).append(y)
        assert not found, found[:20]
        count = sum(len(years) for (ae, _, kind), years in apart.items()
                    if ae == 1.0 and kind is None)
        assert 140 <= count <= 170, count
        assert apart.get((NEGATIVE_AE, 4, None)), apart.get((NEGATIVE_AE, 4, None))
    finally:
        neg.close()
        neg_s.close()


def test_the_premium_array_holds_s_dict_to_the_last_bit(tmp_path):
    """``Data.premium_array`` is ``DIA_US_S``'s ``premium_by_mth()``, bit for bit.

    S sums a point's rows by month in the order its ``sort_values("premium_mth")`` gives,
    which for rows of one month need not be the file's, from ``0.0`` through ``dict.get``;
    ``Data`` takes each point's rows by ``groupby(sort=False)``, sorts them as S does, and
    adds them the same way (Data's docstring).  Floating addition is not associative, so
    the order is the number.  On a schedule whose cash refund pays 0.1, 0.2 and 0.7 at
    policy month 60 and 0.7, 0.2 and 0.1 at 0, written out of month order, and a 0.0 at
    month 12: every month's premium, read through ``premium_pm``, is S's dict's by
    ``float.hex``, 0.0 where S's has no key; the rows by month count the file's, the 0.0
    row's month among them; and each point's last month is its schedule's.  The two
    months' totals differ, so a sum in the file's order or summed twice fails here.
    """
    schedule = _premiums((3, 60, 0.1), (3, 0, 0.7), (3, 60, 0.2), (3, 12, 0.0), (3, 0, 0.2),
                         (3, 60, 0.7), (3, 0, 0.1))
    s, sec = _s_and_sec(tmp_path, [(3, {})], schedule)
    try:
        theirs, mine = _point(s, 3).premium_by_mth(), _point(sec, 3)
        assert sorted(theirs) == [0, 12, 60] and theirs[0] != theirs[60]
        data = sec.Data
        assert data.premium_width() == 61
        for k in range(data.premium_width() + 2):
            assert mine.premium_pm(k).hex() == theirs.get(k, 0.0).hex(), k
        rows = data.premium_rows()[0]
        assert [k for k in range(len(rows)) if rows[k]] == [0, 12, 60]
        assert (rows[0], rows[12], rows[60], data.premium_last()[0]) == (3, 1, 3, 60)
    finally:
        sec.close()
        s.close()


def test_the_pricing_guarantee_sums_the_premiums_as_s_sum_does(tmp_path):
    """``guarantee_mths_pricing()`` totals the premiums as CPython's ``sum`` does.

    ``DIA_US_S`` prices a refund form's guarantee from ``sum(premium_by_mth().values())``,
    which CPython 3.12 and later compensates (Neumaier), and this model writes that sum out
    over the premium table's months with a row, so that the compiled cell, which has no
    Python ``sum``, adds the same bits (R12).  Premiums of 1.0, 1e16 and 1.0 at three
    months of the cash refund, so that each branch of the compensation is taken, are summed
    to ``1.0000000000000002e16`` compensated and ``1e16`` left to right.  On them
    ``guarantee_mths_pricing()`` and the purchase rate of each premium are S's by
    ``float.hex``, and the left-to-right sum is not S's, so a plain loop fails here.
    """
    amounts = (1.0, 1e16, 1.0)
    plain = 0.0
    for amount in amounts:
        plain += amount
    assert plain != sum(amounts)
    schedule = _premiums(*((3, m, a) for m, a in zip((0, 12, 24), amounts)))
    s, sec = _s_and_sec(tmp_path, [(3, {})], schedule)
    try:
        theirs, mine = _point(s, 3), _point(sec, 3)
        assert mine.guarantee_mths_pricing().hex() == theirs.guarantee_mths_pricing().hex()
        for k in (0, 12, 24):
            assert mine.purchase_rate(k).hex() == theirs.purchase_rate(k).hex(), k
        assert mine.annual_income(0) > 0.0
    finally:
        sec.close()
        s.close()


# The ROP table's deferral key is int(round((T - k) / 12)) in DIA_US_S, a round half to
# even, here integer arithmetic on the months: every deferral in months from -3,000 to
# 3,000 is compared.
DEFERRALS = range(-3000, 3001)


def test_the_rop_deferral_rounds_half_to_even_as_s_round_does(sec_model, s_model):
    """``rop_deferral_yrs(k)`` is ``DIA_US_S``'s ``int(round(deferral_yrs(k)))``.

    S keys the ROP table by the deferral in whole years, ``round((T - k) / 12)``, Python's
    round half to even on a float; this model rounds in an int cell on the months, a
    quotient and its remainder, so that the compiled cell does no float arithmetic and no
    ``round`` (R16, as precised at M24).  The two agree where a half falls, an odd or an
    even quotient, and on either side of 0.  So the formula is read from the model and run
    on every deferral of :data:`DEFERRALS`, each against ``int(round(n / 12))``; and on the
    anchor's twin, every policy month of the ``k`` cache, and on the adjusting point's,
    whose income start month changes at its exercise, each ``rop_deferral_yrs(k)`` is S's
    key, an ``int``.  A rounding half up, or by ``int()`` alone, fails at a half or below
    0.
    """
    tree = ast.parse((model_path(SEC) / "Projection" / "__init__.py").read_text(
        encoding="utf-8"))
    found = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "rop_deferral_yrs"]
    assert len(found) == 1
    space = {"income_start_mth_at": lambda k: k + n}
    exec(compile(ast.Module(found, []), "Projection", "exec"), space)
    faults = []
    for n in DEFERRALS:
        if space["rop_deferral_yrs"](0) != int(round(n / 12)):
            faults.append(n)
    assert not faults, faults[:20]
    for point in (1, 13):
        mine, theirs = _row(sec_model, "twin", point, 0), _point(s_model, point)
        for k in range(1447):
            got = mine.rop_deferral_yrs(k)
            assert type(got) is int and got == int(round(theirs.deferral_yrs(k))), (point,
                                                                                     k)


# Rates and the places they are rounded to, as (annuity factor, ROP factor, places): exact
# binary halves at their last place, 1 / 16 to 3 places and 1 / 8 to 2, which go down to
# even, 5 / 2 to none, down, 3 / 16 to 3, up, and -1 / 16 and -1 / 8, below 0; then rates
# that are not halves, and one left unrounded.
RATE_TIES = ((16.0, 0.0, 3), (8.0, 0.0, 2), (0.4, 0.0, 0), (16.0 / 3.0, 0.0, 3),
             (16.0, 2.0, 3), (8.0, 2.0, 2))
RATE_OTHERS = ((3.0, 0.0, 6), (7.0, 0.25, 8), (11.0, 0.0, -1))


def test_the_purchase_rate_rounds_half_to_even_as_s_round_does():
    """``purchase_rate(k)`` rounds as ``DIA_US_S``'s ``round(pr, dp)`` rounds, ties to even.

    The rounding stays a call of Python's ``round`` in the compiled cell, admitted through
    the registry's ``"python_calls"`` (R16, as at M24), since the rate is built from
    ``Projection``'s References.  A rounding written in arithmetic instead, half up as
    ``int(pr * 10 ** dp + 0.5) / 10 ** dp`` is, agrees with ``round`` everywhere but at an
    exact binary half, which no committed point's rate falls on.  So the formula is read
    from the model and run, with no expense load, on the halves of :data:`RATE_TIES`, each
    asserted a half, and the rates of :data:`RATE_OTHERS`, each against ``round(pr, dp)``
    by ``float.hex``, a ``dp`` below 0 leaving the rate unrounded: ``0.0625`` to 3 places
    is ``0.062``, not ``0.063``.
    """
    tree = ast.parse((model_path(SEC) / "Projection" / "__init__.py").read_text(
        encoding="utf-8"))
    found = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "purchase_rate"]
    assert len(found) == 1
    faults = []
    for a, rop, dp in RATE_TIES + RATE_OTHERS:
        pr = (1.0 - rop) / a
        if (a, rop, dp) in RATE_TIES:
            assert abs(math.modf(pr * 10.0 ** dp)[0]) == 0.5, (a, rop, dp)
        space = {"annuity_factor_def": lambda k, a=a: a, "expense_load": 0.0,
                 "rop_factor": lambda k, rop=rop: rop, "purchase_rate_dp": lambda dp=dp: dp}
        exec(compile(ast.Module(found, []), "Projection", "exec"), space)
        want = pr if dp < 0 else round(pr, dp)
        got = space["purchase_rate"](0)
        if type(got) is not float or got.hex() != want.hex():
            faults.append((a, rop, dp, got, want))
    assert round(1.0 / 16.0, 3) == 0.062 and round(2.5) == 2
    assert not faults, faults


def test_a_zero_premium_is_priced_as_s_prices_it(tmp_path):
    """A premium of 0.0 on the schedule is visited by the pricing guarantee, and its ROP
    key read.

    ``DIA_US_S``'s pricing guarantee loops over ``premium_by_mth()``'s keys, a month with
    a premium of 0.0 among them, and reads each key's ROP factor, which the table basis
    joins; this model visits each month with a row, ``Data.premium_rows``, not each month
    with a positive premium.  So the anchor's twin on the table basis with a 0.0 added at
    policy month 12, whose ROP key, issue age 61 and 19 years' deferral, the table lacks:
    its cash flows project in both models, which price its premiums on the table's payout
    factor, but ``guarantee_mths_pricing()``, which ``guarantee_yrs`` shows, is refused
    naming the point and the key, as S raises at that key.  With the key added to the
    table, the twin is S's point, cell by cell.  A loop over positive premiums alone
    answers where S raises.
    """
    schedule = _premiums((1, 0, 100000.0), (1, 12, 0.0), (1, 60, 50000.0))
    s, sec = _s_and_sec(tmp_path / "lacks", [(1, {})], schedule)
    try:
        assert frame_mismatches(_point(s, 1).result_cf(), _point(sec, 1).result_cf(),
                                atol=0.0) == []
        _refused(_point(sec, 1).guarantee_mths_pricing,
                 "point_id 1: rop_factor_table.csv has no rop_factor at issue_age 61, "
                 "deferral_years 19 for the point's sex")
        with pytest.raises(Exception) as excinfo:
            _point(s, 1).guarantee_mths_pricing()
        assert "KeyError" in str(excinfo.value), str(excinfo.value)
    finally:
        sec.close()
        s.close()
    key = {"rop_factor_table.csv": lambda df: pd.concat([df, pd.DataFrame([{
        "issue_age": 61, "sex": "F", "deferral_years": 19, "rop_factor": 0.16,
        "provenance": "[std] a test case"}])], ignore_index=True)}
    s, sec = _s_and_sec(tmp_path / "holds", [(1, {})], schedule, key)
    try:
        theirs, mine = _point(s, 1), _point(sec, 1)
        _sweep(theirs)
        _sweep(mine)
        assert mine.rop_factor(12) == 0.16
        assert _mismatches(theirs, mine, exempt=TWIN_EXEMPT_DEFAULT | SPEC.exempt,
                           atol=0.0) == []
    finally:
        sec.close()
        s.close()


# The decodes' text, each of the values DIA_US_S names written in another case and with a
# space beside it, as (column, the call that reads it, {point_id: value}): the S points a
# variant goes on, each a point whose projection reads the column, the reduction trigger on
# the joint points and the market type through the QLAC overlay alone.  Each set is one
# copy of each model's table.
_TEXT = {"reduction_trigger": ("either", "primary"),
         "market_type": ("NQ", "TradIRA", "RothIRA", "QLAC"),
         "income_form": ("LO", "LO_ROP", "CR", "IR", "PC"), "db_form": ("ROP", "NONE"),
         "timing": ("arrears", "advance"), "mort_basis": ("anchor", "generational"),
         "factor_basis": ("table", "formula")}
_ON = {"reduction_trigger": (8, 9), "market_type": tuple(range(1, 11))}


def _decode_sets():
    """:data:`DECODES`: each column's case and space variants, spread over its points."""
    sets = []
    for column, values in _TEXT.items():
        variants = []
        for i, value in enumerate(values):
            variants += [value.swapcase(), f" {value}" if i % 2 else f"{value} "]
        points = _ON.get(column, tuple(range(1, 18)))
        for start in range(0, len(variants), len(points)):
            chunk = variants[start:start + len(points)]
            sets.append((column, "qlac_flags" if column == "market_type" else "result_cf",
                         dict(zip(points, chunk))))
    return sets


DECODES = _decode_sets()


def _decoded(column):
    """The name a decode's refusal gives: the column's, ``timing`` as it is."""
    return f"invalid {column}"


def test_each_decode_is_s_exact_comparison(tmp_path):
    """Each text column is decoded by ``DIA_US_S``'s exact comparison: another case or a
    space is refused, in both models, with S's message.

    ``DIA_US_S``'s accessors compare the text as it stands, ``v not in (...)``, and so does
    each ``has_*`` flag of ``Data`` that ``Projection``'s decodes read, element by element
    (USLIB-SEC-PLAN.md §7.3, *For M17 and later*).  A decode that folded the case or
    stripped the text would project a point S refuses.  So each value S names, in every
    text column a projection branches on, is written in its other case and beside a space
    (:data:`DECODES`), each on a point of its own whose projection reads the column, and
    each point's call, ``result_cf`` or, for the market type, ``qlac_flags``, raises S's
    ``ValueError("invalid ...")`` in this model and in ``DIA_US_S`` on the same table.
    """
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    found = []
    for number, (column, call, values) in enumerate(DECODES):
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
                want = ("raised", f"ValueError: {_decoded(column)}")
                for model, name in ((sec, "SEC"), (s, "S")):
                    got = _did(_point(model, point).cells[call])
                    if got != want:
                        found.append(f"{name} {column} {value!r} on {point}: {got}")
        finally:
            s.close()
            sec.close()
    assert not found, "\n".join(found)


def _reversed_rows(df):
    """An edit of a table that writes its rows in reverse, every key out of order."""
    return df.iloc[::-1].reset_index(drop=True)


def _one_sex(sex):
    """An edit of a table that keeps the rows of ``sex`` alone, written in reverse."""
    return lambda df: _reversed_rows(df[df["sex"] == sex])


# The four assumption tables written in reverse, the scale and the two factor tables for
# the male life alone: the mortality table numbers F 1 and M 2, and the other three M 1.
NUMBERED_EDITS = {"mort_table.csv": _reversed_rows, "improvement_scale.csv": _one_sex("M"),
                  "payout_factor_table.csv": _one_sex("M"),
                  "rop_factor_table.csv": _one_sex("M")}

# The tables crossed, so that the numberings NUMBERED_EDITS gives alike differ: the payout
# table for the female life alone, F 1, the ROP table for the male alone, M 1, and the
# mortality table and the scale as shipped, F 1 and M 2.
CROSSED_EDITS = {"payout_factor_table.csv": _one_sex("F"),
                 "rop_factor_table.csv": _one_sex("M")}

# Each table's schedule: Projection's cell of each life's sex, or Data's vector of the
# point's sex, which the factor tables are scanned for.
SCHEDULES_BY_TABLE = {"mort_table.csv": "mort_schedule",
                      "improvement_scale.csv": "improvement_schedule",
                      "payout_factor_table.csv": "payout_schedule",
                      "rop_factor_table.csv": "rop_schedule"}

# The points on the table basis whose reports read the payout factor at a key the table
# written for the male life alone lacks: the female ones whose income start month is not
# behind them.
NO_PAYOUT = [1, 2, 4]


def _numbering(model, file):
    """Each sex's number in ``file`` as ``model`` reads it: its sorted order from 1."""
    read = {"mort_table.csv": model.Data.mort_table,
            "improvement_scale.csv": model.Data.improvement_scale,
            "payout_factor_table.csv": model.Data.payout_factor_table,
            "rop_factor_table.csv": model.Data.rop_factor_table}[file]
    keys = sorted(read().reset_index()["sex"].unique())
    return {sex: number for number, sex in enumerate(keys, 1)}


def _schedule_faults(model, table):
    """Where a schedule is not its sex's number in its own table, 0 for a sex it lacks."""
    found = []
    for file, cell in SCHEDULES_BY_TABLE.items():
        number = _numbering(model, file)
        if cell in ("payout_schedule", "rop_schedule"):
            have = model.Data.cells[cell]().tolist()
            want = [number.get(sex, 0) for sex in table["sex"]]
            if have != want:
                found.append(f"{file}: {cell} {have}, not {want}")
            continue
        for label in table.index:
            p = _point(model, label)
            for life in _lives(p):
                if p.cells[cell](life) != number.get(p.sex(life), 0):
                    found.append(f"{file}: point {label}: {cell}({life}) "
                                 f"{p.cells[cell](life)}")
    return found


def test_the_tables_number_each_sex_by_their_own_and_join_by_key(tmp_path):
    """Each table numbers its sexes by its own, and every join reads its key's row.

    ``Data`` tables the mortality table and the improvement scale by schedule and age, a
    schedule per sex in each table's own sorted order, and holds the payout and ROP
    factor tables as row vectors in file order, the sex numbered by each table, scanned
    for a point's key (the Data docstring).  A sex is M or F, so four tables cannot
    number their sexes four ways at once, and two readings make every pair differ.  On the
    four tables written in reverse, the scale and both factor tables holding the male
    life alone (:data:`NUMBERED_EDITS`), the male is 2 in the mortality table and 1 in the
    other three, the female 1 and 0.  On the tables crossed (:data:`CROSSED_EDITS`), the
    payout table holds the female alone and the ROP table the male, so the female is 1
    and 0 there and the male 0 and 1, each 1 and 2 in the other two.  The committed table
    and two male twins, the anchor on the table basis and the generational cash refund,
    are read on both, and in each, each life's ``mort_schedule`` and
    ``improvement_schedule``, and each point's ``payout_schedule`` and ``rop_schedule``,
    is its sex's number in that table, 0 for a sex the table lacks.  Then, on the tables
    written in reverse against the tables as shipped, every point projects exactly what it
    projects as shipped, the male anchor on the table basis reading its payout and ROP
    factors from the last rows, but two: the female generational twin, whose sex the
    scale lacks, refused at the first age it reads there, and the female points on the
    table basis whose reports read the payout factor (:data:`NO_PAYOUT`), refused there,
    each naming the point.  A schedule read from another table's numbering, a factor
    scanned without the sex or the form, or a table read in file order, reads another row.
    """
    table = _committed()
    male = pd.concat([table.loc[[1]].assign(sex="M"), table.loc[[16]].assign(sex="M")])
    male.index = pd.Index([27, 28], name="point_id")
    table = pd.concat([table, male])
    premiums = _committed_schedule()
    schedule = pd.concat([premiums, premiums[premiums["point_id"] == 1].assign(point_id=27),
                          premiums[premiums["point_id"] == 16].assign(point_id=28)],
                         ignore_index=True)
    crossed = _read(_sec_inputs(tmp_path / "crossed", table, CROSSED_EDITS, schedule),
                    "crossed")
    try:
        assert [_numbering(crossed, file) for file in SCHEDULES_BY_TABLE] == [
            {"F": 1, "M": 2}, {"F": 1, "M": 2}, {"F": 1}, {"M": 1}]
        found = _schedule_faults(crossed, table)
    finally:
        crossed.close()
    assert not found, "\n".join(found[:20])
    shipped = _read(_sec_inputs(tmp_path / "shipped", table, schedule=schedule), "shipped")
    model = _read(_sec_inputs(tmp_path / "numbered", table, NUMBERED_EDITS, schedule),
                  "numbered")
    try:
        assert (model.Data.mort_sexes(), model.Data.improvement_sexes()) == (2, 1)
        assert [_numbering(model, file) for file in SCHEDULES_BY_TABLE] == [
            {"F": 1, "M": 2}, {"M": 1}, {"M": 1}, {"M": 1}]
        found = _schedule_faults(model, table)
        no_payout = []
        for label in table.index:
            p = _point(model, label)
            if label == 16:
                _refused(p.result_cf, "point_id 16: improvement_scale.csv has no "
                                      "improvement_rate at attained age 60 for the sex of "
                                      "life 1")
                continue
            try:
                p.result_cf()
            except Exception:                   # held to its message below
                no_payout.append(label)
                continue
            for report in REPORTS:
                if frame_mismatches(_point(shipped, label).cells[report](),
                                    p.cells[report](), rtol=0, atol=0):
                    found.append(f"point {label}: {report} moved")
            _release(model, _key(model, label))
            _release(shipped, _key(shipped, label))
        assert not found, "\n".join(found[:20])
        assert no_payout == NO_PAYOUT, no_payout
        for label in no_payout:
            _refused(_point(model, label).result_cf,
                     f"point_id {label}: payout_factor_table.csv has no payout_factor at "
                     f"income_start_age 80 for the point's sex and payout form")
    finally:
        model.close()
        shipped.close()


def test_every_padded_array_holds_nan_and_no_reader_reads_it(sec_model, tmp_path):
    """The padding is NaN, and the readers refuse an age before reading it, by name.

    ``Data`` tables the two age tables from age 0 and from schedule 0, and pads what no
    file holds with NaN, as its docstring says, so that a read past a check, were one
    lost, would make every number after it NaN rather than another key's value: row 0 of
    each table, a schedule for a sex the table lacks, whose extents are (1, 0), so that no
    age lies between them, and each row's ages below its first, 20 as shipped.  Inside,
    nothing is NaN.

    And on the extract labelled otherwise than by position (:func:`_relabelled`), where a
    label read as ``idx + 1`` would name another point, each age reader refuses an age
    below its table's first, naming the point, the age and the life, and on a mortality
    table without the female rows a female point, schedule 0 there, is refused at the
    first age it reads.
    """
    data = sec_model.Data
    for sexes, array, first, last in (
            (data.mort_sexes(), data.mort_table_array(), data.mort_age_first(),
             data.mort_age_last()),
            (data.improvement_sexes(), data.improvement_array(),
             data.improvement_age_first(), data.improvement_age_last())):
        assert array.shape[0] == len(first) == len(last) == sexes + 1 == 3
        assert np.isnan(array[0]).all() and (first[0], last[0]) == (1, 0)
        for s in range(1, sexes + 1):
            assert first[s] == 20 and last[s] == array.shape[1] - 1 == 120, s
            assert not np.isnan(array[s, first[s]:last[s] + 1]).any(), s
            assert np.isnan(array[s, :first[s]]).all(), s
    extract = _relabelled(_committed())
    schedule = _relabelled_schedule(_committed_schedule())
    no_female = {"mort_table.csv": lambda df: df[df["sex"] == "M"]}
    for tag, edits in (("padded", None), ("no_female", no_female)):
        model = _read(_sec_inputs(tmp_path / tag, extract, edits, schedule), tag)
        try:
            p = _point(model, 108)
            assert p.point_id() == 108 != point_keys(model)[0] + 1
            if edits is None:
                _refused(lambda: p.mort_rate_base_at(19, 1),
                         "point_id 108: mort_table.csv has no mort_rate at attained age 19 "
                         "for the sex of life 1")
                _refused(lambda: p.improvement_rate_at(0, 2),
                         "point_id 108: improvement_scale.csv has no improvement_rate at "
                         "attained age 0 for the sex of life 2")
                continue
            assert (p.mort_schedule(1), p.mort_schedule(2)) == (0, 1)
            _refused(p.result_cf, "point_id 108: mort_table.csv has no mort_rate at "
                                  "attained age 60 for the sex of life 1")
        finally:
            model.close()


# Data's readers, each a DataFrame or a path, which only the label accessors, the cells
# kept for a reader and Data's own cells read; and the count cells, each a table's check,
# an int.  Every other Data cell is a vector or an int in the docstring's table.
READERS = ("input_dir", "model_point_table", "premium_schedule_table", "mort_table",
           "improvement_scale", "payout_factor_table", "rop_factor_table")
COUNTS = ("mort_table_count", "improvement_scale_count", "payout_factor_count",
          "rop_factor_count")


def _vector_kinds():
    """The Data docstring's table of its vectors, as {cell: "int64", "float64" or "int"}.

    The table's first two columns, by the widths its rules give: every cell a row names,
    one to a row, and the dtype beside it.
    """
    source = (model_path(SEC) / "Data" / "__init__.py").read_text(encoding="utf-8")
    lines = ast.get_docstring(ast.parse(source)).splitlines()
    head = next(i for i, line in enumerate(lines) if line.split()[:2] == ["Cells", "dtype"])
    widths = [len(rule) for rule in lines[head - 1].split()]
    first, dtype = widths[0], slice(widths[0] + 2, widths[0] + 2 + widths[1])
    kinds = {}
    for line in lines[head + 2:]:
        if line.startswith("="):
            break
        for name in re.findall(r"(\w+)\(\)", line[:first]):
            assert name not in kinds, name
            kinds[name] = line[dtype].strip()
    return kinds


def test_each_data_vector_is_the_int64_or_float64_its_docstring_states(sec_model):
    """Every ``Data`` cell but the readers and the counts is the int64 or float64 array,
    or the int, that the Data docstring's table of its vectors states; and each count is
    an int.

    That is what compiles to a typed memoryview or a C ``long long`` (the Data
    docstring): an array of bools, objects or text compiles as a Python object, and so does
    a check returned as a numpy int.  The typing guard, C3, finds that in the compiled
    model's declarations; this finds it in seconds, in every run, naming the cell.  And
    each vector is of R5's kind, int64 for ages, months, years, codes, flags and schedules,
    float64 for amounts and rates, as the table states it: a month held as a float64 reads
    the same numbers, and compiled reads a double through ``int()``, Python arithmetic,
    which neither C3 nor C5 sees.  Every cell is in the table, and every cell the table
    names is a cell.
    """
    data = sec_model.Data
    kinds = _vector_kinds()
    vectors = {name for name, cells in data.cells.items()
               if not cells.parameters and name not in READERS + COUNTS}
    assert set(kinds) == vectors, set(kinds) ^ vectors
    assert set(kinds.values()) == {"int64", "float64", "int"}, set(kinds.values())
    found = [f"{name}: {type(data.cells[name]()).__name__}, not an int" for name in COUNTS
             if type(data.cells[name]()) is not int]
    for name, kind in kinds.items():
        value = data.cells[name]()
        if kind == "int":
            if type(value) is not int:
                found.append(f"{name}: {type(value).__name__}, not an int")
        elif not (isinstance(value, np.ndarray) and value.dtype == np.dtype(kind)):
            found.append(f"{name}: {getattr(value, 'dtype', type(value).__name__)}, not "
                         f"{kind}")
    assert not found, found
    assert set(READERS) < set(data.cells)


def test_every_parameterless_cell_returns_a_python_number(sec_model):
    """Every parameterless cell but the reporting ones returns a Python int, float or bool.

    R11: a ``Projection`` cell that reads a ``Data`` vector converts the element, ``int()``,
    ``float()`` or ``bool()``, so that modelx returns a Python number, as the compiled cell
    does, and not a numpy scalar, whose arithmetic and printing differ, and which C4
    compares as a kind of its own.  A conversion left out moves no number and still
    compiles, so it is asserted here: on every committed point, each parameterless cell
    outside :func:`sec_support.reporting_cells` returns exactly an ``int``, a ``float`` or
    a ``bool``.
    """
    from sec_support import reporting_cells
    space = sec_model.Projection
    reporting = reporting_cells(SEC, space)
    names = sorted(name for name, cell in space.cells.items()
                   if not cell.parameters and name not in reporting)
    assert {"point_id", "is_joint", "is_rop", "payment_freq", "commute_frac"} <= set(names)
    found = []
    for key in point_keys(sec_model):
        proj = projection(sec_model, key)
        found += [f"{key}: {name} {type(value).__name__}" for name in names
                  if type(value := proj.cells[name]()) not in (int, float, bool)]
    assert not found, found


def _references(space):
    """The References a space's ``__init__.py`` assigns, a name to a literal value."""
    source = (model_path(SEC) / space / "__init__.py").read_text(encoding="utf-8")
    return {node.targets[0].id: node.value.value for node in ast.parse(source).body
            if isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Constant)}


def _comment(file):
    """The comment lines of ``file`` beside the model, joined into one line."""
    source = (model_path(SEC).parent / file).read_text(encoding="utf-8")
    return source, " ".join(line.lstrip("# ") for line in source.splitlines()
                            if line.startswith("#"))


# The codes, in their numbering's order: the timings, the kinds with the total, the
# phases and the annuity factor's bases.  A phase is a cell's value, never a cache index.
TIMING_CODES = ("BEF_NB", "BEF_DECR")
KIND_CODES = ("DEATH", "REFUND", "ALL")
PHASE_CODES = ("PRE_ISSUE", "DEFERRAL", "PAYOUT", "TERMINATED")
BASIS_CODES = ("PURCHASE", "ADJUST_OLD", "ADJUST_NEW")

# The lives, 1 and 2, index every per-life cache from 0, which the cells refuse.
LIVES = 2


def test_the_spec_sizes_each_cache_as_its_comment_derives():
    """``spec_sec.py`` gives each cache the size its comment derives from the contract.

    The spec check, C3, holds the compiled caches to the spec, and C4 at the contract's
    extremes holds the spec to the largest argument a projection reads; neither sees a
    size one below the comment's, which drops the headroom and reads the same numbers.  So
    this reads the spec as mx2cy does, and the bounds of the contract from the model's own
    References, and holds each size to the comment's derivation from them: ``t`` to
    ``12 * (omega_age - issue_age_min) + future_horizon_mth + 3``, ``k`` to
    ``12 * (omega_age - issue_age_min) + accel_months + 1``, ``y`` to ``omega_age -
    issue_age_min + 3``, ``x`` to ``omega_age + 1``, and ``life`` to 3; every 2-D cache to
    one inner width, the widest of the timings', the kinds', the bases' and the lives',
    since gcc refuses two widths and MSVC, which builds the Windows leg, accepts them
    (USLIB-SEC-PLAN.md §7.2, *For M16 and later*); and the codes dense from 0, ints, as
    the caches index them.  And ``Data.premium_last_mth``, the premium table's last
    month, to ``12 * (omega_age - issue_age_min) - 1``, the month before the latest income
    start month the caches hold.  A change to a bound or a size is derived again in the
    comment and here.
    """
    source, comment = _comment("spec_sec.py")
    for formula in ("12 * (omega_age - issue_age_min) + future_horizon_mth + 3",
                    "12 * (omega_age - issue_age_min) + accel_months + 1",
                    "omega_age - issue_age_min + 3", "omega_age + 1",
                    "12 * (omega_age - issue_age_min) - 1"):
        assert formula in comment, formula
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    proj, data = _references("Projection"), _references("Data")
    low, omega, accel, horizon = (proj["issue_age_min"], proj["omega_age"],
                                  proj["accel_months"], data["future_horizon_mth"])
    assert low == 0, proj
    for names in (TIMING_CODES, KIND_CODES, PHASE_CODES, BASIS_CODES):
        values = [proj[name] for name in names]
        assert values == list(range(len(names))), (names, values)
        assert all(type(v) is int for v in values), (names, values)
    t, k = 12 * (omega - low) + horizon + 3, 12 * (omega - low) + accel + 1
    y = omega - low + 3
    width = max(len(TIMING_CODES), len(KIND_CODES), len(BASIS_CODES), LIVES + 1)
    assert sizes == {"t": t, ("t", "life"): (t, width), ("t", "timing"): (t, width),
                     ("t", "kind"): (t, width), "k": k, ("k", "life"): (k, width),
                     ("k", "basis"): (k, width), "y": y, ("y", "life"): (y, width),
                     ("y", "kind"): (y, width), ("x", "life"): (omega + 1, width),
                     "life": LIVES + 1}, sizes
    assert len({size[1] for size in sizes.values() if isinstance(size, tuple)}) == 1
    assert data["premium_last_mth"] == 12 * (omega - low) - 1, data["premium_last_mth"]


def test_the_sample_raises_the_recursion_limit_its_comment_derives():
    """``sample_sec.py`` sets the recursion limit its comment derives, before the import.

    The export does not raise the recursion limit as modelx does (F7), so the sample sets
    it, and its comment records the measured need: a cold ``net_cf`` in the last month of
    the longest cover, a cash refund issued at 0 commencing 1,440 months of cover 120
    months on, needs a limit of 2,924 in the export, and the reports and checks the sample
    runs in ascending ``t``, 48 from a script's top level, 64 where the installment
    refund's twin is read first (measured at M24).  The limit is four times the first,
    rounded up to the thousand.  No build can tell a lower limit above the reports' need:
    a limit of 1,000 builds the same model.  So this holds the
    limit, read from the sample's code, to the value derived from its comment's need, and
    holds the call before the import of the export.  A change to the need is measured
    again and written in the comment.
    """
    source, comment = _comment("sample_sec.py")
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


def test_the_sample_traces_sex_on_a_copy_whose_joint_sex_is_blank():
    """``sample_sec.py`` calls ``sex(1)`` and ``sex(2)`` on a second instance of the export,
    whose table's one point is a single life with a blank ``joint_sex``, after the
    committed points.

    ``sex(life)`` returns its column as read, so mx2cy must see it return something other
    than text, or it compiles to ``str`` and raises ``TypeError`` on a blank or a number
    (the sample's docstring).  The committed table's single-life points give a blank
    ``sex(2)`` today, so dropping the trace changes no declaration and no compile test
    fails; a table regenerated with no single life would.  A second build in every
    session to show it would cost a compile, so this holds the trace in the sample's code:
    a frame whose ``joint`` is set to ``False`` and ``joint_sex`` to ``None``; then a
    second ``_c_DIA_US_SEC()`` instance, its ``Data.model_point_file`` set, a
    ``Projection`` of it, and ``sex(1)`` and ``sex(2)`` called on that, in that order.
    """
    source, _ = _comment("sample_sec.py")
    lines = [(node.lineno, ast.unparse(node)) for node in ast.walk(ast.parse(source))
             if isinstance(node, (ast.Assign, ast.Expr))]

    def first(pattern, after=0):
        found = [(line, re.fullmatch(pattern, text)) for line, text in lines
                 if line > after and re.fullmatch(pattern, text)]
        assert found, pattern
        return min(found, key=lambda f: f[0])

    blank, _ = first(r"(\w+) = \1\.assign\(joint=False, joint_sex=None\)")
    made, match = first(rf"(\w+) = _c_{SEC}\(\)", blank)
    second = match.group(1)
    read, _ = first(rf"{second}\.Data\.model_point_file = .+", made)
    proj, match = first(rf"(\w+) = {second}\.Projection\[\d+\]", read)
    p = match.group(1)
    first(rf"\({p}\.sex\(1\), {p}\.sex\(2\)\)", proj)


def test_the_runner_sums_the_block_as_groupby_does(sec_model):
    """``run_sec.py``'s running sum of the block is pandas' ``groupby`` sum, bit for bit.

    A block run keeps one point's frame at a time, so it sums the frames as it goes,
    compensated, with ``add``, so that the block is the frames concatenated and summed by
    ``t``, to the last bit (USLIB-SEC-PLAN.md §7.9, *Record -- M23*, carried).  The
    printed block, to two decimals, cannot show a last bit, so ``add`` itself is read
    from the runner, which runs the model when imported, and run here on the committed
    points' frames.  A plain running sum differs from ``groupby``'s on them, so the
    comparison can fail.
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


# run_sec.py run as though it sat at /m/products/deferred_income_annuity, a copy too
# shallow to have a repository above it: the source compiled under that name, so that its
# own __file__ is it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/deferred_income_annuity/run_sec.py"
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
    for args in ((copy, "19", "--cython"), (shallow, runner)):
        done = _run_sec(*args, check=False)
        stderr = done.stderr.decode(errors="replace")
        assert done.returncode != 0 and done.stdout == b"", stderr
        assert "a lifelib.create() copy carries no tools/, so it cannot build" in stderr, (
            stderr)


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
    exactly.  ``python tools/gen_sec_fingerprint.py DIA_US_SEC --check`` runs the same
    comparison from the command line.
    """
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# DIA_US_SEC's fingerprint, frozen at M13 from the model as Phase 1 left it and committed
# alone, before Phase 2 changed anything.  Each point is keyed by its point_id; each column
# holds (its sum over the frame, its largest absolute value, (its values at the months)).
# The block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a
# refreeze goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: DIA_US_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "premiums": (148750.0000001148, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (373878.48512026895, 2626.2396128617056, (
                0.0, 0.0, 1487.707130757074, 119.20287150460497, 0.00018645098247136176)),
            "claims": (50249.99070704699, 443.2063825704713, (
                42.18744523027951, 195.73215112717034, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1985.4638793471313, 5.056974431379476, (
                4.166666666666667, 4.941315936186, 3.4612934079026743, 0.4091458561465175,
                1.0967334403685464e-06)),
            "liability_cf": (277363.93970654823, 99953.64588810306, (
                -99953.64588810306, 200.67346706335633, 1491.1684241649768,
                119.6120173607515, 0.0001875477159117303)),
            "net_cf": (-277363.93970654823, 99953.64588810306, (
                99953.64588810306, -200.67346706335633, -1491.1684241649768,
                -119.6120173607515, -0.0001875477159117303)),
        },
        "result_pols": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_death_last": (0.9999999494480459, 0.0029547092171364753, (
                0.0004218744523027951, 0.001304881007514469, 0.0025779555117311226,
                0.0008122101121449884, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
            "payment_factor": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
        },
    },
    2: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "premiums": (148750.0000001148, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (373878.1847120341, 2626.237502700149, (
                0.0, 0.0, 1487.7059353968411, 119.20277572609501, 0.00018645083265955728)),
            "claims": (50249.99713274943, 443.2063825704713, (
                42.18744523027951, 195.73215112717034, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1985.4638793471313, 5.056974431379476, (
                4.166666666666667, 4.941315936186, 3.4612934079026743, 0.4091458561465175,
                1.0967334403685464e-06)),
            "liability_cf": (277363.64572401595, 99953.64588810306, (
                -99953.64588810306, 200.67346706335633, 1491.167228804744,
                119.61192158224154, 0.00018754756609992582)),
            "net_cf": (-277363.64572401595, 99953.64588810306, (
                99953.64588810306, -200.67346706335633, -1491.167228804744,
                -119.61192158224154, -0.00018754756609992582)),
        },
        "result_pols": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_death_last": (0.9999999494480459, 0.0029547092171364753, (
                0.0004218744523027951, 0.001304881007514469, 0.0025779555117311226,
                0.0008122101121449884, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
            "payment_factor": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
        },
    },
    3: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "premiums": (148750.0000001148, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (372584.9811186173, 2617.1536355088233, (
                0.0, 0.0, 1482.560123899215, 118.79046641194505, 0.0001858059196995336)),
            "claims": (50277.65862970876, 443.2063825704713, (
                42.18744523027951, 195.73215112717034, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1985.4638793471313, 5.056974431379476, (
                4.166666666666667, 4.941315936186, 3.4612934079026743, 0.4091458561465175,
                1.0967334403685464e-06)),
            "liability_cf": (276098.1036275584, 99953.64588810306, (
                -99953.64588810306, 200.67346706335633, 1486.0214173071176,
                119.19961226809157, 0.00018690265313990216)),
            "net_cf": (-276098.1036275584, 99953.64588810306, (
                99953.64588810306, -200.67346706335633, -1486.0214173071176,
                -119.19961226809157, -0.00018690265313990216)),
        },
        "result_pols": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_death_last": (0.9999999494480459, 0.0029547092171364753, (
                0.0004218744523027951, 0.001304881007514469, 0.0025779555117311226,
                0.0008122101121449884, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
            "payment_factor": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
        },
    },
    4: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "premiums": (148750.0000001148, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (452962.09716526803, 3181.747680179228, (
                0.0, 0.0, 1802.3902651116077, 144.4169290658139, 0.0002258895106295971)),
            "claims": (7329.178998245647, 443.2063825704713, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1985.4638793471313, 5.056974431379476, (
                4.166666666666667, 4.941315936186, 3.4612934079026743, 0.4091458561465175,
                1.0967334403685464e-06)),
            "liability_cf": (313526.74004274595, 99995.83333333333, (
                -99995.83333333333, 4.941315936186, 1805.8515585195105, 144.8260749219604,
                0.00022698624406996564)),
            "net_cf": (-313526.74004274595, 99995.83333333333, (
                99995.83333333333, -4.941315936186, -1805.8515585195105, -144.8260749219604,
                -0.00022698624406996564)),
        },
        "result_pols": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_death_last": (0.9999999494480459, 0.0029547092171364753, (
                0.0004218744523027951, 0.001304881007514469, 0.0025779555117311226,
                0.0008122101121449884, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
            "payment_factor": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
        },
    },
    5: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "premiums": (148750.0000001148, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (381440.49137967173, 2628.0137985764886, (
                0.0, 0.0, 1482.560123899215, 118.79046641194505, 0.0001858059196995336)),
            "claims": (41499.99999963117, 332.1114840122652, (
                42.18744523027951, 195.73215112717034, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1985.4638793471313, 5.056974431379476, (
                4.166666666666667, 4.941315936186, 3.4612934079026743, 0.4091458561465175,
                1.0967334403685464e-06)),
            "liability_cf": (276175.9552585352, 99953.64588810306, (
                -99953.64588810306, 200.67346706335633, 1486.0214173071176,
                119.19961226809157, 0.00018690265313990216)),
            "net_cf": (-276175.9552585352, 99953.64588810306, (
                99953.64588810306, -200.67346706335633, -1486.0214173071176,
                -119.19961226809157, -0.00018690265313990216)),
        },
        "result_pols": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_death_last": (0.9999999494480459, 0.0029547092171364753, (
                0.0004218744523027951, 0.001304881007514469, 0.0025779555117311226,
                0.0008122101121449884, 1.0768345799005572e-08)),
            "certain_floor": (41.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
            "payment_factor": (103.77797539930125, 0.7150000000032242, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
        },
    },
    6: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "premiums": (148750.0000001148, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (466053.7795158201, 3273.7077585372067, (
                0.0, 0.0, 1854.4836322393194, 148.59092193012637, 0.00023241825495057137)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1985.4638793471313, 5.056974431379476, (
                4.166666666666667, 4.941315936186, 3.4612934079026743, 0.4091458561465175,
                1.0967334403685464e-06)),
            "liability_cf": (319289.24339505244, 99995.83333333333, (
                -99995.83333333333, 4.941315936186, 1857.9449256472221, 149.0000677862729,
                0.0002335149883909399)),
            "net_cf": (-319289.24339505244, 99995.83333333333, (
                99995.83333333333, -4.941315936186, -1857.9449256472221, -149.0000677862729,
                -0.0002335149883909399)),
        },
        "result_pols": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_death_last": (0.9999999494480459, 0.0029547092171364753, (
                0.0004218744523027951, 0.001304881007514469, 0.0025779555117311226,
                0.0008122101121449884, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
            "payment_factor": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
        },
    },
    7: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "premiums": (148750.0000001148, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (380630.3003502908, 2259.6948267319, (
                0.0, 0.0, 2259.6948267319, 102.14185426330023, 0.00015976501940310445)),
            "claims": (41499.99999963117, 332.1114840122652, (
                42.18744523027951, 195.73215112717034, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1985.4638793471313, 5.056974431379476, (
                4.166666666666667, 4.941315936186, 3.4612934079026743, 0.4091458561465175,
                1.0967334403685464e-06)),
            "liability_cf": (275365.76422915433, 99953.64588810306, (
                -99953.64588810306, 200.67346706335633, 2263.1561201398026,
                102.55100011944675, 0.000160861752843473)),
            "net_cf": (-275365.76422915433, 99953.64588810306, (
                99953.64588810306, -200.67346706335633, -2263.1561201398026,
                -102.55100011944675, -0.000160861752843473)),
        },
        "result_pols": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_death_last": (0.9999999494480459, 0.0029547092171364753, (
                0.0004218744523027951, 0.001304881007514469, 0.0025779555117311226,
                0.0008122101121449884, 1.0768345799005572e-08)),
            "certain_floor": (120.0, 1.0, (
                0.0, 0.0, 1.0, 0.0, 0.0)),
            "payment_factor_life": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
            "payment_factor": (120.43691100770673, 0.7150000000032242, (
                0.0, 0.0, 0.7150000000032242, 0.03231915430996991, 5.0551953972892716e-08)),
        },
    },
    8: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (363.86311494301873, 1.0, (
                1.0, 0.9532156577227293, 0.5397667963745717, 0.0356813641622318,
                6.132029977189829e-08)),
            "premiums": (149921.19125400326, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (385179.7381435378, 2818.4992039261183, (
                0.0, 0.0, 1540.7393830523072, 92.23371518344356, 0.00013399444353940916)),
            "claims": (25682.25058221909, 316.371538196647, (
                0.0408063091095201, 128.1680632768345, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2326.686442475089, 5.948400413103436, (
                4.166666666666667, 5.611953208768775, 4.6024281802444795,
                0.44063631375493156, 1.0967334403685464e-06)),
            "liability_cf": (263267.48391422874, 99995.79252702423, (
                -99995.79252702423, 133.78001648560326, 1545.3418112325517,
                92.6743514971985, 0.0001350911769797777)),
            "net_cf": (-263267.48391422874, 99995.79252702423, (
                99995.79252702423, -133.78001648560326, -1545.3418112325517,
                -92.6743514971985, -0.0001350911769797777)),
        },
        "result_pols": {
            "pols_if": (363.86311494301873, 1.0, (
                1.0, 0.9532156577227293, 0.5397667963745717, 0.0356813641622318,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (255.88141671809174, 1.0, (
                1.0, 0.7088627049052068, 0.22528010737422893, 0.0026373797290391984, 0.0)),
            "lives_if_last": (363.86311494301873, 1.0, (
                1.0, 0.9532156577227293, 0.5397667963745717, 0.0356813641622318,
                6.132029977189829e-08)),
            "lives_death_last": (0.999999949448046, 0.00387464985150493, (
                4.08063091095201e-07, 0.0008544537551788967, 0.0034400819136483074,
                0.0009251371105884684, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (96.87759124215614, 0.7088883104555843, (
                0.0, 0.0, 0.3875155034930994, 0.02319794961529703, 3.3701302650280206e-08)),
            "payment_factor": (96.87759124215614, 0.7088883104555843, (
                0.0, 0.0, 0.3875155034930994, 0.02319794961529703, 3.3701302650280206e-08)),
        },
    },
    9: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (363.86311494301873, 1.0, (
                1.0, 0.9532156577227293, 0.5397667963745717, 0.0356813641622318,
                6.132029977189829e-08)),
            "premiums": (149921.19125400326, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (411553.7351430198, 2788.1160798009114, (
                0.0, 0.0, 1679.5103951012964, 115.87121696368264, 0.00017256478174083105)),
            "claims": (26788.37022610164, 316.371538196647, (
                0.0408063091095201, 128.1680632768345, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2326.686442475089, 5.948400413103436, (
                4.166666666666667, 5.611953208768775, 4.6024281802444795,
                0.44063631375493156, 1.0967334403685464e-06)),
            "liability_cf": (290747.6005575933, 99995.79252702423, (
                -99995.79252702423, 133.78001648560326, 1684.1128232815408,
                116.31185327743758, 0.0001736615151811996)),
            "net_cf": (-290747.6005575933, 99995.79252702423, (
                99995.79252702423, -133.78001648560326, -1684.1128232815408,
                -116.31185327743758, -0.0001736615151811996)),
        },
        "result_pols": {
            "pols_if": (363.86311494301873, 1.0, (
                1.0, 0.9532156577227293, 0.5397667963745717, 0.0356813641622318,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (255.88141671809174, 1.0, (
                1.0, 0.7088627049052068, 0.22528010737422893, 0.0026373797290391984, 0.0)),
            "lives_if_last": (363.86311494301873, 1.0, (
                1.0, 0.9532156577227293, 0.5397667963745717, 0.0356813641622318,
                6.132029977189829e-08)),
            "lives_death_last": (0.999999949448046, 0.00387464985150493, (
                4.08063091095201e-07, 0.0008544537551788967, 0.0034400819136483074,
                0.0009251371105884684, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (120.56252305043378, 0.8167640831189856, (
                0.0, 0.0, 0.4920038221800535, 0.03394386947116676, 5.0551953972892716e-08)),
            "payment_factor": (120.56252305043378, 0.8167640831189856, (
                0.0, 0.0, 0.4920038221800535, 0.03394386947116676, 5.0551953972892716e-08)),
        },
    },
    10: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "premiums": (148750.0000001148, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (437420.7654541888, 2617.1536355088233, (
                0.0, 0.0, 1771.7965866077245, 191.06701105950813, 0.00040222239257941834)),
            "claims": (50173.54294198535, 443.2063825704713, (
                42.18744523027951, 195.73215112717034, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1985.4638793471313, 5.056974431379476, (
                4.166666666666667, 4.941315936186, 3.4612934079026743, 0.4091458561465175,
                1.0967334403685464e-06)),
            "liability_cf": (340829.7722754065, 99953.64588810306, (
                -99953.64588810306, 200.67346706335633, 1775.2578800156273,
                191.47615691565466, 0.0004033191260197869)),
            "net_cf": (-340829.7722754065, 99953.64588810306, (
                99953.64588810306, -200.67346706335633, -1775.2578800156273,
                -191.47615691565466, -0.0004033191260197869)),
        },
        "result_pols": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_death_last": (0.9999999494480459, 0.0029547092171364753, (
                0.0004218744523027951, 0.001304881007514469, 0.0025779555117311226,
                0.0008122101121449884, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
            "payment_factor": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
        },
    },
    11: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "premiums": (210000.0, 210000.0, (
                210000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (638467.6390752277, 5585.601752703725, (
                0.0, 0.0, 4058.068891916527, 325.1536909914487, 0.0005085886302428809)),
            "claims": (98573.33296093854, 620.4889355986599, (
                88.59363498358697, 274.0250115780385, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1985.4638793471313, 5.056974431379476, (
                4.166666666666667, 4.941315936186, 3.4612934079026743, 0.4091458561465175,
                1.0967334403685464e-06)),
            "liability_cf": (529026.4359155134, 209907.23969834976, (
                -209907.23969834976, 278.96632751422453, 4061.5301853244296,
                325.5628368475952, 0.0005096853636832495)),
            "net_cf": (-529026.4359155134, 209907.23969834976, (
                209907.23969834976, -278.96632751422453, -4061.5301853244296,
                -325.5628368475952, -0.0005096853636832495)),
        },
        "result_pols": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_death_last": (0.9999999494480459, 0.0029547092171364753, (
                0.0004218744523027951, 0.001304881007514469, 0.0025779555117311226,
                0.0008122101121449884, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (63.46147905095481, 0.5551895302471521, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
            "payment_factor": (63.46147905095481, 0.5551895302471521, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
        },
    },
    12: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "premiums": (250000.0, 250000.0, (
                250000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (760080.5227086045, 6649.525896075864, (
                0.0, 0.0, 4831.034395138723, 387.0877273707723, 0.0006054626550510487)),
            "claims": (117349.20590587921, 738.6773042841188, (
                105.46861307569877, 326.22025187861726, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1985.4638793471313, 5.056974431379476, (
                4.166666666666667, 4.941315936186, 3.4612934079026743, 0.4091458561465175,
                1.0967334403685464e-06)),
            "liability_cf": (629415.1924938308, 249890.36472025764, (
                -249890.36472025764, 331.1615678148033, 4834.495688546625,
                387.4968732269188, 0.0006065593884914173)),
            "net_cf": (-629415.1924938308, 249890.36472025764, (
                249890.36472025764, -331.1615678148033, -4834.495688546625,
                -387.4968732269188, -0.0006065593884914173)),
        },
        "result_pols": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_death_last": (0.9999999494480459, 0.0029547092171364753, (
                0.0004218744523027951, 0.001304881007514469, 0.0025779555117311226,
                0.0008122101121449884, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (63.46147905095481, 0.5551895302471521, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
            "payment_factor": (63.46147905095481, 0.5551895302471521, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
        },
    },
    13: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "premiums": (148750.0000001148, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (438452.3532173224, 3835.778170613267, (
                0.0, 0.0, 2786.7815787123545, 223.29150648730223, 0.00034926105585014885)),
            "claims": (69317.31870518246, 443.2063825704713, (
                42.18744523027951, 195.73215112717034, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1985.4638793471313, 5.056974431379476, (
                4.166666666666667, 4.941315936186, 3.4612934079026743, 0.4091458561465175,
                1.0967334403685464e-06)),
            "liability_cf": (361005.13580173714, 99953.64588810306, (
                -99953.64588810306, 200.67346706335633, 2790.2428721202573,
                223.70065234344875, 0.0003503577892905174)),
            "net_cf": (-361005.13580173714, 99953.64588810306, (
                99953.64588810306, -200.67346706335633, -2790.2428721202573,
                -223.70065234344875, -0.0003503577892905174)),
        },
        "result_pols": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_death_last": (0.9999999494480459, 0.0029547092171364753, (
                0.0004218744523027951, 0.001304881007514469, 0.0025779555117311226,
                0.0008122101121449884, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (63.46147905095481, 0.5551895302471521, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
            "payment_factor": (63.46147905095481, 0.5551895302471521, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
        },
    },
    14: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "premiums": (148750.0000001148, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (372738.4979477012, 14941.678546767947, (
                0.0, 0.0, 1482.560123899215, 118.79046641194505, 0.0001858059196995336)),
            "claims": (50277.65862970876, 443.2063825704713, (
                42.18744523027951, 195.73215112717034, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1985.4638793471313, 5.056974431379476, (
                4.166666666666667, 4.941315936186, 3.4612934079026743, 0.4091458561465175,
                1.0967334403685464e-06)),
            "liability_cf": (276251.6204566423, 99953.64588810306, (
                -99953.64588810306, 200.67346706335633, 1486.0214173071176,
                119.19961226809157, 0.00018690265313990216)),
            "net_cf": (-276251.6204566423, 99953.64588810306, (
                99953.64588810306, -200.67346706335633, -1486.0214173071176,
                -119.19961226809157, -0.00018690265313990216)),
        },
        "result_pols": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_death_last": (0.9999999494480459, 0.0029547092171364753, (
                0.0004218744523027951, 0.001304881007514469, 0.0025779555117311226,
                0.0008122101121449884, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
            "payment_factor": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
        },
    },
    15: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (107757.72099369307, 1640.6764803997796, (
                0.0, 0.0, 79.53640333471633, 74.16122565390165, 0.00011599916352615842)),
            "claims": (28499.99999967758, 221.4076560081768, (
                42.18744523027951, 130.4881007514469, 0.0, 0.0, 0.0)),
            "commutations": (135401.2245074111, 135401.2245074111, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1985.4638793471313, 5.056974431379476, (
                4.166666666666667, 4.941315936186, 3.4612934079026743, 0.4091458561465175,
                1.0967334403685464e-06)),
            "liability_cf": (173644.4093801289, 135485.52209396064, (
                -99953.64588810306, 135.42941668763288, 82.997696742619, 74.57037151004818,
                0.00011709589696652696)),
            "net_cf": (-173644.4093801289, 135485.52209396064, (
                99953.64588810306, -135.42941668763288, -82.997696742619,
                -74.57037151004818, -0.00011709589696652696)),
        },
        "result_pols": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_death_last": (0.9999999494480459, 0.0029547092171364753, (
                0.0004218744523027951, 0.001304881007514469, 0.0025779555117311226,
                0.0008122101121449884, 1.0768345799005572e-08)),
            "certain_floor": (120.0, 1.0, (
                0.0, 0.0, 1.0, 0.0, 0.0)),
            "payment_factor_life": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.40335803760501693, 0.03231915430996991,
                5.0551953972892716e-08)),
            "payment_factor": (120.43691100770673, 0.7150000000032242, (
                0.0, 0.0, 0.7150000000032242, 0.03231915430996991, 5.0551953972892716e-08)),
        },
    },
    16: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (350.79342836044043, 1.0, (
                1.0, 0.8701509952098756, 0.5244715811896083, 0.06308344319410257,
                1.1685238184017797e-07)),
            "premiums": (148933.97238022063, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (405644.1333102528, 2409.7332839060823, (
                0.0, 0.0, 1630.0850455348923, 192.2729895724894, 0.00030074349179676956)),
            "claims": (40686.50563563836, 338.70185257247607, (
                36.63898889509909, 152.82949219372898, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2279.1975988817276, 5.285409892719522, (
                4.166666666666667, 5.122919068857596, 4.472010507532859, 0.779030076922915,
                2.08994273067087e-06)),
            "liability_cf": (299675.8641645523, 99959.19434443823, (
                -99959.19434443823, 157.95241126258657, 1634.557056042425,
                193.0520196494123, 0.0003028334345274404)),
            "net_cf": (-299675.8641645523, 99959.19434443823, (
                99959.19434443823, -157.95241126258657, -1634.557056042425,
                -193.0520196494123, -0.0003028334345274404)),
        },
        "result_pols": {
            "pols_if": (350.79342836044043, 1.0, (
                1.0, 0.8701509952098756, 0.5244715811896083, 0.06308344319410257,
                1.1685238184017797e-07)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (350.79342836044043, 1.0, (
                1.0, 0.8701509952098756, 0.5244715811896083, 0.06308344319410257,
                1.1685238184017797e-07)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (350.79342836044043, 1.0, (
                1.0, 0.8701509952098756, 0.5244715811896083, 0.06308344319410257,
                1.1685238184017797e-07)),
            "lives_death_last": (0.9999999036678514, 0.003022571236450333, (
                0.0003663898889509909, 0.0010188632812915266, 0.0023336161705973524,
                0.001495842118627147, 2.052023326326152e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (129.93322211542375, 0.7718696865195971, (
                0.0, 0.0, 0.522137965019011, 0.06158760107547542, 9.633214857691646e-08)),
            "payment_factor": (129.93322211542375, 0.7718696865195971, (
                0.0, 0.0, 0.522137965019011, 0.06158760107547542, 9.633214857691646e-08)),
        },
    },
    17: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "premiums": (148750.0000001148, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (371612.1025549993, 2602.7929387992044, (
                0.0, 0.0, 1477.7165545230068, 120.60710681157339, 0.0002232224381127659)),
            "claims": (49947.71268544535, 432.45044370818727, (
                42.18744523027951, 195.73215112717034, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1985.4638793471313, 5.056974431379476, (
                4.166666666666667, 4.941315936186, 3.4612934079026743, 0.4091458561465175,
                1.0967334403685464e-06)),
            "liability_cf": (274795.279119677, 99953.64588810306, (
                -99953.64588810306, 200.67346706335633, 1481.1778479309096,
                121.01625266771991, 0.00022431917155313444)),
            "net_cf": (-274795.279119677, 99953.64588810306, (
                99953.64588810306, -200.67346706335633, -1481.1778479309096,
                -121.01625266771991, -0.00022431917155313444)),
        },
        "result_pols": {
            "pols_if": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (317.50122929076656, 1.0, (
                1.0, 0.8393048810114214, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "lives_death_last": (0.9999999494480459, 0.0029547092171364753, (
                0.0004218744523027951, 0.001304881007514469, 0.0025779555117311226,
                0.0008122101121449884, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (102.08366918753217, 0.7150000000032242, (
                0.0, 0.0, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
            "payment_factor": (102.08366918753217, 0.7150000000032242, (
                0.0, 0.0, 0.40593599311674805, 0.033131364422114895,
                6.132029977189829e-08)),
        },
    },
    18: {"rows": 661, "months": (0, 165, 330, 495, 660),
        "result_cf": {
            "pols_if": (259.21730460499197, 0.9754115011951324, (
                0.9754115011951324, 0.7459152775417122, 0.3250710186811638,
                0.021903203699907895, 6.132029977189829e-08)),
            "premiums": (48750.00000011479, 48750.00000011479, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (372738.4979477012, 14941.678546767947, (
                0.0, 0.0, 1184.9634485160052, 78.10740089000937, 0.0001858059196995336)),
            "claims": (47818.808749222015, 443.2063825704713, (
                41.15011928365053, 295.6169806332176, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1532.6555878417594, 4.476588358547012, (
                4.064214588313052, 4.284385202564309, 2.6382222338994845,
                0.25117411543541557, 9.935863674753385e-07)),
            "liability_cf": (373339.96228465025, 48604.47544486698, (
                45.21433387196358, 299.9013658357819, 1187.6016707499048, 78.35857500544479,
                0.00018679950606700896)),
            "net_cf": (-373339.96228465025, 48604.47544486698, (
                -45.21433387196358, -299.9013658357819, -1187.6016707499048,
                -78.35857500544479, -0.00018679950606700896)),
        },
        "result_pols": {
            "pols_if": (259.21730460499197, 0.9754115011951324, (
                0.9754115011951324, 0.7459152775417122, 0.3250710186811638,
                0.021903203699907895, 6.132029977189829e-08)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (259.21730460499197, 0.9754115011951324, (
                0.9754115011951324, 0.7459152775417122, 0.3250710186811638,
                0.021903203699907895, 6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (259.21730460499197, 0.9754115011951324, (
                0.9754115011951324, 0.7459152775417122, 0.3250710186811638,
                0.021903203699907895, 6.132029977189829e-08)),
            "lives_death_last": (0.9754114506431785, 0.0029547092171364753, (
                0.0004115011928365053, 0.0019707798708881175, 0.00267968795387008,
                0.0006526335290591122, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.3223913307272937, 0.021250570170848783,
                5.0551953972892716e-08)),
            "payment_factor": (101.3686692380809, 0.7120452907860877, (
                0.0, 0.0, 0.3223913307272937, 0.021250570170848783,
                5.0551953972892716e-08)),
        },
    },
    19: {"rows": 479, "months": (0, 119, 239, 358, 478),
        "result_cf": {
            "pols_if": (101.36866918752895, 0.7120452907860877, (
                0.7120452907860877, 0.40335803760501693, 0.11187935371150086,
                0.004400342059577031, 6.132029977189829e-08)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (371252.24550740723, 2615.386781546326, (
                2615.386781546326, 1477.4040702283398, 405.69368634978673,
                15.572564244642106, 0.00018645098247136176)),
            "claims": (8306.78432484535, 430.5220184108041, (
                430.5220184108041, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (517.1498981422361, 2.9668553782753655, (
                2.9668553782753655, 2.098912153315265, 0.7452331232549979,
                0.037520385532677863, 6.69304550718522e-07)),
            "liability_cf": (380076.17973039486, 3048.8756553354056, (
                3048.8756553354056, 1479.502982381655, 406.4389194730417,
                15.610084630174784, 0.00018712028702208027)),
            "net_cf": (-380076.17973039486, 3048.8756553354056, (
                -3048.8756553354056, -1479.502982381655, -406.4389194730417,
                -15.610084630174784, -0.00018712028702208027)),
        },
        "result_pols": {
            "pols_if": (101.36866918752895, 0.7120452907860877, (
                0.7120452907860877, 0.40335803760501693, 0.11187935371150086,
                0.004400342059577031, 6.132029977189829e-08)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (101.36866918752895, 0.7120452907860877, (
                0.7120452907860877, 0.40335803760501693, 0.11187935371150086,
                0.004400342059577031, 6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (101.36866918752895, 0.7120452907860877, (
                0.7120452907860877, 0.40335803760501693, 0.11187935371150086,
                0.004400342059577031, 6.132029977189829e-08)),
            "lives_death_last": (0.7120452402341337, 0.0029424989981745586, (
                0.0029424989981745586, 0.0027934411217623856, 0.0018847144362819923,
                0.00017819455195540977, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (100.65662394729482, 0.7091027917879131, (
                0.7091027917879131, 0.40056459648325454, 0.10999463927521887,
                0.004222147507621621, 5.0551953972892716e-08)),
            "payment_factor": (100.65662394729482, 0.7091027917879131, (
                0.7091027917879131, 0.40056459648325454, 0.10999463927521887,
                0.004222147507621621, 5.0551953972892716e-08)),
        },
    },
    20: {"rows": 420, "months": (0, 104, 209, 314, 419),
        "result_cf": {
            "pols_if": (64.01917900040468, 0.5577000000018264, (
                0.5577000000018264, 0.2853706121233593, 0.06584759323072924,
                0.002188797954712187, 6.132029977189829e-08)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (245048.6107463768, 2259.6948267319, (
                2259.6948267319, 893.7733600157696, 203.88534281056644, 6.56906347148242,
                0.00015976501940310445)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (313.6243799825197, 2.3237500000076103, (
                2.3237500000076103, 1.4487349194803323, 0.4174787513101568,
                0.017330653236759214, 5.915676968691274e-07)),
            "liability_cf": (245362.2351263593, 2262.0185767319076, (
                2262.0185767319076, 895.22209493525, 204.3028215618766, 6.586394124719179,
                0.00016035658709997357)),
            "net_cf": (-245362.2351263593, 2262.0185767319076, (
                -2262.0185767319076, -895.22209493525, -204.3028215618766,
                -6.586394124719179, -0.00016035658709997357)),
        },
        "result_pols": {
            "pols_if": (64.01917900040468, 0.5577000000018264, (
                0.5577000000018264, 0.2853706121233593, 0.06584759323072924,
                0.002188797954712187, 6.132029977189829e-08)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (64.01917900040468, 0.5577000000018264, (
                0.5577000000018264, 0.2853706121233593, 0.06584759323072924,
                0.002188797954712187, 6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (64.01917900040468, 0.5577000000018264, (
                0.5577000000018264, 0.2853706121233593, 0.06584759323072924,
                0.002188797954712187, 6.132029977189829e-08)),
            "lives_death_last": (0.5576999494498724, 0.0028033679377134635, (
                0.0025104697546742827, 0.00256784386708786, 0.0013353332628446013,
                0.00011025162776236294, 1.0768345799005572e-08)),
            "certain_floor": (60.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (63.46147905095481, 0.5551895302471521, (
                0.5551895302471521, 0.28280276825627143, 0.06451225996788464,
                0.002078546326949824, 5.0551953972892716e-08)),
            "payment_factor": (77.53691100751328, 0.7150000000032242, (
                0.7150000000032242, 0.28280276825627143, 0.06451225996788464,
                0.002078546326949824, 5.0551953972892716e-08)),
        },
    },
    21: {"rows": 467, "months": (0, 116, 233, 349, 466),
        "result_cf": {
            "pols_if": (93.01568019456184, 0.6775268941874188, (
                0.6775268941874188, 0.3789023807899722, 0.10103675140839982,
                0.0038500003525154115, 6.132029977189829e-08)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (87990.066825561, 919.1565207383783, (
                79.53640333471633, 863.4279264503919, 227.93858899303413, 8.436093091436932,
                0.00011599916352615842)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (470.5812461836162, 2.823028725780912, (
                2.823028725780912, 1.9716548024733578, 0.673010089151779,
                0.03282778828816982, 6.529800494814851e-07)),
            "liability_cf": (88460.64807174464, 921.2042399123444, (
                82.35943206049724, 865.3995812528652, 228.6115990821859, 8.468920879725102,
                0.00011665214357563991)),
            "net_cf": (-88460.64807174464, 921.2042399123444, (
                -82.35943206049724, -865.3995812528652, -228.6115990821859,
                -8.468920879725102, -0.00011665214357563991)),
        },
        "result_pols": {
            "pols_if": (93.01568019456184, 0.6775268941874188, (
                0.6775268941874188, 0.3789023807899722, 0.10103675140839982,
                0.0038500003525154115, 6.132029977189829e-08)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (93.01568019456184, 0.6775268941874188, (
                0.6775268941874188, 0.3789023807899722, 0.10103675140839982,
                0.0038500003525154115, 6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (93.01568019456184, 0.6775268941874188, (
                0.6775268941874188, 0.3789023807899722, 0.10103675140839982,
                0.0038500003525154115, 6.132029977189829e-08)),
            "lives_death_last": (0.6775268436354649, 0.0028033679377134635, (
                0.0027998530896564677, 0.0026240743779819, 0.0017020604576022946,
                0.00017358599998269861, 1.0768345799005572e-08)),
            "certain_floor": (107.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (92.33815335092639, 0.6747270410977624, (
                0.6747270410977624, 0.3762783064119903, 0.09933469095079753,
                0.003676414352532713, 5.0551953972892716e-08)),
            "payment_factor": (111.14191100766482, 0.7150000000032242, (
                0.7150000000032242, 0.3762783064119903, 0.09933469095079753,
                0.003676414352532713, 5.0551953972892716e-08)),
        },
    },
    22: {"rows": 599, "months": (0, 149, 299, 448, 598),
        "result_cf": {
            "pols_if": (200.46035531633294, 0.9185696609756028, (
                0.9185696609756028, 0.6314709019448987, 0.24448054845789444,
                0.013690509478364274, 6.132029977189829e-08)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (438452.35321732226, 3835.778170613267, (
                0.0, 0.0, 1670.972240552415, 91.47203261377551, 0.00034926105585014885)),
            "claims": (58352.76785140808, 443.2063825704713, (
                214.21728834252195, 391.42927852902073, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1122.1971510882759, 3.9400627416779948, (
                3.827373587398345, 3.5385756619267656, 1.8424929673499035,
                0.14223005829666224, 8.567664107350667e-07)),
            "liability_cf": (497927.31821981876, 4215.632031730925, (
                218.0446619299203, 394.9678541909475, 1672.814733519765, 91.61426267207217,
                0.0003501178222608839)),
            "net_cf": (-497927.31821981876, 4215.632031730925, (
                -218.0446619299203, -394.9678541909475, -1672.814733519765,
                -91.61426267207217, -0.0003501178222608839)),
        },
        "result_pols": {
            "pols_if": (200.46035531633294, 0.9185696609756028, (
                0.9185696609756028, 0.6314709019448987, 0.24448054845789444,
                0.013690509478364274, 6.132029977189829e-08)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (200.46035531633294, 0.9185696609756028, (
                0.9185696609756028, 0.6314709019448987, 0.24448054845789444,
                0.013690509478364274, 6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (200.46035531633294, 0.9185696609756028, (
                0.9185696609756028, 0.6314709019448987, 0.24448054845789444,
                0.013690509478364274, 6.132029977189829e-08)),
            "lives_death_last": (0.9185696104236488, 0.0029547092171364753, (
                0.001428115255616813, 0.002609528523526805, 0.002624462932488719,
                0.0004508713765929255, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (63.46147905095481, 0.5551895302471521, (
                0.0, 0.0, 0.24185608552540572, 0.013239638101771348,
                5.0551953972892716e-08)),
            "payment_factor": (63.46147905095481, 0.5551895302471521, (
                0.0, 0.0, 0.24185608552540572, 0.013239638101771348,
                5.0551953972892716e-08)),
        },
    },
    23: {"rows": 48, "months": (0, 11, 23, 35, 47),
        "result_cf": {
            "pols_if": (0.00041701855920424764, 4.245667410253595e-05, (
                4.245667410253595e-05, 1.4008772419444333e-05, 3.3869882781458802e-06,
                5.94430392025299e-07, 6.132029977189829e-08)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (0.9929583547479648, 0.10174613331276695, (
                0.10174613331276695, 0.033571598724259466, 0.007963224258808068,
                0.0013598238616896457, 0.00013399444353940916)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (0.001751164506588803, 0.0001769028087605665, (
                0.0001769028087605665, 5.8369885081018055e-05, 1.4465262437914695e-05,
                2.602180960923249e-06, 2.7514689977727867e-07)),
            "liability_cf": (0.9947095192545535, 0.10192303612152752, (
                0.10192303612152752, 0.033629968609340484, 0.007977689521245983,
                0.001362426042650569, 0.00013426959043918643)),
            "net_cf": (-0.9947095192545535, 0.10192303612152752, (
                -0.10192303612152752, -0.033629968609340484, -0.007977689521245983,
                -0.001362426042650569, -0.00013426959043918643)),
        },
        "result_pols": {
            "pols_if": (0.00041701855920424764, 4.245667410253595e-05, (
                4.245667410253595e-05, 1.4008772419444333e-05, 3.3869882781458802e-06,
                5.94430392025299e-07, 6.132029977189829e-08)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (0.00041701855920424764, 4.245667410253595e-05, (
                4.245667410253595e-05, 1.4008772419444333e-05, 3.3869882781458802e-06,
                5.94430392025299e-07, 6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (0.00041701855920424764, 4.245667410253595e-05, (
                4.245667410253595e-05, 1.4008772419444333e-05, 3.3869882781458802e-06,
                5.94430392025299e-07, 6.132029977189829e-08)),
            "lives_death_last": (4.240612214856306e-05, 4.071008904157375e-06, (
                4.071008904157375e-06, 1.3432478747190826e-06, 3.8271037248263396e-07,
                8.14109603862659e-08, 1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (0.0002497416247162768, 2.559044346686524e-05, (
                2.559044346686524e-05, 8.443683030239017e-06, 2.002851937208973e-06,
                3.420129544431227e-07, 3.3701302650280206e-08)),
            "payment_factor": (0.0002497416247162768, 2.559044346686524e-05, (
                2.559044346686524e-05, 8.443683030239017e-06, 2.002851937208973e-06,
                3.420129544431227e-07, 3.3701302650280206e-08)),
        },
    },
    24: {"rows": 450, "months": (0, 112, 224, 336, 449),
        "result_cf": {
            "pols_if": (81.87074780576177, 0.6314709019448986, (
                0.6314709019448986, 0.3439849391032658, 0.08790468561901821,
                0.003201219869061903, 6.132029977189829e-08)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (302600.0774223771, 2628.013798576489, (
                2628.013798576489, 1254.7802744572655, 317.12847371404837,
                11.23571686863485, 0.00018580591969953364)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (409.33588577651534, 2.6311287581037446, (
                2.6311287581037446, 1.7899585527740471, 0.57125545522063,
                0.026630081343869485, 6.37053706811205e-07)),
            "liability_cf": (303009.4133081536, 2630.644927334593, (
                2630.644927334593, 1256.5702330100396, 317.699729169269, 11.262346949978719,
                0.00018644297340634486)),
            "net_cf": (-303009.4133081536, 2630.644927334593, (
                -2630.644927334593, -1256.5702330100396, -317.699729169269,
                -11.262346949978719, -0.00018644297340634486)),
        },
        "result_pols": {
            "pols_if": (81.87074780576177, 0.6314709019448986, (
                0.6314709019448986, 0.3439849391032658, 0.08790468561901821,
                0.003201219869061903, 6.132029977189829e-08)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (81.87074780576177, 0.6314709019448986, (
                0.6314709019448986, 0.3439849391032658, 0.08790468561901821,
                0.003201219869061903, 6.132029977189829e-08)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (81.87074780576177, 0.6314709019448986, (
                0.6314709019448986, 0.3439849391032658, 0.08790468561901821,
                0.003201219869061903, 6.132029977189829e-08)),
            "lives_death_last": (0.6314708513929447, 0.0028033679377134635, (
                0.002609528523526805, 0.002598643214348606, 0.0016239899737409413,
                0.00014433426006637455, 1.0768345799005572e-08)),
            "certain_floor": (11.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (81.23927695436882, 0.6288613734213718, (
                0.6288613734213718, 0.34138629588891717, 0.08628069564527727,
                0.0030568856089955286, 5.0551953972892716e-08)),
            "payment_factor": (82.32797539920453, 0.7150000000032242, (
                0.7150000000032242, 0.34138629588891717, 0.08628069564527727,
                0.0030568856089955286, 5.0551953972892716e-08)),
        },
    },
    25: {"rows": 1, "months": (0,),
        "result_cf": {
            "pols_if": (6.132029977189829e-08, 6.132029977189829e-08, (
                6.132029977189829e-08,)),
            "premiums": (0.0, 0.0, (
                0.0,)),
            "annuity_payments": (0.00018645098247136176, 0.00018645098247136176, (
                0.00018645098247136176,)),
            "claims": (0.0, 0.0, (
                0.0,)),
            "commutations": (0.0, 0.0, (
                0.0,)),
            "expenses": (2.555012490495762e-07, 2.555012490495762e-07, (
                2.555012490495762e-07,)),
            "liability_cf": (0.00018670648372041133, 0.00018670648372041133, (
                0.00018670648372041133,)),
            "net_cf": (-0.00018670648372041133, 0.00018670648372041133, (
                -0.00018670648372041133,)),
        },
        "result_pols": {
            "pols_if": (6.132029977189829e-08, 6.132029977189829e-08, (
                6.132029977189829e-08,)),
            "pols_new_biz": (0.0, 0.0, (
                0.0,)),
            "lives_if_1": (6.132029977189829e-08, 6.132029977189829e-08, (
                6.132029977189829e-08,)),
            "lives_if_2": (0.0, 0.0, (
                0.0,)),
            "lives_if_last": (6.132029977189829e-08, 6.132029977189829e-08, (
                6.132029977189829e-08,)),
            "lives_death_last": (1.0768345799005572e-08, 1.0768345799005572e-08, (
                1.0768345799005572e-08,)),
            "certain_floor": (0.0, 0.0, (
                0.0,)),
            "payment_factor_life": (5.0551953972892716e-08, 5.0551953972892716e-08, (
                5.0551953972892716e-08,)),
            "payment_factor": (5.0551953972892716e-08, 5.0551953972892716e-08, (
                5.0551953972892716e-08,)),
        },
    },
    26: {"rows": 733, "months": (0, 183, 366, 549, 732),
        "result_cf": {
            "pols_if": (363.86311494301873, 1.0, (
                0.0, 0.9606683655717615, 0.5607357891285012, 0.03861329758228967,
                6.132029977189829e-08)),
            "premiums": (149921.19125400326, 100000.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (385179.7381435378, 2818.4992039261183, (
                0.0, 0.0, 1608.9957485098853, 99.82132284778152, 0.00013399444353940916)),
            "claims": (25682.250582219094, 316.371538196647, (
                0.0, 120.94204887472814, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2389.718744541361, 6.10801053408221, (
                0.0, 5.797225968626325, 4.9007550487782705, 0.48876443055830937,
                1.1522555707872038e-06)),
            "liability_cf": (263330.5162162951, 99995.68836035756, (
                0.0, 126.73927484335447, 1613.8965035586637, 100.31008727833982,
                0.00013514669911019635)),
            "net_cf": (-263330.5162162951, 99995.68836035756, (
                0.0, -126.73927484335447, -1613.8965035586637, -100.31008727833982,
                -0.00013514669911019635)),
        },
        "result_pols": {
            "pols_if": (363.86311494301873, 1.0, (
                0.0, 0.9606683655717615, 0.5607357891285012, 0.03861329758228967,
                6.132029977189829e-08)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (317.50122929076656, 1.0, (
                0.0, 0.8511406253317861, 0.4217534381159279, 0.0356925290265281,
                6.132029977189829e-08)),
            "lives_if_2": (255.8814167180917, 1.0, (
                0.0, 0.7357799297766557, 0.24035136596356751, 0.0030288768299316865, 0.0)),
            "lives_if_last": (363.86311494301873, 1.0, (
                0.0, 0.9606683655717615, 0.5607357891285012, 0.03861329758228967,
                6.132029977189829e-08)),
            "lives_death_last": (0.999999949448046, 0.00387464985150493, (
                0.0, 0.000806280325831521, 0.0035335137021212937, 0.0010041553658839686,
                1.0768345799005572e-08)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (96.87759124215611, 0.7088883104555843, (
                0.0, 0.0, 0.40468284543155386, 0.025106329213233355,
                3.3701302650280206e-08)),
            "payment_factor": (96.87759124215611, 0.7088883104555843, (
                0.0, 0.0, 0.40468284543155386, 0.025106329213233355,
                3.3701302650280206e-08)),
        },
    },
}
# END generated fingerprint: DIA_US_SEC


# ---------------------------------------------------------------------------
# Compiled (USLIB-SEC-PLAN.md Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython CI job, which sets USLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is DIA's
# own: the comparison on the splice grid, at the contract's extremes, where the cap on
# mortality binds and a NaN meets it, where the reference rate's floor binds, on a label
# that is not text and on keys written as floats, the refusals, the total's sign of zero,
# the deepest call, a Reference set late and the runner.  Each comparison adds
# _dia_c4_also's calls, which no swept cell reaches.  None asks for sec_read, sec_model or
# s_model, which sweep every committed point; the grid and cap tests alone ask for
# spliced.


def _quietly(call, *args):
    """``call(*args)``, its raise dropped: a point's projection holds what it refuses."""
    try:
        call(*args)
    except Exception:                       # a refused call: C4 compares the sweep's raises
        pass


def _dia_c4_also(proj):
    """What C4 compares of a ``DIA_US_SEC`` point beyond its full sweep (M24).

    ``sec_support.full_sweep`` reaches a cell of more than ``t`` only at the keys some
    swept cell asks of it.  So, as ``sample_sec.py`` does, this calls the per-life cells
    no report reads, for both lives at ``t = 0 .. proj_len()``, ``lives_death`` and, from
    ``t_entry()``, ``age``, ``mort_rate_base`` and ``improvement_rate``; each life's
    ``sex`` label; ``claims_ann`` at the total, ``ALL``, for every policy year
    ``result_annual`` shows; and the two engine cells at the arguments the sample passes.
    Every timing, both kinds and every basis are reached by the reports.  Passed to
    :func:`compiled_mismatches` as ``also``, which must not raise: a call a point refuses,
    a single life's second age among them, is dropped here, and its raise is compared
    where the sweep meets it.
    """
    entry = proj.t_entry()
    for t in range(proj.proj_len() + 1):
        for life in (1, 2):
            _quietly(proj.lives_death, t, life)
            if t >= entry:
                for cell in ("age", "mort_rate_base", "improvement_rate"):
                    _quietly(proj.cells[cell], t, life)
    for life in (1, 2):
        _quietly(proj.sex, life)
    try:
        years = list(proj.result_annual().index)
    except Exception:                       # a refused point: the sweep holds the raise
        years = []
    for y in years:
        _quietly(proj.claims_ann, y, proj.ALL)
    try:
        start = proj.income_start_mth()
        guarantee = proj.guarantee_mths_pricing()
    except Exception:                       # a refused point: the sweep holds the raise
        return
    _quietly(proj.annuity_factor, start, guarantee, proj.pricing_rate, start)
    _quietly(proj.pricing_disc_factor, 20.0)


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)


def _copied(folder, file):
    """An edit that replaces ``file`` with the copy in ``folder``, as written there."""
    return lambda _: pd.read_csv(folder / file)


def _case_rows(*rows):
    """A table of committed rows and its premium schedule, the rows labelled 1 to n.

    Each row is ``(point_id, {column: value})``, the committed row with ``columns`` set,
    taking its point's premiums under its new label, or ``(point_id, columns, premiums)``,
    with ``premiums`` its own, as ``(premium_mth, premium_amt)`` pairs.
    """
    committed, schedule = _committed(), _committed_schedule()
    table, premiums = [], []
    for label, (point, columns, *given) in enumerate(rows, 1):
        row = committed.loc[[point]].assign(**columns)
        row.index = pd.Index([label], name="point_id")
        table.append(row)
        premiums.append(_premiums(*((label, m, a) for m, a in given[0])) if given
                        else schedule[schedule["point_id"] == point].assign(point_id=label))
    return pd.concat(table), pd.concat(premiums, ignore_index=True)


def _frames(folder, tag, refs=None):
    """Each point's ``proj_len()`` in modelx, on the case in ``folder``, in table order."""
    model = _read(folder, tag, refs)
    try:
        return [projection(model, key).proj_len() for key in point_keys(model)]
    finally:
        model.close()


def _mismatch_lines(found):
    return f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


# How many rows of the splice grid C4 compares at once.  compiled_mismatches sweeps every
# row of its case in one modelx read, _dia_c4_also's calls with it, and keeps every value
# of every row, in the parent and in the child, until it compares them.  A DIA row on the
# grid runs at most 720 months, so twenty rows hold what SPIA's twenty did, below
# WholeLife's chunk (USLIB-SEC-PLAN.md §7.2, *For M16 and later*, item 7).
C4_CHUNK = 20


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_the_splice_grid(spliced,
                                                                             sec_build,
                                                                             tmp_path):
    """C4 on the branches: compiled, every cell of the splice grid is modelx's.

    The sample traces the committed points alone, and they leave branches untaken, which
    are typed all the same, because every branch of a cell returns the one type the
    others return (sample_sec.py).  What the compiled model computes on them is held
    here: the splice grid's rows, S's points and variants restated in force at T2's months
    and issued later, every form, trigger, basis, timing, frequency and market type among
    them, the three options, the commuted and accelerating guarantees and the capped
    rates, under the splice's References with the reference rate's change switched on
    (:data:`SPLICED_REFS`), on the splice's set-apart tables.  The grid is the one this
    run's ``spliced`` selects, the core by default and the full grid under
    ``USLIB_SEC_FULL=1``, and the test carries no ``sec_full`` mark, since a skipped
    compile test fails the cython job.  The grid's SEC table goes beside the build
    :data:`C4_CHUNK` rows at a time, each chunk with its points' premiums still due;
    modelx sweeps every row fully, with :func:`_dia_c4_also`'s calls, and the compiled
    model must agree at every argument modelx caches, identically on x86-64 and to 1e-12
    relative elsewhere, with every raise and every ``Data`` array
    (``sec_support.compiled_mismatches``).
    """
    build = sec_build(SEC)
    inputs = spliced[1].Data.input_dir()
    table = pd.read_csv(inputs / TABLE, index_col="point_id")
    schedule = pd.read_csv(inputs / SCHEDULE)
    assert len(table) == len(spliced[1].Data.model_point_table())
    edits = {file: _copied(inputs, file) for file in SPLICED_EDITS}
    chunks = [table.iloc[i:i + C4_CHUNK] for i in range(0, len(table), C4_CHUNK)]
    assert sum(len(chunk) for chunk in chunks) == len(table) and len(chunks) > 1
    found = []
    for i, chunk in enumerate(chunks):
        due = schedule[schedule["point_id"].isin(chunk.index)]
        folder = compiled_case(build, tmp_path / f"grid{i}", model_points=chunk,
                               edits={**edits, SCHEDULE: due})
        found += compiled_mismatches(build, folder, refs=SPLICED_REFS, also=_dia_c4_also)
        shutil.rmtree(tmp_path / f"grid{i}")
    assert not found, _mismatch_lines(found)


def _factor_keys_at_0():
    """Edits of the two factor tables adding the keys the anchor's twin on the table
    basis reads from issue age 0: its payout factor at income start age 20, and its ROP
    factors at issue age 0 and 5, 20 and 15 years' deferral."""
    def payout(df):
        return pd.concat([df, pd.DataFrame([{
            "income_start_age": 20, "sex": "F", "payout_form": "CR",
            "payout_factor": 21.75, "provenance": "[std] a test case"}])],
            ignore_index=True)

    def rop(df):
        return pd.concat([df, pd.DataFrame([
            {"issue_age": 0, "sex": "F", "deferral_years": 20, "rop_factor": 0.0123,
             "provenance": "[std] a test case"},
            {"issue_age": 5, "sex": "F", "deferral_years": 15, "rop_factor": 0.0234,
             "provenance": "[std] a test case"}])], ignore_index=True)
    return {"payout_factor_table.csv": payout, "rop_factor_table.csv": rop}


def _contract_extremes():
    """The contract's extremes, as [(case, the table, its premiums, the edits, the
    References, its frames)].

    Each table holds at most four points, since a point at the longest cover holds about
    0.3 GB of modelx's graph in C4's sweep, and all read the age tables from age 0
    (:data:`FROM_AGE_0`):

    * the longest covers, each from issue age 0: the cash refund on computed factors,
      issued at the valuation date, 1,440 months, and 120 months on, 1,560, ``t`` to
      1,560 in the month after it and ``k`` to 1,440 in the instalments scheduled to date;
      the installment refund 120 months on, 1,560 months, whose refund period's search
      reads the payout schedule from issue; and the same paying in advance from policy
      month 1,440, the latest income start month, whose refund period rounds up to a
      whole instalment, so that its stop rule is policy month 1,441: 1,561 months, ``t`` to
      1,561, the longest frame the contract allows;
    * options and lives at 0: that installment refund in advance from 1,440, issued at the
      valuation date and accelerated at its income start month, so that ``accel_cost``
      reads the pricing survival to policy month 1,445, the top of ``k``, and ``y`` to
      121; the period certain from 1,320, its 10 years ending at 1,440, the latest month
      the caches hold; the joint cash refund on either death at 0 and 0, quarterly in
      advance with a 3% COLA; and the generational cash refund at 0, issued in 1990, so
      that its improvement exponent is negative at first;
    * the edges: the anchor on the table basis at 0, reading payout and ROP keys the
      shipped tables lack and the test adds (:func:`_factor_keys_at_0`); the start-date
      adjustment at 0; the joint cash refund whose first life is issued at 119 and its
      second at 0, income at policy month 24 after premiums at 0 and 13, the pricing
      guarantee's inline kernel on the second life alone; and the anchor in its last month,
      a frame of one row;
    * accelerations past the age stop, which ``Data`` bounds from below alone, on the
      twin of S point 14, issued at 60, whose stop is policy month 720: exercised at 1,447,
      the first policy month past ``k``'s cache, and at ``2**53 - 1``, the largest month
      ``Data`` accepts, each projecting its 720 months, ``accel_cost()`` 0 without reading
      the survival at the exercise; issued at 0 and exercised at 1,441, a month past its
      stop, its frame 1,440; and exercised at its stop, 720, the survival read five months
      past it (M24);

    under the reference rate's change switched on (:data:`SWITCHED_ON`).
    """
    advance = {"issue_age": 0, "income_start_mth": 1440, "timing": "advance"}
    return [
        ("the longest covers", *_case_rows(
            (3, {"issue_age": 0}), (3, {"issue_age": 0, "duration_mth": -120}),
            (5, {"issue_age": 0, "duration_mth": -120}),
            (5, {**advance, "duration_mth": -120})), FROM_AGE_0, SWITCHED_ON,
         [1440, 1560, 1560, 1561]),
        ("options and lives at 0", *_case_rows(
            (5, {**advance, "accel_mth": 1440}),
            (7, {"issue_age": 0, "income_start_mth": 1320}),
            (8, {"issue_age": 0, "joint_age": 0, "frequency": 4, "timing": "advance",
                 "cola_rate": 0.03}),
            (16, {"issue_age": 0, "issue_year": 1990})), FROM_AGE_0, SWITCHED_ON,
         [1441, 1440, 1440, 1440]),
        ("the edges", *_case_rows(
            (1, {"issue_age": 0}), (13, {"issue_age": 0}),
            (8, {"issue_age": 119, "joint_age": 0, "income_start_mth": 24},
             ((0, 100000.0), (13, 50000.0))), (25, {})),
         {**FROM_AGE_0, **_factor_keys_at_0()}, SWITCHED_ON, [1440, 1440, 1440, 1]),
        ("accelerations past the age stop", *_case_rows(
            (14, {"accel_mth": 1447}), (14, {"accel_mth": 2**53 - 1}),
            (14, {"issue_age": 0, "accel_mth": 1441}), (14, {"accel_mth": 720})),
         FROM_AGE_0, SWITCHED_ON, [720, 720, 1440, 720]),
    ]


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_contract_extremes(
        sec_build, tmp_path):
    """C4 where the caches end: the contract's longest frames, its youngest issue age and
    its latest income start month and guarantee end.

    The points of :func:`_contract_extremes` read every cache keyed by ``t``, ``k``,
    ``y`` and ``x`` as far as ``spec_sec.py`` sizes it, on age tables extended to age 0
    with a value of their own at every age and sex, so that a compiled read of the key
    beside the right one changes a number the comparison sees.  Frames are asserted first,
    in modelx.  modelx then sweeps each point fully, with :func:`_dia_c4_also`'s calls,
    and the compiled model must agree everywhere, every raise included.  A cache one too
    small for the contract raises ``IndexError`` compiled where modelx reads on, and
    fails here, though the spec check passes it, which holds the caches to the spec and
    not the spec to the contract.
    """
    build = sec_build(SEC)
    found = []
    for i, (case, rows, premiums, edits, refs, frames) in enumerate(_contract_extremes()):
        folder = compiled_case(build, tmp_path / f"x{i}", model_points=rows,
                               edits={**edits, SCHEDULE: premiums})
        assert _frames(folder, "extremes", refs) == frames, case
        found += [f"{case}: {line}" for line in compiled_mismatches(
            build, folder, refs=refs, also=_dia_c4_also)]
        shutil.rmtree(tmp_path / f"x{i}")
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_where_the_cap_binds(spliced,
                                                                              sec_build,
                                                                              tmp_path):
    """C4 where ``mort_rate_py`` caps the annual rate at 1, and where a NaN meets the cap
    and the checks.

    The cap, ``min(mort_ae_factor * q, 1.0)``, binds inside the frame on the points of
    :data:`CAPPED`, on the splice's inputs: the joint annuitant of S point 8 at 117, the
    male life of variant 18 on the table basis, and omega inside variant 30's 30-year
    guarantee.  Their twins and their rows restated in force the month before the cap are
    the splice's own (``events``), read under :data:`SEC_REFS`.  First, in modelx, each
    must reach a rate of the float 1.0 and hold it to the end of its frame, the branch on
    which the cap is already reached; then modelx sweeps them, with :func:`_dia_c4_also`'s
    calls, and the compiled model must agree everywhere.

    And the committed twins of S points 1, 8 and 15 under an A/E of NaN, a Reference set
    before the model computes, which the compiled model reads as modelx does, so that a
    NaN reaches the cap compiled: ``min`` keeps its first argument there, and each check
    fails on the NaN residual (``test_a_residual_that_is_not_a_number_fails_its_check``),
    the period certain commuted in full failing all four.  First, in modelx, the rate in
    the first month is NaN and the checks are ``False``; then C4 holds the compiled NaN
    and every verdict to modelx's in every cell it reaches.
    """
    build = sec_build(SEC)
    inputs = spliced[3].parent
    events = pd.read_csv(inputs / TABLE, index_col="point_id")
    labels = [*CAPPED, *(_label(events, "derived", p, month)
                         for p, (_, _, month) in CAPPED.items())]
    lives = [life for life, *_ in CAPPED.values()] * 2
    schedule = pd.read_csv(inputs / SCHEDULE)
    edits = {file: _copied(inputs, file) for file in SPLICED_EDITS}
    folder = compiled_case(build, tmp_path / "capped", model_points=events.loc[labels],
                           edits={**edits, SCHEDULE: schedule[schedule["point_id"].isin(
                               labels)]})
    model = _read(folder, "capped", SEC_REFS)
    try:
        for key, life in zip(point_keys(model), lives, strict=True):
            p = projection(model, key)
            capped = [t for t in range(p.proj_len()) if p.mort_rate(t, life) == 1.0]
            assert capped == list(range(capped[0], p.proj_len())), key
            assert type(p.mort_rate(capped[-1], life)) is float, key
    finally:
        model.close()
    found = compiled_mismatches(build, folder, refs=SEC_REFS, also=_dia_c4_also)
    nan = {"mort_ae_factor": NAN}
    folder = compiled_case(build, tmp_path / "nan",
                           model_points=_committed().loc[[1, 8, 15]],
                           edits={SCHEDULE: _committed_schedule().query(
                               "point_id in (1, 8, 15)")})
    model = _read(folder, "nan_cap", nan)
    try:
        for key in point_keys(model):
            p = projection(model, key)
            assert math.isnan(p.mort_rate(p.t_entry(), 1)), key
            assert p.check_lives_roll_fwd() is False, key
        assert not any(projection(model, point_keys(model)[2]).cells[check]()
                       for check in CHECKS)
    finally:
        model.close()
    found += compiled_mismatches(build, folder, refs=nan, also=_dia_c4_also)
    assert not found, _mismatch_lines(found)


# The reference rate's change, as (the column on the point in force, the Reference), at
# which its floor at 0 binds on the whole change: a fall before the valuation date that a
# rise at it only part offsets, and a rise before it that a fall at it more than offsets.
# Neither part alone is below 0 in both, so a floor on each part fails.
FLOORS = ((-0.01, 0.005), (-0.005, 0.0025), (0.0025, -0.005))


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_where_the_floor_binds(
        sec_build, tmp_path):
    """C4 where the commutation rate's floor on the reference rate's change binds.

    The commutation discount rate is ``i_p + max(0, ref_rate_shift_init() +
    ref_rate_shift) + m_c``, the floor on the whole change since issue, column and
    Reference added first (§7.9, *Record -- M11*), and neither the grid, whose change is a
    rise, nor the committed points, at no change, bind it.  So S point 15's period certain
    is restated in force at its income start month, 240, by the generator, commuting at
    252, and read at each case of :data:`FLOORS`, a column and a Reference of opposite
    signs whose sum is below 0: first, in modelx, the rate in the commutation month is
    ``i_p + m_c``, 5.25%, the floor binding, and the commuted value S's on its shipped
    rate; then C4 holds the compiled model to modelx everywhere.
    """
    build = sec_build(SEC)
    s = _read(model_path(TWIN), "s_floor")
    try:
        spec = dataclasses.replace(SPEC, derived=((15, 240),), future=())
        table, companions = build_sec_table(spec, s)
        want = _point(s, 15).commuted_value(252)
    finally:
        s.close()
    table = table.set_index("point_id")
    label = _label(table, "derived", 15, 240)
    schedule = companions[SCHEDULE]
    found = []
    for i, (change, shift) in enumerate(FLOORS):
        rows = _set("ref_rate_shift_init", [label], change)(table.loc[[label]])
        folder = compiled_case(build, tmp_path / f"floor{i}", model_points=rows,
                               edits={SCHEDULE: schedule[schedule["point_id"] == label]})
        refs = {"ref_rate_shift": shift}
        model = _read(folder, "floor", refs)
        try:
            p = projection(model, point_keys(model)[0])
            assert change + shift < 0.0 and max(change, shift) > 0.0
            assert p.commute_disc_rate(12) == pytest.approx(0.0525, rel=1e-12)
            assert p.commuted_value(12) == pytest.approx(want, rel=1e-12)
        finally:
            model.close()
        found += [f"{change}, {shift}: {line}" for line in compiled_mismatches(
            build, folder, refs=refs, also=_dia_c4_also)]
    assert not found, _mismatch_lines(found)


# The columns the model reads by value that a spreadsheet may save as floats: the table's
# whole numbers, the purchase rounding and the option months being floats already, their
# blanks NaN.
FLOAT_COLUMNS = ("duration_mth", "issue_age", "certain_period", "income_start_mth",
                 "frequency", "issue_year")


def _as_floats(columns):
    """An edit that writes ``columns`` as floats."""
    return lambda df: df.assign(**{c: df[c].astype(float) for c in columns})


@pytest.mark.cython
def test_the_compiled_model_reads_keys_written_as_floats_as_modelx_does(sec_build,
                                                                         tmp_path):
    """C4 on keys written as floats: the compiled model reads 60.0 as 60, as modelx does.

    The committed table with its labels written ``1.0`` to ``26.0``, and its whole
    numbers written as floats, as a spreadsheet can save them (:data:`FLOAT_COLUMNS`); its
    premium schedule's labels and months as floats; and the four assumption tables' keys
    as floats (:data:`FLOAT_KEYS`).  ``Data`` reads each by value, so first, in seconds,
    modelx's ``Data`` on the floats is held to its ``Data`` on the same rows as written:
    every array of the same dtype and values, and every check of the same type, so that a
    key read as a float fails here, naming its cell, and not in the compiled sweep.  Then
    modelx sweeps every point (:func:`_dia_c4_also`), and the compiled model must agree
    everywhere, every ``Data`` array included, in dtype and shape.
    """
    build = sec_build(SEC)
    rows = _committed()
    as_written = _read(_sec_inputs(tmp_path / "ints", rows), "keys_ints")
    floats = _as_floats(FLOAT_COLUMNS)(rows)
    floats.index = pd.Index(rows.index.astype(float), name="point_id")
    schedule = _as_floats(("point_id", "premium_mth"))(_committed_schedule())
    folder = compiled_case(build, tmp_path / "floats", model_points=floats,
                           edits={**FLOAT_KEYS, SCHEDULE: schedule})
    written = pd.read_csv(folder.parent / TABLE)
    assert all(written[c].dtype == float for c in ("point_id", *FLOAT_COLUMNS))
    assert all(pd.read_csv(folder.parent / SCHEDULE)[c].dtype == float
               for c in ("point_id", "premium_mth"))
    model = _read(folder, "keys_floats")
    try:
        apart = []
        for name, cells in as_written.Data.cells.items():
            if cells.parameters or name in READERS:
                continue
            want, got = cells(), model.Data.cells[name]()
            if isinstance(want, np.ndarray):
                if not (isinstance(got, np.ndarray) and got.dtype == want.dtype
                        and np.array_equal(got, want, equal_nan=want.dtype.kind == "f")):
                    apart.append(f"{name}: {getattr(got, 'dtype', type(got))}")
            elif type(got) is not type(want) or got != want:
                apart.append(f"{name}: {got!r}, not {want!r}")
        assert not apart, apart
    finally:
        model.close()
        as_written.close()
    found = compiled_mismatches(build, folder, also=_dia_c4_also)
    assert not found, _mismatch_lines(found)


# A single life's joint_sex as no projection reads it, as (case, the rows): numbers, which
# pandas reads as ints, and a blank beside a text, which it reads as an object column.
LABELS_NOT_TEXT = [("numbers", ((1, {"joint_sex": 7}), (3, {"joint_sex": 8}))),
                   ("a blank and a text",
                    ((1, {"joint_sex": NAN}), (3, {"joint_sex": "M"})))]


@pytest.mark.cython
def test_the_compiled_model_returns_a_label_that_is_not_text_as_modelx_does(sec_build,
                                                                             tmp_path):
    """C4 on a label that is not text: compiled, ``sex(2)`` returns what modelx returns.

    ``sex(life)`` returns its column as read, and ``Data`` checks ``joint_sex`` on a joint
    contract alone, so a single life's may be a number, which pandas reads as an int, or a
    blank, NaN.  An accessor typed ``str`` would raise ``TypeError`` compiled; the sample
    types ``sex`` on a blank copy as a Python object (sample_sec.py).  So on the anchor's
    twin and the cash refund on computed factors, each case of :data:`LABELS_NOT_TEXT`:
    after checking, in modelx, that each label is the int, the NaN or the text the file
    holds, modelx sweeps both points, each life's ``sex`` with them
    (:func:`_dia_c4_also`), and the compiled model must agree everywhere, the label and
    its type included.
    """
    build = sec_build(SEC)
    found = []
    for i, (case, rows) in enumerate(LABELS_NOT_TEXT):
        table, premiums = _case_rows(*rows)
        folder = compiled_case(build, tmp_path / f"labels{i}", model_points=table,
                               edits={SCHEDULE: premiums})
        model = _read(folder, "labels")
        try:
            labels = [projection(model, key).sex(2) for key in point_keys(model)]
        finally:
            model.close()
        if case == "numbers":
            assert labels == [7, 8] and all(isinstance(x, (int, np.integer))
                                            for x in labels), labels
        else:
            assert math.isnan(labels[0]) and labels[1] == "M", labels
        found += [f"{case}: {line}" for line in compiled_mismatches(
            build, folder, also=_dia_c4_also)]
    assert not found, _mismatch_lines(found)


# The compiled model's own refusals: what it does with a key past the caches spec_sec.py
# sizes, which no projection the contract allows reaches, as (cell, arguments, what modelx
# does, "{label}" standing for the point's label).  modelx answers a month outside the
# frame, a policy month or a policy year past the contract's, with a number, as the cells
# say, and refuses a code past the timing, the kind and the basis, a life past the two and
# an age outside the mortality table by name; compiled, each is past a cache, and raises
# IndexError rather than read or write beyond it.  Every 2-D cache after its first
# dimension is three wide (spec_sec.py), so the first code or life past it is 3.
_NO_RATE = ("ValueError: point_id {label}: mort_table.csv has no mort_rate at attained "
            "age {x} for the sex of life 1")
COMPILED_ONLY = [
    ("net_cf", (1563,), ("ok", None)),
    ("net_cf", (-1,), ("ok", None)),
    ("claim_pp", (0, 3), ("raised", "ValueError: invalid kind")),
    ("claims", (0, 3), ("raised", "ValueError: invalid kind")),
    ("pols_if_at", (0, 3), ("raised", "ValueError: invalid timing")),
    ("lives_if", (13, 3), ("raised", "ValueError: invalid life")),
    ("lives_if_init", (3,), ("raised", "ValueError: invalid life")),
    ("annuity_factor_at", (240, 3), ("raised", "ValueError: invalid basis")),
    ("lives_if_pm", (1447, 1), ("ok", None)),
    ("cum_annuity_pp", (1447,), ("ok", None)),
    ("lives_if_ann", (123,), ("ok", None)),
    ("mort_rate_base_at", (121, 1), ("raised", _NO_RATE.replace("{x}", "121"))),
    ("mort_rate_base_at", (-1, 1), ("raised", _NO_RATE.replace("{x}", "-1"))),
]

# The codes and lives inside the caches that a cell does not take: there the cell itself
# refuses it, compiled as in modelx.  As (cell, its arguments), on the extract's first row,
# the joint point issued 13 months on, whose survival opens at t = 13: the total, ALL, 2,
# where claim_pp takes a kind; a timing of 2; and a life of 0.
CODES_IN_CACHE = [
    ("claim_pp", (13, 2)), ("pols_if_at", (13, 2)), ("lives_if_init", (0,)),
    ("age_at_entry", (0,)), ("mort_schedule", (0,)), ("improvement_schedule", (0,)),
    ("lives_if", (13, 0)), ("lives_if_pm", (12, 0)), ("mort_rate_base_at", (70, 0)),
    ("improvement_rate_at", (70, 0)),
]

# What a direct call refuses on a point that projects, on the extract (_relabelled), as
# (label, cell, arguments): a single life's second issue age, and each age reader below
# its table's first age.
DIRECT = [(103, "age_at_entry", (2,)), (108, "mort_rate_base_at", (19, 1)),
          (108, "improvement_rate_at", (19, 2))]


def _labels_moved(schedule):
    """The premium schedule of :func:`_relabelled`'s extract, each premium under its
    point's new label, where its label is a number; a text, or a column dropped, as it is.
    """
    if "point_id" not in schedule:
        return schedule
    labels = [p + 100 if isinstance(p, (int, float)) and p == p else p
              for p in schedule["point_id"].astype(object)]
    return schedule.assign(point_id=labels)


def _refusal_cases():
    """Every refusal the compiled model must make as modelx does, as (case, the table,
    its premiums, the edits, the References, [(position, cell, arguments)], the Data
    cells to read).

    Each table is an extract, labelled otherwise than by position (:func:`_relabelled`),
    with its premium schedule relabelled with it, so that a refusal naming a point by
    ``idx + 1`` names another.  A position, not a label, since a table ``Data`` refuses has
    no keys to give: each is the row's place in the table written, ``Projection``'s
    ``idx``, which the test indexes ``Projection`` by in modelx too.
    """
    committed, schedule = _committed(), _committed_schedule()
    premiums = _labels_moved(schedule)

    def at(table, label):
        return list(table.index).index(label)

    def extract(edit=None):
        return _relabelled(edit(committed) if edit is not None else committed)

    cases = []
    for case, edit, _ in MALFORMED:
        cases.append((case, extract(edit), premiums, None, {}, [(0, "result_cf", ())],
                      ("model_point_table",)))
    for case, edit, _ in SCHEDULES:
        cases.append((case, extract(), _labels_moved(edit(schedule)), None, {},
                      [(0, "result_cf", ())], ("premium_schedule_table",)))
    for case, file, edit, _ in TABLES:
        reader, count, point = TABLE_READERS[file]
        table = extract()
        cases.append((case, table, premiums, {file: edit}, {},
                      [(at(table, point + 100), "result_cf", ())], (count,)))
    for case, point, edit, _ in REFUSED:
        table = extract(edit)
        cases.append((case, table, premiums, None, {},
                      [(at(table, point + 100), "result_cf", ())], ()))
    for case, edit, label, _, refs, *_ in NOT_ISSUED:
        table = extract(edit)
        cases.append((case, table, premiums, None, refs,
                      [(at(table, label + 100), cell, ()) for cell in ("result_cf",
                                                                       "stop_mth")], ()))
    for case, edit, point, cell, _ in UNDECODABLE:
        table = extract(edit)
        cases.append((case, table, premiums, None, {},
                      [(at(table, point + 100), cell, ())], ()))
    for column, call, values in DECODES:
        edit = _both(*(_set(column, [point], value) for point, value in values.items()))
        table = extract(edit)
        cases.append((f"{column} in another case or spaced", table, premiums, None, {},
                      [(at(table, point + 100), call, ()) for point in values], ()))
    table = _relabelled(_not_decodable_table())
    calls = []
    for _, _, point, _, is_refused, cell, args, _ in NOT_DECODABLE:
        calls += [(at(table, point + 100), "result_cf", ())] if is_refused else []
        calls += [(at(table, point + 100), cell, args)]
    cases.append(("values a point cannot use", table, premiums, None, {}, calls, ()))
    table = extract()
    zero = pd.concat([premiums[premiums["point_id"] != 101], _labels_moved(_premiums(
        (1, 0, 100000.0), (1, 12, 0.0), (1, 60, 50000.0)))], ignore_index=True)
    cases.append(("a zero premium at a ROP key the table lacks", table, zero, None, {},
                  [(at(table, 101), "guarantee_mths_pricing", ())], ()))
    table = extract(_set("issue_age", [1], 61))
    cases.append(("a payout key the table lacks", table, premiums, None, {},
                  [(at(table, 101), "result_cf", ())], ()))
    table = extract()
    cases.append(("codes and lives no cell takes, inside the caches", table, premiums,
                  None, {}, [(0, cell, args) for cell, args in CODES_IN_CACHE]
                  + [(at(table, label), cell, args) for label, cell, args in DIRECT], ()))
    table = extract()
    cases.append(("a sex the mortality table lacks", table, premiums,
                  {"mort_table.csv": lambda df: df[df["sex"] == "M"]}, {},
                  [(at(table, 108), "result_cf", ())], ()))
    table = extract()
    table.index = pd.Index([*table.index[:-1], "1x"], name="point_id")
    cases.append(("a label written as text", table,
                  premiums[premiums["point_id"] != 101], None, {},
                  [(len(table) - 1, "point_id", ())], ("point_id",)))
    return cases


# The compiled model's refusal under a Reference moved from its shipped value: below an
# A/E of 1 accel_cost reads the pricing survival at an exercise past the age stop, as S
# does, and from policy month 1,442 that is past the k cache (accel_cost).
BELOW_ONE = "compiled only, below an A/E of 1"


def _s_accel_cost(folder, month, ae):
    """``DIA_US_S``'s ``accel_cost()`` on its point 14 exercising at ``month``, read at
    ``mort_ae_factor`` ``ae``."""
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    due = pd.read_csv(model_path(TWIN).parent / "premium_schedule.csv")
    inputs = temp_inputs(folder, model_path(TWIN),
                         model_points=s_table.loc[[14]].assign(accel_mth=month),
                         edits={"premium_schedule.csv": due[due["point_id"] == 14]})
    model = _read(inputs, "s_late", {"mort_ae_factor": ae})
    try:
        return _point(model, 14).accel_cost()
    finally:
        model.close()


@pytest.mark.cython
def test_the_compiled_model_refuses_what_modelx_refuses(sec_build, tmp_path):
    """Compiled, the model refuses what modelx refuses, with modelx's error and message.

    A ``ValueError`` raised in a cell typed ``long long`` or ``double`` propagates out of
    the compiled model as out of modelx.  So, each on its own inputs and References
    (:func:`_refusal_cases`), on an extract labelled otherwise than by position: every
    case of :data:`MALFORMED`, of :data:`SCHEDULES` and of :data:`TABLES`, refused by a
    projection and by the ``Data`` cell that checks the table, so that a compiled ``Data``
    cell refuses each value its modelx cell refuses; every case of :data:`REFUSED`, a
    point owing nothing, of :data:`NOT_ISSUED`, a point the contract does not issue, by
    ``result_cf`` and ``stop_mth``, of :data:`UNDECODABLE` and of :data:`DECODES`, each
    value S names in another case and spaced, and of :data:`NOT_DECODABLE`, by the
    point's projection and by its accessor's direct call; a premium of 0.0 at a ROP key
    the table lacks, and a payout key it lacks; a sex the mortality table lacks, schedule
    0, refused at the first age read; a label written as text, by ``Data.point_id``; a
    code or a life a cell does not take, inside its cache (:data:`CODES_IN_CACHE`); and the
    direct calls of :data:`DIRECT`.

    And the refusals that are the compiled model's alone (:data:`COMPILED_ONLY`): a month
    past the ``t`` cache either side, a code past the timing, kind and basis caches, a
    life past the life caches, a policy month past the ``k`` cache, a policy year past
    the ``y`` cache and an age past the ``x`` cache either side, each raising
    ``IndexError`` compiled, beside what modelx does.  And one a Reference moved from its
    shipped value reaches (:data:`BELOW_ONE`): with ``mort_ae_factor`` at
    :data:`BELOW_ONE_AE`, set before the model computes anything (K7), ``accel_cost()``
    on the anchor exercising at policy month 1,442 raises ``IndexError`` compiled, where
    modelx gives ``DIA_US_S``'s cost to the last bit, and at 1,441, inside the cache,
    computes modelx's number.

    The cases share one directory, which each case's inputs overwrite in turn, and one
    copy of the compiled package: each child reads its inputs afresh, as the compiled
    ``Data`` reads its files once an import.
    """
    build = sec_build(SEC)
    cases = _refusal_cases()
    first = _relabelled(_committed()).index[0]
    cases.append(("compiled only", _relabelled(_committed()),
                  _labels_moved(_committed_schedule()), None, {},
                  [(0, cell, args) for cell, args, _ in COMPILED_ONLY], ()))
    late = _relabelled(_both(_set("accel_mth", [10], 1441),
                             _set("accel_mth", [14], 1442))(_committed()))
    at = list(late.index)
    cases.append((BELOW_ONE, late, _labels_moved(_committed_schedule()), None,
                  {"mort_ae_factor": BELOW_ONE_AE},
                  [(at.index(110), "accel_cost", ()), (at.index(114), "accel_cost", ())],
                  ()))
    s_cost = _s_accel_cost(tmp_path / "s", 1442, BELOW_ONE_AE)
    dest = tmp_path / "refused"
    folder = compiled_case(build, dest)
    found, refused, only = [], 0, iter(COMPILED_ONLY)
    for case, table, premiums, edits, refs, calls, data in cases:
        temp_inputs(dest, model_path(SEC), model_points=table, model_point_file=TABLE,
                    edits={**(edits or {}), SCHEDULE: premiums})
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
            status, text = next(have[idx])
            where = f"{case}: idx {idx}: {cell}{args}"
            if case == BELOW_ONE:
                if modelx_did[0] != "ok" or type(modelx_did[1]) is not float:
                    found.append(f"{where}: modelx {modelx_did}, not a number")
                elif idx == at.index(110):
                    if (status, text) != modelx_did and not (
                            status == "ok" and _as_modelx(text, modelx_did[1])):
                        found.append(f"{where}: compiled {status} {text!r}, modelx "
                                     f"{modelx_did}")
                else:
                    if modelx_did[1].hex() != s_cost.hex():
                        found.append(f"{where}: modelx {modelx_did[1]!r}, S {s_cost!r}")
                    if (status, str(text).split(":")[0]) != ("raised", "IndexError"):
                        found.append(f"{where}: compiled {status} {text!r}, not "
                                     f"IndexError")
                continue
            if case == "compiled only":
                *_, (does, what) = next(only)
                if what is not None:
                    what = what.replace("{label}", str(first))
                if modelx_did[0] != does or what is not None and modelx_did[1] != what:
                    found.append(f"{where}: modelx {modelx_did}, not {(does, what)}")
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
    assert refused == sum(len(calls) + len(data) for *_, calls, data in cases[:-2])
    assert s_cost > 0.0


@pytest.mark.cython
def test_the_compiled_all_total_keeps_s_sign_of_zero(sec_build, tmp_path):
    """Compiled, ``claims(t, ALL)`` is ``DIA_US_S``'s ``claims(t)`` with its sign of zero.

    C4 compares numbers, and ``-0.0 == 0.0``, so a compiled total begun at ``0.0`` would
    pass it; :func:`test_the_all_total_is_s_total_with_its_sign_of_zero` holds modelx to
    S's bits.  Here the compiled model is: on the twin of S point 4 at ``mort_ae_factor``
    :data:`NEGATIVE_AE`, set before it computes, every month's ``claims(t, ALL)`` and
    ``liability_outgo(t)`` are S's by ``float.hex``, ``-0.0`` in most months.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "negzero")
    refs = {"mort_ae_factor": NEGATIVE_AE}
    s = _read(model_path(TWIN), "s_negzero_c", refs)
    try:
        theirs = _point(s, 4)
        months = range(theirs.proj_len())
        want = [theirs.claims(t).hex() for t in months]
        want += [theirs.liability_outgo(t).hex() for t in months]
    finally:
        s.close()
    total = _references("Projection")["ALL"]
    position = list(_committed().index).index(4)
    calls = [("claims", (t, total)) for t in months]
    calls += [("liability_outgo", (t,)) for t in months]
    got = run_compiled(folder.parent, build.package.name,
                       {"refs": refs, "calls": {position: calls}})
    assert got["exit"] == 0, got["stderr"]
    have = [value.hex() if status == "ok" and type(value) is float else (status, value)
            for status, value in got["values"][position]]
    assert sum(h == "-0x0.0p+0" for h in have) > len(months) // 2
    assert have == want, [(c, h, w) for c, h, w in zip(calls, have, want) if h != w][:10]


def _deepest_rows():
    """The four points the stack test runs cold, each at the contract's longest cover from
    issue age 0, and their premiums: the cash refund on computed factors, issued at the
    valuation date and 120 months on, 1,440 months of cover each, the deepest chain the
    contract allows; the installment refund 120 months on; and the installment refund in
    advance from policy month 1,440, 120 months on, whose stop rule is 1,441."""
    return _case_rows((3, {"issue_age": 0}), (3, {"issue_age": 0, "duration_mth": -120}),
                      (5, {"issue_age": 0, "duration_mth": -120}),
                      (5, {"issue_age": 0, "duration_mth": -120, "income_start_mth": 1440,
                           "timing": "advance"}))


# The cold call the stack test makes compiled, in a thread whose stack is reserved at each
# of these sizes in KiB, and then on the main thread.  1 MiB is the size asserted; the
# others bracket what the call needs, and the test reports the smallest that ran.
STACK_KIB = (256, 320, 384, 448, 512, 640, 768, 1024, 2048)

# How long the stack test waits for each child, in seconds: one runs in a few seconds, more
# under load.  A bracketing size may kill its child on a stack overflow by design, and
# where the overflow hangs instead, as Windows Error Reporting could, the wait ends sooner
# than for the two runs asserted, and the size is recorded as timed out.
BRACKET_TIMEOUT, ASSERTED_TIMEOUT = 120, 300


@pytest.mark.cython
def test_the_longest_cover_runs_cold_on_a_one_megabyte_stack(sec_build, tmp_path):
    """The deepest call the contract allows runs compiled on a 1 MiB stack (F7).

    On the four points of :func:`_deepest_rows`, a cold ``net_cf`` in the last month runs
    each life's survival, one cell a month from the end of the cover back to
    ``t_entry()``, 1,440 months from issue age 0, and 1,441 on the installment refund in
    advance, 1,446 to 1,451 cells deep in modelx on a model just read
    (:func:`test_the_deepest_cold_call_runs_one_cell_a_month`), the longest chains the
    contract allows.  Compiled it runs on the C stack, which the interpreter's recursion
    limit does not count.  1 MiB is the stack MSVC gives an executable's main thread
    unless the executable asks for more: a host that embeds Python, where python.exe
    itself asks for 2,000,000 bytes.  A thread whose stack is reserved at 1 MiB stands in
    for it on every platform (``sec_support.run_compiled``), and in one each call runs cold
    and returns modelx's number, identically on x86-64 (``sec_support.exact_here``) and to
    1e-12 elsewhere.  With MSVC 14.37 the calls needed between 320 and 384 KiB on the
    machine they were measured on, about 224 bytes a level and about 36 KiB fixed, about
    354 KiB at 1,451 levels, 2.9 times under 1 MiB (measured at M24).  gcc's need comes
    from the ``cython`` job's Linux leg, whose warning records it: on ``SPIA_US_SEC``'s
    chain, as long, it ran on 768 KiB and not on 640, about twice MSVC's bytes a level,
    which would put this chain at about 610 to 770 KiB, 1.3 times under 1 MiB at the
    least, an estimate the leg's warning replaces.  A stack too small kills the child,
    and the test fails naming the stack.  The thread's stack is read back too, from
    Windows or from glibc, and must be at most 1 MiB and a page: a stand-in larger than
    asked for would stand for nothing.  And the calls run again on the child's main
    thread, which is what ``run_sec.py --cython`` runs on.

    The calls run first at each size of :data:`STACK_KIB`, before anything is asserted,
    and every size's outcome goes into a warning, which the job's summary shows, and into
    the failure, if there is one: the smallest size that ran bounds the stack the chain
    needs on the compiler at hand.  A size below the need kills its child on a stack
    overflow, by design.  Each bracketing child is waited for :data:`BRACKET_TIMEOUT`
    seconds and the two asserted runs :data:`ASSERTED_TIMEOUT`, so that an overflow that
    hangs, rather than ends its child, costs minutes, not the job's hour, and a bracketing
    size that timed out is recorded as such.
    """
    build = sec_build(SEC)
    rows, premiums = _deepest_rows()
    folder = compiled_case(build, tmp_path / "longest", model_points=rows,
                           edits={**FROM_AGE_0, SCHEDULE: premiums})
    model = _read(folder, "longest")
    try:
        calls, want = {}, {}
        for key, cover in zip(point_keys(model), (1440, 1440, 1440, 1441), strict=True):
            proj = projection(model, key)
            last = proj.proj_len() - 1
            assert proj.duration_mth(last) == cover - 1, key
            calls[key] = [("net_cf", (last,))]
            want[key] = proj.net_cf(last)
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
# expenses(12), before expense_maint is set to 90.0 and after.
STALE_CHILD = """\\
import json, sys
sys.path.insert(0, sys.argv[1])
model = __import__(sys.argv[2]).mx_model
p = model.Projection
early = p[3]
values = [p.expenses(12), early.expenses(12)]
p.expense_maint = 90.0
values += [p.expenses(12), early.expenses(12), p[18].expenses(12)]
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
    moves ``expenses(12)`` on every point on the books then: the base ``Projection``, the
    anchor's twin at ``idx`` 0, the twin of S point 4, made before, and the anchor in
    payment a month, made after, so that a modelx-cython that began to clear caches would
    be seen here, and the advice changed with it.  A compiled value meets modelx's as C4
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
                 projection(model, 18).expenses(12))
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
    modelx's: point 19's description, the anchor a month into its income phase, and its
    first fifteen rows of cash flows and of counts, survival and payment factors, and the
    block's lines for each point, its first fifteen rows and its first twelve projection
    years.

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
    done = _run_sec(runner, "19", "--cython", "--build", str(empty), check=False)
    stderr = done.stderr.decode(errors="replace")
    assert done.returncode != 0 and done.stdout == b"", stderr
    assert f"holds no build of {SEC} for this interpreter" in stderr, stderr
