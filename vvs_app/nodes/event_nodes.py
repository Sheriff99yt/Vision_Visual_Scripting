from vvs_app.nodes.default_functions import Indent, FontFamily, FontSize
# from vvs_app.nodes.nodes_configuration import *
from vvs_app.master_node import MasterNode
# from nodeeditor.node_editor_widget import *


class Event(MasterNode):
    icon = "icons/event.png"
    name = "Event"
    category = "EVENT"
    sub_category = "Event"
    return_type_dict = {"None": "void"}

    def __init__(self, scene, isSetter):
        super().__init__(scene, inputs=[], outputs=[0]) if isSetter else super().__init__(scene, inputs=[0], outputs=[0])
        self.is_setter = isSetter
        self.is_event = True
        self.set_node_color("#90FF1010")
        self.return_type = self.return_type_dict[list(self.return_type_dict.keys())[0]]

    def getNodeCode(self):
        if self.is_setter:
            if self.syntax == "Python":
                childCode = self.get_other_socket_code(0)

                python_code = f"""
def {self.name}():
{Indent(childCode)}"""

                raw_code = python_code

            elif self.syntax == "C++":
                childCode = self.get_other_socket_code(0)
                L_P = "{"
                R_P = "}"
                CPP_code = f"""
{self.return_type} {self.name}()
{L_P}
{Indent(childCode)}
{R_P}"""
                raw_code = CPP_code
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
                self.showCode = not self.isInputConnected(0)

                cpp_code = f"""
{self.name}()"""

                raw_code = cpp_code
            if self.isSelected() is True:
                colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{self.nodeColor};" '''
            else:
                colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

            getCode = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{raw_code}</span></p></pre> """

            return getCode
