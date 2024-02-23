"""Source module for Life SCR standard formulas

This module contains formulas to calculate SCR.

.. rubric:: Common cells parameters


Attributes:
    risk: one of the following strings that represents a life sub-module.
        only Mortality, Longevity, Lapse and Life expense risks are
        implemented.

* "mort": Mortality risk
* "longev": Longevity risk
* "disab": Disability risk
* "lapse": Lapse risk
* "exps": Life expense risk
* "rev": Revision risk
* "cat": Life catastrophe risk

"""

from modelx.serialize.jsonvalues import *

def _formula(t0, PolicyID, ScenID=1):
    pass


_bases = []

_allow_none = None

_spaces = [
    "Projection"
]

# ---------------------------------------------------------------------------
# Cells

def LapseRisk(shock):
    """The capital requirement for lapse risk for each shock

    Args:
        shock: string that represents each lapse shock
            ("up", "down", "mass")
    """

    if shock in ['up', 'down']:
        return max(NetAstValue() - NetAstValue('lapse', shock), 0)

    elif shock == 'mass':

        retail_share = 1
        nonretail_share = 1 - retail_share

        retail = NetAstValue() - NetAstValue('lapse', shock) \
            if retail_share else 0

        nonretail = NetAstValue() - NetAstValue('lapse', shock, 'noretail') \
            if nonretail_share else 0

        return max(retail_share * retail + nonretail_share * nonretail, 0)

    else:
        raise ValueError("Unknown shock: %s" % shock)


def Life(risk):
    """The capital requirement for each risk under the life underwriting risk

    Args:
        risk: string that represents life risk sub-module ("mort",
            "longev", "disab", "lapse", "exps", "rev", "cat")
    """

    if risk == 'lapse':
        return max(LapseRisk(shock) for shock in ['up', 'down', 'mass'])    
    else:
        return max(NetAstValue() - NetAstValue(risk), 0)


def NetAstValue(risk='base', shock=None, scope=None):
    """Net value of assets minus liabilities

    This formula is simplified and present value of net
    liability cashflows is used in replacement for net asset value,
    based on the assumption that the value of assets
    does not change by life risk scenarios.

    Args:
        risk: string that represents life risk sub-module ("mort",
            "longev", "disab", "lapse", "exps", "rev", "cat")
        shock: string that represents each lapse shock
            ("up", "down", "mass")
        scope: "nonretail" or None (by default)

    """
    return Projection[risk, shock, scope].PV_NetCashflow(t0)


def SCR_life():
    r"""The capital requirement for life underwriting risk

    .. math::
        \sqrt{\sum_{i,j}Corr_{(i,j)}\cdot SCR_i\cdot SCR_j}

    where i, j are a combination of risks

    """
    return sum(Life(r) * Life(c) * Corr[r, c] for r, c in Corr) ** 0.5


# ---------------------------------------------------------------------------
# References

Corr = ("IOSpec", 1401497102096, 1401497102096)