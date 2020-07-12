import sys
from lifelib.projects.simplelife.scripts import simplelife

if '' not in sys.path:
    sys.path.insert(0, '')

model = simplelife.build()


def run_simplelife():
    proj = model.Projection
    for i in range(10, 301, 10):
        print(i, proj(i).PV_NetCashflow(0))


if __name__ == '__main__':
    import timeit
    print(timeit.timeit('run_simplelife()', number=1, globals=globals()))
