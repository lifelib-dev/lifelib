"""Run the FXWholeLife_JP_S reference model and print its cash flow statement.

    python products/fx_whole_life/run.py            # anchor cell (point_id = 1)
    python products/fx_whole_life/run.py 3          # another model point

The model is 'gaika-date shushin hoken' -- Japanese foreign-currency-denominated
whole life assurance. Every figure the model computes is in USD; the JPY columns
are a three-rate translation of the USD ledger, not a single-rate conversion of the
net figure, and 'fx_spread_jpy' is the difference.

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "FXWholeLife_JP_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
if proj.shape() == "SINGLE":
    prem = "single premium USD {:,.2f}".format(proj.single_premium())
else:
    pay = ("whole of life" if proj.prem_months() == 0
           else "{} months".format(proj.prem_months()))
    prem = "premium USD {:,.2f}/month for {}".format(proj.premium_mth_pp(), pay)

print("model point {}: {} - {} {}, {} shape, cover USD {:,.0f}, {} months".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.issue_age(),
    proj.shape(), proj.sum_assured(), proj.proj_len()))
print("{}   crediting {:.2%} over a floor of {:.2%}   TTM JPY {:,.2f}/USD "
      "+/- {:.2f}".format(prem, proj.credit_rate(), proj.guar_floor(),
                          proj.fx_rate(0), proj.fx_spread()))
print("low_cv = {}   idb_basis = {}   idb_ratchet = {}   apl = {}   "
      "dyn_lapse = {}   fx_path = {}   mort_be_factor = {:.2f}".format(
          proj.low_cv(), proj.idb_basis(), proj.idb_ratchet(), proj.apl_on(),
          proj.dyn_lapse(), proj.fx_path(), proj.mort_be_factor()))
if proj.target_on():
    print("target rider: {:.0%} of JPY {:,.0f} = JPY {:,.0f}, action = {}, "
          "reached at month {}".format(
              proj.target_g(), proj.premium_jpy0(), proj.target_amount_jpy(),
              proj.target_action(), proj.target_month()))
print()

df = proj.result_cf()
print(df.head(6).round(4).to_string())
print("...")
print(df.tail(3).round(4).to_string())
print()

tot = df.sum()
print("whole run, per policy issued (USD): premiums {:,.2f}  death claims {:,.2f}"
      "  surrenders {:,.2f}".format(
          tot["premiums"], tot["claims_death"], tot["claims_lapse"]))
print("                                    conversions {:,.2f}  claim expenses {:,.2f}"
      "  expenses {:,.2f}  commission {:,.2f}".format(
          tot["conversions"], tot["claim_expenses"], tot["expenses"],
          tot["commissions"]))
print("                                    net_cf {:,.2f}".format(tot["net_cf"]))
# Translate month by month at that month's TTM, not once at fx_rate(0): on a model
# point with an FX path the issue-date rate is not the rate the ledger used, and a
# single-rate translation understates the yen net.  Done this way the printed identity
# net_cf_jpy = sum(net_cf x TTM(t)) + fx_spread_jpy holds on every model point.
tot_translated = sum(proj.net_cf(t) * proj.fx_rate(t) for t in range(proj.proj_len()))
print("whole run, JPY: net_cf_jpy {:,.0f}   against sum of net_cf x TTM(t) {:,.0f}   "
      "spread income {:,.0f}".format(
          tot["net_cf_jpy"], tot_translated, tot["fx_spread_jpy"]))
print()
print("checks: pols_roll_fwd {}  av_roll_fwd {}  cv_ledger {}  net_cf {}  "
      "fx_ledger {}".format(
          proj.check_pols_roll_fwd(), proj.check_av_roll_fwd(),
          proj.check_cv_ledger(), proj.check_net_cf(), proj.check_fx_ledger()))

model.close()
