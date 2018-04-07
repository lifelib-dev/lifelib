import modelx as mx

try:
    import ifrs17sim.ifrs17sim as ifrs17sim
except ImportError:
    import ifrs17sim


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set()

    model, proj = ifrs17sim.build(True), mx.cur_model().OuterProjection[171]
    proj.CSM_Unfloored(10)
    proj.CSM_Unfloored.series.sort_index().plot()