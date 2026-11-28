r"""
LMM caplets
===================================

On the left, the Black volatility of the caplet on each forward rate that
:mod:`~economic.BasicLMM` sets at a whole year,
from the volatility table of ``lmm_input.xlsx``:
a caplet on :math:`F_k` is priced by Black's formula with this volatility,
the shifted forward rate :math:`F_k(0) + \alpha` and the shifted strike.
On the right, the Monte Carlo prices of at-the-money caplets on the same rates
against Black's formula,
which checks the distribution of the rates and the monthly step that simulates them.
The band is the 95% Monte Carlo interval, from the standard errors of antithetic
pair means.

.. seealso::
    * :mod:`~economic.BasicLMM.Validation` in :mod:`~economic.BasicLMM`
    * :doc:`/libraries/economic/lmm-simulation` notebook in the :mod:`~economic` library
"""
import matplotlib.pyplot as plt
import modelx as mx
from matplotlib.ticker import MultipleLocator, PercentFormatter

# Chart style of the LMM notebooks
BLUE, INK_2, GRID, AXIS = "#2a78d6", "#52514e", "#e1e0d9", "#c3c2b7"
plt.rcParams.update({
    "axes.edgecolor": AXIS, "axes.grid": True, "grid.color": GRID,
    "axes.spines.top": False, "axes.spines.right": False, "axes.titlelocation": "left",
    "axes.labelcolor": INK_2, "xtick.color": AXIS, "ytick.color": AXIS,
    "xtick.labelcolor": INK_2, "ytick.labelcolor": INK_2, "legend.frameon": False,
})

model = mx.read_model("BasicLMM")
lmm, validation = model.LMM, model.Validation
caplets = validation.caplet_test()
ks = caplets.index.get_level_values("k")
expiry = caplets.index.get_level_values("expiry")

fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4))
left.plot(expiry, [lmm.caplet_vol(k) for k in ks], color=BLUE, linewidth=2)
left.set_title("Black volatility of caplets (rate + shift)")
left.set_xlabel("expiry in years")
left.set_ylim(0, None)
left.yaxis.set_major_locator(MultipleLocator(0.02))
left.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))

half_width = 1.96 * caplets["se"] / caplets["theory"]
ratio = caplets["mc"] / caplets["theory"] - 1
limit = 1.2 * max(half_width.max(), ratio.abs().max())
right.fill_between(expiry, -half_width, half_width, color=BLUE, alpha=0.1, linewidth=0,
                   label="95% Monte Carlo interval")
right.plot(expiry, ratio, color=BLUE, linewidth=2,
           label="Monte Carlo price / Black's formula \N{MINUS SIGN} 1")
right.axhline(0, color=AXIS, linewidth=1)
right.set_ylim(-limit, limit)
right.set_title("At-the-money caplets against Black's formula")
right.set_xlabel("expiry in years")
right.yaxis.set_major_locator(MultipleLocator(0.04))
right.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
fig.legend(*right.get_legend_handles_labels(), loc="lower center", ncols=2)
fig.tight_layout(rect=(0, 0.08, 1, 1))
