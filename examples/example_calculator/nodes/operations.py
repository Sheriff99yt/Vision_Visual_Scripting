from examples.example_calculator.nodes_configuration import *
from examples.example_calculator.editor_node_base import *


@register_node(OP_NODE_ADD)
class MasterNode_Add(MasterNode):
    icon = "icons/add.png"
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = "+"
    content_label_objname = "calc_node_bg"

    def evalOperation(self, input1, input2):
        return input1 + input2


@register_node(OP_NODE_SUB)
class MasterNode_Sub(MasterNode):
    icon = "icons/sub.png"
    op_code = OP_NODE_SUB
    op_title = "Substract"
    content_label = "-"
    content_label_objname = "calc_node_bg"

    def evalOperation(self, input1, input2):
        return input1 - input2

@register_node(OP_NODE_MUL)
class MasterNode_Mul(MasterNode):
    icon = "icons/mul.png"
    op_code = OP_NODE_MUL
    op_title = "Multiply"
    content_label = "*"
    content_label_objname = "calc_node_mul"

    def evalOperation(self, input1, input2):
        print('foo')
        return input1 * input2

@register_node(OP_NODE_DIV)
class MasterNode_Div(MasterNode):
    icon = "icons/divide.png"
    op_code = OP_NODE_DIV
    op_title = "Divide"
    content_label = "/"
    content_label_objname = "calc_node_div"

    def evalOperation(self, input1, input2):
        return input1 / input2

# way how to register by function call
# register_node_now(OP_NODE_ADD, CalcNode_Add)

# @register_node(OP_NODE_IF)
# class CalcNode_If(CalcNode):
#     icon = "icons/if.png"
#     op_code = OP_NODE_IF
#     op_title = "If Statment"
#     content_label = ""
#     content_label_objname = "function_if"
#
#     def evalOperation(self, input1):
#         return input1
