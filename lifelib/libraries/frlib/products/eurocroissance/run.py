"""Run the EC_FR_S reference model and print its provision and cash flow statements.

    python products/eurocroissance/run.py            # Chassis A, the worked example
    python products/eurocroissance/run.py 2          # Chassis B, same asset path
    python products/eurocroissance/run.py 7          # an in-force Chassis A cell

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "EC_FR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
t0 = proj.proj_start()
n = proj.proj_len()
last = n - 1                      # the frame is t = t0 .. proj_len() - 1
chassis = ("A (1 deg: euros and parts)" if proj.is_euro_leg()
           else "B (2 deg: parts only)")
print("model point {}: {} - chassis {}, {}{}, term {} years, in force {} years".format(
    point_id, proj.model_point()["policy_id"], chassis, proj.sex(),
    proj.issue_age(), proj.policy_term(), proj.duration_inforce()))
print("projection: t = {} .. {} ({} monthly periods; policy year = t // 12 + 1)".format(
    t0, last, last - t0 + 1))
print("guarantee {:.0%} of net versements = {:,.2f} at t = {}   scenario {}".format(
    proj.guarantee_rate(), proj.mg(last), last, proj.scenario()))
print("charges: entry {:.2%}  parts {:.2%} p.a.  performance {:.0%}  exit {:.2%}"
      .format(proj.entry_charge_rate(), proj.parts_charge_rate(),
              proj.perf_charge_rate(), proj.exit_charge_rate()))
print("part value {:.4f} at inception, floor {:.4f}   i_pm {:.2%} at month boundary {} "
      "to {:.2%} at boundary {}".format(
          proj.part_value_init(), proj.min_part_value(), proj.i_pm(t0), t0,
          proj.i_pm(n), n))
print("decrements {}   partial rachat factor {:.2f}   lock-up {} years".format(
    proj.decrement_basis(), proj.wd_factor(), proj.lock_up_years()))
print()
# Policy months are 0-based: t = 0 is the issue month and t = 11 the first anniversary,
# so the anniversary that closes policy year y is month 12 * y - 1.  The notes' two
# worked-example tables are exactly those rows.
anniv = [t for t in range(t0, n) if t % 12 == 11]
print("Provisions at the anniversary months (per policy), t = 12y - 1:")
prov = proj.result_provisions()
# i_pm and asset_return are rates in a table of money amounts; rounding them to 2
# would print a 2.25% discount rate as 0.02.
rounding = {c: (4 if c in ("i_pm", "asset_return", "part_value", "parts") else 2)
            for c in prov.columns}
print(prov.loc[anniv].round(rounding).to_string())
print()
print("Provisions month by month over the first policy year, t = {} .. {}:".format(
    t0, min(t0 + 12, n) - 1))
print(prov.loc[t0:min(t0 + 12, n) - 1].round(rounding).to_string())
print()
print("Cash flows, the first 13 months (t = {} .. {}):".format(
    t0, min(t0 + 13, n) - 1))
print(proj.result_cf().head(13).round(2).to_string())
print()
print("The same frame summed into policy years:")
print(proj.result_cf_annual().round(2).to_string())
print()
# The notes' policy-year-6 shock closes at the anniversary of policy year 6.
shock = min(12 * (t0 // 12 + 6) - 1, last)
print("Exit values at t = {}: surrender {:,.2f}  death {:,.2f}  "
      "maturity at t = {} {:,.2f}".format(
          shock, proj.surrender_value(shock),
          proj.death_payout(shock), last, proj.maturity_value(last)))
print("Insurer own funds, peak: contribution {:,.2f}   PGT {:,.2f}".format(
    max(proj.insurer_contribution(t) for t in range(t0, n)),
    max(proj.pgt(t) for t in range(t0, n))))
print()
print("Checks: assets {}  parts {}  guarantee {}  policies {}".format(
    proj.check_assets_roll_fwd(), proj.check_parts_roll_fwd(),
    proj.check_guarantee_roll_fwd(), proj.check_pols_roll_fwd()))
print("        PM funds the guarantee {}  PGT covers it {}  part value floor {}"
      .format(proj.check_guarantee_funding(), proj.check_pgt_covers_guarantee(),
              proj.check_part_value_floor()))
print("        own funds not paid {}  in-force PM re-struck {}".format(
    proj.check_own_funds_not_paid(), proj.check_pm_restruck()))

model.close()
