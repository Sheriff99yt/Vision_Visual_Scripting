import textwrap

from examples.example_calculator.nodes.default_functions import Indent, FontFamily, FontSize
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
        self.nodeColor = "#90FF1010"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def toGetter(self):
        self.isSetter = False
        self.initSockets(inputs=[0], outputs=[0])
        self.getNodeCode = self.getterCode

    def toSetter(self):
        self.isSetter = True
        self.initSockets(inputs=[], outputs=[0])
        self.getNodeCode = self.setterCode

    def getterCode(self):
        brotherCode = self.NodeCodeAtOutput(0)
        self.showCode = not self.isInputConnected(0)

        rawCode = f"""
{self.name}()
{brotherCode}"""

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        getCode = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{rawCode}</span></p></pre> """


        return getCode


    def setterCode(self):
        childCode = self.NodeCodeAtOutput(0)

        rawCode = f"""
def {self.name}():
{Indent(childCode)}"""

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        setterCode = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{rawCode}</span></p></pre> """

        return setterCode