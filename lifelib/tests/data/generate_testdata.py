import sys, os, pickle
from lifelib.projects.simplelife.scripts import simplelife
from lifelib.tests.data import round_signif

filepath = os.path.join(os.path.dirname(__file__), 'data_simplelife')

if '' not in sys.path:
    sys.path.insert(0, '')


def generate_data(model):
    data = []
    proj = model.Projection
    for i in range(10, 301, 10):
        data.append(round_signif(proj(i).PV_NetCashflow(0), 10))

    with open(filepath, 'wb') as file:
        pickle.dump(data, file, protocol=4)


if __name__ == '__main__':
    generate_data(simplelife.build())
