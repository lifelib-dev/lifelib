"""
:mod:`ifrs17sim` CSM waterfall chars
====================================

Draw a graph of CSM amortization pattern.
"""
import math
import collections
import pandas as pd
import seaborn as sns
sns.set()


def draw_waterfall(df, ax=None):
    """Draw waterfall chart"""
    data = df.stack()
    bottom = df.cumsum(axis=1).shift(1, axis=1).fillna(0).stack()
    flowvals= set(df.iloc[:, 1:].stack())
    colors = CustomColorMap(flowvals)
    xlabel = [idx[1] + '(' + str(idx[0]) + ')' for idx in df.stack().index]
    ax = sns.barplot(data=data, bottom=bottom,
                     palette=colors.get_palette(data),
                     ax=ax)
    ax.set_xticklabels(labels=xlabel, rotation='vertical')
    ax.get_figure().tight_layout()
    return ax


class CustomColorMap:
    """Change color by size and sign"""

    def __init__(self, data):

        self.pallen = 20
        self.palette = pal = sns.color_palette("RdBu", self.pallen)

        self.posmax = max([val for val in data if val >= 0] or [0])
        self.negmin = min([val for val in data if val < 0] or [0])

    def get_index(self, value):

        if value > self.posmax:
            return self.pallen - 1
        elif value < self.negmin:
            return 0
        else:
            absmax = self.posmax if value >= 0 else abs(self.negmin)

            idx0 = self.pallen / 2
            return min(idx0 + math.floor(idx0 * value / absmax),
                       self.pallen - 1)

    def get_palette(self, data):
        idxs = [int(self.get_index(val)) for val in data]
        return [self.palette[i] for i in idxs]


if __name__ == '__main__':
    from lifelib.projects.ifrs17sim import ifrs17sim

    model = ifrs17sim.build(True)
    proj = model.OuterProjection[1]
    liab = [proj.InnerProjection[t].pv_NetLiabilityCashflow[t] for t in
            range(10)]

    proj.CSM_Unfloored(15)
    data = collections.OrderedDict()

    for cells in ['CSM_Unfloored',
                  'IntAccrCSM',
                  'AdjCSM_FulCashFlows',
                  'TransServices']:
        data[cells] = [proj.cells[cells](t) for t in range(15)]

    df = pd.DataFrame(data)
    df['TransServices'] = -1 * df['TransServices']

    draw_waterfall(df)