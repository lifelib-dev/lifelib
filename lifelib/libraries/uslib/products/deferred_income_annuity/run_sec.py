"""Run the DIA_US_SEC model and print a model point's cash flows, or the block's.

    python products/deferred_income_annuity/run_sec.py           # point 1: the anchor cell
    python products/deferred_income_annuity/run_sec.py 19        # the anchor, in payout
    python products/deferred_income_annuity/run_sec.py --block   # every model point, summed
    python products/deferred_income_annuity/run_sec.py 19 --cython  # point 19, compiled

``t`` counts months from the valuation date, which is the same instant for every model
point, so row ``t`` of one point's frame is the same month as row ``t`` of any other's, and
a block is the frames summed row by row.  Points are named by their ``point_id``, and
``Projection`` is indexed by a point's position in the table, as basiclife's BasicTerm_SC
is, so the runner maps the one to the other.  It takes the key from the model: the
position where ``Projection`` takes ``idx``, as every compiled model does, and the label
where it takes ``point_id``, as an SEC model does before its Phase 2.  A label that is not
one of the table's is refused, naming them, whether it is a number or not.

The shipped table is a set of test cases, not a block valued at one date.  Mortality
improvement is dated by calendar year, from each contract's issue year, and every row keeps
the issue year of the S point it was taken from, 2026.  So the twins stand in 2026 at
``t = 0``, a row restated in force ``d`` months stands ``d`` months later, and the row
issued 13 months after the valuation date stands 13 months earlier: ``--block`` adds points
valued at different calendar dates, which shows how frames add and nothing more.  A real
block carries each contract's actual issue year, and its points then share one valuation
date.

``--cython`` runs the compiled model instead of modelx, and prints the same lines.  It is
``DIA_US_SEC_nomx_cy`` beside the model, which the repository's ``tools/build_sec_cy.py``
builds there the first time, and again whenever it is not built for this interpreter or
the model, ``sample_sec.py``, ``spec_sec.py`` or the tool is newer than it: about a
minute, which it says on stderr.  The build is never committed, and ``.gitignore`` covers
everything it leaves.  A ``lifelib.create()`` copy of the library carries no ``tools/``,
wherever it is put, so there ``--cython`` stops, saying so, where it would build.
``--build DIR`` runs the package a build put in ``DIR`` instead, on the CSVs the build
copied there, and never builds.  Either way the runner stops, saying why, if the package
imports without its extension modules, which would compute the same numbers uncompiled.

A block run asks every point for its frame first, then projects each, and releases each
point's ItemSpace once read, so that it holds one point's cells at a time.  Deleting the
ItemSpace is not enough, because it sits in reference cycles that only Python's cyclic
collector frees, so the runner collects after each release, in both passes.  It freezes
everything alive (``gc.freeze``) once the model and its table are read, and again once it
has every point's length, so that each collection scans only what the block has made
since.  The block's sum is kept as it goes, a frame at a time, compensated as pandas'
``groupby`` sum is, so that it is the sum of the frames concatenated and grouped by ``t``,
bit for bit.

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
NAME = "DIA_US_SEC"
SUFFIXES = tuple(importlib.machinery.EXTENSION_SUFFIXES)
USAGE = ("usage: python run_sec.py [point_id | --block] [--cython] [--build DIR]")


def parse(argv):
    """``(point_id or None for the block, cython, build_dir)``, or exit with the usage.

    Any argument but an option is the point's label: ``int`` of it where it reads as a
    whole number, and the text otherwise, which no label of the table matches, so that
    the run refuses it naming the table's labels.
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
        elif arg.startswith("--") or point is not None:
            sys.exit(USAGE)
        else:
            try:
                point = int(arg)
            except ValueError:  # not a number, so no point_id: refused below, by name
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
            print(f"building {NAME} with {tool.name}, which takes about a minute ...",
                  file=sys.stderr)
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
    key = {label: i for i, label in enumerate(table.index)}
else:
    key = {label: label for label in table.index}


def release(label):
    """Drop a point's ItemSpace once read, and collect it (the module docstring)."""
    del model.Projection[key[label]]
    gc.collect()


def add(total, compensation, frame):
    """Add ``frame``'s rows to the running sum's first rows, compensated (Kahan), as
    pandas' ``groupby`` sum adds each group's values in turn."""
    rows = len(frame)
    y = frame - compensation[:rows]
    t = total[:rows] + y
    compensation[:rows] = (t - total[:rows]) - y
    total[:rows] = t


def rows_shown(n, most):
    """What a heading says of the rows printed from a frame of ``n``: at most ``most``."""
    if n == 1:
        return "the one row, t = 0"
    if n <= most:
        return "all {} rows, t = 0..{}".format(n, n - 1)
    return "first {} rows, t = 0..{}".format(most, most - 1)


def shown(df):
    """A frame rounded for printing, with no negative zero: before an annuity commences,
    and after a contract ends, ``net_cf = -liability_cf`` is -0.0, which equals 0."""
    return (df.round(2) + 0.0).to_string()


def lives(proj):
    """The covered lives at issue, ``F60 + M63``, as run.py prints them."""
    text = "{}{}".format(proj.sex(1), proj.age_at_entry(1))
    if proj.is_joint():
        text += " + {}{}".format(proj.sex(2), proj.age_at_entry(2))
    return text


def premiums_due(proj):
    """The premiums still due at the valuation date, by policy month, or ``none``."""
    due = proj.premium_by_mth()
    if not due:
        return "none"
    return ", ".join("{:,.0f} at month {}".format(due[k], k) for k in sorted(due))


def describe(proj):
    """One line on where the point stands at the valuation date."""
    d = proj.duration_mth_init()
    if d < 0:
        return "to be issued at t = {}, {} months after the valuation date".format(-d, -d)
    if d == 0:
        return "issued at the valuation date, t = 0"
    alive = "{:.6g}".format(proj.lives_if_init(1))
    if proj.is_joint():
        alive += " and {:.6g}".format(proj.lives_if_init(2))
    start = proj.income_start_mth()
    if d < start:
        return ("in deferral {} month{}: policy year {}, lives {} alive, premiums paid "
                "{:,.0f}, income bought {:,.2f}/yr, the income starts at t = {}".format(
                    d, "" if d == 1 else "s", proj.policy_year(0), alive,
                    proj.cum_premium_pp_init(), proj.annual_income_init(), start - d))
    paid, left = d - start, max(start + proj.certain_mths_eff() - d, 0)
    return ("in payout {} month{}: policy year {}, lives {} alive, income {:,.2f}/yr, {} "
            "certain month{} left".format(
                paid, "" if paid == 1 else "s", proj.policy_year(0), alive,
                proj.annual_income_init(), left, "" if left == 1 else "s"))


def origin(label):
    """Where the generator took the row from, where the table records it."""
    if "row_kind" not in table.columns:
        return ""
    kind, source, m = (table.at[label, c]
                       for c in ("row_kind", "source_policy_id", "source_mth"))
    if kind == "derived":
        return " (S's {} at its month {})".format(source, m)
    if kind == "future":
        return " (S's {}, issued {} months on)".format(source, -m)
    return " (S's {})".format(source)


if point_id is None:
    # Every point's frame first.  The table checks itself as it is read, but whether a
    # point still owes a payment, and whether the contract covers it, are the product's
    # rules, which proj_len() applies, so a point owing nothing would otherwise stop the
    # run part-way, after the points before it.  A refusal names the point by its label.
    # The model and its table are frozen first, so that the collection after each release
    # scans only what the release left.
    rows = {}
    gc.freeze()
    for label in table.index:
        rows[label] = model.Projection[key[label]].proj_len()
        release(label)
    gc.freeze()
    total, columns = np.zeros((max(rows.values(), default=0), 0)), None
    print("model points, t = 0 the valuation date for each:")
    for label in table.index:
        proj = model.Projection[key[label]]
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
    print("the block, {} (months from the valuation date):".format(
        rows_shown(len(block), 15)))
    print(shown(block.head(15)))
    print()
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", block["pols_if"].groupby(years).first())
    last = min(len(annual), 12)
    print("the block summed into projection year{}, year = t // 12 + 1:".format(
        " 1" if last == 1 else "s 1-{}".format(last)))
    print(shown(annual.head(12)))
else:
    if point_id not in key:
        sys.exit("no model point {} in the table: {}".format(point_id, list(key)))
    label = point_id
    proj = model.Projection[key[label]]
    start = proj.income_start_mth()
    print("model point {}: {}{} - {} {} {} - premiums due {}".format(
        label, table.at[label, "policy_id"], origin(label), proj.market_type(),
        proj.income_form(), lives(proj), premiums_due(proj)))
    print("deferral DB = {}   income starts at policy month {} (attained age {})   "
          "m = {} in {}   COLA = {:.0%}".format(
              proj.db_form(), start, proj.age_at_entry(1) + start // 12,
              proj.payment_freq(), proj.payment_timing(), proj.cola_rate()))
    print("at the valuation date: {}".format(describe(proj)))
    n = proj.proj_len()
    print("proj_len = {} month{} from the valuation date (t = 0..{}); the stop rule at "
          "policy month {}".format(n, "" if n == 1 else "s", n - 1, proj.stop_mth()))
    income = proj.annual_income_payout()
    print("pricing factors = {}   CP(T) = {:,.0f}   B = {:,.2f}/yr = {:,.2f}/instalment   "
          "guarantee = {:.4f} yrs ({} certain months)".format(
              proj.factor_basis(), proj.cum_premium_payout(), income,
              income / proj.payment_freq(), proj.guarantee_yrs(),
              proj.certain_mths_eff()))
    if proj.is_qlac():
        flags = proj.qlac_flags()
        print("QLAC: room at t = {} {:,.0f}   compliance {}".format(
            proj.t_entry(), proj.qlac_room(proj.t_entry()),
            "OK" if not flags else "; ".join(flags)))
    print("net_cf: INCOME POSITIVE (library convention);   "
          "liability_cf = -net_cf: OUTGO POSITIVE")
    print()
    print("{} (months from the valuation date):".format(rows_shown(n, 15)))
    print(shown(proj.result_cf().head(15)))
    print()
    print("counts, survival and payment factors, {}:".format(rows_shown(n, 15)))
    print((proj.result_pols().head(15).round(6) + 0.0).to_string())
    print()
    annual = proj.result_annual()
    first = int(annual.index[0])
    print("annual display grid, policy years {}-{} (the technical notes' worked-example "
          "table, from the valuation date's policy year):".format(
              first, int(annual.index[min(len(annual), 25) - 1])))
    print(annual.head(25).round(2).to_string())
    lo = start - 2 - proj.duration_mth_init()
    if lo >= 0:
        print()
        print("monthly cash flows around the income start date, t = {} to {} (policy "
              "months {} to {}):".format(lo, lo + 5, start - 2, start + 3))
        print(shown(proj.result_cf().loc[lo:lo + 5]))

if not cython:
    model.close()
