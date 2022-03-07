from time import sleep

from qtpy.QtCore import *
from qtpy.QtWidgets import *


class PropertiesList(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.widget = QFrame()
        self.setWidgetResizable(True)
        self.setWidget(self.widget)


    def varUpdate(self,name,type):
        def initVar(self):
            start = False
            if start == False:
                start = True
                self.myForm = QFormLayout()
                self.myForm.setAlignment(Qt.AlignTop)
                self.widget.setLayout(self.myForm)
                self.myForm.addRow(QLabel(f"{name}"), type)
            else:
                self.myForm.addRow(QLabel(f"{name}"), type)



    def infoUpdate(self):
        self.myInfo = QLabel()
