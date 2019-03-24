"""The main module to build a simplelife model.

This module contains only one function :py:func:`build`,
which creates a model from source modules and return it.

If this module is run as a script, the :py:func:`build` function is called
and the created model is available as ``model`` global variable.
"""
import os
import modelx as mx

# %% Code block for overriding lapse logic.

def SurrRateMult_outer(t):
    """Surrender rate multiple for the outer projection (Default: 1)"""
    if t == 0:
        return 1
    else:
        return SurrRateMult(t-1)


def SurrRateMult_inner(t):
    """Surrender rate multiple for the inner projection (Default: 1)"""
    if t == 0:
        return outer.SurrRateMult(t)

    elif t == t0:
        return _space.parent(t-1).SurrRateMult(t-1)

    else:
        return SurrRateMult(t-1)


def PolsSurr(t):
    """Number of policies: Surrender"""    
    return PolsIF_Beg1(t) * asmp.SurrRate(t) * SurrRateMult(t)


def PolsIF_End_inner(t):
    """Number of policies: End of period"""
    if t == t0:
        return outer.PolsIF_End(t)
    else:
        return PolsIF_Beg1(t-1) - PolsDeath(t-1) - PolsSurr(t-1)

# %% Code block for overriding discounting logic.

def IntAccumCF_outer(t):
    """Intrest on accumulated cashflows"""
    return (AccumCF(t)
            + PremIncome(t)
            - ExpsTotal(t)) * DiscRate(t, 0)


def IntAccumCF_inner(t):
    """Intrest on accumulated cashflows"""
    return (AccumCF(t)
            + PremIncome(t)
            - ExpsTotal(t)) * DiscRate(t)


def DiscRateAdj(t):
    """Adjustment to the outer discount rates"""
    if t == 0:
        return 0
    else:
        return DiscRateAdj(t-1)

    
def DiscRate_outer(t, dur):
    """Discount rates for the outer projection"""
    return scen.DiscRate(dur) + DiscRateAdj(t)


def DiscRate_inner(t):
    """Discount rates for the inner projection"""
    return outer.DiscRate(t0, t)
    
    
# %% Code block for build function

def build(load_saved=False):
    """Build a model and return it.

    Read input data from `input.xlsx`, create `Input` space and its
    subspace and cells and populate them with the data.

    Args:
        load_saved: If ``True``, input data is read from `ifrs17sim.mx` file
            instead of `input.xlsx`, which is saved when
            :py:func:`build_input <simplelife.build_input.build_input>`
            is executed last time. Defaults to ``False``
    """

    # Make sure the current directory is this folder
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    # ------------------------------------------------------------------------
    # Build Input space

    from build_input import build_input

    if load_saved:
        model = mx.open_model('ifrs17sim.mx')
        input = model.Input
    else:
        model = mx.new_model(name='ifrs17sim')
        input = build_input(model, 'input.xlsx')
        model.save('ifrs17sim.mx')

    # ------------------------------------------------------------------------
    # Build CommFunc space

    lifetable_refs = {'Input': input}

    def lifetable_params(Sex, IntRate, TableID):
        refs={'MortalityTable': Input.MortalityTables(TableID).MortalityTable}
        return {'refs': refs}

    lifetable = model.import_module(
        module='lifetable',
        name='LifeTable',
        formula=lifetable_params,
        refs=lifetable_refs)

    # ------------------------------------------------------------------------
    # Build Policy space

    from policy import policy_attrs

    policy_refs = {'PolicyData': input.PolicyData,
                   'ProductSpec': input.ProductSpec,
                   'LifeTable': lifetable,
                   'PolicyAttrs': policy_attrs}

    def policy_params(PolicyID):
        refs = {attr: PolicyData[PolicyID].cells[attr] for attr in PolicyAttrs}
        alias = {'PremTerm': refs['PolicyTerm'],
                 'x': refs['IssueAge'],
                 'm': refs['PolicyTerm'],
                 'n': refs['PolicyTerm']}

        refs.update(alias)
        return {'refs': refs}

    policy = model.import_module(
        module='policy',
        name='Policy',
        formula=policy_params,
        refs=policy_refs)

    # ------------------------------------------------------------------------
    # Build Assumption space

    asmp_refs = {'Policy': policy,
                 'ProductSpec': input.ProductSpec,
                 'MortalityTables': input.MortalityTables,
                 'asmp': input.Assumption,
                 'asmp_tbl': input.AssumptionTables}

    def asmp_params(PolicyID):
        refs = {'pol': Policy[PolicyID]}
        alias = {'prod': refs['pol'].Product,
                 'polt': refs['pol'].PolicyType,
                 'gen': refs['pol'].Gen}
        refs.update(alias)
        return {'refs': refs}

    asmp = model.import_module(
        module='assumption',
        name='Assumption',
        formula=asmp_params,
        refs=asmp_refs)

    asmp.allow_none = True

    # ------------------------------------------------------------------------
    # Build Assumption space

    def econ_params(ScenID):
        refs = {'Scenario': Input.Scenarios[ScenID]}
        return {'refs': refs}

    economic = model.import_module(
        module='economic',
        name='Economic',
        formula=econ_params,
        refs={'asmp': asmp,
              'Input': input})

    # ------------------------------------------------------------------------
    # Build Projection space
    
    # Model tree structure
    # 
    # lifelib --+
    #           +--BaseProj
    #           +--OuterProj[PolicyID] <--- BaseProj
    #                    +--InnerProj[t] <-- BaseProj

    proj_refs = {'Pol': policy,
                 'Asmp': asmp,
                 'Scen': economic}

    def proj_params(PolicyID, ScenID=1):
        refs = {'pol': Pol[PolicyID],
                'asmp': Asmp[PolicyID],
                'scen': Scen[ScenID]}

        return {'refs': refs}

    baseproj = model.import_module(
        module='projection',
        name='BaseProj')

    ifrs = model.import_module(
        module='ifrs',
        name='IFRS')

    outerproj = model.new_space(
        bases=[ifrs, baseproj],
        name='OuterProj',
        formula=proj_params,
        refs=proj_refs)

    def innerproj_params(t0):
        refs = {'pol': _space.parent.pol,
                'asmp': _space.parent.asmp,
                'scen': _space.parent.scen,
                'outer': _space.parent}
        
        return {'refs': refs}

    innerproj = outerproj.new_space(
        bases=baseproj,
        name='InnerProj',
        formula=innerproj_params)

    pvs = innerproj.import_module(
        module='present_value',
        name='PresentValue')
    
    def pvs_params(t_rate):
        refs = {'last_t': _space.parent.last_t,
                'InsurIF_Beg1': _space.parent.InsurIF_Beg1,
                'InsurIF_End': _space.parent.InsurIF_End,
                'PremIncome': _space.parent.PremIncome,
                'BenefitSurr': _space.parent.BenefitSurr,
                'BenefitDeath': _space.parent.BenefitDeath,
                'BenefitTotal': _space.parent.BenefitTotal,
                'ExpsCommTotal': _space.parent.ExpsCommTotal,
                'ExpsAcq': _space.parent.ExpsAcq,
                'ExpsMaint': _space.parent.ExpsMaint,
                'ExpsTotal': _space.parent.ExpsTotal,
                'DiscRate': _space.parent.parent[t_rate].DiscRate}
        
        return {'refs': refs}
        
    pvs.set_formula(pvs_params)
    
    # Add or override functions.
    baseproj.new_cells(name='SurrRateMult', formula=SurrRateMult_outer)
    baseproj.PolsSurr.set_formula(PolsSurr)
    outerproj.IntAccumCF.set_formula(IntAccumCF_outer)
    outerproj.new_cells(name='DiscRate', formula=DiscRate_outer)
    outerproj.new_cells(formula=DiscRateAdj)
    innerproj.new_cells(name='DiscRate', formula=DiscRate_inner)
    innerproj.SurrRateMult.set_formula(SurrRateMult_inner)
    innerproj.IntAccumCF.set_formula(IntAccumCF_inner)
    innerproj.PolsIF_End.set_formula(PolsIF_End_inner)
    
    return model


if __name__ == '__main__':
    model = build()
