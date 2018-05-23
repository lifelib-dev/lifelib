import sys
import os.path
import pickle
import pathlib

from lifelib.projects.nestedlife import nestedlife
from tests.data.generate_testdata_nestedlife import (
    round_signif,
    get_nested,
    set_model,
    update_model)

if '' not in sys.path:
    sys.path.insert(0, '')


datadir = pathlib.Path(__file__).parents[1].joinpath('data')

testdata1 = str(datadir.joinpath('data_nestedlife1'))
testdata2 = str(datadir.joinpath('data_nestedlife2'))


def test_nestedlife():
    model = nestedlife.build(load_saved=False)

    for testdata, func in zip([testdata1, testdata2],
                          [set_model, update_model]):

        data = get_nested(func(model), 'nop_Surrender')

        with open(testdata, 'rb') as file:
            data_saved = pickle.load(file)

        assert data == data_saved


