# Rente_FR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 842: need_max 840; lives_if(t+1,.) in pols_if/lives_death/result_pols and check_lives_roll_fwd over
#     range(proj_len()+1) (:1225) -> max t = 840 -> 841 exclusive, +1 margin; tariff_lives t <=
#     tariff_horizon_mths = 12*(120-50) = 840
#   gen in [1940, 1981): gen is a birth year (absolute); the generational table mort_table.csv covers birth
#     years 1940..1980, so mort_rate_at_age(table_sex, gen, x) is 3 x 41 x 155 entries
#   x < 155: mort_rate_at_age x = attained age; returns 1.0 for x >= omega 120 (:606) but is still cached by
#     x. Older life reaches entry 85 + 69 = 154 when the younger (50) drives an 840-month frame (lives_if via
#     mort_rate(t-1), check_lives_roll_fwd_resid age_at_entry+j) -> 155. mort_table.csv age max 120 covers
#     only x<120
{'cells_param_size': {'t': 842, 'gen': (1940, 1981), 'x': 155}}
