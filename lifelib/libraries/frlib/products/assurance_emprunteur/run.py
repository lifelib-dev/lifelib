"""Run the ADE_FR_S reference model and print its cash flow statement.

    python products/assurance_emprunteur/run.py         # the worked-example anchor cell
    python products/assurance_emprunteur/run.py 2       # the capital restant du premium
    python products/assurance_emprunteur/run.py 9       # a claim in payment, ITT month 18

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "ADE_FR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{}, loan {:,.0f} EUR at {:.2%} over {} months".format(
    point_id, proj.policy_id(), proj.sex(), proj.age_at_entry(),
    proj.capital_initial(), proj.loan_rate_annual(), proj.loan_term_months()))
print("echeance = {:,.2f}/month   quotite = {:.0%}   premium basis = {}   "
      "premium = {:,.2f}/month".format(
          proj.echeance(), proj.quotite(), proj.premium_basis(), proj.prem_pp(0)))
print("indemnity = {} (IR {:.2f})   franchise = {} days   ITT cap = {} months   "
      "IPT benefit = {}".format(
          proj.indemnity_basis(), proj.indemnity_ratio(), proj.franchise_days(),
          proj.itt_max_months(), proj.ipt_benefit_basis()))

T = proj.proj_len()


def cover_end(indicator):
    """The first month the guarantee is off, or None if it outlives the loan.

    Months are 0-based, so the frame is range(T) and the answer is an index in it.
    """
    return next((t for t in range(T) if not indicator(t)), None)


def show(month):
    return ("runs to loan expiry" if month is None
            else "off from t = {}".format(month))


end_deces = cover_end(proj.cover_deces)
end_ptia = cover_end(proj.cover_ptia)
end_itt = cover_end(proj.cover_itt)
print("cover ends: deces age {} ({}), PTIA age {} ({}), ITT/IPT age {} ({}); "
      "loan runs {} months, t = 0 .. {}".format(
          proj.deces_end_age(), show(end_deces), proj.ptia_end_age(), show(end_ptia),
          proj.itt_ipt_end_age(), show(end_itt), T, T - 1))
if end_itt is not None:
    print("  -> {} months of loan with no ITT/IPT cover, CRD {:,.2f} still owed, "
          "{:.6f} of a policy moved out of claim".format(
              T - end_itt, proj.crd(end_itt),
              proj.pols_itt_transfer(end_itt) + proj.pols_ipt_transfer(end_itt)))
print("status = {} (claim duration {} months)   ITT months paid per inception = "
      "{:.6f}".format(proj.status(), proj.claim_duration_months(),
                      proj.itt_annuity_months()))
if proj.status() == "healthy":
    print("PV at {:.1%}: premiums {:,.2f}   outgo {:,.2f}   margin {:.2%}".format(
        proj.disc_rate, proj.pv_premiums(), proj.pv_outgo(),
        1.0 - proj.pv_outgo() / proj.pv_premiums()))
else:
    print("PV at {:.1%}: premiums {:,.2f}   outgo {:,.2f}   (a claim in payment: the "
          "margin is not a pricing quantity)".format(
              proj.disc_rate, proj.pv_premiums(), proj.pv_outgo()))
print("checks: crd {}  states {}  roll-forward {}  benefit split {}  cover end {}".format(
    proj.check_crd(), proj.check_states(), proj.check_pols_roll_fwd(),
    proj.check_benefit_split(), proj.check_cover_end()))
print()
print(proj.result_cf().head(15).round(2).to_string())

model.close()
