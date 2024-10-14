import sys
from functools import partial

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtWidgets, QtCore

# from userManager_form.pwd_update_form.form import pwdUpdateView
from view.userManager_form.form import Ui_Form
from PyQt5.QtWidgets import *

class UserManagerView(QWidget):

    def __init__(self, parent=None,):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 用户信息表
        # 标志该行是否正在编辑，True为正在编辑，False为完成编辑
        self.editCheck = []

    # def on_clicked_user_edit(self, editRow, editConfirm, editCancel):
    #     print(f"editConfirm I: {editRow}")
    #     try:
    #         # col_num = 9
    #         tag = self.editCheck[editRow]
    #         if not tag:
    #             self.editCheck[editRow] = True
    #             layout1 = self.ui.tableWidget.cellWidget(editRow, 5).layout()
    #             for n in range(5):
    #                 layout1.itemAt(n).widget().setEnabled(True)
    #             for n in range(2, 5):
    #                 self.ui.tableWidget.item(editRow, n).setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
    #             layout2 = self.ui.tableWidget.cellWidget(editRow, 6).layout()
    #             layout2.itemAt(0).widget().setEnabled(False)
    #             layout2.itemAt(1).widget().setEnabled(False)
    #             layout2.itemAt(2).widget().setText('确认修改')
    #             layout2.itemAt(2).widget().setStyleSheet('margin:5px;height : 50px;width:100px;font : 18px')
    #             editCancelBtn = QPushButton('取消修改')
    #             editCancelBtn.clicked.connect(editCancel)
    #             editCancelBtn.setStyleSheet('margin:5px;height : 50px;width:60px;font : 18px')
    #             layout2.addWidget(editCancelBtn)
    #             # spaceItem_3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
    #             #                                      QtWidgets.QSizePolicy.Expanding)
    #             # layout2.addItem(spaceItem_3)
    #             layout2.setStretch(0, 1)
    #             layout2.setStretch(1, 2)
    #             layout2.setStretch(2, 2)
    #             layout2.setStretch(3, 2)
    #             layout2.setStretch(4, 8)
    #         else:
    #             check_list = []
    #             user_info = []
    #             layout = self.ui.tableWidget.cellWidget(editRow, 5).layout()
    #             for n in range(5):
    #                 result = layout.itemAt(n).widget().isChecked()
    #                 check_list.append(result)
    #                 # exec("identity_check_{}_{} = self.check{}.isChecked()".format(n + 1, editRow, n + 1, editRow))
    #                 # exec("check_list.append(identity_check_{}_{})".format(n + 1, editRow))
    #             for n in range(1, 5):
    #                 if n > 1:
    #                     self.ui.tableWidget.item(editRow, n).setFlags(Qt.ItemIsEnabled)
    #                     # exec("self.ui.tableWidget{}_{}.setFlags(Qt.ItemIsEditable)".format(editRow, n))
    #                 exec("item_{}_{} = self.ui.tableWidget.item(editRow,n).text()".format(editRow, n))
    #                 exec("user_info.append(item_{}_{})".format(editRow, n))
    #             # 将check_list的true和false转换为对应的1和0
    #             j = 0
    #             tag1 = False
    #             for k in check_list:
    #                 if k:
    #                     check_list[j] = 1
    #                     tag1 = True
    #                 else:
    #                     check_list[j] = 0
    #                 j += 1
    #             if tag1 is False:
    #                 # QPushButton.setChecked()
    #                 QMessageBox.information(self, "提示", '请至少选择一种身份', QMessageBox.Yes)
    #                 self.editCheck[editRow] = True
    #                 return
    #             # 将user_info和check_list拼接
    #             user_info.extend(check_list)
    #             # print(user_info)
    #             REQmsg = user_info
    #             editConfirm(REQmsg)
    #             for n in range(5):
    #                 exec("self.check{}.setEnabled(False)".format(n + 1, editRow))
    #
    #             exec("self.editBtn.setText('编辑')".format(editRow))
    #             self.editCheck[editRow] = False
    #             # exec("self.edit_btn_{}.toggle()".format(i))
    #             exec(
    #                 "self.editBtn.setStyleSheet('''margin:5px;height : 50px;width:60px;font : 18px''')".format(
    #                     editRow))
    #             layout2 = self.ui.tableWidget.cellWidget(editRow, 6).layout()
    #             layout2.itemAt(0).widget().setEnabled(True)
    #             layout2.itemAt(1).widget().setEnabled(True)
    #     except Exception as e:
    #         print('on_clicked_user_edit', e)


class TableWidget(QWidget):
    control_signal = pyqtSignal(list)

    def __init__(self, user_info, col_name, current_page,
                 editConfirm, editCancel, on_clicked_user_del, on_clicked_pwdUpda, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)
        self.col = len(col_name)
        self.col_name = col_name
        self.col_label = ['账号', '姓名', '电话', '邮箱', '用户身份', '操作']
        self.col_num = len(self.col_label)
        self.cur_page = current_page
        self.editCheck = []
        self.is_edit = False
        self.is_add = False
        self.table = QTableWidget()
        self.init_table(user_info, editConfirm, editCancel, on_clicked_user_del, on_clicked_pwdUpda)

    def init_table(self, user_info, editConfirm, editCancel, on_clicked_user_del, on_clicked_pwdUpda):
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
            self.row = len(user_info)
            self.table.clear()
            self.table.setRowCount(self.row)
            self.table.setColumnCount(self.col_num)
            self.table.setHorizontalHeaderLabels(self.col_label)
            # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应宽度
            self.editCheck = []
            # 设置表格高度
            for i in range(self.row):
                self.table.setRowHeight(i, 55)
            self.table.horizontalHeader().setStretchLastSection(True)
            for row in range(0, self.row):
                for i in range(0, self.col - 5):
                    # self.table.setColumnWidth(0, 50)
                    self.table.setItem(row, i, QTableWidgetItem(user_info[row][i]))
                    self.table.item(row, i).setTextAlignment(Qt.AlignCenter)
                    self.table.item(row, i).setFlags(Qt.ItemIsEditable)
                    font = self.table.item(row, i).font()
                    font.setPointSize(14)
                # 为每一行的尾部添加操作按钮
                # 先新建一个widget用来存储layout,不然存不进表中
                # 为用户身份列添加复选框
                self.table.setCellWidget(row, self.col - 5, QWidget())
                # 标注员
                self.check1 = QCheckBox()
                self.check1.setText('标注员')
                if user_info[row][self.col - 5] == 1:
                    self.check1.setChecked(True)
                else:
                    self.check1.setChecked(False)
                self.check1.setEnabled(False)
                self.check1.setStyleSheet('margin:2px;font : 14px')

                # 学员
                self.check2 = QCheckBox()
                self.check2.setText('学员')
                if user_info[row][self.col - 4] == 1:
                    self.check2.setChecked(True)
                else:
                    self.check2.setChecked(False)
                self.check2.setEnabled(False)
                self.check2.setStyleSheet('margin:2px;font : 14px')

                # 培训导师
                self.check3 = QCheckBox()
                self.check3.setText('培训导师')
                if user_info[row][self.col - 3] == 1:
                    self.check3.setChecked(True)
                else:
                    self.check3.setChecked(False)
                self.check3.setEnabled(False)
                self.check3.setStyleSheet('margin:2px;font : 14px')

                # 医生
                self.check4 = QCheckBox()
                self.check4.setText('医生')
                if user_info[row][self.col - 2] == 1:
                    self.check4.setChecked(True)
                else:
                    self.check4.setChecked(False)
                self.check4.setEnabled(False)
                self.check4.setStyleSheet('margin:2px;font : 14px')

                # 研究员
                self.check5 = QCheckBox()
                self.check5.setText('研究员')
                if user_info[row][self.col - 1] == 1:
                    self.check5.setChecked(True)
                else:
                    self.check5.setChecked(False)
                self.check5.setEnabled(False)
                self.check5.setStyleSheet('margin:2px;font : 14px')
                layout = QHBoxLayout()
                layout.addWidget(self.check1)
                layout.addWidget(self.check2)
                layout.addWidget(self.check3)
                layout.addWidget(self.check4)
                layout.addWidget(self.check5)
                layout.setStretch(0, 3)
                layout.setStretch(1, 2)
                layout.setStretch(2, 4)
                layout.setStretch(3, 2)
                layout.setStretch(4, 3)
                self.table.setColumnWidth(0, 150)
                self.table.setColumnWidth(1, 150)
                self.table.setColumnWidth(2, 200)
                self.table.setColumnWidth(3, 200)
                self.table.setColumnWidth(4, 600)
                self.table.setColumnWidth(5, 400)
                self.table.cellWidget(row, self.col - 5).setLayout(layout)

                # 添加最后一列
                self.table.setCellWidget(row, self.col - 4, QWidget())
                self.editCheck.append(False)
                self.editBtn = QPushButton('编辑')
                delBtn = QPushButton('删除')
                self.pwdUpdaBtn = QPushButton('密码修改')
                self.pwdUpdaBtn.clicked.connect(partial(on_clicked_pwdUpda, row))
                self.editBtn.clicked.connect(partial(self.on_clicked_user_edit, row, editConfirm, editCancel))
                delBtn.clicked.connect(partial(on_clicked_user_del, row))
                self.editBtn.setStyleSheet('margin:5px;height : 50px;width:60px;font : 18px')
                delBtn.setStyleSheet('margin:5px;height : 50px;width:60px;font : 18px')
                self.pwdUpdaBtn.setStyleSheet('margin:5px;height : 50px;width:100px;font : 18px')
                layout = QHBoxLayout()
                layout.addWidget(delBtn)
                layout.addWidget(self.pwdUpdaBtn)
                layout.addWidget(self.editBtn)
                # spaceItem_3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                #                                     QtWidgets.QSizePolicy.Expanding)
                # layout.addItem(spaceItem_3)
                layout.setStretch(0, 1)
                layout.setStretch(1, 1)
                layout.setStretch(2, 1)
                layout.setStretch(3, 8)
                self.table.cellWidget(row, self.col - 4).setLayout(layout)
            self.__layout = QVBoxLayout()
            self.__layout.addWidget(self.table)
            self.setLayout(self.__layout)
            self.setStyleSheet(style_sheet)
        except Exception as e:
            print('init_table', e)


    def setPageController(self, page):
        """自定义页码控制器"""
        control_layout = QHBoxLayout()
        homePage = QPushButton("首页")
        prePage = QPushButton("<上一页")
        self.curPage = QLabel(str(self.cur_page))
        nextPage = QPushButton("下一页>")
        finalPage = QPushButton("尾页")
        self.totalPage = QLabel("共" + str(page) + "页")
        skipLable_0 = QLabel("跳到")
        self.skipPage = QLineEdit()
        skipLabel_1 = QLabel("页")
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

    def on_clicked_user_edit(self, editRow, editConfirm, editCancel):
        print(f"editConfirm I: {editRow}")
        try:
            # col_num = 9
            tag = self.editCheck[editRow]
            if not tag:
                if self.is_edit:
                    QMessageBox.information(self, '提示', '请先完成编辑')
                    return
                if self.is_add:
                    QMessageBox.information(self, '提示', '请先完成添加')
                    return
                self.is_edit = True
                self.editCheck[editRow] = True
                layout1 = self.table.cellWidget(editRow, 4).layout()
                for n in range(5):
                    layout1.itemAt(n).widget().setEnabled(True)
                for n in range(1, 4):
                    self.table.item(editRow, n).setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
                layout2 = self.table.cellWidget(editRow, 5).layout()
                layout2.itemAt(0).widget().setEnabled(False)
                layout2.itemAt(1).widget().setEnabled(False)
                layout2.itemAt(2).widget().setText('确认修改')
                layout2.itemAt(2).widget().setStyleSheet('margin:5px;height : 50px;width:100px;font : 18px')
                editCancelBtn = QPushButton('取消修改')
                editCancelBtn.clicked.connect(editCancel)
                editCancelBtn.setStyleSheet('margin:5px;height : 50px;width:100px;font : 18px')
                layout2.addWidget(editCancelBtn)
                # spaceItem_3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                #                                      QtWidgets.QSizePolicy.Expanding)
                # layout2.addItem(spaceItem_3)
                layout2.setStretch(0, 1)
                layout2.setStretch(1, 2)
                layout2.setStretch(2, 2)
                layout2.setStretch(3, 2)
                layout2.setStretch(4, 8)
            else:
                check_list = []
                user_info = []
                layout = self.table.cellWidget(editRow, 4).layout()
                for n in range(5):
                    result = layout.itemAt(n).widget().isChecked()
                    check_list.append(result)
                    # exec("identity_check_{}_{} = self.check{}.isChecked()".format(n + 1, editRow, n + 1, editRow))
                    # exec("check_list.append(identity_check_{}_{})".format(n + 1, editRow))
                for n in range(0, 4):
                    if n > 1:
                        self.table.item(editRow, n).setFlags(Qt.ItemIsEnabled)
                    exec("item_{}_{} = self.table.item(editRow,n).text()".format(editRow, n))
                    exec("user_info.append(item_{}_{})".format(editRow, n))
                # 将check_list的true和false转换为对应的1和0
                j = 0
                tag1 = False
                for k in check_list:
                    if k:
                        check_list[j] = 1
                        tag1 = True
                    else:
                        check_list[j] = 0
                    j += 1
                if tag1 is False:
                    # QPushButton.setChecked()
                    QMessageBox.information(self, "提示", '请至少选择一种身份', QMessageBox.Yes)
                    self.editCheck[editRow] = True
                    return
                labeller = check_list[0]
                student = check_list[1]
                teacher = check_list[2]
                doctor = check_list[3]
                researcher = check_list[4]
                if labeller == 1:
                    if student == 1 or teacher == 1 or doctor == 1 or researcher == 1:
                        QMessageBox.information(self, "提示", '标注员角色的用户只能具有标注员角色', QMessageBox.Yes)
                        return
                elif student == 1:
                    if labeller == 1 or teacher == 1 or doctor == 1 or researcher == 1:
                        QMessageBox.information(self, "提示", '学员角色的用户只能具有学员角色', QMessageBox.Yes)
                        return
                elif doctor == 1:
                    if labeller == 1 or student == 1:
                        QMessageBox.information(self, "提示", '医生角色的用户只能同时具有培训导师和研究员两种角色',
                                                QMessageBox.Yes)
                        return
                elif teacher == 1:
                    if labeller == 1 or student == 1 or doctor == 1 or researcher == 1:
                        QMessageBox.information(self, "提示", '只有医生角色的用户可以同时具有培训导师和研究员两种角色',
                                                QMessageBox.Yes)
                        return
                elif researcher == 1:
                    if labeller == 1 or student == 1 or doctor == 1 or teacher == 1:
                        QMessageBox.information(self, "提示", '只有医生角色的用户可以同时具有培训导师和研究员两种角色',
                                                QMessageBox.Yes)
                        return
                # 将user_info和check_list拼接
                user_info.extend(check_list)
                # print(user_info)
                REQmsg = user_info
                editConfirm(REQmsg)
                layout1 = self.table.cellWidget(editRow, 4).layout()
                for n in range(5):
                    layout1.itemAt(n).widget().setEnabled(False)

                exec("self.editBtn.setText('编辑')".format(editRow))
                self.editCheck[editRow] = False
                # exec("self.edit_btn_{}.toggle()".format(i))
                exec(
                    "self.editBtn.setStyleSheet('''margin:5px;height : 50px;width:60px;font : 18px''')".format(
                        editRow))
                layout2 = self.table.cellWidget(editRow, 5).layout()
                layout2.itemAt(0).widget().setEnabled(True)
                layout2.itemAt(1).widget().setEnabled(True)
        except Exception as e:
            print('on_clicked_user_edit', e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = UserManagerView()
    view.show()
    sys.exit(app.exec_())
