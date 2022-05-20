from vvs_app.nodes.default_functions import Indent, FontFamily, FontSize
from vvs_app.nodes.nodes_configuration import *
from vvs_app.master_node import MasterNode
from nodeeditor.node_editor_widget import *



class Event(MasterNode):
    icon = "icons/light/event.png"
    name = "Event"
    category = "EVENT"
    sub_category = "Event"
    node_color = "#90FF1010"

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[0]) if isSetter else super().__init__(scene, inputs=[0], outputs=[0])
        self.is_setter = isSetter
        self.is_event = True

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

            return self.grNode.highlight_code(raw_code)

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

            return self.grNode.highlight_code(raw_code)
