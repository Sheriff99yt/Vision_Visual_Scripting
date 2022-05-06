from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from qtpy.QtGui import QPixmap, QIcon, QDrag
from qtpy.QtCore import QSize, Qt, QByteArray, QDataStream, QMimeData, QIODevice, QPoint
from qtpy.QtWidgets import QAbstractItemView, QListWidgetItem

from vvs_app.nodes.nodes_configuration import FUNCTIONS, get_node_by_type, LISTBOX_MIMETYPE
from nodeeditor.utils import dumpException


class NodeList(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # init
        self.setIconSize(QSize(28, 28))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)

        self.header().hide()
        self.setRootIsDecorated(False)

        self.math_list = QTreeWidgetItem(self, ["Math"])
        self.math_list.setSizeHint(0, QSize(28, 28))

        self.addMyFunctions()

    def addMyFunctions(self):
        Funs = list(FUNCTIONS.keys())
        for Fun in Funs:
            node = get_node_by_type(Fun)
            self.addMyItem(node.name, node.icon, node.node_type)

    def addMyItem(self, name, icon=None, node_type=0):
        item = QTreeWidgetItem(self.math_list, [name])
        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(0, QIcon(pixmap))
        item.setSizeHint(0, QSize(28, 28))

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, Qt.UserRole + 1, pixmap)
        item.setData(Qt.UserRole + 2, Qt.UserRole + 3, node_type)

    def startDrag(self, *args, **kwargs):
        try:
            item = self.currentItem()
            node_type = item.data(Qt.UserRole + 2, Qt.UserRole + 3)

            pixmap = QPixmap(item.data(Qt.UserRole, Qt.UserRole + 1))

            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            dataStream << pixmap
            dataStream.writeInt(node_type)
            dataStream.writeQString(item.text(0))
            dataStream.writeQStringList(["N"])

            mimeData = QMimeData()
            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e:
            dumpException(e)
