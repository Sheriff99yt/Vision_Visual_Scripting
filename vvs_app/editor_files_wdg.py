from vvs_app.master_window import *


class FilesWDG(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterRef = None

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.Model = QFileSystemModel()
        self.Model.setRootPath("")

        self.tree_wdg = QTreeView()
        self.tree_wdg.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tree_wdg.setModel(self.Model)
        self.tree_wdg.setSortingEnabled(True)
        self.tree_wdg.setColumnWidth(0, 130)
        self.tree_wdg.sortByColumn(0, Qt.AscendingOrder)
        self.tree_wdg.hideColumn(1)
        self.tree_wdg.hideColumn(2)
        layout.addWidget(self.tree_wdg)

        self.tree_wdg.clicked.connect(self.OpenSelectedFiles)
        self.tree_wdg.contextMenuEvent = self.tree_wdg_contextMenuEvent
        self.CreateDefaultDir()

    def tree_wdg_contextMenuEvent(self, event):
        context_menu = QMenu(self)
        delete = context_menu.addAction("Delete")
        context_menu.addAction("Cancel")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        if action == delete:
            file_path = QFileSystemModel().filePath(self.tree_wdg.selectedIndexes()[0])
            delete_Q = QMessageBox.warning(self, "Warning !", f"You Are About To Delete\n\n{file_path}\n\nThis is Irreversible Are You Sure?", QMessageBox.Save | QMessageBox.Cancel)
            if delete_Q == QMessageBox.Save:
                try:
                    os.remove(file_path)
                except Exception:
                    warning = QMessageBox(QMessageBox.Warning, "Permissions Error",
                                       "You Don't have Permissions To Delete a Directory", QMessageBox.Ok)
                    warning.exec_()


    def OpenSelectedFiles(self):
        all_files = []

        selected_files = self.tree_wdg.selectedIndexes()

        for file_name in selected_files:
            file_path = QFileSystemModel().filePath(file_name)

            if file_path.endswith(".json"):
                if not all_files.__contains__(file_path):
                    all_files.append(file_path)
                    # print(all_files)

        self.masterRef.on_file_open(all_files)

    def CreateDefaultDir(self):

        self.Project_Directory = f"C:/Users/{os.getlogin()}/AppData/Roaming/VVS"
        if os.path.exists(self.Project_Directory) is False:
            self.Project_Directory = f"C:/Users/{os.getlogin()}/AppData/Roaming/VVS"

        self.tree_wdg.setRootIndex(self.Model.index(self.Project_Directory))
        self.MakeDir(self.Project_Directory)

    def on_open_folder(self):
        Dir = QFileDialog.getExistingDirectory(self, "Set Project Location")
        if Dir != "":
            self.Project_Directory = Dir
            self.tree_wdg.setRootIndex(self.Model.index(self.Project_Directory))
            self.MakeDir(self.Project_Directory)

    def MakeDir(self, Dir):
        if os.listdir(self.Project_Directory).__contains__("VVS AutoSave") is False:
            os.makedirs(Dir + "/VVS AutoSave")

    def new_graph_name(self, subwnd, all_names):
        x = 1
        names = []
        for item in all_names:
            item = item.replace("*", "")
            names.append(item)

        newName = f"New Graph {x}"
        while names.__contains__(newName):
            x += 1
            newName = f"New Graph {x}"
        else:
            subwnd.setWindowTitle(newName)
            subwnd.widget().setWindowTitle(newName)

    def deleteOldAutoSaves(self):
        AutoSaveDir = self.Project_Directory + "/VVS AutoSave"
        dirContentList = os.listdir(AutoSaveDir)

        FolderContentSize = 0
        for file in dirContentList:
            file = os.path.join(AutoSaveDir, file)
            FolderContentSize += os.stat(file).st_size

        FolderContentSizeInGBs = FolderContentSize/(1000 * 1000 * 1000)

        if FolderContentSizeInGBs >= self.masterRef.global_switches.switches_Dict["AutoSave Folder MaxSize"]:
            self.msg = QMessageBox()
            self.msg.setText(f"AutoSave Folder Has Exceeded the Set Limit of {FolderContentSizeInGBs} Gigabytes")
            self.msg.show()
            # self.masterRef.statusBar().showMessage(f"""AutoSave Folder Has Exceeded the Set Limit of {FolderContentSizeInGBs} Gigabytes""")
