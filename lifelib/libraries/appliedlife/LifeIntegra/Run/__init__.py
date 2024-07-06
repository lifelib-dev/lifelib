"""Projection runs

The Run space represents projection runs.
This space serves as the base space for its dynamic sub spaces.
and it is parameterized with run_id.

Both parameters are string IDs, indicating what date and sensitivity
combination should be used for each dynamic instance of this space.

.. rubric:: Parameters

Attributes:

    run_id: an integer key representing the run identity


"""

from modelx.serialize.jsonvalues import *

_formula = lambda run_id: None

_bases = []

_allow_none = None

_spaces = [
    "GMXB",
    "GLWB"
]

# ---------------------------------------------------------------------------
# References

run_id = 1