import sys
# from view.taskSettings_form.form import Ui_Form
from functools import partial

from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QComboBox, QLineEdit, QListView, QCompleter
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QMouseEvent, QFont, QBrush, QIntValidator
import sys
from PyQt5 import QtWidgets


class DetailTableWidget(QWidget):
    control_signal = pyqtSignal(list)
    # 暂时可以保留这个当前页码和总的显示数量，方便后面更新分页
    def __init__(self,  *args, **kwargs, ):
        super(DetailTableWidget, self).__init__(*args, **kwargs)
        # self.tableRow = len(sampleList)
        # self.tableCol = len(col_label)
        # self.col_label = col_label
        # self.sampleList = sampleList
        # # self.current_page = current_page
        # self.totalNum = totalNum
        # self.thme_id = theme_id
        self.initUI()


        # self.init_ui()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.tableLayout = QVBoxLayout()
        self.layout.addLayout(self.tableLayout)
        self.setLayout(self.layout)


    def init_ui(self, col_label=None, sampleList=None, totalNum=0, on_clicked_deltaskBtn=None):
        style_sheet = """
            QLineEdit{
                max-width: 40px
            }
            QLabel{
                font-size: 14px;
            }
        """
        self.tableRow = len(sampleList)
        self.tableCol = len(col_label)
        self.col_label = col_label
        self.sampleList = sampleList
        # self.current_page = current_page
        self.totalNum = totalNum
        # self.thme_id = theme_id

        self.table = QTableWidget(self.tableRow, self.tableCol)
        self.table.setHorizontalHeaderLabels(self.col_label)
        # print(self.col_label)
        for row in range(0, self.tableRow):
            # 这里只是填充前面几列的数据，最后一列的操作后面填充
            for col in range(0, self.tableCol-1):
                if isinstance(self.sampleList[row][col+4], int):
                    # 因为前面有其它数字所以需要这样加
                    self.text_item = QTableWidgetItem(str(self.sampleList[row][col+4]))
                else:
                    self.text_item = QTableWidgetItem(self.sampleList[row][col+4])
                self.text_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.text_item.setFont(QFont('', 12))
                self.table.setItem(row, col, self.text_item)


            # 为最后一列添加按钮
            layout = QHBoxLayout()
            self.table.setCellWidget(row, self.tableCol-1, QWidget())
            deltaskBtn = QPushButton('删除')
            deltaskBtn.clicked.connect(partial(on_clicked_deltaskBtn,row))
            deltaskBtn.setStyleSheet('border: none;color:blue')
            deltaskBtn.setFont(QFont('', 12))
            # choosefileBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
            deltaskBtn.setCursor(Qt.PointingHandCursor)
            layout.addWidget(deltaskBtn)


            layout.setStretch(0, 1)
            layout.setStretch(1, 1)
            # layout.setStretch(2, 1)
            # layout.setStretch(3, 1)
            self.table.cellWidget(row, self.tableCol-1).setLayout(layout)
            self.table.setRowHeight(row, 50)

        self.table.horizontalHeader().setStyleSheet(
            '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应宽度
        # self.table.horizontalHeader().setDefaultSectionSize(200)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)

        # 随内容分配列宽
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置一次选择一行
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 设置除了最后一列以外的列宽
        # 设置除最后一列之外的列的宽度
        # for i in range(0, self.tableCol-1):
        #     self.table.setColumnWidth(i, 150)

        # 直接设置最后一列宽度
        # self.table.setColumnWidth(self.tableCol-1, 600)

        # self.layout = QVBoxLayout()
        self.setStyleSheet(style_sheet)
        self.tableLayout.addWidget(self.table)
        # self.setLayout(self.layout)


    # def initTable(self, data):
    #     pass

    # def setPageController(self, page):
    #     """自定义页码控制器"""
    #     control_layout = QHBoxLayout()
    #     homePage = QPushButton("首页")
    #     prePage = QPushButton("<上一页")
    #     self.curPage = QLabel("{}".format(self.current_page))
    #     nextPage = QPushButton("下一页>")
    #     finalPage = QPushButton("尾页")
    #     self.totalPage = QLabel("共" + str(page) + "页")
    #     self.totalNum = QLabel("共" + str(self.totalNum) + "条样本")
    #     skipLable_0 = QLabel("跳到")
    #     self.skipPage = QLineEdit()
    #     intValidator = QIntValidator(self)
    #     self.skipPage.setValidator(intValidator)
    #     self.skipPage.setText('1')
    #     skipLabel_1 = QLabel("页")
    #     confirmSkip = QPushButton("确定")
    #     homePage.clicked.connect(self.__home_page)
    #     prePage.clicked.connect(self.__pre_page)
    #     nextPage.clicked.connect(self.__next_page)
    #     finalPage.clicked.connect(self.__final_page)
    #     confirmSkip.clicked.connect(self.__confirm_skip)
    #     control_layout.addStretch(1)
    #     control_layout.addWidget(homePage)
    #     control_layout.addWidget(prePage)
    #     control_layout.addWidget(self.curPage)
    #     control_layout.addWidget(nextPage)
    #     control_layout.addWidget(finalPage)
    #     control_layout.addWidget(self.totalPage)
    #     control_layout.addWidget(self.totalNum)
    #     control_layout.addWidget(skipLable_0)
    #     control_layout.addWidget(self.skipPage)
    #     control_layout.addWidget(skipLabel_1)
    #     control_layout.addWidget(confirmSkip)
    #     control_layout.addStretch(1)
    #     self.__layout.addLayout(control_layout)
    #
    # def __home_page(self):
    #     """点击首页信号"""
    #     self.control_signal.emit(["home", self.curPage.text()])
    #
    # def __pre_page(self):
    #     """点击上一页信号"""
    #     self.control_signal.emit(["pre", self.curPage.text()])
    #
    # def __next_page(self):
    #     """点击下一页信号"""
    #     self.control_signal.emit(["next", self.curPage.text()])
    #
    # def __final_page(self):
    #     """尾页点击信号"""
    #     self.control_signal.emit(["final", self.curPage.text()])
    #
    # def __confirm_skip(self):
    #     """跳转页码确定"""
    #     self.control_signal.emit(["confirm", self.skipPage.text()])
    #
    # def showTotalPage(self):
    #     """返回当前总页数"""
    #     return int(self.totalPage.text()[1:-1])


