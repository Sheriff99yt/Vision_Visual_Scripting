from qtpy.QtWidgets import *
from qtpy.QtCore import Qt
from examples.example_calculator.nodes_configuration import set_function_ID, FUN_INPUT
from examples.example_calculator.master_node import MasterNode, MasterGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException


class CalcInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("1", self)
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)

    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@set_function_ID(FUN_INPUT)
class MasterNode_Input(MasterNode):
    icon = "icons/in.png"
    node_type = FUN_INPUT
    name = "Input"
    content_label_objname = "calc_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        pass

    def initInnerClasses(self):
        self.content = CalcInputContent(self)
        self.grNode = MasterGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)