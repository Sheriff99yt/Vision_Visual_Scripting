from time import sleep

from qtpy.QtCore import *
from qtpy.QtWidgets import *


class PropertiesList(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.widget = QFrame()
        # self.setWidgetResizable(True)
        # self.setWidget(self.widget)
        self.start = True

    def varUpdate(self, name, type):
        if self.start == True:
            self.start = False
            self.widget = QFrame()
            self.setWidgetResizable(True)
            self.setWidget(self.widget)
            self.myForm = QFormLayout()
            self.myForm.setSpacing(8)
            self.myForm.setAlignment(Qt.AlignTop)
            self.widget.setLayout(self.myForm)
            self.myForm.addRow(QLabel(f"{name}"), type)
        else:
            self.myForm.addRow(QLabel(f"{name}"), type)

    def clearWnd(self):
        pass


    def infoUpdate(self):
        self.myInfo = QLabel()
