import os, math, pickle
from lifelib.projects.simplelife import simplelife


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


if __name__ == '__main__':
    model = simplelife.build(load_saved=False)
    generate_data()