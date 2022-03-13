import textwrap

from examples.example_calculator.nodes.default_functions import Indent
from examples.example_calculator.nodes_configuration import *
from examples.example_calculator.master_node import MasterNode, MasterGraphicsNode
from nodeeditor.node_editor_widget import *



@set_event_ID(FUN_EVENT)
class Event(MasterNode):
    icon = "icons/event.png"
    node_type = FUN_EVENT
    name = "Event"
    content_label_objname = "calc_node_event"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[0])
        self.grNode._brush_title = QBrush(QColor("#C16401"))

    def getNodeCode(self):
        EventName = self.name

        childCode = self.NodeCodeAtOutput(0)

        code = f"""\
def {EventName}(self):
{Indent(childCode)}"""

        return code

