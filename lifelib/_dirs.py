import os.path

LIB_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(LIB_DIR, 'projects')
TEMPLATE_V0_DIR = os.path.join(LIB_DIR, 'projects_v0')
TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR)
             if os.path.isdir(os.path.join(TEMPLATE_DIR, f)) and f[0] != '_']
DEFAULT_TEMPLATE = "simplelife"
