from examples.example_calculator.nodes_configuration import *
from examples.example_calculator.master_node import MasterNode, MasterGraphicsNode

@register_node(VAR_FLOAT)
class Float_Var(MasterNode):
    icon = ""
    node_ID = VAR_FLOAT
    op_title = "Float Var"
    content_label_objname = "var_node_float"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[1])

    def getNodeCode(self):
        self.var_name = "prince"
        self.var_value = "10.5"
        code = """{}={}""".format(self.var_name, self.var_value)
        return code


@register_node(VAR_INTEGER)
class Integer_Var(MasterNode):
    icon = ""
    node_ID = VAR_INTEGER
    op_title = "Integer Var"
    content_label_objname = "var_node_integer"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[2])

    def getNodeCode(self):
        self.var_name = "age"
        self.var_value = "50"
        code = """{}={}""".format(self.var_name, self.var_value)
        return code


@register_node(VAR_BOOLEAN)
class Boolean_Var(MasterNode):
    icon = ""
    node_ID = VAR_BOOLEAN
    op_title = "Boolean Var"
    content_label_objname = "var_node_boolean"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])

    def getNodeCode(self):
        self.var_name = "isExample"
        self.var_value = "True"
        code = """{}={}""".format(self.var_name, self.var_value)
        return code


@register_node(VAR_STRING)
class String_Var(MasterNode):
    icon = ""
    node_ID = VAR_STRING
    op_title = "String Var"
    content_label_objname = "var_node_string"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[4])

    def getNodeCode(self):
        self.var_name = "name"
        self.var_value = "Ahmed"
        code = """{}={}""".format(self.var_name, self.var_value)
        return code
