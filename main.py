import sys

from PyQt5.QtWidgets import *

from Script_Editor_WND import ScriptEditorWND

if __name__ == '__main__':

    app = QApplication(sys.argv)

    mainWindow = ScriptEditorWND()

    mainWindow.initUI()

    sys.exit(app.exec_())
