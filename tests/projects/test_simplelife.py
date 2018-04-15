import os.path
import math
import pickle
import pytest

from lifelib.projects.simplelife import simplelife
from .generate_testdata import round_signif

model = simplelife.build(load_saved=True)
filepath = os.path.join(os.path.dirname(__file__), 'data')

def test_simpleflie():
    data = []
    proj = model.Projection
    for i in range(10, 301, 10):
        data.append(round_signif(proj(i).pv_NetLiabilityCashflow(0), 10))

    with open(filepath, 'rb') as file:
        data_saved = pickle.load(file)

    assert data == data_saved


