from PyQt5.QtGui import QBrush, QColor

from vvs_app.nodes.default_functions import FontSize, FontFamily
from vvs_app.nodes.nodes_configuration import *
from vvs_app.master_node import MasterNode

FloatColor = "#7000FF10"
IntegerColor = "#aa0070FF"
BooleanColor = "#aaFF1010"
StringColor = "#70FF10FF"


class FloatVar(MasterNode):
    icon = ""
    name = "user_float"
    category = "VARIABLE"
    sub_category = "VARIABLE"
    node_color = FloatColor

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[1]) if not isSetter else super().__init__(scene, inputs=[0, 1], outputs=[0, 1])
        self.is_setter = isSetter
        self.node_return = "float"

    def getNodeCode(self):
        raw_code = "Empty"
        if self.is_setter:
            self.outputs[1].socket_code = self.name
            self.showCode = not self.isInputConnected(0)
            brotherCode = self.get_other_socket_code(0)
            setInput = self.get_my_input_code(1)
            if self.syntax == "Python":
                if self.node_structure == 'single value':
                    python_code = f"""
{self.name} = {setInput}
{brotherCode}"""
                    raw_code = python_code

                elif self.node_structure == 'array':
                    python_code = f"""
{self.name} = numpy.array('f',[{setInput}])
{brotherCode}"""
                    raw_code = python_code

            elif self.syntax == "C++":
                if self.node_structure == 'single value':
                    CPP_code = f"""
float {self.name} = {setInput};
{brotherCode}"""
                    raw_code = CPP_code
                elif self.node_structure == 'array':
                    L_P = "{"
                    R_P = "}"
                    CPP_code = f"""
list &lt; float &gt; {self.name}({L_P}{setInput}{R_P});
{brotherCode}"""
                    raw_code = CPP_code
            return self.grNode.highlight_code(raw_code)
        else:
            self.showCode = False
            getCode = self.outputs[0].socket_code = self.name
            return getCode


class IntegerVar(MasterNode):
    icon = ""
    name = "user_integer"
    category = "VARIABLE"
    sub_category = "VARIABLE"
    node_color = IntegerColor

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[2]) if not isSetter else super().__init__(scene, inputs=[0, 2], outputs=[0, 2])
        self.is_setter = isSetter
        self.node_return = "integer"

    def getNodeCode(self):
        raw_code = "Empty"
        if self.is_setter:
            self.outputs[1].socket_code = self.name
            self.showCode = not self.isInputConnected(0)
            brotherCode = self.get_other_socket_code(0)
            setInput = self.get_my_input_code(1)
            if self.syntax == "Python":
                if self.node_structure == 'single value':
                    python_code = f"""
{self.name} = {setInput}
{brotherCode}"""
                    raw_code = python_code

                elif self.node_structure == 'array':
                    python_code = f"""
{self.name} = numpy.array('i',[{setInput}])
{brotherCode}"""
                    raw_code = python_code
            elif self.syntax == "C++":
                if self.node_structure == 'single value':
                    CPP_code = f"""
int {self.name} = {setInput};
{brotherCode}"""
                    raw_code = CPP_code
                elif self.node_structure == 'array':
                    L_P = "{"
                    R_P = "}"
                    CPP_code = f"""
list &lt; int &gt; {self.name}({L_P}{setInput}{R_P});
{brotherCode}"""
                    raw_code = CPP_code
            return self.grNode.highlight_code(raw_code)

        else:
            self.showCode = False
            getCode = self.outputs[0].socket_code = self.name
            return getCode


class BooleanVar(MasterNode):
    icon = ""
    name = "user_boolean"
    category = "VARIABLE"
    sub_category = "VARIABLE"
    node_color = BooleanColor

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[3]) if not isSetter else super().__init__(scene, inputs=[0, 3], outputs=[0, 3])
        self.is_setter = isSetter
        self.node_return = "boolean"

    def getNodeCode(self):
        raw_code = "Empty"
        if self.is_setter:
            self.outputs[1].socket_code = self.name
            self.showCode = not self.isInputConnected(0)
            brotherCode = self.get_other_socket_code(0)
            setInput = self.get_my_input_code(1)
            if self.syntax == "Python":
                if self.node_structure == 'single value':
                    python_code = f"""
{self.name} = {setInput}
{brotherCode}"""
                    raw_code = python_code

                elif self.node_structure == 'array':
                    python_code = f"""
{self.name} = numpy.array('?',[{setInput}])
{brotherCode}"""
                    raw_code = python_code
            elif self.syntax == "C++":
                if self.node_structure == 'single value':
                    CPP_code = f"""
bool {self.name} = {setInput};
{brotherCode}"""
                    raw_code = CPP_code
                elif self.node_structure == 'array':
                    L_P = "{"
                    R_P = "}"
                    CPP_code = f"""
list &lt; bool &gt; {self.name} = {L_P}{setInput}{R_P};
{brotherCode}"""
                    raw_code = CPP_code
            return self.grNode.highlight_code(raw_code)
        else:
            self.showCode = False
            getCode = self.outputs[0].socket_code = self.name
            return getCode


class StringVar(MasterNode):
    icon = ""
    name = "user_string"
    category = "VARIABLE"
    sub_category = "VARIABLE"
    node_color = StringColor

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[4]) if not isSetter else super().__init__(scene, inputs=[0, 4], outputs=[0, 4])
        self.is_setter = isSetter
        self.node_return = "string"

    def getNodeCode(self):
        raw_code = "Empty"
        if self.is_setter:
            self.outputs[1].socket_code = self.name
            self.showCode = not self.isInputConnected(0)
            brotherCode = self.get_other_socket_code(0)
            setInput = f"{chr(34)}{self.get_my_input_code(1)}{chr(34)}"
            if self.syntax == "Python":
                if self.node_structure == 'single value':
                    python_code = f"""
{self.name} = {setInput}
{brotherCode}"""
                    raw_code = python_code
                elif self.node_structure == 'array':
                    python_code = f"""
{self.name} = numpy.array('S',[{setInput}])
{brotherCode}"""
                    raw_code = python_code
            elif self.syntax == "C++":
                if self.node_structure == 'single value':
                    CPP_code = f"""
string {self.name} = {setInput};
{brotherCode}"""
                    raw_code = CPP_code
                elif self.node_structure == 'array':
                    L_P = "{"
                    R_P = "}"
                    CPP_code = f"""
list &lt;string&gt; {self.name} = {L_P}{setInput}{R_P};
{brotherCode}"""
                    raw_code = CPP_code

            return self.grNode.highlight_code(raw_code)
        else:
            self.showCode = False
            getCode = self.outputs[0].socket_code = self.name
            return getCode
