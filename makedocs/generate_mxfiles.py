import sys
import os
import importlib

if sys.path[0] != '':
    sys.path.insert(0, '')

from lifelib import TEMPLATES

modules = [importlib.import_module('lifelib.projects.' + name + '.' + name)
           for name in TEMPLATES]

for module in modules:
    os.chdir(os.path.dirname(module.__file__))
    module.build()
