import json

from matplotlib import pyplot as plt

from view.modelTrain import modelTrainView, Parameter_view

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
import numpy as np
import pickle

import weakref
import os, time


from view.progressBarView import ProgressBarView


class modelTrainController(QWidget):
    process_value = pyqtSignal(int)
    is_reload_controller = pyqtSignal(str)

    def __init__(self, client, cAppUtil):
        try:
            super().__init__()
            self.client = client
            self.cAppUtil = cAppUtil
            self.view = modelTrainView()
            # 列表，当前数据集合包含的单个样本的长度,可能会有多种长度
            self.set_file_type = None
            self.algorithm_info = []
            self.set_info = []
            self.type_info = []
            self.click_stop_button = False
            # 训练参数 json格式,后续可拓展
            self.train_para = {
                "nb_class",
                "n_epoch",
                "sample_len",
            }
            # 当前页面中被选中的数据集名称
            self.set_name = None
            # 当前页面中被选中的数据集id
            self.set_id = None
            # 当前页面中被选中的算法名称
            self.algorithm_name = None
            # 当前页面中被选中的算法id
            self.alg_id = None
            # 所选训练集是否包含不同长度的样本
            self.config_id = None
            self.set_different_len = None
            self.classifier_state = None
            self.classifier_train_state = None
            # 当前被选中算法和数据集对应的模型信息
            self.cls_info = None
            self.cur_classifier_name = None
            # 当前算法页面
            self.alg_page = 1
            # 算法页面最大值
            self.alg_page_max = 1
            # 算法单页记录数
            self.alg_page_row = 8
            self.apv = 10
            # 当前算法搜索页面
            self.alg_search_page = 1
            # 搜索算法页面最大值
            self.alg_search_page_max = 1
            # 搜索算法信息列表
            self.search_algorithm_info = []
            # 搜索算法关键字
            self.alg_key_word = None
            # 搜索算法值
            self.alg_key_value = None
            # 是否处于算法搜索状态
            self.is_alg_search = False
            # 当前数据集页面
            self.set_page = 1
            # 数据集页面最大值
            self.set_page_max = 1
            # 数据集单页记录数
            self.set_page_row = 10
            # 当前数据集搜索页面
            self.set_search_page = 1
            # 当前数据集搜索页面最大值
            self.set_search_page_max = 1
            self.search_set_info = []
            self.epoch = 0
            self.set_key_word = None
            self.set_key_value = None
            self.is_set_search = False
            # self.view.ui.trainbtn.clicked.connect(self.on_btnTrain_clicked)
            self.view.ui.pushButton_15.clicked.connect(self.on_btnMatch_clicked)
            # self.view.ui.pushButton_16.clicked.connect(self.show_train_performance)
            self.view.ui.trainbtn.hide()
            # self.view.ui.pushButton_16.setEnabled(False)
            self.view.ui.pushButton_16.hide()
            self.view.ui.algorithm_tableWidget.itemClicked.connect(self.on_clicked_alg_table_item)
            self.view.ui.trainset_tableWidget.itemClicked.connect(self.on_clicked_set_table_item)
            self.trainOutput = weakref.proxy(self.view.ui.editTrainOutput)
            self.client.getModelInfo([self.alg_page, self.alg_page_row, self.set_page, self.set_page_row, False, False])
            self.client.getModelInfoResSig.connect(self.getModelInfoRes)
            self.client.get_classifierInfo_by_setId_and_algIdResSig.connect(self.get_classifierInfo_by_setId_and_algIdRes)
            self.client.modelAlgInfoPagingResSig.connect(self.modelAlgInfoPagingRes)
            self.client.modelInquiryAlgInfoResSig.connect(self.modelInquiryAlgInfoRes)
            self.client.modelSetInfoPagingResSig.connect(self.modelSetInfoPagingRes)
            self.client.modelInquirySetInfoResSig.connect(self.modelInquirySetInfoRes)
            self.client.matchAlgSetResSig.connect(self.matchAlgSetRes)
            self.client.runProcessForTrainResSig.connect(self.runProcessForTrainRes)
            self.client.getTrainPerformanceResSig.connect(self.getTrainPerformanceRes)
            self.client.getProgressResSig.connect(self.getProgressRes)
            self.client.train_cancelResSig.connect(self.train_cancelRes)
        except Exception as e:
            print('__init__', e)

    def getModelInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                alg_reset = REPData[8]
                set_reset = REPData[9]
                if alg_reset == False and set_reset == False:
                    self.algorithm_info = REPData[2]
                    self.alg_page_max = REPData[3]
                    self.set_info = REPData[4]
                    self.set_page_max = REPData[5]
                    self.type_info = REPData[6]
                    self.set_file_type = REPData[7]
                    if self.alg_page_max <= 0:
                        self.alg_page_max = 1
                    if self.set_page_max <= 0:
                        self.set_page_max = 1
                    self.view.initAlgorithmTable(self.algorithm_info, self.show_parameter_setting)
                    self.view.ui.label.setText("共" + str(self.alg_page_max) + "页")
                    self.view.ui.label_3.setText(str(self.alg_page))
                    self.view.page_control_signal.connect((self.page_controller))
                    self.view.ui.pushButton.clicked.connect(self.on_query_alg_info)
                    self.view.ui.pushButton_11.clicked.connect(self.on_reset_alg_info)
                    self.view.initSetTable(self.set_info)
                    self.view.ui.label_2.setText("共" + str(self.set_page_max) + "页")
                    self.view.ui.label_4.setText(str(self.set_page))
                    self.view.page_control_signal_1.connect((self.page_controller_1))
                    self.view.ui.pushButton_10.clicked.connect(self.on_query_set_info)
                    self.view.ui.pushButton_12.clicked.connect(self.on_reset_set_info)
                elif alg_reset == True and set_reset == False:
                    self.algorithm_info = REPData[2]
                    self.alg_page_max = REPData[3]
                    if self.alg_page_max <= 0:
                        self.alg_page_max = 1
                    self.view.initAlgorithmTable(self.algorithm_info, self.show_parameter_setting)
                    self.view.ui.label.setText("共" + str(self.alg_page_max) + "页")
                    self.view.ui.label_3.setText(str(self.alg_page))
                    self.view.ui.lineEdit.clear()
                    self.view.ui.label_algname.setText('当前选中算法:无')
                    self.alg_id = None
                    QMessageBox.information(self, '提示', '刷新算法页面成功', QMessageBox.Ok)
                elif alg_reset == False and set_reset == True:
                    self.set_info = REPData[2]
                    self.set_page_max = REPData[3]
                    if self.set_page_max <= 0:
                        self.set_page_max = 1
                    self.view.initSetTable(self.set_info)
                    self.view.ui.label_2.setText("共" + str(self.set_page_max) + "页")
                    self.view.ui.label_4.setText(str(self.set_page))
                    self.view.ui.lineEdit_2.clear()
                    self.view.ui.label_setname.setText("当前选中数据集:无")
                    self.set_id = None
                    QMessageBox.information(self, '提示', '刷新数据集页面成功', QMessageBox.Ok)
            else:
                QMessageBox.information(self, '提示', '获取模型训练界面信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('getModelInfoRes', e)

    def on_reset_alg_info(self):
        try:
            self.alg_page = 1
            self.is_alg_search = False
            self.alg_search_page = 1
            self.alg_search_page_max = 1
            self.client.getModelInfo([self.alg_page, self.alg_page_row, self.set_page, self.set_page_row, True, False])
        except Exception as e:
            print('on_reset_alg_info', e)

    def on_reset_set_info(self):
        try:
            self.set_page = 1
            self.is_set_search = False
            self.set_search_page = 1
            self.set_search_page_max = 1
            self.client.getModelInfo([self.alg_page, self.alg_page_row, self.set_page, self.set_page_row, False, True])
        except Exception as e:
            print('on_reset_set_info', e)


    def on_query_alg_info(self):
        try:
            self.alg_key_word = self.view.ui.comboBox.currentText()
            self.alg_key_value = self.view.ui.lineEdit.text()
            self.search_algorithm_info.clear()
            self.alg_search_page = 1
            self.is_alg_search = False
            if self.alg_key_value == '':
                QMessageBox.information(self, '提示', '请输入要搜索的算法信息', QMessageBox.Ok)
                return
            if self.alg_key_word == '算法类型' and self.alg_key_value != '波形' and self.alg_key_value != '状态':
                QMessageBox.information(self, '提示', '算法类型查询只有波形或状态俩种选择', QMessageBox.Ok)
                return
            if self.alg_key_word == '算法名称':
                self.alg_key_word = 'alg_name'
            elif self.alg_key_word == '算法类型':
                self.alg_key_word = 'type'
            REQmsg = [self.alg_key_word, self.alg_key_value, self.alg_search_page, self.alg_page_row]
            self.client.modelInquiryAlgInfo(REQmsg)
        except Exception as e:
            print('on_query_alg_info', e)

    def on_query_set_info(self):
        try:
            self.set_key_word = self.view.ui.comboBox_2.currentText()
            self.set_key_value = self.view.ui.lineEdit_2.text()
            self.search_set_info.clear()
            self.set_search_page = 1
            self.is_set_search = False
            if self.set_key_value == '':
                QMessageBox.information(self, '提示', '请输入要搜索的数据集信息', QMessageBox.Ok)
                return
            if self.set_key_word == '数据集名称':
                self.set_key_word = 'set_name'
            REQmsg = [self.set_key_word, self.set_key_value, self.set_search_page, self.set_page_row]
            self.client.modelInquirySetInfo(REQmsg)
        except Exception as e:
            print('on_query_alg_info', e)

    def modelAlgInfoPagingRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "提示", "跳转页面失败", QMessageBox.Yes)
                return
            else:
                isSearch = REPData[3]
                if isSearch:
                    self.search_algorithm_info.clear()
                    self.search_algorithm_info = REPData[2]
                    self.view.initAlgorithmTable(self.search_algorithm_info, self.show_parameter_setting)
                    self.view.ui.label.setText("共" + str(self.alg_search_page_max) + "页")
                    self.view.ui.label_3.setText(str(self.alg_search_page))
                else:
                    self.algorithm_info.clear()
                    self.algorithm_info = REPData[2]
                    self.view.initAlgorithmTable(self.algorithm_info, self.show_parameter_setting)
                    self.view.ui.label.setText("共" + str(self.alg_page_max) + "页")
                    self.view.ui.label_3.setText(str(self.alg_page))
        except Exception as e:
            print('modelAlgInfoPagingRes', e)

    def modelInquirySetInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.is_set_search = True
                self.set_search_page_max = REPData[3]
                QMessageBox.information(self, '提示', '查询数据集信息成功', QMessageBox.Ok)
                self.search_set_info.clear()
                self.search_set_info = REPData[2]
                self.view.initSetTable(self.search_set_info)
                self.view.ui.label_2.setText("共" + str(self.set_search_page_max) + "页")
                self.view.ui.label_4.setText(str(self.set_search_page))
            else:
                self.view.ui.lineEdit_2.clear()
                QMessageBox.information(self, '提示', '查询数据集信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('inquiryAlgorithmInfoRes', e)

    def modelSetInfoPagingRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "提示", "跳转页面失败", QMessageBox.Yes)
                return
            else:
                isSearch = REPData[3]
                if isSearch:
                    self.search_set_info.clear()
                    self.search_set_info = REPData[2]
                    self.view.initSetTable(self.set_info)
                    self.view.ui.label_2.setText("共" + str(self.set_search_page_max) + "页")
                    self.view.ui.label_4.setText(str(self.set_search_page))
                else:
                    self.set_info.clear()
                    self.set_info = REPData[2]
                    self.view.initSetTable(self.set_info)
                    self.view.ui.label_2.setText("共" + str(self.set_page_max) + "页")
                    self.view.ui.label_4.setText(str(self.set_page))
        except Exception as e:
            print('modelSetInfoPagingRes', e)

    def modelInquiryAlgInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.is_alg_search = True
                self.alg_search_page_max = REPData[3]
                QMessageBox.information(self, '提示', '查询算法信息成功', QMessageBox.Ok)
                self.search_algorithm_info.clear()
                self.search_algorithm_info = REPData[2]
                self.view.initAlgorithmTable(self.search_algorithm_info, self.show_parameter_setting)
                self.view.ui.label.setText("共" + str(self.alg_search_page_max) + "页")
                self.view.ui.label_3.setText(str(self.alg_search_page))
            else:
                self.view.ui.lineEdit.clear()
                QMessageBox.information(self, '提示', '查询算法信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('inquiryAlgorithmInfoRes', e)

    def page_controller(self, signal):
        try:
            if "home" == signal[0]:
                if self.is_alg_search == False:
                    if self.alg_page == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.alg_page = 1
                    self.view.ui.label_3.setText(str(self.alg_page))
                else:
                    if self.alg_search_page == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.alg_search_page = 1
                    self.view.ui.label_3.setText(str(self.alg_search_page))
            elif "pre" == signal[0]:
                if self.is_alg_search == False:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.alg_page <= 1:
                        return
                    self.alg_page = self.alg_page - 1
                    self.view.ui.label_3.setText(str(self.alg_page))
                else:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.alg_search_page <= 1:
                        return
                    self.alg_search_page = self.alg_search_page - 1
                    self.view.ui.label_3.setText(str(self.alg_search_page))
            elif "next" == signal[0]:
                if self.is_alg_search == False:
                    if self.alg_page_max == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.alg_page = self.alg_page + 1
                    self.view.ui.label_3.setText(str(self.alg_page))
                else:
                    if self.alg_search_page_max == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.alg_search_page = self.alg_search_page + 1
                    self.view.ui.label_3.setText(str(self.alg_search_page))
            elif "final" == signal[0]:
                if self.is_alg_search == False:
                    if self.alg_page == self.alg_page_max:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.alg_page = self.alg_page_max
                    self.view.ui.label_3.setText(str(self.alg_page_max))
                else:
                    if self.alg_search_page == self.alg_search_page_max:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.alg_search_page = self.alg_search_page_max
                    self.view.ui.label_3.setText(str(self.alg_search_page_max))
            elif "confirm" == signal[0]:
                if self.is_alg_search == False:
                    if self.alg_page == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.alg_page_max < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.alg_page = int(signal[1])
                    self.view.ui.label_3.setText(signal[1])
                else:
                    if self.alg_search_page == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.alg_search_page_max < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.alg_search_page = int(signal[1])
                    self.view.ui.label_3.setText(signal[1])
            if self.is_alg_search == False:
                msg = [self.alg_page, self.alg_page_row, signal[0], self.is_alg_search]
            else:
                msg = [self.alg_search_page, self.alg_page_row, signal[0], self.is_alg_search, self.alg_key_word, self.alg_key_value]
            self.client.modelAlgInfoPaging(msg)
        except Exception as e:
            print('page_controller', e)

    def page_controller_1(self, signal):
        try:
            if "home" == signal[0]:
                if self.is_set_search == False:
                    if self.set_page == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.set_page = 1
                    self.view.ui.label_4.setText(str(self.set_page))
                else:
                    if self.set_search_page == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.set_search_page = 1
                    self.view.ui.label_4.setText(str(self.set_search_page))
            elif "pre" == signal[0]:
                if self.is_set_search == False:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.set_page <= 1:
                        return
                    self.set_page = self.set_page - 1
                    self.view.ui.label_4.setText(str(self.set_page))
                else:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.set_search_page <= 1:
                        return
                    self.set_search_page = self.set_search_page - 1
                    self.view.ui.label_4.setText(str(self.set_search_page))
            elif "next" == signal[0]:
                if self.is_set_search == False:
                    if self.set_page_max == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.set_page = self.set_page + 1
                    self.view.ui.label_4.setText(str(self.set_page))
                else:
                    if self.set_search_page_max == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.set_search_page = self.set_search_page + 1
                    self.view.ui.label_4.setText(str(self.set_search_page))
            elif "final" == signal[0]:
                if self.is_set_search == False:
                    if self.set_page == self.set_page_max:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.set_page = self.set_page_max
                    self.view.ui.label_4.setText(str(self.set_page_max))
                else:
                    if self.set_search_page == self.set_search_page_max:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.set_search_page = self.set_search_page_max
                    self.view.ui.label_4.setText(str(self.set_search_page_max))
            elif "confirm" == signal[0]:
                if self.is_set_search == False:
                    if self.set_page == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.set_page_max < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.set_page = int(signal[1])
                    self.view.ui.label_4.setText(signal[1])
                else:
                    if self.set_search_page == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.set_search_page_max < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.set_search_page = int(signal[1])
                    self.view.ui.label_4.setText(signal[1])
            if self.is_set_search == False:
                msg = [self.set_page, self.set_page_row, signal[0], self.is_set_search]
            else:
                msg = [self.set_search_page, self.set_page_row, signal[0], self.is_set_search,
                       self.set_key_word, self.set_key_value]
            self.client.modelSetInfoPaging(msg)
        except Exception as e:
            print('page_controller_1', e)

    def show_parameter_setting(self, row):
        try:
            self.Parameter_view = Parameter_view()
            self.Parameter_view.ui.label.setText(self.algorithm_info[row][3])
            self.Parameter_view.ui.label_3.setText(self.algorithm_info[row][8])
            self.Parameter_view.ui.label_6.setText(self.algorithm_info[row][13])
            self.Parameter_view.show()
            self.Parameter_view.ui.pushButton_save.clicked.connect(self.close_window)
        except Exception as e:
            print('show_parameter_setting', e)

    def close_window(self):
        self.Parameter_view.close()

    # def init_process_barView(self):
    #     # 总进度条视图
    #     self.processBarView = ProcessBarView()
    #     self.processBarView.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
    #     # 进度条当前进度值
    #     self.pv = 0
    #     self.processBarView.ui.progressBar.setMaximum(100)
    #     self.processBarView.ui.progressBar.setValue(self.pv)
    #     self.process_value.connect(self.processBar_value_set)
    #     self.processBarView.ui.stop_pushButton.hide()
        # self.processBarView.ui.stop_pushButton.clicked.connect(self.on_clicked_stop_pushButton)


    # 禁用页面控件
    # 一定要放在运行算法后面，否则进入模态后会导致算法无法运行
    def disable_controls(self):
        try:
            self.view.ui.trainset_tableWidget.setEnabled(False)
            self.view.ui.algorithm_tableWidget.setEnabled(False)
            self.view.ui.pushButton_15.setEnabled(False)
            # self.view.ui.trainbtn.setEnabled(False)
            self.view.ui.pushButton.setEnabled(False)
            self.view.ui.pushButton_2.setEnabled(False)
            self.view.ui.pushButton_3.setEnabled(False)
            self.view.ui.pushButton_4.setEnabled(False)
            self.view.ui.pushButton_5.setEnabled(False)
            self.view.ui.pushButton_6.setEnabled(False)
            self.view.ui.pushButton_7.setEnabled(False)
            self.view.ui.pushButton_8.setEnabled(False)
            self.view.ui.pushButton_9.setEnabled(False)
            self.view.ui.pushButton_10.setEnabled(False)
            self.view.ui.pushButton_11.setEnabled(False)
            self.view.ui.pushButton_12.setEnabled(False)
            self.view.ui.pushButton_13.setEnabled(False)
            self.view.ui.pushButton_14.setEnabled(False)
            # self.view.ui.pushButton_16.setEnabled(False)
            # self.view_lock()
        except Exception as e:
            print('disable_controls', e)

    # 启用页面控件
    def enable_controls(self):
        try:
            self.view.ui.trainset_tableWidget.setEnabled(True)
            self.view.ui.algorithm_tableWidget.setEnabled(True)
            self.view.ui.pushButton_15.setEnabled(True)
            # self.view.ui.trainbtn.setEnabled(True)
            self.view.ui.pushButton.setEnabled(True)
            self.view.ui.pushButton_2.setEnabled(True)
            self.view.ui.pushButton_3.setEnabled(True)
            self.view.ui.pushButton_4.setEnabled(True)
            self.view.ui.pushButton_5.setEnabled(True)
            self.view.ui.pushButton_6.setEnabled(True)
            self.view.ui.pushButton_7.setEnabled(True)
            self.view.ui.pushButton_8.setEnabled(True)
            self.view.ui.pushButton_9.setEnabled(True)
            self.view.ui.pushButton_10.setEnabled(True)
            self.view.ui.pushButton_11.setEnabled(True)
            self.view.ui.pushButton_12.setEnabled(True)
            self.view.ui.pushButton_13.setEnabled(True)
            self.view.ui.pushButton_14.setEnabled(True)
            # self.view.ui.pushButton_16.setEnabled(True)
            # self.view_unlock()
        except Exception as e:
            print('enable_controls', e)


    # 向页面中的文本框中输出信息
    def output_info(self, msg):
        self.trainOutput.appendPlainText(msg)
        QApplication.processEvents()

    # 判断当前被选中的算法能否使用被选中的训练集进行训练操作,如果满足条件则激活相应按钮
    def if_train_abel(self):
        # 未选中算法或数据集
        if self.set_id == None or self.alg_id == None:
            return False
        # 训练集为不同长度，同时算法不支持使用不同长度的样本作为训练集
        # if self.set_different_len and not self.alg_different_len_avilable:
        #     self.view.ui.trainbtn.setEnabled(False)
        #     self.view.ui.pushButton_train_then_test.setEnabled(False)
        #     return False
        # else:
        #     """
        #     训练集样本不同长，算法支持不同长
        #     训练集样本同长，算法不支持不同长
        #     训练集样本同长，算法支持不同长
        #     """
        #     self.view.ui.trainbtn.setEnabled(True)
        #     self.view.ui.pushButton_train_then_test.setEnabled(True)
        #     return True
        # 判断算法是否为状态标注算法以及数据集是否为状态标注数据集
        # 当算法为波形标注算法且数据集为状态标注数据集或同为波形标注算法和数据集
        tag = False
        # 判断算法和数据集是否为同一类型，只有同为波形数据集和波形算法或同为状态数据集和状态算法才能够进行模型构建
        if not (self.if_selected_set_is_state_annotation_set() ^
                self.if_selected_algorithm_avilabel_for_state_annotation_set()):
            tag = True
        else:
            tag = False
        # 判断是否满足模型构建的要求，满足
        if tag == True:
            if self.alg_id and self.set_id:
                self.client.get_classifierInfo_by_setId_and_algId([self.alg_id, self.set_id, self.config_id])
        else:
            self.view.ui.trainbtn.setEnabled(False)
            return False

    def get_classifierInfo_by_setId_and_algIdRes(self, REPData):
        try:
            if REPData[0] == '1':
                classifier_info = REPData[2]
                if len(classifier_info) > 0:
                    self.cls_info = classifier_info[0]
                    self.classifier_train_state = '已训练'
                    classifier_name = self.cls_info[1]
                else:
                    self.cls_info = None
                    classifier_name = '无'
                    self.classifier_train_state = '未训练'
                self.view.ui.label_model_state.setText(
                    '当前模型状态：' + classifier_name + '|' + self.classifier_train_state)
            else:
                QMessageBox.information(self, '提示', '根据算法和数据集信息获取模型信息失败,请重试', QMessageBox.Ok)
            self.view.ui.pushButton_15.setEnabled(True)
        except Exception as e:
            print('get_classifierInfo_by_setId_and_algIdRes', e)


    # 响应函数,用户点击页面上的训练按钮
    def on_btnTrain_clicked(self):
        row = self.view.ui.algorithm_tableWidget.currentRow()
        if not self.view.ui.algorithm_tableWidget.currentRow() > -1:
            QMessageBox.critical(self, 'Alert', '未选择训练算法')
            return
        if not self.view.ui.trainset_tableWidget.currentRow() > -1:
            QMessageBox.critical(self, 'Alert', '未选择训练数据集')
            return
        if self.is_alg_search:
            if self.search_algorithm_info[row][4] != 'uploaded':
                QMessageBox.critical(self, 'Alert', '未上传训练算法文件')
                return
        else:
            if self.algorithm_info[row][4] != 'uploaded':
                QMessageBox.critical(self, 'Alert', '未上传训练算法文件')
                return
        if self.classifier_train_state == '已训练':
            reply = QMessageBox.information(self, '提示', '模型已完成训练，是否需要重复进行训练？',
                                            QMessageBox.Yes | QMessageBox.No)
            if reply != 16384:
                self.client.train_cancel([self.client.tUser[0]])
                return
        self.trainOutput.clear()
        if self.is_alg_search:
            train_algorithm_filename = self.search_algorithm_info[self.view.ui.algorithm_tableWidget.currentRow()][2]
        else:
            train_algorithm_filename = self.algorithm_info[self.view.ui.algorithm_tableWidget.currentRow()][2]
        self.view.ui.trainbtn.setText("训练中")
        # self.processBarView._set_window_title(title="训练中")
        self.view.ui.trainbtn.setEnabled(False)
        self.trainOutput.appendPlainText("训练开始")
        self.client.runProcessForTrain([train_algorithm_filename])
        self.disable_controls()
        # self.view_lock()

    def on_btnMatch_clicked(self):
        try:
            self.view.ui.pushButton_15.setEnabled(False)
            row = self.view.ui.algorithm_tableWidget.currentRow()
            if not self.view.ui.algorithm_tableWidget.currentRow() > -1:
                QMessageBox.critical(self, 'Alert', '未选择训练算法')
                self.view.ui.pushButton_15.setEnabled(True)
                return
            if not self.view.ui.trainset_tableWidget.currentRow() > -1:
                QMessageBox.critical(self, 'Alert', '未选择训练数据集')
                self.view.ui.pushButton_15.setEnabled(True)
                return
            if self.is_alg_search:
                if self.search_algorithm_info[row][4] != 'uploaded':
                    QMessageBox.critical(self, 'Alert', '未上传训练算法文件')
                    self.view.ui.pushButton_15.setEnabled(True)
                    return
            else:
                if self.algorithm_info[row][4] != 'uploaded':
                    QMessageBox.critical(self, 'Alert', '未上传训练算法文件')
                    self.view.ui.pushButton_15.setEnabled(True)
                    return
            if self.is_alg_search:
                alg_name = self.search_algorithm_info[row][1]
            else:
                alg_name = self.algorithm_info[row][1]
            self.client.matchAlgSet([self.alg_id, self.set_id, self.config_id, alg_name])
        except Exception as e:
            print('on_btnMatch_clicked', e)

    def get_set_channel_info(self, set_description):
        return set_description.split('+')[3]

    # 响应函数，点击数据集表中的选项。对训练集进行检测，判断其中包含的样本长度是否一致
    def on_clicked_set_table_item(self, item=None):
        try:
            if self.alg_id == None:
                QMessageBox.information(self.view, '提示', '请先选择使用的算法', QMessageBox.Yes)
                return
            row = item.row()
            # 被选中的训练集信息
            if self.is_set_search:
                set_info = self.search_set_info[row]
            else:
                set_info = self.set_info[row]
            self.set_id = set_info[0]
            self.config_id = set_info[2]
            self.set_description = json.loads(set_info[3])
            set_type = None
            # if self.if_selected_set_is_state_annotation_set():
            set_type = self.set_description['type']
            if set_type == 'wave':
                set_type = '波形标注数据集'
            else:
                set_type = '状态标注数据集'
            self.view.ui.label_setname.setText('当前选中数据集：{}'.format(set_info[1])+'    '+set_type)
            self.client.get_classifierInfo_by_setId_and_algId([self.alg_id, self.set_id, self.config_id])
        except Exception as e:
            print('on_clicked_set_table_item', e)

    # 响应函数，点击算法表中的选项
    def on_clicked_alg_table_item(self, item=None):
        try:
            row = item.row()
            if self.is_alg_search:
                alg_info = self.search_algorithm_info[row]
            else:
                alg_info = self.algorithm_info[row]
            self.alg_id = alg_info[0]
            if alg_info[17] == "state":
                annotation = '状态标注算法'
            else:
                annotation = '波形标注算法'
            self.view.ui.label_algname.setText('当前选中算法：{}      '.format(alg_info[1]) + annotation)
            train_para = json.loads(alg_info[3])
            self.epoch = train_para["n_epoch"]
            if self.set_id != None:
                self.client.get_classifierInfo_by_setId_and_algId([self.alg_id, self.set_id, self.config_id])
        except Exception as e:
            print('on_clicked_alg_table_item', e)


    # 当前选择的算法或数据集发生变化，或是完成训练或测试，刷新控件状态
    # def refresh_view_controls_state(self):
    #     try:
    #         self.if_train_abel()
    #         # self.get_classifier_train_test_state()
    #     except Exception as e:
    #         print('refresh_view_controls_state', e)

    # 锁定当前页面，禁止用户进行操作
    # def view_lock(self):
    #     # 使自动扫描窗口进入模态
    #     # self.ud_thread = threading.Thread(target=self.processBar_update)
    #     # self.ud_thread.start()
    #     # self.processBarView.setWindowModality(Qt.ApplicationModal)
    #     # self.processBarView.setFixedSize(1, 1)
    #     # self.processBarView.setWindowFlags(Qt.FramelessWindowHint)
    #     self.processBarView.exec_()
    #     # self.processBarView.hide()

    # 解锁页面
    # def view_unlock(self):
    #     self.pv = 100
    #     self.processBarView.ui.progressBar.setValue(self.pv)
    #     time.sleep(0.3)
    #     self.processBarView.close()
    #     self.pv = 0

    # def processBar_update(self, epoch):
    #     try:
    #         self.pv = (epoch / self.epoch) * 100
    #         # 进度条超过初始值在更新self.pv的值
    #         self.pv = max(self.pv, self.apv)
    #         self.process_value.emit(self.pv)
    #     except Exception as e:
    #         print('processBar_update', e)

    # def processBar_value_set(self, process_value):
    #     self.processBarView.ui.progressBar.setValue(process_value)


    # 判断是否为状态标注算法
    def if_selected_algorithm_avilabel_for_state_annotation_set(self):
        self.cur_alg_train_parameter = self.algorithm_info[self.view.ui.algorithm_tableWidget.currentRow()][17]
        if self.cur_alg_train_parameter == 'waveform':
            return False
        else:
            return True

    # 判断是否为睡眠状态标注数据集,睡眠数据集的定义包含N1,N2,N3,REM(WAKE可有可无)，样本长度为30s
    # def if_selected_set_is_sleep_state_annotation_set(self):
    #     set_description = self.set_info[self.view.ui.trainset_tableWidget.currentRow()][3]
    #     annotation = []
    #     for des in set_description.split('+')[0].split(' '):
    #         annotation.append(des.split('-')[0])
    #     if set_description.split('+')[0].split(' ')[0].split('-')[1] != '30000':
    #         return False
    #     # print(category)
    #     if 'REM' in annotation and 'NREM1' in annotation and 'NREM2' in annotation and 'NREM3' in annotation and len(annotation) == 4:
    #         return True
    #     if 'REM' in annotation and 'NREM1' in annotation and 'NREM2' in annotation and 'NREM3' in annotation and 'WAKE' in annotation and len(annotation) == 5:
    #         return True
    #     return False
    #
    # # 判断是否为睡眠状态标注算法
    # def if_selected_algorithm_avilabel_for_sleep_state_annotation_set(self):
    #     self.cur_alg_train_parameter = self.algorithm_info[self.view.ui.algorithm_tableWidget.currentRow()][3]
    #     self.cur_alg_test_parameter = self.algorithm_info[self.view.ui.algorithm_tableWidget.currentRow()][8]
    #     train_para = self.cur_alg_train_parameter.split(' ')
    #     test_para = self.cur_alg_train_parameter.split(' ')
    #     state_annotation_para_key = 'sleepAnnotationAlgorithm'
    #     for t in train_para:
    #         if t == '':
    #             continue
    #         key, value = t.split('-')
    #         if key == state_annotation_para_key and value == 'True':
    #             return True
    #     return False

    def if_selected_set_is_state_annotation_set(self):
        try:
            set_description = self.set_info[self.view.ui.trainset_tableWidget.currentRow()][3]
            annotation = set_description.split(' ')[0].split('-')[0]
            for typeInfo in self.type_info:
                name = typeInfo[1]
                if name == annotation:
                    # print(typeInfo)
                    category = typeInfo[3]
            # print(category)
            if '状态' in category:
                return True
            return False
        except Exception as e:
            print('if_selected_set_is_state_annotation_set', e)

    def runProcessForTrainRes(self, REPData):
        try:
            if REPData[0] == '0':
                # self.refresh_view_controls_state()
                # self.view_unlock()
                self.view.ui.trainset_tableWidget.setEnabled(True)
                self.view.ui.algorithm_tableWidget.setEnabled(True)
                self.view.ui.trainbtn.setText("训练")
                QMessageBox.information(self.view, '提示', '开启算法进程失败, 请重试', QMessageBox.Yes)
                return
            else:
                # self.view_lock()
                # self.get_progress()
                self.timer = QTimer(self)
                # 每5秒查询一次
                self.timer.start(5000)
                self.timer.timeout.connect(self.get_progress)
                self.progressBar = ProgressBarView(window_title="训练中", maximum=self.epoch, hasStopBtn=False)
                self.progressBar.show()
                # self.processBarView.exec_()
                # self.processBar_value_set(self.apv)
        except Exception as e:
            print('runProcessForTrainRes', e)

    def get_progress(self):
        self.client.getProgress([self.client.tUser[0]])

    def getProgressRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self.view, '提示', '读取进度信息失败', QMessageBox.Yes)
                self.timer.stop()
                self.enable_controls()
                self.view.ui.trainbtn.setText('训练')
            else:
                temp = ""
                if REPData[3]:
                    for i in REPData[3]:
                        temp = str(i)
                        # temp += "\n"
                        self.output_info(temp)
                if REPData[2] == True:
                    epoch = int(REPData[4])
                    # self.processBar_update(epoch)
                    self.progressBar.updateProgressBar(epoch)
                if REPData[2] == False:
                    self.timer.stop()
                    self.progressBar.updateProgressBar(self.epoch)
                    self.progressBar.close()
                    if REPData[5] == False:
                        self.trainOutput.appendPlainText("训练结束")
                        self.trainOutput.appendPlainText('算法运行失败')
                        QMessageBox.information(self.view, '提示', '算法运行失败', QMessageBox.Yes)
                    else:
                        self.trainOutput.appendPlainText("训练结束")
                        self.trainOutput.appendPlainText('算法运行成功')
                        self.cur_classifier_name = REPData[4]
                        self.output_info(
                            '提示:' + '{}模型已训练完成，可通过模型管理功能查看模型信息'.format(self.cur_classifier_name))
                        QMessageBox.information(self.view, '提示', '算法运行成功', QMessageBox.Yes)
                    self.enable_controls()
                    self.view.ui.trainbtn.setText('训练')
        except Exception as e:
            print('getProgressRes', e)

    def show_train_performance(self):
        if self.alg_id == None:
            QMessageBox.information(self.view, '提示', '未选择算法', QMessageBox.Yes)
            return
        if self.set_id == None:
            QMessageBox.information(self.view, '提示', '未选择数据集', QMessageBox.Yes)
            return
        self.client.getTrainPerformance([self.alg_id, self.set_id])

    def getTrainPerformanceRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self.view, '提示', '未保存训练性能', QMessageBox.Yes)
            else:
                performance = REPData[2]
                epoch = performance['epoch']
                accuracy_list = performance['train_acc_list']
                epoch_list = np.linspace(0, epoch, len(accuracy_list))
                plt.plot(epoch_list, accuracy_list, color='red', linestyle='--', linewidth=2)
                plt.xlabel('Epochs')
                plt.ylabel('Accuracy')
                plt.title('Accuracy vs Epochs')
                plt.show()
        except Exception as e:
            print('runProcessForTrainRes', e)

    def matchAlgSetRes(self, REPData):
        try:
            if REPData[0] == '0':
                if REPData[1] == "当前服务器存在正在执行的训练、测试或扫描任务":
                    QMessageBox.information(self.view, '提示', '当前服务器存在正在执行的训练、测试或扫描任务', QMessageBox.Yes)
                else:
                    QMessageBox.information(self.view, '提示', '算法与数据集匹配失败', QMessageBox.Yes)
                self.view.ui.pushButton_15.setEnabled(True)
            else:
                self.custom_msg_box = CustomMessageBox()
                self.timer_2 = QTimer()
                self.timer_2.start(5000)
                self.timer_2.timeout.connect(self.train_cancel)
                result = self.custom_msg_box.exec_()
                if result == QMessageBox.AcceptRole:
                    self.on_btnTrain_clicked()
                else:
                    self.client.train_cancel([self.client.tUser[0]])
        except Exception as e:
            print('matchAlgSetRes', e)

    def refresh_train_btn(self):
        self.view.ui.trainbtn.setEnabled(True)

    def train_cancel(self):
        print('start')
        self.timer_2.stop()
        self.custom_msg_box.close()
        self.view.ui.pushButton_15.setEnabled(True)

    def train_cancelRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self.view, '提示', '撤销训练算法对象失败', QMessageBox.Yes)
        except Exception as e:
            print('train_cancelRes', e)

    def exit(self):
        self.client.getModelInfoResSig.disconnect()
        self.client.get_classifierInfo_by_setId_and_algIdResSig.disconnect()
        self.client.runProcessForTrainResSig.disconnect()
        self.client.matchAlgSetResSig.disconnect()
        self.client.modelInquiryAlgInfoResSig.disconnect()
        self.client.modelAlgInfoPagingResSig.disconnect()
        self.client.modelInquirySetInfoResSig.disconnect()
        self.client.modelSetInfoPagingResSig.disconnect()
        self.client.getTrainPerformanceResSig.disconnect()
        self.client.getProgressResSig.disconnect()
        self.client.train_cancelResSig.disconnect()



class CustomMessageBox(QMessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("提示")
        self.setText("算法与数据集匹配成功,是否开始训练。")

        # 创建自定义按钮并设置名称
        button1 = QPushButton("训练")
        button2 = QPushButton("不训练")

        # 将按钮添加到消息框中
        self.addButton(button1, QMessageBox.AcceptRole)
        self.addButton(button2, QMessageBox.RejectRole)
