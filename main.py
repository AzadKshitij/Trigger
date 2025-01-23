import sys
from PyQt6.QtWidgets import *
from node_editor_widget import NodeEditorWidget
from config_parser import read_config


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_config()
    app = QApplication(sys.argv)
    wnd = NodeEditorWidget()

    sys.exit(app.exec())
