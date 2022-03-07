from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *

from examples.example_calculator.nodes_configuration import VARIABLES, get_class_from_nodesID, LISTBOX_MIMETYPE
from nodeeditor.utils import dumpException


class QDMVarListbox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mylayout = QVBoxLayout()
        self.mylayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mylayout)

        self.myCompoBox = QComboBox()
        self.VarList = QListWidget()
        self.addBtn = QPushButton("Add Variable")
        self.Hlayout = QHBoxLayout()

        self.myCompoBox.setMinimumHeight(28)
        self.addBtn.setMinimumHeight(28)

        self.Hlayout.addWidget(self.myCompoBox)
        self.Hlayout.addWidget(self.addBtn)
        self.Hlayout.setContentsMargins(2, 2, 2, 2)

        self.mylayout.addLayout(self.Hlayout)
        self.mylayout.addWidget(self.VarList)

        self.VarList.setIconSize(QSize(28, 28))
        self.VarList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.VarList.setDragEnabled(True)

        self.VarList.startDrag = self.startDrag
        self.VarList.startDrag = self.startDrag
        self.VarList.itemClicked = self.itemClicked

        self.IDs = []
        self.addAllVars()

    def addAllVars(self):
        Vars = list(VARIABLES.keys())
        Vars.sort()
        for item in Vars:
            node = get_class_from_nodesID(item)

            self.myCompoBox.addItem(node.op_title)
            # print(node.node_ID)
            self.IDs.append(node.node_ID)

        self.addBtn.clicked.connect(self.addVariable)

    def addVariable(self):
        node = get_class_from_nodesID(self.IDs.__getitem__(self.myCompoBox.currentIndex()))
        self.addMyItem(node.op_title, node.icon, node.node_ID)

    def addMyItem(self, name, icon=None, node_ID=0):
        item = QListWidgetItem(name, self.VarList)  # can be (icon, text, parent, <int>type)

        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(28, 28))
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, node_ID)

    def itemClicked(self, *args, **kwargs):
        print("WWWWWWeeeeeeeeeeeeeeee")


    def startDrag(self, *args, **kwargs):
        try:
            item = self.VarList.currentItem()
            print(item.text())
            node_ID = item.data(Qt.UserRole + 1)

            pixmap = QPixmap(item.data(Qt.UserRole))

            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            dataStream << pixmap
            dataStream.writeInt(node_ID)
            dataStream.writeQString(item.text())

            mimeData = QMimeData()
            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e:
            dumpException(e)

