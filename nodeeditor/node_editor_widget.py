# -*- coding: utf-8 -*-
"""
A module containing ``NodeEditorWidget`` class
"""
import os
import subprocess
import tempfile

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from nodeeditor.node_edge import Edge, EDGE_TYPE_BEZIER
from nodeeditor.graph_graphics import GraphGraphics
from nodeeditor.node_node import Node
from nodeeditor.node_scene import NodeScene, InvalidFile
from nodeeditor.utils import dumpException


class NodeEditorWidget(QWidget):
    Scene_class = NodeScene
    GraphGraphics_class = GraphGraphics
    """The ``NodeEditorWidget`` class"""

    def __init__(self, parent: QWidget = None):
        """
        :param parent: parent widget
        :type parent: ``QWidget``

        :Instance Attributes:

        - **filename** - currently graph's filename or ``None``
        """
        super().__init__(parent)

        self.filename = None
        self.file_path = ''
        self.createWidgetWindow()


    def createWidgetWindow(self):
        """
        Set up this ``NodeEditorWidget`` with its layout,  :class:`~nodeeditor.node_scene.Scene` and
        :class:`~nodeeditor.node_graphics_view.QDMGraphicsView`
        """


        widget_layout = QHBoxLayout()
        widget_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(widget_layout)

        text_code_layout = QVBoxLayout()
        text_code_layout.setContentsMargins(0, 0, 0, 0)

        text_code_widget = QWidget()
        text_code_widget.resize(800, 100)
        text_code_widget.setLayout(text_code_layout)

        # crate graphics scene
        self.scene = self.__class__.Scene_class()

        # create graphics view
        self.graph_graphics_view = self.__class__.GraphGraphics_class(self.scene.grScene, self)

        # create widget splitter
        self.v_splitter = QSplitter(Qt.Vertical)

        self.editor_wnd = QSplitter(Qt.Horizontal)

        self.text_code_wnd = QTextEdit()
        self.text_code_wnd.setReadOnly(True)

        self.code_output = QTextEdit()
        self.code_output.setStyleSheet("background-color: #282828")
        self.code_output.setFont(QFont('Roboto', 12))

        self.syntax_selector = QComboBox()
        self.syntax_selector.setMinimumWidth(80)
        self.syntax_selector.currentTextChanged.connect(self.UpdateTextCode)
        self.syntax_selector.addItem("Python")
        self.syntax_selector.addItem("C++")

        self.run_btn = QPushButton()
        self.run_btn.setMaximumSize(30, 30)
        self.run_btn.setIcon(QIcon("icons/run.png"))
        self.run_btn.clicked.connect(self.run_code)

        code_wnd_bar = QHBoxLayout()
        code_wnd_bar.setContentsMargins(4, 4, 4, 4)
        code_wnd_bar.addWidget(QLabel("Select Syntax"))
        code_wnd_bar.addWidget(self.syntax_selector)
        code_wnd_bar.addItem(QSpacerItem(20, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum))
        code_wnd_bar.addWidget(QLabel("Run"))
        code_wnd_bar.addWidget(self.run_btn)

        text_code_layout.addLayout(code_wnd_bar)
        text_code_layout.addWidget(self.text_code_wnd)

        # Connecting NodeEditorWidget to other Child classes to enable calling functions from Parent classes
        self.scene.setNodeEditorWidget(self)
        self.graph_graphics_view.setNodeEditorWidget(self)

        self.editor_wnd.addWidget(self.graph_graphics_view)
        self.editor_wnd.addWidget(text_code_widget)

        self.v_splitter.addWidget(self.editor_wnd)
        self.v_splitter.addWidget(self.code_output)

        widget_layout.addWidget(self.v_splitter)

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
        name = os.path.splitext(os.path.basename(self.filename))[0] if self.isFilenameSet() else "New Graph"
        # name = os.path.basename(self.filename) if self.isFilenameSet() else "New Graph"
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
            # QApplication.restoreOverrideCursor()
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


    def run_code(self):
        self.code_output.clear()
        fname = f"C:/Users/{os.getlogin()}/AppData/Roaming/VVS"+f"""/code_runner.py"""
        with open(fname, 'w') as newPyFile:
            newPyFile.writelines(self.text_code_wnd.toPlainText())

        process = subprocess.Popen(fname, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        output = output.decode('UTF-8')
        error = error.decode('UTF-8')

        colorStyle = f''' style=" Font-size:12px ; color: #FF3333;" '''
        code = f""" <pre><p style="font-family: Roboto "><span {colorStyle} >{error}</span></p></pre> """

        self.code_output.append(output)
        self.code_output.append(code)

    def UpdateTextCode(self):
        self.text_code_wnd.clear()
        s = self.syntax_selector.currentText()
        for node in self.scene.nodes:
            node.syntax = s
            # Don't add Text Code OF Node in these cases !
            if node.getNodeCode() is None or node.showCode is not True:
                pass
            else:
                self.text_code_wnd.append(node.getNodeCode())
        # print(self.text_code_wnd.find("f"))
        # print("o")
