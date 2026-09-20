"""Run the Child_KR_S reference model and print its cash flow statement.

    python products/child/run.py            # anchor cell (point_id = 1)
    python products/child/run.py 4          # another model point

Output is ASCII-only so it prints on a Windows console under any code page: amounts are
KRW, the product is written "eorini boheom (children's insurance)" rather than in hangul,
the foetal-enrolment rider is "taea gaip", the premium waiver is "napip myeonje", the
policyholder is the "gyeyakja", and the surrender-value forms are "pyojunhyeong"
(standard), "mijigeuphyeong" (nil until premiums are paid) and "mijigeuphyeong III"
(graded).  The contract's own clock is boheom nai, the Korean insurance age; the decrement
tables are read at man nai, age last birthday, and on a taea contract the two differ by
exactly the pre-birth period.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Child_KR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]

FORMS = {
    "std": "pyojunhyeong (standard surrender value)",
    "susp": "mijigeuphyeong (nil during the payment period, {:.0%} after)",
    "graded": "mijigeuphyeong III (graded ladder, 5% to {:.0%} after napip wallyo)",
}
form = FORMS[proj.cv_form()]
if "{" in form:
    form = form.format(proj.cv_floor_ratio())

if proj.foetal():
    issue = "taea gaip (written in utero), gyeyak nai 0, birth at policy month {}".format(
        proj.birth_month())
else:
    issue = "issued at boheom nai {}".format(proj.issue_age())

waivers = []
if proj.waiver_child():
    waivers.append("child")
if proj.waiver_payer():
    waivers.append("gyeyakja ({}{}, man nai)".format(proj.payer_sex(), proj.payer_age()))
waiver_txt = " + ".join(waivers) if waivers else "none"

print("Child_KR_S - eorini boheom (children's insurance), monthly grid, boheom nai")
print("model point {}: {} - sex {}, {}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), issue))
print("term to boheom nai {} (t = 0 .. {}, {} rows), premium term {} years"
      " (t = 0 .. {}), monthly"
      .format(proj.term_age(), proj.proj_len() - 1, proj.proj_len(),
              proj.prem_period_years(), proj.prem_end()))
print("form: {}".format(form))
if proj.foetal():
    print("premium: KRW {:,.0f} core + KRW {:,.0f} taea module to t = {}, so KRW {:,.0f}"
          " to t = {} and KRW {:,.0f} after".format(
              proj.premium_mth(), proj.premium_foetal_mth(), proj.foetal_prem_end(),
              proj.premium_mth() + proj.premium_foetal_mth(), proj.foetal_prem_end(),
              proj.premium_mth()))
else:
    print("premium: KRW {:,.0f} a month, level, no taea module".format(
        proj.premium_mth()))
print("napip myeonje (premium waiver) on: {}".format(waiver_txt))
print("cover: sanghae huyu janghae (accidental disability) KRW {:,.0f} x disability rate;"
      " cancer KRW {:,.0f}; yusaam (borderline) KRW {:,.0f}".format(
          proj.sum_assured("disability"), proj.sum_assured("cancer"),
          proj.sum_assured("minor_cancer")))
print("       cerebral KRW {:,.0f}; cardiac KRW {:,.0f}; surgery KRW {:,.0f};"
      " hospital KRW {:,.0f}/day; liability KRW {:,.0f}".format(
          proj.sum_assured("cerebral"), proj.sum_assured("cardiac"),
          proj.sum_assured("surgery"), proj.hosp_daily(),
          proj.sum_assured("liability")))
print("myeonchaek gigan (cancer waiting period) = {} months; gamaek gigan (reduced"
      " benefit period) = {} months".format(proj.waiting_mths(), proj.reduction_mths()))
print("basis: bojang bubun applied rate {:.2%}   gongsi iyul {:.2%} (floor {:.2%})"
      "   lapse basis {}   mort_be_factor {:.2f}".format(
          0.0275, 0.017, 0.003, proj.lapse_basis(), proj.mort_be_factor()))
print("pyojun haeyak gongjeaek (statutory surrender charge cap) = KRW {:,.2f}"
      "   over {} months".format(proj.surr_chg_cap_pp(), proj.surr_chg_period()))
print("notional bohom gaipgeumaek (byeolpyo 15 no. 9) = KRW {:,.0f} from a first-year"
      " risk premium of KRW {:,.2f}".format(
          proj.sa_notional_pp(), proj.risk_prem_ann_pp()))
print("acquisition cost = KRW {:,.2f} ({:.2f} months of premium) of which first-year"
      " commission KRW {:,.2f}".format(
          proj.acq_cost_pp(), proj.acq_cost_months(), proj.comm_init_pp()))
print()

df = proj.result_cf()
n = proj.proj_len() - 1          # the last index of the frame, the terminal gyeyak haedangil
m = proj.prem_period_mths()
b = proj.birth_month()
rows = [t for t in (0, 1, b - 1, b, b + 1, b + 11, b + 12) if 0 <= t <= n]
rows += [t for t in (m - 1, m, m + 1) if t <= n and t not in rows]
rows += [t for t in (n // 2, n - 60, n) if t <= n and t not in rows]
rows = sorted(set(rows))

print("cash flow statement (KRW per policy issued) - the months around birth, around"
      " napip wallyo (completion of premium payment), and the tail:")
print(df.loc[rows].round(2).to_string())
print()

val = proj.result_val()
print("account and surrender values at the same durations (KRW per policy):")
print(val.loc[rows].round(2).to_string())
print()

pol = proj.result_pols()
print("policy counts and decrement rates at the same durations:")
print(pol.loc[rows].round(6).to_string())
print()

print("undiscounted totals per policy issued (KRW):")
print(df.sum().round(2).to_string())
print()

print("equivalence on the shipped basis, at the bojang bubun applied rate of 2.75%:")
print("  EPV of all outgo             KRW {:,.2f}".format(proj.epv_outgo_pp()))
print("  EPV of one unit of premium   {:,.4f} monthly units".format(
    proj.epv_prem_unit_pp()))
print("  equivalence monthly premium  KRW {:,.2f}   against a shipped KRW {:,.2f}"
      .format(proj.equiv_premium_mth_pp(), proj.premium_mth()))
print()

print("checks:")
print("  policy count roll forward       {}".format(proj.check_pols_roll_fwd()))
print("  paying / waived split           {}".format(proj.check_waiver_split()))
print("  every exit accounted for        {}".format(proj.check_exit_total()))
print("  no cover before birth           {}".format(proj.check_cover_at_birth()))
print("  once-only benefit ledgers       {}".format(proj.check_once_only()))
print("  taea module inside its terms    {}".format(proj.check_neonatal_term()))
print("  surrender value form floor      {}".format(proj.check_cv_floor()))
print("  gyeyakja jeongnipaek bounds     {}".format(proj.check_av_bounds()))
print("  surrender charge under cap      {}".format(proj.check_surr_chg_cap()))
print("  acquisition cost under cap      {}".format(proj.check_acq_cost_cap()))
print("  published hwangeuplyul grid     {}".format(proj.check_refund_grid()))
print("  equivalence premium identity    {}".format(proj.check_equiv_premium()))
print("  net cash flow ledger            {}".format(proj.check_net_cf()))

model.close()
