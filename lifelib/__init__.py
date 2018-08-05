import os.path

VERSION = (0, 0, 10, 'dev')
__version__ = '.'.join([str(x) for x in VERSION])
LIB_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(LIB_DIR, 'projects')
TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR)
             if os.path.isdir(os.path.join(TEMPLATE_DIR, f))]

