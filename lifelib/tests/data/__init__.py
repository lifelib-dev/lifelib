import math

def round_signif(x, digit):
    if x == 0:
        return 0
    else:
        base = int(math.log10(abs(x)))
        return round(x, digit - base - 1)