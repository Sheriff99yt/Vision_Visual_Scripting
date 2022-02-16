import os
from qtpy.QtGui import QIcon, QKeySequence
from qtpy.QtWidgets import *
from qtpy.QtCore import Qt, QSignalMapper

from nodeeditor.utils import loadStylesheets
from nodeeditor.node_editor_window import NodeEditorWindow
from examples.example_calculator.master_node_editor import NodeEditorSubWindow
from examples.example_calculator.master_node_designer import *
from examples.example_calculator.editor_drag_node_listbox import QDMNodeListbox
from examples.example_calculator.editor_drag_var_listbox import QDMVarListbox

from nodeeditor.utils import dumpException, pp
from examples.example_calculator.calc_conf import CALC_NODES

# Enabling edge validators
from nodeeditor.node_edge import Edge
from nodeeditor.node_edge_validators import (
    edge_validator_debug,
    edge_cannot_connect_two_outputs_or_two_inputs,
    edge_cannot_connect_input_and_output_of_same_node
)
Edge.registerEdgeValidator(edge_validator_debug)
Edge.registerEdgeValidator(edge_cannot_connect_two_outputs_or_two_inputs)
Edge.registerEdgeValidator(edge_cannot_connect_input_and_output_of_same_node)


# images for the dark skin
import examples.example_calculator.qss.nodeeditor_dark_resources


DEBUG = False


class MasterWindow(NodeEditorWindow):

    def initUI(self):
        self.name_company = 'MyTeam'
        self.name_product = 'Vision Visual Scripting'

        self.stylesheet_filename = os.path.join(os.path.dirname(__file__), "qss/nodeeditor.qss")
        loadStylesheets(
            os.path.join(os.path.dirname(__file__), "qss/nodeeditor-dark.qss"),
            self.stylesheet_filename
        )

        self.empty_icon = QIcon(".")

        if DEBUG:
            print("Registered nodes:")
            pp(CALC_NODES)


        self.masterDisplay = QStackedWidget()
        self.mdiArea = QMdiArea()
        self.nodeDesigner = NodeDesignerSubWindow()

        self.masterDisplay.addWidget(self.mdiArea)
        self.masterDisplay.addWidget(self.nodeDesigner)
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.masterDisplay)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)


        # Create Details List Window
        self.CreateDetailsDock()

        # Create Nodes List
        self.createNodesDock()
        self.createToolsDock()

        #self.createGraphsDock()

        # Create Variable List
        self.CreateVariablesDock()


        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.readSettings()

        self.setWindowTitle("Vision Visual Scripting")
        self.NodeDesignerBtn.setChecked(True)
        self.updateActiveWnd()
    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()
            # hacky fix for PyQt 5.14.x
            import sys
            sys.exit(0)


    def createActions(self):
        super().createActions()

        self.actClose = QAction("Cl&ose", self, statusTip="Close the active window", triggered=self.mdiArea.closeActiveSubWindow)
        self.actCloseAll = QAction("Close &All", self, statusTip="Close all the windows", triggered=self.mdiArea.closeAllSubWindows)
        self.actTile = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)
        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild, statusTip="Move the focus to the next window", triggered=self.mdiArea.activateNextSubWindow)
        self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild, statusTip="Move the focus to the previous window", triggered=self.mdiArea.activatePreviousSubWindow)

        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

        self.actAbout = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)

    def getCurrentNodeEditorWidget(self):
        """ we're returning NodeEditorWidget here... """
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.widget().fileNew()
            subwnd.show()
        except Exception as e: dumpException(e)


    def onFileOpen(self):
        fnames, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file', self.getFileDialogDirectory(), self.getFileDialogFilter())

        try:
            for fname in fnames:
                if fname:
                    existing = self.findMdiChild(fname)
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        # we need to create new subWindow and open the file
                        nodeeditor = NodeEditorSubWindow()
                        if nodeeditor.fileLoad(fname):
                            self.statusBar().showMessage("File %s loaded" % fname, 5000)
                            nodeeditor.setTitle()
                            subwnd = self.createMdiChild(nodeeditor)
                            subwnd.show()
                        else:
                            nodeeditor.close()
        except Exception as e: dumpException(e)


    def about(self):
        QMessageBox.about(self, "About Calculator NodeEditor Example",
                "The <b>Calculator NodeEditor</b> example demonstrates how to write multiple "
                "document interface applications using PyQt5 and NodeEditor. For more information visit: "
                "<a href='https://www.blenderfreak.com/'>www.BlenderFreak.com</a>")

    def createMenus(self):
        super().createMenus()


        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        #self.windowMenu.aboutToShow.connect(self.updateWindowMenu)
        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actAbout)

        self.editMenu.aboutToShow.connect(self.updateEditMenu)

    def updateMenus(self):
        # print("update Menus")
        active = self.getCurrentNodeEditorWidget()
        hasMdiChild = (active is not None)

        self.actSave.setEnabled(hasMdiChild)
        self.actSaveAs.setEnabled(hasMdiChild)
        self.actClose.setEnabled(hasMdiChild)
        self.actCloseAll.setEnabled(hasMdiChild)
        self.actTile.setEnabled(hasMdiChild)
        self.actCascade.setEnabled(hasMdiChild)
        self.actNext.setEnabled(hasMdiChild)
        self.actPrevious.setEnabled(hasMdiChild)
        self.actSeparator.setVisible(hasMdiChild)

        self.updateEditMenu()

    def updateEditMenu(self):
        try:
            # print("update Edit Menu")
            active = self.getCurrentNodeEditorWidget()
            hasMdiChild = (active is not None)

            self.actPaste.setEnabled(hasMdiChild)

            self.actCut.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actDelete.setEnabled(hasMdiChild and active.hasSelectedItems())

            self.actUndo.setEnabled(hasMdiChild and active.canUndo())
            self.actRedo.setEnabled(hasMdiChild and active.canRedo())
        except Exception as e: dumpException(e)



    def updateWindowMenu(self):

        self.toolbar_tools = self.windowMenu.addAction("Tools Toolbar")
        self.toolbar_tools.setCheckable(False)
        self.toolbar_tools.setChecked(self.toolsDock.isVisible())


        self.toolbar_details = self.windowMenu.addAction("Details Toolbar")
        self.toolbar_details.setCheckable(True)
        self.toolbar_details.triggered.connect(self.onWindowDetailsToolbar)
        self.toolbar_details.setChecked(not self.detailsDock.isVisible())


        self.toolbar_vars = self.windowMenu.addAction("Variables Toolbar")
        self.toolbar_vars.setCheckable(True)
        self.toolbar_vars.triggered.connect(self.onWindowVarsToolbar)
        self.toolbar_vars.setChecked(not self.varsDock.isVisible())


        self.toolbar_nodes = self.windowMenu.addAction("Nodes Toolbar")
        self.toolbar_nodes.setCheckable(True)
        self.toolbar_nodes.triggered.connect(self.onWindowNodesToolbar)
        self.toolbar_nodes.setChecked(not self.nodesDock.isVisible())

        self.windowMenu.addSeparator()

        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        #self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.getCurrentNodeEditorWidget())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)



    def onWindowNodesToolbar(self):
        if self.nodesDock.isVisible():
            self.nodesDock.hide()
        else:
            self.nodesDock.show()


    def onWindowVarsToolbar(self):
        if self.varsDock.isVisible():
            self.varsDock.hide()
        else:
            self.varsDock.show()

    def onWindowDetailsToolbar(self):
        if self.detailsDock.isVisible():
            self.detailsDock.hide()
        else:
            self.detailsDock.show()


    def createToolBars(self):
        pass

    def createGraphsDock(self):
        self.graphsDock = QDockWidget("Graphs")
        self.graphsDock.setWidget(self.mdiArea)
        self.graphsDock.setFeatures(self.graphsDock.DockWidgetClosable | self.graphsDock.DockWidgetMovable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.graphsDock)


    def createToolsDock(self):

        self.NodeDesignerBtn = QPushButton(self)
        self.NodeDesignerBtn.setCheckable(True)
        self.NodeDesignerBtn.setMinimumSize(60, 60)
        self.NodeDesignerBtn.setMaximumSize(60, 60)

        self.toolsDock = QDockWidget("Tools")
        self.addDockWidget(Qt.TopDockWidgetArea, self.toolsDock)
        self.toolsDock.setLayoutDirection(Qt.LeftToRight)
        self.dockedWidget = QWidget(self)
        self.toolsDock.setWidget(self.dockedWidget)
        self.dockedWidget.setLayout(QHBoxLayout())
        self.dockedWidget.layout().addWidget(self.NodeDesignerBtn)

        self.dockedWidget.layout().addItem(QSpacerItem(20, 60, QSizePolicy.Expanding))
        self.dockedWidget.layout().setContentsMargins(4, 4, 4, 0)

        self.toolsDock.setFeatures(self.toolsDock.NoDockWidgetFeatures)

        self.NodeDesignerBtn.clicked.connect(self.updateActiveWnd)



    def updateActiveWnd(self):
        if self.NodeDesignerBtn.isChecked():
            # self.nodesDock.hide()
            # self.varsDock.hide()
            # self.detailsDock.hide()
            # self.toolbar_details.setVisible(False)
            # self.toolbar_vars.setVisible(False)
            # self.toolbar_nodes.setVisible(False)
            self.masterDisplay.setCurrentIndex(1)


        else:
            # self.nodesDock.show()
            # self.varsDock.show()
            # self.detailsDock.show()
            # self.toolbar_details.setVisible(True)
            # self.toolbar_vars.setVisible(True)
            # self.toolbar_nodes.setVisible(True)
            self.masterDisplay.setCurrentIndex(0)


    def createNodesDock(self):

        self.nodesListWidget = QDMNodeListbox()

        self.nodesDock = QDockWidget("Nodes")
        self.nodesDock.setWidget(self.nodesListWidget)
        self.nodesDock.setFeatures(self.nodesDock.DockWidgetClosable | self.nodesDock.DockWidgetMovable)
        self.addDockWidget(Qt.RightDockWidgetArea, self.nodesDock)

    def CreateVariablesDock(self):
        self.varsListWidget = QDMVarListbox()

        self.varsDock = QDockWidget("Variables")
        self.varsDock.setWidget(self.varsListWidget)
        self.varsDock.setFeatures(self.varsDock.DockWidgetClosable | self.varsDock.DockWidgetMovable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.varsDock)

    def CreateDetailsDock(self):
        self.DetialsWidget = QDMVarListbox()

        self.detailsDock = QDockWidget("Details")
        self.detailsDock.setWidget(self.DetialsWidget)
        self.detailsDock.setFeatures(self.detailsDock.DockWidgetClosable | self.detailsDock.DockWidgetMovable)

        self.addDockWidget(Qt.RightDockWidgetArea, self.detailsDock)


    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else NodeEditorSubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        # nodeeditor.scene.addItemSelectedListener(self.updateEditMenu)
        # nodeeditor.scene.addItemsDeselectedListener(self.updateEditMenu)
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeeditor.addCloseEventListener(self.onSubWndClose)
        return subwnd

    def onSubWndClose(self, widget, event):
        existing = self.findMdiChild(widget.filename)
        self.mdiArea.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()
        else:
            event.ignore()


    def findMdiChild(self, filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None


    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)
