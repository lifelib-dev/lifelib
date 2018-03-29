import os.path
import math
import pickle
import pytest

from lifelib.projects.simplelife import simplelife

model = simplelife.build(load_saved=True)
filepath = os.path.join(os.path.dirname(__file__), 'data')


def round_signif(x, digit):
    if x == 0:
        return 0
    else:
        base = int(math.log10(abs(x)))
        return round(x, digit - base - 1)


def generate_data():
    data = []
    proj = model.Projection
    for i in range(10, 301, 10):
        data.append(round_signif(proj(i).pv_NetLiabilityCashflow(0), 10))

    with open(filepath, 'wb') as file:
        pickle.dump(data, file, protocol=4)


def test_simpleflie():
    data = []
    proj = model.Projection
    for i in range(10, 301, 10):
        data.append(round_signif(proj(i).pv_NetLiabilityCashflow(0), 10))

    with open(filepath, 'rb') as file:
        data_saved = pickle.load(file)

    assert data == data_saved


