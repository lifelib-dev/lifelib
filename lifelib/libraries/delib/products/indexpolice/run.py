"""Run the Index_DE_S reference model and print its cash flow statement.

    python products/indexpolice/run.py            # anchor cell (point_id = 1)
    python products/indexpolice/run.py 8          # another model point

The frame counts policy **months**.  Three views are printed - the twelve months of one
*Indexjahr* on the monthly frame, the whole run summed into policy years by
``result_cf_annual()``, and the annual state of ``result_index()``, which is where the
*Indexjahr*, the three credits and the account live.

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Index_DE_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
df = proj.result_cf()

print("model point {}: {} - {}{} -> Rentenbeginn at {}, {} policy years "
      "(t = {} .. {} months)".format(
          point_id, proj.policy_id(), proj.sex(), proj.entry_age(),
          proj.ann_start_age(), proj.proj_len_y() - proj.k_start(),
          proj.t_start(), proj.proj_len() - 1))
print("premium form = {}   {:,.2f} EUR a year x {} years {} -> collected "
      "{:,.2f} EUR   Beitragssumme {:,.2f} EUR".format(
          proj.prem_form(), proj.prem_base_pp(proj.k_start()),
          proj.prem_term_y(), proj.prem_freq(),
          proj.prem_gross_pp(proj.k_start()), proj.prem_sum()))
print("payoff = {}   index = {}   Cap {:.2%} monthly   Quote {:.2%}   "
      "election = {}".format(
          proj.payoff_form(), proj.index_id(), proj.index_cap(proj.k_start()),
          proj.index_quote(proj.k_start()), proj.elect_id()))
print("guarantee = {:.0%} of Beitragssumme at i_g = {:.2%}   "
      "Beitragsgarantie {:,.2f} EUR   Stornoabzug {}".format(
          proj.guar_level(), proj.guar_rate(),
          proj.guar_level() * proj.prem_sum(),
          "on" if proj.surr_charge_on() else "off"))
print()
k0 = proj.k_start()
print("the twelve months of Indexjahr k = {} (cap {:.2%}, sum of capped months "
      "{:+.4%}, raw year {:+.4%}, credited {:+.4%})".format(
          k0 + 1, proj.index_cap(k0 + 1), proj.index_sum(k0 + 1),
          proj.index_return_year(k0 + 1), proj.index_credit_rate(k0 + 1)))
print("  month   raw      capped")
for t in range(12 * (k0 + 1), 12 * (k0 + 1) + 12):
    print("  {:>5}  {:+8.4%} {:+9.4%}".format(
        proj.index_month(t), proj.index_return_mth(t),
        proj.index_return_capped_mth(t)))
print()
print("summed into policy years")
print(proj.result_cf_annual().round(2).to_string())
print()
print("annual state")
print(proj.result_index().round(4).to_string())
print()
print("totals: premiums {:,.2f}  claims {:,.2f}  expenses {:,.2f}  "
      "net_cf {:,.2f}".format(
          df["premiums"].sum(),
          df["claims_death"].sum() + df["claims_lapse"].sum()
          + df["claims_maturity"].sum(),
          df["expenses"].sum(), df["net_cf"].sum()))
state = proj.result_index()
print("credits: guaranteed interest {:,.2f}  safe arm {:,.2f}  index {:,.2f}  "
      "budget ratio {:.4f}".format(
          state["guar_int"].sum(), state["surplus_credit"].sum(),
          state["index_credit"].sum(), proj.index_budget_ratio()))
n = proj.proj_len_y()
print("at Rentenbeginn: account {:,.2f}  guaranteed capital {:,.2f}  "
      "benefit {:,.2f}  monthly Rente {:,.2f}".format(
          proj.av_pp(n), proj.guar_cap_pp(n), proj.mat_pp(n - 1),
          proj.ann_monthly_pp()))
print("checks: net_cf {}  av roll fwd {}  pols roll fwd {}  surplus alloc {}  "
      "lock-in {}  index credit {}".format(
          proj.check_net_cf(), proj.check_av_roll_fwd(),
          proj.check_pols_roll_fwd(), proj.check_surplus_alloc(),
          proj.check_lock_in(), proj.check_index_credit()))

model.close()
