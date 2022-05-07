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
    node_type = None
    name = "float"
    category = "VARIABLE"
    sub_category = "VARIABLE"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[1])
        self.isVar = True
        self.grNode._brush_title = QBrush(QColor(FloatColor))

    def toGetter(self):
        self.isSetter = False
        self.initSockets(inputs=[], outputs=[1])

    def toSetter(self):
        self.isSetter = True
        self.initSockets(inputs=[0, 1], outputs=[0, 1])

    def getNodeCode(self):
        if self.isSetter:
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
regester_Node(FloatVar)


class IntegerVar(MasterNode):
    icon = ""
    node_type = None
    name = "integer"
    category = "VARIABLE"
    sub_category = "VARIABLE"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[2])
        self.isVar = True
        self.grNode._brush_title = QBrush(QColor(IntegerColor))

    def toGetter(self):
        self.isSetter = False
        self.initSockets(inputs=[], outputs=[2])

    def toSetter(self):
        self.isSetter = True
        self.initSockets(inputs=[0, 2], outputs=[0, 2])

    def getNodeCode(self):
        if self.isSetter:
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
regester_Node(IntegerVar)


class BooleanVar(MasterNode):
    icon = ""
    node_type = None
    name = "boolean"
    category = "VARIABLE"
    sub_category = "VARIABLE"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        self.isVar = True
        self.grNode._brush_title = QBrush(QColor(BooleanColor))

    def toGetter(self):
        self.isSetter = False
        self.initSockets(inputs=[], outputs=[3])

    def toSetter(self):
        self.isSetter = True
        self.initSockets(inputs=[0, 3], outputs=[0, 3])

    def getNodeCode(self):
        if self.isSetter:
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
regester_Node(BooleanVar)


class StringVar(MasterNode):
    icon = ""
    node_type = None
    name = "string"
    category = "VARIABLE"
    sub_category = "VARIABLE"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[4])
        self.isVar = True
        self.grNode._brush_title = QBrush(QColor(StringColor))

    def toGetter(self):
        self.isSetter = False
        self.initSockets(inputs=[], outputs=[4])

    def toSetter(self):
        self.isSetter = True
        self.initSockets(inputs=[0, 4], outputs=[0, 4])

    def getNodeCode(self):
        if self.isSetter:
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
regester_Node(StringVar)


class ListVar(MasterNode):
    icon = ""
    node_type = None
    name = "list"
    category = "VARIABLE"
    sub_category = "VARIABLE"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[5])
        self.isVar = True
        self.grNode._brush_title = QBrush(QColor(StringColor))

    def toGetter(self):
        self.isSetter = False
        self.initSockets(inputs=[], outputs=[5])

    def toSetter(self):
        self.isSetter = True
        self.initSockets(inputs=[0, 5], outputs=[0, 5])

    def getNodeCode(self):
        if self.isSetter:
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
regester_Node(ListVar)
