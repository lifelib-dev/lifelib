"""
:mod:`ifrs17sim` CSM waterfall chars
====================================

Draw a graph of CSM amortization pattern.
"""

import collections
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def draw_waterfall(df, ax=None, **kwargs):
    """Draw waterfall chart"""
    data = df.stack()
    bottom = df.cumsum(axis=1).shift(1, axis=1).fillna(0).stack()
    palette = WaterfallColorPalette(df)
    xlabel = [idx[1] + '(' + str(idx[0]) + ')' for idx in df.stack().index]
    ax = sns.barplot(data=data, bottom=bottom,
                     palette=palette.colors,
                     ax=ax)
    ax.set_xticklabels(labels=xlabel, rotation='vertical')
    if 'title' in kwargs:
        ax.set_title(kwargs['title'])
    ax.get_figure().tight_layout()
    return ax


class WaterfallColorPalette:
    """Returns color palette for drawing waterfall bars.

    The length of `data` columns

    Args:
        data: a DataFrame of waterfall data.
        length: the number of bars in an interval. Defaults to the length of
                `data` columns.
    """
    
    def __init__(self, data, length=None):

        self.data = data
        if length is None:
            self.length = len(data.columns)
        else:
            self.length = length

        self.paired = plt.get_cmap('Paired').colors
        self.colors = self.set_colors()

    def set_colors(self):

        result = []
        row_count, _ = self.data.shape

        for row in range(row_count):
            for col in range(self.length):
                sign = self.data.iloc[row, col] >= 0
                result.append(self.get_color(col, sign))

        return result

    def get_color(self, idx, sign):
        pair_count = len(self.paired) // 2
        idx = 2 * (idx % pair_count)
        return self.paired[idx + 1] if sign else self.paired[idx]


class CustomColorMap:
    """Unused. Colors changing by size and sign of data

    Args:
        data: a sequence of bar values.
    """
    import math

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

    def get_colors(self, data):
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
    plt.show()