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
    icon = "icons/light/if.png"
    name = "IF Statement"
    category = "FUNCTION"
    sub_category = "Process"
    node_color = "#90FF5733"
    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 3], outputs=[0, 0])

        self.set_input_label_text(0, "Action")
        self.set_input_label_text(1, "Condition")

        self.set_output_label_text(0, "True")
        self.set_output_label_text(1, "False")

    def getNodeCode(self):
        if self.syntax == "Python":
            self.showCode = not self.isInputConnected(0)

            condition = self.get_my_input_code(1)

            true = self.get_other_socket_code(0)

            false = self.get_other_socket_code(1)

            if self.isOutputConnected(1) and self.isOutputConnected(0):
                python_code = f"""
if {condition}:
{Indent(true)}
else:
{Indent(false)}"""
            elif self.isOutputConnected(1) and self.isOutputConnected(0) is False:
                python_code = f"""
if not {condition}:
{Indent(false)}"""
            else:
                python_code = f"""
if {condition}:
{Indent(true)}"""

            raw_code = python_code
        elif self.syntax == "C++":
            self.showCode = not self.isInputConnected(0)

            condition = self.get_my_input_code(1)

            true = self.get_other_socket_code(0)

            false = self.get_other_socket_code(1)

            if self.isOutputConnected(1) and self.isOutputConnected(0):
                python_code = f"""
if ({condition})
{Indent(true)}
else
{Indent(false)}"""
            elif self.isOutputConnected(1) and self.isOutputConnected(0) is False:
                python_code = f"""
if (not {condition})
{Indent(false)}"""
            else:
                python_code = f"""
if ({condition})
{Indent(true)}"""
            raw_code = python_code

        return self.grNode.highlight_code(raw_code)


class ForLoop(MasterNode):
    icon = "icons/light/Loop.png"
    name = "For Loop"
    category = "FUNCTION"
    sub_category = "Process"
    node_color = "#905050FF"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 2], outputs=[0])

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

        return self.grNode.highlight_code(raw_code)

class ForEachLoop(MasterNode):
    icon = "icons/light/Loop.png"
    name = "For Each Loop"
    category = "FUNCTION"
    sub_category = "Process"
    node_color = "#905050FF"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 5], outputs=[0, 6])

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

        return self.grNode.highlight_code(raw_code)

class GreaterThan(MasterNode):
    icon = "icons/light/more_than.png"
    name = "Greater Than"
    category = "FUNCTION"
    sub_category = "Process"
    node_color = logicOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[3])
        self.showCode = False

    def getNodeCode(self):
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}&gt;{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return self.grNode.highlight_code(raw_code)

class LessThan(MasterNode):
    icon = "icons/light/less_than.png"
    name = "Less Than"
    category = "FUNCTION"
    sub_category = "Process"
    node_color = logicOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[3])
        self.showCode = False

    def getNodeCode(self):
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}&lt;{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return self.grNode.highlight_code(raw_code)

class Equal(MasterNode):
    icon = "icons/light/equal.png"
    name = "Equal"
    category = "FUNCTION"
    sub_category = "Process"
    node_color = logicOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[3])
        self.showCode = False


    def getNodeCode(self):
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}=={B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax

        return self.grNode.highlight_code(raw_code)

# Logic
class And(MasterNode):
    icon = "icons/light/and.png"
    name = "And"
    category = "FUNCTION"
    sub_category = "Logic"
    node_color = logicOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[3, 3], outputs=[3])
        self.showCode = False

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
    icon = "icons/light/add.png"
    name = "Add"
    category = "FUNCTION"
    sub_category = "Math"
    node_color = mathOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False

    def getNodeCode(self):
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}+{B})"

            raw_code = python_code

        elif self.syntax == "C++":
            raw_code = self.syntax
        return self.grNode.highlight_code(raw_code)

class Sub(MasterNode):
    icon = "icons/light/sub.png"
    name = "Subtract"
    category = "FUNCTION"
    sub_category = "Math"
    node_color = mathOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False

    def getNodeCode(self):
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}+{B})"

            raw_code = python_code

        elif self.syntax == "C++":
            raw_code = self.syntax
        return self.grNode.highlight_code(raw_code)

class Mul(MasterNode):
    icon = "icons/light/mul.png"
    name = "Multiply"
    category = "FUNCTION"
    sub_category = "Math"
    node_color = mathOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False

    def getNodeCode(self):
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}*{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax
        return self.grNode.highlight_code(raw_code)

class Div(MasterNode):
    icon = "icons/light/divide.png"
    name = "Divide"
    category = "FUNCTION"
    sub_category = "Math"
    node_color = mathOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False

    def getNodeCode(self):
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A}/{B})"

            raw_code = python_code

        elif self.syntax == "C++":

            raw_code = self.syntax
        return self.grNode.highlight_code(raw_code)

# Input
class UserInput(MasterNode):
    icon = ""
    name = "User Input"
    category = "FUNCTION"
    sub_category = "Input"
    node_color = "#505050"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 6, 4], outputs=[0])

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
        return self.grNode.highlight_code(raw_code)

class RawCode(MasterNode):
    icon = ""
    name = "Raw Code"
    category = "FUNCTION"
    sub_category = "Input"
    node_color = "#303030"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 4], outputs=[0])

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
        return self.grNode.highlight_code(raw_code)

# Output
class Print(MasterNode):
    icon = "icons/light/print.png"
    name = "Print"
    category = "FUNCTION"
    sub_category = "Output"
    node_color = "#90702070"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 6], outputs=[0])

    def getNodeCode(self):
        if self.syntax == "Python":
            self.showCode = not self.isInputConnected(0)
            brotherCode = self.get_other_socket_code(0)
            printCode = self.get_my_input_code(1)
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

            self.showCode = not self.isInputConnected(0)
            brotherCode = self.get_other_socket_code(0)
            printCode = self.get_my_input_code(1)
            if self.isInputConnected(1):
                python_code = f"""
cout >> {printCode};
{brotherCode}"""

            else:
                python_code = f"""
cout >> "{printCode}";
{brotherCode}"""

            raw_code = python_code

        return self.grNode.highlight_code(raw_code)


class Return(MasterNode):
    icon = "icons/light/return.png"
    name = "Return"
    category = "FUNCTION"
    sub_category = "Output"
    node_color = "#90702070"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 6], outputs=[0])

    def getNodeCode(self):
        if self.syntax == "Python":
            self.showCode = not self.isInputConnected(0)
            brotherCode = self.get_other_socket_code(0)
            printCode = self.get_my_input_code(1)
            python_code = f"""
return {printCode}
{brotherCode}"""
            raw_code = python_code

        elif self.syntax == "C++":

            self.showCode = not self.isInputConnected(0)
            brotherCode = self.get_other_socket_code(0)
            printCode = self.get_my_input_code(1)
            python_code = f"""
return {printCode};
{brotherCode}"""
            raw_code = python_code
        return self.grNode.highlight_code(raw_code)

# Khyria Efforts
# code = f"""<pre><b><span style=\" Font-size:20px ; background-color:#553E0B0B;\"  >
# if {condition}:
# {textwrap.indent(true, "    ")}
# else:
# {textwrap.indent(false, "    ")}</span></pre>"""