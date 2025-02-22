
from functools import partial


from PyQt5 import QtWidgets, QtCore

from PyQt5.Qt import *

from view.diagAssess import DiagAssessView, PrentryView, sign_InfoView1
from view.diagAssess import DiagListView



class diagAssessController(QWidget):
    switchToEEG = pyqtSignal(list)

    def __init__(self, appUtil=None,  client=None):
        super().__init__()
        self.view = DiagListView()
        self.client = client
        self.appUtil = appUtil


        self.User = self.client.tUser

        self.client. da_get_ClassContentsResSig.connect(self.da_get_ClassContentsRes)
        self.client.da_del_ClassResSig.connect(self.da_del_ClassRes)
        self.client.da_get_ClassStudentResSig.connect(self.get_ClassStudentRes)
        self.client.da_get_contentsResSig.connect(self.get_contentsRes)
        self.client.da_del_StudentsTestResSig.connect(self.da_del_StudentsTestRes)
        self.client.da_get_diagResSig.connect(self.da_get_diagRes)

        self.uid = None
        self.check_id = None
        self.file_id = None
        self.measure_date = None
        self.file_name = None

        self.prentryView = None
        self.prentryView2 = None

        self.sign_InfoView = None
        self.get_contents()

    # 槽对象中的槽函数
    def exit(self):
        if self.prentryView is not None:
            self.prentryView.close()
        if self.prentryView2 is not None:
            self.prentryView2.close()
        self.client.da_get_ClassContentsResSig.disconnect()
        self.client.da_del_ClassResSig.disconnect()
        self.client.da_get_ClassStudentResSig.disconnect()
        self.client.da_get_contentsResSig.disconnect()
        self.client.da_del_StudentsTestResSig.disconnect()
        self.client.da_get_diagResSig.disconnect()


    def get_ClassStudentRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "查看学员", REPData[2], QMessageBox.Yes)
            return False
        else:
            self.pre_info = REPData[2]
            qnumDict = {}
            anumDict = {}
            if REPData[3] is not None:
                for u in REPData[3]:
                     qnumDict.setdefault(u[0], u[1])
            if REPData[4] is not None:
                for p in REPData[4]:
                      anumDict.setdefault(p[0], p[1])

            col_num = 5

            self.prentryView = PrentryView()
            self.prentryView.setAttribute(Qt.WA_DeleteOnClose)
            self.prentryView.resize(700,600)

            self.prentryView.setWindowTitle("学习评估[查看学员]")
            self.prentryView.setWindowModality(Qt.ApplicationModal)


            self.prentryView.ui.btnReturn.clicked.connect(self.on_btnReturn_clicked)
            if self.client.tUser[8]:
                self.prentryView.ui.btnConfirm.setText("删除学员")
                self.prentryView.ui.btnConfirm.setToolTip('删除当前选中学员的学习和测试记录')
                self.prentryView.ui.btnConfirm.clicked.connect(self.on_btnDelStudent_clicked)
            else:
                self.prentryView.ui.btnConfirm.hide()

            self.prentryView.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.prentryView.ui.tableWidget.resizeRowsToContents()
            self.prentryView.ui.tableWidget.resizeColumnsToContents()
            self.prentryView.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.prentryView.ui.tableWidget.clicked.connect(self.on_tableWidget_itemClicked)
            #self.prentryView.ui.btnConfirm.clicked.connect(self.on_btnConfirm_clicked)

            self.prentryView.ui.tableWidget.setColumnCount(col_num)

            row_num = len(self.pre_info)
            if row_num <= 0:
                self.prentryView.ui.tableWidget.setRowCount(1)
                self.prentryView.ui.tableWidget.setItem(0, 0, QTableWidgetItem("[学习评估[无学员]]"))
                self.prentryView.ui.tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
                self.prentryView.ui.tableWidget.item(0, 0).setFlags(Qt.ItemIsEditable)
                font = self.prentryView.ui.tableWidget.item(0, 0).font()
                font.setPointSize(14)
                self.prentryView.show()
                return
            else:
              itemName = ['', '学员帐号', '学员姓名', '得分', '操作']
              for i in range(col_num):
                  header_item = QTableWidgetItem(itemName[i])
                  font = header_item.font()
                  font.setPointSize(14)
                  header_item.setFont(font)
                  header_item.setForeground(QBrush(Qt.black))
                  self.prentryView.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
            self.prentryView.ui.tableWidget.setColumnWidth(0, 40)
            self.prentryView.ui.tableWidget.setColumnWidth(1, 120)
            self.prentryView.ui.tableWidget.setColumnWidth(2, 120)
            self.prentryView.ui.tableWidget.setColumnWidth(3, 120)
            self.prentryView.ui.tableWidget.setColumnWidth(4, 280)
            #self.prentryView.ui.tableWidget.horizontalHeader().setHighlightSections(False)


            self.checkBox=[]
            self.prentryView.ui.tableWidget.setRowCount(row_num)
            iFont = QFont("", 14)
            for r in range(row_num):
                self.prentryView.ui.tableWidget.setCellWidget(r, 0, QCheckBox())
                self.checkBox.insert(r,self.prentryView.ui.tableWidget.cellWidget(r, 0))
                self.checkBox[r].setCheckState(QtCore.Qt.Unchecked)
                self.checkBox[r].setCheckable(True)
                self.checkBox[r].setStyleSheet('margin:2px;height : 50px;font : 14px;')

                item = QTableWidgetItem(self.pre_info[r][4])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFont(iFont)
                self.prentryView.ui.tableWidget.setItem(r, 1, item)

                item = QTableWidgetItem(self.pre_info[r][5])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFont(iFont)
                self.prentryView.ui.tableWidget.setItem(r, 2, item)
                if self.pre_info[r][2]=="tested":
                   item = QTableWidgetItem(f"{self.pre_info[r][3]}%")
                else:
                   item = QTableWidgetItem("未提交")
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFont(iFont)
                self.prentryView.ui.tableWidget.setItem(r, 3, item)

                layout = QHBoxLayout()

                #self.prentryView.ui.tableWidget.setCellWidget(r, 4, QWidget())

                manualBtn = QPushButton('查看测试内容', self.prentryView.ui.tableWidget)
                manualBtn.clicked.connect(partial(self.da_get_ClassContents, self.pre_info[r]))
                manualBtn.setStyleSheet('height : 50px;font : 14px;color:blue')
                manualBtn.setCursor(Qt.PointingHandCursor)
                manualBtn.setToolTip("查看课堂测试内容")
                self.prentryView.ui.tableWidget.setCellWidget(r, 4, manualBtn)

                # layout.addWidget(manualBtn)
                # self.prentryView.ui.tableWidget.cellWidget(r, 4).setLayout(layout)

            self.prentryView.ui.tableWidget.verticalHeader().setVisible(False)

        self.prentryView.show()


    def da_get_ClassContents(self,stdInfo):
            self.prentryView.hide()
            self.stu_id = stdInfo[1]
            self.class_id = stdInfo[0]
            msg = [self.class_id]
            self.client.da_get_ClassContents(msg)

    def  da_get_ClassContentsRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, '提示', REPData[2])
            self.prentryView.show()
            return False


        self.prentryView2 = PrentryView()
        self.prentryView2.setAttribute(Qt.WA_DeleteOnClose)
        self.prentryView2.resize(700,600)

        self.prentryView2.setWindowTitle("学习评估[测试内容]")
        self.prentryView2.setWindowModality(Qt.ApplicationModal)

        self.prentryView2.ui.btnConfirm.setEnabled(False)


        self.prentryView2.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.prentryView2.ui.tableWidget.resizeRowsToContents()
        self.prentryView2.ui.tableWidget.resizeColumnsToContents()
        self.prentryView2.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.prentryView2.ui.tableWidget.clicked.connect(self.on_tableWidget_itemClicked2)
        self.prentryView2.ui.btnConfirm.clicked.connect(self.on_btnConfirm_clicked)
        self.prentryView2.ui.btnReturn.clicked.connect(self.on_btnReturn2_clicked)

        self.prentryView2.ui.btnConfirm.setText("查看脑电图标注")
        col_num = 4
        self.prentryView2.ui.tableWidget.setColumnCount(col_num)

        self.classContentsInfo= REPData[2]

        self.userNamesDict = {}
        if REPData[3] is not None:
          for u in REPData[3]:
            self.userNamesDict.setdefault(u[0], u[1])

        row_num=len(self.classContentsInfo)

        if row_num <= 0:
                self.prentryView2.ui.tableWidget.setRowCount(1)
                self.prentryView2.ui.tableWidget.setItem(0, 0, QTableWidgetItem("[无测试内容]"))
                self.prentryView2.ui.tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
                self.prentryView2.ui.tableWidget.item(0, 0).setFlags(Qt.ItemIsEditable)
                font = self.prentryView2.ui.tableWidget.item(0, 0).font()
                font.setPointSize(14)
                self.prentryView2.show()
                return
        itemName = ['医生', '检查单号', '文件名', '诊断信息']
        for i in range(col_num):
            header_item = QTableWidgetItem(itemName[i])
            font = header_item.font()
            font.setPointSize(14)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            self.prentryView2.ui.tableWidget.setHorizontalHeaderItem(i, header_item)

        self.prentryView2.ui.tableWidget.setColumnWidth(0, 160)
        self.prentryView2.ui.tableWidget.setColumnWidth(1, 120)
        self.prentryView2.ui.tableWidget.setColumnWidth(2, 120)
        self.prentryView2.ui.tableWidget.setColumnWidth(3, 120)

        self.prentryView2.ui.tableWidget.setRowCount(row_num)
        self.prentryView2.ui.tableWidget.horizontalHeader().setHighlightSections(False)

        for r in range(0, row_num):
                item = QTableWidgetItem(self.userNamesDict.get(self.classContentsInfo[r][2]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                font.setPointSize(14)
                item.setFont(font)
                self.prentryView2.ui.tableWidget.setItem(r, 0, item)

                item = QTableWidgetItem(self.classContentsInfo[r][3])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                font.setPointSize(14)
                item.setFont(font)
                self.prentryView2.ui.tableWidget.setItem(r, 1, item)

                fn = '{:>03}.edf'.format(self.classContentsInfo[r][1])
                item = QTableWidgetItem(fn)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                font.setPointSize(14)
                item.setFont(font)
                self.prentryView2.ui.tableWidget.setItem(r, 2, item)

                btn = QPushButton('查看诊断信息', self.prentryView2.ui.tableWidget)
                btn.clicked.connect(partial(self.on_btnSignInfo_clicked, [self.classContentsInfo[r][0], self.classContentsInfo[r][2]]))
                btn.setStyleSheet('height : 50px;font : 14px;color:blue')
                btn.setCursor(Qt.PointingHandCursor)
                btn.setToolTip("查诊断信息")
                self.prentryView2.ui.tableWidget.setCellWidget(r, 3, btn)

        self.prentryView2.ui.tableWidget.verticalHeader().setVisible(False)
        self.prentryView2.show()

    def on_btnConfirm_clicked(self):
        self.switchToEEG.emit([self.file_id, self.file_name, self.check_id, self.patient_id, self.measure_date,
                               ['diagAssessController', ''],
                               "result", self.stu_id, True, False, self.class_id])
        self.prentryView2.hide()

    # 客户端发送提取取学习测试信息的请求
    def get_contents(self):
        msg = [self.client.tUser[0]]
        self.client.da_get_contents(msg)


    # 处理客户端传回的提取学习测试信息
    def get_contentsRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "提取课堂内容信息不成功", REPData[2], QMessageBox.Yes)
            return False

        self.diags_viewInfo = REPData[2]
        self.diags_viewInfo_row = None
        self.std_uid = None

        self.view.show()
        if self.client.tUser[8]:
           self.view.init_table(self.diags_viewInfo,
                              self.on_clicked_manual_query, self.on_btnDelClass_clicked)
        else:
           self.view.init_table(self.diags_viewInfo, self.on_clicked_manual_query, None)

    def on_clicked_manual_query(self, diags_viewInfo, trow):
        self.class_id = diags_viewInfo[0]
        self.row = trow

        msg = [self.class_id, self.client.tUser[0]]
        self.client.da_get_ClassStudent(msg)
        self.view.hide()


    # 响应prentryView单击表格事件，选择病人/测量日期/文件名
    def on_tableWidget_itemClicked2(self):
        row = self.prentryView2.ui.tableWidget.currentRow()

        if row < 0  or row>=len(self.classContentsInfo):
            self.prentryView2.ui.btnConfirm.setDisabled(True)
            return
        self.check_id = self.classContentsInfo[row][0]
        self.file_id = self.classContentsInfo[row][1]
        self.uid = self.classContentsInfo[row][2]
        self.patient_id = self.classContentsInfo[row][4]
        self.prentryView2.ui.btnConfirm.setEnabled(True)

    # 响应prentryView单击表格事件，选择病人/测量日期/文件名
    def on_tableWidget_itemClicked(self):
        row = self.prentryView.ui.tableWidget.currentRow()
        #self.std_uid=self.pre_info[row][4]
        self.stu_id = self.pre_info[row][1]
        if row < 0:
            return
        #self.checkBox[row].setCheckState(QtCore.Qt.CheckState.Checked)
        #self.stu_id = self.pre_info[row][1]
        self.prentryView.ui.btnConfirm.setEnabled(True)
        #self.prentryView.ui.btnReturn.setEnabled(True)
        self.prentryView.setWindowTitle(f"学习评估[选择学员]:{self.pre_info[row][4]}-{self.pre_info[row][5]}")

    # 点击删除课堂按钮
    def on_btnDelClass_clicked(self, diags_viewInfo):
        reply = QMessageBox.information(self, '提示', f'删除课堂[{diags_viewInfo[1]}]的内容、学员及其学习、测试记录.确定吗？',
                                        QMessageBox.Yes | QMessageBox.No)
        if reply == 16384:
            msg = [diags_viewInfo[0]]
            self.client.da_del_class(msg)
            self.view.hide()
        return

    #回调 删除班级
    def da_del_ClassRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, '提示', REPData[2])
            self.view.show()
            return False
        self.get_contents()

    # 回调 删除学生及其学习测试记录
    def da_del_StudentsTestRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, '提示', REPData[2])
            self.prentryView.show()
            return False
        self.view.show()


    # prentryView2，点击返回按钮
    def on_btnReturn2_clicked(self):
        self.prentryView2.hide()
        self.prentryView.show()


    # prentryView，点击返回按钮
    def on_btnReturn_clicked(self):
       self.prentryView.hide()
       self.view.show()

    # prentryView选择文件后，点击删除按钮
    def on_btnDelStudent_clicked(self):
       st=[]
       stuid=[]
       for i in range(0,len(self.checkBox)):
           if self.checkBox[i].isChecked():
               st.append(self.pre_info[i][5])
               stuid.append(self.pre_info[i][1])
       if len(st)<=0:
           QMessageBox.information(self, '提示', '请勾选要删除学员。',QMessageBox.No)
           return
       reply = QMessageBox.information(self, '提示', f'删除当前班级：\n{st}\n的学员资格及其学习、测试记录。确定吗?',QMessageBox.Yes | QMessageBox.No)
       if reply == 16384:
           msg = [self.class_id, stuid]
           self.client.da_del_studentsTest(msg)
           self.prentryView.hide()

       return

    # 学习测试/打开诊断信息窗口
    def on_btnSignInfo_clicked(self, msg):
        self.prentryView2.hide()
        self.client.da_get_diag(msg)

    #学习测试/打开诊断信息窗口
    def da_get_diagRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "提取诊断信息不成功", REPData[2], QMessageBox.Yes)
            return False

        self.diag=REPData[2]

        self.sign_InfoView = sign_InfoView1()

        if self.diag is None or len(self.diag) == 0:
            QMessageBox.information(self, "提取诊断信息", '提取诊断信息为空', QMessageBox.Yes)
        else:
            self.sign_InfoView.ui.measure_date_lineEdit.setText(str(self.diag[0][1]))
            self.sign_InfoView.ui.d_user_lineEdit_3.setText(self.User[2])
            self.sign_InfoView.ui.state_lineEdit_3.setText(self.diag[0][3])
            dt= QtCore.QDateTime.fromString(str(self.diag[0][4]),"yyyy-MM-dd")
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
            self.sign_InfoView.ui.close_pushButton.clicked.connect(self.signInfo_close_pushButton_clicked)
        self.sign_InfoView.show()

    def signInfo_close_pushButton_clicked(self):
        self.sign_InfoView.close()
        self.sign_InfoView = None
        self.prentryView2.show()