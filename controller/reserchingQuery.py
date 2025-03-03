import datetime
import json
import math
from functools import partial

import numpy as np
import time

import threading
import inspect
import ctypes

from PyQt5 import QtWidgets, QtCore
from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.Qt import *

from view.reserchingQuery import ReserchingView
from view.reserchingQuery import SettingView
from view.reserchingQuery import diagListView

from view.manual_form.combo_check_box2 import CheckableComboBox

class reserchingQueryController(QWidget):
    switchToEEG = pyqtSignal(list)

    def __init__(self, appUtil=None, client=None):
        super().__init__()
        self.view = diagListView()
        self.view.page_control_signal.connect(self.rg_paging)

        self.appUtil = appUtil
        self.client = client
        self.User = self.client.tUser

        self.client.rgQ_theme_commitResSig.connect(self.theme_commitRes)
        self.client.rgQ_pagingResSig.connect(self.rg_pagingRes)
        self.client.rgQ_label_commitResSig.connect(self.label_commitRes)
        self.client.rgQ_get_labelsResSig.connect(self.get_labelsRes)
        # self.client.rgQ_get_type_infoResSig.connect(self.get_type_infoRes)
        # self.client.rgQ_openEEGFileResSig.connect(self.openEEGFileRes)
        # self.client.rgQ_load_dataDynamicalResSig.connect(self.load_dataDynamicalRes)
        # self.client.rgQ_update_sampleInfo12ResSig.connect(self.update_sampleInfo12Res)
        # self.client.rgQ_del_sampleInfo13ResSig.connect(self.del_sampleInfo13Res)
        # self.client.rgQ_update_sampleInfo15ResSig.connect(self.update_sample1415Res)
        # self.client.rgQ_init_SampleListResSig.connect(self.init_SampleListRes)
        # self.client.rgQ_del_sample19ResSig.connect(self.del_sample19Res)
        # self.client.rgQ_add_sampleInfo_stateResSig.connect(self.add_sampleInfo_stateRes)
        # self.client.rgQ_update_sampleInfo_stateResSig.connect(self.add_sampleInfo_stateRes)
        # self.client.rgQ_del_sampleInfo_stateResSig.connect(self.del_sampleInfo_stateRes)


        self.check_id = None
        self.file_id = None
        self.measure_date = None
        self.file_name = None


        #self.montages = self.get_montage()
        self.sign_InfoView=None

        self.curPageIndex = 1
        self.pageRows = 12
        self.curPageMax = 1

        self.paitentNamesDict = {}
        self.get_label()


    # 槽对象中的槽函数
    def exit(self):
        # self.stopRolling()
        self.client.rgQ_theme_commitResSig.disconnect()
        self.client.rgQ_pagingResSig.disconnect()
        self.client.rgQ_label_commitResSig.disconnect()
        self.client.rgQ_get_labelsResSig.disconnect()
        # self.client.rgQ_get_type_infoResSig.disconnect()
        # self.client.rgQ_openEEGFileResSig.disconnect()
        # self.client.rgQ_load_dataDynamicalResSig.disconnect()
        # self.client.rgQ_update_sampleInfo12ResSig.disconnect()
        # self.client.rgQ_del_sampleInfo13ResSig.disconnect()
        # self.client.rgQ_update_sampleInfo15ResSig.disconnect()
        # self.client.rgQ_init_SampleListResSig.disconnect()
        # self.client.rgQ_del_sample19ResSig.disconnect()
        # self.client.rgQ_add_sampleInfo_stateResSig.disconnect()
        # self.client.rgQ_update_sampleInfo_stateResSig.disconnect()
        # self.client.rgQ_del_sampleInfo_stateResSig.disconnect()

    def rg_paging(self,page_to):
       if page_to[0] == "home":
           self.curPageIndex=1
           self.view.ui.curPage.setText(str(self.curPageIndex))
       elif page_to[0] == "pre":
           if self.curPageIndex <= 1:
               return
           self.curPageIndex=self.curPageIndex-1
           self.view.ui.curPage.setText(str(self.curPageIndex))
       elif page_to[0] == "next":
           self.curPageIndex=self.curPageIndex+1
           self.view.ui.curPage.setText(str(self.curPageIndex))
       elif page_to[0] == "final":
           self.curPageIndex = self.curPageMax
           self.view.ui.curPage.setText(str(self.curPageIndex))
       elif page_to[0] == "confirm":
           pp=self.view.ui.skipPage.text()
           if int(pp) > self.curPageMax or int(pp) <= 0:
               QMessageBox.information(self, "查询", f'页数：1 至 {self.curPageMax}', QMessageBox.Yes)
               self.view.ui.skipPage.setText(str(self.curPageMax))
               return False
           self.curPageIndex = int(pp)
           self.view.ui.curPage.setText(str(self.curPageIndex))
       elif page_to[0] == "query":
           self.curPageIndex = 1
           self.view.ui.curPage.setText(str(self.curPageIndex))
       theme_name = self.view.ui.theme_lineEdit.text()
       theme_state = self.view.ui.comboBox.currentText()
       task_state = self.view.ui.comboBox2.currentText()
       self.view.setDisabled(True)
       msg=[self.client.tUser[0], self.curPageIndex, self.pageRows,page_to[0],theme_name,theme_state,task_state]
       self.client.rgQ_paging(msg)

    def rg_pagingRes(self, REPData):
        self.view.setEnabled(True)
        if REPData[0] == '0':
            QMessageBox.information(self, "查询", REPData[2], QMessageBox.Yes)
            return False
        self.diags_viewInfo = REPData[2]

        self.paitentNamesDict = {}
        if REPData[3] is not None:
          for p in REPData[3]:
            self.paitentNamesDict.setdefault(p[0], p[1])
        self.userNamesDict = {}
        if REPData[8] is not None:
            for p in REPData[8]:
                self.userNamesDict.setdefault(p[0], p[1])
        self.themeDict = {}
        if REPData[9] is not None:
            for p in REPData[9]:
                self.themeDict.setdefault(p[0], p[1])

        self.curPageIndex = REPData[4]
        if REPData[5]!=0:
            self.curPageMax = REPData[5]

        self.view.show()
        self.view.init_table(self.diags_viewInfo, self.userNamesDict, self.paitentNamesDict, self.themeDict,
                                     self.on_clicked_manual_query, self.on_clicked_theme_commit, self.on_clicked_label_commit, self.curPageIndex,
                                     self.curPageMax)

    # 获取提取取诊断信息
    # 向客户端发送提取取诊断信息的请求
    def get_label(self):
        self.theme_id = None
        self.check_id = None
        self.file_id = None
        self.uid = None
        self.measure_date = None
        self.file_name = None
        self.page = ['file_name']
        msg=[self.client.tUser[0], self.curPageIndex, self.pageRows]
        self.client.rgQ_get_labels(msg)

    # 处理客户端传回的提取取诊断信息
    def get_labelsRes(self, REPData):

        if REPData[0] == '0':
            QMessageBox.information(self, "提取未标注信息不成功", REPData[2], QMessageBox.Yes)
            return False

        self.diags_viewInfo = REPData[2]

        self.paitentNamesDict = {}
        if REPData[3] is not None:
          for p in REPData[3]:
            self.paitentNamesDict.setdefault(p[0], p[1])
        self.userNamesDict = {}
        if REPData[4] is not None:
            for p in REPData[4]:
                self.userNamesDict.setdefault(p[0], p[1])
        self.themeDict = {}
        if REPData[5] is not None:
            for p in REPData[5]:
                self.themeDict.setdefault(p[0], p[1])

        self.curPageIndex = REPData[6]
        if REPData[7]!=0:
            self.curPageMax = REPData[7]

        self.check_id = None
        self.file_id = None
        self.measure_date = None
        self.file_name = None

        self.view.show()
        self.view.init_table(self.diags_viewInfo, self.userNamesDict, self.paitentNamesDict, self.themeDict,
                                     self.on_clicked_manual_query, self.on_clicked_theme_commit, self.on_clicked_label_commit,
                                     self.curPageIndex, self.curPageMax)


    def on_clicked_label_commit(self, diags_viewInfo, stats):
        reply = QMessageBox.information(self, '提示', f'设置当前任务{stats},确定吗?', QMessageBox.Yes | QMessageBox.No)
        if  reply == 16384:
            try:
                self.theme_id = diags_viewInfo[0]
                self.check_id = diags_viewInfo[7]
                self.uid = diags_viewInfo[12]
                self.file_id = diags_viewInfo[11]
                msg = [self.theme_id, self.check_id,self.file_id, self.uid, stats]
                self.client.rgQ_label_commit(msg)
            except:
                QMessageBox.information(self, '提示', '任务设置，无效')

    def label_commitRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "任务设置", REPData[2], QMessageBox.Yes)
            return
        QMessageBox.information(self, "任务设置，操作成功", REPData[2], QMessageBox.Yes)
        self.page = ['file_name']
        self.get_label()

    def on_clicked_theme_commit(self, diags_viewInfo,stats):
        reply = QMessageBox.information(self, '提示', f'设置当前主题为{stats},确定吗?', QMessageBox.Yes | QMessageBox.No)
        if reply == 16384:
            try:
                msg = [diags_viewInfo[0], stats]
                self.client.rgQ_theme_commit(msg)
                self.view.setDisabled(True)
                #self.view.show()
            except:
                QMessageBox.information(self, '提示', '无效')


    def theme_commitRes(self, REPData):
        self.view.setEnabled(True)
        if REPData[0] == '0':
            QMessageBox.information(self, "主题设置", REPData[2], QMessageBox.Yes)
            return False
        QMessageBox.information(self, "主题设置", REPData[2], QMessageBox.Yes)
        self.page = ['file_name']
        self.get_label()

    def on_clicked_manual_query(self, diags_viewInfo, patient_name):
        self.theme_id = diags_viewInfo[0]
        self.theme_name = diags_viewInfo[1]
        self.check_id = diags_viewInfo[7]
        self.check_num = diags_viewInfo[8]
        self.patient_id = diags_viewInfo[9]
        self.task_state = diags_viewInfo[3]
        self.uid = diags_viewInfo[12]

        self.measure_date = diags_viewInfo[10]

        self.patient_name = patient_name

        self.file_name = '{:>03}.bdf'.format(str(diags_viewInfo[11]))
        self.file_id = diags_viewInfo[11]
        self.page = ['file_name']
        try:
            self.switchToEEG.emit([self.file_id, self.file_name, self.check_id, self.patient_id, self.measure_date,
                                   ['reserchingQueryController', ''],
                                   "reslab", self.uid, True, False, self.theme_id])
        except:
            QMessageBox.information(self, '提示', '当前文件无效')