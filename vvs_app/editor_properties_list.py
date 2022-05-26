from time import sleep

from qtpy.QtCore import *
from qtpy.QtWidgets import *


class PropertiesList(QScrollArea):
    def __init__(self, parent=None, master_ref =None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.master_ref = master_ref
        self.myForm = None

    def clear_properties(self):
        widget = QFrame()
        self.setWidget(widget)
        self.myForm = None


    def create_properties_widget(self, name, widget):
        if self.myForm:
            self.myForm.addRow(QLabel(f"{name}"), widget)
        else:
            self.myForm = QFormLayout()
            widget = QFrame()
            self.setWidget(widget)
            widget.setLayout(self.myForm)
            self.myForm.setSpacing(8)
            self.myForm.setAlignment(Qt.AlignTop)
            self.myForm.addRow(QLabel(f"{name}"), widget)

    def create_order_wdg(self):
        grNodesRef = self.master_ref.currentNodeEditor().scene.getSelectedItems()
        if grNodesRef and len(grNodesRef) == 1:
                self.order = QSpinBox()
                node = grNodesRef[0].node
                self.order.setValue(node.getNodeOrder())
                self.order.valueChanged.connect(self.orderChanged)
                self.myForm.addRow(QLabel(f"Node Order"), self.order)

    def orderChanged(self):
        i = self.node.scene.nodes
        if self.order.value() > len(i)-1:
            self.order.setValue(len(i)-1)
        i[self.node.getNodeOrder()], i[self.order.value()] = i[self.order.value()], i[self.node.getNodeOrder()]

        self.node.scene.node_editor.UpdateTextCode()
