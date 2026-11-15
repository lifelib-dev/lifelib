"""Run VA_US_SEC and print a model point's guarantees, account value and cash flows.

    python products/variable_annuity/run_sec.py          # point 1, the anchor cell
    python products/variable_annuity/run_sec.py 2        # the worked example, in force
    python products/variable_annuity/run_sec.py --block  # the block, row by row
    python products/variable_annuity/run_sec.py 1 --cython  # on the compiled model

``t`` counts months from the valuation date, which is the same instant for every model
point, so row ``t`` of one point's frame is the same month as row ``t`` of any other's, and
a block is the frames summed row by row. Point 1 is the worked example's anchor cell
issued at the valuation date: its row ``t = 26`` is the worked example's month, the 27th
policy month. Point 2 is the worked example's carried state in force at the valuation
date with 26 policy months elapsed, so the same month is its row ``t = 0``, and the two
print the same worked-example block.

The guarantees move at the contract's own events, so the bases are printed at the
anniversary months, those where ``duration_mth(t) % 12 == 11``, and the cash flows are
printed month by month for the first year and summed into projection years,
``t // 12 + 1``, by the runner itself: ``VA_US_SEC`` publishes no annual report.

Points are named by their ``point_id``, and ``Projection`` is indexed by a point's position
in the table, as basiclife's BasicTerm_SC is, so the runner maps the one to the other.  It
takes the key from the model: the position where ``Projection`` takes ``idx``, as every
compiled model does, and the label where it takes ``point_id``, as an SEC model does before
its Phase 2.  It passes each timing, ``BEF_PREM`` or ``BEF_FEE``, as the model's own
Reference of the name, the int code, where the model defines one, and as the text
otherwise.  A label the table does not hold, a number or not, is refused with the labels
it does hold.

``--cython`` runs the compiled model instead of modelx, and prints the same lines.  It is
``VA_US_SEC_nomx_cy`` beside the model, which the repository's ``tools/build_sec_cy.py``
builds there the first time, and again whenever it is not built for this interpreter or
the model, ``sample_sec.py``, ``spec_sec.py`` or the tool is newer than it: about five
minutes, which it says on stderr.  The build is never committed, and ``.gitignore`` covers
everything it leaves.  A ``lifelib.create()`` copy of the library carries no ``tools/``,
wherever it is put, so there ``--cython`` stops, saying so, where it would build.
``--build DIR`` runs the package a build put in ``DIR`` instead, on the CSVs the build
copied there, and never builds.  Either way the runner stops, saying why, if the package
imports without its extension modules, which would compute the same numbers
uncompiled.

A block run asks every point for its frame before it projects any, because whether a point
is still in cover, and whether the contract issues it, are the product's rules, which
``proj_len()`` applies, and such a point would otherwise stop the run part-way.  It
releases each point's ItemSpace once it is read, so that it holds one point's cells at a
time.  Deleting the ItemSpace is not enough, because it sits in reference cycles that only
Python's cyclic collector frees, so the runner collects after each release, in both
passes.  It freezes everything alive (``gc.freeze``) once the model and its table are read,
and again once it has every point's length, so that each collection scans only what the
block has made since, and it unfreezes them at the end.  The block's sum is kept as it
goes, a frame at a time, compensated as pandas' ``groupby`` sum is, so that it is the sum
of the frames concatenated and grouped by ``t``, bit for bit; a NaN in a frame, which
``groupby`` would skip, propagates into the sum.

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import gc
import importlib
import importlib.machinery
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
NAME = "VA_US_SEC"
SUFFIXES = tuple(importlib.machinery.EXTENSION_SUFFIXES)
USAGE = "usage: python run_sec.py [point_id | --block] [--cython] [--build DIR]"


def parse(argv):
    """``(point_id or None for the block, cython, build_dir)``, or exit with the usage.

    A point is named by its label, read as an int where it is one: a label that is not a
    number is no ``point_id``, and is refused with the table's labels, by name.
    """
    point, block, cython, build = None, False, False, None
    args = iter(argv)
    for arg in args:
        if arg == "--block":
            block = True
        elif arg == "--cython":
            cython = True
        elif arg == "--build":
            build = next(args, None)
            if build is None:
                sys.exit(USAGE)
            cython = True
        elif arg in ("--help", "-h") or point is not None:
            sys.exit(USAGE)
        else:
            try:
                point = int(arg)
            except ValueError:
                point = arg
    if block and point is not None:
        sys.exit(USAGE)
    return (None if block else (1 if point is None else point)), cython, build


def _built(package):
    """The compiled space module of ``package`` built for this interpreter, if any."""
    found = [package / f"_mx_classes{suffix}" for suffix in SUFFIXES]
    return [path for path in found if path.is_file()]


def _tool():
    """``tools/build_sec_cy.py`` of the repository holding this product, or ``None``.

    The product sits at ``lifelib/libraries/<lib>/products/<product>`` in the repository,
    and a ``lifelib.create()`` copy of the library has no repository above it, and no
    tool, wherever it is put, as ``sec_support._tool`` finds it.
    """
    up = HERE.parents
    if len(up) < 5 or up[2].name != "libraries":
        return None
    return up[4] / "tools" / "build_sec_cy.py"


def compiled_model(build_dir):
    """The compiled model: from ``build_dir``, or built in place first where it is stale."""
    if build_dir is None:
        out, tool = HERE, _tool()
        package = out / f"{NAME}_nomx_cy"
        sources = [*(HERE / NAME).rglob("*.py"), HERE / "sample_sec.py",
                   HERE / "spec_sec.py", *([tool] if tool else [])]
        built = _built(package)
        newest = max((path.stat().st_mtime for path in sources if path.is_file()),
                     default=0.0)
        if not built or min(path.stat().st_mtime for path in built) < newest:
            if tool is None or not tool.is_file():
                sys.exit("--cython builds the model with the source repository's "
                         "tools/build_sec_cy.py, and a lifelib.create() copy carries no "
                         "tools/, so it cannot build")
            print(f"building {NAME} with {tool.name}, which takes about five "
                  f"minutes ...", file=sys.stderr)
            done = subprocess.run([sys.executable, str(tool), str(HERE)],
                                  stdout=subprocess.DEVNULL)
            if done.returncode:
                sys.exit(f"the build failed; {tool.name} printed why")
    else:
        out = Path(build_dir).resolve()
        package = out / f"{NAME}_nomx_cy"
        if not _built(package):
            sys.exit(f"{package} holds no build of {NAME} for this interpreter")
    sys.path.insert(0, str(out))
    model = importlib.import_module(f"{NAME}_nomx_cy").mx_model
    space = type(model.Projection)
    if not sys.modules[space.__module__].__file__.endswith(SUFFIXES):
        sys.exit(f"{package} imported without its extension modules, so it would run "
                 f"uncompiled; rebuild it with tools/build_sec_cy.py")
    return model


point_id, cython, build_dir = parse(sys.argv[1:])
if cython:
    model = compiled_model(build_dir)
else:
    import modelx as mx
    model = mx.read_model(HERE / NAME)
table = model.Data.model_point_table()
# Projection's key for each point_id: its position, or the label itself (the docstring).
if cython or tuple(model.Projection.parameters) == ("idx",):
    position = {label: i for i, label in enumerate(table.index)}
else:
    position = {label: label for label in table.index}


def key(label):
    """The key that selects point ``label`` in ``Projection``."""
    return position[label]


def code(label):
    """The argument that stands for timing ``label``: the model's own int Reference named
    ``label`` where it defines one, and the text otherwise."""
    value = getattr(model.Projection, label, label)
    return value if isinstance(value, int) and not isinstance(value, bool) else label


def add(total, compensation, frame):
    """Add ``frame``'s rows to the running sum's first rows, compensated (Kahan), as
    pandas' ``groupby`` sum adds each group's values in turn."""
    rows = len(frame)
    y = frame - compensation[:rows]
    t = total[:rows] + y
    compensation[:rows] = (t - total[:rows]) - y
    total[:rows] = t


def months(n):
    """``n`` with its unit: "1 month", "15 months"."""
    return "{} month{}".format(n, "" if n == 1 else "s")


def release(label):
    """Drop a point's ItemSpace once read, and collect it (see the module docstring)."""
    del model.Projection[key(label)]
    gc.collect()


def describe(proj):
    """One line on where the point stands at the valuation date."""
    d = proj.duration_mth_init()
    if d < 0:
        return "to be issued at t = {}, {} after the valuation date".format(-d, months(-d))
    if d == 0:
        return "issued at the valuation date, t = 0"
    return ("in force {}: contract year {}, attained age {}, {:.6f} in force, "
            "AV {:,.2f} per contract{}".format(
                months(d), proj.policy_year(0), proj.age(0), proj.pols_if(0),
                proj.av_pp_init(), ", depleted" if proj.depleted_open(0) else ""))


def origin(label):
    """Where the generator took the row from, where the table records it."""
    if "row_kind" not in table.columns:
        return ""
    kind, source, m = (table.at[label, c]
                       for c in ("row_kind", "source_policy_id", "source_mth"))
    if kind == "derived":
        return " (S's {} at its month {})".format(source, m)
    if kind == "future":
        return " (S's {}, issued {} on)".format(source, months(-m))
    return " (S's {})".format(source)


def events(proj, n):
    """The first withdrawal and the account value running out.

    Each in the frame, or before the valuation date on a point in force that has already
    withdrawn, or whose account value is already exhausted.
    """
    first = [t for t in range(proj.t_entry(), n) if proj.is_first_wd(t)]
    empty = [t for t in range(proj.t_entry(), n) if proj.depleted_flag(t)]
    if first:
        wd = "in contract year {}, at t = {}".format(proj.policy_year(first[0]), first[0])
    elif proj.has_wd_init():
        wd = "before the valuation date"
    else:
        wd = "not in the frame"
    if proj.depleted_open(proj.t_entry()):
        out = "before the valuation date"
    elif empty:
        out = "in contract year {}, at t = {}".format(proj.policy_year(empty[0]),
                                                     empty[0])
    else:
        out = "not in the frame"
    return "first withdrawal {}; account value runs out {}".format(wd, out)


if point_id is None:
    gc.freeze()
    rows = {}
    for label in table.index:
        rows[label] = model.Projection[key(label)].proj_len()
        release(label)
    gc.freeze()
    total, columns = np.zeros((max(rows.values(), default=0), 0)), None
    print("model points, t = 0 the valuation date for each:")
    for label in table.index:
        proj = model.Projection[key(label)]
        df = proj.result_cf()
        if columns is None:
            columns = list(df.columns)
            total = np.zeros((len(total), len(columns)))
            compensation = np.zeros_like(total)
        add(total, compensation, df[columns].to_numpy())
        print("  {:>2}  {:<16} {}; proj_len {}".format(
            label, table.at[label, "policy_id"], describe(proj), rows[label]))
        del proj, df
        release(label)                          # each point is read once, then released
    block = pd.DataFrame(total, columns=columns,
                         index=pd.RangeIndex(len(total), name="t"))
    print()
    print("the block, first 12 rows, t = 0..11 (months from the valuation date):")
    print(block.head(12).round(2).to_string())
    print()
    print("the block summed into projection years 1-12, year = t // 12 + 1:")
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", block["pols_if"].groupby(years).first())
    print(annual.head(12).round(2).to_string())
else:
    label = point_id
    if label not in position:
        sys.exit("no model point {} in the table: {}".format(label, list(position)))
    proj = model.Projection[key(label)]
    entry = proj.t_entry()
    print("model point {}: {}{} - {}{} {} {} life, premium {:,.0f}".format(
        label, table.at[label, "policy_id"], origin(label), proj.sex(),
        proj.age_at_entry(), proj.tax_status(), proj.designated_lives(),
        proj.premium_single()))
    print("GLWB {} at {:.2%} of GWB, bonus {:.2%}, step-up on {}; GMDB {} at {:.2%} of RB"
          .format(proj.glwb_option(), proj.phi_glwb(entry), proj.bonus_pct,
                  proj.stepup_basis(), proj.gmdb_option(), proj.phi_gmdb(entry)))
    print("For Life Guarantee {}; GLWB activates at age {} at {:.0%} of GAWA".format(
        "in effect" if proj.forlife_flag() else "not in effect", proj.wd_start_age(),
        proj.wd_intensity()))
    print("at the valuation date: {}".format(describe(proj)))
    n = proj.proj_len()
    print("proj_len = {} from the valuation date (t = 0..{}); cover ends at policy month "
          "{}, attained age {}".format(months(n), n - 1, proj.maturity_mth(),
                                       proj.omega_age))
    print(events(proj, n))
    print()

    worked = proj.t_of_month(26)          # the 27th policy month, 26 months elapsed
    if entry <= worked < n:
        print("worked-example month (the 27th policy month, t = {}), per contract:".format(
            worked))
        print("  BOM subaccounts    {:>12,.2f} {:>12,.2f}   total {:>12,.2f}".format(
            proj.sa_pp_at(worked, 1, code("BEF_PREM")),
            proj.sa_pp_at(worked, 2, code("BEF_PREM")),
            proj.av_pp_at(worked, code("BEF_PREM"))))
        print("  after growth       {:>12,.2f} {:>12,.2f}   total {:>12,.2f}".format(
            proj.sa_pp_at(worked, 1, code("BEF_FEE")),
            proj.sa_pp_at(worked, 2, code("BEF_FEE")),
            proj.av_pp_at(worked, code("BEF_FEE"))))
        print("  rider fees         GLWB {:>9,.2f}   GMDB {:>9,.2f}   total {:>12,.2f}"
              .format(proj.fee_glwb_pp(worked), proj.fee_gmdb_pp(worked),
                      proj.charge_pp(worked)))
        print("  EOM subaccounts    {:>12,.2f} {:>12,.2f}   total {:>12,.2f}".format(
            proj.sa_pp(worked, 1), proj.sa_pp(worked, 2), proj.av_pp(worked)))
        print("  GMDB test          DB {:>12,.2f}   guarantee claim {:>10,.2f}".format(
            proj.db_pp(worked), proj.gmdb_claim_pp(worked)))
        print("  guarantee bases    GWB {:>11,.2f}   BB {:>11,.2f}   GAWA {:>9,.2f}   "
              "RB {:>11,.2f}".format(proj.gwb_pp(worked), proj.bb_pp(worked),
                                    proj.gawa_pp(worked), proj.rb_pp(worked)))
        print()

    anniversaries = [t for t in range(entry, n) if proj.duration_mth(t) % 12 == 11]
    print("guarantee bases and account value (per contract), at the anniversary months")
    print("closing the first fourteen contract years on the books, duration_mth(t) % 12 "
          "== 11:")
    bases = proj.result_bases().loc[anniversaries[:14],
                                    ["gwb_pp", "gawa_pp", "bb_pp", "rb_pp", "adj_pp",
                                     "db_pp"]]
    av = proj.result_av().loc[anniversaries[:14], ["av_pp"]]
    print(bases.join(av).round(2).to_string())
    print()
    print("cash flows, t = 0..11 (months from the valuation date):")
    cf = proj.result_cf()
    print(cf.head(12).round(2).to_string())
    print()
    print("cash flows summed into projection years 1-14, year = t // 12 + 1:")
    years = pd.Index(cf.index // 12 + 1, name="proj_year")
    annual = cf.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", cf["pols_if"].groupby(years).first())
    print(annual.head(14).round(2).to_string())

if not cython:
    model.close()
gc.unfreeze()
