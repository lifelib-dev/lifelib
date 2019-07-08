"""
:mod:`ifrs17sim` CSM waterfall chars
====================================

Draw a graph of CSM amortization pattern.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# %% Draw Actuarl vs Estimated charts

def _get_est(inner, item, t0, t_max):
    """Get estimated values for ``item`` (nan for t < t0)."""
    cells = inner[t0].cells[item]
    return [cells[t] if t >= t0 else np.nan
            for t in range(t_max)]


def _get_act(outer, item, t0, t_max):
    """Get actual values for ``item`` (nan for t > t0)."""
    cells = outer.cells[item]
    return [cells[t] if t <= t0 else np.nan
            for t in range(t_max)]


def _get_actest(outer, inner, item, t0_max, t_max):
    """Get a pair of actual and estimated values at t0."""
    return (_get_act(outer, item, t0_max, t_max),
            _get_est(inner, item, t0_max, t_max))


def _draw_single_ncf(values, ax, xlim, ls):
    """Draw a plotted line of values."""
    ax.plot(values, marker='o', linestyle=ls)
    ax.set_xlim(right=xlim, left=-1)


def draw_actest(outer, inner, item, act_len, t_max):
    """Draw a graph of actual and estimated"""

    _, axs = plt.subplots(nrows=act_len, sharex=True, sharey=True)

    axs[0].set_title(item)

    for t0 in range(act_len):
        ax = axs[t0]
        act, est = _get_actest(outer, inner, item, t0, t_max + 1)
        _draw_single_ncf(est, ax, t_max, ':')
        _draw_single_ncf(act, ax, t_max, '-')


def draw_actest_pairs(outer, inner, items, act_len, t_max):
    """Draw pairs of line graphs."""
    ncols = len(items)
    nrows = act_len

    if ncols == 1:
        return draw_actest(outer, inner, items[0], act_len, t_max)

    _, axs = plt.subplots(nrows=nrows, ncols=ncols, sharex=True)

    for col, item in enumerate(items):
        axs[0][col].set_title(items[col])
        for t0 in range(nrows):
            ax = axs[t0][col]
            act, est = _get_actest(outer, inner, item, t0, t_max + 1)
            _draw_single_ncf(est, ax, t_max, ':')
            _draw_single_ncf(act, ax, t_max, '-')

# %% Waterfall chart functions

def get_waterfalldata(space, items, length, reverseitems=[]):
    """Create a DataFrame for drawing waterfall chart"""

    data = type(space.cells)(space.cells, items).to_frame(range(length))
    for outflow in reverseitems:
        data[outflow] = -1 * data[outflow]
    return data


def draw_waterfall(df, ax=None, stocks=[0], **kwargs):
    """Draw waterfall chart

    `stocks` parameter is for specifying column indexes of `df` that are to
    be interpreted as stock items as opposed to flow items,
    i.e. bars for these columns are drawn from zero.
    """

    if ax is None:
        plt.figure()
        ax = plt.gca()

    cols = len(df.columns)
    cumsum = df.copy()
    bottom = df.copy()
    bottom.iloc[:,:] = 0

    for c in range(cols):
        if (c + 1) % cols in stocks:
            cumsum.iloc[:, list(range(c + 1))] = 0
            bottom.iloc[:, c] = 0
        else:
            bottom.iloc[:, c] = cumsum.cumsum(axis=1).iloc[:, c]

    data = df.stack()
    bottom = bottom.stack().shift(1, axis=0).fillna(0)

    palette = WaterfallColorPalette(df)
    xlabel = [idx[1] + '(' + str(idx[0]) + ')' for idx in df.stack().index]
    ax = sns.barplot(data=[[i] for i in data], bottom=list(bottom),
                     palette=palette.colors,
                     ax=ax)
    ax.set_xticklabels(labels=xlabel, rotation='vertical')
    if 'title' in kwargs:
        ax.set_title(kwargs['title'])
    ax.get_figure().tight_layout()
    return ax


# %% Unused

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

# %% Draw stacked bar pair charts

def draw_stackedbarpairs(data, ax=None, **kwargs):
    """Draw pairs of stacked bars

    Draw a series of pairs of stacked bars. For each column,
    bars are drawn either on the left or right of the x ticks,
    depending the sines of values (left if negative, right if positive).
    Bars on each side of each x tick are stacked each other.

    Args:
        data: DataFrame
    """

    if ax is None:
        ax = plt.gca()

    rbars = data[data >= 0]
    lbars = -1 * data[data < 0]

    rbottom, lbottom = \
        [bars.fillna(0).cumsum(axis=1).shift(1, axis=1).fillna(0)
         for bars in [rbars, lbars]]

    def draw_single_bar(data, bottom, ax, n, **kwargs):
        width = 0.4
        return ax.bar(np.arange(len(data)) + n * (width / 2), 
                      data, width - 0.05, bottom=bottom, **kwargs)
    
    legend = [[],[]]
    for c in data.columns:
        bar = draw_single_bar(rbars[c], rbottom[c], ax, +1, label=c)
        color = bar.patches[0].get_facecolor()
        draw_single_bar(lbars[c], lbottom[c], ax, -1, color=color)
        # legend[0].append(bar)
        # legend[1].append(c)
    
    ax.legend()

    if 'title' in kwargs:
        ax.set_title(kwargs['title'])
