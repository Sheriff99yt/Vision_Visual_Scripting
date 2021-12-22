from Node_Graphics import MyGraphicsNode
from Node_Content import MyNodeContent
from Socket_Class import *


class Node():
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[]):
        self.scene = scene

        self.title = title

        self.content = MyNodeContent()
        self.graphicsNode = MyGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.graphicScene.addItem(self.graphicsNode)

        self.socket_spacing = 22

        # create socket for inputs and outputs
        self.inputs = []
        self.outputs = []

        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP)
            counter += 1
            self.outputs.append(socket)

    @property
    def pos(self):
        return self.graphicsNode.pos()  # QPointF

    def setPos(self, x, y):
        self.graphicsNode.setPos(x, y)

    def getSocketPosition(self, index, position):
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.graphicsNode.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = self.graphicsNode.height - self.graphicsNode.edge_size - self.graphicsNode._padding - index * self.socket_spacing
        else:
            # start from top
            y = self.graphicsNode.title_height + self.graphicsNode._padding + self.graphicsNode.edge_size + index * self.socket_spacing

        return [x, y]

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.node.updateConnectedEdges()
