import os
import subprocess

from qtpy.QtGui import *
from qtpy.QtWidgets import *
from qtpy.QtCore import *

from nodeeditor.node_editor_widget import NodeEditorWidget
from nodeeditor.utils import loadStylesheets
from nodeeditor.node_editor_window import NodeEditorWindow
from vvs_app.editor_settings_wnd import SettingsWidget
from vvs_app.master_editor_wnd import MasterEditorWnd
from vvs_app.master_designer_wnd import MasterDesignerWnd
from vvs_app.editor_node_list import NodeList
from vvs_app.editor_files_wdg import FilesWDG
from vvs_app.editor_var_events_lists import VarEventList
from vvs_app.editor_proterties_list import PropertiesList
from vvs_app.global_switches import *

from nodeeditor.utils import dumpException
# from vvs_app.nodes_configuration import FUNCTIONS

# Enabling edge validators
from nodeeditor.node_edge import Edge
from nodeeditor.node_edge_validators import (
    edge_cannot_connect_two_outputs_or_two_inputs,
    edge_cannot_connect_input_and_output_of_same_node
)

# Edge.registerEdgeValidator(edge_validator_debug)
from vvs_app.master_node import MasterNode
from vvs_app.nodes.nodes_configuration import register_Node

Edge.registerEdgeValidator(edge_cannot_connect_two_outputs_or_two_inputs)
Edge.registerEdgeValidator(edge_cannot_connect_input_and_output_of_same_node)

# images for the dark skin

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

        for cls in MasterNode.__subclasses__():
            register_Node(cls)

        self.global_switches = GlobalSwitches()
        self.global_switches.MasterRef = self

        self.settingsWidget = None

        self.stackedDisplay = QStackedWidget()

        self.graphs_parent_wdg = QMdiArea()

        self.CreateLibraryWnd()

        # Create Node Designer Window
        self.node_designer = MasterDesignerWnd()

        self.stackedDisplay.addWidget(self.graphs_parent_wdg)

        self.stackedDisplay.addWidget(self.node_designer)

        self.graphs_parent_wdg.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.graphs_parent_wdg.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.graphs_parent_wdg.setTabsClosable(True)
        self.graphs_parent_wdg.setTabsMovable(True)
        self.graphs_parent_wdg.subWindowActivated.connect(self.active_graph_switched)

        self.setCentralWidget(self.stackedDisplay)

        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        # Create Welcome Screen and allow user to set the project Directory
        self.create_welcome_screen()

        # Create Details List Window
        self.create_properties_dock()

        # Create Nodes List
        self.create_functions_dock()

        # Create Files Dock
        self.create_files_dock()

        # Create Variable List
        self.create_var_event_dock()

        self.createActions()
        self.create_menus()
        self.createStatusBar()
        self.update_menus()

        self.readSettings()

        self.CreateToolBar()

        self.setWindowTitle("Vision Visual Scripting")
        self.update_libraries_wnd()
        self.library_menu.setEnabled(False)
        self.node_designer_menu.setEnabled(False)


    def create_welcome_screen(self):
        Elayout = QVBoxLayout()
        Elayout.setAlignment(Qt.AlignCenter)
        Elayout.setSpacing(20)

        self.empty_screen = QWidget()
        self.empty_screen.setLayout(Elayout)

        user_text = QLabel("Select Your Project Directory...")
        user_text.setFont(QFont("Roboto", 14))
        w_image = QPixmap("icons/VVS_White.png")

        welcome_image = QLabel()
        welcome_image.setPixmap(w_image)
        self.brows_btn = QPushButton("Brows..")

        Elayout.addWidget(welcome_image)
        Elayout.addItem(QSpacerItem(120, 120))
        Elayout.addWidget(user_text)
        Elayout.addWidget(self.brows_btn)

        self.stackedDisplay.addWidget(self.empty_screen)
        self.switch_display(Welcome=True)

    def CreateOfflineDir(self):
        self.Offline_Dir = f"C:/Users/{os.getlogin()}/AppData/Roaming/VVS/Offline Library"
        if os.path.exists(self.Offline_Dir):
            pass
        else:
            self.Offline_Dir = os.makedirs(os.getenv('AppData') + "/VVS/Offline Library")

        self.library_offline_list.setRootIndex(self.Model.index(self.Offline_Dir))

    def CreateLibraryWnd(self):
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
        self.library_offline_list.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

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

        self.on_file_open(all_files)

    def active_graph_switched(self):
        self.update_menus()
        if self.currentNodeEditor():
            self.VEStackedWdg.setCurrentWidget(self.currentNodeEditor().scene.user_nodes_wdg)

    def switch_display(self, Welcome=False, Editor=False, Designer=False, Library=False):
        # Use the Argument To Force Activate the Specified Window

        if Editor or Library:
            self.stackedDisplay.setCurrentIndex(0)
            return
        elif Designer:
            self.stackedDisplay.setCurrentIndex(1)
            return

        elif Welcome:
            self.stackedDisplay.setCurrentIndex(2)
            return

    def CreateToolBar(self):
        # Create Tools self.tools_bar
        self.tools_bar = QToolBar("Tools", self)
        self.tools_bar.setIconSize(QSize(20, 20))
        self.tools_bar.setFloatable(False)

        # Add self.tools_bar To Main Window
        self.addToolBar(self.tools_bar)

        # Add and connect self.settingsBtn
        self.settingsBtn = QAction(QIcon("icons/Settings.png"), "&Open Settings Window", self)
        self.settingsBtn.setCheckable(True)
        self.settingsBtn.triggered.connect(self.onSettingsOpen)
        self.settingsBtn.setShortcut(QKeySequence(self.global_switches.switches_Dict["Settings Window"]))
        self.tools_bar.addAction(self.settingsBtn)
        self.actions_list["Settings Window"] = self.settingsBtn

        # Add Separator
        self.tools_bar.addSeparator()

        # Add and connect self.node_editor_btn
        self.node_editor_btn = QAction(QIcon("icons/Edit 2.png"), "&Node Editor", self)
        self.node_editor_btn.setCheckable(True)
        self.node_editor_btn.triggered.connect(self.activate_editor_wnd)
        # self.node_designer_btn.setShortcut(QKeySequence("key"))
        self.tools_bar.addAction(self.node_editor_btn)

        # Add and connect self.node_designer_btn
        self.node_designer_btn = QAction(QIcon("icons/node design.png"), "&Node Designer", self)
        self.node_designer_btn.setEnabled(False)
        self.node_designer_btn.setCheckable(True)
        self.node_designer_btn.triggered.connect(self.activate_designer_wnd)
        # self.node_designer_btn.setShortcut(QKeySequence("`"))
        self.tools_bar.addAction(self.node_designer_btn)

        # Add and connect self.library_btn
        self.library_btn = QAction(QIcon("icons/library.png"), "&Library", self)
        self.library_btn.setCheckable(True)
        self.library_btn.triggered.connect(self.activate_library_wnd)
        self.library_btn.setShortcut(QKeySequence("`"))
        self.tools_bar.addAction(self.library_btn)

        # Add Separator
        self.tools_bar.addSeparator()

        # # Add Separator
        # self.tools_bar.addSeparator()

    def onSettingsOpen(self):
        if self.settingsWidget:
            if self.settingsWidget.isHidden():
                self.settingsWidget.show()
                self.settingsBtn.setChecked(True)
            else:
                self.settingsWidget.hide()
        else:
            self.settingsWidget = SettingsWidget()
            self.settingsWidget.masterRef = self
            self.settingsWidget.show()
            self.settingsBtn.setChecked(True)

            self.settingsWidget.setWindowTitle("Settings")
            self.settingsWidget.setGeometry(300, 150, 1200, 800)

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

        self.actClose = QAction("Cl&ose", self, statusTip="Close the active window", triggered=self.graphs_parent_wdg.closeActiveSubWindow)
        self.actCloseAll = QAction("Close &All", self, statusTip="Close all the windows", triggered=self.graphs_parent_wdg.closeAllSubWindows)
        self.actTile = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.graphs_parent_wdg.tileSubWindows)
        self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows", triggered=self.graphs_parent_wdg.cascadeSubWindows)
        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild, statusTip="Move the focus to the next window", triggered=self.graphs_parent_wdg.activateNextSubWindow)
        self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild, statusTip="Move the focus to the previous window", triggered=self.graphs_parent_wdg.activatePreviousSubWindow)

        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

        self.actAbout = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)
        self.actDoc = QAction("&Documentation", self, triggered=self.open_doc)

        self.actions_list = {"New Graph": self.actNew,
                             "Open": self.actOpen,
                             "Set Project Location": self.actSetProjectDir,
                             "Save": self.actSave,
                             "Save As": self.actSaveAs,
                             "Exit": self.actExit,

                             "Undo": self.actUndo,
                             "Redo": self.actRedo,
                             "Cut": self.actCut,
                             "Copy": self.actCopy,
                             "Paste": self.actPaste,
                             "Delete": self.actDelete}

    def open_doc(self):
        subprocess.Popen('hh.exe "VVS-Help.chm"')

    def currentNodeEditor(self):
        """ we're returning NodeEditorWidget here... """
        activeSubWindow = self.graphs_parent_wdg.activeSubWindow()

        if activeSubWindow:
            return activeSubWindow.widget()
        else:
            return None

    def on_new_graph_tab(self):
        # Overrides Node Editor Window > actNew action
        try:
            subwnd = self.new_graph_tab()

            all_names = []
            for item in self.graphs_parent_wdg.subWindowList(): all_names.append(item.widget().windowTitle())

            self.filesWidget.new_graph_name(subwnd, all_names)

        except Exception as e:
            dumpException(e)

    def on_file_open(self, all_files=False):

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
                        self.graphs_parent_wdg.setActiveSubWindow(subwnd)

                    else:
                        # We need to create new subWindow and open the file
                        subwnd = self.new_graph_tab()
                        node_editor = subwnd.widget()

                        if node_editor.fileLoad(file_name):
                            self.statusBar().showMessage("File %s loaded" % file_name, 5000)
                            node_editor.setWindowTitle(os.path.splitext(os.path.basename(file_name))[0])
                        else:
                            node_editor.close()

        except Exception as e:
            dumpException(e)

    def create_menus(self):
        super().create_menus()

        self.node_editor_menu = self.menuBar().addMenu("&Node Editor")

        self.library_menu = self.menuBar().addMenu("&Library")

        self.node_designer_menu = self.menuBar().addMenu("&Node Designer")

        self.update_window_menu()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actDoc)
        self.helpMenu.addAction(self.actAbout)

        self.editMenu.aboutToShow.connect(self.update_edit_menu)

    def update_menus(self):
        # print("update Menus")
        active = self.currentNodeEditor()
        hasMdiChild = (active is not None)

        # Update File Menu
        self.actSave.setEnabled(hasMdiChild)
        self.actSaveAs.setEnabled(hasMdiChild)

        # Update Node Editor Menu
        self.actClose.setEnabled(hasMdiChild)
        self.actCloseAll.setEnabled(hasMdiChild)
        self.actTile.setEnabled(hasMdiChild)
        self.actCascade.setEnabled(hasMdiChild)
        self.actNext.setEnabled(hasMdiChild)
        self.actPrevious.setEnabled(hasMdiChild)
        self.actSeparator.setVisible(hasMdiChild)

        # Update Edit Menu
        self.update_edit_menu()

    def update_edit_menu(self):
        try:
            # print("update Edit Menu")
            active = self.currentNodeEditor()
            hasMdiChild = (active is not None)

            self.actPaste.setEnabled(hasMdiChild)

            self.actCut.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actDelete.setEnabled(hasMdiChild and active.hasSelectedItems())

            self.actUndo.setEnabled(hasMdiChild and active.canUndo())
            self.actRedo.setEnabled(hasMdiChild and active.canRedo())

        except Exception as e:
            dumpException(e)

    def update_window_menu(self):

        self.toolbar_library = self.library_menu.addAction("Libraries Window")
        self.toolbar_library.setCheckable(True)
        self.toolbar_library.triggered.connect(self.update_libraries_wnd)
        self.toolbar_library.setChecked(False)

        self.toolbar_properties = self.node_editor_menu.addAction("Properties Window")
        self.toolbar_properties.setCheckable(True)
        self.toolbar_properties.triggered.connect(self.update_details_wnd)
        self.toolbar_properties.setChecked(True)

        self.toolbar_files = self.node_editor_menu.addAction("Project Files Window")
        self.toolbar_files.setCheckable(True)
        self.toolbar_files.triggered.connect(self.update_files_wnd)
        self.toolbar_files.setChecked(True)

        self.toolbar_events_vars = self.node_editor_menu.addAction("Variables & Events Window")
        self.toolbar_events_vars.setCheckable(True)
        self.toolbar_events_vars.triggered.connect(self.update_events_vars_wnd)
        self.toolbar_events_vars.setChecked(True)

        self.toolbar_functions = self.node_editor_menu.addAction("Functions Window")
        self.toolbar_functions.setCheckable(True)
        self.toolbar_functions.triggered.connect(self.update_functions_wnd)
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
            action.setChecked(child is self.currentNodeEditor())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def update_functions_wnd(self):
        self.toolbar_functions.setChecked(self.toolbar_functions.isChecked())
        self.functionsDock.setVisible(self.toolbar_functions.isChecked())

    def update_events_vars_wnd(self):
        self.toolbar_events_vars.setChecked(self.toolbar_events_vars.isChecked())
        self.varsEventsDock.setVisible(self.toolbar_events_vars.isChecked())

    def update_details_wnd(self):
        self.toolbar_properties.setChecked(self.toolbar_properties.isChecked())
        self.proprietiesDock.setVisible(self.toolbar_properties.isChecked())

    def update_libraries_wnd(self):
        self.toolbar_library.setChecked(self.toolbar_library.isChecked())
        self.librariesDock.setVisible(self.toolbar_library.isChecked())

    def update_files_wnd(self):
        self.toolbar_files.setChecked(self.toolbar_files.isChecked())
        self.filesDock.setVisible(self.toolbar_files.isChecked())

    def create_graphs_dock(self):
        self.graphsDock = QDockWidget("Graphs")
        self.graphsDock.setWidget(self.graphs_parent_wdg)
        self.graphsDock.setFeatures(self.graphsDock.DockWidgetClosable | self.graphsDock.DockWidgetMovable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.graphsDock)

    def activate_editor_wnd(self):
        self.switch_display(Editor=True)

        self.node_editor_btn.setChecked(True)
        self.node_designer_btn.setChecked(False)
        self.library_btn.setChecked(False)

        self.node_editor_menu.setEnabled(True)
        self.library_menu.setEnabled(False)

        self.toolbar_library.setChecked(False)
        self.librariesDock.setVisible(self.toolbar_library.isChecked())

        self.toolbar_functions.setChecked(True)
        self.functionsDock.setVisible(self.toolbar_functions.isChecked())

        self.toolbar_files.setChecked(True)
        self.filesDock.setVisible(self.toolbar_files.isChecked())

        self.toolbar_properties.setChecked(True)
        self.proprietiesDock.setVisible(self.toolbar_properties.isChecked())

    def activate_designer_wnd(self):
        self.switch_display(Designer=True)

        self.node_designer_btn.setChecked(True)
        self.library_btn.setChecked(False)
        self.node_editor_btn.setChecked(False)

        self.node_editor_menu.setEnabled(False)
        self.library_menu.setEnabled(False)

        self.toolbar_library.setChecked(False)
        self.librariesDock.setVisible(self.toolbar_library.isChecked())


    def activate_library_wnd(self):
        self.switch_display(Library=True)

        self.library_btn.setChecked(True)
        self.node_editor_btn.setChecked(False)
        self.node_designer_btn.setChecked(False)

        self.node_editor_menu.setEnabled(False)
        self.library_menu.setEnabled(True)

        self.toolbar_library.setChecked(True)
        self.librariesDock.setVisible(self.toolbar_library.isChecked())

        self.toolbar_functions.setChecked(False)
        self.functionsDock.setVisible(self.toolbar_functions.isChecked())

        self.toolbar_files.setChecked(False)
        self.filesDock.setVisible(self.toolbar_files.isChecked())

        self.toolbar_properties.setChecked(False)
        self.proprietiesDock.setVisible(self.toolbar_properties.isChecked())

    def create_functions_dock(self):
        self.nodesListWidget = NodeList()

        self.functionsDock = QDockWidget("Functions")
        self.functionsDock.setWidget(self.nodesListWidget)
        self.functionsDock.setFeatures(self.functionsDock.DockWidgetMovable)
        self.addDockWidget(Qt.RightDockWidgetArea, self.functionsDock)

    def create_files_dock(self):
        self.filesWidget = FilesWDG()
        self.filesWidget.masterRef = self

        self.brows_btn.clicked.connect(self.filesWidget.on_open_folder)

        self.filesDock = QDockWidget("Project Files")
        self.filesDock.setWidget(self.filesWidget)
        self.filesDock.setFeatures(self.filesDock.DockWidgetMovable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.filesDock)

    def create_properties_dock(self):
        self.proprietiesWdg = PropertiesList()

        self.proprietiesDock = QDockWidget("Properties")
        self.proprietiesDock.setWidget(self.proprietiesWdg)
        self.proprietiesDock.setFeatures(self.proprietiesDock.DockWidgetMovable)

        self.addDockWidget(Qt.RightDockWidgetArea, self.proprietiesDock)

    def create_var_event_dock(self):
        self.varsEventsDock = QDockWidget("Variables & Events")

        self.VEStackedWdg = QStackedWidget()

        self.varsEventsDock.setWidget(self.VEStackedWdg)
        self.varsEventsDock.setFeatures(self.varsEventsDock.DockWidgetMovable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.varsEventsDock)

    def create_user_nodes_list(self):
        new_wdg = self.MakeCopyOfClass(VarEventList)
        new_wdg = new_wdg()

        self.VEStackedWdg.addWidget(new_wdg)

        self.VEStackedWdg.setCurrentWidget(new_wdg)

        return new_wdg

    def delete_user_nodes_wgd(self, ref):
        self.VEStackedWdg.removeWidget(ref)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def new_graph_tab(self):
        # This Check Prevents The Parent graph from opening in Cascade view-mode
        if not self.graphs_parent_wdg.subWindowList():
            self.switch_display(Editor=True)

        VEL = self.create_user_nodes_list()

        node_editor = MasterEditorWnd()

        node_editor.scene.user_nodes_wdg = VEL
        VEL.Scene = node_editor.scene

        node_editor.scene.masterRef = self
        node_editor.scene.history.masterRef = self

        subwnd = QMdiSubWindow()
        subwnd.setAttribute(Qt.WA_DeleteOnClose, True)
        subwnd.setWidget(node_editor)

        self.graphs_parent_wdg.addSubWindow(subwnd)
        subwnd.setWindowIcon(self.empty_icon)

        node_editor.scene.addItemSelectedListener(self.update_edit_menu)
        node_editor.scene.addItemsDeselectedListener(self.update_edit_menu)

        node_editor.scene.history.addHistoryModifiedListener(self.update_edit_menu)
        node_editor.addCloseEventListener(self.on_sub_wnd_close)

        self.graphs_parent_wdg.setViewMode(QMdiArea.TabbedView)

        subwnd.show()
        return subwnd

    def on_sub_wnd_close(self, widget, event):
        self.delete_user_nodes_wgd(widget.scene.user_nodes_wdg)

        existing = self.findMdiChild(widget.filename)

        self.graphs_parent_wdg.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()
            if (len(self.graphs_parent_wdg.subWindowList())-1) == 0:
                self.switch_display(Welcome=True)
            else:
                self.switch_display(Editor=True)

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

    def get_settings_content(self, widget):
        if type(widget) == QKeySequenceEdit:
            value = widget.keySequence().toString()
        elif type(widget) == QSpinBox or type(widget) == QDoubleSpinBox:
            value = widget.value()
        elif type(widget) == QLineEdit or type(widget) == QLabel:
            value = widget.text()
        else:
            value = None
            print("Widget Not Supported")
        return value

    def set_settings_content(self, widget, new_value: int):
        if type(widget) == QKeySequenceEdit:
            widget.setKeySequence(new_value)
        elif type(widget) == QSpinBox or type(widget) == QDoubleSpinBox:
            widget.setValue(new_value)
        elif type(widget) == QLineEdit or type(widget) == QLabel:
            widget.setText(new_value)
        else:
            print("Widget Not Supported")

    def about(self):
        QMessageBox.about(self, "About Calculator NodeEditor Example",
                          "The <b>Calculator NodeEditor</b> example demonstrates how to write multiple "
                          "document interface applications using PyQt5 and NodeEditor. For more information visit: "
                          "<a href='https://www.blenderfreak.com/'>www.BlenderFreak.com</a>")
