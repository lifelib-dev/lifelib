import os.path
import sys
import shutil
import math
import modelx as mx
import lifelib
import lifelib.commands.create as cmd
import pytest


@pytest.mark.parametrize('argv', [
    [],
    ['--template', 'basiclife']
])
def test_argparser(argv):
    tempdir = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'mylife')

    parser = cmd.get_argparser()
    argv.append(tempdir)
    args = parser.parse_args(argv)

    assert args.template == 'basiclife' and args.proj_dir == tempdir


@pytest.mark.parametrize('argv', [
    [],
    ['--template', 'basiclife']
])
def test_main(argv, tmp_path):
    tempdir = str(tmp_path / 'mylife')

    argv.append(tempdir)
    cmd.main(argv)

    while True:
        try:
            shutil.rmtree(tempdir)
            break
        except (PermissionError, OSError):
            pass

    assert True


@pytest.mark.parametrize(
    "library, model_dir, target, method, args, expected",
    [
        ["basiclife",
         "BasicTermASL_ME",
         ("BasicTermASL_ME", "Projection", "pv_net_cf", ()),
         "__getitem__",
         (0,),
         34191.46241209286],

        ["basiclife",
         "BasicTerm_SE",
         ("BasicTerm_SE", "Projection", (1,), "pv_net_cf", ()),
         None,
         None,
         108625.00562388412],

        ["basiclife",
         "BasicTerm_ME",
         ("BasicTerm_ME", "Projection", "pv_net_cf", ()),
         "__getitem__",
         (0,),
         108625.00562388412],

        ["basiclife",
         "BasicTerm_S",
         ("BasicTerm_S", "Projection", (1,), "pv_net_cf", ()),
         None,
         None,
         910.92066093366],

        ["basiclife",
         "BasicTerm_M",
         ("BasicTerm_M", "Projection", "pv_net_cf", ()),
         "__getitem__",
         (0,),
         910.92066093366],

        ["savings",
         "CashValue_SE",
         ("CashValue_SE", "Projection", "pv_net_cf", ()),
         None,
         None,
         4950173.438724911],

        ["savings",
         "CashValue_ME",
         ("CashValue_ME", "Projection", "pv_net_cf", ()),
         "__getitem__",
         (0,),
         4950173.438724911],

        ["fastlife",
         "model",
         ("fastlife", "Projection", "PV_NetCashflow", (0,)),
         "__getitem__",
         (1,),
         8954.018303162458],

        ["simplelife",
         "model",
         ('simplelife', 'Projection', (1,), 'PV_NetCashflow', (0,)),
         None,
         None,
         8954.018303162458],

        ["nestedlife",
         "model",
         ('nestedlife', 'OuterProj', (1,), 'PV_NetCashflow', (0,)),
         None,
         None,
         8954.018303162458],

        ["ifrs17sim",
         "model",
         ('ifrs17sim', 'OuterProj', (1,), 'CSM', (10,)),
         None,
         None,
         1946.6462116677003],

        ["solvency2",
         "model",
         ('solvency2', 'SCR_life', (0, 1), 'SCR_life', ()),
         None,
         None,
         5929.437677484881],

        ["smithwilson",
         "model",
         ('smithwilson', 'SmithWilson', 'P', (10,)),
         None,
         None,
         1.0216540491640598]

    ]
)
def test_package(library, model_dir, target, method, args, expected, tmp_path):

    lib_dir = os.path.join(tmp_path, library)
    lifelib.create(library, lib_dir)

    m = mx.read_model(os.path.join(lib_dir, model_dir))

    actual = mx.core.mxsys.get_object_from_idtuple(target)

    if method:
        actual = getattr(actual, method)(*args)

    assert math.isclose(actual, expected)
    m.close()
