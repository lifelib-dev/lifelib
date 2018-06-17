import sys
import os

if sys.path[0] != '':
    sys.path.insert(0, '')

from lifelib.projects.simplelife import simplelife
from lifelib.projects.nestedlife import nestedlife
from lifelib.projects.ifrs17sim import ifrs17sim

for module in [simplelife, nestedlife, ifrs17sim]:
    os.chdir(os.path.dirname(module.__file__))
    module.build()
