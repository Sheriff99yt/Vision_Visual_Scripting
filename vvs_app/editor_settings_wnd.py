from functools import partial

from PyQt5 import *

from examples.example_calculator.master_window import *
from nodeeditor.node_scene_history import SceneHistory

class settingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterRef = None

        self.settingsList = [[Appearance.__name__, Appearance], [System.__name__, System], [KeyMapping.__name__, KeyMapping]]

        self.settingsLayout = QVBoxLayout()
        self.setLayout(self.settingsLayout)

        self.settingsSplitter = QSplitter(Qt.Horizontal)
        self.settingsLayout.addWidget(self.settingsSplitter)
        self.settingsSplitter.setChildrenCollapsible(False)

        self.settingsTree = QTreeWidget()
        self.settingsTree.header().hide()
        self.settingsTree.setMaximumWidth(250)
        self.settingsTree.setMinimumWidth(150)
        self.settingsSplitter.addWidget(self.settingsTree)

        for Item in self.settingsList:
            self.Setting = QTreeWidgetItem([Item[0]])
            self.Setting.setData(5, 6, Item[1])
            self.settingsTree.addTopLevelItem(self.Setting)

        self.settingsWidget = QWidget()
        self.settingsSplitter.addWidget(self.settingsWidget)

        self.settingsTree.clicked.connect(self.settingsWidgetChange)

    def settingsWidgetChange(self):
        selected = self.settingsTree.selectedItems()
        old = self.settingsSplitter.widget(1)
        old.deleteLater()

        self.settingsWidget = selected[0].data(5, 6)()
        self.settingsSplitter.addWidget(self.settingsWidget)
        self.settingsWidget.masterRef = self.masterRef

class Appearance(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterRef = None

        self.Appearance_Layout = QGridLayout()
        self.AppearanceWnd_Name = QLabel(Appearance.__name__)
        self.Appearance_Layout.addWidget(self.AppearanceWnd_Name, 0, 0)

        self.spacer = QSpacerItem(50, 50)
        self.Appearance_Layout.addItem(self.spacer, 1, 0)

        # Content


        self.setLayout(self.Appearance_Layout)
        self.layout().setAlignment(Qt.AlignTop)

class System(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterRef = None

        self.System_Layout = QGridLayout()
        self.SystemWnd_Name = QLabel(System.__name__)
        self.System_Layout.addWidget(self.SystemWnd_Name, 0, 0)

        self.spacer = QSpacerItem(50, 50)
        self.System_Layout.addItem(self.spacer, 1, 0)

        # Edits AutoSave Trigger
        self.autoSaveLbl = QLabel("AutoSave Trigger")
        self.System_Layout.addWidget(self.autoSaveLbl, 2, 0, alignment=Qt.AlignRight)
        self.System_Layout.setColumnMinimumWidth(0, 50)

        self.autoSaveSteps = QSpinBox()
        self.System_Layout.addWidget(self.autoSaveSteps, 2, 1, 1, 10, alignment=Qt.AlignLeft)
        self.autoSaveSteps.setMaximumWidth(200)
        self.autoSaveSteps.editingFinished.connect(lambda :self.masterRef.GlobalSwitches.change_autoSaveSteps(self.autoSaveSteps.value()))

        self.setLayout(self.System_Layout)
        self.layout().setAlignment(Qt.AlignTop)

class KeyMapping(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterRef = None

        self.KeyMapping_Layout = QGridLayout()
        self.KeyMappingWnd_Name = QLabel(KeyMapping.__name__)
        self.KeyMapping_Layout.addWidget(self.KeyMappingWnd_Name, 0, 0)

        self.spacer = QSpacerItem(50, 50)
        self.KeyMapping_Layout.addItem(self.spacer, 1, 0)

        self.settingslist = ["New Graph", "Open", "Set Project Location", "Save", "Save As", "Exit",
                             "Undo", "Redo", "Cut", "Copy", "Paste", "Delete"]

        for item in self.settingslist:
            lbl = QLabel(item)
            self.KeyMapping_Layout.addWidget(lbl, self.settingslist.index(item)+2, 0, alignment=Qt.AlignRight)
            self.KeyMapping_Layout.setColumnMinimumWidth(0, 50)

            KeySequence = QKeySequenceEdit()
            self.KeyMapping_Layout.addWidget(KeySequence, self.settingslist.index(item)+2, 1, 1, 10, alignment=Qt.AlignLeft)
            KeySequence.setMaximumWidth(100)

        self.Handlers()

        self.setLayout(self.KeyMapping_Layout)
        self.layout().setAlignment(Qt.AlignTop)

    def Handlers(self):
        # File Shortcuts
        self.KeyMapping_Layout.itemAtPosition(
            self.settingslist.index("New Graph") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actNew, self.masterRef.actOpen, "New Graph", 1))
        self.KeyMapping_Layout.itemAtPosition(
            self.settingslist.index("Open") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actOpen, self.masterRef.actSetProjectDir, "Open", 1))
        self.KeyMapping_Layout.itemAtPosition(
            self.settingslist.index("Set Project Location") + 2,2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actSetProjectDir, self.masterRef.actSave, "Set Project Location", 1))
        self.KeyMapping_Layout.itemAtPosition(
            self.settingslist.index("Save") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actSave, self.masterRef.actSaveAs, "Save", 1))
        self.KeyMapping_Layout.itemAtPosition(
            self.settingslist.index("Save As") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actSaveAs, self.masterRef.actExit, "Save As", 1))
        self.KeyMapping_Layout.itemAtPosition(
            self.settingslist.index("Exit") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actExit, None, "Exit", 1))

        # Edit Shortcuts
        self.KeyMapping_Layout.itemAtPosition(
            self.settingslist.index("Undo") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actUndo, self.masterRef.actRedo, "Undo", 2))
        self.KeyMapping_Layout.itemAtPosition(
            self.settingslist.index("Redo") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actRedo, self.masterRef.actCut, "Redo", 2))
        self.KeyMapping_Layout.itemAtPosition(
            self.settingslist.index("Cut") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actCut, self.masterRef.actCopy, "Cut", 2))
        self.KeyMapping_Layout.itemAtPosition(
            self.settingslist.index("Copy") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actCopy, self.masterRef.actPaste, "Copy", 2))
        self.KeyMapping_Layout.itemAtPosition(
            self.settingslist.index("Paste") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actPaste, self.masterRef.actDelete, "Paste", 2))
        self.KeyMapping_Layout.itemAtPosition(
            self.settingslist.index("Delete") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actDelete, None, "Delete", 2))

    def shortcutEdit(self, ChangingAct, NextAct, Text, Num):
        index = self.settingslist.index(Text)
        NewShortcut = self.KeyMapping_Layout.itemAtPosition(index + 2, 2).widget().keySequence().toString()

        self.masterRef.GlobalSwitches.change_Switches(NewShortcut, Text)

        if Num == 1:
            self.masterRef.fileMenu.removeAction(ChangingAct)
            ChangingAct.setShortcut(NewShortcut)
            self.masterRef.fileMenu.insertAction(NextAct, ChangingAct)
        elif Num == 2:
            self.masterRef.editMenu.removeAction(ChangingAct)
            ChangingAct.setShortcut(NewShortcut)
            self.masterRef.editMenu.insertAction(NextAct, ChangingAct)
