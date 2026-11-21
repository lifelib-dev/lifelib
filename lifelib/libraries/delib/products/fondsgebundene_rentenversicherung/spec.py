# FRV_DE_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 601: t = proj_start()..proj_len(): loops range(proj_start(), proj_len()) (lines 1886-2094) plus
#     units_pp(t+1) / pols_if(t+1) at t = proj_len()-1 (check_units_roll_fwd_resid line 1919,
#     check_pols_roll_fwd_resid line 1990). Max t = 600 (table-limited, see need_source) -> bound 601.
#     Product-spec envelope (no table limit) would give 804+1 = 805.
#   x < 101: mort_rate_tariff_at_age(x) reads data.mort_table().loc[x, 'qx_tariff'] unclamped (line 1269);
#     mort_table.csv ages 18..100 -> bound 100+1 = 101. Reachable x = age(t) = entry_age + policy_year(t) - 1
#     (line 682) <= 85 (annuity_age max, product-spec.md:204).
{'cells_param_size': {'t': 601, 'x': 101}}
