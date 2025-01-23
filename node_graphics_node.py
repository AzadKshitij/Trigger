from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *



class QTRGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.content = self.node.content

        self._title_color = QColor("#ffffff")
        self._title_font = QFont("Arial", 10)

        self.width = 180
        self.height = 240
        self.edge_size = 10.0
        self.title_height = 24.0
        self._padding = 4.0

        self._pen_width = 1.5  # Pen width for outline
        self._pen_default = QPen(QColor("#7F000000"), self._pen_width)
        self._pen_selected = QPen(QColor("#FFFFA637"), self._pen_width)

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

        self.initTitle()
        self.title = self.node.title

        # init socket
        self.initSockets()

        self.initContent()
        self.initUI()
        self.wasMoved = False

    @property
    def title(self): return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def boundingRect(self):
        padding = self._pen_width / 2  # Adjust for outline width
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(
            self.width
            - 2 * self._padding
        )

    def initContent(self):
        # Ensure self.content is properly initialized as a QWidget (or a subclass)
        if not hasattr(self, 'content') or self.content is None:
            self.content = QWidget()  # Replace with any specific widget type you need

        # Create the QGraphicsProxyWidget to embed the content widget into the graphics item
        self.grContent = QGraphicsProxyWidget(self)

        # Cast the geometry values to integers to avoid the TypeError
        x = int(self.edge_size)
        y = int(self.title_height + self.edge_size)
        width = int(self.width - 2 * self.edge_size)
        height = int(self.height - 2 * self.edge_size - self.title_height)

        # Set the geometry for self.content inside the graphics item
        self.content.setGeometry(x, y, width, height)

        # Set the widget for the proxy
        self.grContent.setWidget(self.content)


    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = None) -> None:
        # Title background
        path_title = QPainterPath()
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title)

        # Content background
        path_content = QPainterPath()
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size,
                                    self.edge_size)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content)

        # Outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        pen = self._pen_selected if self.isSelected() else self._pen_default
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path_outline)

    def initSockets(self):
        pass

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # optimize me! just update the selected nodes
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()

                self.wasMoved = True

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if self.wasMoved:
            self.wasMoved = False
            self.node.scene.history.storeHistory("Node moved")
