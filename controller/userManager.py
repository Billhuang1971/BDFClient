#!/usr/bin/python
# author bluenor
from PyQt5.QtCore import Qt

from view.userManager_form.pwd_update_form.form import pwdUpdateView
from util.clientAppUtil import clientAppUtil
from view.userManager import UserManagerView, TableWidget
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from functools import partial
import sys
import numpy as np


class userManagerController(QWidget):
    update_done_signal = QtCore.pyqtSignal(list)

    def __init__(self, client, cAppUtil):
        super().__init__()
        self.client = client
        self.cAppUtil = cAppUtil
        self.view = UserManagerView()
        self.client.addUserInfoResSig.connect(self.addUserInfoRes)
        self.client.delUserInfoResSig.connect(self.delUserInfoRes)
        self.client.updateUserInfoResSig.connect(self.updateUserInfoRes)
        self.client.getUserInfoResSig.connect(self.getUserInfoRes)
        self.client.userPagingResSig.connect(self.userPagingRes)
        self.client.inquiryUserInfoResSig.connect(self.inquiryUserInfoRes)
        self.view.ui.pushButton.clicked.connect(self.on_clicked_user_add)
        self.view.ui.pushButton_2.clicked.connect(self.on_clicked_user_query)
        self.view.ui.pushButton_3.clicked.connect(self.reset)
        self.curPageIndex = 1
        self.pageRows = 12
        self.curPageMax = 1
        # 用户信息表
        # 标志该行是否正在编辑，True为正在编辑，False为完成编辑
        # self.editCheck = []
        # 存放当前用户信息的列表
        self.userInfo = []
        self.searchInfo = []
        self.tableWidget = None
        self.key_word = None
        self.key_value = None
        self.isSearch = False
        self.searchPage = 1
        self.searchPageMax = 1
        # 数据库用户表的列名
        self.col_name = ['account', 'name', 'phone', 'email', 'labeler', 'student', 'teacher', 'doctor', 'researcher']
        self.col_num = len(self.col_name)
        self.client.getUserInfo([self.curPageIndex, self.pageRows, False])

    def reset(self):
        try:
            if self.tableWidget.is_edit:
                QMessageBox.information(self, '提示', '请先完成编辑')
                return
            if self.tableWidget.is_add:
                QMessageBox.information(self, '提示', '请先完成添加')
                return
            self.curPageIndex = 1
            self.key_word = None
            self.key_value = None
            self.isSearch = False
            self.searchPage = 1
            self.searchPageMax = 1
            self.curPageMax = 1
            self.client.getUserInfo([self.curPageIndex, self.pageRows, True])
        except Exception as e:
            print('reset', e)

    def on_clicked_user_query(self):
        if self.tableWidget.is_edit:
            QMessageBox.information(self, '提示', '请先完成编辑')
            return
        if self.tableWidget.is_add:
            QMessageBox.information(self, '提示', '请先完成添加')
            return
        self.key_word = self.view.ui.comboBox.currentText()
        self.key_value = self.view.ui.lineEdit.text()
        self.searchInfo.clear()
        if self.key_value == '':
            QMessageBox.information(self, '提示', '请输入要搜索的用户信息', QMessageBox.Yes)
            return
        if self.key_word == '姓名':
            self.key_word = 'name'
        elif self.key_word == '账号':
            self.key_word = 'account'
        elif self.key_word == '电话':
            self.key_word = 'phone'
        elif self.key_word == '邮箱':
            self.key_word = 'email'
        REQmsg = [self.key_word, self.key_value, self.searchPage, self.pageRows]
        self.client.inquiryUserInfo(REQmsg)

    def inquiryUserInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.isSearch = True
                self.searchPageMax = REPData[3]
                print(REPData[3])
                user_info = []
                user_info_1 = REPData[2]
                for i in user_info_1:
                    temp = i[1]
                    temp_list_1 = [temp]
                    temp_list_2 = list(i)[3:6]
                    temp_list_3 = list(i)[7:]
                    temp_list_1.extend(temp_list_2)
                    temp_list_1.extend(temp_list_3)
                    user_info.append(temp_list_1)
                print(user_info)
                self.searchInfo = user_info
                self.clear(self.view.ui.verticalLayout_3)
                self.tableWidget = TableWidget(self.searchInfo, self.col_name, self.searchPage,
                                               self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                               self.on_clicked_pwdUpda)
                self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.searchPageMax)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
                QMessageBox.information(self, '提示', '查询用户信息成功', QMessageBox.Ok)
                # self.view.ui.pushButton_2.setText('取消查询')
            else:
                self.view.ui.lineEdit.clear()
                QMessageBox.information(self, '提示', '查询用户信息失败', QMessageBox.Ok)
        except Exception as e:
            print('inqPatientInfoRes', e)

    # 处理客户端传回的用户信息
    def getUserInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.curPageMax = REPData[3]
                reset = REPData[4]
                user_info = []
                user_info_1 = REPData[2][1:]
                for i in user_info_1:
                    temp = i[1]
                    temp_list_1 = [temp]
                    temp_list_2 = list(i)[3:6]
                    temp_list_3 = list(i)[7:]
                    temp_list_1.extend(temp_list_2)
                    temp_list_1.extend(temp_list_3)
                    user_info.append(temp_list_1)
                print(user_info)
                if reset:
                    self.isSearch = False
                    self.searchInfo.clear()
                    self.userInfo.clear()
                    self.view.ui.lineEdit.clear()
                    self.clear(self.view.ui.verticalLayout_3)
                    self.userInfo = user_info
                    self.tableWidget = TableWidget(self.userInfo, self.col_name, self.curPageIndex,
                                                    self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                                   self.on_clicked_pwdUpda)
                    self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
                    QMessageBox.information(self, '提示', '刷新页面成功', QMessageBox.Ok)
                else:
                    self.userInfo = user_info
                    self.tableWidget = TableWidget(self.userInfo, self.col_name, self.curPageIndex,
                                                   self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                                   self.on_clicked_pwdUpda)
                    self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
                # self.view.ui.verticalLayout.setStretch(0, 1)
                # self.view.ui.verticalLayout.setStretch(1, 12)
            else:
                QMessageBox.information(self, '提示', '获取用户信息失败', QMessageBox.Ok)
        except Exception as e:
            print('getUserInfoRes', e)

    def page_controller(self, signal):
        try:
            if "home" == signal[0]:
                if self.isSearch == False:
                    if self.curPageIndex == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.curPageIndex = 1
                    self.tableWidget.curPage.setText(str(self.curPageIndex))
                else:
                    if self.searchPage == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.searchPage = 1
                    self.tableWidget.curPage.setText(str(self.searchPage))
            elif "pre" == signal[0]:
                if self.isSearch == False:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.curPageIndex <= 1:
                        return
                    self.curPageIndex = self.curPageIndex - 1
                    self.tableWidget.curPage.setText(str(self.curPageIndex))
                else:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.searchPage <= 1:
                        return
                    self.searchPage = self.searchPage - 1
                    self.tableWidget.curPage.setText(str(self.searchPage))
            elif "next" == signal[0]:
                if self.isSearch == False:
                    if self.curPageMax == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.curPageIndex = self.curPageIndex + 1
                    self.tableWidget.curPage.setText(str(self.curPageIndex))
                else:
                    if self.searchPageMax == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.searchPage = self.searchPage + 1
                    self.tableWidget.curPage.setText(str(self.searchPage))
            elif "final" == signal[0]:
                if self.isSearch == False:
                    if self.curPageIndex == self.curPageMax:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.curPageIndex = self.curPageMax
                    self.tableWidget.curPage.setText(str(self.curPageMax))
                else:
                    if self.searchPage == self.searchPageMax:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.searchPage = self.searchPageMax
                    self.tableWidget.curPage.setText(str(self.searchPageMax))
            elif "confirm" == signal[0]:
                if self.isSearch == False:
                    if self.curPageIndex == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.curPageMax < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.curPageIndex = int(signal[1])
                    self.tableWidget.curPage.setText(signal[1])
                else:
                    if self.searchPage == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.searchPageMax < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.searchPage = int(signal[1])
                    self.tableWidget.curPage.setText(signal[1])
            if self.isSearch == False:
                msg = [self.curPageIndex, self.pageRows, signal[0], self.isSearch]
            else:
                msg = [self.searchPage, self.pageRows, signal[0], self.isSearch, self.key_word, self.key_value]
            self.client.userPaging(msg)
        except Exception as e:
            print('page_controller', e)

    def userPagingRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "提示", "跳转页面失败", QMessageBox.Yes)
            else:
                isSearch = REPData[3]
                if isSearch:
                    user_info = []
                    user_info_1 = REPData[2][0:]
                    for i in user_info_1:
                        temp = i[1]
                        temp_list_1 = [temp]
                        temp_list_2 = list(i)[3:6]
                        temp_list_3 = list(i)[7:]
                        temp_list_1.extend(temp_list_2)
                        temp_list_1.extend(temp_list_3)
                        user_info.append(temp_list_1)
                    print(user_info)
                    self.searchInfo = user_info
                    self.clear(self.view.ui.verticalLayout_3)
                    self.tableWidget = TableWidget(self.searchInfo, self.col_name, self.searchPage,
                                                   self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                                   self.on_clicked_pwdUpda)
                    self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.searchPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
                else:
                    user_info = []
                    if self.curPageIndex == 1:
                        user_info_1 = REPData[2][1:]
                    else:
                        user_info_1 = REPData[2][0:]
                    for i in user_info_1:
                        temp = i[1]
                        temp_list_1 = [temp]
                        temp_list_2 = list(i)[3:6]
                        temp_list_3 = list(i)[7:]
                        temp_list_1.extend(temp_list_2)
                        temp_list_1.extend(temp_list_3)
                        user_info.append(temp_list_1)
                    print(user_info)
                    self.userInfo = user_info
                    self.clear(self.view.ui.verticalLayout_3)
                    self.tableWidget = TableWidget(self.userInfo, self.col_name, self.curPageIndex,
                                                   self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                                   self.on_clicked_pwdUpda)
                    self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
        except Exception as e:
            print('userPagingRes', e)

    def clear(self, layout, num=0, count=-1):
        item_list = list(range(layout.count()))
        item_list.reverse()
        # print(item_list)
        j = 0
        for i in item_list:
            if num == 0 and count == -1:
                item = layout.itemAt(i)
                layout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
            elif num != 0 and count == -1:
                item = layout.itemAt(i)
                layout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
                j += 1
                if j == num:
                    return
            elif num == 0 and count != -1:
                if j == count:
                    item = layout.itemAt(i)
                    layout.removeItem(item)
                    if item.widget():
                        item.widget().deleteLater()
                    return
                j += 1

    # 用户编辑功能
    # 向客户端发送更新用户信息的请求
    def editConfirm(self, REQmsg):
        REQmsg.append(self.isSearch)
        self.client.updateUserInfo(REQmsg)

    def editCancel(self):
        try:
            reply = QMessageBox.information(self, "提示", '是否取消编辑', QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                self.clear(self.view.ui.verticalLayout_3)
                self.tableWidget = TableWidget(self.userInfo, self.col_name, self.curPageIndex,
                                               self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                               self.on_clicked_pwdUpda)
                self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
                self.tableWidget.is_edit = False
        except Exception as e:
            print('editCancel', e)

    # 处理客户端传回的更新用户信息结果
    def updateUserInfoRes(self,REPDATA):
        try:
            if REPDATA[2][0] == True:
                if REPDATA[0] == '1':
                    self.update_done_signal.emit([True, 0])
                elif REPDATA[0] == '0' and REPDATA[2][3] == 0:
                    self.update_done_signal.emit([False, 0])
                elif REPDATA[0] == '0' and REPDATA[2][3] == 1:
                    self.update_done_signal.emit([False, 1])
            else:
                if REPDATA[0] == '1':
                    isSearch = REPDATA[2][9]
                    if isSearch:
                        QMessageBox.information(self, "提示", "更新用户信息成功", QMessageBox.Yes)
                        user_info_m = REPDATA[2]
                        for i in self.searchInfo:
                            if i[0] == user_info_m[0]:
                                for j in range(1, 9):
                                    i[j] = user_info_m[j]
                        self.clear(self.view.ui.verticalLayout_3)
                        self.tableWidget = TableWidget(self.searchInfo, self.col_name, self.searchPage,
                                                       self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                                       self.on_clicked_pwdUpda)
                        self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
                        self.tableWidget.setPageController(self.searchPageMax)  # 表格设置页码控制
                        self.tableWidget.control_signal.connect(self.page_controller)
                    else:
                        QMessageBox.information(self, "提示", "更新用户信息成功", QMessageBox.Yes)
                        user_info_m = REPDATA[2]
                        for i in self.userInfo:
                            if i[0] == user_info_m[0]:
                                for j in range(1, 9):
                                    i[j] = user_info_m[j]
                        self.clear(self.view.ui.verticalLayout_3)
                        self.tableWidget = TableWidget(self.userInfo, self.col_name, self.curPageIndex,
                                                       self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                                       self.on_clicked_pwdUpda)
                        self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
                        self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                        self.tableWidget.control_signal.connect(self.page_controller)
                elif REPDATA[0] == '0':
                    QMessageBox.information(self, "提示", "该用户已经在线,无法修改信息", QMessageBox.Yes)
                    self.clear(self.view.ui.verticalLayout_3)
                    self.tableWidget = TableWidget(self.userInfo, self.col_name, self.curPageIndex,
                                                   self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                                   self.on_clicked_pwdUpda)
                    self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
            self.tableWidget.is_edit = False
        except Exception as e:
            print("updateUserInfo", e)

    # 用户删除
    # 处理删除用户信息方法
    def on_clicked_user_del(self, i):
        try:
            if self.tableWidget.is_edit:
                QMessageBox.information(self, '提示', '请先完成编辑')
                return
            if self.tableWidget.is_add:
                QMessageBox.information(self, '提示', '请先完成添加')
                return
            if self.curPageMax == 1 and len(self.userInfo) == 1:
                QMessageBox.information(self, "提示", "至少保留一个用户", QMessageBox.Yes)
                return
            reply = QMessageBox.question(self, "用户删除", "是否删除该用户", QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                delIndex = i
                if self.isSearch:
                    REQmsg = ['account', self.searchInfo[i][0], delIndex, self.searchPage, self.isSearch,
                              self.key_word, self.key_value]
                else:
                    REQmsg = ['account', self.userInfo[i][0], delIndex, self.curPageIndex, self.isSearch]
                # 调用客户端删除用户信息方法
                self.client.delUserInfo(REQmsg)
        except Exception as e:
            print('on_clicked_user_del', e)

    # 处理客户端传回的删除用户信息结果
    def delUserInfoRes(self,REPDATA):
        try:
            if REPDATA[0] == '1':
                isSearch = REPDATA[6]
                curPage = REPDATA[5]
                maxPage = REPDATA[4]
                if isSearch:
                    QMessageBox.information(self, "提示", "删除用户信息成功", QMessageBox.Yes)
                    self.searchInfo.clear()
                    user_info = []
                    self.searchPage = curPage
                    user_info_1 = REPDATA[3][0:]
                    for i in user_info_1:
                        temp = i[1]
                        temp_list_1 = [temp]
                        temp_list_2 = list(i)[3:6]
                        temp_list_3 = list(i)[7:]
                        temp_list_1.extend(temp_list_2)
                        temp_list_1.extend(temp_list_3)
                        user_info.append(temp_list_1)
                    print(user_info)
                    self.searchInfo = user_info
                    self.searchPageMax = maxPage
                    if self.searchPageMax == 0:
                        self.searchPageMax = 1
                    self.clear(self.view.ui.verticalLayout_3)
                    self.tableWidget = TableWidget(self.searchInfo, self.col_name, self.searchPage,
                                                   self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                                   self.on_clicked_pwdUpda)
                    self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.searchPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
                else:
                    QMessageBox.information(self, "提示", "删除用户信息成功", QMessageBox.Yes)
                    self.userInfo.clear()
                    user_info = []
                    self.curPageIndex = curPage
                    if self.curPageIndex == 1:
                        user_info_1 = REPDATA[3][1:]
                    else:
                        user_info_1 = REPDATA[3][0:]
                    for i in user_info_1:
                        temp = i[1]
                        temp_list_1 = [temp]
                        temp_list_2 = list(i)[3:6]
                        temp_list_3 = list(i)[7:]
                        temp_list_1.extend(temp_list_2)
                        temp_list_1.extend(temp_list_3)
                        user_info.append(temp_list_1)
                    print(user_info)
                    self.userInfo = user_info
                    self.curPageMax = maxPage
                    self.clear(self.view.ui.verticalLayout_3)
                    self.tableWidget = TableWidget(self.userInfo, self.col_name, self.curPageIndex,
                                                   self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                                   self.on_clicked_pwdUpda)
                    self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
            elif REPDATA[0] == '0':
                if REPDATA[3] == 0:
                    QMessageBox.information(self, "提示", "该用户已经在线,无法进行删除操作", QMessageBox.Yes)
                if REPDATA[3] == 1:
                    QMessageBox.information(self, "提示", "请删除该用户的关联信息后,再删除用户", QMessageBox.Yes)
                isSearch = REPDATA[4]
                if isSearch:
                    self.clear(self.view.ui.verticalLayout_3)
                    self.tableWidget = TableWidget(self.searchInfo, self.col_name, self.searchPage,
                                                   self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                                   self.on_clicked_pwdUpda)
                    self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.searchPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
                else:
                    self.clear(self.view.ui.verticalLayout_3)
                    self.tableWidget = TableWidget(self.userInfo, self.col_name, self.curPageIndex,
                                                   self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                                   self.on_clicked_pwdUpda)
                    self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
        except Exception as e:
             print("delUserInfo", e)

    # 用户添加
    # 确认添加用户信息方法
    def addConfirm(self):
        try:
            judge_list = []
            if self.isSearch:
                row_num = len(self.searchInfo)
            else:
                row_num = len(self.userInfo)
            layout = self.tableWidget.table.cellWidget(row_num, 4).layout()
            if layout.itemAt(0).widget().isChecked():
                labeller = 1
            else:
                labeller = 0

            if layout.itemAt(1).widget().isChecked():
                student = 1
            else:
                student = 0

            if layout.itemAt(2).widget().isChecked():
                teacher = 1
            else:
                teacher = 0

            if layout.itemAt(3).widget().isChecked():
                doctor = 1
            else:
                doctor = 0

            if layout.itemAt(4).widget().isChecked():
                researcher = 1
            else:
                researcher = 0

            if labeller == 0 and student == 0 and teacher == 0 and doctor == 0 and researcher == 0:
                QMessageBox.information(self, "提示", '请至少选择一种身份', QMessageBox.Yes)
                return
            if labeller == 0 and student == 0 and teacher == 0 and doctor == 0 and researcher == 0:
                QMessageBox.information(self, "提示", '请至少选择一种身份', QMessageBox.Yes)
                return
            elif labeller == 1:
                if student == 1 or teacher == 1 or doctor == 1 or researcher == 1:
                    QMessageBox.information(self, "提示", '标注员角色的用户只能具有标注员角色', QMessageBox.Yes)
                    return
            elif student == 1:
                if labeller == 1 or teacher == 1 or doctor == 1 or researcher == 1:
                    QMessageBox.information(self, "提示", '学员角色的用户只能具有学员角色', QMessageBox.Yes)
                    return
            elif doctor == 1:
                if labeller == 1 or student == 1:
                    QMessageBox.information(self, "提示", '医生角色的用户只能同时具有培训导师和研究员两种角色', QMessageBox.Yes)
                    return
            elif teacher == 1:
                if labeller == 1 or student == 1 or researcher == 1:
                    QMessageBox.information(self, "提示", '只有医生角色的用户可以同时具有培训导师和研究员两种角色', QMessageBox.Yes)
                    return
            elif researcher == 1:
                if labeller == 1 or student == 1 or doctor == 1 or teacher == 1:
                    QMessageBox.information(self, "提示", '只有医生角色的用户可以同时具有培训导师和研究员两种角色', QMessageBox.Yes)
                    return

            for j in range(0, 4):
                judge_list.append(self.tableWidget.table.item(row_num, j).text())
            if judge_list[0] == '' and judge_list[1] == '':
                QMessageBox.information(self, "提示", '账号、姓名不完善', QMessageBox.Yes)
            elif judge_list[0] == '' and judge_list[1] != '':
                QMessageBox.information(self, "提示", '账号不完善', QMessageBox.Yes)
            elif judge_list[0] != '' and judge_list[1] == '':
                QMessageBox.information(self, "提示", '姓名不完善', QMessageBox.Yes)
            elif self.has_chinese(judge_list[0]):
                QMessageBox.information(self, "提示", '不接受带中文的账号', QMessageBox.Yes)
            else:
                administrator = 0
                e_pwd = self.cAppUtil.md5_string('123456')
                if self.isSearch:
                    user_info_d = [judge_list[0], e_pwd, judge_list[1], judge_list[2], judge_list[3], administrator,
                                   labeller, student, teacher, doctor, researcher, self.searchPage, self.isSearch,
                                   self.key_word, self.key_value]
                else:
                    user_info_d = [judge_list[0], e_pwd, judge_list[1], judge_list[2], judge_list[3], administrator,
                                   labeller, student, teacher, doctor, researcher, self.curPageIndex, self.isSearch]
                print(f"user_info_d: {user_info_d}")
                REQmsg = user_info_d
                self.client.addUserInfo(REQmsg)
        except Exception as e:
            print('addConfirm', e)

    # 取消添加用户信息方法
    def addCancel(self):
        reply = QMessageBox.information(self, "提示", '是否取消添加', QMessageBox.Yes | QMessageBox.No)
        if reply == 16384:
            self.clear(self.view.ui.verticalLayout_3)
            self.tableWidget = TableWidget(self.userInfo, self.col_name, self.curPageIndex,
                                           self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                           self.on_clicked_pwdUpda)
            self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
            self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
            self.tableWidget.control_signal.connect(self.page_controller)
            self.tableWidget.is_add = False

    # 添加用户信息方法
    def on_clicked_user_add(self,):
        try:
            if self.tableWidget.is_edit:
                QMessageBox.information(self, '提示', '请先完成编辑')
                return
            if self.tableWidget.is_add:
                QMessageBox.information(self, '提示', '请先完成添加')
                return
            self.tableWidget.is_add = True
            row_num = self.tableWidget.table.rowCount()
            self.tableWidget.table.setRowCount(row_num + 1)
            self.tableWidget.table.setRowHeight(row_num, 55)
            self.tableWidget.table.setEditTriggers(QAbstractItemView.DoubleClicked)
            # self.tableWidget.setInputMethodHints(self, Qt.ImhHiddenText)
            # 为新一行添加文本item
            for i in range(0, 4):
                self.tableWidget.table.setItem(row_num, i, QTableWidgetItem())
                self.tableWidget.table.item(row_num, i).setTextAlignment(Qt.AlignCenter)
                font = self.tableWidget.table.item(row_num, i).font()
                font.setPointSize(12)

            # 为新一行添加身份复选框
            self.tableWidget.table.setCellWidget(row_num, 4, QWidget())
            # 标注员
            check1 = QCheckBox()
            check1.setText('标注员')
            check1.setStyleSheet('margin:2px;font : 14px')
            # 学员
            check2 = QCheckBox()
            check2.setText('学员')
            check2.setStyleSheet('margin:2px;font : 14px')
            # 培训导师
            check3 = QCheckBox()
            check3.setText('培训导师')
            check3.setStyleSheet('margin:2px;font : 14px')
            # 医生
            check4 = QCheckBox()
            check4.setText('医生')
            check4.setStyleSheet('margin:2px;font : 14px')
            # 研究员
            check5 = QCheckBox()
            check5.setText('研究员')
            check5.setStyleSheet('margin:2px;font : 14px')

            layout = QHBoxLayout()
            layout.addWidget(check1)
            layout.addWidget(check2)
            layout.addWidget(check3)
            layout.addWidget(check4)
            layout.addWidget(check5)

            layout.setStretch(0, 3)
            layout.setStretch(1, 2)
            layout.setStretch(2, 4)
            layout.setStretch(3, 2)
            layout.setStretch(4, 3)
            self.tableWidget.table.cellWidget(row_num, 4).setLayout(layout)

            # 添加最后一列
            self.tableWidget.table.setCellWidget(row_num, 5, QWidget())
            confirmBtn = QPushButton('确认')
            cancelBtn = QPushButton('取消')
            confirmBtn.clicked.connect(self.addConfirm)
            cancelBtn.clicked.connect(self.addCancel)
            confirmBtn.setStyleSheet('margin:5px;height : 50px;width:60px;font : 18px')
            cancelBtn.setStyleSheet('margin:5px;height : 50px;width:60px;font : 18px')
            layout = QHBoxLayout()
            layout.addWidget(confirmBtn)
            layout.addWidget(cancelBtn)
            spaceItem_3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            layout.addItem(spaceItem_3)
            layout.setStretch(0, 2)
            layout.setStretch(1, 2)
            layout.setStretch(2, 4)
            self.tableWidget.table.cellWidget(row_num, 5).setLayout(layout)
        except Exception as e:
            print('on_clicked_user_add', e)

    # 处理客户端传回的添加用户信息结果
    def addUserInfoRes(self, REPDATA):
        try:
            if REPDATA[0] == '1':
                isSearch = REPDATA[4]
                if isSearch:
                    self.searchInfo.clear()
                    QMessageBox.information(self, "提示", '添加用户信息成功, 请翻转到尾页查看', QMessageBox.Yes)
                    user_info = []
                    user_info_1 = REPDATA[2][0:]
                    for i in user_info_1:
                        temp = i[1]
                        temp_list_1 = [temp]
                        temp_list_2 = list(i)[3:6]
                        temp_list_3 = list(i)[7:]
                        temp_list_1.extend(temp_list_2)
                        temp_list_1.extend(temp_list_3)
                        user_info.append(temp_list_1)
                    print(user_info)
                    self.searchInfo = user_info
                    self.searchPageMax = REPDATA[3]
                    self.clear(self.view.ui.verticalLayout_3)
                    self.tableWidget = TableWidget(self.searchInfo, self.col_name, self.searchPage,
                                                   self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                                   self.on_clicked_pwdUpda)
                    self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.searchPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
                else:
                    # 添加内存中的用户数据
                    self.userInfo.clear()
                    QMessageBox.information(self, "提示", '添加用户信息成功, 请翻转到尾页查看', QMessageBox.Yes)
                    user_info = []
                    if self.curPageIndex == 1:
                        user_info_1 = REPDATA[2][1:]
                    else:
                        user_info_1 = REPDATA[2][0:]
                    for i in user_info_1:
                        temp = i[1]
                        temp_list_1 = [temp]
                        temp_list_2 = list(i)[3:6]
                        temp_list_3 = list(i)[7:]
                        temp_list_1.extend(temp_list_2)
                        temp_list_1.extend(temp_list_3)
                        user_info.append(temp_list_1)
                    print(user_info)
                    self.userInfo = user_info
                    self.curPageMax = REPDATA[3]
                    self.clear(self.view.ui.verticalLayout_3)
                    self.tableWidget = TableWidget(self.userInfo, self.col_name, self.curPageIndex,
                                                   self.editConfirm, self.editCancel, self.on_clicked_user_del,
                                                   self.on_clicked_pwdUpda)
                    self.view.ui.verticalLayout_3.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
            elif REPDATA[0] == '0':
                QMessageBox.information(self, "提示", '添加的账号已存在，请重新添加', QMessageBox.Yes)
                self.tableWidget.table.setRowCount(self.tableWidget.table.rowCount() - 1)
            self.tableWidget.is_add = False
        except Exception as e:
            print("addUserInfo", e)

    # 密码修改功能
    # 确认密码修改方法
    def pwd_update_confirm(self, account, new_pwd):
        try:
            new_pwd = self.cAppUtil.md5_string(new_pwd)
            REQmsg = []
            flag = True
            REQmsg.append(flag)
            REQmsg.append(account)
            REQmsg.append(new_pwd)
            self.client.updateUserInfo(REQmsg)
        except Exception as e:
            print('pwd_update_confirm', e)
        # self.client.updateUserInfo(REQmsg)

    # 点击密码修改响应函数
    def on_clicked_pwdUpda(self, i):
        try:
            if self.tableWidget.is_edit:
                QMessageBox.information(self, '提示', '请先完成编辑')
                return
            if self.tableWidget.is_add:
                QMessageBox.information(self, '提示', '请先完成添加')
                return
            update_account = self.tableWidget.table.item(i, 0).text()
            self.pwd_update_view = pwdUpdateView(controller=self, update_account=update_account)
            self.pwd_update_view.comfirm_signal.connect(self.pwd_update_confirm)
        except Exception as e:
            print('on_clicked_pwdUpda', e)

    def has_chinese(self, text):
        for char in text:
            if '\u4e00' <= char <= '\u9fa5':
                return True
        return False

    def exit(self):
        self.client.getUserInfoResSig.disconnect()
        self.client.addUserInfoResSig.disconnect()
        self.client.updateUserInfoResSig.disconnect()
        self.client.delUserInfoResSig.disconnect()
        self.client.userPagingResSig.disconnect()
        self.client.inquiryUserInfoResSig.disconnect()
