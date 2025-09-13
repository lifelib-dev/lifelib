import sys
import os.path
import pickle
import pathlib
import modelx as mx

import lifelib.projects.simplelife.model as simplelife
from lifelib.tests.data.generate_testdata import round_signif

testdata = str(pathlib.Path(__file__).parents[1].joinpath('data/data_simplelife'))
modelpath = pathlib.Path(simplelife.__file__).parent


def test_simpleflie():
    model = mx.read_model(modelpath)
    data = []
    proj = model.Projection
    for i in range(10, 301, 10):
        data.append(round_signif(proj(i).PV_NetCashflow(0), 10))

    with open(testdata, 'rb') as file:
        data_saved = pickle.load(file)

    assert data == data_saved
    model.close()


