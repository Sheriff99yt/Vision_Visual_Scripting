# -*- coding: utf-8 -*-
"""
A module containing the Main Window class
"""
import os, json
from qtpy.QtCore import *
from qtpy.QtWidgets import *
# from nodeeditor.node_editor_widget import NodeEditorWidget
from nodeeditor.node_editor_widget import NodeEditorWidget
from datetime import datetime


class NodeEditorWindow(QMainWindow):
    NodeEditorWidget_class = NodeEditorWidget

    """Class representing NodeEditor's Main Window"""
    def __init__(self):

        """
        :Instance Attributes:

        - **name_company** - name of the company, used for permanent profile settings
        - **name_product** - name of this App, used for permanent profile settings
        """
        super().__init__()

        self.name_company = 'The Team'
        self.name_product = 'Vision Visual Scripting'
        self.initUI()


    def initUI(self):

        """Set up this ``QMainWindow``. Create :class:`~nodeeditor.node_editor_widget.NodeEditorWidget`, Actions and Menus"""
        self.createActions()
        self.create_menus()

        # create node editor widget

        self.central_window = self.__class__.NodeEditorWidget_class(self)
        self.central_window.scene.addHasBeenModifiedListener(self.setTitle)
        self.setCentralWidget(self.central_window)


        self.createStatusBar()

        # set window properties
        # self.setGeometry(200, 200, 800, 600)
        self.setTitle()
        self.show()


    def sizeHint(self):
        return QSize(800, 600)

    def createStatusBar(self):

        """Create Status bar and connect to `Graphics View` scenePosChanged event"""
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        # self.nodeeditor.GraphView.scenePosChanged.connect(self.onScenePosChanged)

    def createActions(self):
        """Create basic `File` and `Edit` actions"""
        self.actNew = QAction('&New Graph', self, shortcut=self.global_switches.switches_Dict["New Graph"], statusTip="Create new graph", triggered=self.on_new_graph_tab)
        self.actOpen = QAction('&Open', self, shortcut=self.global_switches.switches_Dict["Open"], statusTip="Open file", triggered=self.on_file_open)
        self.actSetProjectDir = QAction('&Open Project', self, shortcut=self.global_switches.switches_Dict["Set Project Location"], statusTip="Set a Folder For Your Project", triggered=self.filesWidget.on_open_folder)
        self.actSave = QAction('&Save', self, shortcut=self.global_switches.switches_Dict["Save"], statusTip="Save file", triggered=self.onFileSave)
        self.actSaveAs = QAction('Save &As...', self, shortcut=self.global_switches.switches_Dict["Save As"], statusTip="Save file as...", triggered=self.on_file_save_as)
        self.actExit = QAction('E&xit', self, shortcut=self.global_switches.switches_Dict["Exit"], statusTip="Exit application", triggered=self.close)
        self.actUndo = QAction('&Undo', self, shortcut=self.global_switches.switches_Dict["Undo"], statusTip="Undo last operation", triggered=self.onEditUndo)
        self.actRedo = QAction('&Redo', shortcut=self.global_switches.switches_Dict["Redo"], statusTip="Redo last operation", triggered=self.onEditRedo)
        self.actCut = QAction('Cu&t', shortcut=self.global_switches.switches_Dict["Cut"], statusTip="Cut to clipboard", triggered=self.onEditCut)
        self.actCopy = QAction('&Copy', shortcut=self.global_switches.switches_Dict["Copy"], statusTip="Copy to clipboard", triggered=self.onEditCopy)
        self.actPaste = QAction('&Paste', shortcut=self.global_switches.switches_Dict["Paste"], statusTip="Paste from clipboard", triggered=self.onEditPaste)
        self.actDelete = QAction('&Delete', shortcut=self.global_switches.switches_Dict["Delete"], statusTip="Delete selected items", triggered=self.onEditDelete)

    def create_menus(self):
        """Create Menus for `File` and `Edit`"""
        self.createFileMenu()
        self.createEditMenu()

    def createFileMenu(self):
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&File')
        self.fileMenu.addAction(self.actNew)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actOpen)
        self.fileMenu.addAction(self.actSetProjectDir)
        self.fileMenu.addAction(self.actSave)
        self.fileMenu.addAction(self.actSaveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actExit)

    def createEditMenu(self):
        menubar = self.menuBar()
        self.editMenu = menubar.addMenu('&Edit')
        self.editMenu.addAction(self.actUndo)
        self.editMenu.addAction(self.actRedo)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actCut)
        self.editMenu.addAction(self.actCopy)
        self.editMenu.addAction(self.actPaste)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actDelete)

    def setTitle(self):
        """Function responsible for setting window title"""
        title = "Node Editor - "
        title += self.currentNodeEditor().getUserFriendlyFilename()

        self.setWindowTitle(title)


    def closeEvent(self, event):
        """Handle close event. Ask before we loose work"""
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def isModified(self) -> bool:
        """Has current :class:`~nodeeditor.node_scene.Scene` been modified?

        :return: ``True`` if current :class:`~nodeeditor.node_scene.Scene` has been modified
        :rtype: ``bool``
        """
        nodeeditor = self.currentNodeEditor()
        return nodeeditor.scene.isModified() if nodeeditor else False

    def currentNodeEditor(self) -> NodeEditorWidget:
        """get current :class:`~nodeeditor.node_editor_widget`

        :return: get current :class:`~nodeeditor.node_editor_widget`
        :rtype: :class:`~nodeeditor.node_editor_widget`
        """
        return self.centralWidget()

    def maybeSave(self) -> bool:
        """If current `Scene` is modified, ask a dialog to save the changes. Used before
        closing window / mdi child document

        :return: ``True`` if we can continue in the `Close Event` and shutdown. ``False`` if we should cancel
        :rtype: ``bool``
        """
        if not self.isModified():
            return True

        res = QMessageBox.warning(self, "About to loose your work?",
                "The document has been modified.\n Do you want to save your changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
              )

        if res == QMessageBox.Save:
            return self.onFileSave()
        elif res == QMessageBox.Cancel:
            return False

        return True


    def onScenePosChanged(self, x:int, y:int):
        """Handle event when cursor position changed on the `Scene`

        :param x: new cursor x position
        :type x:
        :param y: new cursor y position
        :type y:
        """
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    def getFileDialogDirectory(self):
        """Returns starting directory for ``QFileDialog`` file open/save"""
        return ''

    def getFileDialogFilter(self):
        """Returns ``str`` standard file open/save filter for ``QFileDialog``"""
        return 'Graph (*.json);;All files (*)'

    # def onNewGraphTab(self):
    #     # This is overridden by Master Window Function
    #     """Hande New Graph operation"""
    #     print("No Waaaayyyyy")
    #     if self.maybeSave():
    #         self.CurrentNodeEditor().setup_new_graph()
    #         self.setTitle()

    def on_file_open(self):
        """Handle File Open operation"""
        if self.maybeSave():
            fname, filter = QFileDialog.getOpenFileName(self, 'Open graph from file', self.getFileDialogDirectory(), self.getFileDialogFilter())
            if fname != '' and os.path.isfile(fname):
                self.currentNodeEditor().fileLoad(fname)
                self.setTitle()

    def onFileSave(self):
        """Handle File Save operation"""
        current_node_editor = self.currentNodeEditor()
        if current_node_editor is not None:
            if not current_node_editor.isFilenameSet(): return self.on_file_save_as()
            current_node_editor.fileSave()
            self.statusBar().showMessage("Successfully saved %s" % current_node_editor.filename, 5000)

            # support for MDI app
            if hasattr(current_node_editor, "setTitle"): current_node_editor.setTitle()
            else: self.setTitle()
            return True

    def onFileAutoSave(self):
        current_node_editor = self.currentNodeEditor()
        if current_node_editor is not None:
            Now = str(datetime.now()).replace(":", ".")[0:19]
            fname = f"""{self.filesWidget.Project_Directory}/VVS AutoSave/{(current_node_editor.windowTitle()).replace("*","")} {Now}.json"""
            self.onBeforeSaveAs(current_node_editor, fname)
            current_node_editor.fileAutoSave(fname)
            self.filesWidget.deleteOldAutoSaves()
            self.statusBar().showMessage("Successfully Auto Saved %s" % fname , 5000)

            # support for MDI app
            if hasattr(current_node_editor, "setTitle"):
                current_node_editor.setTitle()
            else:
                self.setTitle()
            return True

    def on_file_save_as(self):
        """Handle File Save As operation"""
        current_node_editor = self.currentNodeEditor()
        if current_node_editor is not None:
            fname, filter = QFileDialog.getSaveFileName(self, 'Save graph to file', f"""{self.filesWidget.Project_Directory}/{self.currentNodeEditor().windowTitle().replace("*", "")}""", self.getFileDialogFilter())
            if fname == '': return False

            self.onBeforeSaveAs(current_node_editor, fname)
            current_node_editor.fileSave(fname)
            current_node_editor.setWindowTitle(os.path.splitext(os.path.basename(current_node_editor.filename))[0])
            self.statusBar().showMessage("Successfully saved as %s" % current_node_editor.filename, 5000)

            # support for MDI app
            if hasattr(current_node_editor, "setTitle"):
                current_node_editor.setTitle()
            else:
                self.setTitle()
            return True

    def onBeforeSaveAs(self, current_nodeeditor: 'NodeEditorWidget', filename: str):
        """
        Event triggered after choosing filename and before actual fileSave(). We are passing current_nodeeditor because
        we will loose focus after asking with QFileDialog and therefore getCurrentNodeEditorWidget will return None
        """
        pass

    def onEditUndo(self):
        """Handle Edit Undo operation"""
        if self.currentNodeEditor():
            self.currentNodeEditor().scene.history.undo()

    def onEditRedo(self):
        """Handle Edit Redo operation"""
        if self.currentNodeEditor():
            self.currentNodeEditor().scene.history.redo()

    def onEditDelete(self):
        """Handle Delete Selected operation"""
        if self.currentNodeEditor():
            self.currentNodeEditor().scene.getView().deleteSelected()

    def onEditCut(self):
        """Handle Edit Cut to clipboard operation"""
        if self.currentNodeEditor():
            data = self.currentNodeEditor().scene.clipboard.serializeSelected(delete=True)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        """Handle Edit Copy to clipboard operation"""
        if self.currentNodeEditor():
            data = self.currentNodeEditor().scene.clipboard.serializeSelected(delete=False)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        """Handle Edit Paste from clipboard operation"""
        if self.currentNodeEditor():
            raw_data = QApplication.instance().clipboard().text()

            try:
                data = json.loads(raw_data)
            except ValueError as e:
                print("Pasting of not valid json data!", e)
                return

            # check if the json data are correct
            if 'nodes' not in data:
                print("JSON does not contain any nodes!")
                return
            self.currentNodeEditor().scene.clipboard.deserializeFromClipboard(data)

    def readSettings(self):
        """Read the permanent profile settings for this app"""
        settings = QSettings(self.name_company, self.name_product)
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(600, 1200))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        """Write the permanent profile settings for this app"""
        settings = QSettings(self.name_company, self.name_product)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())
