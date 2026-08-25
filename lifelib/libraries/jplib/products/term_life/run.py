"""Run the Term_JP_A reference model and print its cash flow statement.

    python products/term_life/run.py            # anchor cell (point_id = 1)
    python products/term_life/run.py 3          # another model point

This file and everything it prints are ASCII-only, so the output lands on a Windows
console under any code page: the product is romanized "teiki hoken" rather than
written in kanji, the two term shapes are "nen manryo" (the renewable fixed-year
term) and "sai manryo" (to a stated age, never renewed), and amounts are labelled
JPY rather than carrying a currency sign.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Term_JP_A")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
shape = "nen manryo (renewable)" if proj.term_type() == "nen" else "sai manryo (fixed)"
print("Term_JP_A - teiki hoken (level term life), JPY, annual grid")
print("model point {}: {} - {}{}, {} {}-year term, cover {:,.0f}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.age_at_entry(),
    shape, proj.policy_term(), proj.sum_assured()))
print("premium = {:,.0f}/month ({:,.0f} p.a.)   horizon = {} years to attained age {}"
      "   boundary = {}".format(
          proj.premium_mth_pp(1), proj.prem_pp(1), proj.proj_len(),
          proj.age(proj.proj_len()) + 1, proj.contract_boundary()))
print("modules: living_needs = {}   wop = {}   reinstatement = {}".format(
    proj.living_needs(), proj.wop(), proj.reinstatement()))
print()

df = proj.result_cf()
print(df.head(12).round(2).to_string())
if len(df) > 12:
    print("... {} further years to t = {}".format(len(df) - 12, proj.proj_len()))
print()
print("undiscounted totals: premiums {:,.2f}   claims {:,.2f}   net_cf {:+,.2f}".format(
    df["premiums"].sum(),
    df["claims_death"].sum() + df["claims_living_needs"].sum(),
    df["net_cf"].sum()))
print("checks: pols_roll_fwd {}   lapse_pool {}   payer {}   prem_level {}   net_cf {}".format(
    proj.check_pols_roll_fwd(), proj.check_lapse_pool(), proj.check_pols_payer(),
    proj.check_prem_level(), proj.check_net_cf()))

model.close()
