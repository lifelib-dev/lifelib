"""The main module to build a solvency2 model.

This module contains only one function :py:func:`build`,
which creates a model from source modules and return it.

If this module is run as a script, the :py:func:`build`
function is called and the created model is available as
``model`` global variable.
"""
import os
import modelx as mx


def build():
    """Build a model and return it.

    Read input data from `input.xlsx`, create `Input` space and its
    subspace and cells and populate them with the data.

    Args:
        load_saved: If ``True``, input data is read from `solvency2.mx` file
            instead of `input.xlsx`, which is saved when
            :py:func:`build_input <solvency2.build_input.build_input>`
            is executed last time. Defaults to ``False``
    """

    # Make sure the current directory is this folder
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    # ------------------------------------------------------------------------
    # Build Input space

    from build_input import build_input
    from build_input_scr import build_input_scr

    model = mx.new_model(name='solvency2')
    input = build_input(model, 'input.xlsx')
    build_input_scr(input, 'input_scr.xlsx')

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
        refs = {attr: PolicyData[PolicyID].cells[attr]() for attr in PolicyAttrs}
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
    # Build SCR_life space
    
    def scrlife_params(t0, PolicyID, ScenID=1):
        pass
    
    scr_life = model.import_module(
        module='scr_life',
        name='SCR_life',
        formula=scrlife_params,
        refs={'Corr': input.CorrLife})


    # ------------------------------------------------------------------------
    # Build Projection space

    projbase = model.import_module(
        module='projection',
        name='BaseProj')

    pvmixin = model.import_module(
        module='present_value',
        name='PV')
    
    override = model.new_space(name='Override')
    
    override.import_module(
        module='override.mortality',
        name='Mortality',
        bases=[projbase, pvmixin]
    )
    
    
    override.import_module(
        module='override.lapse',
        name='Lapse',
        bases=[projbase, pvmixin]
    )

    override.import_module(
        module='override.lapse_mass',
        name='LapseMass',
        bases=[projbase, pvmixin]
    )
    
    override.import_module(
        module='override.expense',
        name='Expense',
        bases=[projbase, pvmixin]
    )
    

    proj_refs = {'Policy': policy,
                 'Assumption': asmp,
                 'Economic': economic}


    def proj_params(Risk='base', Shock=None, Scope=None):

        if Risk == 'mort' or Risk == 'longev':
            base = _space.model.Override.Mortality
        
        elif Risk == 'lapse':
            if Shock == 'mass':
                base = _space.model.Override.LapseMass
            else:
                base = _space.model.Override.Lapse
        elif Risk == 'exps':
                base = _space.model.Override.Expense
        else:
            base = _space
    
        refs = {'pol': Policy[PolicyID],
                'asmp': Assumption[PolicyID],
                'scen': Economic[ScenID],
                'DiscRate': Economic[ScenID].DiscRate,
                'Factor': _space.model.Input.Factor}
        
        return {'base': base, 'refs': refs}


    proj = scr_life.new_space(
        name='Projection',
        bases=[projbase, pvmixin],
        formula=proj_params,
        refs=proj_refs)

    return model


if __name__ == '__main__':
    model = build()




