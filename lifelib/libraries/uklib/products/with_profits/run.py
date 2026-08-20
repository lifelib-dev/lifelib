"""Run the WP_UK_A reference model and print its payout and cash flow statements.

    python products/with_profits/run.py            # scenario A, the up market
    python products/with_profits/run.py 2          # scenario B, the down market
    python products/with_profits/run.py 5          # the conventional endowment

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "WP_UK_A")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
t0 = proj.proj_start()
print("model point {}: {} - {} {}{}, in force {} years".format(
    point_id, proj.model_point()["policy_id"], proj.chassis(), proj.sex(),
    proj.age_at_entry(), proj.duration_inforce()))
print("fund return {:+.1%} ({})   bonus {:.2%}   AMC {:.2%}   guarantee charge {:.2%}"
      .format(proj.fund_return(), proj.tax_basis(), proj.bonus_rate(t0),
              model.Projection.amc_rate, model.Projection.guar_charge_rate_base))
print("carried in: asset share {:,.2f}   smoothed payout {:,.2f}   "
      "guaranteed benefit {:,.2f}".format(
          proj.asset_share(t0 - 1), proj.smoothed_payout(t0 - 1),
          proj.guar_benefit_pp(t0 - 1)))
print("smoothing cap {:+.0%} y/y, target corridor {:.0%}-{:.0%} of asset share; "
      "guarantee dates {}".format(
          model.Projection.smooth_cap, model.Projection.corridor_lo,
          model.Projection.corridor_hi,
          ", ".join(str(y) for y in proj.guarantee_years()) or "none"))
print("projection runs {} to {} ({})".format(
    t0, proj.proj_len(),
    "forced encashment" if proj.is_forced_encashment()
    else "endowment term" if not proj.is_unitised() else "limiting age"))
print()
print("Payout machinery (per policy):")
payout = proj.result_payout()
# bonus_rate is the one rate in a table of money amounts; rounding it to 2 would
# print a 1.50% declaration as 0.02.
print(payout.head(3).round(
    {c: (4 if c == "bonus_rate" else 2) for c in payout.columns}).to_string())
print()
print("Cash flows:")
print(proj.result_cf().head(3).round(2).to_string())
print()
print("Checks: policies {}  asset share {}  FB/MVR exclusive {}  MVR bound {}  "
      "fund non-negative {}  payout corridor {}".format(
          proj.check_pols_roll_fwd(), proj.check_asset_share_roll_fwd(),
          proj.check_fb_mvr_exclusive(), proj.check_mvr_bound(),
          proj.check_fund_nonneg(), proj.check_payout_corridor()))

model.close()
