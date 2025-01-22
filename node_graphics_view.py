from PyQt6.QtWidgets import QGraphicsView, QApplication
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from node_graphics_socket import QTRGraphicsSocket
from node_graphics_edge import QTRGraphicsEdge

from node_edge import Edge, EDGE_TYPE_BEZIER
from node_graphics_cutline import QDMCutLine

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

EDGE_DRAG_START_THRESHOLD = 10

DEBUG = True


class QTRGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene
        self.is_dragging = False  # Flag to check if the view is being dragged
        self.last_pos = QPointF()
        self.is_zooming = False
        self.zoomClamp = True

        self.initUI()

        self.setScene(self.grScene)

        self.mode = MODE_NOOP
        self.editingFlag = False

        self.zoomInFactor = 1.15
        self.zoomClamp = False
        self.zoom = 10
        self.zoomStep = 0.2
        self.zoomRange = [0, 10]

        # cutline
        self.cutline = QDMCutLine()
        self.grScene.addItem(self.cutline)

    def initUI(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing |
                            QPainter.RenderHint.SmoothPixmapTransform |
                            QPainter.RenderHint.TextAntialiasing)

        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # MouseButton.MiddleButton

        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):
        # Create a QMouseEvent for a mouse button release with appropriate event details
        releaseEvent = QMouseEvent(
            QEvent.Type.MouseButtonRelease,  # Event type
            event.scenePosition(),  # Position of the mouse event (relative to widget)
            event.globalPosition(),  # Global position of the mouse
            Qt.MouseButton.LeftButton,  # Button that was released
            Qt.MouseButton.NoButton,  # No button pressed after release
            event.modifiers()  # Any keyboard modifiers (e.g., Shift, Ctrl)
        )

        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        # Create a fake QMouseEvent for simulating a mouse press with the Left Button
        fakeEvent = QMouseEvent(
            event.type(),  # Original event type (e.g., MouseMove, MousePress)
            event.scenePosition(),  # Local position of the event relative to the widget
            event.globalPosition(),  # Global position of the event
            Qt.MouseButton.LeftButton,  # Simulating Left Button being pressed
            event.buttons(),  # The current state of mouse buttons (pressed buttons)
            event.modifiers()  # Any active modifiers (e.g., Shift, Ctrl)
        )

        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(
            event.type(),  # Original event type (e.g., MouseMove, MousePress)
            event.scenePosition(),  # Local position of the event relative to the widget
            event.globalPosition(),  # Global position of the event
            Qt.MouseButton.LeftButton,  # Simulating Left Button being pressed
            event.buttons(),  # The current state of mouse buttons (pressed buttons)
            event.modifiers()  # Any active modifiers (e.g., Shift, Ctrl)
        )
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

    def leftMouseButtonPress(self, event):
        # get item which we clicked on
        item = self.getItemAtClick(event)

        # we store the position of last LMB click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        if DEBUG:
            print("LMB Click on", item, self.debug_modifiers(event))

        # logic
        if hasattr(item, "node") or isinstance(item, QTRGraphicsEdge)  or item is None:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(
                    QEvent.Type.MouseButtonPress,
                    event.scenePosition(),
                    event.globalPosition(),
                    Qt.MouseButton.LeftButton,
                    # Qt.MouseButton.NoButton,
                    event.buttons() | Qt.MouseButton.LeftButton,
                    event.modifiers() | Qt.KeyboardModifier.ControlModifier
                )
                super().mousePressEvent(fakeEvent)
                return

        # logic
        if type(item) is QTRGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res:
                return

        if item is None:
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(
                    QEvent.Type.MouseButtonRelease,
                    event.scenePosition(),
                    event.scenePosition(),
                    Qt.MouseButton.LeftButton,
                    Qt.MouseButton.NoButton,
                    event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)
                return

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        # get item which we release mouse button on
        item = self.getItemAtClick(event)

        if hasattr(item, "node") or isinstance(item, QTRGraphicsEdge) or item is None:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(
                    event.type(),
                    event.scenePosition(),
                    event.globalPosition(),
                    Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton,
                    event.modifiers() | Qt.KeyboardModifier.ControlModifier
                )
                super().mouseReleaseEvent(fakeEvent)
                return

        # logic
        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item)
                if res:
                    return

        if self.mode == MODE_EDGE_CUT:
            self.cutIntersectingEdges()
            self.cutline.line_points = []
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)
            self.mode = MODE_NOOP
            return

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        item = self.getItemAtClick(event)

        if DEBUG:
            if isinstance(item, QTRGraphicsEdge):
                print('RMB DEBUG:', item.edge, ' connecting sockets:', item.edge.start_socket, '<-->', item.edge.end_socket)
            if type(item) is QTRGraphicsSocket:
                print('RMB DEBUG:', item.socket, 'has edge:', item.socket.edge)

            if item is None:
                print('SCENE:')
                print('  Nodes:')
                for node in self.grScene.scene.nodes: print('    ', node)
                print('  Edges:')
                for edge in self.grScene.scene.edges: print('    ', edge)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()

        if self.mode == MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos())
            self.cutline.line_points.append(pos)
            self.cutline.update()

        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        # when escape key is pressed
        if event.key() == Qt.Key.Key_Control:
            self.is_zooming = True

        if event.key() == Qt.Key.Key_Delete:
            if not self.editingFlag:
                self.deleteSelected()
            else:
                super().keyPressEvent(event)

        elif event.key() == Qt.Key.Key_S and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            print("Save File!")
            self.grScene.scene.saveToFile("graph.json.txt")
        elif event.key() == Qt.Key.Key_L and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            print("Load File!")
            self.grScene.scene.loadFromFile("graph.json.txt")


        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        # when escape key is pressed
        if event.key() == Qt.Key.Key_Control:
            self.is_zooming = False

    def wheelEvent(self, event):
        # if self.is_zooming:
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # calculate our zoom Factor
            zoomOutFactor = 1 / self.zoomInFactor
            clampled = False
            # calculate zoom
            if event.angleDelta().y() > 0:
                zoomFactor = self.zoomInFactor
                self.zoom += self.zoomStep
            else:
                zoomFactor = zoomOutFactor
                self.zoom -= self.zoomStep

            if self.zoom < self.zoomRange[0]:
                self.zoom = self.zoomRange[0]
                clampled = True

            if self.zoom > self.zoomRange[1]:
                self.zoom = self.zoomRange[1]
                clampled = True
            # set scene scale
            # self.scale(zoomFactor, zoomFactor)
            if not clampled:
                self.scale(zoomFactor, zoomFactor)


        elif event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            # Redirect vertical scrolling to horizontal scrolling
            scroll_amount = event.angleDelta().y()  # Get the vertical delta
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - scroll_amount)
            # self.horizontalScrollBar().setValue(2)

        else:
            # Normal scrolling
            super().wheelEvent(event)

    def cutIntersectingEdges(self):
        for ix in range(len(self.cutline.line_points) - 1):
            p1 = self.cutline.line_points[ix]
            p2 = self.cutline.line_points[ix + 1]

            for edge in self.grScene.scene.edges:
                if edge.grEdge.intersectsWith(p1, p2):
                    edge.remove()

    def deleteSelected(self):
        for item in self.grScene.selectedItems():
            if isinstance(item, QTRGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, 'node'):
                item.node.remove()

    def debug_modifiers(self, event):
        out = "MODS: "
        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            out += "SHIFT "
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            out += "CTRL "
        if event.modifiers() & Qt.KeyboardModifier.AltModifier:
            out += "ALT "
        return out

    def getItemAtClick(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):
        if DEBUG:
            print('View::edgeDragStart ~ Start dragging edge')
            print('View::edgeDragStart ~   assign Start Socket', item.socket)

        self.previousEdge = item.socket.edge
        self.last_start_socket = item.socket
        self.dragEdge = Edge(self.grScene.scene, item.socket, None, EDGE_TYPE_BEZIER)
        if DEBUG:
            print('View::edgeDragStart ~   dragEdge:', self.dragEdge)

    def edgeDragEnd(self, item):
        """ return True if skip the rest of the code """
        self.mode = MODE_NOOP
        if DEBUG:
            print('View::edgeDragEnd ~ End dragging edge')

        if type(item) is QTRGraphicsSocket:
            if item.socket != self.last_start_socket:
                if DEBUG:
                    print('View::edgeDragEnd ~   previous edge:', self.previousEdge)

                if item.socket.hasEdge():
                    item.socket.edge.remove()

                if DEBUG:
                    print('View::edgeDragEnd ~   assign End Socket', item.socket)

                if self.previousEdge is not None: self.previousEdge.remove()

                if DEBUG:
                    print('View::edgeDragEnd ~  previous edge removed')

                self.dragEdge.start_socket = self.last_start_socket
                self.dragEdge.end_socket = item.socket
                self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)

                if DEBUG:
                    print('View::edgeDragEnd ~  reassigned start & end sockets to drag edge')

                self.dragEdge.updatePositions()
                return True

        if DEBUG:
            print('View::edgeDragEnd ~ End dragging edge')

        self.dragEdge.remove()
        self.dragEdge = None

        if DEBUG:
            print('View::edgeDragEnd ~ about to set socket to previous edge:', self.previousEdge)

        if self.previousEdge is not None:
            self.previousEdge.start_socket.edge = self.previousEdge

        if DEBUG:
            print('View::edgeDragEnd ~ everything done.')

        return False

    def distanceBetweenClickAndReleaseIsOff(self, event):
        """ measures if we are too far from the last LMB click scene position """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD * EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x() * dist_scene.x() + dist_scene.y() * dist_scene.y()) > edge_drag_threshold_sq
