from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QImage
from qtpy.QtGui import QFont, QColor, QPen, QBrush, QPainterPath

from examples.example_calculator.nodes_configuration import *
from examples.example_calculator.master_node import MasterNode, MasterGraphicsNode
import textwrap

@set_node_ID(FUN_IF, Fun=True)
class IfStatement(MasterNode):

    icon = "icons/if.png"
    node_type = FUN_IF
    name = "IF Statement"
    content_label_objname = "node_if_statement"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 3], outputs=[0, 0])
        self.isVar = False

        self.grNode._brush_title = QBrush(QColor("#3E0B0B"))


    def getNodeCode(self):
        self.nodeCode = not self.inputs[0].hasAnyEdge()

        condition = self.getConnectedSocketCode(1) if not None else ""

        true = self.getConnectedNodeAtOutput(0)
        if true is None:
            true = ""
        else:
            true = true.getNodeCode()

        false = self.getConnectedNodeAtOutput(1)
        if false is None:
            false = ""
        else:
            false = false.getNodeCode()

        code = f"""
if {condition}:
    {textwrap.indent(true, "    ")}
else:
    {textwrap.indent(false, "    ")}
"""

        return code

    


@set_node_ID(FUN_FOR_LOOP, Fun=True)
class ForLoop(MasterNode):
    icon = "icons/Loop.png"
    node_type = FUN_FOR_LOOP
    name = "For Loop"
    content_label_objname = "node_for_loop"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 2, 2], outputs=[0])
        self.isVar = False
        self.grNode.height = 120
        self.grNode._brush_title = QBrush(QColor("#0A3C67"))


    def getNodeCode(self):
        self.nodeCode = not self.inputs[0].hasAnyEdge()

        firstIndex = self.getConnectedSocketName(1) if not None else ""

        lastIndex = self.getConnectedSocketName(2) if not None else ""

        loopCode = self.getConnectedNodeAtOutput(0)
        if loopCode is None:
            loopCode = ""
        else:
            loopCode = loopCode.getNodeCode()

        code = f"""
for {firstIndex} in {lastIndex}:
    {textwrap.indent(loopCode, "    ")}"""
        return code


@set_node_ID(FUN_PRINT, Fun=True)
class Print(MasterNode):
    icon = "icons/print.png"
    node_type = FUN_PRINT
    name = "Print"
    content_label_objname = "node_print"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 4], outputs=[0])
        self.isVar = False
        self.grNode._brush_title = QBrush(QColor("#401447"))

    def getNodeCode(self):
        self.nodeCode = not self.inputs[0].hasAnyEdge()

        printCode = self.getConnectedSocketName(1)
        childCode = self.getConnectedNodeAtOutput(0)
        if childCode is None:
            childCode = ""
        else:
            childCode = childCode.getNodeCode()

        code = f"""
print({printCode})
{childCode}"""
        return code


@set_node_ID(FUN_ADD, Fun=True)
class Add(MasterNode):
    icon = "icons/add.png"
    node_type = FUN_ADD
    name = "Add"
    content_label = "+"
    content_label_objname = "node_add"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.isVar = False
        self.nodeCode = False
        self.grNode._brush_title = QBrush(QColor("#16602E"))

    def getNodeCode(self):
        A = self.getConnectedSocketNodeCode(0) if not None else ""
        B = self.getConnectedSocketNodeCode(1) if not None else ""

        code = f"{A}+{B}"

        self.outputs[0].socketCode = code
        return code


@set_node_ID(FUN_SUB, Fun=True)
class Sub(MasterNode):
    icon = "icons/sub.png"
    node_type = FUN_SUB
    name = "Subtract"
    content_label = "-"
    content_label_objname = "node_subtract"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.isVar = False
        self.nodeCode = False
        self.grNode._brush_title = QBrush(QColor("#16602E"))

    def getNodeCode(self):
        A = self.getConnectedSocketNodeCode(0) if not None else ""
        B = self.getConnectedSocketNodeCode(1) if not None else ""

        code = f"{A}-{B}"

        self.outputs[0].socketCode = code
        return code


@set_node_ID(FUN_MUL, Fun=True)
class Mul(MasterNode):
    icon = "icons/mul.png"
    node_type = FUN_MUL
    name = "Multiply"
    content_label = "*"
    content_label_objname = "node_mul"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.isVar = False
        self.nodeCode = False
        self.grNode._brush_title = QBrush(QColor("#16602E"))

    def getNodeCode(self):
        A = self.getConnectedSocketNodeCode(0) if not None else ""
        B = self.getConnectedSocketNodeCode(1) if not None else ""

        code = f"{A}*{B}"

        self.outputs[0].socketCode = code
        return code


@set_node_ID(FUN_DIV, Fun=True)
class Div(MasterNode):
    icon = "icons/divide.png"
    node_type = FUN_DIV
    name = "Divide"
    content_label = "/"
    content_label_objname = "node_div"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.isVar = False
        self.nodeCode = False
        self.grNode._brush_title = QBrush(QColor("#16602E"))

    def getNodeCode(self):
        A = self.getConnectedSocketNodeCode(0) if not None else ""
        B = self.getConnectedSocketNodeCode(1) if not None else ""

        code = f"{A}/{B}"

        self.outputs[0].socketCode = code
        return code


@set_node_ID(FUN_GREATER_THAN, Fun=True)
class GreaterThan(MasterNode):
    icon = "icons/more_than.png"
    node_type = FUN_GREATER_THAN
    name = "Greater Than"
    content_label = ">"
    content_label_objname = "node_greater_than"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[3])
        self.isVar = False
        self.nodeCode = False

    def getNodeCode(self):
        A = self.getConnectedSocketNodeCode(0) if not None else ""
        B = self.getConnectedSocketNodeCode(1) if not None else ""

        code = f"{A}>{B}"

        self.outputs[0].socketCode = code
        return code


@set_node_ID(FUN_LESS_THAN, Fun=True)
class LessThan(MasterNode):
    icon = "icons/less_than.png"
    node_type = FUN_LESS_THAN
    name = "Less Than"
    content_label = "<"
    content_label_objname = "node_less_than"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[3])
        self.isVar = False
        self.nodeCode = False

    def getNodeCode(self):
        A = self.getConnectedSocketNodeCode(0) if not None else ""
        B = self.getConnectedSocketNodeCode(1) if not None else ""

        code = f"{A}<{B}"

        self.outputs[0].socketCode = code
        return code


@set_node_ID(FUN_Equal, Fun=True)
class Equal(MasterNode):
    icon = "icons/equal.png"
    node_type = FUN_Equal
    name = "Equal"
    content_label = "<"
    content_label_objname = "node_equal"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[3])
        self.isVar = False
        self.nodeCode = False

    def getNodeCode(self):
        A = self.getConnectedSocketNodeCode(0) if not None else ""
        B = self.getConnectedSocketNodeCode(1) if not None else ""

        code = f"{A}=={B}"

        self.outputs[0].socketCode = code
        return code


@set_node_ID(FUN_AND, Fun=True)
class And(MasterNode):
    icon = "icons/and.png"
    node_type = FUN_AND
    name = "And"
    content_label = "&"
    content_label_objname = "node_and"

    def __init__(self, scene):
        super().__init__(scene, inputs=[3, 3], outputs=[3])
        self.isVar = False
        self.nodeCode = False

    def getNodeCode(self):
        A = self.getConnectedSocketNodeCode(0) if not None else ""
        B = self.getConnectedSocketNodeCode(1) if not None else ""

        code = f"{A} and {B}"

        self.outputs[0].socketCode = code
        return code
