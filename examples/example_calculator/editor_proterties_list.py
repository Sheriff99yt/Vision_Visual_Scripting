from time import sleep

from qtpy.QtCore import *
from qtpy.QtWidgets import *


class PropertiesList(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWidgetResizable(True)

        self.varStart = True
        self.infoStart = True


    def varUpdate(self, name, type):

        if self.varStart == True:
            self.varStart = False
            self.infoStart = True

            widget = QFrame()
            self.setWidget(widget)
            self.myForm = QFormLayout()
            widget.setLayout(self.myForm)
            self.myForm.setSpacing(8)
            self.myForm.setAlignment(Qt.AlignTop)
            self.myForm.addRow(QLabel(f"{name}"), type)
        else:
            self.myForm.addRow(QLabel(f"{name}"), type)


    def infoUpdate(self, Info):
        if self.infoStart == True:
            self.infoStart = False
            self.varStart = True
            widget = QFrame()
            self.setWidget(widget)
            self.infoLayout = QVBoxLayout()
            self.infoLayout.setAlignment(Qt.AlignTop)
            widget.setLayout(self.infoLayout)
            self.infoLayout.addWidget(Info)
        else:
            self.infoLayout.addWidget(Info)

