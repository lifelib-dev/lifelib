# mx2cy's spec for VA_US_SEC: the length of each C-array cache in Projection, by the
# cells' parameters (USLIB-SEC-PLAN.md F4, section 6.1 step 6).  A compiled cache raises
# IndexError for an argument outside [0, size), so each size covers the largest argument
# any cell is called with on a point the contract allows, in its frame and in the month
# after it, t = proj_len(), which the roll-forwards read and C4's full sweep evaluates
# every monthly cell at; plus one because the index starts at 0; and one of headroom.
# mx2cy keys a size by a cell's parameter names, so every cell taking t alone shares one.
# The contract is three References and one of Data's.  Projection.proj_len refuses a point
# issued below issue_age_min, 35, the GLWB's youngest issue age product-spec.md admits
# (and one issued above issue_age_max, 85, glwb_issue_age_max, 80, or, on an elected
# GMDB, gmdb_issue_age_max, 79, which size nothing: an older issue only shortens every
# frame); cover runs to attained age omega_age, 120, so 12 * (omega_age - issue_age_min)
# = 1,020 months from issue at 35; and Data refuses a point issued more than
# future_horizon_mth, 120 months, after the valuation date.  The fourth Reference,
# subaccount_id_max, 9, bounds the subaccount ids a fund set may hold, which proj_len
# refuses past it.  So no point a report projects outruns these sizes, and a change to
# issue_age_min, omega_age, future_horizon_mth or subaccount_id_max needs them recomputed
# here and the model rebuilt.
#
# t, months from the valuation date.  The longest frame is a contract issued at 35 and
# 120 months on: 1,020 + 120 = 1,140 months, t = 0 .. 1,139, and the month after,
# t = proj_len() = 1,140, which C4's sweep calls.  Every cell reading t + 1 is guarded by
# is_active(t) there, the count's roll-forward residual and av_at(t, EOM) among them, and
# lapse_wd_factor's read of the anniversary closing its year, anniv_mth(t), is_wd_year's
# scan of its year and phi_glwb's read of vix_sq at its quarter's last month stay in the
# frame, so nothing reads 1,141: 1,141 values, and one of headroom, 1,142
# = 12 * (omega_age - issue_age_min) + future_horizon_mth + 2.  Data.read_last_mth, the
# last month the scenario and programme arrays hold, is the last t, 1,141, and moves with
# it.
# timing, beside t in pols_if_at, sa_pp_at, av_pp_at, av_at, gwb_pp_at, gawa_pp_at and
# rb_pp_at: one numbering for three families, the count's BEF_NB 0 to AFT_DECR 3, the
# account value's BEF_PREM 4 to EOM 8, and the bases' own BEF_ANNIV 9, which share
# BEF_PREM and BEF_WD with the account value: (1,142, 10).
# kind, beside t in pols_decr, claim_pp, claim_from_av_pp, claims, claims_from_av and
# claims_over_av: DEATH 0 to MATURITY 2 and ALL 3, sized 10 all the same: (1,142, 10).
# name, beside t in scenario_rate: VIX_SQ 0 and CMT10 1, sized 10 all the same.
# i, beside t in inv_return_mth, unit_growth, sa_pp and sa_weight: a subaccount id, 1 ..
# subaccount_id_max, slot 0 unused, 10 = subaccount_id_max + 1, which is the timings'
# count too: (1,142, 10).  Every 2-D cache of a model has one inner width, because
# Cython's generated unpickle code converts the 2-D caches of a space with one function,
# written for one width: given two widths, it passes the narrower array where the wider is
# expected, which gcc 14 refuses (-Wincompatible-pointer-types, made an error on every gcc
# and clang by tools/build_sec_cy.py), and would write past its end.  So a kind 4 to 9, a
# name 2 to 9, or a timing a cell does not take, is inside the cache, where the cell
# refuses it as modelx does, ValueError("invalid kind"), ("invalid name") or ("invalid
# timing"), and a code from 10 raises IndexError, compiled alone.
# (t, i, timing), sa_pp_at, the one 3-D cache, with one inner shape: (1,142, 10, 10).
# i alone, a subaccount id (alloc, fund_expense_rate, sa_pp_init): 1 .. subaccount_id_max,
# slot 0 unused, 10 = subaccount_id_max + 1, no headroom, which would break the one width;
# Data.read_last_sub_id, the last id the fund, opening-value and return arrays hold, is
# the last i, 9, and moves with it.
# j, a position in a fund set (subaccount_id): 0 .. subaccount_id_max - 1, at most nine
# distinct ids: 9 values, and one of headroom, 10 = subaccount_id_max + 1.
# m, an elapsed policy month (t_of_month, prem_scheduled_pm, wd_scheduled_pm):
# 0 .. 12 * (omega_age - issue_age_min) - 1 = 1,019, the last covered policy month at
# issue age 35; is_wd_year reads 12 * (policy_year(t) - 1), at most 1,008, and vix_sq
# reads 3k - 1, at most 1,019: 1,020 values, and one of headroom, 1,021
# = 12 * (omega_age - issue_age_min) + 1.
# k, shared by a count of completed years (surr_charge_rate_at, 0 .. 84) and a contract
# quarter (phi_glwb_vix and vix_sq, 1 .. 340 = 4 * (omega_age - issue_age_min)); a size
# two derivations share is the larger: 341 values, and one of headroom, 342
# = 4 * (omega_age - issue_age_min) + 2.
# a (gawa_pct_at_age) and x (mort_rate_base_at), an attained age, issue_age_min ..
# omega_age - 1 from age 0: 120 values, and one of headroom, 121 = omega_age + 1.  Each
# rests on issue_age_min only through its being 0 or more.  Data.read_last_age, the last
# age the mortality and GAWA% arrays hold, is the last a, 120, and moves with it.
{"spaces": {"Projection": {"cells_param_size": {
    "t": 1142, ("t", "timing"): (1142, 10), ("t", "kind"): (1142, 10),
    ("t", "name"): (1142, 10), ("t", "i"): (1142, 10), ("t", "i", "timing"): (1142, 10, 10),
    "i": 10, "j": 10, "m": 1021, "k": 342, "a": 121, "x": 121}}}}
