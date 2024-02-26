import ctypes
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qtpy.QtWidgets import QApplication
from master_window import MasterWindow, Splash

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "", ".."))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyle('Fusion')
    app.setWindowIcon(QIcon("vvs_app/icons/Dark/VVS_Logo_Thick.png"))

    # Show app Icon In Task Manager
    myappid = 'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    splash = Splash()

    wnd = MasterWindow()

    splash.run(wnd)

    sys.exit(app.exec_())
