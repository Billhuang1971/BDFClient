import sys

from view.configOptions_form.form1 import Ui_Form
from view.configOptions_form.prentry import Ui_Prentry
from PyQt5.QtWidgets import *

class configOptionsView(QWidget):
    def __init__(self, parent=None,):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

class PrentryView(QWidget):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_Prentry()
        self.ui.setupUi(self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = configOptionsView()
    view.show()
    sys.exit(app.exec_())
