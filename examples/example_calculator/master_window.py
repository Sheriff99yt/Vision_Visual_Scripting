import os
from qtpy.QtGui import *
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from copy import *
from nodeeditor.utils import loadStylesheets
from nodeeditor.node_editor_window import NodeEditorWindow
from examples.example_calculator.master_editor_wnd import MasterEditorWnd
from examples.example_calculator.master_designer_wnd import MasterDesignerWnd
from examples.example_calculator.editor_node_list import NodeList
from examples.example_calculator.editor_files_wdg import FilesWDG
from examples.example_calculator.editor_var_events_lists import VarEventList
from examples.example_calculator.editor_proterties_list import PropertiesList

from nodeeditor.utils import dumpException, pp
# from examples.example_calculator.nodes_configuration import FUNCTIONS

# Enabling edge validators
from nodeeditor.node_edge import Edge
from nodeeditor.node_edge_validators import (
    edge_validator_debug,
    edge_cannot_connect_two_outputs_or_two_inputs,
    edge_cannot_connect_input_and_output_of_same_node
)

# Edge.registerEdgeValidator(edge_validator_debug)
Edge.registerEdgeValidator(edge_cannot_connect_two_outputs_or_two_inputs)
Edge.registerEdgeValidator(edge_cannot_connect_input_and_output_of_same_node)

# images for the dark skin
import examples.example_calculator.qss.nodeeditor_dark_resources

DEBUG = False


class MasterWindow(NodeEditorWindow):

    def MakeCopyOfClass(self, classRef):
        class NewVEList(classRef):
            pass

        return NewVEList

    def initUI(self):
        self.name_company = 'MyTeam'
        self.name_product = 'Vision Visual Scripting'

        self.stylesheet_filename = os.path.join(os.path.dirname(__file__), "qss/nodeeditor.qss")
        loadStylesheets(
            os.path.join(os.path.dirname(__file__), "qss/nodeeditor-night.qss"), self.stylesheet_filename)

        self.empty_icon = QIcon("")

        if DEBUG:
            print("Registered nodes:")
            # pp(FUNCTIONS)
        self.graphsNames = []

        self.all_VE_lists = []
        self.all_graphs = []

        self.stackedDisplay = QStackedWidget()

        self.graphs_parent_wdg = QMdiArea()

        # Create Node Designer Window
        self.nodeDesigner = MasterDesignerWnd()

        self.stackedDisplay.addWidget(self.graphs_parent_wdg)
        self.stackedDisplay.addWidget(self.nodeDesigner)
        self.graphs_parent_wdg.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.graphs_parent_wdg.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.graphs_parent_wdg.setViewMode(QMdiArea.TabbedView)
        self.graphs_parent_wdg.setDocumentMode(True)
        self.graphs_parent_wdg.setTabsClosable(True)
        self.graphs_parent_wdg.setTabsMovable(True)
        self.setCentralWidget(self.stackedDisplay)

        self.graphs_parent_wdg.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.graphs_parent_wdg.subWindowActivated.connect(self.ActiveGraphSwitched)

        # Create Details List Window
        self.CreatePropertiesDock()

        # Create Nodes List
        self.createFunctionsDock()

        # Creat Files Dock
        self.CreateFilesDock()

        # Create Variable List
        self.CreateVarEventDock()

        self.createActions()
        self.createMenus()
        self.createStatusBar()
        self.updateMenus()

        self.readSettings()

        self.CreateToolBar()

        self.setWindowTitle("Vision Visual Scripting")

        self.CodeWndSettingBtn.triggered.connect(self.RotateTextCodeWnd)

        # self.NodeDesignerBtn.setChecked(True)
        # self.updateActiveWnd()

    def ActiveGraphSwitched(self):
        if self.CurrentNodeEditor():
            self.VEStackedWdg.setCurrentWidget(self.CurrentNodeEditor().scene.VEListWdg)

    def CreateToolBar(self):
        self.nodeDesignerBtn = QAction(QIcon("icons/Pencil_1.png"), "&Toggle Designer", self)
        self.toolsBar = QToolBar("Tools", self)
        self.toolsBar.setIconSize(QSize(26, 26))
        self.toolsBar.setFloatable(False)

        self.addToolBar(self.toolsBar)
        # self.editToolBar.addAction(self.nodeDesignerBtn)

        self.nodeDesignerBtn.setCheckable(True)
        self.nodeDesignerBtn.triggered.connect(self.updateActiveWnd)
        self.nodeDesignerBtn.setShortcut(QKeySequence("`"))

        mySpacer = QWidget()
        mySpacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolsBar.addWidget(mySpacer)

        self.CodeWndSettingBtn = QAction(QIcon("icons/Oriantation.png"), "&Code Window View Mode", self)
        self.toolsBar.addAction(self.CodeWndSettingBtn)

        self.CodeWndSettingBtn.setCheckable(True)
        self.CodeWndSettingBtn.setShortcut(QKeySequence("Ctrl+Shift+R"))
        self.codeWndCopy = QAction(QIcon("icons/Copy.png"), "&Copy The Code From The Code Window", self)
        self.toolsBar.addAction(self.codeWndCopy)

        self.codeWndCopy.setCheckable(True)
        self.codeWndCopy.triggered.connect(self.CopyTextCode)
        self.codeWndCopy.setShortcut(QKeySequence("Ctrl+Shift+C"))

    def CopyTextCode(self):
        node_editor = self.CurrentNodeEditor()

        if node_editor is not None:
            node_editor.TextCodeWnd.selectAll()
            node_editor.TextCodeWnd.copy()
            python_file_name = node_editor.windowTitle()

            text = node_editor.TextCodeWnd.toPlainText()
            if os.listdir(self.filesWidget.Project_Directory).__contains__("Generated Scripts") is False:
                os.makedirs(self.filesWidget.Project_Directory + "/Generated Scripts")
                f = self.filesWidget.Project_Directory + f"""/Generated Scripts/{python_file_name}.py"""
                with open(f, 'w') as newPyFile:
                    newPyFile.writelines(text)
            else:
                f = self.filesWidget.Project_Directory + f"""/Generated Scripts/{python_file_name}.py"""
                with open(f, 'w') as newPyFile:
                    newPyFile.writelines(text)

    def closeEvent(self, event):
        self.graphs_parent_wdg.closeAllSubWindows()
        if self.graphs_parent_wdg.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()
            # hacky fix for PyQt 5.14.x
            import sys
            sys.exit(0)

    def createActions(self):
        super().createActions()

        self.actSetProjectDir = QAction('&Open Project', self, shortcut='Ctrl+Shift+O', statusTip="Set a Folder For Your Project", triggered=self.filesWidget.onSetProjectFolder)

        self.actClose = QAction("Cl&ose", self, statusTip="Close the active window",
                                triggered=self.graphs_parent_wdg.closeActiveSubWindow)
        self.actCloseAll = QAction("Close &All", self, statusTip="Close all the windows",
                                   triggered=self.graphs_parent_wdg.closeAllSubWindows)
        self.actTile = QAction("&Tile", self, statusTip="Tile the windows",
                               triggered=self.graphs_parent_wdg.tileSubWindows)
        self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows",
                                  triggered=self.graphs_parent_wdg.cascadeSubWindows)
        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                               statusTip="Move the focus to the next window",
                               triggered=self.graphs_parent_wdg.activateNextSubWindow)
        self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild,
                                   statusTip="Move the focus to the previous window",
                                   triggered=self.graphs_parent_wdg.activatePreviousSubWindow)

        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

        self.actAbout = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)

    def CurrentNodeEditor(self):
        """ we're returning NodeEditorWidget here... """
        activeSubWindow = self.graphs_parent_wdg.activeSubWindow()

        if activeSubWindow:
            return activeSubWindow.widget()
        else:
            return None

    def onNewGraphTab(self):
        # Overrides Node Editor Window > actNew action
        try:
            self.filesWidget.removeDeletedGraphs()

            subwnd = self.newGraphTab()
            subwnd.widget().newGraph()

            subwnd.show()

            self.filesWidget.CreateNewGraph(subwnd)
        except Exception as e:
            dumpException(e)

    def onFileOpen(self, all_files=False):
        if all_files == False:
            file_names, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file', self.filesWidget.Project_Directory, self.getFileDialogFilter())
        else:
            file_names = all_files

        try:
            for file_name in file_names:
                if file_name:
                    if self.findMdiChild(file_name):
                        subwnd = self.findMdiChild(file_name)

                        nodeEditor = subwnd.widget()

                        self.all_graphs.append(nodeEditor)
                        nodeEditor.scene.masterRef = self

                        self.graphs_parent_wdg.setActiveSubWindow(subwnd)

                    else:
                        # we need to create new subWindow and open the file
                        nodeEditor = MasterEditorWnd()
                        subwnd = self.newGraphTab(nodeEditor)

                        if nodeEditor.fileLoad(file_name):
                            self.statusBar().showMessage("File %s loaded" % file_name, 5000)
                            nodeEditor.setWindowTitle(os.path.splitext(os.path.basename(file_name))[0])
                            subwnd.show()
                        else:
                            nodeEditor.close()
        except Exception as e:
            dumpException(e)

    def about(self):
        QMessageBox.about(self, "About Calculator NodeEditor Example",
                          "The <b>Calculator NodeEditor</b> example demonstrates how to write multiple "
                          "document interface applications using PyQt5 and NodeEditor. For more information visit: "
                          "<a href='https://www.blenderfreak.com/'>www.BlenderFreak.com</a>")

    def createMenus(self):
        super().createMenus()

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        # self.windowMenu.aboutToShow.connect(self.updateWindowMenu)
        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actAbout)

        self.editMenu.aboutToShow.connect(self.updateEditMenu)

    def updateMenus(self):
        # print("update Menus")
        active = self.CurrentNodeEditor()
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
            active = self.CurrentNodeEditor()
            hasMdiChild = (active is not None)

            self.actPaste.setEnabled(hasMdiChild)

            self.actCut.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actDelete.setEnabled(hasMdiChild and active.hasSelectedItems())

            self.actUndo.setEnabled(hasMdiChild and active.canUndo())
            self.actRedo.setEnabled(hasMdiChild and active.canRedo())
        except Exception as e:
            dumpException(e)

    def updateWindowMenu(self):

        self.toolbar_details = self.windowMenu.addAction("Properties Window")
        self.toolbar_details.setCheckable(True)
        self.toolbar_details.triggered.connect(self.onWindowDetailsToolbar)
        self.toolbar_details.setChecked(not self.proprietiesDock.isVisible())

        self.toolbar_Files = self.windowMenu.addAction("Project Files Window")
        self.toolbar_Files.setCheckable(True)
        self.toolbar_Files.triggered.connect(self.onWindowFilesToolbar)
        self.toolbar_Files.setChecked(not self.proprietiesDock.isVisible())

        self.toolbar_vars = self.windowMenu.addAction("Variables & Events Window")
        self.toolbar_vars.setCheckable(True)
        self.toolbar_vars.triggered.connect(self.onWindowVarsToolbar)
        self.toolbar_vars.setChecked(not self.varsDock.isVisible())

        self.toolbar_nodes = self.windowMenu.addAction("Functions Window")
        self.toolbar_nodes.setCheckable(True)
        self.toolbar_nodes.triggered.connect(self.onWindowNodesToolbar)
        self.toolbar_nodes.setChecked(not self.nodesDock.isVisible())

        self.windowMenu.addSeparator()

        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        # self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.graphs_parent_wdg.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.CurrentNodeEditor())
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
        if self.proprietiesDock.isVisible():
            self.proprietiesDock.hide()
        else:
            self.proprietiesDock.show()

    def onWindowFilesToolbar(self):
        if self.filesDock.isVisible():
            self.filesDock.hide()
        else:
            self.filesDock.show()

    def createGraphsDock(self):
        self.graphsDock = QDockWidget("Graphs")
        self.graphsDock.setWidget(self.graphs_parent_wdg)
        self.graphsDock.setFeatures(self.graphsDock.DockWidgetClosable | self.graphsDock.DockWidgetMovable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.graphsDock)

    def updateActiveWnd(self):
        if self.nodeDesignerBtn.isChecked():
            self.stackedDisplay.setCurrentIndex(1)
        else:
            self.stackedDisplay.setCurrentIndex(0)

    def createFunctionsDock(self):
        self.nodesListWidget = NodeList()

        self.nodesDock = QDockWidget("Functions")
        self.nodesDock.setWidget(self.nodesListWidget)
        self.nodesDock.setFeatures(self.nodesDock.DockWidgetMovable)
        self.addDockWidget(Qt.RightDockWidgetArea, self.nodesDock)

    def CreateFilesDock(self):
        self.filesWidget = FilesWDG()
        self.filesWidget.masterRef = self

        self.filesDock = QDockWidget("Project Files")
        self.filesDock.setWidget(self.filesWidget)
        self.filesDock.setFeatures(self.filesDock.DockWidgetMovable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.filesDock)

    def CreatePropertiesDock(self):
        self.proprietiesWdg = PropertiesList()

        self.proprietiesDock = QDockWidget("Properties")
        self.proprietiesDock.setWidget(self.proprietiesWdg)
        self.proprietiesDock.setFeatures(self.proprietiesDock.DockWidgetMovable)

        self.addDockWidget(Qt.RightDockWidgetArea, self.proprietiesDock)

    def CreateVarEventDock(self):
        self.varsDock = QDockWidget("Variables & Events")

        self.VEStackedWdg = QStackedWidget()
        self.varsDock.setWidget(self.VEStackedWdg)
        self.varsDock.setFeatures(self.varsDock.DockWidgetMovable)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.varsDock)

    def CreateNewVEList(self):

        new_wdg = self.MakeCopyOfClass(VarEventList)
        new_wdg = new_wdg()
        self.all_VE_lists.append(new_wdg)

        self.VEStackedWdg.addWidget(new_wdg)

        self.VEStackedWdg.setCurrentWidget(new_wdg)

        return new_wdg

    def DeleteVEList(self, ref):
        self.all_VE_lists.remove(ref)
        self.VEStackedWdg.removeWidget(ref)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def RotateTextCodeWnd(self):
        if self.CurrentNodeEditor():
            self.CurrentNodeEditor().setCodeWndViewMode()

    def newGraphTab(self, oldNodeEditor=None):

        VEL = self.CreateNewVEList()

        nodeEditor = oldNodeEditor if oldNodeEditor is not None else MasterEditorWnd()
        self.all_graphs.append(nodeEditor)

        nodeEditor.scene.VEListWdg = VEL
        VEL.Scene = nodeEditor.scene

        nodeEditor.scene.masterRef = self
        nodeEditor.scene.history.masterWndRef = self

        subwnd = self.graphs_parent_wdg.addSubWindow(nodeEditor)

        subwnd.setWindowIcon(self.empty_icon)
        # nodeeditor.scene.addItemSelectedListener(self.updateEditMenu)
        # nodeeditor.scene.addItemsDeselectedListener(self.updateEditMenu)
        nodeEditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeEditor.addCloseEventListener(self.onSubWndClose)

        return subwnd

    def onSubWndClose(self, widget, event):
        existing = self.findMdiChild(widget.filename)

        self.graphs_parent_wdg.setActiveSubWindow(existing)

        self.DeleteVEList(self.graphs_parent_wdg.activeSubWindow().widget().scene.VEListWdg)

        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def findMdiChild(self, filename):
        for window in self.graphs_parent_wdg.subWindowList():
            if window.widget().filename == filename:
                return window
        return None

    def setActiveSubWindow(self, window):
        if window:
            self.graphs_parent_wdg.setActiveSubWindow(window)


