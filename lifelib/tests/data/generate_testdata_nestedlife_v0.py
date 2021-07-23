import sys, os, pickle
from lifelib.tests.data.generate_testdata import round_signif
from lifelib.projects.nestedlife.scripts import nestedlife

import numpy as np

if '' not in sys.path:
    sys.path.insert(0, '')

# %% Code block for overriding the default model

def SurrRateMult(t):
    if t == 0:
        return 1
    else:
        return SurrRateMult(t-1)


def PolsSurr(t):
    """Number of policies: Surrender"""
    return PolsIF_Beg1(t) * asmp.SurrRate(t) * SurrRateMult(t)


def PolsIF_End_inner(t):
    """Number of policies: End of period"""
    if t == t0:
        return outer.PolsIF_End(t)
    else:
        return PolsIF_Beg1(t-1) - PolsDeath(t-1) - PolsSurr(t-1)


def set_model(model):
    # Policy point ID and aliases
    polid = 171
    outer = model.OuterProj

    model.BaseProj.new_cells(formula=SurrRateMult)
    model.BaseProj.PolsSurr.set_formula(PolsSurr)
    model.OuterProj.InnerProj.PolsIF_End.set_formula(PolsIF_End_inner)

    outer[polid].SurrRateMult[1] = 2
    outer[polid].SurrRateMult[2] = 0.5
    outer[polid].SurrRateMult[3] = 1

    inner = outer[polid].InnerProj

    inner[1].SurrRateMult[1] = 2
    inner[2].SurrRateMult[2] = 0.5
    inner[3].SurrRateMult[3] = 1

    return outer[polid]


def update_model(model):

    polid = 171
    outer = model.OuterProj

    outer[polid].SurrRateMult[1] = 0.5
    outer[polid].SurrRateMult[2] = 2
    outer[polid].SurrRateMult[3] = 1

    inner = outer[polid].InnerProj

    inner[1].SurrRateMult[1] = 0.5
    inner[2].SurrRateMult[2] = 2
    inner[3].SurrRateMult[3] = 1

    return outer[polid]


def get_nested(outer, item):

    cells = outer.cells[item]

    act = [cells[t] for t in range(50)]
    expect = []

    for t0 in range(0, 6):
        expect_t0 = [np.nan] * 50
        for t in range(0, 50):
            if t < t0:
                expect_t0[t] = 0
            else:
                cells = outer.InnerProj[t0].cells[item]
                expect_t0[t] = cells[t]

        expect.append(expect_t0)

    act = [round_signif(val, 10) for val in act]
    expect = [[round_signif(val, 10) for val in inner] for inner in expect]

    return [act, expect]


def save_data(outer, filename):

    data = get_nested(outer, 'PolsSurr')
    filepath = os.path.join(os.path.dirname(__file__), filename)

    with open(filepath, 'wb') as file:
        pickle.dump(data, file, protocol=4)


def generate_data(model):
    save_data(set_model(model), 'data_nestedlife1')
    save_data(update_model(model), 'data_nestedlife2')


if __name__ == '__main__':
    generate_data(model = nestedlife.build(True))




