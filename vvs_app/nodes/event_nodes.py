from vvs_app.nodes.default_functions import Indent, FontFamily, FontSize
from vvs_app.nodes.nodes_configuration import *
from vvs_app.master_node import MasterNode
from nodeeditor.node_editor_widget import *



class User_Function(MasterNode):
    icon = "event.png"
    name = "user_function"
    category = "User_Function"
    sub_category = "User_Function"
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
def {self.name}(){self.get_return()}:
{Indent(childCode)}"""

                raw_code = python_code

            elif self.syntax == "C++":
                childCode = self.get_other_socket_code(0)

                L_P = "{"
                R_P = "}"
                CPP_code = f"""
{self.get_return()} {self.name}()
{L_P}
{Indent(childCode)}
{R_P}"""
                raw_code = CPP_code
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
                self.showCode = not self.isInputConnected(0)

                cpp_code = f"""
{self.name}()"""
                raw_code = cpp_code
            return self.grNode.highlight_code(raw_code)
