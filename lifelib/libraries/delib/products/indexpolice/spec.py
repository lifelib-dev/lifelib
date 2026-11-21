# Index_DE_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 481: t = t_start()..proj_len(): loops range(t_start(), proj_len()) (lines 1688,1758,1866) and
#     check_pols_roll_fwd_resid reads pols_if(t+1) at t = proj_len()-1 (line 1744). Max t = 480 -> bound 481
#     (product-spec-only envelope: 540+1 = 541).
#   k < 41: policy/index year k = k_start()..proj_len_y(): loops range(k_start(), proj_len_y()) (lines
#     1726-1913) plus av(k+1) (lines 1173,1714) and guar_cap_pp(k+1) (line 1802) at k = proj_len_y()-1. Tables
#     keyed k 0..39 (surplus_rate_table.csv / election_table.csv / index_return_table.csv /
#     index_param_table.csv column t) -> max proj_len_y 40 -> max k 40 -> bound 41.
{'cells_param_size': {'t': 481, 'k': 41}}
