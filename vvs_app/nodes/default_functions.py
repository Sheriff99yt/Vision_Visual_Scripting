from qtpy.QtGui import *

from vvs_app.nodes.nodes_configuration import *
from vvs_app.master_node import MasterNode
from textwrap import *

FontSize = 14
FontFamily = "Roboto"
mathOperators = "#70307030"
logicOperators = "#30000050"


def Indent(String):
    return indent(String, '     ')

# Process
class IfStatement(MasterNode):
    icon = "icons/if.png"
    name = "IF Statement"
    category = "FUNCTION"
    sub_category = "Process"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 3], outputs=[0, 0])
        self.set_node_color("#90FF5733")
        self.set_input_label_text(1, "Condition")

    def getNodeCode(self):
        if self.syntax == "Python":
            self.showCode = not self.isInputConnected(0)

            condition = self.get_my_input_code(1)

            true = self.get_other_socket_code(0)

            false = self.get_other_socket_code(1)

            if self.isOutputConnected(1):
                python_code = f"""
if {condition}:
{Indent(true)}
else:
{Indent(false)}"""

            else:
                python_code = f"""
if {condition}:
{Indent(true)}"""

            raw_code = python_code
        elif self.syntax == "C++":
            raw_code = self.syntax


        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{raw_code}</span></p></pre> """

        return code

class ForLoop(MasterNode):
    icon = "icons/Loop.png"
    name = "For Loop"
    category = "FUNCTION"
    sub_category = "Process"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 2], outputs=[0])
        self.set_node_color("#905050FF")

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

class ForEachLoop(MasterNode):
    icon = "icons/Loop.png"
    name = "For Each Loop"
    category = "FUNCTION"
    sub_category = "Process"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 5], outputs=[0, 6])
        self.set_node_color("#905050FF")

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

class GreaterThan(MasterNode):
    icon = "icons/more_than.png"
    name = "Greater Than"
    category = "FUNCTION"
    sub_category = "Process"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[3])
        self.showCode = False
        self.set_node_color(logicOperators)

    def getNodeCode(self):
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}&gt;{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code

class LessThan(MasterNode):
    icon = "icons/less_than.png"
    name = "Less Than"
    category = "FUNCTION"
    sub_category = "Process"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[3])
        self.showCode = False
        self.set_node_color(logicOperators)



    def getNodeCode(self):
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}&lt;{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code

class Equal(MasterNode):
    icon = "icons/equal.png"
    name = "Equal"
    category = "FUNCTION"
    sub_category = "Process"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[3])
        self.showCode = False
        self.set_node_color(logicOperators)


    def getNodeCode(self):
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}=={B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code

# Logic
class And(MasterNode):
    icon = "icons/and.png"
    name = "And"
    category = "FUNCTION"
    sub_category = "Logic"

    def __init__(self, scene):
        super().__init__(scene, inputs=[3, 3], outputs=[3])
        self.showCode = False
        self.set_node_color(logicOperators)

    def getNodeCode(self):
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A} and {B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code

# Math
class Add(MasterNode):
    icon = "icons/add.png"
    name = "Add"
    category = "FUNCTION"
    sub_category = "Math"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False
        self.set_node_color(mathOperators)

    def getNodeCode(self):
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}+{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code

class Sub(MasterNode):
    icon = "icons/sub.png"
    name = "Subtract"
    category = "FUNCTION"
    sub_category = "Math"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False
        self.set_node_color(mathOperators)

    def getNodeCode(self):
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}+{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code

class Mul(MasterNode):
    icon = "icons/mul.png"
    name = "Multiply"
    category = "FUNCTION"
    sub_category = "Math"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False
        self.set_node_color(mathOperators)

    def getNodeCode(self):
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}*{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code

class Div(MasterNode):
    icon = "icons/divide.png"
    name = "Divide"
    category = "FUNCTION"
    sub_category = "Math"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False
        self.set_node_color(mathOperators)

    def getNodeCode(self):
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}/{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return raw_code

# Input
class UserInput(MasterNode):
    icon = ""
    name = "User Input"
    category = "FUNCTION"
    sub_category = "Input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 6, 4], outputs=[0])
        self.nodeColor = "#505050"
        self.set_node_color("#505050")

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

class RawCode(MasterNode):
    icon = ""
    name = "Raw Code"
    category = "FUNCTION"
    sub_category = "Input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 4], outputs=[0])
        self.set_node_color("#303030")

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

# Output
class Print(MasterNode):
    icon = "icons/print.png"
    name = "Print"
    category = "FUNCTION"
    sub_category = "Output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 6], outputs=[0])
        self.set_node_color("#90702070")

    def getNodeCode(self):
        if self.syntax == "Python":
            self.showCode = not self.isInputConnected(0)
            brotherCode = self.get_other_socket_code(0)
            printCode = self.get_my_input_code(1)
            # print(self.isInputConnected(0))
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
# Khyria Efforts
# code = f"""<pre><b><span style=\" Font-size:20px ; background-color:#553E0B0B;\"  >
# if {condition}:
# {textwrap.indent(true, "    ")}
# else:
# {textwrap.indent(false, "    ")}</span></pre>"""