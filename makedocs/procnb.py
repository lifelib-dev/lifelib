import os
import re
import nbformat

# Update and copy Jupyter notebooks to be built as static pages by nbsphinx

def is_target_simplelife(node):
    return (node['cell_type'] == 'code'
            and re.match("^import simplelife", node['source']))


def proc_simplelife(node):
    node['metadata']['nbsphinx'] = 'hidden'

    src = re.sub(
        "import simplelife",
        "import lifelib.projects.simplelife.simplelife as simplelife",
        node['source']
    )
    node['source'] = src


def is_target_ifrs17sim(node):
    return (node['cell_type'] == 'code'
            and re.match("^%matplotlib notebook", node['source']))


def proc_ifrs17sim(node):
    node['metadata']['nbsphinx'] = 'hidden'
    src = re.sub(
        "^%matplotlib notebook",
        "%matplotlib inline",
        node['source']
    )
    src = re.sub(
        "import ifrs17sim",
        "import lifelib.projects.ifrs17sim.ifrs17sim as ifrs17sim",
        src
    )
    src = re.sub(
        "from draw_charts import draw_waterfall",
        "from lifelib.projects.ifrs17sim.draw_charts import draw_waterfall",
        src
    )
    node['source'] = src

entries = [

    {"project": "simplelife",
     "notebook": "simplelife-space-overview.ipynb",
     "is_target": is_target_simplelife,
     "proc": proc_simplelife},

    {"project": "ifrs17sim",
     "notebook": "ifrs17sim_csm_waterfall.ipynb",
     "is_target": is_target_ifrs17sim,
     "proc": proc_ifrs17sim},

    {"project": "ifrs17sim",
     "notebook": "ifrs17sim_charts_baseline.ipynb",
     "is_target": is_target_ifrs17sim,
     "proc": proc_ifrs17sim},

    {"project": "ifrs17sim",
     "notebook": "ifrs17sim_charts_lapsescen.ipynb",
     "is_target": is_target_ifrs17sim,
     "proc": proc_ifrs17sim}
]

def adjust_notebook(file, is_target, proc):

    nb = nbformat.read(file, as_version=nbformat.NO_CONVERT)
    node = next(c for c in nb.cells if is_target(c))
    proc(node)
    return nb


thisdir = os.path.abspath(os.path.dirname(__file__))


for entry in entries:
    project = entry.pop("project")
    notebook = entry.pop("notebook")
    os.chdir(thisdir + '/../lifelib/projects/' + project)
    nb = adjust_notebook(notebook, **entry)
    os.chdir(thisdir + '/source/projects')
    if os.path.isfile(notebook):
        os.remove(notebook)
    nbformat.write(nb, notebook)
