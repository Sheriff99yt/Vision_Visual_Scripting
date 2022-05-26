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
    icon = "if.png"
    name = "IF Statement"
    category = "FUNCTION"
    sub_category = "Process"
    node_color = "#90FF5733"
    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 3], outputs=[0, 0])

        # self.icon = self.scene.masterRef.global_switches.get_icon("if.png")

        self.set_input_label_text(0, "Action")
        self.set_input_label_text(1, "Condition")

        self.set_output_label_text(0, "True")
        self.set_output_label_text(1, "False")

    def getNodeCode(self):
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        condition = self.get_my_input_code(1)
        true = self.get_other_socket_code(0)
        false = self.get_other_socket_code(1)

        if self.syntax == "Python":
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
            L_P = "{"
            R_P = "}"
            if self.isOutputConnected(1) and self.isOutputConnected(0):
                CPP_code = f"""
if ({condition})
{L_P}
{Indent(true)}
{R_P}
else
{L_P}
{Indent(false)}
{R_P}"""
            elif self.isOutputConnected(1) and self.isOutputConnected(0) is False:
                CPP_code = f"""
if (not {condition})
{L_P}
{Indent(false)}
{R_P}"""
            else:
                CPP_code = f"""
if ({condition})
{L_P}
{Indent(true)}
{R_P}"""
            raw_code = CPP_code

        return self.grNode.highlight_code(raw_code)


class ForLoop(MasterNode):
    icon = "Loop.png"
    name = "For Loop"
    category = "FUNCTION"
    sub_category = "Process"
    node_color = "#905050FF"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 2], outputs=[0])

    def getNodeCode(self):
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        range = self.get_my_input_code(1)
        loopCode = self.get_other_socket_code(0)

        if self.syntax == "Python":

            python_code = f"""
for item in range({range}):
{Indent(loopCode)}"""
            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = f"""
for (int i=0;i&lt;{range};i++)
{Indent(loopCode)}"""
            raw_code = CPP_code

        return self.grNode.highlight_code(raw_code)


class ForEachLoop(MasterNode):
    icon = "Loop.png"
    name = "For Each Loop"
    category = "FUNCTION"
    sub_category = "Process"
    node_color = "#905050FF"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 5], outputs=[0, 6])

    def getNodeCode(self):
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        list = self.get_my_input_code(1)
        loopCode = self.get_other_socket_code(0)
        self.outputs[1].socket_code = 'item'

        if self.syntax == "Python":
            python_code = f"""
for item in {list}:
{Indent(loopCode)}"""
            raw_code = python_code

        elif self.syntax == "C++":
            L_P = "{"
            R_P = "}"
            CPP_code = f"""
for (auto item : {list})
{L_P}
{Indent(loopCode)}
{R_P}"""
            raw_code = CPP_code
        return self.grNode.highlight_code(raw_code)


# Logic
class And(MasterNode):
    icon = "and.png"
    name = "And"
    category = "FUNCTION"
    sub_category = "Logic"
    node_color = logicOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[6, 6], outputs=[3])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        if self.syntax == "Python":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            python_code = self.outputs[0].socket_code = f"({A} and {B})"

            raw_code = python_code

        elif self.syntax == "C++":
            A = self.get_my_input_code(0)
            B = self.get_my_input_code(1)

            CPP_code = self.outputs[0].socket_code = f"({A} && {B})"

            raw_code = CPP_code

        return raw_code


class GreaterThan(MasterNode):
    icon = "more_than.png"
    name = "Greater Than"
    category = "FUNCTION"
    sub_category = "Logic"
    node_color = logicOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[6, 6], outputs=[3])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        A = self.get_my_input_code(0)
        B = self.get_my_input_code(1)

        if self.syntax == "Python":
            python_code = self.outputs[0].socket_code = f"({A}&gt;{B})"
            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = self.outputs[0].socket_code = f"({A}&gt;{B})"
            raw_code = CPP_code

        return self.grNode.highlight_code(raw_code)


class LessThan(MasterNode):
    icon = "less_than.png"
    name = "Less Than"
    category = "FUNCTION"
    sub_category = "Logic"
    node_color = logicOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[6, 6], outputs=[3])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        A = self.get_my_input_code(0)
        B = self.get_my_input_code(1)

        if self.syntax == "Python":
            python_code = self.outputs[0].socket_code = f"({A}&lt;{B})"
            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = self.outputs[0].socket_code = f"({A}&lt;{B})"
            raw_code = CPP_code

        return self.grNode.highlight_code(raw_code)


class Equal(MasterNode):
    icon = "equal.png"
    name = "Equal"
    category = "FUNCTION"
    sub_category = "Logic"
    node_color = logicOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[6, 6], outputs=[3])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        A = self.get_my_input_code(0)
        B = self.get_my_input_code(1)

        if self.syntax == "Python":
            python_code = self.outputs[0].socket_code = f"({A}=={B})"
            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = self.outputs[0].socket_code = f"({A}=={B})"
            raw_code = CPP_code

        return self.grNode.highlight_code(raw_code)


# Math
class Add(MasterNode):
    icon = "add.png"
    name = "Add"
    category = "FUNCTION"
    sub_category = "Math"
    node_color = mathOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        A = self.get_my_input_code(0)
        B = self.get_my_input_code(1)

        if self.syntax == "Python":
            python_code = self.outputs[0].socket_code = f"({A}+{B})"
            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = self.outputs[0].socket_code = f"({A}+{B})"
            raw_code = CPP_code

        return self.grNode.highlight_code(raw_code)


class Sub(MasterNode):
    icon = "sub.png"
    name = "Subtract"
    category = "FUNCTION"
    sub_category = "Math"
    node_color = mathOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        A = self.get_my_input_code(0)
        B = self.get_my_input_code(1)

        if self.syntax == "Python":
            python_code = self.outputs[0].socket_code = f"({A}+{B})"
            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = self.outputs[0].socket_code = f"({A}+{B})"
            raw_code = CPP_code

        return self.grNode.highlight_code(raw_code)


class Mul(MasterNode):
    icon = "mul.png"
    name = "Multiply"
    category = "FUNCTION"
    sub_category = "Math"
    node_color = mathOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        A = self.get_my_input_code(0)
        B = self.get_my_input_code(1)

        if self.syntax == "Python":
            python_code = self.outputs[0].socket_code = f"({A}*{B})"
            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = self.outputs[0].socket_code = f"({A}*{B})"
            raw_code = CPP_code

        return self.grNode.highlight_code(raw_code)


class Div(MasterNode):
    icon = "divide.png"
    name = "Divide"
    category = "FUNCTION"
    sub_category = "Math"
    node_color = mathOperators

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.showCode = False

    def getNodeCode(self):
        raw_code = "Empty"
        A = self.get_my_input_code(0)
        B = self.get_my_input_code(1)

        if self.syntax == "Python":
            python_code = self.outputs[0].socket_code = f"({A}/{B})"
            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = self.outputs[0].socket_code = f"({A}/{B})"
            raw_code = CPP_code

        return self.grNode.highlight_code(raw_code)


# Input
class UserInput(MasterNode):
    icon = "user input.png"
    name = "User Input"
    category = "FUNCTION"
    sub_category = "Input"
    node_color = "#505050"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 6, 4], outputs=[0])

    def getNodeCode(self):
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        brotherCode = self.get_other_socket_code(0)
        inputName = self.get_my_input_code(1)
        if inputName != "" and inputName is not None: inputName += " = "
        inputCode = self.get_my_input_code(2)

        if self.syntax == "Python":
            python_code = f"""
{inputName}input("{inputCode}")
{brotherCode}"""

            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = f"""
cout &lt;&lt; "{inputCode}", cin >> {inputName};
{brotherCode}"""

            raw_code = CPP_code
        return self.grNode.highlight_code(raw_code)


class RawCode(MasterNode):
    icon = "Row Code.png"
    name = "Raw Code"
    category = "FUNCTION"
    sub_category = "Input"
    node_color = "#303030"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 4], outputs=[0])

    def getNodeCode(self):
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        brotherCode = self.get_other_socket_code(0)
        inputCode = self.get_my_input_code(1)

        if self.syntax == "Python":
            python_code = f"""
{inputCode}
{brotherCode}"""

            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = f"""
{inputCode}
{brotherCode}"""

            raw_code = CPP_code
        return self.grNode.highlight_code(raw_code)


# Output
class Print(MasterNode):
    icon = "print.png"
    name = "Print"
    category = "FUNCTION"
    sub_category = "Output"
    node_color = "#90702070"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 6], outputs=[0])

    def getNodeCode(self):
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        brotherCode = self.get_other_socket_code(0)
        printCode = self.get_my_input_code(1)

        if self.syntax == "Python":
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
            if self.isInputConnected(1):
                CPP_code = f"""
cout &lt;&lt; {printCode};
{brotherCode}"""

            else:
                CPP_code = f"""
cout &lt;&lt; "{printCode}";
{brotherCode}"""

            raw_code = CPP_code

        return self.grNode.highlight_code(raw_code)


class Return(MasterNode):
    icon = "return.png"
    name = "Return"
    category = "FUNCTION"
    sub_category = "Output"
    node_color = "#90702070"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 6], outputs=[])

    def getNodeCode(self):
        raw_code = "Empty"
        self.showCode = not self.isInputConnected(0)
        brotherCode = self.get_other_socket_code(0)
        printCode = self.get_my_input_code(1)

        if self.syntax == "Python":
            python_code = f"""
return {printCode}
{brotherCode}"""
            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = f"""
return {printCode};
{brotherCode}"""
            raw_code = CPP_code
        return self.grNode.highlight_code(raw_code)


# Khyria Efforts
# code = f"""<pre><b><span style=\" Font-size:20px ; background-color:#553E0B0B;\"  >
# if {condition}:
# {textwrap.indent(true, "    ")}
# else:
# {textwrap.indent(false, "    ")}</span></pre>"""