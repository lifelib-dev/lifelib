r"""
LMM LIBOR rate and 10-year yield
===================================

Fan charts of the LIBOR rate and of the 10-year yield in the scenarios that
:mod:`~economic.BasicLMM` generates from ``lmm_input.xlsx``.
The blue bands are percentiles over the stochastic scenarios, around their median.
The orange line is the certainty-equivalent (CE) scenario, scenario 0,
which follows the initial forward curve.
The forward rates are shifted lognormal, so they stay above minus the shift,
the dashed line, and their distribution has a long upper tail.

.. seealso::
    * :mod:`~economic.BasicLMM.LMM` in :mod:`~economic.BasicLMM`
    * :doc:`/libraries/economic/lmm-simulation` notebook in the :mod:`~economic` library
"""
import matplotlib.pyplot as plt
import modelx as mx
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MultipleLocator, PercentFormatter

# Chart style of the LMM notebooks: blue for the stochastic scenarios, orange for CE
BLUE, ORANGE, INK_2, MUTED = "#2a78d6", "#eb6834", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
plt.rcParams.update({
    "axes.edgecolor": AXIS, "axes.grid": True, "grid.color": GRID,
    "axes.spines.top": False, "axes.spines.right": False, "axes.titlelocation": "left",
    "axes.labelcolor": INK_2, "xtick.color": AXIS, "ytick.color": AXIS,
    "xtick.labelcolor": INK_2, "ytick.labelcolor": INK_2, "legend.frameon": False,
})
BANDS = [(1, 99), (5, 95), (25, 75)]    # nested percentile bands
WASH = 0.10                             # opacity of each band

lmm = mx.read_model("BasicLMM").LMM
years = np.arange(lmm.step_size() + 1) / 12

fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
for ax, paths, title in [(axes[0], lmm.libor_rate_paths(),
                          f"LIBOR rate, {lmm.tenor_mth()} months"),
                         (axes[1], lmm.spot_rate_paths(120),
                          "10-year yield, annually compounded")]:
    stochastic = paths[1:]
    for lo, hi in BANDS:
        ax.fill_between(years, np.percentile(stochastic, lo, axis=0),
                        np.percentile(stochastic, hi, axis=0),
                        color=BLUE, alpha=WASH, linewidth=0)
    ax.plot(years, np.median(stochastic, axis=0), color=BLUE, linewidth=2)
    ax.plot(years, paths[0], color=ORANGE, linewidth=2)
    ax.axhline(0, color=AXIS, linewidth=1)
    ax.axhline(-lmm.shift(), color=MUTED, linewidth=1, linestyle=(0, (4, 3)))
    ax.set_title(title)
    ax.set_xlabel("years from the valuation date")
    ax.set_xlim(0, years[-1])
    ax.yaxis.set_major_locator(MultipleLocator(0.02))
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))

handles = [Patch(color=BLUE, alpha=1 - (1 - WASH) ** k, linewidth=0,
                 label=f"{lo} to {hi} percentile")
           for k, (lo, hi) in enumerate(BANDS, start=1)]
handles += [Line2D([], [], color=BLUE, linewidth=2, label="median"),
            Line2D([], [], color=ORANGE, linewidth=2, label="CE scenario"),
            Line2D([], [], color=MUTED, linewidth=1, linestyle=(0, (4, 3)),
                   label="minus the shift")]
fig.legend(handles=handles, loc="lower center", ncols=3)
fig.tight_layout(rect=(0, 0.14, 1, 1))
