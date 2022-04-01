from examples.example_calculator.master_window import *


class FilesWDG(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterWmdRef = None
        self.Project_Directory = ""

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.Model = QFileSystemModel()
        self.Model.setRootPath("")

        self.tree_wdg = QTreeView()
        self.tree_wdg.setModel(self.Model)
        self.tree_wdg.setSortingEnabled(True)
        self.tree_wdg.setColumnWidth(0, 130)
        self.tree_wdg.sortByColumn(0, Qt.AscendingOrder)
        self.tree_wdg.hideColumn(1)
        self.tree_wdg.hideColumn(2)
        self.tree_wdg.setStyleSheet("color: white")
        layout.addWidget(self.tree_wdg)

        self.CreateDefaultDir()

    def CreateDefaultDir(self):
        defaultDir = os.getenv('AppData') + "\VVS"
        if os.path.exists(defaultDir):
            Dir = defaultDir
        else:
            os.makedirs(os.getenv('AppData') + "\VVS")
            Dir = defaultDir

        self.Project_Directory = Dir
        self.tree_wdg.setRootIndex(self.Model.index(self.Project_Directory))

    def onSetProjectFolder(self):
        Dir = QFileDialog.getExistingDirectory(self, "Set Project Location")
        if Dir != "":
            x = False
            DirCont = os.listdir(Dir)
            if DirCont != []:
                for i in DirCont:
                    if os.path.isdir(Dir + "/" + i):
                        x = True
                if x:
                    Q = QMessageBox.question(self, "Warning",
                                             "Project Folder Isn't Empty\n\n- Do You Still Want To Use It?",
                                             QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
                    if Q == QMessageBox.Yes:
                        self.Project_Directory = Dir
                        self.tree_wdg.setRootIndex(self.Model.index(self.Project_Directory))
                    elif Q == QMessageBox.No:
                        self.onSetProjectFolder()
                    elif Q == QMessageBox.Cancel:
                        QMessageBox.about(self, "Note", f"""Your Data is Being Saved in\n\n {self.Project_Directory}""")
                else:
                    self.Project_Directory = Dir
                    self.tree_wdg.setRootIndex(self.Model.index(self.Project_Directory))
        else:
            QMessageBox.about(self, "Note", f"""Your Data is Being Saved By Default in\n\n {self.Project_Directory}""")

    def MakeDir(self, Name):
        os.makedirs(self.Project_Directory + "/" + Name)
        os.makedirs(self.Project_Directory + "/" + Name + "/" + "AutoSave")

    def CreateNewGraph(self, subwnd):
        # Auto rename new graph
        x = 0
        newName = "New Graph"
        while self.masterWmdRef.graphsNames.__contains__(newName):
            x += 1
            newName = f"New Graph {x}"
        else:
            self.masterWmdRef.graphsNames.append(newName)
            subwnd.setWindowTitle(newName)

        # Create Graph directory
        Folder_List = os.listdir(self.Project_Directory)
        if Folder_List.__contains__(subwnd.windowTitle()) is False:
            self.MakeDir(str(subwnd.windowTitle()))
