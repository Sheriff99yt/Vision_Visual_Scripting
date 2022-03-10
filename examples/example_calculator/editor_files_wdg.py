from qtpy.QtCore import *
from qtpy.QtWidgets import *


class FilesWDG(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        l1 = QTreeWidgetItem(["My Folder"])
        l2 = QTreeWidgetItem(["old Folder"])

        for i in range(3):
            l1_child = QTreeWidgetItem(["Graph_0"])
            l1.addChild(l1_child)

        for j in range(2):
            l2_child = QTreeWidgetItem(["Graph_0"])
            l2.addChild(l2_child)

        self.setColumnCount(2)
        self.setHeaderLabels(["Folders"])
        self.addTopLevelItem(l1)
        self.addTopLevelItem(l2)
