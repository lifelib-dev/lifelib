"""Run the KLV_DE_S reference model and print its cash flow statement.

    python products/kapitallebensversicherung/run.py            # anchor cell (point_id = 1)
    python products/kapitallebensversicherung/run.py 8          # another model point

The frame counts policy **months**; three views are printed - the first twelve months of
``result_cf()``, the whole run summed into policy years by ``result_cf_annual()``, and the
annual state of ``result_surplus()``.

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "KLV_DE_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} {} - SE {:,.0f} EUR, ratio {:.2f}, term {}, "
      "prem_term {}".format(
          point_id, proj.policy_id(), proj.sex(), proj.issue_age(), proj.smoker(),
          proj.sum_assured(), proj.death_ratio(), proj.policy_term(),
          proj.prem_term()))
print("issue {} at i1 = {:.2%} (cap {:.2%}), zillmer_on = {}, alpha = {:.4f} "
      "(cap {:.3f})".format(
          proj.issue_year(), proj.rechnungszins(), proj.hrz_max(),
          proj.zillmer_on(), proj.alpha_rate(), proj.zillmer_max()))
print("frequency {} {} x {}, phi = {:.3f}   surplus_use = {}   scenario = {}   "
      "bfz_year = {}".format(
          proj.prem_freq(), proj.unterjaehrig_form(), proj.instalments(),
          proj.prem_freq_load(), proj.surplus_use(), proj.scenario_id(),
          proj.bfz_year()))
print("Bruttobeitrag {:,.4f} EUR p.a.   Beitragssumme {:,.2f}   alpha_cost "
      "{:,.2f}   P^n {:,.4f}   P^Z {:,.4f}".format(
          proj.prem_gross_pp(), proj.beitragssumme(), proj.alpha_cost(),
          proj.prem_net_level_pp(), proj.prem_zill_pp()))
print("frame t = {} .. {} months ({} policy years; policy_year = t // 12 + 1)   "
      "pols_if_init {:.6f}".format(
          proj.t_start(), proj.proj_len() - 1, proj.proj_len_y(),
          proj.pols_if_init()))
print()
df = proj.result_cf()
print("first 12 months")
print(df.head(12).round(2).to_string())
print()
print("summed into policy years")
print(proj.result_cf_annual().head(12).round(2).to_string())
print()
print("annual state")
print(proj.result_surplus().head(12).round(2).to_string())
print()
print("totals over {} rows: premiums {:,.2f}  claims {:,.2f}  expenses {:,.2f}  "
      "commissions {:,.2f}  net_cf {:,.2f}".format(
          len(df), df["premiums"].sum(),
          df["claims_death"].sum() + df["claims_maturity"].sum()
          + df["claims_lapse"].sum(),
          df["expenses"].sum(), df["commissions"].sum(), df["net_cf"].sum()))
print("checks: net_cf {}  pols {}  closure {}  reserve {}  surplus {}".format(
    proj.check_net_cf(), proj.check_pols_roll_fwd(),
    proj.check_decrement_closure(), proj.check_res_roll_fwd(),
    proj.check_surplus_roll_fwd()))
print("        surr floor {}  surr non-negative {}  equivalence {}  i1 cap {}  "
      "zillmer cap {}".format(
          proj.check_surr_floor(), proj.check_surr_nonneg(), proj.check_equivalence(),
          proj.check_rechnungszins_cap(), proj.check_zillmer_cap()))

model.close()
