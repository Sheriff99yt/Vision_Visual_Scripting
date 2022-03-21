from PyQt5.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

from examples.example_calculator.nodes.nodes_configuration import *
from examples.example_calculator.master_node import MasterNode, MasterGraphicsNode
from textwrap import *

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

FontSize = 18
FontFamily = "Roboto"
mathOperators = "#70307030"
logicOperators = "#707070FF"


def Indent(String):
    return indent(String, '     ')

@set_function_ID(FUN_IF)
class IfStatement(MasterNode):
    icon = "icons/if.png"
    node_type = FUN_IF
    name = "IF Statement"
    content_label_objname = "node_if_statement"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 3], outputs=[0, 0])
        self.nodeColor = "#90FF5733"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        self.showCode = not self.isInputConnected(0)

        condition = self.NodeCodeAtInput(1)

        true = self.NodeCodeAtOutput(0)

        false = self.NodeCodeAtOutput(1)

        rawCode = f"""
if {condition}:
{Indent(true)}
else:
{Indent(false)}"""

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{rawCode}</span></p></pre> """

        return code


# code = f"""<pre><b><span style=\" Font-size:20px ; background-color:#553E0B0B;\"  >
# if {condition}:
# {textwrap.indent(true, "    ")}
# else:
# {textwrap.indent(false, "    ")}</span></pre>"""


@set_function_ID(FUN_FOR_LOOP)
class ForLoop(MasterNode):
    icon = "icons/Loop.png"
    node_type = FUN_FOR_LOOP
    name = "For Loop"
    content_label_objname = "node_for_loop"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 2, 2], outputs=[0])
        self.grNode.height = 120
        self.nodeColor = "#905050FF"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        self.showCode = not self.isInputConnected(0)

        firstIndex = self.NodeCodeAtInput(1)

        lastIndex = self.NodeCodeAtInput(2)

        loopCode = self.NodeCodeAtOutput(0)

        rawCode = f"""
for i in range({firstIndex},{lastIndex}):
{Indent(loopCode)}"""
        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{rawCode}</span></p></pre> """

        return code


@set_function_ID(FUN_PRINT)
class Print(MasterNode):
    icon = "icons/print.png"
    node_type = FUN_PRINT
    name = "Print"
    content_label_objname = "node_print"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 4], outputs=[0])
        self.nodeColor = "#90702070"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        self.showCode = not self.isInputConnected(0)

        brotherCode = self.NodeCodeAtOutput(0)
        printCode = self.NodeCodeAtInput(1)

        rawCode = f"""
print({printCode})
{brotherCode}"""

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{rawCode}</span></p></pre> """

        return code

@set_function_ID(FUN_USER_INPUT)
class Print(MasterNode):
    icon = ""
    node_type = FUN_USER_INPUT
    name = "Input"
    content_label_objname = "node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 4], outputs=[0])
        self.nodeColor = "#505050"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        self.showCode = not self.isInputConnected(0)

        brotherCode = self.NodeCodeAtOutput(0)
        inputCode = self.NodeCodeAtInput(1)

        rawCode = f"""
input({inputCode})
{brotherCode}"""

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{rawCode}</span></p></pre> """

        return code


@set_function_ID(FUN_ADD)
class Add(MasterNode):
    icon = "icons/add.png"
    node_type = FUN_ADD
    name = "Add"
    content_label = ""
    content_label_objname = "node_add"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False
        self.grNode._brush_title = QBrush(QColor(mathOperators))

    def getNodeCode(self):
        A = self.NodeCodeAtInput(0)
        B = self.NodeCodeAtInput(1)

        rawCode = f"({A}+{B})"

        if self.isSelected() is True:
            colorStyle = f' style=" Font-size:{FontSize}px ; background-color:{mathOperators};" '
        else:
            colorStyle = f' style=" Font-size:{FontSize}px ;" '

        code = f' <p style="font-family: {FontFamily} "><span {colorStyle} >{rawCode}</span></p> '

        return rawCode


@set_function_ID(FUN_SUB)
class Sub(MasterNode):
    icon = "icons/sub.png"
    node_type = FUN_SUB
    name = "Subtract"
    content_label = ""
    content_label_objname = "node_subtract"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False
        self.grNode._brush_title = QBrush(QColor(mathOperators))

    def getNodeCode(self):
        A = self.NodeCodeAtInput(0)
        B = self.NodeCodeAtInput(1)

        rawCode = f"({A}-{B})"

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{mathOperators};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{rawCode}</span></p></pre> """

        return rawCode


@set_function_ID(FUN_MUL)
class Mul(MasterNode):
    icon = "icons/mul.png"
    node_type = FUN_MUL
    name = "Multiply"
    content_label = ""
    content_label_objname = "node_mul"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False
        self.grNode._brush_title = QBrush(QColor(mathOperators))

    def getNodeCode(self):
        A = self.NodeCodeAtInput(0)
        B = self.NodeCodeAtInput(1)

        rawCode = f"({A}*{B})"

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{mathOperators};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{rawCode}</span></p></pre> """

        return rawCode


@set_function_ID(FUN_DIV)
class Div(MasterNode):
    icon = "icons/divide.png"
    node_type = FUN_DIV
    name = "Divide"
    content_label = ""
    content_label_objname = "node_div"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False
        self.grNode._brush_title = QBrush(QColor(mathOperators))

    def getNodeCode(self):
        A = self.NodeCodeAtInput(0)
        B = self.NodeCodeAtInput(1)

        rawCode = f"({A}/{B})"

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{mathOperators};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{rawCode}</span></p></pre> """

        return rawCode


@set_function_ID(FUN_GREATER_THAN)
class GreaterThan(MasterNode):
    icon = "icons/more_than.png"
    node_type = FUN_GREATER_THAN
    name = "Greater Than"
    content_label = ""
    content_label_objname = "node_greater_than"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[3])
        self.showCode = False
        self.grNode._brush_title = QBrush(QColor(logicOperators))

    def getNodeCode(self):
        A = self.NodeCodeAtInput(0)
        B = self.NodeCodeAtInput(1)

        rawCode = f"({A}>{B})"

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{mathOperators};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{rawCode}</span></p></pre> """

        return rawCode


@set_function_ID(FUN_LESS_THAN)
class LessThan(MasterNode):
    icon = "icons/less_than.png"
    node_type = FUN_LESS_THAN
    name = "Less Than"
    content_label = ""
    content_label_objname = "node_less_than"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[3])
        self.showCode = False
        self.grNode._brush_title = QBrush(QColor(logicOperators))

    def getNodeCode(self):
        A = self.NodeCodeAtInput(0)
        B = self.NodeCodeAtInput(1)

        rawCode = f"({A}<{B})"

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{logicOperators};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{rawCode}</span></p></pre> """

        return rawCode


@set_function_ID(FUN_Equal)
class Equal(MasterNode):
    icon = "icons/equal.png"
    node_type = FUN_Equal
    name = "Equal"
    content_label = ""
    content_label_objname = "node_equal"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[3])
        self.showCode = False
        self.grNode._brush_title = QBrush(QColor(logicOperators))

    def getNodeCode(self):
        A = self.NodeCodeAtInput(0)
        B = self.NodeCodeAtInput(1)

        rawCode = f"({A}=={B})"

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{logicOperators};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{rawCode}</span></p></pre> """

        return rawCode


@set_function_ID(FUN_AND)
class And(MasterNode):
    icon = "icons/and.png"
    node_type = FUN_AND
    name = "And"
    content_label = ""
    content_label_objname = "node_and"

    def __init__(self, scene):
        super().__init__(scene, inputs=[3, 3], outputs=[3])
        self.showCode = False
        self.grNode._brush_title = QBrush(QColor(logicOperators))

    def getNodeCode(self):
        A = self.NodeCodeAtInput(0)
        B = self.NodeCodeAtInput(1)

        rawCode = f"({A} and {B})"

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{logicOperators};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{rawCode}</span></p></pre> """

        return rawCode
