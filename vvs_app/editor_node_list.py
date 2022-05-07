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
        self.setIconSize(QSize(20, 20))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)

        self.header().hide()
        self.setRootIsDecorated(False)
        self.setColumnCount(2)
        self.setColumnWidth(0, 70)

        self.categories = {"+ Process": None, "+ Logic": None, "+ Math": None, "+ Input": None, "+ Output": None}
        for category in list(self.categories.keys()):
            item = QTreeWidgetItem(self, [category])
            item.setSizeHint(1, QSize(18, 18))
            self.categories[category.replace("+ ", "")] = item
            del self.categories[category]
            once = True
            for i in range(len(FUNCTIONS)):
                if FUNCTIONS[i].sub_category == category.replace("+ ", "") and once:
                    item.setData(Qt.UserRole + 2, Qt.UserRole + 3, FUNCTIONS[i].node_type)
                    item.setData(Qt.UserRole, Qt.UserRole + 1, FUNCTIONS[i].icon)
                    item.setText(1, FUNCTIONS[i].name)
                    item.setIcon(1,QIcon(QPixmap(FUNCTIONS[i].icon)))
                    once = False

        self.itemClicked.connect(lambda: self.currentItem().setText(0, self.currentItem().text(0).replace("+", "-")) if self.currentItem().text(0).__contains__("+") else self.currentItem().setText(0, self.currentItem().text(0).replace("-", "+")))
        self.itemClicked.connect(lambda: self.currentItem().setExpanded(True) if self.currentItem().text(0).__contains__("-") else self.currentItem().setExpanded(False))
        self.setExpandsOnDoubleClick(False)

        self.addMyFunctions()

    def addMyFunctions(self):
        Funs = list(FUNCTIONS.keys())
        for Fun in Funs:
            node = get_node_by_type(Fun)
            self.addMyItem(node.name, node.icon, node)

    def addMyItem(self, name, icon=None, node=None):
        item = QTreeWidgetItem(self.categories[node.sub_category], [name])
        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(0, QIcon(pixmap))
        item.setSizeHint(0, QSize(22, 22))
        item.setFirstColumnSpanned(True)

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, Qt.UserRole + 1, pixmap)
        item.setData(Qt.UserRole + 2, Qt.UserRole + 3, node.node_type)

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

            if item.parent():
                iteme = item.parent()
                iteme.setData(Qt.UserRole + 2, Qt.UserRole + 3, FUNCTIONS[node_type].node_type)
                iteme.setData(Qt.UserRole, Qt.UserRole + 1, FUNCTIONS[node_type].icon)
                iteme.setText(1, FUNCTIONS[node_type].name)
                iteme.setIcon(1, QIcon(QPixmap(FUNCTIONS[node_type].icon)))
        except Exception as e:
            dumpException(e)
