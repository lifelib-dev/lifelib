# mx2cy's spec for DIA_US_SEC: the length of each C-array cache in Projection, by the
# cells' parameters (USLIB-SEC-PLAN.md F4, section 6.1 step 6).  A compiled cache raises
# IndexError for an argument outside [0, size), so each size covers the largest argument
# any cell is called with on a point the contract allows, in its frame and in the month
# after it, t = proj_len(), which lives_if reads and C4's full sweep evaluates every
# monthly cell at; plus one because the index starts at 0; and one of headroom.  mx2cy
# keys a size by a cell's parameter names, so every cell taking t alone shares one.  The
# contract is three Projection References and one of Data's: issue_age_min, 0, asked of
# each covered life on every form, since DIA_US_S projects every form from 0 and a frame
# runs to the age stop on its youngest life; omega_age, 120; accel_months, 6; and
# Data.future_horizon_mth, 120.  Projection.stop_mth refuses, naming the point, an issue
# age of a covered life below issue_age_min, an income start month, at issue or in force,
# past 12 * (omega_age - issue_age_min), 1,440, and a period certain ending past it.  So
# the stop rule ends by policy month 1,441: an installment refund in advance whose income
# starts at the age stop rounds its refund period up to a whole instalment, one month past
# horizon_mths.  And Data refuses a policy issued more than future_horizon_mth months
# after the valuation date.  So no point a report projects outruns these sizes, and a
# change to issue_age_min, omega_age, accel_months or future_horizon_mth needs them
# recomputed here and the model rebuilt, as does Data.premium_last_mth, 12 * (omega_age -
# issue_age_min) - 1, the last month of Data's premium table, which a test holds to it.
#
# t, months from the valuation date.  The longest frame is the stop rule at policy month
# 12 * (120 - 0) + 1 = 1,441, from a policy issued 120 months on: 1,561 months,
# t = 0 .. 1,560, and 1,561 in the month after, where lives_if reads the closing time point
# and C4's sweep evaluates every monthly cell: 1,562, and one of headroom, 1,563.  In
# general 12 * (omega_age - issue_age_min) + future_horizon_mth + 3.
# timing, beside t in pols_if_at: BEF_NB 0 and BEF_DECR 1; kind, beside t in claim_pp and
# claims: DEATH 0, REFUND 1 and ALL 2; life, beside t in the per-life monthly cells: 1 and
# 2.  Every 2-D cache of a model has one inner width, the widest, here 3, because
# Cython's generated unpickle code converts the 2-D caches of a space with one function
# for each inner width: given two widths, it passes the narrower array where the wider is
# expected, which gcc 14 refuses (-Wincompatible-pointer-types, made an error on every gcc
# and clang by tools/build_sec_cy.py) and MSVC accepts, and would write past its end.  So
# (1,563, 3) for each.  A timing 2, a kind beyond the cell's or a life 0 is inside the
# cache, where the cell refuses it as modelx does, ValueError("invalid timing"),
# ValueError("invalid kind") or ValueError("invalid life"); a code or a life of 3 raises
# IndexError, compiled alone.
# k, a policy month or the time point opening it, from issue: the payout schedule, its
# floor and the instalments scheduled to date are read to the stop rule's month less one,
# 1,440, and to horizon_mths, 1,440, and the schedule, its floor and the pricing survival
# five months past an acceleration exercised at the age stop, 1,440 at most, 1,445, as
# accel_cost reads it; the premiums and their pricing at policy months before the income
# start month, and the pricing survival, the start-date adjustment's factors and the
# payout factor at the income start month, 1,440 at most.  Data bounds the exercise month
# from below alone, and a point accelerating past its age stop projects, as DIA_US_S
# projects it: there accel_cost reads the pricing survival a month after the stop alone,
# 1,441 at most, DIA_US_S's survival at every later month when mort_ae_factor is 1 or
# more, and its cost 0 (an A/E below 1 is read on, past the cache from an exercise at
# 1,442, model-sec.md's What it refuses).  So k is at most 1,445: 1,446, and one of
# headroom, 1,447.  In general 12 * (omega_age - issue_age_min) + accel_months + 1.
# life beside k in lives_if_pm, and basis beside it in annuity_factor_at: PURCHASE 0,
# ADJUST_OLD 1 and ADJUST_NEW 2; each 3 wide, the one inner width, (1,447, 3).
# y, a policy year: the annual rates by policy year of the pricing survival to policy
# month 1,445, year 121, and of the projection's mortality to policy month 1,440, year
# 121; the annual display cells to the stop rule's year, 120.  So 122, and one of
# headroom, 123: omega_age - issue_age_min + 3.  life beside y in mort_rate_py and
# mort_rate_mth_py, and kind beside it in claims_ann, each (123, 3).
# x, an attained age, read by the two age readers below omega_age alone, from
# issue_age_min: 0 .. 119, 120, and one of headroom, 121: omega_age + 1.  life beside it,
# (121, 3).  A reader's extent check runs before the array is read, so an age below a
# table's first, 20 as shipped, is refused by name.
# life, alone in age_at_entry, lives_if_init and the two schedules: 3.
{"spaces": {"Projection": {"cells_param_size": {
    "t": 1563, ("t", "life"): (1563, 3), ("t", "timing"): (1563, 3),
    ("t", "kind"): (1563, 3), "k": 1447, ("k", "life"): (1447, 3),
    ("k", "basis"): (1447, 3), "y": 123, ("y", "life"): (123, 3),
    ("y", "kind"): (123, 3), ("x", "life"): (121, 3), "life": 3}}}}
