from examples.example_calculator.nodes_configuration import *
from examples.example_calculator.master_node import MasterNode, MasterGraphicsNode


@register_node(FUN_IF,Fun=True)
class If_Statement(MasterNode):
    icon = "icons/if.png"
    node_ID = FUN_IF
    op_title = "IF Statement"
    content_label_objname = "calc_node_if_statement"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 3], outputs=[0, 0])
        pass

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



@register_node(FUN_FOR_LOOP,Fun=True)
class For_Loop(MasterNode):
    icon = "icons/Loop.png"
    node_ID = FUN_FOR_LOOP
    op_title = "For Loop"
    content_label_objname = "calc_node_for_loop"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 2], outputs=[0, 0])
        pass

    def getNodeCode(self):
        self.i = 'i'
        self.list = 'list'
        self.loopCode ="""print(i)"""

        code ="""for {} in {}:
{}
""".format(self.i, self.list, self.loopCode)
        return code



@register_node(FUN_PRINT,Fun=True)
class Print(MasterNode):
    icon = "icons/if.png"
    node_ID = FUN_PRINT
    op_title = "Print"
    content_label_objname = "calc_node_print"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 4], outputs=[0])
        pass

    def getNodeCode(self):
        self.print = 'x'
        code ="""print("{}")""".format(self.print)
        return code



@register_node(FUN_ADD,Fun=True)
class MasterNode_Add(MasterNode):
    icon = "icons/add.png"
    node_ID = FUN_ADD
    op_title = "Add"
    content_label = "+"
    content_label_objname = "calc_node_bg"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        pass



@register_node(FUN_SUB,Fun=True)
class MasterNode_Sub(MasterNode):
    icon = "icons/sub.png"
    node_ID = FUN_SUB
    op_title = "Substract"
    content_label = "-"
    content_label_objname = "calc_node_bg"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        pass



@register_node(FUN_MUL,Fun=True)
class MasterNode_Mul(MasterNode):
    icon = "icons/mul.png"
    node_ID = FUN_MUL
    op_title = "Multiply"
    content_label = "*"
    content_label_objname = "calc_node_mul"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        pass



@register_node(FUN_DIV,Fun=True)
class MasterNode_Div(MasterNode):
    icon = "icons/divide.png"
    node_ID = FUN_DIV
    op_title = "Divide"
    content_label = "/"
    content_label_objname = "calc_node_div"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        pass
