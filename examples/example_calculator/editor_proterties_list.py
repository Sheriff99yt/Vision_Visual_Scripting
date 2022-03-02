from qtpy.QtCore import *
from qtpy.QtWidgets import *


class PropertiesList(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ListOfItems = None
        self.myLayout = QHBoxLayout()
        self.setLayout(self.myLayout)

        self.nameList = QVBoxLayout()
        self.optionList = QVBoxLayout()
        self.nameList.setAlignment(Qt.AlignTop)
        self.optionList.setAlignment(Qt.AlignTop)
        self.myLayout.addLayout(self.nameList)
        self.myWidget = QFrame()

        self.nameList.addWidget(self.myWidget)

        self.myLayout.addLayout(self.optionList)

        self.initUI()

    def initUI(self):
        # init
        x = {"name": "First settings", "color": "yellow"}
        y = {"name": "Second settings", "color": "blue"}

        self.ListOfItems = [x, y, x, y, x, y, x, y, x, y, x, y, x, y, x, y, x, y, x, y, x, y, x, y]

        self.UpdateDetailsList()

    # @TODO: To Be Coded

    def UpdateDetailsList(self):
        for Item in self.ListOfItems:
            lbl = QLabel(Item.get("name"))
            lbl2 = QLabel(Item.get("color"))

            # lbl.adjustSize()
            # lbl2.adjustSize()

            self.nameList.addWidget(lbl)
            self.optionList.addWidget(lbl2)
