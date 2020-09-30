import sys
import os.path
import argparse
import shutil
from lifelib._dirs import (
    TEMPLATE_DIR, TEMPLATE_V0_DIR, TEMPLATES, DEFAULT_TEMPLATE)


def get_argparser():
    parse = argparse.ArgumentParser(description="Create a new project.")
    parse.add_argument('proj_dir',
                       help="Path to the project folder")
    parse.add_argument('--template', default=DEFAULT_TEMPLATE,
                       help="Name of a template project")
    return parse


def main(argv=sys.argv[1:]):
    """Create a new project."""

    args = vars(get_argparser().parse_args(argv))

    if args['template'] not in TEMPLATES:
        raise ValueError("Template %s not found" % args['template'])
    else:
        template = args['template']

    create(template, args['proj_dir'])

    return 0


def create(template=DEFAULT_TEMPLATE, path=None):
    """Create new project folder from template.

    Args:
        template(:obj:`str`, optional): name of a project template.
            Defaults to ``simplelife``.
        path(:obj:`str`, optional): path to the project folder. Absolute path
            or relative path to the current working directory/folder.
            If omitted, ``template`` is used.
    """

    if not path:
        path = template

    proj_dir = os.path.abspath(path)
    tpath = os.path.join(TEMPLATE_DIR, template)
    shutil.copytree(tpath, proj_dir)


def create_v0(template=DEFAULT_TEMPLATE, path=None):
    """Create new project folder from old project.

    Args:
        template(:obj:`str`, optional): name of a project template.
            Defaults to ``simplelife``.
        path(:obj:`str`, optional): path to the project folder. Absolute path
            or relative path to the current working directory/folder.
            If omitted, ``template`` is used.
    """

    if not path:
        path = template

    proj_dir = os.path.abspath(path)
    tpath = os.path.join(TEMPLATE_V0_DIR, template)
    shutil.copytree(tpath, proj_dir)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
