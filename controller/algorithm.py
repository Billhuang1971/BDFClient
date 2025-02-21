import hashlib
import json
import math
import pickle
import threading
from asyncio import sleep
from functools import partial

# from pyqt5_plugins.examplebuttonplugin import QtGui

from view.algorithm import algorithmView, ParameterView, FileUploadView, Parameter_view, TableWidget, \
    train_parameter_view

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

import numpy as np
import sys, re, os
import shutil

from view.progressBarView import ProgressBarView


class algorithmController(QWidget):
    # is_reload_controller = pyqtSignal(str)
    upload_finished = pyqtSignal(list)
    update_process = pyqtSignal(int)

    def __init__(self, client, cAppUtil):
        try:
            super().__init__()
            self.client = client
            self.cAppUtil = cAppUtil
            self.view = algorithmView()
            self.root_path = os.path.dirname(os.path.dirname(__file__))+'\\'
            print(self.root_path)
            self.algorithm_file_path = os.path.join(self.root_path, 'upload', 'algorithm\\')
            print(self.algorithm_file_path)
            # self.negative_scheme_edit_view = None
            self.previous_select = None
            # self.negative_scheme_detail = None
            # self.parameter_in_Combobox = ['样本长度一致', '状态标注', '睡眠标注算法', '负例识别算法']
            self.algorithmInfo = []
            # self.is_search = False
            self.search_algorithm_info = []
            self.mac = self.cAppUtil.getMacAddress()
            self.block_size = 5*1024*1024
            self.block_num = None
            # update属性代表当前是否在修改状态
            # self.update = -1
            # self.insert = -1
            self.file_train_algorithm, self.file_test_algorithm, self.file_predict_algorithm = None, None, None
            # header表格头 field数据库表属性
            self.header = ['算法名称', '算法类型']
            self.field = ['alg_name', 'alg_type']
            # 算法文件信息
            self.new_alg_info = {'alg_name': '',  'training_para': '',
                                 'test_para': '',  'predict_para': '', 'alg_type': ''}
            # 训练参数 json格式,后续可拓展
            self.train_para = {
                "nb_class": '',
                "n_epoch": '',
                "sample_len": '',
            }
            self.predict_para = {}
            self.curPageIndex = 1
            self.pageRows = 12
            self.curPageMax = 1
            self.tableWidget = None
            self.key_word = None
            self.key_value = None
            self.isSearch = False
            self.searchPage = 1
            self.searchPageMax = 1
            self.upload_finished.connect(self.uploadFinished)
            # self.update_process.connect(self.updateProcessValue)
            self.view.ui.pushButton.clicked.connect(self.reset)
            self.view.ui.btnAdd.clicked.connect(self.on_clicked_add_algorithm)
            self.view.ui.btnDel.clicked.connect(self.on_clicked_del_algorithm)
            self.view.ui.btnSelect.clicked.connect(self.on_clicked_select_algorithm)
            self.client.getAlgorithmInfoResSig.connect(self.getAlgorithmInfoRes)
            self.client.addAlgorithmInfoResSig.connect(self.addAlgorithmInfoRes)
            self.client.addAlgorithmFileResSig.connect(self.addAlgorithmFileRes)
            self.client.delAlgorithmInfoResSig.connect(self.delAlgorithmInfoRes)
            self.client.getAlgorithmFileNameResSig.connect(self.getAlgorithmFileNameRes)
            self.client.inquiryAlgorithmInfoResSig.connect(self.inquiryAlgorithmInfoRes)
            self.client.algorithmInfoPagingResSig.connect(self.algorithmInfoPagingRes)
            self.client.getAlgorithmInfo([self.curPageIndex, self.pageRows, False])
        except Exception as e:
            print('__init__', e)

    def show_parameter_setting(self, row):
        try:
            self.Parameter_view = Parameter_view()
            self.Parameter_view.ui.label.setText(self.algorithmInfo[row][3])
            self.Parameter_view.ui.label_3.setText(self.algorithmInfo[row][8])
            self.Parameter_view.ui.label_6.setText(self.algorithmInfo[row][13])
            self.Parameter_view.show()
            self.Parameter_view.ui.pushButton_save.clicked.connect(self.close_window)
        except Exception as e:
            print('show_parameter_setting', e)

    def close_window(self):
        self.Parameter_view.close()

    def reset(self):
        try:
            self.curPageIndex = 1
            self.isSearch = False
            self.searchPage = 1
            self.searchPageMax = 1
            self.client.getAlgorithmInfo([self.curPageIndex, self.pageRows, True])
        except Exception as e:
            print('reset', e)

    def getAlgorithmInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                algorithm_info = REPData[2]
                self.curPageMax = REPData[3]
                if self.curPageMax <= 0:
                    self.curPageMax = 1
                reset = REPData[4]
                self.algorithmInfo.clear()
                for i in algorithm_info:
                    temp = list(i)
                    self.algorithmInfo.append(temp)
                print(self.algorithmInfo)
                if reset:
                    self.isSearch = False
                    self.search_algorithm_info.clear()
                    self.view.ui.lineValue.clear()
                    self.clear(self.view.ui.verticalLayout_4)
                    self.tableWidget = TableWidget(self.algorithmInfo, self.curPageIndex,
                                                   self.on_train_alg_upload_btn_clicked,
                                                   self.on_test_alg_upload_btn_clicked,
                                                   self.on_predict_alg_upload_btn_clicked, self.show_parameter_setting)
                    self.view.ui.verticalLayout_4.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
                    QMessageBox.information(self, '提示', '刷新页面成功', QMessageBox.Ok)
                else:
                    self.tableWidget = TableWidget(self.algorithmInfo, self.curPageIndex,
                                                   self.on_train_alg_upload_btn_clicked,
                                                   self.on_test_alg_upload_btn_clicked,
                                                   self.on_predict_alg_upload_btn_clicked, self.show_parameter_setting)
                    self.view.ui.verticalLayout_4.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
                    self.init_comboCond()
            else:
                QMessageBox.information(self, '提示', '获取算法信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('getAlgorithmInfoRes', e)

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

    def algorithmInfoPagingRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "提示", "跳转页面失败", QMessageBox.Yes)
            else:
                isSearch = REPData[3]
                if isSearch:
                    self.search_algorithm_info.clear()
                    self.search_algorithm_info = REPData[2]
                    self.clear(self.view.ui.verticalLayout_4)
                    self.tableWidget = TableWidget(self.search_algorithm_info, self.searchPage,
                                                   self.on_train_alg_upload_btn_clicked,
                                                   self.on_test_alg_upload_btn_clicked,
                                                   self.on_predict_alg_upload_btn_clicked, self.show_parameter_setting)
                    self.view.ui.verticalLayout_4.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.searchPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
                    QMessageBox.information(self, "提示", "跳转页面成功", QMessageBox.Yes)
                else:
                    self.algorithmInfo.clear()
                    self.algorithmInfo = REPData[2]
                    self.clear(self.view.ui.verticalLayout_4)
                    self.tableWidget = TableWidget(self.algorithmInfo, self.curPageIndex,
                                                   self.on_train_alg_upload_btn_clicked,
                                                   self.on_test_alg_upload_btn_clicked,
                                                   self.on_predict_alg_upload_btn_clicked, self.show_parameter_setting)
                    self.view.ui.verticalLayout_4.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
                    QMessageBox.information(self, "提示", "跳转页面成功", QMessageBox.Yes)
        except Exception as e:
            print('userPagingRes', e)

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
            self.client.algorithmInfoPaging(msg)
        except Exception as e:
            print('page_controller', e)

    def init_comboCond(self):
        self.view.ui.comboCond.clear()
        for i in range(len(self.field)):
            self.view.ui.comboCond.addItem(self.header[i], self.field[i])


    # 初始化参数设置页面
    def init_parameterView(self):
        try:
            self.parameterView = ParameterView()
            self.parameterView.setWindowModality(Qt.ApplicationModal)
            self.parameterView.show()
            self.parameterView.ui.lineEdit.setText('{}')
            self.parameterView.ui.lineEdit.setEnabled(False)
            self.parameterView.ui.pushButton.clicked.connect(self.add_train_parameter)
            self.parameterView.ui.pushButton_save.clicked.connect(self.on_parameterView_confirm_btn_clicked)
        except Exception as e:
            print('init_parameterView', e)

    def add_train_parameter(self):
        try:
            self.train_parameter_view = train_parameter_view()
            self.train_parameter_view.setWindowModality(Qt.ApplicationModal)
            self.train_parameter_view.show()
            self.set_train_para = False
            self.train_parameter_view.ui.pushButton.clicked.connect(self.on_clicked_save_train_para)
        except Exception as e:
            print('add_train_parameter', e)

    def on_clicked_save_train_para(self):
        try:
            if self.train_parameter_view.ui.lineEdit.text() == "":
                QMessageBox.information(self, "提示", "未填写训练轮次", QMessageBox.Yes)
            elif self.train_parameter_view.ui.lineEdit_2.text() == "":
                QMessageBox.information(self, "提示", "未填写分类类别数", QMessageBox.Yes)
            self.train_para['n_epoch'] = int(self.train_parameter_view.ui.lineEdit.text())
            self.train_para['nb_class'] = int(self.train_parameter_view.ui.lineEdit_2.text())
            if self.train_parameter_view.ui.lineEdit_3.text() != "":
                self.train_para['sample_len'] = int(self.train_parameter_view.ui.lineEdit_3.text())
            else:
                self.train_para['sample_len'] = self.train_parameter_view.ui.lineEdit_3.text()
            self.set_train_para = True
            self.train_parameter_view.close()
        except Exception as e:
            print('on_clicked_save_train_para', e)


    def on_clicked_add_algorithm(self):
        self.init_parameterView()

    def on_clicked_del_algorithm(self):
        try:
            if self.tableWidget.select_row is None:
                QMessageBox.information(self, '提示', '请选择要删除的算法信息', QMessageBox.Ok)
                return
            reply = QMessageBox.information(self, '提示', '是否删除选中的算法', QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                if self.isSearch:
                    self.client.delAlgorithmInfo(REQmsg=[self.search_algorithm_info[self.tableWidget.select_row][0],
                                                         self.searchPage, self.isSearch, self.key_word, self.key_value])
                else:
                    self.client.delAlgorithmInfo(REQmsg=[self.algorithmInfo[self.tableWidget.select_row][0],
                                                         self.curPageIndex, self.isSearch])
            else:
                return
        except Exception as e:
            print('on_clicked_del_algorithm', e)

    def on_clicked_select_algorithm(self):
        try:
            self.key_word = self.view.ui.comboCond.currentText()
            self.key_value = self.view.ui.lineValue.text()
            self.search_algorithm_info.clear()
            self.isSearch = False
            self.searchPage = 1
            if self.key_value == '':
                QMessageBox.information(self, '提示', '请输入要搜索的算法信息', QMessageBox.Ok)
                return
            if self.key_word == '算法类型' and self.key_value != '波形' and self.key_value != '状态':
                QMessageBox.information(self, '提示', '算法类型查询只有波形或状态俩种选择', QMessageBox.Ok)
                return
            if self.key_word == '算法名称':
                self.key_word = 'alg_name'
            elif self.key_word == '算法类型':
                self.key_word = 'type'
            REQmsg = [self.key_word, self.key_value, self.searchPage, self.pageRows]
            self.client.inquiryAlgorithmInfo(REQmsg)
        except Exception as e:
            print('on_clicked_select_algorithm', e)


    def addAlgorithmInfoRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '添加算法信息失败, 请重新尝试', QMessageBox.Ok)
                return
            else:
                self.isSearch = False
                self.searchPage = 1
                self.searchPageMax = 1
                self.algorithmInfo.clear()
                self.view.ui.lineValue.clear()
                self.algorithmInfo = REPData[2]
                self.curPageMax = REPData[3]
                self.parameterView.ui.pushButton_save.setEnabled(True)
                self.parameterView.close()
                self.clear(self.view.ui.verticalLayout_4)
                self.curPageIndex = REPData[3]
                self.tableWidget = TableWidget(self.algorithmInfo, self.curPageIndex,
                                               self.on_train_alg_upload_btn_clicked,
                                               self.on_test_alg_upload_btn_clicked,
                                               self.on_predict_alg_upload_btn_clicked, self.show_parameter_setting)
                self.view.ui.verticalLayout_4.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
                # self.is_reload_controller.emit("modelTrainController")
                QMessageBox.information(self, '提示', '添加算法信息成功', QMessageBox.Ok)
        except Exception as e:
            print('addLessonRes', e)

    def delAlgorithmInfoRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', '删除算法信息失败, 请重新尝试', QMessageBox.Ok)
                return
            else:
                if self.isSearch:
                    self.search_algorithm_info.clear()
                    self.searchPage = REPData[4]
                    self.search_algorithm_info = REPData[2]
                    self.searchPageMax = REPData[3]
                    self.clear(self.view.ui.verticalLayout_4)
                    self.tableWidget = TableWidget(self.search_algorithm_info, self.searchPage,
                                                   self.on_train_alg_upload_btn_clicked,
                                                   self.on_test_alg_upload_btn_clicked,
                                                   self.on_predict_alg_upload_btn_clicked, self.show_parameter_setting)
                    self.view.ui.verticalLayout_4.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.searchPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
                else:
                    self.algorithmInfo.clear()
                    self.curPageIndex = REPData[4]
                    self.algorithmInfo = REPData[2]
                    self.curPageMax = REPData[3]
                    self.clear(self.view.ui.verticalLayout_4)
                    self.tableWidget = TableWidget(self.algorithmInfo, self.curPageIndex,
                                                   self.on_train_alg_upload_btn_clicked,
                                                   self.on_test_alg_upload_btn_clicked,
                                                   self.on_predict_alg_upload_btn_clicked, self.show_parameter_setting)
                    self.view.ui.verticalLayout_4.addWidget(self.tableWidget)
                    self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                    self.tableWidget.control_signal.connect(self.page_controller)
                QMessageBox.information(self, '提示', '删除算法成功', QMessageBox.Ok)
                self.tableWidget.select_row = None
                # self.is_reload_controller.emit('modelTrainController')
                print(self.algorithmInfo)
        except Exception as e:
            print('delAlgorithmInfoRes', e)

    def inquiryAlgorithmInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.isSearch = True
                self.searchPageMax = REPData[3]
                if self.searchPageMax <= 0:
                    self.searchPageMax = 1
                QMessageBox.information(self, '提示', '查询算法信息成功', QMessageBox.Ok)
                self.search_algorithm_info.clear()
                self.search_algorithm_info = REPData[2]
                self.clear(self.view.ui.verticalLayout_4)
                self.tableWidget = TableWidget(self.search_algorithm_info, self.searchPage,
                                               self.on_train_alg_upload_btn_clicked,
                                               self.on_test_alg_upload_btn_clicked,
                                               self.on_predict_alg_upload_btn_clicked, self.show_parameter_setting)
                self.view.ui.verticalLayout_4.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.searchPageMax)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
            else:
                self.view.ui.lineValue.clear()
                QMessageBox.information(self, '提示', '查询算法信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('inquiryAlgorithmInfoRes', e)

    def getAlgorithmFileName(self, alg_id, flag):
        try:
            self.fileUploadView.ui.pushButton_save.setEnabled(False)
            self.fileUploadView.ui.pushButton_train_algorithm_select.setEnabled(False)
            # 用户未选择算法文件
            if flag == 'training':
                if not self.file_train_algorithm:
                    QMessageBox.information(self.view, '上传失败', "失败原因:尚未选择训练算法文件")
                    return
            elif flag == 'test':
                if not self.file_test_algorithm:
                    QMessageBox.information(self.view, '上传失败', "失败原因:尚未选择测试算法文件")
                    return
            elif flag == 'predict':
                if not self.file_predict_algorithm:
                    QMessageBox.information(self.view, '上传失败', "失败原因:尚未选择预测算法文件")
                    return
            if not os.path.exists(self.algorithm_file_path):
                os.makedirs(self.algorithm_file_path)
            result = self.cAppUtil.isNull(self.algorithm_file_path)
            if result:
                REQmsg = [alg_id, flag]
                print(REQmsg)
                self.client.getAlgorithmFileName(REQmsg)
            else:
                # self.testFile(self.algorithm_file_path)
                # file_list = os.listdir(self.algorithm_file_path)
                # for file in file_list:
                #     file_path = os.path.join(self.algorithm_file_path, file)
                #     os.remove(file_path)
                # reUpload = True
                # self.client.getAlgorithmFileName([alg_id, flag, reUpload])
                if flag == 'training':
                    # file_hash = self.calculate_md5(self.file_train_algorithm[0])
                    file_name_d = 'training.{:>08}'.format(alg_id)
                elif flag == 'test':
                    # file_hash = self.calculate_md5(self.file_test_algorithm[0])
                    file_name_d = 'test.{:>08}'.format(alg_id)
                elif flag == 'predict':
                    # file_hash = self.calculate_md5(self.file_train_algorithm[0])
                    file_name_d = 'predict.{:>08}'.format(alg_id)
                file_name = self.testFile(self.algorithm_file_path)
                if file_name == '':
                    QMessageBox.information(self, '提示', f'本地预处理{file_name_d}的过程出错，上传过程需重新开始',
                                            QMessageBox.Ok)
                    return
                else:
                    r = self.check_txt_files(self.algorithm_file_path)
                    if not r:
                        self.progressBarView = ProgressBarView(window_title="上传算法文件中", hasStopBtn=False,
                                                               maximum=100,
                                                               speed=5)
                        self.progressBarView.show()
                        self.progressBarView.updateProgressBar(0)
                        self.client.addAlgorithmFile(['unknown', alg_id, flag, file_name_d, self.mac])
                    else:
                        self.progressBarView = ProgressBarView(window_title="上传算法文件中", hasStopBtn=False,
                                                               maximum=100,
                                                               speed=5)
                        self.progressBarView.show()
                        self.progressBarView.updateProgressBar(0)
                        self.client.addAlgorithmFile(['continue', alg_id, flag, file_name_d, self.mac])
                # file_path = os.path.join(self.algorithm_file_path, file_name)
                # result = self.check_file_integrity(file_path, file_hash)
                # if not result:
                #     QMessageBox.information(self, '提示', f'本地预处理{file_name_d}的过程出错，上传过程需重新开始', QMessageBox.Ok)
                #     return
        except Exception as e:
            print('getAlgorithmFileName', e)

    def calculate_md5(self, file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
            md5_hash = hashlib.md5(content).hexdigest()
        return md5_hash

    def testFile(self, folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".py"):
                return file_name
        return ''

    def check_txt_files(self, folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".txt"):
                return True
        return False

    def check_file_integrity(self, file_path, expected_hash):
        file_hash = self.calculate_md5(file_path)
        if file_hash == expected_hash:
            return True
        else:
            return False

    def getAlgorithmFileNameRes(self, REPData):
        try:
            if REPData[0] == '1':
                alg_id = REPData[2]
                state = REPData[3]
                # 返回的命名放入此变量
                self.filename = REPData[4] + '.py'
                print(self.filename)
                msg = ['start', alg_id, state]
                fileMsg = self.packageFileMsg(state='start', msg=msg)
                # 复制算法文件到指定文件夹
                if state == 'training':
                    shutil.copyfile(self.file_train_algorithm[0],
                                    self.algorithm_file_path + self.filename)
                    path = os.path.join(self.algorithm_file_path, self.filename)
                    self.block_num = math.ceil((os.stat(path).st_size) / self.block_size)
                    print(self.block_num)
                elif state == 'test':
                    shutil.copyfile(self.file_test_algorithm[0],
                                    self.algorithm_file_path + self.filename)
                    path = os.path.join(self.algorithm_file_path, self.filename)
                    self.block_num = math.ceil((os.stat(path).st_size) / self.block_size)
                elif state == 'predict':
                    shutil.copyfile(self.file_predict_algorithm[0],
                                    self.algorithm_file_path + self.filename)
                    path = os.path.join(self.algorithm_file_path, self.filename)
                    self.block_num = math.ceil((os.stat(path).st_size) / self.block_size)
                self.client.addAlgorithmFile(fileMsg)
        except Exception as e:
            print('getAlgorithmFileNameRes', e)

    def packageFileMsg(self, state='', msg=None, data=None):
        try:
            file_msg = []
            alg_id = msg[1]
            file_state = msg[2]
            if state == 'start':
                file_msg = [state, alg_id, file_state, self.mac, self.filename]
            elif state == 'uploading':
                block_id = msg[3]
                file_msg = [state, alg_id, file_state, self.mac, data, block_id]
            elif state == 'uploaded':
                file_msg = [state, alg_id, file_state, self.mac]
            elif state == 'continue':
                file_msg = [state, alg_id, file_state, self.mac, self.filename]
            return file_msg
        except Exception as e:
            print('packageFileMsg', e)

    def readFileData(self, file_path, block_size, block_id):
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
            print('readFileData', e)
        return data

    def removeFiles(self, filepath, filename='', fullname=''):
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

    def addAlgorithmFileRes(self, REPData):
        try:
            if REPData[0] == '1':
                msg = REPData[3]
                state = msg[0]
                alg_id = msg[1]
                file_state = msg[2]
                file_path = os.path.join(self.algorithm_file_path, self.filename)
                file_name = 'uploading.txt'
                upload_file_path = os.path.join(self.algorithm_file_path, file_name)
                # 算法文件上传协议6.1情况
                if state == 'waiting':
                    block_id = msg[3]
                    if block_id == 1:
                        # word = str(alg_id) + ',' + str(file_state) + ',' + str(self.filename) + ',' + str(self.mac)
                        # with open(upload_file_path, 'w') as f:
                        #     f.write(word)
                        self.makeText(alg_id, file_state, upload_file_path)
                        self.progressBarView = ProgressBarView(window_title="上传算法文件中", hasStopBtn=False, maximum=100,
                                                               speed=5)
                        self.progressBarView.show()
                        self.progressBarView.updateProgressBar(0)
                        # self.dlgProgress = QProgressDialog('正在处理并上传', '', 0, 0, self)
                        # self.dlgProgress.setFixedSize(300, 100)
                        # self.dlgProgress.setCancelButtonText(None)
                        # self.dlgProgress.setAttribute(Qt.WA_DeleteOnClose, True)
                        # self.dlgProgress.setWindowTitle("算法文件上传进度")
                        # self.dlgProgress.setWindowModality(Qt.ApplicationModal)  # 进度对话框
                        # self.dlgProgress.setRange(0, 101)
                        # self.dlgProgress.show()
                        # self.value = 0
                        # self.dlgProgress.setValue(self.value)
                        # self.thread_start(flag='1', file_path=file_path)
                    # 请求文件块数超出文件总块数情况
                    if block_id > self.block_num:
                        REQmsg = self.packageFileMsg(state='uploaded', msg=msg)
                        self.client.addAlgorithmFile(REQmsg)
                    else:
                        data = self.cAppUtil.readByte(file_path, self.block_size, block_id)
                        self.progressBarView.updateProgressBar(block_id/self.block_size * 100)
                        # data = self.readFileData(file_path, self.block_size, block_id)
                        REQmsg = self.packageFileMsg('uploading', msg, data)
                        self.client.addAlgorithmFile(REQmsg)
                # 算法文件上传协议6.2情况
                elif state == 'wrongSite' or state == 'unknownError' or state == 'cleaned' or state == 'wrongServer':
                    # 清空上传错误的脑电文件及其对应记录
                    self.removeFiles(self.algorithm_file_path, filename=self.filename)
                    QMessageBox.information(self, "算法文件上传",
                                            "算法文件上传出错，请重新尝试", QMessageBox.Yes)

                # 算法文件上传协议6.3情况
                elif state == 'uploaded':
                    # self.removeFiles(self.algorithm_file_path, filename=self.filename)
                    # QMessageBox.information(self, "算法文件上传",
                    #                         "算法文件上传完成", QMessageBox.Yes)
                    self.upload_finished.emit([file_state, alg_id])
                # 算法文件上传协议6.3情况
                elif state == 'recover':
                    self.removeFiles(self.algorithm_file_path, filename=file_name)
                    REQmsg = self.packageFileMsg('continue', msg)
                    self.client.addAlgorithmFile(REQmsg)
                else:
                    print(f'状态{state}暂时无法处理服务器传回的这个状态')
            else:
                if len(REPData) > 2:
                    QMessageBox.information(self, "算法文件上传", REPData[2], QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "算法文件上传", REPData[1], QMessageBox.Yes)
        except Exception as e:
            print('addAlgorithmFileRes', e)

    def uploadFinished(self, msg):
        try:
            fileState = msg[0]
            alg_id = msg[1]
            # _translate = QtCore.QCoreApplication.translate
            self.removeFiles(self.algorithm_file_path)
            self.progressBarView.close()
            QMessageBox.information(self, "算法文件上传", "算法文件上传完成", QMessageBox.Yes)
            self.fileUploadView.ui.pushButton_train_algorithm_select.setEnabled(True)
            self.fileUploadView.ui.pushButton_save.setEnabled(True)
            self.fileUploadView.close()
            if self.isSearch:
                for i in range(len(self.search_algorithm_info)):
                    self.search_algorithm_info[i] = list(self.search_algorithm_info[i])
                if fileState == 'training':
                    self.file_train_algorithm = None
                    for i in range(len(self.search_algorithm_info)):
                        if self.search_algorithm_info[i][0] == alg_id:
                            self.search_algorithm_info[i][4] = 'uploaded'
                            # self.tableWidget.table.removeCellWidget(i, 1)
                            break
                elif fileState == 'test':
                    self.file_test_algorithm = None
                    for i in range(len(self.search_algorithm_info)):
                        if self.search_algorithm_info[i][0] == alg_id:
                            self.search_algorithm_info[i][9] = 'uploaded'
                            # self.tableWidget.table.removeCellWidget(i, 2)
                            break
                elif fileState == 'predict':
                    self.file_predict_algorithm = None
                    for i in range(len(self.search_algorithm_info)):
                        if self.search_algorithm_info[i][0] == alg_id:
                            self.search_algorithm_info[i][14] = 'uploaded'
                            # self.tableWidget.table.removeCellWidget(i, 3)
                            break
                self.clear(self.view.ui.verticalLayout_4)
                self.tableWidget = TableWidget(self.search_algorithm_info, self.searchPage,
                                               self.on_train_alg_upload_btn_clicked,
                                               self.on_test_alg_upload_btn_clicked,
                                               self.on_predict_alg_upload_btn_clicked, self.show_parameter_setting)
                self.view.ui.verticalLayout_4.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.searchPageMax)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
            else:
                for i in range(len(self.algorithmInfo)):
                    self.algorithmInfo[i] = list(self.algorithmInfo[i])
                if fileState == 'training':
                    self.file_train_algorithm = None
                    for i in range(len(self.algorithmInfo)):
                        if self.algorithmInfo[i][0] == alg_id:
                            self.algorithmInfo[i][4] = 'uploaded'
                            # self.tableWidget.table.removeCellWidget(i, 1)
                            break
                elif fileState == 'test':
                    self.file_test_algorithm = None
                    for i in range(len(self.algorithmInfo)):
                        if self.algorithmInfo[i][0] == alg_id:
                            self.algorithmInfo[i][9] = 'uploaded'
                            # self.tableWidget.table.removeCellWidget(i, 2)
                            break
                elif fileState == 'predict':
                    self.file_predict_algorithm = None
                    for i in range(len(self.algorithmInfo)):
                        if self.algorithmInfo[i][0] == alg_id:
                            self.algorithmInfo[i][14] = 'uploaded'
                            # self.tableWidget.table.removeCellWidget(i, 3)
                            break
                self.clear(self.view.ui.verticalLayout_4)
                self.tableWidget = TableWidget(self.algorithmInfo, self.curPageIndex,
                                               self.on_train_alg_upload_btn_clicked,
                                               self.on_test_alg_upload_btn_clicked,
                                               self.on_predict_alg_upload_btn_clicked, self.show_parameter_setting)
                self.view.ui.verticalLayout_4.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
        except Exception as e:
            print('uploadFinished', e)

    # def get_selected_items_of_parameterCombobox(self):
    #     items = self.parameterCombobox.get_selected()
    #     para = []
    #     for i in items:
    #         para.append(i.text())
    #     return para
    #
    # def on_parameterCombobox_select_changed(self):
    #     try:
    #         select_items = [i.text() for i in self.parameterCombobox.get_selected()]
    #         if self.previous_select is None:
    #             self.previous_select = select_items
    #         else:
    #             if self.previous_select == select_items:
    #                 return
    #             else:
    #                 self.previous_select = select_items
    #         # print(select_items)
    #         if "负例识别算法" in select_items:
    #             self.negative_scheme_edit_view = scheme_edit_view(controller=self)
    #             self.negative_scheme_edit_view.add_confirm_signal.connect(self.get_negative_scheme_detail)
    #             self.negative_scheme_edit_view.setWindowModality(Qt.ApplicationModal)
    #             self.negative_scheme_edit_view.show()
    #         else:
    #             self.negative_scheme_detail = None
    #     except Exception as e:
    #         print('on_parameterCombobox_select_changed', e)
    #
    # def get_negative_scheme_detail(self, detail):
    #     self.negative_scheme_detail = detail
    #
    # 根据算法添加时用户选择参数构建对应算法描述语句，用于存入数据库
    # def get_selected_algorithm_parameters(self):
    #     para = self.get_selected_items_of_parameterCombobox()
    #     parameters = ['differentsampleLength-True', 'stateAnnotation-False', 'sleepAnnotationAlgorithm-False',
    #                   'negativeRecogAlgorithm-False']
    #     for text in para:
    #         if text == '样本长度一致':
    #             parameters[0] = 'differentsampleLength-False'
    #         if text == '状态标注':
    #             parameters[1] = 'stateAnnotation-True'
    #         if text == '睡眠标注算法':
    #             parameters[2] = 'sleepAnnotationAlgorithm-True'
    #         if text == '负例识别算法':
    #             parameters[3] = 'negativeRecogAlgorithm-True'
    #     ans = ''
    #     for p in parameters:
    #         ans += p + ' '
    #     return ans


    # 相应函数，点击参数设置页面上的保存按钮
    def on_parameterView_confirm_btn_clicked(self):
        # 对新算法的信息进行设置
        try:
            alg_name = self.parameterView.ui.lineEdit_alg_name.text()
            alg_type = self.parameterView.ui.comboBox.currentText()
            if alg_type == '波形标注算法':
                alg_type = 'waveform'
            elif alg_type == '状态标注算法':
                alg_type = 'state'
            # train_para = self.parameterView.ui.lineEdit.text()
            test_para = self.parameterView.ui.lineEdit_2.text()
            predict_para = json.dumps(self.predict_para)
            if not alg_name:
                QMessageBox.information(self.view, '算法名称', "请输入算法名称")
                return
            if not self.set_train_para:
                QMessageBox.information(self.view, '训练参数', "未设置训练参数")
                return
            # for i in self.algorithmInfo:
            #     if i[1] == alg_name:
            #         QMessageBox.information(self.view, '算法名称', "算法名称已被使用，请更改")
            #         return
            train_para = json.dumps(self.train_para)
            self.set_new_alg_info_parameter(alg_name, train_para, test_para, predict_para, alg_type)
            self.parameterView.ui.pushButton_save.setEnabled(False)
            # 数据检查完毕，开始添加算法信息
            self.client.addAlgorithmInfo([self.new_alg_info])
        except Exception as e:
            print('on_parameterView_confirm_btn_clicked', e)

    # 通过控件状态，来对算法的相应信息进行设定
    def set_new_alg_info_parameter(self, alg_name, training_para, test_para, predict_para, alg_type):
        try:
            self.new_alg_info['alg_name'] = alg_name
            self.new_alg_info['training_para'] = training_para
            self.new_alg_info['test_para'] = test_para
            self.new_alg_info['predict_para'] = predict_para
            self.new_alg_info['alg_type'] = alg_type
        except Exception as e:
            print('set_new_alg_info_parameter', e)

    # 响应函数，用户点击算法选择页面上的测试算法按钮
    def on_test_alg_upload_btn_clicked(self, row):
        try:
            if self.isSearch:
                alg_id = self.search_algorithm_info[row][0]
                alg_name = self.search_algorithm_info[row][1]
            else:
                alg_id = self.algorithmInfo[row][0]
                alg_name = self.algorithmInfo[row][1]
            self.fileUploadView = FileUploadView()
            self.fileUploadView.ui.label.setText(alg_name)
            self.fileUploadView.ui.label_trainalg_file_path.setText('测试算法文件选择')
            self.fileUploadView.ui.pushButton_train_algorithm_select.setText('测试算法文件路径:选择')
            self.fileUploadView.ui.pushButton_train_algorithm_select.clicked.connect(self.on_test_alg_btn_clicked)
            self.fileUploadView.ui.pushButton_save.clicked.connect(partial(self.getAlgorithmFileName, alg_id, 'test'))
            self.fileUploadView.setWindowModality(Qt.ApplicationModal)
            self.fileUploadView.show()
        except Exception as e:
            print('on_train_alg_upload_btn_clicked', e)

    def on_test_alg_btn_clicked(self):
        try:
            # 数据库中标签添加成功，将文件复制到classifier文件夹目录下
            test_algorithm = QFileDialog.getOpenFileName(self, "打开文件", self.root_path, "Python Files (*.py)")
            # 用户成功选择算法文件,将算法文件信息存储，并将算法名称显示到页面
            if test_algorithm[0]:
                self.file_test_algorithm = test_algorithm
                f_name = self.file_test_algorithm[0].split('/')[-1]
                _translate = QtCore.QCoreApplication.translate
                self.fileUploadView.ui.label_trainalg_file_path.setText(_translate("Parameter",
                                                                                 "<html><head/><body><p><span style=\" font-size:12pt;\">测试算法文件：" + f_name + "</span></p></body></html>"))
        except Exception as e:
            print('on_test_alg_btn_clicked', e)

    # 响应函数，用户点击算法选择页面上的训练算法按钮
    def on_train_alg_upload_btn_clicked(self, row):
        try:
            if self.isSearch:
                alg_id = self.search_algorithm_info[row][0]
                alg_name = self.search_algorithm_info[row][1]
            else:
                alg_id = self.algorithmInfo[row][0]
                alg_name = self.algorithmInfo[row][1]
            self.fileUploadView = FileUploadView()
            self.fileUploadView.ui.label.setText(alg_name)
            self.fileUploadView.ui.pushButton_train_algorithm_select.clicked.connect(self.on_train_alg_btn_clicked)
            self.fileUploadView.ui.pushButton_save.clicked.connect(partial(self.getAlgorithmFileName, alg_id, 'training'))
            self.fileUploadView.setWindowModality(Qt.ApplicationModal)
            self.fileUploadView.show()
        except Exception as e:
            print('on_train_alg_upload_btn_clicked', e)
    def on_train_alg_btn_clicked(self):
        try:
            # 数据库中标签添加成功，将文件复制到classifier文件夹目录下
            train_algorithm = QFileDialog.getOpenFileName(self, "打开文件", self.root_path, "Python Files (*.py)")
            print(self.root_path)
            print(train_algorithm)
            # 用户成功选择算法文件
            if train_algorithm[0]:
                self.file_train_algorithm = train_algorithm
                f_name = self.file_train_algorithm[0].split('/')[-1]
                _translate = QtCore.QCoreApplication.translate
                self.fileUploadView.ui.label_trainalg_file_path.setText(_translate("Parameter",
                                                                                  "<html><head/><body><p><span style=\" font-size:12pt;\">训练算法文件：" + f_name + "</span></p></body></html>"))
        except Exception as e:
            print('on_train_alg_btn_clicked', e)

    # 响应函数，用户点击算法选择页面上的预测算法按钮
    def on_predict_alg_upload_btn_clicked(self, row):
        try:
            if self.isSearch:
                alg_id = self.search_algorithm_info[row][0]
                alg_name = self.search_algorithm_info[row][1]
            else:
                alg_id = self.algorithmInfo[row][0]
                alg_name = self.algorithmInfo[row][1]
            self.fileUploadView = FileUploadView()
            self.fileUploadView.ui.label.setText(alg_name)
            self.fileUploadView.ui.label_trainalg_file_path.setText('预测算法文件选择')
            self.fileUploadView.ui.pushButton_train_algorithm_select.setText('预测算法文件路径:选择')
            self.fileUploadView.ui.pushButton_train_algorithm_select.clicked.connect(self.on_predict_alg_btn_clicked)
            self.fileUploadView.ui.pushButton_save.clicked.connect(partial(self.getAlgorithmFileName, alg_id, 'predict'))
            self.fileUploadView.setWindowModality(Qt.ApplicationModal)
            self.fileUploadView.show()
        except Exception as e:
            print('on_train_alg_upload_btn_clicked', e)

    def on_predict_alg_btn_clicked(self):
        try:
            predict_algorithm = QFileDialog.getOpenFileName(self, "打开文件", self.root_path, "Python Files (*.py)")
            # 用户成功选择算法文件
            if predict_algorithm[0]:
                self.file_predict_algorithm = predict_algorithm
                f_name = self.file_predict_algorithm[0].split('/')[-1]
                _translate = QtCore.QCoreApplication.translate
                self.fileUploadView.ui.label_trainalg_file_path.setText(_translate("Parameter",
                                                                                     "<html><head/><body><p><span style=\" font-size:12pt;\">预测算法文件：" + f_name + "</span></p></body></html>"))
        except Exception as e:
            print('on_predict_alg_btn_clicked', e)

    # def thread_start(self, flag='', file_path=''):
    #     if flag == '1':
    #         # 处理后上传
    #         self.thread1 = threading.Thread(target=self.timeCount, args=(file_path,))
    #         self.thread1.start()
    #         # self.thread = threading.Thread(target=self.process_edf)
    #         # self.thread.start()
    #     else:
    #         # 重新上传
    #         self.thread1 = threading.Thread(target=self.timeCount, args=(file_path,))
    #         self.thread1.start()


    # def timeCount(self, from_filepath):
    #     if not os.path.exists(from_filepath):
    #         self.update_process.emit(100)
    #         return
    #     # 根据文件大小预估时间(单位kB)
    #     file_size = (os.path.getsize(from_filepath) // 1024)
    #     if from_filepath.endswith('.py'):
    #         # 进度条更新周期
    #         turn_time = 0.01
    #         # 预估时间
    #         guess_time = file_size // 0.01
    #     # 进度条更新轮次
    #     turn = int(guess_time / turn_time)
    #     for i in range(turn):
    #         sleep(turn_time)
    #         incre_value = math.ceil(turn_time * 100 / guess_time)
    #         self.update_process.emit(incre_value)

    # def updateProcessValue(self, incre_value):
    #     if self.value == 100:
    #         return
    #     self.value += incre_value
    #     if self.value > 100:
    #         self.value = 100
    #     self.dlgProgress.setValue(self.value)

    def makeText(self, alg_id, file_state, upload_file_path):
        word = str(alg_id) + ',' + str(file_state) + ',' + str(self.filename) + ',' + str(self.mac)
        with open(upload_file_path, 'w') as f:
            f.write(word)

    def exit(self):
        self.client.getAlgorithmInfoResSig.disconnect()
        self.client.addAlgorithmInfoResSig.disconnect()
        self.client.addAlgorithmFileResSig.disconnect()
        self.client.delAlgorithmInfoResSig.disconnect()
        self.client.getAlgorithmFileNameResSig.disconnect()
        self.client.inquiryAlgorithmInfoResSig.disconnect()
        self.client.algorithmInfoPagingResSig.disconnect()
