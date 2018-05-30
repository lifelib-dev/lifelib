"""Source module to create ``Economic`` space from.

.. rubric:: Project Templates

This module is included in the following project templates.

* :mod:`simplelife`
* :mod:`nestedlife`

References:
    Scenario

"""

def InflFac(t):
    if t == 0:
        return 1
    else:
        return InflFac(t - 1) / (1 + asmp.InflRate)

def DiscRate(t):
    return Scenario.IntRate(t)

def InvRetRate(t):
    return Scenario.IntRate(t)
