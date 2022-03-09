import turtle

from PyQt5.QtCore import QRectF, QPoint
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsItem

turtle.forward(100)  # draw base

turtle.left(120)
turtle.forward(100)

turtle.left(120)
turtle.forward(100)

turtle.done()


# -*- coding: utf-8 -*-
from time import sleep
"""
A module containing Graphics representation of a :class:`~nodeeditor.node_socket.Socket`
"""

Exectuable = 0
socket_type =[
    QColor('white'),
    QColor("green"),
    QColor("#blue"),
    QColor("#red"),
    QColor("#purple")]





class QDMGraphicsSocket(QGraphicsItem):
    """Class representing Graphic `Socket` in ``QGraphicsScene``"""
    def __init__(self, socket:'Socket'):
        """
        :param socket: reference to :class:`~nodeeditor.node_socket.Socket`
        :type socket: :class:`~nodeeditor.node_socket.Socket`
        """
        super().__init__(socket.node.grNode)

        self.socket = socket
        self.socket_type = socket_type

        self.isHighlighted = False

        self.radius = 6
        self.outline_width = 1
        self.initAssets()

    def getSocketColor(self, key):
        """Returns the ``QColor`` for this ``key``"""
        if type(key) == Exectuable: return socket_type[0]
        elif type(key) == float: return socket_type[1]
        elif type(key) == int: return socket_type[2]
        elif type(key) == bool: return socket_type[3]
        elif type(key) == str: return socket_type[4]

        return Qt.transparent


    def changeSocketType(self):
        """Change the Socket Type"""
        self._color_background = self.socket_type
        self._brush = QBrush(self._color_background)
        # print("Socket changed to:", self._color_background.getRgbF())
        self.update()

    def initAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""

        # determine socket color
        self._color_background = self.getSocketColor()
        self._color_outline = QColor("#FF000000")
        self._color_highlight = QColor("#FF37A6FF")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._pen_highlight = QPen(self._color_highlight)
        self._pen_highlight.setWidthF(2)
        self._brush = QBrush(self._color_background)


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting a circle"""
        painter.setBrush(self._brush)
        painter.setPen(self._pen if not self.isHighlighted else self._pen_highlight)

        if self.socket_type == Executable:
            painter.drawPolygon(QPoint(-self.radius, self.radius),QPoint(self.radius, 0), QPoint(-self.radius, -self.radius))

        elif self.socket_type == Float or Integer or Boolean or String:
            painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)
        else:
            painter.drawRect(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)


    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )
