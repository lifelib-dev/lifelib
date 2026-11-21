# Basis_DE_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1225: t = 0..proj_len(): result loops range(proj_len()) and check_pols_roll_fwd reads pols_if(t+1)
#     at t=proj_len()-1 (line 1807); av roll-forward reads mort_rate(12*k) with k up to proj_len_y() (line
#     1843) -> t = 12*proj_len_y() = proj_len(). Max t = 1224 -> bound 1225.
#   k < 103: projection year k = 0..proj_len_y(): result_cf_annual/checks loop range(proj_len_y()) (lines
#     1854,1891,1968,2037) and check_av_roll_fwd_resid reads av_at(k+1, BEF_PREM) (line 1843). proj_len_y max
#     = 121-20+1 = 102 -> max k 102 -> bound 103. Table lookups by k clamp (surplus_table min(max(k,0),max)
#     line 1236; behaviour_table min(duration_y(k)+1, max) line 744).
#   x < 122: mort_rate_at_age(x, y) reads data.mort_table().loc[x] unclamped (line 946); mort_table.csv age
#     keys 20..121; mort_rate short-circuits to 1.0 at age >= omega_age() (line 986). Bound 121+1 = 122.
{'cells_param_size': {'t': 1225, 'k': 103, 'x': 122}}
