import sys

from view.patientInfo_form.form import Ui_Form
from PyQt5.QtWidgets import *

class patientInfoView(QWidget):
    def __init__(self, parent=None,):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = patientInfoView()
    view.show()
    sys.exit(app.exec_())
