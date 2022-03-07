from PyQt5.QtWidgets import QDoubleSpinBox, QLineEdit

from examples.example_calculator.nodes_configuration import *
from examples.example_calculator.master_node import MasterNode
from examples.example_calculator.editor_proterties_list import PropertiesList


@register_node(VAR_FLOAT, Fun=False)
class FloatVar(MasterNode):
    icon = ""
    node_ID = VAR_FLOAT
    op_title = "Float Var"
    content_label_objname = "var_node_float"

    def __init__(self, scene, isFun=False):
        super().__init__(scene, inputs=[], outputs=[1])
        self.isVar = True
        self.name = self.outputs[0].socketName
        self.value = self.outputs[0].socketValue

    def getNodeCode(self):
        code = f"""{self.name}={self.value}"""
        return self.name

    def updateProperties(self):
        PropertiesList.varUpdate("Variable Name", QLineEdit().setValue(self.name))
        PropertiesList.varUpdate("Variable Value", QDoubleSpinBox().setValue(self.value))


@register_node(VAR_INTEGER, Fun=False)
class IntegerVar(MasterNode):
    icon = ""
    node_ID = VAR_INTEGER
    op_title = "Integer Var"
    content_label_objname = "var_node_integer"

    def __init__(self, scene, isFun=False):
        super().__init__(scene, inputs=[], outputs=[2])
        self.isVar = True

    def getNodeCode(self):
        name = self.outputs[0].socketName
        value = self.outputs[0].socketValue
        self.outputs[0].socketValue = "8"

        code = f"""{name}={value}"""
        return name


@register_node(VAR_BOOLEAN, Fun=False)
class BooleanVar(MasterNode):
    icon = ""
    node_ID = VAR_BOOLEAN
    op_title = "Boolean Var"
    content_label_objname = "var_node_boolean"

    def __init__(self, scene, isFun=False):
        super().__init__(scene, inputs=[], outputs=[3])
        self.isVar = True

    def getNodeCode(self):
        name = self.outputs[0].socketName
        value = self.outputs[0].socketValue

        code = f"""{name}={value}"""
        return name


@register_node(VAR_STRING, Fun=False)
class StringVar(MasterNode):
    icon = ""
    node_ID = VAR_STRING
    op_title = "String Var"
    content_label_objname = "var_node_string"

    def __init__(self, scene, isFun=False):
        super().__init__(scene, inputs=[], outputs=[4])
        self.isVar = True

    def getNodeCode(self):
        name = self.outputs[0].socketName
        value = self.outputs[0].socketValue

        code = f"""{name}={value}"""
        return name
