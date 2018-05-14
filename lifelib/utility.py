
import sys, os

def set_projdir(file):
    """Set the current folder to the folder containing `file`.

    Returns:
        path to the current folder
    """

    proj_dir = os.path.abspath(os.path.dirname(file))
    if sys.path[0] == '':
        os.chdir(proj_dir)
    elif proj_dir not in sys.path:
        sys.path.insert(0, proj_dir)

    return proj_dir