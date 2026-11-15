# mx2cy's spec for WholeLife_US_SEC: the length of each C-array cache in Projection, by the
# cells' parameters (USLIB-SEC-PLAN.md F4, section 6.1 step 6).  A compiled cache raises
# IndexError for an argument outside [0, size), so each size covers the largest argument
# any cell is called with on a point the contract allows, in its frame and in the month
# after it, t = proj_len(), which the roll-forward reads and C4's full sweep evaluates
# every monthly cell at; plus one because the index starts at 0; and one of headroom where
# that leaves room.  mx2cy keys a size by a cell's parameter names, so every cell taking t
# alone shares one.  The contract is three References.  Projection.proj_len refuses a
# point issued below issue_age_min, 0, the youngest issue age product-spec.md admits
# (level pay from 0 to 80); cover ends at Projection.maturity_age, 100; and Data refuses a
# point issued more than future_horizon_mth, 120 months, after the valuation date.  So no
# point a report projects outruns these sizes, and a change to any of the three needs
# them recomputed here and the model rebuilt.
#
# t, months from the valuation date.  The longest frame is a policy issued at 0, covered
# to attained age 100, 100 policy years, and issued 120 months on: 12 * 100 + 120 = 1,320
# months, t = 0 .. 1,319, and 1,320 in the month after.  The roll-forward check's residual,
# check_pols_roll_fwd_resid(t), reads the count carried into t + 1, so C4's sweep, which
# evaluates it at t = 1,320 too, reads pols_if_at at 1,321: 1,322, with no headroom.  A
# longer future_horizon_mth, a higher maturity_age or a lower issue_age_min needs t raised
# to 12 * (maturity_age - issue_age_min) + the horizon + 2.
# timing, beside t in pols_if_at: BEF_NB 0 to AFT_DECR 4, the codes, and no more, so a
# code past them raises IndexError: (1,322, 5).
# kind, beside t in claim_pp: DEATH 0, LAPSE 1 and MATURITY 2, sized 5 all the same:
# (1,322, 5).  Every 2-D cache of a model has one inner width, timing's here, because
# Cython's generated unpickle code converts the 2-D caches of a space with one function,
# written for one width: given (1,322, 3) beside (1,322, 5), it passed the narrower array
# where the wider was expected, which gcc 14 refuses (-Wincompatible-pointer-types, made
# an error on every gcc and clang by tools/build_sec_cy.py), and would write past its end.
# So a kind 3 or 4 is inside the cache, where claim_pp refuses it as modelx does,
# ValueError("invalid kind"), and a kind from 5 raises IndexError, compiled alone.
# y, shared by three cells keyed by one integer: cv_pp_anniv's policy year, 0 ..
# maturity_age - issue_age_min, since cv_pp reads duration(t) and duration(t) + 1, the
# last 100 at issue age 0; and the attained age nsp and mort_rate_guar_at read,
# issue_age_min .. maturity_age, since age_anniv(t) reaches 100 in the last covered month.
# Each is read in cover alone (is_active, is_anniv, or a premium instalment, which falls
# in cover), so none in the month after the frame: 101, and one of headroom, 102.  A
# policy year and an age share the size, so it is the larger of the two derivations: a
# higher maturity_age, or a lower issue_age_min, needs y raised to
# max(maturity_age - issue_age_min, maturity_age) + 2.
{"spaces": {"Projection": {"cells_param_size": {
    "t": 1322, ("t", "timing"): (1322, 5), ("t", "kind"): (1322, 5), "y": 102}}}}
