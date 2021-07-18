import os.path

_here = os.path.abspath(os.path.dirname(__file__))


TEMPLATE_DIRS = [
    os.path.join(_here, 'libraries'),
    os.path.join(_here, 'projects')
]

# dict of library paths
TEMPLATES = {}
for d in TEMPLATE_DIRS:
    for f in os.listdir(d):
        fullpath = os.path.join(d, f)
        if os.path.isdir(fullpath) and f[0] != '_':
            TEMPLATES[f] = fullpath

DEFAULT_TEMPLATE = "basiclife"

