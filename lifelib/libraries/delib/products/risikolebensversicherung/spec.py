# RLV_DE_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 481: t = proj_start()..proj_len(): loops range(proj_start(), proj_len()) (lines 1841-2068),
#     check_pols_roll_fwd_resid reads pols_if(t+1) at t = proj_len()-1 (line 1855);
#     mort_rate_tar(12*y)/benefit_pp(12*y) with y <= proj_len_y()-1 stay < proj_len(). Max t = 480 -> bound
#     481.
#   x < 81: mort_rate_at_age(sex_code, smoker_code, x) reads mort_table.csv .at[(sex, smoker, int(x))]
#     unclamped (line 720); age keys 18..80 -> bound 80+1 = 81. Reachable x = age(t)/age2(t) = issue_age +
#     duration(t) (lines 681-698) <= Endalter 75 (product-spec.md:186).
{'cells_param_size': {'t': 481, 'x': 81}}
