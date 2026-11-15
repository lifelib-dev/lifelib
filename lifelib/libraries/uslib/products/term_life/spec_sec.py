# mx2cy's spec for Term_US_SEC: the length of each C-array cache in Projection, by the
# cells' parameters (USLIB-SEC-PLAN.md F4, section 6.1 step 6).  A compiled cache raises
# IndexError for an argument outside [0, size), so each size covers the largest argument
# any cell is called with on a point the contract allows, in its frame and in the month
# after it, t = proj_len(), which the roll-forward reads and C4's full sweep evaluates
# every monthly cell at; plus one because the index starts at 0; and one of headroom where
# that leaves room.  mx2cy keys a size by a cell's parameter names, so every cell taking t
# alone shares one.  The contract is four References.  Projection.proj_len refuses a point
# issued below issue_age_min, 18, the youngest issue age of every plan, and one whose
# level period is below policy_term_min, 10 years, the shortest plan's (product-spec.md);
# cover ends at Projection.expiry_age, 95; and Data refuses a point issued more than
# future_horizon_mth, 120 months, after the valuation date.  So no point a report projects
# outruns these sizes, and a change to any of the four needs them recomputed here and the
# model rebuilt.
#
# t, months from the valuation date.  The longest frame is a policy issued at 18, covered
# to attained age 95, 77 policy years, and issued 120 months on: 12 * 77 + 120 = 1,044
# months, t = 0 .. 1,043, and 1,044 in the month after: 1,045, and one of headroom, 1,046.
# A longer future_horizon_mth needs t raised to 12 * 77 + the horizon + 2.
# timing, beside t in pols_if_at: BEF_NB = 0 and BEF_DECR = 1, the codes, and no more, so
# a code that is neither raises IndexError: (1,046, 2).
# y, a policy year: 1 .. 77 in cover.  conv_rate asks for the year after month t's only
# inside the conversion window, at most year 31 on a thirty-year plan, and jump_ratio
# reads years n and n + 1, at most 31 on the plans product-spec.md offers: 78, and one of
# headroom, 79, which also holds the 78 jump_ratio reads on a 77-year plan issued at 18,
# the longest level period whose shock falls in cover.
# d, a post-level-term duration in years, policy_year - n: 1 .. 67 in cover on a plan of
# the shortest level period, policy_term_min, issued at 18, and 68 in the month after its
# frame, where mort_rate reads it, as it reads it in every month: 69, with no headroom.
{"spaces": {"Projection": {"cells_param_size": {
    "t": 1046, ("t", "timing"): (1046, 2), "y": 79, "d": 69}}}}
