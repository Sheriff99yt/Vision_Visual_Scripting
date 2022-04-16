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

        self.stylesheet_filename = os.path.join(os.path.dirname(__file__), "qss/nodeeditor-night.qss")
        loadStylesheets(
            os.path.join(os.path.dirname(__file__), "qss/nodeeditor-night.qss"), self.stylesheet_filename)

        self.empty_icon = QIcon(".")

        if DEBUG:
            print("Registered nodes:")
            # pp(FUNCTIONS)
        self.graphsNames = []

        self.all_VE_lists = []
        self.all_graphs = []

        self.stackedDisplay = QStackedWidget()

        self.graphs_parent_wdg = QMdiArea()

        self.InitLibraryWnd()

        # Create Node Designer Window
        self.node_designer = MasterDesignerWnd()
        self.stackedDisplay.addWidget(self.graphs_parent_wdg)
        self.stackedDisplay.addWidget(self.node_designer)

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

        # Create Files Dock
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
        self.LibrariesWnd()
        self.library_menu.setEnabled(False)
        self.node_designer_menu.setEnabled(False)

        # self.NodeDesignerBtn.setChecked(True)
        # self.updateActiveWnd()


    def CreateOfflineDir(self):
        self.Offline_Dir = f"C:/Users/{os.getlogin()}/AppData/Roaming/VVS/Offline Library"
        if os.path.exists(self.Offline_Dir):
            pass
        else:
            self.Offline_Dir = os.makedirs(os.getenv('AppData') + "/VVS/Offline Library")

        self.library_offline_list.setRootIndex(self.Model.index(self.Offline_Dir))

    # def onSetProjectFolder(self):
    #     Dir = QFileDialog.getExistingDirectory(self, "Set Project Location")
    #     if Dir != "":
    #         self.Offline_Dir = Dir
    #         self.tree_wdg.setRootIndex(self.Model.index(self.Offline_Dir))
    #         self.MakeDir(self.Offline_Dir)

    def InitLibraryWnd(self):
        self.librariesDock = QDockWidget("Libraries")
        self.library_subwnd = QTabWidget()

        self.librariesDock.setWidget(self.library_subwnd)
        self.librariesDock.setFeatures(self.librariesDock.DockWidgetMovable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.librariesDock)

        offline_Vlayout = QVBoxLayout()
        offline_Vlayout.setContentsMargins(0, 0, 0, 0)

        self.Model = QFileSystemModel()
        self.Model.setRootPath("")

        self.library_offline_list = QTreeView()
        self.library_offline_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.library_offline_list.setModel(self.Model)
        self.library_offline_list.setSortingEnabled(True)
        self.library_offline_list.setColumnWidth(0, 130)
        self.library_offline_list.sortByColumn(0, Qt.AscendingOrder)
        self.library_offline_list.hideColumn(1)
        self.library_offline_list.hideColumn(2)
        self.library_offline_list.setStyleSheet("color: white")

        offline_Vlayout.addWidget(self.library_offline_list)

        self.library_online_list = QListWidget()

        topVlayout = QVBoxLayout()
        search_bar_layout = QHBoxLayout()

        self.search_line_edit = QLineEdit()
        self.search_btn = QPushButton()

        search_bar_layout.addWidget(self.search_line_edit)
        search_bar_layout.addWidget(self.search_btn)

        self.search_btn.setMaximumSize(30, 30)
        self.search_btn.setIcon(QIcon("icons/search.png"))
        self.search_line_edit.setMinimumHeight(30)

        topVlayout.addLayout(search_bar_layout)
        topVlayout.addWidget(self.library_online_list)

        online_widget = QWidget()
        online_widget.setLayout(topVlayout)

        offline_widget = QWidget()
        offline_widget.setLayout(offline_Vlayout)

        self.library_subwnd.addTab(offline_widget, "    Offline    ")
        self.library_subwnd.addTab(online_widget, "    Online    ")

        self.CreateOfflineDir()
        self.library_offline_list.clicked.connect(self.ViewSelectedFiles)

    def ViewSelectedFiles(self):
        all_files = []

        selected_files = self.library_offline_list.selectedIndexes()

        for file_name in selected_files:
            file_path = QFileSystemModel().filePath(file_name)

            if file_path.endswith(".json"):
                if not all_files.__contains__(file_path):
                    all_files.append(file_path)
                    # print(all_files)

        self.onFileOpen(all_files)

    def ActiveGraphSwitched(self):
        if self.CurrentNodeEditor():
            self.VEStackedWdg.setCurrentWidget(self.CurrentNodeEditor().scene.VEListWdg)

    def CreateToolBar(self):
        # Create Tools self.tools_bar
        self.tools_bar = QToolBar("Tools", self)
        self.tools_bar.setIconSize(QSize(26, 26))
        self.tools_bar.setFloatable(False)

        # Add self.tools_bar To Main Window
        self.addToolBar(self.tools_bar)

        # Add and connect self.node_editor_btn
        self.node_editor_btn = QAction(QIcon("icons/Edit 2.png"), "&Node Editor", self)
        self.node_editor_btn.triggered.connect(self.ActivateEditorWnd)
        # self.node_designer_btn.setShortcut(QKeySequence("`"))
        self.tools_bar.addAction(self.node_editor_btn)

        # Add and connect self.node_designer_btn
        self.node_designer_btn = QAction(QIcon("icons/node design.png"), "&Node Designer", self)
        self.node_designer_btn.setEnabled(False)
        self.node_designer_btn.triggered.connect(self.ActivateDesignerWnd)
        # self.node_designer_btn.setShortcut(QKeySequence("`"))
        self.tools_bar.addAction(self.node_designer_btn)

        # Add and connect self.library_btn
        self.library_btn = QAction(QIcon("icons/library.png"), "&Library", self)
        self.library_btn.triggered.connect(self.ActivateLibraryWnd)
        self.library_btn.setShortcut(QKeySequence("`"))
        self.tools_bar.addAction(self.library_btn)

        # Add Spacer Wdg
        mySpacer = QWidget()
        mySpacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tools_bar.addWidget(mySpacer)

        # Add and connect self.code_orientation_btn
        self.code_orientation_btn = QAction(QIcon("icons/Orientation.png"), "&Code Window View Mode", self)
        self.tools_bar.addAction(self.code_orientation_btn)
        self.code_orientation_btn.triggered.connect(self.RotateTextCodeWnd)
        self.code_orientation_btn.setShortcut(QKeySequence("Ctrl+Shift+R"))

        # Add and connect self.code_copy_btn
        self.copy_code_btn = QAction(QIcon("icons/Copy.png"), "&Copy The Code From The Code Window", self)
        self.tools_bar.addAction(self.copy_code_btn)
        self.copy_code_btn.triggered.connect(self.CopyTextCode)
        self.copy_code_btn.setShortcut(QKeySequence("Ctrl+Shift+C"))

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

        self.actSetProjectDir = QAction('&Open Project', self, shortcut='Ctrl+Shift+O',
                                        statusTip="Set a Folder For Your Project",
                                        triggered=self.filesWidget.onSetProjectFolder)

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
            file_names, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file',
                                                              self.filesWidget.Project_Directory,
                                                              self.getFileDialogFilter())
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

        self.node_editor_menu = self.menuBar().addMenu("&Node Editor")

        self.library_menu = self.menuBar().addMenu("&Library")

        self.node_designer_menu = self.menuBar().addMenu("&Node Designer")

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

        self.toolbar_library = self.library_menu.addAction("Libraries Window")
        self.toolbar_library.setCheckable(True)
        self.toolbar_library.triggered.connect(self.LibrariesWnd)
        self.toolbar_library.setChecked(False)

        self.toolbar_properties = self.node_editor_menu.addAction("Properties Window")
        self.toolbar_properties.setCheckable(True)
        self.toolbar_properties.triggered.connect(self.DetailsWnd)
        self.toolbar_properties.setChecked(True)

        self.toolbar_files = self.node_editor_menu.addAction("Project Files Window")
        self.toolbar_files.setCheckable(True)
        self.toolbar_files.triggered.connect(self.FilesWnd)
        self.toolbar_files.setChecked(True)

        self.toolbar_events_vars = self.node_editor_menu.addAction("Variables & Events Window")
        self.toolbar_events_vars.setCheckable(True)
        self.toolbar_events_vars.triggered.connect(self.EventsVarsWnd)
        self.toolbar_events_vars.setChecked(True)

        self.toolbar_functions = self.node_editor_menu.addAction("Functions Window")
        self.toolbar_functions.setCheckable(True)
        self.toolbar_functions.triggered.connect(self.FunctionsWnd)
        self.toolbar_functions.setChecked(True)

        self.node_editor_menu.addSeparator()

        self.node_editor_menu.addAction(self.actClose)
        self.node_editor_menu.addAction(self.actCloseAll)
        self.node_editor_menu.addSeparator()
        self.node_editor_menu.addAction(self.actTile)
        # self.windowMenu.addAction(self.actCascade)
        self.node_editor_menu.addSeparator()
        self.node_editor_menu.addAction(self.actNext)
        self.node_editor_menu.addAction(self.actPrevious)
        self.node_editor_menu.addAction(self.actSeparator)

        windows = self.graphs_parent_wdg.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.node_editor_menu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.CurrentNodeEditor())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def FunctionsWnd(self):
        self.toolbar_functions.setChecked(self.toolbar_functions.isChecked())
        self.functionsDock.setVisible(self.toolbar_functions.isChecked())

    def EventsVarsWnd(self):
        self.toolbar_events_vars.setChecked(self.toolbar_events_vars.isChecked())
        self.varsEventsDock.setVisible(self.toolbar_events_vars.isChecked())

    def DetailsWnd(self):
        self.toolbar_properties.setChecked(self.toolbar_properties.isChecked())
        self.proprietiesDock.setVisible(self.toolbar_properties.isChecked())

    def LibrariesWnd(self):
        self.toolbar_library.setChecked(self.toolbar_library.isChecked())
        self.librariesDock.setVisible(self.toolbar_library.isChecked())

    def FilesWnd(self):
        self.toolbar_files.setChecked(self.toolbar_files.isChecked())
        self.filesDock.setVisible(self.toolbar_files.isChecked())

    def createGraphsDock(self):
        self.graphsDock = QDockWidget("Graphs")
        self.graphsDock.setWidget(self.graphs_parent_wdg)
        self.graphsDock.setFeatures(self.graphsDock.DockWidgetClosable | self.graphsDock.DockWidgetMovable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.graphsDock)

    def ActivateEditorWnd(self):
        self.node_editor_menu.setEnabled(True)
        self.library_menu.setEnabled(False)
        self.stackedDisplay.setCurrentIndex(0)

        self.toolbar_library.setChecked(False)
        self.librariesDock.setVisible(self.toolbar_library.isChecked())

        self.toolbar_functions.setChecked(True)
        self.functionsDock.setVisible(self.toolbar_functions.isChecked())

        self.toolbar_files.setChecked(True)
        self.filesDock.setVisible(self.toolbar_files.isChecked())

        self.toolbar_properties.setChecked(True)
        self.proprietiesDock.setVisible(self.toolbar_properties.isChecked())

    def ActivateDesignerWnd(self):
        self.node_editor_menu.setEnabled(False)
        self.library_menu.setEnabled(False)
        self.stackedDisplay.setCurrentIndex(1)

        self.toolbar_library.setChecked(False)
        self.librariesDock.setVisible(self.toolbar_library.isChecked())


    def ActivateLibraryWnd(self):
        self.node_editor_menu.setEnabled(False)
        self.library_menu.setEnabled(True)
        self.stackedDisplay.setCurrentIndex(0)

        self.toolbar_library.setChecked(True)
        self.librariesDock.setVisible(self.toolbar_library.isChecked())

        self.toolbar_functions.setChecked(False)
        self.functionsDock.setVisible(self.toolbar_functions.isChecked())

        self.toolbar_files.setChecked(False)
        self.filesDock.setVisible(self.toolbar_files.isChecked())

        self.toolbar_properties.setChecked(False)
        self.proprietiesDock.setVisible(self.toolbar_properties.isChecked())

    def createFunctionsDock(self):
        self.nodesListWidget = NodeList()

        self.functionsDock = QDockWidget("Functions")
        self.functionsDock.setWidget(self.nodesListWidget)
        self.functionsDock.setFeatures(self.functionsDock.DockWidgetMovable)
        self.addDockWidget(Qt.RightDockWidgetArea, self.functionsDock)

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
        self.varsEventsDock = QDockWidget("Variables & Events")

        self.VEStackedWdg = QStackedWidget()
        self.varsEventsDock.setWidget(self.VEStackedWdg)
        self.varsEventsDock.setFeatures(self.varsEventsDock.DockWidgetMovable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.varsEventsDock)

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

        ref = self.graphs_parent_wdg.activeSubWindow()
        if ref:
            ref = ref.widget().scene.VEListWdg

            self.DeleteVEList(ref)


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
