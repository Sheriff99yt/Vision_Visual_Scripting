from examples.example_calculator.nodes_configuration import *
from examples.example_calculator.master_node import MasterNode, MasterGraphicsNode
from nodeeditor.node_editor_widget import *


@register_node(FUN_EVENT,Fun=True)
class Event(MasterNode):
    icon = ""
    node_ID = FUN_EVENT
    op_title = "Event"
    content_label_objname = "calc_node_event"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[0])
        pass


    def getNodeCode(self):
        self.eventName = "Event 01"
        self.connectedCode = """print("Test")"""
        code = """def {}(self):
    {}""".format(self.eventName, self.connectedCode)
        return code