"""Draw a graph of liability cashflows of a simple whole life policy"""

import nestedlife

polid = 171
model = nestedlife.build(load_saved=True)
outer = model.OuterProjection
inner = model.OuterProjection.InnerProjection

#%% Code block for overwiting the model

def nop_Surrender_outer(t):
    """Number of policies: Surrender"""
    
    if t == 1:
        surr_rate_mult = 2
    elif t == 2:
        surr_rate_mult = 0.5
    else:
        surr_rate_mult = 1
    
    return nop_BoP1(t) * asmp.SurrRate(t) * surr_rate_mult


def nop_EoP_inner(t):
    """Number of policies: End of period"""
    if t == t0:
        return outer.nop_EoP(t)
    else:
        return nop_BoP1(t - 1) - nop_Death(t - 1) - nop_Surrender(t - 1)


outer.new_cells(name='nop_Surrender', formula=nop_Surrender_outer)
outer[171].InnerProjection[1].SurrRateMult = 2
outer[171].InnerProjection[2].SurrRateMult = 0.5
inner.new_cells(name='nop_EoP', formula=nop_EoP_inner)

#%% Code block for drawing graphs

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()    
    
def get_nested(item):
    
    cells = getattr(outer[polid], item)
    
    act = [cells[t] for t in range(50)]
    expect = []
    
    for t0 in range(0, 6):
        expect_t0 = [np.nan] * 50
        for t in range(0, 50):
            if t < t0:
                expect_t0[t] = np.nan
            else:
                cells = getattr(outer[polid].InnerProjection[t0], item)
                expect_t0[t] = cells[t]
    
        expect.append(expect_t0)
        
    return act, expect
    

def mask_act(act, t0):
    masked_act = act.copy()
    for t, val in enumerate(masked_act):
        if t > t0:
            masked_act[t] = np.nan
    return masked_act


def draw_graphs(item):
    
    act, expect = get_nested(item)
    
    nrows = len(expect)
    fg, axs = plt.subplots(nrows=nrows, sharex=True, sharey=True)
    for t0, ax in enumerate(axs):
        draw_single_ncf(expect[t0], ax, ':')
        draw_single_ncf(mask_act(act, t0), ax, '-')


def draw_single_ncf(ncf, ax, ls):
    ax.plot(ncf, marker='o', linestyle=ls)
    ax.set_xlim(right=10, left=-1)


#%% Code block for PV graph 
    
def draw_bars(item):
    
    term = 5
    
    expect = []
    for t0 in range(term):
        expect_t0 = [np.nan] * term
        for t in range(t0, term):
            cells = getattr(outer[polid].InnerProjection[t0], item)
            expect_t0[t] = cells[t]
            
        expect.append(expect_t0)
    
    fg, ax = plt.subplots()
    ax.set_xlim(left=-0.5, right=term + 1)
    
    for t0 in range(term):
        draw_single_bar(expect[t0], ax, t0)
    
    
def draw_single_bar(data, ax, t0):

    size = len(data)
    width = 1/ (size + 1)
    ax.bar(np.arange(size) + t0 * (width + 0.05), data, width)
    


#%% PV Test
liab0 = outer[171].InnerProjection[0]
item = ['pv_incm_Premium',
        'pv_bnft_Death',
        'pv_bnft_Surrender',
        'pv_exps_Total']

draw_bars('pv_incm_Premium')

