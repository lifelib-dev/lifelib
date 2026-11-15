# mx2cy's spec for SPIA_US_SEC: the length of each C-array cache in Projection, by the
# cells' parameters (USLIB-SEC-PLAN.md F4, section 6.1 step 6).  A compiled cache raises
# IndexError for an argument outside [0, size), so each size covers the largest argument
# any cell is called with on a point the contract allows, in its frame and in the month
# after it, t = proj_len(), which lives_if reads and C4's full sweep evaluates every
# monthly cell at; plus one because the index starts at 0; and one of headroom where that
# leaves room.  mx2cy keys a size by a cell's parameter names, so every cell taking t alone
# shares one.  The contract is three Projection References and one of Data's.
# Projection.proj_len refuses a point any of whose covered lives was below issue_age_min,
# 0, at the annuity date, on every form, since SPIA_US_S projects every age from 0 and a
# frame runs to the age stop on its youngest life, whatever the form; and an elected
# certain period above 12 * (omega_age - issue_age_min), 1,440 months, the longest the
# caches below hold; the age stop ends the frame when the youngest life reaches
# omega_age, 120; and Data refuses an annuity commencing more than future_horizon_mth,
# 120 months, after the valuation date.  So no point a report projects outruns these
# sizes, and a change to issue_age_min, omega_age or future_horizon_mth needs them
# recomputed here and the model rebuilt.
#
# t, months from the valuation date.  The longest frame is any form on a youngest life
# of 0, to the age stop, 12 * (120 - 0) = 1,440 months, commencing 120 months on: 1,560
# months, t = 0 .. 1,559, and 1,560 in the month after, where lives_if reads the closing
# time point and C4's sweep evaluates every monthly cell: 1,561, and one of headroom,
# 1,562.  Nothing reads t + 1 at t = proj_len().  A certain period of 1,440 months, the
# longest proj_len admits, ends at the same policy month as the age stop at 0.  In
# general 12 * (omega_age - issue_age_min) + future_horizon_mth + 2.
# timing, beside t in pols_if_at: BEF_NB 0 and BEF_DECR 1; kind, beside t in claim_pp:
# REFUND 0; life, beside t in the per-life monthly cells: 1 and 2.  Every 2-D cache of a
# model has one inner width, the widest, life's 3, because Cython's generated unpickle
# code converts the 2-D caches of a space with one function for each inner width: given
# two widths, it passes the narrower array where the wider is expected, which gcc 14
# refuses (-Wincompatible-pointer-types, made an error on every gcc and clang by
# tools/build_sec_cy.py) and MSVC accepts, and would write past its end.  So (1,562, 3)
# for each.  A timing 2 or a kind 1 or 2 is inside the cache, where the cell refuses it
# as modelx does, ValueError("invalid timing") or ValueError("invalid kind"), and a life
# 0 likewise, ValueError("invalid life"); a code or a life of 3 raises IndexError,
# compiled alone.
# k, a policy month or the time point opening it, from the annuity date: the schedule is
# read at every policy month of the frame, to the stop rule's month less one, 1,439 on a
# youngest life of 0 and on a certain period of 1,440 months; the payments to date, G(k),
# on a cash refund up to the stop rule's month itself, in an advance payment month of the
# last month, and on an installment refund up to horizon_mths, both at most 1,440 from
# issue age 0; the commuted value and the withdrawal's floor inside the certain period
# alone.  So k is at most 12 * (omega_age - issue_age_min) = 1,440, G at the stop month
# in general: 1,441, and one of headroom, 1,442.  In general
# 12 * (omega_age - issue_age_min) + 2.
# y, a policy year, read by annual_income at the schedule's policy months, by
# commute_util_rate inside a certain period, and by surr_charge_rate in every month of the
# frame: 1 .. 120, the policy year of the frame's last month, 1,439, // 12 + 1: 121, and
# one of headroom, 122; omega_age - issue_age_min + 2.
# x, an attained age, read by the two age readers below omega_age alone, from
# issue_age_min: 0 .. 119, since claims weights by the last-death density on every form,
# a certain_only annuity at 0 on the table basis among them: 120, and one of headroom,
# 121; omega_age + 1.
# Beside it life, 3 wide, as every 2-D cache.  A reader's extent check runs before the
# array is read, so an age below a table's first, 40 as shipped, is refused by name.
# life, alone in age_at_entry, death_mth, lives_if_init and the two schedules: 3.
{"spaces": {"Projection": {"cells_param_size": {
    "t": 1562, ("t", "life"): (1562, 3), ("t", "timing"): (1562, 3),
    ("t", "kind"): (1562, 3), "k": 1442, "y": 122, ("x", "life"): (121, 3),
    "life": 3}}}}
