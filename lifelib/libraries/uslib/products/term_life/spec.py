# Term_US_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 937: need_max 924 + largest forward offset 12 (conv_elig(t+12), Projection/__init__.py:497) + 1
#     margin (t = proj_len terminal) = 937
#   d < 68: plt_mort_factor(d) (Projection/__init__.py:390), d = policy_year(t) - policy_term(), called only
#     when d >= 1 (line 418). Max policy_year = 95-18 = 77, min level term 10 (plan_term_years line 238):
#     d_max = 67, bound 68
{'cells_param_size': {'t': 937, 'd': 68}}
