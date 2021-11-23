from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def result():

    data = {sim: Proj[sim].monte_carlo() for sim in range(1, 6)}
    return pd.concat(data, names=["sim_id", "point_id"])


# ---------------------------------------------------------------------------
# References

Proj = ("Interface", ("..", "Projection"), "auto")

pd = ("Module", "pandas")