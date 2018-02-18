"""The main module to build a simplelife model.

This module contains only one function :py:func:`build`,
which creates a model from source modules and return it.

If this module is run as a script, the :py:func:`build` function is called
and the created model is available as ``model`` global variable.
"""

import sys, os
import modelx as mx

if '__file__' in globals():
    proj_dir = os.path.abspath(os.path.dirname(__file__))
    if proj_dir not in sys.path:
        sys.path.insert(0, proj_dir)
else:
    proj_dir = ''


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

    # ------------------------------------------------------------------------
    # Build Input space

    from build_input import build_input

    if load_saved:
        model = mx.open_model(proj_dir + '/lifelib.mx')
        input = model.Input
    else:
        model = mx.new_model(name='lifelib')
        input = build_input(model, proj_dir + '/input.xlsm')
        model.save(proj_dir + '/lifelib.mx')

    # ------------------------------------------------------------------------
    # Build CommFunc space

    lifetable_refs = {'Input': input}

    def lifetable_params(Sex, IntRate, TableID):
        refs={'MortalityTable': Input.MortalityTables(TableID).MortalityTable}
        return {'bases': _self,
                'refs': refs}

    lifetable = model.new_space_from_module(
        module_='lifetable',
        name='LifeTable',
        paramfunc=lifetable_params,
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

    policy = model.new_space_from_module(
        module_='policy',
        name='Policy',
        paramfunc=policy_params,
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

    asmp = model.new_space_from_module(
        module_='assumptions',
        name='Assumptions',
        paramfunc=asmp_params,
        refs=asmp_refs)

    asmp.can_have_none = True

    # ------------------------------------------------------------------------
    # Build Assumptions space

    def econ_params(ScenID):
        refs = {'Scenario': Input.Scenarios[ScenID]}
        return {'bases': _self,
                'refs': refs}

    economic = model.new_space_from_module(
        module_='economic',
        name='Economic',
        paramfunc=econ_params,
        refs={'asmp': asmp,
              'Input': input})

    # ------------------------------------------------------------------------
    # Build Projection space

    proj_refs = {'Policy': policy,
                 'Assumptions': asmp,
                 'Economic': economic}

    def proj_params(PolicyID, ScenID=3):
        refs = {'pol': Policy[PolicyID],
                'asmp': Assumptions[PolicyID],
                'scen': Economic[ScenID]}
        return {'bases': _self,
                'refs': refs}

    proj = model.new_space_from_module(
        module_='projection',
        name='Projection',
        paramfunc=proj_params,
        refs=proj_refs)

    return model


if __name__ == '__main__':
    model = build()




