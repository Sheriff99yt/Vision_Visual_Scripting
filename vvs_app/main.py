import os, sys

from PyQt5.QtGui import QIcon
from qtpy.QtWidgets import QApplication

# This Import Is Important for Node Registration.. (Do not remove !!!)
from vvs_app.nodes import *

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "", ".."))

from vvs_app.master_window import MasterWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # print(QStyleFactory.keys())
    app.setStyle('Fusion')
    app.setWindowIcon(QIcon("icons/VVS_Logo.png"))

    wnd = MasterWindow()
    wnd.showMaximized()

    # msg = QMessageBox()
    # msg.setText(f"""Your Data is Being Saved By Default in\n\n {wnd.filesWidget.Project_Directory}""")
    # msg.setWindowTitle("Note")
    # msg.setWindowIcon(QIcon("icons/VVS_Logo.png"))
    # msg.setStyleSheet("background-color: #282828; color: rgb(255, 255, 255);")
    # msg.exec_()

    sys.exit(app.exec_())