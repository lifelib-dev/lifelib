"""Run the RILA_US_SEC model and print a model point's interim values and cash flows.

    python products/registered_index_linked_annuity/run_sec.py          # point 1
    python products/registered_index_linked_annuity/run_sec.py 16       # in force 71 months
    python products/registered_index_linked_annuity/run_sec.py --block  # the block
    python products/registered_index_linked_annuity/run_sec.py 1 --cython  # compiled

``t`` counts months from the valuation date, which is the same instant for every model
point, so row ``t`` of one point's frame is the same month as row ``t`` of any other's, and
a block is the frames summed row by row. On point 1, issued at the valuation date, every
number is the one ``run.py`` prints for ``RILA_US_S``'s point 1; on point 16, the same
contract in force 71 months, row ``t = 0`` is ``RILA_US_S``'s month 71, the worked
example's Term End Date at +40%.

Points are named by their ``point_id``, and ``Projection`` is indexed by a point's position
in the table, as basiclife's BasicTerm_SC is, so the runner maps the one to the other.  It
takes the key from the model: the position where ``Projection`` takes ``idx``, as every
compiled model does, and the label where it takes ``point_id``, as an SEC model does before
its Phase 2.  A label the table lacks, or one that is not a number, is refused, naming the
table's labels.

``--cython`` runs the compiled model instead of modelx, and prints the same lines.  It is
``RILA_US_SEC_nomx_cy`` beside the model, which the repository's ``tools/build_sec_cy.py``
builds there the first time, and again whenever it is not built for this interpreter or
the model, ``sample_sec.py``, ``spec_sec.py`` or the tool is newer than it: about a
minute and a half, which it says on stderr.  The build is never committed, and
``.gitignore`` covers everything it leaves.  A ``lifelib.create()`` copy of the library
carries no ``tools/``, wherever it is put, so there ``--cython`` stops, saying so, where it
would build.  ``--build DIR`` runs the package a build put in ``DIR`` instead, on the CSVs
the build copied there, and never builds.  Either way the runner stops, saying why, if the
package imports without its extension modules, which would compute the same numbers
uncompiled.

The shipped table is a set of test cases, not a block valued at one date: each row
restated in force runs on its own copy of its scenario, re-based to its month, so
``--block`` adds points whose markets differ, which shows how frames add and nothing more.

A block run asks every point for its frame before it projects any, because whether a point
is still in cover, and whether the contract issues it, are the product's rules, which
``proj_len()`` applies, and such a point would otherwise stop the run part-way.  It
releases each point's ItemSpace once it is read, so that it holds one point's cells at a
time: about 6.4 MB a point compiled.  Deleting the ItemSpace is not enough, because it
sits in reference cycles that only Python's cyclic collector frees, so the runner
collects after each release, in both passes.  It freezes everything alive
(``gc.freeze``) once the model and its table are read, and again once it has every
point's length, so that each collection scans only what the block has made since, and it
unfreezes them at the end.  The block's sum is kept as it goes, a frame at a time,
compensated as pandas' ``groupby`` sum is, so that it is the sum of the frames concatenated
and grouped by ``t``, bit for bit.

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
NAME = "RILA_US_SEC"
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
            print(f"building {NAME} with {tool.name}, which takes about a minute and a "
                  f"half ...", file=sys.stderr)
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


def rows_shown(n, most):
    """What a heading says of the rows printed from a frame of ``n``: at most ``most``."""
    if n == 1:
        return "the one row, t = 0"
    if n <= most:
        return "all {} rows, t = 0..{}".format(n, n - 1)
    return "first {} rows, t = 0..{}".format(most, most - 1)


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
            "AV {:,.2f} per contract".format(months(d), proj.duration(0) + 1, proj.age(0),
                                             proj.pols_if(0), proj.av_pp_init()))


def crediting(proj, t):
    """The rate the option in force at month ``t`` credits at: its cap, step or edge."""
    if proj.is_step_crediting():
        return "step rate {:.2%}".format(proj.step_rate(t))
    if proj.is_edge_crediting():
        return "edge rate {:.2%}".format(proj.edge_rate(t))
    cap = proj.cap_rate(t)
    return "uncapped" if cap == float("inf") else "cap {:.2%}".format(cap)


def term_under_way(proj):
    """Where the term in force in the point's first month on the books started."""
    t = proj.t_entry()
    d = proj.duration_mth_init()
    start, level = proj.term_start_month(t), proj.index_at_term_start(t)
    if start < d:
        began = ("began at policy month {}, {} before the valuation date: I_s = {:.2f} "
                 "from the model point".format(start, months(d - start), level))
    else:
        began = ("starts at policy month {}, t = {}: I_s = {:.2f} from the "
                 "scenario".format(start, t, level))
    return "{}, {}".format(began, crediting(proj, t))


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


def iv_rows(proj):
    """The months the decomposition prints: the first on the books, its first
    anniversary, its first term midpoint and its first two Term End Dates."""
    frame = range(proj.t_entry(), proj.proj_len())
    anniv = [t for t in frame if proj.is_anniv(t)][:1]
    mid = [t for t in frame if proj.tau(t) == proj.term_years() / 2.0][:1]
    ends = [t for t in frame if proj.is_term_end(t)][:2]
    return sorted(set([proj.t_entry()] + anniv + mid + ends))


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
        print("  {:>2}  {:<17} {}; proj_len {}".format(
            label, table.at[label, "policy_id"], describe(proj), rows[label]))
        del proj, df
        release(label)                          # each point is read once, then released
    block = pd.DataFrame(total, columns=columns,
                         index=pd.RangeIndex(len(total), name="t"))
    print()
    print("the block, {} (months from the valuation date):".format(
        rows_shown(len(block), 12)))
    print(block.head(12).round(2).to_string())
    print()
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", block["pols_if"].groupby(years).first())
    last = min(len(annual), 12)
    print("the block summed into projection year{}, year = t // 12 + 1:".format(
        " 1" if last == 1 else "s 1-{}".format(last)))
    print(annual.head(12).round(2).to_string())
else:
    label = point_id
    if label not in position:
        sys.exit("no model point {} in the table: {}".format(label, list(position)))
    proj = model.Projection[key(label)]
    print("model point {}: {}{} - {}{} premium {:,.0f}, one {}-year {} option, "
          "buffer {:.0%}".format(
              label, table.at[label, "policy_id"], origin(label), proj.sex(),
              proj.age_at_entry(), proj.premium_pp(), proj.term_years(),
              proj.crediting_type(), proj.buffer()))
    print("interim value family = {} / {}   scenario = {}".format(
        proj.iv_family(), proj.amort_rule(), proj.scenario_id()))
    print("at the valuation date: {}".format(describe(proj)))
    print("term under way: {}".format(term_under_way(proj)))
    n = proj.proj_len()
    print("proj_len = {} from the valuation date (t = 0..{}); the Maturity Date closes "
          "policy month {}, at attained age {}".format(
              months(n), n - 1, proj.maturity_mth() - 1,
              proj.age_at_entry() + proj.policy_term()))
    # The budget is a share of the notional, struck at the term's start; on a term begun
    # before the valuation date the notional entering t_entry() is no longer the one it
    # opened on, a withdrawal since having reduced it, so the amounts are said to be on it.
    t = proj.t_entry()
    notional, beta = proj.inv_amt_basis_pp(t), proj.opt_budget(t)
    print("option budget of the term in force at t = {}: beta = {:.4%}, {:,.2f} on the "
          "notional entering that month, {:,.2f}; the fixed leg {:,.2f}, accreting at "
          "{:.4%}, a {:.2%} spread".format(
              t, beta, beta * notional, notional, notional * (1 - beta),
              proj.fixed_leg_yield(t), proj.nge_spread_implied(t)))
    print()
    print("interim value decomposition in the first month on the books, the first month "
          "ending on an anniversary, the first term midpoint and the first term ends:")
    print(proj.result_iv().loc[iv_rows(proj)].round(2).to_string())
    print()
    print("cash flows, {} (months from the valuation date):".format(rows_shown(n, 12)))
    print(proj.result_cf().head(12).round(2).to_string())

if not cython:
    model.close()
gc.unfreeze()
