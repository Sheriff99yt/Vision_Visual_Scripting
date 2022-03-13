from time import sleep

from qtpy.QtCore import *
from qtpy.QtWidgets import *


class PropertiesList(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.widget = QFrame()
        # self.setWidgetResizable(True)
        # self.setWidget(self.widget)
        self.varStart = True
        self.infoStart = True

    def varUpdate(self, name, type):

        if self.varStart == True:
            self.varStart = False
            self.infoStart = True

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


    def infoUpdate(self, Info):
        if self.infoStart == True:
            self.infoStart = False
            self.varStart = True
            widget = QFrame()
            self.setWidget(widget)
            self.infoLayout = QHBoxLayout()
            widget.setLayout(self.infoLayout)
            self.infoLayout.addWidget(Info)
        else:
            self.infoLayout.addWidget(Info)

