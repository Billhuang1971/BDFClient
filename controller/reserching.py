import datetime
import json
import math
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

from view.reserching import ReserchingView
from view.reserching import SettingView

from view.reserching import diagListView

from view.manual_form.combo_check_box2 import CheckableComboBox

class reserchingController(QWidget):
    switchToEEG = pyqtSignal(list)
    def __init__(self, appUtil=None, Widget=None, client=None, mainMenubar=None, mainLayout=None):
        super().__init__()
        self.view = diagListView() #首页ui
        self.view.page_control_signal.connect(self.rg_paging)
        self.mainLayout = mainLayout
        self.mainMenubar = mainMenubar
        self.client = client
        self.User = self.client.tUser
        self.client.rg_pagingResSig.connect(self.rg_pagingRes)
        self.client.rg_label_commitResSig.connect(self.label_commitRes)
        self.client.rg_get_notlabelsResSig.connect(self.get_notlabelsRes)
        self.client.rg_get_type_infoResSig.connect(self.get_type_infoRes)
        self.client.changestateResSig.connect(self.changestateRes)
        self.check_id = None
        self.file_id = None
        self.measure_date = None
        self.file_name = None
        # maincontroller提供的一个label，用于显示相关参数信息
        self.widget_from_main = Widget


        #self.montages = self.get_montage()
        self.sign_InfoView=None
        msg = [self.User[0],self.User[2]]
        self.client.rg_get_type_info(msg)

        self.curPageIndex = 1
        self.pageRows = 12
        self.curPageMax = 1

        self.initEEGfile()

        self.paitentNamesDict = {}
        self.exclude_av = ['Ldelt1', 'Ldelt2', 'Rdelt1', 'Rdelt2', 'A1', 'A2', 'M1', 'M2', 'LOC', 'ROC',
                           'CHIN1', 'CHIN2', 'ECGL', 'ECGR', 'LAT1', 'LAT2', 'RAT1', 'RAT2',
                           'CHEST', 'ABD', 'FLOW', 'SNORE', 'DIF5', 'DIF6']
    def initEEGfile(self):
        self.uping = 0
        self.downing = 0
        self.sensitivity = 10
        self.duration = None
        self.cursor = None

        self.pick_labels = []
        self.pick_channel = ''
        self.pick_first = None
        self.pick_second = None
        self.pick_seg = None
        self.pick_sample_color = None
        self.pick_sample = None
        self.pick_events = []

        self.status_annotate = False
        self.state_left = None
        self.state_right = None
        self.state_picked = None
        self.cur_sample_index = 0

        self.patient_id = None
        self.measure_date = None
        self.file_name = None

        self.start_time = None
        self.end_time = None
        self.n_times = None

        self.patientInfo = None
        self.sample_list = None
        self.status_info = None
        self.p_sample = ''
        self.p_cur_sample = ''
        self.p_type = ''

        self.begin = 0
        self.index = 0
        self.start_t = 0
        self.end_t = 0
        self.idx = ''
        self.type_info = ""
        self.user_info = ""
        self.diags_viewInfo = None
        self.userNamesDict = {}


    def get_type_infoRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "提取类型、用户信息不成功", REPData[2], QMessageBox.Yes)
            return False
        self.type_info = REPData[1]#类型信息
        self.user_info = REPData[2]#用户信息
        self.montages = REPData[3]#通道信息

        self.type_filter = [x[1] for x in self.type_info]#拿类型名字
        self.user_filter = [x[3] for x in self.user_info]#拿用户名字

        self.init_prentryView()
    # 槽对象中的槽函数
    def exit(self):
        self.client.rg_pagingResSig.disconnect()
        self.client.rg_label_commitResSig.disconnect()
        self.client.rg_get_notlabelsResSig.disconnect()
        self.client.rg_get_type_infoResSig.disconnect()
        self.client.changestateResSig.disconnect()


    # 初始化信息选择界面（选择病人-测量日期-文件）
    def init_prentryView(self):
        self.start_time = None
        self.end_time = None
        self.n_times = None
        self.patientInfo = ''
        self.sample_list = ''
        self.end = 0

        self.get_notlabel() #获取进入页面信息
        #self.diagListView.show()
        self.mainLayout.addWidget(self.view)

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
       self.client.rg_paging(msg)

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
        self.userNamesDict.setdefault(self.client.tUser[0], self.client.tUser[2])
        self.curPageIndex = REPData[4]
        if REPData[5]!=0:
            self.curPageMax = REPData[5]

        self.view.show()
        self.view.init_table(self.diags_viewInfo, self.userNamesDict, self.paitentNamesDict,
                                     self.on_clicked_manual_query, self.on_clicked_submit,self.curPageIndex,
                                     self.curPageMax)

    # 获取提取取诊断信息
    # 向客户端发送提取取诊断信息的请求
    def get_notlabel(self):#留

        self.theme_id = None
        self.check_id = None
        self.file_id = None
        self.uid = None
        self.measure_date = None
        self.file_name = None
        self.page = ['file_name']
        msg=[self.client.tUser[0],self.curPageIndex,self.pageRows]
        self.client.rg_get_notlabels(msg)

    # 处理客户端传回的提取取诊断信息
    def get_notlabelsRes(self, REPData):#留

        if REPData[0] == '0':
            QMessageBox.information(self, "提取未标注信息不成功", REPData[2], QMessageBox.Yes)
            return False

        self.diags_viewInfo = REPData[2]

        self.paitentNamesDict = {}
        if REPData[3] is not None:
          for p in REPData[3]:
            self.paitentNamesDict.setdefault(p[0], p[1])
        self.userNamesDict = {}
        self.userNamesDict.setdefault(self.client.tUser[0],self.client.tUser[2])

        self.curPageIndex = REPData[4]
        if REPData[5]!=0:
            self.curPageMax = REPData[5]
        self.check_id = None
        self.file_id = None
        self.measure_date = None
        self.file_name = None

        self.view.show()
        self.view.init_table(self.diags_viewInfo, self.userNamesDict,self.paitentNamesDict,
                                     self.on_clicked_manual_query, self.on_clicked_submit,self.curPageIndex,self.curPageMax,)


    def on_clicked_manual_query(self, diags_viewInfo, patient_name):
        self.theme_id = None
        self.check_id = None
        self.file_id = None
        self.measure_date = None
        self.file_name = None
        self.theme_id = diags_viewInfo[0]
        self.theme_name = diags_viewInfo[1]
        self.check_id = diags_viewInfo[7]
        self.check_num = diags_viewInfo[8]
        self.patient_id = diags_viewInfo[9]
        self.task_state = diags_viewInfo[3]

        self.uid = self.client.tUser[0]
        self.measure_date = diags_viewInfo[10]
        self.patient_name = patient_name

        self.file_name = '{:>03}.bdf'.format(str(diags_viewInfo[11]))
        self.file_id = diags_viewInfo[11]
        self.page = ['file_name']
        try:
            msg = [self.check_id, self.file_id, self.patient_id, self.theme_id,self.client.tUser[0],diags_viewInfo[3]]#标注状态 diags_viewInfo[3]
            self.client.changestate(msg)
        except:
            QMessageBox.information(self, '提示', '当前文件无效')
            self.mainMenubar.setEnabled(True)

    #完成标注任务
    def on_clicked_submit(self,diags_viewInfo, patient_name):
        theme_id = diags_viewInfo[0]
        check_id = diags_viewInfo[7]
        file_id = diags_viewInfo[11]
        uid = self.client.tUser[0]
        msg=[theme_id,check_id,file_id,uid]
        self.client.rg_label_commit(msg)
    def changestateRes(self,REPdata):
        self.switchToEEG.emit([self.file_id, self.file_name, self.check_id, self.patient_id, self.measure_date,
                               ['reserchingController', ''], "reslab", self.client.tUser[0], True, True, self.theme_id])
    def label_commitRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "完成标注", REPData[2], QMessageBox.Yes)
            return False
        QMessageBox.information(self, "完成标注，操作成功", REPData[2], QMessageBox.Yes)
        self.page = ['file_name']
        self.get_notlabel()
        while self.mainLayout.count() > 1:
             witem = self.mainLayout.itemAt(self.mainLayout.count() - 1)
             witem.widget().hide()
             self.mainLayout.removeItem(witem)
        self.mainLayout.addWidget(self.view)




