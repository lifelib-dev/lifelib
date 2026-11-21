# MYGA_US_S: declared parameter sizes (cells_param_size, model level), only where Probe A showed a
# policy valid for the product raising on the traced range. Sources (model folder, product-spec.md):
#   t < 1202: need_max 1200 + 1 (pols_if(t+1) in av_at EOM line 1518 and check_pols_roll_fwd_resid line 1584) + 1
#     margin = 1202. free_wd_base calls av_pp_at(12*(y-1)) <= 1188, inside
#   y < 101: contract year policy_year(t) (callers lines 671, 771) <= 1199//12 + 1 = 100, +1 = 101
{'cells_param_size': {'t': 1202, 'y': 101}}
