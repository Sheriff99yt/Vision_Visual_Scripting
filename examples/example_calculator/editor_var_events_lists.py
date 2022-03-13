from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *

from examples.example_calculator.nodes.default_functions import *
from examples.example_calculator.nodes_configuration import VARIABLES, get_node_by_ID, LISTBOX_MIMETYPE, \
    set_user_var_ID_now, set_user_event_ID_now
from nodeeditor.utils import dumpException
from examples.example_calculator.user_data import UserData


class VarEventList(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.userData = UserData()

        # Add QTabWidget and add Both Variables Tab and Events Tab
        tab1 = QWidget()
        tab2 = QWidget()
        self.addTab(tab1, "Variables")
        self.addTab(tab2, "Events")

        # Create Variables List
        self.VarList = QListWidget()
        self.EventList = QListWidget()

        # Create Variables and Events WNDs layout
        self.varLayout = QVBoxLayout()
        self.varLayout.setContentsMargins(0, 0, 0, 0)

        self.eventLayout = QVBoxLayout()
        self.eventLayout.setContentsMargins(0, 0, 0, 0)

        # Set Layouts For both
        tab1.setLayout(self.varLayout)
        tab2.setLayout(self.eventLayout)

        ## Setup CompoBox and add Button For Vars
        self.varCompoBox = QComboBox()
        self.varAddBtn = QPushButton("Add Variable")
        self.varHlayout = QHBoxLayout()
        self.varCompoBox.setMinimumHeight(28)
        self.varAddBtn.setMinimumHeight(28)
        self.VarList.setIconSize(QSize(28, 28))
        self.varHlayout.setContentsMargins(2, 2, 2, 2)
        self.varHlayout.addWidget(self.varCompoBox)
        self.varHlayout.addWidget(self.varAddBtn)
        self.varLayout.addLayout(self.varHlayout)
        self.varLayout.addWidget(self.VarList)
        self.VarList.setDragEnabled(True)

        # Setup CompoBox and add Button For Vars
        self.eventCompoBox = QComboBox()
        self.eventAddBtn = QPushButton("Add Event")
        self.eventHlayout = QHBoxLayout()
        self.eventCompoBox.setMinimumHeight(28)
        self.eventAddBtn.setMinimumHeight(28)
        self.EventList.setIconSize(QSize(28, 28))
        self.eventHlayout.setContentsMargins(2, 2, 2, 2)
        self.eventHlayout.addWidget(self.eventCompoBox)
        self.eventHlayout.addWidget(self.eventAddBtn)
        self.eventLayout.addLayout(self.eventHlayout)
        self.eventLayout.addWidget(self.EventList)
        self.EventList.setDragEnabled(True)

        self.Proprieties = None

        self.VarList.startDrag = self.VarStartDrag
        self.EventList.startDrag = self.EventStartDrag

        self.VarList.itemClicked.connect(self.VarSelectionChanged)
        self.EventList.itemClicked.connect(self.EventSelectionChanged)

        self.varsIds = []
        self.eventsIds = []

        self.InitList()

    def newNodeFrom(self, var):
        class newNode(var):
            pass
        return newNode

    def InitList(self):
        Events = 0
        # Events = list(FUNCTIONS.keys())[0]
        # Events.sort()
        # for node_type in Events:
        node = get_node_by_ID(Events)
        self.eventCompoBox.addItem(node.name)
        self.eventsIds.append(node.node_type)

        Vars = list(VARIABLES.keys())
        Vars.sort()
        for node_type in Vars:
            node = get_node_by_ID(node_type)
            self.varCompoBox.addItem(node.name)
            self.varsIds.append(node.node_type)

        # self.loadVars(self.userData.LoadData())
        self.varAddBtn.clicked.connect(self.addNewVariable)
        self.eventAddBtn.clicked.connect(self.addNewEvent)

    def addNewVariable(self):
        # Get new Variable type and construct new Variable object
        node = get_node_by_ID(self.varsIds.__getitem__(self.varCompoBox.currentIndex()))

        newVar = self.newNodeFrom(node)

        varData = self.userData.AddVar(newVar)

        # Add new copy of Var class Info to Dict of USERVARS
        set_user_var_ID_now(varData[2], newVar)

        # Add new QListItem to the UI List using Init Data
        self.addMyItem(newVar.name, newVar.icon, varData[2], node.node_type, self.VarList)

    def addNewEvent(self):
        # Get new Event type and construct new Variable object
        node = get_node_by_ID(self.eventsIds.__getitem__(self.eventCompoBox.currentIndex()))

        newEvent = self.newNodeFrom(node)

        eventData = self.userData.AddEvent(newEvent)

        # Add new copy of Var class Info to Dict of USEREVENTS
        set_user_event_ID_now(eventData[2], newEvent)

        # Add new QListItem to the UI List using Init Data
        self.addMyItem(newEvent.name, newEvent.icon, eventData[2], node.node_type, self.EventList)

    def addMyItem(self, name, icon=None, new_node_ID=0, node_type=int, List=QListWidget):
        item = QListWidgetItem(name, List)  # can be (icon, text, parent, <int>type)

        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(28, 28))
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, pixmap)

        item.setData(80, node_type)

        item.setData(90, new_node_ID)

        item.setData(91, name)

    def EventSelectionChanged(self, *args, **kwargs):
        self.Proprieties.infoStart = True

        item = self.EventList.currentItem()
        name = QLineEdit()
        name.setText(f"{item.data(91)}")
        self.Proprieties.infoUpdate(name)
        self.Proprieties.infoUpdate(QLabel("This is a Test Text"))

    def VarSelectionChanged(self, *args, **kwargs):
        self.Proprieties.varStart = True

        item = self.VarList.currentItem()
        name = QLineEdit()
        name.setText(f"{item.data(91)}")

        self.Proprieties.varUpdate("Variable Name", name)

        if item.data(80) == 20:
            value = QDoubleSpinBox()
            self.Proprieties.varUpdate("Variable Value", value)

        elif item.data(80) == 21:
            value = QSpinBox()
            self.Proprieties.varUpdate("Variable Value", value)

        elif item.data(80) == 22:
            value = QCheckBox()
            self.Proprieties.varUpdate("Variable Value", value)

        elif item.data(80) == 23:
            value = QLineEdit()
            self.Proprieties.varUpdate("Variable Value", value)

    def VarStartDrag(self, *args, **kwargs):
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
            dataStream.writeQString(item.text())
            dataStream.writeQStringList(["V"])

            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e:
            dumpException(e)

    def EventStartDrag(self, *args, **kwargs):
        try:
            item = self.EventList.currentItem()
            event_ID = item.data(90)
            pixmap = QPixmap(item.data(Qt.UserRole))
            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            mimeData = QMimeData()
            drag = QDrag(self)

            dataStream << pixmap
            dataStream.writeInt(event_ID)
            dataStream.writeQString(item.text())
            dataStream.writeQStringList(["E"])

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
