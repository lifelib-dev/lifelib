# ADE_FR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 482: need_max 480 (product-spec.md:87, 40y*12) ; largest arg reached = proj_len (pols_if(t+1) in
#     check_pols_roll_fwd_resid/pols_if_at, itt_cohorts_raw(t+1) in pols_itt_close, crd(t+1)) -> 480+1 = 481
#     exclusive, +1 margin = 482
#   k < 482: crd(k) is a time point 0..proj_len(): crd(t+1) and check_crd->crd(proj_len()) (:583); 480+1 =
#     481, +1 margin
{'cells_param_size': {'t': 482, 'k': 482}}
