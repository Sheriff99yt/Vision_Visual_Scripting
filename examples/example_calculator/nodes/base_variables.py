from PyQt5.QtWidgets import QDoubleSpinBox, QLineEdit

from examples.example_calculator.nodes_configuration import *
from examples.example_calculator.master_node import MasterNode
from examples.example_calculator.editor_proterties_list import PropertiesList


@set_var_ID(VAR_FLOAT)
class FloatVar(MasterNode):
    icon = ""
    node_type = VAR_FLOAT
    name = "Float Var"
    content_label_objname = "var_node_float"
    node_value = float

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


@set_var_ID(VAR_INTEGER)
class IntegerVar(MasterNode):
    icon = ""
    node_type = VAR_INTEGER
    name = "Integer Var"
    content_label_objname = "var_node_integer"
    node_value = int

    def __init__(self, scene, isFun=False):
        super().__init__(scene, inputs=[], outputs=[2])
        self.isVar = True

    def getNodeCode(self):
        name = self.outputs[0].socketName
        value = self.outputs[0].socketValue
        self.outputs[0].socketValue = "8"

        code = f"""{name}={value}"""
        return name


@set_var_ID(VAR_BOOLEAN)
class BooleanVar(MasterNode):
    icon = ""
    node_type = VAR_BOOLEAN
    name = "Boolean Var"
    content_label_objname = "var_node_boolean"
    node_value = bool

    def __init__(self, scene, isFun=False):
        super().__init__(scene, inputs=[], outputs=[3])
        self.isVar = True

    def getNodeCode(self):
        name = self.outputs[0].socketName
        value = self.outputs[0].socketValue

        code = f"""{name}={value}"""
        return name


@set_var_ID(VAR_STRING)
class StringVar(MasterNode):
    icon = ""
    node_type = VAR_STRING
    name = "String Var"
    content_label_objname = "var_node_string"
    node_value = str

    def __init__(self, scene, isFun=False):
        super().__init__(scene, inputs=[], outputs=[4])
        self.isVar = True

    def getNodeCode(self):
        name = self.outputs[0].socketName
        value = self.outputs[0].socketValue

        code = f"""{name}={value}"""
        return name
