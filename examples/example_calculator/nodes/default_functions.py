from examples.example_calculator.nodes_configuration import *
from examples.example_calculator.master_node import MasterNode, MasterGraphicsNode


@register_node(FUN_IF)
class If_Statement(MasterNode):
    icon = "icons/if.png"
    op_code = FUN_IF
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



@register_node(FUN_FOR_LOOP)
class For_Loop(MasterNode):
    icon = "icons/Loop.png"
    op_code = FUN_FOR_LOOP
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



@register_node(FUN_PRINT)
class Print(MasterNode):
    icon = "icons/if.png"
    op_code = FUN_PRINT
    op_title = "Print"
    content_label_objname = "calc_node_print"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 4], outputs=[0])
        pass

    def getNodeCode(self):
        self.print = 'x'
        code ="""print("{}")""".format(self.print)
        return code



@register_node(FUN_ADD)
class MasterNode_Add(MasterNode):
    icon = "icons/add.png"
    op_code = FUN_ADD
    op_title = "Add"
    content_label = "+"
    content_label_objname = "calc_node_bg"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        pass



@register_node(FUN_SUB)
class MasterNode_Sub(MasterNode):
    icon = "icons/sub.png"
    op_code = FUN_SUB
    op_title = "Substract"
    content_label = "-"
    content_label_objname = "calc_node_bg"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        pass



@register_node(FUN_MUL)
class MasterNode_Mul(MasterNode):
    icon = "icons/mul.png"
    op_code = FUN_MUL
    op_title = "Multiply"
    content_label = "*"
    content_label_objname = "calc_node_mul"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        pass



@register_node(FUN_DIV)
class MasterNode_Div(MasterNode):
    icon = "icons/divide.png"
    op_code = FUN_DIV
    op_title = "Divide"
    content_label = "/"
    content_label_objname = "calc_node_div"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        pass
