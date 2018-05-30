import sys
from modelx.qtgui import get_modeltree
from qtpy.QtWidgets import QApplication

import simplelife

if __name__ == "__main__":

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    view = get_modeltree(simplelife.build(load_saved=False))
    view.show()
    app.exec_()
