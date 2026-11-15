# mx2cy's spec for IUL_US_SEC: the length of each C-array cache in Projection, by the
# cells' parameters (USLIB-SEC-PLAN.md F4, section 6.1 step 6).  A compiled cache raises
# IndexError for an argument outside [0, size), so each size covers the largest argument
# any cell is called with on a point the contract allows, in its frame and in the month
# after it, t = proj_len(), which the roll-forwards read and C4's full sweep evaluates
# every monthly cell at; plus one because the index starts at 0; and one of headroom where
# that leaves room.  mx2cy keys a size by a cell's parameter names, so every cell taking t
# alone shares one.  The contract is three References and one of Data's.
# Projection.proj_len refuses a point issued below issue_age_min, 0, the youngest issue
# age product-spec.md admits (Data refuses a negative one first), or above issue_age_max,
# 85, and one at or past maturity_age, 121, where the projection ends; Data refuses a
# point issued more than future_horizon_mth, 120 months, after the valuation date; and
# seg_term_mth, 12, is the segment term.  So no point a report projects outruns these
# sizes, and a change to issue_age_min, maturity_age, seg_term_mth or future_horizon_mth
# needs them recomputed here and the model rebuilt; issue_age_max sizes nothing, since
# every size rests on the youngest issue age.
#
# t, months from the valuation date.  The longest frame is a policy issued at 0, to the
# end of the projection at 121, 1,452 months, issued 120 months on: 1,572 months,
# t = 0 .. 1,571, and 1,572 in the month after, which the count and the account value's
# opening timing are carried into: 1,573, and one of headroom, 1,574.  av_change and the
# three relative residuals read t + 1 only in cover, so nothing reads 1,573.  A longer
# future_horizon_mth, a higher maturity_age or a lower issue_age_min needs t raised to
# 12 * (maturity_age - issue_age_min) + the horizon + 2.
# The one width, 12: the slots' 0 to seg_term_mth - 1; the timings', BEF_NB 0 to EOM 9,
# one numbering for the count's three timings and the accounts' seven; and the kinds',
# DEATH 0 to WITHDRAWAL 3.  So (1,574, 12) beside t in the cells of a timing (pols_if_at,
# fa_pp_at, lca_pp_at, av_pp_at, av_at), of a kind (claim_pp, claims_from_av) and of a
# slot k, a segment's months since its creation in month t (seg_share, seg_wd_pp,
# seg_ded_pp, seg_bal_pp, seg_ded_cum_pp, seg_wd_cum_pp).  Every 2-D cache of a model has
# one inner width, the widest, because Cython's generated unpickle code converts the 2-D
# caches of a space with one function, written for one width: given two, it passes the
# narrower array where the wider is expected, which gcc 14 refuses
# (-Wincompatible-pointer-types, made an error by tools/build_sec_cy.py), and would write
# past its end.  So a timing 10 or 11, or a kind 4 to 11, is inside the cache, where the
# cell refuses it as modelx does, and a code from 12 raises IndexError, compiled alone; a
# slot from 12, which a seg_term_mth above 12 asks for, raises IndexError compiled, where
# modelx projects: a higher seg_term_mth needs the width raised to it.
# k alone, the ladder's slot at the valuation date, read by the five seg_*_init readers:
# 1 to seg_term_mth, 12: 13, and one of headroom, 14, so that slot 13 meets the reader's
# own refusal compiled.  A higher seg_term_mth needs k raised to seg_term_mth + 2.
# m, the policy month a segment was created in, read by seg_new_pp: 0 to the last covered
# policy month at issue age 0, 1,451: 1,452, and one of headroom, 1,453.  A higher
# maturity_age or a lower issue_age_min needs m raised to
# 12 * (maturity_age - issue_age_min) + 1.
# y, a policy year, read by lapse_rate_base_py and coi_rate_guar_py in cover alone: 1 to
# 121 at issue age 0: 122, and one of headroom, 123.  A higher maturity_age or a lower
# issue_age_min needs y raised to maturity_age - issue_age_min + 2.
# a, an attained age, read by corridor_factor_at and mort_rate_base_at in cover alone:
# issue_age_min to maturity_age - 1, 0 to 120: 121, and one of headroom, 122.  Ages below
# a table's first read it clamped at that age, 18 in the mortality table as shipped.  A
# higher maturity_age needs a raised to maturity_age + 1.
{"spaces": {"Projection": {"cells_param_size": {
    "t": 1574, ("t", "timing"): (1574, 12), ("t", "kind"): (1574, 12),
    ("t", "k"): (1574, 12), "k": 14, "m": 1453, "y": 123, "a": 122}}}}
