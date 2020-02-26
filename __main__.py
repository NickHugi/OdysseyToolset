import sys
from toolset import Toolset
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Toolset()
    sys.exit(app.exec_())
