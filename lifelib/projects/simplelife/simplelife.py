"""The main module to build a simplelife model.

This module contains only one function :py:func:`build`,
which creates a model from source modules and return it.

If this module is run as a script, the :py:func:`build` function is called
and the created model is available as ``model`` global variable.
"""
import os
import modelx as mx

def build(load_saved=False):
    """Build a model and return it.

    Read input data from `input.xlsm`, create `Input` space and its
    subspace and cells and populate them with the data.

    Args:
        load_saved: If ``True``, input data is read from `lifelib.mx` file
            instead of `input.xlsm`, which is saved when
            :py:func:`build_input <simplelife.build_input.build_input>`
            is executed last time. Defaults to ``False``
    """

    # Make sure the current directory is this folder
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    # ------------------------------------------------------------------------
    # Build Input space

    from build_input import build_input

    if load_saved:
        model = mx.open_model('simplelife.mx')
        input = model.Input
    else:
        model = mx.new_model(name='simplelife')
        input = build_input(model, 'input.xlsm')
        model.save('simplelife.mx')

    # ------------------------------------------------------------------------
    # Build CommFunc space

    lifetable_refs = {'Input': input}

    def lifetable_params(Sex, IntRate, TableID):
        refs={'MortalityTable': Input.MortalityTables(TableID).MortalityTable}
        return {'bases': _self,
                'refs': refs}

    lifetable = model.import_module(
        module_='lifetable',
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
        return {'bases': _self,
                'refs': refs}

    policy = model.import_module(
        module_='policy',
        name='Policy',
        formula=policy_params,
        refs=policy_refs)

    # ------------------------------------------------------------------------
    # Build Assumptions space

    asmp_refs = {'Policy': policy,
                 'ProductSpec': input.ProductSpec,
                 'MortalityTables': input.MortalityTables,
                 'asmp': input.Assumptions,
                 'asmp_tbl': input.AssumptionTables}

    def asmp_params(PolicyID):
        refs = {'pol': Policy[PolicyID]}
        alias = {'prd': refs['pol'].Product,
                 'polt': refs['pol'].PolicyType,
                 'gen': refs['pol'].Gen}
        refs.update(alias)
        return {'bases': _self,
                'refs': refs}

    asmp = model.import_module(
        module_='assumptions',
        name='Assumptions',
        formula=asmp_params,
        refs=asmp_refs)

    asmp.allow_none = True

    # ------------------------------------------------------------------------
    # Build Assumptions space

    def econ_params(ScenID):
        refs = {'Scenario': Input.Scenarios[ScenID]}
        return {'bases': _self,
                'refs': refs}

    economic = model.import_module(
        module_='economic',
        name='Economic',
        formula=econ_params,
        refs={'asmp': asmp,
              'Input': input})

    # ------------------------------------------------------------------------
    # Build Projection space

    projbase = model.import_module(
        module_='projection',
        name='ProjBase')

    pvmixin = model.import_module(
        module_='present_values',
        name='PV')

    proj_refs = {'Policy': policy,
                 'Assumptions': asmp,
                 'Economic': economic}

    def proj_params(PolicyID, ScenID=1):
        refs = {'pol': Policy[PolicyID],
                'asmp': Assumptions[PolicyID],
                'scen': Economic[ScenID],
                'DiscRate': Economic[ScenID].DiscRate}
        return {'bases': _self,
                'refs': refs}

    proj = model.new_space(
        name='Projection',
        bases=[projbase, pvmixin],
        formula=proj_params,
        refs=proj_refs)

    return model


if __name__ == '__main__':
    model = build()




