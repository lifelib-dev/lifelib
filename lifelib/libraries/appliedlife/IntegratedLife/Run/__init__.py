"""Projection runs

The :mod:`~appliedlife.IntegratedLife.Run` space represents projection runs.
This space is parameterized with :attr:`run_id`, and for each value
of :attr:`run_id`, a dynamic subspace is created,
representing a specific run associated to the :attr:`run_id`.

.. rubric:: Parameters

Attributes:

    run_id: an integer key representing the run identity


Example:

    The sample code below shows how to create ``Run[1]`` and
    examine its contents.

    .. code-block:: python

        >>> import modelx as mx

        >>> m = mx.read_model("IntegratedLife")

        >>> m.Run[1]
        <ItemSpace IntegratedLife.Run[1]>

        >>> m.Run[1].run_id
        1

        >>> m.Run[1].GMXB.run_id
        1

        >>> m.Run[1].GMXB.result_pv()

                         Premiums         Death  ...  Change in AV  Net Cashflow
        point_id scen                            ...
        1        1     50000000.0  4.535395e+06  ...  1.141797e+07  6.097680e+06
                 2     50000000.0  4.592794e+06  ...  1.244402e+07  6.732840e+06
                 3     50000000.0  4.514334e+06  ...  1.215701e+07  6.499784e+06
                 4     50000000.0  4.667772e+06  ...  1.250695e+07  6.648902e+06
                 5     50000000.0  4.403177e+06  ...  1.138434e+07  6.107113e+06
                          ...           ...  ...           ...           ...
        8        96    32500000.0  3.013149e+06  ...  5.651292e+06 -1.669267e+07
                 97    32500000.0  3.050556e+06  ...  8.690729e+06 -6.839240e+05
                 98    32500000.0  3.013149e+06  ...  3.701018e+06 -1.436214e+07
                 99    32500000.0  3.230455e+06  ...  8.484874e+06  1.174996e+06
                 100   32500000.0  3.013149e+06  ...  7.439794e+06 -1.503688e+06

        [800 rows x 9 columns]
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