"""The main script to build a simplelife model.

.. rubric:: Model

Attributes:
    model: The model object that contains all the spaces.

.. rubric:: Spaces

Attributes:
    lifetable: :py:mod:`LifeTable<simplelife.lifetable>` space
    policy: :py:mod:`Policy<simplelife.policy>` space
    asmp: :py:mod:`Assumptions<simplelife.assumptions>` space
    proj: :py:mod:`Projection<simplelife.projection>` sapce
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
    """Build a model and return it"""

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




