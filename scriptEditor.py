from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from scriptGraphicsView import MyGraphicsView

from scriptGraphicsScene import MyGraphicsScene

class ScriptEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI

    def initUI(self):

        self.setGeometry(100, 100, 1600, 800)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.graphicScene = MyGraphicsScene()

        self.view = MyGraphicsView(self.graphicScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Script Graph")

        self.show()

        self.addDebugContent()



    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)


        rect = self.graphicScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.graphicScene.addText("This is my Awesome text!", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))


        widget1 = QPushButton("Hello World")
        proxy1 = self.graphicScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)


        widget2 = QTextEdit()
        proxy2 = self.graphicScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)


        line = self.graphicScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)
