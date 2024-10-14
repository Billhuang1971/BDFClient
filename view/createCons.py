import datetime
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from functools import partial
from view.createConsultation_form.form import Ui_Form
from view.createConsultation_form.prentry import Ui_Prentry
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, QTime
from PyQt5.Qt import *


class createConsView(QWidget):
    create_cons_page_control_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 会诊信息表的列数
        self.col_num = 8
        self.selected_row = []

    def initView(self, on_clicked_doctor_add, on_clicked_doctor_del, createCons, set_selectRow,
                 on_clicked_history_select, getHistoryCons):
        try:
            self.tableWidget = QTableWidget()
            self.ui.verticalLayout_left.insertWidget(1, self.tableWidget)
            self.ui.verticalLayout_left.setStretch(0, 1)
            self.ui.verticalLayout_left.setStretch(1, 9)
            self.ui.docSelBtn.clicked.connect(on_clicked_doctor_add)
            self.ui.delButton.clicked.connect(on_clicked_doctor_del)
            self.ui.selectButton.clicked.connect(on_clicked_history_select)
            self.ui.historyListButton.clicked.connect(getHistoryCons)
            self.ui.verifyButton.clicked.connect(createCons)
            self.tableWidget.itemClicked.connect(set_selectRow)

            self.ui.homePage.clicked.connect(self.home_page)
            self.ui.prePage.clicked.connect(self.pre_page)
            self.ui.nextPage.clicked.connect(self.next_page)
            self.ui.finalPage.clicked.connect(self.final_page)
            self.ui.confirmSkip.clicked.connect(self.confirm_skip)
        except Exception as e:
            print('initView', e)

    def initTable(self, consInfo):
        try:
            col_num = self.col_num
            row_num = len(consInfo)
            self.tableWidget.setRowCount(row_num)
            self.tableWidget.setColumnCount(col_num)
            self.tableWidget.setInputMethodHints(Qt.ImhHiddenText)
            # 设置表格高度
            for i in range(row_num):
                self.tableWidget.setRowHeight(i, 55)
            # 设置除最后一列之外的列的宽度
            for i in range(0, col_num - 1):
                self.tableWidget.setColumnWidth(i, 150)
            self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

            # 设置列头
            col_label = ['检查单号', '病人名称', '测量日期', '开单医生', '上传医生', '状态', '会诊医生', '会诊时间']
            # 设置表头列表名称
            self.tableWidget.setHorizontalHeaderLabels(col_label)
            # 设置表头格式
            self.tableWidget.horizontalHeader().setStyleSheet(
                '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
            # 使表格填满整个widget
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            print(consInfo)
            for row in range(0, row_num):
                for col in range(self.col_num):
                    if isinstance(consInfo[row][col], datetime.date):
                        textItem = QTableWidgetItem(consInfo[row][col].strftime("%Y-%m-%d"))
                    else:
                        textItem = QTableWidgetItem(str(consInfo[row][col]))
                    textItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    textItem.setFont(QFont('', 12))
                    textItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

                    if col <= 4 and row > 0:
                        if consInfo[row][col] == consInfo[row - 1][col] and \
                                consInfo[row][0] == consInfo[row - 1][0]:
                            textItem = QTableWidgetItem('')
                            textItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tableWidget.setItem(row, col, textItem)
        except Exception as e:
            print('initTable', e)


    def initDoctorTable(self, docInfo):
        try:
            col_num = 1
            row_num = len(docInfo)
            self.ui.tableWidget2.setRowCount(row_num)
            self.ui.tableWidget2.setColumnCount(col_num)
            self.ui.tableWidget2.setInputMethodHints(Qt.ImhHiddenText)
            # 设置表格高度
            for i in range(row_num):
                self.ui.tableWidget2.setRowHeight(i, 30)
            # 设置除最后一列之外的列的宽度
            for i in range(0, col_num - 1):
                self.ui.tableWidget2.setColumnWidth(i, 150)
            self.ui.tableWidget2.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

            # 设置列头
            col_label = ['新增医生名单']
            # 设置表头列表名称
            # self.ui.tableWidget2.setHorizontalHeaderLabels(col_label)
            for i in range(len(col_label)):
                header_item = QTableWidgetItem(col_label[i])
                font = header_item.font()
                font.setPointSize(12)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                self.ui.tableWidget2.setHorizontalHeaderItem(i, header_item)
            # self.ui.tableWidget2.horizontalHeader().setHighlightSections(False)
            # self.ui.tableWidget2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            # 设置表头格式
            self.ui.tableWidget2.horizontalHeader().setStyleSheet(
                '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
            # 使表格填满整个widget
            self.ui.tableWidget2.horizontalHeader().setStretchLastSection(True)
            print(docInfo)
            for row in range(0, row_num):
                for col in range(1):
                    print(f'docInfo: {docInfo[row][col]}')
                    textItem = QTableWidgetItem(str(docInfo[row][col]))
                    textItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    textItem.setFont(QFont('', 12))
                    textItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.ui.tableWidget2.setItem(row, col, textItem)
        except Exception as e:
            print('initTable', e)


    def home_page(self):
        self.create_cons_page_control_signal.emit(["home"])

    def pre_page(self):
        self.create_cons_page_control_signal.emit(["pre"])

    def next_page(self):
        self.create_cons_page_control_signal.emit(["next"])

    def final_page(self):
        self.create_cons_page_control_signal.emit(["final"])

    def confirm_skip(self):
        self.create_cons_page_control_signal.emit(["confirm"])


class PrentryView(QWidget):
    prentry_page_control_signal = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Prentry()
        self.ui.setupUi(self)

        self.ui.prePage.clicked.connect(self.pre_page)
        self.ui.nextPage.clicked.connect(self.next_page)
        self.ui.finalPage.clicked.connect(self.final_page)
        self.ui.confirmSkip.clicked.connect(self.confirm_skip)
    
    def home_page(self):
        self.prentry_page_control_signal.emit(["home"])

    def pre_page(self):
        self.prentry_page_control_signal.emit(["pre"])

    def next_page(self):
        self.prentry_page_control_signal.emit(["next"])

    def final_page(self):
        self.prentry_page_control_signal.emit(["final"])

    def confirm_skip(self):
        self.prentry_page_control_signal.emit(["confirm"])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = createConsView()
    view.show()
    sys.exit(app.exec_())
