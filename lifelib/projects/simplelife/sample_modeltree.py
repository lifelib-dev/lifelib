from modelx.qtgui import *
import simplelife

if __name__ == "__main__":
    show_modeltree(simplelife.build(load_saved=False))
