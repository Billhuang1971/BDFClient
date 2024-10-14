import sys
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore

from view.basicConfig_form.form import Ui_Form
from PyQt5.QtWidgets import *


class BasicConfigView(QWidget):

    def __init__(self, parent=None, ):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 用户信息表
        # 标志该行是否正在编辑，True为正在编辑，False为完成编辑
        self.editCheck = []

    def refresh(self, configInfo, updateBasicConfig, editCancel, on_clicked_user_del):
        try:
            self.editCheck = []
            col_num = 7
            self.row_num = len(configInfo)
            print(f'row_num: {self.row_num}')
            self.ui.tableWidget.setRowCount(self.row_num)
            # 设置表格高度
            for i in range(self.row_num):
                self.ui.tableWidget.setRowHeight(i, 55)

            self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
            for row in range(0, self.row_num):
                print(f'configInfo: {configInfo[row]}')
                for i in range(0, col_num - 2):
                    self.ui.tableWidget.setColumnWidth(0, 50)
                    self.ui.tableWidget.setItem(row, i + 1, QTableWidgetItem(str(configInfo[row][i + 1])))
                    self.ui.tableWidget.item(row, i + 1).setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget.item(row, i + 1).setFlags(Qt.ItemIsEditable)
                    font = self.ui.tableWidget.item(row, i + 1).font()
                    font.setPointSize(12)
                # 为每一行的头部添加复选框
                self.ui.tableWidget.setCellWidget(row, 0, QCheckBox())
                self.checkBox = self.ui.tableWidget.cellWidget(row, 0)
                self.checkBox.setCheckState(QtCore.Qt.Unchecked)
                self.checkBox.setCheckable(True)
                self.checkBox.setStyleSheet('margin:10px')

                self.ui.tableWidget.setCellWidget(row, 6, QCheckBox())
                self.checkBox = self.ui.tableWidget.cellWidget(row, 6)
                self.checkBox.setCheckState(QtCore.Qt.Unchecked)
                self.checkBox.setEnabled(False)
                if configInfo[row][6] == 1:
                    self.checkBox.setChecked(True)
                else:
                    self.checkBox.setChecked(False)
                self.checkBox.setStyleSheet('margin:10px')


                self.ui.tableWidget.setColumnWidth(1, 150)
                self.ui.tableWidget.setColumnWidth(2, 200)
                self.ui.tableWidget.setColumnWidth(3, 200)
                self.ui.tableWidget.setColumnWidth(4, 200)
                self.ui.tableWidget.setColumnWidth(5, 200)
                self.ui.tableWidget.setColumnWidth(6, 100)


                # 为每一行的尾部添加操作按钮
                # 先新建一个widget用来存储layout,不然存不进表中
                # # 添加最后一列
                self.ui.tableWidget.setCellWidget(row, col_num, QWidget())
                self.editCheck.append(False)
                self.editBtn = QPushButton('编辑')
                self.delBtn = QPushButton('删除')

                self.editBtn.clicked.connect(partial(self.on_clicked_user_edit, row, updateBasicConfig, editCancel))
                self.delBtn.clicked.connect(partial(on_clicked_user_del, row))
                self.editBtn.setStyleSheet('margin:5px;height : 50px;width:60px;font : 18px')
                self.delBtn.setStyleSheet('margin:5px;height : 50px;width:60px;font : 18px')
                layout = QHBoxLayout()
                layout.addWidget(self.delBtn)
                layout.addWidget(self.editBtn)
                layout.setStretch(0, 1)
                layout.setStretch(1, 1)
                layout.setStretch(2, 8)
                self.ui.tableWidget.cellWidget(row, col_num).setLayout(layout)
        except Exception as e:
            print('initTable', e)

    def on_clicked_user_edit(self, editRow, updateBasicConfig, editCancel):
        print(f"editConfirm I: {editRow}")
        try:
            tag = self.editCheck[editRow]
            if not tag:
                self.editCheck[editRow] = True
                for n in range(1, 6):
                    self.ui.tableWidget.item(editRow, n).setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
                layout2 = self.ui.tableWidget.cellWidget(editRow, 7).layout()
                self.checkBox = self.ui.tableWidget.cellWidget(editRow, 6)
                if not self.checkBox.isChecked():
                    self.checkBox.setCheckable(True)
                    self.checkBox.setEnabled(True)
                layout2.itemAt(0).widget().setEnabled(False)
                layout2.itemAt(1).widget().setText('确认修改')
                layout2.itemAt(1).widget().setStyleSheet('margin:5px;height : 50px;width:100px;font : 18px')
                editCancelBtn = QPushButton('取消修改')
                editCancelBtn.clicked.connect(editCancel)
                editCancelBtn.setStyleSheet('margin:5px;height : 50px;width:60px;font : 18px')
                layout2.addWidget(editCancelBtn)
                layout2.setStretch(0, 1)
                layout2.setStretch(1, 2)
                layout2.setStretch(2, 2)
                layout2.setStretch(3, 2)
                layout2.setStretch(4, 8)
            else:
                updateBasicConfig(editRow)
                for n in range(1, 5):
                    self.ui.tableWidget.item(editRow, n).setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
        except Exception as e:
            print('on_clicked_user_edit', e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = BasicConfigView()
    view.show()
    sys.exit(app.exec_())
