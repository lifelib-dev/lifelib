import sys
import os

if sys.path[0] != '':
    sys.path.insert(0, '')

from lifelib.projects.simplelife import simplelife
from lifelib.projects.nestedlife import nestedlife
from lifelib.projects.ifrs17sim import ifrs17sim
from lifelib.projects.solvency2 import solvency2

for module in [simplelife, nestedlife, ifrs17sim, solvency2]:
    os.chdir(os.path.dirname(module.__file__))
    module.build()
