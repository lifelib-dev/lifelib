"""Run the Riester_DE_S reference model and print its cash flow statement.

    python products/riester_rente/run.py            # anchor cell (point_id = 1)
    python products/riester_rente/run.py 11         # another model point

The frame counts projection **months**.  Three views are printed - the first months of
``result_cf()``, the whole run summed into projection years by ``result_cf_annual()``, and
the annual state of ``result_acct()``, which is where the two accounts, the subsidy chain
and the Beitragsgarantie live.

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Riester_DE_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {}{} concluded at age {}, in force {} years, "
      "Rentenbeginn {}".format(
          point_id, proj.sex(), proj.age(0), proj.issue_age(),
          proj.duration_init(), proj.rentenbeginn_age()))
print("contribution form = {} ({}), contrib_ratio = {:.2f}, "
      "frequency = {} (phi = {:.4f}), bfs_year = {}".format(
          proj.contrib_form(), proj.income_id(), proj.contrib_ratio(),
          proj.prem_freq(), proj.prem_freq_load(), proj.bfs_year()))
print("t = 0 .. {} months ({} years), conversion at k = {} / t = {} (age {}, "
      "calendar {}), rechnungszins = {:.4f}, scenario = {}".format(
          proj.proj_len() - 1, proj.proj_len_y(), proj.k_conv(), proj.t_conv(),
          proj.age_y(proj.k_conv()), proj.calendar_year_y(proj.k_conv()),
          proj.rechnungszins(), proj.scenario_id()))
print("opening: av_total_pp = {:,.2f}  guar_pp = {:,.2f}  "
      "garantieluecke_pp = {:,.2f}".format(
          proj.av_total_pp(0), proj.guar_pp(0), proj.garantieluecke_pp(0)))
print()
print("conversion: account {:,.2f}  guarantee {:,.2f}  capital {:,.2f}  "
      "Garantieluecke {:,.2f}".format(
          proj.account_conv_pp(), proj.guar_pp(proj.k_conv() + 1),
          proj.capital_conv_pp(), proj.garantieluecke_conv_pp()))
print("            ann_factor {:.8f}  rentenfaktor curr {:.6f} / guar {:.2f} "
      "-> applied {:.6f}".format(
          proj.ann_factor(), proj.rentenfaktor_curr(),
          proj.rentenfaktor_guar(), proj.rentenfaktor_applied()))
print("            Kleinbetragsrente {}  Teilkapital {:,.2f}  "
      "Abfindung {:,.2f}  Rente {:,.2f} a month ({:,.2f} p.a.)".format(
          proj.is_kleinbetrag(), proj.teilkapital_pp(),
          proj.commutation_pp(), proj.annuity_month_pp(),
          proj.annuity_pp(proj.k_conv())))
if proj.rentengarantie_years() > 0 and not proj.is_kleinbetrag():
    print("            Rentengarantiezeit {} y = {} instalments, t = {} .. {}".format(
        proj.rentengarantie_years(), 12 * proj.rentengarantie_years(),
        proj.t_conv(), proj.t_conv() + 12 * proj.rentengarantie_years() - 1))
print()

df = proj.result_cf()
print("first 13 months")
print(df.head(13).round(2).to_string())
print()
print("the Rentenbeginn, month by month")
print(df.loc[proj.t_conv() - 1:proj.t_conv() + 2].round(2).to_string())
print()
print("summed into projection years")
print(proj.result_cf_annual().head(8).round(2).to_string())
print()
print("annual state")
print(proj.result_acct().head(8).round(2).to_string())
print()
print("totals over {} months ({} years): premiums {:,.2f}  zulagen {:,.2f}  "
      "claims {:,.2f}".format(
          proj.proj_len(), proj.proj_len_y(), df["premiums"].sum(),
          df["zulagen"].sum(),
          df[["claims_death", "claims_lapse", "claims_transfer",
              "claims_lumpsum", "claims_commutation",
              "claims_annuity"]].to_numpy().sum()))
print("                     expenses {:,.2f}  commissions {:,.2f}  "
      "net_cf {:,.2f}".format(
          df["expenses"].sum(), df["commissions"].sum(), df["net_cf"].sum()))
print("checks: net_cf {}  av {}  guar {}  pols {}  conversion {}  "
      "zulage lag {}".format(
          proj.check_net_cf(), proj.check_av_roll_fwd(),
          proj.check_guar_roll_fwd(), proj.check_pols_roll_fwd(),
          proj.check_conversion(), proj.check_zulage_lag()))

model.close()
