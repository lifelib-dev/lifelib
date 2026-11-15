"""The cap on each S model's annual mortality rate, sent a NaN and taken past 1.

USLIB-SEC-PLAN.md §8.2 item 4 caps the annual mortality of the ten ``_S`` models whose rate
is a product of factors at the float 1.0, with its bound second, ``min(q, 1.0)``, as §5.1
step 6 writes it for the ``_SEC`` models.  ``min`` keeps its first argument unless a later
one compares smaller, and no comparison with NaN holds, so with its bound first the cap
reads a NaN, a missing factor, as 1, certain death with every flow finite; and bounded by
the int ``1`` it returns an int where the product passes it.  Where a shipped point's
product passes 1, in ``SPIA_US_S`` alone, at its terminal ages, either order gives 1.0,
and no shipped point sends a cap a NaN, so neither the S models' own modules nor the twin
identity can see how the cap is written, nor whether it is there, but for both of
``SPIA_US_S``'s caps at once: with either alone its rate is still 1.0.  The cap tests of
``DIA_US_SEC``, ``FIA_US_SEC``, ``IUL_US_SEC``, ``RILA_US_SEC``, ``Term_US_SEC``,
``UL_US_SEC``, ``ULSG_US_SEC``, ``VUL_US_SEC`` and ``WholeLife_US_SEC`` see their S
model's cap and its float bound, where the product passes 1, and ``SPIA_US_SEC``'s splice
sees ``SPIA_US_S``'s rating cap, on a point rated 1.25.  Of these ``IUL_US_SEC``'s,
``RILA_US_SEC``'s and ``ULSG_US_SEC``'s also see the order of an S model's cap, each
reading both models with ``mort_ae_factor`` a NaN, and ``VUL_US_SEC``'s NaN test sees
``VUL_US_S``'s, since it reads both models and sends the cap of each a NaN.

So each S model is read for the test, the product is fed a NaN and then a factor that takes
it past 1, through each name in :data:`MORT_CAP_FEEDS` in turn, and ``mort_rate`` and
``mort_rate_mth`` must be the float NaN, then the float 1.0.  An A/E factor is a Reference,
set on ``Projection``; a class factor or a rating is cells, whose formula is replaced, as
modelx allows.  So that a factor left outside the cap fails the test, every factor of the
product is fed or differs from 1 at one of the reads, and so that a cap on one branch of the
product fails it, the reads take each branch: the class factor is fed wherever there is one,
1 on every shipped point; ``Term_US_S`` is read at ``t = 0``, in its level term, and at
``t = 120``, the first month after it, where M(1) is 3.5; ``ULSG_US_S`` at ``t = 12``, where
its improvement factor is 0.99; ``DIA_US_S`` on its first point, on the anchor basis, and on
point 16, its one point on the generational basis, where its improvement factor is 0.87; and
the others at ``t = 0`` of their first point.  ``SPIA_US_S`` caps twice, the A/E's product
and then the rating's, so it is fed at each: a NaN in its A/E factor reaches both caps, and
a rating fed a NaN or taken past 1 reaches the second alone.  One more test holds its first
cap where the second cannot bind.  Every S model registered is fed here or named in
:data:`NO_MORT_FACTOR`, so a model registered later must say which.  Each ``_SEC`` model's
own module sends its caps a NaN on its own rows (§5.1, step 6).
"""
import math

import modelx as mx
import pytest

from us_registry import MODELS, is_sec, model_path, point_keys, projection

#: S model -> (the names fed, each in turn, and the reads: each a point, ``None`` for the
#: first, and the arguments of ``mort_rate``).  The reads take each branch of the product,
#: and at one of them every factor of the product but the names fed differs from 1.
MORT_CAP_FEEDS = {
    "DIA_US_S": (("mort_ae_factor",), ((None, (0, 1)), (16, (0, 1)))),
    "FIA_US_S": (("mort_ae_factor",), ((None, (0,)),)),
    "IUL_US_S": (("mort_ae_factor", "class_factor"), ((None, (0,)),)),
    "RILA_US_S": (("mort_ae_factor",), ((None, (0,)),)),
    "SPIA_US_S": (("mort_ae_factor", "rating_factor"), ((None, (0, 1)),)),
    "Term_US_S": (("class_factor",), ((None, (0,)), (None, (120,)))),
    "UL_US_S": (("mort_ae_factor", "class_factor"), ((None, (0,)),)),
    "ULSG_US_S": (("mort_ae_factor", "class_factor"), ((None, (12,)),)),
    "VUL_US_S": (("mort_ae_factor", "class_factor"), ((None, (0,)),)),
    "WholeLife_US_S": (("ae_best_est",), ((None, (0,)),)),
}

#: The S models whose ``mort_rate`` is the table's rate with no factor, and so no cap.
NO_MORT_FACTOR = frozenset({"MYGA_US_S", "VA_US_S"})

CASES = [(name, feed) for name, (feeds, _) in sorted(MORT_CAP_FEEDS.items())
         for feed in feeds]


def _nan():
    """NaN, what a blank factor carries: the formula a test puts in place of a cell's.

    It names no global of this module: modelx runs a formula in the model's namespace.
    """
    return float("nan")


def _huge():
    """A factor that takes past 1 any rate above 1e-6, put in place of a cell's formula."""
    return 1e6


def _half():
    """A rating below 1, put in place of ``rating_factor``'s formula."""
    return 0.5


def _feed(model, feed, value, formula):
    """Set ``feed`` to ``value``, or, if it is cells, set its formula to ``formula``."""
    if feed in model.Projection.cells:
        model.Projection.cells[feed].formula = formula
    else:
        setattr(model.Projection, feed, value)


def _rates(name, feeds):
    """``mort_rate`` and ``mort_rate_mth`` at each read :data:`MORT_CAP_FEEDS` gives.

    The model is read for the test.  ``feeds`` is a sequence of ``(feed, value, formula)``,
    :func:`_feed`'s arguments after the model, applied in turn before any point is taken.
    """
    _, reads = MORT_CAP_FEEDS[name]
    model = mx.read_model(model_path(name), name=f"{name}_cap")
    try:
        for feed in feeds:
            _feed(model, *feed)
        first = point_keys(model)[0]
        rates = []
        for point, args in reads:
            proj = projection(model, first if point is None else point)
            rates += [proj.mort_rate(*args), proj.mort_rate_mth(*args)]
        return rates
    finally:
        model.close()


def test_every_s_model_is_fed_or_named_without_a_factor():
    """Each S model registered is fed below or named in ``NO_MORT_FACTOR``, not both."""
    s_models = {name for name in MODELS if not is_sec(name)}
    assert not NO_MORT_FACTOR & set(MORT_CAP_FEEDS)
    assert NO_MORT_FACTOR | set(MORT_CAP_FEEDS) == s_models


@pytest.mark.parametrize("name, feed", CASES)
def test_a_nan_that_reaches_the_cap_stays_nan(name, feed):
    """With a NaN fed to the product, each rate is the float NaN, not the cap's 1.0."""
    rates = _rates(name, [(feed, float("nan"), _nan)])
    assert [type(r) is float and math.isnan(r) for r in rates] == [True] * len(rates), rates


@pytest.mark.parametrize("name, feed", CASES)
def test_a_product_past_1_is_capped_at_the_float_1(name, feed):
    """With the product taken past 1, each rate is the float 1.0, and not the int 1."""
    rates = _rates(name, [(feed, 1e6, _huge)])
    assert [(type(r), r) for r in rates] == [(float, 1.0)] * len(rates)


def test_spia_caps_the_ae_product_before_the_rating():
    """``SPIA_US_S`` caps ``q_be``, the A/E's product, before the rating scales it.

    The notes' construction, ``q_be = min(1, AE * q_base)`` and then
    ``q_rated = min(1, theta * q_be)``: with the A/E's product taken past 1 and a rating of
    0.5, the rate is 0.5 exactly, where without the first cap the second would bind at 1.0.
    """
    rates = _rates("SPIA_US_S", [("mort_ae_factor", 1e6, None),
                                 ("rating_factor", 0.5, _half)])
    assert (type(rates[0]), rates[0]) == (float, 0.5)
