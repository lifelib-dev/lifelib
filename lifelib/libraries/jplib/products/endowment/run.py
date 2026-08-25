"""Run the Endowment_JP_A reference model and print its cash flow statement.

    python products/endowment/run.py            # anchor cell (point_id = 1)
    python products/endowment/run.py 2          # the education cell

Output is ASCII-only so it prints on a Windows console under any code page: the
currency is written "JPY" rather than with a sign, and the two Japanese product names
are romanized -- yoro hoken (endowment assurance) and gakushi hoken (education
endowment).
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Endowment_JP_A")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
label = ("yoro hoken (endowment)" if proj.cell() == "endowment"
         else "gakushi hoken (education endowment)")
second = ("" if proj.cell() != "education"
          else "   policyholder {}{}, waiver = {}".format(
              proj.ph_sex(), proj.ph_issue_age(), proj.waiver()))

print("model point {}: {} - {} - insured {}{}, {}-year term, "
      "{}-year premium term".format(
          point_id, proj.policy_id(), label, proj.sex(), proj.issue_age(),
          proj.policy_term(), proj.prem_term()))
print("sum assured = JPY {:,.0f}   premium = JPY {:,.0f} p.a.   "
      "schedule = {}{}".format(
          proj.sum_assured(), proj.premium_pp(), proj.schedule_id(), second))
print("net level premium = JPY {:,.2f} at i_cv = {:.2%}   implied rate = {:.4%}   "
      "henreiritsu = {:.4%}".format(
          proj.prem_net_level_pp(), proj.i_cv, proj.implied_rate(), proj.henreiritsu()))
print("checks: in-force roll-fwd {}   policy value roll-fwd {}   terminal value {}   "
      "surrender charge {}   staged value {}   net cf {}".format(
          proj.check_pols_roll_fwd(), proj.check_pol_val_roll_fwd(),
          proj.check_pol_val_terminal(), proj.check_surr_charge(),
          proj.check_staged_value(), proj.check_net_cf()))
print()

result = proj.result_cf()
print(result.round(2).to_string())
print()
print("undiscounted totals per policy issued (JPY, income positive):")
print(result.drop(columns=["pols_if", "pols_if_pay", "pols_wv"]
                          ).sum().round(2).to_string())

model.close()
