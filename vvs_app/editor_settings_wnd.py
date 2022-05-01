from functools import partial

from PyQt5 import *
from vvs_app.master_window import *


class settingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterRef = None

        self.settingsCategoriesList = [[Appearance.__name__, Appearance], [System.__name__, System], [KeyMapping.__name__, KeyMapping]]

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

        for Item in self.settingsCategoriesList:
            self.Setting = QTreeWidgetItem([Item[0]])
            self.Setting.setData(5, 6, Item[1])
            self.settingsTree.addTopLevelItem(self.Setting)

        self.currentSettingsWidget = QWidget()
        self.settingsSplitter.addWidget(self.currentSettingsWidget)

        self.settingsTree.clicked.connect(self.settingsWidgetChange)


    def settingsWidgetChange(self):
        selected = self.settingsTree.selectedItems()
        old = self.settingsSplitter.widget(1)
        old.deleteLater()

        self.currentSettingsWidget = selected[0].data(5, 6)()
        self.settingsSplitter.addWidget(self.currentSettingsWidget)
        self.currentSettingsWidget.masterRef = self.masterRef
        self.currentSettingsWidget.fill()

        # FW = self.currentSettingsWidget.Layout.itemAtPosition(2, 0).widget()
        # FW.setMinimumWidth(100)
        # FW.setAlignment(Qt.AlignCenter, Qt.AlignRight)
        # Add Reset Btn
        self.resetBtn = QPushButton("Rest")
        self.currentSettingsWidget.Layout.addWidget(self.resetBtn, self.currentSettingsWidget.Layout.rowCount() + 1, 1)
        self.resetBtn.setFixedWidth(100)
        self.resetBtn.clicked.connect(lambda: self.masterRef.GlobalSwitches.change_Switches(self.masterRef.GlobalSwitches.Default_switches_Dict, self.currentSettingsWidget.settingsList, False))

class Appearance(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterRef = None


        self.Layout = QGridLayout()
        self.AppearanceWnd_Name = QLabel(Appearance.__name__)
        self.Layout.addWidget(self.AppearanceWnd_Name, 0, 0)

        self.spacer = QSpacerItem(50, 50)
        self.Layout.addItem(self.spacer, 1, 0)

        # Content
        self.settingsList =[]

        self.setLayout(self.Layout)
        self.layout().setAlignment(Qt.AlignTop)

    def fill(self):
        pass

class System(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterRef = None

        self.Layout = QGridLayout()
        self.SystemWnd_Name = QLabel(System.__name__)
        self.Layout.addWidget(self.SystemWnd_Name, 0, 0)

        self.spacer = QSpacerItem(50, 50)
        self.Layout.addItem(self.spacer, 1, 0)

        # Content
        self.settingsList = ["autoSaveSteps", "AutoSave Folder Max Size"]

            # Edits AutoSave Trigger
        self.autoSaveLbl = QLabel("AutoSave Trigger")
        self.Layout.addWidget(self.autoSaveLbl, 2, 0, Qt.AlignRight)
        self.Layout.setColumnMinimumWidth(0, 50)

        self.autoSaveSteps = QSpinBox()
        self.Layout.addWidget(self.autoSaveSteps, 2, 1, 1, 10, Qt.AlignLeft)
        self.autoSaveSteps.setMinimumWidth(50)
        self.autoSaveSteps.editingFinished.connect(lambda : self.masterRef.GlobalSwitches.change_Switches(self.autoSaveSteps.value(), ["autoSaveSteps"], CounterReset=True))

            # Edit AutoSave Folder Max Size
        self.autoSaveFolderMaxSizeLbl = QLabel("AutoSave Folder Max Size (GB)")
        self.Layout.addWidget(self.autoSaveFolderMaxSizeLbl, 3, 0, Qt.AlignRight)
        self.Layout.setColumnMinimumWidth(0, 50)

        self.autoSaveFolderMaxSizeSB = QDoubleSpinBox()
        self.autoSaveFolderMaxSizeSB.setDecimals(5)
        self.Layout.addWidget(self.autoSaveFolderMaxSizeSB, 3, 1, Qt.AlignLeft)
        self.autoSaveFolderMaxSizeSB.setMinimumWidth(50)
        self.autoSaveFolderMaxSizeSB.editingFinished.connect(lambda: self.masterRef.GlobalSwitches.change_Switches(self.autoSaveFolderMaxSizeSB.value(), ["AutoSave Folder Max Size"], CounterReset=True))

        self.setLayout(self.Layout)
        self.layout().setAlignment(Qt.AlignTop)

    def fill(self):
        self.autoSaveSteps.setValue(self.masterRef.GlobalSwitches.switches_Dict["autoSaveSteps"])
        self.autoSaveFolderMaxSizeSB.setValue(self.masterRef.GlobalSwitches.switches_Dict["AutoSave Folder Max Size"])

class KeyMapping(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterRef = None

        self.Layout = QGridLayout()
        self.KeyMappingWnd_Name = QLabel(KeyMapping.__name__)
        self.Layout.addWidget(self.KeyMappingWnd_Name, 0, 0)

        self.spacer = QSpacerItem(50, 50)
        self.Layout.addItem(self.spacer, 1, 0)

        # Content
        self.settingsList = ["New Graph", "Open", "Set Project Location", "Save", "Save As", "Exit",
                             "Undo", "Redo", "Cut", "Copy", "Paste", "Delete", "Settings Window"]
        for item in self.settingsList:
            lbl = QLabel(item)
            self.Layout.addWidget(lbl, self.settingsList.index(item) + 2, 0, Qt.AlignRight)
            self.Layout.setColumnMinimumWidth(0, 50)

            KeySequence = QKeySequenceEdit()
            self.Layout.addWidget(KeySequence, self.settingsList.index(item) + 2, 1, 1, 10, alignment=Qt.AlignLeft)
            KeySequence.setMaximumWidth(100)

        # # Add Reset Btn
        # self.resetBtn = QPushButton("Rest")
        # self.Layout.addWidget(self.resetBtn, self.Layout.rowCount() + 1, 1)
        # self.resetBtn.setFixedWidth(100)
        # self.resetBtn.clicked.connect(lambda: self.masterRef.GlobalSwitches.onReset(self.settingsList))

        self.setLayout(self.Layout)
        self.layout().setAlignment(Qt.AlignTop)

        self.Btns_Connects()

    def fill(self):
        for i in range(self.Layout.rowCount() - 2):
            if self.Layout.itemAtPosition(i + 2, 0):
                Label = self.Layout.itemAtPosition(i + 2, 0).widget().text()
                currentKS = self.masterRef.GlobalSwitches.switches_Dict[Label]
                self.Layout.itemAtPosition(i + 2, 1).widget().setKeySequence(currentKS)

    def Btns_Connects(self):
        # File Shortcuts
        self.Layout.itemAtPosition(
            self.settingsList.index("New Graph") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actNew, self.masterRef.actOpen, "New Graph", 1))
        self.Layout.itemAtPosition(
            self.settingsList.index("Open") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actOpen, self.masterRef.actSetProjectDir, "Open", 1))
        self.Layout.itemAtPosition(
            self.settingsList.index("Set Project Location") + 2,2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actSetProjectDir, self.masterRef.actSave, "Set Project Location", 1))
        self.Layout.itemAtPosition(
            self.settingsList.index("Save") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actSave, self.masterRef.actSaveAs, "Save", 1))
        self.Layout.itemAtPosition(
            self.settingsList.index("Save As") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actSaveAs, self.masterRef.actExit, "Save As", 1))
        self.Layout.itemAtPosition(
            self.settingsList.index("Exit") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actExit, None, "Exit", 1))

        # Edit Shortcuts
        self.Layout.itemAtPosition(
            self.settingsList.index("Undo") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actUndo, self.masterRef.actRedo, "Undo", 2))
        self.Layout.itemAtPosition(
            self.settingsList.index("Redo") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actRedo, self.masterRef.actCut, "Redo", 2))
        self.Layout.itemAtPosition(
            self.settingsList.index("Cut") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actCut, self.masterRef.actCopy, "Cut", 2))
        self.Layout.itemAtPosition(
            self.settingsList.index("Copy") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actCopy, self.masterRef.actPaste, "Copy", 2))
        self.Layout.itemAtPosition(
            self.settingsList.index("Paste") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actPaste, self.masterRef.actDelete, "Paste", 2))
        self.Layout.itemAtPosition(
            self.settingsList.index("Delete") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.actDelete, None, "Delete", 2))

        self.Layout.itemAtPosition(
            self.settingsList.index("Settings Window") + 2, 2).widget().editingFinished.connect(
            lambda: self.shortcutEdit(self.masterRef.settingsBtn, None, "Settings Window", 3))

    def shortcutEdit(self, ChangingAct, NextAct, Text, Num):
        index = self.settingsList.index(Text)
        NewShortcut = self.Layout.itemAtPosition(index + 2, 2).widget().keySequence().toString()

        self.masterRef.GlobalSwitches.change_Switches(NewShortcut, [Text], CounterReset=False)

        if Num == 1:
            self.masterRef.fileMenu.removeAction(ChangingAct)
            ChangingAct.setShortcut(NewShortcut)
            self.masterRef.fileMenu.insertAction(NextAct, ChangingAct)
        elif Num == 2:
            self.masterRef.editMenu.removeAction(ChangingAct)
            ChangingAct.setShortcut(NewShortcut)
            self.masterRef.editMenu.insertAction(NextAct, ChangingAct)
        elif Num == 3:
            ChangingAct.setShortcut(NewShortcut)
