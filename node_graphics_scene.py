from math import floor, ceil
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtCore import QLine, Qt, QPointF


class QTRGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene

        # Settings
        self.gridSize = 20
        self.gridSquares = 5

        self._color_background = QColor("#21252b")
        self._color_light = QColor("#282c34")
        self._color_dark = QColor("#292929")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)

    def setGrScene(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # create grid
        l, r, t, b = int(floor(rect.left())), int(ceil(rect.right())), \
            int(floor(rect.top())), int(ceil(rect.bottom()))

        f_left = l - (l % self.gridSize)
        f_top = t - (t % self.gridSize)

        # compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(f_left, r, self.gridSize):
            if x % (self.gridSize * self.gridSquares) != 0:
                lines_light.append(QLine(x, t, x, b))
            else:
                lines_dark.append(QLine(x, t, x, b))

        for y in range(f_top, b, self.gridSize):
            if y % (self.gridSize * self.gridSquares) != 0:
                lines_light.append(QLine(l, y, r, y))
            else:
                lines_dark.append(QLine(l, y, r, y))

        # draw lines
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)
