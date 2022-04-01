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

        self.tree_wdg.doubleClicked.connect(self.onDoubleClicked)

        self.CreateDefaultDir()

    def onDoubleClicked(self):
        if self.Project_Directory.__contains__(self.tree_wdg.currentIndex().parent().data()):
            fname = f"""{self.Project_Directory}/{self.tree_wdg.currentIndex().data()}"""
        else:
            fname = f"""{self.Project_Directory}/{self.tree_wdg.currentIndex().parent().data()}/{self.tree_wdg.currentIndex().data()}"""

        if fname[-5] == ".":
            if self.masterWmdRef.findMdiChild(fname):
                subwnd = self.masterWmdRef.findMdiChild(fname)
                nodeEditor = subwnd.widget()
                VEL = self.masterWmdRef.CreateNewVEList()
                nodeEditor.scene.VEListWdg = VEL
                VEL.Scene = nodeEditor.scene
                self.masterWmdRef.all_graphs.append(nodeEditor)
                self.masterWmdRef.graphs_parent_wdg.setActiveSubWindow(subwnd)
            else:
                # we need to create new subWindow and open the file
                nodeEditor = MasterEditorWnd()
                subwnd = self.masterWmdRef.newGraphTab(nodeEditor)

                nodeEditor.scene.masterRef = self.masterWmdRef
                nodeEditor.scene.history.masterWndRef = self.masterWmdRef
                # self.masterWmdRef.CodeWndSettingBtn.triggered.connect(nodeEditor.setCodeWndViewMode)

                if nodeEditor.fileLoad(fname):
                    self.masterWmdRef.statusBar().showMessage("File %s loaded" % fname, 5000)
                    nodeEditor.setWindowTitle(os.path.splitext(os.path.basename(fname))[0])
                    subwnd.show()
                else:
                    nodeEditor.close()
        else:
            msg = QMessageBox()
            msg.setText("File Format Isn't Supported!")
            msg.setWindowTitle("Incompatible File")
            msg.setStyleSheet("background-color: #282828; color: rgb(255, 255, 255);")
            msg.exec_()

    def CreateDefaultDir(self):
        defaultDir = os.getenv('AppData') + "/VVS"
        if os.path.exists(defaultDir):
            Dir = defaultDir
        else:
            os.makedirs(os.getenv('AppData') + "/VVS")
            Dir = defaultDir

        self.Project_Directory = Dir
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
        wnds = self.masterWmdRef.graphs_parent_wdg.subWindowList()
        if wnds != []:
            for wnd in wnds:
                Y = [int(s) for s in wnd.windowTitle().split() if s.isdigit()]
                wndsN.append(f"New Graph {Y[0] if Y else 1}")

        list2 = [i for i in wndsN + self.masterWmdRef.graphsNames if
                 i not in wndsN or i not in self.masterWmdRef.graphsNames]  # this is the difference between the two lists

        if list2 != []:
            for li in list2:
                if self.masterWmdRef.graphsNames.__contains__(li):
                    self.masterWmdRef.graphsNames.remove(li)

    def CreateNewGraph(self, subwnd):
        x = 1
        newName = f"New Graph {x}"
        while self.masterWmdRef.graphsNames.__contains__(newName):
            x += 1
            newName = f"New Graph {x}"
        else:
            self.masterWmdRef.graphsNames.append(newName)
            subwnd.setWindowTitle(newName)
            subwnd.widget().setWindowTitle(newName)
