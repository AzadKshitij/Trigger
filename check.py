from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QMouseEvent, QPainter, QPen
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem, QApplication


class CustomGraphicsView(QGraphicsView):

    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        self.is_dragging = False  # Flag to check if the view is being dragged
        self.last_pos = QPointF()  # Last mouse position during drag

        # Call the function to draw a line when the view is created
        self.draw_line()

    def mousePressEvent(self, event: QMouseEvent):
        # Handle middle mouse button press to start panning
        if event.button() == Qt.MouseButton.MiddleButton:
            self.is_dragging = True
            self.last_pos = event.globalPosition()  # Record initial mouse position
            self.setCursor(Qt.CursorShape.ClosedHandCursor)  # Change cursor to closed hand
        else:
            # Handle other mouse buttons (left or right) normally
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        # Handle middle mouse button release to stop panning
        if event.button() == Qt.MouseButton.MiddleButton:
            self.is_dragging = False
            self.setCursor(Qt.CursorShape.ArrowCursor)  # Reset cursor to normal arrow
        else:
            # Handle other mouse buttons (left or right) normally
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        # Handle mouse move during dragging
        if self.is_dragging:
            # Calculate the offset from the last mouse position
            delta = self.last_pos - event.globalPosition()
            self.last_pos = event.globalPosition()  # Update last mouse position

            # Move the scene (i.e., move the contents of the view)
            self.translateScene(delta.x(), delta.y())

        else:
            super().mouseMoveEvent(event)

    def translateScene(self, dx, dy):
        # Translate the scene by the given delta
        scene_rect = self.sceneRect()
        new_scene_rect = scene_rect.translated(dx, dy)
        self.setSceneRect(new_scene_rect)  # Move the scene within the view

    def draw_line(self):
        # Draw a line in the scene
        line_item = QGraphicsLineItem(0, 0, 100, 100)  # Line from (0, 0) to (100, 100)

        # Customize the line's appearance (optional)
        pen = QPen(Qt.GlobalColor.blue)
        pen.setWidth(3)
        line_item.setPen(pen)

        # Add the line to the scene
        self.scene().addItem(line_item)


# Sample usage of the custom QGraphicsView
app = QApplication([])
scene = QGraphicsScene()
view = CustomGraphicsView(scene)
view.setScene(scene)
view.setSceneRect(-400, -300, 800, 600)  # Set scene size
view.show()
app.exec()
