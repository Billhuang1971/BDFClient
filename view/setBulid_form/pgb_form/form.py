from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *


class pgbView(QDialog):
    def __init__(self, parent=None, thread=None, maximum=100, content=''):
        super(pgbView, self).__init__(parent)
        self.thread = thread
        self.maximum = maximum
        self.init_view(content)

    def init_view(self, content):
        self.setWindowTitle(content)
        self.setFixedSize(180, 60)
        self.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.pgb = QProgressBar()
        self.pgb.setMaximum(self.maximum)
        self.pgb.setMinimum(0)
        self.spaceItem_1 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spaceItem_2 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        font = QFont()
        font.setPointSize(12)
        font1 = QFont()
        font1.setPointSize(9)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()

        self.horizontalLayout_1.addWidget(self.pgb)
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        # self.verticalLayout.addLayout(self.horizontalLayout_2)
