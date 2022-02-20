from qtpy.QtWidgets import *
from qtpy.QtCore import Qt
from examples.example_calculator.nodes_configuration import *
from nodeeditor.node_socket import *
from examples.example_calculator.editor_node_base import MasterNode, MasterGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException
from nodeeditor.node_editor_widget import *


@register_node(EXECUTION_EVENT)
class Event(MasterNode):
    icon = "icons/if.png"
    op_code = EXECUTION_EVENT
    op_title = "Event"
    content_label_objname = "calc_node_event"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[0])
        pass


    def getNodeCode(self):
        self.eventName = 'Event 01'
        self.connectedCode = 'print("Test")'
        code = """def {}(self):
    {}""".format(self.eventName, self.connectedCode)
        return code