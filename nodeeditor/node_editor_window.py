# -*- coding: utf-8 -*-
"""
A module containing the Main Window class
"""
import os, json

from PyQt6.QtGui import QImage
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from nodeeditor.node_editor_widget import NodeEditorWidget
from datetime import datetime

from vvs_app.editor_files_wdg import FilesWDG
from vvs_app.global_switches import GlobalSwitches
from vvs_app.master_node import MasterNode
from vvs_app.nodes.nodes_configuration import *


class NodeEditorWindow(QMainWindow):

    """Class representing NodeEditor's Main Window"""
    def __init__(self):
        """
        :Instance Attributes:

        - **name_company** - name of the company, used for permanent profile settings
        - **name_product** - name of this App, used for permanent profile settings
        """
        super().__init__()

        self.files_widget = FilesWDG(self)

        self.name_company = 'The Team'
        self.name_product = 'Vision Visual Scripting'

        self.global_switches = GlobalSwitches(master=self)

        for cls in MasterNode.__subclasses__():
            register_Node(cls)

        self.set_nodes_icons()


    def set_nodes_icons(self):
        for cls in MasterNode.__subclasses__():
            icon = os.path.split(cls.icon)[-1]
            cls.icon = self.global_switches.get_icon(icon)

    def sizeHint(self):
        return QSize(800, 600)

    def createStatusBar(self):

        """Create Status bar and connect to `Graphics View` scenePosChanged event"""
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)

    def create_menus(self):
        """Create Menus for `File` and `Edit`"""
        self.createFileMenu()
        self.createEditMenu()

    def createFileMenu(self):
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&File')
        for i in self.actions_creation_dict["File Menu"]:
            if i.__contains__("addSeparator"):
                self.fileMenu.addSeparator()
            else:
                mylist = self.actions_creation_dict["File Menu"][i]
                act = QAction(mylist[3], parent=self, statusTip=mylist[1], triggered=mylist[2])
                self.fileMenu.addAction(act)
                self.actions_creation_dict["File Menu"][i][0] = act

    def createEditMenu(self):
        menubar = self.menuBar()
        self.editMenu = menubar.addMenu('&Edit')
        for i in self.actions_creation_dict["Edit Menu"]:
            if i.__contains__("addSeparator"):
                self.editMenu.addSeparator()
            else:
                mylist = self.actions_creation_dict["Edit Menu"][i]
                act = QAction(mylist[3], parent=self, statusTip=mylist[1], triggered=mylist[2])
                self.editMenu.addAction(act)
                self.actions_creation_dict["Edit Menu"][i][0] = act

    def selectAllNodes(self):
        return self.currentNodeEditor().select_all_nodes()

    def setTitle(self):
        """Function responsible for setting window title"""
        title = "Node Editor - "
        title += self.currentNodeEditor().getUserFriendlyFilename()

        self.setWindowTitle(title)

    def closeEvent(self, event):
        """Handle close event. Ask before we loose work"""
        if self.ask_save():
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

    def ask_save(self) -> bool:
        """If current `Scene` is modified, ask a dialog to save the changes. Used before
        closing window / mdi child document

        :return: ``True`` if we can continue in the `Close Event` and shutdown. ``False`` if we should cancel
        :rtype: ``bool``
        """
        if not self.isModified():
            return True
        elif self.global_switches.switches_Dict["System"]["Always Save Before Closing"]:
            if self.onFileSave():
                return True
            else:
                return self.save_message()

        elif self.global_switches.switches_Dict["System"]["Save New Project Folder On Close"]:
            return self.save_unsaved_files()

        else:
            return self.save_message()

    def save_message(self, new_dir=False):
        if new_dir:
            msg = "The Folder has not been Set.\n Do you want to save your changes?"
        else:
            msg = "The document has been modified.\n Do you want to save your changes?"

        res = QMessageBox.warning(self, "About to loose your work?", msg,
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)


        if res == QMessageBox.Save:
            if new_dir:
                return self.files_widget.set_project_folder()
            else:
                return self.onFileSave()

        elif res == QMessageBox.Cancel:
            return False

        elif res == QMessageBox.Discard:
            return True

    def onScenePosChanged(self, x: int, y: int):
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

    def on_file_open(self):
        """Handle File Open operation"""
        if self.ask_save():
            fname, filter = QFileDialog.getOpenFileName(self, 'Open graph from file', self.getFileDialogDirectory(),
                                                        self.getFileDialogFilter())
            if fname != '' and os.path.isfile(fname):
                self.currentNodeEditor().fileLoad(fname)
                self.setTitle()

    def onFileSave(self):
        """Handle File Save operation"""
        # This Function Overrides the File With the same name
        # Check If a file Already Exists with the same name
        current_node_editor = self.currentNodeEditor()
        if current_node_editor is not None:
            if not current_node_editor.isFilenameSet():
                return self.on_file_save_as()
            current_node_editor.fileSave()
            self.statusBar().showMessage("Successfully saved %s" % current_node_editor.filename, 5000)

            # support for MDI app
            if hasattr(current_node_editor, "setTitle"): current_node_editor.setTitle()
            else: self.setTitle()
            return True

    def save_unsaved_files(self):
        current_node_editor = self.currentNodeEditor()
        if current_node_editor is not None:
            must_change = self.files_widget.Project_Directory == self.files_widget.default_system_dir

            if must_change:
                new = self.files_widget.set_project_folder()
                if new:
                    return current_node_editor.fileSave(
                        f'{self.files_widget.Project_Directory}/{current_node_editor.windowTitle().replace("*", "")}.json')
                else:
                    return self.save_message(new_dir=True)
            else:
                return current_node_editor.fileSave(
                    f'{self.files_widget.Project_Directory}/{current_node_editor.windowTitle().replace("*", "")}.json')


    def onFileAutoSave(self):
        current_node_editor = self.currentNodeEditor()
        if current_node_editor is not None:
            Now = str(datetime.now()).replace(":", ".")[0:19]
            fname = f"""{self.files_widget.Project_Directory}/VVS Auto Backup/{(current_node_editor.windowTitle()).replace("*", "")} {Now}.json"""
            self.onBeforeSaveAs(current_node_editor, fname)
            current_node_editor.fileAutoSave(fname)
            self.files_widget.size_limit_warning()
            self.statusBar().showMessage("Successfully Auto Saved %s" % fname, 5000)

            # # support for MDI app
            # if hasattr(current_node_editor, "setTitle"):
            #     current_node_editor.setTitle()
            # else:
            #     self.setTitle()

            return True

    def on_file_save_as(self):
        """Handle File Save As operation"""
        current_node_editor = self.currentNodeEditor()
        if current_node_editor is not None:
            fname, filter = QFileDialog.getSaveFileName(self, 'Save graph to file', f"""{self.files_widget.Project_Directory}/{self.currentNodeEditor().windowTitle().replace("*", "")}""", self.getFileDialogFilter())
            if fname == '':return False

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

    def before_window_close(self):
        pass
