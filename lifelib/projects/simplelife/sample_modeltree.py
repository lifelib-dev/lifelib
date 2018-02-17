from modelx.qtgui import *
import simplelife

if __name__ == "__main__":
    simplelife.load_input = True
    show_modeltree(simplelife.build())
