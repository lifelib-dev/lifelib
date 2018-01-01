"""Source module to create "Economic" space from.

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

# Public Enum id_GlobalProjection
#
# gprj_EndOfScen          'Boolean
# gprj_InvRetRate         '(Year)
# gprj_InvRetRateM        '(Month)
# gprj_DiscRate           '(Year)
# gprj_DiscRateM          '(Month)
# gprj_DiscFac            '(Month)
# gprj_InflFac            '(Month)
# gprj_End = gprj_InflFac
#
# End Enum