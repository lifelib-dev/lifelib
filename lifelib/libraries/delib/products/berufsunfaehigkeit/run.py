"""Run the BU_DE_S reference model and print its cash flow statement.

    python products/berufsunfaehigkeit/run.py            # anchor cell (point_id = 1)
    python products/berufsunfaehigkeit/run.py 5          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "BU_DE_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} {} ({}) - BU-Rente {:,.2f} EUR/month, "
      "cover to {}, benefit to {}".format(
          point_id, proj.status(), proj.sex(), proj.entry_age(),
          proj.berufsgruppe(), proj.occ_factor(), proj.bu_rente_mth(),
          proj.cover_end_age(), proj.benefit_end_age()))
print("premium form = {}   mode = {} (M = {}, freq_load {:.2f})   "
      "Karenzzeit = {} m   Beitragsverrechnung = {:.2f}   Risikozuschlag = {:.2f}".format(
          proj.premium_form(), proj.prem_mode(), proj.prem_mode_months(),
          proj.freq_load(), proj.karenz_months(), proj.beitragsverrechnung(),
          proj.risk_factor()))
print("Bruttobeitrag {:,.4f} EUR p.a.   instalment {:,.4f} EUR   "
      "Zahlbeitrag {:,.4f} EUR   Beitragssumme {:,.2f} EUR".format(
          proj.prem_gross_level_pp(), proj.prem_gross_pp(0), proj.prem_zahl_pp(0),
          proj.prem_gross_level_pp() * proj.beitragssumme_unit()))
print("proj_len = {} monthly rows (t = 0 .. {}), ages {} to {}".format(
    proj.proj_len(), proj.proj_len() - 1, proj.age(0), proj.age(proj.proj_len() - 1)))
print()

df = proj.result_cf()
print(df.head(14).round(6).to_string())
print()
print("totals over {} months: premiums {:,.2f}  surplus_credit {:,.2f}  "
      "claims_bu_rente {:,.2f}".format(
          proj.proj_len(), df["premiums"].sum(),
          df["surplus_credit"].sum(), df["claims_bu_rente"].sum()))
print("                       claims_reintegration {:,.2f}  expenses {:,.2f}  "
      "claim_expenses {:,.2f}  net_cf {:,.2f}".format(
          df["claims_reintegration"].sum(), df["expenses"].sum(),
          df["claim_expenses"].sum(), df["net_cf"].sum()))
print("checks: net_cf {}  states {}  pols roll fwd {}  dis roll fwd {}  "
      "runoff roll fwd {}  prem split {}  cover end {}".format(
          proj.check_net_cf(), proj.check_states(), proj.check_pols_roll_fwd(),
          proj.check_dis_roll_fwd(), proj.check_runoff_roll_fwd(),
          proj.check_prem_split(), proj.check_cover_end()))

model.close()
