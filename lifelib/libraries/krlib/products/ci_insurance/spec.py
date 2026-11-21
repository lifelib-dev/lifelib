# CI_KR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   s < 1165: post-CI cohort label s = month-end of entry: ci_cohort_ids(t) (:1534) = [-1..-min(t,12)] +
#     [1..t] with t <= proj_len, so s <= proj_len = 1152; need 1153, + 12 margin (same horizon as t)
#   t < 1165: need_max 1152 + 1 (t = proj_len reached: check_cv_carve_out sweeps range(proj_len() + 1)
#     :2335; resid_db_pp(t + 1, s) :1690; epv_ben/epv_resid recurse t+1 to proj_len :1268/:1252) + 12 margin
#   y < 111: mort_table.csv age keys 15..110 (mort_rate_at_age :773); ci_incidence_table.csv age 15..100
#     read only for y <= ci_cover_end_age = 100 (:889, constant :2496); bound = 110+1
{'cells_param_size': {'s': 1165, 't': 1165, 'y': 111}}
