from typing import TypeVar
from copy import deepcopy

from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from copy import *

from examples.example_calculator.nodes.default_functions import *
from examples.example_calculator.nodes_configuration import VARIABLES, get_node_by_ID, LISTBOX_MIMETYPE, \
    set_user_var_ID_now
from nodeeditor.utils import dumpException
from examples.example_calculator.user_data import UserData


class VarList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.userData = UserData()

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

        self.proprietiesRef = None

        self.VarList.startDrag = self.startDrag
        self.VarList.startDrag = self.startDrag
        self.VarList.itemClicked.connect(self.selectionChanged)

        self.IDs = []

        self.InitList()

    def newVarFrom(self, var):
        class newVar(var):
            pass

        return newVar

    def InitList(self):
        Vars = list(VARIABLES.keys())
        Vars.sort()
        for node_type in Vars:
            node = get_node_by_ID(node_type)
            self.myCompoBox.addItem(node.name)
            self.IDs.append(node.node_type)

        # self.loadVars(self.userData.LoadData())

        self.addBtn.clicked.connect(self.addNewVariable)

    def tryVarRename(self, node: None):
        pass

    def addNewVariable(self):
        # Get new Variable type and construct new Variable object
        node = get_node_by_ID(self.IDs.__getitem__(self.myCompoBox.currentIndex()))

        newVar = self.newVarFrom(node)

        varData = self.userData.AddVar(newVar)

        print(node.node_type)

        print(newVar.node_type)

        # Add new copy of Var class Info to Dict of USERVARS
        set_user_var_ID_now(varData[2], newVar)

        # Add new QListItem to the UI List using Init Data
        self.addMyItem(newVar.name, newVar.icon, varData[2], node.node_type)

    def addMyItem(self, name, icon=None, var_ID=0, var_type=int):
        item = QListWidgetItem(name, self.VarList)  # can be (icon, text, parent, <int>type)

        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(28, 28))
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, pixmap)

        item.setData(80, var_type)

        item.setData(90, var_ID)

        item.setData(91, name)

    def selectionChanged(self, *args, **kwargs):
        self.proprietiesRef.start = True

        item = self.VarList.currentItem()
        name = QLineEdit()
        name.setText(f"{item.data(91)}")

        if item.data(80) == 12:
            value = QDoubleSpinBox()
            self.proprietiesRef.varUpdate("Variable Name", name)
            self.proprietiesRef.varUpdate("Variable Value", value)

        elif item.data(80) == 13:
            value = QSpinBox()
            self.proprietiesRef.varUpdate("Variable Name", name)
            self.proprietiesRef.varUpdate("Variable Value", value)

        elif item.data(80) == 14:
            value = QCheckBox()
            self.proprietiesRef.varUpdate("Variable Name", name)
            self.proprietiesRef.varUpdate("Variable Value", value)

        elif item.data(80) == 15:
            value = QLineEdit()
            self.proprietiesRef.varUpdate("Variable Name", name)
            self.proprietiesRef.varUpdate("Variable Value", value)

    def startDrag(self, *args, **kwargs):
        try:

            item = self.VarList.currentItem()
            var_ID = item.data(90)
            pixmap = QPixmap(item.data(Qt.UserRole))
            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            mimeData = QMimeData()
            drag = QDrag(self)

            dataStream << pixmap
            dataStream.writeInt(var_ID)
            dataStream.writeBool(True)
            dataStream.writeQString(item.text())

            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e:
            dumpException(e)

    def loadVars(self, Vars: list):
        for var in Vars:
            currentVar = get_node_by_ID(var[1])
            self.addMyItem(var[0], currentVar.icon, var.node_type)
