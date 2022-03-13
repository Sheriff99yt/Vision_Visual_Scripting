import textwrap

from examples.example_calculator.nodes.default_functions import Indent
from examples.example_calculator.nodes_configuration import *
from examples.example_calculator.master_node import MasterNode, MasterGraphicsNode
from nodeeditor.node_editor_widget import *


FontSize = 20

@set_event_ID(FUN_EVENT)
class Event(MasterNode):
    icon = "icons/event.png"
    node_type = FUN_EVENT
    name = "Event"
    content_label_objname = "calc_node_event"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[0])
        self.nodeColor = "#55C16401"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        EventName = self.name

        childCode = self.NodeCodeAtOutput(0)

        rawCode = f"""
def {EventName}():
{Indent(childCode)}"""

        colorStyle = f''' style=\" Font-size:20px ; background-color:{self.nodeColor};\"  ''' if self.isSelected() is True else f'  style=\" Font-size:{FontSize}px ;\"   '
        code = f"""<pre><b><span{colorStyle}>{rawCode}</span></pre>"""

        return code
