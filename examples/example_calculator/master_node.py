from qtpy.QtGui import QImage,QColor
from qtpy.QtCore import QRectF
from qtpy.QtWidgets import QLabel

from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.utils import dumpException


class MasterGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        # self.node_color=QColor("")

    # def initAssets(self):
    #     super().initAssets()
    #     pass

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)
        # if self.node.isDirty(): offset = 0
        # if self.node.isInvalid(): offset = 48
        offset = 0
        self.icons = QImage("")
        painter.drawImage(QRectF(offset, 0, 24, 24), self.icons)

    
    def UpdateIcon(self, icon: None):
        self.icons = QImage(icon)
        print(self.icons)


class MasterContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)

class MasterNode(Node):
    icon = ""
    node_ID = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"

    GraphicsNode_class = MasterGraphicsNode
    NodeContent_class = MasterContent

    def __init__(self, scene, inputs=[2,2], outputs=[1]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)
        self.value = None
        # it's really important to mark all nodes Dirty by default
        # self.markDirty(True)

    # def initSettings(self):
    #     super().initSettings()
    #     pass
    # def evalOperation(self, input1, input2):
    #     return 123
    #
    # def evalImplementation(self):
    #     i1 = self.getInput(0)
    #     i2 = self.getInput(1)
    #
    #     if i1 is None or i2 is None:
    #         self.markInvalid()
    #         self.markDescendantsDirty()
    #         self.grNode.setToolTip("Connect all inputs")
    #         return None
    #
    #     else:
    #         val = self.evalOperation(i1.eval(), i2.eval())
    #         self.value = val
    #         self.markDirty(False)
    #         self.markInvalid(False)
    #         self.grNode.setToolTip("")
    #
    #         self.markDescendantsDirty()
    #         self.evalChildren()
    #
    #         return val
    #
    # def eval(self):
    #     if not self.isDirty() and not self.isInvalid():
    #         print(" _> returning cached %s value:" % self.__class__.__name__, self.value)
    #         return self.value
    #
    #     try:
    #
    #         val = self.evalImplementation()
    #         return val
    #     except ValueError as e:
    #         self.markInvalid()
    #         self.grNode.setToolTip(str(e))
    #         self.markDescendantsDirty()
    #     except Exception as e:
    #         self.markInvalid()
    #         self.grNode.setToolTip(str(e))
    #         dumpException(e)

    def onInputChanged(self, socket=None):
        # print("%s::__onInputChanged" % self.__class__.__name__)
        # self.markDirty()
        # self.eval()
        pass

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.node_ID
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
        return res
    
