import modelx as mx
import lifelib.projects.simplelife.model
import lifelib.projects.fastlife.model


import pathlib

simplepath = pathlib.Path(lifelib.projects.simplelife.model.__file__).parent
fastpath = pathlib.Path(lifelib.projects.fastlife.model.__file__).parent


def test_fastlife():

    simple = mx.read_model(simplepath)
    fast = mx.read_model(fastpath)

    simplesum = sum([simple.Projection[i].PV_NetCashflow(0) for i in range(1, 301)])
    fastsum = sum(fast.Projection.PV_NetCashflow(0))

    assert simplesum == fastsum
    simple.close()
    fast.close()
