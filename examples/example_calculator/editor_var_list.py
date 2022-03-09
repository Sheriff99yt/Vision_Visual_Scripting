from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *

from examples.example_calculator.editor_proterties_list import PropertiesList
from examples.example_calculator.nodes_configuration import VARIABLES, get_class_from_nodesID, LISTBOX_MIMETYPE
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

        self.VarList.startDrag = self.startDrag
        self.VarList.startDrag = self.startDrag
        self.VarList.itemClicked.connect(self.myClick)

        self.IDs = []
        self.varNames = []

        self.InitList()

    def properiesRef(self, Ref: None):
        self.proretiesRef = Ref

    def InitList(self):
        Vars = list(VARIABLES.keys())
        Vars.sort()
        for node_ID in Vars:
            node = get_class_from_nodesID(node_ID)
            self.myCompoBox.addItem(node.name)
            self.IDs.append(node.node_ID)

        # self.loadVars(self.userData.LoadData())

        self.addBtn.clicked.connect(self.addVariable)

    def autoVarRename(self, node: 'Node'):
        newName = node.name
        x = 0
        # does a variable already has this name ?
        while self.varNames.__contains__(newName):
            # change the name
            x = + 1
            newName = f"{newName}{x}"
        else:
            node.name = newName
            self.varNames.append(newName)
            return newName

    def tryVarRename(self, node: None):
        pass

    def addVariable(self):
        node = get_class_from_nodesID(self.IDs.__getitem__(self.myCompoBox.currentIndex()))
        self.addMyItem(self.autoVarRename(node), node.icon, node.node_ID)
        # self.userData.SaveVar(node)

    def loadVars(self, Vars: list):
        for var in Vars:
            currentVar = get_class_from_nodesID(var[1])
            self.addMyItem(var[0], currentVar.icon, var.node_ID)


    def addMyItem(self, name, icon=None, node_ID=0):
        item = QListWidgetItem(name, self.VarList)  # can be (icon, text, parent, <int>type)

        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(28, 28))
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, node_ID)

        item.setData(90, node_ID)
        item.setData(91, name)

        # if node_ID == 12:
        #
        # elif node_ID == 13:
        #
        # elif node_ID == 14:
        #
        # elif node_ID == 15:

    def myClick(self, *args, **kwargs):
        self.proretiesRef.start = True

        item = self.VarList.currentItem()
        name = QLineEdit()
        name.setText(f"{item.data(91)}")

        if item.data(90) == 12:
            value = QDoubleSpinBox()
            self.proretiesRef.varUpdate("Variable Name", name)
            self.proretiesRef.varUpdate("Variable Value", value)

        elif item.data(90) == 13:
            value = QSpinBox()
            self.proretiesRef.varUpdate("Variable Name", name)
            self.proretiesRef.varUpdate("Variable Value", value)

        elif item.data(90) == 14:
            value = QCheckBox()
            self.proretiesRef.varUpdate("Variable Name", name)
            self.proretiesRef.varUpdate("Variable Value", value)

        elif item.data(90) == 15:
            value = QLineEdit()
            self.proretiesRef.varUpdate("Variable Name", name)
            self.proretiesRef.varUpdate("Variable Value", value)

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
