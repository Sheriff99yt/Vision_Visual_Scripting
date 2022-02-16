import os, sys
from qtpy.QtWidgets import QApplication

sys.path.insert(0, os.path.join( os.path.dirname(__file__), "..", ".." ))

from examples.example_calculator.master_window import MasterWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # print(QStyleFactory.keys())
    app.setStyle('Fusion')

    wnd = MasterWindow()
    wnd.show()

    sys.exit(app.exec_())
