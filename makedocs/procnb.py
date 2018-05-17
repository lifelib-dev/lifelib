import os
import re
import nbformat


def adjust_notebook(file):
    nb = nbformat.read(file, as_version=nbformat.NO_CONVERT)

    def is_target(node):
        return (node['cell_type'] == 'code'
                and re.match("^%matplotlib notebook", node['source']))

    def is_mdtarget(node):
        return (node['cell_type'] == 'markdown')

    node = next(c for c in nb.cells if is_target(c))

    node['metadata']['nbsphinx'] = 'hidden'

    src = re.sub("^%matplotlib notebook",
                 "%matplotlib inline", node['source'])

    src = re.sub("import ifrs17sim",
                 "import lifelib.projects.ifrs17sim.ifrs17sim as ifrs17sim",
                 src)

    src = re.sub("from draw_charts import draw_waterfall",
                 "from lifelib.projects.ifrs17sim.draw_charts import draw_waterfall",
                 src)

    node['source'] = src
    return nb


notebook = 'ifrs17sim-demo.ipynb'
os.chdir('../lifelib/projects/ifrs17sim')
nb = adjust_notebook(notebook)
os.chdir(os.path.abspath(os.path.dirname(__file__)) + '/source/projects')
if os.path.isfile(notebook):
    os.remove(notebook)
nbformat.write(nb, notebook)