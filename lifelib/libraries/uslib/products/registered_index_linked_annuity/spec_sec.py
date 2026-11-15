# mx2cy's spec for RILA_US_SEC: the length of each C-array cache in Projection, by the
# cells' parameters (USLIB-SEC-PLAN.md F4, section 6.1 step 6).  A compiled cache raises
# IndexError for an argument outside [0, size), so each size covers the largest argument
# any cell is called with on a point the contract allows, in its frame and in the month
# after it, t = proj_len(), which the roll-forwards read and C4's full sweep evaluates
# every monthly cell at; plus one because the index starts at 0; and one of headroom.
# mx2cy keys a size by a cell's parameter names, so every cell taking t alone shares one.
# The contract is four References and one of Data's.  Projection.proj_len refuses a point
# issued below issue_age_min, 0, or above issue_age_max, 111, the oldest issue age
# RILA_US_S projects on the shipped tables; cover runs to the Maturity Date,
# max(maturity_age - issue age, maturity_min_years) years from issue, 90 and 10 as
# shipped, so 12 * max(maturity_age - issue_age_min, maturity_min_years) = 1,080 months
# from issue at 0; and Data refuses a point issued more than future_horizon_mth, 120
# months, after the valuation date.  So no point a report projects outruns these sizes,
# and a change to issue_age_min, issue_age_max, maturity_age, maturity_min_years or
# future_horizon_mth needs them recomputed here and the model rebuilt.
#
# t, months from the valuation date.  The longest frame is a contract issued at 0 and
# 120 months on: 1,080 + 120 = 1,200 months, t = 0 .. 1,199, and the month after,
# t = proj_len() = 1,200, which C4's sweep calls.  There the count's roll-forward residual
# and av_at(t, AFT_WD) are 0.0 before they read t + 1, but market_state holds the instant
# proj_len() + 1, 1,201, which index_level, mvr, risk_free, div_yield and impl_vol read,
# unguarded, at t = proj_len(): 1,202 values, and one of headroom, 1,203
# = 12 * max(maturity_age - issue_age_min, maturity_min_years) + future_horizon_mth + 3.
# Data.read_last_mth, the last month the scenario and withdrawal arrays hold, is the last
# t, 1,202, and moves with it.
# timing, beside t in pols_if_at, inv_amt_pp_at, interim_value_pp_at, iv_notional_pp,
# fixed_proxy_pp, budget_amort_pp, deriv_proxy_pp, trading_cost_pp, fixed_acct_pp_at,
# holding_acct_pp_at, av_pp_at and av_at: one numbering for two families, the count's
# BEF_NB 0 to AFT_DECR 4 and the value cells' BEF_CREDIT 5 to AFT_WD 8: (1,203, 9).
# kind, beside t in pols_decr, claim_pp, claim_from_av_pp, claims, claims_from_av and
# claims_over_av: DEATH 0 to MATURITY 2 and ALL 3; bucket, beside t in roll_to_acct_pp,
# wd_bucket_value_pp and wd_alloc_pp: OPTION 0 to HOLDING 2; name, beside t in
# market_state: INDEX_LEVEL 0 to IMPL_VOL 4; basis, beside t in opt_portfolio_at and
# opt_portfolio_abs_at: CURRENT 0 to UPDATED_EXPIRY 2; rule, beside t in credit_rate_by:
# TERM_END 0 and PRORATED 1; each sized 9 all the same: (1,203, 9).  Every 2-D cache of a
# model has one inner width, timing's here, because Cython's generated unpickle code
# converts the 2-D caches of a space with one function, written for one width: given two
# widths, it passes the narrower array where the wider is expected, which gcc 14 refuses
# (-Wincompatible-pointer-types, made an error on every gcc and clang by
# tools/build_sec_cy.py), and would write past its end.  So a code a cell does not take but
# below 9 is inside the cache, where the cell refuses it as modelx does,
# ValueError("invalid kind"), ("invalid bucket"), ("invalid name"), ("invalid basis"),
# ("invalid rule") or ("invalid timing"), and a code from 9 raises IndexError, compiled
# alone.
# leg, between t and a timing in opt_component_pp and between t and a basis in
# opt_component_at: ATM_CALL 0 to EDGE_BINARY 6, seven legs, by the width 9, one inner
# shape for both 3-D caches (M17): (1,203, 7, 9).  A leg from 7 raises IndexError,
# compiled alone.
# kind, alone in guar_min_rate: the rate kinds CAP 4, STEP 5 and EDGE 6, numbered after the
# claim kinds: 7 values from 0, and one of headroom, 8.
# bucket, alone in roll_share: OPTION 0 to HOLDING 2, sized 9 all the same, the width of
# the 2-D bucket caches, since roll_to_acct_pp passes it every bucket code its own cache
# holds: so a code 3 to 8 reaches roll_share's refusal, ValueError("invalid bucket"), in
# both engines, and none raises IndexError there alone.
# i, in opt_leg: the Floor's four legs, 0 .. 3, and one of headroom, 5.
# a, an attained age (mort_rate_base_at): issue_age_min .. the age the last covered year
# is entered at, max(maturity_age, issue_age_max + maturity_min_years) - 1 = 120, read
# from age 0: 121 values, and one of headroom, 122
# = max(maturity_age, issue_age_max + maturity_min_years) + 1.  Data.read_last_age, the
# last age the mortality array holds, is the last a, 121, and moves with it.
# cy, complete contract years at a month end (surr_charge_rate_at), 0 .. the longest
# policy_term(), max(maturity_age - issue_age_min, maturity_min_years) = 90: 91 values,
# and one of headroom, 92.
# y, a contract year (lapse_rate_base_py), 1 .. policy_term() + 1 = 91, the policy year
# at the month end of the last covered month at issue age 0: 92 values from 0, and one of
# headroom, 93.
# m, a policy month end (wd_amount_pm), 1 .. 12 * policy_term() = 1,080 at issue age 0:
# 1,081 values from 0, and one of headroom, 1,082.
{"spaces": {"Projection": {"cells_param_size": {
    "t": 1203,
    ("t", "timing"): (1203, 9), ("t", "kind"): (1203, 9), ("t", "bucket"): (1203, 9),
    ("t", "name"): (1203, 9), ("t", "basis"): (1203, 9), ("t", "rule"): (1203, 9),
    ("t", "leg", "timing"): (1203, 7, 9), ("t", "leg", "basis"): (1203, 7, 9),
    "kind": 8, "bucket": 9, "i": 5, "a": 122, "cy": 92, "y": 93, "m": 1082}}}}
