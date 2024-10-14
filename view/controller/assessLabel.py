import os
import mne
import math
import numpy as np
import time,datetime
import bisect
import threading
import inspect
import ctypes
import pypinyin
from PyQt5 import QtCore

from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5 import QtCore
from pyqt5_plugins.examplebutton import QtWidgets

from view.assessLabel import AssessLabelView
from view.assessLabel import SettingView
from view.assessLabel import PrentryView
from view.manual_form.combo_check_box2 import CheckableComboBox


class assessLabelController(QWidget):
    is_reload_controller = QtCore.pyqtSignal(str)

    def __init__(self, appUtil=None, Widget=None, client=None, mainMenubar=None):
        super().__init__()
        self.view = AssessLabelView()
        self.client = client
        self.appUtil = appUtil
        self.User = client.tUser
        # maincontroller提供的一个label，用于显示相关参数信息
        self.widget_from_main = Widget
        self.mainMenubar = mainMenubar
        self.view.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.ui.tableWidget.resizeColumnsToContents()
        self.view.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view.ui.tableWidget.clicked.connect(self.on_tableWidgetList_itemClicked)
        self.view.ui.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.ui.tableWidget.customContextMenuRequested.connect(self.sampleList_menu)
        self.view.ui.btnUp.clicked.connect(self.on_btnUp_clicked)
        self.view.ui.btnDown.clicked.connect(self.on_btnDown_clicked)
        self.view.ui.btnUping.clicked.connect(self.on_btnUping_clicked)
        self.view.ui.btnDowning.clicked.connect(self.on_btnDowning_clicked)
        self.view.ui.btnBegin.clicked.connect(self.on_btnBegin_clicked)
        self.view.ui.btnEnd.clicked.connect(self.on_btnEnd_clicked)
        self.view.ui.editTime.timeChanged.connect(self.timeChange)
        self.view.ui.btnRuler.clicked.connect(self.on_btnRuler_clicked)
        self.view.ui.btnSetting.clicked.connect(self.on_btnSetting_clicked)
        self.view.ui.btnPrevSample.clicked.connect(self.on_btnPrevSample_clicked)
        self.view.ui.btnNextSample.clicked.connect(self.on_btnNextSample_clicked)
        self.view.ui.btnStateAnnotate.clicked.connect(self.btnStateAnnotate_clicked)
        self.view.ui.btnShowInfo.clicked.connect(self.on_btnShowInfo_clicked)
        self.root_path = self.appUtil.root_path
        self.curPageIndex = 1
        self.pageRows = 12
        self.curPageMax = 1
        self.classifier_key_word = None
        self.classifier_key_value = None
        self.isSearch = False
        self.searchPage = 1
        self.searchPageMax = 1
        self.search_init_info = []
        self.init_info = []
        self.file_info = []
        self.pre_info = []
        # 计算平均时排除
        self.exclude_av = ['Ldelt1', 'Ldelt2', 'Rdelt1', 'Rdelt2', 'A1', 'A2', 'M1', 'M2', 'LOC', 'ROC',
                           'CHIN1', 'CHIN2', 'ECGL', 'ECGR', 'LAT1', 'LAT2', 'RAT1', 'RAT2',
                           'CHEST', 'ABD', 'FLOW', 'SNORE', 'DIF5', 'DIF6']

        # self.set_canvas()
        # self.set_contextmenu()
        # self.init_prentryView()
        self.initEEGfile()
        self.client.getAssessInfoResSig.connect(self.getAssessInfoRes)
        self.client.getModelIdNameResSig.connect(self.getModelIdNameRes)
        self.client.assessClassifierInfoPagingResSig.connect(self.assessClassifierInfoPagingRes)
        self.client.getAssessFileInfoResSig.connect(self.getAssessFileInfoRes)
        self.client.assessOpenEEGFileResSig.connect(self.assessOpenEEGFileRes)
        self.client.assess_load_dataDynamicalResSig.connect(self.load_dataDynamicalRes)
        self.client.update_labelListInfoResSig.connect(self.update_labelListInfoRes)
        self.client.update_labelListInfo12ResSig.connect(self.update_labelListInfo12Res)
        self.client.del_labelListInfoResSig.connect(self.del_labelListInfoRes)
        self.client.del_labelListInfo15ResSig.connect(self.del_labelListInfo15Res)
        self.client.getAssessInfo([self.User[0], self.User[2]])


    def initEEGfile(self):
        try:
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
            self.type_info = []
            self.user_info = []
            self.model_name = None
        except Exception as e:
            print('initEEGfile', e)

    def getAssessInfoRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "提取类型、用户信息不成功", REPData[2], QMessageBox.Yes)
                return False
            self.type_info = REPData[1]
            self.user_info = REPData[2]
            self.montages = REPData[3]
            self.type_filter = [x[1] for x in self.type_info]
            self.type_name_dic = {}
            for i in self.type_info:
                self.type_name_dic[i[0]] = i[1]
            self.user_filter = [x[3] for x in self.user_info]
            self.set_canvas()
            self.set_contextmenu()
            self.init_prentryView()
        except Exception as e:
            print('getAssessInfoRes', e)

    # 初始化信息选择界面（选择分类器-文件）
    def init_prentryView(self):
        try:
            self.model_id = None
            self.file_name = None

            self.prentryView = PrentryView()
            self.prentryView.setAttribute(Qt.WA_DeleteOnClose)
            self.prentryView.setWindowTitle("信息选择")
            self.prentryView.setWindowModality(Qt.ApplicationModal)
            # self.prentryView.show()
            # self.prentryView.ui.btnConfirm.setEnabled(False)
            # self.prentryView.ui.btnReturn.setEnabled(False)
            self.prentryView.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.prentryView.ui.tableWidget.resizeRowsToContents()
            self.prentryView.ui.tableWidget.resizeColumnsToContents()
            self.prentryView.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.prentryView.ui.tableWidget.clicked.connect(self.on_tableWidget_itemClicked)
            self.prentryView.ui.btnConfirm.clicked.connect(self.on_btnConfirm_clicked)
            self.prentryView.ui.btnReturn.clicked.connect(self.on_btnReturn_clicked)
            self.page = ['model_name']
            self.client.getModelIdName([self.curPageIndex, self.pageRows, False])
            # self.init_tableWidget()
        except Exception as e:
            print('init_prentryView', e)

    def getModelIdNameRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.init_info.clear()
                self.init_info = REPData[2]
                self.curPageMax = REPData[3]
                if self.curPageMax <= 0:
                    self.curPageMax = 1
                reset = REPData[4]
                itemName = ['分类器名称']
                if reset:
                    self.isSearch = False
                    self.search_init_info.clear()
                    self.prentryView.ui.lineEdit_2.clear()
                    self.init_tableWidget(self.search_init_info, itemName)
                    self.prentryView.ui.label_2.setText("共" + str(self.searchPageMax) + "页")
                    self.prentryView.ui.label.setText(str(self.searchPage))
                    QMessageBox.information(self, '提示', '刷新页面成功', QMessageBox.Ok)
                else:
                    self.init_tableWidget(self.init_info, itemName)
                    self.prentryView.ui.label_2.setText("共" + str(self.curPageMax) + "页")
                    self.prentryView.ui.label.setText(str(self.curPageIndex))
                    self.prentryView.page_control_signal.connect(self.page_controller)
                    self.prentryView.ui.btnConfirm.setVisible(False)
                    self.prentryView.ui.btnReturn.setVisible(False)
                    self.prentryView.show()
            else:
                QMessageBox.information(self, '提示', '获取评估标注界面信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('getClearLabelInfoRes', e)

    def page_controller(self, signal):
        try:
            if "home" == signal[0]:
                if self.isSearch == False:
                    if self.curPageIndex == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.curPageIndex = 1
                    self.view.ui.label.setText(str(self.curPageIndex))
                else:
                    if self.searchPage == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.searchPage = 1
                    self.view.ui.label.setText(str(self.searchPage))
            elif "pre" == signal[0]:
                if self.isSearch == False:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.curPageIndex <= 1:
                        return
                    self.curPageIndex = self.curPageIndex - 1
                    self.view.ui.label.setText(str(self.curPageIndex))
                else:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.searchPage <= 1:
                        return
                    self.searchPage = self.searchPage - 1
                    self.view.ui.label.setText(str(self.searchPage))
            elif "next" == signal[0]:
                if self.isSearch == False:
                    if self.curPageMax == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.curPageIndex = self.curPageIndex + 1
                    self.view.ui.label.setText(str(self.curPageIndex))
                else:
                    if self.searchPageMax == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.searchPage = self.searchPage + 1
                    self.view.ui.label.setText(str(self.searchPage))
            elif "final" == signal[0]:
                if self.isSearch == False:
                    if self.curPageIndex == self.curPageMax:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.curPageIndex = self.curPageMax
                    self.view.ui.label.setText(str(self.curPageMax))
                else:
                    if self.searchPage == self.searchPageMax:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.searchPage = self.searchPageMax
                    self.view.ui.label.setText(str(self.searchPageMax))
            elif "confirm" == signal[0]:
                if self.isSearch == False:
                    if self.curPageIndex == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.curPageMax < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.curPageIndex = int(signal[1])
                    self.view.ui.label.setText(signal[1])
                else:
                    if self.searchPage == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.searchPageMax < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.searchPage = int(signal[1])
                    self.view.ui.label.setText(signal[1])
            if self.isSearch == False:
                msg = [self.curPageIndex, self.pageRows, signal[0], self.isSearch]
            else:
                msg = [self.searchPage, self.pageRows, signal[0], self.isSearch, self.key_word, self.key_value]
            self.client.assessClassifierInfoPaging(msg)
        except Exception as e:
            print('page_controller', e)

    def assessClassifierInfoPagingRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "提示", "跳转页面失败", QMessageBox.Yes)
                return
            else:
                isSearch = REPData[3]
                itemName = ['分类器名称']
                if isSearch:
                    self.search_init_info.clear()
                    self.search_init_info = REPData[2]
                    self.init_tableWidget(self.search_init_info, itemName)
                    self.prentryView.ui.label_2.setText("共" + str(self.searchPageMax) + "页")
                    self.prentryView.ui.label.setText(str(self.searchPage))
                    QMessageBox.information(self, "提示", "跳转页面成功", QMessageBox.Yes)
                else:
                    self.init_info.clear()
                    self.init_info = REPData[2]
                    self.init_tableWidget(self.init_info, itemName)
                    self.prentryView.ui.label_2.setText("共" + str(self.curPageMax) + "页")
                    self.prentryView.ui.label.setText(str(self.curPageIndex))
                    QMessageBox.information(self, "提示", "跳转页面成功", QMessageBox.Yes)
        except Exception as e:
            print('assessClassifierInfoPagingRes', e)



    # 初始化prentryView中表格（模型/文件）
    def init_tableWidget(self, pre_info, itemName):
        try:
            col_num = len(itemName)
            self.prentryView.ui.tableWidget.setColumnCount(col_num)
            self.prentryView.ui.tableWidget.setHorizontalHeaderLabels(itemName)
            # for i in range(col_num):
            #     header_item = QTableWidgetItem(itemName[i])
            #     font = header_item.font()
            #     font.setPointSize(12)
            #     header_item.setFont(font)
            #     header_item.setForeground(QBrush(Qt.black))
            #     self.prentryView.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
            self.prentryView.ui.tableWidget.horizontalHeader().setHighlightSections(False)
            self.prentryView.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            row_num = len(pre_info)
            self.prentryView.ui.tableWidget.setRowCount(row_num)
            if itemName == ['分类器名称']:
                for r in range(row_num):
                    item = QTableWidgetItem(str(pre_info[r][1]))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(10)
                    item.setFont(font)
                    self.prentryView.ui.tableWidget.setItem(r, 0, item)
            else:
                for r in range(row_num):
                    for c in range(col_num):
                        if c == 0:
                            item = QTableWidgetItem(str(pre_info[r][1]))
                            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = item.font()
                            font.setPointSize(10)
                            item.setFont(font)
                        elif c == 1:
                            item = QTableWidgetItem(str(pre_info[r][3]))
                            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = item.font()
                            font.setPointSize(10)
                            item.setFont(font)
                        elif c == 2:
                            item = QTableWidgetItem(str(pre_info[r][2]))
                            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = item.font()
                            font.setPointSize(10)
                            item.setFont(font)
                        elif c == 3:
                            item = QTableWidgetItem(str(pre_info[r][0]))
                            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = item.font()
                            font.setPointSize(10)
                            item.setFont(font)
                        self.prentryView.ui.tableWidget.setItem(r, c, item)
            self.prentryView.ui.tableWidget.verticalHeader().setVisible(False)
        except Exception as e:
            print('init_tableWidget', e)

    # 响应prentryView单击表格事件，选择模型/文件名
    def on_tableWidget_itemClicked(self):
        try:
            row = self.prentryView.ui.tableWidget.currentRow()
            if self.model_id == None:
                self.model_id = self.init_info[row][0]
                self.model_name = self.init_info[row][1]
                self.client.getAssessFileInfo([self.model_id])
            else:
                self.check_id = self.file_info[row][1]
                self.file_id = self.file_info[row][2]
                self.patient_id = self.pre_info[row][4]
                self.measure_date = self.pre_info[row][2]
                self.prentryView.ui.btnConfirm.setEnabled(True)
        except Exception as e:
            print('on_tableWidget_itemClicked', e)

    def getAssessFileInfoRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "提示", "获取标注文件列表失败", QMessageBox.Yes)
                return
            else:
                self.pre_info = REPData[2]
                self.file_info.clear()
                self.file_info = REPData[3]
                itemName = ['病人名称', '检查单号', '检查日期', '文件名称']
                self.init_tableWidget(self.pre_info, itemName)
                self.prentryView.ui.pushButton.setVisible(False)
                self.prentryView.ui.pushButton_2.setVisible(False)
                self.prentryView.ui.pushButton_3.setVisible(False)
                self.prentryView.ui.pushButton_4.setVisible(False)
                self.prentryView.ui.pushButton_5.setVisible(False)
                self.prentryView.ui.label_2.setVisible(False)
                self.prentryView.ui.label.setVisible(False)
                self.prentryView.ui.lineEdit.setVisible(False)
                self.prentryView.ui.lineEdit_2.setVisible(False)
                self.prentryView.ui.comboBox.setVisible(False)
                self.prentryView.ui.pushButton_6.setVisible(False)
                self.prentryView.ui.pushButton_7.setVisible(False)
                self.prentryView.ui.btnReturn.setVisible(True)
                self.prentryView.ui.btnConfirm.setVisible(True)
                self.prentryView.ui.btnConfirm.setEnabled(False)
        except Exception as e:
            print('getAssessFileInfoRes', e)

    # prentryView选择文件后，点击确认按钮载入数据显示图像
    # def _on_btnConfirm_clicked(self):
    #     self.patient_id = int(self.file_name.split('_')[0])
    #     self.measure_date = self.file_name.split('_')[1]
    #     self.patient_name = self.DbUtil.get_patientInfo('patient_id',self.patient_id)[0][1]
    #     patient_name = ''.join(pypinyin.lazy_pinyin(self.patient_name, pypinyin.Style.NORMAL))
    #     try:
    #         name = self.file_name[: self.file_name.index('.')]
    #         package = name.split('_')[0] + '_' + patient_name
    #         path = os.path.join(self.root_path, 'data', 'formated_data', package, self.file_name)
    #         self.raw = mne.io.read_raw_edf(path)
    #     except:
    #         QMessageBox.information(self, '提示', '当前文件无效')
    #         return
    #     self.channels = self.raw.info['ch_names']
    #     self.index_channels = mne.pick_channels(self.channels, include=[])
    #     self.sampling_rate = int(self.raw.info['sfreq'])
    #     self.duration = int(self.raw.n_times // self.sampling_rate)
    #     meas_date = self.raw.info['meas_date']
    #     if isinstance(meas_date, tuple):
    #         meas_date = datetime.datetime.fromtimestamp(meas_date[0])
    #     start_time = meas_date.strftime('%H:%M:%S')
    #     end_time = meas_date + datetime.timedelta(seconds=self.duration)
    #     end_time = end_time.strftime('%H:%M:%S')
    #
    #     self.montage = 'Default'
    #     self.mont_idx = 0
    #     self.begin = 0
    #     self.index = 0
    #     self.load_dataDynamical()
    #     self.prentryView.close()
    #     patient = self.DbUtil.get_patientInfo('patient_id', self.patient_id)
    #     model_name = self.DbUtil.get_modelIdName('classifier_id', self.model_id)[0][1]
    #     self.view.show_patient_info(patient, self.file_name, self.measure_date, start_time, end_time, model_name)
    #     self.init_SampleList()
    #     self.setup_and_paint_eeg()

    def on_btnConfirm_clicked(self):
        try:
            self.pick_channel = ''
            self.pick_first = None
            self.pick_second = None
            self.pick_seg = None
            self.pick_sample_color = None
            self.pick_sample = None
            self.pick_labels = []
            if self.is_status_showed == False:
                self.is_status_showed = True
                self.view.ui.btnShowInfo.setText("状态隐藏")
            if self.status_annotate:
                self.btnStateAnnotate_clicked()
            self.view.setDisabled(True)
            self.mainMenubar.setDisabled(True)
            msg = [self.check_id, self.file_id, self.patient_id, self.model_id]
            self.client.assessOpenEEGFile(msg)
            self.prentryView.hide()
            self.view.show()
        except Exception as ee:
            QMessageBox.information(self, '提示', f'当前文件无效:{ee}')
            self.mainMenubar.setEnabled(True)
            return

    def assessOpenEEGFileRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', REPData[2])
                self.mainMenubar.setEnabled(True)
                return False
            else:
                self.patientInfo = REPData[1]
                self.sample_list = REPData[2]
                self.channels = REPData[3]
                self.index_channels = REPData[4]
                self.sampling_rate = REPData[5]
                self.n_times = REPData[6]
                # 时长, n_time//sampling_rate
                self.duration = REPData[7]

                meas_date = REPData[8]
                self.start_time = REPData[9]
                self.end_time = REPData[10]
                self.status_info = REPData[11]

                self.montage = 'Default'
                self.mont_idx = 0
                self.begin = 0
                self.index = 0
                self.file_name = "{:>03}.edf".format(self.file_id)
                self.view.show_patient_info(self.patientInfo, self.file_name,
                                            self.measure_date, self.start_time,
                                            self.end_time, self.model_name)

                self.disp_SampleList_ReadInitData()
        except Exception as e:
            print('assessOpenEEGFileRes', e)

    def disp_SampleList_ReadInitData(self):
        try:
            self.init_SampleList()
            REQdata = self.load_dataDynamical()
            msg = [self.check_id, self.file_id, REQdata]
            self.client.assess_load_dataDynamical(msg)
        except Exception as e:
            print('disp_SampleList_ReadInitData', e)

    def load_dataDynamicalRes(self, REPData):
        try:
            self.view.setEnabled(True)
            self.mainMenubar.setEnabled(True)
            if REPData[0] == '0':
                QMessageBox.information(self, "读EEG数据", REPData[2], QMessageBox.Yes)
                return False
            # ['1', REQmsg[1], REQData[0], data, times]
            data = REPData[3]
            times = REPData[4]
            if REPData[2] == 1:
                self.data = data
            # index记录上一次脑电图像所在块号，与当前块号cur_num比较，调整内存数据
            elif REPData[2] == 2:
                self.data = np.hstack((self.data, data))
            elif REPData[2] == 3:
                self.data = np.hstack((data, self.data))
            else:
                QMessageBox.information(self, "读EEG数据", f"{REPData[2]}不匹配", QMessageBox.Yes)
            if REPData[1] == 9:
                self.setup_and_paint_eeg()
            elif REPData[1] == 10:
                self.view.ui.btnUp.setEnabled(True)
                self.view.ui.btnDown.setEnabled(True)
                self.view.ui.btnUping.setEnabled(True)
                self.view.ui.btnDowning.setEnabled(True)
                self.view.ui.btnBegin.setEnabled(True)
                self.view.ui.btnEnd.setEnabled(True)
                self.view.ui.editTime.setEnabled(True)
                self.timeChangeUpdateUi()
                if self.uping % 2 == 1:
                    self.thread = threading.Thread(target=self.do_uping)
                    self.thread.start()
                elif self.downing % 2 == 1:
                    self.thread = threading.Thread(target=self.do_downing)
                    self.thread.start()
        except Exception as e:
            print('load_dataDynamicalRes', e)

    def timeChangeUpdateUi(self):
        try:
            self.remove_lines(self.channels)
            self.paint(self.data, self.begin, self.end)
            self.view.ui.tableWidget.scrollToItem(self.view.ui.tableWidget.item(self.show_sample_index, 0),
                                                  QAbstractItemView.PositionAtCenter)
        except Exception as e:
            print('timeChangeUpdateUi', e)

    def do_uping(self):
        try:
            while True:
                time.sleep(1)
                if self.on_btnUp_clicked(self.move_length):
                    self.stop_thread(self.thread)
        except Exception as e:
            print('do_uping', e)

    def do_downing(self):
        try:
            while True:
                time.sleep(1)
                if self.on_btnDown_clicked(self.move_length):
                    self.stop_thread(self.thread)
        except Exception as e:
            print('do_downing', e)

    # prentryView返回按钮
    def on_btnReturn_clicked(self):
        try:
            self.model_id = None
            self.file_id = None
            self.check_id = None
            itemName = ['分类器名称']
            self.init_tableWidget(self.init_info, itemName)
            self.prentryView.ui.pushButton.setVisible(True)
            self.prentryView.ui.pushButton_2.setVisible(True)
            self.prentryView.ui.pushButton_3.setVisible(True)
            self.prentryView.ui.pushButton_4.setVisible(True)
            self.prentryView.ui.pushButton_5.setVisible(True)
            self.prentryView.ui.label_2.setVisible(True)
            self.prentryView.ui.label.setVisible(True)
            self.prentryView.ui.lineEdit.setVisible(True)
            self.prentryView.ui.lineEdit_2.setVisible(True)
            self.prentryView.ui.comboBox.setVisible(True)
            self.prentryView.ui.pushButton_6.setVisible(True)
            self.prentryView.ui.pushButton_7.setVisible(True)
            self.prentryView.ui.btnReturn.setVisible(False)
            self.prentryView.ui.btnConfirm.setVisible(False)
        except Exception as e:
            print('on_btnReturn_clicked', e)

    # 动态将edf文件的一小时连续数据读入内存，类似滑动窗口（每次滑动替换20min数据），保持当前位置处于中间20min（开端末尾特殊情况）
    # 跳转到某一时间/样本根据情况不处理或替换20min/40min/60min数据
    def load_dataDynamical(self):
        try:
            size = 120
            num = math.ceil(self.duration / size)
            if self.begin == 0:
                cur_num = 1
            else:
                cur_num = math.ceil(self.begin / size)
            # 不超过60min且已分配内存
            if num <= 3 and self.index > 0:
                return
            # 超过60min且不需要调整
            if num > 3:
                if cur_num == self.index:
                    return
                if self.index == 1 and cur_num == 2:
                    return
                if self.index == 2 and cur_num == 1:
                    return
                if self.index == num - 1 and cur_num == num:
                    return
                if self.index == num and cur_num == num - 1:
                    return
            # raw_copy = self.raw.copy()
            # 数据首次载入到内存
            if self.index == 0:
                self.start_t = 0
                REQdata = [1, -1, -1]
                if num <= 3:
                    self.end_t = self.duration
                else:
                    self.end_t = size * 3
                    REQdata = [1, self.start_t, self.end_t]
            # index记录上一次脑电图像所在块号，与当前块号cur_num比较，调整内存数据
            elif self.index < cur_num:
                if cur_num == self.index + 1:
                    # 2 < cur_num <= num-1
                    self.start_t += size
                    if cur_num == num - 1:
                        self.end_t = self.duration
                        REQdata = [2, self.start_t + size * 2, -1]
                    else:
                        self.end_t += size
                        REQdata = [2, self.start_t + size * 2, self.end_t]
                    self.data = self.data[:, size * self.sampling_rate:]

                elif cur_num == self.index + 2:
                    # cur_num == num-1(含num=4，cur_num=3），！=num ！=3（num!=4)
                    if cur_num == num - 1 or (cur_num != num and cur_num != 3):
                        # cur_num ==num-1且num ==4
                        if num == 4:
                            self.start_t += size
                            self.end_t = self.duration
                            REQdata = [2, self.start_t + size * 2, -1]
                            self.data = self.data[:, size * self.sampling_rate:]
                        elif cur_num == num - 1:
                            self.start_t += size * 2
                            self.end_t = self.duration
                            REQdata = [2, self.start_t + size, -1]
                            self.data = self.data[:, size * 2 * self.sampling_rate:]
                        else:
                            self.start_t += size * 2
                            self.end_t += size * 2
                            REQdata = [2, self.start_t + size, self.end_t]
                            self.data = self.data[:, size * 2 * self.sampling_rate:]

                    # cur_num == num or cur_num == 3(num!=4)
                    else:
                        self.start_t += size
                        if cur_num == num:
                            self.end_t = self.duration
                            REQdata = [2, self.start_t + size * 2, -1]
                        # cur_num == 3
                        else:
                            self.end_t += size
                            REQdata = [2, self.start_t + size * 2, self.end_t]
                        self.data = self.data[:, size * self.sampling_rate:]
                elif cur_num == self.index + 3:
                    if cur_num == num - 1:
                        # cur_num ==num-1且num=5
                        if num == 5:
                            self.start_t += size * 2
                            self.end_t = self.duration
                            REQdata = [2, self.start_t + size, -1]
                            self.data = self.data[:, size * 2 * self.sampling_rate:]
                        else:
                            self.start_t = (num - 3) * size
                            self.end_t = self.duration
                            REQdata = [1, self.start_t, -1]
                    elif cur_num == num or cur_num == 4:
                        # cur_num == num且num=4
                        if num == 4:
                            self.start_t += size
                            self.end_t = self.duration
                            REQdata = [2, self.start_t + size * 2, -1]
                            self.data = self.data[:, size * self.sampling_rate:]
                        elif cur_num == num:
                            self.start_t += size * 2
                            self.end_t = self.duration
                            REQdata = [2, self.start_t + size, -1]
                            self.data = self.data[:, size * 2 * self.sampling_rate:]
                        # cur_num == 4(num!=4 !=5)
                        else:
                            self.start_t += size * 2
                            self.end_t += size * 2
                            REQdata = [2, self.start_t + size, self.end_t]
                            self.data = self.data[:, size * 2 * self.sampling_rate:]
                    else:
                        self.start_t = (cur_num - 2) * size
                        self.end_t = (cur_num + 1) * size
                        REQdata = [1, self.start_t, self.end_t]
                else:
                    if cur_num == num or cur_num == num - 1:
                        self.start_t = (num - 3) * size
                        self.end_t = self.duration
                        REQdata = [1, self.start_t, -1]
                    else:
                        self.start_t = (cur_num - 2) * size
                        self.end_t = (cur_num + 1) * size
                        REQdata = [1, self.start_t, self.end_t]
            elif self.index > cur_num:
                if cur_num == self.index - 1:
                    # 2 <= cur_num < num -1
                    self.start_t -= size
                    self.end_t = self.start_t + size * 3
                    REQdata = [3, self.start_t, self.start_t + size]
                    self.data = self.data[:, :size * 2 * self.sampling_rate]
                elif cur_num == self.index - 2:
                    if cur_num == num - 2 or cur_num == 1:
                        self.start_t -= size
                        self.end_t = self.start_t + size * 3
                        REQdata = [3, self.start_t, self.start_t + size]
                        self.data = self.data[:, :size * 2 * self.sampling_rate]
                    else:
                        self.start_t -= size * 2
                        self.end_t -= size * 2
                        REQdata = [3, self.start_t, self.start_t + size * 2]
                        self.data = self.data[:, :size * self.sampling_rate]
                elif cur_num == self.index - 3:
                    if cur_num == 1 or cur_num == num - 3:
                        if num == 4:
                            self.start_t -= size
                            self.end_t = self.start_t + size * 3
                            REQdata = [3, self.start_t, self.start_t + size]
                            self.data = self.data[:, :size * 2 * self.sampling_rate]
                        else:
                            self.start_t -= size * 2
                            self.end_t = self.start_t + size * 3
                            REQdata = [3, self.start_t, self.start_t + size * 2]
                            self.data = self.data[:, :size * self.sampling_rate]
                    else:
                        self.start_t = (cur_num - 2) * size
                        self.end_t = (cur_num + 1) * size
                        REQdata = [1, self.start_t, self.end_t]
                else:
                    if cur_num == 1:
                        self.start_t = 0
                        self.end_t = size * 3
                    else:
                        self.start_t = (cur_num - 2) * size
                        self.end_t = (cur_num + 1) * size
                    REQdata = [1, self.start_t, self.end_t]

            self.index = cur_num
            return REQdata
        except Exception as e:
            print('load_dataDynamical', e)

    # 获取样本并根据是否显示状态/类型/用户筛选样本，显示在样本列表
    def init_SampleList(self):
        try:
            itemName = ['开始时间', '模型标注','用户标注']
            col_num = 3
            self.view.ui.tableWidget.setColumnCount(col_num)
            for i in range(col_num):
                header_item = QTableWidgetItem(itemName[i])
                font = header_item.font()
                font.setPointSize(8)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                self.view.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
            self.view.ui.tableWidget.horizontalHeader().setHighlightSections(False)
            self.view.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            row_num = len(self.sample_list)
            self.view.ui.tableWidget.setRowCount(row_num)
            for r in range(row_num):
                for c in range(col_num):
                    if c == 0:
                        item = QTableWidgetItem(str(time.strftime('%H:%M:%S', time.gmtime(int(self.sample_list[r][1]/self.sampling_rate)))))
                    elif c == 1:
                        mtype_name = self.type_name_dic[self.sample_list[r][4]]
                        item = QTableWidgetItem(mtype_name)
                    elif c == 2:
                        if self.sample_list[r][6]:
                            utype_name = self.type_name_dic[self.sample_list[r][6]]
                        else:
                            utype_name = ''
                        item = QTableWidgetItem(utype_name)
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(8)
                    item.setFont(font)
                    self.view.ui.tableWidget.setItem(r, c, item)
            self.view.ui.tableWidget.verticalHeader().setVisible(False)
            self.view.ui.tableWidget.resizeRowsToContents()
        except Exception as e:
            print('init_SampleList', e)

    # 响应样本列表点击事件，跳转到某一样本
    def on_tableWidgetList_itemClicked(self):
        try:
            row = self.view.ui.tableWidget.currentRow()
            pre_index = self.cur_sample_index
            self.cur_sample_index = row
            sample = self.sample_list[row]
            central = sample[1]
            # 样本不完全在当前窗口内,窗口时间调整
            if not (self.begin <= sample[1] / self.sampling_rate and self.end >= sample[2] / self.sampling_rate):
                self.begin = int(central / self.sampling_rate - self.paint_length / 4)
                self.begin = max(0, self.begin)
                self.end = self.begin + self.paint_length
                if self.end > self.duration:
                    self.end = self.duration
                    self.begin = self.end - self.paint_length
                hour = int(self.begin / 3600)
                minute = int((self.begin % 3600) / 60)
                second = self.begin % 60
                self.view.ui.editTime.setTime(QTime(hour, minute, second))
                # self.load_dataDynamical()
            self.restore_pre_sample_color(pre_index)
            # 当前波形样本显示红色
            if sample[0] != 'all':
                self.change_sample_color(sample, color='red')
            self.show_jump_sample_detail(sample)
        except Exception as e:
            print('on_tableWidgetList_itemClicked', e)

    # 设置画布相关参数
    def set_canvas(self):
        try:
            self.fig = plt.figure()
            self.canvas = FigureCanvas(self.fig)
            self.axes = None
            self.ax_hscroll = None
            self.is_status_showed = True
            self.status_annotated = {}
            self.scroll_position = None
            try:
                mpl.rcParams['keymap.all_axes'].remove('a')
            except Exception:
                ...
            font = {'family': 'SimHei', 'weight': 'bold', 'size': '14'}
            plt.rc('font', **font)  # 步骤一（设置字体的更多属性）
            plt.rc('axes', unicode_minus=False)  # 步骤二（解决坐标轴负数的负号显示问题）
            self.view.ui.glCanvas.addWidget(self.canvas, 0, 0, 1, 1)
            self.canvas.mpl_connect("pick_event", self.handle_pick_event)
            self.canvas.mpl_connect("button_release_event", self.do_mouse_release_event)
            self.canvas.mpl_connect("scroll_event", self.do_scroll_event)
            self.canvas.mpl_connect("key_press_event", self.do_key_press_event)
            self.canvas.setFocusPolicy(Qt.ClickFocus)
            self.canvas.setFocus()
        except Exception as e:
            print('set_canvas', e)

    # 设置画布和样本列表中右击菜单列表
    def set_contextmenu(self):
        try:
            self.popMenu1 = QMenu(self.canvas)
            self.popMenu2 = QMenu(self.canvas)
            cancelAction = QAction("取消选择", self, triggered=self.cancel_select)
            self.popMenu1.addAction(cancelAction)
            self.popMenu1.addSeparator()
            self.popMenu2.addAction(cancelAction)
            self.popMenu2.addSeparator()
            delAction = QAction("删除样本",self, triggered=self.del_sample)
            self.popMenu1.addAction(delAction)
            self.popMenu1.addSeparator()
            self.popMenu2.addAction(delAction)
            self.popMenu2.addSeparator()
            # 向右键菜单栏添加波形和状态
            sms = {}
            groups = ['正常波形', '异常波形', '伪迹波形', '正常状态', '异常状态', '伪迹状态']
            for g in groups[:3]:
                sm = self.popMenu1.addMenu(g)
                sms[g] = sm
            for g in groups[3:]:
                sm = self.popMenu2.addMenu(g)
                sms[g] = sm
            for t in self.type_info:
                action = QAction(t[1], self)
                action.triggered.connect(lambda chk, t=t: self.act_dispatch(t))
                if t[3] == '正常波形':
                    sms[groups[0]].addAction(action)
                elif t[3] == '异常波形':
                    sms[groups[1]].addAction(action)
                elif t[3] == '伪迹波形':
                    sms[groups[2]].addAction(action)
                elif t[3] == '正常状态':
                    sms[groups[3]].addAction(action)
                elif t[3] == '异常状态':
                    sms[groups[4]].addAction(action)
                elif t[3] == '伪迹状态':
                    sms[groups[5]].addAction(action)
                elif t[3] == '特殊标签1':
                    self.popMenu1.addAction(action)
                elif t[3] == '特殊标签2':
                    self.popMenu2.addAction(action)

            self.Menu = QMenu(self.view.ui.tableWidget)
            cancelAction1 = QAction("取消选择", self, triggered=self.cancel_menu)
            self.Menu.addAction(cancelAction1)
            self.Menu.addSeparator()
            delAction1 = QAction("删除样本", self, triggered=self.del_label)
            self.Menu.addAction(delAction1)
            self.Menu.addSeparator()
            sms = {}
            for g in groups[:3]:
                sm = self.Menu.addMenu(g)
                sms[g] = sm
            for t in self.type_info:
                action = QAction(t[1], self)
                action.triggered.connect(lambda chk, t=t: self.update_label(t))
                if t[3] == '正常波形':
                    sms[groups[0]].addAction(action)
                elif t[3] == '异常波形':
                    sms[groups[1]].addAction(action)
                elif t[3] == '伪迹波形':
                    sms[groups[2]].addAction(action)
                elif t[3] == '特殊标签1':
                    self.Menu.addAction(action)
        except Exception as e:
            print('set_contextmenu', e)

    # 初始化相关参数并绘图
    def setup_and_paint_eeg(self):
        try:
            self.calc_sen(len(self.channels) + 1)
            self.scale = self.sen / self.sensitivity
            self.begin = 0
            self.end = self.begin + self.paint_length
            # 初始通道名
            self.channels_default = self.channels[:]
            # 单通道名
            self.channels_name = []
            for ch in self.channels:
                ch = ch.split('-')[0]
                self.channels_name.append(ch)
            self.scales = {}
            self.labels_alpha = {}
            for ch in self.channels:
                self.scales[ch] = self.scale
                self.labels_alpha[ch] = 1.
            self.widget_from_main.setText('绘图长度(s): {}    移动长度(s): {}    灵敏度(µV/mm)：{}    参考方案：{}'.format(self.paint_length, self.move_length, self.sensitivity, self.montage))
            self.paint(self.data, self.begin, self.end, updateY=True)
        except Exception as e:
            print('setup_and_paint_eeg', e)

    # 主画图方法， data为脑电数据，begin为画图开始事件，end为画图结束事件，updateY为是否更新y坐标轴
    def paint(self, data, begin, end, updateY=False, channels=[]) -> None:
        try:
            if data is None:
                return
            self.create_axes(begin, end, updateY, btn='Reset')
            if updateY:
                self.paint_hscroll_status()
            # 获取当前窗口内样本
            window_samples = self.window_sampleList(begin, end)
            status_info = []
            for item in window_samples:
                if item[0] == 'all':
                    status_info.append(item)
                else:
                    continue
            self.paint_status(status_info, Update=True)
            self.paint_channels(data, begin, end, window_samples, channels=channels)
            if self.pick_sample is not None:
                self.pick_sample.set_color('r')
            self.canvas.setFocus()
        except Exception as e:
            print('paint', e)

    # 绘制各导联与样本图像
    def paint_channels(self, data, begin: int, end: int, window_samples=[], channels=[]):
        try:
            if self.scroll_position is not None:
                self.scroll_position.remove()
            self.scroll_position = self.ax_hscroll.axvline(begin, color='red')
            if len(channels) == 0:
                channels = self.channels
            self.pick_events = []
            color = 'black'
            x = np.linspace(begin, end, (end - begin) * self.sampling_rate)
            s = (begin - self.start_t) * self.sampling_rate
            e = (end - self.start_t) * self.sampling_rate
            chs = set([y for x in self.channels for y in x.split('-')])
            if 'AV' in chs:
                ex_chs = tuple([self.channels_name.index(x) for x in self.exclude_av if x in self.channels_name])
                temp_data = data[:, s:e]
                temp_data = np.delete(temp_data, ex_chs, axis=0)
                av = np.mean(temp_data, axis=0)

            #  获取当前窗口的样本
            samples = window_samples
            for i in range(len(channels)):
                index = self.channels.index(channels[i])
                label = channels[i]
                if '-' in label:
                    g1, g2 = label.split('-')
                    try:
                        g1_index = self.channels_name.index(g1)
                        y1 = data[g1_index, s:e]
                    except ValueError:
                        continue
                    if g2 == 'REF':
                        y2 = 0
                    elif g2 == 'AV':
                        y2 = av
                    else:
                        try:
                            g2_index = self.channels_name.index(g2)
                            y2 = data[g2_index, s:e]
                        except ValueError:
                            continue
                    y = y1 - y2
                else:
                    y = data[index, s:e]
                if x.shape != y.shape:
                    y = np.resize(y, x.shape)
                y = y * self.scales[label]
                # 在create_axes中 axes.invert_yaxis反转y轴，y轴取值上负下正，脑电取值默认下负上正，需要对其取反
                y = -y + index + 1
                # label属性就是设置图例用来保存当前数据是哪个通道以便拾取的时候知道,但是没有调用legend方法所以图例不会显示出来
                self.axes.plot(x, y, color=color, label=label, picker=True,
                               alpha=self.labels_alpha[label], linewidth=0.5)
                # 画样本
                # sample: [channel,begin,end,mid,mtype_id,uid,utpye_id]
                # sample label: channel|begin|end|mid|mtype_id|uid|utype_id
                for sample in samples:
                    if sample[0] != label:
                        continue
                    color2 = 'blue'
                    index1 = sample[1] - begin * self.sampling_rate if sample[1] > begin * self.sampling_rate else 0
                    index2 = sample[2] - begin * self.sampling_rate if sample[2] > begin * self.sampling_rate else 0
                    s_label = '|'.join([str(x) for x in sample[:]])
                    self.axes.plot(x[index1:index2], y[index1:index2], color=color2, picker=True, label=s_label,
                                   alpha=self.labels_alpha[label], linewidth=1)
            self.canvas.draw()
        except Exception as e:
            print('paint_channels', e)

    # 绘制单个样本
    def paint_sample(self, data, start, end, channel, color, label):
        try:
            x = np.linspace(start / self.sampling_rate, end / self.sampling_rate, end - start)
            s = start - self.start_t * self.sampling_rate
            e = end - self.start_t * self.sampling_rate
            index = self.channels.index(channel)
            if '-' in channel:
                g1, g2 = channel.split('-')
                g1_index = self.channels_name.index(g1)
                y1 = data[g1_index, s:e]
                if g2 == 'REF':
                    y2 = 0
                elif g2 == 'AV':
                    ex_chs = tuple([self.channels_name.index(x) for x in self.exclude_av if x in self.channels_name])
                    temp_data = data[:, s:e]
                    temp_data = np.delete(temp_data, ex_chs, axis=0)
                    y2 = np.mean(temp_data, axis=0)
                else:
                    g2_index = self.channels_name.index(g2)
                    y2 = data[g2_index, s:e]
                y = y1 - y2
            else:
                y = data[index, s:e]
            y = y * self.scales[channel]
            y = -y + index + 1
            self.axes.plot(x, y, color=color, label=label, picker=True,
                           alpha=self.labels_alpha[channel], linewidth=1)
            self.canvas.draw()
        except Exception as e:
            print('paint_sample', e)

    # 绘制状态
    def paint_status(self, status_info, Update=False):
        try:
            # status_info = [(channel,begin,end,mid,mtype_id,uid,utype_id)]
            if Update == True:
                for x in self.status_annotated:
                    for i in self.status_annotated[x][:-1]:
                        i.remove()
                    x.remove()
                self.status_annotated.clear()
            keys = [x[0] for x in self.type_info]
            for status in status_info:
                if status[6]:
                    type_name = self.type_name_dic[status[6]]
                    t_id = status[6]
                else:
                    type_name = self.type_name_dic[status[4]]
                    t_id = status[4]
                idx = keys.index(t_id)
                description = self.type_info[idx][3]
                if description == '正常状态':
                    color = 'green'
                elif description == '异常状态':
                    color = 'red'
                else:
                    color = 'dodgerblue'
                label = '|'.join([str(x) for x in status[:]])
                x0, x1 = status[1] / self.sampling_rate, status[2] / self.sampling_rate
                rect = self.axes.axvspan(x0, x1, label=label, facecolor=color, alpha=0.3, picker=True)
                t = x0
                texts = []
                texts.append(self.axes.text(t, -0.2, type_name, fontsize='x-small'))
                if not (x0, x1) in self.status_hscroll:
                    rect1 = (x0, x1)
                    self.status_hscroll[rect1] = self.ax_hscroll.axvspan(x0, x1, facecolor=color, alpha=0.5)
                texts.append(self.status_hscroll[(x0, x1)])
                self.status_annotated[rect] = texts
            if not self.is_status_showed:
                self.hide_status()
            else:
                self.canvas.draw()
        except Exception as e:
            print('paint_status', e)

    # 绘制上方时间条中的状态
    def paint_hscroll_status(self):
        try:
            # status_info = self.DbUtil.get_labelStatusInfo(self.patient_id, self.measure_date, self.file_name, self.model_id)
            status_info = self.status_info
            # status_info = [(channel,begin,end,mid,mtype_id,uid,utype_id)]
            self.status_hscroll = {}
            keys = [x[0] for x in self.type_info]
            for status in status_info:
                if status[6]:
                    t_id = status[6]
                else:
                    t_id = status[4]
                idx = keys.index(t_id)
                description = self.type_info[idx][3]
                if description == '正常状态':
                    color = 'green'
                elif description == '异常状态':
                    color = 'red'
                else:
                    color = 'dodgerblue'
                x0, x1 = status[1] / self.sampling_rate, status[2] / self.sampling_rate
                rect = (x0, x1)
                self.status_hscroll[rect] = self.ax_hscroll.axvspan(x0, x1, facecolor=color, alpha=0.5)
            if not self.is_status_showed:
                self.hide_status()
            else:
                self.canvas.draw()
        except Exception as e:
            print('paint_hscroll_status', e)

    # 响应选中对象事件
    def handle_pick_event(self, event):
        try:
            self.pick_events.append(event)
            if len(self.pick_events) == 0:
                return
            event = self.pick_events.pop(0)
            mouseevent = event.mouseevent
            artist = event.artist
            # 状态标记状态
            if self.status_annotate:
                if not self.is_status_showed:
                    return
                if artist in self.status_annotated:
                    self.state_picked = artist
                return
            # 点击右键
            if mouseevent.button == 3:
                return
            # 鼠标左键
            elif mouseevent.button == 1:
                # 点击y轴标签
                if isinstance(artist, mpl.text.Text):
                    pl = artist.get_text()
                    if pl == 'Reset':
                        self.labels_alpha.update((k, 1.) for k in self.labels_alpha)
                        self.pick_labels = []
                    else:
                        if pl in self.pick_labels:
                            self.pick_labels.remove(pl)
                        else:
                            self.pick_labels.append(pl)
                        # 设置透明度
                        self.set_alpha()
                    self.focus_lines()
                # 点击线、点
                elif isinstance(artist, mpl.lines.Line2D):
                    label = artist.get_label()
                    # 点击点
                    if label == "pp":
                        return
                    # 点击线
                    elif len(label.split('|')) == 1:
                        return
                    # 点击样本
                    else:
                        self.restore_pre_sample_color(self.cur_sample_index)
                        if self.pick_sample is not None:
                            self.pick_sample.set_color(self.pick_sample_color)
                        if label.split('|')[0] not in self.pick_labels:
                            self.pick_labels = []
                            self.pick_labels.append(label.split('|')[0])
                            self.set_alpha()
                            self.focus_lines()
                        self.remove_lines(['pp', 'pickedsegment'])
                        xdata, ydata = artist.get_data()
                        # 样本label格式：channel|begin|end|mid|mtype_id|uid|utype_id
                        label = label.split('|')
                        label[1] = int(label[1])
                        label[2] = int(label[2])
                        label[3] = int(label[3])
                        label[4] = int(label[4])
                        label[5] = int(label[5])
                        if label[6] == 'None':
                            label[6] = None
                        else:
                            label[6] = int(label[6])
                        self.view.ui.tableWidget.selectRow(self.sample_list.index(tuple(label)))
                        m = abs(ydata.max() - ydata.min())
                        m = m / self.scales[label[0]]
                        self.pick_channel = ''
                        self.pick_sample_color = artist.get_color()
                        self.pick_sample = artist
                        artist.set_color('r')
                        b_t = label[1] / self.sampling_rate
                        e_t = label[2] / self.sampling_rate
                        msb = int(b_t * 1000) % 1000
                        mse = int(e_t * 1000) % 1000
                        b_t = time.strftime('%H:%M:%S.{:03}'.format(msb), time.gmtime(b_t))
                        e_t = time.strftime('%H:%M:%S.{:03}'.format(mse), time.gmtime(e_t))
                        user_name = ""
                        for u in self.user_info:
                            if u[0] == label[3]:
                                user_name = u[3]
                                break
                        mtype_name = self.type_name_dic[label[4]]
                        if label[6] != None:
                            utype_name = self.type_name_dic[label[6]]
                        else:
                            utype_name = ''
                        model_name = self.model_name
                        self.view.show_sample_detail(model_name, mtype_name, label[0], len(xdata) / self.sampling_rate,
                                                str(b_t), str(e_t), str(m), user_name, utype_name)
                        self.canvas.draw()
            else:
                return
        except Exception as e:
            print('handle_pick_event', e)

    # 响应鼠标按键被释放事件
    def do_mouse_release_event(self, event):
        try:
            # 左键
            if event.button == 1:
                x, y = event.xdata, event.ydata
                # 点击在脑电图axes中
                if event.inaxes == self.axes:
                    # 非状态标注下，不响应鼠标按键松开事件
                    if not self.status_annotate:
                        return
                    if self.state_left is None:
                        self.state_left = int(x * self.sampling_rate)
                        self.state_left_line = self.axes.vlines(
                            self.state_left / self.sampling_rate, 0, 50, color='red')
                    else:
                        return
                    self.canvas.draw()
                # 点击在跳转滚动条上
                elif event.inaxes == self.ax_hscroll:
                    self.on_axhscroll_clicked(begin=int(x))
            # 右键
            elif event.button == 3:
                if self.duration is None:
                    return
                # 根据波形/状态禁用子菜单
                if self.status_annotate:
                    self.popMenu2.exec_(QCursor.pos())
                else:
                    self.popMenu1.exec_(QCursor.pos())
        except Exception as e:
            print('do_mouse_release_event', e)

    # 响应键盘按键按下事件
    def do_key_press_event(self, event):
        try:
            if event.key == 'escape':
                self.cancel_select()
            elif event.key == 'a':
                self.btnStateAnnotate_clicked()
            elif event.key == 'left':
                self.on_btnDown_clicked()
            elif event.key == 'right':
                self.on_btnUp_clicked()
        except Exception as e:
            print('do_key_press_event', e)

    # 响应鼠标滚轮滚动事件
    def do_scroll_event(self, event):
        try:
            if event.button == "down":
                self.on_btnUp_clicked()
            else:
                self.on_btnDown_clicked()
        except Exception as e:
            print('do_scroll_event', e)

    # 右击菜单栏：取消选择
    def cancel_select(self):
        try:
            if self.status_annotate:
                self.cancel_state_annotate()
                return
            self.pick_channel = ''
            self.remove_lines(['pp', 'pickedsegment'])
            if self.pick_sample is not None:
                self.pick_sample.set_color(self.pick_sample_color)
                self.canvas.draw()
                self.pick_sample_color = None
                self.pick_sample = None
                self.view.show_sample_detail()
            self.restore_pre_sample_color(self.cur_sample_index)
            self.labels_alpha.update((k, 1.) for k in self.labels_alpha)
            self.pick_labels = []
            self.focus_lines()
        except Exception as e:
            print('cancel_select', e)

    # 创建坐标系
    def create_axes(self, begin, end, updateY, btn)-> None:
        try:
            max_y = len(self.channels) + 1
            if self.axes is None:
                self.axes = plt.subplot2grid((33, 1), (3, 0), rowspan=30)
            if self.ax_hscroll is None:
                # 创建一个水平滚动条的子图对象
                self.ax_hscroll = plt.subplot2grid((33, 1), (0, 0), rowspan=1)
                self.ax_hscroll.set_xlim(0, self.duration)
                self.ax_hscroll.get_yaxis().set_visible(False)
                # self.ax_hscroll.get_xaxis().set_visible(True)
                # 创建矩形对象
                hsel_patch = mpl.patches.Rectangle((0, 0), self.duration,
                                                   1,
                                                   edgecolor='k',
                                                   facecolor=(0.75, 0.75, 0.75),
                                                   alpha=0.25, linewidth=1,
                                                   clip_on=False)
                self.ax_hscroll.add_patch(hsel_patch)
            if updateY:
                self.ax_hscroll.clear()
                self.ax_hscroll.set_xlim(0, self.duration)
                self.axes.clear()
                self.axes.set_ylim([0, max_y])
                self.axes.set_yticks(range(max_y))
                self.axes.set_yticklabels([btn] + self.channels)
                for ytl in self.axes.get_yticklabels():
                    ytl.set_picker(True)
                    ytl.set_fontsize(10)
                self.axes.invert_yaxis()
                self.fig.subplots_adjust(left=0.07)
                self.fig.subplots_adjust(right=0.97)
            self.axes.set_xlim([begin, end])
            self.axes.set_xticks(np.arange(begin, end + 1, 1))
            xlabels = [time.strftime('%H:%M:%S', time.gmtime(i))
                       for i in range(begin, end + 1)]
            self.axes.set_xticklabels(xlabels)
            for xtl in self.axes.get_xticklabels():
                xtl.set_fontsize(10)
            hxticks = np.linspace(0, self.duration, 11)
            self.ax_hscroll.set_xticks(hxticks)
            hxlabels = [time.strftime('%H:%M:%S', time.gmtime(int(hxticks[i])))
                        for i in range(0, 11)]
            self.ax_hscroll.set_xticklabels(hxlabels)
            for xhtl in self.ax_hscroll.get_xticklabels():
                xhtl.set_fontsize(10)
        except Exception as e:
            print('create_axes', e)

    # 获取坐标轴x轴和y轴分别占图像的百分比，为了计算图像的真实长度（厘米）
    def get_axes_fraction(self) -> tuple:
        try:
            flag = False
            if self.axes is None:
                flag = True
                self.axes = self.fig.add_subplot(111)
                self.fig.tight_layout()
            axesL = self.axes.figure.subplotpars.left
            axesR = self.axes.figure.subplotpars.right
            axesT = self.axes.figure.subplotpars.top
            axesB = self.axes.figure.subplotpars.bottom
            if flag:
                self.fig.delaxes(self.axes)
                self.axes = None
            return (axesR - axesL, axesT - axesB)
        except Exception as e:
            print('get_axes_fraction', e)

    def calc_sen(self, max_y):
        try:
            x_fraction, y_fraction = self.get_axes_fraction()
            figureSize = self.view.ui.listView.size()
            figureWidth = figureSize.width()
            figureHeight = figureSize.height()
            screen = QApplication.primaryScreen()
            xDPI = screen.physicalDotsPerInchX()
            yDPI = screen.physicalDotsPerInchX()
            figureWidthMM = (figureWidth / xDPI) * 25.4
            figureHeightMM = (figureHeight / yDPI) * 25.4
            axesXWidthMM = x_fraction * figureWidthMM
            pl = int(round(axesXWidthMM / 30))
            self.move_length = pl
            self.paint_length = pl
            self.sen = max_y / (y_fraction * figureHeightMM)
        except Exception as e:
            print('calc_sen', e)

    # 去除画布中的导联/样本
    def remove_lines(self, ch=[], sample=False):
        if ch is None or len(ch) == 0:
            return
        lines = self.axes.get_lines()
        for l in lines:
            label = l.get_label() if sample else l.get_label().split('|')[0]
            if label in ch:
                l.remove()
        self.canvas.draw()

    # 恢复各通道的透明度
    def focus_lines(self):
        try:
            lines = self.axes.get_lines()
            for l in lines:
                label = l.get_label().split('|')[0]
                if label in self.labels_alpha:
                    l.set_alpha(self.labels_alpha[label])
            self.canvas.draw()
        except Exception as e:
            print('focus_lines', e)

    # 更换线段（样本）颜色
    def change_sample_color(self, sample, color):
        try:
            s_label = '|'.join([str(x) for x in sample[:]])
            lines = self.axes.get_lines()
            for l in lines:
                label = l.get_label()
                if label == s_label:
                    l.set_color(color)
            self.canvas.draw()
        except Exception as e:
            print('change_sample_color', e)

    # 恢复sample_index指向的样本颜色
    def restore_pre_sample_color(self, sample_index):
        try:
            if len(self.sample_list) > sample_index:
                sample = self.sample_list[sample_index]
                # self.cur_sample_index指向的样本在本窗口内 回复其颜色
                if sample[0] != 'all' and not (sample[2] <= self.begin * self.sampling_rate or sample[1] >= self.end * self.sampling_rate):
                    color = 'blue'
                    self.change_sample_color(sample, color)
            else:
                return
        except Exception as e:
            print('restore_pre_sample_color', e)

    # 设置透明度
    def set_alpha(self):
        try:
            for k in self.labels_alpha:
                if self.pick_labels == []:
                    self.labels_alpha[k] = 1
                elif k in self.pick_labels:
                    self.labels_alpha[k] = 1
                else:
                    self.labels_alpha[k] = 0.075
        except Exception as e:
            print('set_alpha', e)

    # 响应右击菜单选中事件
    def act_dispatch(self, type):
        try:
            if self.status_annotate:
                self.update_state(type)
                return
            if self.pick_sample is None:
                QMessageBox.information(self.view, ' ', "无效选择")
                return
            # 修改样本
            if self.pick_sample is not None:
                self.update_sample(type)
            self.remove_lines(['pp', 'pickedsegment'])
            self.pick_channel = ''
            self.pick_sample_color = None
            self.pick_sample = None
            self.labels_alpha.update((k, 1.) for k in self.labels_alpha)
            self.pick_labels = []
            self.focus_lines()
        except Exception as e:
            print('act_dispatch', e)

    # 修改样本
    def update_sample(self, type):
        try:
            color = 'blue'
            self.pick_sample.set_color(color)
            label = self.pick_sample.get_label().split('|')
            label[1] = int(label[1])
            label[2] = int(label[2])
            label[3] = int(label[3])
            label[4] = int(label[4])
            label[5] = int(label[5])
            if label[6] == 'None':
                label[6] = None
            else:
                label[6] = int(label[6])
            idx = self.sample_list.index(tuple(label))
            pick_channel = label[0]
            start = label[1]
            end = label[2]
            mid = label[3]
            mtype_id = label[4]
            uid = self.client.tUser[0]
            utype_id, utype_name = type[0], type[1]
            self.p_sample = self.pick_sample
            self.client.update_labelListInfo([self.model_id, self.check_id, self.file_id, start, pick_channel,
                                              end, mtype_id, uid, utype_id, idx])
        except Exception as e:
            print('update_sample', e)

    def update_labelListInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                idx = REPData[2][9]
                pick_channel = REPData[2][4]
                start = REPData[2][3]
                end = REPData[2][5]
                mid = REPData[2][0]
                mtype_id = REPData[2][6]
                uid = REPData[2][7]
                utype_id = REPData[2][8]
                cur_sample = (pick_channel, start, end, mid, mtype_id, uid, utype_id)
                s_label = '|'.join([str(x) for x in cur_sample[:]])
                xdata, ydata = self.p_sample.get_data()
                self.sample_list[idx] = cur_sample
                self.p_sample.set_label(s_label)
                m = abs(ydata.max() - ydata.min())
                m = m / self.scales[pick_channel]
                b_t = start / self.sampling_rate
                e_t = end / self.sampling_rate
                msb = int(b_t * 1000) % 1000
                mse = int(e_t * 1000) % 1000
                b_t = time.strftime('%H:%M:%S.{:03}'.format(msb), time.gmtime(b_t))
                e_t = time.strftime('%H:%M:%S.{:03}'.format(mse), time.gmtime(e_t))
                user_name = self.client.tUser[3]
                mtype_name = self.type_name_dic[mtype_id]
                model_name = self.model_name
                utype_name = self.type_name_dic[utype_id]
                self.view.show_sample_detail(model_name, mtype_name, pick_channel, (end - start) / self.sampling_rate, str(b_t), str(e_t), str(m), user_name, utype_name)
                for c in range(3):
                    if c == 0:
                        item = QTableWidgetItem(str(time.strftime('%H:%M:%S', time.gmtime(int(self.sample_list[idx][1] / self.sampling_rate)))))
                    elif c == 1:
                        item = QTableWidgetItem(mtype_name)
                    elif c == 2:
                        item = QTableWidgetItem(utype_name)
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(8)
                    item.setFont(font)
                    self.view.ui.tableWidget.setItem(idx, c, item)
                self.view.ui.tableWidget.repaint()
                self.is_reload_controller.emit("clearLabelController")
            else:
                QMessageBox.information(self.view, '添加失败', "失败原因: %s", REPData[1])
        except Exception as e:
            print('update_labelListInfoRes', e)

    # 删除样本
    def del_sample(self):
        try:
            # 删除状态
            if self.status_annotate:
                self.del_state()
                return
            if self.pick_sample is None:
                QMessageBox.information(self.view, ' ', "请选择样本")
                return
            label = self.pick_sample.get_label().split('|')
            label[1] = int(label[1])
            label[2] = int(label[2])
            label[3] = int(label[3])
            label[4] = int(label[4])
            label[5] = int(label[5])
            if label[6] == 'None':
                label[6] = None
            else:
                label[6] = int(label[6])
            idx = self.sample_list.index(tuple(label))
            pick_channel, start, end, mid, mtype_id = label[0], label[1], label[2], label[3], label[4]
            self.client.del_labelListInfo15([mid, self.check_id, self.file_id, start, pick_channel, end, mtype_id, idx, label])
        except Exception as e:
            print('del_sample', e)

    def del_labelListInfo15Res(self, REPData):
        try:
            if REPData[0] == '1':
                idx = REPData[2][7]
                self.remove_lines([self.pick_sample.get_label()], sample=True)
                # 删除波形样本
                self.view.show_sample_detail()
                self.pick_channel = ''
                self.pick_sample_color = None
                self.pick_sample = None
                self.labels_alpha.update((k, 1.) for k in self.labels_alpha)
                self.pick_labels = []
                self.focus_lines()
                self.sample_list.pop(idx)
                self.view.ui.tableWidget.removeRow(idx)
                self.view.ui.tableWidget.repaint()
                QMessageBox.information(self, "成功", "删除成功")
                self.is_reload_controller.emit("clearLabelController")
            else:
                QMessageBox.information(self, "错误", "删除失败")
                return
        except Exception as e:
            print('del_labelListInfo15Res', e)

    # 点击按钮跳转到上一样本
    def on_btnPrevSample_clicked(self):
        try:
            if self.duration is None:
                return
            start = self.begin * self.sampling_rate
            end = start + self.paint_length * self.sampling_rate
            sz = len(self.sample_list)
            if sz == 0:
                return
            if sz > self.cur_sample_index:
                pre_index = self.cur_sample_index
            else:
                pre_index = sz - 1
            pre_sample = self.sample_list[pre_index]
            pre_mid = pre_sample[1]
            if pre_mid >= start and pre_mid <= end:
                # 第一个样本
                if self.cur_sample_index == 0:
                    return
                # 非第一个样本
                self.cur_sample_index -= 1
            # self.cur_sample_index 失效，重新查找左边第一个index
            else:
                idx = self.bin_search(start)
                if idx == 0:
                    return
                self.cur_sample_index = idx - 1
            sample = self.sample_list[self.cur_sample_index]
            central = sample[1]
            if not (self.begin <= sample[1] / self.sampling_rate and self.end >= sample[2] / self.sampling_rate):
                self.begin = int(central / self.sampling_rate - self.paint_length / 4)
                self.begin = max(0, self.begin)
                self.end = self.begin + self.paint_length
                if self.end > self.duration:
                    self.end = self.duration
                    self.begin = self.end - self.paint_length
                hour = int(self.begin / 3600)
                minute = int((self.begin % 3600) / 60)
                second = self.begin % 60
                self.view.ui.editTime.setTime(QTime(hour, minute, second))
                # self.load_dataDynamical()
            self.restore_pre_sample_color(pre_index)
            if sample[0] != 'all':
                self.change_sample_color(sample, color='red')
            self.show_jump_sample_detail(sample)
            self.view.ui.tableWidget.scrollToItem(self.view.ui.tableWidget.item(self.cur_sample_index, 0),
                                                  QAbstractItemView.PositionAtCenter)
            self.view.ui.tableWidget.selectRow(self.cur_sample_index)
        except Exception as e:
            print('on_btnPrevSample_clicked', e)

    # 点击按钮跳转到下一样本
    def on_btnNextSample_clicked(self):
        try:
            if self.duration is None:
                return
            start = self.begin * self.sampling_rate
            end = start + self.paint_length * self.sampling_rate
            sz = len(self.sample_list)
            if sz == 0:
                return
            if sz > self.cur_sample_index:
                pre_index = self.cur_sample_index
            else:
                pre_index = sz - 1
            pre_sample = self.sample_list[pre_index]
            pre_mid = pre_sample[1]
            if pre_mid >= start and pre_mid <= end:
                # 最后一个样本
                if self.cur_sample_index == sz - 1:
                    return
                # 非最后一个样本
                self.cur_sample_index += 1
            # self.cur_sample_index 失效，重新查找右边第一个index
            else:
                idx = self.bin_search(start)
                if idx == sz:
                    return
                self.cur_sample_index = idx
            sample = self.sample_list[self.cur_sample_index]
            central = sample[1]
            if not (self.begin <= sample[1] / self.sampling_rate and self.end >= sample[2] / self.sampling_rate):
                self.begin = int(central / self.sampling_rate - self.paint_length / 4)
                self.begin = max(0, self.begin)
                self.end = self.begin + self.paint_length
                if self.end > self.duration:
                    self.end = self.duration
                    self.begin = self.end - self.paint_length
                hour = int(self.begin / 3600)
                minute = int((self.begin % 3600) / 60)
                second = self.begin % 60
                self.view.ui.editTime.setTime(QTime(hour, minute, second))
                # self.load_dataDynamical()
            self.restore_pre_sample_color(pre_index)
            if sample[0] != 'all':
                self.change_sample_color(sample, color='red')
            self.show_jump_sample_detail(sample)
            self.view.ui.tableWidget.scrollToItem(self.view.ui.tableWidget.item(self.cur_sample_index, 0),
                                                  QAbstractItemView.PositionAtCenter)
            self.view.ui.tableWidget.selectRow(self.cur_sample_index)
        except Exception as e:
            print('on_btnNextSample_clicked', e)

    # 显示跳转的样本信息
    def show_jump_sample_detail(self, sample):
        try:
            mtype_name = self.type_name_dic[sample[4]]
            if sample[6]:
                utype_name = self.type_name_dic[sample[6]]
            else:
                utype_name =''
            lent = (sample[2] - sample[1]) / self.sampling_rate
            b_t = sample[1] / self.sampling_rate
            e_t = sample[2] / self.sampling_rate
            msb = int(b_t * 1000) % 1000
            mse = int(e_t * 1000) % 1000
            b_t = time.strftime('%H:%M:%S.{:03}'.format(msb), time.gmtime(b_t))
            e_t = time.strftime('%H:%M:%S.{:03}'.format(mse), time.gmtime(e_t))
            if sample[0] != 'all':
                idx = self.channels.index(sample[0])
                s = sample[1] - self.start_t * self.sampling_rate
                e = sample[2] - self.start_t * self.sampling_rate
                if '-' in sample[0]:
                    g1, g2 = sample[0].split('-')
                    g1_index = self.channels_name.index(g1)
                    y1 = self.data[g1_index, s:e]
                    if g2 == 'REF':
                        y2 = 0
                    elif g2 == 'AV':
                        ex_chs = tuple([self.channels_name.index(x) for x in self.exclude_av if x in self.channels_name])
                        temp_data = self.data[:, s:e]
                        temp_data = np.delete(temp_data, ex_chs, axis=0)
                        y2 = np.mean(temp_data, axis=0)
                    else:
                        g2_index = self.channels_name.index(g2)
                        y2 = self.data[g2_index, s:e]
                    y = y1 - y2
                else:
                    y = self.data[idx, s:e]
                channel = sample[0]
                if len(y) > 0:
                    m = abs(y.max() - y.min())
                else:
                    m = ''
            else:
                channel = ''
                m = ''
            user_name = ""
            for u in self.user_info:
                if u[0] == sample[3]:
                    user_name = u[3]
                    break
            self.view.show_sample_detail(self.model_name, mtype_name, channel, lent, str(b_t), str(e_t), str(m), user_name, utype_name)
        except Exception as e:
            print('show_jump_sample_detail', e)

    # 修改状态
    def update_state(self, type):
        try:
            if self.state_left is None and self.state_picked is None:
                return
            if self.state_picked is not None and self.state_right is None:
                label = self.state_picked.get_label().split('|')
                label[1] = int(label[1])
                label[2] = int(label[2])
                label[3] = int(label[3])
                label[4] = int(label[4])
                label[5] = int(label[5])
                if label[6] == 'None':
                    label[6] = None
                else:
                    label[6] = int(label[6])
                idx = self.sample_list.index(tuple(label))
                pick_channel, begin, end, mid, mtype_id = label[0], label[1], label[2], label[3], label[4]
                uid = self.User[0]
                utype_id, utype_name = type[0], type[1]
                self.client.update_state_labelListInfo([self.model_id, self.check_id, self.file_id, begin, pick_channel,
                                                  end, mtype_id, uid, utype_id, idx, label])
        except Exception as e:
            print('update_state', e)

    def update_state_labelListInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                idx = REPData[2][9]
                pick_channel = REPData[2][4]
                begin = REPData[2][3]
                end = REPData[2][5]
                mid = REPData[2][0]
                mtype_id = REPData[2][6]
                uid = REPData[2][7]
                utype_id = REPData[2][8]
                label = REPData[2][10]
                utype_name = self.type_name_dic[utype_id]
                mtype_name = self.type_name_dic[mtype_id]
                status = (pick_channel, begin, end, mid, mtype_id, uid, utype_id)
                s_label = '|'.join([str(x) for x in status[:]])
                self.state_picked.set_label(s_label)
                keys = [x[0] for x in self.type_info]
                c_idx = keys.index(utype_id)
                description = self.type_info[c_idx][3]
                if description == '正常状态':
                    color = 'green'
                elif description == '异常状态':
                    color = 'red'
                else:
                    color = 'dodgerblue'
                self.state_picked.set_fc(color)
                x0, x1 = label[1] / self.sampling_rate, label[2] / self.sampling_rate
                rect = (x0, x1)
                self.status_hscroll[rect].set_fc(color)
                self.status_annotated[self.state_picked][0].set_text(utype_name)
                self.state_picked = None
                self.sample_list[idx] = status
                self.show_jump_sample_detail(status)
                self.cancel_state_annotate()
                for c in range(3):
                    if c == 0:
                        item = QTableWidgetItem(str(time.strftime('%H:%M:%S', time.gmtime(int(self.sample_list[idx][1] / self.sampling_rate)))))
                    elif c == 1:
                        item = QTableWidgetItem(mtype_name)
                    elif c == 2:
                        item = QTableWidgetItem(utype_name)
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(8)
                    item.setFont(font)
                    self.view.ui.tableWidget.setItem(idx, c, item)
                self.view.ui.tableWidget.repaint()
                self.view.ui.tableWidget.selectRow(idx)
            else:
                return
        except Exception as e:
            print('update_state_labelListInfoRes', e)

    # 删除状态
    def del_state(self):
        try:
            if self.state_picked is not None:
                label = self.state_picked.get_label().split('|')
                label[1] = int(label[1])
                label[2] = int(label[2])
                label[3] = int(label[3])
                label[4] = int(label[4])
                label[5] = int(label[5])
                if label[6] == 'None':
                    label[6] = None
                else:
                    label[6] = int(label[6])
                idx = self.sample_list.index(tuple(label))
                pick_channel, start, end, mid, mtype_id = label[0], label[1], label[2], label[3], label[4]
                self.client.del_labelListInfo16(
                    [mid, self.check_id, self.file_id, start, pick_channel, end, mtype_id, idx, label])
        except Exception as e:
            print('del_state', e)

    def del_labelListInfo16Res(self, REPData):
        try:
            if REPData[0] == '1':
                idx = REPData[2][7]
                self.remove_state(self.state_picked)
                self.state_picked = None
                self.cancel_state_annotate()
                self.sample_list.pop(idx)
                self.view.ui.tableWidget.removeRow(idx)
                self.view.ui.tableWidget.repaint()
        except Exception as e:
            print('del_labelListInfo16Res', e)

    def remove_state(self, artist):
        try:
            if artist in self.status_annotated:
                for x in self.status_annotated[artist]:
                    x.remove()
                self.status_annotated.pop(artist)
                artist.remove()
                self.canvas.draw()
        except Exception as e:
            print('remove_state', e)

    def cancel_state_annotate(self):
        try:
            self.state_left = None
            if self.state_left_line is not None:
                self.state_left_line.remove()
                self.state_left_line = None
            self.state_right = None
            if self.state_right_line is not None:
                self.state_right_line.remove()
                self.state_right_line = None
            if self.state_picked is not None:
                self.state_picked = None
            self.canvas.draw()
        except Exception as e:
            print('cancel_state_annotate', e)

    def show_status(self):
        try:
            for x in self.status_annotated:
                for t in self.status_annotated[x][:-1]:
                    t.set(visible=True)
                x.set(visible=True)
            self.canvas.draw()
        except Exception as e:
            print('show_status', e)

    def hide_status(self):
        try:
            for x in self.status_annotated:
                for t in self.status_annotated[x][:-1]:
                    t.set(visible=False)
                x.set(visible=False)
            self.canvas.draw()
        except Exception as e:
            print('hide_status', e)

    # 进入/退出状态标注
    def btnStateAnnotate_clicked(self):
        try:
            if self.duration is None:
                return
            self.cancel_select()
            self.status_annotate = not self.status_annotate
            if self.status_annotate:
                self.view.ui.btnStateAnnotate.setStyleSheet("background-color: yellow")
            else:
                self.view.ui.btnStateAnnotate.setStyleSheet("")
            self.state_left = None
            self.state_left_line = None
            self.state_right = None
            self.state_right_line = None
            self.state_picked = None
        except Exception as e:
            print('btnStateAnnotate_clicked', e)

    # 初始化绘图设置页面
    def on_btnSetting_clicked(self):
        try:
            if self.duration is None:
                return
            self.stopRolling()
            type_name = [x[1] for x in self.type_info]
            user_name = [x[3] for x in self.user_info]
            if self.montage == 'Default':
                channels = [x for x in self.channels_default]
            else:
                channels = [x for x in self.montages[self.mont_idx - 1]['channels']]
            self.settingView = SettingView(type_name, user_name, self.type_filter, self.user_filter)
            self.settingView.ui.comboBoxChannel = CheckableComboBox(self.settingView.ui.gbSettings, channels, self.channels, self.channels_name)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(2)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.settingView.ui.comboBoxChannel.sizePolicy().hasHeightForWidth())
            self.settingView.ui.comboBoxChannel.setSizePolicy(sizePolicy)
            self.settingView.ui.comboBoxChannel.setObjectName("comboBoxChannel")
            self.settingView.ui.gridLayout_2.addWidget(self.settingView.ui.comboBoxChannel, 8, 1, 1, 2)

            self.settingView.ui.comboBoxRef.clear()
            self.settingView.ui.comboBoxRef.addItem('Default')
            for item in self.montages:
                self.settingView.ui.comboBoxRef.addItem(item.get('name'))
            if self.mont_idx > 0:
                self.settingView.ui.comboBoxRef.setCurrentIndex(self.mont_idx)
            self.settingView.ui.comboBoxRef.setCurrentIndex(self.mont_idx)
            self.settingView.ui.spinBoxMove.setValue(self.move_length)
            self.settingView.ui.spinBoxPaint.setValue(self.paint_length)
            self.settingView.ui.dbSpinSensitivity.setValue(self.sensitivity)

            self.settingView.setAttribute(Qt.WA_DeleteOnClose)
            self.settingView.setWindowTitle("绘图参数")
            self.settingView.setWindowModality(Qt.ApplicationModal)
            self.settingView.show()
            self.settingView.ui.comboBoxRef.currentTextChanged.connect(self.on_comboBoRef_clicked)
            self.settingView.ui.btnConfirm.clicked.connect(self.on_btnConfirmSetting_clicked)
            self.settingView.ui.btnExit.clicked.connect(self.on_btnExit_clicked)
        except Exception as e:
            print('on_btnSetting_clicked', e)

    def on_comboBoRef_clicked(self):
        try:
            montage = self.settingView.ui.comboBoxRef.currentText()
            mont_idx = self.settingView.ui.comboBoxRef.currentIndex()
            if montage == 'Default':
                channels = [x for x in self.channels_default]
            else:
                channels = [x for x in self.montages[mont_idx - 1]['channels']]
            filter = channels
            self.settingView.ui.comboBoxChannel = CheckableComboBox(self.settingView.ui.gbSettings, channels, filter ,self.channels_name)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(2)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.settingView.ui.comboBoxChannel.sizePolicy().hasHeightForWidth())
            self.settingView.ui.comboBoxChannel.setSizePolicy(sizePolicy)
            self.settingView.ui.comboBoxChannel.setObjectName("comboBoxChannel")
            self.settingView.ui.gridLayout_2.addWidget(self.settingView.ui.comboBoxChannel, 8, 1, 1, 2)
        except Exception as e:
            print('on_comboBoRef_clicked', e)

    # 根据绘图设置页面调整相应参数
    def on_btnConfirmSetting_clicked(self):
        try:
            self.sensitivity = float(self.settingView.ui.dbSpinSensitivity.text())
            self.type_filter = [x for x in self.settingView.ui.comboBoxSample.checkedItems]
            self.user_filter = [x for x in self.settingView.ui.comboBoxUser.checkedItems]
            self.channels = [x for x in self.settingView.ui.comboBoxChannel.checkedItems]
            self.montage = self.settingView.ui.comboBoxRef.currentText()
            self.mont_idx = self.settingView.ui.comboBoxRef.currentIndex()
            self.calc_sen(len(self.channels) + 1)
            self.paint_length = int(self.settingView.ui.spinBoxPaint.text())
            self.move_length = int(self.settingView.ui.spinBoxMove.text())
            self.scale = self.sen / self.sensitivity
            channels = self.channels
            for ch in channels:
                self.scales[ch] = self.scale
                self.labels_alpha[ch] = 1.
            if self.begin + self.paint_length > self.duration:
                self.end = self.duration
                self.begin = self.end - self.paint_length
            else:
                self.end = self.begin + self.paint_length
            self.settingView.close()
            self.remove_lines(channels)
            self.pick_channel = ''
            self.pick_sample_color = None
            self.pick_sample = None
            self.pick_labels = []

            self.status_annotate = False
            self.state_left = None
            self.state_right = None
            self.state_picked = None
            self.view.ui.btnStateAnnotate.setStyleSheet("")
            self.cursor = None
            self.cur_sample_index = 0
            self.init_SampleList()
            self.widget_from_main.setText('绘图长度(s): {}    移动长度(s): {}    灵敏度(µV/mm)：{}    参考方案：{}'.format(self.paint_length, self.move_length, self.sensitivity, self.montage))
            self.paint(self.data, self.begin, self.end, channels=channels, updateY=True)
        except Exception as e:
            print('on_btnConfirmSetting_clicked', e)

    def on_btnExit_clicked(self):
        self.settingView.close()

    # 状态显示/隐藏
    def on_btnShowInfo_clicked(self):
        try:
            if self.duration is None:
                return
            self.cancel_select()
            if self.is_status_showed:
                self.hide_status()
                self.is_status_showed = False
                self.view.ui.btnShowInfo.setText("状态显示")
            else:
                self.show_status()
                self.is_status_showed = True
                self.view.ui.btnShowInfo.setText("状态隐藏")
            self.init_SampleList()
        except Exception as e:
            print('on_btnShowInfo_clicked', e)

    # 点击上方时间条，跳转
    def on_axhscroll_clicked(self, begin=None):
        try:
            if self.duration is None:
                return
            if begin is None:
                begin = 0
            if begin >= self.duration - self.paint_length:
                self.end = self.duration
                self.begin = self.end - self.paint_length
            else:
                self.begin = begin
                self.end = self.begin + self.paint_length
            hour = int(self.begin / 3600)
            minute = int((self.begin % 3600) / 60)
            second = self.begin % 60
            self.view.ui.editTime.setTime(QTime(hour, minute, second))
        except Exception as e:
            print('on_axhscroll_clicked', e)

    # 响应时间框编辑，跳转到具体时间
    def timeChange(self):
        try:
            if self.duration is None:
                return
            time = self.view.ui.editTime.time()
            h = time.hour()
            m = time.minute()
            s = time.second()
            begin = h * 3600 + m * 60 + s
            if begin >= self.duration - self.paint_length:
                self.end = self.duration
                self.begin = self.end - self.paint_length
            else:
                self.begin = begin
                self.end = self.begin + self.paint_length
            # self.load_dataDynamical()

            size = 120
            num = math.ceil(self.duration / size)
            if self.begin == 0:
                cur_num = 1
            else:
                cur_num = math.ceil(self.begin / size)
            # 不超过60min且已分配内存
            if num <= 3 and self.index > 0:
                self.timeChangeUpdateUi()
                return
            # 超过60min且不需要调整
            if num > 3:
                if cur_num == self.index:
                    self.timeChangeUpdateUi()
                    return
                if self.index == 1 and cur_num == 2:
                    self.timeChangeUpdateUi()
                    return
                if self.index == 2 and cur_num == 1:
                    self.timeChangeUpdateUi()
                    return
                if self.index == num - 1 and cur_num == num:
                    self.timeChangeUpdateUi()
                    return
                if self.index == num and cur_num == num - 1:
                    self.timeChangeUpdateUi()
                    return

            REQdata = self.load_dataDynamical()
            if REQdata is None:
                return
            if self.downing % 2 == 1 or self.uping % 2 == 1:
                self.stop_thread(self.thread)
            self.view.setDisabled(True)
            self.mainMenubar.setDisabled(True)
            # self.view.ui.btnUp.setDisabled(True)
            # self.view.ui.btnDown.setDisabled(True)
            # self.view.ui.btnUping.setDisabled(True)
            # self.view.ui.btnDowning.setDisabled(True)
            # self.view.ui.btnBegin.setDisabled(True)
            # self.view.ui.btnEnd.setDisabled(True)
            # self.view.ui.editTime.setDisabled(True)
            msg = [self.check_id, self.file_id, REQdata]
            # self.client.mq_load_dataDynamical10(msg)
            self.client.as_load_dataDynamical10(msg)
        except Exception as e:
            print('timeChange', e)

    def on_btnUp_clicked(self, step=0):
        try:
            if self.duration is None:
                return
            if step != 0:
                if self.end == self.duration:
                    self.on_btnUping_clicked()
                    return True
                if self.end + step > self.duration:
                    self.end = self.duration
                    self.begin = self.end - self.paint_length
                else:
                    self.begin = self.begin + step
                    self.end = self.end + step
            elif self.end == self.duration:
                return True
            elif self.end + self.move_length > self.duration:
                self.end = self.duration
                self.begin = self.end - self.paint_length
            else:
                self.begin = self.begin + self.move_length
                self.end = self.end + self.move_length
            hour = int(self.begin / 3600)
            minute = int((self.begin % 3600) / 60)
            second = self.begin % 60
            self.view.ui.editTime.setTime(QTime(hour, minute, second))
            return False
        except Exception as e:
            print('on_btnUp_clicked', e)

    def on_btnUping_clicked(self):
        try:
            if self.duration is None:
                return
            self.uping = self.uping + 1
            if self.uping % 2 == 1:
                self.view.ui.btnDowning.setDisabled(True)
                self.view.ui.btnUping.setText("■")
                self.thread = threading.Thread(target=self.do_uping)
                self.thread.start()
            else:
                self.view.ui.btnDowning.setDisabled(False)
                self.view.ui.btnUping.setText(">>")
                self.stop_thread(self.thread)
        except Exception as e:
            print('on_btnUping_clicked', e)

    def do_uping(self):
        while True:
            time.sleep(1)
            if self.on_btnUp_clicked(self.move_length):
                self.stop_thread(self.thread)

    def on_btnBegin_clicked(self):
        try:
            if self.duration is None:
                return
            self.begin = 0
            self.end = self.begin + self.paint_length
            hour = int(self.begin / 3600)
            minute = int((self.begin % 3600) / 60)
            second = self.begin % 60
            self.view.ui.editTime.setTime(QTime(hour, minute, second))
        except Exception as e:
            print('on_btnBegin_clicked', e)

    def on_btnEnd_clicked(self):
        try:
            if self.duration is None:
                return
            self.end = self.duration
            self.begin = self.end - self.paint_length
            hour = int(self.begin / 3600)
            minute = int((self.begin % 3600) / 60)
            second = self.begin % 60
            self.view.ui.editTime.setTime(QTime(hour, minute, second))
        except Exception as e:
            print('on_btnEnd_clicked', e)

    def on_btnDown_clicked(self, step=0):
        try:
            if self.duration is None:
                return
            if step != 0:
                if self.begin == 0:
                    self.on_btnDowning_clicked()
                    return True
                if self.begin - step < 0:
                    self.begin = 0
                    self.end = self.begin + self.paint_length
                else:
                    self.begin = self.begin - step
                    self.end = self.end - step
            elif self.begin == 0:
                return True
            elif self.begin - self.move_length < 0:
                self.begin = 0
                self.end = self.paint_length
            else:
                self.begin = self.begin - self.move_length
                self.end = self.end - self.move_length
            hour = int(self.begin / 3600)
            minute = int((self.begin % 3600) / 60)
            second = self.begin % 60
            self.view.ui.editTime.setTime(QTime(hour, minute, second))
            return False
        except Exception as e:
            print('on_btnDown_clicked', e)

    def on_btnDowning_clicked(self):
        try:
            if self.duration is None:
                return
            self.downing = self.downing + 1
            if self.downing % 2 == 1:
                self.view.ui.btnUping.setDisabled(True)
                self.view.ui.btnDowning.setText("■")
                self.thread = threading.Thread(target=self.do_downing)
                self.thread.start()
            else:
                self.view.ui.btnUping.setDisabled(False)
                self.view.ui.btnDowning.setText("<<")
                self.stop_thread(self.thread)
        except Exception as e:
            print('on_btnDowning_clicked', e)

    def do_downing(self):
        while True:
            time.sleep(1)
            if self.on_btnDown_clicked(self.move_length):
                self.stop_thread(self.thread)

    # 设置参考线
    def on_btnRuler_clicked(self):
        try:
            if self.axes is None:
                return
            if self.cursor is None:
                self.cursor = Cursor(self.axes, useblit=True, color='red',
                                     linewidth=1, horizOn=False)
            else:
                self.cursor = None
            self.canvas.draw()
        except Exception as e:
            print('on_btnRuler_clicked')

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

    def stop_thread(self, thread):
        try:
            self._async_raise(thread.ident, SystemExit)
        except Exception as e:
            print('stop_thread', e)

    def stopRolling(self):
        if self.downing % 2 == 1:
            self.on_btnDowning_clicked()
        if self.uping % 2 == 1:
            self.on_btnUping_clicked()

    # 获取当前窗口内的样本
    def window_sampleList(self, begin, end):
        try:
            start = begin * self.sampling_rate
            end = end * self.sampling_rate
            self.show_sample_index = -1
            window_samples = []
            count = 0
            for idx, item in enumerate(self.sample_list):
                if item[2] <= start:
                    count = idx
                    continue
                elif item[1] >= end:
                    break
                window_samples.append(item)
                # 获取当前窗口第一个样本索引
                if self.show_sample_index < 0:
                    self.show_sample_index = idx
            # 若当前窗口无样本
            if self.show_sample_index < 0:
                self.show_sample_index = count
            return window_samples
        except Exception as e:
            print('window_sampleList', e)

    # self.sample_list按起始点排序，二分查找start对应样本的插入位置
    def bin_search(self, target):
        try:
            left = 0
            right = len(self.sample_list)
            while left < right:
                mid = (left + right) // 2
                if self.sample_list[mid][1] < target:
                    left = mid + 1
                else:
                    right = mid
            return left
        except Exception as e:
            print('bin_search', e)

    # 样本列表右键菜单
    def sampleList_menu(self, pos):
        try:
            row = -1
            row = self.view.ui.tableWidget.currentRow()
            if row == -1:
                return
            self.rclick_pick_sample = self.sample_list[row]
            if self.rclick_pick_sample[0] == 'all':
                return
            self.Menu.exec_(self.view.ui.tableWidget.mapToGlobal(pos))
        except Exception as e:
            print('sampleList_menu', e)

    def cancel_menu(self):
        try:
            self.rclick_pick_sample = None
            self.pick_channel = ''
            self.remove_lines(['pp', 'pickedsegment'])
            if self.pick_sample is not None:
                self.pick_sample.set_color(self.pick_sample_color)
                self.canvas.draw()
                self.pick_sample_color = None
                self.pick_sample = None
                self.view.show_sample_detail()
            self.restore_pre_sample_color(self.cur_sample_index)
            self.labels_alpha.update((k, 1.) for k in self.labels_alpha)
            self.pick_labels = []
            self.focus_lines()
            return
        except Exception as e:
            print('cancel_menu', e)

    # 样本列表右键菜单-删除样本
    def del_label(self):
        try:
            sample = self.rclick_pick_sample
            label = '|'.join([str(x) for x in sample[:]])
            idx = self.sample_list.index(sample)
            pick_channel, start, end, mid, mtype_id = sample[0], sample[1], sample[2], sample[3], sample[4]
            self.client.del_labelListInfo([mid, self.check_id, self.file_id, start, pick_channel, end, mtype_id, idx, label])
        except Exception as e:
            print('del_label', e)

    def del_labelListInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                idx = REPData[2][7]
                label = REPData[2][8]
                self.remove_lines([label], sample=True)
                # 删除波形样本
                self.view.show_sample_detail()
                self.pick_channel = ''
                self.pick_sample_color = None
                self.pick_sample = None
                self.labels_alpha.update((k, 1.) for k in self.labels_alpha)
                self.pick_labels = []
                self.focus_lines()
                self.sample_list.pop(idx)
                self.view.ui.tableWidget.removeRow(idx)
                self.view.ui.tableWidget.repaint()
                QMessageBox.information(self, "成功", "删除成功")
                self.is_reload_controller.emit("clearLabelController")
            else:
                QMessageBox.information(self, "错误", "删除失败")
                return
        except Exception as e:
            print('del_labelListInfoRes', e)

    # 样本列表右键菜单-修改样本类型
    def update_label(self, type):
        try:
            sample = self.rclick_pick_sample
            label = '|'.join([str(x) for x in sample[:]])
            idx = self.sample_list.index(sample)
            pick_channel, start, end, mid, mtype_id = sample[0], sample[1], sample[2], sample[3], sample[4]
            uid = self.client.tUser[0]
            utype_id, utype_name = type[0], type[1]
            self.client.update_labelListInfo12([self.model_id, self.check_id, self.file_id, start, pick_channel,
                                                  end, mtype_id, uid, utype_id, idx, label])
        except Exception as e:
            print('update_label', e)

    def update_labelListInfo12Res(self, REPData):
        try:
            if REPData[0] == '1':
                idx = REPData[2][9]
                pick_channel = REPData[2][4]
                start = REPData[2][3]
                end = REPData[2][5]
                mid = REPData[2][0]
                mtype_id = REPData[2][6]
                uid = REPData[2][7]
                utype_id = REPData[2][8]
                label = REPData[2][10]
                cur_sample = (pick_channel, start, end, mid, mtype_id, uid, utype_id)
                s_label = '|'.join([str(x) for x in cur_sample[:]])
                color = 'blue'
                self.remove_lines([label], sample=True)
                self.sample_list[idx] = cur_sample
                if not (end <= self.begin * self.sampling_rate or start >= self.end * self.sampling_rate):
                    self.paint_sample(self.data, start, end, pick_channel, color, s_label)
                    self.show_jump_sample_detail(cur_sample)
                self.pick_channel = ''
                self.pick_sample_color = None
                self.pick_sample = None
                self.labels_alpha.update((k, 1.) for k in self.labels_alpha)
                self.pick_labels = []
                self.focus_lines()
                for c in range(3):
                    if c == 0:
                        item = QTableWidgetItem(
                            str(time.strftime('%H:%M:%S', time.gmtime(int(self.sample_list[idx][1] / self.sampling_rate)))))
                    elif c == 1:
                        mtype_name = self.type_name_dic[mtype_id]
                        item = QTableWidgetItem(mtype_name)
                    elif c == 2:
                        utype_name = self.type_name_dic[utype_id]
                        item = QTableWidgetItem(utype_name)
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(8)
                    item.setFont(font)
                    self.view.ui.tableWidget.setItem(idx, c, item)
                self.view.ui.tableWidget.repaint()
        except Exception as e:
            print('update_labelListInfo12Res', e)

    def exit(self):
        try:
            self.client.getAssessInfoResSig.disconnect()
            self.client.getModelIdNameResSig.disconnect()
            self.client.assessClassifierInfoPagingResSig.disconnect()
            self.client.assessOpenEEGFileResSig.disconnect()
            self.client.assess_load_dataDynamicalResSig.disconnect()
            self.client.update_labelListInfoResSig.disconnect()
            self.client.update_labelListInfo12ResSig.disconnect()
            self.client.update_state_labelListInfoResSig.disconnect()
            self.client.del_labelListInfoResSig.disconnect()
            self.client.del_labelListInfo15ResSig.disconnect()
            self.client.del_labelListInfo16ResSig.disconnect()
        except Exception as e:
            print('exit', e)