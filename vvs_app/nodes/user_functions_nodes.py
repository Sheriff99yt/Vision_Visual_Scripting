from vvs_app.nodes.default_functions import Indent, FontFamily, FontSize
from vvs_app.nodes.nodes_configuration import *
from vvs_app.master_node import MasterNode
from nodeeditor.node_editor_widget import *



class UserFunction(MasterNode):
    icon = "event.png"
    name = "user_function"
    category = "User_Function"
    sub_category = "User_Function"
    node_usage = 'function'

    def __init__(self, scene, isSetter):
        if isSetter:
            super().__init__(scene, inputs=[], outputs=[0])
            self.getNodeCode = self.write_function
        else:
            super().__init__(scene, inputs=[0], outputs=[0])
            self.getNodeCode = self.call_function

        self.is_setter = isSetter

    def write_function(self):
        childCode = self.get_other_socket_code(0)
        raw_code = "Empty"
        L_P = "{"
        R_P = "}"

        if self.syntax == "Python":
            python_code = f"""
def {self.name}(){self.get_return()}:
{Indent(childCode)}"""
            raw_code = python_code

        elif self.syntax == "C++":
            CPP_code = f"""
{self.get_return()} {self.name}()
{L_P}
{Indent(childCode)}
{R_P}"""
            raw_code = CPP_code

        elif self.syntax == "Rust":
            rust_code = f"""
fn {self.name}(){self.get_return()} {L_P}
{Indent(childCode)}
{R_P}"""
            raw_code = rust_code
        return self.grNode.highlight_code(raw_code)

    def call_function(self):
        self.showCode = not self.isInputConnected(0)
        brotherCode = self.get_other_socket_code(0)
        raw_code = "Empty"

        if self.syntax == "Python":
            python_code = f"""
{self.name}()
{brotherCode}"""
            raw_code = python_code

        elif self.syntax == "C++":
            cpp_code = f"""
{self.name}();
{brotherCode}"""
            raw_code = cpp_code

        elif self.syntax == "Rust":
            rust_code = f"""
{self.name}();
{brotherCode}"""
            raw_code = rust_code

        return self.grNode.highlight_code(raw_code)
