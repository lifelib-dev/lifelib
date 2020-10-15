import os.path
import sys
import shutil
import lifelib.commands.create as cmd
import pytest


@pytest.mark.parametrize('argv', [
    [],
    ['--template', 'simplelife']
])
def test_argparser(argv):
    tempdir = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'mylife')

    parser = cmd.get_argparser()
    argv.append(tempdir)
    args = parser.parse_args(argv)

    assert args.template == 'simplelife' and args.proj_dir == tempdir


@pytest.mark.parametrize('argv', [
    [],
    ['--template', 'simplelife']
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
