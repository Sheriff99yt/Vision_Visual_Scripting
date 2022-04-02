from examples.example_calculator.master_window import *


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
        if os.path.exists(self.Project_Directory):
            pass
        else:
            self.Project_Directory = os.makedirs(os.getenv('AppData') + "/VVS")

        self.tree_wdg.setRootIndex(self.Model.index(self.Project_Directory))
        self.MakeDir(self.Project_Directory)

    def onSetProjectFolder(self):
        Dir = QFileDialog.getExistingDirectory(self, "Set Project Location")
        if Dir != "":
            DirCont = os.listdir(Dir)
            if DirCont != []:
                Q = QMessageBox.question(self, "Warning",
                                         "Project Folder Isn't Empty\n\n- Do You Still Want To Use It?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
                if Q == QMessageBox.Yes:
                    self.Project_Directory = Dir
                    self.tree_wdg.setRootIndex(self.Model.index(self.Project_Directory))
                    self.MakeDir(self.Project_Directory)
                elif Q == QMessageBox.No:
                    self.onSetProjectFolder()
                elif Q == QMessageBox.Cancel:
                    QMessageBox.about(self, "Note", f"""Your Data is Being Saved in\n\n {self.Project_Directory}""")
            else:
                self.Project_Directory = Dir
                self.tree_wdg.setRootIndex(self.Model.index(self.Project_Directory))
                self.MakeDir(self.Project_Directory)
        else:
            QMessageBox.about(self, "Note", f"""Your Data is Being Saved By Default in\n\n {self.Project_Directory}""")

    def MakeDir(self, Dir):
        if os.listdir(self.Project_Directory).__contains__("AutoSave") is False:
            os.makedirs(Dir + "/AutoSave")

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

    def CreateNewGraph(self, subwnd):
        x = 1
        newName = f"New Graph {x}"
        while self.masterRef.graphsNames.__contains__(newName):
            x += 1
            newName = f"New Graph {x}"
        else:
            self.masterRef.graphsNames.append(newName)
            subwnd.setWindowTitle(newName)
            subwnd.widget().setWindowTitle(newName)
