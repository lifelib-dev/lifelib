"""Run the Cancer_JP_S reference model and print its cash flow statement.

    python products/cancer/run.py            # anchor cell (point_id = 1)
    python products/cancer/run.py 4          # another model point

Output is ASCII-only so it prints on a Windows console under any code page: the product
is written "gan hoken (cancer insurance)" and amounts are labelled JPY.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Cancer_JP_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - gan hoken (cancer insurance), {} chassis".format(
    point_id, proj.policy_id(),
    "shushin (whole of life)" if proj.chassis() == "shushin"
    else "teiki (10-year renewable)"))
print("{}{}  base amount JPY {:,.0f}  diagnosis JPY {:,.0f} on a {}-month cycle  "
      "in-situ {:.0%}".format(
          proj.sex(), proj.issue_age(), proj.base_amount(), proj.diag_benefit(),
          proj.cycle_months(), proj.insitu_pct()))
print("daily JPY {:,.0f} (no day limit)  surgery JPY {:,.0f}  treatment JPY {:,.0f}/month "
      "capped at {} months  outpatient JPY {:,.0f}/day".format(
          proj.daily_amount(), proj.surg_mult() * proj.base_amount(),
          proj.treat_benefit(), proj.treat_cap(), proj.outp_daily()))
print("premium = JPY {:,.2f}/month ({:,.2f} p.a.), {}   waiting period = {} months   "
      "waiver = {}".format(
          proj.premium_mth_pp(), 12 * proj.premium_mth_pp(),
          proj.prem_period_type(),
          proj.wait_months(), proj.waiver_trigger()))
print("advanced-medicine rider = {}   discharge rider = {}   "
      "repeat conditioned = {}".format(
          proj.adv_rider(), proj.disch_rider(), proj.repeat_conditioned()))
print("projection = {} months to attained age {}".format(
    proj.proj_len(), proj.omega_age()))
print()

cols = ["pols_if", "pols_healthy", "pols_cancer", "premiums", "claims_diag",
        "claims_insitu", "claims_hosp", "claims_surgery", "claims_treat",
        "claims_outpatient", "claims_advanced", "claims_discharge",
        "claims_lapse", "expenses", "claim_expenses", "commissions", "net_cf"]
df = proj.result_cf()
# The notes' display convention: cash flows to JPY 0.01, pols_if and the state split to
# six decimals, the diagnosed state to eight.  Rounding the whole frame to 2 collapses
# the three policy-count columns to 0.99 / 0.00 and hides the asymmetry the table exists
# to show -- premiums ride on pols_healthy, the care benefits on pols_cancer.
decimals = {c: 2 for c in cols}
decimals.update({"pols_if": 6, "pols_healthy": 6, "pols_cancer": 8})
print(df[cols].head(12).round(decimals).to_string())
print()
print("policy year 1 totals (unrounded sums):")
year1 = df.head(12).sum()
for col in ("premiums", "claims_diag", "claims_insitu", "claims_hosp",
            "claims_surgery", "claims_treat", "claims_outpatient",
            "claims_advanced", "expenses", "claim_expenses",
            "commissions", "net_cf"):
    print("  {:<20s} {:>16,.4f}".format(col, year1[col]))
print()
print("checks: " + "  ".join(
    "{}={}".format(name, getattr(proj, name)())
    for name in ("check_pols_roll_fwd", "check_cancer_roll_fwd",
                 "check_cycle_ledger", "check_insitu_ledger",
                 "check_treat_cap", "check_adv_cap", "check_net_cf")))

model.close()
