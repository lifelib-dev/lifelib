# mx2cy's spec for VUL_US_SEC: the length of each C-array cache in Projection, by the cells'
# parameters (USLIB-SEC-PLAN.md F4, section 6.1 step 6).  A compiled cache raises
# IndexError for an argument outside [0, size), so each size covers the largest argument
# any cell is called with on a point the contract allows, in its frame and in the month
# after it, t = proj_len(), which the roll-forwards read and C4's full sweep evaluates
# every monthly cell at; plus one because the index starts at 0; and one of headroom where
# that leaves room.  mx2cy keys a size by a cell's parameter names, so every cell taking t
# alone shares one.  The contract is four References and one of Data's.
# Projection.proj_len refuses a point issued below issue_age_min, 0, or above
# issue_age_max, 85, the issue ages product-spec.md admits, one issued above omega_age,
# 121, and a lineup of more than subaccount_max, 9, subaccounts; the projection ends at
# omega_age + 1, attained age 122; and Data refuses a point issued more than
# future_horizon_mth, 120 months, after the valuation date.  So no point a report projects
# outruns these sizes, and a change to any of issue_age_min, omega_age, subaccount_max and
# future_horizon_mth needs them recomputed here and the model rebuilt; issue_age_max sizes
# nothing, since every size rests on the youngest issue age.
#
# t, months from the valuation date.  The longest frame is a policy issued at 0, to the
# end of the projection at 122, 122 policy years, and issued 120 months on:
# 12 * (121 - 0 + 1) + 120 = 1,584 months, t = 0 .. 1,583, and 1,584 in the month after,
# which the roll-forwards read: 1,585, and one of headroom, 1,586.  av_change and the
# three residuals read t + 1 only in cover, and the pricing path is not read outside it,
# so nothing reads 1,585.  A longer future_horizon_mth, a higher omega_age or a lower
# issue_age_min needs t raised to 12 * (omega_age - issue_age_min + 1) + the horizon + 2.
# Data.return_horizon_mth, the last month Data's return array holds, is t's last index,
# 1,585, so that the array is no larger than the months a frame reads: it is raised with t.
# m, the pricing path's policy month from issue (age_pricing, policy_year_pricing,
# prem_pricing_pp, db_pricing_pp, naar_pricing_pp, mth_deduction_pricing_pp,
# fa_pricing_pp, av_pricing_pp, sa_pricing_pp and the three _at cells): funding_ratio
# reads the path at duration_mth(t) in cover alone, at most 12 * 122 - 1 = 1,463 at issue
# age 0, wherever the valuation date falls: 1,464, and one of headroom, 1,465.  A higher
# omega_age or a lower issue_age_min needs m raised to
# 12 * (omega_age - issue_age_min + 1) + 1.
# The one width, 9: timing's nine codes, BEF_NB 0 to EOM 8, one numbering for the count's
# three timings and the account value's six; the kinds, DEATH 0 to WITHDRAWAL 3; and the
# subaccounts' positions, 0 to subaccount_max - 1, 8.  Every dimension after the first is
# that width: (1,586, 9) beside t in the cells of a timing, a kind or a subaccount,
# (1,586, 9, 9) beside t in sa_pp_at, (1,465, 9) beside m in the pricing path's cells of
# a timing or a subaccount, and (1,465, 9, 9) in sa_pricing_pp_at.  Cython's generated
# unpickle code converts the caches of one depth by their inner shape, with one function
# for each shape: given two inner widths among the 2-D caches, it passes the narrower
# array where the wider is expected, which gcc 14 refuses (-Wincompatible-pointer-types,
# made an error on every gcc and clang by tools/build_sec_cy.py), and would write past its
# end.  So every 2-D cache has one inner width, and every 3-D cache one inner shape; the
# two depths need not agree, since the converters are named by the shape.  A kind 4 to 8,
# a subaccount past the lineup, or a timing a cell does not take is inside the cache, where
# the cell refuses it as modelx does, ValueError("invalid kind"), the subaccount's guard or
# ValueError("invalid timing"), and a code or a position from 9 raises IndexError,
# compiled alone.  A larger subaccount_max needs i and the width raised to it.
# i, a subaccount's position, alone (alloc, fund_expense_ann, sa_pp_init,
# scenario_last_mth): 0 .. subaccount_max - 1, 9 values, the width.
# y, a policy year, read by prem_persistency_py, lapse_rate_base_py, coi_rate_guar_at and
# coi_rate_at in cover alone, the pricing path's policy_year_pricing(m) among them: 1 .. 122
# at issue age 0: 123, and one of headroom, 124.  A higher omega_age or a lower
# issue_age_min needs y raised to omega_age - issue_age_min + 3.
# a, an attained age, read by corridor_factor_at and mort_rate_base_at in cover alone, the
# pricing path's from the issue age on: issue_age_min .. omega_age, 0 .. 121: 122, and one
# of headroom, 123.  Ages 0 to 17 read the tables clamped at their first age, 18 as
# shipped.  A higher omega_age needs a raised to omega_age + 2.
{"spaces": {"Projection": {"cells_param_size": {
    "t": 1586, ("t", "timing"): (1586, 9), ("t", "kind"): (1586, 9),
    ("t", "i"): (1586, 9), ("t", "i", "timing"): (1586, 9, 9),
    "m": 1465, ("m", "timing"): (1465, 9), ("m", "i"): (1465, 9),
    ("m", "i", "timing"): (1465, 9, 9),
    "i": 9, "y": 124, "a": 123}}}}
