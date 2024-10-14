import sys
from datetime import time
from functools import partial


from PyQt5 import QtGui


from view.dataImport_form.form_change_one import Ui_DataImportForm

from PyQt5.Qt import *
from PyQt5.QtCore import  Qt,  QEvent
from PyQt5.QtGui import QBrush
import sys

from view.dataImport_form.addform import Ui_AddForm

class DataImportView(QWidget):
    def __init__(self, parent=None,):
        super().__init__(parent)
        self.ui = Ui_DataImportForm()
        self.ui.setupUi(self)
        # header表格头 field数据库表属性
        self.header = ['病人姓名', '医院单号', '检查日期', '检查描述', '开单医生','脑电上传医生', '脑电上传状态']

        self.field = ['pname', 'check_number', 'measure_date', 'description', 'pdoctorname', 'cdoctorname', 'state']

        self.header_1 = ['文件名', '状态']
        self.field_1= ['file_name', 'state']

    def initTable(self, data):
        col_num = len(self.header)
        self.ui.tableWidget.setColumnCount(col_num)
        self.data = data

        if data:
            row_num = len(data)
            self.ui.tableWidget.setRowCount(row_num)

            for i in range(col_num):
                header_item = QTableWidgetItem(self.header[i])
                font = header_item.font()
                font.setPointSize(16)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                header_item.setData(Qt.UserRole, self.field[i])
                self.ui.tableWidget.setHorizontalHeaderItem(i, header_item)

            for r in range(row_num):
                for c in range(col_num):
                    item = QTableWidgetItem(str(data[r][c + 4]))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(16)
                    item.setFont(font)
                    self.ui.tableWidget.setItem(r, c, item)
                # 添加事件过滤器到每个单元格
                self.ui.tableWidget.viewport().installEventFilter(self)

            # 设置垂直滚动条不显示
            # self.ui.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            # 不显示表格第四列
            self.ui.tableWidget.setColumnHidden(3, True)
            self.ui.tableWidget.horizontalHeader().setHighlightSections(False)
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        else:
            for i in range(col_num):
                header_item = QTableWidgetItem(self.header[i])
                font = header_item.font()
                font.setPointSize(16)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                header_item.setData(Qt.UserRole, self.field[i])
                self.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
            # 不显示表格第四列
            self.ui.tableWidget.setColumnHidden(3, True)
            self.ui.tableWidget.horizontalHeader().setHighlightSections(False)
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.ToolTip:
            pos = event.pos()
            item = self.ui.tableWidget.itemAt(pos)
            if item:
                row = self.ui.tableWidget.row(item)
                font = item.font()
                font.setPointSize(16)
                QToolTip.setFont(font)  # 确保使用应用程序的默认字体
                # QToolTip.setStyleSheet("QToolTip { font-size: 14pt; font-style: italic; background-color: yellow; }")
                QToolTip.showText(event.globalPos(), f"检查描述: \n{self.data[row][7]}")
            else:
                QToolTip.hideText()
            return True
        return False

    # def initTable(self, data):
    #     col_num = len(self.header)
    #     if data:
    #         row_num = len(data)
    #         self.ui.tableWidget.setColumnCount(col_num)
    #         self.ui.tableWidget.setRowCount(row_num)
    #         for i in range(col_num):
    #             header_item = QTableWidgetItem(self.header[i])
    #             font = header_item.font()
    #             font.setPointSize(16)
    #             header_item.setFont(font)
    #             header_item.setForeground(QBrush(Qt.black))
    #             header_item.setData(Qt.UserRole, self.field[i])
    #             self.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
    #
    #         for r in range(row_num):
    #             for c in range(col_num):
    #                 # 具体传哪一个参数在这里修改
    #                 self.item = QTableWidgetItem(str(data[r][c+4]))
    #                 self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    #                 font = self.item.font()
    #                 # font = header_item.font()
    #                 font.setPointSize(16)
    #                 self.item.setFont(font)
    #                 self.ui.tableWidget.setItem(r, c, self.item)
    #         self.ui.tableWidget.horizontalHeader().setHighlightSections(False)
    #         self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    #     else:
    #         self.ui.tableWidget.setColumnCount(col_num)
    #         # self.ui.tableWidget.setRowCount(row_num)
    #         for i in range(col_num):
    #             header_item = QTableWidgetItem(self.header[i])
    #             font = header_item.font()
    #             font.setPointSize(16)
    #             header_item.setFont(font)
    #             header_item.setForeground(QBrush(Qt.black))
    #             header_item.setData(Qt.UserRole, self.field[i])
    #             self.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
    #             self.ui.tableWidget.horizontalHeader().setHighlightSections(False)
    #             self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # 初始化第二个表格
    def initTable_1(self, data):
        col_num = len(self.header_1)
        row_num = len(data)
        self.ui.tableWidget_2.setColumnCount(col_num)
        self.ui.tableWidget_2.setRowCount(row_num)
        for i in range(col_num):
            header_item = QTableWidgetItem(self.header_1[i])
            font = header_item.font()
            font.setPointSize(16)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            header_item.setData(Qt.UserRole, self.field_1[i])
            self.ui.tableWidget_2.setHorizontalHeaderItem(i, header_item)

        for r in range(row_num):
            for c in range(col_num):
                # 具体传哪一个参数在这里修改
                self.item = QTableWidgetItem(str(data[r][c]))
                self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = self.item.font()
                # font = header_item.font()
                font.setPointSize(16)
                self.item.setFont(font)
                self.ui.tableWidget_2.setItem(r, c, self.item)
        self.ui.tableWidget_2.horizontalHeader().setHighlightSections(False)
        self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

# 添加诊断信息弹出框
class AddFormView(QWidget):
    def __init__(self, parent=None,):
        super().__init__(parent)
        self.ui = Ui_AddForm()
        self.ui.setupUi(self)

    def initTabel(self, name):
        # pass
        self.ui.label_cdoctor.setText(name)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = AddFormView()
    view.show()
    sys.exit(app.exec_())