# Immediate_KR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   m < 805: period count m of annuity_factor_certain(m, i) :676 / accum_factor(m, i) :692: m =
#     annuity_term_mths() - t (:751,:778), m = t (:1266, t <= proj_len) -> m <= proj_len = 792; need 793, + 12
#     margin
#   t < 805: need_max 792 + 1 (t = proj_len reached: check_av_roll_fwd/check_lives_roll_fwd/check_surr_value
#     sweep range(proj_len() + 1) :1241,:1284,:1435; lives_if(t + 1), pols_if(t + 1), av_pp(t + 1),
#     disc_factor(t + 1)) + 12 margin
{'cells_param_size': {'m': 805, 't': 805}}
