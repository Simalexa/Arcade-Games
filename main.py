from PyQt5 import QtWidgets # import PyQt5 widgets
from choosing import mainWindow

import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = mainWindow()
    application.show()
    sys.exit(app.exec())