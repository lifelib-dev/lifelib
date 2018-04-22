from lifelib.projects.simplelife import simplelife

model = simplelife.build(load_saved=True)


def run_simplelife():
    proj = model.Projection
    for i in range(10, 301, 10):
        print(i, proj(i).pv_NetLiabilityCashflow(0))


if __name__ == '__main__':
    import timeit
    print(timeit.timeit('run_simplelife()', number=1, globals=globals()))
