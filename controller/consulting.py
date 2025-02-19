from PyQt5.Qt import *

from view.consulting import DiagListView, PrentryView
from view.consulting import sign_InfoView

class consultingController(QWidget):
    switchToEEG = pyqtSignal(list)
    def __init__(self, appUtil=None, client=None,page=None):
        super().__init__()
        self.view = DiagListView()
        self.client = client
        self.appUtil = appUtil
        self.uid=None
        self.sign_InfoView = None
        self.User = self.client.tUser
        self.patientname=None
        self.client.ct_get_diags_notDiagResSig.connect(self.get_diags_notDiagRes)
        self.client.ct_get_fileNameByIdDateResSig.connect(self.get_fileNameByIdDateRes)
        self.client.ct_get_diags_notDiag([self.client.tUser[0]])
        self.client.ct_diag_refusedResSig.connect(self.diag_refusedRes)
        self.client.ct_get_diagResSig.connect(self.ct_get_diagRes)
        self.client.ct_diag_updateResSig.connect(self.diag_updateRes) #保存诊断信息
        self.client.ct_diag_commitResSig.connect(self.diag_commitRes)#提交诊断信息
        # 处理客户端传回的提取取诊断信息
    def get_diags_notDiagRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "提取未诊断信息不成功", REPData[2], QMessageBox.Yes)
            return False

        self.diags_viewInfo = REPData[2]
        self.userNamesDict = {}
        self.paitentNamesDict = {}
        if REPData[3] is not None:
            for u in REPData[3]:
                self.userNamesDict.setdefault(u[0], u[1])
        if REPData[4] is not None:
            for p in REPData[4]:
                self.paitentNamesDict.setdefault(p[0], p[1])
        self.check_id = None
        self.file_id = None
        self.measure_date = None
        self.file_name = None
        self.view.init_table(self.diags_viewInfo, self.client.tUser, self.userNamesDict, self.paitentNamesDict,
                             self.on_clicked_manual_query, self.on_clicked_diag_query, self.on_clicked_diag_refused)
        self.view.show()

    # 槽对象中的槽函数
    def exit(self):
        self.client.ct_get_diags_notDiagResSig.disconnect()
        self.client.ct_get_fileNameByIdDateResSig.disconnect()

    def on_clicked_manual_query(self, diags_viewInfo, patient_name):
        self.check_id = diags_viewInfo[-4]
        self.uid = diags_viewInfo[2]
        self.patient_id = diags_viewInfo[0]
        self.measure_date = diags_viewInfo[1]
        self.patient_name = patient_name

        self.file_id = None
        self.file_name = None
        self.returnTo = 0
        msg = [diags_viewInfo[-4]]
        self.client.ct_get_fileNameByIdDate(msg)
        self.view.hide()

    def get_fileNameByIdDateRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "选择脑电数据文件", REPData[2], QMessageBox.Yes)
            return False
        else:
            self.pre_info = REPData[1]
            col_num = 1
            self.prentryView = PrentryView()
            self.prentryView.setAttribute(Qt.WA_DeleteOnClose)
            self.prentryView.setWindowTitle("[选择脑电数据文件]")
            self.prentryView.setWindowModality(Qt.ApplicationModal)
            self.prentryView.ui.btnConfirm.setEnabled(False)
            self.prentryView.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.prentryView.ui.tableWidget.resizeRowsToContents()
            self.prentryView.ui.tableWidget.resizeColumnsToContents()
            self.prentryView.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.prentryView.ui.tableWidget.clicked.connect(self.on_tableWidget_itemClicked)
            self.prentryView.ui.btnConfirm.clicked.connect(self.on_btnConfirm_clicked)
            self.prentryView.ui.btnReturn.clicked.connect(self.on_btnReturn_clicked)

            self.prentryView.ui.tableWidget.setColumnCount(col_num)
            itemName = ['脑电数据文件列表']
            row_num = len(self.pre_info)
            if row_num <= 0:
                itemName = ['脑电数据文件列表[无相关文件]']
            for i in range(col_num):
                header_item = QTableWidgetItem(itemName[i])
                font = header_item.font()
                font.setPointSize(10)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                self.prentryView.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
            self.prentryView.ui.tableWidget.horizontalHeader().setHighlightSections(False)
            self.prentryView.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            self.prentryView.ui.tableWidget.setRowCount(row_num)
            for r in range(row_num):
                fn = '{:>03}.bdf'.format(self.pre_info[r][1])
                item = QTableWidgetItem(fn)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                font.setPointSize(10)
                item.setFont(font)
                self.prentryView.ui.tableWidget.setItem(r, 0, item)
            self.prentryView.ui.tableWidget.verticalHeader().setVisible(False)
        self.prentryView.show()

    def on_tableWidget_itemClicked(self):
        row = self.prentryView.ui.tableWidget.currentRow()
        if row < 0:
            return
        self.file_id = self.pre_info[row][1]
        self.file_name = '{:>03}.bdf'.format(self.file_id)
        self.prentryView.ui.btnConfirm.setEnabled(True)

    def on_btnConfirm_clicked(self):
        self.prentryView.close()
        self.switchToEEG.emit([self.file_id, self.file_name, self.check_id, self.patient_id, self.measure_date, ['consultingController',''], "sample_info", self.client.tUser[0], True, True, None])
        #file_id,file_name,check_id,patient_id,measure_date,['从哪个模块来','从那个模块的第几页来'],样本的table，用户id，是否允许更新，是否允许插入,theme_id/classid
    def on_btnReturn_clicked(self):
        self.prentryView.close()
        self.view.show()

    def on_clicked_diag_query(self, diags_viewInfo, patient_name):
        self.check_id = diags_viewInfo[-4]
        self.uid = diags_viewInfo[2]
        self.patientname=patient_name
        if self.sign_InfoView is None:
            # self.view.ui.btnSignInfo.setDisabled(True)
            msg = [self.check_id, self.uid]
            self.client.ct_get_diag(msg)
        else:
            try:
                # self.sign_InfoView.setWindowFlag(Qt.WindowStaysOnTopHint,True)
                self.sign_InfoView.show()
                self.sign_InfoView.activateWindow()
            except Exception as e:
                print(f"setWindowFlag:{e}")
    def ct_get_diagRes(self,REPData):
        # self.view.ui.btnSignInfo.setEnabled(True)
        if REPData[0] == '0':
            QMessageBox.information(self, "[脑电会诊]提取诊断信息不成功", REPData[2], QMessageBox.Yes)
            return False

        self.diag = REPData[2]
        #diag=[patient_id,measure_time（测量时间）,上传医生的id,会诊状态，diag.sign_date，alpha,slow,fast,amplitude,eyes，hyperventilation,sleep,abnormal_wave,attack_stage,summary,diag.checkid,开单医生的用户id,检查单号，cUid（上传医生）]
        self.sign_InfoView = sign_InfoView()

        if self.diag[0][3] != 'notDiagnosed' or self.diag[0][2] != self.User[0]:
            self.sign_InfoView.ui.save_pushButton.hide()
            self.sign_InfoView.ui.commit_pushButton.hide()
            self.sign_InfoView.ui.alpha_lineEdit.setReadOnly(True)
            self.sign_InfoView.ui.slow_lineEdit.setReadOnly(True)
            self.sign_InfoView.ui.fast_lineEdit.setReadOnly(True)
            self.sign_InfoView.ui.amplitude_lineEdit.setReadOnly(True)
            self.sign_InfoView.ui.eyes_lineEdit.setReadOnly(True)
            self.sign_InfoView.ui.hyperventilation_lineEdit.setReadOnly(True)
            self.sign_InfoView.ui.sleep_lineEdit.setReadOnly(True)
            self.sign_InfoView.ui.abnormal_wave_lineEdit.setReadOnly(True)
            self.sign_InfoView.ui.attack_stage_lineEdit.setReadOnly(True)
            self.sign_InfoView.ui.summary_textEdit.setReadOnly(True)
        else:
            self.sign_InfoView.ui.save_pushButton.clicked.connect(self.signInfo_save_pushButton_clicked)
            self.sign_InfoView.ui.commit_pushButton.clicked.connect(self.signInfo_commit_pushButton_clicked)
        self.sign_InfoView.ui.close_pushButton.clicked.connect(self.signInfo_close_pushButton_clicked)

        if self.diag is None or len(self.diag) == 0:
            self.sign_InfoView.ui.patient_lineEdit.setText(self.patientname)
            self.sign_InfoView.ui.measure_date_lineEdit.setText(str(self.diag[0][1]))
            self.sign_InfoView.ui.d_user_lineEdit_3.setText(self.userNamesDict.get(self.uid))
            self.sign_InfoView.ui.state_lineEdit_3.setText('notDiagnosed')
            # self.sign_InfoView.ui.sign_dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
            self.sign_InfoView.ui.sign_dateTimeEdit.setDateTime(None)

            self.sign_InfoView.ui.alpha_lineEdit.setText("")
            self.sign_InfoView.ui.slow_lineEdit.setText("")
            self.sign_InfoView.ui.fast_lineEdit.setText("")
            self.sign_InfoView.ui.amplitude_lineEdit.setText("")
            self.sign_InfoView.ui.eyes_lineEdit.setText("")
            self.sign_InfoView.ui.hyperventilation_lineEdit.setText("")
            self.sign_InfoView.ui.sleep_lineEdit.setText("")
            self.sign_InfoView.ui.abnormal_wave_lineEdit.setText("")
            self.sign_InfoView.ui.attack_stage_lineEdit.setText("")
            self.sign_InfoView.ui.summary_textEdit.setText("")

        else:
            self.sign_InfoView.ui.patient_lineEdit.setText(self.patientname)
            self.sign_InfoView.ui.measure_date_lineEdit.setText(str(self.diag[0][1]))
            self.sign_InfoView.ui.d_user_lineEdit_3.setText(self.userNamesDict.get(self.uid))
            self.sign_InfoView.ui.state_lineEdit_3.setText(self.diag[0][3])
            dt = QDateTime.fromString(str(self.diag[0][4]), "yyyy-MM-dd hh:mm:ss")
            self.sign_InfoView.ui.sign_dateTimeEdit.setDateTime(dt)
            self.sign_InfoView.ui.alpha_lineEdit.setText(self.diag[0][5])
            self.sign_InfoView.ui.slow_lineEdit.setText(self.diag[0][6])
            self.sign_InfoView.ui.fast_lineEdit.setText(self.diag[0][7])
            self.sign_InfoView.ui.amplitude_lineEdit.setText(self.diag[0][8])
            self.sign_InfoView.ui.eyes_lineEdit.setText(self.diag[0][9])
            self.sign_InfoView.ui.hyperventilation_lineEdit.setText(self.diag[0][10])
            self.sign_InfoView.ui.sleep_lineEdit.setText(self.diag[0][11])
            self.sign_InfoView.ui.abnormal_wave_lineEdit.setText(self.diag[0][12])
            self.sign_InfoView.ui.attack_stage_lineEdit.setText(self.diag[0][13])
            self.sign_InfoView.ui.summary_textEdit.setText(self.diag[0][14])
            # self.sign_InfoView.ui.del_pushButton.setEnabled(True)
        self.sign_InfoView.show()
    def signInfo_save_pushButton_clicked(self):
        reply = QMessageBox.information(self, '提示', '保存诊断,确定吗?', QMessageBox.Yes | QMessageBox.No)
        if self.User != None and reply == 16384:
            sign_dateTime = self.sign_InfoView.ui.sign_dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            alpha = self.sign_InfoView.ui.alpha_lineEdit.text()
            slow = self.sign_InfoView.ui.slow_lineEdit.text()
            fast = self.sign_InfoView.ui.fast_lineEdit.text()
            amplitude = self.sign_InfoView.ui.amplitude_lineEdit.text()
            eyes = self.sign_InfoView.ui.eyes_lineEdit.text()
            hyperventilation = self.sign_InfoView.ui.hyperventilation_lineEdit.text()
            sleep = self.sign_InfoView.ui.sleep_lineEdit.text()
            abnormal_wave = self.sign_InfoView.ui.abnormal_wave_lineEdit.text()
            attack_stage = self.sign_InfoView.ui.attack_stage_lineEdit.text()
            summary = self.sign_InfoView.ui.summary_textEdit.toPlainText()

            msg = [self.check_id, '', self.uid, sign_dateTime, alpha, slow, fast, amplitude, eyes,
                   hyperventilation, sleep, abnormal_wave, attack_stage, summary]
            self.client.ct_diag_update(msg)
    def diag_updateRes(self,REPData):
        # self.view.ui.btnSignInfo.setEnabled(True)
        if REPData[0] == '0':
            QMessageBox.information(self, "填写诊断信息不成功", REPData[2], QMessageBox.Yes)
            return False
        self.sign_InfoView.hide()
    def signInfo_commit_pushButton_clicked(self):
        if self.diag is None or len(self.diag) == 0:
            return
        reply = QMessageBox.information(self, '提示', '提交当前的诊断信息,提交后不能修改.确定吗?',
                                        QMessageBox.Yes | QMessageBox.No)
        if reply == 16384:
            # sign_dateTime = self.sign_InfoView.ui.sign_dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            sign_dateTime = None
            alpha = self.sign_InfoView.ui.alpha_lineEdit.text()
            slow = self.sign_InfoView.ui.slow_lineEdit.text()
            fast = self.sign_InfoView.ui.fast_lineEdit.text()
            amplitude = self.sign_InfoView.ui.amplitude_lineEdit.text()
            eyes = self.sign_InfoView.ui.eyes_lineEdit.text()
            hyperventilation = self.sign_InfoView.ui.hyperventilation_lineEdit.text()
            sleep = self.sign_InfoView.ui.sleep_lineEdit.text()
            abnormal_wave = self.sign_InfoView.ui.abnormal_wave_lineEdit.text()
            attack_stage = self.sign_InfoView.ui.attack_stage_lineEdit.text()
            summary = self.sign_InfoView.ui.summary_textEdit.toPlainText()
            msg = [self.check_id, '', self.uid, sign_dateTime, alpha, slow, fast, amplitude, eyes,
                   hyperventilation, sleep, abnormal_wave, attack_stage, summary]
            REQ = [msg, self.measure_date, self.patientname, self.User[2]]
            self.sign_InfoView.hide()
            self.client.ct_diag_commit(REQ)
    def diag_commitRes(self,REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "完成诊断", REPData[2], QMessageBox.Yes)
            return False
        QMessageBox.information(self, "完成诊断，操作成功", REPData[2], QMessageBox.Yes)
        # self.view.show()

        self.page = ['file_name']
        self.get_diags_notDiag()
    def get_diags_notDiag(self):
        self.check_id = None
        self.file_id = None
        self.measure_date = None
        self.file_name = None
        self.page = ['file_name']
        msg = [self.client.tUser[0]]
        self.client.ct_get_diags_notDiag(msg)
    def signInfo_close_pushButton_clicked(self):
        self.sign_InfoView.close()
        self.sign_InfoView = None
    def on_clicked_diag_refused(self, diags_viewInfo,patient_name):
        reply = QMessageBox.information(self, "拒绝诊断信息",
                                        f'拒绝:{patient_name},测量日期{diags_viewInfo[1]}的诊断，确定吗?',
                                        QMessageBox.Yes | QMessageBox.No)
        if reply == 16384:
            self.check_id = diags_viewInfo[-4]
            msg = [self.check_id, diags_viewInfo[2], str(diags_viewInfo[1]), patient_name]  # check_id user_id,masure_date patient_name,username
            self.client.ct_diag_refused(msg)
    def diag_refusedRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "拒绝诊断", REPData[2], QMessageBox.Yes)
            return False
        QMessageBox.information(self, "拒绝诊断，操作成功", REPData[2], QMessageBox.Yes)
        self.page = ['file_name']
        self.client.ct_get_diags_notDiag([self.client.tUser[0]])
