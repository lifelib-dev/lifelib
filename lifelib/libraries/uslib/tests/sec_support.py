"""Support for the SEC models' tests: the twin and splice comparisons, and the generator.

USLIB-SEC-PLAN.md puts a ``<Name>_US_SEC`` model beside each ``<Name>_US_S`` (its D1): the S
model taught to run in force at a valuation date, and then to compile.  The S model is not
touched.  It stays the reference, and this module is how the SEC suites lean on it rather
than restate it: every S worked example, its intermediate cells included, becomes an SEC
assertion through a comparison instead of through a second copy of the golden.

What is here, by the plan's tests (its §5.2):

T1, the twin identity
    :func:`sweep` evaluates on an S model point what the conventions suite's sweep
    evaluates and every other ``result_*`` report, and :func:`twin_mismatches` then
    compares every cell of the S model, at every argument tuple the S cell cached inside
    its frame, less :data:`TWIN_EXEMPT_DEFAULT`; an S cell the SEC model lacks is a
    mismatch.  At stage ``"EC"``, and at stage ``"E"`` for a code a product brings
    forward, as ``FIA_US_SEC`` does its phases, :func:`codes` turns S's timing and phase
    strings into the SEC model's int References for the comparison.
T2 and T3, the splice and the future new business
    :func:`temp_inputs` writes a temporary input directory -- the model, its CSVs, extra
    model points and edited tables; :func:`shift_months` re-bases a month-keyed table for
    a point whose valuation date is a later S month; and :func:`frame_mismatches` compares
    two ``result_cf()`` frames on an offset.
T6, regeneration
    :class:`SecSpec` says how one product's SEC model point table derives from its S model,
    :data:`SEC_SPECS` holds one per product, :func:`build_sec_table` builds the table and
    its companions, and :func:`write_generated` and :func:`check_generated` write them, or
    report cell by cell where the committed files have drifted from S.
C2, the Phase 1 fingerprint
    :func:`fingerprint` takes, in brief, what an SEC model computes on every point,
    :func:`fingerprint_text` writes it out as the literal a product module freezes, and
    :func:`fingerprint_mismatches` holds a later version of the model to it (§5.4).
Compiling, for Phase 2's compile tests
    :func:`require_cython` skips a compile test, or fails it in the ``cython`` job, where
    :func:`cython_missing` finds the toolchain missing; :class:`SecBuilds` compiles each
    SEC model once a session, into a temporary directory; :func:`compiled_case` puts a
    build beside a copy of its inputs; and :func:`run_compiled` runs calls on it in a
    child process, on a stack of a given size.  :func:`cython_shards` and
    :func:`cython_shard` split the compile tests among the ``cython`` job's legs.
C3, C4 and C5, and the release
    :func:`reporting_cells` is R17's allowlist, the cells that may stay Python, and
    :func:`data_readers` the ``Data`` cells that read a file, which stay Python too.
    :func:`typing_faults`, :func:`spec_faults` and :func:`c_faults` read a build's
    declarations, its caches against the spec, and its generated C (C3);
    :func:`compiled_mismatches` holds the compiled model to modelx, cell by cell, after a
    :func:`full_sweep` of every point, bit for bit where :func:`exact_here` (C4);
    :func:`static_faults` reads the formulas, and needs no compiler (C5); and
    :func:`release_faults` runs a product's ``run_sec.py --block`` on a compiled block and
    counts the ItemSpaces it keeps (F5).  :func:`object_return_faults` holds the reporting
    cells of :func:`object_cells` to ``object`` in a build's declarations (C3);
    :func:`sample_engine_faults` reads a ``sample_sec.py`` for a call of every engine
    cell; and :func:`block_sum_faults` holds a runner's running sum, :func:`runner_add`,
    to ``groupby``'s, bit for bit.

**Why the generator lives in the tests.**  ``tools/gen_sec_points.py`` is only a command
line over :func:`write_generated` and :func:`check_generated`.  The logic is here because
``lifelib.create()`` copies a library, this ``tests/`` folder with it, but not the
repository's ``tools/``, and T6 has to regenerate inside such a copy too.  A user who edits
an S row in their copy must hear that the SEC table has gone stale from the suite that
ships with the copy, not from a tool they do not have.

**Two clocks, and which way an offset runs.**  Every SEC model point carries
``source_mth``, and SEC month ``t`` is S month ``t + source_mth``: 0 for the twin of an S
new-business row; 108 for the twin of ``WholeLife_US_S`` point 1, which S opens at its own
policy month 108; ``d`` for a row derived from S month ``d``; ``-k`` for a future row
issued ``k`` months after the valuation date.  Both comparisons take their ``t_offset`` in
that one sense, SEC ``t`` against S ``t + t_offset``, so a test passes the row's
``source_mth`` to either: :func:`twin_mismatches` evaluates the SEC cells at S's cached
``t - t_offset``, and :func:`frame_mismatches` reads SEC row ``t`` against S row
``t + t_offset``.  A wrong sign cannot pass quietly: it compares the wrong months, and those
differ.

**What the generator writes.**  The SEC model point table and its companions are input
files as ``CLAUDE.md`` defines them, so none of their cells may name a company or a
product.  The generator copies every text cell from S, where the T6 check keeps it current,
or composes it from S's own keys and a month (``TL-000001-M12``), and it adds no word of its
own beyond a fixed template (D8).  It cannot vouch for S: a name in an S cell is copied.
That is why ``CLAUDE.md``'s pre-commit search still applies to every file it writes.

**Floats in CSV.**  Every file this module writes goes through one writer, for two
properties.  It is deterministic: the same values give the same bytes, so a regeneration
with no S change leaves the committed files alone.  And its floats come back from
``pd.read_csv``, as the models call it, exactly wherever that parser can produce the double
at all, which plain ``repr`` falls well short of.  pandas' default parser keeps at most 17
digits, counts a leading ``0`` among them, and accumulates them in floating point, so it
misreads about a third of the shortest round-trip strings of random doubles (31 to 40 %
over four samples of 20,000 to 30,000) and nearly half of those of counts between 0.9 and
1 (pandas 3.0.5; ``float_precision="round_trip"`` is exact, but no model reader passes it).
So a float is written as its shortest ``repr`` when the default parser reads that back
exactly, and otherwise as the nearest 17-digit string that both the default parser and a
correctly rounding one read as the same double.  For some doubles no such string exists:
the default parser produces them from no text near them.  That is 6 to 9 % of random
doubles, and about one count in six between 0.9 and 1.  Those get the correctly rounded
text the default parser reads closest, which a correct parser reads exactly and the
default parser to within two ulps.  That is far inside the 1e-9 every comparison here
uses, and it never touches a value typed into a table: a short decimal such as ``0.0445``
reads back exactly, so only computed values, a count or a balance carried over from S,
are ever at stake.

**Why T6 reads a float by its value.**  The text chosen for a computed float depends on the
parser it was chosen for, and the float itself on the platform that computed it.  pandas'
parser is C code: a build that contracts its digit loop into fused multiply-adds, as
compilers for arm64 may, reads 15 % of the texts this writer weighs differently and would
pick another text for 7 % of random doubles (measured on a Python model of the parser that
reproduces pandas 3.0.5 on all of 55,000 texts), and a pandas that parses correctly would
pick ``repr`` for every one of them.  And
``pow``, which turns annual rates monthly in every model here, is not rounded alike by
every platform's libm.  So :func:`check_generated` compares a float cell by value, to
1e-12, and :func:`write_generated` leaves a file alone when only such spellings differ: the
suite runs on Linux, Windows and macOS against whichever pandas they install, and a
committed file written on one of them must check clean on the others.
"""
import csv
import dataclasses
import io
import itertools
import math
import numbers
import pathlib
import re
import shutil
from collections.abc import Callable, Mapping

import modelx as mx
import numpy as np
import pandas as pd

from us_registry import MODELS, model_path


# ---------------------------------------------------------------------------
# T1 -- the twin identity


TWIN_EXEMPT_DEFAULT = frozenset({"model_point", "pols_if_init", "input_dir"})
"""The cells whose meaning SEC changes by design, which the twin identity (T1) skips.

``model_point``
    The SEC row carries columns its S twin does not: ``policy_count``, ``duration_mth``,
    ``row_kind``, ``source_policy_id``, ``source_mth`` and any opening state (D5, D6, D8),
    and a renamed column such as ``pols_if_init`` turned ``policy_count``.  The Series
    cannot agree, and nothing is lost by skipping it: whatever the projection reads from it
    reaches T1 through the cells that read it, whether an accessor (``sum_assured``,
    ``age_at_entry``, ...) or a per-``t`` formula that subscripts ``model_point()`` itself,
    as ``WholeLife_US_S.premium_pp_ann(t)`` and ``VUL_US_S.coi_rate(t)`` do.
``pols_if_init``
    SEC's is the count in force *at* the valuation date (D5), so it is 0 for a policy issued
    at ``t = 0``, whose count enters through ``pols_new_biz(0)`` instead.  S's is the count
    at issue.  ``pols_if(0)``, the count that weights row 0, still agrees, and T1 compares
    it.
``input_dir``
    A ``Data`` cell, which T1 meets when it compares two ``Data`` Spaces: two models read
    from two folders resolve it to two directories by construction.  The conventions suite
    asserts it elsewhere, that each model's resolves to its own parent.

A product adds its own exemptions in its :class:`SecSpec`'s ``exempt``, and T1 skips the
union.  Every name added there is a cell T1 no longer checks, so each needs a reason as
specific as these three.  That includes an S cell the SEC model drops or renames, which
:func:`twin_mismatches` otherwise reports as missing.
"""


def codes(proj):
    """The codes an SEC ``Projection`` names, ``{name: int}``: timings, kinds, categories.

    At stage ``"EC"`` an SEC model spells what its S twin spells as text as an int
    Reference named as the text it replaces (USLIB-SEC-PLAN.md R9, R10): a timing,
    ``pols_if_at(t, BEF_DECR)``, and a phase, ``LEVEL``, or a categorical column decoded,
    ``WholeLife_US_SEC``'s premium period, ``TO_100``.  Those are its References whose
    names are all capitals and whose values are ints, bools excepted, and they are what
    this returns.  Passed to :func:`twin_mismatches` as ``codes``, they turn S's strings
    into SEC's ints, in the arguments S cached and in the values S returned.  At stage
    ``"E"`` there are none unless a product brings a code forward, as ``FIA_US_SEC`` does
    its phases (``PRE_ISSUE`` to ``MATURED``, M8); for an S model there are none, and it
    returns ``{}``.

    So every other Reference an SEC model holds is named in lower case, however constant:
    an all-capital int Reference is read as a code.
    """
    return {name: value for name, value in proj.refs.items()
            if name.isupper() and isinstance(value, int) and not isinstance(value, bool)}


def sweep(proj):
    """Evaluate on one model point what T1 compares, and return it.

    That is ``result_cf()`` first, then every other ``result_*`` cells, then every
    ``check_*`` cells except the per-``t`` ``*_resid`` ones.  It is the conventions sweep,
    the ``result_cf()`` and checks that
    ``test_model_conventions.test_every_model_point_projects`` calls on every point, plus
    every other ``result_*`` report, such as ``result_cf_annual()``.

    It exists for T1.  :func:`twin_mismatches` enumerates the argument tuples each S cell
    has cached, so what the S sweep evaluates inside its frame is what T1 covers.  A cell
    the sweep never reaches, such as ``Term_US_S.pols_lapse``, which no result column
    reads, holds no keys and is compared nowhere.  A test that wants more calls the extra
    cells on the S side before it compares.

    Returns ``{name: value}`` in evaluation order, so a caller can assert on the checks
    without calling them a second time.
    """
    names = ["result_cf"]
    names += [c for c in proj.cells if c.startswith("result_") and c != "result_cf"]
    names += [c for c in proj.cells
              if c.startswith("check_") and not c.endswith("_resid")]
    return {name: proj.cells[name]() for name in names}


def _args(key, n_params):
    """The argument tuple behind one modelx cache key.

    ``Cells.keys()`` does not give tuples throughout (found by experiment, modelx 0.33): a
    cells with no parameter is cached under ``()``, a cells with one under the bare argument
    (``5``, not ``(5,)``), and a cells with two or more under the full tuple, defaults
    filled in, so ``claims(3)`` on ``claims(t, kind=None)`` is cached as ``(3, None)``.

    The bare argument of a one-parameter cells may itself be a tuple: ``f(("call",
    "put"))`` is cached under ``("call", "put")``.  Only the parameter count tells that key
    from a two-argument one, which is why the count is passed in, and why the cached value
    is read by calling the cells with these arguments rather than through
    ``Cells.items()``: that looks each key up again by ``cells[key]``, which takes such a
    tuple for two arguments and raises ``TypeError``.
    """
    if n_params == 0:
        return ()
    if n_params == 1:
        return (key,)
    return tuple(key)


def _py(x):
    """A numpy scalar as the Python scalar it holds, so messages read ``1.5``, not
    ``np.float64(1.5)``."""
    return x.item() if isinstance(x, np.generic) else x


def _call(name, args):
    return f"{name}({', '.join(repr(_py(a)) for a in args)})"


def _typed(x):
    return f"{_py(x)!r} ({type(x).__name__})"


def _error_text(err):
    """One line for an exception, unwrapping modelx's ``FormulaError``.

    modelx re-raises any error inside a formula as ``FormulaError``, whose first line is
    always "Error raised during formula execution" and whose second line is the original
    error, ``ValueError: ...``.  The second line is the informative one.
    """
    lines = [line for line in str(err).splitlines() if line.strip()]
    if type(err).__name__ == "FormulaError" and len(lines) > 1:
        return lines[1]
    return f"{type(err).__name__}: {lines[0] if lines else ''}".rstrip(": ")


def _is_bool(x):
    return isinstance(x, (bool, np.bool_))


def _is_number(x):
    """A real number, Python or numpy, that is not a bool.

    ``bool`` is a ``numbers.Real``, and ``True == 1``.  A cells that returned ``True`` in S
    and ``1`` in SEC has changed type, and the house's ``check_*`` contract is that a check
    returns a bool, so bools are compared as bools, never as numbers.
    """
    return isinstance(x, numbers.Real) and not _is_bool(x)


def _close(a, b, rtol, atol):
    """Whether two numbers agree: symmetric, so S against SEC reads as SEC against S.

    Equal values, infinities included, agree, and so do two NaNs.  An infinity agrees with
    nothing else, which the tolerance alone would get wrong: ``|inf - 5| <= rtol * inf``.
    """
    if a == b or (a != a and b != b):
        return True
    if not (math.isfinite(a) and math.isfinite(b)):
        return False
    return abs(a - b) <= atol + rtol * max(abs(a), abs(b))


def _close_arrays(x, y, rtol, atol):
    """:func:`_close`, element by element, on two float arrays of one shape."""
    with np.errstate(invalid="ignore", over="ignore"):
        same = (x == y) | (np.isnan(x) & np.isnan(y))
        finite = np.isfinite(x) & np.isfinite(y)
        near = np.abs(x - y) <= atol + rtol * np.maximum(np.abs(x), np.abs(y))
    return same | (finite & near)


def _numeric(series):
    dtype = series.dtype
    return pd.api.types.is_numeric_dtype(dtype) and not pd.api.types.is_bool_dtype(dtype)


def _few(labels, show):
    """Up to five labels, and how many more there are."""
    labels = list(labels)
    text = ", ".join(show(v) for v in labels[:5])
    return text + (f" and {len(labels) - 5} more" if len(labels) > 5 else "")


def _column_summary(x, y, rtol, atol, show):
    """How two aligned Series differ, in one line, or ``None`` where they agree.

    Numeric Series compare as arrays.  Anything else (a str column, an object column of
    mixed values such as a ``model_point()`` row) compares element by element, as single
    values do.
    """
    xv, yv = x.to_numpy(), y.to_numpy()
    if not len(xv):
        return None
    if _numeric(x) and _numeric(y):
        xf = x.to_numpy(dtype=float, na_value=np.nan)
        yf = y.to_numpy(dtype=float, na_value=np.nan)
        bad = ~_close_arrays(xf, yf, rtol, atol)
        with np.errstate(invalid="ignore", over="ignore"):
            gap = np.abs(yf - xf)
        gap[np.isnan(gap)] = np.inf      # a NaN against a number is the largest gap
    else:
        bad = np.array([bool(_value_diffs(p, q, rtol, atol)) for p, q in zip(xv, yv)],
                       dtype=bool)
        gap = None
    n = int(bad.sum())
    if not n:
        return None
    i = int(np.flatnonzero(bad)[0])
    text = (f"{n} of {len(xv)} differ, first at {show(x.index[i])}: "
            f"S {_py(xv[i])!r}, SEC {_py(yv[i])!r}")
    if gap is not None and n > 1:
        gap[~bad] = -1.0
        j = int(np.argmax(gap))
        text += f"; largest |diff| {gap[j]:.3g} at {show(x.index[j])}"
    return text


def _on_sec_clock(a, b, t_offset):
    """Relabel S's ``t``-indexed pandas value on SEC's clock, and say how to show a label.

    Under an offset an S row ``t`` is SEC row ``t - t_offset``.  Only SEC months at or
    after ``max(0, -t_offset)`` have a counterpart on both sides: none precedes the
    valuation date, and a future point's months before its issue have none in S.  Both
    sides are cut to those months, so the label sets compare like for like.
    """
    name = a.index.name
    if t_offset and name == "t" and b.index.name == "t":
        start = max(0, -t_offset)
        a = a.copy(deep=False)
        a.index = a.index - t_offset
        a, b = a[a.index >= start], b[b.index >= start]
        return a, b, lambda v: f"t={_py(v)} (S t={_py(v) + t_offset})"
    if name is None:
        return a, b, lambda v: repr(_py(v))
    return a, b, lambda v: f"{name}={_py(v)!r}"


def _pandas_diffs(a, b, rtol, atol, t_offset):
    """How two Series, or two DataFrames, differ: label sets first, then values.

    The values compare on the labels both sides hold, with tolerance.  A label or a
    column present on one side only is reported too, rather than dropped from the
    comparison: on a new-business twin the SEC frame must be the S frame, so a row SEC
    never projects is a difference, not a smaller comparison.
    """
    a, b, show = _on_sec_clock(a, b, t_offset)
    lines = []
    frame = isinstance(a, pd.DataFrame)
    if frame:
        only_s = [c for c in a.columns if c not in b.columns]
        only_sec = [c for c in b.columns if c not in a.columns]
        if only_s:
            lines.append(f"columns only in S: {only_s}")
        if only_sec:
            lines.append(f"columns only in SEC: {only_sec}")
        if not only_s and not only_sec and list(a.columns) != list(b.columns):
            lines.append("the same columns in a different order")
        columns = [c for c in a.columns if c in b.columns]
    if a.index.is_unique and b.index.is_unique:
        only_s = a.index.difference(b.index, sort=False)
        only_sec = b.index.difference(a.index, sort=False)
        if len(only_s):
            lines.append(f"{len(only_s)} labels only in S: {_few(only_s, show)}")
        if len(only_sec):
            lines.append(f"{len(only_sec)} labels only in SEC: {_few(only_sec, show)}")
        shared = a.index.intersection(b.index, sort=False)
        a, b = a.loc[shared], b.loc[shared]
    elif not a.index.equals(b.index):
        return lines + ["cannot align: duplicate labels, and the two indexes differ"]
    if frame:
        for c in columns:
            text = _column_summary(a[c], b[c], rtol, atol, show)
            if text:
                lines.append(f"column {c!r}: {text}")
    else:
        text = _column_summary(a, b, rtol, atol, show)
        if text:
            lines.append(text)
    return lines


def _value_diffs(a, b, rtol, atol, t_offset=0):
    """How S's value ``a`` and SEC's value ``b`` differ: descriptions, empty if they agree.

    Numbers, Python or numpy, compare with tolerance; bools, strings, ``None`` and paths
    compare exactly; Series and DataFrames compare on their shared labels with tolerance
    (:func:`_pandas_diffs`); arrays, lists, tuples, dicts and sets compare element by
    element.  Those are every kind of value the twelve S models cache (surveyed over the
    first point of each: floats, ints, bools and strings, Series and DataFrames, one dict
    in ``DIA_US_S``, one tuple in ``RILA_US_S``, a list in ``VA_US_S`` and ``VUL_US_S``).

    Two values of different known kinds, a ``str`` against an ``int``, simply differ.  A
    value of a kind not listed is reported as *uncomparable* rather than passed: a check
    that cannot look at a value has not shown it equal.
    """
    if _is_bool(a) or _is_bool(b):
        if _is_bool(a) and _is_bool(b) and bool(a) == bool(b):
            return []
        return [f"S {_typed(a)}, SEC {_typed(b)}"]
    if _is_number(a) and _is_number(b):
        if _close(a, b, rtol, atol):
            return []
        with np.errstate(invalid="ignore", over="ignore"):
            return [f"S {_py(a)!r}, SEC {_py(b)!r}, diff {_py(b) - _py(a):+.3g}"]
    if isinstance(a, str) and isinstance(b, str):
        return [] if a == b else [f"S {a!r}, SEC {b!r}"]
    if a is None and b is None:
        return []
    if isinstance(a, pathlib.PurePath) and isinstance(b, pathlib.PurePath):
        return [] if a == b else [f"S {str(a)!r}, SEC {str(b)!r}"]
    if isinstance(a, pd.DataFrame) and isinstance(b, pd.DataFrame):
        return _pandas_diffs(a, b, rtol, atol, t_offset)
    if isinstance(a, pd.Series) and isinstance(b, pd.Series):
        return _pandas_diffs(a, b, rtol, atol, t_offset)
    if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
        if a.shape != b.shape:
            return [f"shape: S {a.shape}, SEC {b.shape}"]
        # As nested lists, or as the scalar a 0-d array holds, each compared as its kind.
        return _value_diffs(a.tolist(), b.tolist(), rtol, atol)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            return [f"length: S {len(a)}, SEC {len(b)}"]
        return [f"[{i}] {line}" for i, (x, y) in enumerate(zip(a, b))
                for line in _value_diffs(x, y, rtol, atol)]
    if isinstance(a, Mapping) and isinstance(b, Mapping):
        lines = []
        only_s = [k for k in a if k not in b]
        only_sec = [k for k in b if k not in a]
        if only_s:
            lines.append(f"keys only in S: {_few(only_s, repr)}")
        if only_sec:
            lines.append(f"keys only in SEC: {_few(only_sec, repr)}")
        return lines + [f"[{k!r}] {line}" for k in a if k in b
                        for line in _value_diffs(a[k], b[k], rtol, atol)]
    if isinstance(a, (set, frozenset)) and isinstance(b, (set, frozenset)):
        return [] if a == b else [f"S {a!r}, SEC {b!r}"]
    if _known(a) and _known(b):
        return [f"S {_typed(a)}, SEC {_typed(b)}"]
    return [f"uncomparable: S {type(a).__name__}, SEC {type(b).__name__}"]


_KNOWN_KINDS = (str, pathlib.PurePath, pd.DataFrame, pd.Series, np.ndarray, list, tuple,
                Mapping, set, frozenset)


def _known(x):
    """Whether :func:`_value_diffs` knows how to compare a value of this kind."""
    return x is None or _is_bool(x) or _is_number(x) or isinstance(x, _KNOWN_KINDS)


def _frame_end(space):
    """S's ``proj_len()``, the exclusive end of its frame, or ``None`` if it has none.

    Every model's ``Projection`` has the cell, and a ``Data`` Space or a synthetic one need
    not.  It is read, never compared here: a comparison may exempt it, as the splice does.
    """
    cells = space.cells
    if "proj_len" not in cells or cells["proj_len"].parameters:
        return None
    return cells["proj_len"]()


def _is_month(x):
    return isinstance(x, numbers.Integral) and not _is_bool(x)


def _twin_lines(s_proj, sec_proj, exempt, arg_map, t_offset, rtol, atol, codes=None):
    """Every mismatch line, lazily, so :func:`twin_mismatches` can stop at its limit."""
    sec_cells = sec_proj.cells
    end = _frame_end(s_proj)
    for name in list(s_proj.cells):
        if name in exempt:
            continue
        if name not in sec_cells:
            yield (f"{name}: a cell of S that SEC lacks; a cell SEC drops by design is "
                   f"named in the spec's exempt, with its reason")
            continue
        s_cells, cells = s_proj.cells[name], sec_cells[name]
        n_params = len(s_cells.parameters)
        s_t_pos = s_cells.parameters.index("t") if "t" in s_cells.parameters else None
        params = cells.parameters
        t_pos = params.index("t") if "t" in params else None
        for key in list(s_cells.keys()):
            args = _args(key, n_params)
            if (end is not None and s_t_pos is not None and s_t_pos < len(args)
                    and _is_month(args[s_t_pos]) and args[s_t_pos] >= end):
                continue                        # read ahead of S's frame: not compared
            expected = s_cells(*args)           # a cached key: the cache, not a new value
            sec_args = args if arg_map is None else arg_map(name, args)
            if sec_args is None:
                continue
            sec_args = tuple(codes.get(a, a) if codes and isinstance(a, str) else a
                             for a in sec_args)
            if t_pos is not None and t_pos < len(sec_args):
                t = sec_args[t_pos]
                if _is_month(t):
                    t = int(t) - t_offset
                    if t < 0:
                        continue
                    sec_args = sec_args[:t_pos] + (t,) + sec_args[t_pos + 1:]
            label = _call(name, args)
            if sec_args != args:
                label += f" [SEC {_call(name, sec_args)}]"
            try:
                actual = cells(*sec_args)
            except Exception as err:            # reported, so the sweep goes on
                yield f"{label}: SEC raised {_error_text(err)}"
                continue
            if (codes and isinstance(expected, str) and expected in codes
                    and _is_month(actual)):
                code = codes[expected]          # S's label against SEC's code (R10)
                for line in _value_diffs(code, actual, rtol, atol, t_offset):
                    yield f"{label}: S {expected!r} is code {code}; {line}"
                continue
            for line in _value_diffs(expected, actual, rtol, atol, t_offset):
                yield f"{label}: {line}"


def twin_mismatches(s_proj, sec_proj, *, exempt=TWIN_EXEMPT_DEFAULT, arg_map=None,
                    t_offset=0, rtol=1e-9, atol=1e-9, limit=50, codes=None):
    """Where the SEC model differs from its S twin, cell by cell: T1 (§5.2).

    For every cells name of the S Space not in ``exempt``, and for every argument tuple the
    S cells has cached inside S's frame, the SEC cells is evaluated at the same arguments
    and its value compared with the value S cached.  So the S Space must be swept first
    (:func:`sweep`), and what the sweep reached inside the frame is what is compared.  The
    S cache is read, never re-evaluated.  Through this, the S goldens are asserted on the
    SEC model too, with no number restated, wherever they sit on a cells the sweep
    reaches: ``result_cf()``, and intermediate cells such as MYGA's surrender trace.  An S
    cells the SEC Space lacks is reported, one line for the cells, rather than left out of
    the comparison: a cells renamed or dropped would otherwise take its goldens with it
    without a word.  One the SEC model drops by design is named in ``exempt``, with its
    reason, as any other exemption is.

    Only S's own frame is compared.  Where S has a ``proj_len()`` cell, as every model's
    ``Projection`` does, a key whose S ``t`` is at or past it is skipped.  S evaluates such
    a month only when a formula reads ahead of its frame, as ``Term_US_S.jump_ratio()``
    reads ``premium_pp_ann(12n)`` on a point whose cover ends with the level period, or
    ``conv_rate`` reads ``conv_elig(t + 12)`` near expiry, and it answers from its tables
    as though cover went on, where an SEC model answers that the month is outside cover
    (R1).  S's frame ends where cover ends, on either clock, and :func:`frame_mismatches`
    holds the two frames' ends together.

    ``s_proj`` and ``sec_proj`` are usually ItemSpaces, ``Projection[1]`` of each model, but
    any two Spaces work, ``Data`` against ``Data`` included.

    The arguments are mapped before the SEC call.  ``arg_map(name, args)`` returns SEC's
    arguments for S's (the default is the identity); returning ``None`` skips that key.
    Then, with ``codes``, :func:`codes` of the SEC Space, each string argument that names
    a code is passed as that code: S's ``pols_if_at(t, "BEF_DECR")`` is SEC's
    ``pols_if_at(t, BEF_DECR)`` (R9).  And a string S returned that names a code is
    compared with SEC's value as that code, where SEC returned an int: S's ``"LEVEL"``
    against SEC's ``LEVEL`` (R10).  A string SEC still returns, such as a label accessor's
    ``"M"``, is compared as a string.  Then the argument named ``t``, if the SEC cells has
    one, moves to SEC's clock: SEC month ``t`` is S month ``t + t_offset``, as in
    :func:`frame_mismatches`, so the SEC cells is called at S's ``t - t_offset``, and a
    row passes its ``source_mth`` (``d`` for a row derived from S month ``d``; see the
    module docstring).  A key whose SEC ``t`` falls below 0 is
    skipped: no month precedes the valuation date, and R1 forbids evaluating one.  Under an
    offset a ``t``-indexed Series or DataFrame, such as ``result_cf()``, is relabelled the
    same way before it is compared.  Only the
    parameter named ``t`` moves.  Another that holds a month, such as the creation month
    ``m`` of ``IUL_US_S``'s ``seg_bal_pp(t, m)``, which ``IUL_US_SEC`` keys by slot,
    moves through ``arg_map``.

    Values compare by kind (:func:`_value_diffs`): numbers with ``rtol`` and ``atol``,
    symmetrically; bools and strings exactly; pandas values on their shared labels, with
    any label or column found on one side only reported too; containers element by
    element; anything else as *uncomparable*.  An exception the SEC cells raises is
    reported, not propagated, so one broken cells does not hide the rest.

    Returns readable lines, in cells and cache order, empty when the twins agree:
    ``"expenses(0): S 302.5, SEC 302.5833333333333, diff +0.0833"``.  At most ``limit``
    are returned.  When more were found, the scan stops there, so a model that differs
    everywhere fails fast, and the last line says so, unless ``limit`` is 1: then the one
    line is the first mismatch.
    """
    if limit < 1:
        raise ValueError(f"limit must be at least 1, not {limit}")
    found = []
    for line in _twin_lines(s_proj, sec_proj, exempt, arg_map, t_offset, rtol, atol,
                            codes):
        found.append(line)
        if len(found) > limit:
            break
    if len(found) > limit:
        found = found[:limit]
        if limit > 1:
            found[-1] = (f"(more than {limit - 1} mismatches; the scan stopped, and the "
                         f"rest are not listed)")
    return found


def frame_mismatches(s_df, sec_df, *, t_offset=0, columns=None, rtol=1e-9, atol=1e-9):
    """Where two ``result_cf()`` frames differ, SEC row ``t`` being S row ``t + t_offset``.

    The splice (T2) and future new business (T3) compare whole frames on an offset: a row
    derived from S month ``d`` reproduces S from ``d`` on, so its row ``t`` is S's row
    ``t + d``, and ``t_offset=d``.  That is the direction of ``source_mth``, and the one
    :func:`twin_mismatches` takes too, so a test passes a row's ``source_mth`` to both.

    The comparison runs over ``columns``, or by default every column both frames hold, and
    over the shared ``t`` range: from the later first row to the earlier last row, on SEC's
    labels.  Rows before that range are not compared, because they are the part one side
    does not project by design: S's months before the splice, or the pre-issue zeros of a
    future point.  The two frames' *ends* have no such excuse.  Each runs to the end of
    cover, which is one instant on both clocks: S's last row ``L - 1`` is SEC's ``L - 1 -
    d`` for a row derived at ``d``, and ``L - 1 + k`` for one issued ``k`` months late.  So
    frames that end apart are reported, as an SEC ``proj_len()`` that is wrong, even though
    the rows they share agree.  So is a row *inside* the range that one frame lacks, an
    empty range, an explicitly named column either frame lacks, or a comparison left with
    no column at all: a comparison that compares less than the whole splice cannot pass.
    To compare part of a frame, cut both frames to it.

    Returns one line per column that differs, with the count, the first differing row and
    the largest gap, after any line about the frames' shape; empty when the frames agree.
    """
    s_view = s_df.copy(deep=False)
    s_view.index = s_df.index - t_offset
    lines = []
    if columns is None:
        columns = [c for c in s_df.columns if c in sec_df.columns]
    else:
        columns = list(columns)
        for side, df in (("S", s_df), ("SEC", sec_df)):
            missing = [c for c in columns if c not in df.columns]
            if missing:
                lines.append(f"columns missing from {side}: {missing}")
        columns = [c for c in columns if c in s_df.columns and c in sec_df.columns]
    if not columns:
        return lines + ["no column to compare"]
    if not len(s_view) or not len(sec_df):
        return lines + [f"no rows to compare: S has {len(s_df)}, SEC {len(sec_df)}"]
    lo = max(s_view.index.min(), sec_df.index.min())
    hi = min(s_view.index.max(), sec_df.index.max())
    if lo > hi:
        return lines + [
            f"no shared rows: S rows {s_df.index.min()}..{s_df.index.max()} are SEC "
            f"t = {s_view.index.min()}..{s_view.index.max()}, and SEC has "
            f"t = {sec_df.index.min()}..{sec_df.index.max()}"]

    def show(t):
        t = _py(t)
        return f"t={t} (S t={t + t_offset})" if t_offset else f"t={t}"

    if s_view.index.max() != sec_df.index.max():
        lines.append(f"the frames end apart: S ends at {show(s_view.index.max())}, SEC at "
                     f"t={_py(sec_df.index.max())}")
    a = s_view[(s_view.index >= lo) & (s_view.index <= hi)]
    b = sec_df[(sec_df.index >= lo) & (sec_df.index <= hi)]
    for side, mine, other in (("S", a, b), ("SEC", b, a)):
        gaps = mine.index.difference(other.index, sort=False)
        if len(gaps):
            lines.append(f"{len(gaps)} rows inside the shared range only in {side}: "
                         f"{_few(gaps, show)}")
    shared = a.index.intersection(b.index, sort=False)
    for c in columns:
        text = _column_summary(a.loc[shared, c], b.loc[shared, c], rtol, atol, show)
        if text:
            lines.append(f"column {c!r}: {text}")
    return lines


# ---------------------------------------------------------------------------
# Writing CSV -- deterministic, and exact for the models' own reader


def _default_reads(texts):
    """The doubles ``pd.read_csv``'s default parser makes of some float texts.

    The models read every input with a plain ``pd.read_csv(path, index_col=...)``, the C
    parser at its default ``float_precision``, so this is the reading that matters.
    """
    if not texts:
        return []
    buf = io.StringIO("v\n" + "\n".join(texts) + "\n")
    return pd.read_csv(buf, dtype={"v": "float64"})["v"].tolist()


def _candidates(v):
    """17-digit texts near ``v`` that a correctly rounding parser reads as ``v``.

    The nearest first.  Each keeps all 17 digits and no leading zero, so pandas' parser,
    which counts at most 17 digits, leading zeros included, sees every one of them: fixed
    notation from 1 up to 1e16, scientific otherwise.  Which of them the default parser
    also reads as ``v`` is for :func:`_float_texts` to find out.
    """
    sign = "-" if v < 0 else ""
    mantissa, exponent = f"{abs(v):.16e}".split("e")
    n0, e10 = int(mantissa.replace(".", "")), int(exponent)
    out = []
    for j in sorted(range(-12, 13), key=lambda j: (abs(j), j)):
        digits = str(n0 + j)
        if len(digits) != 17:
            continue
        if 0 <= e10 < 16:
            body = digits[:e10 + 1] + "." + digits[e10 + 1:]
        else:
            body = f"{digits[0]}.{digits[1:]}e{e10:+03d}"
        if float(sign + body) == v:
            out.append(sign + body)
    return out


def _float_texts(values):
    """The text written for each float: exact for the models' reader wherever possible.

    The shortest ``repr`` where pandas' default parser reads it back exactly, which covers
    every value that came from a short decimal.  Otherwise the nearest 17-digit text that
    both that parser and a correctly rounding one read as the same double, found by
    asking pandas.  Where none exists, whichever of these correctly rounded texts the
    default parser reads closest.  That is rarely the ``repr``: a fixed-notation ``repr``
    such as ``0.00012345678901234567`` spends four of pandas' 17 digits on leading zeros,
    and reads thousands of ulps off, where its 17-digit scientific form reads within a
    few.
    """
    values = [float(v) for v in values]
    texts = [repr(v) for v in values]
    probe = [i for i, v in enumerate(values) if math.isfinite(v) and v != 0.0]
    first = dict(zip(probe, _default_reads([texts[i] for i in probe])))
    misread = [i for i in probe if first[i] != values[i]]
    if misread:
        options = {i: _candidates(values[i]) for i in misread}
        reads = iter(_default_reads([c for i in misread for c in options[i]]))
        for i in misread:
            v = values[i]
            read = [(texts[i], first[i])] + [(c, next(reads)) for c in options[i]]
            exact = [c for c, r in read[1:] if r == v]
            texts[i] = exact[0] if exact else min(read, key=lambda cr: abs(cr[1] - v))[0]
    return texts


def _csv_text(df):
    """The CSV text of ``df``, exactly as every file this module writes is written.

    The index is written as leading columns when it is named, as a table the models read
    with ``index_col="point_id"`` is, and left out when it is a default, unnamed one.  The
    rest is the house's CSV dialect: a header, ``\\n`` line ends, a blank for a missing
    value, ``True`` and ``False``, integers as integers, and floats from
    :func:`_float_texts`.
    """
    frame = df.reset_index() if any(n is not None for n in df.index.names) else df
    cells = frame.to_numpy(dtype=object)
    rows = [["" for _ in range(cells.shape[1])] for _ in range(cells.shape[0])]
    floats = []
    for i, j in itertools.product(range(cells.shape[0]), range(cells.shape[1])):
        v = cells[i, j]
        if v is None or v is pd.NA or v is pd.NaT:
            continue
        if _is_bool(v):
            rows[i][j] = "True" if v else "False"
        elif isinstance(v, numbers.Integral):
            rows[i][j] = str(int(v))
        elif isinstance(v, numbers.Real):
            if v == v:                          # a NaN stays blank
                floats.append((i, j))
        else:
            rows[i][j] = str(v)
    for (i, j), text in zip(floats, _float_texts([cells[i, j] for i, j in floats])):
        rows[i][j] = text
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow([str(c) for c in frame.columns])
    writer.writerows(rows)
    return buf.getvalue()


def _write_csv(df, path):
    """Write ``df`` as :func:`_csv_text` renders it, byte for byte on every platform."""
    pathlib.Path(path).write_bytes(_csv_text(df).encode("utf-8"))


# ---------------------------------------------------------------------------
# T2 and T3 -- the splice harness


def temp_inputs(tmp_dir, model_dir, *, model_points=None,
                model_point_file="model_point_table.csv", edits=None):
    """Copy a model and its inputs into ``tmp_dir``, with changes; return the model folder.

    The uslib layout puts a model's inputs beside it, as CSVs in the model folder's parent,
    and ``Data.input_dir()`` resolves to wherever the model was read from.  So a model read
    from a temporary folder reads that folder's CSVs, and a test can project against
    changed inputs without touching the tree.  The splice (T2) needs exactly that: extra
    model points opened with S's state at ``d``, and valuation-clock inputs shifted by
    ``d`` (:func:`shift_months`).

    The model folder is copied without ``__pycache__``, and every CSV in its parent
    directory beside it, byte for byte.  Then:

    ``model_points``
        a DataFrame written over ``model_point_file`` (which may be new: an SEC test can
        write an SEC table that is not committed yet).  Index it by ``point_id``, as the
        models' readers do, or give ``point_id`` as a column on a default index; a named
        index is written as columns, a default one is left out.
    ``edits``
        ``{filename: DataFrame}`` written over that file, or ``{filename: callable}``,
        which receives the file as ``pd.read_csv(path)`` reads it, a plain table on a
        default index, and returns the table to write.  An edit must name a file the copy
        holds, so a misspelt name raises instead of writing a file no model reads.  Edits
        apply after ``model_points``.

    What is written comes back as the models read it.  The writer chooses float texts that
    pandas' default parser reads as the same double wherever that parser can produce it,
    and within two ulps where it cannot, which for a computed count just below 1 is about
    one value in six (module docstring).  It writes integers, bools, blanks and strings as
    plain text, which reads back as itself.  The one exception is a string pandas takes for
    a missing value, such as ``NA`` or the empty string, which it takes for one in any CSV.
    A file that is not written is a byte copy.

    Returns the copied model folder, ready for ``mx.read_model``.  modelx keeps models in
    one registry, so read it under a name of its own, and close it.
    """
    tmp_dir, model_dir = pathlib.Path(tmp_dir), pathlib.Path(model_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    dest = tmp_dir / model_dir.name
    shutil.copytree(model_dir, dest, ignore=shutil.ignore_patterns("__pycache__"),
                    dirs_exist_ok=True)
    for csv_path in sorted(model_dir.parent.glob("*.csv")):
        if csv_path.is_file():
            shutil.copy2(csv_path, tmp_dir / csv_path.name)
    if model_points is not None:
        _write_csv(model_points, tmp_dir / model_point_file)
    for name, edit in (edits or {}).items():
        path = tmp_dir / name
        if not path.is_file():
            raise FileNotFoundError(
                f"edits names {name!r}, but the copy of {model_dir.parent} holds no such "
                f"file")
        frame = edit(pd.read_csv(path)) if callable(edit) else edit
        if not isinstance(frame, pd.DataFrame):
            raise TypeError(f"the edit for {name!r} produced a "
                            f"{type(frame).__name__}, not a DataFrame")
        _write_csv(frame, path)
    return dest


def shift_months(df, month_col, d, *, by=(), step=True):
    """Re-base a month-keyed table for a point whose SEC ``t = 0`` is S month ``d``.

    S reads such a table at its own month ``m``; the SEC point reads it at ``t = m - d``.
    So rows at months ``m >= d`` move to ``m - d``.  What happens to the rows before ``d``
    depends on how the model reads the table, and there are two readings.

    ``step=True``, a step function
        The row in force at ``t`` is the last one at or before ``t``: a rate or return
        scenario declared from a month on, a step-filled schedule.  Then the row in force at
        month ``d`` must survive the cut, or the re-based table holds nothing in force from
        month 0 up to its next row.  So where no row sits at exactly ``d``, the last rows
        before ``d`` become month 0.  "Rows", because several share that month when the
        table has another key not named in ``by``, and all of them were in force.  That
        holds only while those keys step on the same months: "a row at exactly ``d``" is
        asked of the whole group, so a scenario with a row at ``d`` would cost another
        scenario, which has none there, its row in force.  A key that steps on months of
        its own is named in ``by``.
    ``step=False``, exact months
        A row applies in its own month only: a transaction schedule, a premium or a
        withdrawal at month ``m``.  Rows before ``d`` have already happened, and their
        effect is in the opening state, not the table, so they are dropped.

    ``by`` names grouping columns, such as a scenario id or a subaccount, whose rows are
    re-based separately, each with its own row in force.  The month column must be a
    column, not the index; rows keep their order and their index labels.

    A negative ``d`` re-bases for a future point issued ``-d`` months after the valuation
    date (T3): every row moves later by ``-d``, and months ``0 .. -d - 1`` are left without
    a row.  They are the point's pre-issue months, which no formula may read (D4), so a read
    there fails loudly rather than finding a value invented for it.
    """
    by = [by] if isinstance(by, str) else list(by)
    months = df[month_col]
    if months.isna().any():
        raise ValueError(f"{month_col!r} has a blank month; a month-keyed table cannot "
                         f"be re-based around one")
    m = months.to_numpy()
    keep = m >= d
    new = m - d
    if step:
        groups = (df.groupby(by, sort=False, dropna=False).indices.values() if by
                  else [np.arange(len(df))])
        for positions in groups:
            mine = m[positions]
            if (mine == d).any():
                continue
            before = positions[mine < d]
            if len(before):
                carried = before[m[before] == m[before].max()]
                keep[carried] = True
                new[carried] = 0
    out = df.iloc[np.flatnonzero(keep)].copy()
    out[month_col] = new[keep]
    return out


# ---------------------------------------------------------------------------
# T6 -- the generated SEC inputs


# The columns the generator writes, and only the generator: neither an S table nor a spec's
# state may supply them.  ``duration_mth`` is the twin's, from ``duration_of``, moved on by
# ``d - source_mth`` for a derived row and set to ``-k`` for a future one.  ``provenance``
# is S's on a twin and composed from S's keys on the other rows (D8), so no extractor may
# write one either: that is the text ``CLAUDE.md`` holds to citing by key.
GENERATED_COLUMNS = ("row_kind", "source_policy_id", "source_mth")
_RESERVED = frozenset({"point_id", "policy_id", "duration_mth", "provenance",
                       *GENERATED_COLUMNS})


def _issued_at_valuation(row):
    """The default ``duration_of``: the S row is new business, issued at ``t = 0``."""
    return 0


@dataclasses.dataclass(frozen=True)
class SecSpec:
    """How one product's SEC model point table and its companions derive from S (D6, D8).

    The SEC table has three kinds of row, all generated, none typed (D8), and each row says
    which it is in ``row_kind``:

    ``"twin"``
        every S row, under its own ``point_id`` and ``policy_id``.  A new-business twin is
        what T1 compares; the twin of an S row already in force is a splice case.
    ``"derived"``
        an S row restated in force at S month ``d``, opened with S's own state there.  T2
        projects it against S from ``d`` on.
    ``"future"``
        an S new-business row issued ``k`` months after the valuation date (D4), T3's case.

    Every row carries ``policy_count``, ``duration_mth`` (months in force at ``t = 0``,
    negative for future new business), ``row_kind``, ``source_policy_id`` (the S policy it
    comes from) and ``source_mth``, where SEC ``t`` is S ``t + source_mth``.

    Fields:

    ``twin``
        the S model's name, as registered in ``us_registry.MODELS``.
    ``column_map``
        S column to SEC column, merged over the default ``{"pols_if_init":
        "policy_count"}`` (D5).  ``None`` drops a column whose meaning an SEC column takes
        over, such as ``Term_US_S``'s ``duration_inforce``, a count of years that
        ``duration_mth`` replaces (D6).  ``point_id`` and ``policy_id`` are never renamed.
    ``duration_of``
        S row (a Series, S column names, named by its ``point_id``) to its twin's
        ``duration_mth``: ``12 * row["duration_inforce"]`` on WholeLife,
        ``row["duration_mth"]`` on UL.  The default says every S row is new business.
    ``derived``
        ``(S point_id, d)`` pairs, in the order the rows are written.
    ``future``
        ``(S point_id, k)`` pairs; each S point must be new business.
    ``state``
        SEC column to ``callable(s_proj, d)``, the opening-state extractors of D6, for the
        derived rows.  Each returns the value S carries into month ``d``, before any
        month-``d`` event.  ``policy_count`` may be among them: its default,
        ``s_proj.pols_if(d)``, is the wrong count for SPIA, whose ``pols_if`` is a closing
        measure (D5).  The columns the generator owns may not: the two ids,
        ``duration_mth``, ``provenance`` and the three it adds, ``row_kind``,
        ``source_policy_id`` and ``source_mth``.
    ``twin_state``
        SEC column to ``callable(s_proj, d)`` for the twin rows, called with ``d`` the
        twin's ``source_mth``: the opening state S itself assumes, so the twin reproduces S.
        UL is the use: S restarts ``cum_prem`` at 0 on its in-force point 3, so that
        point's twin opens with ``cum_prem_init = 0``.  A future row copies its twin's
        values, but for those ``future_state`` sets.  A state column with no
        ``twin_state`` entry is blank on the twins.  And a
        ``twin_state`` column with no ``state`` entry is copied to the derived rows from
        their twin, which is right only for a quantity fixed at issue (a locked rate, a
        solved premium: D6); anything that moves after issue needs a ``state`` entry.
    ``exempt``
        extra cells T1 skips, beyond :data:`TWIN_EXEMPT_DEFAULT`, each for a stated reason,
        an S cell the SEC model drops or renames among them.
    ``twin_arg_map``
        ``callable(name, args)``, or ``None``: the ``arg_map`` T1 passes to
        :func:`twin_mismatches`, for an SEC cell that takes S's arguments otherwise than
        by :func:`codes`, which maps S's strings alone.  At stage ``"EC"``: S's ``None``
        for a total, where SEC's cell takes a code for it, ``claims(t, None)`` as
        ``claims(t, "ALL")``, which ``codes`` then maps (R12); or S's ``(t, m)`` keys
        re-keyed by slot, ``(t, t - m)`` (R15).  ``None``, the default, leaves S's
        arguments as they are.
    ``future_state``
        SEC column to ``callable(s_proj, k)`` for the future rows: S point ``p``'s
        projection and the months ``k`` after the valuation date the row is issued.  A
        future row copies its twin's values, but for these.  FIA is the use: a future
        row's scenario is a copy of S's moved ``k`` months later, ``{id}-F{k}``, which its
        twin's id cannot name.  A column S lacks, and neither ``state`` nor
        ``twin_state`` sets, is blank on the twins and the derived rows.  It may not set
        ``policy_count``, or any column the generator owns.
    ``model_state``
        ``callable(s_model)``, or ``None``: more state columns, whose names the S model's
        inputs give, as SEC column to ``callable(s_proj, d)``.  It is called as the table
        is built, with the S model the generator reads, and each column it gives is set
        on the twins at their ``source_mth`` and on the derived rows at ``d``, as
        ``twin_state`` and ``state`` set theirs, a future row copying its twin's.  Its
        columns come before ``twin_state``'s.  VA is the use: a subaccount value for each
        subaccount S's fund table holds, so that a fund table given a subaccount gives
        the table its column.  It may not set ``policy_count``, a column the generator
        owns, or one ``state`` or ``twin_state`` sets, which is checked as it is called.
    ``companions``
        companion filename to ``callable(s_model, table)``, which builds that file from the
        S model and the finished SEC table (a copy, free to modify): DIA's premium schedule,
        FIA's rate scenarios and RILA's market scenarios re-based to each row, and VA's
        two re-based scenarios (D8).
    ``model_point_file``
        the SEC table's own filename.

    Every file the spec writes ends ``_sec.csv``, which is checked here.  The SEC model
    shares its directory with the S model's inputs, and the suffix is what guarantees the
    generator can never write over one of them (D8: "never into the shared S inputs").
    And no companion may take the table's own name, which would silently replace the
    table with the companion.
    """
    twin: str
    column_map: Mapping[str, str | None] = dataclasses.field(default_factory=dict)
    duration_of: Callable[[pd.Series], int] = _issued_at_valuation
    derived: tuple[tuple[int, int], ...] = ()
    future: tuple[tuple[int, int], ...] = ()
    state: Mapping[str, Callable] = dataclasses.field(default_factory=dict)
    twin_state: Mapping[str, Callable] = dataclasses.field(default_factory=dict)
    exempt: frozenset[str] = frozenset()
    companions: Mapping[str, Callable] = dataclasses.field(default_factory=dict)
    model_point_file: str = "model_point_table_sec.csv"
    twin_arg_map: Callable | None = None
    future_state: Mapping[str, Callable] = dataclasses.field(default_factory=dict)
    model_state: Callable | None = None

    def __post_init__(self):
        for filename in (self.model_point_file, *self.companions):
            if not str(filename).endswith("_sec.csv"):
                raise ValueError(
                    f"{filename!r}: a generated SEC input is named *_sec.csv, so that it "
                    f"can never overwrite an S input in the same directory")
        if self.model_point_file in self.companions:
            raise ValueError(
                f"{self.model_point_file!r} is both the SEC table and a companion; the "
                f"companion would replace the table")
        for field_name, extractors, reserved in (
                ("state", self.state, _RESERVED),
                ("twin_state", self.twin_state, _RESERVED | {"policy_count"}),
                ("future_state", self.future_state, _RESERVED | {"policy_count"})):
            clash = sorted(set(extractors) & reserved)
            if clash:
                raise ValueError(
                    f"{field_name} may not set {clash}: the generator owns them")
        object.__setattr__(self, "derived",
                           tuple((int(p), int(d)) for p, d in self.derived))
        object.__setattr__(self, "future",
                           tuple((int(p), int(k)) for p, k in self.future))
        object.__setattr__(self, "exempt", frozenset(self.exempt))


def _wl_entering(name, opening):
    """What ``WholeLife_US_S`` carries into month ``d`` in cells ``name``.

    The closing value of month ``d - 1``, or, where month ``d`` opens S's frame, the
    opening value S's own formulas read there: ``pua_face(t - 1) if t > proj_start() else
    puaf_inforce()``, and the same for the loan and the accumulation balance.
    """
    def extract(s, d):
        return getattr(s, name)(d - 1) if d > s.proj_start() else opening(s)
    return extract


def _wl_at_prev_anniv(name, opening):
    """``WholeLife_US_S``'s cells ``name`` at the anniversary on or before month ``d``.

    The close of S's month ``anniv_mth(d) - 12``, the month whose end opened the policy year
    containing ``d``, or S's opening value where that month is before S's frame: S's own
    ``x(t - 12) if t - 12 >= proj_start() else <opening>``, read at the year's anniversary.
    """
    def extract(s, d):
        m = s.anniv_mth(d) - 12
        return getattr(s, name)(m) if m >= s.proj_start() else opening(s)
    return extract


# WholeLife_US_SEC's opening state (D6): what WholeLife_US_S carries into month d, each read
# as S's own formulas read it.  The paid-up additions, the loan and the accumulation balance
# entering the month; the additions and the loan at the anniversary that opened its policy
# year, which the year's dividend, OYT gap and loan interest read; the dividend credited
# there, S's div_prev_anniv(d); and the gross premiums since issue, which S's prem_cum sums
# from issue whatever its frame.  S's accumulation balance opens its frame at 0.
_WL_STATE = {
    "pua_face_init": _wl_entering("pua_face", lambda s: s.puaf_inforce()),
    "loan_bal_init": _wl_entering("loan_bal", lambda s: s.loan_inforce()),
    "pua_face_prev_anniv_init": _wl_at_prev_anniv("pua_face", lambda s: s.puaf_inforce()),
    "loan_bal_prev_anniv_init": _wl_at_prev_anniv("loan_bal", lambda s: s.loan_inforce()),
    "div_accum_init": _wl_entering("div_accum", lambda s: 0.0),
    "div_prev_anniv_init": lambda s, d: s.div_prev_anniv(d),
    "prem_cum_init": lambda s, d: s.prem_cum(d - 1) if d > 0 else 0.0,
}


def _spia_lives(life):
    """``SPIA_US_S``'s survival of ``life`` to time ``d``, the start of month ``d``."""
    return lambda s, d: s.lives_if(d, life)


def _spia_cmt10_change(s, d):
    """The 10-year CMT's change ``SPIA_US_S`` has applied by month ``d``, since the annuity
    date: its ``cmt10_shift``, which it applies from month 0 on, and 0 at ``d = 0``, the
    annuity date itself, where a twin stands."""
    return float(s.cmt10_shift) if d > 0 else 0.0


# SPIA_US_SEC's opening state (D6): what SPIA_US_S carries into month d, each read as S's
# own formulas read it: each life's survival to time d, before month d's deaths; the
# commutation fraction applying in month d, before its withdrawal; and the 10-year CMT's
# change since the annuity date, which S applies whole from month 0, so that a row restated
# at d has seen all of it and sees none after (D7's last paragraph).  The count is S's
# pols_if_init, the contracts the point stands for, and not S's pols_if, which is a
# closing measure (D5): mortality decrements each life, never the count.
_SPIA_STATE = {
    "policy_count": lambda s, d: s.pols_if_init(),
    "lives_if_init_1": _spia_lives(1),
    "lives_if_init_2": _spia_lives(2),
    "commute_frac_cum_init": lambda s, d: s.commute_frac_cum(d),
    "cmt10_shift_init": _spia_cmt10_change,
}


def _spia_twin_args(name, args):
    """``SPIA_US_S``'s ``claims`` keys as ``SPIA_US_SEC`` takes them at stage "EC" (R12).

    S's ``claims(t, kind=None)`` is cached under ``(t, None)``, where ``liability_cf``
    asks for the total, and ``(t, "REFUND")``, where the total asks for its one kind; both
    are SEC's ``claims(t)``, the one kind's formula, which is the total.  Only S's
    two-argument keys are mapped, so that a comparison of SEC with SEC, whose keys are
    ``(t,)``, passes through it unchanged; every other cell's arguments pass as they are.
    """
    if name == "claims" and len(args) == 2:
        return args[:1]
    return args


def _spia_c4_also(proj):
    """What C4 compares of a ``SPIA_US_SEC`` point beyond its full sweep (M23).

    ``sec_support.full_sweep`` reaches a cell of more than ``t`` only at the keys some
    swept cell asks of it, and no swept cell asks for ``lives_death(t, life)``, the one
    per-life cell no report reads.  So, as ``sample_sec.py`` does, this calls it for both
    lives, at ``t = 0 .. proj_len()``: life 2 on a single-life point among them, which the
    sample traces too.  Every timing of ``pols_if_at`` and the one kind of ``claim_pp`` are
    reached by the reports.  Passed to :func:`compiled_mismatches` as ``also``, which must
    not raise: on a point its projection refuses after ``proj_len()``, a rating it cannot
    use on the table basis, say, ``lives_death`` raises where the swept cells do, whose
    raises the sweep records and C4 compares, so the call is left out there.
    """
    for t in range(proj.proj_len() + 1):
        for life in (1, 2):
            try:
                proj.lives_death(t, life)
            except Exception:               # a refused point: the sweep holds the raise
                pass


def _myga_entering(name):
    """What ``MYGA_US_S`` carries into month ``d`` in cells ``name``.

    The close of month ``d - 1``, or 0.0 at ``d = 0``: a contract issued at the valuation
    date opens with no state and takes its issue values in its issue month.
    """
    def extract(s, d):
        return getattr(s, name)(d - 1) if d > 0 else 0.0
    return extract


# MYGA_US_SEC's opening state (D6): what MYGA_US_S carries into month d, each read as S's
# own formulas read it.  The account value, the Model #805 floor and P_accum@GMIR entering
# the month; the interest credited to date, and to the anniversary that opened the contract
# year of d, S's close of month 12 duration(d) - 1, which next year's interest-only
# allowance reads; that year's free-withdrawal allowance, S's free_wd_allow at the year of
# d, and the part of it unused, S's free_wd_remain(d - 1); the IRC 72 basis; and the
# declared rate and i0 S credits and holds in month d - 1, the rate and the lock in force
# entering d.
_MYGA_STATE = {
    "av_pp_init": _myga_entering("av_pp"),
    "mgsv_pp_init": _myga_entering("mgsv_pp"),
    "prem_accum_gmir_pp_init": _myga_entering("prem_accum_gmir_pp"),
    "interest_credited_pp_init": _myga_entering("interest_credited_pp"),
    "interest_credited_pp_prev_anniv_init": lambda s, d: (
        s.interest_credited_pp(12 * s.duration(d) - 1) if d >= 12 else 0.0),
    "free_wd_allow_init": lambda s, d: (
        s.free_wd_allow(s.policy_year(d)) if d > 0 else 0.0),
    "free_wd_remain_init": _myga_entering("free_wd_remain"),
    "tax_basis_pp_init": lambda s, d: s.tax_basis_pp(d - 1),
    "credit_rate_init": _myga_entering("credit_rate"),
    "mva_ref_yield_locked_init": _myga_entering("mva_ref_yield_locked"),
}


def _ul_entering(name, opening):
    """What ``UL_US_S`` carries into month ``d`` in cells ``name``.

    The close of month ``d - 1``, or, where month ``d`` opens S's frame, the opening value
    S's own formulas read there.  ``UL_US_S`` opens every point's frame at its own month 0,
    in force or not, so that is ``d = 0``, the month a twin is read at.
    """
    def extract(s, d):
        return getattr(s, name)(d - 1) if d > 0 else opening(s)
    return extract


# UL_US_SEC's opening state (D6): what UL_US_S carries into month d, each read as S's own
# formulas read it.  The account value and the loan entering month d are S's own opening
# timings.  The face in force is the close of month d - 1, after its withdrawal cut, and
# where d opens S's frame it is S's face at issue on S's in-force point and 0 on new
# business, which has no opening state.  The free withdrawal used in the policy year is
# S's wd_used_year(d), already a value entering the month.  The premiums less withdrawals
# to date, S's cum_prem_pp(d - 1), and the MEC latch, S's is_mec(d - 1) as an int code,
# restart at 0 where S's frame opens, as S assumes.
_UL_STATE = {
    "av_pp_init": lambda s, d: s.av_pp_at(d, "BEF_PREM"),
    "loan_bal_init": lambda s, d: s.loan_bal_pp_bom(d),
    "sum_assured_init": _ul_entering(
        "sum_assured_at", lambda s: s.sum_assured() if s.duration_mth_init() > 0 else 0.0),
    "wd_used_year_init": lambda s, d: s.wd_used_year(d),
    "cum_prem_init": _ul_entering("cum_prem_pp", lambda s: 0.0),
    "is_mec_init": lambda s, d: int(s.is_mec(d - 1)) if d > 0 else 0,
}


def _ul_claims_total(name, args):
    """``UL_US_S``'s ``claims`` keys as ``UL_US_SEC`` takes them at stage ``"EC"`` (R12).

    S's ``claims(t, None)``, the total its ``net_cf`` caches, is SEC's ``claims(t)``.  S's
    ``(t, kind)`` keys, which its ``result_cf`` caches, have no SEC cell of that signature:
    they are SEC's split cells, ``claims_death(t)`` and ``claims_lapse(t)``, and in
    ``ULSG_US_SEC`` ``claims_refund(t)``, which T1 reaches through ``result_cf``'s columns,
    so they are skipped.  Every other cell's arguments pass as they are.
    """
    if name != "claims":
        return args
    return (args[0],) if args[1] is None else None


def _myga_codes(name, args):
    """``MYGA_US_S``'s keys as ``MYGA_US_SEC`` takes them at stage ``"EC"`` (R9, R12).

    S's ``claims(t, None)`` and ``claims_over_av(t, None)``, the ``kind=None`` totals,
    are SEC's ``(t, "ALL")``, and S's ``scenario_rate(t, name)`` columns their names
    upper-cased, ``"MARKET_RATE"`` and ``"MVA_REF_YIELD"``; :func:`codes` then turns each
    string into SEC's int code, as it turns S's timings and kinds.  Every other cell's
    arguments pass as they are, and so do SEC's own codes, where a comparison of two SEC
    models passes it SEC's keys.
    """
    if name in ("claims", "claims_over_av") and args[1] is None:
        return (args[0], "ALL")
    if name == "scenario_rate" and isinstance(args[1], str):
        return (args[0], args[1].upper())
    return args


def _dia_lives(life):
    """``DIA_US_S``'s survival of ``life`` to time ``d``, the start of month ``d``."""
    return lambda s, d: s.lives_if(d, life)


def _dia_entering(name):
    """What ``DIA_US_S`` carries into month ``d`` in cells ``name``, valued during a month.

    ``cum_premium_pp`` and ``annual_income`` hold the month's value after the premium
    received at its start, so what enters month ``d`` is S's value in month ``d - 1``, and 0
    at issue.
    """
    return lambda s, d: getattr(s, name)(d - 1) if d > 0 else 0.0


def _dia_pricing_guarantee(s, d):
    """The guarantee period ``DIA_US_S``'s kernel prices every slice of a refund form with.

    ``s.guarantee_mths_pricing()`` on a cash or installment refund in force at ``d``, and
    blank otherwise: on new business ``DIA_US_SEC`` derives it from the whole schedule, and
    the other forms fix it.
    """
    return (s.guarantee_mths_pricing() if d > 0 and s.payout_form() in ("CR", "IR")
            else float("nan"))


def _dia_surv_to_payout(s, d):
    """``DIA_US_S``'s ``l_last(T)``, where the income start month precedes month ``d``.

    Blank where it does not: there ``DIA_US_SEC`` derives the weight from the lives.
    """
    return s.surv_to_payout() if d > s.income_start_mth() else float("nan")


def _dia_commute_weight(s, d):
    """``DIA_US_S``'s ``l_last(t_c)``, where the commutation month precedes month ``d``.

    Blank where it does not, or where the contract never commutes: there ``DIA_US_SEC``
    derives the weight from the lives.
    """
    c = s.commute_mth()
    return s.lives_if_last(c) if 0 <= c < d else float("nan")


def _dia_ref_rate_change(s, d):
    """The reference rate's change ``DIA_US_S`` has applied by month ``d``, since issue: its
    ``ref_rate_shift``, which it applies from month 0 on, and 0 at ``d = 0``, issue itself,
    where a twin stands."""
    return float(s.ref_rate_shift) if d > 0 else 0.0


# DIA_US_SEC's opening state (D6): what DIA_US_S carries into month d, each read as S's own
# formulas read it: each life's survival to time d; the premiums paid and the income bought
# entering month d, S's values in month d - 1, which hold the month's premium; on a refund
# form in force, the guarantee period S's kernel prices every slice with, a fixed point over
# the whole premium schedule, which the premiums still due cannot recover; the two frozen
# cohort weights, l_last(T) and l_last(t_c), where their months precede d; and the reference
# rate's change since issue, which S applies whole from month 0, so that a row restated at d
# has seen all of it and sees none after (D7's last paragraph).  The count is S's
# pols_if_init, the contracts the point stands for, and not S's pols_if, which is weighted
# by survival (D5): mortality decrements each life, never the count.
_DIA_STATE = {
    "policy_count": lambda s, d: s.pols_if_init(),
    "lives_if_init_1": _dia_lives(1),
    "lives_if_init_2": _dia_lives(2),
    "cum_premium_pp_init": _dia_entering("cum_premium_pp"),
    "annual_income_init": _dia_entering("annual_income"),
    "guarantee_mths_pricing_init": _dia_pricing_guarantee,
    "surv_to_payout_init": _dia_surv_to_payout,
    "commute_weight_init": _dia_commute_weight,
    "ref_rate_shift_init": _dia_ref_rate_change,
}


def _dia_premium_schedule(s_model, table):
    """``premium_schedule_sec.csv``: ``DIA_US_S``'s schedule, then the other rows' premiums.

    The twins keep S's ``point_id`` s, so the file opens with S's ``premium_schedule.csv``
    as it stands, in its order, and a twin's ``premium_schedule()`` is S's, row labels and
    all (T1).  Then, in the table's order, a derived row's source premiums still due, those
    of S months ``d`` and later, since those paid earlier are in its ``cum_premium_pp_init``
    and ``annual_income_init``, and a future row's whole schedule, each under the row's
    ``point_id``, every other cell copied from S.  The point key is the ``point_id``
    column, and nothing else in the file names a point.
    """
    s_sched = s_model.Data.premium_schedule_table()
    point_of = {pol: pid
                for pid, pol in s_model.Data.model_point_table()["policy_id"].items()}
    parts = [s_sched]
    for row in table.to_dict("records"):
        if row["row_kind"] == "twin":
            continue
        rows = s_sched[s_sched["point_id"] == point_of[row["source_policy_id"]]]
        if row["row_kind"] == "derived":
            rows = rows[rows["premium_mth"] >= row["source_mth"]]
        parts.append(rows.assign(point_id=row["point_id"]))
    return pd.concat(parts, ignore_index=True)[list(s_sched.columns)]


def _dia_twin_args(name, args):
    """``DIA_US_S``'s ``claims`` and ``claims_ann`` keys as ``DIA_US_SEC`` takes them at
    stage "EC" (R9, R12).

    S's ``claims(t, kind=None)`` and ``claims_ann(y, kind=None)`` are cached under
    ``(t, None)`` and ``(y, None)`` where S asks for the total, which is SEC's code
    ``ALL``: so ``None`` is mapped to ``"ALL"``, which :func:`codes` then turns into the
    int, as it turns S's kinds.  Every other key, and every other cell's arguments, pass as
    they are, SEC's own codes among them, where a comparison of two SEC models passes it
    SEC's keys.
    """
    if name in ("claims", "claims_ann") and len(args) == 2 and args[1] is None:
        return (args[0], "ALL")
    return args


def _fia_entering(name, opening):
    """What ``FIA_US_S`` carries into month ``d`` in cells ``name``.

    The close of month ``d - 1``; where ``d`` opens S's frame, the value S's own formulas
    open it on, ``opening(s)``, as S's in-force points 1, 3 and 7 open at 84; and 0.0 at
    ``d = 0``: a contract issued at the valuation date opens with no state and takes its
    issue values in its issue month.
    """
    def extract(s, d):
        if d > s.entry_mth():
            return getattr(s, name)(d - 1)
        return opening(s) if d > 0 else 0.0
    return extract


# FIA_US_SEC's phase codes, as its References name them; PRE_ISSUE 0 and MATURED 5 never
# open a row.  The product module asserts that these are the model's.
_FIA_PHASE_CODES = {"ACCUM": 1, "INCOME": 2, "DEPLETED": 3, "TERMINATED": 4}


def _fia_phase_prev_anniv(s, d):
    """``FIA_US_S``'s phase at the anniversary on or before month ``d``, as its code.

    S's phase closing month ``12 * (d // 12) - 1``, whose end opened the contract year of
    ``d``, or S's ``phase_init()`` where that month precedes S's frame; 0 at ``d = 0``.
    """
    if d == 0:
        return 0
    prev = 12 * (d // 12) - 1
    return _FIA_PHASE_CODES[s.phase(prev) if prev >= s.entry_mth() else s.phase_init()]


def _fia_payout_prev_anniv(s, d):
    """``FIA_US_S``'s locked payout rate at the anniversary on or before month ``d``.

    Read as :func:`_fia_phase_prev_anniv` reads the phase; 0.0 at ``d = 0``.
    """
    if d == 0:
        return 0.0
    prev = 12 * (d // 12) - 1
    return s.payout_rate_locked(prev) if prev >= s.entry_mth() else s.payout_rate_init()


def _fia_scenario_id(s, d):
    """The row's scenario: S's own at ``d = 0``, else S's re-based to month ``d`` (D8)."""
    return s.scenario_id() if d == 0 else f"{s.scenario_id()}-M{d}"


def _fia_rebased_scenarios(s_model, table):
    """``rate_scenario_sec.csv``: S's scenarios on the valuation clock, each row's copy
    re-based.

    S keys a level by anniversary from issue; on the valuation clock anniversary ``y`` of a
    contract issued at the valuation date is month ``12 y``.  S's own ids are kept at that
    base, for the twins issued at the valuation date; each row whose ``scenario_id`` is
    none of S's gets its source point's path re-based to its ``source_mth`` by
    :func:`shift_months`: ``d`` for a row restated or in force at ``d``, ``-k`` for one
    issued ``k`` months on.  S's scenarios are read through S's reader, so the companion
    follows S's ``rate_scenario_file``, and each row keeps S's ``provenance``.
    """
    s_table = s_model.Data.model_point_table()
    by_policy = dict(zip(s_table["policy_id"], s_table["scenario_id"]))
    s_scen = s_model.Data.rate_scenario().reset_index()
    monthly = s_scen.assign(t=12 * s_scen["t"])
    out, made = [], set()
    for sid in dict.fromkeys(s_scen["scenario_id"]):
        out.append(monthly[monthly["scenario_id"] == sid])
        made.add(sid)
    for _, row in table.iterrows():
        sid = row["scenario_id"]
        if sid in made:
            continue
        path = monthly[monthly["scenario_id"] == by_policy[row["source_policy_id"]]]
        out.append(shift_months(path, "t", int(row["source_mth"])).assign(scenario_id=sid))
        made.add(sid)
    return pd.concat(out, ignore_index=True)


def _fia_codes(name, args):
    """``FIA_US_S``'s keys as ``FIA_US_SEC`` takes them at stage ``"EC"`` (R9, R12).

    S's ``claims(t, None)`` and ``claims_over_av(t, None)``, the ``kind=None`` totals,
    are SEC's ``(t, "ALL")``, and S's ``scenario_value(y, name)`` columns their names
    upper-cased, ``"INDEX_LEVEL"`` and ``"MVA_REF_YIELD"``; :func:`codes` then turns each
    string into SEC's int code, as it turns S's timings and kinds.  Every other cell's
    arguments pass as they are, and so do SEC's own codes, where a comparison of two SEC
    models passes it SEC's keys: ``MYGA_US_SEC``'s map, :func:`_myga_codes`, on FIA's
    scenario reader.
    """
    if name in ("claims", "claims_over_av") and args[1] is None:
        return (args[0], "ALL")
    if name == "scenario_value" and isinstance(args[1], str):
        return (args[0], args[1].upper())
    return args


def _va_twin_args(name, args):
    """``VA_US_S``'s keys as ``VA_US_SEC`` takes them at stage ``"EC"`` (R9, R12).

    S's ``claims(t, None)`` and ``claims_over_av(t, None)``, the ``kind=None`` totals,
    are SEC's ``(t, "ALL")``, and S's ``scenario_rate(t, name)`` columns their names
    upper-cased, ``"VIX_SQ"`` and ``"CMT10"``; :func:`codes` then turns each string into
    SEC's int code, as it turns S's timings and kinds.  Every other cell's arguments pass
    as they are, and so do SEC's own codes.
    """
    if name in ("claims", "claims_over_av") and args[1] is None:
        return (args[0], "ALL")
    if name == "scenario_rate" and isinstance(args[1], str):
        return (args[0], args[1].upper())
    return args


# FIA_US_SEC's opening state (D6): what FIA_US_S carries into month d, each read as S's own
# formulas read it.  The account value, the fixed account, the Model #805 floor and the
# withdrawals to date entering the month; the account value and the fixed account at the
# anniversary that opened the contract year of d, S's av_pp_year_open(d) and
# av_fixed_pp_year_open(d), which the year's index credit, fixed interest and free
# withdrawal read; the benefit base, the rollup base and the lifetime withdrawal, each flat
# between anniversaries, entering the month; the phase (as a code) and the payout rate at
# that anniversary; the index level there, S's index_level(duration(d)), the year's credit
# base; and the row's scenario, S's re-based to d.  S's own in-force points open on S's
# columns, read by S's cells at their entry month.
_FIA_STATE = {
    "av_pp_init": _fia_entering("av_pp", lambda s: s.av_pp_init()),
    "av_fixed_pp_init": _fia_entering("av_fixed_pp", lambda s: s.av_fixed_pp_init()),
    "av_pp_prev_anniv_init": lambda s, d: s.av_pp_year_open(d) if d > 0 else 0.0,
    "av_fixed_pp_prev_anniv_init": (
        lambda s, d: s.av_fixed_pp_year_open(d) if d > 0 else 0.0),
    "benefit_base_pp_init": _fia_entering("benefit_base_pp",
                                          lambda s: s.benefit_base_pp_init()),
    "rollup_base_pp_init": _fia_entering("rollup_base_pp",
                                         lambda s: s.rollup_base_pp_init()),
    "mgsv_pp_init": _fia_entering("mgsv_pp", lambda s: s.mgsv_pp_init()),
    "lw_pp_init": _fia_entering("lw_pp", lambda s: s.lw_pp_init()),
    "payout_rate_locked_prev_anniv_init": _fia_payout_prev_anniv,
    "phase_prev_anniv_init": _fia_phase_prev_anniv,
    "index_level_prev_anniv_init": (
        lambda s, d: s.index_level(s.duration(d)) if d > 0 else 0.0),
    "wd_cum_pp_init": _fia_entering("wd_cum_pp", lambda s: 0.0),
    "scenario_id": _fia_scenario_id,
}


def _vul_entering(name, opening):
    """What ``VUL_US_S`` carries into month ``d`` in cells ``name``.

    The close of month ``d - 1``, or, where month ``d`` opens S's frame, the opening value
    S's own formulas read there.  ``VUL_US_S`` opens every point's frame at its own month 0,
    in force or not, so that is ``d = 0``, the month a twin is read at.
    """
    def extract(s, d):
        return getattr(s, name)(d - 1) if d > 0 else opening(s)
    return extract


def _vul_sa_entering(i):
    """Subaccount ``i``'s value entering month ``d``: ``VUL_US_S``'s own opening timing."""
    def extract(s, d):
        return s.sa_pp_at(d, i, "BEF_PREM")
    return extract


def _vul_no_pin(s, d):
    """A first-month pin, blank: ``VUL_US_S`` applies a pin at its own ``t = 0`` only."""
    return float("nan")


# VUL_US_SEC's opening state (D6): what VUL_US_S carries into month d, each read as S's own
# formulas read it.  Each subaccount's value, the fixed option's, the loan collateral's and
# the debt entering month d are S's own opening timings; the face in force is the close of
# month d - 1, after its Option A cut, and where d opens S's frame it is S's face at issue
# on an in-force point and 0 on new business, which has no opening state.  The two
# first-month pins are blank on every row S restates in force at a later month: S applies a
# pin at its own t = 0 only, which is before month d.  The subaccounts are the shipped
# lineup's, 1 and 2, the ids subaccount_table.csv gives; a lineup with another id needs its
# sa_pp_init_<i> entry here, and test_variable_ul_us_sec.py asserts that the two agree.
_VUL_STATE = {
    **{f"sa_pp_init_{i}": _vul_sa_entering(i) for i in (1, 2)},
    "fa_pp_init": lambda s, d: s.fa_pp_at(d, "BEF_PREM"),
    "la_pp_init": lambda s, d: s.la_pp_at(d, "BEF_PREM"),
    "loan_bal_init": lambda s, d: s.loan_bal_pp_at(d, "BEF_PREM"),
    "sum_assured_init": _vul_entering(
        "sum_assured_at", lambda s: s.sum_assured() if s.duration_mth_init() > 0 else 0.0),
    "corridor_override_m1": _vul_no_pin,
    "coi_rate_override_m1": _vul_no_pin,
}

# VUL_US_S names each subaccount by its id, and VUL_US_SEC at stage EC by its position in
# the lineup, from 0 (R9, R10): the shipped lineup's ids, 1 and 2, at positions 0 and 1.
# test_variable_ul_us_sec.py asserts that this agrees with subaccount_table.csv, as
# _VUL_STATE's ids do.
_VUL_LINEUP = {1: 0, 2: 1}

# The cells of VUL_US_S that take a subaccount id, by the place of the id among their
# arguments.
_VUL_BY_ID = {"alloc": 0, "fund_expense_ann": 0, "sa_pp_init": 0, "scenario_last_mth": 0,
              "gross_return_mth": 1, "inv_return_mth": 1, "wd_sa_pp": 1,
              "mth_deduction_sa_pp": 1, "sa_pp_at": 1, "sa_pp": 1, "sa_pricing_pp_at": 1,
              "sa_pricing_pp": 1}


def _vul_twin_args(name, args):
    """``VUL_US_S``'s keys as ``VUL_US_SEC`` takes them at stage ``"EC"`` (R9, R12).

    S's ``claims(t, None)`` and ``me_charge_pp(t, None)``, the totals its ``net_cf`` and
    ``me_charge`` cache, are SEC's ``claims(t)`` and ``me_charge_pp(t)``.  S's
    ``claims(t, kind)`` and ``me_charge_pp(t, i)`` keys have no SEC cell of that
    signature: they are SEC's ``claims_death(t)``, ``claims_lapse(t)`` and
    ``me_charge_sa_pp(t, i)``, which T1 reaches through ``result_cf``'s columns and the
    totals, and ``test_variable_ul_us_sec.py`` compares with S's keys, so they are skipped.
    A subaccount id, S's argument of a cell of :data:`_VUL_BY_ID`, is its position in the
    lineup, :data:`_VUL_LINEUP`.  Every other cell's arguments pass as they are.
    """
    if name in ("claims", "me_charge_pp"):
        return (args[0],) if args[1] is None else None
    if name in _VUL_BY_ID:
        at = _VUL_BY_ID[name]
        return args[:at] + (_VUL_LINEUP.get(args[at], args[at]),) + args[at + 1:]
    return args


def _vul_c4_also(proj):
    """What C4 compares of a ``VUL_US_SEC`` point beyond its full sweep (M17).

    ``sec_support.full_sweep`` reaches a cell of more than ``t`` only at the keys some
    swept cell asks of it.  So, as ``sample_sec.py`` does, this calls every account cell at
    every timing it takes and ``av_at`` at ``EOM``, ``pols_if_at`` at ``BEF_MAT``, both
    claim cells at every kind they take and every subaccount's timings, at
    ``t = 0 .. proj_len()``, and ``inv_return_mth``, an economic input that refuses a
    month before its re-based path's first, from ``t_entry()``; and the pricing path at
    every policy month from issue to the last in cover, at every timing it takes, with its
    three closes, which with the behaviour module off no cell reaches.  Passed to
    :func:`compiled_mismatches` as ``also``.
    """
    account = (proj.BEF_PREM, proj.BEF_WD, proj.BEF_FEE, proj.BEF_INV, proj.BEF_ME)
    pricing = (proj.BEF_PREM, proj.BEF_FEE, proj.BEF_INV)
    n = proj.subaccount_count()
    for t in range(proj.proj_len() + 1):
        proj.pols_if_at(t, proj.BEF_MAT)
        for timing in account:
            for cell in ("av_pp_at", "unloaned_av_pp_at", "av_at", "fa_pp_at", "la_pp_at",
                         "loan_bal_pp_at"):
                proj.cells[cell](t, timing)
        proj.av_at(t, proj.EOM)
        for i in range(n):
            if t >= proj.t_entry():
                proj.inv_return_mth(t, i)
            for timing in account:
                proj.sa_pp_at(t, i, timing)
        for kind in (proj.DEATH, proj.LAPSE, proj.WITHDRAWAL):
            proj.claim_pp(t, kind)
        for kind in (proj.DEATH, proj.LAPSE, proj.MATURITY):
            proj.claims_from_av(t, kind)
    for m in range(proj.duration_mth(proj.proj_len() - 1) + 1):
        proj.fa_pricing_pp(m)
        proj.av_pricing_pp(m)
        for timing in pricing:
            proj.fa_pricing_pp_at(m, timing)
            proj.av_pricing_pp_at(m, timing)
        for i in range(n):
            proj.sa_pricing_pp(m, i)
            for timing in pricing:
                proj.sa_pricing_pp_at(m, i, timing)


def _rila_entering(name):
    """What ``RILA_US_S`` carries into month ``d`` in cells ``name``.

    The close of month ``d - 1``, or 0.0 at ``d = 0``: a contract issued at the valuation
    date opens with no state, and S credits its purchase payment in its issue month.
    """
    def extract(s, d):
        return getattr(s, name)(d - 1) if d > 0 else 0.0
    return extract


def _rila_prev_anniv(s, d):
    """``RILA_US_S``'s free-withdrawal base for the contract year of month ``d``.

    The Account Value before withdrawals at the anniversary on or before month ``d``, S's
    ``av_pp_at(12 cy - 1, "BEF_WD")`` at the close of the month the anniversary ends; the
    purchase payment in the first contract year, which opened at issue, as S's
    ``free_wd_base`` reads it there; and 0.0 at ``d = 0``, where nothing is in force yet.
    """
    if d <= 0:
        return 0.0
    if d < 12:
        return s.premium_pp()
    return s.av_pp_at(12 * (d // 12) - 1, "BEF_WD")


def _rila_mid_term(s, d):
    """Whether the term ``RILA_US_S`` has in force at month ``d`` began before ``d``.

    On a contract in force, ``d > 0``, every month but a Term Start Date: terms run from
    issue in steps of ``12 x term_years`` policy months.
    """
    return d > 0 and d % (12 * s.term_years()) != 0


def _rila_term_start(name):
    """``RILA_US_S``'s market ``name`` on the Term Start Date of the term in force at ``d``.

    Where that date precedes ``d``, S's scenario at the term's start, the value S locks
    there; blank otherwise, where the SEC model reads the start from the scenario (the
    frozen-weight shape of USLIB-SEC-PLAN.md §7.12, *Record — M12*).
    """
    def extract(s, d):
        if not _rila_mid_term(s, d):
            return float("nan")
        return s.market_state(s.term_start_month(d), name)
    return extract


def _rila_cap(s, d):
    """``RILA_US_S``'s cap in force at ``d``, where S re-solved it at a renewal before it.

    On a capped option under ``nge_reset`` whose term in force at ``d`` began at a
    renewal, after issue and before ``d``: S's ``cap_rate(d)``, the cap solved on the
    market of that renewal and floored at the guaranteed minimum. Blank otherwise: the cap
    of an initial term, or of any term off ``nge_reset``, is the model point's rule.
    """
    if not _rila_mid_term(s, d) or s.is_uncapped() or not s.nge_reset():
        return float("nan")
    if s.term_start_month(d) <= 0:
        return float("nan")
    return s.cap_rate(d)


def _rila_scenario_id(s, d):
    """The row's scenario: S's own at ``d = 0``, else S's re-based to month ``d`` (D8)."""
    return s.scenario_id() if d == 0 else f"{s.scenario_id()}-M{d}"


def _rila_rebased_scenarios(s_model, table):
    """``market_scenario_sec.csv``: S's scenarios on the valuation clock, each row's copy
    re-based.

    S keys a level by its month end from issue, which is the valuation clock of a contract
    issued at the valuation date, so S's scenarios open the file as they stand, under
    their own ids, for the twins.  Each row whose ``scenario_id`` is none of S's gets its
    source point's path re-based to its ``duration_mth`` by :func:`shift_months`, as a
    step function: ``d`` for a row restated in force at ``d``, whose month-0 level is the
    one S holds at ``d``, and ``-k`` for one issued ``k`` months on, whose copy holds no
    level before its issue month.  The path is keyed from issue, so each copy moves by the
    months from issue to the row's valuation date, its ``duration_mth``, which is its
    ``source_mth`` only because ``RILA_US_S`` has no point in force.  S's scenarios are
    read through S's reader, so the companion follows S's ``market_scenario_file``, and
    each copied row keeps S's ``provenance``.
    """
    s_table = s_model.Data.model_point_table()
    by_policy = dict(zip(s_table["policy_id"], s_table["scenario_id"]))
    s_scen = s_model.Data.market_scenario().reset_index()
    out, made = [s_scen], set(s_scen["scenario_id"])
    for row in table.to_dict("records"):
        sid = row["scenario_id"]
        if sid in made:
            continue
        path = s_scen[s_scen["scenario_id"] == by_policy[row["source_policy_id"]]]
        out.append(shift_months(path, "month_end", int(row["duration_mth"]))
                   .assign(scenario_id=sid))
        made.add(sid)
    return pd.concat(out, ignore_index=True)


def _rila_codes(name, args):
    """``RILA_US_S``'s keys as ``RILA_US_SEC`` takes them at stage ``"EC"`` (R9, R12).

    S's ``claims(t, None)`` and ``claims_over_av(t, None)``, the ``kind=None`` totals,
    are SEC's ``(t, "ALL")``, and S's ``market_state(k, name)`` columns their names
    upper-cased, ``"INDEX_LEVEL"`` to ``"IMPL_VOL"``; :func:`codes` then turns each string
    into SEC's int code, as it turns S's timings, kinds, buckets, legs and markets.  Every
    other cell's arguments pass as they are, and so do SEC's own codes, where a comparison
    of two SEC models passes it SEC's keys: :func:`_fia_codes` on RILA's scenario reader.
    """
    if name in ("claims", "claims_over_av") and args[1] is None:
        return (args[0], "ALL")
    if name == "market_state" and isinstance(args[1], str):
        return (args[0], args[1].upper())
    return args


# RILA_US_SEC's opening state (D6): what RILA_US_S carries into month d, each read as S's
# own formulas read it.  The Investment Amount, the Fixed and Holding Accounts, the Account
# Value, the Free Withdrawal Amount still unused and the return-of-premium base entering
# the month, each S's close of month d - 1; the Account Value before withdrawals at the
# anniversary on or before d, the base of the contract year's Free Withdrawal Amount;
# where the term in force at d began before d, the index level, the Market Value Rate and
# the option-pricing market of its Term Start Date, with the cap S re-solved at that
# renewal on a capped option under nge_reset; and the row's scenario, S's re-based to d.
_RILA_STATE = {
    "inv_amt_pp_init": _rila_entering("inv_amt_pp"),
    "fixed_acct_pp_init": _rila_entering("fixed_acct_pp"),
    "holding_acct_pp_init": _rila_entering("holding_acct_pp"),
    "av_pp_init": _rila_entering("av_pp"),
    "av_pp_prev_anniv_init": _rila_prev_anniv,
    "free_wd_remain_init": _rila_entering("free_wd_remain"),
    "rop_pp_init": _rila_entering("rop_pp"),
    "index_at_term_start_init": _rila_term_start("index_level"),
    "mvr_at_term_start_init": _rila_term_start("mvr"),
    "risk_free_at_term_start_init": _rila_term_start("risk_free"),
    "div_yield_at_term_start_init": _rila_term_start("div_yield"),
    "impl_vol_at_term_start_init": _rila_term_start("impl_vol"),
    "cap_rate_init": _rila_cap,
    "scenario_id": _rila_scenario_id,
}


def _va_entering(name, opening):
    """What ``VA_US_S`` carries into month ``d`` in cells ``name``.

    The close of S month ``d - 1``; at ``d = 0``, the first month of S's frame, the value
    S's own formulas open on, ``opening(s)``: S's columns on its in-force point 2, 0 on
    its new business.
    """
    def extract(s, d):
        return getattr(s, name)(d - 1) if d > 0 else opening(s)
    return extract


def _va_fund(i):
    """Subaccount ``i`` entering month ``d``: S's close of ``d - 1``, or at ``d = 0`` S's
    own opening, the account value split by the target allocation; blank (NaN) on a point
    whose fund set holds no subaccount ``i``, which no projection reads."""
    def extract(s, d):
        if i not in s.sub_ids():
            return float("nan")
        return s.sa_pp(d - 1, i) if d > 0 else s.alloc(i) * s.av_pp_init()
    return extract


def _va_funds(s_model):
    """VA's subaccount values, ``sa_pp_init_<i>``, a column for each subaccount the fund
    table of ``s_model`` holds, two as shipped (``SecSpec.model_state``): read from the S
    model the generator reads, so that a fund table given a subaccount gives the table its
    column."""
    ids = s_model.Data.fund_table().index.get_level_values("sub_id")
    return {f"sa_pp_init_{i}": _va_fund(i) for i in sorted({int(i) for i in ids})}


def _va_year_start(s, d):
    """Whether S month ``d`` opens a contract year."""
    return s.duration_mth(d) % 12 == 0


def _va_year_first(s, d):
    """The S month in which the contract year of S month ``d`` began, below 0 where that
    was before S's frame."""
    return d - s.duration_mth(d) % 12


def _va_ytd(name, empty):
    """A contract-year-to-date value entering month ``d``: S's close of ``d - 1`` in the
    year under way; the empty value at a year's start, and at ``d = 0`` on S's in-force
    point, where S restarts it; 0.0 on new business at ``d = 0``, which has no opening
    state."""
    def extract(s, d):
        if d == 0 or _va_year_start(s, d):
            return empty if (d > 0 or s.duration_mth_init() > 0) else 0.0
        return getattr(s, name)(d - 1)
    return extract


def _va_factor(s, d):
    """``gmdb_factor_acc`` entering month ``d``, as :func:`_va_ytd` reads a value whose
    empty value is 1."""
    if d == 0:
        return 1.0 if s.duration_mth_init() > 0 else 0.0
    if _va_year_start(s, d):
        return 1.0
    return s.gmdb_factor_acc(d - 1)


def _va_has_wd(s, d):
    """Whether S has taken a withdrawal before month ``d``: ``has_wd_by(d - 1)``, or S's
    own inference at ``d = 0``."""
    return s.has_wd_by(d - 1) if d > 0 else s.has_wd_init()


def _va_wd_this_year(s, d):
    """Whether S takes a withdrawal in the contract year of ``d`` before ``d``, in its
    frame; False at a year's start and at ``d = 0``, where S scans from ``t = 0``."""
    if d == 0 or _va_year_start(s, d):
        return False
    return any(s.is_wd_taken(u) for u in range(max(0, _va_year_first(s, d)), d))


def _va_rb_prev_anniv(s, d):
    """The roll-up base at the anniversary that opened the year of ``d``, as S reads it in
    month ``d``, ``rb_prior_anniv_pp(d)``; 0.0 on new business at ``d = 0``."""
    if d == 0 and s.duration_mth_init() == 0:
        return 0.0
    return s.rb_prior_anniv_pp(d)


def _va_stepup_ytd(s, d):
    """The largest account value at the quarterly anniversaries of ``d``'s contract year
    that S closed before ``d``, in its frame: the months ``first + 2``, ``+ 5`` and
    ``+ 8``; 0.0 where none."""
    first = _va_year_first(s, d)
    best = 0.0
    for q in (first + 2, first + 5, first + 8):
        if 0 <= q < d:
            best = max(best, s.av_pp(q))
    return best


def _va_phi_prior(s, d):
    """On a ``vix`` point, the VIX-formula rate of the last contract quarter to end before
    month ``d``, the clip's prior for the first fee on the books; 0.0 in the first
    quarter and off the ``vix`` rule."""
    k = s.contract_quarter(d)
    if s.fee_reset_rule() != "vix" or k <= 1:
        return 0.0
    return s.phi_glwb_vix(k - 1)


def _va_scenario_id(s, d):
    """The row's scenario: S's own at policy month 0, else S's re-based to the policy
    month, ``{id}-M{m}``, which rows moved alike share (D7, D8)."""
    m = s.duration_mth(d)
    return s.scenario_id() if m == 0 else f"{s.scenario_id()}-M{m}"


def _va_rebased(s_model, table, reader, by):
    """A VA scenario companion: S's scenarios as they stand, then each row's copy re-based.

    S keys its scenarios by policy month, so a twin issued at the valuation date reads S's
    own ids.  Each row whose scenario_id is none of S's gets its source point's path
    re-based by :func:`shift_months` to its ``duration_mth``, the policy months elapsed at
    the valuation date (negative for a future row), and not to its ``source_mth``:
    ``VA_US_S`` projects its in-force point 2 from the valuation date, so that twin's
    ``source_mth`` is 0 while its path moves by 26.  ``reader`` names S's ``Data`` reader,
    so the companion follows S's ``*_file`` Reference, and ``by`` the columns each re-based
    on its own rows.  The provenance is S's.
    """
    s_table = s_model.Data.model_point_table()
    by_policy = dict(zip(s_table["policy_id"], s_table["scenario_id"]))
    s_scen = getattr(s_model.Data, reader)().reset_index()
    out, made = [], set()
    for sid in dict.fromkeys(s_scen["scenario_id"]):
        out.append(s_scen[s_scen["scenario_id"] == sid])
        made.add(sid)
    for _, row in table.iterrows():
        sid = row["scenario_id"]
        if sid in made:
            continue
        path = s_scen[s_scen["scenario_id"] == by_policy[row["source_policy_id"]]]
        out.append(shift_months(path, "t", int(row["duration_mth"]), by=by)
                   .assign(scenario_id=sid))
        made.add(sid)
    return pd.concat(out, ignore_index=True)


def _va_rebased_returns(s_model, table):
    """``return_scenario_sec.csv``: S's returns re-based per row, each subaccount stepped
    on its own rows (``by="sub_id"``)."""
    return _va_rebased(s_model, table, "return_scenario", "sub_id")


def _va_rebased_rates(s_model, table):
    """``rate_scenario_sec.csv``: S's VIX and CMT path re-based per row."""
    return _va_rebased(s_model, table, "rate_scenario", ())


# VA_US_SEC's opening state (D6): what VA_US_S carries into month d, each read as S's own
# formulas read it.  Beside the subaccount values, a column for each subaccount S's fund
# table holds, two as shipped, blank where a point's set lacks one (_va_funds): the seven
# bases, the locked GAWA%, the bonus period's end and whether a withdrawal has been taken,
# entering the month; the withdrawals, free allowance used, dollar-for-dollar reduction and
# proportional factor of the contract year to date, and whether the year has a withdrawal;
# the roll-up base at the anniversary that opened the year; the year's highest quarterly
# account value so far; the VIX fee of the quarter before; and the row's scenario, S's
# re-based to its policy month.  S's own in-force point 2 opens on S's columns, read by S's
# cells at d = 0.
_VA_STATE = {
    "gwb_pp_init": _va_entering("gwb_pp", lambda s: s.gwb_pp_init()),
    "gawa_pp_init": _va_entering("gawa_pp", lambda s: s.gawa_pp_init()),
    "gawa_pct_init": _va_entering("gawa_pct_fixed", lambda s: s.gawa_pct_init()),
    "bb_pp_init": _va_entering("bb_pp", lambda s: s.bb_pp_init()),
    "rb_pp_init": _va_entering("rb_pp", lambda s: s.rb_pp_init()),
    "np_pp_init": _va_entering("np_pp", lambda s: s.np_pp_init()),
    "rp_pp_init": _va_entering("rp_pp", lambda s: s.rp_pp_init()),
    "adj_pp_init": _va_entering("adj_pp", lambda s: s.adj_pp_init()),
    "bonus_end_init": _va_entering("bonus_end", lambda s: s.bonus_end_init()),
    "has_wd_init": _va_has_wd,
    "sum_wd_pp_ytd_init": _va_ytd("sum_wd_pp", 0.0),
    "free_wd_used_cum_pp_ytd_init": _va_ytd("free_wd_used_cum_pp", 0.0),
    "gmdb_dfd_acc_pp_ytd_init": _va_ytd("gmdb_dfd_acc_pp", 0.0),
    "gmdb_factor_acc_ytd_init": _va_factor,
    "wd_this_year_init": _va_wd_this_year,
    "rb_pp_prev_anniv_init": _va_rb_prev_anniv,
    "stepup_base_pp_ytd_init": _va_stepup_ytd,
    "phi_glwb_init": _va_phi_prior,
    "scenario_id": _va_scenario_id,
}


def _ulsg_entering(name, opening):
    """What ``ULSG_US_S`` carries into month ``d`` in cells ``name``.

    The close of month ``d - 1``, or, where month ``d`` opens S's frame, the opening value
    S's own formulas read there.  ``ULSG_US_S`` opens every point's frame at its own month
    0, in force or not, so that is ``d = 0``, the month a twin is read at.
    """
    def extract(s, d):
        return getattr(s, name)(d - 1) if d > 0 else opening(s)
    return extract


def _ulsg_grace_entering(s, d):
    """The months ``ULSG_US_S``'s point ``s`` has spent in grace entering month ``d``.

    S's ``grace_mth(d - 1)``, or 0 where month ``d`` opens S's frame, as S reads it.  A
    month by which S's lapse latch has shut is refused, naming the point and the month:
    the policy lapsed at the start of the month after its grace expired, its count there is
    0, and the in-force interface carries no latch, so no policy is in force to restate.
    Read so, the counter a row carries is below ``grace_months`` (``ULSG_US_SEC``'s
    ``proj_len()`` refuses one that is not), and it may reset in the row's first month, as
    S's does wherever the month's deduction stops failing.
    """
    if d > 0 and s.is_lapsed(d):
        raise ValueError(
            f"ULSG_US_S point {s.point_id} has lapsed by month {d}: its grace expired, "
            f"so no policy is in force to restate")
    return s.grace_mth(d - 1) if d > 0 else 0


# ULSG_US_SEC's opening state (D6): what ULSG_US_S carries into month d, each read as S's
# own formulas read it.  The account value, the shadow account and the loan entering month d
# are S's own opening timings; the premiums paid to date are the close of month d - 1, S's
# cum_prem_pp, or S's own column where d opens S's frame; and the grace counter carried in
# is S's grace_mth(d - 1), the months already spent in grace, read as 0 where d opens S's
# frame, as S reads it, at a month S has not yet lapsed by.
_ULSG_STATE = {
    "av_pp_init": lambda s, d: s.av_pp_at(d, "BEF_PREM"),
    "sg_pp_init": lambda s, d: s.sg_pp_at(d, "BEF_PREM"),
    "loan_bal_init": lambda s, d: s.loan_bal_pp_at(d, "BEF_INT"),
    "cum_prem_init": _ulsg_entering("cum_prem_pp", lambda s: s.cum_prem_init()),
    "grace_mth_init": _ulsg_grace_entering,
}


def _iul_entering(name, opening):
    """What ``IUL_US_S`` carries into month ``d`` in cells ``name``.

    The close of month ``d - 1``, or, where month ``d`` opens S's frame, the opening value
    S's own formulas read there.  ``IUL_US_S`` opens every point's frame at its own month
    0, so that is ``d = 0``, the month a twin is read at.
    """
    def extract(s, d):
        return getattr(s, name)(d - 1) if d > 0 else opening(s)
    return extract


def _iul_mec_latch(s, d):
    """The MEC latch ``IUL_US_S``'s point ``s`` carries into month ``d``, as an int code.

    ``IUL_US_S``'s ``is_mec`` is the 7-pay test of the month alone and does not latch, so
    the latch ``IUL_US_SEC`` opens with is whether that test failed in any month from 0 to
    ``d - 1``: 1 if so, 0 otherwise, and 0 where ``d`` opens S's frame.  The months are read
    in ascending order, each test reading the premiums paid to date, which S's own sweep
    does not reach, a month at a time.
    """
    for u in range(d):
        if s.is_mec(u):
            return 1
    return 0


# IUL_US_SEC's opening state (D6): what IUL_US_S carries into month d, each read as S's own
# formulas read it.  The account value, the fixed account and the loan collateral entering
# month d are S's own opening timings, and the loan the close of month d - 1, or S's own
# column where d opens S's frame.  The face in force is the close of month d - 1, after its
# withdrawal cut, and where d opens S's frame S's face at issue on a point in force and 0
# on new business, which has no opening state.  The premiums less withdrawals to date and
# the no-lapse accumulator, S's cum_prem_pp(d - 1) and cum_prem_net_pp(d - 1), restart at 0
# where S's frame opens, as S assumes, and so does the MEC latch (_iul_mec_latch).  The
# live index segments are a companion, built by _iul_ladder.
_IUL_STATE = {
    "av_pp_init": lambda s, d: s.av_pp_at(d, "BEF_PREM"),
    "loan_bal_init": _iul_entering("loan_bal_pp", lambda s: s.loan_bal_init()),
    "fa_pp_init": lambda s, d: s.fa_pp_at(d, "BEF_PREM"),
    "lca_pp_init": lambda s, d: s.lca_pp_at(d, "BEF_PREM"),
    "sum_assured_init": _iul_entering(
        "sum_assured_at", lambda s: s.sum_assured() if s.duration_mth_init() > 0 else 0.0),
    "cum_prem_init": _iul_entering("cum_prem_pp", lambda s: 0.0),
    "cum_prem_net_init": _iul_entering("cum_prem_net_pp", lambda s: 0.0),
    "is_mec_init": _iul_mec_latch,
}

_IUL_LADDER = ("point_id", "slot", "seg_bal_pp_init", "seg_ded_cum_pp_init",
               "seg_wd_cum_pp_init", "seg_index_start_init", "seg_index_cap_init")


def _iul_ladder(s_model, table):
    """``inforce_segments_sec.csv``: each derived row's live segments entering month ``d``.

    For each row of the table in force, restated at S month ``d`` or the twin of a point S
    opens in force (``d = 0``), in the table's order, one row for each of its last
    ``min(seg_term_mth, duration_mth)`` policy months, ``duration_mth`` the row's own, a
    month that swept nothing included: ``slot`` ``k``, the months since the segment's
    creation at the valuation date, is the segment ``IUL_US_S`` created at its month
    ``m = d - k``.  Where ``k <= d``, S created it in its own frame, and the row holds its
    balance, the deductions and the draws charged to it to date, each at the close of month
    ``d - 1`` (S's ``seg_bal_pp``, ``seg_ded_cum_pp`` and ``seg_wd_cum_pp`` at
    ``(d - 1, m)``); where ``k > d``, the segment predates S's frame, which S assumes held
    none, and the row is empty.  Either way it holds the cap S declares at ``m``, its
    ``index_cap_at(m)``, and S's index level at ``m`` rebased onto ``IUL_US_SEC``'s path,
    whose level at the valuation date is ``index_level_init``: ``index_level(m)`` times
    ``index_level_init`` over ``index_level(d)``, so that a segment's return, a ratio of
    two levels, is S's.  On S's points as shipped, all new business, ``duration_mth`` is
    ``d``, so every slot is S's own.  The future rows hold none, and so do the twins of S's
    new-business points.  ``point_id`` is the only key to a point.

    It reads only the S cells it needs, and releases nothing: the caller owns the S model,
    and one T6 passes in may be one it still compares against, whose caches a release
    would empty.
    """
    point_of = {pol: pid
                for pid, pol in s_model.Data.model_point_table()["policy_id"].items()}
    rows = []
    for row in table.to_dict("records"):
        s = s_model.Projection[point_of[row["source_policy_id"]]]
        if row["row_kind"] not in ("derived", "twin"):
            continue
        d = int(row["source_mth"]) if row["row_kind"] == "derived" else 0
        base = s.index_level_init / s.index_level(d)
        for k in range(1, min(s.seg_term_mth, int(row["duration_mth"])) + 1):
            m = d - k
            held = (s.seg_bal_pp(d - 1, m), s.seg_ded_cum_pp(d - 1, m),
                    s.seg_wd_cum_pp(d - 1, m)) if k <= d else (0.0, 0.0, 0.0)
            rows.append({"point_id": row["point_id"], "slot": k,
                         "seg_bal_pp_init": held[0], "seg_ded_cum_pp_init": held[1],
                         "seg_wd_cum_pp_init": held[2],
                         "seg_index_start_init": s.index_level(m) * base,
                         "seg_index_cap_init": s.index_cap_at(m)})
    return pd.DataFrame(rows, columns=list(_IUL_LADDER))


_IUL_SEGMENT = frozenset({"seg_share", "seg_wd_pp", "seg_ded_pp", "seg_bal_pp",
                          "seg_ded_cum_pp", "seg_wd_cum_pp"})


def _iul_twin_args(name, args):
    """``IUL_US_S``'s keys as ``IUL_US_SEC`` takes them at stage ``"EC"`` (R12, R15).

    S's ``claims(t, None)``, the total its ``net_cf`` caches, is SEC's ``claims(t)``; S's
    ``claims(t, kind)`` keys have no SEC cell of that signature: they are SEC's
    ``claims_death(t)`` and ``claims_lapse(t)``, which T1 reaches through ``result_cf``'s
    columns and the total, so they are skipped.  S's six segment cells are keyed by
    ``(t, m)``, ``m`` the segment's creation month, and SEC's by ``(t, k)``, ``k`` its
    slot, the months since its creation in month ``t``, ``duration_mth(t) - m``.  S's
    ``t`` is its projection month, which on every S point, all new business, is the
    policy month, so the slot is ``t - m`` on S's clock, before :func:`twin_mismatches`
    moves ``t`` by ``t_offset``: one map for T1, T2's restated rows and T3's rows issued
    later.  A key whose slot falls below 0, a segment not yet born in month ``t``, which S
    answers 0 and SEC's cells answer 0 without a call, is skipped.  Every other cell's
    arguments pass as they are, the engine cells' among them, which SEC keeps with S's
    ``None`` defaults (R14).
    """
    if name == "claims":
        return (args[0],) if args[1] is None else None
    if name in _IUL_SEGMENT:
        t, m = args
        return None if t < m else (t, t - m)
    return args


# SEC model name -> its SecSpec.  Phase 1 registers each product's spec here as its SEC
# model lands, Term first (§5.3).  The conventions suite reads ``exempt`` from it for T1,
# the product module's T6 calls :func:`check_generated` with the name, and
# ``tools/gen_sec_points.py`` writes the files from it.
SEC_SPECS: dict[str, SecSpec] = {
    # Term's only state is the count, which the default extractor reads (s_proj.pols_if(d)),
    # so the spec names rows and nothing else.  The derived rows are an anniversary in the
    # level period, the middle of the first ART year and the last covered month; the
    # future row is issued off a valuation anniversary.  T2's splice grid is built from
    # this spec in a temporary table, not committed.  T1, and T3 on the future rows, hold
    # on Term only while each S point counts one policy, as both do: SEC charges
    # acquisition per policy issued, S once per model point (§7.1), so on a row issued at
    # or after the valuation date from a point of any other count, expenses and net_cf
    # differ in the issue month by design, and no exemption can take that out without
    # taking those cells.
    "Term_US_SEC": SecSpec(
        twin="Term_US_S",
        column_map={"duration_inforce": None},
        derived=((2, 12), (1, 126), (1, 719)),
        future=((1, 3),),
    ),
    # WholeLife's state is seven columns (_WL_STATE above).  S's own columns are renamed in
    # place, puaf_inforce and loan_inforce to pua_face_init and loan_bal_init, and
    # duration_inforce, S's elapsed policy years, is dropped for duration_mth, 108 on S's
    # in-force point 1.  On the twins the five columns S has no column for take what S
    # itself assumes, so each twin reproduces S: on point 1 the paid-up additions at the
    # anniversary are its 4,100, the loan 0, the accumulation balance and last year's
    # dividend 0, S's "before the frame", and the premiums since issue S's prem_cum(107).
    # The derived rows are the two S points that do not reproduce from S's own in-force
    # state (§7.2), REDUCE_PREM and ACCUM, on the anniversary that opens policy year 10;
    # the funded term blend mid-year before its crossover and the loan variant mid-year,
    # whose anniversary values differ from their current ones; the graded final-expense
    # point inside its graded years; and REDUCE_PREM in the last covered month.  The future
    # row is issued off a valuation anniversary.  T2's splice grid is built from this spec
    # in a temporary table, not committed.
    #
    # T1 holds on WholeLife at any count: S already weights its acquisition by the count
    # issued, as SEC charges it.  It skips five S cells besides the default three:
    #   puaf_inforce, loan_inforce: renamed pua_face_init and loan_bal_init, one name for
    #     each opening-state column (D6, §7.2).  Every cell that read them reads the
    #     renamed cells, which T1 compares, and both are 0 on S's new business.
    #   proj_start: S's first projected month on the policy clock, 108 on S's point 1.
    #     Every SEC frame opens at t = 0 (D3), which the conventions assert.
    #   duration_inforce: S's elapsed policy years, which duration_mth replaces (D6).
    #   result_pols: SEC's gains pols_new_biz, the count D5 puts there, so the frame has a
    #     column S's lacks and cannot agree as a whole.  Each column it shares with S is a
    #     cell T1 compares at every month, and test_whole_life_us_sec.py compares the
    #     report itself with S's, on every column both hold.
    #   claims: S's claims(t, kind=None) is split at stage EC into claims_death,
    #     claims_lapse and claims_maturity, the result_cf columns, and a total claims(t)
    #     (R12).  S's keys, (t, kind) and (t, None), have no SEC cell of that signature,
    #     and every value reaches T1 through the three columns of result_cf and through
    #     liability_cf; test_whole_life_us_sec.py compares the total with S's, bit for bit.
    "WholeLife_US_SEC": SecSpec(
        twin="WholeLife_US_S",
        column_map={"duration_inforce": None, "puaf_inforce": "pua_face_init",
                    "loan_inforce": "loan_bal_init"},
        duration_of=lambda row: 12 * int(row["duration_inforce"]),
        derived=((5, 108), (4, 108), (8, 78), (6, 114), (12, 18), (5, 659)),
        future=((2, 3),),
        state=_WL_STATE,
        twin_state={c: f for c, f in _WL_STATE.items()
                    if c not in ("pua_face_init", "loan_bal_init")},
        exempt=frozenset({"puaf_inforce", "loan_inforce", "proj_start",
                          "duration_inforce", "result_pols", "claims"}),
    ),
    # SPIA's state is each life's survival, the commutation fraction and the CMT's change
    # since the annuity date (_SPIA_STATE).  S has no in-force point, so every twin is new
    # business, and the four columns take S's own values at the annuity date: each covered
    # life alive, life 2 at 0 on a single-life contract, no commutation, no change in the
    # CMT.  A derived row's CMT change is S's cmt10_shift, all of it seen by month d.  SEC's
    # cmt10_shift is a change made at the valuation date, on the one path every point
    # shares, which a row in payment sees on top of its column and a future row, bought
    # after it, never sees: so the splice reads its table once, with SEC's cmt10_shift at 0,
    # and compares each future row with S read with its cmt10_shift at 0, the same contract
    # on that path.  The payments to date need no column: they are deterministic, and the
    # model sums them on the policy clock from the annuity date.  The derived rows are the
    # worked example's anchor the month after the joint annuitant's death; the cash refund
    # in its death month, which pays the refund at t = 0; the certain period ending at the
    # valuation date; both lives dead inside the certain period; the commuting point on its
    # second anniversary, with two fractional lives; and the anchor on the table basis in
    # its last month, a one-row frame.  The future row commences 13 months on: more than a
    # year out, so that a read before the annuity date lands at policy year -1, and off
    # every payment step (1, 3, 6 and 12 months), so that its payment months fall apart on
    # the two clocks.  T2's splice grid is built from this spec in a temporary table, not
    # committed.
    #
    # T1 holds on SPIA at any count: neither model charges acquisition, and every flow is
    # the count times a per-contract amount.  It skips one S cell besides the default
    # three:
    #   result_pols: SEC's gains pols_new_biz and puts pols_if first, so the frame has a
    #     column S's lacks and cannot agree as a whole.  Each column it shares with S is a
    #     cell T1 compares at every month, and test_immediate_annuity_us_sec.py compares
    #     the report itself with S's, column by column.
    # S caches claims(t, kind=None) under (t, None) and (t, "REFUND"); at stage EC the one
    # kind is claims(t), its formula and so the total (R12), and the spec's twin_arg_map,
    # _spia_twin_args, maps both keys onto it.  S's label accessors stay S's, called by
    # reporting and T1 alone.  R17 and C5 admit one that returns its point's column:
    # form(), reduction_trigger() and mort_basis() return the column of their own name,
    # and the registry's "reporting_columns" names what the other two return,
    # payment_timing() the "timing" column, and sex(life) "primary_sex" or "joint_sex" by
    # life (M23).
    #
    # Phase 2 sizes its caches from the contract (spec_sec.py holds each derivation):
    #   t 0..1,560: issue_age_min, 0, the youngest issue age of every form and life,
    #     since S projects every age from 0 and a frame runs to the age stop on its
    #     youngest life, the limiting age omega_age, 120, and future_horizon_mth, 120: the
    #     longest frame is 12 * (120 - 0) + 120 months, and lives_if reads the closing
    #     time point t = proj_len();
    #   k 0..1,440, the policy months and time points, from the same youngest age and
    #     omega_age, which also bound the longest certain period the caches hold;
    #   y 1..120, the policy years: k's last month // 12 + 1;
    #   x 0..119, the attained ages, per life: the youngest issue age and omega_age - 1.
    # proj_len() refuses an issue age of any life below issue_age_min, 0, and
    # certain_months above 12 * (omega_age - issue_age_min), each naming the point (M23).
    "SPIA_US_SEC": SecSpec(
        twin="SPIA_US_S",
        derived=((1, 14), (6, 13), (5, 120), (13, 30), (9, 24), (8, 695)),
        future=((8, 13),),
        state=_SPIA_STATE,
        twin_state={c: f for c, f in _SPIA_STATE.items() if c != "policy_count"},
        exempt=frozenset({"result_pols"}),
        twin_arg_map=_spia_twin_args,
    ),
    # MYGA's state is ten columns (_MYGA_STATE above), each read off S as S's own formulas
    # read it.  S's one column of the kind, tax_basis_initial, is renamed in place to
    # tax_basis_pp_init, the name of the S cell that reads it; on new business it keeps its
    # S meaning, the basis at issue.  On the twins the other nine take what S itself
    # assumes, 0 entering month 0, where SEC credits the issue values in the issue month, so
    # each twin reproduces S.  The derived rows are the anchor on its first anniversary,
    # whose $4,000 is free under the year's allowance; the interest-only, net-of-charges
    # point the month after its excess withdrawal, carrying both interest columns, the
    # floor net of charges, the basis and a used-up allowance; Camp B inside its initial
    # term, carrying the P_accum its GMIR-floored cap reads; the registered-contract point
    # in its window, where the rate is redeclared and i0 re-locked from the scenario at
    # t = 0; the stress trace in the second month of its first renewal period, the month
    # after its window, whose rate and i0 come from the opening state; and Camp B in its
    # last covered month, its annual rate declared before the valuation date.  The future
    # row is issued more than a year on, so a missing guard reads contract year -1 before
    # issue.  T2's splice grid is built from this spec in a temporary table, not
    # committed.
    #
    # T1 holds on MYGA at any count: S already charges acquisition and commission on the
    # count issued, as SEC does.  It skips three S cells besides the default three:
    #   av_pp_init, mgsv_pp_init: SEC's are the account value and the Model #805 floor in
    #     force entering month 0 (D6), 0 on a contract issued at the valuation date, where
    #     S's compute the issue values.  SEC credits those by S's rules in the issue month
    #     (prem_to_av_pp, prem_to_mgsv_pp), and every cell they fed, av_pp_at, av_pp,
    #     mgsv_pp and prem_to_av_pp among them, is compared.
    #   result_pols: SEC's gains pols_new_biz, the count D5 puts there, so the frame has a
    #     column S's lacks and cannot agree as a whole.  Each column it shares with S is a
    #     cell T1 compares at every month, and test_fixed_deferred_annuity_us_sec.py
    #     compares the report itself with S's, on every column both hold.
    # At stage EC (M20), S's claims(t, None) and claims_over_av(t, None) keys, the
    # kind=None totals, are SEC's code ALL, and S's scenario_rate columns, "market_rate"
    # and "mva_ref_yield", are SEC's codes named as them upper-cased: the spec's
    # twin_arg_map, _myga_codes, maps both, and codes maps the rest.  T1 skips three more
    # S cells at stage EC:
    #   mva_pp_on, mva_factor_geometric: S's float-parameter cells, which SEC writes inline
    #     in the int-keyed cells that call them (R14): mva_pp and wd_mva_pp, and mva_rate.
    #     Their every value on the projection path reaches T1 through those cells, which it
    #     compares at every month.
    #   surr_charge_id: S returns its schedule's key in lower case, "initial", "renewal" or
    #     "none", and SEC its code, INITIAL, RENEWAL or NONE, which codes, matching case,
    #     cannot map; the rate it selects, surr_charge_rate, is compared at every month,
    #     and the module holds the code to S's text.
    # The three engine cells, mgsv_rate_statutory, mgsv_rate_is_compliant and
    # mva_ref_term_years, are S's formulas, kept for T1 and a reader and admitted by the
    # registry's "engine" (R14).
    #
    # No projection cell calls a label accessor or compares text: the five categorical
    # columns S branches on are decoded in Data into the 0/1 vectors the is_* cells read,
    # one flag for each value S tests, each read where S asks its question, so a value S
    # does not know is answered as S answers it (R6).  The four joins on text keys are
    # numbered in Data (R7): mort_rate_at on the point's sex, by mort_schedule;
    # scenario_rate on its scenario_id, by scenario_number; wd_scheduled_pp on its
    # wd_schedule_id, by wd_schedule_number; and surr_charge_rate on the schedule code
    # surr_charge_id returns, the row of Data's surr_charge_array.  The age cap and the
    # mortality are read through cells keyed by attained age (surr_charge_age_cap_at,
    # mort_rate_at), and the duration factors at the whole years mva_term_years gives,
    # in mva_duration_factor.  proj_len refuses an attained age past the mortality
    # table's last before maturity, against Data's mort_age_lasts, since maturity_age is a
    # Projection Reference that Data cannot read.
    #
    # The caches, each size with every input it depends on (spec_sec.py): t 1,322, from
    # issue_age_min 0, maturity_age 100 and future_horizon_mth 120, and the t + 1 reads in
    # the month after the frame; y 102 for free_wd_base and free_wd_allow, contract years
    # 1 .. 100; a 101 for surr_charge_age_cap_at and mort_rate_at, attained ages 0 .. 99;
    # and one inner width, 8, for the timing, kind and name codes.  proj_len refuses an
    # issue age below issue_age_min or above issue_age_max, 85, the product's ages.
    "MYGA_US_SEC": SecSpec(
        twin="MYGA_US_S",
        column_map={"tax_basis_initial": "tax_basis_pp_init"},
        derived=((1, 12), (5, 30), (3, 30), (4, 60), (2, 61), (3, 479)),
        future=((1, 15),),
        state=_MYGA_STATE,
        twin_state={c: f for c, f in _MYGA_STATE.items() if c != "tax_basis_pp_init"},
        exempt=frozenset({"av_pp_init", "mgsv_pp_init", "result_pols", "mva_pp_on",
                          "mva_factor_geometric", "surr_charge_id"}),
        twin_arg_map=_myga_codes,
    ),
    # UL's state is the account value and the loan, S's own columns under their own names,
    # and four more (_UL_STATE above).  pols_if_init becomes policy_count (the default),
    # and duration_mth is S's own column: UL_US_S runs on the projection clock already, and
    # its point 3, in force 120 months, opens its frame at its own t = 0, so that twin's
    # source_mth is 0 (§5.2).  On the twins the four new columns take what S itself
    # assumes, so each twin reproduces S: on point 3 the face at issue, no withdrawal used,
    # and the premiums paid and the MEC latch restarted at 0.  The derived rows are the
    # first anniversary, inside the surrender-charge period; mid lapse-shock year; S's
    # in-force point six months on, mid-year with its loan; Option B in the month its
    # shortfall begins, the last month a point in permanent shortfall can be restated,
    # since its account value is negative after it; and the first month at attained age
    # 119, where the mortality table's rate reaches 1.0 and every survivor dies, in place of
    # the last covered month, 1031, which at S's mortality no policy reaches.  The future
    # row is issued 25 months after the valuation date, off its anniversaries and more
    # than a year on, so that the months before issue read policy years -2 to 0, where a
    # missing guard would show.  T2's splice grid is built from this spec in a temporary
    # table, not committed.
    #
    # T1 holds on UL at any count: S charges acquisition on the policies in force in the
    # issue month, the policies issued, as SEC does.  It skips two S cells besides the
    # default three:
    #   result_pols: SEC's gains pols_new_biz, the count D5 puts there, so the frame has a
    #     column S's lacks and cannot agree as a whole.  Each column it shares with S is a
    #     cell T1 compares at every month, and test_universal_life_us_sec.py compares the
    #     report itself with S's, on every column both hold.
    #   coi_rate_scale: S's guaranteed COI scale for the point's cell, a Series, which no
    #     compiled cell returns (R10).  SEC numbers the scale instead, coi_schedule, and
    #     every value of it reaches T1 through coi_rate_guar and coi_rate_guar_py, which T1
    #     compares at every month and policy year S read.
    # S's net_cf calls claims(t) with its kind=None default, so S's sweep caches claims
    # under (t, None), and its result_cf under (t, "DEATH") and (t, "LAPSE").  At stage EC
    # claims is split into claims_death and claims_lapse, the result_cf columns, and a total
    # claims(t) (R12), so the spec's twin_arg_map, _ul_claims_total, maps S's total onto
    # SEC's and skips the kind keys, whose values reach T1 through result_cf.  So T1
    # compares the total, where WholeLife's spec exempts it; to T1's tolerance, and
    # test_universal_life_us_sec.py holds it to S's bit for bit.
    #
    # Phase 2's sizes, each with the inputs it depends on.  The contract issues at ages 18
    # to 85 (product-spec), and S projects any age its tables serve, so Phase 2 refuses an
    # issue age below 18, issue_age_min, in proj_len():
    #   t: 0 to 1,356, the longest frame and the month after it, which the roll-forwards
    #     read: 12 x (omega_age 120 - youngest issue age 18 + 1) = 1,236 months of cover,
    #     plus future_horizon_mth 120.
    #   policy years y (prem_persistency_py, coi_rate_guar_py, lapse_rate_base_py): 1 to
    #     103, the year of the last covered month at the youngest issue age 18 and
    #     omega_age 120.
    #   attained ages a (corridor_factor_at, mort_rate_base_at): youngest issue age 18 to
    #     omega_age 120.
    "UL_US_SEC": SecSpec(
        twin="UL_US_S",
        duration_of=lambda row: int(row["duration_mth"]),
        derived=((1, 12), (1, 113), (3, 6), (2, 676), (1, 1008)),
        future=((1, 25),),
        state=_UL_STATE,
        twin_state={c: f for c, f in _UL_STATE.items()
                    if c not in ("av_pp_init", "loan_bal_init")},
        exempt=frozenset({"result_pols", "coi_rate_scale"}),
        twin_arg_map=_ul_claims_total,
    ),
    # DIA's state is eight columns (_DIA_STATE): each life's survival; the premiums paid and
    # the income bought; on a refund form in force, the guarantee period the pricing kernel
    # prices every slice with, a fixed point over the whole schedule, which the premiums
    # still due cannot recover; the frozen cohort weights l_last(T) and l_last(t_c), each
    # given only where its month precedes the valuation month, the projection deriving it
    # from the lives at or after it; and the reference rate's change since issue.  S has no
    # in-force point, so every twin is new business, and the columns take S's own values at
    # issue: each covered life alive, life 2 at 0 on a single-life contract, nothing paid or
    # bought, the three other columns blank, no change in the reference rate.  The
    # instalments scheduled to date need no column: the income is level from the income
    # start month, so they are a schedule the model sums by policy month.  Nor does the
    # acceleration's weight, which S reads only in the exercise month: a row valued after it
    # paid the lump sum before the valuation date.  SEC's ref_rate_shift is a change made at
    # the valuation date, on the one path every point shares, which a row in force sees on
    # top of its column and a future row, issued after it, never sees: so the splice reads
    # its table once, with SEC's ref_rate_shift at 0, and compares each future row with S
    # read with its ref_rate_shift at 0, the same contract on that path.
    #
    # DIA's premiums are a companion, premium_schedule_sec.csv (D8), keyed by point_id as
    # S's premium_schedule.csv is: it opens with S's file as it stands, so each twin keeps
    # S's rows and row labels, then holds each derived row's premiums still due and each
    # future row's whole schedule.  Its reader checks it against the table.
    #
    # The derived rows are the payment-acceleration point in deferral the month before its
    # second premium, which it prices with the guarantee-period column; the anchor a month
    # into payout, its cash refund running; the 10-year period certain inside its guarantee,
    # where the contract open exceeds the life alive; the commuting point a month after its
    # commutation; the start-date adjustment a month after it; the joint point with its
    # joint annuitant dead with certainty; the installment refund inside its derived period;
    # and the anchor in its last month, a one-row frame.  The future row is the joint point
    # issued 13 months on: more than a year out, so that a read before issue lands at policy
    # year -1, and off every payment step.  T2's splice grid is built from this spec in a
    # temporary table, not committed.
    #
    # T1 holds on DIA at any count: neither model charges acquisition, and every flow is the
    # count times a per-contract amount.  It skips one S cell besides the default three:
    #   result_pols: SEC's gains pols_new_biz and puts pols_if first, so the frame has a
    #     column S's lacks and cannot agree as a whole.  Each column it shares with S is a
    #     cell T1 compares at every month, and the product module compares the report
    #     itself with S's, column by column.
    # At stage EC (M24), S's claims(t, None) and claims_ann(y, None) keys, the kind=None
    # totals, are SEC's code ALL, which keeps S's sum of the two kinds' cells: the spec's
    # twin_arg_map, _dia_twin_args, maps None to "ALL", and codes maps it and the rest, the
    # timings, the kinds and the phases.  S's label accessors stay S's, called by reporting
    # and T1 alone: market_type(), income_form(), db_form(), mort_basis(), factor_basis()
    # and reduction_trigger() return the column of their own name, and the registry's
    # "reporting_columns" names what the other three return, payment_timing() the "timing"
    # column, sex(life) "sex" or "joint_sex" by life, and payout_form() the "income_form"
    # column with LO_ROP read as LO.  S's float-parameter cells, annuity_factor and
    # pricing_disc_factor, and its cells returning a DataFrame, a dict and a list,
    # premium_schedule, premium_by_mth and qlac_flags, are kept for S's tests and T1 and
    # called by no compiled cell, the registry's "engine" (R14): annuity_factor_at and
    # guarantee_mths_pricing hold the kernel's body, the premiums are read from Data's
    # premium table, and the discount is written inline.  purchase_rate keeps its
    # round(pr, dp), admitted by the registry's "python_calls", and rop_factor's
    # int(round(deferral_yrs(k))) is rop_deferral_yrs(k), on the integers (R16).
    #
    # Phase 2 sizes its caches from the contract (spec_sec.py holds each derivation):
    #   t 0..1,562: issue_age_min, 0, the youngest issue age of every form and life, since
    #     S projects every form from 0, the limiting age omega_age, 120, and
    #     future_horizon_mth, 120: a stop rule at policy month 1,441 at most, 120 months
    #     on, and lives_if reads the closing time point t = proj_len();
    #   k 0..1,446, the policy months and time points, to the stop rule's month and the
    #     five instalments an acceleration in the last month pulls forward;
    #   y 1..122, the policy years: k's last month // 12 + 1;
    #   x 0..120, the attained ages, per life: issue_age_min and omega_age.
    # stop_mth() refuses an issue age of any life below issue_age_min, 0, an income start
    # month, at issue or in force, past 12 * (omega_age - issue_age_min), 1,440, and a
    # certain period ending past it, each naming the point (M24); the product-spec's 22, 13
    # to 360 and 10 to 30 bound nothing.
    "DIA_US_SEC": SecSpec(
        twin="DIA_US_S",
        derived=((14, 59), (1, 241), (7, 300), (15, 253), (13, 121), (8, 672), (5, 270),
                 (1, 719)),
        future=((8, 13),),
        state=_DIA_STATE,
        twin_state={c: f for c, f in _DIA_STATE.items() if c != "policy_count"},
        exempt=frozenset({"result_pols"}),
        companions={"premium_schedule_sec.csv": _dia_premium_schedule},
        twin_arg_map=_dia_twin_args,
    ),
    # FIA's state is twelve columns and the row's scenario (_FIA_STATE above).  S's own
    # columns are renamed in place under D6 -- av_initial, bb_initial, rb_initial,
    # mgv_initial and lw_initial to their cells' _init, phase_initial (text) to
    # phase_prev_anniv_init (an int code) and payout_rate_initial to
    # payout_rate_locked_prev_anniv_init -- and entry_year, S's elapsed years at entry, is
    # dropped for duration_mth, 84 on S's in-force points 1, 3 and 7.  On every twin each
    # column S has none for takes what S itself assumes, so the twin reproduces S: on points
    # 1, 3 and 7 at 84, S's columns, a fixed account of alloc_fixed x AV, the year-open
    # values equal to the entering ones, withdrawals to date 0 and the index level of
    # anniversary 7.  The derived rows are the fixed account on an anniversary (4 at 60),
    # the anchor's exercise month read mid-year (1 at 95), joint income in force mid-year
    # (5 at 150), the overdrawn anchor near exhaustion (7 at 216), a zero account value with
    # the rider live (2 at 240), the first policy year (8 at 6), the last policy year,
    # entered at 120 (6 at 696), and income in force mid-year with the fixed account
    # accrued since its anniversary (4 at 100).  The last covered month is not among them:
    # at the shipped mortality, 1.0 at age 120, S's count after month 696 is exactly 0, so
    # a row at 707 would project zeros; the splice reaches it on mortality cut at 120.  The
    # future row is issued 15 months on, more than a year, and future_state gives it its own
    # re-based scenario.  T2's splice grid is built from this spec in a temporary table,
    # not committed.
    #
    # The scenario is a companion, rate_scenario_sec.csv (D8): S keys its levels by
    # anniversary from issue, so on the valuation clock each row needs its own copy
    # re-based to its month, the in-force twins included.  It is read through S's reader,
    # rate_scenario(), whose Data Reference rate_scenario_file names it.
    #
    # T1 holds on FIA at any count: S already weights its premium and acquisition by
    # pols_if_init, the count issued.  S's phase strings map onto SEC's int codes through
    # codes(), the phases being codes from stage E.  It skips ten S cells besides the
    # default three:
    #   av_pp_init, av_fixed_pp_init, benefit_base_pp_init, rollup_base_pp_init,
    #     mgsv_pp_init: S computes each issue value by rule in these cells when its
    #     column is blank; SEC's are the columns, 0 on new business, and the issue value
    #     is credited by rule in the issue month (prem_to_av_pp, prem_to_mgsv_pp,
    #     rollup_base_pp_year_open, benefit_base_pp_at), which T1 compares (D6, §7.10).
    #   phase_init, payout_rate_init: dropped; the year-open phase and payout rate are
    #     read through phase_year_open and payout_rate_locked from their _prev_anniv_init
    #     columns.
    #   entry_year, entry_mth: S's late frame on the policy clock.  Every SEC frame opens
    #     at t = 0 (D3), which the conventions assert; duration_mth_init and t_entry
    #     replace them.
    #   result_pols: SEC's gains pols_new_biz, the count D5 puts there.  Each column it
    #     shares with S is a cell T1 compares, and the module compares the report itself.
    # At stage EC (M21), S's claims(t, None) and claims_over_av(t, None) keys, the
    # kind=None totals, are SEC's code ALL, and S's scenario_value columns,
    # "index_level" and "mva_ref_yield", are SEC's codes named as them upper-cased: the
    # spec's twin_arg_map, _fia_codes, maps both, and codes maps the rest.  T1 skips three
    # more S cells at stage EC:
    #   bonus_clawback_on, mva_pp_on, wd_reduction_rate_on: S's float-parameter cells,
    #     which SEC writes inline in the int-keyed cells that call them (R14):
    #     wd_clawback_pp and surr_clawback_pp, wd_mva_pp and mva_pp, and
    #     wd_reduction_rate.  Their every value on the projection path reaches T1 through
    #     those cells, which it compares at every month.
    # The four engine cells, credit_rate_on, payout_rate, mgsv_rate_statutory and
    # mgsv_rate_is_compliant, are S's formulas, kept for T1 and a reader and admitted by
    # the registry's "engine" (R14); T1 compares them at the arguments the module's sweep
    # calls S's with.
    #
    # No projection cell calls a label accessor or compares text: glwb_basis and
    # credit_method are decoded in Data into the 0/1 vectors the is_*_basis and
    # is_credit_* cells read, and the three References, step_up_mode, rb_wd_convention
    # and mva_collar_basis, hold int codes the is_step_up_*, is_rb_* and is_collar_*
    # cells compare, each read where S asks its question, so a value S does not know is
    # answered as S answers it (R6, R10).  The four joins on text keys are numbered in
    # Data (R7): mort_rate_base_at on the point's sex, by mort_schedule; rollup_rate_py on
    # its rollup_id, by rollup_number; scenario_value on its scenario_id, by
    # scenario_number; and wd_scheduled_at on its wd_schedule_id, by wd_schedule_number.
    #
    # The caches, each size with every input it depends on (spec_sec.py).  The contract
    # issues at ages 40 to 80 (product-spec) and runs to the year entered at maturity_age,
    # 120:
    #   t: 0 .. 1,092: 972 months of cover at the youngest issue age, 40, plus
    #     future_horizon_mth, 120, the frame's last month 1,091, and the month after,
    #     t = proj_len(), which C4's sweep calls: every cell that reads t + 1 is guarded
    #     there, the count's roll-forward residual included, so nothing reads 1,093;
    #   y (surr_charge_rate_py, vest_rate_py, rollup_rate_py): contract years 1 .. 81, from
    #     the youngest issue age and maturity_age; the surrender table's last year, 11 as
    #     shipped, caps the first two;
    #   a (mort_rate_base_at): attained ages 40 .. 120, by sex; a (payout_rate_at): the
    #     exercise ages, min_income_age, 50 as shipped, .. 121, the covered age 120 opening
    #     the last contract year plus 1, read in the payout bands' first to last age, the
    #     last band holding above it, so the cache runs to 121 though the table stops at
    #     120;
    #   k (wd_scheduled_at): contract-year counts 0 .. 80; y (index_level, mva_ref_yield,
    #     scenario_value): anniversary numbers 0 .. 81, each read at its valuation month;
    #     scenario_value(y, name) takes the column's code, INDEX_LEVEL or MVA_REF_YIELD.
    # So spec_sec.py sizes t 1,094, y 83, a 123 and k 82, with one inner width, 12, for the
    # timing, kind and name codes; Data.read_last_mth, 1,093, and Data.read_last_age, 122,
    # hold the scenario, rollup, withdrawal, mortality and payout arrays to the last month
    # and age a read reaches.  proj_len refuses an issue age below issue_age_min, 40, or
    # above issue_age_max, 80, the product's ages, and a point whose sex's mortality stops
    # below maturity_age, against Data's mort_age_lasts, since maturity_age is a Projection
    # Reference that Data cannot read.
    "FIA_US_SEC": SecSpec(
        twin="FIA_US_S",
        column_map={"entry_year": None, "av_initial": "av_pp_init",
                    "bb_initial": "benefit_base_pp_init",
                    "rb_initial": "rollup_base_pp_init", "mgv_initial": "mgsv_pp_init",
                    "lw_initial": "lw_pp_init", "phase_initial": "phase_prev_anniv_init",
                    "payout_rate_initial": "payout_rate_locked_prev_anniv_init"},
        duration_of=lambda row: 12 * int(row["entry_year"]),
        derived=((4, 60), (1, 95), (5, 150), (7, 216), (2, 240), (8, 6), (6, 696),
                 (4, 100)),
        future=((2, 15),),
        state=_FIA_STATE,
        twin_state=_FIA_STATE,
        exempt=frozenset({"av_pp_init", "av_fixed_pp_init", "benefit_base_pp_init",
                          "rollup_base_pp_init", "mgsv_pp_init", "phase_init",
                          "payout_rate_init", "entry_year", "entry_mth", "result_pols",
                          "bonus_clawback_on", "mva_pp_on", "wd_reduction_rate_on"}),
        twin_arg_map=_fia_codes,
        companions={"rate_scenario_sec.csv": _fia_rebased_scenarios},
        future_state={"scenario_id": lambda s, k: f"{s.scenario_id()}-F{k}"},
    ),
    # VUL's state is S's own columns under their own names, each subaccount, the fixed
    # option and the debt, and two more, the loan collateral and the face in force
    # (_VUL_STATE above).  pols_if_init becomes policy_count (the default), and
    # duration_mth is S's own column: VUL_US_S runs on the projection clock already, and its
    # points 1 and 2, in force 24 months, and 4, in force 120, open their frames at their
    # own t = 0, so those twins' source_mth is 0 (§5.2).  On the twins the two new columns
    # take what S itself assumes, so each twin reproduces S: the collateral equal to the
    # debt [std], 8,000 on point 4 and 0 elsewhere, and the face at issue in force.  The
    # pins stay as S's table has them, point 1's applying at t = 0, the valuation month.
    # The derived rows are S point 3 on its first anniversary, inside the surrender-charge
    # period, on Option B; S's in-force point 4 six months on, mid-year, its collateral and
    # its debt parted; point 3 in the month its shortfall begins at the shipped
    # assumptions, the last month it can be restated, since a subaccount opens negative in
    # the month after; and point 4 in the first month at attained age 119, where the
    # mortality table's rate reaches 1.0 and every survivor dies, in place of the last
    # covered month, which at S's mortality no policy reaches, and the shortest frame, 36
    # months.  The future row is point 3 issued 25 months after the valuation date, off its
    # anniversaries and more than a year on, so that the months before issue read policy
    # years -2 to 0, where a missing guard would show.  A future row copies its twin's
    # columns, the pins among them, and the twin's are blank: S's one pinned point, 1, is
    # in force, and Data refuses a pin on a point issued after the valuation date, which
    # would never apply.  test_variable_ul_us_sec.py asserts that every S point named in
    # future has both pins blank, so a pinned S new-business point fails there, by name,
    # rather than in Data.  T2's splice grid is built from this spec in a temporary table,
    # not committed.
    #
    # T1 holds on VUL at any count: S charges acquisition on the policies in force in the
    # issue month, the policies issued, as SEC does.  It skips three S cells besides the
    # default three:
    #   result_pols: SEC's gains pols_new_biz, the count D5 puts there, so the frame has a
    #     column S's lacks and cannot agree as a whole.  Each column it shares with S is a
    #     cell T1 compares at every month, and test_variable_ul_us_sec.py compares the
    #     report itself with S's, on every column both hold.
    #   subaccount_ids: S's lineup, a list of the ids, which no compiled cell returns
    #     (R10).  SEC counts the lineup instead, subaccount_count, and names a subaccount
    #     by its position, which _vul_twin_args maps S's ids onto, so every value S reads
    #     by an id reaches T1 through the cells of a subaccount, at every month S read.
    #   coi_rate_scale: S's guaranteed COI scale for the point's cell, a Series, which no
    #     compiled cell returns (R10).  SEC numbers the scale instead, coi_schedule, and
    #     every value of it reaches T1 through coi_rate_guar and coi_rate_guar_at, which T1
    #     compares at every month and policy year S read.
    # S's net_cf calls claims(t) with its kind=None default and S's me_charge calls
    # me_charge_pp(t) with its i=None, so S's sweep caches claims under (t, None) and
    # me_charge_pp under (t, None), and its result_cf and its sum over the lineup cache the
    # kinds and the subaccounts.  At stage EC claims is split into claims_death and
    # claims_lapse, the result_cf columns, and a total claims(t), and me_charge_pp into
    # me_charge_sa_pp(t, i) and a total me_charge_pp(t) (R12), so the spec's twin_arg_map,
    # _vul_twin_args, maps S's two totals onto SEC's and skips the kind and subaccount keys,
    # whose values reach T1 through the totals and the reports, and which
    # test_variable_ul_us_sec.py compares with S's bit for bit.  The label accessors (sex,
    # rate_class, db_option, qual_test, premium_type, surr_charge_id, scenario_id) are
    # called by no projection cell, and are declared reporting; and the two first-month
    # pins are a value array, NaN where blank as S reads it, and a 0/1 flag array (R8).  No
    # cell takes a float parameter.
    #
    # Phase 2's sizes (spec_sec.py), each with the inputs it depends on.  The contract
    # issues at ages 0 to 85 (product-spec), and S projects any age its tables serve; Data
    # refuses an issue age below 0 or not whole, proj_len() refuses one below
    # issue_age_min, 0, or above issue_age_max, 85, and a lineup of more than
    # subaccount_max, 9, and every size below rests on the youngest, 0.  Ages 0 to 17 sit
    # below the mortality and corridor tables' first age, 18, and read those tables
    # clamped there, as S does.
    #   t: 0 to 1,584, the longest frame and the month after it, which the roll-forwards
    #     read: 12 x (omega_age 121 - youngest issue age 0 + 1) = 1,464 months of cover,
    #     plus future_horizon_mth 120.
    #   the pricing month m (sa_pricing_pp_at, fa_pricing_pp_at and their kin): 0 to 1,463,
    #     the last covered policy month at the youngest issue age.  The pricing path is
    #     based at issue, one cell a month, so with dyn_behavior_on a cold call runs back
    #     to issue: the depth Phase 2's stack is sized from is that path's, 1,463 cells and
    #     a few more at issue age 0, wherever the valuation date falls.  And so does an
    #     ascending sweep of a point in force at policy month d, whose first month reads the
    #     path cold: about d + 15 cells deep, 39 on point 1, 135 on point 4 and 903 on point
    #     8 under modelx, against 18 on every committed point with the module off, and
    #     1,477 on a point in force in its last covered month at issue age 0.  A point
    #     issued at or after the valuation date sweeps at about 22 cells deep.
    #   policy years y (coi_rate_guar_at, coi_rate_at, lapse_rate_base_py,
    #     prem_persistency_py): 1 to 122, the year of the last covered month at the
    #     youngest issue age and omega_age 121.
    #   attained ages a (corridor_factor_at, mort_rate_base_at): youngest issue age 0 to
    #     omega_age 121; corridor_factor_at is read from the issue age on by the pricing
    #     path.
    #   subaccounts i: positions 0 to subaccount_max - 1, 8, the one width of every 2-D
    #     cache and of each dimension of every 3-D cache, nine, which timing's nine codes
    #     share; 2 shipped.  Each scenario path is read to its cell's last month
    #     (scenario_last_mth), at min(t, last), from Data's array by scenario, subaccount
    #     and month.
    # The lapse rate, base x the cliff's spike x the dynamic multiplier, has no cap in S or
    # here, and Data holds each base rate to 0 to 1.  With lapse_shock_mult and
    # lapse_dyn_cap at 0 or more, the annual lapse rate is at most max(1, lapse_shock_mult)
    # x (lapse_dyn_cap with dyn_behavior_on, 1 without) x the largest base rate, and stays
    # at most 1 while that product is at most 1: 0.06 as shipped, 0.12 with
    # dyn_behavior_on, 0.36 on the splice.  Past 1 the monthly rate is complex in modelx,
    # and its checks raise as S's do; compiled, the power is NaN and the checks fail
    # instead.
    "VUL_US_SEC": SecSpec(
        twin="VUL_US_S",
        duration_of=lambda row: int(row["duration_mth"]),
        derived=((3, 12), (4, 6), (3, 593), (4, 768)),
        future=((3, 25),),
        state=_VUL_STATE,
        twin_state={c: f for c, f in _VUL_STATE.items()
                    if c in ("la_pp_init", "sum_assured_init")},
        exempt=frozenset({"result_pols", "subaccount_ids", "coi_rate_scale"}),
        twin_arg_map=_vul_twin_args,
    ),
    # RILA's state is thirteen columns and the row's scenario (_RILA_STATE above): seven
    # amounts per contract entering the valuation month, the Investment Amount, which is
    # also the crediting basis, the Fixed and Holding Accounts, the Account Value, of
    # either sign since the interim value can fall below 0 [S2], the Account Value before
    # withdrawals at the anniversary on or before d, the Free Withdrawal Amount still
    # unused and the return-of-premium base; and, where the term in force began before d,
    # the index level, the Market Value Rate and the option-pricing market of its Term
    # Start Date, with the cap re-solved at that renewal on a capped option under
    # nge_reset, each given only where its date precedes the valuation month, the
    # projection reading the scenario at or after it (the frozen-weight shape of §7.12's
    # Record — M12).  S has no in-force point, so every twin is new business, and the
    # columns take S's own opening at issue: every amount 0, every fixing blank.  Terms
    # align with issue, so no term-start month is a column, and RILA_US_S has no
    # Performance Lock, so no lock is one either.
    #
    # The derived rows are the anchor in the last month of its first term (1 at 71); the
    # worked example's withdrawal programme on the anniversary after its $8,000 midpoint
    # withdrawal (2 at 36); the reset point mid-term after its first renewal, its cap
    # re-solved there (13 at 80), and valued at that renewal (13 at 72); a Step option on
    # a one-year term mid-term, its Fixed Account fed by two term ends (4 at 30); the
    # legacy interim-value family the month before the charge-free year's first term end
    # (15 at 59); the uncapped option mid-term (12 at 40); and the notional family in its
    # last covered month (7 at 119).  The future row is the anchor issued 13 months on, more
    # than a year out, so that a read before issue lands at policy year -1, and
    # future_state gives it its own re-based scenario.  T2's splice grid is built from this
    # spec in a temporary table, not committed.
    #
    # The scenario is a companion, market_scenario_sec.csv (D8): S keys its levels by the
    # month end from issue, and its shipped paths step at months 36 and 72, so each derived
    # and future row reads its own copy re-based to its month, under an id of its own.  It
    # is read through S's reader, market_scenario(), whose Data Reference
    # market_scenario_file names it.
    #
    # T1 holds on RILA at any count: S weights its premium and its acquisition by
    # pols_if(0), the count issued, as SEC weights them by the contracts issued.  It skips
    # two S cells besides the default three:
    #   result_pols: SEC's gains pols_new_biz, the count D5 puts there, so the frame has a
    #     column S's lacks and cannot agree as a whole.  Each column it shares with S is a
    #     cell T1 compares at every month, and the product module compares the report
    #     itself with S's, column by column.
    #   opt_legs: S's tuple of leg names, which no C type holds (R10), is SEC's
    #     opt_leg_count() and opt_leg(i), int leg codes, which the product module maps back
    #     onto S's tuple on every twin.
    # S caches claims(t, kind=None) and claims_over_av(t, kind=None) under (t, None), and
    # market_state(k, name) under its lower-case column names: _rila_codes maps the first
    # to SEC's ALL and the second to SEC's upper-cased codes (R9, R12), and codes maps every
    # other string, the timings, kinds, buckets, legs and markets.  S's float-parameter
    # cells, norm_cdf, the five Black-Scholes cells, opt_component, opt_portfolio,
    # opt_portfolio_abs, credit_rate_at and opt_budget_at_cap, are SEC's engine cells
    # (R14), kept for S's tests and T1 and called by no compiled cell; the projection reads
    # their int-keyed forms.  Phase 2's sizes are spec_sec.py's, derived there.
    "RILA_US_SEC": SecSpec(
        twin="RILA_US_S",
        derived=((1, 71), (2, 36), (13, 80), (13, 72), (4, 30), (15, 59), (12, 40),
                 (7, 119)),
        future=((1, 13),),
        state=_RILA_STATE,
        twin_state={c: f for c, f in _RILA_STATE.items() if c != "scenario_id"},
        exempt=frozenset({"result_pols", "opt_legs"}),
        twin_arg_map=_rila_codes,
        companions={"market_scenario_sec.csv": _rila_rebased_scenarios},
        future_state={"scenario_id": lambda s, k: f"{s.scenario_id()}-F{k}"},
    ),
    # VA's state is 20 columns and the row's scenario (_VA_STATE above), the subaccount
    # values among them, a column for each subaccount the S model's fund table holds, built
    # from the S model the generator reads (model_state, _va_funds).  S's own columns are
    # renamed in place under D6 -- duration_mth_init to duration_mth, and the seven bases'
    # *_init to their cells' *_pp_init -- and av_init, the account value, is dropped for the
    # two subaccount values, which S derives by splitting it by the target allocation.  On
    # every twin each column S has none for takes what S itself assumes, so the twin
    # reproduces S: on point 2 at 26 S's columns, its own split, its inferred withdrawal
    # status, an empty year to date, S's fallback RB at the year's anniversary and no
    # quarterly history.  The derived rows are the first policy year (1 at 6), a
    # year start in force (1 at 120), the year to date after a withdrawal (1 at 131), a
    # depleted opening at a year start (3 at 144), the excess withdrawal in the valuation
    # month and after it (4 at 60 and 65), the highest quarterly step-up base (5 at 40),
    # the VIX fee's prior quarter (6 at 41), a depletion without a withdrawal (8 at 560),
    # the last policy month (7 at 719), a row restated from S's in-force point (2 at S
    # month 14, in force at 40), the basic death benefit after a withdrawal (9 at 125) and
    # a never-withdrawing contract before its GWB Adjustment Date (7 at 100).  The future
    # row is issued 15 months on, more than a year; future_state gives it its own re-based
    # scenario.  T2's splice grid is built from this spec in a temporary table.
    #
    # Both scenarios are companions, return_scenario_sec.csv and rate_scenario_sec.csv
    # (D8), read through S's readers by repointing their *_file References: S keys them by
    # policy month, so on the valuation clock each row needs its own copy, re-based to its
    # duration_mth, which is not its source_mth on rows from S's in-force point 2, and
    # named by the months it moves, so that rows moved alike share one.
    #
    # T1 holds on VA at any count: S already weights its premium by pols_if, and its
    # acquisition falls at t = 0, the issue month of every new-business twin.  It skips one
    # S cell besides the default three:
    #   result_pols: SEC's gains pols_new_biz, the count D5 puts there.  Each column it
    #     shares with S is a cell T1 compares, and the module compares the report itself.
    # At stage EC (M22), S's claims(t, None) and claims_over_av(t, None) keys, the
    # kind=None totals, are SEC's code ALL, and S's scenario_rate columns, "vix_sq" and
    # "cmt10", are SEC's codes named as them upper-cased: the spec's twin_arg_map,
    # _va_twin_args, maps both, and codes maps the rest, the timings, the kinds and the
    # phases.  The three engine cells, lapse_itm_mult, fee_rate_vix_raw and
    # fee_rate_vix_clip, are S's formulas, and sub_ids S's list; each is kept for T1 and
    # a reader and admitted by the registry's "engine" (R14), and T1 compares them at the
    # arguments the module's sweep calls S's with.
    #
    # No projection cell calls a label accessor or compares text: glwb_stepup_basis,
    # gmdb_option, fee_reset_rule and rollup_rule are decoded in Data into the ten 0/1
    # vectors the is_* cells read, each read where S asks its question, so a value S
    # does not know is answered as S answers it, with S's message (R6).  The seven joins
    # on text keys are numbered in Data (R7): the fund set by fund_set_number, which
    # alloc, fund_expense_rate, subaccount_count and subaccount_id read; the scenario by
    # return_scenario_number and rate_scenario_number, which inv_return_mth and
    # scenario_rate read; the programme by txn_number; the grid by gawa_grid_number; the
    # withdrawal charge schedule by cdsc_number; and the sex by mort_schedule.  The
    # subaccount cells keep S's subaccount id as their argument, alloc(i) and sa_pp(t, i),
    # since a point's fund set picks its own ids, keyed alike in the returns and the
    # opening columns, so T1 compares them as S keys them.  phase(t) returns a code
    # (R10), with PRE_ISSUE before issue.
    #
    # The caches, each size with every input it depends on (spec_sec.py).  The GLWB
    # issues at Designated Life ages 35 to 80 (product-spec), and cover runs to attained
    # age omega_age, 120, a Projection Reference:
    #   t: 0 .. 1,140: 1,020 months of cover at the youngest issue age, 35, plus
    #     future_horizon_mth, 120, the frame's last month 1,139, and the month after,
    #     t = proj_len(), which C4's sweep calls: every cell that reads t + 1 is guarded
    #     there, the count's roll-forward residual and av_at's EOM included, so nothing
    #     reads 1,141;
    #   m (t_of_month, prem_scheduled_pm, wd_scheduled_pm): policy months 0 .. 1,019;
    #   k (surr_charge_rate_at): completed years 0 .. 84, each schedule's last year capping
    #     the read; k (phi_glwb_vix, vix_sq): contract quarters 1 .. 340;
    #   x (mort_rate_base_at) and a (gawa_pct_at_age): attained ages 35 .. 119;
    #   i (alloc, fund_expense_rate, sa_pp_init, and beside t): subaccount ids 1 ..
    #     subaccount_id_max, 9; j (subaccount_id): positions 0 .. 8.
    # So spec_sec.py sizes t 1,142, m 1,021, k 342, x and a 121, i and j 10, with one
    # inner width, 10, for the timing, kind, name and subaccount codes, and (1,142, 10,
    # 10) for sa_pp_at; Data.read_last_mth, 1,141, Data.read_last_age, 120, and
    # Data.read_last_sub_id, 9, hold the arrays to the last month, age and id a read
    # reaches.  proj_len refuses an issue age below issue_age_min, 35, or above
    # issue_age_max, 85, glwb_issue_age_max, 80, or, on an elected GMDB,
    # gmdb_issue_age_max, 79, and a fund set holding an id above subaccount_id_max, 9.
    # The float-parameter cells lapse_itm_mult, fee_rate_vix_raw and fee_rate_vix_clip
    # are written inline in lapse_dyn_mult and phi_glwb_vix, and kept as engine cells;
    # lapse_itm_mult's parameter is ratio, a name no size holds.  SEC adds no uncached
    # cell.  S rounds no input per t; rollup_rate's math.floor of the CMT rate becomes a
    # float floor, v // 1.0, exact for every finite v, with S's three raises written out.
    "VA_US_SEC": SecSpec(
        twin="VA_US_S",
        column_map={"duration_mth_init": "duration_mth", "av_init": None,
                    "gwb_init": "gwb_pp_init", "gawa_init": "gawa_pp_init",
                    "bb_init": "bb_pp_init", "rb_init": "rb_pp_init",
                    "np_init": "np_pp_init", "rp_init": "rp_pp_init",
                    "adj_init": "adj_pp_init"},
        duration_of=lambda row: int(row["duration_mth_init"]),
        derived=((1, 6), (1, 120), (1, 131), (3, 144), (4, 60), (4, 65), (5, 40), (6, 41),
                 (8, 560), (7, 719), (2, 14), (9, 125), (7, 100)),
        future=((1, 15),),
        state=_VA_STATE,
        twin_state=_VA_STATE,
        exempt=frozenset({"result_pols"}),
        twin_arg_map=_va_twin_args,
        companions={"return_scenario_sec.csv": _va_rebased_returns,
                    "rate_scenario_sec.csv": _va_rebased_rates},
        future_state={"scenario_id": lambda s, k: f"{s.scenario_id()}-F{k}"},
        model_state=_va_funds,
    ),
    # ULSG's state is S's four columns under their own names, the account value, the
    # shadow account, the loan and the premiums paid to date, and one more, the months
    # already spent in grace (_ULSG_STATE above).  pols_if_init becomes policy_count (the
    # default), and duration_mth is S's own column: ULSG_US_S runs on the projection clock
    # already, and its point 1, the worked example in force 300 months, opens its frame at
    # its own t = 0, so that twin's source_mth is 0 (§5.2).  On the twins grace_mth_init
    # takes what S itself assumes there, 0, so each twin reproduces S; S's four columns stay
    # as its table has them.  The derived rows are S point 1 at 81, a month into its grace,
    # its shadow account below 0, which lapses at t = 1; S point 2 on its 20th anniversary,
    # at 240, its first return-of-premium window at t = 0; S point 2 at 305, mid-year, its
    # account value exhausted and the guarantee carrying it, where the valuation date's
    # anniversaries, on which a year of improvement accrues, and its own part; and S point
    # 3 in its last covered month, 731, a one-row frame whose t = 1 is the month carried
    # into.  No row is restated at or after a lapse: the in-force interface carries no lapse
    # latch, a policy that has lapsed is not in force, and the grace counter's extractor
    # refuses such a month, naming the point (S point 1 from 82, point 2 from 504 and point
    # 4 from 236), as proj_len() refuses a hand-made row whose grace has expired.  The
    # future row is S point 2 issued 25 months after the valuation date, off its
    # anniversaries and more than a year on, so that the months before issue read policy
    # years -2 to 0, where a missing guard would show.  The two pins hold in every month, so
    # each derived and future row copies its twin's, which are blank on S points 2 to 4.
    # T2's splice grid is built from this spec in a temporary table, not committed.
    #
    # T1 holds on ULSG at any count: S charges acquisition on the policies in force in the
    # issue month, the policies issued, as SEC does.  It skips seven S cells besides the
    # default three:
    #   result_pols: SEC's gains pols_new_biz, the count D5 puts there, so the frame has a
    #     column S's lacks and cannot agree as a whole.  Each column it shares with S is a
    #     cell T1 compares at every month, and test_guaranteed_ul_us_sec.py compares the
    #     report itself with S's, on every column both hold.
    #   coi_rate_scale: S's guaranteed COI scale for the point's cell, a Series, which no
    #     compiled cell returns (R10).  SEC numbers the scale instead, coi_schedule, and
    #     every value of it reaches T1 through coi_rate_guar and coi_rate_guar_at, which T1
    #     compares at every month and attained age S read.
    #   status: S's labels "IN FORCE" and "IN FORCE - GUARANTEE" name no Reference, so
    #     codes() cannot map S's text onto SEC's codes, IN_FORCE and IN_FORCE_GUARANTEE.
    #     result_av's status column, which T1 compares, holds S's labels at stage EC as at
    #     E, and test_guaranteed_ul_us_sec.py holds the cell to S's labels by its code.
    #   solve_len, sg_pp_solve, guar_min_sg and no_lapse_premium: S's funding-premium
    #     solve, a side calculation that no projection cell of S reads and S's sweep reaches
    #     none of, so T1 has no key of theirs to lose.  SEC reads the premium from its model
    #     point, a value fixed at issue (D6), as basiclife.BasicTerm_SE reads its premium
    #     from a table, and leaves the solve to S.  Kept unchanged, the solve replays the
    #     shadow account from the frame's first month, its base an R1a test at t == 0, so on
    #     a row in force it solves from the valuation date, and on a row issued later, whose
    #     months before issue enter its minimum at 0, it raises "no funding premium found";
    #     its cells take the premium as a float, with dict caches of 7,900 to 18,300
    #     entries (R14).  MYGA, FIA, DIA, RILA and VA keep S's engine cells at stage E,
    #     for S's tests and T1, which call them; ULSG's solve is no engine of its
    #     projection, and its tests stay S's.  A user solves a row in force by giving
    #     ULSG_US_S an S row that carries the row's state, which solves from that row's
    #     own start.
    # S's net_cf calls claims(t) with its kind=None default, so S's sweep caches claims
    # under (t, None), and its result_cf under (t, "DEATH"), (t, "LAPSE") and
    # (t, "REFUND").  At stage EC claims is split into claims_death, claims_lapse and
    # claims_refund, the result_cf columns, and a total claims(t), Python's compensated
    # sum written out, since all three pay in one month on a return-of-premium anniversary
    # (R12), so the spec's twin_arg_map, _ul_claims_total, maps S's total onto SEC's and
    # skips the kind keys, whose values reach T1 through result_cf.  The label accessors
    # (sex, rate_class, premium_type, premium_mode, surr_charge_id) are called by no
    # projection cell, and are declared reporting.  The pins became a value array, NaN
    # where blank, and a 0/1 flag array, and the precision an int array, -1 where blank
    # (R8).  coi_rate and sg_coi_rate round a rate built from a Projection Reference with
    # round(r, dp), which Data cannot precompute, so the call stays, admitted by cell
    # (R16), and is_rop_anniv tests a zero-padded flag array.  No cell takes a float
    # parameter, and SEC adds no uncached cell.
    #
    # Phase 2's sizes, each with the inputs it depends on.  The contract issues at ages 18
    # to 80, S4's Standard classes to 85 (product-spec), and S projects any age its tables
    # serve: the shipped COI scale serves the anchor cell from attained age 45 only.  At
    # stage E Data refuses an issue age only below 0 or not whole, and proj_len() one at
    # or past charges_cease_age; Phase 2's proj_len() refuses one below 18, as UL's C step
    # does, and every size below rests on it:
    #   t: 0 to 1,356, 1,357 values: 12 x (charges_cease_age 121 - youngest issue age 18)
    #     = 1,236 months of cover, plus future_horizon_mth 120, and t = proj_len(), which
    #     the count, the account value's opening timing and the lapse latch are carried
    #     into and pols_lapse_grace(proj_len() - 1) reads through is_lapsed(t + 1).
    #   mort_improve_factor and mort_improve_rate: t from 0, before issue on a future row,
    #     each at least 12 months back in mort_improve_rate.
    #   policy years y (lapse_rate_base_py): 1 to 103, the year of the last covered month
    #     at the youngest issue age; the lapse table's last year, 21 as shipped, clamps it.
    #   attained ages a (mort_rate_base_at, corridor_factor_at, coi_rate_guar_at): the
    #     youngest issue age, 18, to 120, read only in cover.  Each table's reader clamps
    #     the age to the table's first and last ages, as S's does, and Data accepts any run
    #     of ages: the mortality table's first, 45 as shipped, clamps from below with an
    #     effect on the shipped table, at issue ages below 45; on the shipped tables the
    #     corridor's first age, 18, binds only below issue age 18, which Data accepts at
    #     stage E and Phase 2's proj_len() refuses, and neither table's last age binds in
    #     cover, which ends at 120, the mortality table's last age, below the corridor's,
    #     121; on a table shorter than the cover each of the three binds with an effect,
    #     which test_guaranteed_ul_us_sec.py shows on tables shortened at both ends.  The
    #     COI scale clamps at its cell's last age, 121 as shipped, and has no lower clamp,
    #     as in S: an age below its cell's first raises S's KeyError at the read, until R7.
    #     db_pp's inner floor, max(AV', 0.0), changes no death benefit while every corridor
    #     factor is 0 or more and the face above 0, which Data holds both to: where AV' is
    #     below 0 the corridor's amount is 0 or less either way, and the face wins.
    #   anniversaries y (is_rop_anniv): 0 to 102, each anniversary in cover;
    #     rop_ratio_anniv and rop_rate_anniv at the table's anniversaries alone.
    #   depth: a cold net_cf of the last month runs one cell a month back to t_entry() and
    #     14 to 18 more on the committed rows, and at the longest cover, issue age 18, 17
    #     more at the valuation date, 1,252 levels, and 21 issued 120 months on, 1,256,
    #     where the first month's mortality reads the improvement factor of the ten years
    #     before issue: about 313 KiB of C stack at gcc's 255 bytes a level.  Each chain's
    #     head called cold and alone, on a read of its own, runs at most 12 more on the
    #     committed rows, the count's the deepest, which runs 13 more at the longest cover
    #     at the valuation date and 17 issued 120 months on.  The factor is one cell a
    #     year, at most 27 deep called cold.  An ascending sweep needs a
    #     recursion limit of 16 on the committed rows, against ULSG_US_S's 14, and 19 on a
    #     row issued 120 months on, whose first month reads the factor cold, so
    #     sample_sec.py and run_sec.py --cython size theirs from future_horizon_mth; the
    #     limit grows with the horizon up to the factor's cap of 20 years.  In modelx's
    #     export, sys.setrecursionlimit set after the import, the cold net_cf of the last
    #     month needs 916 on the twin of S point 1, 432 months, 1,516 on the committed rows
    #     of 732 months on the books, the twin of S point 3 and the row issued 25 months on,
    #     and 2,524 at the longest cover, issued now and 120 months on; the ascending sweep
    #     of the reports and checks needs 54 everywhere, against ULSG_US_S's 3,929 to 5,977
    #     cold on its four points and 52 ascending.
    # The lapse rate is min(lapse_rate_cap, max(lapse_rate_floor, rate)), in S's order:
    # with the two References from 0 to 1 it is a probability whatever its product, so no
    # count turns complex through it.  The mortality cap is S's, min(q, 1.0), and no
    # departure.
    "ULSG_US_SEC": SecSpec(
        twin="ULSG_US_S",
        duration_of=lambda row: int(row["duration_mth"]),
        derived=((1, 81), (2, 240), (2, 305), (3, 731)),
        future=((2, 25),),
        state=_ULSG_STATE,
        twin_state={"grace_mth_init": _ULSG_STATE["grace_mth_init"]},
        exempt=frozenset({"result_pols", "solve_len", "sg_pp_solve", "guar_min_sg",
                          "no_lapse_premium", "coi_rate_scale", "status"}),
        twin_arg_map=_ul_claims_total,
    ),
    # IUL's state is S's two columns and six more (_IUL_STATE above): the account value and
    # the loan, under S's names; the fixed account and the loan collateral apart from the
    # loan, which S's in-force entry merges (it opens the fixed account at the account value
    # less the loan and the collateral at the loan); the face in force; the two running
    # totals S opens at 0, the premiums less withdrawals and the no-lapse guarantee's
    # accumulator, premiums less withdrawals and loans; and the MEC latch, which S does not
    # keep, so its extractor reads whether S's 7-pay test failed in any month before d.  The
    # live index segments, which S cannot open at all, go in a long companion,
    # inforce_segments_sec.csv, keyed (point_id, slot), slot the months since a segment's
    # creation at the valuation date (§7.4): one row a month for each derived row's last
    # min(12, d) months, built from S's own ladder by _iul_ladder, each start level rebased
    # onto SEC's index path.  pols_if_init becomes policy_count (the default), and
    # duration_mth is S's own column: IUL_US_S runs on the projection clock and ships no
    # point in force, so every twin is new business at source_mth 0, and the six new
    # columns take what S itself assumes there, 0; S's two columns stay as its table has
    # them.  The derived rows are S point 1 on its fifth anniversary, 60, an annual premium
    # falling at t = 0 and the segment born at its fourth anniversary maturing there; S
    # point 4 mid-year at 65, paying monthly, all twelve segments live, its surrender
    # charge and its no-lapse guarantee in force; S point 5 at 6, mid-way through its first
    # year, its ladder six months deep with one segment swept, whose guarantee fails for
    # good at policy month 49, in frame; S point 5 at 384, its fixed account below 0
    # entering the month and its loan above its cash value, and at 605, its account value
    # below 0 too, the exhausted states S carries by design and Data accepts; and S point 1
    # at 888, two years before the end of its projection, which reaches the COI scale's and
    # the mortality table's last rows.  The future row is S point
    # 4 issued 25 months after the valuation date, more than a year on, so that the months
    # before issue read policy years -2 to 0, where a missing guard would show.  T2's
    # splice grid is built from this spec in a temporary table, not committed.
    #
    # IUL_US_S ships no point in force, so IN_FORCE_TWINS is empty, but the generator
    # restates one: _iul_ladder sizes a row's ladder by its own duration_mth, the slots S
    # held from its own month 0 read from S and the older ones empty, as S assumes.  A T2
    # case on such a point needs two things beside the generator: an arg_map moving S's
    # segment month m, a projection month, to the policy month m + duration_mth_init on
    # the six (t, m) segment cells and on seg_new_pp, with the arg_map's cut-off of
    # segments matured before the valuation date moved likewise; and exemptions, with
    # their reasons, for cred_rate_ann and comp_rate_ann, whose first-segment test runs on
    # the policy clock here and on S's projection clock there, and for result_seg's
    # seg_return before S's first maturity, which S guards by its own month.
    #
    # T1 holds on IUL at any count: S charges acquisition on the policies in force in the
    # issue month, the policies issued, as SEC does.  It skips two S cells besides the
    # default three:
    #   result_pols: SEC's gains pols_new_biz, the count D5 puts there, so the frame has a
    #     column S's lacks and cannot agree as a whole.  Each column it shares with S is a
    #     cell T1 compares at every month, and test_indexed_ul_us_sec.py compares the
    #     report itself with S's, on every column both hold.
    #   check_margin: SEC states the margin identity with the debt a surrender recovers,
    #     min(loan_bal_pp(t), csv_pp(t)), as UL_US_SEC, VUL_US_SEC and ULSG_US_SEC do,
    #     where S adds back the whole loan, which holds only while the cash value covers
    #     it.  S's check is False on its point 5, whose loan overruns its cash value from
    #     policy month 383, and SEC's True; on points 1 to 4 both are True.
    # S's net_cf calls claims(t) with its kind=None default, so S's sweep caches claims
    # under (t, None), and its result_cf under (t, kind).  At stage EC claims is a total
    # cell, claims(t), and two cells of a kind, claims_death(t) and claims_lapse(t) (R12),
    # and the six (t, m) segment cells are keyed by slot, (t, k), k = duration_mth(t) - m
    # (R15), so the spec's twin_arg_map, _iul_twin_args, maps S's total onto SEC's, skips
    # S's kind keys, and moves S's creation month to the slot.  S's projection calls its
    # engine cells with their None defaults, index_credit_rate(r, None),
    # seg_credit_base(b, d, None) and index_credit(b, d, r, None, None), and SEC keeps the
    # five engine cells (index_change, index_credit_rate, seg_credit_base, index_credit,
    # seg_matured_value) for S's worked example and for T1, which compares S's keys
    # through them unmapped, S's "REMAINING" read as its code (R14); no SEC projection cell
    # calls them, the credit inlined into seg_return, seg_credit_rate and
    # index_credit_pp.  T1 skips one more S cell: coi_rate_scale, a Series sliced from
    # the COI table, which no compiled cell can hold; SEC reads the scale through
    # coi_schedule() and the Data array instead, and every rate S reads from it reaches T1
    # through coi_rate_guar_py and coi_rate_guar.  The label accessors (sex, rate_class,
    # db_option, qual_test, premium_type, premium_mode, surr_charge_id) are called by no
    # projection cell, and are declared reporting.
    #
    # The compiled model's sizes are spec_sec.py's, each with the References it rests on:
    # the contract issues at ages 0 to 85 (product-spec), which proj_len() holds by
    # issue_age_min and issue_age_max, the projection ends at maturity_age, 121, and the
    # segment term is seg_term_mth, 12, the width of every 2-D cache.
    "IUL_US_SEC": SecSpec(
        twin="IUL_US_S",
        duration_of=lambda row: int(row["duration_mth"]),
        derived=((1, 60), (4, 65), (5, 6), (5, 384), (5, 605), (1, 888)),
        future=((4, 25),),
        state=_IUL_STATE,
        twin_state={c: f for c, f in _IUL_STATE.items()
                    if c not in ("av_pp_init", "loan_bal_init")},
        exempt=frozenset({"result_pols", "check_margin", "coi_rate_scale"}),
        companions={"inforce_segments_sec.csv": _iul_ladder},
        twin_arg_map=_iul_twin_args,
    ),
}


def _derived_policy_id(policy_id, d):
    return f"{policy_id}-M{d}"


def _future_policy_id(policy_id, k):
    return f"{policy_id}-F{k}"


def _derived_provenance(point_id, policy_id, d):
    return f"S point {point_id} ({policy_id}) restated in force at S month {d}"


def _future_provenance(point_id, policy_id, k):
    months = "month" if k == 1 else "months"
    return f"S point {point_id} ({policy_id}) issued {k} {months} after the valuation date"


def _sec_columns(spec, s_table, rename, added=()):
    """The SEC table's columns, in order.

    S's columns in S's order, renamed or dropped by ``rename``; then ``policy_count`` and
    ``duration_mth``, each where S has no column of that name; then the state columns S
    lacks, in the order the spec names them: ``added``, those ``model_state`` gave, then
    ``twin_state``'s, ``state``'s and ``future_state``'s; then the generator's own columns;
    and ``provenance`` last, where the S table has one, as every table in the library keeps
    it.
    """
    columns = [rename.get(c, c) for c in ["point_id", *s_table.columns]]
    columns = [c for c in columns if c is not None]
    provenance = "provenance" in columns
    if provenance:
        columns.remove("provenance")
    for c in ("policy_count", "duration_mth", *added, *spec.twin_state, *spec.state,
              *spec.future_state):
        if c not in columns:
            columns.append(c)
    for c in GENERATED_COLUMNS:
        if c in columns:
            raise ValueError(f"{spec.twin}'s table has a {c!r} column, which the generator "
                             f"writes itself")
        columns.append(c)
    if provenance:
        columns.append("provenance")
    if len(set(columns)) != len(columns):
        dupes = sorted({c for c in columns if columns.count(c) > 1})
        raise ValueError(f"column_map gives two columns one name: {dupes}")
    return columns


def _model_state(spec, s_model):
    """The columns ``spec.model_state`` gives for ``s_model``, checked; ``{}`` if none."""
    if spec.model_state is None:
        return {}
    added = dict(spec.model_state(s_model))
    clash = sorted(set(added) & (_RESERVED | {"policy_count"}))
    if clash:
        raise ValueError(f"model_state may not set {clash}: the generator owns them")
    twice = sorted(set(added) & (set(spec.state) | set(spec.twin_state)))
    if twice:
        raise ValueError(f"model_state sets {twice}, which state or twin_state sets too")
    return added


def build_sec_table(spec, s_model):
    """Build the SEC model point table and its companions from the S model as it stands.

    ``s_model`` is the S model, read from the product directory whose files are wanted; its
    ``Data.model_point_table()`` is the S table, and its ``Projection`` supplies the
    counts and the opening state.

    The rows, in order (see :class:`SecSpec` for the kinds):

    twins
        every S row, with the same ``point_id`` and ``policy_id``, renamed by
        ``column_map``.  ``policy_count`` is the S count; ``duration_mth`` comes from
        ``duration_of``; ``source_mth`` is the first row of the S point's own
        ``result_cf()``: 0 when S projects it from the valuation date, its entry month (108
        for WholeLife point 1) when S keeps the policy clock.  Any other first row means
        ``duration_of`` is wrong, and raises here, before a misaligned twin can reach T1.
    derived rows, for each ``(p, d)``
        the twin of S point ``p``, opened at S month ``d``: ``policy_count`` is
        ``pols_if(d)``, the count S carries into month ``d``; ``duration_mth`` is the twin's
        moved on by ``d - source_mth``, which is ``d`` on new business; ``source_mth`` is
        ``d``; and then ``model_state`` and ``state`` set the opening state.  ``d`` must
        fall inside S's frame, after the twin's own entry month.
    future rows, for each ``(p, k)``
        the twin of new-business point ``p``, issued ``k`` months after the valuation
        date: ``duration_mth`` and ``source_mth`` are ``-k``, and the count is S's; then
        ``future_state`` sets the columns it names.

    Derived and future rows take fresh ``point_id`` s after the largest S one, in the
    spec's order, so the numbering is fixed by the spec, never by a dict or a filesystem.
    Their ``policy_id`` is composed from S's and the month (``TL-000001-M120``,
    ``TL-000001-F3``), and where the S table has a ``provenance`` column theirs is composed
    the same way, citing S's point and policy and the month.  Every other text cell is
    copied from S.  That is D8's rule under ``CLAUDE.md``: the generator adds no name, and
    a reworded S cell reaches the SEC table through T6.

    Returns ``(table, companions)``: the table on a default index, ``point_id`` its first
    column, exactly as the file is written; and ``{filename: DataFrame}`` from the spec's
    companion builders.

    Every S point's ``result_cf()`` is projected, to find its first row.  Pass a model whose
    points are already swept, the instance T1 swept, and that costs nothing.
    """
    s_table = s_model.Data.model_point_table()
    if s_table.index.name != "point_id" or "policy_id" not in s_table.columns:
        raise ValueError(f"{spec.twin}: the S table is not indexed by point_id with a "
                         f"policy_id column")
    ids = [int(i) for i in s_table.index]
    if len(set(ids)) != len(ids):
        raise ValueError(f"{spec.twin}: the S table repeats a point_id")
    rename = {"pols_if_init": "policy_count", **spec.column_map}
    unknown = [c for c in rename if c not in s_table.columns]
    if unknown:
        raise ValueError(f"column_map names {unknown}, which {spec.twin}'s table lacks")
    if "point_id" in rename or "policy_id" in rename:
        raise ValueError("point_id and policy_id carry over unchanged")
    if "policy_count" not in rename.values():
        raise ValueError("no S column becomes policy_count")
    added = _model_state(spec, s_model)
    columns = _sec_columns(spec, s_table, rename, added)
    projs = {pid: s_model.Projection[pid] for pid in ids}
    provenance = "provenance" in columns

    twins = {}
    for record in s_table.reset_index().to_dict("records"):
        pid = int(record["point_id"])
        duration = int(spec.duration_of(s_table.loc[pid]))
        source = int(projs[pid].result_cf().index[0])
        if duration < 0:
            raise ValueError(f"{spec.twin} point {pid}: duration_of gives {duration}; an S "
                             f"row is in force or new business, never future business")
        if source not in (0, duration):
            raise ValueError(
                f"{spec.twin} point {pid}: S opens its frame at t = {source}, which is "
                f"neither the valuation date (0) nor its duration_mth ({duration}); "
                f"duration_of does not describe this row")
        row = {rename.get(c, c): v for c, v in record.items()
               if rename.get(c, c) is not None}
        row["point_id"] = pid
        row["duration_mth"] = duration
        for column, extract in {**added, **spec.twin_state}.items():
            row[column] = extract(projs[pid], source)
        row.update(row_kind="twin", source_policy_id=record["policy_id"],
                   source_mth=source)
        twins[pid] = row

    def twin_of(p, kind):
        if p not in twins:
            raise ValueError(f"a {kind} row names point {p}, which {spec.twin}'s table "
                             f"lacks")
        return twins[p]

    rows = list(twins.values())
    fresh = itertools.count(max(ids) + 1)
    for p, d in spec.derived:
        twin = twin_of(p, "derived")
        proj, source = projs[p], twin["source_mth"]
        if not source < d < proj.proj_len():
            raise ValueError(
                f"derived row ({p}, {d}): d must fall after the twin's entry month "
                f"({source}) and inside S's frame, which ends at {proj.proj_len() - 1}")
        row = dict(twin, point_id=next(fresh),
                   policy_id=_derived_policy_id(twin["policy_id"], d),
                   policy_count=proj.pols_if(d),
                   duration_mth=twin["duration_mth"] + d - source)
        if provenance:
            row["provenance"] = _derived_provenance(p, twin["policy_id"], d)
        for column, extract in {**added, **spec.state}.items():
            row[column] = extract(proj, d)
        row.update(row_kind="derived", source_policy_id=twin["policy_id"], source_mth=d)
        rows.append(row)
    for p, k in spec.future:
        twin = twin_of(p, "future")
        if twin["duration_mth"] != 0 or twin["source_mth"] != 0:
            raise ValueError(f"future row ({p}, {k}): point {p} is in force in S, and only "
                             f"new business can be written later")
        if k < 1:
            raise ValueError(f"future row ({p}, {k}): k counts months after the valuation "
                             f"date, so it is at least 1")
        row = dict(twin, point_id=next(fresh),
                   policy_id=_future_policy_id(twin["policy_id"], k), duration_mth=-k)
        if provenance:
            row["provenance"] = _future_provenance(p, twin["policy_id"], k)
        for column, extract in spec.future_state.items():
            row[column] = extract(projs[p], k)
        row.update(row_kind="future", source_policy_id=twin["policy_id"], source_mth=-k)
        rows.append(row)

    table = pd.DataFrame(rows, columns=columns)
    for key in ("point_id", "policy_id"):
        dupes = sorted(table.loc[table[key].duplicated(), key].astype(str))
        if dupes:
            raise ValueError(f"the SEC table repeats {key} {dupes}; is a (point, month) "
                             f"pair listed twice?")
    companions = {}
    for filename, build in spec.companions.items():
        frame = build(s_model, table.copy())
        if not isinstance(frame, pd.DataFrame):
            raise TypeError(f"the builder of {filename} returned a "
                            f"{type(frame).__name__}, not a DataFrame")
        companions[filename] = frame
    return table, companions


_read_names = itertools.count(1)


def _spec(spec_name):
    try:
        return SEC_SPECS[spec_name]
    except KeyError:
        known = ", ".join(sorted(SEC_SPECS)) or "none yet"
        raise KeyError(f"no SecSpec is registered for {spec_name!r} "
                       f"(registered: {known})") from None


def _generated_texts(spec_name, product_dir, s_model):
    """Build one spec's files and render them: ``(product_dir, {filename: text})``."""
    spec = _spec(spec_name)
    if product_dir is None:
        if spec.twin not in MODELS:
            raise ValueError(f"{spec.twin} is not a registered model, so its product "
                             f"directory is unknown; pass product_dir")
        product_dir = model_path(spec.twin).parent
    product_dir = pathlib.Path(product_dir)
    own = s_model is None
    if own:
        s_model = mx.read_model(product_dir / spec.twin,
                                name=f"{spec.twin}_secgen_{next(_read_names)}")
    try:
        table, companions = build_sec_table(spec, s_model)
    finally:
        if own:
            s_model.close()
    texts = {spec.model_point_file: _csv_text(table)}
    texts.update({name: _csv_text(frame) for name, frame in companions.items()})
    return product_dir, texts


def write_generated(spec_name, product_dir=None, *, s_model=None):
    """Write one SEC model's generated input files from its S model as it stands.

    ``spec_name`` is the SEC model's name in :data:`SEC_SPECS`.  ``product_dir`` is the
    product directory the S model and its inputs are read from, and the files written to,
    by default the S model's own in the registry.  ``s_model`` may pass an S model already
    read from that directory, and swept, to save reading and projecting it again; one read
    here is read under a name of its own and closed.

    The writing is deterministic, so a rewrite with no S change is a no-op: a file that
    :func:`check_generated` finds current is not touched, its bytes and its modification
    time left alone.  That includes a file whose floats are spelled otherwise but agree in
    value, as a file written on another platform may (module docstring), so regenerating
    on a second platform does not churn the committed files.

    Returns ``{path: changed}`` for every file the spec generates.
    """
    product_dir, texts = _generated_texts(spec_name, product_dir, s_model)
    changed = {}
    for name, text in texts.items():
        path = product_dir / name
        changed[path] = bool(_file_drift(name, path, text))
        if changed[path]:
            path.write_bytes(text.encode("utf-8"))
    return changed


# T6 reads a float cell by its value, to these tolerances, not by its spelling (module
# docstring).  Far tighter than the 1e-9 of every comparison above, so nothing T2 could see
# passes here; far looser than the last-bit differences between platforms' parsers and
# libms, so none of those fails here.
_DRIFT_RTOL = 1e-12
_DRIFT_ATOL = 1e-12

# A float as the writer spells one: with a decimal point or an exponent, so that ``1`` and
# ``1.0``, which pandas reads into columns of different dtypes, stay different cells.
_FLOAT_TEXT = re.compile(r"[+-]?(?:\d+\.\d*|\.\d+|\d+(?=[eE]))(?:[eE][+-]?\d+)?")


def _same_cell(committed, generated):
    """Whether a committed cell says what the generated one says.

    The same text, or two float spellings whose values agree to ``_DRIFT_RTOL`` and
    ``_DRIFT_ATOL``.  ``None`` stands for a cell a committed row is missing, and matches
    nothing.
    """
    if committed == generated:
        return True
    if committed is None or generated is None:
        return False
    if _FLOAT_TEXT.fullmatch(committed) and _FLOAT_TEXT.fullmatch(generated):
        return _close(float(committed), float(generated), _DRIFT_RTOL, _DRIFT_ATOL)
    return False


def _rows_text(rows):
    """The CSV text of parsed rows, in the dialect :func:`_csv_text` writes."""
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows(rows)
    return buf.getvalue()


def _file_drift(name, path, generated):
    """:func:`_csv_drift` against the committed file at ``path``, which may be missing."""
    if not path.is_file():
        return [f"{name}: generated, but not committed"]
    try:
        committed = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        return [f"{name}: the committed file is not UTF-8; regenerate it"]
    return _csv_drift(name, committed, generated)


def _csv_drift(name, committed, generated):
    """The cell-by-cell differences between a committed CSV text and the generated one.

    Cells compare by :func:`_same_cell`: as text, but a float by its value.  So two files
    that differ only in how their floats are spelled have no drift.  A file whose cells
    agree but whose text is not what the writer writes (other quoting, CRLF line ends, no
    final newline) is reported, so that it is rewritten.
    """
    if committed == generated:
        return []
    old = list(csv.reader(io.StringIO(committed)))
    new = list(csv.reader(io.StringIO(generated)))
    old_head, old_rows = (old[0], old[1:]) if old else ([], [])
    new_head, new_rows = (new[0], new[1:]) if new else ([], [])
    lines = []
    added = [c for c in new_head if c not in old_head]
    removed = [c for c in old_head if c not in new_head]
    if added:
        lines.append(f"{name}: columns the generator now writes: {added}")
    if removed:
        lines.append(f"{name}: columns the generator no longer writes: {removed}")
    if not added and not removed and old_head != new_head:
        lines.append(f"{name}: the columns are in a different order")
    key = new_head[0] if new_head else "row"

    def ident(row):
        return f"{key} {row[0]}" if row else "a blank line"

    for i in range(max(len(old_rows), len(new_rows))):
        if i >= len(old_rows):
            lines.append(f"{name}: row {i + 1} ({ident(new_rows[i])}) is generated but "
                         f"not committed")
            continue
        if i >= len(new_rows):
            lines.append(f"{name}: committed row {i + 1} ({ident(old_rows[i])}) is no "
                         f"longer generated")
            continue
        if len(old_rows[i]) > len(old_head):
            lines.append(f"{name}: committed row {i + 1} ({ident(old_rows[i])}) has cells "
                         f"beyond its header: {old_rows[i][len(old_head):]}")
        # zip_longest, not zip: a committed row cut short must show its missing cells as
        # missing (None), not drop them from the comparison.
        was = dict(itertools.zip_longest(old_head, old_rows[i]))
        now = dict(itertools.zip_longest(new_head, new_rows[i]))
        for c in new_head:
            if c in old_head and not _same_cell(was.get(c), now.get(c)):
                lines.append(f"{name}: row {i + 1} ({ident(new_rows[i])}), {c}: "
                             f"committed {was.get(c)!r}, generated {now.get(c)!r}")
    if not lines and _rows_text(old) != committed:
        lines.append(f"{name}: the cells agree, but the text differs (quoting or line "
                     f"ends); regenerate it")
    return lines


def check_generated(spec_name, product_dir=None, *, s_model=None):
    """T6: where the committed generated files differ from what S now generates.

    Builds the files as :func:`write_generated` would and compares each with the committed
    one, cell by cell: ``"model_point_table_sec.csv: row 3 (point_id 3), policy_id:
    committed 'TL-000001-M12', generated 'TL-900001-M12'"``.  A cell compares as text,
    except that a float compares by value, to 1e-12 relative or absolute.  The spelling
    the writer picks, and the last bits of a computed value, can differ from one platform
    or pandas to another (module docstring), and a file committed from one must check
    clean on the rest.  ``1`` against ``1.0`` is still drift, since it changes the column's
    dtype.  A file whose cells agree but whose text is not the writer's (quoting, line
    ends) is reported, and so is a missing file.

    So an edit to an S row that an SEC file copies or derives from, such as a reworded
    ``provenance`` cell or a renamed lookup key, fails T6 until the files are regenerated,
    in the same commit (§5.2).  The fix is ``python tools/gen_sec_points.py <name>``, or
    :func:`write_generated` where ``tools/`` is absent, as in a ``lifelib.create()`` copy.

    Takes the same arguments as :func:`write_generated`, and returns the drift lines, empty
    when the committed files are current.
    """
    product_dir, texts = _generated_texts(spec_name, product_dir, s_model)
    lines = []
    for name, text in texts.items():
        lines += _file_drift(name, product_dir / name, text)
    return lines


# ---------------------------------------------------------------------------
# C2 -- the Phase 1 fingerprint


FINGERPRINT_REPORTS = ("result_cf", "result_pols")
"""The reports a fingerprint freezes: the cash flows, and the counts behind them (§5.4).

``result_pols`` carries what no ``result_cf`` column shows, the decrements one by one and
the expiries, and it is cheap, so it is frozen beside the cash flows.
"""

FINGERPRINT_RTOL = 1e-12
"""C2's tolerance: relative, floored at the same fraction of the column's own magnitude."""


def fingerprint_months(rows):
    """The months a fingerprint holds a column's values at, for a frame of ``rows`` months.

    The first and the last month of the frame and the three quartiles between them,
    ``(k * (rows - 1)) // 4`` for ``k = 0 .. 4``, without repeats: ``(0, 179, 359, 539,
    719)`` for a 720-month frame, ``(0,)`` for a one-month frame.  The rule knows nothing
    of the product, so every SEC model freezes its points the same way.
    """
    return tuple(sorted({(k * (rows - 1)) // 4 for k in range(5)}))


def _report_print(df, months):
    """``{column: (sum, scale, values)}`` for one report frame, at ``months``."""
    return {column: (float(df[column].sum()), float(df[column].abs().max()),
                     tuple(float(df[column].iloc[t]) for t in months))
            for column in df.columns}


def _point_frames(model):
    """``(label, {report: frame})`` for every model point of ``model``, in table order."""
    from us_registry import point_keys, projection
    labels = model.Data.model_point_table().index
    for key, label in zip(point_keys(model), labels):
        proj = projection(model, key)
        yield int(label), {name: proj.cells[name]() for name in FINGERPRINT_REPORTS}


def fingerprint(model):
    """What ``model`` computes on each model point, in brief: ``{point_id: {...}}`` (§5.4).

    Each point is keyed by its table label, which names the same point whether
    ``Projection`` is indexed by label or by position.  Its entry holds ``"rows"``, the
    frame's length; ``"months"``, :func:`fingerprint_months` of it; and, for each report
    of :data:`FINGERPRINT_REPORTS`, ``{column: (sum, scale, values)}`` in the report's
    column order: the column's sum over the frame, its largest absolute value, which is the
    magnitude its tolerance is measured against, and its values at the months, each a
    Python float.  A report must be indexed ``t = 0 .. rows - 1``, as every SEC frame is.
    """
    out = {}
    for label, frames in _point_frames(model):
        rows = len(frames[FINGERPRINT_REPORTS[0]])
        months = fingerprint_months(rows)
        entry = {"rows": rows, "months": months}
        for name, df in frames.items():
            if list(df.index) != list(range(rows)):
                raise ValueError(f"{model.name} point {label}: {name}() is not indexed "
                                 f"t = 0 .. {rows - 1}")
            entry[name] = _report_print(df, months)
        out[label] = entry
    return out


def _wrapped(text, indent, width=92):
    """``text`` wrapped at its spaces alone, within ``width`` columns, under ``indent``.

    Never inside a word: ``textwrap`` would break ``1.99e-05`` at its hyphen, and the
    literal would no longer read back as the number.
    """
    import textwrap
    return textwrap.wrap(text, width=width, initial_indent=indent,
                         subsequent_indent=indent, break_long_words=False,
                         break_on_hyphens=False)


def fingerprint_text(name, frozen):
    """``frozen`` written out as the literal a product module holds, its markers included.

    One entry per point, one item per column: ``(sum, scale, (values at the months))``,
    the values wrapped beneath within the house's 92 columns.  Every float is its shortest
    ``repr``, which Python reads back as the same double, so the literal is the freeze
    exactly; that is checked here, by reading the text back, before it is returned.
    """
    out = [f"# BEGIN generated fingerprint: {name} -- tools/gen_sec_fingerprint.py",
           "FINGERPRINT = {"]
    for label, entry in frozen.items():
        out.append(f"    {label}: {{\"rows\": {entry['rows']}, "
                   f"\"months\": {entry['months']!r},")
        for report in (k for k in entry if k not in ("rows", "months")):
            out.append(f"        \"{report}\": {{")
            for column, (total, scale, values) in entry[report].items():
                out.append(f"            \"{column}\": ({total!r}, {scale!r}, (")
                text = ", ".join(repr(v) for v in values)
                out += _wrapped(text + (",)),"  if len(values) == 1 else ")),"), " " * 16)
            out.append("        },")
        out.append("    },")
    out += ["}", f"# END generated fingerprint: {name}"]
    text = "\n".join(out) + "\n"
    long = [line for line in out if len(line) > 92]
    namespace = {}
    exec(text, namespace)                       # the text this function has just written
    if long or namespace["FINGERPRINT"] != frozen:
        raise ValueError(f"the fingerprint of {name} does not write out exactly: "
                         f"{len(long)} lines over 92 columns, or a value that reads back "
                         f"as another")
    return text


def _fp_close(a, b, floor):
    """C2's comparison: within :data:`FINGERPRINT_RTOL` of the larger, or of ``floor``."""
    return abs(a - b) <= FINGERPRINT_RTOL * max(abs(a), abs(b), floor)


def fingerprint_mismatches(frozen, model):
    """C2: where ``model`` departs from the fingerprint ``frozen``, a line per departure.

    The same points in the same order, frames of the same length, and the same reports
    with the same columns in the same order, exactly.  Then each column, at the months the
    freeze names: its values, each held to ``1e-12 * scale``, its scale held the same way,
    so that a spike in a month the freeze does not name is still seen, and its sum to
    ``1e-12 * rows * scale``; and each to 1e-12 of the larger of the two where that is
    larger still (:data:`FINGERPRINT_RTOL`).  So a frozen zero is compared as finely as
    the column's own magnitude allows and no finer, and a column whose scale is 0, such as
    the conversion credits at the shipped zero conversion rates, must stay exactly 0.

    Returns readable lines, empty when the model reproduces the freeze.
    """
    lines = []
    found = list(_point_frames(model))
    if [label for label, _ in found] != list(frozen):
        return [f"points: frozen {list(frozen)}, now {[label for label, _ in found]}"]
    for label, frames in found:
        entry = frozen[label]
        rows = len(frames[FINGERPRINT_REPORTS[0]])
        if rows != entry["rows"]:
            lines.append(f"point {label}: {rows} rows, frozen {entry['rows']}")
            continue
        for report in (k for k in entry if k not in ("rows", "months")):
            df = frames.get(report)
            if df is None or list(df.columns) != list(entry[report]):
                got = None if df is None else list(df.columns)
                lines.append(f"point {label}: {report} columns {got}, frozen "
                             f"{list(entry[report])}")
                continue
            if list(df.index) != list(range(rows)):
                lines.append(f"point {label}: {report} is not indexed t = 0 .. {rows - 1}")
                continue
            now = _report_print(df, entry["months"])
            for column, (total, scale, values) in entry[report].items():
                where = f"point {label}: {report}[{column!r}]"
                n_total, n_scale, n_values = now[column]
                if not _fp_close(total, n_total, rows * scale):
                    lines.append(f"{where} sums to {n_total!r}, frozen {total!r}")
                if not _fp_close(scale, n_scale, scale):
                    lines.append(f"{where} reaches {n_scale!r}, frozen {scale!r}")
                for t, want, have in zip(entry["months"], values, n_values):
                    if not _fp_close(want, have, scale):
                        lines.append(f"{where} at t={t} is {have!r}, frozen {want!r}")
    return lines


# ---------------------------------------------------------------------------
# Compiling an SEC model, for the compile tests (Phase 2, D12, D13)
#
# A compile test builds the model with tools/build_sec_cy.py into a temporary directory,
# never into the tree (D12), and runs the compiled package in a child process only: a
# compiled model that overflows the C stack takes down the child and not the session, and
# on Windows a .pyd that a process holds open cannot be deleted.


def _tool():
    """``tools/build_sec_cy.py`` of the repository holding this library, or ``None``.

    A ``lifelib.create()`` copy of the library has no repository above it, and no tool.
    """
    lib = pathlib.Path(__file__).resolve().parents[1]
    if lib.parent.name != "libraries":
        return None
    return lib.parents[2] / "tools" / "build_sec_cy.py"


def cython_missing():
    """What this machine lacks to compile a model, or ``None`` when it lacks nothing.

    The tool, which a ``lifelib.create()`` copy lacks; modelx-cython, which
    ``requirements.txt`` leaves out because it needs a C compiler; and, on POSIX, the C
    compiler setuptools would run, ``CC`` or the one the interpreter was built with, on
    ``PATH``.  On Windows setuptools finds MSVC through vswhere at build time, and
    ``cl.exe`` is on no ``PATH`` outside a developer prompt, so no probe is made there: a
    missing MSVC fails the build instead, and the error quotes setuptools saying so.
    """
    import importlib.util
    import os
    import shlex
    import shutil as _shutil
    import sysconfig
    tool = _tool()
    if tool is None or not tool.is_file():
        return "tools/build_sec_cy.py is absent, as it is from a lifelib.create() copy"
    if importlib.util.find_spec("modelx_cython") is None:
        return "modelx-cython is not installed: pip install -r requirements-cython.txt"
    if os.name == "posix":
        command = os.environ.get("CC") or sysconfig.get_config_var("CC") or "cc"
        compiler = (shlex.split(command) or ["cc"])[0]
        if _shutil.which(compiler) is None:
            return f"no C compiler: setuptools would run {compiler!r}, which is not on PATH"
    return None


def require_cython():
    """``tools/build_sec_cy.py`` as a module, or a skip, which ``USLIB_REQUIRE_CYTHON=1``
    turns into a failure.

    The compile tests skip where :func:`cython_missing` finds something missing, so the
    ``test`` CI job and lifelib's own bare ``pytest`` stay green without modelx-cython or a
    compiler (D13).  The ``cython`` job installs both and sets ``USLIB_REQUIRE_CYTHON=1``,
    and there a skip would be a green run that compiled nothing, so it fails instead.
    ``pytest`` is imported here, not at the top, because ``tools/gen_sec_points.py``
    imports this module without it.
    """
    import importlib.util
    import os
    import pytest
    missing = cython_missing()
    if missing is not None:
        if os.environ.get("USLIB_REQUIRE_CYTHON") == "1":
            pytest.fail(f"USLIB_REQUIRE_CYTHON=1 forbids a skip, and {missing}")
        pytest.skip(missing)
    spec = importlib.util.spec_from_file_location("build_sec_cy", _tool())
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# The cython CI job's shards (D13, decided at M16)
#
# The job runs one shard to a leg, chosen by USLIB_CYTHON_SHARD, so that no leg compiles
# every model: "toolchain", test_cython_toolchain.py and any compile test tied to no one
# SEC model, and one shard for each SEC model at stage "EC", its product module's compile
# tests with its cases of test_compiled_conventions.py, in one session, so that it compiles
# once.  conftest.py deselects the compile tests outside the shard.

CYTHON_SHARD = "USLIB_CYTHON_SHARD"
TOOLCHAIN_SHARD = "toolchain"


def cython_shards():
    """The ``cython`` job's shards, ``{shard: model}``: ``"toolchain"``, to ``None``, first.

    Then, in the registry's order, the product directory of each SEC model at stage
    ``"EC"``, to the model: ``"term_life"`` to ``"Term_US_SEC"``.  The directory names the
    product's test module, ``test_term_life_us_sec.py``, as it does in the ``sec`` job's
    matrix.  Read from the registry, so a model gains its shard in the commit that moves it
    to stage ``"EC"``, and ``test_compiled_conventions.py`` holds the workflow's matrix to
    these.
    """
    from us_registry import is_sec, meta
    shards = {TOOLCHAIN_SHARD: None}
    for name in MODELS:
        if is_sec(name) and meta(name).get("stage") == "EC":
            shards[model_path(name).parent.name] = name
    return shards


def cython_shard(item, shards):
    """The shard among ``shards`` (:func:`cython_shards`) that runs the test ``item``.

    A test parametrized over a stage-``"EC"`` model is that model's, as each case of
    ``test_compiled_conventions.py`` is; else a test in a shard's product module,
    ``test_<shard>_us_sec.py``, is that shard's; and every other is ``"toolchain"``'s.  So
    no compile test falls outside every shard: one tied to no model, or to a model not yet
    at stage ``"EC"``, runs in the toolchain's.
    """
    by_model = {model: shard for shard, model in shards.items() if model is not None}
    params = getattr(item, "callspec", None)
    for value in (params.params.values() if params is not None else ()):
        if isinstance(value, str) and value in by_model:
            return by_model[value]
    found = re.fullmatch(r"test_(\w+)_us_sec\.py", item.path.name)
    if found and found.group(1) in by_model.values():
        return found.group(1)
    return TOOLCHAIN_SHARD


@dataclasses.dataclass(frozen=True)
class Build:
    """One compiled SEC model: its name, the directory it was built in, its compiled
    package, ``<name>_nomx_cy``, and the text of that package's ``_mx_classes.pxd``, the
    declarations a typing guard reads."""
    name: str
    out: pathlib.Path
    package: pathlib.Path
    pxd: str


class SecBuilds:
    """The SEC models compiled in this test session, each once: ``builds(name)``.

    Each is built by ``tools/build_sec_cy.py`` into a directory of the session's own
    (``tmp_path_factory.mktemp``), from the committed model, sample and spec, and kept as
    a :class:`Build` for the rest of the session.  A build that fails is kept too, and its
    error raised again to every test that asks for it, so a broken build reports itself
    in each test that needs it without being compiled again.  Without the toolchain,
    :func:`require_cython` skips, or fails in the ``cython`` job.  ``conftest.sec_build``
    is the session's one instance.
    """

    def __init__(self, tmp_path_factory):
        self._factory = tmp_path_factory
        self._done = {}

    def __call__(self, name):
        if name not in self._done:
            tool = require_cython()
            try:
                out = self._factory.mktemp(name)
                package = tool.build(model_path(name).parent, model=name, out=out)
                pxd = (package / "_mx_classes.pxd").read_text(encoding="utf-8")
                self._done[name] = Build(name, out, package, pxd)
            except Exception as err:            # kept, and raised to every asker
                self._done[name] = err
        built = self._done[name]
        if isinstance(built, Exception):
            raise built
        return built


def compiled_case(build, dest, *, model_points=None, model_point_file=None, edits=None):
    """A directory where modelx and the compiled model read the same inputs; its model.

    :func:`temp_inputs` copies the model and its CSVs into ``dest``, with
    ``model_points`` and ``edits`` as it takes them, and the compiled package of ``build``
    is copied beside them.  The package reads the CSVs of the directory that holds it
    (USLIB-SEC-PLAN.md F6), so it reads the copies, as the model folder returned does.
    ``model_point_file`` defaults to the SEC table's name in the model's spec.
    """
    if model_point_file is None:
        spec = SEC_SPECS.get(build.name)
        model_point_file = (spec.model_point_file if spec is not None
                            else "model_point_table_sec.csv")
    folder = temp_inputs(dest, model_path(build.name), model_points=model_points,
                         model_point_file=model_point_file, edits=edits)
    shutil.copytree(build.package, pathlib.Path(dest) / build.package.name,
                    ignore=shutil.ignore_patterns("__pycache__", "*.c", "*.html"))
    return folder


COMPILED_RUNNER = '''\
"""Run calls on a compiled SEC package in a child process, and pickle what they returned.

    python runner.py <case dir> <package> <job> <result> <stack KiB> <thread | main>
"""
import ctypes
import importlib
import importlib.machinery
import os
import pickle
import sys
import threading

import numpy as np

case, package, job_path, result_path, kib, where = sys.argv[1:7]
sys.path.insert(0, case)
with open(job_path, "rb") as f:
    job = pickle.load(f)
model = importlib.import_module(package).mx_model
for ref, value in job["refs"].items():
    setattr(model.Projection, ref, value)

# Whether each space's class came from an extension module: a package whose build lost one
# still imports, from the translated .py beside it, and computes the same numbers.
suffixes = tuple(importlib.machinery.EXTENSION_SUFFIXES)
compiled = {type(space).__name__: sys.modules[type(space).__module__].__file__.endswith(
    suffixes) for space in (model.Data, model.Projection)}
values, stack = {}, {}


def reservation():
    """The calling thread's stack in bytes, as reserved: from Windows, or from glibc's
    pthread_getattr_np; None elsewhere, as on macOS."""
    if os.name == "nt":
        low, high = ctypes.c_size_t(), ctypes.c_size_t()
        ctypes.windll.kernel32.GetCurrentThreadStackLimits(ctypes.byref(low),
                                                            ctypes.byref(high))
        return high.value - low.value
    try:
        libc = ctypes.CDLL(None)
        libc.pthread_self.restype = ctypes.c_ulong
        attr, size = ctypes.create_string_buffer(256), ctypes.c_size_t()
        if libc.pthread_getattr_np(ctypes.c_ulong(libc.pthread_self()), attr):
            return None
        libc.pthread_attr_getstacksize(attr, ctypes.byref(size))
        libc.pthread_attr_destroy(attr)
        return size.value
    except (AttributeError, OSError):       # no glibc
        return None


def called(call):
    """``("ok", value)`` or ``("raised", "Type: message")``, a memoryview as an array."""
    try:
        value = call()
    except Exception as err:
        return ("raised", f"{type(err).__name__}: {err}")
    if type(value).__name__ == "_memoryviewslice":
        value = np.asarray(value)
    return ("ok", value)


def run():
    stack["reserved"] = reservation()
    for idx, calls in job["calls"].items():
        proj = model.Projection[idx]
        values[idx] = [called(lambda: getattr(proj, name)(*args)) for name, args in calls]
        del proj
        del model.Projection[idx]
    for name in job.get("data", ()):
        data[name] = called(getattr(model.Data, name))


def on_stack(kib):
    """Run :func:`run` in a thread whose stack is ``kib`` KiB, reserved.

    The reservation is what bounds a recursion.  On Windows ``threading.stack_size`` sets
    the stack a thread commits, and the thread reserves the executable's own, 2,000,000
    bytes for python.exe, so the thread is made by CreateThread with
    STACK_SIZE_PARAM_IS_A_RESERVATION instead.
    """
    if os.name != "nt":
        threading.stack_size(kib * 1024)
        thread = threading.Thread(target=run)
        thread.start()
        thread.join()
        return
    from ctypes import wintypes
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    start = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID)
    kernel32.CreateThread.argtypes = (wintypes.LPVOID, ctypes.c_size_t, start,
                                      wintypes.LPVOID, wintypes.DWORD, wintypes.LPDWORD)
    kernel32.CreateThread.restype = wintypes.HANDLE
    kernel32.WaitForSingleObject.argtypes = (wintypes.HANDLE, wintypes.DWORD)
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    failed = []

    def body(_):
        try:
            run()
        except BaseException as err:
            failed.append(err)
        return 0

    entry = start(body)
    handle = kernel32.CreateThread(None, kib * 1024, entry, None, 0x00010000, None)
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    kernel32.WaitForSingleObject(handle, 0xFFFFFFFF)
    kernel32.CloseHandle(handle)
    if failed:
        raise failed[0]


data = {}
if where == "main":
    run()
else:
    on_stack(int(kib))
with open(result_path, "wb") as f:
    pickle.dump({"compiled": compiled, "values": values, "data": data, "stack": stack}, f)
'''
"""The child that :func:`run_compiled` starts: it imports the compiled package, sets the
References, and makes the calls, in a thread of the stack asked for or on its main
thread."""


def run_compiled(case_dir, package, job, *, stack_kib=1024, main_thread=False,
                 timeout=600):
    """Run ``job`` on the compiled ``package`` in ``case_dir``, in a child; what it found.

    ``job`` is ``{"refs": {name: value}, "calls": {idx: [(cell, args), ...]}}``, and may
    name ``"data"``, a list of ``Data`` cells to read once the calls are made.  The child
    sets each Reference on the base ``Projection`` before any ItemSpace is made, then makes
    each point's calls in order, on ``Projection[idx]``, in a thread whose stack is
    ``stack_kib`` KiB or, with ``main_thread``, on its main thread, which is what
    ``run_sec.py --cython`` runs on.  A compiled chain of cells runs on the C stack, which
    the interpreter's recursion limit does not count (F7).  The thread's stack is
    reserved at that size on every platform: ``threading.stack_size`` sets it on POSIX,
    and on Windows, where that sets only the stack a thread commits, the child makes the
    thread itself (``COMPILED_RUNNER``).

    Returns ``{"exit": code, "stderr": its last lines}``, and when the child exited 0:
    ``"compiled"``, whether each space's class came from an extension module; ``"values"``,
    ``{idx: [("ok", value) or ("raised", "Type: message"), ...]}`` in the calls' order,
    an array returned as a numpy array; ``"data"``, ``{cell: ("ok", value) or ("raised",
    ...)}`` for the ``Data`` cells named; and ``"stack"``, ``{"reserved": bytes}``, the
    stack the thread that made the calls has, read back from Windows or glibc, ``None``
    where neither tells.  A child that dies on its stack has a nonzero exit and no values.
    """
    import os
    import pickle
    import subprocess
    import sys
    import tempfile
    case_dir = pathlib.Path(case_dir)
    work = pathlib.Path(tempfile.mkdtemp(prefix="run_", dir=case_dir.parent))
    runner, job_path, result = work / "runner.py", work / "job.pickle", work / "got.pickle"
    runner.write_text(COMPILED_RUNNER, encoding="utf-8")
    job_path.write_bytes(pickle.dumps(job))
    done = subprocess.run(
        [sys.executable, "-P", str(runner), str(case_dir), package, str(job_path),
         str(result), str(stack_kib), "main" if main_thread else "thread"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}, timeout=timeout)
    found = {"exit": done.returncode, "stderr": done.stderr[-4000:]}
    if done.returncode == 0:
        found.update(pickle.loads(result.read_bytes()))
    return found


# ---------------------------------------------------------------------------
# What may stay Python (R17)


def reporting_cells(name, space):
    """The cells of SEC model ``name``'s ``Projection`` that may stay Python (R17).

    ``model_point``, every ``result_*`` report, every ``check_*`` check but the per-``t``
    ``*_resid`` cells a check reads, and the label accessors the registry entry names
    under ``"reporting"`` (:mod:`us_registry`): cells that hand a reader a table row, text,
    a DataFrame or a verdict.  And the engine cells it names under ``"engine"``: S's cells
    of float parameters, or of no parameter returning a list, a dict or a DataFrame (M24),
    kept for a reader and for T1, which no compiled cell calls (R14).
    They are the typing guard's allowlist (:func:`typing_faults`), and no other cell may
    call one (:func:`static_faults`), so every cell a projection runs compiles to C; an
    engine cell may call another.  ``space`` is the model's ``Projection``.
    """
    from us_registry import meta
    declared = set(meta(name).get("reporting", ())) | set(meta(name).get("engine", ()))
    return frozenset(
        cell for cell in space.cells
        if cell == "model_point" or cell.startswith("result_") or cell in declared
        or (cell.startswith("check_") and not cell.endswith("_resid")))


def engine_faults(space, declared, sized, reporting=()):
    """Where the cells an entry's ``"engine"`` names are not what R14 admits, a line each.

    Each must be a cell of ``space``, the model's ``Projection``, and none a reporting
    cell, ``reporting`` being the entry's ``"reporting"``.  Each must take a parameter
    that no ``spec_sec.py`` size names, ``sized`` holding the names it sizes, since a cell
    keyed by sized ints compiles to C and needs no admission; or take none and return
    what no C type holds, a list, a dict or a DataFrame, found by calling it on the
    space's first point, as ``DIA_US_SEC``'s ``qlac_flags`` and premium schedule do (M24).
    And no other formula of ``space`` may call one, an engine cell excepted, so that every
    cell a projection runs is C.
    """
    import ast
    import textwrap
    point = space[0] if space.parameters else space
    found = []
    for cell in declared:
        if cell not in space.cells:
            found.append(f"{cell} is not a Projection cell")
        elif cell in reporting:
            found.append(f"{cell} is a reporting cell too")
        elif not set(space.cells[cell].parameters) - sized:
            if not space.cells[cell].parameters and isinstance(
                    point.cells[cell](), (list, dict, pd.DataFrame)):
                continue
            found.append(f"{cell} takes only parameters spec_sec.py sizes, "
                         f"{space.cells[cell].parameters}, so it compiles to C")
    for name, cells in space.cells.items():
        if name in declared:
            continue
        tree = ast.parse(textwrap.dedent(cells.formula.source))
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id in declared):
                found.append(f"{name} calls the engine cell {node.func.id}")
    return found


def _names_bound(node, tree):
    """The text constants a sample's loop variable ``node`` can take, or ``None``.

    ``node`` is the name a ``getattr`` call reads its attribute from, as in ``for label in
    LABELS: getattr(p, label)()``.  It is resolved through the ``for`` loop that binds it:
    over a literal tuple, list or set of text, or a module-level name assigned one; or,
    where the loop binds it first of a pair, over ``.items()`` of a dict literal, or of a
    module-level name assigned one, its keys.  Any other loop, one over names the sample
    computes, is not resolved.
    """
    import ast
    assigned = {}
    for statement in tree.body:
        if isinstance(statement, ast.Assign):
            for target in statement.targets:
                if isinstance(target, ast.Name):
                    assigned[target.id] = statement.value

    def texts(value):
        if isinstance(value, ast.Name):
            value = assigned.get(value.id)
        if isinstance(value, (ast.Tuple, ast.List, ast.Set)):
            found = [e.value for e in value.elts
                     if isinstance(e, ast.Constant) and isinstance(e.value, str)]
            return set(found) if len(found) == len(value.elts) else None
        return None

    def keys(value):
        if isinstance(value, ast.Name):
            value = assigned.get(value.id)
        if isinstance(value, ast.Dict):
            found = [k.value for k in value.keys
                     if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            return set(found) if len(found) == len(value.keys) else None
        return None

    for loop in ast.walk(tree):
        if not isinstance(loop, ast.For):
            continue
        if isinstance(loop.target, ast.Name) and loop.target.id == node.id:
            if any(child is node for child in ast.walk(loop)):
                return texts(loop.iter)
        if (isinstance(loop.target, ast.Tuple) and loop.target.elts
                and isinstance(loop.target.elts[0], ast.Name)
                and loop.target.elts[0].id == node.id
                and any(child is node for child in ast.walk(loop))):
            it = loop.iter
            if (isinstance(it, ast.Call) and isinstance(it.func, ast.Attribute)
                    and it.func.attr == "items" and not it.args):
                return keys(it.func.value)
            return None
    return None


def sample_engine_faults(source, engine, parameterless=()):
    """Where a ``sample_sec.py`` calls an ``"engine"`` cell of the registry's nowhere.

    No compiled cell calls an engine cell (:func:`engine_faults`), so the sample's own
    call is the only trace mx2cy types it from: one the sample stops calling compiles with
    object parameters, and C3 still passes, since it admits an engine cell's dict cache by
    name (R14, M25).  So each cell of ``engine`` must be called in ``source``, the
    sample's code, read statically: as an attribute, ``p.bs_call(...)``, through
    ``getattr`` with its name as text, or through ``getattr`` with a loop variable that
    :func:`_names_bound` resolves to a set of names holding it.  A cell of
    ``parameterless``, the engine cells taking no parameter, is called too by a loop that
    calls ``getattr(p, name)()`` over names the sample computes, as a sample that calls
    every cell of no parameter does: such a cell returns a list, a dict or a DataFrame,
    an object traced or not.  Returns a line per cell not called.
    """
    import ast
    tree = ast.parse(source)
    parents = {child: node for node in ast.walk(tree)
               for child in ast.iter_child_nodes(node)}
    called, computed = set(), False
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Attribute):
            called.add(node.func.attr)
        if not (isinstance(node.func, ast.Name) and node.func.id == "getattr"
                and len(node.args) >= 2):
            continue
        name = node.args[1]
        if isinstance(name, ast.Constant) and isinstance(name.value, str):
            called.add(name.value)
        elif isinstance(name, ast.Name):
            bound = _names_bound(name, tree)
            if bound is not None:
                called |= bound
            else:
                up = parents.get(node)
                if (isinstance(up, ast.Call) and up.func is node and not up.args
                        and not up.keywords):
                    computed = True
    return [f"sample_sec.py calls no engine cell {cell}(): untraced, it compiles taking "
            f"objects, which C3 admits in an engine cell (R14)"
            for cell in engine
            if cell not in called and not (computed and cell in parameterless)]


def reporting_columns_faults(entry):
    """Where a registry entry's ``"reporting_columns"`` is not what R17 lets it say (M23).

    The key says what a label accessor returns where that is not its point's column of
    the label's own name (:mod:`us_registry`).  It is a stage-``"EC"`` key, as
    ``"reporting"`` is, a dict whose every key is a label ``"reporting"`` names, each
    mapped to one of three shapes: a column name; a non-empty dict of argument to column
    name, for a label taking one argument; or a pair of a column name and a non-empty
    dict of value to label, for a label returning the column's value through the dict.
    ``entry`` is a :func:`us_registry.meta` dict.  Returns a line per fault.
    """
    if "reporting_columns" not in entry:
        return []
    columns = entry["reporting_columns"]
    if entry.get("stage") != "EC":
        return [f"reporting_columns is declared at stage {entry.get('stage')!r}; it widens "
                f"the compiled model's label check, and the key belongs to stage 'EC'"]
    if not (isinstance(columns, dict) and columns):
        return [f"reporting_columns is {columns!r}, not a non-empty dict of labels"]
    lines = []
    reporting = entry.get("reporting", ())
    for label, shape in columns.items():
        if label not in reporting:
            lines.append(f"reporting_columns names {label!r}, which reporting does not")
        if isinstance(shape, str):
            continue
        if isinstance(shape, dict):
            if not (shape and all(isinstance(c, str) for c in shape.values())):
                lines.append(f"reporting_columns[{label!r}] is {shape!r}, not a non-empty "
                             f"dict of argument to column")
            continue
        if (isinstance(shape, tuple) and len(shape) == 2 and isinstance(shape[0], str)
                and isinstance(shape[1], dict) and shape[1]):
            continue
        lines.append(f"reporting_columns[{label!r}] is {shape!r}: neither a column, a dict "
                     f"of argument to column, nor a pair of a column and a dict of value "
                     f"to label")
    return lines


def _label_calls(shape):
    """``[(args, column, mapping)]``: how :func:`label_faults` calls a label of ``shape``,
    its ``"reporting_columns"`` entry or its own name."""
    if isinstance(shape, dict):
        return [((arg,), column, None) for arg, column in shape.items()]
    if isinstance(shape, tuple):
        return [((), shape[0], shape[1])]
    return [((), shape, None)]


def label_faults(model, name, entry=None):
    """C5's check of the label accessors: each returns its point's column (R17), a line
    per fault.

    For each label SEC model ``name``'s registry entry names under ``"reporting"`` and
    ``model``'s ``Projection`` holds, on every point of the table: called as the entry's
    ``"reporting_columns"`` says (:func:`reporting_columns_faults`), or bare where it says
    nothing, the label must return its point's column as the table holds it, through the
    pair's dict where the shape is a pair, a value the dict lacks as it is.  Text must
    equal the column's text; a blank column, NaN, is the label's value where the label
    returns NaN, as ``SPIA_US_SEC``'s ``sex(2)`` does on a single-life point; anything else,
    a raise among them, is a fault, as is a column the table lacks.  And an entry must be
    needed: a label the entry names as a column or a pair, whose own name is also a
    column, must not return that column, its default, on every point, which would leave
    the entry stale.  ``entry`` stands in for the registry's, as a harness test's does.
    """
    from us_registry import meta, point_keys, projection
    entry = meta(name) if entry is None else entry
    columns = entry.get("reporting_columns", {})
    labels = [cell for cell in entry.get("reporting", ()) if cell in model.Projection.cells]
    found, own, points = [], {cell: 0 for cell in columns}, 0
    table = model.Data.model_point_table()
    for key, point_id in zip(point_keys(model), table.index):
        points += 1
        proj = projection(model, key)
        row = proj.model_point()
        for cell in labels:
            for args, column, mapping in _label_calls(columns.get(cell, cell)):
                call = f"Projection.{cell}({', '.join(repr(a) for a in args)})"
                try:
                    got = proj.cells[cell](*args)
                except Exception as err:            # reported, so the scan goes on
                    found.append(f"{call} raised {_error_text(err)} at point {point_id}, "
                                 f"where the label returns the point's {column!r} column "
                                 f"(R17)")
                    continue
                if column not in row.index:
                    found.append(f"{call}: the table has no {column!r} column, which the "
                                 f"registry says it returns (R17)")
                    continue
                want = row[column]
                if mapping is not None and isinstance(want, str):
                    want = mapping.get(want, want)
                blank = (isinstance(want, float) and want != want
                         and isinstance(got, float) and got != got)
                if not ((isinstance(got, str) and got == want) or blank):
                    found.append(f"{call} returns {got!r} at point {point_id}, where the "
                                 f"label returns the point's {column!r} column, {want!r} "
                                 f"(R17)")
            if (cell in own and not isinstance(columns[cell], dict) and cell in row.index
                    and isinstance(row[cell], str)):
                try:
                    if proj.cells[cell]() == row[cell]:
                        own[cell] += 1
                except Exception:                   # a fault above already
                    pass
    for cell, n in own.items():
        if points and n == points:
            found.append(f"reporting_columns[{cell!r}] is stale: {cell}() returns its own "
                         f"{cell!r} column on every point, its default without the entry")
    return found


# ---------------------------------------------------------------------------
# C3 -- the typing guard, read from what the compiler generated


C_SCALARS = frozenset({"bint", "long long", "double"})
"""The C types a compiled cell returns and takes: a flag, an integer, a real (F3)."""

_MEMORYVIEW = re.compile(r"const (?:double|long long)\[:(?:, :)*\]")
_PXD_CLASS = re.compile(r"^cdef class _c_(\w+)\(", re.M)
_PXD_CPDEF = re.compile(r"\s+cpdef (.+?) (\w+)\(_c_\w+ self((?:, [^)]*)?)\)\s*")
_PXD_CACHE = re.compile(r"\s+cdef (.+?)((?:\[\d+\])*) _v_(\w+)\s*")


def pxd_declarations(pxd, space):
    """What a generated ``_mx_classes.pxd`` declares for the cells of one space.

    Returns ``(cells, caches)``: ``{cell: (return type, ((type, parameter), ...))}`` for
    each cell compiled to a ``cpdef`` method, and ``{cell: (type, sizes)}`` for each cell's
    cache, ``sizes`` being the dimensions of its C array, ``()`` for a single value.  A
    cell missing from ``cells`` stayed a Python method.  ``space`` is the space's name,
    ``"Projection"``; a space the file does not declare has neither.
    """
    blocks = _PXD_CLASS.split(pxd)
    body = dict(zip(blocks[1::2], blocks[2::2])).get(space, "")
    cells, caches = {}, {}
    for line in body.splitlines():
        found = _PXD_CPDEF.fullmatch(line)
        if found and not found.group(2).startswith("_mx"):
            params = tuple(tuple(part.strip().rsplit(" ", 1))
                           for part in found.group(3).split(",") if part.strip())
            cells[found.group(2)] = (found.group(1), params)
            continue
        found = _PXD_CACHE.fullmatch(line)
        if found:
            sizes = tuple(int(n) for n in re.findall(r"\[(\d+)\]", found.group(2)))
            caches[found.group(3)] = (found.group(1), sizes)
    return cells, caches


def data_readers(model):
    """The ``Data`` cells of ``model`` that read an input file: its readers (R5).

    A reader is a cell whose formula names a ``Data`` Reference ending ``_file`` outside
    its ``raise`` statements, as ``model_point_table()`` names ``model_point_file``.  R5
    keeps the S model's readers as they are, Python objects returning DataFrames, and a
    reader of an SEC-only companion file is one too (D8): IUL's in-force ladder, DIA's
    premium schedule.  A cell that only quotes a file's name in a refusal is not one.
    """
    import ast
    files = {ref for ref in model.Data.refs if ref.endswith("_file")}
    found = set()
    for name, cells in model.Data.cells.items():
        tree, _, _, exempt = _syntax(cells)
        if any(isinstance(node, ast.Name) and node.id in files and node not in exempt
               for node in ast.walk(tree)):
            found.add(name)
    return frozenset(found)


def typing_faults(build, model, *, reporting, new_data):
    """C3: what the compiled model holds as Python objects, from its declarations.

    Every ``Projection`` cell of ``model`` outside ``reporting`` (:func:`reporting_cells`)
    must compile to a method returning one of :data:`C_SCALARS` and taking only them, and
    none of their caches may be a Python dict.  Every ``Data`` cell of ``new_data``, the
    ones the S twin lacks, must return a typed memoryview of int64 or float64, or a C
    scalar (R5), but for the readers among them (:func:`data_readers`), which stay
    Python, as the S model's own do.  ``model`` is the modelx model ``build`` was
    compiled from.  Returns a line per fault, empty when the declarations are all C.
    """
    lines = []
    cells, caches = pxd_declarations(build.pxd, "Projection")
    for name in sorted(set(model.Projection.cells) - set(reporting)):
        if name not in cells:
            lines.append(f"Projection.{name} did not compile: it stays a Python method, as "
                         f"one does whose name a call with keywords uses, and an uncached "
                         f"one whose formula holds a generator, a lambda or a nested def "
                         f"(F3)")
            continue
        returns, params = cells[name]
        if returns not in C_SCALARS:
            lines.append(f"Projection.{name} returns {returns}, not a C scalar: a cell "
                         f"mx2cy has no trace of, one the sample never calls or an "
                         f"uncached one, whose formula modelx-cython 0.1.0 never traces "
                         f"(R14), or one returning what mx2cy cannot type, a numpy bool, "
                         f"text, a tuple or a DataFrame (F3)")
        for kind, param in params:
            if kind not in C_SCALARS:
                lines.append(f"Projection.{name} takes {param} as {kind}: a timing or a "
                             f"kind passed as text, not as an int code (R9), or a cell "
                             f"mx2cy has no trace of, as above")
        if caches.get(name, ("",))[0] == "dict":
            lines.append(f"Projection.{name} caches its values in a Python dict")
    data_cells, _ = pxd_declarations(build.pxd, "Data")
    for name in sorted(set(new_data) - data_readers(model)):
        if name not in data_cells:
            lines.append(f"Data.{name} did not compile: it stays a Python method")
            continue
        returns = data_cells[name][0]
        if returns not in C_SCALARS and not _MEMORYVIEW.fullmatch(returns):
            lines.append(f"Data.{name} returns {returns}, not a typed memoryview or a C "
                         f"scalar: an array of bools, objects or text, or one a cell uses "
                         f"whole (R5, R13)")
    return lines


def object_cells(name, space):
    """The cells of SEC model ``name``'s ``Projection`` that must compile to ``object``.

    ``model_point``, every ``result_*`` report and the label accessors the registry entry
    names under ``"reporting"``: the reporting cells that hand a reader a table row, a
    DataFrame or a point's column as read, which ``Data`` may hold as text, a number or a
    blank.  The other reporting cells of :func:`reporting_cells` are typed: a ``check_*``
    returns a ``bint``, and an ``"engine"`` cell a C scalar.  ``space`` is the model's
    ``Projection``.
    """
    from us_registry import meta
    labels = set(meta(name).get("reporting", ()))
    return frozenset(cell for cell in space.cells
                     if cell == "model_point" or cell.startswith("result_")
                     or cell in labels)


def object_return_faults(build, cells, refusing=frozenset()):
    """C3 of the reporting cells: each of ``cells`` that compiled returns ``object``.

    A label accessor returns its point's column as read, and ``Data`` accepts a label that
    is not text, a blank or a number.  mx2cy types a cell from what the sample's calls
    return, so an accessor the sample traces on text alone compiles to ``str``, and the
    compiled model raises ``TypeError`` where modelx returns the value.  The sample
    therefore calls each on a point whose label is not text too, and this holds what it
    makes of that: every cell of ``cells`` (:func:`object_cells`) that ``build``'s
    ``_mx_classes.pxd`` declares returns ``object``, but a label of ``refusing``, which
    modelx refuses wherever its column is not text (:func:`labels_refusing_non_text`), as
    a label validating its column does: it returns text or raises, in either engine.  One
    left a Python method is not declared, and returns what modelx does.  Returns a line
    per fault.
    """
    declared, _ = pxd_declarations(build.pxd, "Projection")
    return [f"Projection.{name} returns {declared[name][0]}, where a reporting cell "
            f"returns object: a label the sample traced on text alone, which raises "
            f"TypeError compiled on a label Data holds as a number or a blank, where "
            f"modelx returns it (R17)"
            for name in sorted(cells)
            if name in declared and declared[name][0] != "object" and name not in refusing]


def labels_refusing_non_text(name, labels):
    """The labels of ``labels`` that SEC model ``name`` refuses, in their own formula,
    wherever they are not text.

    Each label is called, in modelx, on the committed model whose table,
    ``Data.model_point_table()``, is replaced by an input value holding the first point's
    column blank, and then the number 7, past every check ``Data``'s reader makes; called
    as the registry's ``"reporting_columns"`` says (:func:`label_faults`), at each
    argument.  A label is refusing where every such call raises, as a label validating
    its column does.  A refusal of ``Data``'s is not the label's, and is not sought: a
    key label returns a number where its tables are keyed by numbers.  A refusing label
    returns text or raises, so it may compile to ``str`` (:func:`object_return_faults`).
    """
    from us_registry import meta, point_keys, projection
    columns = meta(name).get("reporting_columns", {})
    refusing = set()
    for label in sorted(labels):
        refused = True
        for args, column, _ in _label_calls(columns.get(label, label)):
            for value in (None, 7):
                if not refused:
                    break
                model = mx.read_model(model_path(name),
                                      name=f"{name}_text_{next(_c4_names)}")
                try:
                    table = model.Data.model_point_table().astype({column: object})
                    table.iloc[0, table.columns.get_loc(column)] = value
                    model.Data.model_point_table[()] = table
                    proj = projection(model, point_keys(model)[0])
                    try:
                        proj.cells[label](*args)
                        refused = False
                    except Exception:       # the label's own refusal, which is sought
                        pass
                finally:
                    model.close()
        if refused:
            refusing.add(label)
    return frozenset(refusing)


def spec_faults(build, spec_path):
    """C3's check of the spec: each C-array cache is the size ``spec_path`` gives (F4).

    mx2cy sizes the cache of every cell with integer parameters from the spec's
    ``cells_param_size``, keyed by the parameters' names, and it ignores without a word a
    key that no cell takes, a misspelt one, sizing those caches from the sample's largest
    argument instead, which the committed points fit.  So the spec is read here as mx2cy
    reads it, with ``ast.literal_eval``, and every compiled ``Projection`` cell taking
    only C integers must have a size for its parameters and a cache of exactly that size,
    and every size must be taken by some cell.  A sample argument beyond the size, which
    enlarges the cache, is reported too.  Returns a line per fault.
    """
    import ast
    spec = ast.literal_eval(pathlib.Path(spec_path).read_text(encoding="utf-8"))
    given = spec.get("spaces", {}).get("Projection", {}).get("cells_param_size", {})
    sizes = {(key if isinstance(key, tuple) else (key,)):
             (tuple(size) if isinstance(size, (tuple, list)) else (size,))
             for key, size in given.items()}
    cells, caches = pxd_declarations(build.pxd, "Projection")
    lines, taken, spec_name = [], set(), pathlib.Path(spec_path).name
    for name, (_, params) in sorted(cells.items()):
        if not params or any(kind != "long long" for kind, _ in params):
            continue
        key = tuple(param for _, param in params)
        kind, cache = caches.get(name, ("", ()))
        if key in sizes:
            taken.add(key)
        if kind == "dict":
            continue                        # typing_faults reports a dict cache
        if key not in sizes:
            lines.append(f"Projection.{name}: {spec_name} gives no size for {key}, so the "
                         f"sample sized its cache, {cache}")
        elif cache != sizes[key]:
            lines.append(f"Projection.{name}: a cache of {cache}, where {spec_name} gives "
                         f"{sizes[key]}")
    for key in sorted(set(sizes) - taken):
        lines.append(f"{spec_name} sizes {key}, which no compiled cell takes: mx2cy "
                     f"ignores the size, as it ignores a misspelt name")
    return lines


# The C function Cython writes for one Projection formula, and its body: the definition at
# the start of a line, up to the closing brace that ends its own line.
_C_FORMULA = re.compile(
    r"^static [^\n;{]*?__pyx_f_\w+?_c_Projection__f_(\w+)\([^)]*\) \{\n(.*?)\n\}\n",
    re.S | re.M)

REQUIRED_DIRECTIVES = {"infer_types": "True", "cpow": "True"}
"""The directives ``tools/build_sec_cy.py`` puts at the top of each translated space module,
which C3 requires: without ``infer_types`` an integer local stays a Python object, and
without ``cpow`` a power is complex, and drifts from modelx in its last bits (M14)."""

# What a formula's C does that is Python's work: a builtin it looks up and calls, other
# than an exception a refusal raises, and a list, dict or set it builds.
_C_BUILTIN = re.compile(r"__pyx_builtin_(\w+)")
_C_CONTAINER = re.compile(r"\b(PyList_New|PyDict_New|__Pyx_PyDict_NewPresized|PySet_New)\b")


def _directives(line):
    """The directives of a ``# cython: a=b, c=d`` line, ``{name: value}``, or ``None``."""
    head, _, body = line.partition(":")
    if head.replace(" ", "") != "#cython":
        return None
    pairs = [part.split("=", 1) for part in body.split(",") if part.strip()]
    return {k.strip(): v.strip() for k, v in (p for p in pairs if len(p) == 2)}


def c_faults(build, *, reporting, python_calls=None):
    """C3 on the generated C: the Python a compiled formula still runs.

    A cell typed ``double`` can compute in Python all the same, and its declaration does
    not show it.  So the C of every ``Projection`` formula outside ``reporting`` must
    declare no ``PyObject`` local, which turns every operation on it into a call into the
    interpreter; call no Python builtin, such as ``round`` or ``sum``, but the exceptions a
    refusal raises and those ``python_calls``, the registry's ``"python_calls"``
    (:mod:`us_registry`), admits in that cell, ``{cell: (builtin, ...)}``; and build no
    list, dict or set.  Under Cython's default inference an
    integer local used in arithmetic, and any loop counter, is a Python object, and a
    power of two doubles is complex, so every translated space module must begin with the
    directives of :data:`REQUIRED_DIRECTIVES`, which ``tools/build_sec_cy.py`` writes.
    An uncached cell has no ``_f_`` formula, its public method being its formula, so its
    body is not read here; mx2cy types no such cell, and :func:`typing_faults` and
    :func:`static_faults` refuse it.  Returns a line per fault.
    """
    lines, python_calls = [], python_calls or {}
    for module in sorted(build.package.rglob("_mx_classes.py")):
        first = module.read_text(encoding="utf-8").split("\n", 1)[0]
        given = _directives(first) or {}
        missing = [f"{k}={v}" for k, v in REQUIRED_DIRECTIVES.items() if given.get(k) != v]
        if missing:
            lines.append(f"{module.name} begins {first!r}, without {', '.join(missing)}: "
                         f"tools/build_sec_cy.py puts them on its first line")
    source = build.package / "_mx_classes.c"
    if not source.is_file():
        return lines + [f"no generated C at {source}"]
    found = 0
    for match in _C_FORMULA.finditer(source.read_text(encoding="utf-8", errors="replace")):
        found += 1
        name, body = match.group(1), match.group(2)
        if name in reporting:
            continue
        objects = sorted(set(re.findall(r"PyObject \*__pyx_v_(\w+)", body)))
        if objects:
            lines.append(f"Projection.{name} keeps Python objects in its C locals: "
                         f"{', '.join(objects)}")
        builtins = sorted({b for b in _C_BUILTIN.findall(body)
                           if not b.endswith(("Error", "Exception", "Warning"))}
                          - set(python_calls.get(name, ())))
        if builtins:
            lines.append(f"Projection.{name} calls the Python builtin "
                         f"{', '.join(builtins)} (R12, R16)")
        built = sorted({kind for kind in _C_CONTAINER.findall(body)})
        if built:
            lines.append(f"Projection.{name} builds a Python list, dict or set "
                         f"({', '.join(built)}) (R10, R12)")
    if not found:
        lines.append(f"no Projection formula in {source.name}: its layout has changed "
                     f"under this check")
    return lines


# ---------------------------------------------------------------------------
# C4 -- the compiled model against modelx, cell by cell


COMPILED_RTOL = 1e-12
"""C4's tolerance where it is not exact: relative, floored at the same fraction of the
cell's magnitude (:func:`exact_here`)."""


def exact_here():
    """Whether C4 holds the compiled model to modelx bit for bit on this machine.

    On x86-64 it does.  ``tools/build_sec_cy.py`` compiles with ``-ffp-contract=off``
    there, after any ``-march`` the interpreter's flags or ``CFLAGS`` give, so that gcc and
    clang fuse no multiply and add into one rounding, which they do by default wherever
    the target has fused multiply-add; MSVC, on Windows, emits none for x64 without
    ``/arch:AVX2``, which setuptools does not pass.  And with ``cpow=True`` the compiled
    power is the C ``pow`` that Python's float power calls.  So a compiled cell does
    modelx's arithmetic in modelx's order, and every value Term's tables reach is
    identical (M14).  Elsewhere, on arm64 among others, no run has shown it yet, and C4
    compares to :data:`COMPILED_RTOL` instead.
    """
    import platform
    return platform.machine().lower() in ("x86_64", "amd64")

_c4_names = itertools.count(1)


def full_sweep(proj):
    """Evaluate on one point every value C4 compares, and return what raised.

    Every cell without parameters, the reports among them, and then, for ``t = 0 ..
    proj_len()`` in ascending order, every cell whose one parameter is ``t``: the frame,
    and the month after it, which the count's roll-forward reads.  What those reach is
    evaluated with them: a cell keyed by a timing, a policy year or a duration, at every
    argument the frame asks of it.  A call that raises is recorded, ``{(cell, args):
    "Type: message"}``, and the sweep goes on, unless it is ``proj_len()`` itself.
    """
    raised = {}

    def call(name, args):
        try:
            proj.cells[name](*args)
        except Exception as err:            # recorded, for a raise to meet a raise
            raised[(name, args)] = _error_text(err)

    for name, cells in proj.cells.items():
        if not cells.parameters:
            call(name, ())
    if "proj_len" not in proj.cells or ("proj_len", ()) in raised:
        return raised
    monthly = [name for name, cells in proj.cells.items()
               if tuple(cells.parameters) == ("t",)]
    for t in range(proj.proj_len() + 1):
        for name in monthly:
            call(name, (t,))
    return raised


def _cached_values(proj):
    """``{(cell, args): value}`` for every value ``proj`` has cached, in cache order."""
    found = {}
    for name, cells in proj.cells.items():
        n_params = len(cells.parameters)
        for key in list(cells.keys()):
            args = _args(key, n_params)
            found[(name, args)] = cells(*args)
    return found


# The kinds of value most cells return, which C4 compares at once when they are identical.
_PLAIN = (float, int, bool, str)


def _kind(x):
    """C4's kind of a value: a bool, an int and a real stay apart, numpy's or Python's."""
    kind = type(x)
    if kind is float:
        return "float"
    if kind is bool or isinstance(x, np.bool_):
        return "bool"
    if isinstance(x, numbers.Integral):
        return "int"
    if isinstance(x, numbers.Real):
        return "float"
    return kind.__name__


def _scaled_close(a, b, scale, rtol=COMPILED_RTOL):
    """Within ``rtol`` of the larger of the two, or of ``scale``; at 0, identical."""
    if a == b or (a != a and b != b):
        return True
    if not (math.isfinite(a) and math.isfinite(b)):
        return False
    return abs(a - b) <= rtol * max(abs(a), abs(b), scale)


def _magnitude(values):
    """The largest finite absolute value among the numbers of ``values``; 0.0 if none."""
    found = [abs(float(v)) for v in values if _kind(v) in ("int", "float")]
    return max((v for v in found if math.isfinite(v)), default=0.0)


def _series_text(want, have, rtol=COMPILED_RTOL):
    """How two Series on the same labels differ, value by value, or ``None``."""
    a, b = want.tolist(), have.tolist()
    scale = _magnitude(a)
    bad = [i for i, (x, y) in enumerate(zip(a, b)) if _value_text(x, y, scale, rtol)]
    if not bad:
        return None
    first = bad[0]
    return (f"{len(bad)} of {len(a)} differ, first at {_py(want.index[first])!r}: "
            f"{_value_text(a[first], b[first], scale, rtol)}")


def _value_text(want, have, scale, rtol=COMPILED_RTOL):
    """Why ``have``, a compiled value, is not ``want``, modelx's; ``None`` when it is.

    A bool, an int and a real must stay what they are, and ints compare exactly; reals
    compare within ``rtol``, floored at ``scale``, the cell's magnitude, and at ``rtol``
    0 must be identical, NaN meeting NaN.  A DataFrame compares column by column on the
    same labels, a Series value by value, each against its own magnitude, an array
    exactly, and anything else by equality.
    """
    kind = _kind(want)
    if kind != _kind(have):
        return f"modelx {_typed(want)}, compiled {_typed(have)}"
    if kind in ("bool", "int", "float"):
        same = (_scaled_close(float(want), float(have), scale, rtol) if kind == "float"
                else want == have)
        return None if same else f"modelx {_py(want)!r}, compiled {_py(have)!r}"
    if isinstance(want, pd.DataFrame):
        if list(want.columns) != list(have.columns) or not want.index.equals(have.index):
            return (f"modelx's frame has columns {list(want.columns)} and {len(want)} "
                    f"rows, the compiled one {list(have.columns)} and {len(have)}")
        parts = [f"column {column!r}: {text}" for column in want.columns
                 if (text := _series_text(want[column], have[column], rtol))]
        return "; ".join(parts) or None
    if isinstance(want, pd.Series):
        if not want.index.equals(have.index):
            return "the two Series have different labels"
        return _series_text(want, have, rtol)
    if isinstance(want, np.ndarray):
        same = (want.shape == have.shape and want.dtype == have.dtype
                and np.array_equal(want, have, equal_nan=want.dtype.kind == "f"))
        return None if same else f"modelx {want!r}, compiled {have!r}"
    return None if want == have else f"modelx {want!r}, compiled {have!r}"


def _outcome_text(want, have, scale, rtol=COMPILED_RTOL):
    """Why the compiled outcome is not modelx's, each ``("ok", value)`` or ``("raised",
    "Type: message")``; ``None`` when they agree.  A raise must meet the same raise."""
    if have is None:
        return "the compiled run returned nothing for it"
    if want[0] == have[0] == "ok":
        return _value_text(want[1], have[1], scale, rtol)
    if want[0] == have[0] == "raised" and want[1] == have[1]:
        return None
    show = {"ok": lambda v: f"returned {_typed(v)}" if _kind(v) in ("bool", "int", "float")
            else f"returned a {type(v).__name__}", "raised": lambda v: f"raised {v}"}
    return f"modelx {show[want[0]](want[1])}, compiled {show[have[0]](have[1])}"


def c4_expected(proj, also=None):
    """What C4 expects of one modelx point: ``{(cell, args): ("ok", value) | ("raised",
    "Type: message")}``.

    :func:`full_sweep` first, then, unless the point's ``proj_len()`` raised, ``also(proj)``
    where it is given, a product's calls of the cells and codes no swept cell reaches, the
    pricing path's closes or a timing no formula passes; then every value the point has
    cached, at every argument, and every raise the sweep recorded.  So what ``also`` calls
    enters the expectation, and the compiled run, which repeats every expected call, makes
    it too.  ``also`` must not raise: it calls only what the point computes.
    """
    raised = full_sweep(proj)
    if also is not None and ("proj_len", ()) not in raised:
        also(proj)
    found = {call: ("ok", value) for call, value in _cached_values(proj).items()}
    found.update((call, ("raised", text)) for call, text in raised.items())
    return found


def compiled_mismatches(build, folder, *, refs=None, stack_kib=65536, limit=50,
                        exact=None, also=None):
    """C4: where the compiled model departs from modelx on the model in ``folder``, cell
    by cell.

    ``folder`` is the model folder of a case :func:`compiled_case` made, so modelx and the
    compiled package beside it read the same CSVs.  The model is read from it afresh,
    under a name of its own, ``refs`` are set on its ``Projection``, and every point is
    swept (:func:`full_sweep`): every value modelx then holds in a cache, at every
    argument, is the expectation, and so is every raise.  A fresh read, because the sweep
    evaluates what no projection asks for, a rate before issue among them, which a test
    of the same model's instance may forbid.  The compiled package then makes the same
    calls on the same points with the same ``refs``, in a child (:func:`run_compiled`), on
    a thread of ``stack_kib`` KiB, and reads every ``Data`` cell whose modelx value is an
    array or a number.  ``also``, a callable of one modelx point, adds what it calls to
    the expectation, and so to the compiled run's calls (:func:`c4_expected`).

    They must agree: a number identical where ``exact`` holds, by default where
    :func:`exact_here` does, and elsewhere within :data:`COMPILED_RTOL` relative, floored
    at the cell's largest magnitude on the point; a bool and an int keeping their kind, a
    frame column by column, text exactly, a raise with the same type and message, and
    every ``Data`` array exactly, in dtype and shape too.  Both spaces must come from
    extension modules.  Returns readable lines, ``"point 4: premiums(6): modelx 89.6,
    compiled 89.7"``, empty when the compiled model computes what modelx computes; at
    most ``limit``, the last saying when more were found.
    """
    from us_registry import point_keys, projection
    folder, refs = pathlib.Path(folder), dict(refs or {})
    rtol = 0.0 if (exact_here() if exact is None else exact) else COMPILED_RTOL
    model = mx.read_model(folder, name=f"{build.name}_c4_{next(_c4_names)}")
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        labels = list(model.Data.model_point_table().index)
        keys, expected = point_keys(model), {}
        for key in keys:
            expected[key] = c4_expected(projection(model, key), also)
        data = {}
        for name, cells in model.Data.cells.items():
            try:
                value = cells()
            except Exception as err:            # a raise must meet the same raise
                data[name] = ("raised", _error_text(err))
                continue
            if isinstance(value, np.ndarray) or _kind(value) in ("int", "float"):
                data[name] = ("ok", value)
    finally:
        model.close()
    job = {"refs": refs, "calls": {key: list(found) for key, found in expected.items()},
           "data": list(data)}
    got = run_compiled(folder.parent, build.package.name, job, stack_kib=stack_kib)
    if got["exit"]:
        return [f"the compiled run failed with exit code {got['exit']}:\n{got['stderr']}"]
    lines = [f"{space} was not loaded from an extension module"
             for space, compiled in got["compiled"].items() if not compiled]
    compared = 0
    for key, label in zip(keys, labels):
        found, scales = expected[key], {}
        for (name, _), (status, value) in found.items():
            if status == "ok" and _kind(value) == "float":
                scales[name] = max(scales.get(name, 0.0), _magnitude([value]))
        for ((name, args), want), have in zip(found.items(), got["values"][key]):
            compared += 1
            if (have is not None and want[0] == have[0] == "ok"
                    and type(want[1]) is type(have[1]) and type(want[1]) in _PLAIN
                    and want[1] == have[1]):
                continue                        # identical, the usual case
            text = _outcome_text(want, have, scales.get(name, 0.0), rtol)
            if text:
                lines.append(f"point {label}: {_call(name, args)}: {text}")
    for name, want in data.items():
        compared += 1
        text = _outcome_text(want, got["data"].get(name), 0.0)
        if text:
            lines.append(f"Data.{name}(): {text}")
    if not compared:
        lines.append(f"nothing was compared: {folder} holds no model point")
    if len(lines) > limit:
        lines = lines[:limit - 1] + [f"(and {len(lines) - limit + 1} more)"]
    return lines


# ---------------------------------------------------------------------------
# C5 -- what a compiled Projection formula may not hold


PANDAS_ATTRIBUTES = frozenset({
    "loc", "iloc", "at", "iat", "iterrows", "itertuples", "apply", "values", "to_numpy"})
"""The pandas reads C5 looks for in a ``Projection`` formula, beside the modules."""

C_CALLS = frozenset({"int", "float", "bool", "abs", "min", "max", "range"})
"""The builtins a compiled formula may call, beside cells and ``Data`` vectors: Cython
turns each into C on C numbers, where any other builtin, ``round`` and ``sum`` among them,
is a call into the interpreter, which no declaration shows (R12, R16).  But for ``int`` of
a double: Cython makes it a Python int, converted back to a C integer where it is
returned or used, exact below ``2**63`` and raising ``OverflowError`` past it, a call into
Python that :func:`c_faults` sees only when the int is held in a local, and not as the
temporary of an expression.  A model records each such call (UL's and VUL's
``model-sec.md``, *No Python call kept*), and holds its input below ``2**53`` in
``Data``."""


def _spaces(model):
    """``(name, space)`` for every space of ``model``, the spaces within them included."""
    pending = list(model.spaces.items())
    while pending:
        name, space = pending.pop(0)
        yield name, space
        pending += [(f"{name}.{child}", sub) for child, sub in space.spaces.items()]


def _syntax(cells):
    """A cell's formula parsed: ``(tree, top, parents, exempt)``.

    ``top`` is the formula's own ``def`` or ``lambda``; ``parents`` maps every node to the
    node holding it; ``exempt`` holds the nodes that may hold text, the docstring and
    whatever a ``raise`` holds, its message.
    """
    import ast
    import textwrap
    tree = ast.parse(textwrap.dedent(cells.formula.source))
    first = tree.body[0] if tree.body else None
    top = first.value if isinstance(first, ast.Expr) else first
    parents = {child: node for node in ast.walk(tree)
               for child in ast.iter_child_nodes(node)}
    exempt = set()
    if isinstance(top, ast.FunctionDef) and top.body:
        head = top.body[0]
        if (isinstance(head, ast.Expr) and isinstance(head.value, ast.Constant)
                and isinstance(head.value.value, str)):
            exempt.add(head.value)
    for node in ast.walk(tree):
        if isinstance(node, ast.Raise):
            exempt.update(ast.walk(node))
    return tree, top, parents, exempt


def _element_read(call, parents, ndim):
    """Whether ``call``'s array is read as one element: subscripted at once, by ``ndim``
    indices in all, none a slice, and not written to (mx2cy's usage analysis, F3)."""
    import ast
    remaining, node = ndim, call
    while remaining > 0:
        up = parents.get(node)
        if not (isinstance(up, ast.Subscript) and up.value is node):
            return False
        index = up.slice
        items = index.elts if isinstance(index, ast.Tuple) else [index]
        if len(items) > remaining or any(isinstance(i, (ast.Slice, ast.Starred))
                                         for i in items):
            return False
        remaining -= len(items)
        node = up
    return not isinstance(getattr(node, "ctx", None), (ast.Store, ast.Del))


def _negative_index(call, parents, ndim):
    """The first negative literal among the indices ``call``'s array is read at, as
    written, ``"-1"``, or ``None``: Python and compiled Cython both wrap it to the end of
    the array, so a fault that reads one passes C4 (M23)."""
    import ast
    remaining, node = ndim, call
    while remaining > 0:
        up = parents.get(node)
        if not (isinstance(up, ast.Subscript) and up.value is node):
            return None
        items = up.slice.elts if isinstance(up.slice, ast.Tuple) else [up.slice]
        for item in items:
            value = item
            sign = 1
            while isinstance(value, ast.UnaryOp) and isinstance(value.op,
                                                                (ast.USub, ast.UAdd)):
                sign *= -1 if isinstance(value.op, ast.USub) else 1
                value = value.operand
            if (isinstance(value, ast.Constant) and isinstance(value.value, numbers.Real)
                    and not isinstance(value.value, bool) and sign * value.value < 0):
                return ast.unparse(item)
        remaining -= len(items)
        node = up
    return None


def _vector_text(value):
    """What is wrong with a ``Data`` value a compiled cell reads, or ``None``: it must be
    an int64 or float64 array, a memoryview compiled, or a Python int or float (R5)."""
    if isinstance(value, np.ndarray):
        if value.dtype in (np.dtype("int64"), np.dtype("float64")):
            return None
        return f"an array of {value.dtype}"
    if _kind(value) in ("int", "float") and not isinstance(value, np.generic):
        return None
    return f"a {type(value).__module__.split('.')[0]} {type(value).__name__}"


def _admitted_call(node, parents, cell, python_calls):
    """Whether module name ``node`` heads a call ``python_calls`` admits in ``cell``.

    ``math.erf(x)`` is admitted where the cell's admission names ``"math.erf"``, and only
    as the one argument of a ``float(...)``, which Cython turns into a C double at once, so
    that the call keeps no Python object among the cell's locals or temporaries (R16,
    M25).  A module attribute read but not called, ``math.inf``, is no call, and stays a
    fault; so does an admitted call left unwrapped.
    """
    import ast
    attr = parents.get(node)
    call = parents.get(attr)
    wrap = parents.get(call)
    return (isinstance(attr, ast.Attribute) and attr.value is node
            and isinstance(call, ast.Call) and call.func is attr
            and f"{node.id}.{attr.attr}" in python_calls.get(cell, ())
            and isinstance(wrap, ast.Call) and isinstance(wrap.func, ast.Name)
            and wrap.func.id == "float" and wrap.args == [call] and not wrap.keywords)


def static_faults(model, *, reporting, python_calls=None):
    """C5: what a formula of ``model`` holds that a compiled cell cannot run in C.

    Read from the formulas, so it needs no compiler and runs in the default suite.  Every
    ``Projection`` formula outside ``reporting`` (:func:`reporting_cells`) may refer to no
    module, ``pd`` and ``np`` among them, read no pandas attribute
    (:data:`PANDAS_ATTRIBUTES`), refer to no reporting cell, ``model_point`` among them,
    hold no text outside its docstring and its ``raise`` messages, read no Reference that
    holds text, call ``len()`` nowhere, and hold no generator, comprehension, ``lambda`` or
    nested ``def`` (R10-R13).  Outside its ``raise`` statements it calls no function but
    a cell, a ``Data`` vector and the builtins of :data:`C_CALLS`, and no method, and it
    builds no list, dict, set or tuple, but the index of a table read, ``[s, y]``: each is
    a call into Python inside a cell its declaration types as C (R10, R12).  Every
    ``Data`` cell it calls must return an int64 or float64 array or a Python int or float,
    found by evaluating it, and an array must be read at once by element (R5, R13), at no
    negative literal index, ``[-1]``, which C wraps as Python does, so that C4 cannot see
    a read from the wrong end (:func:`_negative_index`, M23); every ``Data`` array another
    ``Data`` cell calls must be read by element too.  No ``Projection`` cell outside
    the allowlist may be uncached, ``is_cached`` False: mx2cy traces a cell's ``_f_``
    formula, which an uncached cell has none of, so it compiles untyped (R14).  And no
    cell outside the allowlist, in any space, may share its name with a function or a
    method that a call with keywords calls anywhere in the model, the reporting cells
    included, because mx2cy keeps every cell of such a name a Python method (R12).  The
    registry's ``reporting`` must name ``Projection`` cells.  ``python_calls``, the
    registry's ``"python_calls"``, ``{cell: (builtin, ...)}``, admits each builtin it names
    in that cell's formula alone, R16's ``round`` of a projected amount, and each module's
    function it names by its dotted name, ``"math.erf"``, where the call is the one
    argument of a ``float(...)`` (:func:`_admitted_call`, M25).  Returns a line
    per fault, ``"Projection.mort_rate_base, line 9: reads .loc"``, the line counted in the
    formula.
    """
    import ast
    import types
    proj, data = model.Projection, model.Data
    python_calls = python_calls or {}
    lines = [f"the registry's reporting names {name}, which is not a Projection cell"
             for name in sorted(set(reporting) - set(proj.cells))]
    values = {}
    for name, cells in data.cells.items():
        try:
            values[name] = cells()
        except Exception as err:            # reported, and the formulas still read
            lines.append(f"Data.{name} raised {_error_text(err)}")
    arrays = {name: value.ndim for name, value in values.items()
              if isinstance(value, np.ndarray)}
    trees = {(space_name, name): _syntax(cells) for space_name, space in _spaces(model)
             for name, cells in space.cells.items()}
    keyworded = {}
    for (space_name, name), (tree, _, _, _) in trees.items():
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and node.keywords:
                func = node.func
                callee = (func.id if isinstance(func, ast.Name)
                          else getattr(func, "attr", ""))
                keyworded.setdefault(callee, f"{space_name}.{name}, line {node.lineno}")
    for space_name, name in trees:
        if name in keyworded and not (space_name == "Projection" and name in reporting):
            lines.append(f"{space_name}.{name} shares its name with what a call with "
                         f"keywords calls, at {keyworded[name]}: mx2cy keeps every cell "
                         f"of that name a Python method (R12)")
    refs = {ref: value for ref, value in proj.refs.items() if not ref.startswith("__")}
    modules = {ref for ref, value in refs.items() if isinstance(value, types.ModuleType)}
    modules |= {"pd", "np"}
    texts = {ref for ref, value in refs.items() if isinstance(value, str)}
    interfaces = {ref for ref, value in refs.items() if value is data} or {"data"}
    banned = (ast.GeneratorExp, ast.ListComp, ast.SetComp, ast.DictComp, ast.Yield,
              ast.YieldFrom, ast.Lambda, ast.FunctionDef)
    displays = {ast.List: "list", ast.Dict: "dict", ast.Set: "set", ast.Tuple: "tuple"}
    for name in proj.cells:
        if name in reporting:
            continue
        if not proj.cells[name].is_cached:
            lines.append(f"Projection.{name} is uncached: modelx-cython 0.1.0 traces only "
                         f"a cached cell's formula, so an uncached one compiles taking and "
                         f"returning Python objects (R14)")
        tree, top, parents, exempt = trees[("Projection", name)]
        for node in ast.walk(tree):
            where = f"Projection.{name}, line {getattr(node, 'lineno', '?')}"
            kind = displays.get(type(node))
            if kind and node not in exempt and not (
                    isinstance(parents.get(node), ast.Subscript)
                    and parents[node].slice is node):
                lines.append(f"{where}: builds a {kind}, a Python object")
            if isinstance(node, ast.Name):
                if node.id in modules and not _admitted_call(node, parents, name,
                                                             python_calls):
                    lines.append(f"{where}: refers to the module {node.id}")
                elif node.id in reporting:
                    lines.append(f"{where}: refers to the reporting cell {node.id}")
                elif node.id in texts:
                    lines.append(f"{where}: reads {node.id}, a Reference holding text")
            elif isinstance(node, ast.Attribute) and node.attr in PANDAS_ATTRIBUTES:
                lines.append(f"{where}: reads .{node.attr}")
            elif (isinstance(node, ast.Constant) and isinstance(node.value, str)
                  and node not in exempt):
                lines.append(f"{where}: holds the text {node.value!r}")
            elif isinstance(node, banned) and node is not top:
                lines.append(f"{where}: holds a {type(node).__name__}")
            elif isinstance(node, ast.Call) and node not in exempt:
                func = node.func
                if isinstance(func, ast.Name) and func.id == "len":
                    lines.append(f"{where}: calls len()")
                elif isinstance(func, ast.Name):
                    if (func.id not in proj.cells and func.id not in C_CALLS
                            and func.id not in python_calls.get(name, ())):
                        lines.append(f"{where}: calls {func.id}(), a call into Python: a "
                                     f"compiled formula calls cells, Data vectors and "
                                     f"{', '.join(sorted(C_CALLS))} alone")
                elif not (isinstance(func, ast.Attribute)
                          and isinstance(func.value, ast.Name)
                          and func.value.id in interfaces | modules):
                    lines.append(f"{where}: calls the method "
                                 f".{getattr(func, 'attr', '?')}(), a call into Python")
                elif (isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name)
                      and func.value.id in interfaces and func.attr in values):
                    text = _vector_text(values[func.attr])
                    if text:
                        lines.append(f"{where}: reads data.{func.attr}(), {text}, where a "
                                     f"Data vector is an int64 or float64 array or an int")
                    elif (func.attr in arrays
                          and not _element_read(node, parents, arrays[func.attr])):
                        lines.append(f"{where}: uses data.{func.attr}() other than by one "
                                     f"element")
                    elif func.attr in arrays:
                        negative = _negative_index(node, parents, arrays[func.attr])
                        if negative:
                            lines.append(f"{where}: reads data.{func.attr}() at the "
                                         f"negative index {negative}, which wraps to the "
                                         f"array's end in Python and in C alike")
    for name in data.cells:
        tree, _, parents, _ = trees[("Data", name)]
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id in arrays
                    and not _element_read(node, parents, arrays[node.func.id])):
                lines.append(f"Data.{name}, line {node.lineno}: uses {node.func.id}() "
                             f"other than by one element, which compiles it as a Python "
                             f"object (R13)")
    return lines


# ---------------------------------------------------------------------------
# A compiled block run, and what it keeps (F5, K2)


RELEASE_RUNNER = '''\
"""Run an SEC model's run_sec.py over a block, compiled, counting its ItemSpaces.

    python probe.py <run_sec.py> <case dir> <package> <result>

After each collection the runner makes once it has frozen what was alive, the Projection
ItemSpaces still alive are counted.  When the runner is done, what it froze is unfrozen
and they are counted again, so that one kept since before the freeze is seen too.  Then,
if none is, a control: an ItemSpace made and deleted, counted before a collection and
after it.
"""
import contextlib
import gc
import io
import pickle
import runpy
import sys

runner, case, package, result_path = sys.argv[1:5]
collect, after = gc.collect, []


def alive():
    """The ItemSpaces of the base Projection's class alive and not frozen, less the base."""
    module = sys.modules.get(package)
    if module is None:
        return 0
    base = module.mx_model.Projection
    return sum(1 for o in gc.get_objects() if type(o) is type(base) and o is not base)


def counted(*args, **kwargs):
    found = collect(*args, **kwargs)
    if gc.get_freeze_count():
        after.append(alive())
    return found


gc.collect = counted
sys.argv = [runner, "--block", "--build", case]
printed, stopped = io.StringIO(), None
try:
    with contextlib.redirect_stdout(printed):
        runpy.run_path(runner, run_name="__main__")
except SystemExit as stop:
    stopped = stop.code
gc.collect = collect
gc.unfreeze()
kept = alive()
held = freed = None
if stopped in (None, 0) and not kept:
    gc.disable()
    model = sys.modules[package].mx_model
    proj = model.Projection[0]
    proj.proj_len()
    del proj
    del model.Projection[0]
    held = alive()
    collect()
    freed = alive()
    gc.enable()
with open(result_path, "wb") as f:
    pickle.dump({"stopped": stopped, "printed": printed.getvalue(), "after": after,
                 "kept": kept, "held": held, "freed": freed}, f)
'''
"""The child that :func:`release_faults` starts around the product's own runner."""


def release_faults(case_dir, package, runner, *, points, timeout=600):
    """Where a compiled block run keeps what it has released (F5, K2), a line each.

    ``runner`` is a product's ``run_sec.py``, run with ``--block --build case_dir`` on
    the compiled ``package`` there, in a child, as a user runs it, ``points`` the number
    of points in the case's table.  A compiled ItemSpace holds every cell's cache in its
    C struct, about 430 KB for Term, and a deleted one is not freed: it refers to
    itself, as its own ``_space`` and in its own ``_mx_roots``, cycles only the cyclic
    collector frees.  So the runner releases each point once read, deleting it and
    collecting, in its frame pass and in its projections, after freezing what was alive
    before the block.  So, counting the ``Projection`` ItemSpaces alive besides the
    base: none may be alive after any collection the runner makes once frozen, and there
    must be at least one such collection for every point; none may be alive when the
    block ends, frozen or not; and then the control must still find the cycle, a deleted
    ItemSpace alive until a collection frees it.  If the control fails, modelx-cython
    frees an ItemSpace on its own, and the collection can go.
    """
    import os
    import pickle
    import subprocess
    import sys
    import tempfile
    case_dir = pathlib.Path(case_dir)
    work = pathlib.Path(tempfile.mkdtemp(prefix="release_", dir=case_dir.parent))
    probe, result = work / "probe.py", work / "found.pickle"
    probe.write_text(RELEASE_RUNNER, encoding="utf-8")
    done = subprocess.run(
        [sys.executable, "-P", str(probe), str(runner), str(case_dir), package,
         str(result)], capture_output=True, text=True, encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}, timeout=timeout)
    if done.returncode:
        return [f"the block run failed with exit code {done.returncode}:\n"
                f"{done.stderr[-4000:]}"]
    found = pickle.loads(result.read_bytes())
    if found["stopped"] not in (None, 0):
        return [f"run_sec.py --block stopped: {found['stopped']}"]
    lines, after = [], found["after"]
    if len(after) < points:
        lines.append(f"the runner collected {len(after)} times once frozen, over "
                     f"{points} points: it does not collect after each release")
    worst = max(after, default=0)
    if worst:
        first = next(i for i, n in enumerate(after) if n) + 1
        lines.append(f"up to {worst} ItemSpaces were alive after a release and its "
                     f"collection, the first time at collection {first}: the runner keeps "
                     f"a point it has read")
    if found["kept"]:
        lines.append(f"{found['kept']} ItemSpaces were still alive when the block ended")
    if found["held"] not in (None, 1):
        lines.append(f"the control: a deleted ItemSpace left {found['held']} alive before "
                     f"a collection, not 1; if modelx-cython no longer holds it in a "
                     f"cycle, the runner's collection can go")
    if found["freed"]:
        lines.append(f"the control: a collection left {found['freed']} deleted ItemSpaces "
                     f"alive")
    return lines


def runner_add(runner):
    """The running sum ``add(total, compensation, frame)`` of a product's ``run_sec.py``.

    The runner runs the model when imported, so the function is read from its source and
    run alone, as every product's runner defines it, at the module's top level.
    """
    import ast
    tree = ast.parse(pathlib.Path(runner).read_text(encoding="utf-8"))
    found = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "add"]
    if len(found) != 1:
        raise ValueError(f"{runner} defines add() {len(found)} times, not once")
    space = {}
    exec(compile(ast.Module(found, []), str(runner), "exec"), space)
    return space["add"]


def block_sum_faults(add, frames):
    """Where a runner's running sum of ``frames`` is not pandas' ``groupby`` sum, a line.

    A block run keeps one point's frame at a time, so it sums the frames as it goes, with
    ``add``, compensated, so that its block is the frames concatenated and summed by
    ``t``, bit for bit; the printed block, to two decimals, cannot show a last bit.  So
    ``add`` (:func:`runner_add`) sums ``frames``, each a ``result_cf()`` indexed by ``t``
    from 0, into arrays as long as the longest, as the runner does, and the sum must equal
    ``pd.concat(frames).groupby(level=0).sum()`` by ``np.array_equal``.  The frames must
    be finite: ``groupby`` skips a NaN, which the runner's sum carries.  Returns a line
    per fault.
    """
    if not frames:
        return ["no frames to sum"]
    columns = list(frames[0].columns)
    lines = []
    for i, frame in enumerate(frames):
        if list(frame.index) != list(range(len(frame))):
            lines.append(f"frame {i} is not indexed by t = 0, 1, ...")
        if list(frame.columns) != columns:
            lines.append(f"frame {i} has the columns {list(frame.columns)}, not {columns}")
        elif not np.isfinite(frame.to_numpy(dtype=float)).all():
            lines.append(f"frame {i} is not finite, where groupby skips a NaN")
    if lines:
        return lines
    rows = max(len(frame) for frame in frames)
    total = np.zeros((rows, len(columns)))
    compensation = np.zeros_like(total)
    for frame in frames:
        add(total, compensation, frame[columns].to_numpy())
    want = pd.concat(frames).groupby(level=0).sum()[columns].to_numpy()
    if want.shape != total.shape:
        return [f"the sum is {total.shape}, groupby's {want.shape}"]
    if not np.array_equal(total, want):
        bad = np.argwhere(total != want)
        t, c = bad[0]
        lines.append(f"the running sum departs from groupby's in {len(bad)} values, first "
                     f"{columns[c]} at t = {t}: {float(total[t, c])!r}, where groupby "
                     f"gives {float(want[t, c])!r}")
    return lines


def label_mismatches(build, folder, labels):
    """C4 on label accessors alone: ``(modelx's values, a line per mismatch)``.

    ``folder`` is a :func:`compiled_case` of ``build``, and ``labels`` names label
    accessors of no parameter.  Each is called on every point, in modelx and, in a child,
    compiled (:func:`run_compiled`), and the two must agree: a value of the same kind,
    equal, or NaN on both sides, or the same raise.  A label that is not text, a blank or
    a number ``Data`` accepts, is where an accessor typed ``str`` compiled departs, raising
    ``TypeError`` where modelx returns the value (C3, M22).  The values modelx returned
    are ``{point_id: {label: ("ok", value) or ("raised", text)}}``, for the caller's
    assertions on what the case holds.
    """
    from us_registry import point_keys, projection
    model = mx.read_model(folder, name=f"{build.name}_labels_{next(_c4_names)}")
    try:
        ids = list(model.Data.model_point_table().index)
        keys = point_keys(model)
        want = {}
        for point_id, key in zip(ids, keys):
            proj = projection(model, key)
            want[point_id] = {}
            for label in labels:
                try:
                    want[point_id][label] = ("ok", proj.cells[label]())
                except Exception as err:            # compared with the compiled raise
                    want[point_id][label] = ("raised", _error_text(err))
    finally:
        model.close()
    job = {"refs": {}, "calls": {i: [(label, ()) for label in labels]
                                 for i in range(len(ids))}}
    got = run_compiled(folder.parent, build.package.name, job)
    if got["exit"]:
        return want, [f"the compiled run failed: {got['stderr']}"]
    lines = [f"{space} is not compiled" for space, done in got["compiled"].items()
             if not done]
    for i, point_id in enumerate(ids):
        for label, have in zip(labels, got["values"][i]):
            mine = want[point_id][label]
            same = mine[0] == have[0] and (
                (mine[0] == "raised" and mine[1] == have[1])
                or (mine[0] == "ok" and _kind(mine[1]) == _kind(have[1])
                    and (mine[1] == have[1]
                         or (_kind(mine[1]) == "float" and mine[1] != mine[1]
                             and have[1] != have[1]))))
            if not same:
                lines.append(f"point {point_id}: {label}() is {have!r} compiled, "
                             f"{mine!r} in modelx")
    return want, lines
