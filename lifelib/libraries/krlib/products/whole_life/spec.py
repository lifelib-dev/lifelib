# WholeLife_KR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1236: need_max 1212 + 12 for pols_surr(t) -> pols_reinstate(t + 12) (:1552) at t = proj_len-1 (max t
#     = proj_len+11, cell returns 0 there but is cached) + 12 margin = 1212+12+12
#   n < 102: n is the number of annual payments of annuity_due(y, n), the only Cell taking n (the month
#     annuities take u): prem_period() <= proj_years() = 115 - 15 + 1 = 101, or surr_chg_prem_years = 20; the
#     recursion goes down
#   u < 1225: month index from issue: epv_death_mth/annuity_due_mth/... (:862-:912) recurse u+1 up to u =
#     proj_len (returns 0) -> need 1212+1; + 12 margin
#   d < 1225: anniversary month d = 0..proj_len (checks sweep range(proj_len() + 1) :1824,:1858; cv_pp(t +
#     1) :1605, results :1998-2004); need 1212+1, + 12 margin
{'cells_param_size': {'t': 1236, 'n': 102, 'u': 1225, 'd': 1225}}
