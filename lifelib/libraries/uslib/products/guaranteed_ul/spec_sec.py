# mx2cy's spec for ULSG_US_SEC: the length of each C-array cache in Projection, by the
# cells' parameters (USLIB-SEC-PLAN.md F4, section 6.1 step 6).  A compiled cache raises
# IndexError for an argument outside [0, size), so each size covers the largest argument
# any cell is called with on a point the contract allows, in its frame and in the month
# after it, t = proj_len(), which the roll-forwards read and C4's full sweep evaluates
# every monthly cell at; plus one because the index starts at 0; and one of headroom where
# that leaves room.  mx2cy keys a size by a cell's parameter names, so every cell taking t
# alone shares one.  The contract is two References and one of Data's.
# Projection.proj_len refuses a point issued below issue_age_min, 18, the youngest issue
# age product-spec.md admits, and one issued at or past charges_cease_age, 121, where the
# projection ends, attained age 121; and Data refuses a point issued more than
# future_horizon_mth, 120 months, after the valuation date.  So no point a report projects
# outruns these sizes, and a change to any of the three needs them recomputed here and the
# model rebuilt.
#
# t, months from the valuation date.  The longest frame is a policy issued at 18, to the
# end of the projection at 121, 103 policy years, and issued 120 months on:
# 12 * (121 - 18) + 120 = 1,356 months, t = 0 .. 1,355, and 1,356 in the month after,
# which the count, the account value's opening timing and the lapse latch are carried
# into: 1,357, and one of headroom, 1,358.  pols_lapse_grace reads is_lapsed(t + 1), and
# av_change and the three residuals read t + 1, each only in cover, so nothing reads
# 1,357.  The improvement factor reads t - 12 and 12 * mort_improve_max_years, 240, inside
# the frame.  A longer future_horizon_mth, a higher charges_cease_age or a lower
# issue_age_min needs t raised to 12 * (charges_cease_age - issue_age_min) + the horizon
# + 2.
# timing, beside t in pols_if_at, av_pp_at, sg_pp_at, av_at and loan_bal_pp_at: BEF_NB 0
# to BEF_INT 9, one numbering for the count's three timings, the accounts' six and the
# loan's one, and no more, so a code past them raises IndexError: (1,358, 10).
# kind, beside t in claim_pp and claims_from_av: DEATH 0 to MATURITY 5, sized 10 all the
# same: (1,358, 10).  Every 2-D cache of a model has one inner width, timing's here,
# because Cython's generated unpickle code converts the 2-D caches of a space with one
# function, written for one width: given two widths, it passes the narrower array where
# the wider is expected, which gcc 14 refuses (-Wincompatible-pointer-types, made an error
# on every gcc and clang by tools/build_sec_cy.py), and would write past its end.  So a
# kind 6 to 9, or a timing a cell does not take, is inside the cache, where the cell
# refuses it as modelx does, ValueError("invalid kind") or ValueError("invalid timing"),
# and a code from 10 raises IndexError, compiled alone.
# y, a policy year, read by lapse_rate_base_py, and a completed year, an anniversary, read
# by is_rop_anniv, rop_ratio_anniv and rop_rate_anniv, all in cover alone: policy years
# 1 .. 103 and anniversaries 0 .. 102 at issue age 18: 104, and one of headroom, 105.  A
# higher charges_cease_age or a lower issue_age_min needs y raised to
# charges_cease_age - issue_age_min + 2.
# a, an attained age, read by corridor_factor_at, mort_rate_base_at and coi_rate_guar_at in
# cover alone: issue_age_min .. charges_cease_age - 1, 18 .. 120: 121, and one of
# headroom, 122.  A higher charges_cease_age needs a raised to charges_cease_age + 1.
{"spaces": {"Projection": {"cells_param_size": {
    "t": 1358, ("t", "timing"): (1358, 10), ("t", "kind"): (1358, 10),
    "y": 105, "a": 122}}}}
