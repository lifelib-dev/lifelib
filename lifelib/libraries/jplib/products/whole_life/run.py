"""Run the WholeLife_JP_S reference model and print its cash flow statement.

    python products/whole_life/run.py            # anchor cell (point_id = 1)
    python products/whole_life/run.py 5          # another model point

Output is ASCII-only so it prints on a Windows console under any code page: amounts are
JPY, the product is written "shushin hoken (whole life)" rather than in kana, and the
suppressed-surrender-value form is written "tei-kaiyaku-henreikin-gata".
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "WholeLife_JP_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
form = ("tei-kaiyaku-henreikin-gata, k = {:.2f}".format(proj.low_cv_rate())
        if proj.low_cv() else "ordinary form")
term = ("whole-of-life premium" if proj.prem_term() == 0
        else "{}-year premium term".format(proj.prem_term()))

print("WholeLife_JP_S - shushin hoken (whole life), monthly grid")
print("model point {}: {} - {}{}, cover JPY {:,.0f}, {}, {}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.age_at_entry(),
    proj.sum_assured(), term, form))
print("premium = JPY {:,.2f} p.a. (nenbarai: one month in twelve)   "
      "projection = {} months ({} years) to attained age {}".format(
          proj.premium_pp(), proj.proj_len(), proj.proj_years(), proj.omega_age()))
print("modules: default rate = {:.2%}   loan utilisation = {:.2%}   "
      "cliff spike = {:.2%}   dynamic lapse = {}   mort_be_factor = {:.2f}".format(
          proj.model_point()["default_rate"], proj.pol_loan_util(),
          proj.lapse_spike(), proj.dyn_lapse(), proj.mort_be_factor()))
print("net level premium pi = JPY {:,.2f}   surrender value at the first "
      "anniversary is JPY {:,.2f}".format(proj.prem_net_level_pp(), proj.cv_pp(1)))
print()

# t is 0-based and counts policy MONTHS, so 払込満了 - the end of the premium term -
# is the month t = 12 m, which is where the surrender value steps up.
df = proj.result_cf()
rows = [t for t in (0, 1, 2, 11, 12, 13) if t < proj.proj_len()]
cliff = proj.prem_period_months()
rows += [t for t in (cliff - 2, cliff - 1, cliff, cliff + 1)
         if 0 <= t < proj.proj_len() and t not in rows]
print("first policy months (t = 0 is the first), and the months around 払込満了:")
print(df.loc[sorted(rows)].round(2).to_string())
print()
annual = df.groupby(df.index // 12).sum()
annual["pols_if"] = [proj.pols_if(12 * y) for y in annual.index]
annual.index.name = "policy year - 1"
print("the same statement grouped into policy years (pols_if at the anniversary):")
print(annual.head(18).round(2).to_string())
print()
print("undiscounted totals per policy issued (JPY):")
print(df.sum().round(2).to_string())
print()
print("roll-forward checks: pols {}  decrements {}  policy value {}  "
      "reserve {}  loans {}  net cf {}".format(
          proj.check_pols_roll_fwd(), proj.check_decrement_sum(),
          proj.check_pol_val_roll_fwd(), proj.check_reserve_identity(),
          proj.check_loan_roll_fwd(), proj.check_net_cf()))

model.close()
