from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QImage
from qtpy.QtGui import QFont, QColor, QPen, QBrush, QPainterPath

from examples.example_calculator.nodes_configuration import *
from examples.example_calculator.master_node import MasterNode, MasterGraphicsNode
from textwrap import *

FontSize = 20

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
        self.isVar = False
        self.nodeColor = "#553E0B0B"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))


    def getNodeCode(self):
        self.nodeCode = not self.isInputConnected()

        condition = self.InputSocketCodeAt(1)

        true = self.NodeCodeAtOutput(0)

        false = self.NodeCodeAtOutput(1)

        rawCode = f"""
if {condition}:
{Indent(true)}
else:
{Indent(false)}
"""

        colorStyle = f''' style=\" Font-size:20px ; background-color:{self.nodeColor};\"  ''' if self.isSelected() is True else f'  style=\" Font-size:{FontSize}px ;\"   '
        code = f"""<pre><b><span{colorStyle}>{rawCode}</span></pre>"""

# code = f"""<pre><b><span style=\" Font-size:20px ; background-color:#553E0B0B;\"  >
# if {condition}:
# {textwrap.indent(true, "    ")}
# else:
# {textwrap.indent(false, "    ")}</span></pre>"""

        return code


@set_function_ID(FUN_FOR_LOOP)
class ForLoop(MasterNode):
    icon = "icons/Loop.png"
    node_type = FUN_FOR_LOOP
    name = "For Loop"
    content_label_objname = "node_for_loop"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 2, 2], outputs=[0])
        self.isVar = False
        self.grNode.height = 120
        self.nodeColor = "#550A3C67"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))


    def getNodeCode(self):
        self.nodeCode = not self.isInputConnected()

        firstIndex = self.SocketNameAt(1)

        lastIndex = self.SocketNameAt(2)

        loopCode = self.NodeCodeAtOutput(0)

        rawCode = f"""
for {firstIndex} in range({lastIndex}):
{Indent(loopCode)}
"""
        colorStyle = f''' style=\" Font-size:20px ; background-color:{self.nodeColor};\"  ''' if self.isSelected() is True else f'  style=\" Font-size:{FontSize}px ;\"   '
        code = f"""<pre><b><span{colorStyle}>{rawCode}</span></pre>"""

        return code


@set_function_ID(FUN_PRINT)
class Print(MasterNode):
    icon = "icons/print.png"
    node_type = FUN_PRINT
    name = "Print"
    content_label_objname = "node_print"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 4], outputs=[0])
        self.isVar = False
        self.nodeColor = "#55401447"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        self.nodeCode = not self.isInputConnected()

        printCode = self.SocketNameAt(1)
        childCode = self.NodeCodeAtOutput(0)

        rawCode = f"""
print({printCode})
{childCode}"""
        colorStyle = f''' style=\" Font-size:20px ; background-color:{self.nodeColor};\"  ''' if self.isSelected() is True else f'  style=\" Font-size:{FontSize}px ;\"   '
        code = f"""<pre><b><span{colorStyle}>{rawCode}</span></pre>"""

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
        self.isVar = False
        self.nodeCode = False
        self.nodeColor = "#5516602E"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        A = self.InputSocketNodeCodeAt(0)
        B = self.InputSocketNodeCodeAt(1)

        rawCode = f"{A}+{B}"

        self.outputs[0].socketCode = rawCode

        colorStyle = f''' style=\" Font-size:20px ; background-color:{self.nodeColor};\"  ''' if self.isSelected() is True else f'  style=\" Font-size:{FontSize}px ;\"   '
        code = f"""<pre><b><span{colorStyle}>{rawCode}</span></pre>"""

        return code


@set_function_ID(FUN_SUB)
class Sub(MasterNode):
    icon = "icons/sub.png"
    node_type = FUN_SUB
    name = "Subtract"
    content_label = ""
    content_label_objname = "node_subtract"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.isVar = False
        self.nodeCode = False
        self.nodeColor = "#5516602E"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        A = self.InputSocketNodeCodeAt(0)
        B = self.InputSocketNodeCodeAt(1)

        rawCode = f"{A}-{B}"

        self.outputs[0].socketCode = rawCode

        colorStyle = f''' style=\" Font-size:20px ; background-color:{self.nodeColor};\"  ''' if self.isSelected() is True else f'  style=\" Font-size:{FontSize}px ;\"   '
        code = f"""<pre><b><span{colorStyle}>{rawCode}</span></pre>"""

        return code


@set_function_ID(FUN_MUL)
class Mul(MasterNode):
    icon = "icons/mul.png"
    node_type = FUN_MUL
    name = "Multiply"
    content_label = ""
    content_label_objname = "node_mul"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.isVar = False
        self.nodeCode = False
        self.nodeColor = "#5516602E"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        A = self.InputSocketNodeCodeAt(0)
        B = self.InputSocketNodeCodeAt(1)

        rawCode = f"{A}*{B}"

        self.outputs[0].socketCode = rawCode

        colorStyle = f''' style=\" Font-size:20px ; background-color:{self.nodeColor};\"  ''' if self.isSelected() is True else f'  style=\" Font-size:{FontSize}px ;\"   '
        code = f"""<pre><b><span{colorStyle}>{rawCode}</span></pre>"""

        return code


@set_function_ID(FUN_DIV)
class Div(MasterNode):
    icon = "icons/divide.png"
    node_type = FUN_DIV
    name = "Divide"
    content_label = ""
    content_label_objname = "node_div"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.isVar = False
        self.nodeCode = False
        self.nodeColor = "#5516602E"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        A = self.InputSocketNodeCodeAt(0)
        B = self.InputSocketNodeCodeAt(1)

        rawCode = f"{A}/{B}"

        self.outputs[0].socketCode = rawCode

        colorStyle = f''' style=\" Font-size:20px ; background-color:{self.nodeColor};\"  ''' if self.isSelected() is True else f'  style=\" Font-size:{FontSize}px ;\"   '
        code = f"""<pre><b><span{colorStyle}>{rawCode}</span></pre>"""

        return code


@set_function_ID(FUN_GREATER_THAN)
class GreaterThan(MasterNode):
    icon = "icons/more_than.png"
    node_type = FUN_GREATER_THAN
    name = "Greater Than"
    content_label = ""
    content_label_objname = "node_greater_than"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[3])
        self.isVar = False
        self.nodeCode = False
        self.nodeColor = "#55777777"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))


    def getNodeCode(self):
        A = self.InputSocketNodeCodeAt(0)
        B = self.InputSocketNodeCodeAt(1)

        rawCode = f"{A}>{B}"

        self.outputs[0].socketCode = rawCode

        colorStyle = f''' style=\" Font-size:20px ; background-color:{self.nodeColor};\"  ''' if self.isSelected() is True else f'  style=\" Font-size:{FontSize}px ;\"   '
        code = f"""<pre><b><span{colorStyle}>{rawCode}</span></pre>"""

        return code


@set_function_ID(FUN_LESS_THAN)
class LessThan(MasterNode):
    icon = "icons/less_than.png"
    node_type = FUN_LESS_THAN
    name = "Less Than"
    content_label = ""
    content_label_objname = "node_less_than"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[3])
        self.isVar = False
        self.nodeCode = False
        self.nodeColor = "#55777777"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))


    def getNodeCode(self):
        A = self.InputSocketNodeCodeAt(0)
        B = self.InputSocketNodeCodeAt(1)

        rawCode = f"{A}<{B}"

        self.outputs[0].socketCode = rawCode

        colorStyle = f''' style=\" Font-size:20px ; background-color:{self.nodeColor};\"  ''' if self.isSelected() is True else f'  style=\" Font-size:{FontSize}px ;\"   '
        code = f"""<pre><b><span{colorStyle}>{rawCode}</span></pre>"""

        return code


@set_function_ID(FUN_Equal)
class Equal(MasterNode):
    icon = "icons/equal.png"
    node_type = FUN_Equal
    name = "Equal"
    content_label = ""
    content_label_objname = "node_equal"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[3])
        self.isVar = False
        self.nodeCode = False
        self.nodeColor = "#55777777"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        A = self.InputSocketNodeCodeAt(0)
        B = self.InputSocketNodeCodeAt(1)

        rawCode = f"{A}=={B}"

        self.outputs[0].socketCode = rawCode

        colorStyle = f''' style=\" Font-size:20px ; background-color:{self.nodeColor};\"  ''' if self.isSelected() is True else f'  style=\" Font-size:{FontSize}px ;\"   '
        code = f"""<pre><b><span{colorStyle}>{rawCode}</span></pre>"""

        return code


@set_function_ID(FUN_AND)
class And(MasterNode):
    icon = "icons/and.png"
    node_type = FUN_AND
    name = "And"
    content_label = ""
    content_label_objname = "node_and"

    def __init__(self, scene):
        super().__init__(scene, inputs=[3, 3], outputs=[3])
        self.isVar = False
        self.nodeCode = False
        self.nodeColor = "#55777777"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        A = self.InputSocketNodeCodeAt(0)
        B = self.InputSocketNodeCodeAt(1)

        rawCode = f"{A} and {B}"

        self.outputs[0].socketCode = rawCode

        colorStyle = f''' style=\" Font-size:20px ; background-color:{self.nodeColor};\"  ''' if self.isSelected() is True else f'  style=\" Font-size:{FontSize}px ;\"   '
        code = f"""<pre><b><span{colorStyle}>{rawCode}</span></pre>"""

        return code
