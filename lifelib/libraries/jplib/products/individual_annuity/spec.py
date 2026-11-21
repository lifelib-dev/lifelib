# Annuity_JP_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1275: need_max 1273; max index 1273 via pols_if(t+1) in pols_death:1308, pols_if_at:1274,
#     lives_if(t+1):1530; exclusive 1274 + 1 spare
#   s < 109: anniversary s in range(proj_years()) (:1567) with s+1 (check_fund_resid:1553) and s+1 in
#     av_at_m; proj_years:494 = omega 126 - 20 + 1 = 107; exclusive 108 + 1 spare
#   u < 1275: u = t+1 (claims:1415-1417) <= 1273; exclusive 1274 + 1 spare
{'cells_param_size': {'t': 1275, 's': 109, 'u': 1275}}
