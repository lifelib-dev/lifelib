"""
Draw radar charts
=================

This module contains :func:`draw_radar`, a function to draw radar charts a.k.a
spyder charts.

The code in this module is derived from the matplot example,
`Radar chart (aka spider or star chart) <https://matplotlib.org/gallery/specialty_plots/radar_chart.html>`_.

See `Matplotlib license <https://matplotlib.org/users/license.html>`_.
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection


def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    def draw_poly_patch(self):
        # rotate theta such that the first axis is at the top
        verts = unit_poly_verts(theta + np.pi / 2)
        return plt.Polygon(verts, closed=True, edgecolor='k')

    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plt.Circle((0.5, 0.5), 0.5)

    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_patch = patch_dict[frame]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame.

            # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
            spine_type = 'circle'
            verts = unit_poly_verts(theta + np.pi / 2)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    return theta


def unit_poly_verts(theta):
    """Return vertices of polygon for subplot axes.

    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts


def get_rgrids(max_value, rgrid_count):
    """Calculate radial grid steps and return it as a list"""

    import math

    digits = math.floor(math.log(max_value, 10))
    scale = max_value / (10**digits)

    ubound = math.ceil(scale) * (10**digits)
    step = ubound / (rgrid_count+1)

    return list(step * i for i in range(1, rgrid_count+1))


def draw_radar(df: pd.DataFrame, ax_title=None, fig_title=None,
               colors=('b', 'r', 'g', 'm', 'y')):
    """Draw radar chart"""

    spoke_count, line_count = df.shape

    theta = radar_factory(spoke_count, frame='polygon')
    spoke_labels = list(df.index)

    fig, ax = plt.subplots(subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    if len(colors) < line_count:
        colors = (colors * (line_count // len(colors) + 1))[:line_count]

    ax.set_rgrids(get_rgrids(df.max().max(), 4))
    if ax_title:
        ax.set_title(ax_title, weight='normal', size='medium',
                     position=(0.5, 1.09),
                     horizontalalignment='center', verticalalignment='center')

    for col, color in zip(df, colors):
        ax.plot(theta, list(df[col]), color=color)
        ax.fill(theta, list(df[col]), facecolor=color, alpha=0.25)

    ax.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    labels = list(df.columns)
    legend = ax.legend(labels, loc=(0.9, .95),
                       labelspacing=0.1)

    fig.text(0.5, 0.965, fig_title,
             horizontalalignment='center', color='black', weight='bold',
             size='large')

    return ax


if __name__ == '__main__':

    data = {'Line 1': [0.88, 1.30, 0.50, 0.03],
            'Line 2': [0.07, 0.95, 0.04, 0.05],
            'Line 3': [0.01, 0.02, 0.85, 0.19],
            'Line 4': [0.02, 0.01, 0.07, 0.60],
            'Line 5': [0.01, 0.01, 0.02, 0.71]}

    index = ['Sulfate', 'Nitrate', 'EC', 'OC1']

    df = pd.DataFrame(data=data, index=index)

    draw_radar(df, fig_title='Sample Radar')

    plt.show()
