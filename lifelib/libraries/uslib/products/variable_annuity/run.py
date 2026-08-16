"""Run the VA_US_S reference model and print its cash flow statement.

    python products/variable_annuity/run.py            # anchor cell (point_id = 1)
    python products/variable_annuity/run.py 2          # the in-force worked-example cell

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "VA_US_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} {} {} life, premium {:,.0f}, entered at policy month {}".format(
    point_id, proj.policy_id(), proj.sex(), proj.age_at_entry(), proj.tax_status(),
    proj.designated_lives(), proj.premium_pp(0), proj.duration_mth_init()))
print("GLWB {} at {:.2%} of GWB, bonus {:.2%}, step-up on {}; GMDB {} at {:.2%} of RB"
      .format(proj.glwb_option(), proj.phi_glwb(1), 0.06, proj.stepup_basis(),
              proj.gmdb_option(), proj.phi_gmdb(1)))
print("For Life Guarantee {}; GLWB activates at age {} at {:.0%} of GAWA; "
      "projected to age {} ({} months)".format(
          "in effect" if proj.forlife_flag() else "not in effect",
          proj.wd_start_age(), proj.wd_intensity(),
          proj.age(proj.proj_len()) + 1, proj.proj_len()))
print()

worked = proj.t_of_month(27)
if worked >= 1:
    print("worked-example month (policy month 27), per contract:")
    print("  BOM subaccounts    {:>12,.2f} {:>12,.2f}   total {:>12,.2f}".format(
        proj.sa_pp(worked - 1, 1), proj.sa_pp(worked - 1, 2), proj.av_pp(worked - 1)))
    print("  after growth       {:>12,.2f} {:>12,.2f}   total {:>12,.2f}".format(
        proj.sa_pp_at(worked, 1, "BEF_FEE"), proj.sa_pp_at(worked, 2, "BEF_FEE"),
        proj.av_pp_at(worked, "BEF_FEE")))
    print("  rider fees         GLWB {:>9,.2f}   GMDB {:>9,.2f}   total {:>12,.2f}".format(
        proj.fee_glwb_pp(worked), proj.fee_gmdb_pp(worked), proj.charge_pp(worked)))
    print("  EOM subaccounts    {:>12,.2f} {:>12,.2f}   total {:>12,.2f}".format(
        proj.sa_pp(worked, 1), proj.sa_pp(worked, 2), proj.av_pp(worked)))
    print("  GMDB test          DB {:>12,.2f}   guarantee claim {:>10,.2f}".format(
        proj.db_pp(worked), proj.gmdb_claim_pp(worked)))
    print()

print("guarantee bases at each of the first 10 contract anniversaries (per contract):")
annivs = [proj.t_of_month(12 * y) for y in range(1, 11)]
print(proj.result_bases().loc[[t for t in annivs if 0 <= t <= proj.proj_len()],
                              ["gwb_pp", "gawa_pp", "bb_pp", "rb_pp", "db_pp"]]
      .round(2).to_string())
print()

print("cash flows, first 12 months:")
print(proj.result_cf().head(13).round(2).to_string())

model.close()
