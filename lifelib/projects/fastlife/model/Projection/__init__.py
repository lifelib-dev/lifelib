"""Space for cashflow projection.

This Space is for projecting cashflows of individual model points.
Most Cells in this Spaces are defined in its base Spaces,
:mod:`~simplelife.model.BaseProj` and :mod:`~simplelife.model.PV`.

This Space is parametrized with ``PolicyID`` and ``ScenID``,
and calling this space with a pair of integers returns the ItemSpace
for the policy ID and scenario ID.
``ScenID`` has a default value of 1,
so for example ``Projection[1]`` represents the Projection Space for Policy 1.
The present values of the cashflow items are also calculated in
the Space by the Cells inherited from the base Space :mod:`~simplelife.model.BaseProj`.

This Space has child Spaces,
:mod:`~simplelife.model.Projection.Policy` and :mod:`~simplelife.model.Projection.Assumptions`.
The :mod:`~simplelife.model.Projection.Policy` Space contains Cells representing policy attributes, such as
product type, issue age, sum assured, etc.
It also contains Cells for calculating policy values such as premium rates and
cash surrender value rates.
The :mod:`~simplelife.model.Projection.Assumptions` Space contains Cells to pick up assumption data for
its model point.

.. rubric:: Composition Structure

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     node_width=150;
     Proj[label="Projection
[PolicyID, ScenID=1]", stacked];
     Proj <- Assumptions [hstyle=composition];
     Proj <- Policy [hstyle=composition];
   }

.. rubric:: Inheritance Structure

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     BaseProj[style=dotted]
     BaseProj <- OuterProj [hstyle=generalization]
     PresentValue[style=dotted]
     PresentValue <- OuterProj [hstyle=generalization];
   }

.. rubric:: References

The following attributes are referenced in this Space by its base Spaces.

Attributes:
    pol: Alias for :mod:`~simplelife.model.Projection.Policy` child Space
    asmp: Alias for :mod:`~simplelife.model.Projection.Assumptions` child Space
    scen: Alias for :mod:`~simplelife.model.Economic` Space


"""

from modelx.serialize.jsonvalues import *

_formula = lambda PolicyID, ScenID=1: None

_bases = [
    ".BaseProj",
    ".PV"
]

_allow_none = None

_spaces = [
    "Policy",
    "Assumptions"
]

# ---------------------------------------------------------------------------
# Cells

def DiscRate(t):
    """Rates for discount cashflows

    Refers to :func:`Economic[ScenID].DiscRate<simplelife.model.Economic.DiscRate>`
    """
    return scen[ScenID].DiscRate(t)


def InflFactor(t):
    """Inflation factors to adjust expense cashflows

    Refers to :func:`Economic[ScenID].InflFactor<simplelife.model.Economic.InflFactor>`
    """
    return scen[ScenID].InflFactor(t)


def InvstRetRate(t):
    """Rate of investment return

    Refers to :func:`Economic[ScenID].InvstRetRate<simplelife.model.Economic.InvstRetRate>`
    """
    return scen[ScenID].InvstRetRate(t)


def PolsDeath(t):
    """Number of policies: Death"""


    return PolsIF_Beg1(t) * BaseMortRate(t) * asmp.MortFactor(t)


def PolsIF_End(t):
    """Number of policies: End of period"""
    if t == 0:
        return 0 # pol.PolicyCount()
    else:
        return PolsIF_Beg1(t-1) - PolsDeath(t-1) - PolsSurr(t-1)


def PolsMaturity(t):
    """Number of policies: Maturity"""

    return (pol.PolicyTerm == t) * PolsIF_End(t)


def PolsNewBiz(t):
    """Number of policies: New business"""
    return pol.PolicyCount() if t == 0 else 0


def BaseMortRate(t):
    """Bae mortality rate"""

    keys = pd.concat([asmp.MortTableID(), pol.Sex(), AttAge(t)],
                      axis=1, keys=["ID", "Sex", "Age"])

    exist = (t <= last_t())

    keys_exist = keys[exist]
    keys_non_exist = keys[~exist]


    result = keys_exist.apply(
            lambda key: asmp.MortalityTables[key["ID"], key["Sex"]][key["Age"]], axis=1)


    result = pd.concat([result, pd.Series(0, index=keys_non_exist.index)])
    result.name = "BaseMortRate"

    return result


def SizePremium(t):
    """Premium income per policy from t to t+1"""
    return SizeSumAssured(t) * pol.GrossPremRate() * pol.PremFreq()


def SizeSumAssured(t):
    """Sum assured per policy at time ``t``"""
    return  pol.SumAssured()


def PV_PremIncome(t):
    """Present value of premium income"""

    exist = (t <= last_t())

    if not exist.any():
        return 0
    else:
        result = exist * PremIncome(t) + PV_PremIncome(t+1) / (1 + DiscRate(t))
        result.name = "PV_PremIncome"
        return result


def last_t():

    result = np.minimum(asmp.LastAge() - pol.IssueAge(), pol.PolicyTerm())
    result.name = "last_t"

    return result


def SizeExpsCommInit(t):
    """Initial commission per policy at time t"""
    if t == 0:
        return SizePremium(t) * asmp.CommInitPrem() * (1 + asmp.CnsmpTax)
    else:
        return 0


def PV_BenefitTotal(t):
    """Present value of total benefits"""

    exist = (t <= last_t())

    if not exist.any():
        return 0
    else:
        result = (-BenefitTotal(t) + PV_BenefitTotal(t+1)) / (1 + DiscRate(t))
        result.name = "PV_BenefitTotal"
        return result


# ---------------------------------------------------------------------------
# References

pol = ("Interface", (".", "Policy"), "auto")

asmp = ("Interface", (".", "Assumptions"), "auto")

scen = ("Interface", ("..", "Economic"), "auto")

ScenID = 1