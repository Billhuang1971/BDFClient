import time

import sys

from view.login_form.form import Ui_mainWindow
from PyQt5.QtWidgets import *


class LoginView(QMainWindow, Ui_mainWindow, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = LoginView()
    view.show()
    sys.exit(app.exec_())
