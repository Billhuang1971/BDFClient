import sys

from PyQt5.QtCore import Qt, pyqtSignal,QRegExp
from PyQt5.QtGui import QFont,QIntValidator,QRegExpValidator
from PyQt5 import QtCore
from functools import partial
from view.patientManager_form.form import Ui_Form
from PyQt5.QtWidgets import *

class patientManagerView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 病人信息表的列数
        self.col_num = 7
        self.selected_row = []

    def initView(self, on_clicked_patient_add, on_clicked_patient_del, on_clicked_patient_edit, tUser):
        try:
            # self.ui.verticalLayout.addWidget(self.tableWidget)
            # self.ui.verticalLayout.setStretch(0, 1)
            # self.ui.verticalLayout.setStretch(1, 9)
            if tUser[9] == 1:
                self.ui.addButton.clicked.connect(on_clicked_patient_add)
                self.ui.delButton.clicked.connect(on_clicked_patient_del)
                self.ui.editButton.clicked.connect(on_clicked_patient_edit)
            elif tUser[8] == 1 or tUser[10] == 1:
                self.ui.addButton.setEnabled(False)
                self.ui.delButton.setEnabled(False)
                self.ui.editButton.setEnabled(False)
            else:
                self.ui.addButton.clicked.connect(on_clicked_patient_add)
                self.ui.delButton.clicked.connect(on_clicked_patient_del)
                self.ui.editButton.clicked.connect(on_clicked_patient_edit)
            # self.ui.addButton.adjustSize()
            # self.ui.editButton.adjustSize()
            # self.ui.delButton.adjustSize()
        except Exception as e:
            print('initView', e)

    # def initTable(self, patientInfo, prev_page, next_page):
    #     try:
    #         col_num = self.col_num
    #         row_num = len(patientInfo)
    #         self.tableWidget.setRowCount(row_num)
    #         self.tableWidget.setColumnCount(col_num)
    #         self.tableWidget.setInputMethodHints(Qt.ImhHiddenText)
    #         # 设置表格高度
    #         for i in range(row_num):
    #             self.tableWidget.setRowHeight(i, 55)
    #         # 设置除最后一列之外的列的宽度
    #         for i in range(0, col_num - 1):
    #             self.tableWidget.setColumnWidth(i, 150)
    #         self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
    #         # 设置列头
    #         col_label = ['姓名', '出生日期', '性别', '医保卡号', '电话号码', '籍贯', '现居住地']
    #         # 设置表头列表名称
    #         self.tableWidget.setHorizontalHeaderLabels(col_label)
    #         # 设置表头格式
    #         self.tableWidget.horizontalHeader().setStyleSheet(
    #             '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
    #         # 使表格填满整个widget
    #         self.tableWidget.horizontalHeader().setStretchLastSection(True)
    #         # print(patientInfo)
    #         for row in range(0, row_num):
    #             for col in range(0, col_num):
    #                 if not isinstance(patientInfo[row][col], str):
    #                     patientInfo[row][col] = str(patientInfo[row][col])
    #                 textItem = QTableWidgetItem(patientInfo[row][col])
    #                 textItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    #                 textItem.setFont(QFont('', 12))
    #                 textItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    #                 self.tableWidget.setItem(row, col, textItem)
    #
    #     except Exception as e:
    #         print('initTable', e)

class NoSpaceDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            editor.setValidator(QRegExpValidator(QRegExp("[^\\s]+")))  # 禁止空格
        return editor
class TableWidget(QWidget):
    control_signal = pyqtSignal(list)

    def __init__(self, patientInfo, current_page,
                 *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)
        self.col_label = ['姓名', '出生日期', '性别', '医保卡号', '电话号码', '籍贯', '现居住地']
        self.col_num = len(self.col_label)
        self.cur_page = current_page
        self.table = QTableWidget()
        self.init_table(patientInfo)

    def init_table(self, patientInfo):
        style_sheet = """
            QTableWidget {
                border: 1px solid blue;
                background-color:rgb(255,255,255)
            }
            QPushButton{
                max-width: 30ex;
                max-height: 12ex;
                font-size: 14px;
            }
            QLineEdit{
                max-width: 30px
            }
        """
        try:
            col_num = self.col_num
            row_num = len(patientInfo)
            self.table.setRowCount(row_num)
            self.table.setColumnCount(col_num)
            self.table.setInputMethodHints(Qt.ImhHiddenText)
            # 设置表格高度
            for i in range(row_num):
                self.table.setRowHeight(i, 55)
            # 设置除最后一列之外的列的宽度
            for i in range(0, col_num - 1):
                self.table.setColumnWidth(i, 150)
            self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
            # 设置列头
            col_label = ['姓名', '出生日期', '性别', '医保卡号', '电话号码', '籍贯', '现居住地']
            # 设置表头列表名称
            self.table.setHorizontalHeaderLabels(col_label)
            # 设置表头格式
            self.table.horizontalHeader().setStyleSheet(
                '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
            # 使表格填满整个widget
            self.table.horizontalHeader().setStretchLastSection(True)
            # print(patientInfo)
            for row in range(0, row_num):
                for col in range(0, col_num):
                    if not isinstance(patientInfo[row][col], str):
                        patientInfo[row][col] = str(patientInfo[row][col])
                    textItem = QTableWidgetItem(patientInfo[row][col])
                    textItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    textItem.setFont(QFont('', 12))
                    textItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.table.setItem(row, col, textItem)
            self.__layout = QVBoxLayout()
            self.__layout.addWidget(self.table)
            self.setLayout(self.__layout)
            self.setStyleSheet(style_sheet)
        except Exception as e:
            print('initTable', e)

    def setPageController(self, page):
        """自定义页码控制器"""
        control_layout = QHBoxLayout()
        homePage = QPushButton("首页")
        prePage = QPushButton("<上一页")
        self.curPage = QLabel(str(self.cur_page))
        font = QFont()
        font.setPixelSize(14)
        self.curPage.setFont(font)
        nextPage = QPushButton("下一页>")
        finalPage = QPushButton("尾页")
        self.totalPage = QLabel("共" + str(page) + "页")
        self.totalPage.setFont(font)
        skipLable_0 = QLabel("跳到")
        skipLable_0.setFont(font)
        self.skipPage = QLineEdit()
        self.skipPage.setValidator(QIntValidator(1, 999999))
        skipLabel_1 = QLabel("页")
        skipLabel_1.setFont(font)
        confirmSkip = QPushButton("确定")
        homePage.clicked.connect(self.__home_page)
        prePage.clicked.connect(self.__pre_page)
        nextPage.clicked.connect(self.__next_page)
        finalPage.clicked.connect(self.__final_page)
        confirmSkip.clicked.connect(self.__confirm_skip)
        control_layout.addStretch(1)
        control_layout.addWidget(homePage)
        control_layout.addWidget(prePage)
        control_layout.addWidget(self.curPage)
        control_layout.addWidget(nextPage)
        control_layout.addWidget(finalPage)
        control_layout.addWidget(self.totalPage)
        control_layout.addWidget(skipLable_0)
        control_layout.addWidget(self.skipPage)
        control_layout.addWidget(skipLabel_1)
        control_layout.addWidget(confirmSkip)
        control_layout.addStretch(1)
        self.__layout.addLayout(control_layout)
        # self.__layout.setStretch(0, 12)
        # self.__layout.setStretch(1, 1)

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

    def __confirm_skip(self):
        """跳转页码确定"""
        self.control_signal.emit(["confirm", self.skipPage.text()])

    def showTotalPage(self):
        """返回当前总页数"""
        return int(self.totalPage.text()[1:-1])
if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = patientManagerView()
    view.show()
    sys.exit(app.exec_())
