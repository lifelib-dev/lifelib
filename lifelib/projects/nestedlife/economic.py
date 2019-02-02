"""Source module to create ``Economic`` space from.

.. rubric:: Project Templates

This module is included in the following project templates.

* :mod:`simplelife`
* :mod:`nestedlife`

References:
    Scenario

"""

def InflFactor(t):
    if t == 0:
        return 1
    else:
        return InflFactor(t-1) / (1 + asmp.InflRate)

def DiscRate(t):
    return Scenario.IntRate(t)

def InvstRetRate(t):
    return Scenario.IntRate(t)
