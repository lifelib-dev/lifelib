# Medical_JP_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1190: need_max 1188; max index 1188 via t+1 in check_* residuals (pols_if, agg_days_*, adv_paid,
#     lump_count, waived; :1413-1523); exclusive 1189 + 1 spare
#   x < 120: mort_rate_at_age(x):563 (clamps to omega) called with lo and lo+1 (:595) from age(t) <= 118;
#     lo+1 reaches 119 when age_basis_offset = 0.5; mort_table.csv max 118 => 119 + 1
{'cells_param_size': {'t': 1190, 'x': 120}}
