"""Tests of the SEC harness and row generator in :mod:`sec_support`, on ``Term_US_S``.

Phase 0 of USLIB-SEC-PLAN.md builds the SEC test machinery before any SEC model exists, so
it is tested here on what does exist.  ``Term_US_S`` is compared with a second read of
itself, where the twin identity must hold exactly and must break where a Reference is
changed.  Small synthetic models stand in where a difference of a given kind must be seen.
And a synthetic :class:`SecSpec`, never registered except under ``monkeypatch`` for the
regeneration round trip, generates a table from Term's two points.

What each test pins, against the plan (its §4 item 3 and §5.2):

* T1's comparison, :func:`twin_mismatches`: silent on a true twin, but only after it has
  compared every value the S sweep cached, a tuple argument included; loud, and specific,
  on a changed one; bounded by ``limit``; an SEC error, an uncomparable value or an S cell
  the SEC model lacks reported rather than raised or passed; S's reads past its own frame
  left out; an offset, or an argument map, turning S's call into SEC's; and, at stage
  ``"EC"``, :func:`codes` turning S's timing and phase strings into SEC's int References.
* T2 and T3's harness: :func:`temp_inputs` copies a product so an added point projects
  exactly as its source, and writes floats the models' reader reads back exactly;
  :func:`shift_months` re-bases a table under both readings; :func:`frame_mismatches`
  compares on an offset and refuses to pass a comparison that compares nothing, or less
  than the whole splice.
* T6's generator: :func:`build_sec_table` writes twins, a derived row and a future row
  with the right counts, durations, sources and ids, and no text that is not S's own or
  composed from S's keys and a month (``CLAUDE.md``); :func:`write_generated` is a no-op on
  a rerun; and :func:`check_generated` reports an edited S row cell by cell, but reads a
  float by its value, so a file written on another platform checks clean.
* C2's fingerprint: :func:`fingerprint_months` names the frame's first, last and quartile
  months; :func:`fingerprint_text` writes a literal that reads back as the freeze exactly,
  within 92 columns; and :func:`fingerprint_mismatches` reports every kind of departure,
  a spike in a month the freeze does not name and a zero column that moves included.
* Compiling: :func:`cython_missing` names what a machine lacks, and :func:`require_cython`
  skips, or fails under ``USLIB_REQUIRE_CYTHON=1``; :class:`SecBuilds` builds a model
  once and keeps a failed build's error for every asker; C3's readers find every kind of
  fault in written declarations, a reporting label typed as text among them, a written
  spec and written C; C5's static check finds every construct it forbids in a synthetic
  model, a negative literal index among them, and passes the ones it allows; the sample
  check finds an engine cell no call reaches; C4's comparison keeps a value's kind and
  floors its tolerance at the magnitude, or at a tolerance of 0 tells one ulp apart;
  :func:`full_sweep` reaches every cell at every month and keeps each raise; and the
  block-sum check fails a plain running sum by an ulp.  None of these compiles anything.

modelx keeps every model in one registry, and ``conftest.term_life`` already holds the
default name, so every model here is read under a name of its own and closed.
"""
import dataclasses
import io
import itertools
import math
import re

import modelx as mx
import numpy as np
import pandas as pd
import pytest

from sec_support import (
    SEC_SPECS, TWIN_EXEMPT_DEFAULT, SecSpec, build_sec_table, check_generated, codes,
    fingerprint,
    fingerprint_mismatches, fingerprint_months, fingerprint_text, frame_mismatches,
    shift_months, sweep, temp_inputs, twin_mismatches, write_generated)
from us_registry import model_path

TERM = "Term_US_S"

_names = itertools.count(1)


def _name(tag):
    """A model name no other read in this process uses."""
    return f"{TERM}_secsup_{tag}_{next(_names)}"


def _read(tag, path=None):
    return mx.read_model(path or model_path(TERM), name=_name(tag))


@pytest.fixture(scope="module")
def s_model():
    """Term_US_S with point 1 swept, the S side of every comparison here."""
    model = _read("s")
    sweep(model.Projection[1])
    yield model
    model.close()


@pytest.fixture
def other():
    """A second, cold read of Term_US_S, free to be changed by the test that holds it."""
    model = _read("other")
    yield model
    model.close()


# The synthetic spec: Term's two points as twins, point 1 restated in force at month 12,
# and point 1 written 3 months after the valuation date.  ``duration_inforce`` is a count of
# years that SEC's ``duration_mth`` replaces (D6), so it is dropped.
SPEC = SecSpec(twin=TERM, column_map={"duration_inforce": None},
               derived=((1, 12),), future=((1, 3),))


# ---------------------------------------------------------------------------
# T1 -- twin_mismatches


def test_a_second_read_of_the_same_model_is_its_twin(s_model, other):
    """The identity holds between two reads of one model, and is not vacuous.

    An empty list could also mean nothing was compared, so the test also asserts that
    the S sweep cached thousands of values and that every one of them was evaluated on the
    other side.
    """
    s_proj, o_proj = s_model.Projection[1], other.Projection[1]
    assert twin_mismatches(s_proj, o_proj) == []
    compared = {name: set(s_proj.cells[name].keys()) for name in s_proj.cells
                if name not in TWIN_EXEMPT_DEFAULT}
    assert sum(len(keys) for keys in compared.values()) > 10_000
    for name, keys in compared.items():
        assert keys <= set(o_proj.cells[name].keys()), f"{name} was not compared"


def _cells_named(lines):
    return {line.split("(", 1)[0] for line in lines}


def test_a_changed_reference_is_found_in_the_cells_it_moves(s_model, other):
    """A higher maintenance expense shows in ``expenses`` and what sums it, and only there.

    ``premiums``, ``claims`` and ``pols_if`` read no expense, so no line may name them.
    """
    other.Projection.expense_maint = 31.0
    lines = twin_mismatches(s_model.Projection[1], other.Projection[1], limit=10_000)
    assert _cells_named(lines) == {"expenses", "net_cf", "result_cf", "result_cf_annual"}
    assert any(line.startswith("expenses(0): S 302.5, SEC 302.58") for line in lines)
    frame_lines = [line for line in lines if line.startswith("result_cf()")]
    assert {re.search(r"column '(\w+)'", line).group(1) for line in frame_lines} == {
        "expenses", "net_cf"}
    assert all("720 of 720 differ" in line for line in frame_lines)


def test_the_limit_stops_the_scan_and_says_so(s_model, other):
    """At most ``limit`` lines, the last one saying that more were found."""
    other.Projection.expense_maint = 31.0
    lines = twin_mismatches(s_model.Projection[1], other.Projection[1], limit=5)
    assert len(lines) == 5
    assert all(line.startswith("expenses(") for line in lines[:4])
    assert "more than 4 mismatches" in lines[-1]
    assert len(twin_mismatches(s_model.Projection[1], other.Projection[1], limit=1)) == 1
    with pytest.raises(ValueError):
        twin_mismatches(s_model.Projection[1], other.Projection[1], limit=0)


def _premium_taxes_failing_at_issue(t):
    if t == 0:
        raise ValueError("no premium tax at issue")
    return premium_tax_rate * premiums(t)                           # noqa: F821


def test_an_error_in_the_sec_model_is_reported_not_raised(s_model, other):
    """One broken cells is a line, and the comparison goes on past it."""
    other.Projection.premium_taxes.formula = _premium_taxes_failing_at_issue
    lines = twin_mismatches(s_model.Projection[1], other.Projection[1], limit=10_000)
    assert "premium_taxes(0): SEC raised ValueError: no premium tax at issue" in lines
    assert "net_cf(0): SEC raised ValueError: no premium tax at issue" in lines
    later = ("premium_taxes(1)", "net_cf(1)")
    assert not [line for line in lines if line.startswith(later)]


# Two synthetic Spaces whose cells return every kind of value the comparison knows, and one
# it does not.  Where S and SEC differ, they differ on purpose.
S_KINDS = {
    "phase": lambda: "LEVEL",
    "flag": lambda: True,
    "legs": lambda: ("call", "put"),
    "ids": lambda: [1, 2],
    "by_mth": lambda: {"a": 1.0, "b": 2.0},
    "blank": lambda: float("nan"),
    "cap": lambda: float("inf"),
    "opaque": lambda: object(),
    "rate": lambda t: 0.01 * t,
    "scalar_array": lambda: np.array(5.0),
    "grid": lambda: np.ones((2, 2)),
}
SEC_KINDS = {
    "phase": lambda: 1,
    "flag": lambda: 1.0,
    "legs": lambda: ("call", "put"),
    "ids": lambda: [1, 2, 3],
    "by_mth": lambda: {"a": 1.0 + 1e-12, "c": 3.0},
    "blank": lambda: float("nan"),
    "cap": lambda: 1e308,
    "opaque": lambda: object(),
    "rate": lambda t: 0.01 * t,
    "scalar_array": lambda: np.array(5.0),
    "grid": lambda: np.array([[1.0, 1.0], [1.0, 2.0]]),
}


def _space(model, formulas):
    space = model.new_space("P")
    space.pd = pd
    space.np = np
    for name, formula in formulas.items():
        space.new_cells(name, formula=formula)
    return space


def test_values_compare_by_kind():
    """Each kind of value is compared as that kind, and an unknown kind is never passed."""
    s, sec = mx.new_model(_name("kinds_s")), mx.new_model(_name("kinds_sec"))
    try:
        s_space, sec_space = _space(s, S_KINDS), _space(sec, SEC_KINDS)
        for name in S_KINDS:
            s_space.cells[name](*([5] if name == "rate" else []))
        lines = twin_mismatches(s_space, sec_space, exempt=frozenset(), limit=100)
    finally:
        s.close()
        sec.close()
    assert sorted(lines) == sorted([
        "phase(): S 'LEVEL' (str), SEC 1 (int)",
        "flag(): S True (bool), SEC 1.0 (float)",
        "ids(): length: S 2, SEC 3",
        "by_mth(): keys only in S: 'b'",
        "by_mth(): keys only in SEC: 'c'",
        "cap(): S inf, SEC 1e+308, diff -inf",
        "opaque(): uncomparable: S object, SEC object",
        "grid(): [1] [1] S 1.0, SEC 2.0, diff +1",
    ])


def test_an_s_cell_the_sec_model_lacks_is_reported_unless_exempt():
    """A cells renamed or dropped is a line of its own, not a comparison left out.

    The SEC Space here has S's ``rate`` under another name, so every golden on ``rate``
    would go unchecked without a word.  Exempting it, as a product does for a cell it drops
    by design, with its reason, takes the line out.
    """
    s, sec = mx.new_model(_name("lack_s")), mx.new_model(_name("lack_sec"))
    try:
        s_space = _space(s, {"rate": "lambda t: 0.01 * t",
                             "net": "lambda t: 2.0 * rate(t)"})
        sec_space = _space(sec, {"mort_rate": "lambda t: 0.01 * t",
                                 "net": "lambda t: 2.0 * mort_rate(t)"})
        s_space.net(3)
        lines = twin_mismatches(s_space, sec_space, exempt=frozenset())
        exempted = twin_mismatches(s_space, sec_space, exempt=frozenset({"rate"}))
    finally:
        s.close()
        sec.close()
    assert lines == ["rate: a cell of S that SEC lacks; a cell SEC drops by design is "
                     "named in the spec's exempt, with its reason"]
    assert exempted == []


# A frame of months 0 to 4, whose ratio reads month 5, past it, as Term_US_S's jump_ratio()
# reads premium_pp_ann(12n) on a point whose cover ends with the level period.  The SEC
# side answers 0.0 there, outside cover; ``lift`` moves its premium inside the frame.
def _frame_pair(tag, lift=0.0, frame=True):
    s, sec = mx.new_model(_name(f"{tag}_s")), mx.new_model(_name(f"{tag}_sec"))
    s_formulas = {"prem": "lambda t: 100.0 + t", "ratio": "lambda: prem(5) / prem(4)"}
    sec_formulas = {"prem": f"lambda t: 100.0 + {lift} + t if t < 5 else 0.0",
                    "ratio": "lambda: 105.0 / prem(4)"}
    if frame:
        s_formulas["proj_len"] = sec_formulas["proj_len"] = "lambda: 5"
    return s, sec, _space(s, s_formulas), _space(sec, sec_formulas)


def test_only_the_s_frame_is_compared():
    """A month S reads ahead of its frame, at or past its ``proj_len()``, is not compared.

    S answers such a read from its tables as though cover went on, where SEC answers that
    the month is outside cover (:func:`_frame_pair`).  Inside the frame a difference is
    still found, and a Space with no ``proj_len`` is compared at every month it cached.
    """
    found = {}
    for tag, lift, frame in (("same", 0.0, True), ("lifted", 1.0, True),
                             ("frameless", 0.0, False)):
        s, sec, s_space, sec_space = _frame_pair(tag, lift, frame)
        try:
            s_space.ratio()
            assert sorted(s_space.cells["prem"].keys()) == [4, 5]
            found[tag] = twin_mismatches(s_space, sec_space)
        finally:
            s.close()
            sec.close()
    assert found["same"] == []
    assert found["lifted"] == ["prem(4): S 104.0, SEC 105.0, diff +1",
                               "ratio(): S 1.0096153846153846, SEC 1.0, diff -0.00962"]
    assert found["frameless"] == ["prem(5): S 105.0, SEC 0.0, diff -105"]


def test_a_cells_cached_at_a_tuple_argument_is_compared():
    """A one-parameter cells called with a tuple is compared at that tuple.

    modelx caches ``f(("call", "put"))`` under the bare tuple, which ``Cells.items()`` looks
    up again as two arguments, raising ``TypeError`` before anything is compared.
    """
    s, sec = mx.new_model(_name("tuple_s")), mx.new_model(_name("tuple_sec"))
    try:
        s_space = _space(s, {"leg_value": lambda legs: float(len(legs))})
        sec_space = _space(sec, {"leg_value": lambda legs: (
            2.0 if legs[0] == "call" else 0.0)})
        s_space.leg_value(("call", "put"))
        s_space.leg_value(("put", "call"))
        lines = twin_mismatches(s_space, sec_space)
    finally:
        s.close()
        sec.close()
    assert lines == ["leg_value(('put', 'call')): S 2.0, SEC 0.0, diff -2"]


def test_an_offset_reads_s_t_as_sec_t_plus_offset():
    """``t_offset`` maps S's ``t`` to SEC's in one sense, for cells and frames alike.

    The SEC cells here is the S one restarted three months on: SEC month ``t`` is S month
    ``t + 3``, so both comparisons take ``3``, the ``source_mth`` of a row derived from S
    month 3.  :func:`twin_mismatches` calls the SEC cells at S's ``t - 3`` and skips the S
    months before 3, which have no SEC month; :func:`frame_mismatches` reads SEC row ``t``
    against S row ``t + 3``.  The wrong sign fails both.
    """
    frame = ("lambda: pd.DataFrame({'x': [rate(t) for t in range(10)]}, "
             "index=pd.Index(range(10), name='t'))")
    s, sec = mx.new_model(_name("off_s")), mx.new_model(_name("off_sec"))
    try:
        s_space = _space(s, {"rate": lambda t: 0.01 * t, "result_x": frame})
        sec_space = _space(sec, {"rate": lambda t: 0.01 * (t + 3), "result_x": (
            "lambda: pd.DataFrame({'x': [rate(t) for t in range(7)]}, "
            "index=pd.Index(range(7), name='t'))")})
        s_df, sec_df = s_space.result_x(), sec_space.result_x()
        assert twin_mismatches(s_space, sec_space, t_offset=3) == []
        assert sorted(sec_space.cells["rate"].keys()) == list(range(7))
        assert frame_mismatches(s_df, sec_df, t_offset=3) == []
        unshifted = twin_mismatches(s_space, sec_space)
        twin_wrong = twin_mismatches(s_space, sec_space, t_offset=-3)
    finally:
        s.close()
        sec.close()
    assert unshifted[0] == "rate(0): S 0.0, SEC 0.03, diff +0.03"
    assert "result_x(): 3 labels only in S: t=7, t=8, t=9" in unshifted
    assert twin_wrong[0] == "rate(0) [SEC rate(3)]: S 0.0, SEC 0.06, diff +0.06"
    shifted_wrong = frame_mismatches(s_df, sec_df, t_offset=-3)
    assert len(shifted_wrong) == 2
    assert shifted_wrong[0] == "the frames end apart: S ends at t=12 (S t=9), SEC at t=6"
    assert shifted_wrong[1].startswith(
        "column 'x': 4 of 4 differ, first at t=3 (S t=0): S 0.0, SEC 0.06; largest")


def test_arg_map_turns_s_arguments_into_sec_ones():
    """Phase 2's mapping: S's timing strings become the int codes the SEC cells take (R9).

    The label shows both calls when they differ, so a wrong code is read off the line, and
    ``None`` from the map skips a key the SEC model has no counterpart for.
    """
    codes = {"BEF_DECR": 2, "AFT_DECR": 3}

    def to_codes(name, args):
        return (args[0], codes[args[1]]) if name == "pols_at" else args

    def bef_decr_only(name, args):
        return to_codes(name, args) if args[1] == "BEF_DECR" else None

    s, sec = mx.new_model(_name("map_s")), mx.new_model(_name("map_sec"))
    try:
        s_space = _space(s, {"pols_at": lambda t, timing: (
            1.0 * t if timing == "BEF_DECR" else 2.0 * t)})
        sec_space = _space(sec, {"pols_at": lambda t, timing: (
            1.0 * t if timing == 2 else 2.0 * t)})
        for args in ((1, "BEF_DECR"), (1, "AFT_DECR"), (2, "BEF_DECR")):
            s_space.pols_at(*args)
        assert twin_mismatches(s_space, sec_space, arg_map=to_codes) == []
        assert twin_mismatches(s_space, sec_space) == [
            "pols_at(1, 'BEF_DECR'): S 1.0, SEC 2.0, diff +1",
            "pols_at(2, 'BEF_DECR'): S 2.0, SEC 4.0, diff +2"]
        codes["BEF_DECR"] = 3
        assert twin_mismatches(s_space, sec_space, arg_map=bef_decr_only) == [
            "pols_at(1, 'BEF_DECR') [SEC pols_at(1, 3)]: S 1.0, SEC 2.0, diff +1",
            "pols_at(2, 'BEF_DECR') [SEC pols_at(2, 3)]: S 2.0, SEC 4.0, diff +2"]
    finally:
        s.close()
        sec.close()


# S spells a timing and a phase as text, and SEC, at stage "EC", as int References named as
# the text (R9, R10).  Both keep a label accessor's text.  SEC also holds References that
# are not codes: a bool, a lower-case int and an all-capital float.
S_TEXT = {
    "pols_if_at": "lambda t, timing: 10.0 * t + (1.0 if timing == 'BEF_DECR' else 0.0)",
    "phase": "lambda t: 'LEVEL' if t < 2 else 'PLT'",
    "sex": "lambda: 'M'",
}
SEC_CODES = {
    "pols_if_at": "lambda t, timing: 10.0 * t + (1.0 if timing == BEF_DECR else 0.0)",
    "phase": "lambda t: LEVEL if t < lift else PLT",
    "sex": "lambda: 'M'",
}


def test_codes_turn_s_strings_into_sec_ints():
    """``codes`` maps S's timing arguments and phase values onto SEC's int References.

    With them the two Spaces agree: ``pols_if_at(1, "BEF_DECR")`` is called as
    ``pols_if_at(1, 1)``, S's ``"LEVEL"`` is compared with SEC's ``LEVEL``, and the label
    accessor's ``"M"`` stays a string on both sides.  Without them SEC is called with S's
    strings and compared with S's labels, and a phase coded wrongly is reported as such.
    """
    s, sec = mx.new_model(_name("codes_s")), mx.new_model(_name("codes_sec"))
    try:
        s_space, sec_space = _space(s, S_TEXT), _space(sec, SEC_CODES)
        for name, value in {"BEF_NB": 0, "BEF_DECR": 1, "LEVEL": 1, "PLT": 2, "FLAG": True,
                            "lift": 2, "RATE": 0.5}.items():
            setattr(sec_space, name, value)
        for timing in ("BEF_NB", "BEF_DECR"):
            s_space.pols_if_at(1, timing)
        s_space.phase(0), s_space.phase(3), s_space.sex()
        found = {"codes": codes(sec_space)}
        found["with"] = twin_mismatches(s_space, sec_space, exempt=frozenset(),
                                        codes=found["codes"])
        found["without"] = twin_mismatches(s_space, sec_space, exempt=frozenset())
        sec_space.lift = 0                  # month 0 now coded PLT, which S calls LEVEL
        found["wrong"] = twin_mismatches(s_space, sec_space, exempt=frozenset(),
                                         codes=found["codes"])
    finally:
        s.close()
        sec.close()
    assert found["codes"] == {"BEF_NB": 0, "BEF_DECR": 1, "LEVEL": 1, "PLT": 2}
    assert found["with"] == []
    assert found["without"] == [
        "pols_if_at(1, 'BEF_DECR'): S 11.0, SEC 10.0, diff -1",
        "phase(0): S 'LEVEL' (str), SEC 1 (int)", "phase(3): S 'PLT' (str), SEC 2 (int)"]
    assert found["wrong"] == ["phase(0): S 'LEVEL' is code 1; S 1, SEC 2, diff +1"]


def test_a_spec_maps_s_none_total_onto_the_code_sec_takes():
    """A spec's ``twin_arg_map`` turns S's ``None`` for a total into SEC's code (R12).

    S's ``claims(t, kind=None)`` caches its total under ``(t, None)``, and at stage
    ``"EC"`` an SEC model takes the total as a code, ``claims(t, ALL)``.  :func:`codes`
    maps S's strings alone, so the spec's map names the code by its string, and ``codes``
    then turns that into SEC's int, as T1 passes both.  Without the map, SEC is called with
    S's ``None``.
    """
    spec = SecSpec(twin=TERM, twin_arg_map=lambda name, args: (
        (args[0], "ALL") if name == "claims" and args[1] is None else args))
    s, sec = mx.new_model(_name("total_s")), mx.new_model(_name("total_sec"))
    try:
        s_space = _space(s, {"claims": (
            "lambda t, kind=None: 3.0 * t if kind is None else 1.0 * t")})
        sec_space = _space(sec, {"claims": (
            "lambda t, kind: 3.0 * t if kind == ALL else 1.0 * t")})
        sec_space.ALL, sec_space.DEATH = 0, 1
        s_space.claims(2), s_space.claims(2, "DEATH")
        found = {"with": twin_mismatches(s_space, sec_space, exempt=frozenset(),
                                         arg_map=spec.twin_arg_map,
                                         codes=codes(sec_space)),
                 "without": twin_mismatches(s_space, sec_space, exempt=frozenset(),
                                            codes=codes(sec_space))}
    finally:
        s.close()
        sec.close()
    assert found["with"] == []
    assert found["without"] == ["claims(2, None): S 6.0, SEC 2.0, diff -4"]
    assert SecSpec(twin=TERM).twin_arg_map is None


def test_frame_mismatches_will_not_pass_a_comparison_of_nothing():
    """An empty overlap, a missing named column or a gap is a line, never a silent pass."""
    df = pd.DataFrame({"pols_if": [1.0, 0.9, 0.8, 0.7], "net_cf": [-5.0, 1.0, 1.0, 1.0]},
                      index=pd.Index(range(4), name="t"))
    assert frame_mismatches(df, df.copy()) == []
    assert frame_mismatches(df, df, t_offset=10) == [
        "no shared rows: S rows 0..3 are SEC t = -10..-7, and SEC has t = 0..3"]
    assert frame_mismatches(df, df, columns=["net_cf", "claims"]) == [
        "columns missing from S: ['claims']", "columns missing from SEC: ['claims']"]
    renamed = df.rename(columns={"pols_if": "lives", "net_cf": "cash"})
    assert frame_mismatches(df, renamed) == ["no column to compare"]
    gapped = df.drop(index=2)
    assert frame_mismatches(df, gapped) == ["1 rows inside the shared range only in S: t=2"]
    moved = df.copy()
    moved.loc[1, "net_cf"] = 1.0 + 1e-6
    assert frame_mismatches(df, moved) == [
        "column 'net_cf': 1 of 4 differ, first at t=1: S 1.0, SEC 1.000001"]
    assert frame_mismatches(df, moved, atol=1e-5) == []


def test_frame_mismatches_reports_a_frame_that_ends_too_soon_or_too_late():
    """The splice must run to the end of cover, which is one instant on both clocks.

    A row derived from S month 120 of a 720-month frame is SEC ``t = 0 .. 599``.  An SEC
    frame cut short by a wrong ``proj_len()``, or run on past the end, agrees with S on
    every row the two share, and must still fail.
    """
    s = pd.DataFrame({"net_cf": np.arange(720.0)}, index=pd.Index(range(720), name="t"))
    good = s.loc[120:].set_axis(pd.Index(range(600), name="t"))
    assert frame_mismatches(s, good, t_offset=120) == []
    assert frame_mismatches(s, good.loc[:479], t_offset=120) == [
        "the frames end apart: S ends at t=599 (S t=719), SEC at t=479"]
    late = pd.concat([good, pd.DataFrame({"net_cf": [0.0] * 30},
                                         index=pd.Index(range(600, 630), name="t"))])
    assert frame_mismatches(s, late, t_offset=120) == [
        "the frames end apart: S ends at t=599 (S t=719), SEC at t=629"]
    # A future point issued 3 months on: SEC t = 3 .. 722 is S t = 0 .. 719, and the
    # pre-issue rows 0 .. 2 are not compared.
    future = pd.concat([pd.DataFrame({"net_cf": [0.0] * 3},
                                     index=pd.Index(range(3), name="t")),
                        s.set_axis(pd.Index(range(3, 723), name="t"))])
    assert frame_mismatches(s, future, t_offset=-3) == []
    assert frame_mismatches(s, future.loc[:700], t_offset=-3) == [
        "the frames end apart: S ends at t=722 (S t=719), SEC at t=700"]


# ---------------------------------------------------------------------------
# T2 and T3 -- temp_inputs and shift_months


def test_temp_inputs_projects_an_added_point_exactly_like_its_source(s_model, tmp_path):
    """Point 99, a copy of point 1 in a copied product, projects exactly as point 1 does."""
    table = s_model.Data.model_point_table()
    points = pd.concat([table, table.loc[[1]].rename(index={1: 99})])
    folder = temp_inputs(tmp_path, model_path(TERM), model_points=points)
    assert folder == tmp_path / TERM
    assert not list(folder.rglob("__pycache__"))
    source = model_path(TERM).parent
    for csv_path in source.glob("*.csv"):
        if csv_path.name != "model_point_table.csv":
            assert (tmp_path / csv_path.name).read_bytes() == csv_path.read_bytes()
    model = _read("tmp", folder)
    try:
        assert model.Data.input_dir() == tmp_path
        pd.testing.assert_frame_equal(model.Data.model_point_table(), points)
        one, copy = model.Projection[1], model.Projection[99]
        assert frame_mismatches(one.result_cf(), copy.result_cf(), rtol=0, atol=0) == []
        assert frame_mismatches(s_model.Projection[1].result_cf(), copy.result_cf(),
                                rtol=0, atol=0) == []
        sweep(one)
        assert twin_mismatches(one, copy, rtol=0, atol=0) == []
    finally:
        model.close()


# Floats plain ``repr`` writes and pandas' default parser reads back wrong, by 1 to 1,685
# ulps, but for which a 17-digit text exists that it reads exactly.  Measured on pandas
# 3.0.5; the last two lose digits to leading zeros, which pandas counts among its 17.
HARD_FLOATS = [0.17893481367543618, 0.9051438366771739, 0.29830276735556926,
               0.9669622001623905, 0.9955002834343927, 0.00012345678901234567,
               0.0012345678901234567]
# Floats no decimal text near them makes the default parser produce: read to within an ulp.
UNREACHABLE_FLOATS = [0.22733602246716966, 0.22520718999059186]


def test_temp_inputs_writes_floats_the_models_read_back_exactly(tmp_path):
    """Written values come back from ``pd.read_csv`` as the models call it, exactly.

    The control half shows the test has teeth: written as plain ``repr``, every one of
    the hard floats comes back wrong.  It applies where the installed pandas has the
    defect, as 3.0.5 does; a pandas whose parser rounds correctly reads every text right,
    and the exactness asserted below then holds with no workaround to test.
    """
    values = HARD_FLOATS + UNREACHABLE_FLOATS + [53730.123456789123, 0.0445, 100000.0]
    plain = pd.read_csv(io.StringIO("v\n" + "\n".join(map(repr, HARD_FLOATS)) + "\n"))
    if plain["v"].tolist() != HARD_FLOATS:
        assert all(a != b for a, b in zip(plain["v"], HARD_FLOATS))

    frame = pd.DataFrame({"point_id": range(1, len(values) + 1), "value": values,
                          "label": "x", "flag": True, "count": 3})
    frame.loc[0, "label"] = None
    temp_inputs(tmp_path, model_path(TERM), model_points=frame,
                model_point_file="floats_sec.csv")
    back = pd.read_csv(tmp_path / "floats_sec.csv", index_col="point_id")
    assert back["value"].tolist()[:len(HARD_FLOATS)] == HARD_FLOATS
    reached = back["value"].tolist()[len(HARD_FLOATS):len(HARD_FLOATS) + 2]
    for got, want in zip(reached, UNREACHABLE_FLOATS):
        assert abs(got - want) <= np.spacing(want)
    assert back["value"].tolist()[-3:] == [53730.123456789123, 0.0445, 100000.0]
    texts = pd.read_csv(tmp_path / "floats_sec.csv", dtype=str)["value"]
    assert [float(t) for t in texts] == values, "a text a correct parser misreads"
    assert pd.isna(back["label"].iloc[0]) and (back["label"].iloc[1:] == "x").all()
    assert back["flag"].tolist() == [True] * len(values)
    assert back["count"].dtype == np.int64


def test_temp_inputs_edits_by_value_or_by_function_and_refuses_a_missing_file(tmp_path):
    """An edit replaces a file or transforms it; one naming a file the copy lacks raises."""
    def double(df):
        return df.assign(factor=df["factor"] * 2)

    temp_inputs(tmp_path, model_path(TERM), edits={"class_factor_table.csv": double})
    edited = pd.read_csv(tmp_path / "class_factor_table.csv")
    shipped = pd.read_csv(model_path(TERM).parent / "class_factor_table.csv")
    assert edited["factor"].tolist() == (shipped["factor"] * 2).tolist()
    assert list(edited.columns) == list(shipped.columns)
    with pytest.raises(FileNotFoundError, match="class_factors.csv"):
        temp_inputs(tmp_path, model_path(TERM), edits={"class_factors.csv": shipped})


def _table(rows, columns=("month", "rate")):
    return pd.DataFrame(rows, columns=list(columns))


def test_shift_months_reads_a_step_table_and_an_exact_one():
    """Step: the row in force at ``d`` becomes month 0.  Exact: earlier rows are dropped."""
    table = _table([(0, 0.01), (12, 0.02), (24, 0.03)])
    step = shift_months(table, "month", 18)
    assert step.values.tolist() == [[0, 0.02], [6, 0.03]]
    exact = shift_months(table, "month", 18, step=False)
    assert exact.values.tolist() == [[6, 0.03]]
    at_a_row = shift_months(table, "month", 12)
    assert at_a_row.values.tolist() == [[0, 0.02], [12, 0.03]]
    assert shift_months(table, "month", 0).equals(table)
    assert list(step.index) == [1, 2], "rows keep their labels"
    assert step["month"].dtype == table["month"].dtype


def test_shift_months_re_bases_each_group_and_every_row_in_force():
    """Each ``by`` group keeps its own row in force; rows sharing that month all survive."""
    table = _table([("A", 0, 0.01), ("A", 12, 0.02), ("A", 24, 0.03),
                    ("B", 0, 0.05), ("B", 6, 0.06)], columns=("scenario_id", "month", "r"))
    shifted = shift_months(table, "month", 12, by="scenario_id")
    assert shifted.values.tolist() == [["A", 0, 0.02], ["A", 12, 0.03], ["B", 0, 0.06]]
    ungrouped = shift_months(table, "month", 12)
    assert ungrouped.values.tolist() == [["A", 0, 0.02], ["A", 12, 0.03]]
    two_keys = shift_months(table.drop(index=[1, 2]), "month", 3)
    assert two_keys.values.tolist() == [["A", 0, 0.01], ["B", 0, 0.05], ["B", 3, 0.06]]


def test_shift_months_moves_a_future_point_later_and_refuses_a_blank_month():
    """``d = -k`` moves every row ``k`` months on and invents nothing before it."""
    table = _table([(0, 0.01), (12, 0.02)])
    assert shift_months(table, "month", -3).values.tolist() == [[3, 0.01], [15, 0.02]]
    with pytest.raises(ValueError, match="blank month"):
        shift_months(_table([(0, 0.01), (None, 0.02)]), "month", 1)


# ---------------------------------------------------------------------------
# T6 -- build_sec_table, write_generated, check_generated


# The words the generator composes ids and provenance from, beside S's keys and a month:
# ``TL-000001-M12``, ``TL-000001-F3``, "S point 1 (TL-000001) restated in force at S month
# 12", "... issued 3 months after the valuation date".  A word outside this set in a
# generated text cell is one the generator added, which ``CLAUDE.md`` forbids.
TEMPLATE_WORDS = {"M", "F", "S", "point", "restated", "in", "force", "at", "month",
                  "months", "issued", "after", "the", "valuation", "date"}
ROW_KINDS = {"twin", "derived", "future"}


def _foreign_text(table, s_table, rename):
    """Every text cell that is neither copied from its S row nor composed from S's keys.

    A cell passes if it equals its source S row's value in the same column, renamed back;
    or, with that row's ``policy_id``, ``point_id`` and the row's month taken out, if
    what is left is template words and punctuation only.
    """
    s_rows = {r["policy_id"]: r for r in s_table.reset_index().to_dict("records")}
    s_column = {new: old for old, new in rename.items() if new is not None}
    foreign = []
    for record in table.to_dict("records"):
        source = s_rows[record["source_policy_id"]]
        for column, value in record.items():
            if not isinstance(value, str):
                continue
            if column == "row_kind" and value in ROW_KINDS:
                continue
            if source.get(s_column.get(column, column)) == value:
                continue
            rest = value
            keys = (source["policy_id"], str(abs(record["source_mth"])),
                    str(source["point_id"]))
            for key in sorted(keys, key=len, reverse=True):
                rest = rest.replace(key, " ")
            words = set(re.findall(r"[A-Za-z]+", rest))
            if not words <= TEMPLATE_WORDS or re.search(r"\d", rest):
                foreign.append((record["point_id"], column, value))
    return foreign


SEC_COLUMNS = ["point_id", "policy_id", "age_at_entry", "sex", "rate_class", "plan",
               "sum_assured", "premium_mode", "policy_count", "plt_mort_factor_override",
               "duration_mth", "row_kind", "source_policy_id", "source_mth"]


def test_build_sec_table_writes_twins_a_derived_and_a_future_row(s_model):
    """The table of D8 from Term's two points: every column and every generated cell."""
    table, companions = build_sec_table(SPEC, s_model)
    s_table = s_model.Data.model_point_table()
    assert companions == {}
    assert list(table.columns) == SEC_COLUMNS
    assert table["row_kind"].tolist() == ["twin", "twin", "derived", "future"]
    assert table["point_id"].tolist() == [1, 2, 3, 4]
    assert table["policy_id"].tolist() == [
        "TL-000001", "TL-000002", "TL-000001-M12", "TL-000001-F3"]
    assert table["point_id"].is_unique and table["policy_id"].is_unique
    assert table["duration_mth"].tolist() == [0, 0, 12, -3]
    assert table["source_mth"].tolist() == [0, 0, 12, -3]
    assert table["source_policy_id"].tolist() == [
        "TL-000001", "TL-000002", "TL-000001", "TL-000001"]
    assert table["policy_count"].tolist() == [
        1.0, 1.0, s_model.Projection[1].pols_if(12), 1.0]
    assert s_model.Projection[1].pols_if(12) < 1.0
    # Every column S has is S's value for the source row, renamed where it was renamed.
    for record in table.to_dict("records"):
        source = s_table.loc[1 if record["source_policy_id"] == "TL-000001" else 2]
        for column in ("age_at_entry", "sex", "rate_class", "plan", "sum_assured",
                       "premium_mode", "plt_mort_factor_override"):
            assert record[column] == source[column] or (
                pd.isna(record[column]) and pd.isna(source[column]))
    assert _foreign_text(table, s_table, {"pols_if_init": "policy_count"}) == []


def test_future_state_sets_a_future_rows_columns_from_s_and_k(s_model):
    """A future row takes ``future_state``'s values; the twins and the derived row do not.

    Two columns: ``sum_assured``, which S's table has, so the twins and the derived row
    keep S's value; and ``fresh``, which S's lacks and nothing else sets, so it is a column
    of its own, after the state columns, blank on every row but the future one.  Without
    ``future_state`` among the columns the table is built with, the second would be dropped
    without a word.
    """
    spec = dataclasses.replace(SPEC, future_state={
        "sum_assured": lambda s, k: s.sum_assured() + k,
        "fresh": lambda s, k: f"{s.plan()}-{k}"})
    table, _ = build_sec_table(spec, s_model)
    assert table["sum_assured"].tolist() == [100000.0, 100000.0, 100000.0, 100003.0]
    assert list(table.columns) == SEC_COLUMNS[:-3] + ["fresh", *SEC_COLUMNS[-3:]]
    assert table["fresh"].isna().tolist() == [True, True, True, False]
    assert table["fresh"].iloc[3] == "T10-3"


def _by_sum_assured(model):
    """A ``model_state``: a column for each sum assured of ``model``'s table, the count S
    carries into the row's month on a point of that sum, and 0.0 on another."""
    sums = sorted(set(model.Data.model_point_table()["sum_assured"]))
    return {f"pols_{x:.0f}": (lambda s, d, x=x: s.pols_if(d) if s.sum_assured() == x
                              else 0.0) for x in sums}


def test_model_state_takes_its_columns_from_the_s_model_the_table_is_built_from(
        s_model, tmp_path):
    """``model_state`` gives state columns named by the S model the table is built from.

    On Term's table, whose two points each assure 100,000, :func:`_by_sum_assured` gives one
    column, which comes before the state's and is set as the state is: the twins at their
    ``source_mth``, the derived row at its month, the future row its twin's.  On a copy
    whose second point assures 200,000 it gives a column for each, read off that copy, as
    VA's subaccount values are read off the fund table the generator's S model reads.
    """
    spec = dataclasses.replace(SPEC, model_state=_by_sum_assured,
                               state={"fresh": lambda s, d: float(d)})
    table, _ = build_sec_table(spec, s_model)
    assert list(table.columns) == [*SEC_COLUMNS[:-3], "pols_100000", "fresh",
                                   *SEC_COLUMNS[-3:]]
    assert table["pols_100000"].tolist() == [1.0, 1.0, s_model.Projection[1].pols_if(12),
                                             1.0]
    assert table["fresh"].iloc[2] == 12.0
    folder = temp_inputs(tmp_path, model_path(TERM), edits={
        "model_point_table.csv": lambda df: df.assign(sum_assured=[100000.0, 200000.0])})
    model = _read("sums", folder)
    try:
        table, _ = build_sec_table(spec, model)
    finally:
        model.close()
    assert [c for c in table.columns if c.startswith("pols_")] == [
        "pols_100000", "pols_200000"]
    assert table["pols_200000"].tolist() == [0.0, 1.0, 0.0, 0.0]


def test_generated_text_is_s_text_or_composed_from_s_keys(tmp_path):
    """With a ``provenance`` column in S: twins copy it, the generated rows cite S by key.

    Term's table has no ``provenance`` column, so one is added in a copy.  The words it
    holds cite sources by key, as ``CLAUDE.md`` requires of any provenance cell.
    """
    provenance = ["worked example anchor cell [S5]", "[std] variant without the override"]
    folder = temp_inputs(tmp_path, model_path(TERM), edits={
        "model_point_table.csv": lambda df: df.assign(provenance=provenance)})
    model = _read("prov", folder)
    try:
        table, _ = build_sec_table(SPEC, model)
        s_table = model.Data.model_point_table()
    finally:
        model.close()
    assert list(table.columns) == SEC_COLUMNS + ["provenance"]
    assert table["provenance"].tolist() == provenance + [
        "S point 1 (TL-000001) restated in force at S month 12",
        "S point 1 (TL-000001) issued 3 months after the valuation date"]
    assert _foreign_text(table, s_table, {"pols_if_init": "policy_count"}) == []
    planted = table.copy()
    planted.loc[2, "provenance"] = "S point 1 restated by Example Mutual at S month 12"
    assert _foreign_text(planted, s_table, {"pols_if_init": "policy_count"}) == [
        (3, "provenance", "S point 1 restated by Example Mutual at S month 12")]


@pytest.mark.parametrize("change, error", [
    ({"model_point_file": "model_point_table.csv"}, "never overwrite"),
    ({"companions": {"premium_rates.csv": lambda m, t: t}}, "never overwrite"),
    ({"state": {"policy_id": lambda s, d: "x"}}, "the generator owns them"),
    ({"twin_state": {"policy_count": lambda s, d: 2.0}}, "the generator owns them"),
    ({"state": {"provenance": lambda s, d: "x"}}, "the generator owns them"),
    ({"companions": {"model_point_table_sec.csv": lambda m, t: t}}, "would replace"),
    ({"future_state": {"policy_count": lambda s, k: 2.0}}, "the generator owns them"),
    ({"future_state": {"duration_mth": lambda s, k: 0}}, "the generator owns them"),
])
def test_a_spec_that_could_clobber_s_or_the_generator_is_refused(change, error):
    with pytest.raises(ValueError, match=error):
        dataclasses.replace(SPEC, **change)


@pytest.mark.parametrize("change, error", [
    ({"derived": ((1, 0),)}, "after the twin's entry month"),
    ({"derived": ((1, 720),)}, "inside S's frame"),
    ({"derived": ((7, 12),)}, "point 7"),
    ({"derived": ((1, 12), (1, 12))}, "repeats policy_id"),
    ({"future": ((1, 0),)}, "at least 1"),
    ({"column_map": {"no_such_column": None}}, "no_such_column"),
    ({"column_map": {"sex": "plan"}}, "two columns one name"),
    ({"duration_of": lambda row: -1}, "never future business"),
    ({"model_state": lambda m: {"policy_count": lambda s, d: 2.0}},
     "the generator owns them"),
    ({"model_state": lambda m: {"fresh": lambda s, d: 0.0},
      "state": {"fresh": lambda s, d: 1.0}}, "state or twin_state sets too"),
])
def test_build_sec_table_rejects_a_spec_that_does_not_fit_the_s_table(s_model, change,
                                                                    error):
    with pytest.raises(ValueError, match=error):
        build_sec_table(dataclasses.replace(SPEC, **change), s_model)


def _policy_ids(s_model, table):
    """A companion built from the SEC table: one row per SEC point and its policy."""
    return table[["point_id", "policy_id", "source_mth"]]


def test_regeneration_is_stable_and_reports_an_edited_s_row(tmp_path, monkeypatch):
    """T6's round trip, in a copy of the product directory.

    Written, the files check clean and a rewrite touches nothing.  Then a reworded S
    ``policy_id`` reaches every cell that copies or composes it, in the table and in its
    companion, and nothing else.
    """
    temp_inputs(tmp_path, model_path(TERM))
    spec = dataclasses.replace(SPEC, companions={"policy_ids_sec.csv": _policy_ids})
    monkeypatch.setitem(SEC_SPECS, "Term_US_SEC_selftest", spec)
    table_path = tmp_path / "model_point_table_sec.csv"
    companion_path = tmp_path / "policy_ids_sec.csv"

    assert write_generated("Term_US_SEC_selftest", tmp_path) == {
        table_path: True, companion_path: True}
    assert check_generated("Term_US_SEC_selftest", tmp_path) == []
    written, stamp = table_path.read_bytes(), table_path.stat().st_mtime_ns
    assert write_generated("Term_US_SEC_selftest", tmp_path) == {
        table_path: False, companion_path: False}
    assert table_path.read_bytes() == written and table_path.stat().st_mtime_ns == stamp
    assert written.decode().splitlines()[3] == (
        "3,TL-000001-M12,35,M,StdNT,T10,100000.0,A,0.939248,3.5,12,derived,TL-000001,12")

    s_csv = tmp_path / "model_point_table.csv"
    s_csv.write_bytes(s_csv.read_bytes().replace(b"TL-000001", b"TL-900001"))
    drift = check_generated("Term_US_SEC_selftest", tmp_path)
    found = [re.match(r"(\S+): row \d+ \(point_id (\d+)\), (\w+): committed", line)
             for line in drift]
    assert all(found), drift
    assert {m.groups() for m in found} == {
        ("model_point_table_sec.csv", point, column)
        for point in ("1", "3", "4") for column in ("policy_id", "source_policy_id")
    } | {("policy_ids_sec.csv", point, "policy_id") for point in ("1", "3", "4")}
    assert ("model_point_table_sec.csv: row 3 (point_id 3), policy_id: committed "
            "'TL-000001-M12', generated 'TL-900001-M12'") in drift

    write_generated("Term_US_SEC_selftest", tmp_path)
    assert check_generated("Term_US_SEC_selftest", tmp_path) == []
    companion_path.unlink()
    assert check_generated("Term_US_SEC_selftest", tmp_path) == [
        "policy_ids_sec.csv: generated, but not committed"]

    # A committed row cut short shows its missing cells, and a stray line is a row too.
    write_generated("Term_US_SEC_selftest", tmp_path)
    text = table_path.read_bytes()
    table_path.write_bytes(text.replace(b",TL-900001,-3\n", b"\n") + b"\n")
    assert check_generated("Term_US_SEC_selftest", tmp_path) == [
        "model_point_table_sec.csv: row 4 (point_id 4), source_policy_id: committed None, "
        "generated 'TL-900001'",
        "model_point_table_sec.csv: row 4 (point_id 4), source_mth: committed None, "
        "generated '-3'",
        "model_point_table_sec.csv: committed row 5 (a blank line) is no longer generated"]


def test_regeneration_reads_a_float_by_its_value_not_its_spelling(tmp_path, monkeypatch):
    """A committed float spelled otherwise, or a last bit off, is current and left alone.

    Another platform's pandas may spell a computed float otherwise, and its libm may compute
    it a last bit apart (``sec_support``'s module docstring), so neither is drift and
    neither is rewritten.  A real change of value is drift, and so is ``1`` for ``1.0``,
    which changes the dtype pandas reads; so are cells beyond the header, and text that is
    not the writer's own once its cells agree.
    """
    model = _read("respell", temp_inputs(tmp_path, model_path(TERM)))
    monkeypatch.setitem(SEC_SPECS, "Term_US_SEC_selftest", SPEC)
    path = tmp_path / "model_point_table_sec.csv"
    try:
        _respellings(model, path, tmp_path)
    finally:
        model.close()


def _respellings(model, path, product_dir):
    """The body of the test above, on an S model read once from ``product_dir``."""
    def check():
        return check_generated("Term_US_SEC_selftest", product_dir, s_model=model)

    def write():
        return write_generated("Term_US_SEC_selftest", product_dir, s_model=model)[path]

    write()
    written = path.read_bytes().decode("utf-8")
    row = written.splitlines()[3].split(",")
    count = float(row[8])
    assert row[:3] == ["3", "TL-000001-M12", "35"] and 0.9 < count < 1.0

    def with_count(text):
        """The committed table with the derived row's policy_count spelled ``text``."""
        lines = written.splitlines()
        cells = lines[3].split(",")
        cells[8] = text
        lines[3] = ",".join(cells)
        return "\n".join(lines) + "\n"

    def committed(text):
        path.write_bytes(text.encode("utf-8"))
        stamp = path.stat().st_mtime_ns
        drift = check()
        rewritten = write()
        assert rewritten == bool(drift)
        assert rewritten or path.stat().st_mtime_ns == stamp
        return drift

    spelled = f"{count:.16e}"
    assert spelled != row[8] and float(spelled) == count
    assert committed(with_count(spelled)) == []
    assert committed(with_count(repr(math.nextafter(count, 2.0)))) == []
    moved = repr(count * (1 + 1e-9))
    assert committed(with_count(moved)) == [
        f"model_point_table_sec.csv: row 3 (point_id 3), policy_count: committed "
        f"{moved!r}, generated {row[8]!r}"]
    assert committed(written.replace("\n3,", "\n3.0,")) == [
        "model_point_table_sec.csv: row 3 (point_id 3), point_id: committed '3.0', "
        "generated '3'"]
    assert committed(written.replace(",twin,TL-000002,0\n", ",twin,TL-000002,0,x\n")) == [
        "model_point_table_sec.csv: committed row 2 (point_id 2) has cells beyond its "
        "header: ['x']"]
    assert committed(written.replace("\n", "\r\n")) == [
        "model_point_table_sec.csv: the cells agree, but the text differs (quoting or line "
        "ends); regenerate it"]
    assert path.read_bytes().decode("utf-8") == written


def test_an_unregistered_spec_name_is_refused():
    with pytest.raises(KeyError, match="Term_US_SEC_nonesuch"):
        check_generated("Term_US_SEC_nonesuch")


# ---------------------------------------------------------------------------
# C2 -- fingerprint, fingerprint_text and fingerprint_mismatches


_FP_RESULT_CF = """def result_cf():
    ts = list(range(rows))
    flows = [100.0 * point_id + t + (lift if t == 4 else 0.0)
             + (spike if t == 1 else 0.0) - (spike if t == 3 else 0.0) for t in ts]
    return pd.DataFrame({"pols_if": [1.0] * rows, "net_cf": flows,
                         "conv_credits": [zero] * rows}, index=pd.Index(ts, name="t"))
"""

_FP_RESULT_POLS = """def result_pols():
    ts = list(range(rows))
    return pd.DataFrame({"pols_death": [1.9988090701711986e-05 * (t + 1) for t in ts]},
                        index=pd.Index(ts, name="t"))
"""


def _fp_model(tag, rows):
    """A synthetic model the fingerprint reads as it reads an SEC model: two points.

    ``net_cf`` moves with three References: ``lift`` at month 4, which a nine-month frame's
    fingerprint names, and ``spike`` up at month 1 and down at month 3, which it names
    not, so that the sum and the named months stand still and only the largest value
    moves.  ``conv_credits`` is ``zero`` throughout, a column whose scale is 0, as Term's
    conversion credits are at the shipped rates.  ``pols_death`` holds small counts whose
    shortest ``repr`` carries an exponent, and so a hyphen.
    """
    model = mx.new_model(_name(tag))
    data = model.new_space("Data")
    data.pd = pd
    data.new_cells("model_point_table", formula=(
        "lambda: pd.DataFrame({'x': [0.0, 0.0]}, index=pd.Index([1, 2], name='point_id'))"))
    proj = model.new_space("Projection", formula=lambda point_id: None)
    proj.pd = pd
    proj.rows, proj.lift, proj.spike, proj.zero = rows, 0.0, 0.0, 0.0
    proj.new_cells("result_cf", formula=_FP_RESULT_CF)
    proj.new_cells("result_pols", formula=_FP_RESULT_POLS)
    return model


def test_fingerprint_months_are_the_first_last_and_quartile_months():
    """Five months a frame holds, fewer where a short frame has fewer, never repeated."""
    assert fingerprint_months(720) == (0, 179, 359, 539, 719)
    assert fingerprint_months(723) == (0, 180, 361, 541, 722)
    assert fingerprint_months(9) == (0, 2, 4, 6, 8)
    assert fingerprint_months(3) == (0, 1, 2)
    assert fingerprint_months(1) == (0,)


def test_a_fingerprint_writes_out_and_reads_back_exactly():
    """The literal is the freeze exactly, within 92 columns, a one-month frame included.

    The counts' exponents put hyphens in the wrapped lines, where ``textwrap`` would break
    a number in two unless told not to, and a one-month tuple needs its trailing comma.
    """
    for rows in (9, 1):
        model = _fp_model(f"fp_text{rows}", rows)
        try:
            frozen = fingerprint(model)
        finally:
            model.close()
        assert list(frozen) == [1, 2]
        assert frozen[2]["rows"] == rows
        assert frozen[2]["months"] == fingerprint_months(rows)
        assert list(frozen[2]["result_cf"]) == ["pols_if", "net_cf", "conv_credits"]
        total, scale, values = frozen[2]["result_cf"]["net_cf"]
        assert (total, scale) == (sum(200.0 + t for t in range(rows)), 200.0 + rows - 1)
        assert values == tuple(200.0 + t for t in fingerprint_months(rows))
        text = fingerprint_text("Synthetic", frozen)
        lines = text.splitlines()
        assert lines[0] == ("# BEGIN generated fingerprint: Synthetic -- "
                            "tools/gen_sec_fingerprint.py")
        assert lines[-1] == "# END generated fingerprint: Synthetic"
        assert max(len(line) for line in lines) <= 92
        namespace = {}
        exec(text, namespace)
        assert namespace["FINGERPRINT"] == frozen
    assert any(line.strip().endswith(",)),") for line in lines)


def test_every_departure_from_a_fingerprint_is_reported():
    """A value at a named month, the largest value alone, a zero column, the frame, the
    columns and the points: each departure is a line, and the unchanged model has none."""
    model = _fp_model("fp_mismatch", 9)
    try:
        frozen = fingerprint(model)
        found = {"unchanged": fingerprint_mismatches(frozen, model)}
        for case, ref, value in (("lift", "lift", 1e-8), ("spike", "spike", 50.0),
                                 ("zero", "zero", 1e-300), ("rows", "rows", 10)):
            setattr(model.Projection, ref, value)
            found[case] = fingerprint_mismatches(frozen, model)
            setattr(model.Projection, ref, 9 if ref == "rows" else 0.0)
        renamed = {1: {**frozen[1], "result_pols": {"pols_lapse": (0.0, 0.0, (0.0,))}},
                   2: frozen[2]}
        found["columns"] = fingerprint_mismatches(renamed, model)
        found["points"] = fingerprint_mismatches({1: frozen[1]}, model)
    finally:
        model.close()
    assert found["unchanged"] == []
    assert found["lift"] == [
        "point 1: result_cf['net_cf'] sums to 936.00000001, frozen 936.0",
        "point 1: result_cf['net_cf'] at t=4 is 104.00000001, frozen 104.0",
        "point 2: result_cf['net_cf'] sums to 1836.00000001, frozen 1836.0",
        "point 2: result_cf['net_cf'] at t=4 is 204.00000001, frozen 204.0"]
    assert found["spike"] == [
        "point 1: result_cf['net_cf'] reaches 151.0, frozen 108.0",
        "point 2: result_cf['net_cf'] reaches 251.0, frozen 208.0"]
    assert found["zero"][:3] == [
        "point 1: result_cf['conv_credits'] sums to 9e-300, frozen 0.0",
        "point 1: result_cf['conv_credits'] reaches 1e-300, frozen 0.0",
        "point 1: result_cf['conv_credits'] at t=0 is 1e-300, frozen 0.0"]
    assert found["rows"] == ["point 1: 10 rows, frozen 9", "point 2: 10 rows, frozen 9"]
    assert found["columns"] == ["point 1: result_pols columns ['pols_death'], frozen "
                                "['pols_lapse']"]
    assert found["points"] == ["points: frozen [1], now [1, 2]"]


# ---------------------------------------------------------------------------
# Compiling: require_cython, SecBuilds, and the checks of C3, C4 and C5


def test_cython_missing_names_what_this_machine_lacks(monkeypatch):
    """The tool, modelx-cython and, on POSIX, the C compiler, each named when missing."""
    import importlib.util
    import os
    import pathlib

    import sec_support
    present = pathlib.Path(__file__)
    found = {}
    monkeypatch.setattr(sec_support, "_tool", lambda: present.with_name("no_such_tool.py"))
    found["tool"] = sec_support.cython_missing()
    monkeypatch.setattr(sec_support, "_tool", lambda: present)
    real = importlib.util.find_spec
    with monkeypatch.context() as patch:
        patch.setattr(importlib.util, "find_spec",
                      lambda name, *args: None if name == "modelx_cython"
                      else real(name, *args))
        found["modelx_cython"] = sec_support.cython_missing()
    if importlib.util.find_spec("modelx_cython") is not None and os.name == "posix":
        monkeypatch.setenv("CC", "no-such-compiler-cc")
        found["compiler"] = sec_support.cython_missing()
    assert "tools/build_sec_cy.py is absent" in found["tool"]
    assert "modelx-cython is not installed" in found["modelx_cython"]
    # Read only where it was taken: a machine without modelx-cython never reaches the
    # compiler check, as on every leg of CI's test job.
    if "compiler" in found:
        assert found["compiler"].endswith("'no-such-compiler-cc', which is not on PATH")


def test_require_cython_skips_and_the_cython_job_fails_instead(monkeypatch):
    """Without the toolchain a compile test skips, and under ``USLIB_REQUIRE_CYTHON=1``
    fails, saying what is missing; with it, the build tool comes back as a module."""
    import sec_support
    monkeypatch.setattr(sec_support, "cython_missing", lambda: "no compiler here")
    monkeypatch.delenv("USLIB_REQUIRE_CYTHON", raising=False)
    with pytest.raises(pytest.skip.Exception, match="no compiler here"):
        sec_support.require_cython()
    monkeypatch.setenv("USLIB_REQUIRE_CYTHON", "0")
    with pytest.raises(pytest.skip.Exception, match="no compiler here"):
        sec_support.require_cython()
    monkeypatch.setenv("USLIB_REQUIRE_CYTHON", "1")
    with pytest.raises(pytest.fail.Exception,
                       match="USLIB_REQUIRE_CYTHON=1 forbids a skip, and no compiler here"):
        sec_support.require_cython()
    tool = sec_support._tool()
    if tool is not None and tool.is_file():
        monkeypatch.setattr(sec_support, "cython_missing", lambda: None)
        module = sec_support.require_cython()
        assert callable(module.build) and module.DIRECTIVE.startswith("# cython:")


def test_sec_builds_compiles_each_model_once_and_keeps_a_failure(monkeypatch,
                                                                 tmp_path_factory):
    """A model is built once a session, and a failed build fails every asker unbuilt."""
    import types

    import sec_support
    calls = []

    def build(product_dir, model, out):
        calls.append(model)
        if model == "Term_US_S":
            raise RuntimeError("the compiler failed")
        package = out / f"{model}_nomx_cy"
        package.mkdir()
        (package / "_mx_classes.pxd").write_text("cdef class _c_Projection(x):\n",
                                                 encoding="utf-8")
        return package

    monkeypatch.setattr(sec_support, "require_cython",
                        lambda: types.SimpleNamespace(build=build))
    builds = sec_support.SecBuilds(tmp_path_factory)
    first, again = builds("Term_US_SEC"), builds("Term_US_SEC")
    assert first is again and calls == ["Term_US_SEC"]
    assert first.package == first.out / "Term_US_SEC_nomx_cy"
    assert first.pxd.startswith("cdef class _c_Projection")
    errors = []
    for _ in range(2):
        with pytest.raises(RuntimeError, match="the compiler failed") as excinfo:
            builds("Term_US_S")
        errors.append(excinfo.value)
    assert errors[0] is errors[1] and calls == ["Term_US_SEC", "Term_US_S"]


# A compiled model's declarations, as mx2cy writes them: Data, then Projection.  Of the
# Projection cells, a and e are C; b returns an object and caches in a dict, as an
# untraced cell does; c takes its timing as text; f takes a policy year the spec does not
# size; d is missing, a Python method; g takes and returns objects and has no cache, as an
# uncached cell does, since mx2cy traces no uncached formula; result_cf is a report.
# Data.y is an object, and so is Data.table, a reader of an input file, which may stay one.
PXD = """\
cdef class _c_Data(_mx_sys.BaseSpace):

    cdef const double[:] _v_x
    cdef object _v_y
    cdef object _v_table

    cpdef const double[:] x(_c_Data self)
    cpdef object y(_c_Data self)
    cpdef object table(_c_Data self)

cdef class _c_Projection(_mx_sys.BaseSpace):

    cdef double[100] _v_a
    cdef dict _v_b
    cdef dict _v_c
    cdef double[100][2] _v_e
    cdef bint[7] _v_f
    cdef object _v_result_cf

    cpdef _mx_copy_refs(_c_Projection self, object base, object base_root)
    cpdef double a(_c_Projection self, long long t)
    cpdef object b(_c_Projection self, long long t)
    cpdef double c(_c_Projection self, long long t, str timing)
    cpdef double e(_c_Projection self, long long t, long long timing)
    cpdef bint f(_c_Projection self, long long y)
    cpdef object g(_c_Projection self, object t)
    cpdef object result_cf(_c_Projection self)
"""


def _declared_model(tag):
    """A modelx model with the cells :data:`PXD` declares, d among them.  ``Data.table``
    reads ``table_file``, and ``Data.y`` names it only in a refusal, which a reader's
    formula does not."""
    model = mx.new_model(_name(tag))
    data = model.new_space("Data")
    data.table_file = "table.csv"
    data.new_cells("x", formula="lambda: 0.0")
    data.new_cells("y", formula=(
        "def y():\n    if False:\n        raise ValueError(f'{table_file} is bad')\n"
        "    return 0.0\n"))
    data.new_cells("table", formula="lambda: table_file")
    proj = model.new_space("Projection")
    for name in ("a", "b", "c", "d", "e", "f", "g"):
        proj.new_cells(name, formula="lambda t: 0.0")
    proj.cells["g"].is_cached = False
    proj.new_cells("result_cf", formula="lambda: 0.0")
    return model


def test_the_typing_guard_reads_every_kind_of_fault_from_the_declarations(tmp_path):
    """C3 on a written ``.pxd``: an object, a text parameter, a dict cache, a cell not
    compiled, an uncached cell, which mx2cy leaves untyped, an object ``Data`` vector but a
    reader's; and the spec: a size off, a size missing, a misspelt key."""
    from sec_support import Build, data_readers, spec_faults, typing_faults
    build = Build("Synthetic", tmp_path, tmp_path / "pkg", PXD)
    model = _declared_model("pxd")
    try:
        readers = data_readers(model)
        found = typing_faults(build, model, reporting={"result_cf"},
                              new_data={"x", "y", "table"})
    finally:
        model.close()
    assert readers == {"table"}
    assert [line.split(":")[0].split(",")[0] for line in found] == [
        "Projection.b returns object", "Projection.b caches its values in a Python dict",
        "Projection.c takes timing as str",
        "Projection.c caches its values in a Python dict",
        "Projection.d did not compile", "Projection.g returns object",
        "Projection.g takes t as object", "Data.y returns object"]
    assert "an uncached one" in found[5] and "has no trace of" in found[6], found[5:7]
    spec = tmp_path / "spec_sec.py"
    spec.write_text('# sizes\n{"spaces": {"Projection": {"cells_param_size": {\n'
                    '    "t": 100, ("t", "timing"): (100, 3), "tt": 5}}}}\n',
                    encoding="utf-8")
    assert spec_faults(build, spec) == [
        "Projection.e: a cache of (100, 2), where spec_sec.py gives (100, 3)",
        "Projection.f: spec_sec.py gives no size for ('y',), so the sample sized its "
        "cache, (7,)",
        "spec_sec.py sizes ('tt',), which no compiled cell takes: mx2cy ignores the size, "
        "as it ignores a misspelt name"]


# The C Cython writes for six formulas, its names shortened: a keeps C locals alone, and
# raises a ValueError, a builtin an exception; e a Python object, as an integer local does
# under Cython's default inference; g calls the builtin round; h builds a list for sum; k
# builds a dict; and the report result_cf keeps a Python object too, as it may.
_C_SOURCE = """\
static double __pyx_f_1S_13_c_Projection__f_a(void *__pyx_v_self, PY_LONG_LONG __pyx_v_t) {
  PY_LONG_LONG __pyx_v_n;
  double __pyx_r;
  __pyx_t_1 = __Pyx_PyObject_FastCall(__pyx_builtin_ValueError, __pyx_callargs, 2);
  return __pyx_r;
}

static double __pyx_f_1S_13_c_Projection__f_g(void *__pyx_v_self, PY_LONG_LONG __pyx_v_t) {
  __pyx_t_2 = __Pyx_PyObject_FastCall(__pyx_builtin_round, __pyx_callargs, 3);
  return 0.0;
}

static double __pyx_f_1S_13_c_Projection__f_h(void *__pyx_v_self, PY_LONG_LONG __pyx_v_t) {
  __pyx_t_1 = PyList_New(2);
  __pyx_t_2 = __Pyx_PyObject_FastCall(__pyx_builtin_sum, __pyx_callargs, 2);
  return 0.0;
}

static double __pyx_f_1S_13_c_Projection__f_k(void *__pyx_v_self, PY_LONG_LONG __pyx_v_t) {
  __pyx_t_1 = __Pyx_PyDict_NewPresized(2);
  return 0.0;
}

static double __pyx_f_1S_13_c_Projection__f_e(void *__pyx_v_self, PY_LONG_LONG __pyx_v_t) {
  PyObject *__pyx_v_n = NULL;
  PyObject *__pyx_v_rate = NULL;
  return 0.0;
}

static PyObject *__pyx_f_1S_13_c_Projection__f_result_cf(void *__pyx_v_self) {
  PyObject *__pyx_v_ts = NULL;
  return __pyx_r;
}
"""


def test_the_generated_c_is_read_for_python_work_and_the_directives(tmp_path):
    """C3 on written C: a projection formula's Python-object locals, its builtins but an
    exception and the containers it builds are faults, a report's are not, and a
    translated module must open with both of the tool's directives, in any order."""
    from sec_support import Build, c_faults
    package = tmp_path / "pkg"
    package.mkdir()
    (package / "_mx_classes.c").write_text(_C_SOURCE, encoding="utf-8")
    module = package / "_mx_classes.py"
    module.write_text("# cython: cpow=True, infer_types=True\nimport x\n",
                      encoding="utf-8")
    build = Build("Synthetic", tmp_path, package, "")
    found = c_faults(build, reporting={"result_cf"})
    assert found == [
        "Projection.g calls the Python builtin round (R12, R16)",
        "Projection.h calls the Python builtin sum (R12, R16)",
        "Projection.h builds a Python list, dict or set (PyList_New) (R10, R12)",
        "Projection.k builds a Python list, dict or set (__Pyx_PyDict_NewPresized) "
        "(R10, R12)",
        "Projection.e keeps Python objects in its C locals: n, rate"]
    # The registry's "python_calls" admits a builtin in its cell alone: round in g, which
    # leaves h's sum a fault; and round admitted in h admits nothing there.
    admitted = c_faults(build, reporting={"result_cf"}, python_calls={"g": ("round",)})
    assert admitted == found[1:], admitted
    assert c_faults(build, reporting={"result_cf"}, python_calls={"h": ("round",)}) == found
    for first, missing in (("# cython: infer_types=True", "cpow=True"),
                           ("# cython: infer_types=True, cpow=False", "cpow=True"),
                           ("import x", "infer_types=True, cpow=True")):
        module.write_text(f"{first}\nimport x\n", encoding="utf-8")
        assert c_faults(build, reporting={"result_cf", "e", "g", "h", "k"}) == [
            f"_mx_classes.py begins {first!r}, without {missing}: tools/build_sec_cy.py "
            f"puts them on its first line"]
    (package / "_mx_classes.c").write_text("int main(void) { return 0; }\n",
                                           encoding="utf-8")
    assert c_faults(build, reporting=set())[-1] == (
        "no Projection formula in _mx_classes.c: its layout has changed under this check")


# A model holding one of each construct C5 forbids, and the right way beside it.  ``label``
# is a reporting cell, and so may hold text; ``kw_target`` is called with a keyword.
STATIC_DATA = {
    "vec": "lambda: np.array([1.0, 2.0, 3.0])",
    "grid": "lambda: np.ones((2, 3))",
    "flags": "lambda: np.array([True, False])",
    "table": "lambda: pd.DataFrame({'x': [1.0]})",
    "count": "lambda: 3",
    "doubled": "lambda: vec() * 2",
    "picked": "lambda: np.array([vec()[0], grid()[1, 2]])",
}
STATIC_PROJECTION = {
    "fine": 'def fine(t):\n    """A docstring is text."""\n'
            '    if t < 0:\n        raise ValueError(f"no month {t}")\n'
            '    return float(data.vec()[t]) + data.grid()[0, t] + data.count()\n',
    "kw_target": "lambda t: 0.0",
    "uses_pd": "lambda t: pd.isna(t)",
    "uses_loc": "lambda t: data.table().loc[t, 'x']",
    "returns_text": "lambda t: 'LEVEL'",
    "generator": "lambda t: sum(x for x in range(t))",
    "keyword": "lambda t: kw_target(t=t)",
    "measures": "lambda t: len(data.vec())",
    "reads_label": "lambda t: label() == 'M'",
    "label": "lambda: 'M'",
    "flag": "lambda t: data.flags()[t]",
    "text_ref": "lambda t: 1.0 if mode == 0 else 0.0",
    "sliced": "lambda t: data.vec()[1:]",
    "half": "lambda t: data.grid()[t]",
    "nested": "def nested(t):\n    def inner():\n        return t\n    return inner()\n",
    "rounds": "lambda t: round(1.5 * t, 2)",
    "listed": "lambda t: [1.0, 2.0][t]",
    "keyed": "lambda t: {12: 1.0, 6: 0.5}[t]",
    "paired": "lambda t: (1.0, 2.0)[t] + abs(min(t, 1)) + max(float(t), 0.0)",
    "method": "lambda t: (1.5 * t).is_integer()",
    "uncached": "lambda t: 2.0 * t",
}

# The cells of STATIC_PROJECTION made uncached, as R14 once had float engine cells made.
STATIC_UNCACHED = ("uncached",)


def test_the_static_check_finds_what_a_compiled_cell_cannot_run():
    """C5 on a synthetic model: every forbidden construct a line, the allowed ones none."""
    from sec_support import static_faults
    model = mx.new_model(_name("static"))
    try:
        data = model.new_space("Data")
        data.np, data.pd = np, pd
        for name, formula in STATIC_DATA.items():
            data.new_cells(name, formula=formula)
        proj = model.new_space("Projection")
        proj.data, proj.pd, proj.mode = data, pd, "A"
        for name, formula in STATIC_PROJECTION.items():
            proj.new_cells(name, formula=formula)
        for name in STATIC_UNCACHED:
            proj.cells[name].is_cached = False
        found = static_faults(model, reporting={"label", "missing"})
    finally:
        model.close()
    expected = [
        "the registry's reporting names missing, which is not a Projection cell",
        "Projection.kw_target shares its name with what a call with keywords calls, at "
        "Projection.keyword, line 1",
        "Projection.uses_pd, line 1: refers to the module pd",
        "Projection.uses_loc, line 1: reads .loc",
        "Projection.uses_loc, line 1: holds the text 'x'",
        "Projection.uses_loc, line 1: reads data.table(), a pandas DataFrame",
        "Projection.returns_text, line 1: holds the text 'LEVEL'",
        "Projection.generator, line 1: holds a GeneratorExp",
        "Projection.generator, line 1: calls sum(), a call into Python",
        "Projection.measures, line 1: calls len()",
        "Projection.measures, line 1: uses data.vec() other than by one element",
        "Projection.reads_label, line 1: refers to the reporting cell label",
        "Projection.reads_label, line 1: holds the text 'M'",
        "Projection.flag, line 1: reads data.flags(), an array of bool",
        "Projection.text_ref, line 1: reads mode, a Reference holding text",
        "Projection.sliced, line 1: uses data.vec() other than by one element",
        "Projection.half, line 1: uses data.grid() other than by one element",
        "Projection.nested, line 2: holds a FunctionDef",
        "Projection.nested, line 4: calls inner(), a call into Python",
        "Projection.rounds, line 1: calls round(), a call into Python",
        "Projection.listed, line 1: builds a list, a Python object",
        "Projection.keyed, line 1: builds a dict, a Python object",
        "Projection.paired, line 1: builds a tuple, a Python object",
        "Projection.method, line 1: calls the method .is_integer(), a call into Python",
        "Projection.uncached is uncached: modelx-cython 0.1.0 traces only a cached cell's",
        "Data.doubled, line 1: uses vec() other than by one element",
    ]
    for line in expected:
        assert any(f.startswith(line) for f in found), (line, found)
    assert len(found) == len(expected), found
    assert not [f for f in found if f.startswith(("Projection.fine", "Projection.label",
                                                  "Data.picked"))]
    # The registry's "python_calls" admits a builtin in its cell alone: round in rounds,
    # which leaves generator's sum a fault; and round admitted elsewhere admits nothing.
    model = mx.new_model(_name("static"))
    try:
        data = model.new_space("Data")
        data.np, data.pd = np, pd
        for name, formula in STATIC_DATA.items():
            data.new_cells(name, formula=formula)
        proj = model.new_space("Projection")
        proj.data, proj.pd, proj.mode = data, pd, "A"
        for name, formula in STATIC_PROJECTION.items():
            proj.new_cells(name, formula=formula)
        for name in STATIC_UNCACHED:
            proj.cells[name].is_cached = False
        admitted = static_faults(model, reporting={"label", "missing"},
                                 python_calls={"rounds": ("round",)})
        elsewhere = static_faults(model, reporting={"label", "missing"},
                                  python_calls={"generator": ("round",)})
    finally:
        model.close()
    rounds = "Projection.rounds, line 1: calls round(), a call into Python"
    assert [f for f in found if not f.startswith(rounds)] == admitted, admitted
    assert any(f.startswith("Projection.generator, line 1: calls sum()") for f in admitted)
    assert elsewhere == found, elsewhere


def test_static_faults_admit_a_module_call_by_its_dotted_name():
    """``"python_calls"`` admits ``"math.erf"`` in its cell alone, wrapped in ``float``.

    ``RILA_US_SEC``'s pricing keeps Python's ``math`` (M25): C5 clears the module name
    only as the head of a call the cell's admission names, and only where that call is the
    one argument of a ``float(...)``, which keeps the cell's locals C.  A module attribute
    read but not called, ``math.inf``, stays a fault whatever is admitted, and so do an
    admitted call left unwrapped and a call admitted in another cell.
    """
    import math
    from sec_support import static_faults
    cells = {
        "erfs": "lambda t: float(math.erf(t / 2.0))",
        "logs": "lambda t: float(math.log(t + 1.0))",
        "infs": "lambda t: math.inf",
        "bare": "lambda t: math.erf(t / 2.0) + 1.0",
    }
    model = mx.new_model(_name("dotted"))
    try:
        data = model.new_space("Data")
        proj = model.new_space("Projection")
        proj.data, proj.math = data, math
        for name, formula in cells.items():
            proj.new_cells(name, formula=formula)

        def faults(admitted):
            return sorted(f.split(",")[0] for f in static_faults(
                model, reporting=set(), python_calls=admitted))

        everything = ["Projection.bare", "Projection.erfs", "Projection.infs",
                      "Projection.logs"]
        assert faults({}) == everything
        assert all(f.endswith("refers to the module math")
                   for f in static_faults(model, reporting=set()))
        assert faults({"erfs": ("math.erf",)}) == [
            "Projection.bare", "Projection.infs", "Projection.logs"]
        assert faults({"infs": ("math.inf",)}) == everything
        assert faults({"logs": ("math.erf",)}) == everything
        assert faults({"bare": ("math.erf",)}) == everything
        assert faults({"erfs": ("math.erf",), "logs": ("math.log",)}) == [
            "Projection.bare", "Projection.infs"]
    finally:
        model.close()


ENGINE_PROJECTION = {
    "model_point": "lambda: data.table()",
    "result_cf": "lambda: 0",
    "check_roll": "lambda: check_roll_resid(0) == 0.0",
    "check_roll_resid": "lambda t: 0.0",
    "statutory": "lambda rate: max(0.0015, math.floor(rate / 0.0005 + 0.5) * 0.0005)",
    "compliant": "lambda rate: 0.028 >= statutory(rate)",
    "monthly": "lambda t: 0.01 * t",
    "calls_engine": "lambda t: statutory(0.02) * t",
}


def test_the_registry_admits_engine_cells_by_name(monkeypatch):
    """``"engine"``: :func:`reporting_cells` admits the cells it names, so that C3 and C5
    pass a float-parameter cell of S's, ``math`` and all, and fault a compiled cell that
    calls one; one engine cell may call another.  Without the key, the same cells are
    faults.  And ``MYGA_US_SEC``, the first model to declare it, has its three admitted."""
    import us_registry
    from sec_support import reporting_cells, static_faults
    model = mx.new_model(_name("engine"))
    try:
        data = model.new_space("Data")
        data.new_cells("table", formula="lambda: 0")
        proj = model.new_space("Projection")
        proj.data, proj.math = data, math
        for name, formula in ENGINE_PROJECTION.items():
            proj.new_cells(name, formula=formula)
        base = {"twin": "Toy_US_S", "stage": "EC", "param": "idx"}
        monkeypatch.setitem(us_registry.MODELS, "Toy_US_SEC",
                            ("products/toy/Toy_US_SEC", base))
        plain = reporting_cells("Toy_US_SEC", proj)
        monkeypatch.setitem(us_registry.MODELS, "Toy_US_SEC",
                            ("products/toy/Toy_US_SEC",
                             {**base, "engine": ("compliant", "statutory")}))
        admitted = reporting_cells("Toy_US_SEC", proj)
        before = static_faults(model, reporting=plain)
        after = static_faults(model, reporting=admitted)
    finally:
        model.close()
    assert plain == {"model_point", "result_cf", "check_roll"}, plain
    assert admitted == plain | {"compliant", "statutory"}, admitted
    assert any(f.startswith("Projection.statutory, line 1: refers to the module math")
               for f in before), before
    assert not [f for f in after if f.startswith(("Projection.statutory",
                                                  "Projection.compliant"))], after
    assert after == ["Projection.calls_engine, line 1: refers to the reporting cell "
                     "statutory"], after
    sec = mx.read_model(model_path("MYGA_US_SEC"), name=_name("myga_engine"))
    try:
        cells = reporting_cells("MYGA_US_SEC", sec.Projection)
    finally:
        sec.close()
    assert {"mgsv_rate_statutory", "mgsv_rate_is_compliant",
            "mva_ref_term_years"} <= cells, cells


# Engine cells of each kind R14 admits, and of the kinds it does not (M24).
ENGINE_KINDS = {
    "statutory": "lambda rate: 0.0015 * rate",
    "flags": "lambda: [] if monthly(0) == 0.0 else ['breach']",
    "schedule": "lambda: {0: 100000.0, 60: 50000.0}",
    "frame": "lambda: data.table()",
    "level": "lambda: 0.5",
    "keyed": "lambda t: 0.01 * t",
    "monthly": "lambda t: 0.01 * t",
    "calls_engine": "lambda t: len(flags()) * t",
}


def test_the_benchmark_repeats_a_companion_keyed_by_point(tmp_path):
    """``tools/bench_sec_cy.py`` repeats a companion keyed by ``point_id`` with the table
    (C6, M24): each copy's rows under the label :func:`block_text` gives their point in
    that copy, matched by value and mapped by the point's position, not its label, on a
    table labelled 7 and 3 whose companion lists them the other way round, and with two
    rows for one point; and a companion naming no point of the table is refused.  It
    skips where the tool is absent, as from a ``lifelib.create()`` copy."""
    import importlib.util
    tool = model_path("DIA_US_SEC").parents[5] / "tools" / "bench_sec_cy.py"
    if not tool.is_file():
        pytest.skip("tools/bench_sec_cy.py is the source repository's, and it is absent")
    spec = importlib.util.spec_from_file_location("bench_sec_cy_harness", tool)
    bench = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bench)
    header, rows = ["point_id", "issue_age"], [["7", "60"], ["3", "65"]]
    (tmp_path / "model_point_table_sec.csv").write_text(
        "point_id,issue_age\n7,60\n3,65\n", encoding="utf-8")
    path = tmp_path / "premium_schedule_sec.csv"
    path.write_text("point_id,premium_mth,premium_amt\n3.0,0,10\n7,0,20\n3,12,30\n",
                    encoding="utf-8")
    assert bench.block_text(header, rows, 2) == ("point_id,issue_age\n1,60\n2,65\n"
                                                 "3,60\n4,65\n")
    assert bench.companions(tmp_path, "model_point_table_sec.csv") == [path]
    assert bench.companion_text(path, header, rows, 2) == (
        "point_id,premium_mth,premium_amt\n2,0,10\n1,0,20\n2,12,30\n4,0,10\n3,0,20\n"
        "4,12,30\n")
    path.write_text("point_id,premium_mth,premium_amt\n5,0,10\n", encoding="utf-8")
    with pytest.raises(ValueError, match=r"point_id \['5'\] is no point of the table"):
        bench.companion_text(path, header, rows, 1)


def test_an_engine_cell_takes_a_float_or_returns_a_container():
    """:func:`engine_faults`, the convention's check of ``"engine"`` (R14, precised at
    M24): a cell taking a parameter no spec size names is admitted, and so is one taking
    none that returns a list, a dict or a DataFrame, called on the space's first point,
    and may call a compiled cell; one taking none that returns a scalar, and one taking
    only sized parameters, compile to C and are faults; and a compiled cell calling an
    engine cell is a fault, whatever the engine cell returns."""
    from sec_support import engine_faults
    model = mx.new_model(_name("engine_kinds"))
    try:
        data = model.new_space("Data")
        data.new_cells("table", formula="lambda: pd.DataFrame({'premium_mth': [0, 60]})")
        data.pd = pd
        proj = model.new_space("Projection", formula="lambda idx: None")
        proj.data = data
        for name, formula in ENGINE_KINDS.items():
            proj.new_cells(name, formula=formula)
        found = engine_faults(proj, ("statutory", "flags", "schedule", "frame", "level",
                                     "keyed"), {"t"}, ())
        clean = engine_faults(proj, ("statutory", "flags", "schedule", "frame"), {"t"},
                              ("frame",))
    finally:
        model.close()
    assert found == [
        "level takes only parameters spec_sec.py sizes, (), so it compiles to C",
        "keyed takes only parameters spec_sec.py sizes, ('t',), so it compiles to C",
        "calls_engine calls the engine cell flags"], found
    assert clean == ["frame is a reporting cell too",
                     "calls_engine calls the engine cell flags"], clean


def test_the_compiled_comparison_keeps_kinds_and_floors_at_the_magnitude():
    """C4's comparison: a bool, an int and a real keep their kind, a real compares to
    1e-12 floored at the cell's magnitude, frames and Series by column and value, arrays
    exactly, and a raise only with the same raise."""
    from sec_support import _outcome_text, _value_text
    frame = pd.DataFrame({"pols_if": [1.0, 0.5], "net_cf": [-300.0, 12.5]},
                         index=pd.Index([0, 1], name="t"))
    row = pd.Series({"plan": "T10", "sum_assured": 250000.0, "override": float("nan")})
    agree = [(True, True), (np.bool_(False), False), (3, 3), (1.0, 1.0 + 5e-13),
             (0.0, 1e-13, 1.0), (float("nan"), float("nan")), ("M", "M"),
             (frame, frame.copy()), (row, row.copy()),
             (np.arange(3), np.arange(3)), (np.array([np.nan]), np.array([np.nan]))]
    for case in agree:
        scale = case[2] if len(case) > 2 else 0.0
        assert _value_text(case[0], case[1], scale) is None, case
    off = frame.copy()
    off.loc[1, "net_cf"] = 12.5 * (1 + 1e-9)
    differ = [(True, 1), (1, True), (3, 3.0), (3, 4), (1.0, 1.0 + 5e-12),
              (0.0, 1e-13, 0.0), (float("nan"), 0.0), ("M", "F"), (frame, off),
              (frame, frame.rename(columns={"net_cf": "net"})),
              (row, row.replace("T10", "T20")),
              (np.arange(3), np.arange(3.0)), (np.arange(3), np.arange(1, 4))]
    for case in differ:
        scale = case[2] if len(case) > 2 else 0.0
        assert _value_text(case[0], case[1], scale), case
    assert "column 'net_cf': 1 of 2 differ, first at 1" in _value_text(frame, off, 0.0)
    raised = ("raised", "ValueError: point_id 2: no rate at attained age 30")
    assert _outcome_text(raised, raised, 0.0) is None
    assert _outcome_text(raised, ("raised", "IndexError: Out of bounds"), 0.0) == (
        "modelx raised ValueError: point_id 2: no rate at attained age 30, compiled "
        "raised IndexError: Out of bounds")
    assert _outcome_text(("ok", 1.5), raised, 0.0) == (
        "modelx returned 1.5 (float), compiled raised ValueError: point_id 2: no rate at "
        "attained age 30")
    assert _outcome_text(("ok", frame), None, 0.0) == (
        "the compiled run returned nothing for it")
    nudged = frame.copy()
    nudged.loc[1, "net_cf"] = np.nextafter(12.5, 13.0)
    for want, have in ((1.0, 1.0 + 5e-13), (0.046900001716041806, 0.046900001716041792),
                       (frame, nudged)):
        assert _value_text(want, have, 0.0) is None
        assert _value_text(want, have, 0.0, rtol=0.0), (want, have)
    for same in ((1.0, 1.0), (float("nan"), float("nan")), (-0.0, 0.0), (frame, frame)):
        assert _value_text(*same, 0.0, rtol=0.0) is None


def test_c4_expects_what_also_calls_beyond_the_full_sweep():
    """``c4_expected`` takes what a product's ``also`` calls into C4's expectation (M17).

    The full sweep reaches a cell of a timing only at the keys a swept cell asks of it, so
    a timing no formula passes is compared only where ``also`` calls it; and a point whose
    ``proj_len()`` raises is not given to ``also``, whose loops it bounds.
    """
    from sec_support import c4_expected
    model = mx.new_model(_name("also"))
    try:
        proj = model.new_space("Projection")
        proj.new_cells("proj_len", formula="lambda: 2")
        proj.new_cells("at", formula="lambda t, timing: 1.0 * t + timing")
        proj.new_cells("flow", formula="lambda t: at(t, 0)")
        swept = c4_expected(proj)
        also = c4_expected(proj, also=lambda p: [p.at(t, 5) for t in range(3)])
        proj.cells["proj_len"].formula = "lambda: undefined_name"
        called = []
        c4_expected(proj, also=called.append)
    finally:
        model.close()
    assert sorted(args for name, args in swept if name == "at") == [(0, 0), (1, 0), (2, 0)]
    assert sorted(args for name, args in also if name == "at") == [
        (0, 0), (0, 5), (1, 0), (1, 5), (2, 0), (2, 5)]
    assert also[("at", (2, 5))] == ("ok", 7.0)
    assert called == []


def test_vul_maps_s_ids_and_totals_onto_its_positions_and_total_cells():
    """``_vul_twin_args`` maps ``VUL_US_S``'s keys as ``VUL_US_SEC`` takes them (R9, R12).

    S's totals, ``claims(t, None)`` and ``me_charge_pp(t, None)``, are SEC's one-argument
    totals, and its kind and subaccount keys of those two are skipped; a subaccount id,
    first or second among a cell's arguments, is its position in the shipped lineup; and
    any other cell's arguments pass as they are.
    """
    from sec_support import _vul_twin_args
    assert _vul_twin_args("claims", (5, None)) == (5,)
    assert _vul_twin_args("claims", (5, "DEATH")) is None
    assert _vul_twin_args("me_charge_pp", (5, None)) == (5,)
    assert _vul_twin_args("me_charge_pp", (5, 2)) is None
    assert _vul_twin_args("alloc", (2,)) == (1,)
    assert _vul_twin_args("scenario_last_mth", (1,)) == (0,)
    assert _vul_twin_args("sa_pp_at", (5, 2, "BEF_PREM")) == (5, 1, "BEF_PREM")
    assert _vul_twin_args("sa_pricing_pp", (7, 1)) == (7, 0)
    assert _vul_twin_args("av_pp_at", (5, "BEF_PREM")) == (5, "BEF_PREM")
    assert _vul_twin_args("net_cf", (5,)) == (5,)


def test_the_full_sweep_reaches_every_cell_and_every_month_and_keeps_the_raises():
    """``full_sweep`` evaluates every cell without parameters and every monthly cell at
    ``t = 0 .. proj_len()``, what they reach with them, and records each raise."""
    from sec_support import _cached_values, full_sweep
    model = mx.new_model(_name("sweep"))
    try:
        proj = model.new_space("Projection")
        proj.new_cells("proj_len", formula="lambda: 3")
        proj.new_cells("rate", formula="lambda t: 0.01 * t")
        proj.new_cells("count_at", formula="lambda t, timing: rate(t) + timing")
        proj.new_cells("count", formula="lambda t: count_at(t, 1)")
        proj.new_cells("strict", formula=(
            "def strict(t):\n    if t == 2:\n        raise ValueError('no month 2')\n"
            "    return 1.0\n"))
        raised = full_sweep(proj)
        cached = _cached_values(proj)
    finally:
        model.close()
    assert raised == {("strict", (2,)): "ValueError: no month 2"}
    assert sorted(args for name, args in cached if name == "count_at") == [
        (t, 1) for t in range(4)]
    assert sorted(args for name, args in cached if name == "strict") == [(0,), (1,), (3,)]
    assert cached[("rate", (3,))] == 0.03 and cached[("proj_len", ())] == 3


def test_spia_maps_s_claims_keys_onto_its_one_kind_and_passes_its_own():
    """``_spia_twin_args`` maps ``SPIA_US_S``'s two ``claims`` keys onto SEC's
    ``claims(t)``.

    S's ``(t, None)``, the total, and ``(t, "REFUND")``, the kind the total asks for, are
    both SEC's ``(t,)``, the one kind's formula; SEC's own ``(t,)``, as a comparison of SEC
    with SEC passes it, is unchanged, and so is every other cell's key.
    """
    from sec_support import _spia_twin_args
    assert _spia_twin_args("claims", (5, None)) == (5,)
    assert _spia_twin_args("claims", (5, "REFUND")) == (5,)
    assert _spia_twin_args("claims", (5,)) == (5,)
    assert _spia_twin_args("claim_pp", (5, "REFUND")) == (5, "REFUND")
    assert _spia_twin_args("pols_if_at", (5, "BEF_DECR")) == (5, "BEF_DECR")


def test_dia_maps_s_totals_onto_all_and_passes_its_kinds_and_its_own():
    """``_dia_twin_args`` maps ``DIA_US_S``'s totals onto SEC's ``ALL`` and passes the rest.

    S's ``claims(t, None)`` and ``claims_ann(y, None)``, the totals, are ``(t, "ALL")`` and
    ``(y, "ALL")``, which ``codes`` then turns into SEC's int; S's kinds, SEC's own int
    codes, as a comparison of SEC with SEC passes them, and every other cell's key, a
    ``None`` among them, pass as they are.
    """
    from sec_support import _dia_twin_args
    assert _dia_twin_args("claims", (5, None)) == (5, "ALL")
    assert _dia_twin_args("claims_ann", (3, None)) == (3, "ALL")
    assert _dia_twin_args("claims", (5, "REFUND")) == (5, "REFUND")
    assert _dia_twin_args("claims_ann", (3, 2)) == (3, 2)
    assert _dia_twin_args("claim_pp", (5, None)) == (5, None)
    assert _dia_twin_args("pols_if_at", (5, "BEF_DECR")) == (5, "BEF_DECR")


# A table of two points for the label check, a blank among its labels.
LABEL_TABLE = pd.DataFrame(
    {"form": ["life_only", "cash_refund"], "timing": ["arrears", "advance"],
     "primary_sex": ["M", "F"], "joint_sex": ["F", float("nan")],
     "income_form": ["LO_ROP", "JS"], "sex": ["M", "F"]},
    index=pd.Index([7, 9], name="point_id"))


def _label_model(labels):
    """A model indexed by ``idx`` over :data:`LABEL_TABLE`, its label cells ``labels``."""
    model = mx.new_model(_name("labels"))
    data = model.new_space("Data")
    data.table = LABEL_TABLE
    data.new_cells("model_point_table", formula="lambda: table")
    proj = model.new_space("Projection", formula=lambda idx: None)
    proj.data = data
    proj.new_cells("model_point", formula="lambda: data.model_point_table().iloc[idx]")
    for name, formula in labels.items():
        proj.new_cells(name, formula=formula)
    return model


def test_the_label_check_holds_each_shape_of_reporting_columns():
    """``label_faults`` checks a label against the column ``"reporting_columns"`` names.

    In each of the three shapes: a column, for ``payment_timing``, which returns
    ``timing``; a dict of argument to column, for ``sex(life)``, whose second life is
    blank on one point, NaN against NaN; and a pair of a column and a dict of value to
    label, for ``payout_form``, which reads ``income_form`` with ``LO_ROP`` as ``LO``.  Each
    passes as written and fails, a line a point, where the label returns another column;
    a label taking an argument called without a dict entry is a line, not a
    ``TypeError``; text where the column is blank is a fault; and an entry the label
    does not need, its own column being what it returns, is stale.
    """
    from sec_support import label_faults
    good = {
        "form": 'lambda: model_point()["form"]',
        "payment_timing": 'lambda: model_point()["timing"]',
        "sex": 'lambda life: model_point()["primary_sex" if life == 1 else "joint_sex"]',
        "payout_form": ('lambda: {"LO_ROP": "LO"}.get(model_point()["income_form"], '
                        'model_point()["income_form"])')}
    entry = {"stage": "EC", "reporting": tuple(good),
             "reporting_columns": {"payment_timing": "timing",
                                   "sex": {1: "primary_sex", 2: "joint_sex"},
                                   "payout_form": ("income_form", {"LO_ROP": "LO"})}}
    model = _label_model(good)
    try:
        assert label_faults(model, "SPIA_US_SEC", entry) == []
    finally:
        model.close()
    wrong = {**good,
             "payment_timing": 'lambda: model_point()["form"]',
             "sex": 'lambda life: model_point()["primary_sex"] if life == 1 else "F"',
             "payout_form": 'lambda: model_point()["income_form"]'}
    model = _label_model(wrong)
    try:
        found = label_faults(model, "SPIA_US_SEC", entry)
        bare = label_faults(model, "SPIA_US_SEC",
                            {**entry, "reporting_columns": {"payment_timing": "timing"}})
        stale = label_faults(model, "SPIA_US_SEC",
                             {**entry, "reporting": ("form",),
                              "reporting_columns": {"form": "form"}})
    finally:
        model.close()
    assert sorted(f.split(" returns ")[0] + " " + f.split(" at point ")[1].split(",")[0]
                  for f in found if " returns " in f) == [
        "Projection.payment_timing() 7", "Projection.payment_timing() 9",
        "Projection.payout_form() 7", "Projection.sex(2) 9"], found
    assert len(found) == 4, found
    assert any(f.startswith("Projection.sex() raised TypeError") for f in bare), bare
    assert stale == ["reporting_columns['form'] is stale: form() returns its own 'form' "
                     "column on every point, its default without the entry"], stale


@pytest.mark.parametrize("columns, fault", [
    ({"payment_timing": "timing"}, None),
    ({"sex": {1: "primary_sex", 2: "joint_sex"}}, None),
    ({"payout_form": ("income_form", {"LO_ROP": "LO"})}, None),
    ({"timing": "timing"}, "which reporting does not"),
    ({"sex": {}}, "not a non-empty dict of argument to column"),
    ({"payout_form": ("income_form", {})}, "neither a column"),
    ({"payout_form": ["income_form"]}, "neither a column"),
    ({}, "not a non-empty dict of labels"),
])
def test_reporting_columns_takes_three_shapes_of_a_declared_label(columns, fault):
    """``reporting_columns_faults`` admits a column, a dict of argument to column and a
    pair of a column and a dict, each for a label ``"reporting"`` names, at stage EC."""
    from sec_support import reporting_columns_faults
    entry = {"stage": "EC", "reporting": ("payment_timing", "sex", "payout_form"),
             "reporting_columns": columns}
    found = reporting_columns_faults(entry)
    if fault is None:
        assert found == []
    else:
        assert len(found) == 1 and fault in found[0], found
    assert "belongs to stage 'EC'" in reporting_columns_faults(
        {"stage": "E", "reporting_columns": {"payment_timing": "timing"}})[0]


# A compiled model's Projection as mx2cy declares it where a label was traced on text
# alone: sex returns str and rate_class unicode, where plan and the reports return object;
# mode stayed a Python method; check_roll returns a bint and statutory, an engine cell, a
# double, as each may.
LABEL_PXD = """\
cdef class _c_Projection(_mx_sys.BaseSpace):

    cdef object _v_model_point
    cdef object _v_sex

    cpdef object model_point(_c_Projection self)
    cpdef str sex(_c_Projection self)
    cpdef object plan(_c_Projection self)
    cpdef unicode rate_class(_c_Projection self)
    cpdef bint check_roll(_c_Projection self)
    cpdef double statutory(_c_Projection self, double rate)
    cpdef object result_cf(_c_Projection self)
    cpdef double premium(_c_Projection self, long long t)
"""


def test_a_reporting_cell_compiled_to_text_is_a_fault(monkeypatch, tmp_path):
    """C3 of the reporting cells (M22): :func:`object_cells` takes ``model_point``, the
    reports and the registry's labels, and :func:`object_return_faults` faults each the
    declarations type other than ``object``, ``str`` and ``unicode`` alike, but a label
    it is told refuses what is not text; a label left a Python method, a check's
    ``bint``, an engine cell's ``double`` and a compiled cell's are no fault of it."""
    import us_registry
    from sec_support import Build, object_cells, object_return_faults
    model = mx.new_model(_name("labels"))
    try:
        proj = model.new_space("Projection")
        for name in ("model_point", "sex", "plan", "rate_class", "mode", "check_roll",
                     "result_cf"):
            proj.new_cells(name, formula="lambda: 0")
        proj.new_cells("statutory", formula="lambda rate: rate")
        proj.new_cells("premium", formula="lambda t: 0.0")
        monkeypatch.setitem(us_registry.MODELS, "Toy_US_SEC", (
            "products/toy/Toy_US_SEC",
            {"twin": "Toy_US_S", "stage": "EC", "param": "idx",
             "reporting": ("sex", "plan", "rate_class", "mode"),
             "engine": ("statutory",)}))
        cells = object_cells("Toy_US_SEC", proj)
    finally:
        model.close()
    assert cells == {"model_point", "sex", "plan", "rate_class", "mode", "result_cf"}
    build = Build("Toy_US_SEC", tmp_path, tmp_path / "pkg", LABEL_PXD)
    found = object_return_faults(build, cells)
    assert [line.split(",")[0] for line in found] == [
        "Projection.rate_class returns unicode", "Projection.sex returns str"], found
    assert object_return_faults(build, cells - {"rate_class", "sex"}) == []
    assert [line.split(",")[0] for line in object_return_faults(
        build, cells, refusing={"rate_class"})] == ["Projection.sex returns str"]


def test_a_label_refusing_what_is_not_text_may_compile_to_text():
    """:func:`labels_refusing_non_text` (M22, precised at M26): a label whose own formula
    refuses its column blank and as a number returns text or raises, so it may compile to
    ``str``: ``SPIA_US_SEC``'s ``form`` and ``payment_timing`` validate theirs.  Its
    ``sex(life)`` returns the column as read, and is not refusing; nor is
    ``MYGA_US_SEC``'s ``sex``, which ``Data`` refuses as a number its mortality table
    does not key, and which returns the number where the table keys it."""
    from sec_support import labels_refusing_non_text
    assert labels_refusing_non_text("SPIA_US_SEC", {"form", "payment_timing", "sex"}) == {
        "form", "payment_timing"}
    assert labels_refusing_non_text("MYGA_US_SEC", {"sex"}) == set()


# Reads of a Data array at a negative literal index, which C5 refuses, and reads beside
# them that it passes: an index computed from t, a literal written as +1, - -1 or -0.
NEGATIVE_PROJECTION = {
    "last": "lambda t: data.vec()[-1]",
    "corner": "lambda t: data.grid()[0, -2] + data.grid()[t, 1]",
    "ending": "lambda t: data.grid()[1][-1.0]",
    "fine": "lambda t: data.vec()[t - 1] + data.vec()[+1] + data.vec()[- -1]"
            " + data.vec()[-0]",
}


def test_the_static_check_refuses_a_negative_literal_index():
    """C5 refuses ``data.x()[-1]`` in a projection formula (M23): Python and compiled
    Cython both wrap it to the array's end, so a read from the wrong end passes C4.  Each
    index of a 2-D read is held, a chained one included, and a computed index and a
    literal that is not negative pass."""
    from sec_support import static_faults
    model = mx.new_model(_name("negative"))
    try:
        data = model.new_space("Data")
        data.np = np
        data.new_cells("vec", formula="lambda: np.array([1.0, 2.0, 3.0])")
        data.new_cells("grid", formula="lambda: np.ones((2, 3))")
        proj = model.new_space("Projection")
        proj.data = data
        for name, formula in NEGATIVE_PROJECTION.items():
            proj.new_cells(name, formula=formula)
        found = static_faults(model, reporting=set())
    finally:
        model.close()
    assert found == [
        "Projection.last, line 1: reads data.vec() at the negative index -1, which wraps "
        "to the array's end in Python and in C alike",
        "Projection.corner, line 1: reads data.grid() at the negative index -2, which "
        "wraps to the array's end in Python and in C alike",
        "Projection.ending, line 1: reads data.grid() at the negative index -1.0, which "
        "wraps to the array's end in Python and in C alike"], found


ENGINE_SAMPLE = '''\
"""A sample's docstring names statutory(), which is no call."""
LABELS = ("sex", "plan")
NAMED = ("schedule", "plan")
FAMILIES = {"curve": ("A",), "pols_if_at": ("BEF_NB",)}
for idx in range(3):
    p = projection[idx]
    p.bs_call(100.0, 100.0, 1.0, 0.04, 0.02, 0.2)
    getattr(p, "norm_cdf")(0.0)
    for label in LABELS:
        getattr(p, label)()
    for name in NAMED:
        getattr(p, name)()
    for cell, labels in FAMILIES.items():
        getattr(p, cell)(0)
'''


def test_the_sample_check_finds_an_engine_cell_it_never_calls():
    """:func:`sample_engine_faults` (M25): an engine cell is called by attribute, by
    ``getattr`` with its name, or by ``getattr`` over a literal set of names, or a dict's
    keys, holding it; a name in the docstring or in a set no loop calls is no call.  A
    loop calling ``getattr(p, name)()`` over names the sample computes reaches a cell of
    no parameter alone, and only where the caller says the cell takes none."""
    from sec_support import sample_engine_faults
    engine = ("bs_call", "norm_cdf", "schedule", "curve", "statutory", "flags")
    found = sample_engine_faults(ENGINE_SAMPLE, engine, ("flags",))
    assert [line.split("(")[0] for line in found] == [
        "sample_sec.py calls no engine cell statutory",
        "sample_sec.py calls no engine cell flags"], found
    computed = ENGINE_SAMPLE + (
        "NOARG = sorted(n for n, params in cells.items() if not params)\n"
        "for name in NOARG:\n    getattr(p, name)()\n")
    found = sample_engine_faults(computed, engine, ("flags",))
    assert [line.split("(")[0] for line in found] == [
        "sample_sec.py calls no engine cell statutory"], found
    assert len(sample_engine_faults(computed, engine, ())) == 2
    argued = ENGINE_SAMPLE + "for name in NOARG:\n    getattr(p, name)(0.5)\n"
    assert len(sample_engine_faults(argued, engine, ("flags",))) == 2
    assert sample_engine_faults(ENGINE_SAMPLE, ()) == []


def _block_frames():
    """Three frames by ``t`` whose plain running sum at ``t = 0``, ``0.1 + 0.2 + 0.3``, is
    ``0.6000000000000001``, where ``groupby``'s compensated sum is ``0.6``."""
    return [pd.DataFrame({"net_cf": values, "pols_if": [1.0] * len(values)},
                         index=pd.RangeIndex(len(values), name="t"))
            for values in ([0.1, 1e16, 5.0], [0.2, 1.0], [0.3])]


def test_the_block_sum_check_holds_a_runner_to_groupby_bit_for_bit():
    """:func:`block_sum_faults` (M23): a runner's compensated ``add`` sums frames of
    unequal lengths to ``groupby``'s sum, bit for bit, and a plain running sum, which
    departs by an ulp, is a fault; so are a frame not finite, where ``groupby`` skips a
    NaN, and one not indexed from 0.  :func:`runner_add` reads ``add`` from a product's
    runner without running it."""
    from sec_support import block_sum_faults, runner_add

    def plain(total, compensation, frame):
        total[:len(frame)] += frame

    add = runner_add(model_path("Term_US_SEC").parent / "run_sec.py")
    assert block_sum_faults(add, _block_frames()) == []
    assert block_sum_faults(plain, _block_frames()) == [
        "the running sum departs from groupby's in 1 values, first net_cf at t = 0: "
        "0.6000000000000001, where groupby gives 0.6"]
    frames = _block_frames()
    frames[1].loc[1, "net_cf"] = np.nan
    assert block_sum_faults(add, frames) == [
        "frame 1 is not finite, where groupby skips a NaN"]
    frames = _block_frames()
    frames[2].index = pd.RangeIndex(1, 2, name="t")
    assert block_sum_faults(add, frames) == ["frame 2 is not indexed by t = 0, 1, ..."]
    assert block_sum_faults(add, []) == ["no frames to sum"]
