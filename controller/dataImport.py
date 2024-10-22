import ctypes
import inspect
import math
import os.path
import pickle
import sys
import threading
from datetime import datetime
from time import time, sleep

import mne
from PyQt5.Qt import *
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QRect, QDateTime, QTimer
from PyQt5.QtGui import QBrush, QFont
from PyQt5.QtWidgets import *
from view.dataImport import DataImportView
from view.dataImport import AddFormView
import pyedflib
import re
import datetime
from view.dataImport_form.patient_table import PatientTableWidget
from view.dataImport_form.doctor_table import DoctorTableWidget




class dataImportController(QWidget):
    # 上传信号
    uploadFileSig = pyqtSignal()
    # 进度条相关信号
    upload_finished = pyqtSignal()
    upload_failed = pyqtSignal()
    # update_process = pyqtSignal(int)
    def __init__(self, client, cAppUtil):
        super().__init__()

        self.client = client
        self.cAppUtil = cAppUtil
        self.view = DataImportView()
        self.root_path = os.path.join(os.path.dirname(__file__))[:-10]
        # 存放处理过后的脑电文件目录
        self.dir_path = os.path.join(self.root_path, 'upload', 'EEG')

        self.client.getPatientCheckInfoResSig.connect(self.getPatientCheckInfoRes)
        self.client.delPatientCheckInfoResSig.connect(self.delPatientCheckInfoRes)
        self.client.addCheckInfoResSig.connect(self.addCheckInfoRes)
        self.client.checkMakeFileNameResSig.connect(self.checkMakeFileNameRes)
        self.client.writeEEGResSig.connect(self.writeEEGRes)
        self.client.updateCheckInfoResSig.connect(self.updateCheckInfoRes)
        self.client.getFileInfoResSig.connect(self.getFileInfoRes)
        self.client.getChoosePatientInfoResSig.connect(self.get_choose_patient_infoRes)
        self.client.getChooseDoctorInfoResSig.connect(self.get_choose_doctor_infoRes)
        self.uploadFileSig.connect(self.on_btnUpload_clicked)


        # 如果服务端出现异常关闭当前界面的所有线程
        self.client.serverExceptSig.connect(self.upload_failedCall)


        # 进度条值
        # 全局变量
        self.progress_value = 0
        # 处理的线程
        self.processthread = None

        # # 存放当前标注类型信息列表
        self.patientCheck_info = []
        # 存放脑电数据信息列表
        self.file_info = []
        # 存放所有医生信息
        self.doctor = []
        # 存放所有病人
        self.patient = []

        # 当前选择行索引
        self.row = -1
        # 用来保存文件每次传的块大小(5M)
        self.block_size = 5*1024*1024
        # 用来存放当前文件大小
        self.block_num = None
        # 存放选中需要转换的脑电文件路径
        self.from_filepath = None
        # 增加bdf文件转化为edf文件后的新文件名
        self.convert_filepath = None
        # 存放返回的脑电文件名字
        self.file_path = None
        # 存放获取的文件名
        self.filename = None
        # 存放要上传的脑电文件check_id
        self.check_id = None
        # 存放要上传文件的file_id
        self.file_id = None
        # 存放用户当前config_id
        self.config_id = self.client.tUser[12]
        # 存放当前check_id的file_infoxinxi
        self.change_file = None

        # 每页的样本最大数量
        self.perPageNum = 13

        # 获取两个表格的信息
        self.getPatientCheckInfo()

        # self.view.ui.flushButton.clicked.connect(self.on_flushButton_clicked)
        self.view.ui.delButton.clicked.connect(self.on_btnDel_clicked)
        # self.view.ui.addButton.clicked.connect(self.on_btnAdd_clicked)
        self.view.ui.chooseBtn.clicked.connect(self.on_btnChoose_clicked)
        self.view.ui.processButton.clicked.connect(self.on_btnProcess_clicked)

        self.view.ui.sendMsgButton.clicked.connect(self.on_btnSendMsg_clicked)

        # 进度条相关
        # self.update_process.connect(self.update_processCall)
        self.upload_finished.connect(self.upload_finishedCall)
        self.upload_failed.connect(self.upload_failedCall)

        # 先设置处理文件按钮不可用
        self.view.ui.processButton.setDisabled(True)

        # # 只能选中一行
        self.view.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.ui.tableWidget.resizeRowsToContents()
        self.view.ui.tableWidget.resizeRowsToContents()
        self.view.ui.tableWidget.resizeColumnsToContents()
        self.view.ui.tableWidget.clicked.connect(self.on_tableWidget_itemClicked)


        self.view.ui.tableWidget_2.setSelectionMode(QAbstractItemView.NoSelection)
        self.view.ui.tableWidget_2.resizeRowsToContents()
        self.view.ui.tableWidget_2.resizeRowsToContents()
        self.view.ui.tableWidget_2.resizeColumnsToContents()

        # 设置按钮初始状态
        self.view.ui.chooseBtn.setEnabled(False)
        self.view.ui.processButton.setEnabled(False)
        self.view.ui.delButton.setEnabled(False)
        self.view.ui.sendMsgButton.setEnabled(False)


        # 存储添加的信息
        self.addInfo = {}

        # 添加部分的槽函数链接
        # 设置选择医生
        self.view.ui.patientBtn.clicked.connect(self.onChoose_Patient)
        # self.addFormView.ui.patientBtn.clicked.connect(self.onChoose_Patient)
        self.view.ui.pdoctorBtn.clicked.connect(self.onChoose_Doctor)
        # self.addFormView.ui.pdoctorBtn.clicked.connect(self.onChoose_Doctor)

        # 设置选中病人
        self.view.ui.btnConfirm.clicked.connect(self.onClick_ButtonToText)
        self.view.ui.btnExit.clicked.connect(self.on_btnCancelAdd_clicked)

        # 设置当前上传脑电医生
        self.view.ui.label_cdoctor.setText(self.client.tUser[2])
        # self.ui.label_cdoctor.setText(self.client.tUser[2])
        # self.addFormView.ui.btnConfirm.clicked.connect(self.onClick_ButtonToText)
        # self.addFormView.ui.btnExit.clicked.connect(self.on_btnCancelAdd_clicked)



    # 获取病人检查信息功能
    # 获取病人检查信息方法
    def getPatientCheckInfo(self, value=''):
        account = self.client.tUser[1]
        uid = self.client.tUser[0]
        REQmsg = [account, uid, value]
        self.client.getPatientCheckInfo(REQmsg)

    # 处理客户端返回的查询标注类型的结果
    def getPatientCheckInfoRes(self, REPData):
        try:
            if REPData[0] == '1':

                self.view.ui.textEdit.clear()
                # 清空file_info界面
                self.view.ui.tableWidget_2.setRowCount(0)
                self.view.ui.tableWidget_2.clearContents()

                patientCheck_info_1 = REPData[3][0]

                # 增加了文件信息获取
                self.file_info = REPData[3][3]
                if len(patientCheck_info_1) != 0:
                    self.patientCheck_info = patientCheck_info_1
                    # 设置当存在记录的时候就不能添加
                    if len(self.patientCheck_info) >= 1:
                        # self.view.ui.addButton.setEnabled(False)
                        self.view.ui.groupBox_4.setEnabled(False)
                        # self.view.ui.delButton.setEnabled(True)
                        # pass
                    # self.view.ui.lineValue.clear()
                    self.view.ui.delButton.setEnabled(True)
                    self.view.initTable(self.patientCheck_info)
                    if len(self.file_info) != 0:

                        self.change_file=self.changeFileInfo(self.file_info)

                        # self.view.initTable_1(self.file_info)

                    # 检查是否有没有传完的文件
                    self.checkDirNull()
                    # QMessageBox.information(self, "病人诊断信息", '查询成功！')
                else:
                    # 设置添加按钮起作用
                    self.view.ui.groupBox_4.setEnabled(True)
                    # self.view.ui.addButton.setEnabled(True)
                    # 如果不存在病人检查单信息直接清空两个表格
                    self.view.ui.textEdit.clear()
                    # 清空file_info界面
                    self.view.ui.tableWidget_2.setRowCount(0)
                    self.view.ui.tableWidget_2.clearContents()

                    self.view.initTable(None)
                    self.view.ui.tableWidget.setRowCount(0)
                    self.view.ui.tableWidget.clearContents()
                    # 如果没有信息显示自动弹出添加框
                    # self.on_btnAdd_clicked()


            else:
                QMessageBox.information(self, "病人诊断信息", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('getPatientCheckInfoRes', e)

    # 获取脑电数据文件
    def getFileInfo(self, value=''):
        account = self.client.tUser[1]
        uid = self.client.tUser[0]
        REQmsg = [account, uid, value]
        self.client.getFileInfo(REQmsg)

    # 处理客户端返回的查询获取脑电数据文件的结果
    def getFileInfoRes(self, REPData):
        print('REPData:',REPData)
        try:
            if REPData[0] == '1':
                file_info_1 = REPData[3]
                if len(file_info_1) != 0:
                    self.file_info = file_info_1
                    # TODO:暂时这样修改
                    self.change_file = self.changeFileInfo(self.file_info)
                    if self.row != -1:
                        check_id = self.patientCheck_info[self.row][0]
                        if check_id in self.change_file.keys():
                            self.view.initTable_1(self.change_file[check_id])
                            self.view.ui.sendMsgButton.setEnabled(True)
                        else:
                            # 该方法只能清除内容，表头还是保留的
                            # self.view.ui.tableWidget_2.clear()
                            self.view.ui.sendMsgButton.setEnabled(False)
                            self.view.ui.tableWidget_2.setRowCount(0)
                            self.view.ui.tableWidget_2.clearContents()
                    # self.view.initTable_1(self.file_info)
                    # QMessageBox.information(self, "病人诊断信息", '查询成功！')
                else:
                    self.change_file = None
                    # self.change_file = self.changeFileInfo(self.file_info)
                    # self.view.initTable_1(self.file_info)
            else:
                QMessageBox.information(self, "脑电数据信息", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('getFileInfoRes', e)


    # 添加病人检查信息类型功能
    # 添加病人检查信息方法
    def on_btnAdd_clicked(self):
        self.addFormView = AddFormView()
        # 设置不关闭对话框就不进行其他操作
        self.addFormView.setWindowModality(Qt.ApplicationModal)
        self.addFormView.show()

        # 显示对话框，阻塞程序直到对话框关闭
        # result = self.addFormView.exec_()

        # 暂存增加的所有信息
        self.addInfo = {}
        self.addFormView.initTabel(self.client.tUser[2])
        # 找到当前医生用户在下拉列表位置
        # index = [self.doctor.index(i) for i in self.doctor if i[0] == self.client.tUser[0]]
        # 设置开单和诊断医生都为当前医生
        # self.addFormView.ui.combo_cdoctor.setCurrentIndex(index[0])
        # self.addFormView.ui.combo_pdoctor.setCurrentIndex(index[0])

        # 设置选择医生
        self.addFormView.ui.patientBtn.clicked.connect(self.onChoose_Patient)
        self.addFormView.ui.pdoctorBtn.clicked.connect(self.onChoose_Doctor)

        # 设置选中病人
        self.addFormView.ui.btnConfirm.clicked.connect(self.onClick_ButtonToText)
        self.addFormView.ui.btnExit.clicked.connect(self.on_btnCancelAdd_clicked)
        # 设置关闭对象自动释放资源
        self.addFormView.setAttribute(Qt.WA_DeleteOnClose)


    # 点击选择病人方法
    def onChoose_Patient(self):
        # 获取病人信息
        # self.addFormView.hide()
        self.get_choose_patient_info(flag='1')

    # 获取病人信息
    def get_choose_patient_info(self, flag='1', key_word='', key_value=''):
        # 获取病人所有信息
        if flag == '1':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum]
            self.client.getChoosePatientInfo(REQmsg)
        # 病人信息没有条件的翻页
        elif flag == '2':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.patient_start]
            self.client.getChoosePatientInfo(REQmsg)
        # 病人信息重置的首页
        elif flag == '3':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum]
            self.client.getChoosePatientInfo(REQmsg)
        # 病人信息有条件的首页
        elif flag == '4':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, key_word, key_value]
            self.client.getChoosePatientInfo(REQmsg)
        # 病人信息有搜索条件的翻页
        elif flag == '5':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.patient_start, key_word, key_value]
            self.client.getChoosePatientInfo(REQmsg)
        else:
            pass

    # 获取病人信息返回的结果
    def get_choose_patient_infoRes(self, REPData):
        try:
            if REPData[0] == '1':
                flag = REPData[3][0]
                if flag == '1':
                    patient_info = REPData[3][1]
                    self.patient_info = patient_info
                    self.patient_totalNum = REPData[3][2]
                    col_label_detail = ['姓名', '出生日期', '性别', '卡号', '操作']
                    # detail_info = [('235353', '林一', 897), ('00000', '王二', 888)]
                    # totalNumDetail = 2

                    # 初始化除了表格以外其他框架
                    self.view.tableWidget_patient = PatientTableWidget()
                    # 初始化选择框
                    self.view.tableWidget_patient.comboCond.addItems(['姓名', '卡号'])

                    self.view.tableWidget_patient.resize(1500, 800)
                    self.view.tableWidget_patient.setWindowTitle("病人相关信息")
                    # 初始化表格信息
                    self.view.tableWidget_patient.init_ui(col_label=col_label_detail,
                                                                       sampleList=self.patient_info,
                                                                       totalNum=self.patient_totalNum,
                                                                       on_clicked_selectBtn=self.patient_on_clicked_selectBtn)
                    # 返回
                    self.view.tableWidget_patient.returnBtn.triggered.connect(self.patientReturnBtnTrigger)
                    # 搜索
                    self.view.tableWidget_patient.btnSelect.clicked.connect(self.search_patient)
                    # 重置
                    self.view.tableWidget_patient.btnReSelect.clicked.connect(self.research_patient)
                    # 页码相关
                    self.patient_page = math.ceil(self.patient_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_patient.setPageController(self.patient_page)
                    self.view.tableWidget_patient.control_signal.connect(self.patient_page_controller)

                    # 设置不关闭对话框就不进行其他操作
                    self.view.tableWidget_patient.setWindowModality(Qt.ApplicationModal)
                    # 设置关闭对象自动释放资源
                    self.view.tableWidget_patient.setAttribute(Qt.WA_DeleteOnClose)

                    self.view.tableWidget_patient.show()
                elif flag == '2':
                    patient_info = REPData[3][1]
                    self.patient_info = patient_info
                    # self.theme_info = theme_info
                    if self.patient_info:
                        self.clear(self.view.tableWidget_patient.verticalLayout_1)
                        col_label_detail = ['姓名', '出生日期', '性别', '卡号', '操作']
                        # 页码不会改变是因为这里创建时候没有传入当前页码值
                        # 这里只是改变重新创建当前表格值
                        self.view.tableWidget_patient.init_ui(current_page=self.patient_cur_page, col_label=col_label_detail,
                                                            sampleList=self.patient_info, totalNum=self.patient_totalNum,
                                                            on_clicked_selectBtn=self.patient_on_clicked_selectBtn)

                        # 源代码
                        if self.patient_is_fromSkip:
                            self.view.tableWidget_patient.skipPage.setText(str(self.patient_cur_page))
                        else:
                            self.view.tableWidget_patient.skipPage.setText(str(self.patient_skip_page))
                    else:
                        QMessageBox.information(self, "分页信息查询", '下一页无信息！！', QMessageBox.Yes)
                elif flag == '3':
                    # 清除表格内容
                    self.clear(self.view.tableWidget_patient.verticalLayout_1)
                    # 清除页面控制器
                    self.view.tableWidget_patient.control_signal.disconnect(self.patient_page_controller)
                    self.clear(self.view.tableWidget_patient.control_layout)
                    patient_info = REPData[3][1]
                    self.patient_info = patient_info
                    self.patient_totalNum = REPData[3][2]
                    col_label_detail = ['姓名', '出生日期', '性别', '卡号', '操作']
                    self.view.tableWidget_patient.init_ui(col_label=col_label_detail,
                                                          sampleList=patient_info,
                                                          totalNum=self.patient_totalNum,
                                                          on_clicked_selectBtn=self.patient_on_clicked_selectBtn)
                    # 页码相关
                    self.patient_page = math.ceil(self.patient_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_patient.setPageController(self.patient_page)
                    self.view.tableWidget_patient.control_signal.connect(self.patient_page_controller)

                # 点击搜索按钮
                elif flag == '4':
                    # 清除表格内容
                    self.clear(self.view.tableWidget_patient.verticalLayout_1)
                    # 清除页面控制器
                    self.view.tableWidget_patient.control_signal.disconnect(self.patient_page_controller)
                    self.clear(self.view.tableWidget_patient.control_layout)
                    patient_info = REPData[3][1]
                    self.patient_info = patient_info
                    self.patient_totalNum = REPData[3][2]
                    col_label_detail = ['姓名', '出生日期', '性别', '卡号', '操作']
                    self.view.tableWidget_patient.init_ui(col_label=col_label_detail,
                                                          sampleList=patient_info,
                                                          totalNum=self.patient_totalNum,
                                                          on_clicked_selectBtn=self.patient_on_clicked_selectBtn)
                    # 页码相关
                    self.patient_page = math.ceil(self.patient_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_patient.setPageController(self.patient_page)
                    self.view.tableWidget_patient.control_signal.connect(self.patient_page_controller)
                elif flag == '5':
                    patient_info = REPData[3][1]
                    self.patient_info = patient_info
                    # self.theme_info = theme_info
                    if patient_info:
                        self.clear(self.view.tableWidget_patient.verticalLayout_1)
                        col_label_detail = ['姓名', '出生日期', '性别', '卡号', '操作']
                        # 页码不会改变是因为这里创建时候没有传入当前页码值
                        # 这里只是改变重新创建当前表格值
                        self.view.tableWidget_patient.init_ui(current_page=self.patient_cur_page,
                                                              col_label=col_label_detail,
                                                              sampleList=patient_info, totalNum=self.patient_totalNum,
                                                              on_clicked_selectBtn=self.patient_on_clicked_selectBtn)

                        # 源代码
                        if self.patient_is_fromSkip:
                            self.view.tableWidget_patient.skipPage.setText(str(self.patient_cur_page))
                        else:
                            self.view.tableWidget_patient.skipPage.setText(str(self.patient_skip_page))
                    else:
                        QMessageBox.information(self, "分页信息查询", '下一页无信息！！', QMessageBox.Yes)

                else:
                    pass
        except Exception as e:
            print('get_choose_patient_infoRes', e)

    # 选择具体某个病人信息后方法
    def patient_on_clicked_selectBtn(self, row):
        print("选中当前行：", row)
        id = self.patient_info[row][0]
        print("当前选中用户的id为:", id)
        name = self.patient_info[row][1]
        print("当前选中用户的姓名为:", name)
        # 将选中行的内容添加到暂存的添加
        self.addInfo['patient_id'] = id
        self.view.tableWidget_patient.hide()
        self.view.ui.patientBtn.setText(name)
        self.view.ui.patientBtn.setFont(QFont("Agency FB", 16))
        self.view.ui.patientBtn.setStyleSheet("color: blue;")

        # self.addFormView.ui.patientBtn.setText(name)
        # self.addFormView.ui.patientBtn.setFont(QFont("Agency FB", 12))
        # self.addFormView.ui.patientBtn.setStyleSheet("color: blue;")
        # self.addFormView.show()


    # 选择病人的搜索功能首页界面
    def search_patient(self):
        key_word = self.view.tableWidget_patient.comboCond.currentText()
        key_value = self.view.tableWidget_patient.lineValue.text()
        if key_word == '姓名':
            key_word = 'name'
        elif key_word == '卡号':
            key_word = 'card'
        print("key_word:", key_word)
        print("key_value:", key_value)
        # 只有当搜索框有值时候才搜索
        if key_value:
            self.get_choose_patient_info(flag='4', key_word=key_word, key_value=key_value)
        else:
            QMessageBox.information(self, "提示", "搜索框内没有填写内容!!", QMessageBox.Yes)


    # 选择病人的重置功能
    def research_patient(self):
        self.view.tableWidget_patient.comboCond.setCurrentIndex(0)
        self.view.tableWidget_patient.lineValue.clear()
        self.get_choose_patient_info(flag='3')


    # 选择病人信息的返回
    def patientReturnBtnTrigger(self):
        self.view.tableWidget_patient.hide()
        # self.addFormView.show()
        print("返回上级按键被触发！！！")

    # 病人选择信息界面相关跳转
    def patient_page_controller(self, signal):
        total_page = self.view.tableWidget_patient.showTotalPage()
        is_fromSkip = False
        if "home" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                return
            self.view.tableWidget_patient.curPage.setText("1")
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            self.view.tableWidget_patient.curPage.setText(str(int(signal[1]) - 1))
        elif "next" == signal[0]:
            if total_page == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.view.tableWidget_patient.curPage.setText(str(int(signal[1]) + 1))
        elif "final" == signal[0]:
            self.view.tableWidget_patient.curPage.setText(str(total_page))
        elif "confirm" == signal[0]:
            if total_page < int(signal[1]) or int(signal[1]) < 1:
                QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                self.view.tableWidget_patient.skipPage.setText('1')
                return
            is_fromSkip = True
            self.view.tableWidget_patient.curPage.setText(signal[1])
        self.changeTableContent_patient(is_fromSkip)  # 改变表格内容

    def changeTableContent_patient(self, is_fromSkip):
        """根据当前页改变表格的内容"""
        self.patient_is_fromSkip = is_fromSkip
        self.patient_cur_page = int(self.view.tableWidget_patient.curPage.text())
        self.patient_skip_page = int(self.view.tableWidget_patient.skipPage.text())
        self.patient_start = (self.patient_cur_page - 1) * self.perPageNum
        # theme_id = self.theme_detailID
        # row = self.row_detail

        key_word = self.view.tableWidget_patient.comboCond.currentText()
        key_value = self.view.tableWidget_patient.lineValue.text()
        if key_word == '姓名':
            key_word = 'name'
        elif key_word == '卡号':
            key_word = 'card'
        print("key_word:", key_word)
        print("key_value:", key_value)
        # 只有当搜索框有值时候才搜索
        if key_value:
            # 有搜索条件的翻页
            self.get_choose_patient_info(flag='5', key_word=key_word, key_value=key_value)
        else:
            # 无搜索条件的翻页
            self.get_choose_patient_info(flag='2')


    # 清理布局
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


    # 选择医生信息
    def onChoose_Doctor(self):
        # self.addFormView.hide()
        self.get_choose_doctor_info(flag='1')

    # 获取医生信息
    def get_choose_doctor_info(self, flag='1', key_word='', key_value=''):
        # 获取医生所有信息
        if flag == '1':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum]
            self.client.getChooseDoctorInfo(REQmsg)
        # 医生信息没有条件的翻页
        elif flag == '2':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.doctor_start]
            self.client.getChooseDoctorInfo(REQmsg)
        # 医生信息重置的首页
        elif flag == '3':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum]
            self.client.getChooseDoctorInfo(REQmsg)
        # 医生信息有条件的首页
        elif flag == '4':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, key_word, key_value]
            self.client.getChooseDoctorInfo(REQmsg)
        # 医生信息有搜索条件的翻页
        elif flag == '5':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.doctor_start, key_word, key_value]
            self.client.getChooseDoctorInfo(REQmsg)
        else:
            pass


    # 获取医生信息返回的结果
    def get_choose_doctor_infoRes(self, REPData):
        try:
            if REPData[0] == '1':
                flag = REPData[3][0]
                if flag == '1':
                    doctor_info = REPData[3][1]
                    self.doctor_info = doctor_info
                    self.doctor_totalNum = REPData[3][2]
                    col_label_detail = ['姓名', '电话', '邮箱', '操作']
                    # 初始化除了表格以外其他框架
                    self.view.tableWidget_doctor = DoctorTableWidget()
                    # 初始化选择框
                    self.view.tableWidget_doctor.comboCond.addItems(['姓名', '电话', '邮箱'])

                    self.view.tableWidget_doctor.resize(1500, 800)
                    self.view.tableWidget_doctor.setWindowTitle("医生相关信息")
                    # 初始化表格信息
                    self.view.tableWidget_doctor.init_ui(col_label=col_label_detail,
                                                          sampleList=self.doctor_info,
                                                          totalNum=self.doctor_totalNum,
                                                          on_clicked_selectBtn=self.doctor_on_clicked_selectBtn)
                    # 返回
                    self.view.tableWidget_doctor.returnBtn.triggered.connect(self.doctorReturnBtnTrigger)
                    # 搜索
                    self.view.tableWidget_doctor.btnSelect.clicked.connect(self.search_doctor)
                    # 重置
                    self.view.tableWidget_doctor.btnReSelect.clicked.connect(self.research_doctor)
                    # 页码相关
                    self.doctor_page = math.ceil(self.doctor_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_doctor.setPageController(self.doctor_page)
                    self.view.tableWidget_doctor.control_signal.connect(self.doctor_page_controller)

                    # 设置不关闭对话框就不进行其他操作
                    self.view.tableWidget_doctor.setWindowModality(Qt.ApplicationModal)
                    # 设置关闭对象自动释放资源
                    self.view.tableWidget_doctor.setAttribute(Qt.WA_DeleteOnClose)

                    self.view.tableWidget_doctor.show()
                elif flag == '2':
                    doctor_info = REPData[3][1]
                    self.doctor_info = doctor_info
                    # self.theme_info = theme_info
                    if self.doctor_info:
                        self.clear(self.view.tableWidget_doctor.verticalLayout_1)
                        col_label_detail = ['姓名', '电话', '邮箱', '操作']
                        # 页码不会改变是因为这里创建时候没有传入当前页码值
                        # 这里只是改变重新创建当前表格值
                        self.view.tableWidget_doctor.init_ui(current_page=self.doctor_cur_page,
                                                              col_label=col_label_detail,
                                                              sampleList=self.doctor_info,
                                                              totalNum=self.doctor_totalNum,
                                                              on_clicked_selectBtn=self.doctor_on_clicked_selectBtn)

                        # 源代码
                        if self.doctor_is_fromSkip:
                            self.view.tableWidget_doctor.skipPage.setText(str(self.doctor_cur_page))
                        else:
                            self.view.tableWidget_doctor.skipPage.setText(str(self.doctor_skip_page))
                    else:
                        QMessageBox.information(self, "分页信息查询", '下一页无信息！！', QMessageBox.Yes)
                elif flag == '3':
                    # 清除表格内容
                    self.clear(self.view.tableWidget_doctor.verticalLayout_1)
                    # 清除页面控制器
                    self.view.tableWidget_doctor.control_signal.disconnect(self.doctor_page_controller)
                    self.clear(self.view.tableWidget_doctor.control_layout)
                    doctor_info = REPData[3][1]
                    self.doctor_info = doctor_info
                    self.doctor_totalNum = REPData[3][2]
                    col_label_detail = ['姓名', '电话', '邮箱', '操作']
                    self.view.tableWidget_doctor.init_ui(col_label=col_label_detail,
                                                          sampleList=doctor_info,
                                                          totalNum=self.doctor_totalNum,
                                                          on_clicked_selectBtn=self.doctor_on_clicked_selectBtn)
                    # 页码相关
                    self.doctor_page = math.ceil(self.doctor_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_doctor.setPageController(self.doctor_page)
                    self.view.tableWidget_doctor.control_signal.connect(self.doctor_page_controller)

                # 点击搜索按钮
                elif flag == '4':
                    # 清除表格内容
                    self.clear(self.view.tableWidget_doctor.verticalLayout_1)
                    # 清除页面控制器
                    self.view.tableWidget_doctor.control_signal.disconnect(self.doctor_page_controller)
                    self.clear(self.view.tableWidget_doctor.control_layout)
                    doctor_info = REPData[3][1]
                    self.doctor_info = doctor_info
                    self.doctor_totalNum = REPData[3][2]
                    col_label_detail = ['姓名', '电话', '邮箱', '操作']
                    self.view.tableWidget_doctor.init_ui(col_label=col_label_detail,
                                                          sampleList=self.doctor_info,
                                                          totalNum=self.doctor_totalNum,
                                                          on_clicked_selectBtn=self.doctor_on_clicked_selectBtn)
                    # 页码相关
                    self.doctor_page = math.ceil(self.doctor_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_doctor.setPageController(self.doctor_page)
                    self.view.tableWidget_doctor.control_signal.connect(self.doctor_page_controller)
                elif flag == '5':
                    doctor_info = REPData[3][1]
                    self.doctor_info = doctor_info
                    if self.doctor_info:
                        self.clear(self.view.tableWidget_doctor.verticalLayout_1)
                        col_label_detail = ['姓名', '电话', '邮箱', '操作']
                        # 页码不会改变是因为这里创建时候没有传入当前页码值
                        # 这里只是改变重新创建当前表格值
                        self.view.tableWidget_doctor.init_ui(current_page=self.doctor_cur_page,
                                                              col_label=col_label_detail,
                                                              sampleList=doctor_info, totalNum=self.doctor_totalNum,
                                                              on_clicked_selectBtn=self.doctor_on_clicked_selectBtn)

                        # 源代码
                        if self.doctor_is_fromSkip:
                            self.view.tableWidget_doctor.skipPage.setText(str(self.doctor_cur_page))
                        else:
                            self.view.tableWidget_doctor.skipPage.setText(str(self.doctor_skip_page))
                    else:
                        QMessageBox.information(self, "分页信息查询", '下一页无信息！！', QMessageBox.Yes)

                else:
                    pass
        except Exception as e:
            print('get_choose_doctor_infoRes', e)

    # 选中某个医生后方法
    def doctor_on_clicked_selectBtn(self, row):
        print("选中当前行：", row)
        id = self.doctor_info[row][0]
        print("当前选中用户的id为:", id)
        name = self.doctor_info[row][1]
        print("当前选中用户的姓名为:", name)

        self.addInfo['pUid'] = id
        self.view.tableWidget_doctor.hide()

        self.view.ui.pdoctorBtn.setText(name)
        self.view.ui.pdoctorBtn.setFont(QFont("Agency FB", 16))
        self.view.ui.pdoctorBtn.setStyleSheet("color: blue;")
        # self.addFormView.show()


        # self.addFormView.ui.pdoctorBtn.setText(name)
        # self.addFormView.ui.pdoctorBtn.setFont(QFont("Agency FB", 12))
        # self.addFormView.ui.pdoctorBtn.setStyleSheet("color: blue;")
        # self.addFormView.show()


    # 选择医生的搜索功能首页界面
    def search_doctor(self):
        key_word = self.view.tableWidget_doctor.comboCond.currentText()
        key_value = self.view.tableWidget_doctor.lineValue.text()
        if key_word == '姓名':
            key_word = 'name'
        elif key_word == '电话':
            key_word = 'phone'
        elif key_word == '邮箱':
            key_word = 'email'
        print("key_word:", key_word)
        print("key_value:", key_value)
        # 只有当搜索框有值时候才搜索
        if key_value:
            self.get_choose_doctor_info(flag='4', key_word=key_word, key_value=key_value)
        else:
            QMessageBox.information(self, "提示", "搜索框内没有填写内容!!", QMessageBox.Yes)

    # 选择医生的重置功能
    def research_doctor(self):
        self.view.tableWidget_doctor.comboCond.setCurrentIndex(0)
        self.view.tableWidget_doctor.lineValue.clear()
        self.get_choose_doctor_info(flag='3')

    # 选择医生信息的返回
    def doctorReturnBtnTrigger(self):
        self.view.tableWidget_doctor.hide()
        # self.addFormView.show()
        print("返回上级按键被触发！！！")

    # 医生息界面相关跳转
    def doctor_page_controller(self, signal):
        total_page = self.view.tableWidget_doctor.showTotalPage()
        is_fromSkip = False
        if "home" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                return
            self.view.tableWidget_doctor.curPage.setText("1")
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            self.view.tableWidget_doctor.curPage.setText(str(int(signal[1]) - 1))
        elif "next" == signal[0]:
            if total_page == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.view.tableWidget_doctor.curPage.setText(str(int(signal[1]) + 1))
        elif "final" == signal[0]:
            self.view.tableWidget_doctor.curPage.setText(str(total_page))
        elif "confirm" == signal[0]:
            if total_page < int(signal[1]) or int(signal[1]) < 1:
                QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                self.view.tableWidget_doctor.skipPage.setText('1')
                return
            is_fromSkip = True
            self.view.tableWidget_doctor.curPage.setText(signal[1])
        self.changeTableContent_doctor(is_fromSkip)  # 改变表格内容

    def changeTableContent_doctor(self, is_fromSkip):
        """根据当前页改变表格的内容"""
        self.doctor_is_fromSkip = is_fromSkip
        self.doctor_cur_page = int(self.view.tableWidget_doctor.curPage.text())
        self.doctor_skip_page = int(self.view.tableWidget_doctor.skipPage.text())
        self.doctor_start = (self.doctor_cur_page - 1) * self.perPageNum
        # theme_id = self.theme_detailID
        # row = self.row_detail

        key_word = self.view.tableWidget_doctor.comboCond.currentText()
        key_value = self.view.tableWidget_doctor.lineValue.text()
        if key_word == '姓名':
            key_word = 'name'
        elif key_word == '电话':
            key_word = 'phone'
        elif key_word == '邮箱':
            key_word = 'email'
        print("key_word:", key_word)
        print("key_value:", key_value)
        # 只有当搜索框有值时候才搜索
        if key_value:
            # 有搜索条件的翻页
            self.get_choose_doctor_info(flag='5', key_word=key_word, key_value=key_value)
        else:
            # 无搜索条件的翻页
            self.get_choose_doctor_info(flag='2')



    # 获取检查信息
    def onClick_ButtonToText(self):
        self.addInfo['check_num'] = self.view.ui.check_num.text()
        # 检查单号是否为空
        # TODO:后续可以增加检查检查单号格式
        result = self.check_item_pattern(self.addInfo)
        if result:
            # self.addFormView.close()
            strDate = self.view.ui.dateEdit.date().toString("yyyy-MM-dd")
            print(strDate)
            self.addInfo['measure_date'] = strDate
            self.addInfo['description'] = self.view.ui.checkInfo.toPlainText()
            self.addInfo['cUid'] = self.client.tUser[0]
            account = self.client.tUser[1]
            REQmsg = [account, self.addInfo['check_num'], self.addInfo['patient_id'], self.addInfo['description'],
                      self.addInfo['pUid'], self.addInfo['measure_date'], self.addInfo['cUid']]
            print(self.addInfo)
            self.client.addCheckInfo(REQmsg)


    # 取消添加标注类型信息方法
    def on_btnCancelAdd_clicked(self):
        self.addInfo = {}
        # 关闭弹出添加框
        # self.addFormView.close()
        # 清空添加内容表单中的东西
        self.view.ui.check_num.clear()
        self.view.ui.patientBtn.setText('选择病人')
        self.view.ui.patientBtn.setStyleSheet("color: black;")
        self.view.ui.patientBtn.setFont(QFont("Agency FB", 16))
        self.view.ui.pdoctorBtn.setText('选择开单医生')
        self.view.ui.pdoctorBtn.setStyleSheet("color: black;")
        self.view.ui.pdoctorBtn.setFont(QFont("Agency FB", 16))
        # self.view.ui.textEdit.clear()
        self.view.ui.checkInfo.clear()
        self.view.ui.dateEdit.setDate(QDateTime.currentDateTime().date())

    # 处理客户端传回的添加病人检查信息结果
    def addCheckInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.view.ui.tableWidget.clear()
                # 清空添加表单的东西
                self.view.ui.check_num.clear()
                self.view.ui.patientBtn.setText('选择病人')
                self.view.ui.patientBtn.setStyleSheet("color: black;")
                self.view.ui.patientBtn.setFont(QFont("Agency FB", 16))
                self.view.ui.pdoctorBtn.setText('选择开单医生')
                self.view.ui.pdoctorBtn.setStyleSheet("color: black;")
                self.view.ui.pdoctorBtn.setFont(QFont("Agency FB", 16))
                self.view.ui.checkInfo.clear()
                # self.view.ui.textEdit.clear()
                self.view.ui.dateEdit.setDate(QDateTime.currentDateTime().date())
                self.getPatientCheckInfo()


                # self.view.initTable(self.patientCheck_info)
                QMessageBox.information(self, "病人检查", REPData[2], QMessageBox.Yes)
            else:
                QMessageBox.information(self, "病人检查", REPData[2], QMessageBox.Yes)
                self.view.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.view.ui.tableWidget.clear()
                self.view.initTable(self.patientCheck_info)
        except Exception as e:
            print('addCheckInfo', e)


    # 删除病人检查信息功能
    # 删除病人检查信息方法
    def on_btnDel_clicked(self):

        if self.row!=-1:
            self.row = self.view.ui.tableWidget.currentRow()
            # 找到当前检查信息的脑电上传医生
            pdoctorname = self.patientCheck_info[self.row][3]
            if pdoctorname == self.client.tUser[0]:
                answer = QMessageBox.warning(
                    self.view, '确认删除！', '您将进行删除操作！',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if answer == QMessageBox.Yes:
                    if self.row == -1:
                        QMessageBox.information(self.view, ' ', '请先选中一行')
                        return
                    # 暂时只能选中一行删除
                    print('row', self.row)
                    check_id = self.patientCheck_info[self.row][0]
                    account = self.client.tUser[1]
                    REQmsg = [account, check_id, self.row]
                    self.row = -1
                    self.client.delPatientCheckInfo(REQmsg)
                else:
                    return
            else:
                QMessageBox.information(self.view, '提示', '你不是本次检查的脑电上传医生，你无权进行删除！！！')
        else:
            QMessageBox.information(self, ' ', '请先在病人诊断信息中选择一行')
            return

    # 处理客户端返回的删除标注类型信息结果
    def delPatientCheckInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                row = REPData[3][1]
                print('pop values :', self.patientCheck_info[row])
                if len(self.patientCheck_info) != 1:
                    self.patientCheck_info.pop(row)
                    self.view.initTable(self.patientCheck_info)
                else:
                    self.view.ui.tableWidget.setRowCount(0)
                    self.view.ui.tableWidget_2.clearContents()

                # 让添加按钮起作用
                # self.view.ui.addButton.setEnabled(True)
                self.view.ui.delButton.setEnabled(False)
                self.view.ui.groupBox_4.setEnabled(True)


                # 清除信息显示框内容
                self.view.ui.textEdit.clear()

                # 清空file_info表
                self.view.ui.tableWidget_2.setRowCount(0)
                self.view.ui.tableWidget_2.clearContents()
                QMessageBox.information(self, "成功", "删除成功")
                # 设置按钮状态
                self.view.ui.chooseBtn.setEnabled(False)
                self.view.ui.processButton.setEnabled(False)
                self.view.ui.delButton.setEnabled(False)
                self.view.ui.sendMsgButton.setEnabled(False)
                return
            else:
                QMessageBox.information(self, "提示", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('delPatientCheckInfo', e)

    # 响应点击病人诊断信息列表
    def on_tableWidget_itemClicked(self):
        self.row = self.view.ui.tableWidget.currentRow()
        if self.row != -1:
            self.view.ui.textEdit.setPlainText(f'当前选中第{str(self.row+1)}行!\n选中的是检查单号为{str(self.patientCheck_info[self.row][5])}\n病人是{self.patientCheck_info[self.row][self.view.field.index("pname")+4]}\n检测日期是{self.patientCheck_info[self.row][self.view.field.index("measure_date")+4]}')
            if self.patientCheck_info[self.row][3] != self.client.tUser[0]:
                self.view.ui.chooseBtn.setEnabled(False)
                self.view.ui.processButton.setEnabled(False)
                self.view.ui.delButton.setEnabled(False)
                self.view.ui.sendMsgButton.setEnabled(False)
            else:
                self.view.ui.chooseBtn.setEnabled(True)
                self.view.ui.delButton.setEnabled(True)
                # self.view.ui.sendMsgButton.setEnabled(True)
                self.view.ui.processButton.setEnabled(False)
            check_id = self.patientCheck_info[self.row][0]
            if self.change_file:
                if check_id in self.change_file.keys():
                    self.view.initTable_1(self.change_file[check_id])
                    # 有脑电文件的才可以点击这个按钮
                    self.view.ui.sendMsgButton.setEnabled(True)
                else:
                    # 该方法只能清除内容，表头还是保留的
                    # self.view.ui.tableWidget_2.clear()
                    # 没有上传脑电文件的检查单，不能点击这个按钮
                    self.view.ui.sendMsgButton.setEnabled(False)
                    self.view.ui.tableWidget_2.setRowCount(0)
                    self.view.ui.tableWidget_2.clearContents()
            else:
                self.view.ui.tableWidget_2.setRowCount(0)
                self.view.ui.tableWidget_2.clearContents()




    # 处理脑电文件
    # 选择文件
    def on_btnChoose_clicked(self):
        if self.row == -1:
            QMessageBox.information(self, ' ', '请先在病人诊断信息中选择一行')
            return

        get_filename_path, ok = QFileDialog.getOpenFileName(self,
                                                            "导入病人文件",
                                                            "C:/",
                                                            "脑电文件 (*.edf *.bdf *.txt)")

        if ok:
            self.from_filepath = get_filename_path
            # 根据文件后缀判断文件类型
            file_extension = os.path.splitext(self.from_filepath)[1].lower()
            if file_extension == '.bdf':
                self.processthread = threading.Thread(target=self.process_bdf, args=(self.from_filepath,))
                self.from_filepath = get_filename_path
            elif file_extension == '.edf':
                self.convert_edf_to_bdf()
                self.processthread = threading.Thread(target=self.process_bdf, args=(self.convert_filepath,))
                self.from_filepath = self.convert_filepath
            else:
                QMessageBox.information(self, "不支持的文件类型", "请上传有效的脑电文件格式 (.edf 或 .bdf).")
                return

            # self.from_filepath = get_filename_path
            self.view.ui.textEdit.clear()
            self.view.ui.textEdit.setPlainText(
                f'当前选中第{str(self.row + 1)}行!\n选中的病人是{self.patientCheck_info[self.row][self.view.field.index("pname") + 4]}检测日期是{self.patientCheck_info[self.row][self.view.field.index("measure_date") + 4]}\n当前选中需要转换的文件路径为{self.from_filepath}')
            self.view.ui.processButton.setEnabled(True)

    # 将EDF文件转化为BDF文件
    # def convert_edf_to_bdf(self):
    #     try:
    #         # 读取EDF文件
    #         with pyedflib.EdfReader(self.from_filepath) as edf_reader:
    #             n_channels = edf_reader.signals_in_file
    #
    #             # 获取EDF文件的信号头信息
    #             signal_headers = edf_reader.getSignalHeaders()
    #             headers = edf_reader.getHeader()
    #
    #             # 为每个通道创建新的信号头信息，用于BDF文件
    #             for i in range(n_channels):
    #                 signal_headers[i]['digital_min'] = -8388608  # BDF 24位数字最小值
    #                 signal_headers[i]['digital_max'] = 8388607  # BDF 24位数字最大值
    #                 signal_headers[i]['physical_min'] = edf_reader.getPhysicalMinimum(i)  # 保留物理范围
    #                 signal_headers[i]['physical_max'] = edf_reader.getPhysicalMaximum(i)  # 保留物理范围
    #                 signal_headers[i]['prefilter'] = edf_reader.getPrefilter(i)  # 获取预处理信息
    #
    #             # 生成转换后的 BDF 文件名
    #             directory, filename = os.path.split(self.from_filepath)
    #             filename_without_extension = os.path.splitext(filename)[0]
    #             new_filename = f"{filename_without_extension}.bdf"
    #             self.convert_filepath = os.path.join(directory, new_filename)
    #
    #             # 创建BDF头文件
    #             bdf_header = pyedflib.highlevel.make_header(
    #                 patientname=headers['patientname'],
    #                 # recording=headers['recording'],
    #                 startdate=headers['startdate']
    #             )
    #
    #             # 写入BDF文件
    #             with pyedflib.EdfWriter(self.convert_filepath, file_type=pyedflib.FILETYPE_BDF,
    #                                     n_channels=n_channels) as bdf_writer:
    #                 # 设置信号头文件
    #                 bdf_writer.setSignalHeaders(signal_headers)
    #                 bdf_writer.setHeader(bdf_header)
    #
    #                 # 读取每个通道的数据并将其组织成列表
    #                 all_channel_data = []
    #                 for i in range(n_channels):
    #                     signal_data = edf_reader.readSignal(i)
    #                     all_channel_data.append(signal_data)  # 将每个通道的数据加入到列表中
    #
    #                 # 检查数据是否与通道数匹配
    #                 if len(all_channel_data) != n_channels:
    #                     raise pyedflib.WrongInputSize(
    #                         f"Number of channels ({n_channels}) unequal to length of data ({len(all_channel_data)})")
    #
    #                 # 写入所有通道的数据
    #                 bdf_writer.writeSamples(all_channel_data)
    #
    #         print(f"EDF文件 {self.from_filepath} 已成功转换为BDF文件 {self.convert_filepath}")
    #
    #
    #     except Exception as e:
    #         print('Error during EDF to BDF conversion:', e)

    def convert_edf_to_bdf(self):
        try:
            # 使用MNE读取EDF文件并提取注释
            raw = mne.io.read_raw_edf(self.from_filepath, preload=True)
            annotations = raw.annotations  # 提取注释（事件信息）
            print(f"Annotations: {annotations}")  # 打印注释信息

            # 通道筛选与重命名
            # 选择所有以EEG开头的通道
            include_channel = mne.pick_channels_regexp(raw.info['ch_names'], '^EEG')
            # 获取筛选后的通道名称
            channels = mne.pick_info(raw.info, include_channel)['ch_names']

            # 通道名映射，去除前缀（‘EEG F3-REF' -> 'F3-REF'）
            dict_ch = {}
            re_channels = []
            for ch in channels:
                temp = ch.split(' ')[-1]  # 去除前缀，只保留 'F3-REF' 等通道名
                re_channels.append(temp)
                dict_ch[ch] = temp

            # 重命名通道
            raw.rename_channels(dict_ch)
            raw.pick(picks=re_channels)  # 仅保留变换后的通道

            # 使用pyedflib读取EDF文件
            with pyedflib.EdfReader(self.from_filepath) as edf_reader:
                n_channels = edf_reader.signals_in_file

                # 获取EDF文件的信号头信息
                signal_headers = edf_reader.getSignalHeaders()
                headers = edf_reader.getHeader()

                # 过滤出以重新命名后的通道
                index_channels = mne.pick_channels(raw.info['ch_names'], include=re_channels)

                # 仅处理EEG通道的信号头信息，用于BDF文件
                filtered_signal_headers = []
                for i in index_channels:
                    filtered_signal_headers.append({
                        'label': signal_headers[i]['label'],
                        'digital_min': -8388608,  # BDF 24位数字最小值
                        'digital_max': 8388607,  # BDF 24位数字最大值
                        'physical_min': edf_reader.getPhysicalMinimum(i),  # 保留物理范围
                        'physical_max': edf_reader.getPhysicalMaximum(i),  # 保留物理范围
                        'prefilter': edf_reader.getPrefilter(i),  # 获取预处理信息
                        'sample_frequency': edf_reader.getSampleFrequency(i)
                    })

                # 生成转换后的 BDF 文件名
                directory, filename = os.path.split(self.from_filepath)
                filename_without_extension = os.path.splitext(filename)[0]
                new_filename = f"{filename_without_extension}.bdf"
                self.convert_filepath = os.path.join(directory, new_filename)

                # 创建BDF头文件
                bdf_header = pyedflib.highlevel.make_header(
                    patientname=headers['patientname'],
                    startdate=headers['startdate']
                )

                # 写入BDF+文件
                with pyedflib.EdfWriter(self.convert_filepath, file_type=pyedflib.FILETYPE_BDFPLUS,
                                        n_channels=len(filtered_signal_headers)) as bdf_writer:
                    # 设置信号头文件
                    bdf_writer.setSignalHeaders(filtered_signal_headers)
                    bdf_writer.setHeader(bdf_header)

                    # 读取EEG通道的数据并将其组织成列表
                    all_channel_data = []
                    for i in index_channels:
                        signal_data = edf_reader.readSignal(i)
                        all_channel_data.append(signal_data)  # 将每个通道的数据加入到列表中

                    # 检查数据是否与通道数匹配
                    if len(all_channel_data) != len(filtered_signal_headers):
                        raise pyedflib.WrongInputSize(
                            f"Number of channels ({len(filtered_signal_headers)}) unequal to length of data ({len(all_channel_data)})")

                    # 写入所有EEG通道的数据
                    bdf_writer.writeSamples(all_channel_data)

                    # 将注释信息（事件信息）写入BDF文件，确保空描述也被写入
                    for annotation in annotations:
                        onset = annotation['onset']  # 注释的开始时间
                        duration = annotation['duration']  # 注释的持续时间
                        description = annotation['description']  # 注释的描述

                        # 如果description为空或全是空白字符，使用占位符
                        if not description.strip():
                            description = "empty"  # 使用占位符字符串

                        # 写入注释
                        bdf_writer.writeAnnotation(onset, duration, description)

            print(f"EDF文件 {self.from_filepath} 已成功转换为BDF文件 {self.convert_filepath}")

        except Exception as e:
            print('Error during EDF to BDF conversion:', e)

    # 处理脑电文件
    def on_btnProcess_clicked(self):
        # 判断

        try:
            raw = mne.io.read_raw_bdf(self.from_filepath)
            self.duration = raw.n_times/raw.info['sfreq']
            # 存储源文件采样点数
        except Exception as e:
            # self.format_failedInport.emit()
            print('读取未成功', e)
            return

        account = self.client.tUser[1]
        user_id = self.client.tUser[0]
        check_id = self.patientCheck_info[self.row][0]
        mac = self.cAppUtil.getMacAddress()

        # self.config_id = self.client.tUser[12]
        filemsg = ['', check_id, '', mac, self.config_id]
        freq = raw.info['sfreq']
        REQmsg = [account,user_id, filemsg, freq]
        # 这个线程就没有开始过
        self.client.checkMakeFileName(REQmsg)

    # 检查脑电文件配置返回
    def checkMakeFileNameRes(self, REPData):
        try:
            if REPData[0] == '1':
                userConfig = REPData[3][0]
                # 返回的命名放入此变量
                self.filename = REPData[3][1]
                self.make_filepath(self.filename)
                print('userConfig', userConfig)
                print('filename:', self.filename)
                # 在这里保存要上传的脑电文件的信息
                self.check_id, self.file_id = self.returnMsg(self.filename)
                # 创建上传的文件记录
                uploading_name = self.filename + '.txt'
                uploading_path = os.path.join(self.dir_path, uploading_name)
                # TODO：什么时候写这个文件，这里不适合写
                k = ['check_id', 'file_id', 'mac', 'config_id', 'userConfig', 'from_filepath', 'duration', 'uid']
                fileMsg = self.packageMsg('write', userConfig=userConfig, from_filepath=self.from_filepath, duration=self.duration, uid=self.client.tUser[0])[1][1:]
                writeMsg = dict(zip(k, fileMsg))
                with open(uploading_path, 'wb') as f:
                    pickle.dump(writeMsg, f)



                # 进度条相关，这里先注释修改一下
                self.dlgProgress = QProgressDialog('正在处理并上传', '', 0, 0, self)
                self.dlgProgress.setFixedSize(300, 100)
                self.dlgProgress.setCancelButtonText(None)
                self.dlgProgress.setAttribute(Qt.WA_DeleteOnClose, True)
                self.dlgProgress.setWindowTitle("脑电文件上传进度")
                self.dlgProgress.setWindowModality(Qt.ApplicationModal)  # 进度对话框
                self.dlgProgress.setRange(0, 100)
                self.dlgProgress.show()
                # self.value = 5
                self.progress_value = 1
                self.dlgProgress.setValue(self.progress_value)
                # 添加一个定时器，实时计算当前进度条位置


                # 开启线程
                self.thread_start(flag='1', userConfig=userConfig)

                # 使用QTimer定期检查全局变量并更新进度条
                self.updateTimer = QTimer(self)
                self.updateTimer.start(1000)
                self.updateTimer.timeout.connect(self.update_progress_bar)

                # self.progressBar = ProgressBarWidget()
                # self.progressBar.progress_bar.setValue(1)
                # # 手动处理事件循环，确保进度条刷新
                # QApplication.processEvents()

                # self.process_edf(userConfig, self.filename)


                # (userConfig, self.filename)


            elif REPData[0] == '2':
                QMessageBox.information(self, "配置检查", REPData[2], QMessageBox.Yes)
            else:
                QMessageBox.information(self, "配置检查", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('checkMakeFileNameRes', e)

    # 更新进度条位置
    def update_progress_bar(self):
        self.dlgProgress.setValue(self.progress_value)

    # 创建目标文件路径
    def make_filepath(self, filename):
        # 处理过后脑电文件存放路径
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
        processFilename = filename + str('.bdf')
        self.file_path = os.path.join(self.dir_path, processFilename)

    # # 处理.bdf文件
    # def process_bdf(self, userConfig_info, filename):
    #     try:
    #         # 读取BDF文件
    #         with open(self.from_filepath, 'rb') as bdf_file:
    #             bdf_content = bdf_file.read()
    #             # 打开目标文件路径进行二进制写入
    #         with open(self.file_path, 'wb') as output_file:
    #             output_file.write(bdf_content)
    #     except Exception as e:
    #         print('Error processing BDF file:', e)
    #         self.upload_failed.emit()  # 发出上传失败信号
    #         return
    #
    #     # 处理完成后发出上传信号
    #     self.uploadFileSig.emit()

    # TODO:加入预处理后上传BDF文件，待实验
    def process_bdf(self, userConfig_info, filename):
        # sampling_rate = userConfig_info[0]
        # notch = userConfig_info[1]
        # low_pass = userConfig_info[2]
        # high_pass = userConfig_info[3]

        try:
            raw = mne.io.read_raw_bdf(self.from_filepath)
            with pyedflib.EdfReader(self.from_filepath) as f:
                n_channels = f.signals_in_file  # 获取通道数
                physical_mins = []
                physical_maxs = []
                prefilter_info = []  # 用于存储每个通道的预处理信息

                # 遍历每个通道，获取 physical_min 和 physical_max
                for i in range(n_channels):
                    physical_min = f.getPhysicalMinimum(i)
                    physical_max = f.getPhysicalMaximum(i)
                    prefilter = f.getPrefilter(i)  # 获取每个通道的预处理信息（如 HP, LP, N）
                    physical_mins.append(physical_min)
                    physical_maxs.append(physical_max)
                    prefilter_info.append(prefilter)
                    print(f"Channel {i}: Physical Min = {physical_min}, Physical Max = {physical_max}")
                # TODO: 在这里要从列表里把最大值和最小值拎出来
                Physical_Min = min(physical_mins)
                Physical_Max = max(physical_maxs)
        except Exception as e:
            print('raw read error', e)
            return
        try:
            freq = raw.info['sfreq']
            duration = int(raw.n_times // freq)
            meas_date = raw.info['meas_date']
            if isinstance(meas_date, tuple):
                meas_date = datetime.datetime.fromtimestamp(meas_date)

            # 选择包含 'EEG' 前缀的通道
            include_channel = mne.pick_channels_regexp(raw.info['ch_names'], '^sfgre')
            if not include_channel:  # 如果没有 'EEG' 前缀的通道，则不进行重映射
                channels = raw.ch_names
            else:
                # 通道名称
                channels = mne.pick_info(raw.info, include_channel)['ch_names']
                # 通道名映射，去除前缀（‘EEG F3-REF' -> 'F3-REF')
                dict_ch = {ch: ch.split(' ')[-1] for ch in channels}
                raw.rename_channels(dict_ch)
                channels = [dict_ch[ch] for ch in channels]

            raw.pick_channels(channels)
            index_channels = mne.pick_channels(raw.info['ch_names'], include=channels)

            stack_size = 3600
            turn = math.ceil(duration / stack_size)
            #
            # highpass = raw.info['highpass'] if raw.info['highpass'] is not None else 0.0
            # lowpass = raw.info['lowpass'] if raw.info['lowpass'] is not None else 0.0
            # prefilter = f"HP:{highpass:.1f}Hz LP:{lowpass:.1f}Hz N:0.0"
            # print('prefilter:',prefilter)

            # prefilter = f"HP:{raw.info['highpass']}Hz LP:{raw.info['lowpass']}Hz"
            # prefilter = ('HP:{}Hz LP:{}Hz N:NoneHz'.format(high_pass, low_pass))

            signal_headers = pyedflib.highlevel.make_signal_headers(channels,
                                                                    physical_min=Physical_Min,
                                                                    physical_max=Physical_Max,
                                                                    digital_min=-8388608,  # 24位格式的数字最小值
                                                                    digital_max=8388607,  # 24位格式的数字最大值
                                                                    # physical_max=6368.439, physical_min=-6337.78
                                                                    # sample_rate=sampling_rate,
                                                                    sample_rate=freq,
                                                                    # sample_frequency=sampling_rate,
                                                                    prefiler=prefilter_info[0]
                                                                    )
            header = pyedflib.highlevel.make_header(startdate=meas_date)
            with pyedflib.EdfWriter(self.file_path, file_type=pyedflib.FILETYPE_BDF, n_channels=len(channels)) as f:
                f.setSignalHeaders(signal_headers)
                f.setHeader(header)
                for i in range(turn):
                    raw_copy = raw.copy()
                    start = i * stack_size
                    if i == turn - 1:
                        t_raw = raw_copy.crop(tmin=start, include_tmax=True)
                    else:
                        end = start + stack_size
                        t_raw = raw_copy.crop(tmin=start, tmax=end, include_tmax=True)
                    t_raw.load_data()
                    # t_raw.filter(l_freq=high_pass, h_freq=low_pass)  # 带通滤波
                    # t_raw.notch_filter(freqs=notch)
                    # t_raw.resample(sampling_rate, npad='auto')
                    t_signals, t_times = t_raw[index_channels, :]
                    del t_raw

                    t_signals = t_signals * (pow(10, 6))
                    f.writeSamples(t_signals)
                    del t_signals

                    temp = math.ceil(20 / turn)
                    if self.progress_value + temp < 20:
                        self.progress_value += temp
                    else:
                        self.progress_value = 20
                    QApplication.processEvents()

                # with open(self.file_path, 'r+b') as f:
                #     f.seek(0xC0)  # 移动到0x000000C0位置
                #     f.write(b'BDF    ')  # 写入"BDF"，并用空格填充剩余的部分

                self.uploadFileSig.emit()
        except Exception as e:
            print('process_bdf', e)
            return
        return

    # 脑电文件上传
    def on_btnUpload_clicked(self):

        # 关闭处理脑电文件的线程
        if self.processthread.is_alive():
            self.stop_thread(self.processthread)

        self.block_num = math.ceil((os.stat(self.file_path).st_size) / self.block_size)
        self.view.ui.textEdit.setPlainText(f'当前上传文件名:{self.file_path}，当前check_id:{self.check_id}, 当前file_id:{self.file_id}，当前文件一共：{self.block_num}块')
        REQmsg = self.packageMsg(state='start')
        self.client.writeEEG(REQmsg)
        # 9.3加这一行
        self.view.ui.processButton.setEnabled(False)
        # print(REQmsg)

# 脑电协议功能函数
    def writeEEGRes(self,  REPData):
        try:
            if REPData[0] == '1':
                repFilemsg = REPData[3]
                state = repFilemsg[0]
                # 脑电文件传输协议6.1情况
                if state == 'waiting':
                    block_id = repFilemsg[1]
                    # 请求文件块数超出文件总块数情况
                    if block_id > self.block_num:
                        REQmsg = self.packageMsg('uploaded', block_id)
                        self.client.writeEEG(REQmsg)
                    else:

                        self.view.ui.textEdit.setPlainText(f'当前上传脑电文件，上传到第{block_id}块，一共有{self.block_num}块')

                        # 另外一种更新进度条的方式
                        temp = int((block_id / self.block_num) * 80)
                        if temp + 20 < 100:
                            self.progress_value = temp + 20
                        else:
                            self.progress_value = 99
                        # 手动处理事件循环，确保进度条刷新
                        QApplication.processEvents()


                        EEGdata = self.readEEG(self.file_path, self.block_size, block_id)
                        REQmsg = self.packageMsg('uploading', block_id, EEGdata)
                        self.client.writeEEG(REQmsg)
                # 脑电文件传输协议6.2情况
                elif state == 'wrongSite' or state == 'unknownError' or state == 'cleaned' or state == 'wrongServer':
                    # 清空上传错误的脑电文件及其对应记录
                    self.removeFiles(self.dir_path, filename=self.filename)
                    # 上传失败但是删除记录提示
                    self.upload_failed.emit()

                # 脑电文件传输协议6.3情况
                elif state == 'wrongBlock':
                    block_id = repFilemsg[1]
                    EEGdata = self.readEEG(self.file_path, self.block_size, block_id)
                    REQmsg = self.packageMsg('uploading', block_id, EEGdata)
                    self.client.writeEEG(REQmsg)

                # 脑电文件传输协议6.4情况
                elif state == 'uploaded':
                    self.removeFiles(self.dir_path, filename=self.filename)
                    # TODO:直接本地修改状态，然后刷新表格
                    temp = list(self.patientCheck_info[self.row])
                    temp[10] = 'uploading'
                    self.patientCheck_info[self.row] = tuple(temp)
                    self.view.initTable(self.patientCheck_info)


                    self.progress_value = 100
                    # 手动处理事件循环，确保进度条刷新
                    QApplication.processEvents()

                    # 结束进度条，并提示
                    self.upload_finished.emit()
                    # 更新File_info表展示
                    self.getFileInfo()

                # 脑电文件传输协议6.5情况
                # 建议删除协议这一部分
                # elif state == 'recover':
                #     self.removeFiles(self.dir_path, filename=self.filename)
                #     REQmsg = self.packageMsg('continue')
                #     self.client.writeEEG(REQmsg)

                else:
                    print(f'状态{state}暂时无法处理服务器传回的这个状态！！！')
            else:
                if len(REPData) > 2:
                    QMessageBox.information(self, "脑电文件上传", REPData[2], QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "脑电文件上传", REPData[1], QMessageBox.Yes)
        except Exception as e:
            print('writeEEGRes', e)

    # 打包消息格式[account, [脑电文件消息]]
    def packageMsg(self, state='', block_id=None, data='', mac='', userConfig='', from_filepath='', duration='', uid=''):
        REQmsg = []
        account = self.client.tUser[1]
        config_id = self.config_id
        # TODO：动态获取config_id,注释该行
        if mac != '':
            mac = mac
        else:
            mac = self.cAppUtil.getMacAddress()
        if state == 'write':
            filemsg = [state, self.check_id, self.file_id, mac, config_id, userConfig, from_filepath, duration, uid]
        elif state == 'start':
            filemsg = [state, self.check_id, self.file_id, mac, config_id]
        elif state == 'uploading':
            filemsg = [state, self.check_id, self.file_id, mac, block_id, data]
        elif state == 'uploaded':
            filemsg = [state, self.check_id, self.file_id, mac, block_id]
        elif state == 'clean':
            filemsg = [state, self.check_id, self.file_id, mac]
        elif state == 'continue':
            filemsg = [state, self.check_id, self.file_id, mac]
        else:
            pass
        REQmsg = [account, filemsg]
        return REQmsg

    # 读取某文件目录固定块的脑电文件数据
    def readEEG(self, file_path, block_size, block_id):
        try:
            with open(file_path, 'rb') as f:
                received_size = (block_id - 1) * block_size
                f.seek(received_size)
                data = f.read(block_size)
                if not data:
                    return
                else:
                    print(data, "\n")
        except Exception as e:
            print('readEEG', e)
        return data

    # 清空指定路径，指定文件名开头文件
    def removeFiles(self, filepath, filename = '', fullname = ''):
        # 获取文件夹下所有文件
        fileslist = os.listdir(filepath)
        # 删除所有文件
        if filename == '' and fullname == '':
            for file in fileslist:
                file_path = os.path.join(filepath, file)  # 获取文件的完整路径
                os.remove(file_path)  # 删除文件
        # 删除某一文件名文件
        elif filename == '' and fullname != '':
            for file in fileslist:
                if file == fullname:
                    file_path = os.path.join(filepath, file)  # 获取文件的完整路径
                    os.remove(file_path)
        # 删除指定文件名开头文件
        else:
            # 遍历文件夹中的文件
            for file in fileslist:
                if file.startswith(filename):  # 判断文件名是否以指定的文件名开头
                    file_path = os.path.join(filepath, file)  # 获取文件的完整路径
                    os.remove(file_path)  # 删除文件

    # 查找某一路径指定文件后缀文件名
    def findFile(self, filepath, suffix):
        # 获取文件夹下所有文件
        fileslist = os.listdir(filepath)
        fileName = []
        # 遍历文件夹中的文件
        for file in fileslist:
            if file.endswith(suffix):  # 判断文件名是否以指定的文件名开头
                fileName.append(file.split('.')[0])
        return fileName  # 返回不带后缀的文件名

    # 查找同名文件
    def findSameFile(self, filepath, fileName):
        # 获取文件夹下所有文件
        fileslist = os.listdir(filepath)
        # 遍历文件夹中的文件
        for file in fileslist:
            if file == fileName:
                return True
        return False

    # 传入某一路径返回文件相关信息
    def returnMsg(self, filename):
        check_id = int(filename.split('_')[0])
        file_id = int(filename.split('_')[1])
        return check_id, file_id

    # 检查是否有未上传完成的文件
    def checkDirNull(self):
        fileName = self.findFile(self.dir_path, '.txt')
        if fileName:
            # 遍历所有.txt文件
            reply = QMessageBox.information(self, "提示", "系统正在处理未完成的上传任务，完成后才能启动新的上传任务!!!!",
                                            QMessageBox.Yes)
            if reply == 16384:
                # 假定未上传完毕的脑电文件和上传记录各一个，后面如果有多个在此加个for循环，然后微调一下
                f = fileName[0]
                try:
                    with open(os.path.join(self.dir_path, f + '.txt'), 'rb') as file:
                        data = pickle.load(file)
                    self.check_id = data['check_id']
                    self.file_id = data['file_id']
                    mac = str(data['mac'])
                    self.config_id = data['config_id']
                    userConfig = data['userConfig']
                    self.from_filepath = data['from_filepath']
                    duration = data['duration']
                except Exception as e:
                    # .txt文件不完整情况
                    self.removeFiles(self.dir_path, filename=f)
                    QMessageBox.information(self, "提示", "上传记录文件有损坏!!!!，需要进行检查并删除相关记录！！",
                                            QMessageBox.Yes)
                    #TODO:这里上传记录文件有毛病还要分两种情况：1.bdf文件没毛病 2.bdf文件有毛病。协议只考虑了bdf文件没毛病情况，上传记录如果有毛病，里面保存了很多字段，还要判断到底哪里出问题，所有还不如笼统的直接，.txt出毛病就删除所有相关记录方便。

                    REQmsg = self.packageMsg('clean')
                    self.client.writeEEG(REQmsg)
                else:
                    # .txt完整情况,判断是否存在.bdf文件
                    self.filename = f
                    if self.findSameFile(self.dir_path, f + str('.bdf')):
                        # 存在.bdf文件，判断是否损坏
                        self.file_path = os.path.join(self.dir_path, self.filename + str('.bdf'))
                        ret = self.testEEGFile(self.file_path, duration=duration)
                        if ret[0] == '1':
                            #  .bdf文件没有被损害情况
                            self.block_num = math.ceil(
                                (os.stat(self.file_path).st_size) / self.block_size)


                            # 开启进度条
                            self.dlgProgress = QProgressDialog('正在处理并上传', '', 0, 0, self)
                            self.dlgProgress.setFixedSize(300, 100)
                            self.dlgProgress.setCancelButtonText(None)
                            # self.dlgProgress.canceled.connect(self.do_progress_canceled)
                            self.dlgProgress.setAttribute(Qt.WA_DeleteOnClose, True)
                            self.dlgProgress.setWindowTitle("脑电文件上传进度")
                            self.dlgProgress.setWindowModality(Qt.ApplicationModal)  # 进度对话框
                            self.dlgProgress.setRange(0, 100)
                            self.dlgProgress.show()


                            # 设置进度条起始值
                            self.progress_value = 20
                            # 手动处理事件循环，确保进度条刷新
                            QApplication.processEvents()

                            # 设置起始进度条的值
                            REQmsg = self.packageMsg('continue', mac=mac)
                            self.dlgProgress.setValue(self.progress_value)

                            # 还需要弄一个定时器不断访问当前进度并更新进度条值
                            # 使用QTimer定期检查全局变量并更新进度条
                            self.updateTimer = QTimer(self)
                            self.updateTimer.start(1000)
                            self.updateTimer.timeout.connect(self.update_progress_bar)

                            # 发送继续上传信息重新开始上传
                            self.client.writeEEG(REQmsg)
                            # self.continueUpload(REQmsg)

                        else:
                            # .bdf文件被损害情况
                            QMessageBox.information(self,'.bdf文件损坏','预处理过程有问题，.bdf文件损坏', QMessageBox.Yes)
                            self.removeFiles(self.dir_path, fullname=f + str('.bdf'))
                            # 开启进度条
                            self.dlgProgress = QProgressDialog('正在重新处理并上传', '', 0, 0, self)
                            # self.dlgProgress.resize(400, 30)
                            self.dlgProgress.setFixedSize(300, 100)
                            self.dlgProgress.setCancelButtonText(None)
                            # self.dlgProgress.canceled.connect(self.do_progress_canceled)
                            self.dlgProgress.setAttribute(Qt.WA_DeleteOnClose, True)
                            self.dlgProgress.setWindowTitle("脑电文件上传进度")
                            self.dlgProgress.setWindowModality(Qt.ApplicationModal)  # 进度对话框
                            self.dlgProgress.setRange(0, 100)
                            self.progress_value = 1
                            self.dlgProgress.setValue(self.progress_value)
                            self.dlgProgress.show()

                            self.thread_start(flag='1', userConfig=userConfig)
                            # 使用QTimer定期检查全局变量并更新进度条
                            self.updateTimer = QTimer(self)
                            self.updateTimer.start(1000)
                            self.updateTimer.timeout.connect(self.update_progress_bar)

                    else:
                        # 不存在.bdf文件
                        QMessageBox.information(self, '.bdf文件不存在', '预处理过程有问题，.bdf文件不存在！！！', QMessageBox.Yes)
                        self.file_path = os.path.join(self.dir_path, self.filename + str('.bdf'))

                        # 开启进度条
                        self.dlgProgress = QProgressDialog('正在重新处理并上传', '', 0, 0, self)
                        # self.dlgProgress.resize(400, 30)
                        self.dlgProgress.setFixedSize(300, 100)
                        self.dlgProgress.setCancelButtonText(None)
                        # self.dlgProgress.canceled.connect(self.do_progress_canceled)
                        self.dlgProgress.setAttribute(Qt.WA_DeleteOnClose, True)
                        self.dlgProgress.setWindowTitle("脑电文件上传进度")
                        self.dlgProgress.setWindowModality(Qt.ApplicationModal)  # 进度对话框
                        self.dlgProgress.setRange(0, 100)
                        self.progress_value = 1
                        self.dlgProgress.setValue(self.progress_value)
                        self.dlgProgress.show()
                        self.thread_start(flag='1', userConfig=userConfig)

                        # 使用QTimer定期检查全局变量并更新进度条
                        self.updateTimer = QTimer(self)
                        self.updateTimer.start(1000)
                        self.updateTimer.timeout.connect(self.update_progress_bar)

            else:
                # 取消上传的操作
                pass
        else:
            fileBdf = self.findFile(self.dir_path, '.bdf')
            # 不存在。txt文件，但是存在.bdf文件
            if fileBdf:
                QMessageBox.information(self, "提示", "由于文件夹下不存在.txt的上传记录，所以取消上传，并删除本地记录!!!!",
                                    QMessageBox.Yes)
                # 不存在.txt文件
                self.removeFiles(self.dir_path)

    # 开始对应线程
    def thread_start(self, flag='', userConfig=[], REQmsg=[]):
        if flag == '1':
            # 处理后上传
            # self.thread1 = threading.Thread(target=self.timeCount, args=(self.from_filepath,))
            # self.thread1.start()
            # print(self.filename)
            try:
                self.processthread = threading.Thread(target=self.process_bdf, args=(userConfig, self.filename))
                self.processthread.start()
            except Exception as e:
                print(f"Error starting thread:{e}")
        # else:
        #     # 重新上传
        #     # self.thread1 = threading.Thread(target=self.timeCount, args=(self.file_path,))
        #     # self.thread1.start()
        #     self.thread = threading.Thread(target=self.continueUpload, args=(REQmsg,))
        #     self.thread.start()


    # 判断.bdf文件是否损坏
    # 参数testfile为含完整路径的文件名
    def testEEGFile(self, testfile, duration):
        try:
            local_raw = mne.io.read_raw_bdf(testfile)
        except Exception as err:
            ret = ['0', '打开EEG文件无效', testfile]
            return ret
        try:
            local_channels = local_raw.info['ch_names']
            local_index_channels = mne.pick_channels(local_channels, include=[])
            local_sampling_rate = local_raw.info['sfreq']
            local_n_times = local_raw.n_times
            # 这里修改原版不是利用整除
            local_duration = local_n_times / local_sampling_rate
            meas_date = local_raw.info['meas_date']
            if isinstance(meas_date, tuple):
                meas_date = datetime.datetime.fromtimestamp(meas_date[0])
                local_start_time = meas_date.strftime('%H:%M:%S')
                local_end_time = meas_date + datetime.timedelta(seconds=local_duration)
                local_end_time = local_end_time.strftime('%H:%M:%S')
        except Exception as err:
            ret = ['0', '读文件头部信息异常', testfile]
            return ret
        if duration != local_duration:
            ret = ['0', '文件数据不完整']
            return ret
        try:
            raw_copy = local_raw.copy()
            raw_copy.crop(tmin=0, include_tmax=True)
            raw_copy.load_data()
            data, times = raw_copy[local_channels, :]
            print('data.shape', data.shape)
            print('times', times)
            ret = ['1', f'文件测试成功']
            return ret
        except Exception as e:
            ret = ['0', f'读数据块raw_copy不成功:{e}.']
            return ret

    # 脑电文件续传
    def continueUpload(self, REQmsg):
        try:
            self.client.writeEEG(REQmsg)
        except Exception as e:
            print('continueUpload', e)

    # 发送当前check_id数据上传完毕功能
    def on_btnSendMsg_clicked(self):
        if self.row == -1:
            QMessageBox.information(self, ' ', '请先在病人诊断信息中选择一行')
            return
        reply = QMessageBox.information(self, "检查id病人脑电上传状态", f"当前检查单号为：{str(self.patientCheck_info[self.row][5])}病人{self.patientCheck_info[self.row][self.view.field.index('pname') + 4]}脑电文件是否上传完毕？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == 16384:
            # TODO:更新脑电上传的医生，就是更新成当前用户id吗，万一一个check_id脑电文件有多个医生传
            uid = self.client.tUser[0]
            account = self.client.tUser[1]
            check_id = self.patientCheck_info[self.row][0]
            state = 'uploaded'
            REQmsg = [account, 'Send',[check_id, state, uid]]
            self.client.updateCheckInfo(REQmsg)

    # 更新病人检查信息返回
    def updateCheckInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                msg =f"当前检查单号为：{str(self.patientCheck_info[self.row][5])}\n病人{self.patientCheck_info[self.row][self.view.field.index('pname') + 4]}\n脑电文件已经上传完毕！！！"

                # 设置添加按钮起作用
                # self.view.ui.addButton.setEnabled(True)
                self.view.ui.groupBox_4.setEnabled(True)
                self.view.ui.delButton.setEnabled(False)

                self.view.ui.chooseBtn.setEnabled(False)
                self.view.ui.processButton.setEnabled(False)
                # self.view.ui.delButton.setEnabled(False)
                self.view.ui.sendMsgButton.setEnabled(False)

                # 直接从数据库获取然后更新，毕竟可能会出现一种大部分信息都添加的情况
                self.getPatientCheckInfo()
            else:
                QMessageBox.information(self, "病人检查", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('updateCheckInfoRes', e)


    # 转化完成
    def upload_finishedCall(self):
        # 修改传输完毕后的进度条
        # self.progressBar.setValue(100)
        # 停止定时器的计时间
        if hasattr(self, 'updateTimer'):
            self.updateTimer.stop()
        # self.update_timer.stop()
        if hasattr(self, 'dlgProgress'):
            self.dlgProgress.close()
        self.progress_value = 0
        QMessageBox.information(self, '上传完成！ ', '脑电文件上传完成,并且已经删除本地已经处理过后的文件！')
        self.view.ui.textEdit.clear()
        # if self.thread1.is_alive():
        #     self.stop_thread(self.thread1)

    # 服务器端发生异常
    def upload_failedCall(self):
        # if self.self.processthread.is_alive():
        #     self.stop_thread(self.processthread)
        # self.dlgProgress.close()
        # QMessageBox.information(self, '上传失败！ ', '服务端发生异常，紧急关闭所有线程！')
        if hasattr(self, 'updateTimer'):
            self.updateTimer.stop()
        # self.update_timer.stop()
        if hasattr(self, 'dlgProgress'):
            self.dlgProgress.close()
        self.progress_value = 0
        # QMessageBox.information(self, '上传完成！ ', '脑电文件上传完成,并且已经删除本地已经处理过后的文件！')
        self.view.ui.textEdit.clear()
        QMessageBox.information(self, "脑电文件上传", "脑电文件上传出错，已删除上传记录和处理过后的脑电文件！！！", QMessageBox.Yes)

    # 停止线程
    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)

    def _async_raise(self, tid, exctype):
        try:
            tid = ctypes.c_long(tid)
            if not inspect.isclass(exctype):
                exctype = type(exctype)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                tid, ctypes.py_object(exctype))
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")
        except Exception as err:
            print(err)


    # 转换file_info格式(方便点击切换右下角显示)
    def changeFileInfo(self,file_info):
        changeFileInfo = {}
        for i in file_info:
            key = i[0]
            changeFileInfo[key] = []
        for i in file_info:
            key = i[0]
            file_id = i[1]
            file_name = str(file_id).rjust(3, '0') + '.bdf'
            changeFileInfo[key].append((file_name, i[2]))
        return changeFileInfo

    # 检查编辑/增加 数据格式
    def check_item_pattern(self, data):
        if data['check_num'] == '':
            QMessageBox.information(self.view, '提示！', '请输入检查单号：检查单号不能为空！')
            return False
        elif not ('patient_id' in data):
            QMessageBox.information(self.view, '提示！', '未选择病人信息,请重新选择!!')
            return False
        elif not ('pUid' in data):
            QMessageBox.information(self.view, '提示！', '未选择开单医生信息,请重新选择!!!')
            return False
        else:
            return True

    def exit(self):
        self.client.getPatientCheckInfoResSig.disconnect()
        self.client.delPatientCheckInfoResSig.disconnect()
        self.client.addCheckInfoResSig.disconnect()
        self.client.checkMakeFileNameResSig.disconnect()
        self.client.writeEEGResSig.disconnect()
        self.client.updateCheckInfoResSig.disconnect()
        self.client.getFileInfoResSig.disconnect()
        self.client.getChoosePatientInfoResSig.disconnect()
        self.client.getChooseDoctorInfoResSig.disconnect()
