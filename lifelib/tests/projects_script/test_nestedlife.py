import sys
import os.path
import pickle
import pathlib

import pytest

from lifelib.projects.nestedlife.scripts import nestedlife
from lifelib.tests.data.generate_testdata_nestedlife_v0 import (
    round_signif,
    get_nested,
    set_model,
    update_model)

if '' not in sys.path:
    sys.path.insert(0, '')


datadir = pathlib.Path(__file__).parents[1].joinpath('data')

testdata1 = str(datadir.joinpath('data_nestedlife1'))
testdata2 = str(datadir.joinpath('data_nestedlife2'))


@pytest.mark.parametrize("testdata, func",[
    [testdata1, set_model],
    [testdata2, update_model]
])
def test_nestedlife(testdata, func):
    model = nestedlife.build()

    data = get_nested(func(model), 'PolsSurr')

    with open(testdata, 'rb') as file:
        data_saved = pickle.load(file)

    assert data == data_saved
    model.close()


