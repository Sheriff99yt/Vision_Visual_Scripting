from qtpy.QtGui import QIcon, QPixmap
from qtpy.QtCore import QDataStream, QIODevice, Qt
from qtpy.QtWidgets import QAction, QGraphicsProxyWidget, QMenu

from examples.example_calculator.nodes.nodes_configuration import *
from nodeeditor.node_editor_widget import NodeEditorWidget
from nodeeditor.node_edge import EDGE_TYPE_DIRECT, EDGE_TYPE_BEZIER, EDGE_TYPE_SQUARE
from nodeeditor.graph_graphics import MODE_EDGE_DRAG
from nodeeditor.utils import dumpException

DEBUG = False
DEBUG_CONTEXT = False


class MasterEditorWnd(NodeEditorWidget):
    def __init__(self):
        super().__init__()
        # self.setAttribute(Qt.WA_DeleteOnClose)

        self.setTitle()

        self.initNewNodeActions()

        self.scene.addHasBeenModifiedListener(self.setTitle)
        self.scene.history.addHistoryRestoredListener(self.onHistoryRestored)
        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)
        self.scene.setNodeClassSelector(self.getNodeClassFromType)

        self._close_event_listeners = []

    def getNodeClassFromType(self, data):
        if 'node_type' not in data:
            return Node
        else:
            return get_node_by_type(data['node_type'])

    # def doEvalOutputs(self):
    #     # eval all output nodes
    #     for node in self.scene.nodes:
    #         if node.__class__.__name__ == "CalcNode_Output":
    #             node.eval()

    def onHistoryRestored(self):
        # self.doEvalOutputs()
        pass

    def fileLoad(self, filename):
        if super().fileLoad(filename):
            # self.doEvalOutputs()
            return True

        return False

    def initNewNodeActions(self):
        self.node_actions = {}
        Funs = list(FUNCTIONS.keys())
        Funs.sort()
        # Vars = list(USERVARS.keys())
        # Vars.sort()
        for key in Funs:
            node = FUNCTIONS[key]
            self.node_actions[node.node_type] = QAction(QIcon(node.icon), node.name)
            self.node_actions[node.node_type].setData(node.node_type)
        # for key in Vars:
        #     node = USERVARS[key]
        #     self.node_actions[node.node_type] = QAction(QIcon(node.icon), node.name)
        #     self.node_actions[node.node_type].setData(node.node_type)

    def initNodesContextMenu(self):
        context_menu = QMenu(self)
        Funs = list(FUNCTIONS.keys())
        Funs.sort()
        # Vars = list(USERVARS.keys())
        # Vars.sort()
        for key in Funs:
            context_menu.addAction(self.node_actions[key])
        # for key in Vars:
        #     context_menu.addAction(self.node_actions[key])
        return context_menu

    def setTitle(self):
        # self.setWindowTitle(self.getUserFriendlyFilename())
        self.setWindowTitle(self.windowTitle())

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)

    def onDragEnter(self, event):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            if DEBUG: print(" ... denied drag enter event")
            event.setAccepted(False)

    def onDrop(self, event):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            self.node_type = dataStream.readInt()
            text = dataStream.readQString()
            newNodeData = dataStream.readQStringList()


            nodeType = newNodeData[0]

            isEvent = False
            isVar = False
            isNode = False

            if nodeType == "E":
                isEvent = True
            elif nodeType == "N":
                isNode = True
            elif nodeType == "V":
                isVar = True


            mouse_position = event.pos()
            self.scene_position = self.scene.grScene.views()[0].mapToScene(mouse_position)

            if DEBUG: print("GOT DROP: [%d] '%s'" % (self.node_type, text), "mouse:", mouse_position, "scene:", self.scene_position)

            try:
                if isEvent:
                    self.eventSelectMenu(event)
                elif isVar:
                    self.varSelectMenu(event)
                else:
                    node = get_node_by_type(self.node_type)(self.scene)
                    node.setPos(self.scene_position.x(), self.scene_position.y())
                    self.scene.history.storeHistory("Created Node %s" % node.__class__.__name__)


                isEvent = False
                isVar = False
                isNode = False
                self.scene.NodeEditor.UpdateTextCode()

            except Exception as e:
                dumpException(e)

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            # print(" ... drop ignored, not requested format '%s'" % LISTBOX_MIMETYPE)
            event.ignore()

    def ActiveScene(self):
        return self.scene.masterRef.CurrentNodeEditor().scene

    def varSelectMenu(self, event):
        context_menu = QMenu(self)
        getter = context_menu.addAction("Get")
        setter = context_menu.addAction("Set")
        cancel = context_menu.addAction("Cancel")

        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        if action is cancel or action is None:
            return
        else:
            scene = self.ActiveScene()
            userVar = scene.VEListWdg.get_user_var_by_ID(self.node_type)(scene)
            if action == setter:
                userVar.toSetter()
            elif action == getter:
                userVar.toGetter()

            userVar.setPos(self.scene_position.x(), self.scene_position.y())
            self.scene.history.storeHistory("Created user Variable %s" % userVar.__class__.__name__)

    def eventSelectMenu(self, event):
        context_menu = QMenu(self)
        call = context_menu.addAction("Call Event")
        write = context_menu.addAction("Write Event")
        cancel = context_menu.addAction("Cancel")

        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        if action is cancel or action is None:
            return
        else:
            scene = self.ActiveScene()
            userEvent = scene.VEListWdg.get_user_event_by_ID(self.node_type)(scene)
            if action == write:
                userEvent.toSetter()
            elif action == call:
                userEvent.toGetter()

            userEvent.setPos(self.scene_position.x(), self.scene_position.y())
            self.scene.history.storeHistory("Created user Variable %s" % userEvent.__class__.__name__)

    def contextMenuEvent(self, event):
        try:
            item = self.scene.getItemAt(event.pos())
            if DEBUG_CONTEXT: print(item)

            if type(item) == QGraphicsProxyWidget:
                item = item.widget()

            if hasattr(item, 'node') or hasattr(item, 'socket'):
                self.handleNodeContextMenu(event)
            elif hasattr(item, 'edge'):
                self.handleEdgeContextMenu(event)
            # elif item is None:
            else:
                self.handleNewNodeContextMenu(event)

            return super().contextMenuEvent(event)
        except Exception as e:
            dumpException(e)

    def contextMenuEvent(self, event):
        try:
            item = self.scene.getItemAt(event.pos())
            if DEBUG_CONTEXT: print(item)

            if type(item) == QGraphicsProxyWidget:
                item = item.widget()

            if hasattr(item, 'node') or hasattr(item, 'socket'):
                self.handleNodeContextMenu(event)
            elif hasattr(item, 'edge'):
                self.handleEdgeContextMenu(event)
            # elif item is None:
            else:
                self.handleNewNodeContextMenu(event)

            return super().contextMenuEvent(event)
        except Exception as e:
            dumpException(e)

    def handleNodeContextMenu(self, event):
        if DEBUG_CONTEXT: print("CONTEXT: NODE")
        context_menu = QMenu(self)
        copy = context_menu.addAction("Copy")
        cut = context_menu.addAction("Cut")
        delete = context_menu.addAction("Delete")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if type(item) == QGraphicsProxyWidget:
            item = item.widget()

        if hasattr(item, 'node'):
            selected = item.node
        if hasattr(item, 'socket'):
            selected = item.socket.node

        if action == delete:
            item.node.scene.getView().deleteNode(item.node)


    def handleEdgeContextMenu(self, event):
        if DEBUG_CONTEXT: print("CONTEXT: EDGE")
        context_menu = QMenu(self)
        bezierAct = context_menu.addAction("Bezier Edge")
        directAct = context_menu.addAction("Direct Edge")
        squareAct = context_menu.addAction("Square Edge")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if hasattr(item, 'edge'):
            selected = item.edge

        if selected and action == bezierAct: selected.edge_type = EDGE_TYPE_BEZIER
        if selected and action == directAct: selected.edge_type = EDGE_TYPE_DIRECT
        if selected and action == squareAct: selected.edge_type = EDGE_TYPE_SQUARE

    # helper functions
    def determine_target_socket_of_node(self, was_dragged_flag, new_calc_node):
        target_socket = None
        if was_dragged_flag:
            if len(new_calc_node.inputs) > 0: target_socket = new_calc_node.inputs[0]
        else:
            if len(new_calc_node.outputs) > 0: target_socket = new_calc_node.outputs[0]
        return target_socket

    def finish_new_node_state(self, new_node):
        self.scene.doDeselectItems()
        new_node.grNode.doSelect(True)
        new_node.grNode.onSelected()

    def handleNewNodeContextMenu(self, event):

        if DEBUG_CONTEXT: print("CONTEXT: EMPTY SPACE")
        context_menu = self.initNodesContextMenu()
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        if action is not None:
            new_node = get_node_by_type(action.data())(self.scene)
            scene_pos = self.scene.getView().mapToScene(event.pos())
            new_node.setPos(scene_pos.x(), scene_pos.y())
            if DEBUG_CONTEXT: print("Selected node:", new_node)

            if self.scene.getView().mode == MODE_EDGE_DRAG:
                # if we were dragging an edge...
                target_socket = self.determine_target_socket_of_node(
                    self.scene.getView().dragging.drag_start_socket.is_output, new_node)
                if target_socket is not None:
                    self.scene.getView().dragging.edgeDragEnd(target_socket.grSocket)
                    self.finish_new_node_state(new_node)

            else:
                self.scene.history.storeHistory("Created %s" % new_node.__class__.__name__)
