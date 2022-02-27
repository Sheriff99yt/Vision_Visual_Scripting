from qtpy.QtWidgets import *
from qtpy.QtCore import Qt
from examples.example_calculator.nodes_configuration import *
from nodeeditor.node_socket import *
from examples.example_calculator.editor_node_base import MasterNode, MasterGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException


@register_node(OP_NODE_IF)
class If_Statement(MasterNode):
    icon = "icons/if.png"
    op_code = OP_NODE_IF
    op_title = "IF Statement"
    content_label_objname = "calc_node_if_statment"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 3], outputs=[0, 0])

    def getNodeCode(self):
        self.conditionCode = 'bool'
        self.trueCode = """print("True")
"""
        self.falseCode = 'print("False")'
        code ="""if {} is True:
    {}
else:
    {}
""".format(self.conditionCode, self.trueCode, self.falseCode)

        return code



@register_node(OP_NODE_FOR_LOOP)
class For_Loop(MasterNode):
    icon = "icons/Loop.png"
    op_code = OP_NODE_FOR_LOOP
    op_title = "For Loop"
    content_label_objname = "calc_node_for_loop"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 2], outputs=[0, 0])
        pass

    def getNodeCode(self):
        self.i = 'i'
        self.list = 'list'
        self.loopCode ="""
    print(i)"""

        code ="""for {} in {}:
{}
""".format(self.i, self.list, self.loopCode)

        return code


@register_node(PRINT)
class Print(MasterNode):
    icon = "icons/if.png"
    op_code = PRINT
    op_title = "Print"
    content_label_objname = "calc_node_print"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 4], outputs=[0])
        pass

    def getNodeCode(self):
        self.print = 'x'
        code ="""print("{}")""".format(self.print)

        return code