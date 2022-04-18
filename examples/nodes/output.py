from examples.nodes.nodes_configuration import FUN_OUTPUT
from examples.master_node import *
from nodeeditor.node_content_widget import QDMNodeContentWidget


class CalcOutputContent(QDMNodeContentWidget):
    def initUI(self):
        self.lbl = QLabel("42", self)
        self.lbl.setAlignment(Qt.AlignLeft)
        self.lbl.setObjectName(self.node.content_label_objname)


# @set_function_ID(FUN_OUTPUT)
class MasterNode_Output(MasterNode):
    icon = "icons/out.png"
    node_type = FUN_OUTPUT
    name = "Output"
    content_label_objname = "calc_node_output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])

    def initInnerClasses(self):
        self.content = CalcOutputContent(self)
        self.grNode = MasterGraphicsNode(self)

    def evalImplementation(self):
        input_node = self.getInput(0)
        return
