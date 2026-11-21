# CI_UK_S: declared parameter sizes (cells_param_size, model level), only where Probe A showed a
# policy valid for the product raising on the traced range. Sources (model folder, product-spec.md):
#   t < 612: need_max 600 + max offset t+1 (pols_if(proj_len) read at t=proj_len-1) = 601 required; +12 one-year
#     margin => 612.
#   x < 76: pivot_interp(x,...) receives age(t, life) = age_at_entry + t//12 (Projection:433,438). Max attained age:
#     policy ends by 75th birthday (product-spec.md:83) so ANB age in last year <= 74 -> 75 exclusive; +1 margin =
#     76. Note pivot_interp extrapolates beyond ci_rate_table.csv pivots, so no table key caps it.
{'cells_param_size': {'t': 612, 'x': 76}}
