import sys
from PyQt6.QtWidgets import *

from node_editor_window import NodeEditorWindow

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = NodeEditorWindow()

    sys.exit(app.exec())
