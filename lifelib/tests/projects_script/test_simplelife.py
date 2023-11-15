import sys
import os.path
import pickle
import pathlib

from lifelib.projects.simplelife.scripts import simplelife
from lifelib.tests.data.generate_testdata import round_signif

if '' not in sys.path:
    sys.path.insert(0, '')

testdata = str(pathlib.Path(__file__).parents[1].joinpath('data/data_simplelife'))


def test_simpleflie():
    model = simplelife.build()
    data = []
    proj = model.Projection
    for i in range(10, 301, 10):
        data.append(round_signif(proj(i).PV_NetCashflow(0), 10))

    with open(testdata, 'rb') as file:
        data_saved = pickle.load(file)

    assert data == data_saved
    model.close()


