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

from view.diagTrainng import DiagTrainingView
from view.diagTrainng import SettingView

from view.diagTrainng import DiagListView

from view.manual_form.combo_check_box2 import CheckableComboBox

class diagTrainingController(QWidget):
    switchToEEG = pyqtSignal(list)

    def __init__(self, appUtil=None, client=None):
        super().__init__()
        self.view = DiagListView()
        self.class_id = None
        self.study_start_time = None
        self.appUtil = appUtil
        self.client = client
        self.User = self.client.tUser

        self.client.dl_get_studyInfoResSig.connect(self.dl_get_studyInfoRes)
        self.client.dl_get_contentsResSig.connect(self.dl_get_contentsRes)
        self.client.dl_get_diagResSig.connect(self.dl_get_diagRes)

        self.curPageIndex = 1
        self.pageRows = 12
        self.curPageMax = 1
        self.userNamesDict = {}
        self.paitentNamesDict = {}
        self.dl_get_contents()


    # 槽对象中的槽函数
    def exit(self):
        self.client.dl_get_studyInfoResSig.disconnect()
        self.client.dl_get_contentsResSig.disconnect()
        self.client.dl_get_diagResSig.disconnect()


    def study_end(self):
        if self.class_id is not None and self.study_start_time is not None:
              msg = [self.class_id,  self.client.tUser[0], self.study_start_time]
              self.client.dl_study_end(msg)



    # 客户端发送提取取学习诊断信息的请求
    def dl_get_contents(self):
        self.check_id = None
        self.measure_date = None
        self.file_name = None
        self.file_id = None
        self.page = ['file_name']
        msg=[self.client.tUser[0]]
        self.client.dl_get_contents(msg)

    # 处理客户端传回的提取取学习诊断信息
    def dl_get_contentsRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "提取学习诊断信息不成功", REPData[2], QMessageBox.Yes)
            return False

        self.diags_viewInfo = REPData[2]
        self.userNamesDict = {}
        self.paitentNamesDict = {}
        self.student_stateDict={}
        if REPData[3] is not None:
          for u in REPData[3]:
            self.userNamesDict.setdefault(u[0], u[1])
        if REPData[4] is not None:
          for p in REPData[4]:
            self.paitentNamesDict.setdefault(p[0], p[1])
        if REPData[5] is not None:
          for st in REPData[5]:
            self.student_stateDict.setdefault(st[0], st[2])

        self.view.show()
        self.view.init_table(self.diags_viewInfo, self.userNamesDict, self.student_stateDict, self.paitentNamesDict,
                              self.on_clicked_manual_query, self.on_clicked_diag_query, self.on_clicked_learn_query)

    def on_clicked_manual_query(self, diags_viewInfo, patient_name):
        self.class_id = diags_viewInfo[0]
        self.study_start_time = None
        self.check_id = diags_viewInfo[6]
        self.patient_id = diags_viewInfo[8]
        self.measure_date = diags_viewInfo[9]
        self.patient_name = patient_name

        self.file_name ='{:>03}.bdf'.format(str(diags_viewInfo[10]))
        self.file_id = diags_viewInfo[10]
        self.content_uid = diags_viewInfo[11]
        self.page = ['file_name']

        self.switchToEEG.emit([self.file_id, self.file_name, self.check_id, self.patient_id, self.measure_date,
                               ['diagTrainingController', '', self.class_id], "sample_info", diags_viewInfo[11], False, False, None])


    def on_clicked_diag_query(self, diags_viewInfo, patient_name):
        check_id = diags_viewInfo[6]
        self.uid = diags_viewInfo[11]
        msg = [check_id]
        self.client.dl_get_diag(msg)

    def dl_get_diagRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "提取诊断信息不成功", REPData[2], QMessageBox.Yes)
            return False

        diags = REPData[2]
        ud = REPData[3]
        pd = REPData[4]
        userNamesDict = {}
        paitentNamesDict = {}
        if ud is not None:
            for u in ud:
                userNamesDict.setdefault(u[0], u[1])
        if pd is not None:
            for p in pd:
                paitentNamesDict.setdefault(p[0], p[1])

        msg = ""
        lstate = {'notDiagnosed': '未诊断', 'diagnosed': '已诊断', 'refused': '拒绝诊断'}

        for d in diags:
            if d[2] == self.uid:
                msg += f"检查单号:{d[-2]},病人：{paitentNamesDict.get(d[0])},测量时间:{d[1]},诊断医生：{userNamesDict.get(d[2])},诊断时间：{d[4]},状态：{lstate[d[3]]}\n"
                if d[3] == 'diagnosed':
                    msg += f"alpha波活动:{d[5]}\n"
                    msg += f"慢波活动:{d[6]}\n"
                    msg += f"快波活动:{d[7]}\n"
                    msg += f"波幅特点:{d[8]}\n"
                    msg += f"睁闭眼:{d[9]}\n"
                    msg += f"过度换气:{d[10]}\n"
                    msg += f"睡眠:{d[11]}\n"
                    msg += f"异常脑波:{d[12]}\n"
                    msg += f"发作期:{d[13]}\n"
                    msg += f"诊断总结:{d[14]}\n"
                else:
                    msg += "状态：{lstate[d[3]]}\n"
                break
        QMessageBox.information(self, "诊断信息", msg, QMessageBox.Yes)

    def on_clicked_learn_query(self, diags_viewInfo):
        class_id = diags_viewInfo[0]
        msg = [class_id, self.client.tUser[0]]
        self.client.dl_get_studyInfo(msg)

    def dl_get_studyInfoRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, '提示', REPData[2])
            return False
        studyInfo = REPData[2]

        msg = "我的学习记录(时长单位秒)：\n"
        lentim = 0

        for d in studyInfo:
            delta = (d[3] - d[2]).total_seconds()
            lentim += delta
            msg += f"{d[2]}-{d[3]}   时长:%.0f \n" % (delta)
        lentim = lentim / 60.0
        msg += f"[合计时长]  %.0f 分钟\n" % (lentim)
        QMessageBox.information(self, "我的学习记录信息", msg, QMessageBox.Yes)