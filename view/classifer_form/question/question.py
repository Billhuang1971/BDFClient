import sys

from view.classifer_form.question.form import Ui_QuestionForm
from PyQt5.QtWidgets import QWidget

class Question(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui=Ui_QuestionForm()
        self.ui.setupUi(self)