# -*- coding: utf-8 -*-
"""
A module containing ``NodeEditorWidget`` class
"""
import os
import subprocess

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from nodeeditor.graph_graphics import GraphGraphics
from nodeeditor.node_edge import Edge, EDGE_TYPE_BEZIER
from nodeeditor.node_node import Node
from nodeeditor.node_scene import NodeScene, InvalidFile
from nodeeditor.utils import dumpException
from vvs_app.nodes.default_functions import Print
from vvs_app.nodes.event_nodes import UserFunction
from vvs_app.nodes.variables_nodes import FloatVar, IntegerVar, BooleanVar
from vvs_app.nodes.variables_nodes import StringVar, ListVar


class NodeEditorWidget(QWidget):
    """The ``NodeEditorWidget`` class"""

    def __init__(self, masterRef, parent: QWidget = None):
        """
        :param parent: parent widget
        :type parent: ``QWidget``

        :Instance Attributes:

        - **filename** - currently graph's filename or ``None``
        """
        super().__init__(parent)
        self.filename = None
        self.file_path = ''

        self.files_extensions = {'Python': '.py',
                              'C++': '.CPP',
                              'Rust': '.rs'}

        self.return_dataTypes_dict = {
                                    "Languages": ["Python", "C++"],
                                    "mutable": ["", "void"],
                                    "float": ["-> float", "float"],
                                    "integer": ["-> integer", "int"],
                                    "boolean": ["-> boolean", "boolean"],
                                    "string": ["-> string", "string"],
                                    "list": ["-> list", "list"],
                                    "dictionary": ["-> dictionary", "dictionary"],
                                    "tuple": ["-> tuple", "tuple"]
                                      }


        # crate graphics scene
        self.scene = NodeScene(masterRef, nodeeditor=self)

        self.create_widget_window()

    def get_node_return(self, syntax, node_return):
        index = self.return_dataTypes_dict["Languages"].index(syntax)
        return self.return_dataTypes_dict[node_return][index]

    def create_widget_window(self):
        """
        Set up this ``NodeEditorWidget`` with its layout,  :class:`~nodeeditor.node_scene.Scene` and
        :class:`~nodeeditor.node_graphics_view.QDMGraphicsView`
        """


        # create graphics view
        self.graph_graphics_view = GraphGraphics(self.scene.grScene, self)

        widget_layout = QHBoxLayout()
        widget_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(widget_layout)

        self.v_splitter = QSplitter(Qt.Vertical)
        widget_layout.addWidget(self.v_splitter)

        self.editor_wnd = QSplitter(Qt.Horizontal)
        self.v_splitter.addWidget(self.editor_wnd)
        self.editor_wnd.addWidget(self.graph_graphics_view)

        text_code_widget = QWidget()
        text_code_layout = QVBoxLayout()

        text_code_widget.setLayout(text_code_layout)
        self.editor_wnd.addWidget(text_code_widget)

        text_code_widget.resize(800, 100)
        text_code_layout.setContentsMargins(0, 0, 0, 0)


        code_wnd_bar = QHBoxLayout()
        code_wnd_bar.setContentsMargins(0, 0, 5, 0)
        code_wnd_bar.addWidget(QLabel("Select Syntax"))
        text_code_layout.addLayout(code_wnd_bar)

        self.stacked_code_wnd = QStackedWidget()
        self.text_code_wnd = QTextEdit()
        self.multi_code_wnd = QTabWidget()

        self.header_wnd = QTextEdit()
        self.cpp_wnd = QTextEdit()

        self.multi_code_wnd.addTab(self.header_wnd, '    .H    ')
        self.multi_code_wnd.addTab(self.cpp_wnd, '     .CPP    ')

        self.text_code_wnd.setReadOnly(True)
        self.header_wnd.setReadOnly(True)
        self.cpp_wnd.setReadOnly(True)

        self.stacked_code_wnd.addWidget(self.text_code_wnd)

        self.stacked_code_wnd.addWidget(self.multi_code_wnd)
        self.stacked_code_wnd.setCurrentIndex(1)
        text_code_layout.addWidget(self.stacked_code_wnd)

        self.syntax_selector = QComboBox()
        self.syntax_selector.currentIndexChanged.connect(self.syntax_changed)
        self.syntax_selector.setMinimumWidth(80)
        self.syntax_selector.currentTextChanged.connect(self.UpdateTextCode)

        self.syntax_selector.addItem("Python")
        self.syntax_selector.addItem("C++")
        self.syntax_selector.addItem("Rust")

        code_wnd_bar.addWidget(self.syntax_selector)
        code_wnd_bar.addItem(QSpacerItem(10, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum))

        self.code_orientation_btn = QPushButton()
        self.code_orientation_btn.setMaximumSize(25, 25)
        self.code_orientation_btn.setIcon(QIcon(self.scene.masterRef.global_switches.get_icon("orientation.png")))
        self.code_orientation_btn.setWindowIconText("orientation.png")
        self.code_orientation_btn.clicked.connect(self.UpdateTextWndRot)
        code_wnd_bar.addWidget(self.code_orientation_btn)

        self.copy_code_btn = QPushButton()
        self.copy_code_btn.setMaximumSize(25, 25)
        self.copy_code_btn.setIcon(QIcon(self.scene.masterRef.global_switches.get_icon("copy.png")))
        self.copy_code_btn.setWindowIconText("copy.png")
        self.copy_code_btn.clicked.connect(self.CopyTextCode)
        code_wnd_bar.addWidget(self.copy_code_btn)

        self.run_btn = QPushButton()
        self.run_btn.setMaximumSize(25, 25)
        self.run_btn.setIcon(QIcon(self.scene.masterRef.global_switches.get_icon("run.png")))
        self.run_btn.setWindowIconText("run.png")
        self.run_btn.clicked.connect(self.run_code)
        code_wnd_bar.addWidget(self.run_btn)

        # Terminal
        self.code_output = QTextEdit()
        self.code_output.setFont(QFont('Roboto', 12))
        self.v_splitter.addWidget(self.code_output)

    def UpdateTextWndRot(self):
        if self.editor_wnd.orientation() == Qt.Horizontal:
            self.editor_wnd.setOrientation(Qt.Vertical)
        else:
            self.editor_wnd.setOrientation(Qt.Horizontal)

    def isModified(self) -> bool:
        """Has the `Scene` been modified?

        :return: ``True`` if the `Scene` has been modified
        :rtype: ``bool``
        """
        return self.scene.isModified()

    def isFilenameSet(self) -> bool:
        """Do we have a graph loaded from file or are we creating a new one?

        :return: ``True`` if filename is set. ``False`` if it is a new graph not yet saved to a file
        :rtype: ''bool''
        """
        return self.filename is not None

    def getSelectedItems(self) -> list:
        """Shortcut returning `Scene`'s currently selected items

        :return: list of ``QGraphicsItems``
        :rtype: list[QGraphicsItem]
        """
        return self.scene.getSelectedItems()

    def hasSelectedItems(self) -> bool:
        """Is there something selected in the :class:`nodeeditor.node_scene.Scene`?

        :return: ``True`` if there is something selected in the `Scene`
        :rtype: ``bool``
        """
        return self.getSelectedItems() != []

    def canUndo(self) -> bool:
        """Can Undo be performed right now?

        :return: ``True`` if we can undo
        :rtype: ``bool``
        """
        return self.scene.history.canUndo()

    def canRedo(self) -> bool:
        """Can Redo be performed right now?

        :return: ``True`` if we can redo
        :rtype: ``bool``
        """
        return self.scene.history.canRedo()

    def getUserFriendlyFilename(self) -> str:
        """Get user friendly filename. Used in the window title

        :return: just a base name of the file or `'New Graph'`
        :rtype: ``str``
        """
        if self.isFilenameSet():
            name = os.path.splitext(os.path.basename(self.filename))[0]
        else:
            name = self.windowTitle().replace("*", "")
        return name + ("*" if self.isModified() else "")

    def setup_new_graph(self):
        """Empty the scene (create new Graph)"""
        self.scene.clear()
        self.filename = None
        self.scene.history.clear()
        self.scene.history.storeInitialHistoryStamp()
        return self.scene

    def fileLoad(self, filename: str):
        """Load serialized graph from JSON file

        :param filename: file to load
        :type filename: ``str``
        """
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.scene.loadFromFile(filename)
            self.filename = filename
            self.scene.history.clear()
            self.scene.history.storeInitialHistoryStamp()
            return True

        except FileNotFoundError as e:
            print("File Not Found")
            dumpException(e)
            QMessageBox.warning(self, "Error loading %s" % os.path.basename(filename), str(e).replace('[Errno 2]', ''))
            return False
        except InvalidFile as e:
            dumpException(e)
            QMessageBox.warning(self, "Error loading %s" % os.path.basename(filename), str(e))
            return False
        finally:
            QApplication.restoreOverrideCursor()

    def fileSave(self, filename: str = None):
        """Save serialized graph to JSON file. When called with an empty parameter, we won't store/remember the filename.

        :param filename: file to store the graph
        :type filename: ``str``
        """
        if filename is not None:
            self.filename = filename

        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.scene.saveToFile(self.filename)
        QApplication.restoreOverrideCursor()

        return True

    def fileAutoSave(self, filename: str = None):
        """Save serialized graph to JSON file. When called with an empty parameter, we won't store/remember the filename.

        :param filename: file to store the graph
        :type filename: ``str``
        """

        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.scene.saveToFile(filename, silent=True)
        QApplication.restoreOverrideCursor()

        return True

    def addNodes(self):
        """Testing method to create 3 `Nodes` with 3 `Edges` connecting them"""
        node1 = Node(self.scene, "My Awesome Node 1", inputs=[0, 0, 0], outputs=[1, 5])
        node2 = Node(self.scene, "My Awesome Node 2", inputs=[3, 3, 3], outputs=[1])
        node3 = Node(self.scene, "My Awesome Node 3", inputs=[2, 2, 2], outputs=[1])
        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -200)

        edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        edge2 = Edge(self.scene, node2.outputs[0], node3.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        edge3 = Edge(self.scene, node1.outputs[0], node3.inputs[2], edge_type=EDGE_TYPE_BEZIER)

        self.scene.history.storeInitialHistoryStamp()

    def addDebugContent(self):
        """Testing method to put random QGraphicsItems and elements into QGraphicsScene"""
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)

        rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.grScene.addText("This is my Awesome text!", QFont("Roboto"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QPushButton("Hello World")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)

        line = self.grScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)

    def update_text_code_files(self):
        data = self.get_save_directory()

        for item in data:
            with open(item[0], 'w') as newPyFile:
                newPyFile.writelines(item[1])
            if not item[0].endswith('.h'):
                return item[0]

    def run_code(self):
        self.code_output.clear()
        process = subprocess.Popen(self.update_text_code_files(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        output = output.decode('UTF-8')
        error = error.decode('UTF-8')

        colorStyle = f''' style=" Font-size:12px ; color: #FF3333;" '''
        code = f""" <pre><p style="font-family: Roboto "><span {colorStyle} >{error}</span></p></pre> """

        self.code_output.append(output)
        self.code_output.append(code)

    def get_project_directory(self):
        return self.scene.masterRef.files_widget.Project_Directory

    def get_save_directory(self):
        data = []
        self.scene.masterRef.files_widget.get_scripts_dir(self.syntax_selector)

        if self.syntax_selector.currentText() == 'C++':
            Ex = '.h'
            directory = self.get_project_directory() + f"/{self.syntax_selector.currentText()}/{self.windowTitle().replace('*', '')}{Ex}"
            text_code = self.header_wnd.toPlainText()
            data.append([f"{directory}", f"{text_code}"])

            Ex = self.files_extensions[f'{self.syntax_selector.currentText()}']
            directory = self.get_project_directory() + f"/{self.syntax_selector.currentText()}/{self.windowTitle().replace('*', '')}{Ex}"
            text_code = self.cpp_wnd.toPlainText()
            data.append([f"{directory}", f"{text_code}"])

        else:
            Ex = self.files_extensions[f'{self.syntax_selector.currentText()}']
            directory = self.get_project_directory() + f"/{self.syntax_selector.currentText()}/{self.windowTitle().replace('*', '')}{Ex}"
            text_code = self.text_code_wnd.toPlainText()
            data.append([f"{directory}", f"{text_code}"])

        return data

    def CopyTextCode(self):
        self.text_code_wnd.selectAll()
        self.text_code_wnd.copy()
        self.update_text_code_files()

    def syntax_changed(self):
        value = 0
        if self.syntax_selector.currentText() == 'C++':
            value = 1

        self.stacked_code_wnd.setCurrentIndex(value)
        self.UpdateTextCode()

    def get_imports(self):
        syntax = self.syntax_selector.currentText()

        imports = []
        if syntax == "C++":

            value = {
                FloatVar.node_type: 'float',
                IntegerVar.node_type: 'int',
                BooleanVar.node_type: 'bool',
                StringVar.node_type: 'string',
            }

            used_node_types = []
            for node in self.scene.nodes:
                used_node_types.append(node.node_type)

            if used_node_types.__contains__(Print.node_type):
                imports.append(f'#include <iostream>')

            types = []
            for data in self.scene.user_nodes_wdg.user_nodes_data:
                if data[2] == UserFunction.node_type:
                    imports.append(f"{self.get_node_return('C++',data[3])} {data[0]}();")
                else:
                    imports.append(f'extern {value[data[2]]} {data[0]};')

                if not types.__contains__(data[2]):
                    types.append(data[2])


            for node_type in types:
                if node_type == StringVar.node_type:
                    imports.append("#include <string>")
                elif node_type == ListVar.node_type:
                    imports.append("#include <list>")

            return imports

    def UpdateTextCode(self):
        current_syntax = self.syntax_selector.currentText()

        if current_syntax == "C++":
            self.header_wnd.clear()
            imports = self.get_imports()
            for item in imports:
                self.header_wnd.append(item)
            self.header_wnd.append('')

            self.cpp_wnd.clear()
            self.cpp_wnd.append(f'#include "{self.windowTitle().replace("*","")}.h"')
            self.cpp_wnd.append(f'using namespace std;')

            for node in self.scene.nodes:
                node.syntax = current_syntax

                if node.getNodeCode() and node.showCode:
                    self.cpp_wnd.append(node.getNodeCode())

        else:
            self.text_code_wnd.clear()
            for node in self.scene.nodes:
                node.syntax = current_syntax

                if node.getNodeCode() and node.showCode:
                    self.text_code_wnd.append(node.getNodeCode())

