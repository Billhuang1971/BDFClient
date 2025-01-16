import ctypes
import inspect
import threading
import time


from PyQt5.Qt import *
import matplotlib as mpl

from view.EEGView import EEGView
#from view.EEGFrom import QDialogMontage
#from view.EEGFrom import SampleSelect
#from view.EEGFrom import ChannelSelect
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
        self.return_from = msg[5]
        self.tableName = msg[6]
        self.pUid = msg[7]
        self.mainLabel = mainLabel
        self.view = EEGView()
        self.speed = {
            "1x": 3,
            "2x": 1.5,
            "3x": 1
        }
        self.speedText = "1x"


    def startEEG(self):
        try:
            self.view.show()
            self.secondsSpan = 30
            self.nSecWin, nDotSec = self.view.calcSen(self.secondsSpan)
            nWinBlock = 11
            self.moveLen = self.nSecWin
            self.view.ui.moveLength.setCurrentText(str(self.moveLen))

            self.client.openEEGFileResSig.connect(self.openEEGFileRes)
            self.client.loadEEGDataSig.connect(self.loadEEGDataRes)
            self.client.insertSampleSig.connect(self.insertSampleRes)
            self.client.openEEGFile([self.patient_id, self.check_id, self.file_id, self.nSecWin, nDotSec, nWinBlock, self.tableName, self.pUid])
        except Exception as e:
            print("startEEG", e)

    def openEEGFileRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, '提示', REPData[2])
            else:
                msg = REPData[2]
                self.moving = False
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
                self.leftTime = 0
                self.rightTime = self.nSecWin
                data = msg[13]
                labels = msg[14]
                labelBit = msg[15]

                self.view.initView(type_info, self.channels, self.duration, sample_rate, self.patientInfo, self.file_name, self.measure_date, self.start_time, self.end_time, labelBit, self.nSample)
                self.connetEvent(type_info)

                self.data = EEGData()
                self.data.initEEGData(data, self.lenFile, self.lenBlock, self.nSample, self.lenWin, labels)
                data, labels = self.data.getData()
                self.view.refreshWin(data, labels, self.leftTime, self.rightTime)
        except Exception as e:
            print("openEEGFileRes", e)


    def insertSampleRes(self, REPData):
        try:
            if REPData[3][0] == '0':
                QMessageBox.information(self, '提示', "插入样本失败")
            else:
                QMessageBox.information(self, '提示', "插入样本成功")
        except Exception as e:
            print("insertSampleRes", e)


    def loadEEGDataRes(self, REPData):
        try:
            msg = REPData[3][2]
            data = msg[0]
            labels = msg[1]
            self.data.setData(data, labels)
            data, labels = self.data.getData()
            self.view.refreshWin(data, labels, self.leftTime, self.rightTime)
        except Exception as e:
            print("loadEEGDataRes", e)


    def connetEvent(self, type_info):
        self.view.ui.btnUp.clicked.connect(self.onBtnDownClicked)
        self.view.ui.btnDown.clicked.connect(self.onBtnUpClicked)
        self.view.ui.btnUping.clicked.connect(self.onBtnUpingClicked)
        self.view.ui.btnDowning.clicked.connect(self.onBtnDowningClicked)
        self.view.ui.moveSpeed.currentIndexChanged.connect(self.onMoveSpeedChanged)
        self.view.ui.editTime.editingFinished.connect(self.timeChange)
        self.view.ui.btnStateAnnotate.clicked.connect(self.btnStateAnnotateClicked)
        self.view.ui.secondsLine.clicked.connect(self.secondsLineClicked)
        self.view.ui.tableWidget.itemClicked.connect(self.onSampleClicked)
        self.view.ui.hideWave.clicked.connect(self.hideWave)
        self.view.ui.hideState.clicked.connect(self.hideState)
        self.view.ui.secondsSpan.lineEdit().editingFinished.connect(self.secondsSpanChange)
        self.view.ui.moveLength.lineEdit().editingFinished.connect(self.moveLengthChange)
        self.view.ui.returnBtn.clicked.connect(self.on_return_clicked)
        self.view.ui.subtractAverage.clicked.connect(self.subtractAverage)

        self.view.canvas.mpl_connect("pick_event", self.handlePickEvent)
        self.view.canvas.mpl_connect("button_release_event", self.doMouseReleaseEvent)
        self.view.canvas.mpl_connect("scroll_event", self.doScrollEvent)
        self.view.canvas.mpl_connect("key_press_event", self.doKeyPressEvent)
        self.view.canvas.setFocusPolicy(Qt.ClickFocus)
        self.view.canvas.setFocus()

        cancelAction = QAction("取消选择", self, triggered=self.view.cancelSelect)
        self.view.popMenu1.addAction(cancelAction)
        self.view.popMenu1.addSeparator()
        self.view.popMenu2.addAction(cancelAction)
        self.view.popMenu2.addSeparator()
        delAction = QAction("删除样本", self, triggered=self.delSample)
        self.view.popMenu1.addAction(delAction)
        self.view.popMenu1.addSeparator()
        self.view.popMenu2.addAction(delAction)
        self.view.popMenu2.addSeparator()
        # 向右键菜单栏添加波形和状态
        sms = {}
        groups = ['正常波形', '异常波形', '伪迹波形', '正常状态', '异常状态', '伪迹状态']
        for g in groups[:3]:
            sms[g] = self.view.popMenu1.addMenu(g)
        for g in groups[3:]:
            sms[g] = self.view.popMenu2.addMenu(g)
        for t in type_info:
            action = QAction(t[1], self)
            action.triggered.connect(lambda chk, t=t: self.handleMenuAction(t))
            if sms.get(t[3]) is None:
                continue
            sms[t[3]].addAction(action)

    def handleMenuAction(self, t):
        try:
            cmd, label = self.view.checkMenuAction(t)
            if cmd == 0:
                return
            if cmd == 1:
                self.data.insertSample(label)
                upLoadLabel = label
                upLoadLabel[1] = upLoadLabel[1] * self.nSample
                upLoadLabel[2] = upLoadLabel[2] * self.nSample
                upLoadLabel.extend([self.check_id, self.file_id, self.user_id])
                self.client.insertSample([upLoadLabel, self.tableName])
            # else:
            #
        except Exception as e:
            print("handleMenuAction", e)

    def delSample(self):
        pass

    def onMoveSpeedChanged(self):
        self.speedText = self.view.ui.moveSpeed.currentText()

    def secondsSpanChange(self):
        secondsSpan = self.view.ui.secondsSpan.lineEdit().text()
        self.view.secondsSpanChange(int(secondsSpan))
        self.lenWin = self.view.getLenWin()
        self.toBlock = self.view.getIdx(self.lenWin)
        self.lenBlock = self.view.getIdx(self.lenWin * 9)
        self.updateTo = self.lenBlock
        self.updateFrom = 0
        self.fromBlock = 0
        self.readFrom = 0
        self.readTo = self.lenBlock
        self.case = 1
        self.data.initEEGData(self.lenFile, self.lenBlock)
        self.client.loadDataDynamical(self.check_id, self.file_id, self.readFrom, self.readTo)

    def moveLengthChange(self):
        try:
            moveLength = self.view.ui.moveLength.lineEdit().text()
            self.moveLen = int(moveLength)
        except Exception as e:
            print("moveLengthChange", e)

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
        try:
            reg = QRegExp(r"^([01]\d|2[0-3]):[0-5]\d:[0-5]\d$")
            time = self.view.ui.editTime.text()
            if not reg.exactMatch(time):
                self.view.ui.editTime.setText("00:00:00")
                return
            [h, m, s] = time.split(':')
            begin = int(h) * 3600 + int(m) * 60 + int(s)
            if begin < 0 or begin + self.nSecWin > self.duration:
                self.view.ui.editTime.setText("00:00:00")
                self.leftTime = 0
                self.rightTime = self.nSecWin
            else:
                self.leftTime = begin
                self.rightTime = begin + self.nSecWin
            self.checkSolution()
        except Exception as e:
            print("timeChange", e)

    def onBtnDowningClicked(self):
        try:
            if self.moving is False:
                self.view.ui.btnUp.setDisabled(True)
                self.view.ui.btnDown.setDisabled(True)
                self.view.ui.btnUping.setDisabled(True)
                self.view.ui.btnDowning.setText("■")
                self.thread = threading.Thread(target=self.doDowning)
                self.thread.start()
            else:
                self.view.ui.btnUp.setDisabled(False)
                self.view.ui.btnDown.setDisabled(False)
                self.view.ui.btnUping.setDisabled(False)
                self.view.ui.btnDowning.setText("<<")
                self.stopThread()
            self.moving = self.moving is False
        except Exception as e:
            print("onBtnDowningClicked", e)

    def doDowning(self):
        try:
            while True:
                time.sleep(self.speed[self.speedText])
                self.leftTime -= self.moveLen
                self.rightTime -= self.moveLen
                if self.leftTime < 0:
                    self.leftTime = 0
                    self.rightTime = self.nSecWin
                    self.view.changeTime(self.leftTime)
                    self.checkSolution()
                    self.view.ui.btnUp.setDisabled(False)
                    self.view.ui.btnDown.setDisabled(False)
                    self.view.ui.btnUping.setDisabled(False)
                    self.view.ui.btnDowning.setText("<<")
                    self.stopThread()
                    return
                else:
                    self.view.changeTime(self.leftTime)
                    self.checkSolution()
        except Exception as e:
            print("doDowning", e)

    def stopThread(self):
        self._async_raise(self.thread.ident, SystemExit)
    def exit(self):
        pass
    def onBtnUpingClicked(self):
        try:
            if self.moving is False:
                self.view.ui.btnUp.setDisabled(True)
                self.view.ui.btnDown.setDisabled(True)
                self.view.ui.btnDowning.setDisabled(True)
                self.view.ui.btnUping.setText("■")
                self.thread = threading.Thread(target=self.doUping)
                self.thread.start()
            else:
                self.view.ui.btnUp.setDisabled(False)
                self.view.ui.btnDown.setDisabled(False)
                self.view.ui.btnDowning.setDisabled(False)
                self.view.ui.btnUping.setText(">>")
                self.stopThread()
            self.moving = self.moving is False
        except Exception as e:
            print("onBtnUpingClicked", e)

    def doUping(self):
        try:
            while True:
                time.sleep(self.speed[self.speedText])
                self.leftTime += self.moveLen
                self.rightTime += self.moveLen
                if self.rightTime > self.duration:
                    self.leftTime = self.duration - self.nSecWin
                    self.rightTime = self.duration
                    self.view.changeTime(self.leftTime)
                    self.checkSolution()
                    self.view.ui.btnUp.setDisabled(False)
                    self.view.ui.btnDown.setDisabled(False)
                    self.view.ui.btnDowning.setDisabled(False)
                    self.view.ui.btnUping.setText(">>")
                    self.stopThread()
                    return
                else:
                    self.view.changeTime(self.leftTime)
                    self.checkSolution()
        except Exception as e:
            print("doUping", e)

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

    # 响应选中对象事件
    def handlePickEvent(self, event):
        try:
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
        except Exception as e:
            print("handlePickEvent", e)

    def doMouseReleaseEvent(self, event):
        try:
            # 左键
            if event.button == 1:
                ax = self.view.clickAxStatus(event.inaxes)
                # 点击在脑电图axes中
                if ax == EEGView.PICK_AXES:
                    self.view.drawStateLine(event)
                # 点击在跳转滚动条上
                elif ax == EEGView.PICK_AXHSCROLL:
                    x = int(event.xdata)
                    if x + self.nSecWin <= self.duration:
                        self.leftTime = x
                        self.rightTime = x + self.nSecWin
                    else:
                        self.leftTime = max(0, self.duration - self.nSecWin)
                        self.rightTime = self.duration
                    self.view.changeTime(self.leftTime)
                    self.checkSolution()
            # 右键释放菜单
            elif event.button == 3:
                self.view.releaseMenu()
        except Exception as e:
            print("doMouseReleaseEvent", e)

    def checkSolution(self):
        try:
            self.view.onAxhscrollClicked(self.leftTime)
            inBlock, readFrom, readTo, = self.data.queryRange(self.view.getIdx(self.leftTime) // self.nSample)
            if inBlock is False:
                self.client.loadEEGData([self.check_id, self.file_id, readFrom * self.nSample, readTo * self.nSample, self.nSample, self.tableName, self.pUid])
            else:
                data, labels = self.data.getData()
                self.view.refreshWin(data, labels, self.leftTime, self.rightTime)
        except Exception as e:
            print("checkSolution", e)

    def doScrollEvent(self, event):
        if event.button == "down":
            self.onBtnDownClicked()
        else:
            self.onBtnUpClicked()

    def onBtnUpClicked(self):
        try:
            self.leftTime -= self.moveLen
            self.rightTime -= self.moveLen
            if self.leftTime < 0:
                self.rightTime = self.nSecWin
                self.leftTime = 0
            self.view.changeTime(self.leftTime)
            self.checkSolution()
        except Exception as e:
            print("onBtnUpClicked", e)

    def onBtnDownClicked(self):
        try:
            self.leftTime += self.moveLen
            self.rightTime += self.moveLen
            if self.rightTime > self.duration:
                self.rightTime = self.duration
                self.leftTime = self.rightTime - self.nSecWin
            self.view.changeTime(self.leftTime)
            self.checkSolution()
        except Exception as e:
            print("onBtnDownClicked", e)

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
    def subtractAverage(self):
        self.view.remove_mean(self.leftTime,self.rightTime,'on')