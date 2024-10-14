import sys
from datetime import datetime
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from functools import partial

from view.createLesson_form.studentInfo import Ui_StudentInfo
from view.createLesson_form.form import Ui_Form
from view.createLesson_form.student import Ui_Student
from view.createLesson_form.lesson import Ui_Purpose
from view.createLesson_form.lessoninfo import Ui_Lessoninfo
from view.createLesson_form.diagList import Ui_diagList
from view.createLesson_form.prentry import Ui_Prentry
from view.createLesson_form.user import Ui_User

from PyQt5.QtWidgets import *

class createLessonView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 课堂信息表的列数
        self.col_num = 7

    def initView(self, on_clicked_create_lesson, on_clicked_del_lesson, set_selectRow, on_clicked_edit_lesson, on_clicked_inquiry_lesson, reset):
        try:
            self.tableWidget = QTableWidget()
            self.ui.verticalLayout.addWidget(self.tableWidget)
            self.ui.verticalLayout.setStretch(0, 1)
            self.ui.verticalLayout.setStretch(1, 9)
            self.ui.addButton.clicked.connect(on_clicked_create_lesson)
            self.ui.delButton.clicked.connect(on_clicked_del_lesson)
            self.ui.addButton_2.clicked.connect(on_clicked_edit_lesson)
            self.ui.pushButton.clicked.connect(on_clicked_inquiry_lesson)
            self.ui.pushButton_2.clicked.connect(reset)
            self.tableWidget.itemClicked.connect(set_selectRow)
        except Exception as e:
            print('initView', e)

    def initTable(self, lessonInfo, on_clicked_studentView, on_clicked_add_content, on_clicked_show_student, on_clicked_show_file):
        try:
            col_num = self.col_num
            row_num = len(lessonInfo)
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
            col_label = ['课堂名称', '学习时长', '课堂开始日期', '课堂结束日期', '课堂说明', '创建者', '操作']
            # 设置表头列表名称
            self.tableWidget.setHorizontalHeaderLabels(col_label)
            # 设置表头格式
            self.tableWidget.horizontalHeader().setStyleSheet(
                '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
            # 使表格填满整个widget
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            # print(patientInfo)
            for row in range(0, row_num):
                for col in range(0, col_num - 1):
                    if col == 5:
                        textItem = QTableWidgetItem(str(lessonInfo[row][0]))
                    else:
                        if not isinstance(lessonInfo[row][col+2], str):
                            lessonInfo[row][col+2] = str(lessonInfo[row][col+2])
                        textItem = QTableWidgetItem(lessonInfo[row][col+2])
                    textItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    textItem.setFont(QFont('', 12))
                    textItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tableWidget.setItem(row, col, textItem)
                layout = QHBoxLayout()
                self.tableWidget.setCellWidget(row, col_num - 1, QWidget())
                addstudentBtn = QPushButton('添加学员信息')
                addstudentBtn.clicked.connect(partial(on_clicked_studentView, row))
                addstudentBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                addstudentBtn.setCursor(Qt.PointingHandCursor)
                layout.addWidget(addstudentBtn)
                addContentBtn = QPushButton('添加课堂内容信息')
                addContentBtn.clicked.connect(partial(on_clicked_add_content, row))
                addContentBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                addContentBtn.setCursor(Qt.PointingHandCursor)
                layout.addWidget(addContentBtn)
                studentBtn = QPushButton('查看学员信息')
                studentBtn.clicked.connect(partial(on_clicked_show_student, row))
                studentBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                studentBtn.setCursor(Qt.PointingHandCursor)
                # studentBtn.setToolTip("创建课堂:选择病例脑电文件")
                layout.addWidget(studentBtn)
                fileBtn = QPushButton('查看课堂内容信息')
                fileBtn.clicked.connect(partial(on_clicked_show_file, row))
                fileBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                fileBtn.setCursor(Qt.PointingHandCursor)
                # studentBtn.setToolTip("创建课堂:选择病例脑电文件")
                layout.addWidget(fileBtn)
                layout.setStretch(0, 1)
                layout.setStretch(1, 1)
                layout.setStretch(2, 1)
                layout.setStretch(3, 1)
                self.tableWidget.cellWidget(row, col_num - 1).setLayout(layout)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            # 添加最后一列
            for row in range(0, row_num):
                now_time = datetime.now()
                # print(type(now_time))
                start_time = self.tableWidget.item(row, 2).text()
                start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                # print(type(start_time))
                time_difference = now_time - start_time
                time_difference = int(time_difference.total_seconds())
                # print(time_difference)
                if time_difference >= 0:
                    layout = self.tableWidget.cellWidget(row, 6).layout()
                    layout.itemAt(0).widget().setEnabled(False)
                    layout.itemAt(1).widget().setEnabled(False)
                    # layout.itemAt(0).widget().setStyleSheet("QPushButton:disabled {background-color: lightGray;}")
                    layout.itemAt(2).widget().setEnabled(True)
                    layout.itemAt(3).widget().setEnabled(True)

        except Exception as e:
            print('initTable', e)

# class lessonView(QWidget):
#     def __init__(self,  parent=None):
#         super().__init__(parent)
#         self.ui = Ui_Lesson()
#         self.ui.setupUi(self)
#         # self.selected_row = []

class studentView(QMainWindow,QWidget):
    page_control_signal = pyqtSignal(list)
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_Student()
        self.ui.setupUi(self)
        self.selected_row = []
        self.ui.pushButton_2.clicked.connect(self.__home_page)
        self.ui.pushButton_3.clicked.connect(self.__pre_page)
        self.ui.pushButton_4.clicked.connect(self.__next_page)
        self.ui.pushButton_5.clicked.connect(self.__final_page)
        self.ui.pushButton_6.clicked.connect(self.__confirm_skip)

    def initTable(self, studentInfo):
        try:
            col_num = 2
            row_num = len(studentInfo)
            self.ui.tableWidget.setRowCount(row_num)
            self.ui.tableWidget.setColumnCount(col_num)
            self.ui.tableWidget.setInputMethodHints(Qt.ImhHiddenText)
            # 设置表格高度
            for i in range(row_num):
                self.ui.tableWidget.setRowHeight(i, 55)
            # 设置除最后一列之外的列的宽度
            for i in range(0, col_num - 1):
                self.ui.tableWidget.setColumnWidth(i, 80)
            self.ui.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

            # 设置列头
            col_label = ['可选框', '学生姓名']
            # 设置表头列表名称
            self.ui.tableWidget.setHorizontalHeaderLabels(col_label)
            # 设置表头格式
            self.ui.tableWidget.horizontalHeader().setStyleSheet(
                '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
            # 使表格填满整个widget
            self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
            # print(patientInfo)
            for row in range(0, row_num):
                for col in range(1, col_num):
                    # if not isinstance(studentInfo[row][col], str):
                    #     studentInfo[row][col] = str(studentInfo[row][col])
                    textItem = QTableWidgetItem(studentInfo[row])
                    textItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    textItem.setFont(QFont('', 12))
                    textItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.ui.tableWidget.setItem(row, col, textItem)
                self.add_checkBox(row)
        except Exception as e:
            print('initTable', e)

    def __home_page(self):
        """点击首页信号"""
        self.page_control_signal.emit(["home", self.ui.label_6.text()])

    def __pre_page(self):
        """点击上一页信号"""
        self.page_control_signal.emit(["pre", self.ui.label_6.text()])

    def __next_page(self):
        """点击下一页信号"""
        self.page_control_signal.emit(["next", self.ui.label_6.text()])

    def __final_page(self):
        """尾页点击信号"""
        self.page_control_signal.emit(["final", self.ui.label_6.text()])

    def __confirm_skip(self):
        """跳转页码确定"""
        self.page_control_signal.emit(["confirm", self.ui.lineEdit_3.text()])

    def add_checkBox(self, row):
        exec('self.item_checked_{} = QCheckBox()'.format(row))
        exec('self.item_checked_{}.setCheckState(QtCore.Qt.Unchecked)'.format(row))
        exec('self.item_checked_{}.setCheckable(True)'.format(row))
        exec("self.item_checked_{}.setStyleSheet('''margin:10px''')".format(row))
        exec("self.item_checked_{}.clicked.connect(partial(self.rowSelected,{}))".format(row, row))
        exec("self.ui.tableWidget.setCellWidget({}, 0, self.item_checked_{})".format(row, row))

    # 被选择的行的列表
    def rowSelected(self, row):
        tag = eval("self.item_checked_{}.isChecked()".format(row))
        # print(tag)
        if tag:
            self.selected_row.append(row)
            self.selected_row.sort()
        else:
            if row in self.selected_row:
                self.selected_row.remove(row)
        # print(self.selected_row)

class lessonInfoView(QWidget):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_Lessoninfo()
        self.ui.setupUi(self)

class patientView(QWidget):
    page_control_signal = pyqtSignal(list)
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_diagList()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.__home_page)
        self.ui.pushButton_3.clicked.connect(self.__pre_page)
        self.ui.pushButton_4.clicked.connect(self.__next_page)
        self.ui.pushButton_5.clicked.connect(self.__final_page)
        self.ui.pushButton_6.clicked.connect(self.__confirm_skip)

    def initTable(self, viewInfo, userNamesDict, paitentNamesDict, on_clicked_add_EEG, class_id=None, create_name=None):
        try:
            self.ui.tableWidget.clear()
            self.ui.tableWidget.setHorizontalHeaderLabels(
                ["检查单号", '病人', '测量日期', '开单医生', '操作'])
            self.ui.tableWidget.removeRow(0)
            self.row_num = len(viewInfo)
            if self.row_num <= 0:
                self.ui.tableWidget.setRowCount(1)
                self.ui.tableWidget.setItem(0, 0, QTableWidgetItem("[无]"))
                self.ui.tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(0, 0).setFlags(Qt.ItemIsEditable)
                font = self.ui.tableWidget.item(0, 0).font()
                font.setPointSize(12)
                return

            self.ui.tableWidget.setRowCount(self.row_num)
            col_num = 4
            # 设置表格高度
            for i in range(self.row_num):
                self.ui.tableWidget.setRowHeight(i, 50)

            # self.ui.tableWidget.setStretchLastSection(True)
            self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)

            for row in range(0, self.row_num):
                i = 0
                self.ui.tableWidget.setItem(row, i, QTableWidgetItem(viewInfo[row][1]))
                self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                font = self.ui.tableWidget.item(row, i).font()
                font.setPointSize(12)
                i = i + 1
                if paitentNamesDict.get(viewInfo[row][2]) == None:
                    self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(viewInfo[row][2])))
                else:
                    self.ui.tableWidget.setItem(row, i, QTableWidgetItem(paitentNamesDict.get(viewInfo[row][2])))
                self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                font = self.ui.tableWidget.item(row, i).font()
                font.setPointSize(12)
                i = i + 1
                self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(viewInfo[row][5])))
                self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                font = self.ui.tableWidget.item(row, i).font()
                font.setPointSize(12)
                i = i + 1

                if userNamesDict.get(viewInfo[row][4]) == None:
                    self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(viewInfo[row][4])))
                else:
                    self.ui.tableWidget.setItem(row, i, QTableWidgetItem(userNamesDict.get(viewInfo[row][4])))
                self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                font = self.ui.tableWidget.item(row, i).font()
                font.setPointSize(12)

                # 添加最后一列
                layout = QHBoxLayout()
                self.ui.tableWidget.setCellWidget(row, col_num, QWidget())


                manualBtn = QPushButton('选择病例脑电文件')
                manualBtn.clicked.connect(partial(on_clicked_add_EEG, viewInfo[row], class_id, create_name))
                manualBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                manualBtn.setCursor(Qt.PointingHandCursor)
                manualBtn.setToolTip("创建课堂:选择病例脑电文件")
                layout.addWidget(manualBtn)
                layout.setStretch(0, 1)
                layout.setStretch(1, 1)
                self.ui.tableWidget.cellWidget(row, col_num).setLayout(layout)

        except Exception as e:
            print('initTable', e)

    def __home_page(self):
        """点击首页信号"""
        self.page_control_signal.emit(["home", self.ui.label_6.text()])

    def __pre_page(self):
        """点击上一页信号"""
        self.page_control_signal.emit(["pre", self.ui.label_6.text()])

    def __next_page(self):
        """点击下一页信号"""
        self.page_control_signal.emit(["next", self.ui.label_6.text()])

    def __final_page(self):
        """尾页点击信号"""
        self.page_control_signal.emit(["final", self.ui.label_6.text()])

    def __confirm_skip(self):
        """跳转页码确定"""
        self.page_control_signal.emit(["confirm", self.ui.lineEdit_3.text()])


class PrentryView(QWidget):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_Prentry()
        self.ui.setupUi(self)

class UserView(QWidget):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_User()
        self.ui.setupUi(self)

class PurposeView(QWidget):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_Purpose()
        self.ui.setupUi(self)

class studentInfoView(QWidget):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_StudentInfo()
        self.ui.setupUi(self)
        self.selected_row = []

    def initTable(self, studentInfo):
        try:
            col_num = 2
            row_num = len(studentInfo)
            self.ui.tableWidget.setRowCount(row_num)
            self.ui.tableWidget.setColumnCount(col_num)
            self.ui.tableWidget.setInputMethodHints(Qt.ImhHiddenText)
            # 设置表格高度
            for i in range(row_num):
                self.ui.tableWidget.setRowHeight(i, 55)
            # 设置除最后一列之外的列的宽度
            for i in range(0, col_num - 1):
                self.ui.tableWidget.setColumnWidth(i, 150)
            self.ui.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

            # 设置列头
            col_label = ['可选框', '学生姓名']
            # 设置表头列表名称
            self.ui.tableWidget.setHorizontalHeaderLabels(col_label)
            # 设置表头格式
            self.ui.tableWidget.horizontalHeader().setStyleSheet(
                '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
            # 使表格填满整个widget
            self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
            # print(patientInfo)
            for row in range(0, row_num):
                for col in range(1, col_num):
                    # if not isinstance(studentInfo[row][col], str):
                    #     studentInfo[row][col] = str(studentInfo[row][col])
                    textItem = QTableWidgetItem(studentInfo[row])
                    textItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    textItem.setFont(QFont('', 12))
                    textItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.ui.tableWidget.setItem(row, col, textItem)
                self.add_checkBox(row)
        except Exception as e:
            print('initTable', e)

    def add_checkBox(self, row):
        exec('self.item_checked_{} = QCheckBox()'.format(row))
        exec('self.item_checked_{}.setCheckState(QtCore.Qt.Unchecked)'.format(row))
        exec('self.item_checked_{}.setCheckable(True)'.format(row))
        exec("self.item_checked_{}.setStyleSheet('''margin:10px''')".format(row))
        exec("self.item_checked_{}.clicked.connect(partial(self.rowSelected,{}))".format(row, row))
        exec("self.ui.tableWidget.setCellWidget({}, 0, self.item_checked_{})".format(row, row))

    # 被选择的行的列表
    def rowSelected(self, row):
        tag = eval("self.item_checked_{}.isChecked()".format(row))
        # print(tag)
        if tag:
            self.selected_row.append(row)
            self.selected_row.sort()
        else:
            if row in self.selected_row:
                self.selected_row.remove(row)
        # print(self.selected_row)