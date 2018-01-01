import sys
import os.path
import argparse
import shutil
from lifelib import TEMPLATE_DIR, TEMPLATES


def get_argparser():
    parse = argparse.ArgumentParser(description="Create a new project.")
    parse.add_argument('proj_dir',
                       help="Path to the project folder")
    parse.add_argument('--template', default='simplelife',
                       help="Name of a template project")
    return parse


def main(argv=sys.argv[1:]):
    """Create a new project."""

    args = vars(get_argparser().parse_args(argv))

    proj_dir = os.path.abspath(args['proj_dir'])

    if args['template'] not in TEMPLATES:
        raise "Template %s not found" % args['template']
    else:
        template = args['template']

    tpath = os.path.join(TEMPLATE_DIR, template)

    shutil.copytree(tpath, proj_dir)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
