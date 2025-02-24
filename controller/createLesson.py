import copy
from datetime import datetime
from functools import partial

from view.createLesson import createLessonView, studentView, lessonInfoView, patientView, PrentryView, \
    UserView, PurposeView, studentInfoView

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
import numpy as np
import sys, re

class createLessonController(QWidget):

    def __init__(self, client, cAppUtil):
        try:
            super().__init__()
            self.client = client
            self.cAppUtil = cAppUtil
            self.view = createLessonView()
            # 当前设置的用户ID
            self.userID = self.client.tUser[0]
            # 当前选择的配置方案
            self.config_id = self.client.tUser[12]
            # 保存除去class_id的课堂信息内容的列表，按课堂开始日期逆序存放
            self.lessonInfo_withoutid = []
            # 保存课堂信息内容的列表，按课堂开始日期逆序存放
            self.lessonInfo_withID = []
            # 保存学员名字与ID对应的字典
            self.studentInfo = {}
            # 保存学员ID与名字对应的字典
            self.student_id_name_dic = {}
            # 存放学员名字的列表
            self.is_edit = False
            self.student_name_info = []
            self.lesson_info = []
            self.is_search = False
            # 存放选择脑电文件信息
            self.patient_view_info = []
            # 存放用户名字与ID对应字典
            self.userNamesDict = {}
            # 存放病人名字与ID对应字典
            self.patientNamesDict = {}
            self.searchInfo_without_id = []
            self.searchInfo_withID = []
            self.check_id = None
            self.file_id = []
            self.file_name = []
            self.user_id = []
            # 被选择的行
            self.select_row = None
            self.col_num = 7
            # 添加学员列表所需参数
            self.is_student_search = False
            self.search_student_page = 1
            self.search_student_page_max = 1
            self.student_page_max = 1
            self.student_page_current = 1
            self.key_word = None
            self.key_value = None
            # 添加课堂内容列表所需参数
            self.is_eeg_search = False
            self.search_eeg_page = 1
            self.search_eeg_page_max = 1
            self.eeg_page_max = 1
            self.eeg_page_current = 1
            self.key_eeg_word = None
            self.key_eeg_value = None

            self.client.getLessonInfo([self.client.tUser[0], self.client.tUser[1]])
            self.client.getLessonInfoResSig.connect(self.getLessonInfoRes)
            self.client.getDiagCheckIDResSig.connect(self.getDiagCheckIDRes)
            self.client.getFileNameResSig.connect(self.getFileNameRes)
            self.client.addLessonResSig.connect(self.addLessonRes)
            self.client.delLessonResSig.connect(self.delLessonRes)
            self.client.updateLessonResSig.connect(self.updateLessonRes)
            self.client.getStudentInfoResSig.connect(self.getStudentInfoRes)
            self.client.getContentInfoResSig.connect(self.getContentInfoRes)
            # self.client.updateContentInfoResSig.connect(self.updateContentInfoRes)
            self.client.inquiryLessonInfoResSig.connect(self.inquiryLessonInfoRes)
            self.client.getCheckUserIDResSig.connect(self.getCheckUserIDRes)
            self.client.addStudentResSig.connect(self.addStudentRes)
            self.client.getlessonStudentResSig.connect(self.getlessonStudentRes)
            self.client.delStudentResSig.connect(self.delStudentRes)
            self.client.addLessonContentResSig.connect(self.addLessonContentRes)
            self.client.delLessonContentResSig.connect(self.delLessonContentRes)
            self.client.studentPagingResSig.connect(self.studentPagingRes)
            self.client.searchStudentPageInfoResSig.connect(self.searchStudentPageInfoRes)
            self.client.eggPagingResSig.connect(self.eggPagingRes)
            self.client.searchEegPageInfoResSig.connect(self.searchEegPageInfoRes)
        except Exception as e:
            print('__init__', e)

    # 查询功能
    # 响应点击查询函数
    def inquiryLessonInfo(self):
        try:
            if self.is_edit:
                QMessageBox.information(self, '提示', '请先完成修改')
                return
            key_word = self.view.ui.comboBox.currentText()
            key_value = self.view.ui.lineEdit.text()
            self.searchInfo_without_id.clear()
            self.searchInfo_withID.clear()
            self.is_search = True
            if key_value == '':
                QMessageBox.information(self, '提示', '请输入要搜索的课堂信息', QMessageBox.Yes)
                return
            if key_word == '课堂名称':
                key_word = 'name'
            if key_word == '学习时长':
                key_word = 'time'
            if key_word == '创建者':
                key_word = 'uid'
            # elif key_word == '课堂开始日期':
            #     key_word = 'start'
            REQmsg = [key_word, key_value]
            self.client.inquiryLessonInfo(REQmsg)
        except Exception as e:
            print('inquiryLessonInfo', e)

    # 重置功能，刷新初始页面
    def reset(self):
        try:
            if self.is_edit:
                QMessageBox.information(self, '提示', '请先完成修改')
                return
            self.view.tableWidget.clear()
            self.view.initTable(self.lessonInfo_withoutid, self.on_clicked_studentView, self.on_clicked_patientView,
                                self.on_clicked_show_student, self.on_clicked_show_file)
            self.view.ui.lineEdit.clear()
            self.is_search = False
            self.select_row = None
        except Exception as e:
            print('reset', e)

    # 回调，处理服务器传回的查询课堂信息
    def inquiryLessonInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                # 添加课堂信息
                # lesson_info = REPData[2]
                # for i in lesson_info:
                #     id = []
                #     id.append(i[0])
                #     lesson_info_m = list(i)[1:]
                #     lesson_info_m[0] = self.teacher_id_name_dic[lesson_info_m[0]]
                #     temp = lesson_info_m[6]
                #     lesson_info_m[6] = lesson_info_m[3]
                #     lesson_info_m[3] = temp
                #     id.extend(lesson_info_m)
                self.searchInfo_without_id = REPData[3]
                self.searchInfo_withID = REPData[4]
                self.searchInfo_without_id = sorted(self.searchInfo_without_id, key=lambda x: x[4], reverse=True)
                self.searchInfo_withID = sorted(self.searchInfo_withID, key=lambda x: x[5], reverse=True)
                print('searchInfo_without_id{}'.format(self.searchInfo_without_id))
                print('searchInfo_withID:{}'.format(self.searchInfo_withID))
                # 初始化表格
                self.view.tableWidget.clear()
                self.view.initTable(self.searchInfo_without_id, self.on_clicked_studentView,self.on_clicked_patientView,
                                    self.on_clicked_show_student, self.on_clicked_show_file)
            else:
                QMessageBox.information(self, '提示', '查询课堂信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('inquiryLessonInfoRes', e)

    # 回调,响应获取课堂信息方法
    def getLessonInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                # 添加课堂信息
                lesson_info = REPData[2]
                # teacher_info = REPData[5]
                # for i in teacher_info:
                #     self.teacherInfo[i[3]] = i[0]
                #     self.teacher_id_name_dic[i[0]] = i[3]
                # for i in lesson_info:
                #     id = []
                #     id.append(i[0])
                #     lesson_info_m = list(i)[1:]
                #     lesson_info_m[0] = self.teacher_id_name_dic[lesson_info_m[0]]
                #     temp = lesson_info_m[6]
                #     lesson_info_m[6] = lesson_info_m[3]
                #     lesson_info_m[3] = temp
                #     id.extend(lesson_info_m)
                #     self.lessonInfo_withoutid.append(lesson_info_m)
                #     self.lessonInfo_withID.append(id)
                self.lessonInfo_withoutid = REPData[5]
                self.lessonInfo_withID = REPData[6]
                self.lessonInfo_withoutid = sorted(self.lessonInfo_withoutid, key=lambda x: x[4], reverse=True)
                self.lessonInfo_withID = sorted(self.lessonInfo_withID, key=lambda x: x[5], reverse=True)
                print('lessonInfo_withoutid{}'.format(self.lessonInfo_withoutid))
                print('lessonInfo_withID:{}'.format(self.lessonInfo_withID))
                user_info = REPData[3]
                # user_info.pop(0)
                # 添加学生信息
                for i in user_info:
                    self.studentInfo[i[3]] = i[0]
                    self.student_id_name_dic[i[0]] = i[3]
                self.student_name_info = [x[3] for x in user_info]
                print(self.studentInfo, self.student_id_name_dic)
                # 添加病人信息
                # patient_info = REPData[4]
                # self.patientInfo = [x[1] for x in patient_info]
                # 初始化试图
                self.view.initView(self.on_clicked_create_lesson, self.on_clicked_del_lesson, self.set_selectRow,
                                   self.on_clicked_edit_lesson, self.inquiryLessonInfo, self.reset)
                # 初始化表格
                self.view.tableWidget.clear()
                self.view.initTable(self.lessonInfo_withoutid,self.on_clicked_studentView,self.on_clicked_patientView,
                                    self.on_clicked_show_student, self.on_clicked_show_file)
            else:
                QMessageBox.information(self, '提示', '获取课堂信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('getLessonInfoRes', e)

    # 响应点击创建课堂方法
    def on_clicked_create_lesson(self):
        try:
            if self.is_edit:
                QMessageBox.information(self, '提示', '请先完成修改')
                return
            self.lessonInfoView = lessonInfoView()
            self.lessonInfoView.ui.dateTimeEdit_2.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
            self.lessonInfoView.ui.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
            # 设置日历弹出模式
            self.lessonInfoView.ui.dateTimeEdit_2.setCalendarPopup(True)
            self.lessonInfoView.ui.dateTimeEdit.setCalendarPopup(True)
            # 设置时间编辑器弹出功能
            self.lessonInfoView.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
            self.lessonInfoView.ui.dateTimeEdit_2.setDateTime(QDateTime.currentDateTime())
            self.lessonInfoView.setWindowModality(Qt.ApplicationModal)
            self.lessonInfoView.ui.lineEdit_2.setText('1')
            self.lessonInfoView.show()
            self.lessonInfoView.ui.pushButton.clicked.connect(self.on_clicked_confirm_add_lesson)
            self.lessonInfoView.ui.pushButton_2.clicked.connect(self.on_clicked_lesson_return)
        except Exception as e:
            print('on_clicked_patientView', e)


    # 点击响应选取病例脑电文件
    def on_clicked_patientView(self, row):
        try:
            if self.is_edit:
                QMessageBox.information(self, '提示', '请先完成修改')
                return
            if self.is_search:
                create_id = self.searchInfo_withID[row][1]
            else:
                create_id = self.lessonInfo_withID[row][1]
            if create_id != self.client.tUser[0]:
                QMessageBox.information(self, '提示', '无法操作其他创建者的课堂', QMessageBox.Ok)
                return
            class_id = self.lessonInfo_withID[row][0]
            self.patientView = patientView()
            self.client.getDiagCheckID([class_id, self.eeg_page_current, 12, True, row])
        except Exception as e:
            print('on_clicked_patientView', e)

    def getDiagCheckIDRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "提取脑电检查不成功", REPData[1], QMessageBox.Yes)
                return
            else:
                class_id = REPData[5]
                row = REPData[6]
                first_time = REPData[8]
                self.eeg_page_max = REPData[7]
                create_id = self.lessonInfo_withID[row][1]
                self.patient_view_info = REPData[2]
                print(self.patient_view_info)
                self.userNamesDict = {}
                self.patientNamesDict = {}
                for u in REPData[3]:
                    self.userNamesDict.setdefault(u[0], u[1])
                for p in REPData[4]:
                    self.patientNamesDict.setdefault(p[0], p[1])
                print(self.userNamesDict, self.patientNamesDict)
                self.patientView.initTable(self.patient_view_info, self.userNamesDict, self.patientNamesDict,
                                           self.on_clicked_add_EEG, class_id, create_id)
                self.patientView.setWindowModality(Qt.ApplicationModal)
                self.patientView.show()
                self.patientView.ui.label_3.setText("共" + str(self.eeg_page_max) + "页")
                self.patientView.ui.label_6.setText(str(self.eeg_page_current))
                if first_time:
                    self.patientView.page_control_signal.connect(partial(self.page_controller_1, class_id))
                    self.patientView.ui.pushButton.clicked.connect(
                        partial(self.on_clicked_query_egg_info, class_id))
                    self.patientView.ui.pushButton_8.clicked.connect(
                        partial(self.on_clicked_reset_egg_info, class_id, row))
                else:
                    self.patientView.ui.lineEdit.clear()
                    QMessageBox.information(self, '提示', '刷新页面成功', QMessageBox.Ok)
        except Exception as e:
            print('getDiagCheckIDRes', e)

    def on_clicked_query_egg_info(self, lesson_id):
        try:
            self.is_eeg_search = False
            self.search_eeg_page = 1
            self.search_eeg_page_max = 1
            self.key_eeg_word = self.patientView.ui.comboBox.currentText()
            self.key_eeg_value = self.patientView.ui.lineEdit.text()
            if self.key_eeg_value == '':
                QMessageBox.information(self, '提示', '请输入要搜索的脑电检查信息', QMessageBox.Yes)
                return
            if self.key_eeg_word == '检查单号':
                self.key_eeg_word = 'check_number'
            elif self.key_eeg_word == '病人':
                self.key_eeg_word = 'patient_id'
            elif self.key_eeg_word == '开单医生':
                self.key_eeg_word = 'pUid'
            REQmsg = [self.key_eeg_word, self.key_eeg_value, self.search_eeg_page, 12, lesson_id]
            self.client.searchEegPageInfo(REQmsg)
        except Exception as e:
            print('on_clicked_query_egg_info', e)

    def searchEegPageInfoRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '查询脑电检查信息失败, 请重新尝试', QMessageBox.Ok)
                return
            else:
                class_id = REPData[7]
                create_id = None
                for i in self.lessonInfo_withID:
                    if i[0] == class_id:
                        create_id = i[1]
                        break
                self.patient_view_info = REPData[2]
                print(self.patient_view_info)
                self.userNamesDict = {}
                self.patientNamesDict = {}
                for u in REPData[3]:
                    self.userNamesDict.setdefault(u[0], u[1])
                for p in REPData[4]:
                    self.patientNamesDict.setdefault(p[0], p[1])
                self.search_eeg_page_max = REPData[6]
                self.is_eeg_search = True
                self.patientView.initTable(self.patient_view_info, self.userNamesDict, self.patientNamesDict,
                                           self.on_clicked_add_EEG, class_id, create_id)
                self.patientView.setWindowModality(Qt.ApplicationModal)
                self.patientView.show()
                self.patientView.ui.label_3.setText("共" + str(self.search_eeg_page_max) + "页")
                self.patientView.ui.label_6.setText(str(self.search_eeg_page))
        except Exception as e:
            print('searchStudentPageInfoRes', e)

    def on_clicked_reset_egg_info(self, lesson_id, row):
        try:
            self.eeg_page_max = 1
            self.eeg_page_current = 1
            self.key_eeg_word = None
            self.key_eeg_value = None
            self.is_eeg_search = False
            self.search_eeg_pages = 1
            self.search_eeg_page_max = 1
            self.client.getDiagCheckID([lesson_id, self.eeg_page_current, 12, False, row])
        except Exception as e:
            print('reset', e)

    def page_controller_1(self, lesson_id, signal):
        try:
            if "home" == signal[0]:
                if self.is_eeg_search:
                    if self.search_eeg_page == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.search_eeg_page = 1
                    self.patientView.ui.label_6.setText(str(self.search_eeg_page))
                else:
                    if self.eeg_page_current == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.eeg_page_current = 1
                    self.patientView.ui.label_6.setText(str(self.eeg_page_current))
            elif "pre" == signal[0]:
                if self.is_eeg_search:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.search_eeg_page <= 1:
                        return
                    self.search_eeg_page = self.search_eeg_page - 1
                    self.patientView.ui.label_6.setText(str(self.search_eeg_page))
                else:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.eeg_page_current <= 1:
                        return
                    self.eeg_page_current = self.eeg_page_current - 1
                    self.patientView.ui.label_6.setText(str(self.eeg_page_current))
            elif "next" == signal[0]:
                if self.is_eeg_search:
                    if self.search_eeg_page_max == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.search_eeg_page = self.search_eeg_page + 1
                    self.patientView.ui.label_6.setText(str(self.search_eeg_page))
                else:
                    if self.eeg_page_max == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.eeg_page_current = self.eeg_page_current + 1
                    self.patientView.ui.label_6.setText(str(self.eeg_page_current))
            elif "final" == signal[0]:
                if self.is_eeg_search:
                    if self.search_eeg_page == self.search_eeg_page_max:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.search_eeg_page = self.search_eeg_page_max
                    self.patientView.ui.label_6.setText(str(self.search_eeg_page))
                else:
                    if self.eeg_page_current == self.eeg_page_max:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.eeg_page_current = self.eeg_page_max
                    self.patientView.ui.label_6.setText(str(self.eeg_page_current))
            elif "confirm" == signal[0]:
                if self.is_eeg_search:
                    if self.search_eeg_page == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.search_eeg_page_max < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.search_eeg_page = int(signal[1])
                    self.patientView.ui.label_6.setText(signal[1])
                else:
                    if self.eeg_page_current == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.eeg_page_max < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.eeg_page_current = int(signal[1])
                    self.patientView.ui.label_6.setText(signal[1])
            if self.is_eeg_search:
                msg = [self.search_eeg_page, 12, signal[0], lesson_id, self.is_eeg_search, self.key_word, self.key_value]
            else:
                msg = [self.eeg_page_current, 12, signal[0], lesson_id, False]
            self.client.eggPaging(msg)
        except Exception as e:
            print('page_controller_1', e)

    def eggPagingRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '翻页失败, 请重新尝试', QMessageBox.Ok)
                return
            else:
                is_search = REPData[7]
                class_id = REPData[5]
                create_id = None
                for i in self.lessonInfo_withID:
                    if i[0] == class_id:
                        create_id = i[1]
                        break
                if is_search:
                    self.search_eeg_page = REPData[4]
                    self.patient_view_info = REPData[2]
                    print(self.patient_view_info)
                    self.userNamesDict = {}
                    self.patientNamesDict = {}
                    for u in REPData[3]:
                        self.userNamesDict.setdefault(u[0], u[1])
                    for p in REPData[4]:
                        self.patientNamesDict.setdefault(p[0], p[1])
                    print(self.userNamesDict, self.patientNamesDict)
                    self.patientView.initTable(self.patient_view_info, self.userNamesDict, self.patientNamesDict,
                                               self.on_clicked_add_EEG, class_id, create_id)
                    self.patientView.ui.label_3.setText("共" + str(self.search_eeg_page_max) + "页")
                    self.patientView.ui.label_6.setText(str(self.search_eeg_page))
                else:
                    self.eeg_page_current = REPData[6]
                    self.patient_view_info = REPData[2]
                    print(self.patient_view_info)
                    self.userNamesDict = {}
                    self.patientNamesDict = {}
                    for u in REPData[3]:
                        self.userNamesDict.setdefault(u[0], u[1])
                    for p in REPData[4]:
                        self.patientNamesDict.setdefault(p[0], p[1])
                    print(self.userNamesDict, self.patientNamesDict)
                    self.patientView.initTable(self.patient_view_info, self.userNamesDict, self.patientNamesDict,
                                               self.on_clicked_add_EEG, class_id, create_id)
                    self.patientView.ui.label_3.setText("共" + str(self.eeg_page_max) + "页")
                    self.patientView.ui.label_6.setText(str(self.eeg_page_current))
                self.patientView.setWindowModality(Qt.ApplicationModal)
                self.patientView.show()
        except Exception as e:
            print('studentPaging', e)


    def on_clicked_add_EEG(self, viewInfo, class_id, create_name):
        try:
            # create_id = self.teacherInfo[create_name]
            # if create_id != self.client.tUser[0]:
            #     QMessageBox.information(self, '提示', '无法操作其他创建者的课堂')
            #     return
            self.check_id = viewInfo[0]
            self.file_id = []
            self.file_name = []
            msg = [viewInfo[0], self.config_id, class_id]
            self.client.getFileName(msg)
            # self.lessonView.show()
            # self.patientView.close()
        except Exception as e:
            print('on_clicked_add_EEG', e)

    def getFileNameRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self,'提示', "选择诊断病例失败", QMessageBox.Yes)
                return
            else:
                # self.lessonView.show()
                self.patientView.close()
                self.select_file_row = []
                class_id = REPData[2]
                self.pre_info = REPData[1]
                if self.pre_info == []:
                    QMessageBox.information(self, '提示', "没有与当前课堂的频率设置编号一致的脑电数据文件", QMessageBox.Yes)
                    return
                print(self.pre_info)
                col_num = 1
                self.prentryView = PrentryView()
                self.prentryView.setAttribute(Qt.WA_DeleteOnClose)
                self.prentryView.setWindowTitle("创建课堂[选择脑电数据文件]")
                self.prentryView.setWindowModality(Qt.ApplicationModal)
                self.prentryView.ui.btnConfirm.setEnabled(True)
                self.prentryView.ui.btnReturn.setEnabled(True)
                self.prentryView.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.prentryView.ui.tableWidget.resizeRowsToContents()
                self.prentryView.ui.tableWidget.resizeColumnsToContents()
                self.prentryView.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
                # self.prentryView.ui.tableWidget.clicked.connect(self.on_tableWidget_itemClicked)
                self.prentryView.ui.btnConfirm.clicked.connect(partial(self.on_btnConfirm_clicked, class_id))
                self.prentryView.ui.btnReturn.clicked.connect(self.on_btnReturn_clicked)

                self.prentryView.ui.tableWidget.setColumnCount(col_num)
                itemName = ['病例脑电文件列表']
                row_num = len(self.pre_info)
                if row_num <= 0:
                    itemName = ['病例脑电文件列表[无相关文件]']
                for i in range(0, col_num):
                    header_item = QTableWidgetItem(itemName[i])
                    font = header_item.font()
                    font.setPointSize(10)
                    header_item.setFont(font)
                    header_item.setForeground(QBrush(Qt.black))
                    self.prentryView.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
                self.prentryView.ui.tableWidget.setColumnWidth(0, 50)
                self.prentryView.ui.tableWidget.horizontalHeader().setHighlightSections(False)
                self.prentryView.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
                # self.prentryView.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.prentryView.ui.tableWidget.setRowCount(row_num)
                for r in range(row_num):
                    for i in range(0, col_num):
                        fn = '{:>03}.bdf'.format(self.pre_info[r][1])
                        item = QTableWidgetItem(fn)
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        font = item.font()
                        font.setPointSize(10)
                        item.setFont(font)
                        self.prentryView.ui.tableWidget.setItem(r, 0, item)
                    # self.add_checkBox(r)
                self.prentryView.ui.tableWidget.verticalHeader().setVisible(False)
            self.prentryView.show()
        except Exception as e:
            print('getFileNameRes', e)

    def add_checkBox(self, row):
        exec('self.item_checked_{} = QCheckBox()'.format(row))
        exec('self.item_checked_{}.setCheckState(QtCore.Qt.Unchecked)'.format(row))
        exec('self.item_checked_{}.setCheckable(True)'.format(row))
        exec("self.item_checked_{}.setStyleSheet('''margin:10px''')".format(row))
        exec("self.item_checked_{}.clicked.connect(partial(self.rowSelected,{}))".format(row, row))
        exec("self.prentryView.ui.tableWidget.setCellWidget({}, 0, self.item_checked_{})".format(row, row))

    def rowSelected(self, row):
        try:
            tag = eval("self.item_checked_{}.isChecked()".format(row))
            # print(tag)
            if tag:
                self.select_file_row.append(row)
                self.select_file_row.sort()
            else:
                if row in self.select_file_row:
                    self.select_file_row.remove(row)
        except Exception as e:
            print('rowSelected', e)
        # print(self.selected_row)

    def on_btnConfirm_clicked(self, class_id):
        try:
            row = self.prentryView.ui.tableWidget.currentRow()
            if row < 0:
                QMessageBox.information(self, '提示', '未选择文件', QMessageBox.Yes | QMessageBox.No)
                return
            # for i in self.select_file_row:
            self.file_id.append(self.pre_info[row][1])
            file_name = '{:>03}.bdf'.format(self.pre_info[row][1])
            self.file_name.append(file_name)
            reply = QMessageBox.information(self, '提示', '是否选择添加当前文件', QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                # self.set_patient_example = True
                self.prentryView.close()
                self.user_id = []
                self.client.getCheckUserID([self.check_id, self.file_id, class_id])
        except Exception as e:
            print('on_btnConfirm_clicked', e)

    def on_btnReturn_clicked(self):
        self.prentryView.close()
        return

    def on_user_btnReturn_clicked(self):
        self.userView.close()
        return

    def getCheckUserIDRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "选择脑电数据文件失败", REPData[1], QMessageBox.Yes)
                return False
            else:
                self.select_user_row = []
                class_id = REPData[2]
                self.user_info = REPData[1]
                col_num = 2
                row_num = len(self.user_info)
                itemName = ['可选框', '标注用户']
                if row_num <= 0:
                    itemName = ['标注用户列表[无相关用户]']
                    col_num = 1
                self.userView = UserView()
                self.userView.setAttribute(Qt.WA_DeleteOnClose)
                self.userView.setWindowTitle("创建课堂[选择标注用户]")
                self.userView.setWindowModality(Qt.ApplicationModal)
                self.userView.ui.btnConfirm.setEnabled(True)
                self.userView.ui.btnReturn.setEnabled(True)
                self.userView.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.userView.ui.tableWidget.resizeRowsToContents()
                self.userView.ui.tableWidget.resizeColumnsToContents()
                self.userView.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.userView.ui.btnConfirm.clicked.connect(partial(self.on_user_btnConfirm_clicked, class_id))
                self.userView.ui.btnReturn.clicked.connect(self.on_user_btnReturn_clicked)
                self.userView.ui.tableWidget.setColumnCount(col_num)
                for i in range(0, col_num):
                    header_item = QTableWidgetItem(itemName[i])
                    font = header_item.font()
                    font.setPointSize(10)
                    header_item.setFont(font)
                    header_item.setForeground(QBrush(Qt.black))
                    self.userView.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
                # self.userView.ui.tableWidget.setColumnWidth(0, 50)
                self.userView.ui.tableWidget.horizontalHeader().setHighlightSections(False)
                self.userView.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
                self.userView.ui.tableWidget.setRowCount(row_num)
                self.userView.ui.tableWidget.setColumnCount(col_num)
                for r in range(row_num):
                    for i in range(1, col_num):
                        # if i == 1:
                        #     fn = '{:>03}.edf'.format(self.user_info[r][0])
                        #     item1 = QTableWidgetItem(fn)
                        #     item1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        #     font = item1.font()
                        #     font.setPointSize(10)
                        #     item1.setFont(font)
                        #     self.userView.ui.tableWidget.setItem(r, 1, item1)
                        if i == 1:
                            ft = str(self.user_info[r][1])
                            item2 = QTableWidgetItem(ft)
                            item2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = item2.font()
                            font.setPointSize(10)
                            item2.setFont(font)
                            self.userView.ui.tableWidget.setItem(r, 1, item2)
                    self.add_checkBox_1(r)
                self.userView.ui.tableWidget.verticalHeader().setVisible(False)
            self.userView.show()
        except Exception as e:
            print('getCheckUserIDRes', e)

    def add_checkBox_1(self, row):
        exec('self.item_checked_{} = QCheckBox()'.format(row))
        exec('self.item_checked_{}.setCheckState(QtCore.Qt.Unchecked)'.format(row))
        exec('self.item_checked_{}.setCheckable(True)'.format(row))
        exec("self.item_checked_{}.setStyleSheet('''margin:10px''')".format(row))
        exec("self.item_checked_{}.clicked.connect(partial(self.rowSelected_1,{}))".format(row, row))
        exec("self.userView.ui.tableWidget.setCellWidget({}, 0, self.item_checked_{})".format(row, row))

    def rowSelected_1(self, row):
        tag = eval("self.item_checked_{}.isChecked()".format(row))
        # print(tag)
        if tag:
            self.select_user_row.append(row)
            self.select_user_row.sort()
        else:
            if row in self.select_user_row:
                self.select_user_row.remove(row)

    def on_user_btnConfirm_clicked(self, class_id):
        try:
            for i in self.select_user_row:
                self.user_id.append(self.user_info[i][0])
            reply = QMessageBox.information(self, '提示', '是否选择添加当前标注用户', QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                self.userView.close()
                self.purposeView = PurposeView()
                self.purposeView.ui.pushButton_3.clicked.connect(partial(self.on_clicked_addpurPose, class_id))
                self.purposeView.ui.pushButton_5.setEnabled(False)
                self.purposeView.show()
            # else:
            #     for i in self.select_user_row:
            #         self.user_id.append(self.user_info[i][0])
            #     reply = QMessageBox.information(self, '提示', '是否选择添加当前标注用户',
            #                                     QMessageBox.Yes | QMessageBox.No)
            #     if reply == 16384:
            #         self.userView.close()
            #         self.client.updateContentInfo([class_id, self.check_id, self.user_id, self.file_id])
        except Exception as e:
            print('on_btnConfirm_clicked', e)

    def on_clicked_addpurPose(self, class_id):
        try:
            purpose = self.purposeView.ui.comboBox.currentText()
            if purpose == '培训':
                purpose = 'training'
            elif purpose == '测试':
                purpose = 'test'
            reply = QMessageBox.information(self, '提示', '确认添加课堂内容信息', QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                self.client.addLessonContent([class_id, self.check_id, self.user_id, self.file_id, purpose])
        except Exception as e:
            print('on_clicked_addpurPose', e)

    def addLessonContentRes(self, REPData):
        try:
            self.file_id = []
            self.user_id = []
            self.check_id = None
            self.select_file_row = []
            self.select_user_row = []
            self.purposeView.close()
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '添加课堂内容失败, 检查是否重复添加课堂内容', QMessageBox.Ok)
                return
            else:
                QMessageBox.information(self, '提示', '添加课堂内容成功', QMessageBox.Ok)
        except Exception as e:
            print('addLessonContentRes', e)

    # 选取学生信息方法
    def on_clicked_studentView(self, row):
        try:
            if self.is_edit:
                QMessageBox.information(self, '提示', '请先完成修改')
                return
            if self.is_search:
                create_id = self.searchInfo_withID[row][1]
            else:
                create_id = self.lessonInfo_withID[row][1]
            if create_id != self.client.tUser[0]:
                QMessageBox.information(self, '提示', '无法操作其他创建者的课堂', QMessageBox.Ok)
                return
            self.studentView = studentView()
            lesson_id = self.lessonInfo_withID[row][0]
            self.studentView.selected_row = []
            self.student_page_max = 1
            self.student_page_current = 1
            self.student_page_rows = 12
            self.client.getlessonStudent([lesson_id, self.student_page_current, self.student_page_rows, True])
        except Exception as e:
            print('on_clicked_studentView', e)

    def on_clicked_reset_student_info(self, lesson_id):
        try:
            self.student_page_max = 1
            self.student_page_current = 1
            self.key_word = None
            self.key_value = None
            self.is_student_search = False
            self.search_student_page = 1
            self.search_student_page_max = 1
            self.client.getlessonStudent([lesson_id, self.student_page_current, self.student_page_rows, False])
        except Exception as e:
            print('reset', e)

    def getlessonStudentRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '获取课堂学员信息, 请重新尝试', QMessageBox.Ok)
                return
            else:
                student_info = list(REPData[2])
                lesson_id = REPData[3]
                self.student_page_max = REPData[4]
                self.student_page_current = REPData[5]
                first_time = REPData[6]
                student_name = []
                for i in student_info:
                    student_name.append(i[3])
                self.studentView.initTable(student_name)
                self.studentView.setWindowModality(Qt.ApplicationModal)
                self.studentView.show()
                self.studentView.ui.label_3.setText("共" + str(self.student_page_max) + "页")
                self.studentView.ui.label_6.setText(str(self.student_page_current))
                if first_time:
                    self.studentView.page_control_signal.connect(partial(self.page_controller, lesson_id))
                    self.studentView.ui.pushButton_7.clicked.connect(partial(self.on_clicked_add_student_info, lesson_id))
                    self.studentView.ui.pushButton.clicked.connect(partial(self.on_clicked_query_student_info, lesson_id))
                    self.studentView.ui.pushButton_8.clicked.connect(partial(self.on_clicked_reset_student_info, lesson_id))
                else:
                    self.studentView.ui.lineEdit.clear()
                    QMessageBox.information(self, '提示', '刷新页面成功', QMessageBox.Ok)
        except Exception as e:
            print('getlessonStudentRes', e)

    def page_controller(self, lesson_id, signal):
        try:
            if "home" == signal[0]:
                if self.is_student_search:
                    if self.search_student_page == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.search_student_page = 1
                    self.studentView.ui.label_6.setText(str(self.search_student_page))
                else:
                    if self.student_page_current == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.student_page_current = 1
                    self.studentView.ui.label_6.setText(str(self.student_page_current))
            elif "pre" == signal[0]:
                if self.is_student_search:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.search_student_page <= 1:
                        return
                    self.search_student_page = self.search_student_page - 1
                    self.studentView.ui.label_6.setText(str(self.search_student_page))
                else:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.student_page_current <= 1:
                        return
                    self.student_page_current = self.student_page_current - 1
                    self.studentView.ui.label_6.setText(str(self.student_page_current))
            elif "next" == signal[0]:
                if self.is_student_search:
                    if self.search_student_page_max == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.search_student_page = self.search_student_page + 1
                    self.studentView.ui.label_6.setText(str(self.search_student_page))
                else:
                    if self.student_page_max == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.student_page_current = self.student_page_current + 1
                    self.studentView.ui.label_6.setText(str(self.student_page_current))
            elif "final" == signal[0]:
                if self.is_student_search:
                    if self.search_student_page == self.search_student_page_max:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.search_student_page = self.search_student_page_max
                    self.studentView.ui.label_6.setText(str(self.search_student_page))
                else:
                    if self.student_page_current == self.student_page_max:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.student_page_current = self.student_page_max
                    self.studentView.ui.label_6.setText(str(self.student_page_current))
            elif "confirm" == signal[0]:
                if self.is_student_search:
                    if self.search_student_page == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.search_student_page_max < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.search_student_page = int(signal[1])
                    self.studentView.ui.label_6.setText(signal[1])
                else:
                    if self.student_page_current == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.student_page_max < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.student_page_current = int(signal[1])
                    self.studentView.ui.label_6.setText(signal[1])
            if self.is_student_search:
                msg = [self.search_student_page, 12, signal[0], lesson_id, self.is_student_search, self.key_word, self.key_value]
            else:
                msg = [self.student_page_current, 12, signal[0], lesson_id, False]
            self.client.studentPaging(msg)
        except Exception as e:
            print('page_controller', e)

    def studentPagingRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '翻页失败, 请重新尝试', QMessageBox.Ok)
                return
            else:
                is_search = REPData[5]
                if is_search:
                    student_info = list(REPData[2])
                    self.search_student_page = REPData[4]
                    student_name = []
                    for i in student_info:
                        student_name.append(i[3])
                    self.studentView.ui.label_3.setText("共" + str(self.search_student_page_max) + "页")
                    self.studentView.ui.label_6.setText(str(self.search_student_page))
                else:
                    student_info = list(REPData[2])
                    self.student_page_current = REPData[4]
                    student_name = []
                    for i in student_info:
                        student_name.append(i[3])
                    self.studentView.ui.label_3.setText("共" + str(self.student_page_max) + "页")
                    self.studentView.ui.label_6.setText(str(self.student_page_current))
                self.studentView.selected_row.clear()
                self.studentView.initTable(student_name)
                self.studentView.setWindowModality(Qt.ApplicationModal)
                self.studentView.show()
        except Exception as e:
            print('studentPaging', e)

    def on_clicked_query_student_info(self, lesson_id):
        try:
            self.is_student_search = False
            self.search_student_page = 1
            self.search_student_page_max = 1
            self.key_word = self.studentView.ui.comboBox.currentText()
            self.key_value = self.studentView.ui.lineEdit.text()
            if self.key_value == '':
                QMessageBox.information(self, '提示', '请输入要搜索的学员信息', QMessageBox.Yes)
                return
            if self.key_word == '学员姓名':
                self.key_word = 'name'
            REQmsg = [self.key_word, self.key_value, self.search_student_page, 12, lesson_id]
            self.client.searchStudentPageInfo(REQmsg)
        except Exception as e:
            print('on_clicked_query_student_info', e)

    def searchStudentPageInfoRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '查询学员信息失败, 请重新尝试', QMessageBox.Ok)
                return
            else:
                student_info = list(REPData[2])
                # lesson_id = REPData[3]
                # row = REPData[4]
                # create_name = self.lessonInfo_withID[row][1]
                self.search_student_page_max = REPData[5]
                self.is_student_search = True
                search_student_name = []
                for i in student_info:
                    search_student_name.append(i[3])
                self.studentView.initTable(search_student_name)
                self.studentView.setWindowModality(Qt.ApplicationModal)
                self.studentView.show()
                self.studentView.ui.label_3.setText("共" + str(self.search_student_page_max) + "页")
                self.studentView.ui.label_6.setText(str(self.search_student_page))
        except Exception as e:
            print('searchStudentPageInfoRes', e)


    # 确认添加
    def on_clicked_add_student_info(self, lesson_id, create_name):
        try:
            if self.studentView.selected_row == []:
                QMessageBox.information(self, '提示', '未选择学员信息', QMessageBox.Ok)
                return
            else:
                self.lesson_student_id = []
                for index in self.studentView.selected_row:
                    student_name = self.studentView.ui.tableWidget.item(index, 1).text()
                    self.lesson_student_id.append(self.studentInfo[student_name])
                print(self.lesson_student_id)
                if self.is_student_search:
                    self.client.addStudent(
                        [self.lesson_student_id, lesson_id, self.search_student_page, self.is_student_search,
                         self.key_word, self.key_value])
                else:
                    self.client.addStudent([self.lesson_student_id, lesson_id, self.student_page_current, self.is_student_search])
        except Exception as e:
            print('on_clicked_add_student_info', e)

    # def on_clicked_lessonInfoView(self):
    #     try:
    #         self.lessonInfoView = lessonInfoView()
    #
    #         self.lessonInfoView.ui.dateTimeEdit_2.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
    #         self.lessonInfoView.ui.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
    #         # 设置日历弹出模式
    #         self.lessonInfoView.ui.dateTimeEdit_2.setCalendarPopup(True)
    #         self.lessonInfoView.ui.dateTimeEdit.setCalendarPopup(True)
    #         # 设置时间编辑器弹出功能
    #         self.lessonInfoView.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
    #         self.lessonInfoView.ui.dateTimeEdit_2.setDateTime(QDateTime.currentDateTime())
    #         self.lessonInfoView.setWindowModality(Qt.ApplicationModal)
    #         self.lessonInfoView.show()
    #         self.lessonInfoView.ui.pushButton.clicked.connect(self.on_clicked_add_lesson_info)
    #         self.lessonInfoView.ui.pushButton_2.clicked.connect(self.on_clicked_lesson_return)
    #     except Exception as e:
    #         print('on_clicked_patientView', e)

    def on_clicked_lesson_return(self):
        self.lessonInfoView.close()

    def on_clicked_confirm_add_lesson(self):
        try:
            lesson_name = self.lessonInfoView.ui.lineEdit.text()
            lesson_description = self.lessonInfoView.ui.textEdit.toPlainText()
            lesson_start_date = self.lessonInfoView.ui.dateTimeEdit_2.dateTime().toString('yyyy-MM-dd HH:mm:ss')
            lesson_end_date = self.lessonInfoView.ui.dateTimeEdit.dateTime().toString('yyyy-MM-dd HH:mm:ss')
            lesson_time = self.lessonInfoView.ui.lineEdit_2.text()
            # print(lesson_name,lesson_description,lesson_start_date,lesson_end_date,lesson_time)
            now_time = datetime.now()
            l_time = self.lessonInfoView.ui.dateTimeEdit_2.dateTime()
            e_time = self.lessonInfoView.ui.dateTimeEdit.dateTime()
            # print(now_time, l_time, e_time)
            time_difference_1 = l_time.secsTo(now_time)
            time_difference_2 = l_time.secsTo(e_time)
            # print(time_difference_1, time_difference_2)
            if time_difference_1 >= 0:
                QMessageBox.information(self, '提示', '课堂开始时间不能早于当前时间', QMessageBox.Ok)
                return
            if time_difference_2 <= 0:
                QMessageBox.information(self, '提示', '课堂结束时间不能早于开始时间', QMessageBox.Ok)
                return
            if lesson_name == '':
                QMessageBox.information(self, '提示', '未输入课堂名称', QMessageBox.Ok)
                return
            elif lesson_time == '0':
                QMessageBox.information(self, '提示', '学习时长未设置', QMessageBox.Ok)
                return
            info = [lesson_name, lesson_time, lesson_start_date, lesson_end_date,
                                lesson_description]
            # print(self.lesson_info)
            lesson_info = [self.userID, self.config_id]
            lesson_info.extend(info)
            msg = [lesson_info]
            self.client.addLesson(msg)
        except Exception as e:
            print('on_clicked_confirm_add_lesson', e)

    def on_clicked_del_lesson(self):
        try:
            if self.is_edit:
                QMessageBox.information(self, '提示', '请先完成修改')
                return
            if self.select_row is None:
                QMessageBox.information(self, '提示', '请选择要删除的课堂信息')
                return
            if self.is_search:
                create_id = self.searchInfo_withID[self.select_row][1]
            else:
                create_id = self.lessonInfo_withID[self.select_row][1]
            if create_id != self.client.tUser[0]:
                QMessageBox.information(self, '提示', '无法操作其他创建者的课堂')
                return
            del_date_time = self.view.tableWidget.item(self.select_row, 2).text()
            now_date_time = self.cAppUtil.get_now_datetime()
            date = re.compile(r"[\d+]+").findall(now_date_time)
            year_n = int(date[0])
            month_n = int(date[1])
            day_n = int(date[2])
            hour_n = int(date[3])
            minute_n = int(date[4])
            date_d = re.compile(r"[\d+]+").findall(del_date_time)
            year_d = int(date_d[0])
            month_d = int(date_d[1])
            day_d = int(date_d[2])
            hour_d = int(date_d[3])
            minute_d = int(date_d[4])
            if year_n > year_d:
                QMessageBox.information(self, '提示', '过期课堂信息不可删除', QMessageBox.Ok)
                return
            elif year_d == year_n:
                if month_n > month_d:
                    QMessageBox.information(self, '提示', '过期课堂信息不可删除', QMessageBox.Ok)
                    return
                elif month_n == month_d:
                    if day_n > day_d:
                        QMessageBox.information(self, '提示', '过期课堂信息不可删除', QMessageBox.Ok)
                        return
                    elif day_d == day_n:
                        if hour_n > hour_d:
                            QMessageBox.information(self, '提示', '过期课堂信息不可删除', QMessageBox.Ok)
                            return
                        elif hour_d == hour_n:
                            if minute_n > minute_d:
                                QMessageBox.information(self, '提示', '过期课堂信息不可删除', QMessageBox.Ok)
                                return
            reply = QMessageBox.information(self, '提示', '是否删除选中的课堂', QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                if self.is_search:
                    self.client.delLesson(REQmsg=[self.searchInfo_withID[self.select_row][0]])
                else:
                    self.client.delLesson(REQmsg=[self.lessonInfo_withID[self.select_row][0]])
        except Exception as e:
            print('on_clicked_patient_del', e)

    def delLessonRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '删除课堂失败, 请重新尝试', QMessageBox.Ok)
                return
            else:
                if self.is_search:
                    class_id = self.searchInfo_withID[self.select_row][0]
                    self.searchInfo_withID.pop(self.select_row)
                    self.searchInfo_without_id.pop(self.select_row)
                    del_row = 0
                    for i in self.lessonInfo_withID:
                        if i[0] == class_id:
                            break
                        else:
                            del_row += 1
                    print(f'del_row={del_row}', f'class_id={class_id}')
                    self.lessonInfo_withoutid.pop(del_row)
                    self.lessonInfo_withID.pop(del_row)
                    self.view.tableWidget.clear()
                    self.view.initTable(self.searchInfo_without_id, self.on_clicked_studentView,self.on_clicked_patientView,
                                        self.on_clicked_show_student,
                                        self.on_clicked_show_file)
                else:
                    self.lessonInfo_withID.pop(self.select_row)
                    self.lessonInfo_withoutid.pop(self.select_row)
                    self.view.tableWidget.clear()
                    self.view.initTable(self.lessonInfo_withoutid, self.on_clicked_studentView,self.on_clicked_patientView,
                                        self.on_clicked_show_student, self.on_clicked_show_file)
                self.select_row = None
                QMessageBox.information(self, '提示', '删除课堂成功', QMessageBox.Ok)
                print(self.lessonInfo_withoutid)
                print(self.lessonInfo_withID)
        except Exception as e:
            print('delLessonRes', e)

    def set_selectRow(self, item):
        self.select_row = item.row()

    def addLessonRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '创建课堂失败, 请重新尝试', QMessageBox.Ok)
                return
            else:
                self.lesson_info = []
                self.check_id = None
                self.select_file_row = []
                self.select_user_row = []
                lesson_info = REPData[1]
                lesson_info_1 = copy.deepcopy(REPData[1])
                lesson_info[0] = self.client.tUser[2]
                class_id = REPData[2]
                self.lessonInfo_withoutid.append(REPData[1])
                self.lessonInfo_withoutid = sorted(self.lessonInfo_withoutid, key=lambda x: x[4], reverse=True)
                print(self.lessonInfo_withoutid)
                if self.is_search:
                    self.searchInfo_without_id.append(REPData[1])
                    self.searchInfo_without_id = sorted(self.searchInfo_without_id, key=lambda x: x[4], reverse=True)
                    self.view.tableWidget.clear()
                    self.view.initTable(self.searchInfo_without_id, self.on_clicked_studentView,self.on_clicked_patientView,
                                        self.on_clicked_show_student, self.on_clicked_show_file)
                else:
                    self.view.tableWidget.clear()
                    self.view.initTable(self.lessonInfo_withoutid,self.on_clicked_studentView,self.on_clicked_patientView,
                                        self.on_clicked_show_student, self.on_clicked_show_file)

                lesson_info_1.insert(0, class_id)
                lesson_info_1[5] = datetime.strptime(lesson_info_1[5], '%Y-%m-%d %H:%M:%S')
                lesson_info_1[6] = datetime.strptime(lesson_info_1[6], '%Y-%m-%d %H:%M:%S')
                self.lessonInfo_withID.append(lesson_info_1)
                self.lessonInfo_withID = sorted(self.lessonInfo_withID, key=lambda x: x[5], reverse=True)
                if self.is_search:
                    self.searchInfo_withID.append(lesson_info_1)
                    self.searchInfo_withID = sorted(self.searchInfo_withID, key=lambda x: x[5], reverse=True)
                print(self.lessonInfo_withID)
                self.lessonInfoView.close()
                QMessageBox.information(self, '提示', '创建课堂成功', QMessageBox.Ok)

        except Exception as e:
            print('addLessonRes', e)

    def addStudentRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '添加课堂学员失败, 请重新尝试', QMessageBox.Ok)
                return
            else:
                is_search = REPData[5]
                student_info = list(REPData[2])
                student_name = []
                for i in student_info:
                    student_name.append(i[3])
                if is_search:
                    self.search_student_page_max = REPData[3]
                    self.search_student_page = REPData[4]
                    self.studentView.ui.label_3.setText("共" + str(self.search_student_page_max) + "页")
                    self.studentView.ui.label_6.setText(str(self.search_student_page))
                else:
                    self.student_page_max = REPData[3]
                    self.student_page_current = REPData[4]
                    self.studentView.ui.label_3.setText("共" + str(self.student_page_max) + "页")
                    self.studentView.ui.label_6.setText(str(self.student_page_current))
                self.studentView.initTable(student_name)
                self.studentView.setWindowModality(Qt.ApplicationModal)
                self.studentView.show()
                QMessageBox.information(self, '提示', '添加课堂学员成功', QMessageBox.Ok)
                self.studentView.selected_row.clear()
        except Exception as e:
            print('addLessonRes', e)



    def on_clicked_show_file(self, row):
        try:
            if self.is_edit:
                QMessageBox.information(self, '提示', '请先完成修改')
                return
            if self.is_search:
                create_id = self.searchInfo_withID[row][1]
            else:
                create_id = self.lessonInfo_withID[row][1]
            if create_id != self.client.tUser[0]:
                QMessageBox.information(self, '提示', '无法操作其他创建者的课堂', QMessageBox.Ok)
                return
            self.PrentryView_info = PrentryView()
            self.PrentryView_info.ui.tableWidget.clear()
            self.client.getContentInfo([self.lessonInfo_withID[row][0], row])
        except Exception as e:
            print('on_clicked_show_file', e)

    def getContentInfoRes(self, REPData):
        try:
            print(REPData)
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '当前课堂暂无培训内容信息, 请添加', QMessageBox.Ok)
                return
            if REPData[2] == []:
                QMessageBox.information(self, '提示', '当前课堂暂无培训内容信息, 请添加', QMessageBox.Ok)
                return
            else:
                content_info = REPData[3]
                self.select_content_row = []
                row = REPData[4]
                class_id = self.lessonInfo_withID[row][0]
                create_id = self.lessonInfo_withID[row][1]
                lesson_name = self.lessonInfo_withID[row][3]
                class_time = self.lessonInfo_withID[row][5]

                self.PrentryView_info.setAttribute(Qt.WA_DeleteOnClose)
                self.PrentryView_info.setWindowTitle("培训内容[课堂内容信息]")
                self.PrentryView_info.setWindowModality(Qt.ApplicationModal)
                self.PrentryView_info.resize(1400, 1000)
                # self.center()
                self.PrentryView_info.ui.btnConfirm.setEnabled(False)
                self.PrentryView_info.ui.btnReturn.setEnabled(False)
                self.PrentryView_info.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.PrentryView_info.ui.tableWidget.resizeRowsToContents()
                self.PrentryView_info.ui.tableWidget.resizeColumnsToContents()
                self.PrentryView_info.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.PrentryView_info.ui.btnConfirm.setText('删除')
                self.PrentryView_info.ui.btnConfirm.setEnabled(True)
                self.PrentryView_info.ui.btnConfirm.clicked.connect(partial(self.on_clicked_del_content_info, class_id
                                                                            , class_time, create_id))
                col_num = 7
                self.PrentryView_info.ui.tableWidget.setColumnCount(col_num)
                itemName = ['可选框', '课堂名称', '检查单号', '病人名称', '文件列表', '标注用户', '课堂目的']
                row_num = len(content_info)
                if row_num <= 0:
                    itemName = ['病例脑电文件列表[无相关内容]']
                for i in range(col_num):
                    header_item = QTableWidgetItem(itemName[i])
                    font = header_item.font()
                    font.setPointSize(10)
                    header_item.setFont(font)
                    header_item.setForeground(QBrush(Qt.black))
                    self.PrentryView_info.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
                self.PrentryView_info.ui.tableWidget.setColumnWidth(0, 20)
                self.PrentryView_info.ui.tableWidget.horizontalHeader().setHighlightSections(False)
                self.PrentryView_info.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.PrentryView_info.ui.tableWidget.setRowCount(row_num)
                for r in range(row_num):
                    i = 1
                    item = QTableWidgetItem(lesson_name)
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(10)
                    item.setFont(font)
                    self.PrentryView_info.ui.tableWidget.setItem(r, i, item)
                    i += 1
                    item = QTableWidgetItem(content_info[r][1])
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(10)
                    item.setFont(font)
                    self.PrentryView_info.ui.tableWidget.setItem(r, i, item)
                    i += 1
                    item = QTableWidgetItem(content_info[r][5])
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(10)
                    item.setFont(font)
                    self.PrentryView_info.ui.tableWidget.setItem(r, i, item)
                    i += 1
                    fn = '{:>03}.bdf'.format(content_info[r][2])
                    item = QTableWidgetItem(fn)
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(10)
                    item.setFont(font)
                    self.PrentryView_info.ui.tableWidget.setItem(r, i, item)
                    i += 1
                    item = QTableWidgetItem(content_info[r][6])
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(10)
                    item.setFont(font)
                    self.PrentryView_info.ui.tableWidget.setItem(r, i, item)
                    i += 1
                    if content_info[r][4] == 'training':
                        item = QTableWidgetItem('培训')
                    else:
                        item = QTableWidgetItem('测试')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(10)
                    item.setFont(font)
                    self.PrentryView_info.ui.tableWidget.setItem(r, i, item)
                    self.add_checkBox_2(r)
                self.PrentryView_info.ui.tableWidget.verticalHeader().setVisible(False)
                self.PrentryView_info.show()
        except Exception as e:
            print('getContentInfoRes', e)

    def add_checkBox_2(self, row):
        exec('self.item_checked_{} = QCheckBox()'.format(row))
        exec('self.item_checked_{}.setCheckState(QtCore.Qt.Unchecked)'.format(row))
        exec('self.item_checked_{}.setCheckable(True)'.format(row))
        exec("self.item_checked_{}.setStyleSheet('''margin:10px''')".format(row))
        exec("self.item_checked_{}.clicked.connect(partial(self.rowSelected_2,{}))".format(row, row))
        exec("self.PrentryView_info.ui.tableWidget.setCellWidget({}, 0, self.item_checked_{})".format(row, row))

    def rowSelected_2(self, row):
        try:
            tag = eval("self.item_checked_{}.isChecked()".format(row))
            # print(tag)
            if tag:
                self.select_content_row.append(row)
                self.select_content_row.sort()
            else:
                if row in self.select_content_row:
                    self.select_content_row.remove(row)
        except Exception as e:
            print('rowSelected_2', e)


    def center(self):
        qr = self.frameGeometry()  # 获取窗口的几何形状
        cp = QDesktopWidget().availableGeometry().center()  # 获取屏幕的中心点
        qr.moveCenter(cp)  # 将窗口的中心点移动到屏幕的中心点
        self.move(qr.topLeft())  # 将窗口移动到新的位置

    def on_clicked_del_content_info(self, class_id, class_time, create_id):
        try:
            # row = self.PrentryView_info.ui.tableWidget.currentRow()
            now_time = datetime.now()
            time_difference = now_time - class_time
            time_difference = int(time_difference.total_seconds())
            # print(time_difference)
            if self.select_content_row == []:
                QMessageBox.information(self, '提示', '请选择要删除的课堂内容', QMessageBox.Ok)
                return
            if time_difference >= 0:
                QMessageBox.information(self, '提示', '课堂已经开始,无法再删除课堂内容', QMessageBox.Ok)
                return
            if create_id != self.client.tUser[0]:
                QMessageBox.information(self, '提示', '无法操作其他创建者的课堂')
                return
            del_info = []
            for i in self.select_content_row:
                check_info = self.PrentryView_info.ui.tableWidget.item(i, 2).text()
                file = self.PrentryView_info.ui.tableWidget.item(i, 4).text()
                uid_name = self.PrentryView_info.ui.tableWidget.item(i, 5).text()
                purpose = self.PrentryView_info.ui.tableWidget.item(i, 6).text()
                if purpose == '培训':
                    purpose = 'training'
                elif purpose == '测试':
                    purpose = 'test'
                file_id = re.findall(r'[1-9]', file)
                temp = [class_id, check_info, uid_name, file_id, purpose]
                del_info.append(temp)
            # file_id = [int(x) for x in file_id_1]
            # patient_name = self.PrentryView_info.ui.tableWidget.item(row, 2).text()
            # patient_id = self.patientNamesDict[patient_name]
            reply = QMessageBox.information(self, '提示', '是否删除选择的课堂内容信息', QMessageBox.Yes|QMessageBox.No)
            if reply == 16384:
                self.client.delLessonContent(del_info)
        except Exception as e:
            print('on_clicked_del_content_info', e)

    def delLessonContentRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '删除课堂内容信息失败, 请重新尝试', QMessageBox.Ok)
                return
            else:
                self.PrentryView_info.close()
                self.select_content_row = []
                QMessageBox.information(self, '提示', '删除课堂内容信息成功', QMessageBox.Ok)
        except Exception as e:
            print('delLessonContentRes', e)

    # 编辑课堂功能
    def on_clicked_edit_lesson(self):
        try:
            row = self.select_row
            if row is None:
                QMessageBox.information(self, '提示', '请选择要修改的课堂信息')
                return
            if self.is_edit:
                QMessageBox.information(self, '提示', '请先完成修改')
                return
            if self.is_search:
                create_id = self.searchInfo_withID[self.select_row][1]
            else:
                create_id = self.lessonInfo_withID[self.select_row][1]
            if create_id != self.client.tUser[0]:
                QMessageBox.information(self, '提示', '无法操作其他创建者的课堂')
                return
            class_date_time = self.view.tableWidget.item(self.select_row, 2).text()
            now_date_time = self.cAppUtil.get_now_datetime()
            date = re.compile(r"[\d+]+").findall(now_date_time)
            print(date)
            year_n = int(date[0])
            month_n = int(date[1])
            day_n = int(date[2])
            hour_n = int(date[3])
            minute_n = int(date[4])
            date_d = re.compile(r"[\d+]+").findall(class_date_time)
            year_d = int(date_d[0])
            month_d = int(date_d[1])
            day_d = int(date_d[2])
            hour_d = int(date_d[3])
            minute_d = int(date_d[4])
            second_d = int(date_d[5])
            if year_n > year_d:
                QMessageBox.information(self, '提示', '过期课堂信息不可编辑', QMessageBox.Ok)
                return
            elif year_d == year_n:
                if month_n > month_d:
                    QMessageBox.information(self, '提示', '过期课堂信息不可编辑', QMessageBox.Ok)
                    return
                elif month_n == month_d:
                    if day_n > day_d:
                        QMessageBox.information(self, '提示', '过期课堂信息不可编辑', QMessageBox.Ok)
                        return
                    elif day_d == day_n:
                        if hour_n > hour_d:
                            QMessageBox.information(self, '提示', '过期课堂信息不可编辑', QMessageBox.Ok)
                            return
                        elif hour_d == hour_n:
                            if minute_n > minute_d:
                                QMessageBox.information(self, '提示', '过期课堂信息不可编辑', QMessageBox.Ok)
                                return
            self.is_edit = True
            self.itemIsEditable(row)
            # 默认日期
            start_date = QDateTime(year_d, month_d, day_d, hour_d, minute_d, second_d)
            e_date = self.view.tableWidget.item(self.select_row, 3).text()
            date_end = re.compile(r"[\d+]+").findall(e_date)
            year_end = int(date_end[0])
            month_end = int(date_end[1])
            day_end = int(date_end[2])
            hour_end = int(date_end[3])
            minute_end = int(date_end[4])
            second_end = int(date_end[5])
            end_date = QDateTime(year_end, month_end, day_end, hour_end, minute_end, second_end)
            self.edit_widget(row, start_date=start_date, end_date=end_date)
            self.confirmBtn.clicked.connect(lambda: self.editConfirm(row))
            self.cancelBtn.clicked.connect(lambda: self.editCancel(row))
        except Exception as e:
            print('on_clicked_edit_lesson', e)

    def itemIsEditable(self, row=-1):
        try:
            if row == -1:
                for i in range(0, self.view.tableWidget.rowCount()):
                    for j in range(0, self.col_num-1):
                        # 设置第i行第j+1列的单元格为可选择且启用状态
                        self.view.tableWidget.item(i, j).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            else:
                for i in range(0, self.view.tableWidget.rowCount()):
                    for j in range(0, self.col_num-1):
                        if i == row:
                            if j == 5:
                                self.view.tableWidget.item(i, j).setFlags(Qt.ItemIsEditable)
                            else:
                                # 设置第row行第j+1列的单元格为可编辑且启用状态
                                self.view.tableWidget.item(i, j).setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
                        else:
                            # 设置第i行第j+1列的单元格不启用
                            self.view.tableWidget.item(i, j).setFlags(Qt.ItemIsEditable)
        except Exception as e:
            print('itemIsEditable', e)

    def edit_widget(self, row, start_date, end_date):
        # print(row)
        # 设置日期时间控件
        self.cWidget1 = QDateTimeEdit()
        self.cWidget2 = QDateTimeEdit()
        print(start_date, end_date)
        # 设置是否启用日历弹出显示模式
        self.cWidget1.setCalendarPopup(True)
        self.cWidget2.setCalendarPopup(True)
        self.cWidget1.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.cWidget2.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.cWidget1.setDateTime(start_date)
        self.cWidget2.setDateTime(end_date)
        # 在给定行和列的单元格中显示给定小部件
        self.view.tableWidget.setCellWidget(row, 2, self.cWidget1)
        self.view.tableWidget.setCellWidget(row, 3, self.cWidget2)
        # 为新一行添加特定的操作按钮
        widget = QWidget()
        layout = QHBoxLayout()
        self.confirmBtn = QPushButton('确认修改')
        self.cancelBtn = QPushButton('取消修改')
        layout.addWidget(self.confirmBtn)
        layout.addWidget(self.cancelBtn)
        layout.setStretch(0, 1)
        layout.setStretch(1, 1)
        self.cancelBtn.setStyleSheet('''width:80px;font : 18px''')
        self.confirmBtn.setStyleSheet('''width:80px;font : 18px''')
        widget.setLayout(layout)
        self.view.ui.horizontalLayout.addWidget(widget)


    def editCancel(self, row):
        try:
            reply = QMessageBox.information(self, "提示", '是否取消修改', QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                self.clear(row)
                self.itemIsEditable()
                self.is_edit = False
                for i in range(0, self.col_num - 2):
                    self.view.tableWidget.item(row, i).setText(self.lessonInfo_withoutid[row][i+2])
        except Exception as e:
            print('editCancel', e)

    def editConfirm(self, row):
        try:
            # 当前编辑的课堂信息
            lesson_info = []
            row_num = row
            if self.is_search:
                lesson_info.append(self.searchInfo_withID[row_num][0])
            else:
                lesson_info.append(self.lessonInfo_withID[row_num][0])
            now_date = datetime.now()
            start_date = self.cWidget1.dateTime()
            end_date = self.cWidget2.dateTime()
            # print(now_time, l_time, e_time)
            time_difference_1 = start_date.secsTo(now_date)
            time_difference_2 = start_date.secsTo(end_date)
            if time_difference_1 >= 0:
                QMessageBox.information(self, '提示', '课堂开始时间不能早于当前时间', QMessageBox.Ok)
                return
            if time_difference_2 <= 0:
                QMessageBox.information(self, '提示', '课堂结束时间不能早于开始时间', QMessageBox.Ok)
                return
            start_date = start_date.toString("yyyy-MM-dd HH:mm:ss")
            end_date = end_date.toString("yyyy-MM-dd HH:mm:ss")
            for j in range(0, self.col_num - 2):
                if j == 2:
                    lesson_info.append(start_date)
                elif j == 3:
                    lesson_info.append(end_date)
                else:
                    lesson_info.append(self.view.tableWidget.item(row_num, j).text())
                    # print(j)
            print(lesson_info)
            self.clear(row)
            self.client.updateLesson(REQmsg=[lesson_info, self.userID, self.config_id])
        except Exception as e:
            print('editConfirm', e)

    def updateLessonRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '更新课堂信息失败, 请重新尝试', QMessageBox.Ok)
                self.is_edit = False
                return
            else:
                lesson_info_id = REPData[1]
                print(lesson_info_id)
                class_id = lesson_info_id[0]
                lesson_info = REPData[1][1:]
                print(lesson_info)
                if self.is_search:
                    edit_row = 0
                    for i in self.lessonInfo_withID:
                        if i[0] == class_id:
                            break
                        else:
                            edit_row += 1
                    for i in range(3, 8):
                        self.searchInfo_withID[self.select_row][i] = lesson_info_id[i-2]
                    self.searchInfo_withID[self.select_row][5] = datetime.strptime(
                        self.searchInfo_withID[self.select_row][5], '%Y-%m-%d %H:%M:%S')
                    self.searchInfo_withID[self.select_row][6] = datetime.strptime(
                        self.searchInfo_withID[self.select_row][6], '%Y-%m-%d %H:%M:%S')
                    for i in range(2, 7):
                        self.searchInfo_without_id[self.select_row][i] = lesson_info[i-2]
                    for i in range(3, 8):
                        self.lessonInfo_withID[edit_row][i] = lesson_info_id[i-2]
                    for i in range(2, 7):
                        self.lessonInfo_withoutid[edit_row][i] = lesson_info[i-2]
                    self.view.tableWidget.clear()
                    self.view.initTable(self.searchInfo_without_id,
                                        self.on_clicked_studentView,self.on_clicked_patientView,self.on_clicked_show_student,
                                        self.on_clicked_show_file)
                else:
                    for i in range(3, 8):
                        self.lessonInfo_withID[self.select_row][i] = lesson_info_id[i-2]
                    self.lessonInfo_withID[self.select_row][5] = datetime.strptime(
                        self.lessonInfo_withID[self.select_row][5], '%Y-%m-%d %H:%M:%S')
                    self.lessonInfo_withID[self.select_row][6] = datetime.strptime(
                        self.lessonInfo_withID[self.select_row][6], '%Y-%m-%d %H:%M:%S')
                    print(self.lessonInfo_withID)
                    for i in range(2, 7):
                        self.lessonInfo_withoutid[self.select_row][i] = lesson_info[i-2]
                    print(self.lessonInfo_withoutid)
                    self.view.tableWidget.clear()
                    self.view.initTable(self.lessonInfo_withoutid, self.on_clicked_studentView,self.on_clicked_patientView,
                                        self.on_clicked_show_student, self.on_clicked_show_file)
                self.select_row = None
                QMessageBox.information(self, '提示', '更新课堂信息成功', QMessageBox.Ok)
                self.is_edit = False
        except Exception as e:
            print('updateLessonRes', e)


    # 查看学生信息重新选择功能
    def on_clicked_show_student(self, row):
        try:
            if self.is_edit:
                QMessageBox.information(self, '提示', '请先完成修改')
                return
            if self.is_search:
                create_id = self.searchInfo_withID[row][1]
            else:
                create_id = self.lessonInfo_withID[row][1]
            if create_id != self.client.tUser[0]:
                QMessageBox.information(self, '提示', '无法操作其他创建者的课堂', QMessageBox.Ok)
                return
            self.studentView_info = studentInfoView()
            self.client.getStudentInfo([self.lessonInfo_withID[row][0], row])
        except Exception as e:
            print('on_clicked_show_student', e)

    def getStudentInfoRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '获取学员信息失败, 请重新尝试', QMessageBox.Ok)
                return
            else:
                row = REPData[3]
                class_id = self.lessonInfo_withID[row][0]
                create_id = self.lessonInfo_withID[row][1]
                class_time = self.lessonInfo_withID[row][5]
                student_info = REPData[2]
                student_name_info = []
                for i in student_info:
                    student_name_info.append(self.student_id_name_dic[i[1]])
                print(student_name_info)
                self.studentView_info.ui.label.setText('课堂学员信息')
                self.studentView_info.ui.pushButton_2.setText('删除')
                self.studentView_info.ui.pushButton.setEnabled(False)
                self.studentView_info.ui.pushButton_2.clicked.connect(partial(self.on_clicked_del_student_info,
                                                                              class_id, class_time, create_id))
                self.studentView_info.initTable(student_name_info)
                self.studentView_info.show()
        except Exception as e:
            print('getStudentInfoRes', e)

    def on_clicked_del_student_info(self, class_id, class_time, create_id):
        try:
            now_time = datetime.now()
            # start_time = datetime.strptime(class_time, '%Y-%m-%d %H:%M:%S')
            time_difference = now_time - class_time
            time_difference = int(time_difference.total_seconds())
            # print(time_difference)
            if self.studentView_info.selected_row == []:
                QMessageBox.information(self, '提示', '请选择要删除的学员', QMessageBox.Ok)
                return
            elif time_difference >= 0:
                QMessageBox.information(self, '提示', '课堂已经开始,无法再删除课堂学员', QMessageBox.Ok)
                return
            if create_id != self.client.tUser[0]:
                QMessageBox.information(self, '提示', '无法操作其他创建者的课堂')
                return
            del_student_id = []
            for index in self.studentView_info.selected_row:
                student_name = self.studentView_info.ui.tableWidget.item(index, 1).text()
                del_student_id.append(self.studentInfo[student_name])
            reply = QMessageBox.information(self, '提示', '是否删除选中的学员', QMessageBox.Yes|QMessageBox.No)
            if reply == 16384:
                self.client.delStudent([del_student_id, class_id])
        except Exception as e:
            print('on_clicked_del_student_info', e)

    def delStudentRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '删除课堂学员失败, 请重新尝试', QMessageBox.Ok)
                return
            else:
                self.studentView_info.selected_row = []
                self.studentView_info.close()
                QMessageBox.information(self, '提示', '删除课堂学员成功', QMessageBox.Ok)
        except Exception as e:
            print('addLessonRes', e)

    # def updateStudentInfoRes(self, REPData):
    #     try:
    #         if REPData[0] == '0':
    #             QMessageBox.information(self, '提示', '更新学员信息失败, 请重新尝试', QMessageBox.Ok)
    #             return
    #         else:
    #             QMessageBox.information(self, '提示', '更新学员信息成功', QMessageBox.Ok)
    #             self.studentView.close()
    #     except Exception as e:
    #         print('updateStudentInfoRes', e)

    # def updateContentInfoRes(self, REPData):
    #     try:
    #         if REPData[0] == '0':
    #             QMessageBox.information(self, '提示', '更新文件信息失败, 请重新尝试', QMessageBox.Ok)
    #             return
    #         else:
    #             self.select_file_row = []
    #             QMessageBox.information(self, '提示', '更新文件信息成功', QMessageBox.Ok)
    #             self.prentryView.close()
    #     except Exception as e:
    #         print('updateStudentInfoRes', e)

    def clear(self, row):
        # 清理起始日期控件
        self.view.tableWidget.removeCellWidget(row, 2)
        # 清理截至日期控件
        self.view.tableWidget.removeCellWidget(row, 3)
        # 清理确认和取消的按钮布局
        item_list_length = self.view.ui.horizontalLayout.count()
        item = self.view.ui.horizontalLayout.itemAt(item_list_length - 1)
        self.view.ui.horizontalLayout.removeItem(item)
        if item.widget():
            item.widget().deleteLater()

    def exit(self):
        self.client.getLessonInfoResSig.disconnect()
        self.client.getDiagCheckIDResSig.disconnect()
        self.client.getFileNameResSig.disconnect()
        self.client.addLessonResSig.disconnect()
        self.client.delLessonResSig.disconnect()
        self.client.updateLessonResSig.disconnect()
        self.client.getStudentInfoResSig.disconnect()
        # self.client.updateStudentInfoResSig.disconnect()
        self.client.getContentInfoResSig.disconnect()
        # self.client.updateContentInfoResSig.disconnect()
        self.client.inquiryLessonInfoResSig.disconnect()
        self.client.getCheckUserIDResSig.disconnect()
        self.client.addStudentResSig.disconnect()
        self.client.getlessonStudentResSig.disconnect()
        self.client.delStudentResSig.disconnect()
        self.client.addLessonContentResSig.disconnect()
        self.client.delLessonContentResSig.disconnect()
        self.client.studentPagingResSig.disconnect()
        self.client.searchStudentPageInfoResSig.disconnect()
