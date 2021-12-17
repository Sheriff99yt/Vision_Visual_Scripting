import sys

from PyQt5.QtWidgets import *

from scriptEditor import ScriptEditor

if __name__ == '__main__':

    app = QApplication(sys.argv)

    mainWindow = ScriptEditor()

    mainWindow.initUI()

    sys.exit(app.exec_())
