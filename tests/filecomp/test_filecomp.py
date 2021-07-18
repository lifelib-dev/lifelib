import os.path
import pathlib
import filecmp

import pytest

import lifelib
import lifelib.projects.simplelife.scripts as simplelife
import lifelib.projects.nestedlife.scripts as nestedlife
import lifelib.projects.ifrs17sim.scripts as ifrs17sim
import lifelib.projects.solvency2.scripts as solvency2

simplepath = simplelife.__path__[0]
nestedpath = nestedlife.__path__[0]
ifrs17simpath = ifrs17sim.__path__[0]
solvency2path = solvency2.__path__[0]

all_projects = [simplepath, nestedpath, ifrs17simpath, solvency2path]

common_files = [('build_input.py', all_projects),
                ('lifetable.py', all_projects),
                ('policy.py', all_projects),
                ('assumption.py', all_projects),
                ('economic.py', all_projects),
                ('projection.py', all_projects),
                ('present_value.py', all_projects),
                ('draw_charts.py', [nestedpath + "/..", ifrs17simpath + "/.."]),
                ('input.xlsx', all_projects)]


@pytest.mark.parametrize('filename, filepaths', common_files)
def test_filecomp(filename, filepaths):
    """Check equality of common files between simplelife and nestedlife"""

    for path1, path2 in zip(filepaths, filepaths[1:]):
        assert filecmp.cmp(os.path.join(path1, filename),
                           os.path.join(path2, filename))
