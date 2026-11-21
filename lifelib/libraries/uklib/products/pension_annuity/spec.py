# PA_UK_S: declared parameter sizes (cells_param_size, model level), only where Probe A showed a
# policy valid for the product raising on the traced range. Sources (model folder, product-spec.md):
#   t < 792: need_max 780; t-cells evaluated at t <= proj_len-1 (t+1 offsets pass to k-cells) -> 780; +12 margin =>
#     792.
#   k < 792: k = time point 0..proj_len (check_lives_roll_fwd loops range(proj_len()+1), Projection:1006;
#     lives_if(t+1) at t=proj_len-1): max 780 -> 781 required; +11 margin to share t bound => 792.
#   y < 67: annual_income(y) called with y = policy_year(t) = t//12+1 (annuity_pp, Projection:608); t <= 779 -> y <=
#     65 -> 66 exclusive; +1 year margin => 67.
#   a < 66: rpi_index(a)/rpi_peak(a) called with a = y-1 from annual_income (Projection:605) and a=0; y <= 65 -> a
#     <= 64 -> 65 exclusive; +1 margin => 66.
{'cells_param_size': {'t': 792, 'k': 792, 'y': 67, 'a': 66}}
