import modelx as mx
import lifelib.projects.simplelife.model



import pathlib

model_path = pathlib.Path(lifelib.projects.simplelife.model.__file__).parent


model = mx.read_model(model_path)


def run_newlife():
    proj = model.Projection
    for i in range(10, 301, 10):
        print(i, proj(i).PV_NetCashflow(0))


if __name__ == '__main__':
    import timeit
    print(timeit.timeit('run_newlife()', number=1, globals=globals()))
