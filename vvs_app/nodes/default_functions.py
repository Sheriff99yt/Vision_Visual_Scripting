from qtpy.QtGui import *

from vvs_app.nodes.nodes_configuration import *
from vvs_app.master_node import MasterNode
from textwrap import *

FontSize = 18
FontFamily = "Roboto"
mathOperators = "#70307030"
logicOperators = "#30000050"


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
        if self.syntax == "Python":
            self.showCode = not self.isInputConnected(0)

            condition = self.get_my_input_code(1)

            true = self.get_other_socket_code(0)

            false = self.get_other_socket_code(1)

            python_code = f"""
if {condition}:
{Indent(true)}
else:
{Indent(false)}"""
            raw_code = python_code

        elif self.syntax == "C++":
            raw_code = self.syntax


        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{raw_code}</span></p></pre> """

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
        super().__init__(scene, inputs=[0, 2], outputs=[0])
        self.nodeColor = "#905050FF"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        if self.syntax == "Python":
            self.showCode = not self.isInputConnected(0)

            range = self.get_my_input_code(1)

            loopCode = self.get_other_socket_code(0)

            python_code = f"""
for item in range({range}):
{Indent(loopCode)}"""
            raw_code = python_code
        elif self.syntax == "C++":
            raw_code = self.syntax

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        styled_code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{raw_code}</span></p></pre> """

        return styled_code


@set_function_ID(FUN_FOR_EACH_LOOP)
class ForEachLoop(MasterNode):
    icon = "icons/Loop.png"
    node_type = FUN_FOR_EACH_LOOP
    name = "For Each Loop"
    content_label_objname = "node_for_each_loop"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 5], outputs=[0, 6])
        self.nodeColor = "#905050FF"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        if self.syntax == "Python":

            self.showCode = not self.isInputConnected(0)

            list = self.get_my_input_code(1)

            loopCode = self.get_other_socket_code(0)

            self.outputs[1].socket_code = 'item'

            python_code = f"""
for item in {list}:
{Indent(loopCode)}"""
            raw_code = python_code
        elif self.syntax == "C++":
            raw_code = self.syntax

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        styled_code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{raw_code}</span></p></pre> """

        return styled_code


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
        if self.syntax == "Python":
            self.showCode = not self.isInputConnected(0)

            brotherCode = self.get_other_socket_code(0)
            printCode = self.get_my_input_code(1)
            print(self.isInputConnected(0))
            if self.isInputConnected(1):
                python_code = f"""
print({printCode})
{brotherCode}"""

            else:
                python_code = f"""
print("{printCode}")
{brotherCode}"""

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax


        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{raw_code}</span></p></pre> """

        return code

@set_function_ID(FUN_USER_INPUT)
class UserInput(MasterNode):
    icon = ""
    node_type = FUN_USER_INPUT
    name = "User Input"
    content_label_objname = "node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 6, 4], outputs=[0])
        self.nodeColor = "#505050"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        if self.syntax == "Python":
            self.showCode = not self.isInputConnected(0)

            brotherCode = self.get_other_socket_code(0)
            inputName = self.get_my_input_code(1)

            if inputName != "" and inputName is not None: inputName += " = "
            inputCode = self.get_my_input_code(2)

            python_code = f"""
{inputName}input("{inputCode}")
{brotherCode}"""

            raw_code = python_code

        elif self.syntax == "C++":
            raw_code = self.syntax


        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{raw_code}</span></p></pre> """

        return code

@set_function_ID(FUN_RAW_CODE)
class RawCode(MasterNode):
    icon = ""
    node_type = FUN_RAW_CODE
    name = "Raw Code"
    content_label_objname = "node_raw_code"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 4], outputs=[0])
        self.nodeColor = "#303030"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        if self.syntax == "Python":
            self.showCode = not self.isInputConnected(0)

            brotherCode = self.get_other_socket_code(0)
            inputCode = self.get_my_input_code(1)

            python_code = f"""
{inputCode}
{brotherCode}"""

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax


        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{raw_code}</span></p></pre> """

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
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}+{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code


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
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}+{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code


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
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}*{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code


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
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}/{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code


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
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}&gt;{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code


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
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}&lt;{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code

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
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}=={B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code


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
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A} and {B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code
