"""
solvency2: cashflows
===========================

Net liability cashflows by SCR shock scenarios for selected policies

.. seealso::
    * The :mod:`~solvency2` library
"""
import modelx as mx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")

model = mx.read_model("model")


def draw(polid, t0):

    fig, ax = plt.subplots()
    fig.suptitle('Net Cashflows')

    title = 'Policy ID: ' + str(polid) + ', Shock at ' + str(t0)

    data = {}
    for risk, shock in (('base', None),
                        ('mort', None),
                        ('longev', None),
                        ('lapse', 'up'),
                        ('lapse', 'down'),
                        ('lapse', 'mass'),
                        ('exps', None)):

        proj = model.SCR_life[t0, polid].Projection(risk, shock)
        last_t = proj.last_t()
        label = risk + ('(' + shock + ')' if shock else '')
        data[label] = [proj.NetInsurCF[t] for t in range(t0, last_t)]

    return pd.DataFrame(
        data, index=range(t0, last_t)).plot(
        ax=ax, kind='line', title=title)


for polid, t0 in [(41, 5), (171, 5)]:
    draw(polid, t0)
