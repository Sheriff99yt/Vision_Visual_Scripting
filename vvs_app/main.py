import ctypes
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from qtpy.QtWidgets import QApplication

# This Import Is Important for Node Registration.. (Do not remove !!!)
# from vvs_app.nodes import *

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "", ".."))

from vvs_app.master_window import MasterWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyle('Fusion')
    app.setWindowIcon(QIcon("icons/VVS_Logo_Thick.png"))

    # Show app Icon In Task Manager
    myappid = 'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    wnd = MasterWindow()
    # wnd.setWindowFlag(Qt.FramelessWindowHint)
    wnd.showMaximized()

    sys.exit(app.exec_())

