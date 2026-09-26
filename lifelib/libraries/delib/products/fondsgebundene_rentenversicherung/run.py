"""Run the FRV_DE_S reference model and print its non-unit cash flow statement.

    python products/fondsgebundene_rentenversicherung/run.py         # anchor (point_id = 1)
    python products/fondsgebundene_rentenversicherung/run.py 7       # another model point

The frame is 360 months on the anchor cell -- ``t = 0 .. 359``, ``t`` being the 0-based
policy month from inception -- so the printout shows the months that carry the mechanics:
the first six, the acquisition-charge cliff at ``t = 58 .. 60``, and the last two before
*Rentenbeginn*.  Totals are summed at full precision.

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "FRV_DE_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
mp = proj.model_point()

print("model point {}: {} - {}{} -> Rentenbeginn at {}, t = {} .. {}".format(
    point_id, mp["policy_id"], proj.sex(), proj.entry_age(),
    proj.annuity_age(), proj.proj_start(), proj.proj_len() - 1))
print("premium: {} {:,.2f} EUR every {} month(s) for {} years   "
      "Beitragssumme {:,.2f} EUR".format(
          proj.prem_form(), proj.prem_pp_base(), proj.prem_mode_months(),
          proj.prem_term_y(), proj.beitragssumme()))
print("charges: {}  acq {:,.2f} EUR over {} instalments of {:,.2f}  "
      "beta {:.2%}  gamma {:.2%} p.a.  Stueckkosten {:,.2f}/month".format(
          proj.charge_id(), proj.charge_acq_total(), proj.acq_instalments(),
          proj.charge_acq_pp(proj.proj_start()), proj.beta_rate(),
          proj.gamma_rate_ann(), proj.policy_fee_mth()))
print("fund: scenario {}  gross {:.2%} p.a.  TER {:.2%} p.a.  "
      "net {:.6%} per month   death benefit: {}".format(
          proj.scenario_id(), proj.fund_return_gross_ann(proj.proj_start()),
          proj.fund_ter_ann(proj.proj_start()),
          proj.fund_return_net_mth(proj.proj_start()), proj.db_form()))
print()

df = proj.result_cf()
rows = [t for t in (proj.proj_start(), proj.proj_start() + 1, proj.proj_start() + 2,
                    proj.proj_start() + 3, proj.proj_start() + 4, proj.proj_start() + 5,
                    58, 59, 60, proj.proj_len() - 2, proj.proj_len() - 1)
        if proj.proj_start() <= t < proj.proj_len()]
cols = ["pols_if", "premiums", "prem_to_av", "charge_acq", "charge_admin_prem",
        "charge_admin_fund", "charge_policy_fee", "charge_risk", "claims_death",
        "claims_lapse", "claims_maturity", "expenses", "commissions", "net_cf"]
print(df.loc[sorted(set(rows)), cols].round(2).to_string())
print()

print("totals over {} months: premiums {:,.2f}  prem_to_av {:,.2f}  "
      "charges {:,.2f}".format(
          len(df), df["premiums"].sum(), df["prem_to_av"].sum(),
          df["charge_acq"].sum() + df["charge_admin_prem"].sum()
          + df["charge_admin_fund"].sum() + df["charge_policy_fee"].sum()
          + df["charge_risk"].sum() + df["stornoabzug"].sum()))
print("                     claims {:,.2f}  withdrawals {:,.2f}  "
      "death strain {:,.2f}  expenses {:,.2f}  commissions {:,.2f}  "
      "net_cf {:,.2f}".format(
          df["claims_death"].sum() + df["claims_lapse"].sum()
          + df["claims_maturity"].sum(), df["withdrawals"].sum(),
          df["death_strain"].sum(), df["expenses"].sum(),
          df["commissions"].sum(), df["net_cf"].sum()))
print()

print("Rentenbeginn: Fondsguthaben {:,.2f} EUR  Rentenfaktor {:.2f} "
      "(guaranteed {:.2f}, current {:.2f})  ->  monthly annuity {:,.2f} EUR".format(
          proj.av_maturity_pp(), proj.rentenfaktor_applied(),
          proj.rentenfaktor_guar(), proj.rentenfaktor_curr(),
          proj.annuity_mth_pp()))
print("reduction in yield: gross {:.4%} - IRR {:.4%} = {:.4%} p.a.  "
      "(a delib measure, NOT the statutory Effektivkostenquote)".format(
          proj.gross_return_ref(), proj.irr_ann(), proj.reduction_in_yield()))
print()

print("checks: net_cf {}  prem split {}  units {}  av {}  benefit funding {}  "
      "pols {}  acq charge {}".format(
          proj.check_net_cf(), proj.check_prem_split(),
          proj.check_units_roll_fwd(), proj.check_av_roll_fwd(),
          proj.check_benefit_funding(), proj.check_pols_roll_fwd(),
          proj.check_acq_charge()))

model.close()
