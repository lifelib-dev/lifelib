# Pflege_DE_S: declared parameter sizes (cells_param_size, model level), only where Probe A showed a
# policy valid for the product raising on the traced range. Sources (model folder, product-spec.md):
#   t < 1105: t = duration_mth_init()..proj_len(): loops range(proj_len()) / range(duration_mth_init(), proj_len())
#     (lines 1745-2144), pols_if_at(t, END) -> pols_if(t+1) (line 1104) and check_pols_roll_fwd_resid reads
#     pols_if(t+1) (line 1925) at t = proj_len()-1. Max t = 1104 -> bound 1105.
{'cells_param_size': {'t': 1105}}
