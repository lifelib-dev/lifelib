import pathlib
import filecmp
import lifelib
import lifelib.projects.simplelife as simplelife
import lifelib.projects.nestedlife as nestedlife

simplepath = simplelife.__path__[0]
nestedpath = nestedlife.__path__[0]

common_files = ['build_input.py',
                'lifetable.py',
                'policy.py',
                'assumptions.py',
                'economic.py',
                'projection.py',
                'input.xlsm']


def test_filecomp():
    """Check equality of common files between simplelife and nestedlife"""

    result = filecmp.cmpfiles(simplepath, nestedpath, common_files)
    assert common_files == result[0]


sample_files = {simplepath: ['plot_simplelife.py',
                             'plot_pvcashflows.py'],
                nestedpath: ['plot_pvnetcf.py',
                             'plot_actexpct.py']}

example_dir = str(pathlib.Path(lifelib.__path__[0]).parent.joinpath('examples'))

def test_samplecomp():
    for projdir, samples in sample_files.items():
        result = filecmp.cmpfiles(projdir, example_dir, samples)
        assert samples == result[0]
