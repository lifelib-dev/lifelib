
import filecmp
import lifelib.projects.simplelife as simplelife
import lifelib.projects.nestedlife as nestedlife


common_files = ['build_input.py',
                'lifetable.py',
                'policy.py',
                'assumptions.py',
                'economic.py',
                'projection.py']


def test_filecomp():
    """Check equality of common files between simplelife and nestedlife"""
    simplepath = simplelife.__path__[0]
    nestedpath = nestedlife.__path__[0]
    result = filecmp.cmpfiles(simplepath, nestedpath, common_files)

    assert common_files == result[0]
