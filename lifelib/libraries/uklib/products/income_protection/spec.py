# IP_UK_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 636: need_max 624 + t+1 offset -> 625 required; +12 margin => 636.
#   z < 626: z (1-based claim-duration month) ranges 1..max_dur() (claim_rate_vectors, Projection:593),
#     max_dur() = proj_len() + claim_duration_months() + 1 (Projection:465). For an admissible in_claim cell
#     z0 = elapsed claim months <= 12*(attained_age - 18), so proj_len + z0 <= 12*(expiry_age - 18) <=
#     12*(70-18) = 624; max_dur <= 625; exclusive 626. Termination table (termination_table.csv
#     claim_duration_year 1-5) is clamped via min(), so does not limit z.
{'cells_param_size': {'t': 636, 'z': 626}}
