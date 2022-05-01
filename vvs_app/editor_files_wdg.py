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
        self.tree_wdg.setStyleSheet("color: white")
        layout.addWidget(self.tree_wdg)

        self.tree_wdg.clicked.connect(self.OpenSelectedFiles)

        self.CreateDefaultDir()

    def OpenSelectedFiles(self):
        all_files = []

        selected_files = self.tree_wdg.selectedIndexes()

        for file_name in selected_files:
            file_path = QFileSystemModel().filePath(file_name)

            if file_path.endswith(".json"):
                if not all_files.__contains__(file_path):
                    all_files.append(file_path)
                    # print(all_files)

        self.masterRef.onFileOpen(all_files)

    def CreateDefaultDir(self):

        self.Project_Directory = f"C:/Users/{os.getlogin()}/AppData/Roaming/VVS"
        if os.path.exists(self.Project_Directory) is False:
            self.Project_Directory = f"C:/Users/{os.getlogin()}/AppData/Roaming/VVS"

        self.tree_wdg.setRootIndex(self.Model.index(self.Project_Directory))
        self.MakeDir(self.Project_Directory)

    def onSetProjectFolder(self):
        Dir = QFileDialog.getExistingDirectory(self, "Set Project Location")
        if Dir != "":
            self.Project_Directory = Dir
            self.tree_wdg.setRootIndex(self.Model.index(self.Project_Directory))
            self.MakeDir(self.Project_Directory)

    def MakeDir(self, Dir):
        if os.listdir(self.Project_Directory).__contains__("VVS AutoSave") is False:
            os.makedirs(Dir + "/VVS AutoSave")

    def removeDeletedGraphs(self):
        wndsN = []
        wnds = self.masterRef.graphs_parent_wdg.subWindowList()
        if wnds != []:
            for wnd in wnds:
                Y = [int(s) for s in wnd.windowTitle().split() if s.isdigit()]
                wndsN.append(f"New Graph {Y[0] if Y else 1}")

        list2 = [i for i in wndsN + self.masterRef.graphsNames if
                 i not in wndsN or i not in self.masterRef.graphsNames]  # this is the difference between the two lists

        if list2 != []:
            for li in list2:
                if self.masterRef.graphsNames.__contains__(li):
                    self.masterRef.graphsNames.remove(li)

    def new_graph_name(self, subwnd):
        x = 1
        newName = f"New Graph {x}"
        while self.masterRef.graphsNames.__contains__(newName):
            x += 1
            newName = f"New Graph {x}"
        else:
            self.masterRef.graphsNames.append(newName)
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

        if FolderContentSizeInGBs >= self.masterRef.GlobalSwitches.switches_Dict["AutoSave Folder Max Size"]:
            ToDelete = dirContentList[0:len(dirContentList)//2]
            for file in ToDelete:
                file = os.path.join(AutoSaveDir, file)
                os.remove(file)
