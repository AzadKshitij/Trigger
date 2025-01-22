from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsLineItem
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QPen


class QTRGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)

        # Create the line initially
        self.line = None
        self.createLine()

        # Tracking panning position
        self.last_pos = QPointF()

    def initUI(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing |
                            QPainter.RenderHint.SmoothPixmapTransform |
                            QPainter.RenderHint.TextAntialiasing)

        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Enable middle mouse button to move the scene
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

    def createLine(self):
        # Create a line and add it to the scene
        self.line = QGraphicsLineItem(0, 0, 200, 200)  # Line from (0,0) to (200,200)
        pen = QPen(Qt.GlobalColor.blue)  # Set the pen color to blue
        pen.setWidth(3)  # Set the pen width
        self.line.setPen(pen)  # Apply the pen to the line
        self.grScene.addItem(self.line)  # Add the line to the scene

    def updateLinePosition(self):
        # Update the position of the line to reflect the current view's position
        # Calculate the scene's translation (view's position relative to the scene)
        scene_pos = self.mapToScene(self.rect().topLeft())  # Get the top-left of the view's rectangle in scene coordinates
        self.line.setLine(0, 0, scene_pos.x(), scene_pos.y())  # Update the line's end position

    def wheelEvent(self, event):
        super().wheelEvent(event)
        self.updateLinePosition()  # Update the line when zooming

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.updateLinePosition()  # Update the line when panning


# Sample usage of the custom QGraphicsView
app = QApplication([])
scene = QGraphicsScene()
view = QTRGraphicsView(scene)
view.setScene(scene)
view.setSceneRect(-400, -300, 800, 600)  # Set scene size
view.show()
app.exec()
