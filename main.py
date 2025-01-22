import sys
from PyQt6.QtWidgets import *
from node_editor_wnd import NodeEditorWnd
from config_parser import read_config


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_config()
    app = QApplication(sys.argv)
    wnd = NodeEditorWnd()

    sys.exit(app.exec())
