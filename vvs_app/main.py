import ctypes
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qtpy.QtWidgets import QApplication
from vvs_app.master_window import MasterWindow

# This Import Is Important for Node Registration.. (Do not remove !!!)
from vvs_app.nodes import *
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "", ".."))

class Splash(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: transparent")
        self.setAttribute(Qt.WA_TranslucentBackground, on=True)
        self.setWindowFlag(Qt.FramelessWindowHint)

        lo = QVBoxLayout()
        self.setLayout(lo)

        Logo = QLabel()
        pixmap = QPixmap("icons/Dark/VVS_White_Splash.png")
        Logo.setPixmap(pixmap)
        lo.addWidget(Logo)

        self.Loading_Label = QLabel("Loading")
        self.Loading_Label.setStyleSheet("font: 20px; color: white") # font-family: Calibri;
        lo.addWidget(self.Loading_Label)

        self.timer = QTimer()

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()

    def run(self, Main):
        self.show()
        self.timer.start(300)
        self.times = 0
        self.timer.timeout.connect(lambda: self.run_timeout(Main))

    def run_timeout(self, Main):
        if self.times >= 3:
            Main.showMaximized()
            self.close()
            self.timer.stop()
        else:
            self.times += 1
            self.Loading_Label.setText(self.Loading_Label.text() + " .")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyle('Fusion')
    app.setWindowIcon(QIcon("icons/Dark/VVS_Logo_Thick.png"))

    # Show app Icon In Task Manager
    myappid = 'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    splash = Splash()

    wnd = MasterWindow()
    # wnd.setWindowFlag(Qt.FramelessWindowHint)
    splash.run(wnd)

    sys.exit(app.exec_())
    # if selected_theme == night: