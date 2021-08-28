import os.path as path
from lifelib._dirs import TEMPLATES

proj_dir = path.normpath(path.dirname(path.abspath(__file__)) + "\\..")

projects = TEMPLATES

def inplace_change(filename, oldstr, newstr):
    # Code taken from:
    # https://stackoverflow.com/questions/4128144/replace-string-within-file-contents

    # Safely read the input filename using 'with'
    with open(filename, mode='r', encoding='utf-8') as f:
        s = f.read()
        if oldstr not in s:
            print('"{oldstr}" not found in {filename}.'.format(**locals()))
            return

    # Safely write the changed content, if found in the file
    msg = 'Changing "{oldstr}" to "{newstr}" in {filename}'.format(**locals())
    with open(filename, mode='w', encoding='utf-8') as f:
        print(msg)
        s = s.replace(oldstr, newstr)
        f.write(s)


for prj in projects:
    s = (proj_dir + "\\lifelib\\projects\\" + prj + "\\").replace("\\", "\\\\")
    trg = ".\\build\\html\\projects\\generated\\" + prj + ".build_input.html"
    if path.exists(trg):
        inplace_change(trg, s, '')
