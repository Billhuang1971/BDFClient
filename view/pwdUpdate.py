import time

import sys

from view.pwdUpda_form.form import Ui_Form
from PyQt5.QtWidgets import *


class PwdUpdateView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = PwdUpdateView()
    view.show()
    sys.exit(app.exec_())
