import textwrap

from examples.example_calculator.nodes_configuration import *
from examples.example_calculator.master_node import MasterNode, MasterGraphicsNode
from nodeeditor.node_editor_widget import *


@register_node(FUN_EVENT,Fun=True)
class Event(MasterNode):
    icon = "icons/event.png"
    node_ID = FUN_EVENT
    op_title = "Event"
    content_label_objname = "calc_node_event"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[0])
        pass


    def getNodeCode(self):
        EventName = "Event 01"

        childCode = self.getConnectedNodeAtOutput(0)
        if childCode is None:
            childCode = ""
        else:
            childCode = childCode.getNodeCode()
        code = f"""\
def {EventName}(self):
{textwrap.indent(childCode, '     ')}"""

        return code