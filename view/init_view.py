# !/usr/bin/python
# author bluenor

import time

import sys

from view.init_form.form import Ui_mainWindow
from PyQt5.QtWidgets import *

class InitView(QMainWindow, Ui_mainWindow, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)


