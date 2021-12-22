from Node_Graphics import MyGraphicsNode


class Node():
    def __init__(self, scene, title="Undefined Node"):
        self.scene = scene

        self.title = title

        self.graphicNode = MyGraphicsNode(self, self.title)

        self.scene.addNode(self)
        self.scene.graphicScene.addItem(self.graphicNode)


        self.inputs = []
        self.outputs = []

