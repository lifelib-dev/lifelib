# RV_DE_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1237: t = t_start()..proj_len(): loops range(t_start(), proj_len()) (lines 1853, 2268),
#     check_pols_roll_fwd_resid reads pols_if(t+1) at t = proj_len()-1 (lines 2045, 2077), av_release/pup
#     cells read pols_if(12*(k+1)) with k = proj_len_y()-1 (lines 1010, 1091, 1505) = proj_len(). Max t = 1236
#     -> bound 1237.
#   k < 104: policy year k = k_start()..proj_len_y(): loops range(k_start(), proj_len_y()) (lines 2112-2319)
#     with av(k+1) / av_sur(k+1) (lines 2107, 2128) at k = proj_len_y()-1. Max k = 103 -> bound 104. Lookups
#     by k clamp (decl_rate line 1268, lapse line 1312).
{'cells_param_size': {'t': 1237, 'k': 104}}
