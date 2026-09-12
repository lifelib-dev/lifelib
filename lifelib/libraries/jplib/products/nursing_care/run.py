"""Run the LTC_JP_S reference model and print its cash flow statement.

    python products/nursing_care/run.py            # anchor cell (point_id = 1)
    python products/nursing_care/run.py 5          # another model point

The product is 介護保険 (kaigo hoken), private nursing-care insurance written on the
public-scheme-linked design. Output is ASCII-only so it prints on a Windows console
under any code page: amounts are JPY, and the certification grades are printed as the
ASCII codes the input tables use (care1 = yokaigo 1, care2 = yokaigo 2, and so on).

The time index is 0-based: t = 0 is the first policy month, the frame runs t = 0 ..
proj_len() - 1, and the policy year is the 1-based label t // 12 + 1, so policy year 1 is
t = 0 .. 11.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "LTC_JP_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - kaigo hoken (nursing care), {}{}, whole of life, "
      "{} months (t = 0 .. {})".format(
          point_id, proj.policy_id(), proj.sex(), proj.issue_age(), proj.proj_len(),
          proj.proj_len() - 1))
print("lump {:,.0f} JPY at {}   annuity {:,.0f} JPY/yr at {} x{} ({}-tested)   "
      "waiver at {}".format(
          proj.lump_amount(), proj.grade_lump(), proj.annuity_amount(),
          proj.grade_annuity(), proj.annuity_max(), proj.annuity_test(),
          proj.grade_waiver()))
print("premium = {:,.2f} JPY/month ({:,.2f} p.a.)   company limb = {}   "
      "dementia rider = {}   1-year waiting = {}   recovery = {:.2%}   "
      "sel-lapse lambda = {:.2f}".format(
          proj.premium_mth_pp(), 12 * proj.premium_mth_pp(), proj.company_limb(),
          proj.dementia_rider(), proj.waiting_1y(), proj.rec_rate(),
          proj.sel_lapse_lambda()))
print()

df = proj.result_cf()
print("cash flow statement, first 13 months (t = 0 .. 12):")
print(df.head(13).round(2).to_string())
print()
print("policy year 1 totals (t = 0 .. 11, unrounded sums):")
year1 = df.head(12).sum()
for col in ("premiums", "claims_lump", "claims_annuity", "claims_dementia",
            "expenses", "claim_expenses", "commissions", "net_cf"):
    print("  {:<16} {:>16,.2f}".format(col, year1[col]))
print()
print("whole projection: premiums {:,.2f}   claims {:,.2f}   net_cf {:,.2f}".format(
    df["premiums"].sum(),
    df["claims_lump"].sum() + df["claims_annuity"].sum()
    + df["claims_dementia"].sum(),
    df["net_cf"].sum()))
print("checks: pols_roll_fwd={} nesting={} ann_ledger={} net_cf={}".format(
    proj.check_pols_roll_fwd(), proj.check_nesting(),
    proj.check_ann_ledger(), proj.check_net_cf()))

model.close()
