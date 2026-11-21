# VA_US_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 963: need_max 960 + 2 (scenario_rate(t_of_month(3*k-1)) with k = contract_quarter(t) reaches month
#   a < 121: gawa_pct_at_age(age(t)) (lines 1072, 1640, 1658): attained age <= omega_age 120 - 1;
#     gawa_pct_table.csv clamps via index.asof; omega_age 120 + 1 = 121
#   k < 321: contract quarter contract_quarter(t) = duration_mth(t)//3 + 1 (line 723), duration_mth <= 12*80
#     - 1 = 959 -> k <= 320, +1 = 321
#   m < 961: t_of_month(m) month since issue (line 745): m = 3k-1 <= 959 or 12*(policy_year(t)-1)(-1) (lines
#     1046, 1736) <= 959; 959+1 +1 margin = 961
{'cells_param_size': {'t': 963, 'a': 121, 'k': 321, 'm': 961}}
