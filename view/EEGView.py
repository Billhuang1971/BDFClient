import sys

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.Qt import *
import time
import matplotlib as mpl

from view.EEG_form.form import Ui_EEGView


class EEGView(QWidget):
    PICK_FIRST = 1
    PICK_SECOND = 2
    PICK_NO_DOT = 0
    PICK_AXES = 1
    PICK_AXHSCROLL = 2
    PICK_NO_AX = 0
    STATE_ANNOTATE = 0
    WAVE_ANNOTATE = 1

    insertSample = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.ui = Ui_EEGView()
        self.ui.setupUi(self)

        self.cursor = None
        # 类型数据
        self.type_info = []
        # 是否状态标注
        self.states_annotate = False
        # 当前选中的状态
        self.state_picked = None
        # 是否状态显示
        self.is_status_showed = True
        self.is_waves_showed = True
        # 状态标注列表
        self.states_annotated = []
        # 被选中的通道
        self.pick_labels = []
        self.pick_first = None
        self.pick_second = None
        self.cur_sample_index = -1
        self.sample_info = []
        self.sample_list = []
        self.waves = []
        self.states = []
        self.channels_alpha = {}
        self.pick_channel = None
        self.begin = None
        self.sample_rate = None
        self.end = None
        self.User = None
        self.data = None
        self.channels_name = []
        self.userInfo = None
        self.state_left = None
        self.state_right = None
        self.state_left_line = None
        self.state_right_line = None
        self.duration = None
        self.paint_length = None
        self.scroll_position = None
        self.secondsSpan = 30
        self.lenWin = 0
        self.sensitivity = 10
        self.show_seconds_line = True
        self.time_lines = []
        self.wave_lines = []
        self.state_lines = []
        self.sen = 0

        self.create_paint_tools()

    def setTypeInfo(self, type_info):
        self.type_info = type_info

    def getLenWin(self):
        return self.lenWin

    def create_paint_tools(self):
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.ui.glCanvas.addWidget(self.canvas, 0, 0, 1, 1)
        self.fig.subplots_adjust(left=0.05, right=0.95, top=0.99, bottom=0.01)
        self.axes = plt.subplot2grid((33, 1), (2, 0), rowspan=30)
        self.ax_hscroll = plt.subplot2grid((33, 1), (0, 0), rowspan=1)

        self.popMenu1 = QMenu(self.canvas)
        self.popMenu2 = QMenu(self.canvas)
        cancelAction = QAction("取消选择", self, triggered=self.cancelSelect)
        self.popMenu1.addAction(cancelAction)
        self.popMenu1.addSeparator()
        self.popMenu2.addAction(cancelAction)
        self.popMenu2.addSeparator()
        delAction = QAction("删除样本", self, triggered=self.delSample)
        self.popMenu1.addAction(delAction)
        self.popMenu1.addSeparator()
        self.popMenu2.addAction(delAction)
        self.popMenu2.addSeparator()
        # 向右键菜单栏添加波形和状态
        sms = {}
        groups = ['正常波形', '异常波形', '伪迹波形', '正常状态', '异常状态', '伪迹状态']
        for g in groups[:3]:
            sms[g] = self.popMenu1.addMenu(g)
        for g in groups[3:]:
            sms[g] = self.popMenu2.addMenu(g)
        for t in self.type_info:
            action = QAction(t[1], self)
            action.triggered.connect(lambda chk, t=t: self.actDispatch(t))
            if sms.get(t[3]) is None:
                continue
            sms[t[3]].addAction(action)

    def calc_sen(self):
        axesL = self.axes.figure.subplotpars.left
        axesR = self.axes.figure.subplotpars.right
        axesT = self.axes.figure.subplotpars.top
        axesB = self.axes.figure.subplotpars.bottom
        x_fraction, y_fraction = axesR - axesL, axesT - axesB
        figureSize = self.ui.listView.size()
        figureWidth = figureSize.width()
        figureHeight = figureSize.height()
        screen = QApplication.primaryScreen()
        xDPI = screen.physicalDotsPerInchX()
        yDPI = screen.physicalDotsPerInchY()
        figureWidthMM = (figureWidth / xDPI) * 25.4
        figureHeightMM = (figureHeight / yDPI) * 25.4
        self.axesXWidthMM = x_fraction * figureWidthMM
        self.axesYWidthMM = y_fraction * figureHeightMM
        self.lenWin = int(round(self.axesXWidthMM / self.secondsSpan))
        self.ui.moveLength.setCurrentText(str(self.lenWin))
        self.sen = (len(self.channels_name) + 1) / self.axesYWidthMM

    def secondsSpanChange(self, secondsSpan):
        self.secondsSpan = secondsSpan
        self.lenWin = int(round(self.axesXWidthMM / self.secondsSpan))

    def updateXAxis(self):
        self.axes.set_xlim([self.begin, self.end])
        self.axes.set_xticks(np.arange(self.begin, self.end + 1, 1))
        xlabels = [time.strftime('%H:%M:%S', time.gmtime(i))
                   for i in range(self.begin, self.end + 1)]
        self.axes.set_xticklabels(xlabels)
        for xtl in self.axes.get_xticklabels():
            xtl.set_fontsize(10)

    def changeSecondsLine(self):
        self.show_seconds_line = self.show_seconds_line is False

    def checkSecondsLine(self):
        if self.show_seconds_line:
            if len(self.time_lines) > 0:
                self.removeTimeLine()
            self.paintTimeLine()
        else:
            self.removeTimeLine()
        self.canvas.draw()

    def paintTimeLine(self):
        for x in range(self.begin, self.end + 1):
            self.time_lines.append(self.axes.vlines(x, 0, 200, colors='black', alpha=0.7))

    def removeTimeLine(self):
        for line in self.time_lines:
            line.remove()
        self.time_lines = []

    def paintEEG(self):
        x = np.linspace(self.begin, self.end, (self.end - self.begin) * self.sample_rate)
        for i in range(len(self.channels_name)):
            self.axes.plot(x, self.data[i] + i + 1, color='black', label=self.channels_name[i], picker=True,
                           alpha=self.channels_alpha[self.channels_name[i]], linewidth=0.3)

    def setSampleRate(self, sample_rate):
        self.sample_rate = sample_rate

    def getIdx(self, time):
        return time * self.sample_rate

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

    def refreshWin(self, data, begin, end):
        self.data = data
        self.begin = begin
        self.end = end
        self.removeLines()
        self.updateXAxis()
        self.paintEEG()
        self.checkSecondsLine()
        self.filterSamples()
        self.paintWaves()
        self.paintStates()
        if self.pick_first is not None:
            if self.pick_second is None:
                if self.pick_first >= self.begin * self.sample_rate and self.pick_first < self.end * self.sample_rate:
                    self.axes.plot(self.pick_X, self.pick_Y, 'ro', label="pp", markersize=4)
            else:
                if (self.pick_first >= self.begin * self.sample_rate and self.pick_first < self.end * self.sample_rate) or (self.pick_second >= self.begin * self.sample_rate and self.pick_second < self.end * self.sample_rate) or (self.pick_first < self.begin * self.sample_rate and self.pick_second >= self.end * self.sample_rate):
                    self.paintAWave(max(self.pick_first - self.begin * self.sample_rate, 0),
                                    min(self.lenWin * self.sample_rate, self.pick_second - self.begin * self.sample_rate),
                                    self.pick_label, 'pickedsegment', 'red')

        self.canvas.draw()
        self.showLabels()
        self.showCurLabel()

    def changeShowWave(self):
        self.is_waves_showed = self.is_waves_showed is False
        self.ui.hideWave.setChecked(self.is_waves_showed)
        if self.is_waves_showed:
            self.paintWaves()
        else:
            self.removeLines(self.wave_lines, True)
            self.wave_lines = []
            self.resetPickLabels()
            self.focusLines()
        self.canvas.draw()
        self.showLabels()

    def changeShowState(self):
        self.is_status_showed = self.is_status_showed is False
        if self.is_status_showed:
            self.paintStates()
        else:
            for state in self.state_lines:
                state.remove()
            self.state_lines = []
            self.resetPickLabels()
            self.focusLines()
        self.canvas.draw()
        self.showLabels()

    def showLabels(self):
        list = []
        if self.is_status_showed is True and self.is_waves_showed is True:
            list = self.sample_list
        elif self.is_status_showed is True:
            list = self.states
        elif self.is_waves_showed is True:
            list = self.waves
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

        row_num = len(list)
        self.ui.tableWidget.setRowCount(row_num)
        for r in range(row_num):
            for c in range(col_num):
                if c == 0:
                    item = QTableWidgetItem(
                        str(time.strftime('%H:%M:%S',
                                          time.gmtime(int(list[r][1])))))
                else:
                    type_name = ""
                    for type in self.type_info:
                        if type[0] == list[r][5]:
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

    def paintStates(self):
        if self.is_status_showed is False:
            return
        keys = [x[0] for x in self.type_info]
        for state in self.states:
            idx = keys.index(state[5])
            description = self.type_info[idx][3]
            if description == '正常状态':
                color = 'green'
            elif description == '异常状态':
                color = 'red'
            else:
                color = 'dodgerblue'
            self.paintAState(state, color)

    def paintAState(self, state, color):
        label = str(state[2]) + "|" + str(state[1]) + "|" + str(state[3]) + "|" + str(state[4]) + "|" + str(state[5])
        self.state_lines.append(self.axes.axvspan(state[1], state[3], label=label, facecolor=color, alpha=0.3, picker=True))

    def filterSamples(self):
        self.sample_list = []
        self.waves = []
        self.states = []
        for sample in self.sample_info:
            if sample[3] < self.begin or sample[1] >= self.end:
                continue
            self.sample_list.append(sample)
            if sample[2] == 'all':
                self.states.append(sample)
            else:
                self.waves.append(sample)

    def paintWaves(self):
        if self.is_waves_showed is False:
            return
        for wave in self.waves:
            color = 'blue'
            l = (wave[1] - self.begin) * self.sample_rate if wave[1] > self.begin else 0
            r = (wave[3] - self.begin) * self.sample_rate if wave[3] < self.end else (self.end - self.begin) * self.sample_rate
            label = str(wave[2]) + "|" + str(wave[1]) + "|" + str(wave[3]) + "|" + str(wave[4]) + "|" + str(wave[5]) + "|" + str(wave[6])
            self.paintAWave(l, r, wave[2], label, color)

    def updateYAxis(self, channels_name=[]):
        self.channels_name = channels_name
        self.resetPickLabels()
        max_y = len(channels_name) + 1
        self.axes.clear()
        self.axes.set_ylim([0, max_y])
        self.axes.set_yticks(range(max_y))
        self.axes.set_yticklabels(['Reset'] + channels_name)
        for ytl in self.axes.get_yticklabels():
            ytl.set_picker(True)
            ytl.set_fontsize(10)
        self.axes.invert_yaxis()
        self.fig.subplots_adjust(left=0.07)
        self.fig.subplots_adjust(right=0.97)

    def setAxHscroll(self, duration):
        self.ax_hscroll.set_xlim(0, duration)
        self.ax_hscroll.get_yaxis().set_visible(False)
        hsel_patch = mpl.patches.Rectangle((0, 0), duration,
                                           1,
                                           edgecolor='k',
                                           facecolor=(0.75, 0.75, 0.75),
                                           alpha=0.25, linewidth=1,
                                           clip_on=False)
        self.ax_hscroll.add_patch(hsel_patch)
        hxticks = np.linspace(0, duration, 11)
        self.ax_hscroll.set_xticks(hxticks)
        hxlabels = [time.strftime('%H:%M:%S', time.gmtime(int(hxticks[i])))
                    for i in range(0, 11)]
        self.ax_hscroll.set_xticklabels(hxlabels)
        for xhtl in self.ax_hscroll.get_xticklabels():
            xhtl.set_fontsize(10)


    def clickAxStatus(self, ax):
        if ax == self.axes:
            return EEGView.PICK_AXES
        elif ax == self.ax_hscroll:
            return EEGView.PICK_AXHSCROLL
        return EEGView.PICK_NO_AX

    def onAxhscrollClicked(self, begin):
        if self.scroll_position is not None:
            self.scroll_position.remove()
        self.scroll_position = self.ax_hscroll.axvline(begin, color='r', linewidth=0.5)
        self.canvas.draw()

    def isBanWave(self):
        return self.states_annotate or self.is_waves_showed is False

    def resetPickLabels(self):
        self.pick_labels = self.channels_name
        for channel in self.channels_name:
            self.channels_alpha[channel] = 1
        self.removeLines(['pp', 'pickedsegment'])
        self.pick_first = None
        self.pick_second = None

    def cancelStateAnnotate(self):
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

    def cancelWaveAnnotate(self):
        self.pick_channel = None
        self.pick_first = None
        self.pick_second = None
        self.removeLines(['pp', 'pickedsegment'])
        if self.restore_pre_sample_color():
            self.cur_sample_index = -1
            self.showCurLabel()
        self.pick_labels = []
        self.focus_lines()

    def changeStateAnnotateStatus(self):
        self.states_annotate = not self.states_annotate
        if self.states_annotate:
            self.ui.btnStateAnnotate.setText("波形标注")
        else:
            self.ui.btnStateAnnotate.setText("状态标注")

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

    def removeLines(self, ch=None, sample=False):
        if (ch is None or len(ch) == 0) and sample is False:
            lines = self.axes.get_lines()
            for l in lines:
                l.remove()
            return
        lines = self.axes.get_lines()
        for l in lines:
            label = l.get_label() if sample else l.get_label().split('|')[0]
            if label in ch:
                l.remove()

    def clickPointStatus(self, label):
        if self.pick_first is None:
            return EEGView.PICK_FIRST
        elif label == self.pick_channel:
            return EEGView.PICK_SECOND
        return EEGView.PICK_NO_DOT

    def drawStateLine(self, event):
        if not self.states_annotate:
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

    def releaseMenu(self):
        if self.states_annotate:
            self.popMenu2.exec_(QCursor.pos())
        else:
            self.popMenu1.exec_(QCursor.pos())

    def focusLines(self):
        lines = self.axes.get_lines()
        for l in lines:
            label = l.get_label().split('|')[0]
            l.set_alpha(self.channels_alpha[label])
        self.canvas.draw()

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
        self.pick_first = int(event.ind[0] + self.begin * self.sample_rate)
        self.pick_X = mouseevent.xdata
        self.pick_Y = mouseevent.ydata
        self.pick_channel = label
        self.axes.plot(
            mouseevent.xdata, mouseevent.ydata, 'ro', label="pp", markersize=4)
        self.canvas.draw()

    def restorePreSampleColor(self):
        if self.cur_sample_index < 0:
            return
        if self.is_status_showed is True and self.is_waves_showed is True:
            if self.cur_sample_index >= len(self.sample_list):
                return
            sample = self.sample_list[self.cur_sample_index]
        elif self.is_status_showed is True:
            if self.cur_sample_index >= len(self.states):
                return
            sample = self.states[self.cur_sample_index]
        elif self.is_waves_showed is True:
            if self.cur_sample_index >= len(self.waves):
                return
            sample = self.waves[self.cur_sample_index]
        else:
            return
        self.changeSampleColor(sample, 'blue')
        self.showCurLabel()
        for col in range(self.ui.tableWidget.columnCount()):
            self.ui.tableWidget.item(self.cur_sample_index, col).setSelected(False)
        self.cur_sample_index = -1

    def pickCurSample(self, row):
        self.cur_sample_index = row
        if self.is_status_showed is True and self.is_waves_showed is True:
            label = self.sample_list[self.cur_sample_index]
            if label[2] == "all":
                b_t = time.strftime('%H:%M:%S', time.gmtime(label[1]))
                e_t = time.strftime('%H:%M:%S', time.gmtime(label[3]))
                type_name = ""
                for type in self.type_info:
                    if type[0] == label[5]:
                        type_name = type[1]
                        break
                self.showCurLabel(type_name, label[2], str(label[3] - label[1]), str(b_t), str(e_t), "")
            else:
                self.changeSampleColor(label, 'red')
                b_t = time.strftime('%H:%M:%S', time.gmtime(label[1]))
                e_t = time.strftime('%H:%M:%S', time.gmtime(label[3]))
                type_name = ""
                for type in self.type_info:
                    if type[0] == label[5]:
                        type_name = type[1]
                        break
                idx = 0
                for i in range(len(self.channels_name)):
                    if self.channels_name[i] == label[2]:
                        idx = i
                        break
                l = int(max(0, (label[1] - self.begin) * self.sample_rate))
                r = int(min((label[3] - label[1]) * self.sample_rate, self.lenWin * self.sample_rate))
                m = np.max(self.data[idx, l:r])
                self.showCurLabel(type_name, label[2], str(label[3] - label[1]), str(b_t), str(e_t), str(m))
        elif self.is_status_showed is True:
            label = self.states[self.cur_sample_index]
            b_t = time.strftime('%H:%M:%S', time.gmtime(label[1]))
            e_t = time.strftime('%H:%M:%S', time.gmtime(label[3]))
            type_name = ""
            for type in self.type_info:
                if type[0] == label[5]:
                    type_name = type[1]
                    break
            self.showCurLabel(type_name, label[2], str(label[3] - label[1]), str(b_t), str(e_t), "")
        elif self.is_waves_showed is True:
            label = self.waves[self.cur_sample_index]
            self.changeSampleColor(label, 'red')
            b_t = time.strftime('%H:%M:%S', time.gmtime(label[1]))
            e_t = time.strftime('%H:%M:%S', time.gmtime(label[3]))
            type_name = ""
            for type in self.type_info:
                if type[0] == label[5]:
                    type_name = type[1]
                    break
            idx = 0
            for i in range(len(self.channels_name)):
                if self.channels_name[i] == label[2]:
                    idx = i
                    break
            l = int(max(0, (label[1] - self.begin) * self.sample_rate))
            r = int(min((label[3] - label[1]) * self.sample_rate, self.lenWin * self.sample_rate))
            m = np.max(self.data[idx, l:r])
            self.showCurLabel(type_name, label[2], str(label[3] - label[1]), str(b_t), str(e_t), str(m))

    def showSecondPoint(self, event):
        artist = event.artist
        self.pick_label = artist.get_label()
        x = int(event.ind[0] + self.begin * self.sample_rate)
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
        self.paintAWave(max(self.pick_first - self.begin * self.sample_rate, 0), min(self.lenWin * self.sample_rate, self.pick_second - self.begin * self.sample_rate), self.pick_label, 'pickedsegment', 'red')
        self.canvas.draw()

    def clickSample(self, artist):
        label = artist.get_label()
        self.restorePreSampleColor()
        label = label.split('|')
        label[1] = int(label[1])
        label[2] = int(label[2])
        label[3] = int(label[3])
        label[4] = int(label[4])
        self.resetPickLabels()
        self.focusLines()
        self.removeLines(['pp', 'pickedsegment'])
        if self.is_status_showed is True and self.is_waves_showed is True:
            for i in range(len(self.sample_list)):
                if self.sample_list[i][2] == label[0] and self.sample_list[i][1] == label[1]:
                    self.cur_sample_index = i
                    break
            if self.cur_sample_index >= 0 and self.cur_sample_index < len(self.sample_list):
                self.ui.tableWidget.selectRow(self.cur_sample_index)
        elif self.is_waves_showed is True:
            for i in range(len(self.waves)):
                if self.waves[i][2] == label[0] and self.waves[i][1] == label[1]:
                    self.cur_sample_index = i
                    break
            if self.cur_sample_index >= 0 and self.cur_sample_index < len(self.waves):
                self.ui.tableWidget.selectRow(self.cur_sample_index)
        self.pick_first = None
        self.pick_second = None
        self.pick_channel = None
        artist.set_color('r')
        b_t = time.strftime('%H:%M:%S', time.gmtime(label[1]))
        e_t = time.strftime('%H:%M:%S', time.gmtime(label[2]))
        type_name = ""
        for type in self.type_info:
            if type[0] == label[4]:
                type_name = type[1]
                break
        idx = 0
        for i in range(len(self.channels_name)):
            if self.channels_name[i] == label[0]:
                idx = i
                break
        l = int(max(0, (label[1] - self.begin) * self.sample_rate))
        r = int(min((label[2] - label[1]) * self.sample_rate, self.lenWin * self.sample_rate))
        m = np.max(self.data[idx, l:r])
        self.showCurLabel(type_name, label[0], str(label[2] - label[1]), str(b_t), str(e_t), str(m))
        self.canvas.draw()


    def paintAWave(self, start, end, channel, label, color):
        x = np.linspace(self.begin, self.end, (self.end - self.begin) * self.sample_rate)
        idx = -1
        for i in range(len(self.channels_name)):
            if self.channels_name[i] == channel:
                idx = i
                break
        if idx == -1:
            return
        self.wave_lines.append(label)
        self.axes.plot(x[start:end], self.data[idx, start:end] + idx + 1, color=color, picker=True, label=label,
                       alpha=self.channels_alpha[channel], linewidth=1)


    def changeSampleColor(self, sample, color):
        s_label = str(sample[2]) + "|" + str(sample[1]) + "|" + str(sample[3]) + "|" + str(sample[4]) + "|" + str(sample[5]) + "|" + str(sample[6])
        lines = self.axes.get_lines()
        for l in lines:
            label = l.get_label()
            if label == s_label:
                l.set_color(color)
                break
        self.canvas.draw()

    def cancelSelect(self):
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
        self.pick_channel = None
        self.pick_first = None
        self.pick_second = None
        self.restorePreSampleColor()
        self.showCurLabel()
        self.resetPickLabels()
        self.focusLines()

    def actDispatch(self, type):
        self.removeLines(['pp', 'pickedsegment'])
        if self.states_annotate:
            if self.state_left is None or self.state_right is None:
                QMessageBox.information(self.view, ' ', "无效选择")
            else:
                state = ["all", self.state_left // self.sample_rate, self.state_right // self.sample_rate, type[0]]
            self.state_left = None
            self.state_right = None
            self.state_left_line = None
            self.state_right_line = None
            return
        if self.pick_second is not None:
            begin = self.pick_first // self.sample_rate
            end = self.pick_second // self.sample_rate
            wave = [type[1], begin, end, type[0]]
            idx = 0
            for sample in self.sample_info:
                if sample[1] > begin:
                    break
                idx += 1
            self.sample_info.insert(idx, wave)
        elif self.cur_sample_index >= 0 and ():
            pass
        else:
            QMessageBox.information(self.view, ' ', "无效选择")
        self.pick_channel = None
        self.pick_first = None
        self.pick_second = None
        self.restorePreSampleColor()
        self.focusLines()

    def delSample(self):
        pass

    def updateLabel(self, type):
        pass

    def updateSample(self, type):
        pass

    def insertUpdateState(self, type):
        pass

    def cancelMenu(self):
        pass

    def delLabel(self):
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


    # 显示样本信息
    def showCurLabel(self, type_name='', channel='', lent='', begin='', end='', amp=''):
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

    def changeTime(self, x):
        self.ui.editTime.setText(time.strftime("%H:%M:%S", time.gmtime(x)))