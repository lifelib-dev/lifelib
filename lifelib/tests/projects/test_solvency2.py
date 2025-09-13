import sys
import os.path
import pickle
import pathlib
import modelx as mx

import lifelib.projects.solvency2.model as solvency2
from lifelib.tests.data.generate_testdata_solvency2 import generate_data


datadir = pathlib.Path(__file__).parents[1].joinpath('data')
testdata = str(datadir.joinpath('data_solvency2'))
modelpath = pathlib.Path(solvency2.__file__).parent

def test_solvency2():
    model = mx.read_model(modelpath)
    data = generate_data(model)

    with open(testdata, 'rb') as file:
        data_saved = pickle.load(file)

    assert data == data_saved
    model.close()

