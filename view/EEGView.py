import math

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.Qt import *
import time
import matplotlib as mpl

from view.EEG_form.form import Ui_EEGView


class EEGView(QWidget):
    # 点击的点
    PICK_FIRST = 1
    PICK_SECOND = 2
    PICK_NO_DOT = 0

    # 点击的图形
    PICK_AXES = 1
    PICK_AXHSCROLL = 2
    PICK_NO_AX = 0

    # 标注状态
    STATE_ANNOTATE = 0
    WAVE_ANNOTATE = 1
    EVENT_ANNOTATE = 2
    NO_ANNOTATE = 3

    # 样本增加和修改
    ADD_SAMPLE = 1
    UPDATE_SAMPLE = 2
    NO_ACTION = 0

    def __init__(self):
        super().__init__()
        self.labelBit = None
        self.ui = Ui_EEGView()
        self.ui.setupUi(self)

        self.cursor = None
        # 类型数据
        self.type_info = []
        # 当前标注状态（波形、状态、事件）
        self.annotate = EEGView.NO_ANNOTATE
        # 是否状态显示
        self.is_status_showed = True
        self.is_waves_showed = True
        self.is_Event_showed = True
        # 被选中的通道
        self.pick_labels = []
        self.pick_first = None
        self.pick_second = None
        self.cur_sample_index = -1
        self.sample_info = []
        self.waves = [] #当前屏所有波形
        self.states = []#当前屏所有状态
        self.events = [] #当前屏所有事件
        self.channels_alpha = {}
        self.pick_channel = None
        self.begin = None
        self.sample_rate = None
        self.end = None
        self.User = None
        self.data = None
        self.labels = [] #当前屏所有样本
        self.filterlist = [] #当前屏显示的样本（波形、状态、事件随机组合）
        self.channels_name = []
        self.userInfo = None
        self.state_left = None
        self.state_right = None
        self.state_left_line = None
        self.state_right_line = None
        self.eventline = None
        self.lenTime = None
        self.paint_length = None
        self.scroll_position = None
        self.winTime = 0
        self.sensitivity = 10
        self.showSecondLine = True
        self.subtractAverage = False
        self.time_lines = []
        self.wave_lines = [] #绘制出的波形
        self.state_lines = [] #绘制出的状态
        self.Event_lines = [] #绘制出的事件

        self.axHscrollSpan = []
        self.sen = 0
        self.plottedData = None

        self.secondsSpan = 30
        self.createPaintTools()

    # 减平均
    def changeSubtractAverage(self):
        self.subtractAverage = self.subtractAverage is False
        self.filterlist = list(self.labels)
        self.removeLines()
        self.processChan()
        self.paintEEG()
        self.paintWaves()
        self.paintStates()
        self.paintEvents()
        self.removeTimeLine()
        self.paintTimeLine()
        if self.pick_first is not None:
            if self.pick_second is None:
                if self.pick_first >= self.begin * self.sample_rate // self.dawnSample and self.pick_first < self.end * self.sample_rate // self.dawnSample:
                    self.axes.plot(self.pick_X, self.pick_Y, 'ro', label="pp", markersize=4)
            else:
                if (
                        self.pick_first >= self.begin * self.sample_rate // self.dawnSample and self.pick_first < self.end * self.sample_rate // self.dawnSample) or (
                        self.pick_second >= self.begin * self.sample_rate // self.dawnSample and self.pick_second < self.end * self.sample_rate // self.dawnSample) or (
                        self.pick_first < self.begin * self.sample_rate // self.dawnSample and self.pick_second >= self.end * self.sample_rate // self.dawnSample):
                    self.paintAWave(max(self.pick_first - self.begin * self.sample_rate // self.dawnSample, 0),
                                    min(self.winTime * self.sample_rate // self.dawnSample,
                                        self.pick_second - self.begin * self.sample_rate // self.dawnSample),
                                    self.pick_label, 'pickedsegment', 'red')

        self.canvas.draw()
        self.showLabelList()
        self.showlabelInfo()

    # 初始化View
    def initView(self, type_info, channels, lenTime, sampleRate, patientInfo, fileName, measureDate, startTime, endTime, labelBit, dawnSample, typeEEG, montage, sampleFilter, channels_index):
        try:
            # 处理单通道名，获取每个导联所映射的通道
            self.channels_index = channels_index
            self.typeEEG = typeEEG  # True:颅内脑电 False：头皮脑电
            #refList：参考方案列表，即montage
            self.refList = dict(montage)
            self.curRef = 'default'

            self.allChannel = {key: True for key in channels}
            self.sampleFilter = sampleFilter
            #平均参考时计算平均时需要排除的通道
            self.exclude_av = ['Ldelt1', 'Ldelt2', 'Rdelt1', 'Rdelt2', 'A1', 'A2', 'M1', 'M2', 'LOC', 'ROC',
                               'CHIN1', 'CHIN2', 'ECGL', 'ECGR', 'LAT1', 'LAT2', 'RAT1', 'RAT2',
                               'CHEST', 'ABD', 'FLOW', 'SNORE', 'DIF5', 'DIF6']
            self.type_info = type_info
            self.dawnSample = dawnSample
            self.begin = 0
            self.end = self.winTime
            self.lenTime = lenTime
            self.labelBit = labelBit
            self.sample_rate = sampleRate
            self.popMenu1 = QMenu(self.canvas)
            self.popMenu2 = QMenu(self.canvas)
            self.popMenu3 = QMenu(self.canvas)
            self.updateYAxis(channels)
            self.setAxHscroll()
            self.showPatientInfo(patientInfo, fileName,
                                      measureDate, startTime,
                                      endTime)
        except Exception as e:
            print("initView", e)

    # 初始化绘图工具
    def createPaintTools(self):
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.ui.glCanvas.addWidget(self.canvas, 0, 0, 1, 1)
        self.fig.subplots_adjust(0.125, 0.01,  0.9, 0.95)
        self.axes = plt.subplot2grid((33, 1), (2, 0), rowspan=30)
        self.ax_hscroll = plt.subplot2grid((33, 1), (0, 0), rowspan=1)

    # 计算绘图区域物理长度
    def calcSen(self):
        axesL = self.axes.figure.subplotpars.left
        axesR = self.axes.figure.subplotpars.right
        axesT = self.axes.figure.subplotpars.top
        axesB = self.axes.figure.subplotpars.bottom
        x_fraction, y_fraction = axesR - axesL, axesT - axesB
        figureSize = self.ui.listView.size()
        figureWidth = figureSize.width()
        figureHeight = figureSize.height()
        screen = QApplication.primaryScreen()
        self.xDPI = screen.physicalDotsPerInchX()
        self.yDPI = screen.physicalDotsPerInchY()
        figureWidthMM = (figureWidth / self.xDPI) * 25.4
        figureHeightMM = (figureHeight / self.yDPI) * 25.4
        self.axesXWidthMM = x_fraction * figureWidthMM
        self.axesYWidthMM = y_fraction * figureHeightMM
        return self.secondsSpanChange()

    # 改变秒跨度操作
    def secondsSpanChange(self):
        self.secondsSpan = int(self.ui.secondsSpan.lineEdit().text())
        self.winTime = int(round(self.axesXWidthMM / self.secondsSpan))
        px = int(round(self.secondsSpan * self.xDPI / 25.4))
        self.nDotWin = self.winTime * px
        return self.winTime, px

    def sensitivityChange(self):
        self.sensitivity = int(self.ui.sensitivity.lineEdit().text())
        self.filterlist = list(self.labels)
        self.removeLines()
        self.processChan()
        self.paintEEG()
        self.paintWaves()
        self.paintStates()
        self.paintEvents()
        self.removeTimeLine()
        self.paintTimeLine()
        if self.pick_first is not None:
            if self.pick_second is None:
                if self.pick_first >= self.begin * self.sample_rate // self.dawnSample and self.pick_first < self.end * self.sample_rate // self.dawnSample:
                    self.axes.plot(self.pick_X, self.pick_Y, 'ro', label="pp", markersize=4)
            else:
                if (
                        self.pick_first >= self.begin * self.sample_rate // self.dawnSample and self.pick_first < self.end * self.sample_rate // self.dawnSample) or (
                        self.pick_second >= self.begin * self.sample_rate // self.dawnSample and self.pick_second < self.end * self.sample_rate // self.dawnSample) or (
                        self.pick_first < self.begin * self.sample_rate // self.dawnSample and self.pick_second >= self.end * self.sample_rate // self.dawnSample):
                    self.paintAWave(max(self.pick_first - self.begin * self.sample_rate // self.dawnSample, 0),
                                    min(self.winTime * self.sample_rate // self.dawnSample,
                                        self.pick_second - self.begin * self.sample_rate // self.dawnSample),
                                    self.pick_label, 'pickedsegment', 'red')

        self.canvas.draw()
        self.showLabelList()
        self.showlabelInfo()

    # 设置移动长度
    def setMoveLength(self, moveLength):
        self.moveLength = moveLength
        self.ui.moveLength.setCurrentText(str(moveLength))

    # 自动播放时停止绘制样本
    def stopPaintLabel(self):
        self.curShowWaves = self.is_waves_showed
        self.curShowStates = self.is_status_showed
        self.curshowEvents =self.is_Event_showed
        self.is_waves_showed = False
        self.is_status_showed = False
        self.is_Event_showed =False

    # 开始绘制样本
    def startPaintLabel(self):
        self.is_waves_showed = self.curShowWaves
        self.is_status_showed = self.curShowStates
        self.is_Event_showed = self.curshowEvents
        self.paintWaves()
        self.paintStates()
        self.paintEvents()
        self.canvas.draw()
        self.showLabelList()

    # 后退一屏
    def onBtnDownClicked(self):
        self.begin += self.moveLength
        self.end += self.moveLength
        cmd = True
        if self.end > self.lenTime:
            self.begin = self.lenTime - self.winTime
            self.end = self.lenTime
            cmd = False
        self.changeTime()
        self.changeAxStatus()
        return cmd, self.begin * self.sample_rate // self.dawnSample

    # 前进一屏
    def onBtnUpClicked(self):
        self.begin -= self.moveLength
        self.end -= self.moveLength
        cmd = True
        if self.begin < 0:
            self.begin = 0
            self.end = self.winTime
            cmd = False
        self.changeTime()
        self.changeAxStatus()
        return cmd, self.begin * self.sample_rate // self.dawnSample

    # 时间改变
    def timeChange(self, begin):
        if begin < 0 or begin + self.winTime > self.lenTime:
            self.view.ui.editTime.setText("00:00:00")
            self.beign = 0
            self.end = self.winTime
        else:
            self.begin = begin
            self.end = begin + self.winTime
        return self.begin * self.sample_rate // self.dawnSample

    # 更新x轴
    def updateXAxis(self):
        self.axes.set_xlim([self.begin, self.end])
        self.axes.set_xticks(np.arange(self.begin, self.end + 1, 1))
        xlabels = [time.strftime('%H:%M:%S', time.gmtime(i))
                   for i in range(self.begin, self.end + 1)]
        self.axes.set_xticklabels(xlabels)
        for xtl in self.axes.get_xticklabels():
            xtl.set_fontsize(10)

    # 改变秒线状态
    def changeSecondsLine(self):
        self.showSecondLine = self.showSecondLine is False
        if self.showSecondLine:
            self.paintTimeLine()
        else:
            self.removeTimeLine()
        self.canvas.draw()

    # 绘制秒线
    def paintTimeLine(self):
        if self.showSecondLine:
            for x in range(self.begin, self.end + 1):
                self.time_lines.append(self.axes.vlines(x, 0, 200, colors='black', alpha=0.7))

    # 删除秒线
    def removeTimeLine(self):
        for line in self.time_lines:
            line.remove()
        self.time_lines.clear()

    # 绘制脑电信号
    def paintEEG(self):
        x = np.linspace(self.begin, self.end, (self.end - self.begin) * self.sample_rate // self.dawnSample)
        for i in range(len(self.channels_name)):
            self.axes.plot(x, self.plottedData[i], color='black', label=self.channels_name[i], picker=True,
                           alpha=self.channels_alpha[self.channels_name[i]], linewidth=0.7)

    # 更新下采样和窗口时间
    def reCalc(self, nDotSec, nSecWin):
        self.dawnSample = 1 if nDotSec >= self.sample_rate else int(round(self.sample_rate / nDotSec))
        self.lenWin = nSecWin * self.sample_rate // self.dawnSample
        self.end = self.begin + self.winTime
        if self.end > self.lenTime:
            self.begin = self.lenTime - self.winTime
            self.end = self.lenTime
        readFrom = self.begin * self.sample_rate
        return self.dawnSample, self.lenWin, readFrom

    # 更新样本
    def updateSamples(self, readFrom, readTo, case, sample_info):
        if case == 1:
            self.sample_info = sample_info
        elif case == 2:
            idx = 0
            while idx < len(self.sample_info) and self.sample_info[idx][1] < readFrom // self.sample_rate:
                idx += 1
            self.sample_info = self.sample_info[:idx] + sample_info
        elif case == 3:
            idx = len(self.sample_info) - 1
            while idx >= 0 and self.sample_info[idx][1] >= readTo // self.sample_rate:
                idx -= 1
            self.sample_info = sample_info + self.sample_info[idx + 1:]

    # def remove_mean(data, lowlim, highlim, g_submean):
    #     """
    #     如果 g.submean 是 'on'，从信号中去除均值。
    #
    #     参数:
    #     data -- EEG信号数据，格式为 (通道数, 时间点数)
    #     lowlim -- 数据开始点
    #     highlim -- 数据结束点
    #     g_submean -- 是否去均值操作
    #
    #     返回:
    #     data_no_mean -- 去均值后的EEG数据
    #     """
    #     if g_submean == 'on':
    #         # 计算每个通道在指定区间的均值
    #         mean_data = np.mean(data[:, lowlim:highlim], axis=1)
    #         # 从每个通道的信号中减去均值
    #         data_no_mean = data - mean_data[:, np.newaxis]
    #     else:
    #         data_no_mean = data  # 不进行去均值操作
    #
    #     return data_no_mean

    # 更新当前屏
    def refreshWin(self, data, labels):
        try:
            self.data = data
            self.labels = labels
            self.filterlist = list(self.labels)
            self.removeLines()
            self.updateXAxis()
            self.processChan()
            self.paintEEG()
            self.filterSamples()
            self.paintWaves()
            self.paintStates()
            self.paintEvents()
            self.removeTimeLine()
            self.paintTimeLine()
            if self.pick_first is not None:
                if self.pick_second is None:
                    if self.pick_first >= self.begin * self.sample_rate // self.dawnSample and self.pick_first < self.end * self.sample_rate // self.dawnSample:
                        self.axes.plot(self.pick_X, self.pick_Y, 'ro', label="pp", markersize=4)
                else:
                    if (self.pick_first >= self.begin * self.sample_rate // self.dawnSample and self.pick_first < self.end * self.sample_rate // self.dawnSample) or (self.pick_second >= self.begin * self.sample_rate // self.dawnSample and self.pick_second < self.end * self.sample_rate // self.dawnSample) or (self.pick_first < self.begin * self.sample_rate // self.dawnSample and self.pick_second >= self.end * self.sample_rate // self.dawnSample):
                        self.paintAWave(max(self.pick_first - self.begin * self.sample_rate // self.dawnSample, 0),
                                        min(self.winTime * self.sample_rate // self.dawnSample, self.pick_second - self.begin * self.sample_rate // self.dawnSample),
                                        self.pick_label, 'pickedsegment', 'red')

            self.canvas.draw()
            self.showLabelList()
            self.showlabelInfo()
        except Exception as e:
            print("refreshWin", e)

    # 改变波形显示
    def changeShowWave(self):
        self.is_waves_showed = self.is_waves_showed is False
        self.ui.hideWave.setChecked(self.is_waves_showed)
        if self.is_waves_showed is False and self.ui.gblabelbtn1.isChecked():
            self.ui.gblabelbtn4.setChecked(True)
            self.ui.gblabelbtn1.setDisabled(True)
        else:
            self.ui.gblabelbtn1.setDisabled(False)
        if self.is_waves_showed:
            self.paintWaves()
        else:
            self.removeLines(self.wave_lines, True)
            self.wave_lines = []
            self.resetPickLabels()
            self.focusLines()
        self.canvas.draw()
        self.restorePreSampleColor()
        self.showLabelList()
        self.ui.tableWidget.clearSelection()

    # 改变状态显示
    def changeShowState(self):
        self.is_status_showed = self.is_status_showed is False
        self.ui.hideState.setChecked(self.is_status_showed)
        if self.is_status_showed is False and self.ui.gblabelbtn2.isChecked():
            self.ui.gblabelbtn4.setChecked(True)
            self.ui.gblabelbtn2.setDisabled(True)
        else:
            self.ui.gblabelbtn2.setDisabled(False)
        if self.is_status_showed:
            self.paintStates()
        else:
            for state in self.state_lines:
                state[1].remove()
            self.cancelStateAnnotate()
            self.state_lines = []
            self.resetPickLabels()
            self.focusLines()
        self.canvas.draw()
        self.restorePreSampleColor()
        self.showLabelList()
        self.ui.tableWidget.clearSelection()
    def changeShowEvent(self):
        self.is_Event_showed = self.is_Event_showed is False
        self.ui.hideEvent.setChecked(self.is_Event_showed)
        if self.is_Event_showed is False and self.ui.gblabelbtn3.isChecked():
            self.ui.gblabelbtn4.setChecked(True)
            self.ui.gblabelbtn3.setDisabled(True)
        else:
            self.ui.gblabelbtn3.setDisabled(False)
        if self.is_Event_showed:
            self.paintEvents()
        else:
            for event in self.Event_lines:
                event[1].remove()
            self.Event_lines = []
            self.resetPickLabels()
            self.focusLines()
        self.canvas.draw()
        self.restorePreSampleColor()
        self.showLabelList()
        self.ui.tableWidget.clearSelection()

    # 显示样本列表信息
    def showLabelList(self):
        self.filterlist=list(self.labels)
        if self.is_waves_showed is False:
            for sample in self.filterlist.copy():
                if sample[0] != 'all' and sample[1] != sample[2]:
                    self.filterlist.remove(sample)
        if self.is_status_showed is False:
            for sample in self.filterlist.copy():
                if sample[0] == 'all' and sample[1] != sample[2]:
                    self.filterlist.remove(sample)
        if self.is_Event_showed is False:
            for sample in self.filterlist.copy():
                if sample[0] == 'all' and sample[1] == sample[2]:
                    self.filterlist.remove(sample)
        itemName = ['开始时间', '样本类型']
        col_num = 2
        self.ui.tableWidget.setColumnCount(col_num)
        for i in range(col_num):
            header_item = QTableWidgetItem(itemName[i])
            font = header_item.font()
            font.setPointSize(8)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            self.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
        self.ui.tableWidget.horizontalHeader().setHighlightSections(False)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        row_num = len(self.filterlist)
        self.ui.tableWidget.setRowCount(row_num)
        for r in range(row_num):
            for c in range(col_num):
                if c == 0:
                    item = QTableWidgetItem(
                        str(time.strftime('%H:%M:%S',
                                          time.gmtime(int(self.filterlist[r][1]/(self.sample_rate/self.dawnSample))))))
                else:
                    type_name = ""
                    for type in self.type_info:
                        if type[0] == self.filterlist[r][3]:
                            type_name = type[1]
                            break
                    item = QTableWidgetItem(str(type_name))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                font.setPointSize(8)
                item.setFont(font)
                self.ui.tableWidget.setItem(r, c, item)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.resizeRowsToContents()

    # 绘制当前屏幕状态
    def paintStates(self):
        if self.is_status_showed is False:
            return
        keys = [x[0] for x in self.type_info]
        for state in self.states:
            idx = keys.index(state[3])
            description = self.type_info[idx][3]
            type_name = self.type_info[idx][1]
            if description == '正常状态':
                color = 'green'
            elif description == '异常状态':
                color = 'green'
            else:
                color = 'green'#'dodgerblue'
            self.paintAState(state, color)

    # 绘制一个状态
    def paintAState(self, state, color):
        label = str(state[0]) + "|" + str(state[1]) + "|" + str(state[2]) + "|" + str(state[3])
        x0 = state[1]/(self.sample_rate//self.dawnSample)
        x1 = state[2]/(self.sample_rate//self.dawnSample)
        self.state_lines.append([label, self.axes.axvspan(x0, x1, label=label, facecolor=color, alpha=0.3, picker=True)])

    def paintEvents(self):
        if self.is_Event_showed is False:
            return
        for event in self.events:
            color = 'orange'
            start = int(event[1]) * self.dawnSample / self.sample_rate
            # start = (event[1] - (self.begin * self.sample_rate // self.dawnSample)) if event[1] > (
            #              self.begin * self.sample_rate // self.dawnSample) else 0
            label = str(event[0]) + "|" + str(event[1]) + "|" + str(event[2]) + "|" + str(event[3])
            self.paintAEvent(start, label, color)

    def paintAEvent(self, start, label, color):
        self.Event_lines.append([label, self.axes.vlines(start, 0, 200, color=color)])

    # 过滤样本
    def filterSamples(self):
        self.waves = []
        self.states = []
        self.events = []
        for sample in self.labels:
            if sample[0] == 'all' and sample[1] != sample[2]:
                self.states.append(sample)
            elif sample[0] == 'all' and sample[1] == sample[2]:
                self.events.append(sample)
            elif sample[0] != 'all':
                self.waves.append(sample)

    # 绘制当前屏幕波形
    def paintWaves(self):
        if self.is_waves_showed is False:
            return
        for wave in self.waves:
            color = 'blue'
            l = (wave[1] - (self.begin * self.sample_rate // self.dawnSample)) if wave[1] > (self.begin * self.sample_rate // self.dawnSample) else 0
            r = (wave[2] - (self.begin * self.sample_rate // self.dawnSample)) if wave[2] < (self.end * self.sample_rate // self.dawnSample) else (self.end - self.begin) * (self.sample_rate//self.dawnSample)
            label = str(wave[0]) + "|" + str(wave[1]) + "|" + str(wave[2]) + "|" + str(wave[3])
            self.paintAWave(l, r, wave[0], label, color)

    # 更新Y轴
    def updateYAxis(self, channels_name):
        self.channels_name = []
        for channel in channels_name:
            ch0 = channel.split('-')[0]
            ch1 = channel.split('-')[1]
            if self.channels_index.get(ch0) is not None and (ch1.upper() == 'REF' or ch1.upper() == 'AV' or self.channels_index.get(ch1) is not None):
                self.channels_name.append(channel)
        self.resetPickLabels()
        max_y = len(self.channels_name) + 1
        # self.axes.clear()
        self.axes.set_ylim([0, max_y])
        self.axes.set_yticks(range(max_y))
        self.axes.set_yticklabels(['Reset'] + self.channels_name)
        for ytl in self.axes.get_yticklabels():
            ytl.set_picker(True)
            ytl.set_fontsize(10)
        self.axes.invert_yaxis()
        self.fig.subplots_adjust(left=0.07)
        self.fig.subplots_adjust(right=0.97)
        self.canvas.draw()

    def setAxHscroll(self):
        self.ax_hscroll.set_xlim(0, self.lenTime)
        self.ax_hscroll.get_yaxis().set_visible(False)
        hsel_patch = mpl.patches.Rectangle((0, 0), self.lenTime,
                                           1,
                                           edgecolor='k',
                                           facecolor=(0.75, 0.75, 0.75),
                                           alpha=0.25, linewidth=1,
                                           clip_on=False)
        self.ax_hscroll.add_patch(hsel_patch)
        hxticks = np.linspace(0, self.lenTime, 11)
        self.ax_hscroll.set_xticks(hxticks)
        hxlabels = [time.strftime('%H:%M:%S', time.gmtime(int(hxticks[i])))
                    for i in range(0, 11)]
        self.ax_hscroll.set_xticklabels(hxlabels)
        for xhtl in self.ax_hscroll.get_xticklabels():
            xhtl.set_fontsize(10)
        self.paintLabelBit()

    # 绘制时间轴上样本信息
    def paintLabelBit(self):
        for span in self.axHscrollSpan:
            span.remove()
        self.axHscrollSpan = []

        l = 0
        while l <= self.nDotWin:
            if self.labelBit[l]:
                r = l + 1
                while r <= self.nDotWin and self.labelBit[r]:
                    r += 1
                self.axHscrollSpan.append(self.ax_hscroll.axvspan(l * self.lenTime / self.nDotWin, (r - 1) * self.lenTime / self.nDotWin, facecolor="green", alpha=0.5))
                l = r
            else:
                l += 1

    # 判断点击对象
    def clickAxStatus(self, ax):
        if ax == self.axes:
            return EEGView.PICK_AXES
        elif ax == self.ax_hscroll:
            return EEGView.PICK_AXHSCROLL
        return EEGView.PICK_NO_AX

    # 时间轴点击事件
    def onAxhscrollClicked(self, x):
        if x + self.winTime <= self.lenTime:
            self.begin = x
            self.end = x + self.winTime
        else:
            self.begin = max(0, self.lenTime - self.winTime)
            self.end = self.lenTime
        self.changeAxStatus()
        return self.begin * self.sample_rate // self.dawnSample

    # 改变时间轴当前屏幕位置浮标
    def changeAxStatus(self):
        try:
            if self.scroll_position is not None:
                self.scroll_position.remove()
            self.scroll_position = self.ax_hscroll.axvline(self.begin, color='r', linewidth=0.5)
            self.canvas.draw()
        except Exception as e:
            print("changeAxStatus", e)

    # 判断是否处于波形标注且显示波形
    def isinWave(self):
        return self.annotate == EEGView.WAVE_ANNOTATE and self.is_waves_showed is True

    #是否处于事件标注
    def isinEvent(self):
        return self.annotate == EEGView.EVENT_ANNOTATE and self.is_Event_showed is True

    def isinState(self):
        return self.annotate == EEGView.STATE_ANNOTATE

    # 重置选中样本
    def resetPickLabels(self):
        self.pick_labels = self.channels_name
        for channel in self.channels_name:
            self.channels_alpha[channel] = 1
        self.removeLines(['pp', 'pickedsegment'])
        self.pick_first = None
        self.pick_second = None

    # 取消状态标注
    def cancelStateAnnotate(self):
        self.state_left = None
        if self.state_left_line is not None:
            self.state_left_line.remove()
            self.state_left_line = None
        self.state_right = None
        if self.state_right_line is not None:
            self.state_right_line.remove()
            self.state_right_line = None
        self.canvas.draw()

    # 取消波形标注
    def cancelWaveAnnotate(self):
        self.pick_channel = None
        self.pick_first = None
        self.pick_second = None
        self.removeLines(['pp', 'pickedsegment'])
        if self.restore_pre_sample_color():
            self.cur_sample_index = -1
            self.showlabelInfo()
        self.pick_labels = []
        self.focus_lines()

    # 判断选中标签
    def checkPickLabels(self, pl):
        if len(self.pick_labels) == len(self.channels_name):
            self.pick_labels = [pl]
            for channel in self.channels_name:
                self.channels_alpha[channel] = 0.075
            self.channels_alpha[pl] = 1
        elif pl in self.pick_labels:
            if len(self.pick_labels) == 1:
                self.resetPickLabels()
            else:
                self.pick_labels.remove(pl)
                self.channels_alpha[pl] = 0.075
        else:
            self.pick_labels.append(pl)
            self.channels_alpha[pl] = 1
        self.removeLines(['pp', 'pickedsegment'])
        self.pick_first = None
        self.pick_second = None

    # 删除line对象
    def removeLines(self, ch=None, sample=False):
        if (ch is None or len(ch) == 0) and sample is False:
            for state in self.state_lines:
                state[1].remove()
            self.state_lines = []
            self.wave_lines = []
            lines = self.axes.get_lines()
            for l in lines:
                l.remove()
            return
        lines = self.axes.get_lines()
        for l in lines:
            label = l.get_label() if sample else l.get_label().split('|')[0]
            if label in ch:
                l.remove()

    # 判断点击第几个点
    def clickPointStatus(self, label):
        if self.pick_first is None:
            return EEGView.PICK_FIRST
        elif label == self.pick_channel:
            return EEGView.PICK_SECOND
        return EEGView.PICK_NO_DOT

    # 绘制状态线
    def drawStateLine(self, event):
        if self.annotate != EEGView.STATE_ANNOTATE or self.is_status_showed is False:
            return
        x, y = event.xdata, event.ydata
        if self.state_left is None:
            self.state_left = int(x * self.sample_rate)
            self.state_left_line = self.axes.vlines(
                self.state_left / self.sample_rate, 0, 200, color='red')
        elif self.state_right is None:
            self.state_right = int(x * self.sample_rate)
            self.state_right_line = self.axes.vlines(
                self.state_right / self.sample_rate, 0, 200, color='red')
        else:
            mid = (self.state_left + self.state_right) // 2
            if (x * self.sample_rate) < mid:
                self.state_left_line.remove()
                self.state_left = int(x * self.sample_rate)
                self.state_left_line = self.axes.vlines(
                    self.state_left / self.sample_rate, 0, 200, color='red')
            else:
                self.state_right_line.remove()
                self.state_right = int(x * self.sample_rate)
                self.state_right_line = self.axes.vlines(
                    self.state_right / self.sample_rate, 0, 200, color='red')
        self.canvas.draw()

    # 释放菜单
    def releaseMenu(self):
        if self.annotate == EEGView.STATE_ANNOTATE:
            self.popMenu2.exec_(QCursor.pos())
        elif self.annotate == EEGView.WAVE_ANNOTATE:
            self.popMenu1.exec_(QCursor.pos())
        else:
            self.popMenu3.exec_(QCursor.pos())

    # 绘制线透明度
    def focusLines(self):
        lines = self.axes.get_lines()
        for l in lines:
            label = l.get_label().split('|')[0]
            l.set_alpha(self.channels_alpha[label])
        self.canvas.draw()

    # 绘制第一个点
    def showFirstPoint(self, event):
        artist = event.artist
        label = artist.get_label()
        mouseevent = event.mouseevent
        if label not in self.pick_labels:
            return
        self.pick_labels = self.channels_name
        self.checkPickLabels(label)
        self.focusLines()
        self.restorePreSampleColor()
        self.pick_first = int(event.ind[0] + self.begin * self.sample_rate // self.dawnSample)
        self.pick_X = mouseevent.xdata
        self.pick_Y = mouseevent.ydata
        self.pick_channel = label
        self.axes.plot(
            mouseevent.xdata, mouseevent.ydata, 'ro', label="pp", markersize=4)
        self.canvas.draw()
    #绘制事件
    def drawEvent(self, event):
        x, y = event.xdata, event.ydata
        if self.eventline:
            self.eventline.remove()
            self.axes.collections.remove(self.eventline)
        self.lineposition = int(x * self.sample_rate)
        self.eventline = self.axes.vlines(
        self.lineposition / self.sample_rate, 0, 200, color='red')
        self.canvas.draw()

    # 恢复上一个选中的样本颜色
    def restorePreSampleColor(self):
        if self.cur_sample_index < 0:
            return
        if self.cur_sample_index >= len(self.filterlist):
            return
        sample = self.filterlist[self.cur_sample_index]
        if sample[0] == 'all' and sample[1]!=sample[2]:
            self.changeSampleColor(sample, 'green')
        elif sample[0]!='all' and sample[1]!=sample[2]:
            self.changeSampleColor(sample, 'blue')
        elif sample[0]=='all' and sample[1]==sample[2]:
            self.changeSampleColor(sample, 'orange')
        self.showlabelInfo()
        for col in range(self.ui.tableWidget.columnCount()):
            self.ui.tableWidget.item(self.cur_sample_index, col).setSelected(False)
        self.cur_sample_index = -1

    # 点击一个列表样本
    def pickCurSample(self, row):
        self.restorePreSampleColor() #恢复前一个选中的线条颜色
        self.cur_sample_index = row
        label = self.filterlist[self.cur_sample_index]
        if label[0] == "all" and label[1] != label[2]:
            b_t = time.strftime('%H:%M:%S', time.gmtime(label[1]//(self.sample_rate//self.dawnSample)))
            e_t = time.strftime('%H:%M:%S', time.gmtime(label[2]//(self.sample_rate//self.dawnSample)))
            type_name = ""
            for type in self.type_info:
                if type[0] == label[3]:
                    type_name = type[1]
                    break
            #在右下角显示当前选中样本信息
            self.showlabelInfo(type_name, label[0], str((label[2] - label[1]) / (self.sample_rate // self.dawnSample)), str(b_t), str(e_t), "")
            self.changeSampleColor(label, 'red')
        elif label[0]!='all' and label[1]!=label[2]:
            self.changeSampleColor(label, 'red') #改变当前选中线条颜色
            b_t = time.strftime('%H:%M:%S', time.gmtime(label[1]//(self.sample_rate//self.dawnSample)))
            e_t = time.strftime('%H:%M:%S', time.gmtime(label[2]//(self.sample_rate//self.dawnSample)))
            type_name = ""
            for type in self.type_info:
                if type[0] == label[3]:
                    type_name = type[1]
                    break
            idx = 0
            for i in range(len(self.channels_name)):
                if self.channels_name[i] == label[0]:
                    idx = i
                    break
            l = int(max(0, label[1] - self.begin * self.sample_rate // self.dawnSample))
            r = int(min(label[2] -(self.begin * self.sample_rate // self.dawnSample), self.winTime * self.sample_rate // self.dawnSample))
            m = np.max(self.data[idx, l:r])
            self.showlabelInfo(type_name, label[0], str((label[2] - label[1]) / (self.sample_rate // self.dawnSample)), str(b_t), str(e_t), str(m))
        elif label[0] == 'all' and label[1] == label[2]:
            self.changeSampleColor(label, 'red')  # 改变当前选中线条颜色
            b_t = time.strftime('%H:%M:%S', time.gmtime(label[1] // (self.sample_rate // self.dawnSample)))
            e_t = time.strftime('%H:%M:%S', time.gmtime(label[2] // (self.sample_rate // self.dawnSample)))
            type_name = ""
            for type in self.type_info:
                if type[0] == label[3]:
                    type_name = type[1]
                    break
            self.showlabelInfo(type_name, label[0], str((label[2] - label[1]) / (self.sample_rate // self.dawnSample)),
                               str(b_t), str(e_t), '')

    # 绘制第二个点
    def showSecondPoint(self, event):
        artist = event.artist
        self.pick_label = artist.get_label()
        x = int(event.ind[0] + self.begin * self.sample_rate // self.dawnSample)
        if self.pick_second:
            mid = (self.pick_first + self.pick_second) // 2
            if x > mid:
                self.pick_second = x
            else:
                self.pick_first = x
        else:
            if x > self.pick_first:
                self.pick_second = x
            else:
                self.pick_second = self.pick_first
                self.pick_first = x
        if self.pick_first == self.pick_second:
            return
        self.removeLines(['pp', 'pickedsegment'])
        self.paintAWave(max(self.pick_first - self.begin * self.sample_rate // self.dawnSample, 0),
                        min(self.winTime * self.sample_rate // self.dawnSample, self.pick_second - self.begin * self.sample_rate // self.dawnSample),
                        self.pick_label, 'pickedsegment', 'red')
        self.canvas.draw()

    # 点击图像样本
    def clickSample(self, artist):
        label = artist.get_label()
        label = label.split('|')
        label[1] = int(label[1])
        label[2] = int(label[2])
        label[3] = int(label[3])
        self.resetPickLabels()
        self.focusLines()
        for i in range(len(self.filterlist)):
            if self.labels[i] == label:
                row = i
                break
        if row >= 0 and row < len(self.filterlist):
            self.ui.tableWidget.selectRow(row)
        self.pick_first = None
        self.pick_second = None
        self.pick_channel = None
        self.pickCurSample(row)
        self.canvas.draw()

    # 绘制一个波形
    def paintAWave(self, start, end, channel, label, color):
        x = np.linspace(self.begin, self.end, (self.end - self.begin) * self.sample_rate // self.dawnSample)
        idx = -1
        for i in range(len(self.channels_name)):
            if self.channels_name[i] == channel:
                idx = i
                break
        if idx == -1:
            return
        self.wave_lines.append(label)
        self.axes.plot(x[start:end], self.plottedData[idx, start:end], color=color, picker=True, label=label,
                       alpha=self.channels_alpha[channel], linewidth=1)

    # 改变样本颜色
    def changeSampleColor(self, sample, color):
        s_label = str(sample[0]) + "|" + str(sample[1]) + "|" + str(sample[2]) + "|" + str(sample[3])
        lines = self.axes.get_lines()
        if sample[0] == 'all' and sample[1]!=sample[2]:
            for s in self.state_lines:
                if s[0]==s_label:
                    s[1].set_facecolor(color)
            self.canvas.draw()
        elif sample[0]!='all' and sample[1]!=sample[2]: #波形
            for l in lines:
                label = l.get_label()
                if label == s_label:
                    l.set_color(color)
                    break
            self.canvas.draw()
        elif sample[0]=='all' and sample[1]==sample[2]:#事件
            for l in self.Event_lines:
                if l[0] == s_label:
                    l[1].set_color(color)
                    break
            self.canvas.draw()

    # 取消选中
    def cancelSelect(self):
        self.state_left = None
        if self.state_left_line is not None:
            self.state_left_line.remove()
            self.state_left_line = None
        self.state_right = None
        if self.state_right_line is not None:
            self.state_right_line.remove()
            self.state_right_line = None
        if self.eventline is not None:
            self.eventline.remove()
            self.eventline = None
        self.canvas.draw()
        self.pick_channel = None
        self.pick_first = None
        self.pick_second = None
        self.restorePreSampleColor()
        self.showlabelInfo()
        self.resetPickLabels()
        self.focusLines()

    def insertWave(self, type_id):
        begin = self.pick_first
        end = self.pick_second
        wave = [self.pick_channel, begin, end, type_id]
        idx = 0
        while idx < len(self.labels):
            if wave[1] < self.labels[idx][1] or (wave[1] == self.labels[idx][1] and wave[2] < self.labels[idx][2]):
                break
            idx += 1
        self.labels.insert(idx, wave)
        idx = 0
        while idx < len(self.waves):
            if wave[1] < self.waves[idx][1] or (wave[1] == self.waves[idx][1] and wave[2] < self.waves[idx][2]):
                break
            idx += 1
        self.waves.insert(idx, wave)
        idx = 0
        while idx < len(self.filterlist):
            if wave[1] < self.filterlist[idx][1] or (wave[1] == self.filterlist[idx][1] and wave[2] < self.filterlist[idx][2]):
                break
            idx += 1
        self.filterlist.insert(idx, wave)
        color = 'blue'
        l = (wave[1] - (self.begin * self.sample_rate // self.dawnSample)) if wave[1] > (self.begin * self.sample_rate // self.dawnSample) else 0
        r = (wave[2] - (self.begin * self.sample_rate // self.dawnSample)) if wave[2] < (self.end * self.sample_rate // self.dawnSample) else (self.end - self.begin) * (self.sample_rate // self.dawnSample)
        label = str(wave[0]) + "|" + str(wave[1]) + "|" + str(wave[2]) + "|" + str(wave[3])
        self.resetPickLabels()
        self.focusLines()
        self.paintAWave(l, r, wave[0], label, color)
        lBit = (begin * self.dawnSample // self.sample_rate) * self.nDotWin // self.lenTime
        rBit = (end * self.dawnSample // self.sample_rate) * self.nDotWin // self.lenTime
        self.labelBit[lBit: rBit] = True
        self.paintLabelBit()
        self.canvas.draw()
        self.showLabelList()
        self.pick_second = None
        self.pick_first = None
        self.pick_channel = None
        return wave

    def insertState(self, type_id):
        begin = self.state_left // self.dawnSample
        end = self.state_right // self.dawnSample
        state = ["all", begin, end, type_id]
        idx = 0
        while idx < len(self.labels):
            if state[1] < self.labels[idx][1] or (state[1] == self.labels[idx][1] and state[2] < self.labels[idx][2]):
                break
            idx += 1
        self.labels.insert(idx, state)
        idx = 0
        while idx < len(self.states):
            if state[1] < self.states[idx][1] or (state[1] == self.states[idx][1] and state[2] < self.states[idx][2]):
                break
            idx += 1
        self.states.insert(idx, state)
        idx = 0
        while idx < len(self.filterlist):
            if state[1] < self.filterlist[idx][1] or (
                    state[1] == self.filterlist[idx][1] and state[2] < self.filterlist[idx][2]):
                break
            idx += 1
        self.filterlist.insert(idx, state)
        self.resetPickLabels()
        self.focusLines()
        self.paintAState(state, "green")
        lBit = (self.state_left // self.sample_rate) * self.nDotWin // self.lenTime
        rBit = (self.state_right // self.sample_rate) * self.nDotWin // self.lenTime
        self.labelBit[lBit: rBit] = True
        self.paintLabelBit()
        self.showLabelList()
        self.state_left = None
        self.state_right = None
        self.state_left_line.remove()
        self.state_right_line.remove()
        self.state_left_line = None
        self.state_right_line = None
        self.canvas.draw()
        return state

    def insertEvent(self, type_id):
        begin = self.lineposition
        end = self.lineposition
        event = ['all', begin, end, type_id]
        idx = 0
        while idx < len(self.filterlist):
            if event[1] < self.filterlist[idx][1] or (
                    event[1] == self.filterlist[idx][1] and event[2] < self.filterlist[idx][2]):
                break
            idx += 1
        self.filterlist.insert(idx, event)
        idx = 0
        while idx < len(self.labels):
            if event[1] < self.labels[idx][1] or (
                    event[1] == self.labels[idx][1] and event[2] < self.labels[idx][2]):
                break
            idx += 1
        self.labels.insert(idx, event)
        idx = 0
        while idx < len(self.events):
            if event[1] < self.events[idx][1] or (
                    event[1] == self.events[idx][1] and event[2] < self.events[idx][2]):
                break
            idx += 1
        self.events.insert(idx, event)
        self.resetPickLabels()
        self.focusLines()
        self.paintAEvent(begin / self.sample_rate, str(event[0]) + "|" + str(event[1]) + "|" + str(event[2]) + "|" + str(event[3]), 'orange')
        lBit = (self.lineposition // self.sample_rate) * self.nDotWin // self.lenTime
        self.labelBit[lBit: lBit + 1] = True
        self.paintLabelBit()
        self.showLabelList()
        self.lineposition = None
        self.eventline.remove()
        self.eventline = None
        self.canvas.draw()

    # 判断样本是波形还是状态
    def checkMenuAction(self, type):
        if self.cur_sample_index >= 0 and self.cur_sample_index < len(self.filterlist):
            pass
        else:
            label = []
            if self.annotate == EEGView.STATE_ANNOTATE:
                if self.state_left is None or self.state_right is None or self.is_status_showed is False:
                    QMessageBox.information(self.view, ' ', "无效选择")
                    return EEGView.NO_ACTION, label
                begin = self.state_left // self.dawnSample
                end = self.state_right // self.dawnSample
                label = ["all", begin, end, type[0]]
            elif self.annotate == EEGView.WAVE_ANNOTATE:
                if self.pick_first is None or self.pick_second is None or self.is_waves_showed is False:
                    QMessageBox.information(self.view, ' ', "无效选择")
                    return EEGView.NO_ACTION, label
                begin = self.pick_first
                end = self.pick_second
                label = [self.pick_channel, begin, end, type[0]]
            elif self.annotate == EEGView.EVENT_ANNOTATE:
                if self.lineposition is None or self.is_Event_showed is False:
                    QMessageBox.information(self.view, ' ', "无效选择")
                    return EEGView.NO_ACTION, label
                begin = self.lineposition
                end = self.lineposition
                label = ['all', begin, end, type[0]]
            return EEGView.ADD_SAMPLE, label

        # if self.is_waves_showed and self.is_status_showed:
        #     if self.cur_sample_index >= 0 and self.cur_sample_index < len(self.labels):
        #         self.labels[self.cur_sample_index][3] = type[0]
        #         if self.labels[self.cur_sample_index][0] == 'all':
        #             pass
        #         else:
        #             for wave in self.waves:
        #                 if wave[0] == self.labels[self.cur_sample_index][0] and wave[1] == self.labels[self.cur_sample_index][1] and wave[2] == self.labels[self.cur_sample_index][2]:
        #                     wave[3] = type[0]
        #                     break
        #         self.showLabelList()
        #         return 2, self.labels[self.cur_sample_index]
        # elif self.is_waves_showed:
        #     if self.cur_sample_index >= 0 and self.cur_sample_index < len(self.waves):
        #         return 2, self.waves[self.cur_sample_index]
        # elif self.is_status_showed:
        #     if self.cur_sample_index >= 0 and self.cur_sample_index < len(self.states):
        #         return 2, self.states[self.cur_sample_index]
        #
        # QMessageBox.information(self.view, ' ', "无效选择")
        # return 0, []



    def setSelectedTypes(self, sampleFilter):
        self.type_info = sampleFilter


    def delSample(self):
        pass

    # 显示病人相关信息
    def showPatientInfo(self, patient, file_name, measure_date, start_time, end_time):
        name = patient[1]
        birth = str(patient[2])
        sex = patient[3]
        self.ui.labelPatientName.setText(name)
        self.ui.labelPatientBirth.setText(birth)
        self.ui.labelPatientSex.setText(sex)
        self.ui.labelPatientMeasure.setText(str(measure_date))
        self.ui.labelFileName.setText(file_name)
        meas_time = str(start_time) + ' - ' + str(end_time)
        self.ui.labelMeasureTime.setText(meas_time)


    # 显示右下角样本信息
    def showlabelInfo(self, type_name='', channel='', lent='', begin='', end='', amp=''):
        self.ui.labelType.setText(type_name)
        self.ui.labelChannel.setText(channel)
        if lent != '':
            lent = str(round(float(lent), 3))
        self.ui.labelLength.setText(lent)
        self.ui.labelBegin.setText(begin)
        self.ui.labelEnd.setText(end)
        if amp != '':
            amp = str(round(float(amp), 3))
        self.ui.labelAmp.setText(amp)

    # 改变时间信息
    def changeTime(self):
        self.ui.editTime.setText(time.strftime("%H:%M:%S", time.gmtime(self.begin)))

    def refChange(self, Ref):
        self.curRef = Ref
        chanList = self.refList[Ref]
        self.allChannel = {key.upper(): True for key in chanList}

    def processChan(self):
        try:
            self.plottedData = []
            ex_chs = tuple([self.channels_index[x] for x in self.exclude_av if x in self.channels_name])
            temp_data = self.data
            temp_data = np.delete(temp_data, ex_chs, axis=0)
            av = np.mean(temp_data, axis=0)

            for i in range(len(self.channels_name)):
                index = self.channels_index.get(self.channels_name[i].split('-')[0])
                label = self.channels_name[i]
                if '-' in label:
                    g1, g2 = label.split('-')
                    g1 = g1.strip()
                    g2 = g2.strip()
                    g1_index = self.channels_index[g1]
                    y1 = self.data[g1_index]
                    if g2 == 'REF':
                        y2 = 0
                    elif g2 == 'AV':
                        y2 = av
                    else:
                        g2_index = self.channels_index[g2]
                        y2 = self.data[g2_index]
                    y = y1 - y2
                else:
                    y = self.data[index]

                if self.subtractAverage:
                    y = y - np.mean(y)

                y = y / (self.sensitivity * self.axesYWidthMM / (len(self.channels_name) + 1))
                y = -y + i + 1


                self.plottedData.append(y)
            self.plottedData = np.array(self.plottedData)
        except Exception as e:
            print("processChan", e)

    def getCurrentRef(self):
        return self.curRef

    def getCurrentRefList(self):
        return self.refList[self.curRef]

    def checkType(self):
        dgroup = {self.curRef: self.refList[self.curRef]} if self.typeEEG is False else {}
        return self.typeEEG, self.curRef, dgroup, self.channels_name

    def getShownChannel(self):
        return self.channels_name

    def updateShownChannels(self, shownChannels):
        channel = []
        for key in self.allChannel.keys():
            if key in shownChannels:
                self.allChannel[key] = True
                channel.append(key)
            else:
                self.allChannel[key] = False
        self.updateYAxis(channel)
        self.removeLines()
        self.processChan()
        self.paintEEG()
        self.filterSamples()
        self.paintWaves()
        self.paintStates()
        self.paintEvents()
        self.removeTimeLine()
        self.paintTimeLine()
        if self.pick_first is not None:
            if self.pick_second is None:
                if self.pick_first >= self.begin * self.sample_rate // self.dawnSample and self.pick_first < self.end * self.sample_rate // self.dawnSample:
                    self.axes.plot(self.pick_X, self.pick_Y, 'ro', label="pp", markersize=4)
            else:
                if (
                        self.pick_first >= self.begin * self.sample_rate // self.dawnSample and self.pick_first < self.end * self.sample_rate // self.dawnSample) or (
                        self.pick_second >= self.begin * self.sample_rate // self.dawnSample and self.pick_second < self.end * self.sample_rate // self.dawnSample) or (
                        self.pick_first < self.begin * self.sample_rate // self.dawnSample and self.pick_second >= self.end * self.sample_rate // self.dawnSample):
                    self.paintAWave(max(self.pick_first - self.begin * self.sample_rate // self.dawnSample, 0),
                                    min(self.winTime * self.sample_rate // self.dawnSample,
                                        self.pick_second - self.begin * self.sample_rate // self.dawnSample),
                                    self.pick_label, 'pickedsegment', 'red')

        self.canvas.draw()
        self.showLabelList()
        self.showlabelInfo()

    def getSampleFilter(self):
        tempt=[]
        for i in self.type_info:
            if self.is_waves_showed and (i[3][-2:]=='波形' or i[2][-2:]=='波形'):
                tempt.append(i[1])
            elif self.is_status_showed and (i[3][-2:] =='状态'or i[2][-2:]=='状态'):
                tempt.append(i[1])
            elif self.is_Event_showed and i[3][-2:]=='事件':
                tempt.append(i[1])
        return tempt

    def updateSample(self,sampleFilter):
        self.sampleFilter = sampleFilter

    def annotatesignal(self,signal):
        self.annotate=signal


