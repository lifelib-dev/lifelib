"""Run the Term_KR_S reference model and print its cash flow statement.

    python products/term_life/run.py            # anchor cell (point_id = 1)
    python products/term_life/run.py 3          # another model point

This file and everything it prints are ASCII-only, so the output lands on a Windows
console under any code page: the product is romanized "jeonggi boheom" rather than
written in hangul, the two renewal structures are "gaengsin" (renewable, repriced at
attained insurance age) and "bi-gaengsin" (non-renewable), the age basis is romanized
"boheom nai" (insurance age, the six-month rounding rule), and amounts are labelled KRW
rather than carrying a currency sign.

The printed frame is 0-based: t = 0 is the first policy month and the statement runs to
t = proj_len() - 1, so a 20-year contract prints 240 rows.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Term_KR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
shape = ("gaengsin (renewable)" if proj.renewal_type() == "gaengsin"
         else "bi-gaengsin (non-renewable)")
form = ("sunsu bojanghyeong (pure protection)" if proj.maturity_form() == "pure"
        else "mangi hwangeuphyeong (return of premium)")
pay = ("jeongi-nap (whole-term pay)" if proj.pay_term() >= proj.proj_years()
       else "{}-year pay".format(proj.pay_term()))

print("Term_KR_S - jeonggi boheom (level term life), KRW, monthly grid, boheom nai")
print("model point {}: {} - {}{}, {}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(),
    proj.age_at_entry(), shape))
print("  {}-year term, {}, {}, {} class, cover KRW {:,.0f}".format(
    proj.policy_term(), pay, form, proj.rate_class(), proj.sum_assured()))
print("  premium = KRW {:,.0f}/month ({:,.0f} p.a.)   horizon = {} months "
      "({} years) to boheom nai {}   boundary = {}".format(
          proj.premium_mth_pp(0), proj.prem_pp(0), proj.proj_len(),
          proj.proj_years(), proj.age(proj.proj_len() - 1) + 1,
          proj.contract_boundary()))
print("  modules: acc_death = {}   waiver = {}   accel = {}   "
      "reinstatement = {}".format(
          proj.acc_death(), proj.waiver(), proj.accel(), proj.reinstatement()))
print()

df = proj.result_cf()
print(df.head(12).round(2).to_string())
if len(df) > 12:
    print("... {} further months to t = {}".format(
        len(df) - 12, proj.proj_len() - 1))
print()
print("undiscounted totals: premiums {:,.2f}   claims {:,.2f}   "
      "claim exp+expenses+commissions {:,.2f}   net_cf {:+,.2f}".format(
          df["premiums"].sum(),
          (df["claims_death"].sum() + df["claims_acc_death"].sum()
           + df["claims_accel"].sum() + df["claims_maturity"].sum()
           + df["claims_lapse"].sum()),
          (df["claim_expenses"].sum() + df["expenses"].sum()
           + df["commissions"].sum()),
          df["net_cf"].sum()))
print()
print("checks:")
for name in sorted(c for c in model.Projection.cells
                   if c.startswith("check_") and not c.endswith("_resid")):
    print("  {:<24} {}".format(name, getattr(proj, name)()))

model.close()
