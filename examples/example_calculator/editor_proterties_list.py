from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *

from examples.example_calculator.nodes_configuration import *
from nodeeditor.utils import dumpException


class PropertiesList(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.myLayout = QHBoxLayout()
        self.setLayout(self.myLayout)

        self.nameList = QVBoxLayout()
        self.optionList = QVBoxLayout()
        self.nameList.setAlignment(Qt.AlignTop)
        self.optionList.setAlignment(Qt.AlignTop)
        self.myLayout.addLayout(self.nameList)
        self.Twidget =QFrame()

        self.nameList.addWidget(self.Twidget)


        self.myLayout.addLayout(self.optionList)

        self.initUI()


    def initUI(self):
        # init


        x = {"name": "First settings", "color": "yellow"}
        y = {"name": "Second settings", "color": "blue"}

        self.ListOfItems = [x,y,x,y]


        self.UpdateDetailsList()


#@TODO: To Be Coded

    def UpdateDetailsList(self):
        for Item in self.ListOfItems:
            self.nameList.addWidget(QLabel(Item.get("name")))
            self.optionList.addWidget(QLabel(Item.get("color")))


        # self.optionList.addStretch()
        # self.nameList.addStretch()
