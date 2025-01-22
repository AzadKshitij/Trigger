from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class QTRGraphicsSocket(QGraphicsItem):
    def __init__(self, socket, socket_type=1):
        self.socket = socket
        super().__init__(socket.node.grNode)

        self.radius = 6
        self.outline_width = 1.0
        self._colors = [
            QColor("#FFFF7700"),
            QColor("#FF52e220"),
            QColor("#FF0056a6"),
            QColor("#FFa86db1"),
            QColor("#FFb54747"),
            QColor("#FFdbe220"),
        ]
        self._color_background = self._colors[socket_type]

        self._color_outline = QColor("#FF000000")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = None) -> None:
        # painting circle
        if not hasattr(self, 'radius') or self.radius <= 0:
            return
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        # Calculate the position for the circle (centered at (0, 0))
        painter.translate(self.boundingRect().center())
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def boundingRect(self):
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )
