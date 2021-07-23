import sys, os, pickle
from itertools import  product
from lifelib.projects.solvency2.scripts import solvency2
from lifelib.tests.data import round_signif

filepath = os.path.join(os.path.dirname(__file__), 'data_solvency2')

if '' not in sys.path:
    sys.path.insert(0, '')


def generate_data(model):
    data = []
    scr = model.SCR_life
    for t0, polid in product(range(0, 15, 5), (1, 101, 201)):
        data.append(round_signif(scr[t0, polid].SCR_life(), 10))
    return data


def save_date(data):
    with open(filepath, 'wb') as file:
        pickle.dump(data, file, protocol=4)


if __name__ == '__main__':
    save_date(generate_data(solvency2.build()))
