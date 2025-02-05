from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from node_scene import Scene
from node_node import Node
from node_edge import Edge, EDGE_TYPE_BEZIER, EDGE_TYPE_DIRECT
from node_graphics_view import QTRGraphicsView


class NodeEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stylesheet_filename = 'qss/nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # create graphic scene

        self.scene = Scene()
        self.addNodes()

        # create graphic view

        self.view = QTRGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        # self.addDebugContent()

    def addDebugContent(self):
        greenBrush = QBrush(QColor("#6ac977"))
        outlinePen = QPen(QColor("#000000"))
        outlinePen.setWidth(2)

        rect = self.grScene.addRect(-100, -100, 80,
                                    100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        text = self.grScene.addText(
            "This is my Awesome text!", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        text.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QPushButton("Hello World")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        proxy2.setPos(0, 60)

        line = self.grScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        line.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

    def addNodes(self):
        node1 = Node(self.scene, "My Awesome Node 1",
                     inputs=[0, 0, 0], outputs=[1])
        node2 = Node(self.scene, "My Awesome Node 2",
                     inputs=[3, 3, 3], outputs=[1])
        node3 = Node(self.scene, "My Awesome Node 3",
                     inputs=[2, 2, 2], outputs=[1])
        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -150)

    def loadStylesheet(self, filename):

        # Open the file
        file = QFile(filename)
        if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            # Read all contents
            stylesheet = file.readAll()
            # Convert QByteArray to a Python string with proper encoding
            stylesheet_str = str(stylesheet, encoding='utf-8')
            # Apply the stylesheet to the application
            QApplication.instance().setStyleSheet(stylesheet_str)
            file.close()  # Don't forget to close the file after use
        else:
            print(f"Failed to open file: {filename}")
