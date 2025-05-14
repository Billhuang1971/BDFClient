import sys

from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt
import sys
from functools import partial

from view.taskSettings_form.form import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QComboBox, QLineEdit, QListView, QCompleter
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QMouseEvent, QFont, QBrush, QIntValidator
import sys
from PyQt5 import QtWidgets, QtGui


class PatientTableWidget(QMainWindow):
    control_signal = pyqtSignal(list)

    def __init__(self,*args, **kwargs, ):
        super(PatientTableWidget, self).__init__(*args, **kwargs)
        self.addOther()
        # self.__init_ui(on_clicked_selectBtn)

    def init_ui(self, current_page=1, col_label=None, sampleList=None, totalNum=0, on_clicked_selectBtn=None,):

        self.tableRow = len(sampleList)
        self.tableCol = len(col_label)
        self.col_label = col_label
        self.sampleList = sampleList
        self.current_page = current_page
        self.totalNum = totalNum
        self.table = QTableWidget(self.tableRow, self.tableCol)
        self.table.setHorizontalHeaderLabels(self.col_label)

        # print(self.col_label)
        for row in range(0, self.tableRow):
            for col in range(0, self.tableCol-1):
                if isinstance(self.sampleList[row][col+1], int):
                    self.text_item = QTableWidgetItem(str(self.sampleList[row][col+1]))
                else:
                    self.text_item = QTableWidgetItem(self.sampleList[row][col+1])
                self.text_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.text_item.setFont(QFont('', 12))
                self.table.setItem(row, col, self.text_item)

                # 设置最后一列信息
                layout = QHBoxLayout()
                self.table.setCellWidget(row, self.tableCol - 1, QWidget())
                selectBtn = QPushButton('选择')
                selectBtn.clicked.connect(partial(on_clicked_selectBtn, row))
                selectBtn.setStyleSheet('border: none;color:blue')
                selectBtn.setFont(QFont('', 12))
                selectBtn.setCursor(Qt.PointingHandCursor)
                layout.addWidget(selectBtn)
                self.table.cellWidget(row, self.tableCol - 1).setLayout(layout)
            self.table.setRowHeight(row, 50)

        self.table.horizontalHeader().setStyleSheet(
            '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应宽度
        self.table.horizontalHeader().setDefaultSectionSize(200)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_1.addWidget(self.table)

    def addOther(self):
        style_sheet = """
                   QLineEdit{
                       max-width: 40px
                   }
                   QLabel{
                       font-size: 14px;
                   }
               """
        # 添加搜索框
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboCond = QtWidgets.QComboBox()
        self.comboCond.setFixedWidth(int(6 * 16 * 1.67))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.comboCond.setFont(font)
        self.comboCond.setObjectName("comboCond")
        self.horizontalLayout.addWidget(self.comboCond)
        self.lineValue = QtWidgets.QLineEdit()
        self.lineValue.setFixedWidth(int(6 * 16 * 1.67))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineValue.setFont(font)
        self.lineValue.setObjectName("lineValue")
        self.horizontalLayout.addWidget(self.lineValue)
        self.btnSelect = QtWidgets.QPushButton('搜索')
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btnSelect.setFont(font)
        self.btnSelect.setObjectName("btnSelect")
        self.horizontalLayout.addWidget(self.btnSelect)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.horizontalLayout.addItem(spacerItem)

        # 添加重置按钮
        self.btnReSelect = QtWidgets.QPushButton('重置')
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btnReSelect.setFont(font)
        self.btnReSelect.setObjectName("btnReSelect")
        self.horizontalLayout.addWidget(self.btnReSelect)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        # 中心组件相关代码
        # 返回上一级
        bar = self.menuBar()
        self.returnBtn = QAction("<<返回上一级", self)
        self.returnBtn .setFont(QFont('', 12))
        bar.addAction(self.returnBtn)

        # 中心组件
        self.centerWindow = QWidget()
        self.__layout = QVBoxLayout()

        # 添加搜索框以及查询按钮
        self.__layout.addLayout(self.horizontalLayout)

        # 添加表格
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        # self.verticalLayout_1.addWidget(self.table)
        self.__layout.addLayout(self.verticalLayout_1)

        # 中心组件相关代码
        self.centerWindow.setLayout(self.__layout)
        self.setCentralWidget(self.centerWindow)
        self.setStyleSheet(style_sheet)

    def setPageController(self, page):
        """自定义页码控制器"""
        self.control_layout = QHBoxLayout()
        homePage = QPushButton("首页")
        prePage = QPushButton("<上一页")
        self.curPage = QLabel("{}".format(self.current_page))
        nextPage = QPushButton("下一页>")
        finalPage = QPushButton("尾页")
        self.totalPage = QLabel("共" + str(page) + "页")
        self.totalNum = QLabel("共" + str(self.totalNum) + "条样本")
        skipLable_0 = QLabel("跳到")
        self.skipPage = QLineEdit()
        intValidator = QIntValidator(self)
        self.skipPage.setValidator(intValidator)
        self.skipPage.setText('1')
        skipLabel_1 = QLabel("页")
        confirmSkip = QPushButton("确定")
        homePage.clicked.connect(self.__home_page)
        prePage.clicked.connect(self.__pre_page)
        nextPage.clicked.connect(self.__next_page)
        finalPage.clicked.connect(self.__final_page)
        confirmSkip.clicked.connect(self.__confirm_skip)
        self.control_layout.addStretch(1)
        self.control_layout.addWidget(homePage)
        self.control_layout.addWidget(prePage)
        self.control_layout.addWidget(self.curPage)
        self.control_layout.addWidget(nextPage)
        self.control_layout.addWidget(finalPage)
        self.control_layout.addWidget(self.totalPage)
        self.control_layout.addWidget(self.totalNum)
        self.control_layout.addWidget(skipLable_0)
        self.control_layout.addWidget(self.skipPage)
        self.control_layout.addWidget(skipLabel_1)
        self.control_layout.addWidget(confirmSkip)
        self.control_layout.addStretch(1)
        self.__layout.addLayout(self.control_layout)

    def __home_page(self):
        """点击首页信号"""
        self.control_signal.emit(["home", self.curPage.text()])

    def __pre_page(self):
        """点击上一页信号"""
        self.control_signal.emit(["pre", self.curPage.text()])

    def __next_page(self):
        """点击下一页信号"""
        self.control_signal.emit(["next", self.curPage.text()])

    def __final_page(self):
        """尾页点击信号"""
        self.control_signal.emit(["final", self.curPage.text()])

    # def __confirm_skip(self):
    #     """跳转页码确定"""
    #     self.control_signal.emit(["confirm", self.skipPage.text()])

    def __confirm_skip(self):
        """跳转页码确定"""
        try:
            page = int(self.skipPage.text())
            if page < 1:
                raise ValueError
            self.control_signal.emit(["confirm", str(page)])
        except ValueError:
            QMessageBox.warning(self, "输入错误", "请输入有效的页码（正整数）")

    def showTotalPage(self):
        """返回当前总页数"""
        return int(self.totalPage.text()[1:-1])
