# -*- coding: utf-8 -*-
"""
A module containing NodeEditor's class for representing `Node`.
"""
import socket
from collections import OrderedDict

from PyQt5.QtWidgets import *

from nodeeditor.node_graphics_node import QDMGraphicsNode
from PyQt5.QtGui import QColor
from nodeeditor.node_serializable import Serializable
from nodeeditor.node_socket import Socket, LEFT_BOTTOM, LEFT_CENTER, LEFT_TOP, RIGHT_BOTTOM, RIGHT_CENTER, RIGHT_TOP
from nodeeditor.utils import dumpException, pp

DEBUG = False


class Node(Serializable):
    """
    Class representing `Node` in the `Scene`.
    """
    GraphicsNode_class = QDMGraphicsNode
    Socket_class = Socket

    def __init__(self, scene: 'Scene', name: str = "Undefined Node", inputs: list = [], outputs: list = []):
        """

        :param scene: reference to the :class:`~nodeeditor.node_scene.Scene`
        :type scene: :class:`~nodeeditor.node_scene.NodeScene`
        :param name: Node Title shown in Scene
        :type name: str
        :param inputs: list of :class:`~nodeeditor.node_socket.Socket` types from which the `Sockets` will be auto created
        :param outputs: list of :class:`~nodeeditor.node_socket.Socket` types from which the `Sockets` will be auto created

        :Instance Attributes:

            - **scene** - reference to the :class:`~nodeeditor.node_scene.Scene`
            - **grNode** - Instance of :class:`~nodeeditor.node_graphics_node.QDMGraphicsNode` handling graphical representation in the ``QGraphicsScene``. Automatically created in the constructor
            - **content** - Instance of :class:`~nodeeditor.node_graphics_content.QDMGraphicsContent` which is child of ``QWidget`` representing container for all inner widgets inside of the Node. Automatically created in the constructor
            - **inputs** - list containin Input :class:`~nodeeditor.node_socket.Socket` instances
            - **outputs** - list containin Output :class:`~nodeeditor.node_socket.Socket` instances

        """
        super().__init__()

        self._name = name

        self.scene = scene

        # Additional Code
        self.isVar = False
        self.isEvent = False
        self.isSetter = None
        self.showCode = True

        self.nodeID = None

        self.syntax = ""

        # just to be sure, init these variables
        self.grNode = None

        self.initInnerClasses()
        self.initSettings()

        self.name = name

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs = []
        self.outputs = []

        self.initSockets(inputs, outputs)


    def getSocketCode(self, socketID):
        # print(len(self.inputs))
        return self.inputs[socketID].socketCode

    def getNodeOrder(self):
        currentOrder = self.scene.nodes.index(self)
        # print(currentOrder)
        return currentOrder

    def __str__(self):
        return "<%s:%s %s..%s>" % (self.name, self.__class__.__name__, hex(id(self))[2:5], hex(id(self))[-3:])

    @property
    def name(self):
        """
        Name shown in the scene

        :getter: return current Node title
        :setter: sets Node title and passes it to Graphics Node class
        :type: ``str``
        """
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name
        self.grNode.name = self._name

    @property
    def pos(self):
        """
        Retrieve Node's position in the Scene

        :return: Node position
        :rtype: ``QPointF``
        """
        return self.grNode.pos()  # QPointF

    def setPos(self, x: float, y: float):
        """
        Sets position of the Graphics Node

        :param x: X `Scene` position
        :param y: Y `Scene` position
        """
        self.grNode.setPos(x, y)

    def initInnerClasses(self):
        """Sets up graphics Node (PyQt) and Content Widget"""
        graphics_node_class = self.getGraphicsNodeClass()
        if graphics_node_class is not None: self.grNode = graphics_node_class(self)

    def getGraphicsNodeClass(self):
        return self.__class__.GraphicsNode_class

    def initSettings(self):
        """Initialize properties and socket information"""
        self.socket_spacing = 20
        self.LR_offset = 6
        self.input_socket_position = LEFT_TOP
        self.output_socket_position = RIGHT_TOP
        self.input_multi_edged = False
        self.output_multi_edged = True

        self.socket_offsets = {
            LEFT_BOTTOM: -1,
            LEFT_CENTER: -1,
            LEFT_TOP: -1,
            RIGHT_BOTTOM: 1,
            RIGHT_CENTER: 1,
            RIGHT_TOP: 1,
        }

    def initSockets(self, inputs: list, outputs: list, reset: bool = True):
        """
        Create sockets for inputs and outputs

        :param inputs: list of Socket Types (int)
        :type inputs: ``list``
        :param outputs: list of Socket Types (int)
        :type outputs: ``list``
        :param reset: if ``True`` destroys and removes old `Sockets`
        :type reset: ``bool``
        """

        if reset:
            # clear old sockets
            if hasattr(self, 'inputs') and hasattr(self, 'outputs'):
                # remove grSockets from scene
                for socket in (self.inputs + self.outputs):
                    self.scene.grScene.removeItem(socket.grSocket)
                self.inputs = []
                self.outputs = []

        # create new sockets
        counter = 0
        for item in inputs:
            socket = self.__class__.Socket_class(
                node=self, index=counter, position=self.input_socket_position,
                socket_type=item, multi_edges=self.input_multi_edged,
                count_on_this_node_side=len(inputs), is_input=True)

            socket.is_multi_edges = True if socket.socket_type == 0 else False

            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = self.__class__.Socket_class(
                node=self, index=counter, position=self.output_socket_position,
                socket_type=item, multi_edges=self.output_multi_edged,
                count_on_this_node_side=len(outputs), is_input=False)

            socket.is_multi_edges = False if socket.socket_type == 0 else True

            counter += 1
            self.outputs.append(socket)

        self.grNode.AutoResizeGrNode()


    def updateSockets(self):
        pass

    def onEdgeConnectionChanged(self, new_edge: 'Edge'):
        """
        Event handling that any connection (`Edge`) has changed. Currently not used...

        :param new_edge: reference to the changed :class:`~nodeeditor.node_edge.Edge`
        :type new_edge: :class:`~nodeeditor.node_edge.Edge`
        """
        self.scene.NodeEditor.UpdateTextCode()

    def onInputChanged(self, socket: 'Socket'):
        """Event handling when Node's input Edge has changed. We auto-mark this `Node` to be `Dirty` with all it's
        descendants

        :param socket: reference to the changed :class:`~nodeeditor.node_socket.Socket`
        :type socket: :class:`~nodeeditor.node_socket.Socket`
        """

        pass

    def onDeserialized(self, data: dict):
        """Event manually called when this node was deserialized. Currently called when node is deserialized from scene
        Passing `data` containing the data which have been deserialized
        """
        pass

    def onDoubleClicked(self, event):
        """Event handling double click on Graphics Node in `Scene`"""
        pass

    def doSelect(self, new_state: bool = True):
        """Shortcut method for selecting/deselecting the `Node`

        :param new_state: ``True`` if you want to select the `Node`. ``False`` if you want to deselect the `Node`
        :type new_state: ``bool``
        """
        self.grNode.doSelect(new_state)

    def isSelected(self):
        """Returns ``True`` if current `Node` is selected"""
        return self.grNode.isSelected()

    def hasConnectedEdge(self, edge: 'Edge'):
        """Returns ``True`` if edge is connected to any :class:`~nodeeditor.node_socket.Socket` of this `Node`"""
        for socket in (self.inputs + self.outputs):
            if socket.hasAnyEdge(edge):
                return True
        return False

    def getSocketPosition(self, index: int, position: int, num_out_of: int = 1) -> '(x, y)':
        """
        Get the relative `x, y` position of a :class:`~nodeeditor.node_socket.Socket`. This is used for placing
        the `Graphics Sockets` on `Graphics Node`.

        :param index: Order number of the Socket. (0, 1, 2, ...)
        :type index: ``int``
        :param position: `Socket Position Constant` describing where the Socket is located. See :ref:`socket-position-constants`
        :type position: ``int``
        :param num_out_of: Total number of Sockets on this `Socket Position`
        :type num_out_of: ``int``
        :return: Position of described Socket on the `Node`
        :rtype: ``x, y``
        """

        x = self.socket_offsets[position] + self.LR_offset if (
                position in (LEFT_TOP, LEFT_CENTER, LEFT_BOTTOM)) else self.grNode.width + self.socket_offsets[
            position] - self.LR_offset

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = self.grNode.height - self.grNode.edge_roundnes - self.grNode.title_vertical_padding - index * self.socket_spacing

        elif position in (LEFT_CENTER, RIGHT_CENTER):
            num_sockets = num_out_of
            node_height = self.grNode.height
            top_offset = self.grNode.title_height + 2 * self.grNode.title_vertical_padding + self.grNode.edge_padding
            available_height = node_height - top_offset

            total_height_of_all_sockets = num_sockets * self.socket_spacing
            new_top = available_height - total_height_of_all_sockets

            # y = top_offset + index * self.socket_spacing + new_top / 2
            y = top_offset + available_height / 2.0 + (index - 0.5) * self.socket_spacing
            if num_sockets > 1:
                y -= self.socket_spacing * (num_sockets - 1) / 2

        elif position in (LEFT_TOP, RIGHT_TOP):
            # start from top
            y = self.grNode.title_height + self.grNode.title_vertical_padding + self.grNode.edge_roundnes + index * self.socket_spacing
        else:
            # this should never happen
            y = 0

        return [x, y]


    def getSocketScenePosition(self, socket: 'Socket') -> '(x, y)':
        """
        Get absolute Socket position in the Scene

        :param socket: `Socket` which position we want to know
        :return: (x, y) Socket's scene position
        """
        nodepos = self.grNode.pos()
        socketpos = self.getSocketPosition(socket.index, socket.position, socket.count_on_this_node_side)
        return (nodepos.x() + socketpos[0], nodepos.y() + socketpos[1])

    def updateConnectedEdges(self):
        """Recalculate (Refresh) positions of all connected `Edges`. Used for updating Graphics Edges"""
        for socket in self.inputs + self.outputs:
            # if socket.hasEdge():
            for edge in socket.socketEdges:
                edge.updatePositions()

    def remove(self):
        """Safely remove this Node"""

        if DEBUG: print("> Removing Node", self)
        if DEBUG: print(" - remove all edges from sockets")
        for socket in (self.inputs + self.outputs):
            # if socket.hasEdge():
            for edge in socket.socketEdges.copy():
                if DEBUG: print("    - removing from socket:", socket, "edge:", edge)
                edge.remove()
        if DEBUG: print(" - remove grNode")
        self.scene.grScene.removeItem(self.grNode)
        self.grNode = None
        if DEBUG: print(" - remove node from the scene")
        self.scene.removeNode(self)
        if DEBUG: print(" - everything was done.")

    # def markDescendantsDirty(self, new_value: bool=True):
    #     """Mark all children and descendants of this `Node` to be `Dirty`. Not this `Node` it self
    #
    #     :param new_value: ``True`` if children and descendants should be `Dirty`. ``False`` if you want to un-dirty children and descendants
    #     :type new_value: ``bool``
    #     """
    #     for other_node in self.getChildrenNodes():
    #         other_node.markDirty(new_value)
    #         other_node.markDescendantsDirty(new_value)
    #

    def getChildrenNodes(self) -> 'List[Node]':
        """
        Retreive all first-level children connected to this `Node` `Outputs`

        :return: list of `Nodes` connected to this `Node` from all `Outputs`
        :rtype: List[:class:`~nodeeditor.node_node.Node`]
        """
        if self.outputs == []: return []
        other_nodes = []
        for ix in range(len(self.outputs)):
            for edge in self.outputs[ix].socketEdges:
                other_node = edge.getOtherSocket(self.outputs[ix]).node
                other_nodes.append(other_node)
        return other_nodes

    def NodeCodeAtInput(self, index: int = 0):
        if not self.inputs or index > len(self.inputs)-1:
            print("Trying to call from Node Input socket while Node has no input socket")
            return None

        input_socket = self.inputs[index]
        if len(input_socket.socketEdges) == 0: return self.getSocketWdgValue(input_socket)
        connecting_edge = input_socket.socketEdges[0]
        other_socket = connecting_edge.getOtherSocket(self.inputs[index])
        if other_socket is None: return self.getSocketWdgValue(input_socket)
        return other_socket.node.getNodeCode()

    def getSocketWdgValue(self, input_socket):
        if input_socket.socket_type == 1 or input_socket.socket_type == 2:
            return input_socket.userInputWdg.value()

        elif input_socket.socket_type == 3:
            return input_socket.userInputWdg.isChecked()

        elif input_socket.socket_type == 4:
            return input_socket.userInputWdg.text()

    def getConnectedInputNode(self, index: int = 0):
        input_socket = self.inputs[index]
        if len(input_socket.socketEdges) == 0: return None
        connecting_edge = input_socket.socketEdges[0]
        other_socket = connecting_edge.getOtherSocket(self.inputs[index])
        return other_socket.node

    def isInputConnected(self, index: int = 0):
        if not self.inputs:
            print("Trying to call from Node Input socket while Node has no input socket")
            return

        input_socket = self.inputs[index]
        if len(input_socket.socketEdges) == 0:
            return False
        else:
            return True

    # def InputSocketCodeAt(self, index: int = 0):
    #     input_socket = self.inputs[index]
    #     if len(input_socket.socketEdges) == 0: return ""
    #     connecting_edge = input_socket.socketEdges[0]
    #     other_socket = connecting_edge.getOtherSocket(self.inputs[index])
    #
    #     if other_socket is None:
    #         return ""
    #     else:
    #         return other_socket.socketCode

    def InputSocketNameAt(self, index: int = 0):
        input_socket = self.inputs[index]
        if len(input_socket.socketEdges) == 0: return ""
        connecting_edge = input_socket.socketEdges[0]
        other_socket = connecting_edge.getOtherSocket(self.inputs[index])

        if other_socket is None:
            return ""
        else:
            return other_socket.socketName

    def SocketValueAt(self, index: int = 0):
        input_socket = self.inputs[index]
        if len(input_socket.socketEdges) == 0: return ""
        connecting_edge = input_socket.socketEdges[0]
        other_socket = connecting_edge.getOtherSocket(self.inputs[index])
        return other_socket.socketValue

    def getInput(self, index: int = 0) -> ['Node', None]:
        """
        Get the **first**  `Node` connected to the  Input specified by `index`

        :param index: Order number of the `Input Socket`
        :type index: ``int``
        :return: :class:`~nodeeditor.node_node.Node` which is connected to the specified `Input` or ``None`` if
            there is no connection or the index is out of range
        :rtype: :class:`~nodeeditor.node_node.Node` or ``None``
        """
        try:
            input_socket = self.inputs[index]
            if len(input_socket.socketEdges) == 0: return None
            connecting_edge = input_socket.socketEdges[0]
            other_socket = connecting_edge.getOtherSocket(self.inputs[index])
            return other_socket.node
        except Exception as e:
            dumpException(e)
            return None

    def getInputWithSocket(self, index: int = 0) -> [('Node', 'Socket'), (None, None)]:
        """
        Get the **first**  `Node` connected to the Input specified by `index` and the connection `Socket`

        :param index: Order number of the `Input Socket`
        :type index: ``int``
        :return: Tuple containing :class:`~nodeeditor.node_node.Node` and :class:`~nodeeditor.node_socket.Socket` which
            is connected to the specified `Input` or ``None`` if there is no connection or the index is out of range
        :rtype: (:class:`~nodeeditor.node_node.Node`, :class:`~nodeeditor.node_socket.Socket`)
        """
        try:
            input_socket = self.inputs[index]
            if len(input_socket.socketEdges) == 0: return None, None
            connecting_edge = input_socket.socketEdges[0]
            other_socket = connecting_edge.getOtherSocket(self.inputs[index])
            return other_socket.node, other_socket
        except Exception as e:
            dumpException(e)
            return None, None

    def getInputWithSocketIndex(self, index: int = 0) -> ('Node', int):
        """
        Get the **first**  `Node` connected to the Input specified by `index` and the connection `Socket`

        :param index: Order number of the `Input Socket`
        :type index: ``int``
        :return: Tuple containing :class:`~nodeeditor.node_node.Node` and :class:`~nodeeditor.node_socket.Socket` which
            is connected to the specified `Input` or ``None`` if there is no connection or the index is out of range
        :rtype: (:class:`~nodeeditor.node_node.Node`, int)
        """
        try:
            edge = self.inputs[index].socketEdges[0]
            socket = edge.getOtherSocket(self.inputs[index])
            return socket.node, socket.index
        except IndexError:
            # print("EXC: Trying to get input with socket index %d, but none is attached to" % index, self)
            return None, None
        except Exception as e:
            dumpException(e)
            return None, None

    def NodeAtOutput(self, index: int = 0) -> 'Node':
        """
        Get the **first**  `Node` connected to the output specified by `index` and the connection `Socket`

        :param index: Order number of the `Input Socket`
        :type index: ``int``
        :return: Tuple containing :class:`~nodeeditor.node_node.Node` and :class:`~nodeeditor.node_socket.Socket` which
            is connected to the specified `Input` or ``None`` if there is no connection or the index is out of range
        :rtype: (:class:`~nodeeditor.node_node.Node`, int)
        """
        try:
            edge = self.outputs[index].socketEdges[0]
            socket = edge.getOtherSocket(self.outputs[index])
            if socket is None:
                return ""
            else:
                return socket.node

        except IndexError:
            # print("EXC: Trying to get input with socket index %d, but none is attached to" % index, self)
            return None
        except Exception as e:
            dumpException(e)
            return None

    def NodeCodeAtOutput(self, index: int = 0):
        """
        Get the **first**  `Node` connected to the output specified by `index` and the connection `Socket`

        :param index: Order number of the `Input Socket`
        :type index: ``int``
        :return: Tuple containing :class:`~nodeeditor.node_node.Node` and :class:`~nodeeditor.node_socket.Socket` which
            is connected to the specified `Input` or ``None`` if there is no connection or the index is out of range
        :rtype: (:class:`~nodeeditor.node_node.Node`, int)
        """
        try:
            edge = self.outputs[index].socketEdges[0]
            socket = edge.getOtherSocket(self.outputs[index])
            if socket is None:
                return ""
            else:
                return socket.node.getNodeCode()
        except IndexError:
            # print("EXC: Trying to get input with socket index %d, but none is attached to" % index, self)
            return ""
        except Exception as e:
            dumpException(e)
            return ""

    def getInputs(self, index: int = 0) -> 'List[Node]':
        """
        Get **all** `Nodes` connected to the Input specified by `index`

        :param index: Order number of the `Input Socket`
        :type index: ``int``
        :return: all :class:`~nodeeditor.node_node.Node` instances which are connected to the
            specified `Input` or ``[]`` if there is no connection or the index is out of range
        :rtype: List[:class:`~nodeeditor.node_node.Node`]
        """
        ins = []
        for edge in self.inputs[index].socketEdges:
            other_socket = edge.getOtherSocket(self.inputs[index])
            ins.append(other_socket.node)
        return ins

    def getOutputs(self, index: int = 0) -> 'List[Node]':
        """
        Get **all** `Nodes` connected to the Output specified by `index`

        :param index: Order number of the `Output Socket`
        :type index: ``int``
        :return: all :class:`~nodeeditor.node_node.Node` instances which are connected to the
            specified `Output` or ``[]`` if there is no connection or the index is out of range
        :rtype: List[:class:`~nodeeditor.node_node.Node`]
        """
        outs = []
        for edge in self.outputs[index].socketEdges:
            other_socket = edge.getOtherSocket(self.outputs[index])
            outs.append(other_socket.node)
        return outs

    # serialization functions

    def serialize(self) -> OrderedDict:
        inputs, outputs = [], []
        for socket in self.inputs: inputs.append(socket.serialize())
        for socket in self.outputs: outputs.append(socket.serialize())
        return OrderedDict([
            ('id', self.id),
            ('name', self.name),
            ('pos_x', self.grNode.scenePos().x()),
            ('pos_y', self.grNode.scenePos().y()),
            ('inputs', inputs),
            ('outputs', outputs),
            ('is_var', self.isVar),
            ('is_setter', self.isSetter),
        ])

    def deserialize(self, data: dict, hashmap: dict = {}, restore_id: bool = True, *args, **kwargs) -> bool:
        try:
            if restore_id: self.id = data['id']
            hashmap[data['id']] = self

            self.setPos(data['pos_x'], data['pos_y'])
            self.name = data['name']
            self.grNode.name = self.name
            self.syntax = self.scene.NodeEditor.syntax_selector.currentText()

            data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
            data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
            num_inputs = len(data['inputs'])
            num_outputs = len(data['outputs'])

            # print("> deserialize node,   num inputs:", num_inputs, "num outputs:", num_outputs)
            # pp(data)

            # possible way to do it is reuse existing sockets...
            # dont create new ones if not necessary

            for socket_data in data['inputs']:
                found = None
                for socket in self.inputs:
                    # print("\t", socket, socket.index, "=?", socket_data['index'])
                    if socket.index == socket_data['index']:
                        found = socket
                        break
                if found is None:
                    # print("deserialization of socket data has not found input socket with index:", socket_data['index'])
                    # print("actual socket data:", socket_data)
                    # we can create new socket for this
                    found = self.__class__.Socket_class(
                        node=self, index=socket_data['index'], position=socket_data['position'],
                        socket_type=socket_data['socket_type'], count_on_this_node_side=num_inputs,
                        is_input=True
                    )
                    self.inputs.append(found)  # append newly created input to the list
                found.deserialize(socket_data, hashmap, restore_id)

            for socket_data in data['outputs']:
                found = None
                for socket in self.outputs:
                    # print("\t", socket, socket.index, "=?", socket_data['index'])
                    if socket.index == socket_data['index']:
                        found = socket
                        break
                if found is None:
                    # print("deserialization of socket data has not found output socket with index:", socket_data['index'])
                    # print("actual socket data:", socket_data)
                    # we can create new socket for this
                    found = self.__class__.Socket_class(
                        node=self, index=socket_data['index'], position=socket_data['position'],
                        socket_type=socket_data['socket_type'], count_on_this_node_side=num_outputs,
                        is_input=False
                    )
                    self.outputs.append(found)  # append newly created output to the list
                found.deserialize(socket_data, hashmap, restore_id)


            self.isVar = data['is_var']
            self.isSetter = data['is_setter']

            if self.isVar or self.isEvent:
                self.getNodeCode()
                self.grNode.AutoResizeGrNode()



        except Exception as e:
            dumpException(e)

        return True

    def toSetter(self):
        pass

    def toGetter(self):
        pass

    def initUI(self):
        pass

    def getNodeCode(self):
        return None

