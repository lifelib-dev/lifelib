# WP_UK_S: declared parameter sizes (cells_param_size, model level), only where Probe A showed a
# policy valid for the product raising on the traced range. Sources (model folder, product-spec.md):
#   t < 1236: need_max 1224 + t+1 offset -> 1225 required; +12 margin => 1236. bonus_rate offset (t ->
#     12*(t//12)+11) stays inside the year, i.e. <= horizon-1 since horizon is a multiple of 12.
{'cells_param_size': {'t': 1236}}
