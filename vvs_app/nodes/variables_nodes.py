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
    name = "float"
    category = "VARIABLE"
    sub_category = "VARIABLE"

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[1]) if not isSetter else super().__init__(scene, inputs=[0, 1], outputs=[0, 1])
        self.is_setter = isSetter
        self.is_var = True
        self.set_node_color(FloatColor)

    def getNodeCode(self):
        if self.is_setter:
            if self.syntax == "Python":
                self.outputs[1].socket_code = self.name
                self.showCode = not self.isInputConnected(0)
                brotherCode = self.get_other_socket_code(0)
                setInput = self.get_my_input_code(1)

                python_code = f"""
{self.name}={setInput}
{brotherCode}"""
                raw_code = python_code

            elif self.syntax == "C++":

                self.outputs[1].socket_code = self.name
                self.showCode = not self.isInputConnected(0)
                brotherCode = self.get_other_socket_code(0)
                setInput = self.get_my_input_code(1)

                python_code = f"""
float {self.name}="{setInput}";
{brotherCode}"""

                raw_code = python_code

            if self.isSelected() is True:
                colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{FloatColor};" '''
            else:
                colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

            code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{raw_code}</span></p></pre> """

            return code
        else:
            self.showCode = False
            getCode = self.outputs[0].socket_code = self.name
            return getCode


class IntegerVar(MasterNode):
    icon = ""
    name = "integer"
    category = "VARIABLE"
    sub_category = "VARIABLE"

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[2]) if not isSetter else super().__init__(scene, inputs=[0, 2], outputs=[0, 2])
        self.is_setter = isSetter
        self.is_var = True
        self.set_node_color(IntegerColor)

    def getNodeCode(self):
        if self.is_setter:
            if self.syntax == "Python":
                self.outputs[1].socket_code = self.name
                self.showCode = not self.isInputConnected(0)
                brotherCode = self.get_other_socket_code(0)
                setInput = self.get_my_input_code(1)

                python_code = f"""
{self.name}={setInput}
{brotherCode}"""

                raw_code = python_code

            elif self.syntax == "C++":

                self.outputs[1].socket_code = self.name
                self.showCode = not self.isInputConnected(0)
                brotherCode = self.get_other_socket_code(0)
                setInput = self.get_my_input_code(1)

                python_code = f"""
int {self.name}="{setInput}";
{brotherCode}"""

                raw_code = python_code


            if self.isSelected() is True:
                colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{IntegerColor};" '''
            else:
                colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

            code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{raw_code}</span></p></pre> """

            return code
        else:
            self.showCode = False
            getCode = self.outputs[0].socket_code = self.name
            return getCode


class BooleanVar(MasterNode):
    icon = ""
    name = "boolean"
    category = "VARIABLE"
    sub_category = "VARIABLE"

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[3]) if not isSetter else super().__init__(scene, inputs=[0, 3], outputs=[0, 3])
        self.is_setter = isSetter
        self.is_var = True
        self.set_node_color(BooleanColor)

    def getNodeCode(self):
        if self.is_setter:
            if self.syntax == "Python":
                self.outputs[1].socket_code = self.name
                self.showCode = not self.isInputConnected(0)
                brotherCode = self.get_other_socket_code(0)
                setInput = self.get_my_input_code(1)

                python_code = f"""
{self.name}={setInput}
{brotherCode}"""

                raw_code = python_code

            elif self.syntax == "C++":

                self.outputs[1].socket_code = self.name
                self.showCode = not self.isInputConnected(0)
                brotherCode = self.get_other_socket_code(0)
                setInput = self.get_my_input_code(1)

                python_code = f"""
bool {self.name}="{setInput}";
{brotherCode}"""

                raw_code = python_code

            if self.isSelected() is True:
                colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{BooleanColor};" '''
            else:
                colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

            code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{raw_code}</span></p></pre> """

            return code
        else:
            self.showCode = False
            getCode = self.outputs[0].socket_code = self.name
            return getCode


class StringVar(MasterNode):
    icon = ""
    name = "string"
    category = "VARIABLE"
    sub_category = "VARIABLE"

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[4]) if not isSetter else super().__init__(scene, inputs=[0, 4], outputs=[0, 4])
        self.is_setter = isSetter
        self.is_var = True
        self.set_node_color(StringColor)


    def getNodeCode(self):
        if self.is_setter:
            if self.syntax == "Python":
                self.outputs[1].socket_code = self.name
                self.showCode = not self.isInputConnected(0)
                brotherCode = self.get_other_socket_code(0)
                setInput = self.get_my_input_code(1)

                python_code = f"""
{self.name}="{setInput}"
{brotherCode}"""

                raw_code = python_code

            elif self.syntax == "C++":
                self.outputs[1].socket_code = self.name
                self.showCode = not self.isInputConnected(0)
                brotherCode = self.get_other_socket_code(0)
                setInput = self.get_my_input_code(1)

                python_code = f"""
string {self.name}="{setInput}";
{brotherCode}"""

                raw_code = python_code


            if self.isSelected() is True:
                colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{StringColor};" '''
            else:
                colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

            code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{raw_code}</span></p></pre> """

            return code
        else:
            self.showCode = False
            getCode = self.outputs[0].socket_code = self.name
            return getCode


class ListVar(MasterNode):
    icon = ""
    name = "list"
    category = "VARIABLE"
    sub_category = "VARIABLE"

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[5]) if not isSetter else super().__init__(scene, inputs=[0, 5], outputs=[0, 5])
        self.is_setter = isSetter
        self.is_var = True
        self.set_node_color("#555555")

    def getNodeCode(self):
        if self.is_setter:
            if self.syntax == "Python":
                self.outputs[1].socket_code = self.name
                self.showCode = not self.isInputConnected(0)
                brotherCode = self.get_other_socket_code(0)
                setInput = self.get_my_input_code(1)
                if self.isInputConnected(1):
                    python_code = f"""
{self.name}={setInput}
{brotherCode}"""

                else:
                    python_code = f"""
{self.name}=[{setInput}]
{brotherCode}"""

                raw_code = python_code

            elif self.syntax == "C++":

                self.outputs[1].socket_code = self.name
                self.showCode = not self.isInputConnected(0)
                brotherCode = self.get_other_socket_code(0)
                setInput = self.get_my_input_code(1)

                python_code = f"""
string {self.name}="{setInput}";
{brotherCode}"""

                raw_code = python_code


            if self.isSelected() is True:
                colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{StringColor};" '''
            else:
                colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

            code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{raw_code}</span></p></pre> """

            return code
        else:
            self.showCode = False
            getCode = self.outputs[0].socket_code = self.name
            return getCode
