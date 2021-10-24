import sys, shutil
import pathlib
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
    {"dir": "libraries",
     "project": "savings",
     "notebook": "savings_example1.ipynb",
     "is_target": lambda node: True,
     "proc": lambda node: None},

    {"dir": "libraries",
     "project": "basiclife",
     "notebook": "generate_model_points.ipynb",
     "is_target": lambda node: True,
     "proc": lambda node: None},

    {"dir": "libraries",
     "project": "basiclife",
     "notebook": "generate_model_points_with_duration.ipynb",
     "is_target": lambda node: True,
     "proc": lambda node: None},

    {"dir": "libraries",
     "project": "basiclife",
     "notebook": "create_premium_table.ipynb",
     "is_target": lambda node: True,
     "proc": lambda node: None},

    {"dir": "projects",
     "project": "fastlife",
     "notebook": "fastlife-introduction.ipynb",
     "is_target": lambda node: True,
     "proc": lambda node: None},

    {"dir": "projects",
     "project": "simplelife",
     "notebook": "simplelife-space-overview.ipynb",
     "is_target": is_target_simplelife,
     "proc": lambda node: None},

    {"dir": "projects",
     "project": "ifrs17sim",
     "notebook": "ifrs17sim_csm_waterfall.ipynb",
     "is_target": is_target_ifrs17sim,
     "proc": proc_ifrs17sim},

    {"dir": "projects",
     "project": "ifrs17sim",
     "notebook": "ifrs17sim_charts_baseline.ipynb",
     "is_target": is_target_ifrs17sim,
     "proc": proc_ifrs17sim},

    {"dir": "projects",
     "project": "ifrs17sim",
     "notebook": "ifrs17sim_charts_lapsescen.ipynb",
     "is_target": is_target_ifrs17sim,
     "proc": proc_ifrs17sim},

    {"dir": "projects",
     "project": "smithwilson",
     "notebook": "smithwilson-overview.ipynb",
     "is_target": lambda node: True,
     "proc": lambda node: None}
]


def adjust_notebook(file, is_target, proc):

    nb = nbformat.read(file, as_version=nbformat.NO_CONVERT)
    try:
        node = next(c for c in nb.cells if is_target(c))
        proc(node)
    except StopIteration:
        pass
    return nb


thisdir = pathlib.Path(os.path.abspath(os.path.dirname(__file__))).as_posix()


def _get_dirs(project, dir_):

    return (thisdir + '/../lifelib/'+ dir_ + '/' + project,
            thisdir + '/source/' + dir_ + '/notebooks/' + project)


def prepare_notebooks():

    for entry in entries:

        entry = entry.copy()    # To not delete global entries directory
        project = entry.pop("project")
        notebook = entry.pop("notebook")
        dir_ = entry.pop("dir")
        srcdir, trgdir = _get_dirs(project, dir_)

        nb = adjust_notebook(srcdir + '/' + notebook, **entry)

        if not os.path.exists(trgdir):
            pathlib.Path(trgdir).mkdir(parents=True)

        nbformat.write(nb, trgdir + '/' + notebook)


def prepare_models():

    for entry in entries:
        project = entry["project"]
        dir_ = entry["dir"]
        srcdir, trgdir = _get_dirs(project, dir_)

        srcmodel = srcdir + "/" + "model"
        trgmodel = trgdir + "/" + "model"
        if os.path.exists(srcmodel) and os.path.isdir(srcmodel) and not os.path.exists(trgmodel):
            shutil.copytree(srcmodel, trgdir + "/" + "model")


def remove_notebooks():

    for nbdir in (thisdir + "/source/libraries/notebooks",
                  thisdir + "/source/projects/notebooks"):
        if os.path.exists(nbdir):
            shutil.rmtree(nbdir)


if __name__ == "__main__":
    arg = sys.argv[1]
    if arg == "prepare":
        prepare_notebooks()
        prepare_models()
    elif arg == "remove":
        remove_notebooks()
    else:
        raise KeyError
