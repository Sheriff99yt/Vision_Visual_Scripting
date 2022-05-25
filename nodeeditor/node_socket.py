# -*- coding: utf-8 -*-
"""
A module containing NodeEditor's class for representing Socket and Socket Position Constants.
"""
import math
from time import sleep

from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *

from collections import OrderedDict
from nodeeditor.node_serializable import Serializable

DEBUG = False
DEBUG_REMOVE_WARNINGS = False

# Graphical Socket Classes
# -*- coding: utf-8 -*-
"""
A module containing Graphics representation of a :class:`~nodeeditor.node_socket.Socket`
"""


Socket_Types = {}
Socket_Types[0] = 'Executable'
Socket_Types[1] = 'float'
Socket_Types[3] = 'int'
Socket_Types[2] = 'bool'
Socket_Types[4] = 'string'
Socket_Types[5] = 'list'
Socket_Types[6] = 'list_item'

SOCKET_COLORS = [
    QColor("#aaFFFFFF"),
    QColor("#aa00FF10"),
    QColor("#aa0070FF"),
    QColor("#aaFF1010"),
    QColor("#aaFF10FF"),
    QColor("#aaaaaaaa"),
    QColor("#aaaaaaaa")]

SOCKET_COLORS_HOVERED = [
    QColor("#FFFFFF"),
    QColor("#00FF10"),
    QColor("#0070FF"),
    QColor("#FF1010"),
    QColor("#FF10FF"),
    QColor("#aaaaaa"),
    QColor("#aaaaaa")]

SOCKET_COLORS_CONNECTED = [
    QColor("#FFFFFF"),
    QColor("#00FF10"),
    QColor("#0070FF"),
    QColor("#FF1010"),
    QColor("#FF10FF"),
    QColor("#aaaaaa"),
    QColor("#aaaaaa")]

class QDMGraphicsSocket(QGraphicsItem):
    """Class representing Graphic `Socket` in ``QGraphicsScene``"""

    def __init__(self, socket: 'Socket'):
        """
        :param socket: reference to :class:`~nodeeditor.node_socket.Socket`
        :type socket: :class:`~nodeeditor.node_socket.Socket`
        """
        super().__init__(socket.node.grNode)

        self.is_list = False
        self.isConnected = False
        self.hovered = None
        self.socket = socket

        self.isHighlighted = False

        self.radius = 6
        self.outline_width = 1

        self.paint = self.myPaint

        self.initAssets()

        # shadow = QGraphicsDropShadowEffect()
        # shadow.setXOffset(-2)
        # shadow.setYOffset(2)
        # # setting blur radius (optional step)
        # shadow.setBlurRadius(6)
        # shadow.setColor(QColor(6, 6, 6))
        # # adding shadow to the Socket
        # self.setGraphicsEffect(shadow)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        """Handle hover effect"""
        current_theme = self.socket.node.scene.masterRef.global_switches.switches_Dict["Appearance"]["Theme"][0]
        self.hovered = True
        text_color_index = self.socket.node.scene.masterRef.global_switches.themes_colors["Nodes"].index("Text")
        self.socket.socket_label.setDefaultTextColor(QColor(self.socket.node.scene.masterRef.global_switches.themes_colors[current_theme][text_color_index]))
        self.socket.socket_label.show()
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        """Handle hover effect"""
        self.hovered = False
        self.update()
        self.socket.socket_label.hide()

    @property
    def socket_type(self):
        return self.socket.socket_type

    def getSocketColor(self, key):
        """Returns the ``QColor`` for this ``key``"""
        if type(key) == int:
            return SOCKET_COLORS[key]
        elif type(key) == str:
            return QColor(key)
        return Qt.transparent

    def getHoveredSocketColor(self, key):
        """Returns the ``QColor`` for this ``key``"""
        if type(key) == int:
            return SOCKET_COLORS_HOVERED[key]
        elif type(key) == str:
            return QColor(key)
        return Qt.transparent

    def changeSocketType(self):
        """Change the Socket Type"""
        self._current_color = self.getSocketColor(self.socket_type)
        self._brush = QBrush(self._current_color)
        # print("Socket changed to:", self._color_background.getRgbF())
        self.update()

    def initAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        self.setAcceptHoverEvents(True)

        # determine socket color
        self._current_color = self.getSocketColor(self.socket_type)
        self._color_outline = QColor("#FF101010")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self.getSocketColor(self.socket_type))


    def myPaint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting a circle"""
        painter.setBrush(self._brush)
        painter.setPen(self._pen)

        if self.hovered or self.isConnected:
            painter.setBrush(self.getHoveredSocketColor(self.socket_type))

        else:
            painter.setBrush(self._brush)

        if self.socket_type == 0:
            painter.drawPolygon(QPoint(-self.radius, self.radius), QPoint(self.radius, 0),
                                QPoint(-self.radius, -self.radius))
        elif self.socket_type == 6:
            # This is an Object Reference Socket Type
            painter.drawPolygon(QPoint(-self.radius, 0), QPoint(0, self.radius), QPoint(self.radius, 0), QPoint(0, -self.radius))

        elif self.socket_type == 5:
            # This is an Object Reference Socket Type
            painter.drawRect(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)
            painter.setBrush(QBrush(QColor("#FF101010")))

            if not self.isConnected:
                painter.drawRect(-self.radius // 2, -self.radius // 2, self.radius, self.radius)

        elif self.socket_type == 1 or 2 or 3 or 4:
            painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)
            painter.setBrush(QBrush(QColor("#FF101010")))

            if not self.isConnected:
                painter.drawEllipse(-self.radius // 2, -self.radius // 2, self.radius, self.radius)


    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )


# Functional Socket Classes

# -*- coding: utf-8 -*-
"""
A module containing NodeEditor's class for representing Socket and Socket Position Constants.
"""
from collections import OrderedDict
from nodeeditor.node_serializable import Serializable

LEFT_TOP = 1
LEFT_CENTER = 2
LEFT_BOTTOM = 3
RIGHT_TOP = 4
RIGHT_CENTER = 5
RIGHT_BOTTOM = 6


DEBUG = False
DEBUG_REMOVE_WARNINGS = False

class Socket(Serializable):
    """Class representing Socket."""

    def __init__(self, node: 'Node', index: int = 0, position: int = LEFT_TOP, socket_type: int = 1,
                 multi_edges: bool = True,
                 count_on_this_node_side: int = 1, is_input: bool = False):
        """
        :param node: reference to the :class:`~nodeeditor.node_node.Node` containing this `Socket`
        :type node: :class:`~nodeeditor.node_node.Node`
        :param index: Current index of this socket in the position
        :type index: ``int``
        :param position: Socket position. See :ref:`socket-position-constants`
        :param socket_type: Constant defining type(color) of this socket
        :param multi_edges: Can this socket have multiple `Edges` connected?
        :type multi_edges: ``bool``
        :param count_on_this_node_side: number of total sockets on this position
        :type count_on_this_node_side: ``int``
        :param is_input: Is this an input `Socket`?
        :type is_input: ``bool``

        :Instance Attributes:

            - **node** - reference to the :class:`~nodeeditor.node_node.Node` containing this `Socket`
            - **edges** - list of `Edges` connected to this `Socket`
            - **grSocket** - reference to the :class:`~nodeeditor.node_graphics_socket.QDMGraphicsSocket`
            - **position** - Socket position. See :ref:`socket-position-constants`
            - **index** - Current index of this socket in the position
            - **socket_type** - Constant defining type(color) of this socket
            - **count_on_this_node_side** - number of sockets on this position
            - **is_multi_edges** - ``True`` if `Socket` can contain multiple `Edges`
            - **is_input** - ``True`` if this socket serves for Input
            - **is_output** - ``True`` if this socket serves for Output
        """
        super().__init__()

        self.node = node
        self.socket_code = self.node.name
        self.position = position
        self.index = index
        self.socket_type = socket_type
        self.count_on_this_node_side = count_on_this_node_side
        self.is_multi_edges = multi_edges
        self.is_input = is_input
        self.is_output = not self.is_input

        if DEBUG: print("Socket -- creating with", self.index, self.position, "for nodeeditor", self.node)

        self.grSocket = QDMGraphicsSocket(self)

        self.setSocketPosition()

        self.socketEdges = []

        self.userInputWdg = self.SocketInputs()
        self.socket_label = None

    def getSocketCode(self):
        if self.socket_type == 0:
            return self.node.getNodeCode()
        else:
            return self.socket_code

    def SocketInputs(self):
        if self.is_input:
            userInputWdg = None
            scene_pos = self.grSocket.pos()
            if self.socket_type == 1:
                userInputWdg = QDoubleSpinBox()
                userInputWdg.valueChanged.connect(self.node.scene.node_editor.UpdateTextCode)
                userInputWdg.setButtonSymbols(QAbstractSpinBox.NoButtons)
                userInputWdg.setDecimals(6)
                userInputWdg.setMinimum(float("-inf"))
                userInputWdg.setMaximum(float("inf"))
                userInputWdg.setFixedWidth(self.node.grNode.width - self.grSocket.radius * 6)
                userInputWdg.setMaximumHeight(self.grSocket.radius * 2)
                userInputWdg.setFont(QFont("Roboto", self.grSocket.radius))

            elif self.socket_type == 2:
                userInputWdg = QSpinBox()
                userInputWdg.valueChanged.connect(self.node.scene.node_editor.UpdateTextCode)
                userInputWdg.setButtonSymbols(QAbstractSpinBox.NoButtons)
                userInputWdg.setRange(-1000000000, 1000000000)
                userInputWdg.setFixedWidth(self.node.grNode.width - self.grSocket.radius * 6)
                userInputWdg.setMaximumHeight(self.grSocket.radius * 2)
                userInputWdg.setFont(QFont("Roboto", self.grSocket.radius))

            elif self.socket_type == 3:
                userInputWdg = QCheckBox()
                userInputWdg.stateChanged.connect(self.node.scene.node_editor.UpdateTextCode)
                userInputWdg.setFixedSize(self.grSocket.radius * 2, self.grSocket.radius * 2)
                # userInputWdg.setIconSize(QSize(self.grSocket.radius, self.grSocket.radius))

            elif [4, 5, 6].__contains__(self.socket_type):
                userInputWdg = QTextEdit()
                userInputWdg.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                userInputWdg.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                userInputWdg.textChanged.connect(self.node.scene.node_editor.UpdateTextCode)
                userInputWdg.setFixedWidth(self.node.grNode.width - self.grSocket.radius * 6)
                userInputWdg.setMaximumHeight(self.grSocket.radius * 2)
                userInputWdg.setFont(QFont("Roboto", self.grSocket.radius))

            if userInputWdg:
                sceneProxy = self.node.scene.grScene.addWidget(userInputWdg)
                sceneProxy.setParentItem(self.node.grNode)
                sceneProxy.setPos(int(scene_pos.x() + self.grSocket.radius + 4), int(scene_pos.y() - self.grSocket.radius))

                # if selected_theme == night:
                userInputWdg.setStyleSheet("background-color: #555555; border-width: 1px; border-style: solid; border-color: transparent; color: white")

            return userInputWdg


    def __str__(self):
        return "<Socket #%d %s %s..%s>" % (
            self.index, "ME" if self.is_multi_edges else "SE", hex(id(self))[2:5], hex(id(self))[-3:]
        )

    def delete(self):
        """Delete this `Socket` from graphics scene for sure"""
        self.grSocket.setParentItem(None)
        self.node.scene.grScene.removeItem(self.grSocket)
        del self.grSocket
        del self.socket_label

    def changeSocketType(self, new_socket_type: int) -> bool:
        """
        Change the Socket Type

        :param new_socket_type: new socket type
        :type new_socket_type: ``int``
        :return: Returns ``True`` if the socket type was actually changed
        :rtype: ``bool``
        """
        if self.socket_type != new_socket_type:
            self.socket_type = new_socket_type
            self.grSocket.changeSocketType()
            return True
        return False

    def setSocketPosition(self):
        """Helper function to set `Graphics Socket` position. Exact socket position is calculated
        inside :class:`~nodeeditor.node_node.Node`."""
        self.grSocket.setPos(*self.node.getSocketPosition(self.index, self.position, self.count_on_this_node_side,self.grSocket.radius))

    def getSocketPosition(self):
        """
        :return: Returns this `Socket` position according to the implementation stored in
            :class:`~nodeeditor.node_node.Node`
        :rtype: ``x, y`` position
        """
        if DEBUG: print("  GSP: ", self.index, self.position, "nodeeditor:", self.node)
        res = self.node.getSocketPosition(self.index, self.position, self.count_on_this_node_side, self.grSocket.radius)
        if DEBUG: print("  res", res)
        return res

    def hasAnyEdge(self) -> bool:
        """
        Returns ``True`` if any :class:`~nodeeditor.node_edge.Edge` is connected to this socket

        :return: ``True`` if any :class:`~nodeeditor.node_edge.Edge` is connected to this socket
        :rtype: ``bool``
        """
        hasAnyEdges = len(self.socketEdges) > 0
        if hasAnyEdges:
            if self.userInputWdg is not None : self.userInputWdg.hide()
        else:
            if self.userInputWdg is not None :self.userInputWdg.show()
        return hasAnyEdges

    def isConnected(self, edge: 'Edge') -> bool:
        """
        Returns ``True`` if :class:`~nodeeditor.node_edge.Edge` is connected to this `Socket`

        :param edge: :class:`~nodeeditor.node_edge.Edge` to check if it is connected to this `Socket`
        :type edge: :class:`~nodeeditor.node_edge.Edge`
        :return: ``True`` if `Edge` is connected to this socket
        :rtype: ``bool``
        """

        return edge in self.socketEdges

    def addEdge(self, edge: 'Edge'):
        """
        Append an Edge to the list of connected Edges

        :param edge: :class:`~nodeeditor.node_edge.Edge` to connect to this `Socket`
        :type edge: :class:`~nodeeditor.node_edge.Edge`
        """
        self.socketEdges.append(edge)
        self.grSocket.isConnected = self.hasAnyEdge()

    def removeEdge(self, edge: 'Edge'):
        """
        Disconnect passed :class:`~nodeeditor.node_edge.Edge` from this `Socket`
        :param edge: :class:`~nodeeditor.node_edge.Edge` to disconnect
        :type edge: :class:`~nodeeditor.node_edge.Edge`
        """
        if edge in self.socketEdges:
            self.socketEdges.remove(edge)
            self.grSocket.isConnected = self.hasAnyEdge()
        else:
            if DEBUG_REMOVE_WARNINGS:
                print("!W:", "Socket::removeEdge", "wanna remove edge", edge,
                      "from self.edges but it's not in the list!")
            self.grSocket.isConnected = self.hasAnyEdge()

    def removeAllEdges(self, silent: bool = False):
        """Disconnect all `Edges` from this `Socket`"""
        while self.socketEdges:
            edge = self.socketEdges.pop(0)
            if silent:
                edge.remove(silent_for_socket=self)
            else:
                edge.remove()  # just remove all with notifications
        self.grSocket.isConnected = self.hasAnyEdge()

    def determineMultiEdges(self, data: dict) -> bool:
        """
        Deserialization helper function. In our tutorials we created a new version of graph data format.
        This function is here to help solve the issue of opening older files in the newer format.
        If the 'multi_edges' param is missing in the dictionary, we determine if this `Socket`
        should support multiple `Edges`.

        :param data: `Socket` data in ``dict`` format for deserialization
        :type data: ``dict``
        :return: ``True`` if this `Socket` should support multi_edges
        """
        if 'multi_edges' in data:
            return data['multi_edges']
        else:
            # probably older version of file, make RIGHT socket multi edged by default
            return data['position'] in (RIGHT_BOTTOM, RIGHT_TOP)

    def get_wdg_value(self):
        if self.is_input and self.userInputWdg:
            return self.node.scene.masterRef.get_QWidget_content(self.userInputWdg)

    def serialize(self) -> OrderedDict:

        return OrderedDict([
            ('id', self.id),
            ('index', self.index),
            ('multi_edges', self.is_multi_edges),
            ('position', self.position),
            ('socket_type', self.socket_type),
            ('socket_value', self.get_wdg_value()),
        ])

    def deserialize(self, data: dict, hashmap: dict = {}, restore_id: bool = True) -> bool:
        if restore_id: self.id = data['id']
        self.is_multi_edges = self.determineMultiEdges(data)
        self.changeSocketType(data['socket_type'])
        hashmap[data['id']] = self

        if self.is_input and self.userInputWdg:
            self.node.scene.masterRef.set_QWidget_content(self.userInputWdg, data['socket_value'])
            return True
