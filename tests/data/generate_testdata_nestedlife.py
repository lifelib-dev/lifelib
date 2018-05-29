import sys, os, pickle
from tests.data.generate_testdata import round_signif
from lifelib.projects.nestedlife import nestedlife

import numpy as np

if '' not in sys.path:
    sys.path.insert(0, '')

# %% Code block for overriding the default model

def SurrRateMult(t):
    if t == 0:
        return 1
    else:
        return SurrRateMult(t - 1)


def nop_Surrender(t):
    """Number of policies: Surrender"""
    return nop_BoP1(t) * asmp.SurrRate(t) * SurrRateMult(t)


def nop_EoP_inner(t):
    """Number of policies: End of period"""
    if t == t0:
        return outer.nop_EoP(t)
    else:
        return nop_BoP1(t - 1) - nop_Death(t - 1) - nop_Surrender(t - 1)


def set_model(model):
    # Policy point ID and aliases
    polid = 171
    outer = model.OuterProjection[polid]
    inner = outer.InnerProjection

    model.BaseProjection.new_cells(formula=SurrRateMult)
    model.BaseProjection.new_cells(formula=nop_Surrender)
    inner.new_cells(name='nop_EoP', formula=nop_EoP_inner)

    outer.SurrRateMult[1] = 2
    outer.SurrRateMult[2] = 0.5
    outer.SurrRateMult[3] = 1

    inner[1].SurrRateMult[1] = 2
    inner[2].SurrRateMult[2] = 0.5
    inner[3].SurrRateMult[3] = 1

    return outer


def update_model(model):

    polid = 171
    outer = model.OuterProjection[polid]
    inner = outer.InnerProjection

    outer.SurrRateMult[1] = 0.5
    outer.SurrRateMult[2] = 2
    outer.SurrRateMult[3] = 1

    inner[1].SurrRateMult[1] = 0.5
    inner[2].SurrRateMult[2] = 2
    inner[3].SurrRateMult[3] = 1

    return outer


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
                cells = outer.InnerProjection[t0].cells[item]
                expect_t0[t] = cells[t]

        expect.append(expect_t0)

    act = [round_signif(val, 10) for val in act]
    expect = [[round_signif(val, 10) for val in inner] for inner in expect]

    return [act, expect]


def save_data(outer, filename):

    data = get_nested(outer, 'nop_Surrender')
    filepath = os.path.join(os.path.dirname(__file__), filename)

    with open(filepath, 'wb') as file:
        pickle.dump(data, file, protocol=4)


def generate_data(model):
    save_data(set_model(model), 'data_nestedlife1')
    save_data(update_model(model), 'data_nestedlife2')


if __name__ == '__main__':
    generate_data(model = nestedlife.build(True))




