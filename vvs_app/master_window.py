import os
import subprocess
import sys

from qtpy.QtGui import *
from qtpy.QtWidgets import *
from qtpy.QtCore import *

from utils import loadStylesheets
from node_editor_window import NodeEditorWindow
from editor_settings_wnd import SettingsWidget
from master_editor_wnd import NodeEditorTab
from master_designer_wnd import MasterDesignerWnd
from editor_node_list import NodeList
from editor_files_wdg import FilesWDG
from editor_user_nodes_list import UserNodesList
from editor_properties_list import PropertiesList
from global_switches import *

from utils import dumpException
# from nodes_configuration import FUNCTIONS

# Enabling edge validators
from node_edge import Edge
from node_edge_validators import (
    edge_cannot_connect_two_outputs_or_two_inputs,
    edge_cannot_connect_input_and_output_of_same_node
)

# Edge.registerEdgeValidator(edge_validator_debug)
from master_node import MasterNode
from nodes.nodes_configuration import register_Node

Edge.registerEdgeValidator(edge_cannot_connect_two_outputs_or_two_inputs)
Edge.registerEdgeValidator(edge_cannot_connect_input_and_output_of_same_node)

# images for the dark skin

DEBUG = False

class Splash(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: transparent")
        self.setAttribute(Qt.WA_TranslucentBackground, on=True)
        self.setWindowFlag(Qt.FramelessWindowHint)

        lo = QVBoxLayout()
        self.setLayout(lo)

        Logo = QLabel()
        pixmap = QPixmap("vvs_app/icons/Dark/VVS_White2.png")
        Logo.setPixmap(pixmap)
        lo.addWidget(Logo)

        self.Loading_Label = QLabel("Loading")
        self.Loading_Label.setStyleSheet("font: 20px; color: white") # font-family: Calibri;
        lo.addWidget(self.Loading_Label)

        self.timer = QTimer()

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()

    def run(self, Main):
        self.show()
        self.timer.start(300)
        self.times = 0
        self.timer.timeout.connect(lambda: self.run_timeout(Main))

    def run_timeout(self, Main):
        if self.times >= 3:
            Main.showMaximized()
            self.close()
            self.timer.stop()
        else:
            self.times += 1
            self.Loading_Label.setText(self.Loading_Label.text() + " .")

class MasterWindow(NodeEditorWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # self.qss_theme = "qss/nodeeditor-light.qss"
        self.qss_theme = self.global_switches.themes[self.global_switches.switches_Dict["Appearance"]["Theme"][0]] # ["Theme"][0]

        self.stylesheet_filename = os.path.join(os.path.dirname(__file__), self.qss_theme)

        loadStylesheets(
            os.path.join(os.path.dirname(__file__), self.qss_theme), self.stylesheet_filename)

        self.empty_icon = QIcon(".")

        if DEBUG: print("Registered nodes:")

        self.stackedDisplay = QStackedWidget()

        self.graphs_parent_wdg = QMdiArea()

        self.CreateLibraryWnd()

        # Create Node Designer Window
        self.node_designer = MasterDesignerWnd(self)

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

        # Create Nodes List
        self.create_functions_dock()

        # Create Files Dock
        self.create_files_dock()

        # Create Details List Window
        self.create_properties_dock()

        # Create Variable List
        self.create_user_nodes_dock()

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

        self.set_actions_shortcuts()

    def create_welcome_screen(self):
        Elayout = QVBoxLayout()
        Elayout.setAlignment(Qt.AlignCenter)
        Elayout.setSpacing(20)

        self.empty_screen = QWidget()
        self.empty_screen.setLayout(Elayout)

        user_text = QLabel("Select Your Project Directory...")
        user_text.setFont(QFont("Roboto", 14))
        w_image = QPixmap(f"vvs_app/icons/{self.global_switches.switches_Dict['Appearance']['Theme'][0]}/VVS_White1.png")

        welcome_image = QLabel()
        welcome_image.setPixmap(w_image)
        welcome_image.setScaledContents(True)

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
        self.addDockWidget(Qt.RightDockWidgetArea, self.librariesDock)

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
        self.search_btn.setIcon(QIcon("vvs_app/icons/Light/search.png"))
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

        if Editor:
            self.stackedDisplay.setCurrentIndex(0)
            self.library_btn.setChecked(False)
            self.node_editor_btn.setChecked(True)
            self.node_designer_btn.setChecked(False)
            return

        if Library:
            self.stackedDisplay.setCurrentIndex(0)
            self.library_btn.setChecked(True)
            self.node_editor_btn.setChecked(False)
            self.node_designer_btn.setChecked(False)
            return

        elif Designer:
            self.stackedDisplay.setCurrentIndex(1)
            self.library_btn.setChecked(False)
            self.node_editor_btn.setChecked(False)
            self.node_designer_btn.setChecked(True)

            self.node_editor_menu.setEnabled(False)
            self.library_menu.setEnabled(False)

            self.toolbar_library.setChecked(False)
            self.librariesDock.setVisible(self.toolbar_library.isChecked())

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
        self.settingsBtn = QAction(QIcon(self.global_switches.get_icon("settings.png")), "&Open Settings Window", self)
        self.settingsBtn.setIconText("settings.png")
        self.settingsBtn.setCheckable(True)
        self.settingsBtn.triggered.connect(self.onSettingsOpen)
        self.settingsBtn.setShortcut(QKeySequence(self.global_switches.switches_Dict["Key Mapping"]["Settings Window"]))
        self.tools_bar.addAction(self.settingsBtn)
        self.actions_creation_dict["UI"]["Settings Window"] = [self.settingsBtn]

        # Add Separator
        self.tools_bar.addSeparator()

        self.node_editor_btn = QAction(QIcon(self.global_switches.get_icon("edit.png")), "&Node Editor", self)
        self.node_editor_btn.setIconText("edit.png")
        self.node_editor_btn.setCheckable(True)
        self.node_editor_btn.triggered.connect(self.activate_editor_mode)
        self.tools_bar.addAction(self.node_editor_btn)
        self.actions_creation_dict["UI"]["Node Editor Window"] = [self.node_editor_btn]

        # Add and connect self.node_designer_btn
        self.node_designer_btn = QAction(QIcon(self.global_switches.get_icon("node design.png")), "&Node Designer", self)
        self.node_designer_btn.setIconText("node design.png")
        self.node_designer_btn.setEnabled(False)
        self.node_designer_btn.setCheckable(True)
        self.node_designer_btn.triggered.connect(self.activate_designer_mode)
        self.tools_bar.addAction(self.node_designer_btn)
        self.actions_creation_dict["UI"]["Node Designer Window"] = [self.node_designer_btn]

        # Add and connect self.library_btn
        self.library_btn = QAction(QIcon(self.global_switches.get_icon("library.png")), "&Library", self)
        self.library_btn.setIconText("library.png")
        self.library_btn.setCheckable(True)
        self.library_btn.triggered.connect(self.activate_library_mode)
        self.library_btn.setShortcut(QKeySequence("`"))
        self.tools_bar.addAction(self.library_btn)
        self.actions_creation_dict["UI"]["Library Window"] = [self.library_btn]

        # Add Separator
        self.tools_bar.addSeparator()

    def onSettingsOpen(self):
        if self.__dict__.__contains__("settingsWidget"):
            if self.settingsWidget.isHidden():
                self.settingsWidget.show()
                self.settingsBtn.setChecked(True)
            else:
                self.settingsWidget.hide()
        else:
            self.settingsWidget = SettingsWidget(masterRef=self)

            self.global_switches.update_font_size(self.global_switches.switches_Dict["Appearance"]["Font Size"])

            self.settingsWidget.show()
            self.settingsBtn.setChecked(True)

            self.settingsWidget.setWindowTitle("Settings")
            self.settingsWidget.setGeometry(300, 150, 500, 500)

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
        self.actions_creation_dict = \
            {
                "File Menu":
                    {
                        "New Graph": [None, "Create new graph", self.on_new_graph_tab, '&New Graph'],
                        "addSeparator 1": [],
                        "Open": [None, "Open file", self.on_file_open, '&Open'],
                        "Set Project Location": [None, "Set a Folder For Your Project", self.files_widget.set_project_folder, '&Set Project Location'],
                        "Save": [None, "Save file", self.onFileSave, '&Save'],
                        "Save As": [None, "Save file as...", self.on_file_save_as, 'Save &As...'],
                        "addSeparator 2": [],
                        "Exit": [None, "Exit application", self.close, 'E&xit']
                    }
                ,
                "Edit Menu":
                    {
                        "Undo": [None, "Undo last operation", self.onEditUndo, '&Undo'],
                        "Redo": [None, "Redo last operation", self.onEditRedo, "&Redo"],
                        "addSeparator 1": [],
                        "Select All": [None, "Select's All Nodes", self.selectAllNodes, 'Select&All'],
                        "Cut": [None, "Cut to clipboard", self.onEditCut, 'Cu&t'],
                        "Copy": [None, "Copy to clipboard", self.onEditCopy, '&Copy'],
                        "Paste": [None, "Paste from clipboard", self.onEditPaste, '&Paste'],
                        "addSeparator 2": [],
                        "Delete": [None, "Delete selected items", self.onEditDelete, "&Delete"]
                    }
                ,
                "Node Editor Menu":
                    {
                        "Close": [None, "Close the active window", self.graphs_parent_wdg.closeActiveSubWindow, "Cl&ose"],
                        "Close All": [None, "Close all the windows", self.graphs_parent_wdg.closeAllSubWindows, "Close &All"],
                        "addSeparator 2": [],
                        "Tile": [None, "Tile the windows", self.graphs_parent_wdg.tileSubWindows, "&Tile"],
                        "addSeparator 3": [],
                        "Next": [None, "Move the focus to the next window", self.graphs_parent_wdg.activateNextSubWindow, "Ne&xt"],
                        "Previous": [None, "Move the focus to the previous window", self.graphs_parent_wdg.activatePreviousSubWindow, "Pre&vious"]
                    }
                ,
                "Help":
                    {
                        "About": [None, "Show the application's About box", self.about, "&About"],
                        "Doc": [None, "Program Documentation", self.open_doc, "&Documentation"]
                    }
                ,
                "UI":
                    {}
            }
        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

    def set_actions_shortcuts(self):
        shortcuts = self.global_switches.switches_Dict["Key Mapping"]
        for menu in self.actions_creation_dict:
            for act in self.actions_creation_dict[menu]:
                menu_vals = self.actions_creation_dict[menu]
                if not act.__contains__("addSeparator"):
                    if shortcuts.__contains__(act):
                        menu_vals[act][0].setShortcut(shortcuts[act])

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
            for item in self.graphs_parent_wdg.subWindowList():
                all_names.append(item.widget().windowTitle())

            self.files_widget.new_graph_name(subwnd, all_names)

        except Exception as e:
            dumpException(e)

    def on_file_open(self, all_files=False):

        if all_files == False:
            file_names, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file',
                                                              self.files_widget.Project_Directory,
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

        for i in self.actions_creation_dict["Help"]:
            if i.__contains__("addSeparator"):
                self.helpMenu.addSeparator()
            else:
                mylist = self.actions_creation_dict["Help"][i]
                act = QAction(mylist[3], parent=self, statusTip=mylist[1], triggered=mylist[2])
                self.helpMenu.addAction(act)
                self.actions_creation_dict["Help"][i][0] = act

        self.editMenu.aboutToShow.connect(self.update_edit_menu)

    def update_menus(self):
        active = self.currentNodeEditor()
        hasMdiChild = (active is not None)

        Switchs = {"File Menu": ["Save", "Save As"], "Edit Menu": ["Paste", "Select All"], "Node Editor Menu": ["Close", "Close All", "Tile", "Next", "Previous"]}
        for menu in Switchs:
            for act_name in Switchs[menu]:
                self.actions_creation_dict[menu][act_name][0].setEnabled(hasMdiChild)

        # Update Edit Menu
        self.update_edit_menu()

    def update_edit_menu(self):
        try:
            active = self.currentNodeEditor()
            hasMdiChild = (active is not None)

            self.actions_creation_dict["Edit Menu"]["Cut"][0].setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actions_creation_dict["Edit Menu"]["Copy"][0].setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actions_creation_dict["Edit Menu"]["Delete"][0].setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actions_creation_dict["Edit Menu"]["Undo"][0].setEnabled(hasMdiChild and active.canUndo())
            self.actions_creation_dict["Edit Menu"]["Redo"][0].setEnabled(hasMdiChild and active.canRedo())

        except Exception as e:
            dumpException(e)

    def update_window_menu(self):
        self.toolbar_library = self.library_menu.addAction("Libraries Window")
        self.toolbar_library.setCheckable(True)
        self.toolbar_library.triggered.connect(self.update_libraries_wnd)
        self.toolbar_library.setChecked(False)

        self.toolbar_properties = self.node_editor_menu.addAction("Properties Window")
        self.toolbar_properties.setCheckable(True)
        self.toolbar_properties.triggered.connect(self.update_properties_wnd)
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

        for i in self.actions_creation_dict["Node Editor Menu"]:
            if i.__contains__("addSeparator"):
                self.node_editor_menu.addSeparator()
            else:
                mylist = self.actions_creation_dict["Node Editor Menu"][i]
                act = QAction(mylist[3], parent=self, statusTip=mylist[1], triggered=mylist[2])
                self.node_editor_menu.addAction(act)
                self.actions_creation_dict["Node Editor Menu"][i][0] = act
        # self.node_editor_menu.addAction(self.actClose)
        # self.node_editor_menu.addAction(self.actCloseAll)
        # self.node_editor_menu.addSeparator()
        # self.node_editor_menu.addAction(self.actTile)
        # # self.windowMenu.addAction(self.actCascade)
        # self.node_editor_menu.addSeparator()
        # self.node_editor_menu.addAction(self.actNext)
        # self.node_editor_menu.addAction(self.actPrevious)
        # self.node_editor_menu.addAction(self.actSeparator)
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

    def update_properties_wnd(self):
        self.toolbar_properties.setChecked(self.toolbar_properties.isChecked())
        self.proprietiesDock.setVisible(self.toolbar_properties.isChecked())

    def update_libraries_wnd(self):
        self.toolbar_library.setChecked(self.toolbar_library.isChecked())
        self.librariesDock.setVisible(self.toolbar_library.isChecked())

    def update_files_wnd(self):
        self.toolbar_files.setChecked(self.toolbar_files.isChecked())
        self.filesDock.setVisible(self.toolbar_files.isChecked())

    def activate_editor_mode(self):
        if self.graphs_parent_wdg.subWindowList():
            self.switch_display(Editor=True)
        else:
            self.switch_display(Welcome=True)


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

    def activate_designer_mode(self):
        self.switch_display(Designer=True)

    def activate_library_mode(self):
        if self.graphs_parent_wdg.subWindowList():
            self.switch_display(Library=True)
        else:
            self.switch_display(Welcome=True)

        # Handel buttons State
        self.node_editor_menu.setEnabled(False)
        self.library_menu.setEnabled(True)

        self.toolbar_library.setChecked(True)
        self.librariesDock.setVisible(self.toolbar_library.isChecked())

        self.toolbar_files.setChecked(False)
        self.filesDock.setVisible(self.toolbar_files.isChecked())

    def create_functions_dock(self):
        self.functionsDock = QDockWidget("Functions")
        self.nodesListWidget = NodeList()

        self.functionsDock.setWidget(self.nodesListWidget)
        self.functionsDock.setFeatures(self.functionsDock.DockWidgetMovable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.functionsDock)

    def create_files_dock(self):
        self.brows_btn.clicked.connect(self.files_widget.set_project_folder)
        # self.files_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.filesDock = QDockWidget("Project Files")
        self.filesDock.setWidget(self.files_widget)
        self.filesDock.setFeatures(self.filesDock.DockWidgetMovable)
        self.addDockWidget(Qt.RightDockWidgetArea, self.filesDock)

    def create_properties_dock(self):
        self.proprietiesWdg = PropertiesList(master_ref=self)

        self.proprietiesDock = QDockWidget("Properties")
        self.proprietiesDock.setWidget(self.proprietiesWdg)
        self.proprietiesDock.setFeatures(self.proprietiesDock.DockWidgetMovable)

        self.addDockWidget(Qt.RightDockWidgetArea, self.proprietiesDock)

    def create_user_nodes_dock(self):
        self.varsEventsDock = QDockWidget("Variables & Events")
        self.VEStackedWdg = QStackedWidget()

        self.VEStackedWdg.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.varsEventsDock.setWidget(self.VEStackedWdg)
        self.varsEventsDock.setFeatures(self.varsEventsDock.DockWidgetMovable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.varsEventsDock)

    def delete_user_nodes_wgd(self, ref):
        self.VEStackedWdg.removeWidget(ref)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def before_window_close(self):
        self.proprietiesWdg.clear_properties()

    def on_before_save_file(self):
        self.proprietiesWdg.clear_properties()

    def new_graph_tab(self):
        # This Check Prevents The Parent graph from opening in Cascade view-mode
        if not self.graphs_parent_wdg.subWindowList():
            self.switch_display(Editor=True)

        node_editor = NodeEditorTab(masterRef=self)

        VEL = UserNodesList(scene=node_editor.scene, propertiesWdg=self.proprietiesWdg)
        self.VEStackedWdg.addWidget(VEL)
        self.VEStackedWdg.setCurrentWidget(VEL)

        node_editor.scene.user_nodes_wdg = VEL

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
        existing = self.findMdiChild(widget.filename)
        self.graphs_parent_wdg.setActiveSubWindow(existing)

        if self.ask_save():
            event.accept()
            self.delete_user_nodes_wgd(widget.scene.user_nodes_wdg)
            if (len(self.graphs_parent_wdg.subWindowList())-1) == 0:
                self.switch_display(Welcome=True)
            else:
                self.switch_display(Editor=True)
            self.before_window_close()
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

    def get_QWidget_content(self, widget):
        if [QKeySequenceEdit].__contains__(type(widget)):
            return widget.keySequence().toString()
        elif [QSpinBox, QDoubleSpinBox].__contains__(type(widget)):
            return widget.value()
        elif [QLineEdit, QLabel].__contains__(type(widget)):
            return widget.text()
        elif [QTextEdit].__contains__(type(widget)):
            return widget.toPlainText()
        elif [QRadioButton, QCheckBox].__contains__(type(widget)):
            return widget.isChecked()
        elif [QComboBox].__contains__(type(widget)):
            current = widget.currentText()
            widget.removeItem(widget.currentIndex())
            content_list = [current]
            for index in range(widget.__len__()):
                content_list.append(widget.itemText(index))
            widget.clear()
            widget.addItems(content_list)
            return content_list
        else:
            print(widget, "Widget Not Supported << Get")
            return None

    def set_QWidget_content(self, widget, new_value):
        if [QKeySequenceEdit].__contains__(type(widget)):
            widget.setKeySequence(new_value)
        elif [QSpinBox, QDoubleSpinBox].__contains__(type(widget)):
            widget.setValue(new_value)
        elif [QLineEdit, QLabel, QTextEdit].__contains__(type(widget)):
            widget.setText(new_value)
        elif [QRadioButton, QCheckBox].__contains__(type(widget)):
            widget.setChecked(new_value)
        elif [QComboBox].__contains__(type(widget)):
            widget.clear()
            widget.addItems(new_value)
        else:
            print(widget, "Widget Not Supported << Set")

    def about(self):
        QMessageBox.about(self, "About Calculator NodeEditor Example",
                          "The <b>Calculator NodeEditor</b> example demonstrates how to write multiple "
                          "document interface applications using PyQt5 and NodeEditor. For more information visit: "
                          "<a href='https://www.blenderfreak.com/'>www.BlenderFreak.com</a>")
