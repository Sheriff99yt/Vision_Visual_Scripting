from qtpy.QtCore import *
from qtpy.QtWidgets import *


class PropertiesList(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ListOfItems = None
        self.myLayout = QFormLayout()
        self.setLayout(self.myLayout)
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

            self.myLayout.addRow(lbl, lbl2)

