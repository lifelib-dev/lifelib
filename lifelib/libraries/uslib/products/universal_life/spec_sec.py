# mx2cy's spec for UL_US_SEC: the length of each C-array cache in Projection, by the cells'
# parameters (USLIB-SEC-PLAN.md F4, section 6.1 step 6).  A compiled cache raises
# IndexError for an argument outside [0, size), so each size covers the largest argument
# any cell is called with on a point the contract allows, in its frame and in the month
# after it, t = proj_len(), which the roll-forwards read and C4's full sweep evaluates
# every monthly cell at; plus one because the index starts at 0; and one of headroom where
# that leaves room.  mx2cy keys a size by a cell's parameter names, so every cell taking t
# alone shares one.  The contract is three References and one of Data's.
# Projection.proj_len refuses a point issued below issue_age_min, 18, the youngest issue
# age product-spec.md admits, and one issued above omega_age, 120; the projection ends at
# omega_age + 1, attained age 121; and Data refuses a point issued more than
# future_horizon_mth, 120 months, after the valuation date.  So no point a report projects
# outruns these sizes, and a change to any of the four needs them recomputed here and the
# model rebuilt.
#
# t, months from the valuation date.  The longest frame is a policy issued at 18, to the
# end of the projection at 121, 103 policy years, and issued 120 months on:
# 12 * (120 - 18 + 1) + 120 = 1,356 months, t = 0 .. 1,355, and 1,356 in the month after,
# which the roll-forwards read: 1,357, and one of headroom, 1,358.  The two residuals and
# av_change read t + 1 only in cover, so nothing reads 1,357.  A longer
# future_horizon_mth, a higher omega_age or a lower issue_age_min needs t raised to
# 12 * (omega_age - issue_age_min + 1) + the horizon + 2.
# timing, beside t in pols_if_at, av_pp_at and av_at: BEF_NB 0 to EOM 7, one numbering for
# the count's three timings and the account value's five, and no more, so a code past them
# raises IndexError: (1,358, 8).
# kind, beside t in claim_pp and claims_from_av: DEATH 0, LAPSE 1 and MATURITY 2, sized 8
# all the same: (1,358, 8).  Every 2-D cache of a model has one inner width, timing's
# here, because Cython's generated unpickle code converts the 2-D caches of a space with
# one function, written for one width: given two widths, it passes the narrower array
# where the wider is expected, which gcc 14 refuses (-Wincompatible-pointer-types, made an
# error on every gcc and clang by tools/build_sec_cy.py), and would write past its end.
# So a kind 3 to 7, or a timing a cell does not take, is inside the cache, where the cell
# refuses it as modelx does, ValueError("invalid kind") or ValueError("invalid timing"),
# and a code from 8 raises IndexError, compiled alone.
# y, a policy year, read by prem_persistency_py, lapse_rate_base_py and coi_rate_guar_py
# in cover alone: 1 .. 103 at issue age 18: 104, and one of headroom, 105.  A higher
# omega_age or a lower issue_age_min needs y raised to omega_age - issue_age_min + 3.
# a, an attained age, read by corridor_factor_at and mort_rate_base_at in cover alone:
# issue_age_min .. omega_age, 18 .. 120: 121, and one of headroom, 122.  A higher
# omega_age needs a raised to omega_age + 2.
{"spaces": {"Projection": {"cells_param_size": {
    "t": 1358, ("t", "timing"): (1358, 8), ("t", "kind"): (1358, 8),
    "y": 105, "a": 122}}}}
