"""Run the UC_FR_S reference model and print its account value and cash flow statements.

    python products/assurance_vie_uc/run.py            # anchor cell (point_id = 1)
    python products/assurance_vie_uc/run.py 2          # the base run, 360 months

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "UC_FR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{}, premium {:,.0f} split {:.0%} UC / {:.0%} euro".format(
    point_id, proj.policy_id(), proj.sex(), proj.issue_age(), proj.premium(),
    proj.uc_alloc(), proj.euro_alloc()))
print("premium charge {:.2%}  UC mgmt charge {:.4%} p.a.  arbitrage fee {:.2%}  "
      "euro credited {:.2%} p.a. net".format(
          proj.prem_charge_rate(), proj.mgmt_fee_rate_uc(), proj.arbitrage_fee_rate(),
          proj.euro_credit_rate()))
print("garantie plancher = {} ({} basis, levy {}, ceases at age {}, cap {:,.0f})".format(
    proj.plancher_flag(), proj.plancher_basis(), proj.plancher_levy_source(),
    proj.plancher_end_age(), proj.plancher_cap()))
print("scenario {}  withdrawals {}  arbitrage {}  lapse dynamics {}".format(
    proj.uc_return_scenario(), proj.wd_pattern(), proj.arb_pattern(),
    proj.lapse_dynamic()))
print("projecting {} months, t = 0 .. {}; tariff at issue age {:.4%} p.a. of the capital "
      "sous risque".format(proj.proj_len(), proj.proj_len() - 1, proj.plancher_rate(0)))
print()
print("Account value (per policy), first three months:")
print(proj.result_av().head(3).round(4).to_string())
print()
print("Cash flows, first three months:")
print(proj.result_cf().head(3).round(2).to_string())

model.close()
