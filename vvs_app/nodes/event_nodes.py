from vvs_app.nodes.default_functions import Indent, FontFamily, FontSize
from vvs_app.nodes.nodes_configuration import *
from vvs_app.master_node import MasterNode
from nodeeditor.node_editor_widget import *



class Event(MasterNode):
    icon = "icons/event.png"
    name = "Event"
    category = "EVENT"
    sub_category = "Event"
    
    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[0]) if isSetter else super().__init__(scene, inputs=[0], outputs=[0])
        self.is_setter = isSetter
        self.is_event = True
        self.nodeColor = "#90FF1010"
        self.grNode._brush_title = QBrush(QColor(self.nodeColor))

    def getNodeCode(self):
        if self.is_setter:
            if self.syntax == "Python":
                childCode = self.get_other_socket_code(0)

                python_code = f"""
def {self.name}():
{Indent(childCode)}"""

                raw_code = python_code

            elif self.syntax == "C++":

                raw_code = self.syntax


            if self.isSelected() is True:
                colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
            else:
                colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

            setterCode = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{raw_code}</span></p></pre> """

            return setterCode

        else:
            if self.syntax == "Python":
                brotherCode = self.get_other_socket_code(0)
                self.showCode = not self.isInputConnected(0)

                python_code = f"""
{self.name}()
{brotherCode}"""

                raw_code = python_code

            elif self.syntax == "C++":

                raw_code = self.syntax


            if self.isSelected() is True:
                colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
            else:
                colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

            getCode = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{raw_code}</span></p></pre> """

            return getCode
