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
        self.header = ['病人姓名', '医院单号', '检查日期', '检查描述', '开单医生', '脑电上传医生', '操作']
        self.field = ['pname', 'check_number', 'measure_date', 'description', 'pdoctorname', 'cdoctorname', 'actions']

        self.header_1 = ['文件名','状态','操作']
        self.field_1 = ['file_name','state','actions']

        self.header_2 = ['文件名', '状态']
        self.field_2 = ['file_name', 'state']

    def initTable(self, data, on_btnAddFile_clicked=None, on_btnRemove_clicked=None, on_btnComplete_clicked=None):
        col_num = len(self.header)
        self.ui.tableWidget.setColumnCount(col_num)
        self.data = data

        # 存储每行的按钮引用
        self.row_buttons = []

        if data:
            row_num = len(data)
            self.ui.tableWidget.setRowCount(row_num)

            # 设置表头
            for i in range(col_num):
                header_item = QTableWidgetItem(self.header[i])
                font = header_item.font()
                font.setPointSize(16)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                header_item.setData(Qt.UserRole, self.field[i])
                self.ui.tableWidget.setHorizontalHeaderItem(i, header_item)

            # 填充表格数据和按钮
            for r in range(row_num):
                for c in range(col_num - 1):  # 不包括“操作”列
                    item = QTableWidgetItem(str(data[r][c + 4]))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(16)
                    item.setFont(font)
                    # 禁用编辑
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 使文本不可编辑
                    self.ui.tableWidget.setItem(r, c, item)

                # 在最后一列添加按钮
                action_widget = QWidget()
                layout = QHBoxLayout(action_widget)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(5)

                addFileButton = QPushButton("添加")
                addFileButton.clicked.connect(partial(on_btnAddFile_clicked, r))
                removeButton = QPushButton("删除")
                removeButton.clicked.connect(partial(on_btnRemove_clicked, r))
                completeButton = QPushButton("完成")
                completeButton.clicked.connect(partial(on_btnComplete_clicked, r))

                layout.addWidget(addFileButton)
                layout.addWidget(removeButton)
                layout.addWidget(completeButton)
                self.ui.tableWidget.setCellWidget(r, col_num - 1, action_widget)

                # 保存按钮引用
                self.row_buttons.append((addFileButton, removeButton, completeButton))

            # 监听选中行更改
            self.ui.tableWidget.currentCellChanged.connect(self.updateButtonStates)

            # 不显示表格第四列
            self.ui.tableWidget.setColumnHidden(3, True)
            self.ui.tableWidget.horizontalHeader().setHighlightSections(False)
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        else:
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.setColumnCount(0)  # 隐藏所有列，包括表头


    def updateButtonStates(self, currentRow, currentColumn, previousRow, previousColumn):
        for row_index, (addButton, removeButton, completeButton) in enumerate(self.row_buttons):
            is_current_row = row_index == currentRow
            addButton.setEnabled(is_current_row)
            removeButton.setEnabled(is_current_row)
            completeButton.setEnabled(is_current_row)

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


    def initTable_1(self, data ,on_btnDelFile_clicked = None):
        col_num = len(self.header_1)
        row_num = len(data)
        self.ui.tableWidget_1.setColumnCount(col_num)
        self.ui.tableWidget_1.setRowCount(row_num)
        # 设置表头
        for i in range(col_num):
            header_item = QTableWidgetItem(self.header_1[i])
            font = header_item.font()
            font.setPointSize(16)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            header_item.setData(Qt.UserRole, self.field_1[i])
            self.ui.tableWidget_1.setHorizontalHeaderItem(i, header_item)

        # 填充表格数据和按钮
        for r in range(row_num):
            for c in range(col_num - 1): # 不包括“操作”列
                # 具体传哪一个参数在这里修改
                item = QTableWidgetItem(str(data[r][c]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                # font = header_item.font()
                font.setPointSize(16)
                item.setFont(font)

                # 禁用编辑功能
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 禁止编辑

                self.ui.tableWidget_1.setItem(r, c, item)

                # 设置 tooltip 显示完整的文件名
                if c == 0:
                    item.setToolTip(str(data[r][c]))  # 设置 tooltip 为文件名，鼠标悬停时会显示完整文件名

                self.ui.tableWidget_1.setItem(r, c, item)

                # 在最后一列添加按钮
                action_widget = QWidget()
                layout = QHBoxLayout(action_widget)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(5)

                delFileButton = QPushButton("删除")

                # 可以根据需要添加按钮点击事件
                delFileButton.clicked.connect(partial(on_btnDelFile_clicked,  r))

                layout.addWidget(delFileButton)

                self.ui.tableWidget_1.setCellWidget(r, col_num - 1, action_widget)

        self.ui.tableWidget_1.horizontalHeader().setHighlightSections(False)
        self.ui.tableWidget_1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    # 初始化第三个表格
    def initTable_2(self, data):
        col_num = len(self.header_2)
        row_num = len(data)
        self.ui.tableWidget_2.setColumnCount(col_num)
        self.ui.tableWidget_2.setRowCount(row_num)
        for i in range(col_num):
            header_item = QTableWidgetItem(self.header_2[i])
            font = header_item.font()
            font.setPointSize(16)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            header_item.setData(Qt.UserRole, self.field_2[i])
            self.ui.tableWidget_2.setHorizontalHeaderItem(i, header_item)

        for r in range(row_num):
            for c in range(col_num):
                # 具体传哪一个参数在这里修改
                item = QTableWidgetItem(str(data[r][c]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                # font = header_item.font()
                font.setPointSize(16)
                item.setFont(font)

                # 禁用编辑功能
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 禁止编辑

                self.ui.tableWidget_2.setItem(r, c, item)

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