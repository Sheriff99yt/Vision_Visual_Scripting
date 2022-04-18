from time import sleep

from qtpy.QtCore import *
from qtpy.QtWidgets import *


class PropertiesList(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWidgetResizable(True)

        self.varStart = True
        self.infoStart = True


    def detailsUpdate(self, name, type, grNodesRef):

        if self.varStart == True:
            self.varStart = False
            self.infoStart = True

            widget = QFrame()
            self.setWidget(widget)
            self.myForm = QFormLayout()
            widget.setLayout(self.myForm)
            self.myForm.setSpacing(8)
            self.myForm.setAlignment(Qt.AlignTop)

            if grNodesRef and len(grNodesRef) == 1:
                self.order = QSpinBox()
                self.nodeRef = grNodesRef[0].node
                self.order.setValue(self.nodeRef.getNodeOrder())
                self.order.valueChanged.connect(self.orderChanged)
                self.myForm.addRow(QLabel(f"Node Order"), self.order)

            self.myForm.addRow(QLabel(f"{name}"), type)
        else:
            self.myForm.addRow(QLabel(f"{name}"), type)

    def orderChanged(self):
        i = self.nodeRef.scene.nodes
        if self.order.value() > len(i)-1:
            self.order.setValue(len(i)-1)
        i[self.nodeRef.getNodeOrder()], i[self.order.value()] = i[self.order.value()], i[self.nodeRef.getNodeOrder()]

        self.nodeRef.scene.NodeEditor.UpdateTextCode()


