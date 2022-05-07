from PyQt5.QtGui import QBrush, QColor

from vvs_app.nodes.default_functions import FontSize, FontFamily
from vvs_app.nodes.nodes_configuration import *
from vvs_app.master_node import MasterNode

FloatColor = "#7000FF10"
IntegerColor = "#aa0070FF"
BooleanColor = "#aaFF1010"
StringColor = "#70FF10FF"

@set_var_ID(VAR_FLOAT)
class FloatVar(MasterNode):
    icon = ""
    node_type = VAR_FLOAT
    name = "float"
    content_label_objname = "var_node_float"

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[1]) if not isSetter else super().__init__(scene, inputs=[0, 1], outputs=[0, 1])
        self.is_setter = isSetter
        self.is_var = True
        self.grNode._brush_title = QBrush(QColor(FloatColor))

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

                raw_code = self.syntax

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


@set_var_ID(VAR_INTEGER)
class IntegerVar(MasterNode):
    icon = ""
    node_type = VAR_INTEGER
    name = "integer"
    content_label_objname = "var_node_integer"

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[2]) if not isSetter else super().__init__(scene, inputs=[0, 2], outputs=[0, 2])
        self.is_setter = isSetter
        self.is_var = True
        self.grNode._brush_title = QBrush(QColor(IntegerColor))

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

                raw_code = self.syntax


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

@set_var_ID(VAR_BOOLEAN)
class BooleanVar(MasterNode):
    icon = ""
    node_type = VAR_BOOLEAN
    name = "boolean"
    content_label_objname = "var_node_boolean"

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[3]) if not isSetter else super().__init__(scene, inputs=[0, 3], outputs=[0, 3])
        self.is_setter = isSetter
        self.is_var = True
        self.grNode._brush_title = QBrush(QColor(BooleanColor))

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

                raw_code = self.syntax


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

@set_var_ID(VAR_STRING)
class StringVar(MasterNode):
    icon = ""
    node_type = VAR_STRING
    name = "string"
    content_label_objname = "var_node_string"

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[4]) if not isSetter else super().__init__(scene, inputs=[0, 4], outputs=[0, 4])
        self.is_setter = isSetter
        self.is_var = True
        self.grNode._brush_title = QBrush(QColor(StringColor))

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

                raw_code = self.syntax


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


@set_var_ID(VAR_LIST)
class ListVar(MasterNode):
    icon = ""
    node_type = VAR_LIST
    name = "list"
    content_label_objname = "var_node_list"

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[5]) if not isSetter else super().__init__(scene, inputs=[0, 5], outputs=[0, 5])
        self.is_setter = isSetter
        self.is_var = True
        self.grNode._brush_title = QBrush(QColor(StringColor))

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

                raw_code = self.syntax


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

