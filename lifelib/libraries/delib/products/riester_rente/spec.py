# Riester_DE_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   k < 96: projection year k = 0..proj_len_y(): loops range(proj_len_y()) (lines 1995-2239) with
#     av_total_pp(k+1) (av_total_pp_at AFT_INT line 1357; check line 1982), av_total_at(k+1, BEF_PREM) (line
#     1986), guar_pp(k+1) (lines 2014-2017) at k = proj_len_y()-1. Max k = 95 -> bound 96. NOTE k-1 / k -
#     zulage_lag (zulage_lag = 1, line 2292) reach -1 at k = 0 (lines 1145, 2139).
#   t < 1141: t = 0..proj_len(): loops range(proj_len()) (lines 1956, 2174), check_pols_roll_fwd_resid reads
#     pols_if(t+1) at t = proj_len()-1 (line 2053), av roll-forward reads pols_if(12*k) for k <=
#     proj_len_y()-1. Max t = 1140 -> bound 1141.
#   tau in [2027, 2122): tau is a calendar year (absolute) = valuation_year + k with k >= 0 and the
#     reference valuation_year 2027; x < 111, so annuity_mort_rate(x, tau) is 111 x 95 entries
#   x < 111: mort_rate_at_age(x) and annuity_mort_rate(x, tau) return 1.0 for x >= omega_age (110) before
#     reading mort_table_accum.csv / annuity_mort_table.csv .at[x] (lines 784-811); the Rentenfaktor loop runs
#     x0+k <= omega_age (line 1539); both tables end at age 110. Max x = 110 -> bound 111.
{'cells_param_size': {'k': 96, 't': 1141, 'tau': (2027, 2122), 'x': 111}}
