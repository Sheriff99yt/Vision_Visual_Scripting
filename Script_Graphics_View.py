from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MyGraphicsView(QGraphicsView):
    def __init__(self, graphicScene, parent=None):
        super().__init__(parent)

        self.zoomInFactor = 1.1
        self.maxZoom = 15
        self.minZoom = 1
        self.zoomSteps = self.maxZoom // 2

        self.graphicScene = graphicScene

        self.initUI()

        self.setScene(self.graphicScene)

    def initUI(self):
        self.setRenderHints(
            QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.rightMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonPress(self, event):
        return super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        return super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        return super().mousePressEvent(event)

    def rightMouseButtonRelease(self, event):
        return super().mouseReleaseEvent(event)

    def wheelEvent(self, event):

        if event.angleDelta().y() > 0:
            if self.zoomSteps >= self.maxZoom:
                print("Can't")
            else:
                self.zoomSteps += 1
                print("Zoom In", self.zoomSteps)
                self.scale(1 * self.zoomInFactor, 1 * self.zoomInFactor)
        else:
            if self.zoomSteps <= self.minZoom:
                print("Can't")
            else:
                self.zoomSteps -= 1
                print("Zoom Out", self.zoomSteps)
                self.scale(1 / self.zoomInFactor, 1 / self.zoomInFactor)
