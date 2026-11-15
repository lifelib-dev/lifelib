# mx2cy's spec for FIA_US_SEC: the length of each C-array cache in Projection, by the
# cells' parameters (USLIB-SEC-PLAN.md F4, section 6.1 step 6).  A compiled cache raises
# IndexError for an argument outside [0, size), so each size covers the largest argument
# any cell is called with on a point the contract allows, in its frame and in the month
# after it, t = proj_len(), which the roll-forwards read and C4's full sweep evaluates
# every monthly cell at; plus one because the index starts at 0; and one of headroom.
# mx2cy keys a size by a cell's parameter names, so every cell taking t alone shares one.
# The contract is three References and one of Data's.  Projection.proj_len refuses a point
# issued below issue_age_min, 40, the youngest issue age product-spec.md admits (and one
# issued above issue_age_max, 80, which sizes nothing: an older issue only shortens every
# frame); cover runs through the contract year entered at maturity_age, 120, so
# 12 * (maturity_age - issue_age_min + 1) = 972 months from issue at 40; and Data refuses
# a point issued more than future_horizon_mth, 120 months, after the valuation date.  So
# no point a report projects outruns these sizes, and a change to issue_age_min,
# maturity_age or future_horizon_mth needs them recomputed here and the model rebuilt.
#
# t, months from the valuation date.  The longest frame is a contract issued at 40 and
# 120 months on: 972 + 120 = 1,092 months, t = 0 .. 1,091, and the month after,
# t = proj_len() = 1,092, which C4's sweep calls.  Every cell reading t + 1 is guarded by
# is_active(t) there, the count's roll-forward residual and av_at(t, EOY) among them, and
# lapse_rate's read of the anniversary closing its year, anniv_mth(t), stays in the frame,
# so nothing reads 1,093: 1,093 values, and one of headroom, 1,094
# = 12 * (maturity_age - issue_age_min + 1) + future_horizon_mth + 2.  Data.read_last_mth,
# the last month the scenario arrays hold, is the last t, 1,093, and moves with it.
# timing, beside t in pols_if_at, av_pp_at, av_fixed_pp_at, av_indexed_pp_at,
# benefit_base_pp_at, lw_pp_at and av_at: one numbering for three families, the count's
# BEF_NB 0 to AFT_DECR 4, the account value's BEF_PREM 5 to EOY 9, and the benefit base's
# own BEF_ROLLUP 10 and BEF_STEP_UP 11, which shares BEF_WD and EOY with the account value
# and the lifetime withdrawal: (1,094, 12).
# kind, beside t in pols_decr, claim_pp, claim_from_av_pp, claims, claims_from_av and
# claims_over_av: DEATH 0 to MATURITY 2 and ALL 3, sized 12 all the same: (1,094, 12).
# name, beside y in scenario_value: INDEX_LEVEL 0 and MVA_REF_YIELD 1, sized 12 all the
# same: (83, 12).  Every 2-D cache of a model has one inner width, timing's here, because
# Cython's generated unpickle code converts the 2-D caches of a space with one function,
# written for one width: given two widths, it passes the narrower array where the wider is
# expected, which gcc 14 refuses (-Wincompatible-pointer-types, made an error on every gcc
# and clang by tools/build_sec_cy.py), and would write past its end.  So a kind 4 to 11, a
# name 2 to 11, or a timing a cell does not take, is inside the cache, where the cell
# refuses it as modelx does, ValueError("invalid kind"), ("invalid name") or ("invalid
# timing"), and a code from 12 raises IndexError, compiled alone.
# y, a contract year, 1 .. 81 (surr_charge_rate_py, vest_rate_py, rollup_rate_py), and an
# anniversary number, 0 .. 81 (index_level, mva_ref_yield, scenario_value), read in cover
# alone: 81 = maturity_age - issue_age_min + 1, so 82, and one of headroom, 83.
# a, an attained age: issue_age_min .. maturity_age, 40 .. 120 (mort_rate_base_at), and an
# exercise age to maturity_age + 1, 121 (payout_rate_at), the covered age opening the last
# contract year plus 1; activation_rate shares it.  122 values from age 0, and one of
# headroom, 123 = maturity_age + 3.  It rests on issue_age_min only through its being 0 or
# more.  Data.read_last_age, the last age the mortality and payout arrays hold, is the last
# a, 122, and moves with it.
# k, a count of completed contract years, 0 .. 80 (wd_scheduled_at): 81, and one of
# headroom, 82 = maturity_age - issue_age_min + 2.
{"spaces": {"Projection": {"cells_param_size": {
    "t": 1094, ("t", "timing"): (1094, 12), ("t", "kind"): (1094, 12),
    ("y", "name"): (83, 12), "y": 83, "a": 123, "k": 82}}}}
