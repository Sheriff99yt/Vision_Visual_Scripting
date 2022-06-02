from PyQt5.QtGui import QBrush, QColor

from vvs_app.nodes.default_functions import FontSize, FontFamily
from vvs_app.nodes.nodes_configuration import *
from vvs_app.master_node import MasterNode


Numpy_Vars = {'float': "'f'",
              'integer': "'i'",
              'boolean': "'?'",
              'string': "'S'"}

Rust_Vars = {'float': "f32",
             'integer': "i32",
             'boolean': "bool",
             'string': "String"}

class UserVar(MasterNode):
    icon = ""
    name = "user_variable"
    category = "VARIABLE"
    sub_category = "VARIABLE"


    def __init__(self, scene, isSetter, node_usage=None):
        if not self.node_usage: self.node_usage = node_usage
        if isSetter:
            super().__init__(scene, inputs=[0, self.node_usage], outputs=[0, self.node_usage])
            self.getNodeCode = self.get_setter_code
        else:
            super().__init__(scene, inputs=[], outputs=[self.node_usage])
            self.getNodeCode = self.get_getter_code

        self.is_setter = isSetter


    def get_setter_code(self):
        self.outputs[1].socket_code = self.name
        self.showCode = not self.isInputConnected(0)
        brother_code = self.get_other_socket_code(0)
        input_1_code = self.get_my_input_code(1)
        raw_code = "Empty"
        L_P = "{"
        R_P = "}"

        if self.node_usage == 'string':
            input_1_code = f'"{input_1_code}"'

        if self.syntax == "Python":
            if self.node_structure == 'single value':
                python_code = f"""
{self.name} = {input_1_code}
{brother_code}"""
                raw_code = python_code

            elif self.node_structure == 'array':
                python_code = f"""
{self.name} = numpy.array({Numpy_Vars[self.node_usage]},[{input_1_code}])
{brother_code}"""
                raw_code = python_code

        elif self.syntax == "C++":
            if self.node_structure == 'single value':
                CPP_code = f"""
{self.node_usage} {self.name} = {input_1_code};
{brother_code}"""
                raw_code = CPP_code

            elif self.node_structure == 'array':
                CPP_code = f"""
list &lt;{self.node_usage}&gt; {self.name}({L_P}{input_1_code}{R_P});
{brother_code}"""
                raw_code = CPP_code

        elif self.syntax == "Rust":
            if self.node_structure == 'single value':
                rust_code = f"""
let {self.name} = {input_1_code};
{brother_code}"""
                raw_code = rust_code

            elif self.node_structure == 'array':
                rust_code = f"""
let {self.name}: Vec&lt;{Rust_Vars[self.node_usage]}&gt; = vec![{input_1_code}];
{brother_code}"""
                raw_code = rust_code

        return self.grNode.highlight_code(raw_code)

    def get_getter_code(self):
        self.showCode = False
        getCode = self.outputs[0].socket_code = self.name
        return getCode
