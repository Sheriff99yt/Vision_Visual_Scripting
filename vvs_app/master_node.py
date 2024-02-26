from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *

from node_node import Node
from node_graphics_node import QDMGraphicsNode
from utils import dumpException


class MasterNode(Node):
    name = "MasterNode"
    icon = ''

    def __init__(self, scene, inputs, outputs):
        super().__init__(scene, self.name, inputs, outputs, node_icon=self.icon)
        pass

    def serialize(self):
        res = super().serialize()
        res['node_type'] = self.__class__.node_type
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        # print("Deserialized Node '%s'" % self.__class__.__name__, "res:", res)
        return res