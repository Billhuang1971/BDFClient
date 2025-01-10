import ctypes
import inspect
import threading
import time


from PyQt5.Qt import *
import matplotlib as mpl

from view.EEGView import EEGView
from model.EEGData import EEGData


class EEGController(QWidget):
    switchFromEEG = pyqtSignal(list)
    def __init__(self, client=None, appUtil=None, msg=None, mainLabel=None):
        super().__init__()
        self.client = client
        self.appUtil = appUtil
        self.file_id = msg[0]
        self.file_name = msg[1]
        self.check_id = msg[2]
        self.user_id = client.tUser[0]
        self.patient_id = msg[3]
        self.measure_date = msg[4]
        self.return_from=msg[5]
        self.mainLabel = mainLabel
        self.view = EEGView()
        self.view.calcSen()
        self.secondsSpan = 30
        nWinBlock = 11
        self.nSecWin, nDotSec = self.view.changeSecondsSpan(self.secondsSpan)
        self.moveLen = self.nSecWin
        self.view.ui.moveLength.setCurrentText(str(self.moveLen))

        self.client.openEEGFileResSig.connect(self.openEEGFileRes)
        self.client.loadDataDynamicalSig.connect(self.loadDataDynamicalRes)
        self.client.insertSampleSig.connect(self.insertSampleRes)

        self.client.openEEGFile([self.patient_id, self.check_id, self.file_id, self.nSecWin, nDotSec, nWinBlock])

    def openEEGFileRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, '提示', REPData[2])
        else:
            msg = REPData[2]
            print(msg)
            self.moving = True
            self.nSample = msg[11]
            self.patientInfo = msg[0]
            self.channels = msg[3]
            self.index_channels = msg[4]
            sample_rate = msg[5]
            self.lenFile = msg[6] // self.nSample
            self.duration = msg[7]
            self.start_time = msg[8]
            self.end_time = msg[9]
            type_info = msg[1]
            self.montage = msg[2]
            self.lenBlock = msg[10] // self.nSample
            self.lenWin = msg[12]
            data = msg[13]
            labels = msg[14]

            self.view.initView(type_info, self.channels, self.duration, sample_rate, self.patientInfo, self.file_name, self.measure_date, self.start_time, self.end_time)
            self.data = EEGData()
            self.data.initEEGData(data, self.lenFile, self.lenBlock, self.nSample, self.lenWin, labels)
            self.connetEvent()
            data, labels = self.data.getData()
            self.view.refreshWin(data, labels, 0, self.nSecWin)


    def insertSampleRes(self):
        pass

    def insertSample(self):
        pass

    def loadDataDynamicalRes(self, REPData):
        msg = REPData[3][2]
        data = msg[0]
        samples_info = msg[1]
        self.data.setData(data)
        self.view.updateSamples(self.readFrom, self.readTo, self.case, samples_info)
        data = self.data.getData()
        self.view.refreshWin(data, self.left_time, self.right_time)

    def connetEvent(self):
        self.view.insertSample.connect(self.insertSample)
        self.view.ui.btnUp.clicked.connect(self.onBtnDownClicked)
        self.view.ui.btnDown.clicked.connect(self.onBtnUpClicked)
        self.view.ui.btnUping.clicked.connect(self.onBtnUpingClicked)
        self.view.ui.btnDowning.clicked.connect(self.onBtnDowningClicked)
        self.view.ui.btnBegin.clicked.connect(self.onBtnBeginClicked)
        self.view.ui.btnEnd.clicked.connect(self.onBtnEndClicked)
        self.view.ui.editTime.editingFinished.connect(self.timeChange)
        self.view.ui.btnStateAnnotate.clicked.connect(self.btnStateAnnotateClicked)
        self.view.ui.secondsLine.clicked.connect(self.secondsLineClicked)
        self.view.ui.tableWidget.itemClicked.connect(self.onSampleClicked)
        self.view.ui.hideWave.clicked.connect(self.hideWave)
        self.view.ui.hideState.clicked.connect(self.hideState)
        self.view.ui.secondsSpan.lineEdit().editingFinished.connect(self.secondsSpanChange)
        self.view.ui.moveLength.lineEdit().editingFinished.connect(self.moveLengthChange)
        self.view.ui.returnBtn.clicked.connect(self.on_return_clicked)

        self.view.canvas.mpl_connect("pick_event", self.handlePickEvent)
        self.view.canvas.mpl_connect("button_release_event", self.doMouseReleaseEvent)
        self.view.canvas.mpl_connect("scroll_event", self.doScrollEvent)
        self.view.canvas.mpl_connect("key_press_event", self.doKeyPressEvent)
        self.view.canvas.setFocusPolicy(Qt.ClickFocus)
        self.view.canvas.setFocus()

    def secondsSpanChange(self):
        secondsSpan = self.view.ui.secondsSpan.lineEdit().text()
        self.view.secondsSpanChange(int(secondsSpan))
        self.lenWin = self.view.getLenWin()
        self.toBlock = self.view.getIdx(self.lenWin)
        self.lenBlock = self.view.getIdx(self.lenWin * 9)
        self.updateTo = self.lenBlock
        self.updateFrom = 0
        self.fromBlock = 0
        self.left_time = 0
        self.right_time = min(self.lenWin, self.duration)
        self.readFrom = 0
        self.readTo = self.lenBlock
        self.case = 1
        self.data.initEEGData(self.lenFile, self.lenBlock)
        self.client.loadDataDynamical(self.check_id, self.file_id, self.readFrom, self.readTo)

    def moveLengthChange(self):
        moveLength = self.view.ui.moveLength.lineEdit().text()
        self.moveLen = int(moveLength)

    def onSampleClicked(self, item=None):
        if item is None:
            return
        row = item.row()
        self.view.pickCurSample(row)

    def hideWave(self):
        self.view.changeShowWave()

    def hideState(self):
        self.view.changeShowState()

    def secondsLineClicked(self):
        self.view.changeSecondsLine()
        self.view.checkSecondsLine()

    def timeChange(self):
        reg = QRegExp(r"^([01]\d|2[0-3]):[0-5]\d:[0-5]\d$")
        time = self.view.ui.editTime.text()
        if not reg.exactMatch(time):
            self.view.ui.editTime.setText("00:00:00")
            return
        [h, m, s] = time.split(':')
        begin = int(h) * 3600 + int(m) * 60 + int(s)
        if begin < 0 or begin + self.lenWin > self.duration:
            self.view.ui.editTime.setText("00:00:00")
            self.left_time = 0
            self.right_time = self.lenWin
        else:
            self.left_time = begin
            self.right_time = begin + self.lenWin
        self.checkSolution()

    def onBtnDowningClicked(self):
        if self.moving:
            self.view.ui.btnBegin.setDisabled(True)
            self.view.ui.btnEnd.setDisabled(True)
            self.view.ui.btnUp.setDisabled(True)
            self.view.ui.btnDown.setDisabled(True)
            self.view.ui.btnUping.setDisabled(True)
            self.view.ui.btnDowning.setText("■")
            self.thread = threading.Thread(target=self.doDowning)
            self.thread.start()
        else:
            self.view.ui.btnBegin.setDisabled(False)
            self.view.ui.btnEnd.setDisabled(False)
            self.view.ui.btnUp.setDisabled(False)
            self.view.ui.btnDown.setDisabled(False)
            self.view.ui.btnUping.setDisabled(False)
            self.view.ui.btnDowning.setText("<<")
            self._async_raise(self.thread.ident, SystemExit)
        self.moving = self.moving is False

    def doDowning(self):
        while True:
            time.sleep(1)
            self.left_time -= self.moveLen
            self.right_time -= self.moveLen
            if self.left_time < 0:
                self.left_time = 0
                self.right_time = self.lenWin
                self.view.changeTime(self.left_time)
                self.checkSolution()
                self.view.ui.btnBegin.setDisabled(False)
                self.view.ui.btnEnd.setDisabled(False)
                self.view.ui.btnUp.setDisabled(False)
                self.view.ui.btnDown.setDisabled(False)
                self.view.ui.btnUping.setDisabled(False)
                self.view.ui.btnDowning.setText("<<")
                self._async_raise(self.thread.ident, SystemExit)
                return
            else:
                self.view.changeTime(self.left_time)
                self.checkSolution()

    def onBtnUpingClicked(self):
        if self.moving:
            self.view.ui.btnBegin.setDisabled(True)
            self.view.ui.btnEnd.setDisabled(True)
            self.view.ui.btnUp.setDisabled(True)
            self.view.ui.btnDown.setDisabled(True)
            self.view.ui.btnDowning.setDisabled(True)
            self.view.ui.btnUping.setText("■")
            self.thread = threading.Thread(target=self.doUping)
            self.thread.start()
        else:
            self.view.ui.btnBegin.setDisabled(False)
            self.view.ui.btnEnd.setDisabled(False)
            self.view.ui.btnUp.setDisabled(False)
            self.view.ui.btnDown.setDisabled(False)
            self.view.ui.btnDowning.setDisabled(False)
            self.view.ui.btnUping.setText(">>")
            self._async_raise(self.thread.ident, SystemExit)
        self.moving = self.moving is False

    def doUping(self):
        while True:
            time.sleep(1)
            self.left_time += self.moveLen
            self.right_time += self.moveLen
            if self.right_time > self.duration:
                self.left_time = self.duration - self.lenWin
                self.right_time = self.duration
                self.view.changeTime(self.left_time)
                self.checkSolution()
                self.view.ui.btnBegin.setDisabled(False)
                self.view.ui.btnEnd.setDisabled(False)
                self.view.ui.btnUp.setDisabled(False)
                self.view.ui.btnDown.setDisabled(False)
                self.view.ui.btnDowning.setDisabled(False)
                self.view.ui.btnUping.setText(">>")
                self._async_raise(self.thread.ident, SystemExit)
                return
            else:
                self.view.changeTime(self.left_time)
                self.checkSolution()

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

    def onBtnBeginClicked(self):
        self.left_time = 0
        self.right_time = self.lenWin
        self.view.changeTime(self.left_time)
        self.checkSolution()

    def onBtnEndClicked(self):
        self.left_time = self.duration - self.lenWin
        self.right_time = self.duration
        self.view.changeTime(self.left_time)
        self.checkSolution()


    # 响应选中对象事件
    def handlePickEvent(self, event):
        mouseevent = event.mouseevent
        artist = event.artist
        if self.view.isBanWave() or mouseevent.button != 1:
            return

        # 鼠标左键
        # 点击y轴标签
        if isinstance(artist, mpl.text.Text):
            pl = artist.get_text()
            if pl == 'Reset':
                self.view.resetPickLabels()
            else:
                self.view.checkPickLabels(pl)
            self.view.focusLines()
            # 点击线、点
        elif isinstance(artist, mpl.lines.Line2D):
            label = artist.get_label()
            # 点击点
            if label == "pp":
                return
            # 点击线
            if len(label.split('|')) == 1:
                pick_dot = self.view.clickPointStatus(label)
                # 第一个点
                if pick_dot == EEGView.PICK_FIRST:
                    self.view.showFirstPoint(event)
                # 第二个点，在同一个通道上
                elif pick_dot == EEGView.PICK_SECOND:
                    self.view.showSecondPoint(event)
            # 点击样本
            else:
                self.view.clickSample(artist)

    def doMouseReleaseEvent(self, event):
        # 左键
        if event.button == 1:
            ax = self.view.clickAxStatus(event.inaxes)
            # 点击在脑电图axes中
            if ax == EEGView.PICK_AXES:
                self.view.drawStateLine(event)
            # 点击在跳转滚动条上
            elif ax == EEGView.PICK_AXHSCROLL:
                x = int(event.xdata)
                if x + self.lenWin <= self.duration:
                    self.left_time = x
                    self.right_time = x + self.lenWin
                else:
                    self.left_time = max(0, self.duration - self.lenWin)
                    self.right_time = self.duration
                self.view.changeTime(self.left_time)
                self.checkSolution()
        # 右键释放菜单
        elif event.button == 3:
            self.view.releaseMenu()

    def checkSolution(self):
        self.view.onAxhscrollClicked(self.left_time)
        inBlock, readFrom, readTo, fromBlock, toBlock, updateFrom, updateTo, case = self.data.queryRange(
            self.view.getIdx(self.left_time), self.view.getIdx(self.lenWin))
        if inBlock is False:
            self.updateFrom = updateFrom
            self.updateTo = updateTo
            self.fromBlock = fromBlock
            self.toBlock = toBlock
            self.readFrom = readFrom
            self.readTo = readTo
            self.case = case
            self.client.loadDataDynamical(self.check_id, self.file_id, self.readFrom, self.readTo)
        else:
            data = self.data.getData(fromBlock, toBlock)
            self.view.refreshWin(data, self.left_time, self.right_time)

    def doScrollEvent(self, event):
        if event.button == "down":
            self.onBtnDownClicked()
        else:
            self.onBtnUpClicked()

    def onBtnUpClicked(self):
        self.left_time -= self.moveLen
        self.right_time -= self.moveLen
        if self.left_time < 0:
            self.right_time = self.lenWin
            self.left_time = 0
        self.view.changeTime(self.left_time)
        self.checkSolution()

    def onBtnDownClicked(self):
        self.left_time += self.moveLen
        self.right_time += self.moveLen
        if self.right_time > self.duration:
            self.right_time = self.duration
            self.left_time = self.right_time - self.lenWin
        self.view.changeTime(self.left_time)
        self.checkSolution()

    def doKeyPressEvent(self, event):
        if event.key == 'escape':
            self.view.cancelSelect()
        elif event.key == 'a':
            self.btnStateAnnotateClicked()
        elif event.key == 'left':
            self.onBtnUpClicked()
        elif event.key == 'right':
            self.onBtnDownClicked()

    def btnStateAnnotateClicked(self):
        self.view.changeStateAnnotateStatus()
        self.view.cancelSelect()
    def on_return_clicked(self):
        self.view.close()
        self.switchFromEEG.emit(self.return_from)
    def exit(self):
        self.switchFromEEG.disconnect()