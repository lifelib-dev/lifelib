"""Run the VA_KR_S reference model and print its cash flow statement.

    python products/variable_annuity/run.py            # anchor cell (point_id = 1)
    python products/variable_annuity/run.py 4          # the in-the-money GMAB cell

VA_KR_S is the reference model of byeonaek yeongeum boheom, a Korean
individual deferred variable annuity written on a teukbyeol gyejeong (special account)
with a minimum death benefit guarantee (GMDB) and an elective minimum annuity account
guarantee (GMAB).

Output is ASCII-only so it prints on a Windows console under any code page. Korean terms
are romanized (Revised Romanization) and amounts are in KRW.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "VA_KR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]

print("VA_KR_S - byeonaek yeongeum boheom (Variable Annuity), monthly grid, boheom nai")
print("=" * 96)
print("model point {}: {} - {} boheom nai {} at issue, gibon boheomnyo KRW {:,.0f} "
      "per month".format(point_id, proj.policy_id(), proj.sex(),
                         proj.age_at_entry(), proj.basic_prem_pp()))
print("  {}-nyeonnap ({} premiums, KRW {:,.0f} boheomnyo chongaek); yeongeum gaesi nai "
      "{}; {} months to yeongeum gaesi".format(
          proj.pay_term(), proj.pay_months(), proj.prem_total_pp(),
          proj.annuity_age(), proj.t_ann()))
print("  guarantee form: {}; fund set {} (chaegwonhyeong floor {:.0%} on a {}-year "
      "yeongeum gaesi jeon boheom gigan)".format(
          "bojeunghyeong (GMAB on)" if proj.gmab_flag() else "mibojeunghyeong (GMAB off)",
          proj.fund_set(), proj.bond_floor(), proj.defer_years()))
print("  return path '{}': gross asset return {:.2%} bond / {:.2%} equity, less unyong "
      "bosu {:.2%} / {:.2%}".format(
          proj.scenario_id(), proj.gross_return(1), proj.gross_return(2),
          proj.fund_mgmt_fee(1), proj.fund_mgmt_fee(2)))
print("  payout: jongsin yeongeum-hyeong, {}-year bojeung gigan, jeongaekhyeong, at "
      "{:.2%} ({} basis); projected to age {} ({} months)".format(
          proj.guar_period_years, proj.annuity_int_rate(), proj.crediting_basis(),
          proj.omega_age, proj.proj_len()))
print()

print("charge stack, per contract, first month (KRW) - five bases, three deduction points")
print("-" * 96)
print("  from the premium, in the ilban gyejeong (never enters the teukbyeol gyejeong):")
print("    gyeyak chegyeol biyong        {:>14,.2f}".format(proj.acq_charge_pp(0)))
print("    gyeyak gwalli biyong (nabip)  {:>14,.2f}".format(proj.maint_charge_in_pp(0)))
print("    gitabiyong                    {:>14,.2f}".format(proj.other_charge_pp(0)))
print("    = teukbyeol gyejeong tuip     {:>14,.2f}   ({:.2%} of the gibon boheomnyo)"
      .format(proj.prem_to_av_pp(0), proj.prem_alloc_ratio(0)))
print("  from the gyeyakja jeongnibaek, on the wol gyeyak haedangil (wolgongjeaek):")
print("    wiheom boheomnyo              {:>14,.2f}".format(proj.risk_prem_pp(0)))
print("    gyeyak gwalli biyong (hu)     {:>14,.2f}   (steps in at nabip wallyo: {:,.2f})"
      .format(proj.maint_charge_after_pp(0),
              proj.maint_charge_after_pp(proj.pay_months())))
print("    GMDB bojeung biyong           {:>14,.2f}".format(proj.gmdb_charge_pp(0)))
print("    GMAB bojeung biyong, asset    {:>14,.2f}".format(proj.gmab_charge_asset_pp(0)))
print("    GMAB bojeung biyong, premium  {:>14,.2f}   (on boheomnyo chongaek {:,.0f}, "
      "max 7 years)".format(proj.gmab_charge_prem_pp(0), proj.gmab_prem_base_pp(0)))
print("  inside the gijun gagyeok, daily (modelled monthly):")
print("    teukbyeol gyejeong unyong bosu{:>14,.2f}".format(proj.mgmt_fee_pp(0)))
print("    jeungkwon georae / gicho fund {:>14,.2f}   (nil in the base run [std])"
      .format(proj.fund_expense_pp(0)))
print("  on surrender, out of the gyeyakja jeongnibaek:")
print("    haeyak gongjeaek at t = 0     {:>14,.2f}   (pyojun haeyak gongjeaek cap "
      "{:,.2f})".format(proj.surr_chg_pp(0), proj.surr_chg_cap_pp()))
print()

print("the two guarantees at the yeongeum gaesi nai gyeyak haedangil (month {})"
      .format(proj.t_ann()))
print("-" * 96)
print("  gyeyakja jeongnibaek AV(T)      {:>16,.2f}".format(proj.av_ann_pp()))
print("  choejeo yeongeum jeongnipgeum K {:>16,.2f}   (imi nabiphan boheomnyo, 100%)"
      .format(proj.gmab_base_pp()))
print("  GMAB payoff max(0, K - AV(T))   {:>16,.2f}   <- INTRINSIC VALUE ON ONE PATH ONLY"
      .format(proj.gmab_claim_pp()))
print("  yeongeum jaewon transferred     {:>16,.2f}   (teukbyeol gyejeong -> ilban "
      "gyejeong)".format(proj.annuity_fund_pp()))
print("  annuity factor / yeongeum yeonaek {:>14,.6f} {:>16,.2f} gross, {:,.2f} net"
      .format(proj.annuity_factor(), proj.annuity_ann_pp(), proj.annuity_net_pp()))
print("  reaching yeongeum gaesi         {:>16,.6f}   of {:,.4f} contracts at issue"
      .format(proj.pols_annuitised(), proj.pols_if_init()))
print()
print("  A single deterministic path values a written option at its INTRINSIC value.")
print("  By Jensen's inequality that is a LOWER BOUND on the expected cost, and it is")
print("  exactly zero whenever the path lands the account above the strike. The")
print("  statutory bojeung junbigeum is a CTE(70) over 1,000 scenarios, or a standard")
print("  factor, whichever is greater [REG-R10] [REG-R26]; this run publishes NEITHER.")
print()

cf = proj.result_cf()
totals = cf.sum()
gmab_charged = sum(proj.gmab_charges(t) for t in range(0, proj.proj_len()))
gmdb_charged = sum(proj.gmdb_charges(t) for t in range(0, proj.proj_len()))
gmdb_incurred = sum(proj.gmdb_claims(t) for t in range(0, proj.proj_len()))
gmab_incurred = sum(proj.gmab_claims(t) for t in range(0, proj.proj_len()))
print("guarantee charges collected against guarantee cost incurred, undiscounted (KRW)")
print("-" * 96)
print("  GMDB  charged {:>16,.2f}   incurred {:>16,.2f}   residual {:>16,.2f}"
      .format(gmdb_charged, gmdb_incurred, gmdb_charged - gmdb_incurred))
print("  GMAB  charged {:>16,.2f}   incurred {:>16,.2f}   residual {:>16,.2f}"
      .format(gmab_charged, gmab_incurred, gmab_charged - gmab_incurred))
print("  The residual is a SINGLE-PATH RESIDUAL and not a profit.")
print()

print("cash flow statement, first 13 months (KRW, income positive)")
print("-" * 96)
print(cf.head(13).round(2).to_string())
print()
print("undiscounted totals over {} months".format(proj.proj_len()))
print("-" * 96)
print(totals.drop("pols_if").round(2).to_string())
print()

print("account boundary: net_cf = net_cf_gen + net_cf_sep, at the first three months")
print("-" * 96)
for t in (0, 1, 2):
    print("  t = {:>3d}   net_cf {:>16,.2f} = ilban {:>16,.2f} + teukbyeol {:>16,.2f}"
          .format(t, proj.net_cf(t), proj.net_cf_gen(t), proj.net_cf_sep(t)))
print()

print("checks")
print("-" * 96)
names = sorted(c for c in model.Projection.cells
               if c.startswith("check_") and not c.endswith("_resid"))
for name in names:
    value = getattr(proj, name)()
    print("  {:<24s} {}".format(name + "()", value))
print()
print("This model is a mechanics demonstration, not a pricing or reserving result.")

model.close()
