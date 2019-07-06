"""
:mod:`ifrs17sim` IFRS balancesheet itms
=======================================

Fulfilment CF, CSM, Cash balances
"""

# When the current directory is this folder,
# The try-except statement below can be replaced by just the last two
# import statements.
try:
    import ifrs17sim.ifrs17sim as ifrs17sim
    import ifrs17sim.draw_charts as draw_charts
except ImportError:
    import ifrs17sim
    import draw_charts

model = ifrs17sim.build()
proj = model.OuterProj[171]


ifrsbs = proj.cells['CSM',
                    'PV_FutureCF',
                    'AccumCF'].to_frame(range(10))

ifrsbs.columns = ['CSM', 'FCF', 'Cash']
ifrsbs['FCF'] = -1 * ifrsbs['FCF']
ifrsbs['Cash'] = -1 * ifrsbs['Cash']

draw_charts.draw_stackedbarpairs(ifrsbs,
                                 title='Fulfilment CF and CSM')

