# Euro_FR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 482: proj_len 480 (12*proj_years=40); max arg 480 via av(t+1)/av_pp(t+1)/pols_if(t+1) and
#     pb_cum_pp(12*(y+1)) with y<=39 in check_cliquet_resid -> 481 exclusive, +1 margin
#   y < 42: projection year y = t//12 (:624) in range(proj_years=40); ppb_pp(y+1) in
#     check_ppb_roll_fwd/result_pb reaches 40 -> 41 exclusive, +1 margin; r_fin/ref_rate clamp to
#     fin_rate_table.csv y max 39 (:717)
#   v in [-8, 41): v reaches -ppb_vintages_init(); the PPB clock is 8 years (A132-16, product-
#     spec.md:168/239, [std]); no model-point validation enforces 8: a point with more vintages raises
{'cells_param_size': {'t': 482, 'y': 42, 'v': (-8, 41)}}
