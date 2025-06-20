import json
import math
import os
from view.setBuild import setBulidView
from view.setBulid_form.channelselect import channelselectView,channelimportView
from view.setBulid_form.pgb_form.form import pgbView
from PyQt5 import QtCore, QtGui, QtWidgets
from view.setBulid_form.secTable_form.form import SectableView
from view.setBulid_form import Fltselect
from PyQt5.Qt import *
import re
import warnings
from PyQt5.QtCore import QTimer

warnings.filterwarnings(action='ignore')


class setBuildController(QWidget):
    is_reload_controller = QtCore.pyqtSignal(str)
    init_reverse_scheme = QtCore.pyqtSignal(list, list)
    switch_signal = pyqtSignal(str)
    def __init__(self, client, cAppUtil,mainMenubar):
        super().__init__()
        try:
            self.client = client
            self.cAppUtil = cAppUtil
            self.view = setBulidView()
            self.mainMenubar=mainMenubar
            # 进度条加载界面
            self.progressBarView = None
            # 当前添加的标注类型
            self.addType = []
            # 构建集合时生成过滤器的下标
            self.search_index = list()
            # 集合表
            self.set_info = []
            # 构建成功的数据集是否覆盖,默认为否
            self.is_overlay = False
            # 集合名称是否合法
            self.isLegal = True
            # 为标注或状态的标记，True为标注，False为状态
            self.isType = True
            # 是否为第一次选择状态或者标注
            self.first_select = True
            # 反例构建方案,默认Random Select
            self.reverse_scheme = 'Random Select'
            # 主题信息
            self.themeInfo = []
            self.selectedTheme = []
            self.issearch=False
            # 筛选条件表格内容
            self.fltContent = []
            self.fltContentIndex = []
            self.finalContent = []
            self.fltSqlContent = {}
            self.fltAllInfo = {}
            self.view.fltTable(self.fltContent)
            self.fltview=None

            self.channel=[]#选择的通道
            self.ref=None #存储头皮通道选择view的对象
            self.ECIC=None #存储颅内的通道选择view对象
            self.savePath = ''
            self.startBlock = 0
            self.originPath = ''
            self.blockN = 0
            self.closeSig = False

            # 数据来源
            self.dataSource = []

            # 用来判断是否构建完成
            self.isBuildDone = False
            self.channel_state=[]

            # 一页显示多少行
            self.pageRows = 13
            self.curPageIndex = 1
            self.totalPage = 1

            self.client.getSetInitDataResSig.connect(self.getSetInitDataRes)
            self.client.delSetResSig.connect(self.delSetDataRes)
            self.client.getSetBuildFltDataResSig.connect(self.getSetBuildFltDataRes)
            self.client.getSetExportInitDataResSig.connect(self.getSetExportInitDataRes)
            self.client.buildSetSig.connect(self.buildSetRes)
            self.client.buildSetGetPgSig.connect(self.buildSetGetPgRes)
            self.client.buildSetCancelSig.connect(self.buildSetCancelRes)
            self.client.getSetSig.connect(self.getSetRes)
            self.client.getSetSearchSig.connect(self.setSearchRes)
            self.client.getSetDescribeSig.connect(self.showDescribeRes)
            self.view.set_page_control_signal.connect(self.rg_paging)
            self.client.getSetExportDataResSig.connect(self.getSetExportDataRes)
            self.view.ui.re_scheme.currentTextChanged.connect(self.on_reverse_scheme_changed)
            self.client.channel_matchResSig.connect(self.channel_matchRes)
            self.view.ui.pushButton_return.clicked.connect(self.exit_setbuild)

            self.view.ui.refChannel.clicked.connect(self.init_ref) #头皮通道选择
            self.view.ui.ECIC_Btn.clicked.connect(self.init_ECIC) #颅内通道选择
            # TODO 为了方便先暂时这样
            # self.view.ui.refChannel.model().item(0).setCheckState(Qt.Checked)
            # self.view.ui.lineEdit_3.setText('1')
            # self.view.ui.lineEdit_4.setText('0')
            # self.view.ui.lineEdit.setText('80')
            self.show_select()
        except Exception as e:
            print('__init__', e)
    def init_ECIC(self):
        if self.view.ui.lineEdit_3.text()=='':
            QMessageBox.information(self, '提示', '请先输入样本长度')
            return
        if self.ECIC==None:
            self.ECIC=channelimportView()
            self.ECIC.btn_confirm.clicked.connect(self.get_result)
            self.ECIC.btn_cancel.clicked.connect(self.ECIC.close)
        self.ECIC.show()
    def init_ref(self):
        if self.view.ui.lineEdit_3.text()=='':
            QMessageBox.information(self, '提示', '请先输入样本长度')
            return
        if self.ref==None:
            self.ref=channelselectView()
            self.ref.btn_confirm.clicked.connect(self.get_result)
            self.ref.btn_cancel.clicked.connect(self.ref.close)
        self.ref.show()

    def get_result(self):
        reply = QMessageBox.information(self, '提示', '确认选择后将锁定选定通道，重置筛选可解除锁定', QMessageBox.Yes | QMessageBox.No)
        if reply != 16384:
            return
        if self.ref!=None:
            selected = [cb.text() for cb in self.ref.checkboxes if cb.isChecked()]
            self.view.ui.refChannel.setEnabled(False)
            self.channel=selected
            self.ref.close()
        elif self.ECIC!=None:
            selected = [cb.text() for cb in self.ECIC.checkboxes if cb.isChecked()]
            self.view.ui.ECIC_Btn.setEnabled(False)
            self.channel = selected
            self.ECIC.close()
    def show_select(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("构建设置")
        msg_box.setText("请选择构建哪种脑电数据集")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # 修改标准按钮文本
        yes_btn = msg_box.button(QMessageBox.Yes)
        no_btn = msg_box.button(QMessageBox.No)

        msg_box.setWindowFlags(
            Qt.Dialog |  # 基础对话框类型
            Qt.WindowTitleHint |  # 保留标题栏
            Qt.CustomizeWindowHint  # 允许自定义窗口属性
        )
        msg_box.setEscapeButton(None)  # 禁用ESC键
        msg_box.setStyleSheet("""
                /* 调整按钮样式 */
                QPushButton {
                    font-size: 16px;          /* 字体大小 */
                    min-width: 100px;         /* 按钮最小宽度 */
                    min-height: 30px;         /* 按钮最小高度 */
                }

                /* 调整文本标签 */
                QLabel {
                    font-size: 20px;
                    margin-bottom: 20px;
                }
            """)
        if yes_btn:
            yes_btn.setText("头皮数据集")
        if no_btn:
            no_btn.setText("颅内数据集")
        yes_btn.clicked.connect(lambda: self.handle_scalp_dataset())
        no_btn.clicked.connect(lambda: self.handle_intracranial_dataset())
        msg_box.exec_()
    def exit_setbuild(self):
        # 发射切换信号，切换到 MainController
        self.switch_signal.emit("MainController")
        # 打开主菜单
        self.mainMenubar.setEnabled(True)
    def handle_scalp_dataset(self):
        self.set_signal = 'EEG' #头皮

        self.view.ui.groupBox_3.setTitle('头皮样本优选')
        # 数据初始化
        self.init_data()
        # 表格初始化,界面初始化默认先显示数据集的信息
        self.view.init_setTable(self.set_info)
    def handle_intracranial_dataset(self):
        self.set_signal = 'sEEG' #颅内
        self.view.ui.groupBox_3.setTitle('颅内样本优选')
        self.view.ui.label_checkid.setVisible(True)
        self.view.ui.comboBox_checkid.setVisible(True)
        # 数据初始化
        self.init_data()
        # 表格初始化,界面初始化默认先显示数据集的信息
        self.view.init_setTable(self.set_info)
    def exit(self):
        self.client.getSetInitDataResSig.disconnect()
        self.client.delSetResSig.disconnect()
        self.client.getSetBuildFltDataResSig.disconnect()
        self.client.getSetExportInitDataResSig.disconnect()
        self.client.buildSetSig.disconnect()
        self.client.buildSetGetPgSig.disconnect()
        self.client.buildSetCancelSig.disconnect()
        self.client.getSetSig.disconnect()
        self.view.set_page_control_signal.disconnect()
        self.client.getSetSearchSig.disconnect()
        self.client.getSetDescribeSig.disconnect()
        self.view.ui.pushButton_checkchennel.clicked.disconnect()
        self.client.channel_matchResSig.disconnect()

    # 数据初始化
    def init_data(self):
        setInitDataInfo = ["where category in ('正常波形','异常波形','伪迹波形')",
                           "where category in ('正常状态','异常状态','伪迹状态')",
                           ["distinct CONCAT(a.mid, '-', b.classifier_name)",
                            "label_info as a left join classifier as b on a.mid=b.classifier_id"],
                           self.client.tUser[12],
                           [1, self.pageRows, 'home']]
        self.mainMenubar.setDisabled(True)
        self.client.getSetInitData(setInitDataInfo)

    def dataSourceChange(self, isChecked):
        print(f'dataSourceChange')
        self.dataSource = []

        self.view.ui.label_31.setVisible(False)
        self.view.ui.themeBox.setVisible(False)

        if isChecked:
            if self.sender() == self.view.ui.radioButton1:
                self.dataSource.append('诊断标注')
            elif self.sender() == self.view.ui.radioButton2:
                self.dataSource.append('科研标注')
                self.view.ui.label_31.setVisible(True)
                self.view.ui.themeBox.setVisible(True)

            self.reset()

        print(f'dataSource: {self.dataSource}')

    def dataTypeChange(self, isChecked):
        print(f'dataTypeChange')
        self.view.ui.label_13.setVisible(False)
        self.view.ui.comboBox_5.setVisible(False)
        self.view.ui.label_30.setVisible(False)
        self.view.ui.refChannel.setVisible(False)
        self.view.ui.comboBox_2.setEnabled(False)
        self.view.ui.comboBox_3.setEnabled(False)
        self.view.ui.label_ECIC_30.setVisible(False)
        self.view.ui.ECIC_Btn.setVisible(False)

        if isChecked:
            if self.sender() == self.view.ui.radioButton3:
                # self.view.ui.label_13.setVisible(True) #参考方案
                # self.view.ui.comboBox_5.setVisible(True) #参考方案后的combox
                self.view.ui.comboBox_2.setEnabled(True) #波形类型的选择
            elif self.sender() == self.view.ui.radioButton4:
                if self.set_signal=='EEG':
                    self.view.ui.label_30.setVisible(True)#导联选取
                    self.view.ui.refChannel.setVisible(True) #导联选取后的combox
                    self.view.ui.comboBox_3.setEnabled(True) #状态类型的选择
                else:#颅内
                    self.view.ui.label_ECIC_30.setVisible(True)
                    self.view.ui.ECIC_Btn.setVisible(True)
                    self.view.ui.comboBox_3.setEnabled(True)
            self.reset()

    def rg_paging(self, page_to):
        if page_to[0] == "home":
            self.curPageIndex = 1
            self.view.ui.curPage.setText(str(self.curPageIndex))
        elif page_to[0] == "pre":
            if self.curPageIndex <= 1:
                return
            self.curPageIndex = self.curPageIndex - 1
            self.view.ui.curPage.setText(str(self.curPageIndex))
        elif page_to[0] == "next":
            if self.curPageIndex + 1 > self.totalPage:
                QMessageBox.information(self, "查询", f'最大页数：{self.totalPage}', QMessageBox.Yes)
                return False
            self.curPageIndex = self.curPageIndex + 1
            self.view.ui.curPage.setText(str(self.curPageIndex))
        elif page_to[0] == "final":
            self.curPageIndex = self.totalPage
            self.view.ui.curPage.setText(str(self.curPageIndex))
        elif page_to[0] == "confirm":
            pp = self.view.ui.skipPage.text()
            if pp=='':
                QMessageBox.information(self, '提示', '请输入页码')
                return False
            else:
                if int(pp) > self.totalPage:
                    QMessageBox.information(self, "查询", f'最大页数：{self.totalPage}', QMessageBox.Yes)
                    return False
            self.curPageIndex = int(pp)
            self.view.ui.curPage.setText(str(self.curPageIndex))
        if self.issearch:
            key_value= self.view.ui.lineEdit30.text()
            self.client.getSetSearch([self.curPageIndex, self.pageRows, 'home', key_value])
        else:
            msg = [self.curPageIndex, self.pageRows, page_to[0]]
            self.client.getSet(msg)

    def getSetInitDataRes(self, data):
        print(f'getSetInitDataRes: {data}')
        try:
            self.type_info = [info[1] for info in data[0]]
            self.type_ids = [info[0] for info in data[0]]
            self.state_info = [info[1] for info in data[1]]
            self.state_ids = [info[0] for info in data[1]]
            # 设置数据集信息
            tempSetInfo = []
            for id, name, config_id, des, fileTrain, fileTest in data[2][1]:
                print(f'des: {des}')
                tempType = json.loads(des)['type']
                print(f'tempType: {tempType}')
                tempSetInfo.append(
                    [id, name, '波形' if tempType == 'wave' else '状态', fileTrain, fileTest, config_id, des])

            self.set_info = tempSetInfo
            self.view.ui.totalPage.setText(f'共{str(math.ceil(data[2][0] / self.pageRows))}页')
            self.totalPage = math.ceil(data[2][0] / self.pageRows)
            self.view.init_setTable(self.set_info)
            self.set_data = [info[1] for info in data[2][1]]  # 数据集的模糊搜索

            self.all_model = data[3]
            self.montage = data[4]
            self.sampling_rate = data[5][0][2]
            self.reverse_scheme_list = data[6]
            self.themeInfo = data[7]

            list_view_model = QStandardItemModel()
            self.view.ui.re_scheme.setModel(list_view_model)
            self.view.ui.re_scheme.clear()
            item = QStandardItem()
            item.setText("Random Select")
            list_view_model.appendRow(item)
            item2 = QStandardItem()
            item2.setText("Cluster Select")
            list_view_model.appendRow(item2)


            revealMontage = ['Default'] + [item['name'] for item in self.montage]#参考方案
            # 初始化试图
            self.view.init_view(self.type_info, self.state_info, revealMontage, self.set_data, self.themeInfo)
            self.view.ui.comboBox_3.currentTextChanged.connect(
                lambda: self.init_typeFilters(comboBox=self.view.ui.comboBox_3, isType=False))

            self.view.ui.comboBox_2.currentTextChanged.connect(
                lambda: self.init_typeFilters(comboBox=self.view.ui.comboBox_2, isType=True))
            self.view.ui.comboBox_25.currentTextChanged.connect(self.patientChange)
            self.view.ui.comboBox_checkid.currentTextChanged.connect(self.check_nameChange)
            self.view.ui.pushButton_checkchennel.clicked.connect(self.channel_match)

            self.view.ui.themeBox.currentTextChanged.connect(self.themeChange)
            self.view.ui.pushButton.clicked.connect(self.setBuild)
            self.view.ui.tableWidget.customContextMenuRequested.connect(self.menu_select)
            self.view.ui.tableWidget_2.setContextMenuPolicy(Qt.CustomContextMenu)
            self.view.ui.tableWidget_2.customContextMenuRequested.connect(self.fltMenu)
            self.view.ui.lineEdit_2.textChanged.connect(self.on_lineEdit_2_text_changed)
            self.view.ui.pushButton_1.clicked.connect(lambda: self.reset(True))
            self.view.ui.pushButton_3.clicked.connect(self.addFlt)
            self.view.ui.resetSearch.clicked.connect(self.resetSearch)
            self.view.ui.setSearch.clicked.connect(self.setSearch)
            self.view.ui.radioButton1.toggled.connect(self.dataSourceChange)
            self.view.ui.radioButton2.toggled.connect(self.dataSourceChange)
            self.view.ui.radioButton3.toggled.connect(self.dataTypeChange)
            self.view.ui.radioButton4.toggled.connect(self.dataTypeChange)
            self.view.ui.lineEdit_3.textChanged.connect(self.spanChange)
        except Exception as e:
            print('getSetBuildTypeInfoRes', e)

    # 删除集合
    def delSetDataRes(self, data):
        print(f'delSetDataRes: {data}')
        if data[0] == '1':
            self.curPageIndex = 1
            self.view.ui.curPage.setText(str(self.curPageIndex))
            self.client.getSet([1, self.pageRows, 'home'])
        QMessageBox.information(self, '提示', data[1][0])

    # 现在下面那个改为图表格式，不采用目前的方式了
    # 点击添加筛选
    def addFlt(self):
        try:
            typeStr = self.curComboBox.currentText()
            user = self.view.ui.comboBox_24.currentText()
            patient = self.view.ui.comboBox_25.currentText()
            checkName = self.view.ui.comboBox_26.currentText()
            print(f'self.patient_ids: {self.patient_ids}')
        except Exception as e:
            print('addFlt', e)
            QMessageBox.information(self, '提示', '筛选信息为空')
            return
        print(f'addFlt typeStr: {typeStr}, user: {user}, patient: {patient}, checkName: {checkName}')
        tempInfo = [typeStr, user, patient, checkName]
        if self.set_signal=='EEG': #
            tempIndexs = [self.curComboBox.currentIndex(),
                          self.view.ui.comboBox_24.currentIndex() - 1,
                          self.view.ui.comboBox_25.currentIndex() - 1,
                          self.view.ui.comboBox_26.currentIndex() - 1]
        elif self.set_signal=='sEEG':
            tempIndexs = [self.curComboBox.currentIndex(),
                          self.view.ui.comboBox_24.currentIndex(),
                          self.view.ui.comboBox_25.currentIndex(),
                          self.view.ui.comboBox_26.currentIndex() -1]
        print(f'tempIndex: {tempIndexs}')
        print(f'type_ids: {self.type_ids}')
        print(f'user_ids: {self.user_ids}')
        print(f'patient_ids: {self.patient_ids}')
        print(f'fileName: {self.file_name}')
        if '' in tempInfo:
            QMessageBox.warning(self, '提示', '请重新选择选项')
            return
        if tempInfo in self.fltContent:
            QMessageBox.warning(self, '提示', '当前选项已添加，请重新选择')
            return
        self.fltContent.append(tempInfo) #存['tpye_name'，'user_name','patient_name','file_name']
        self.fltContentIndex.append(tempIndexs) #存对应选项的下标
        self.view.fltTable(self.fltContent)
        self.view.ui.comboBox_24.setEnabled(True) #配合通道匹配，添加筛选后恢复可选
        self.view.ui.comboBox_25.setEnabled(True)
        self.view.ui.comboBox_26.setEnabled(True)
        if self.view.ui.radioButton4.isChecked(): #是状态需要匹配的情况下恢复不可选，等匹配了才可选
            self.view.ui.pushButton_3.setEnabled(False) #添加筛选后恢复不可选

        try:
            id = -1
            if self.isType:
                info = self.type_info
            else:
                info = self.state_info
            for label_type in info:
                id += 1
                if label_type == self.curComboBox.currentText():
                    break
            print(f'id: {id}')
            self.addType.append(id) #获取添加的类型id
            self.search_index.append(str(id))
        except Exception as e:
            print('addFlt', e)

    # 搜索数据集
    def setSearch(self):
        print(f'setSearch')
        key_value = self.view.ui.lineEdit30.text()
        self.curPageIndex=1
        self.view.ui.curPage.setText(str(self.curPageIndex))
        self.client.getSetSearch([1, self.pageRows, 'home', key_value])

    def setSearchRes(self, data):
        print(f'setSearchRes')
        self.issearch=True
        self.getSetRes(data)

    def spanChange(self):
        print(f'spanChange')
        self.reset()

    # 重置数据集
    def resetSearch(self):
        print(f'resetSearch')
        self.issearch=False
        self.view.ui.lineEdit30.clear()
        self.curPageIndex=1
        self.view.ui.curPage.setText(str(self.curPageIndex))
        self.client.getSet([1, self.pageRows, 'home'])
    def patientChange(self):
        if self.set_signal=='EEG': #头皮
            self.view.ui.comboBox_26.clear()
            if self.view.ui.comboBox_25.currentText() not in self.file_name.keys():
                return
            if self.view.ui.comboBox_25.currentText() != '全部':
                self.view.ui.comboBox_26.setEnabled(True)
                fileName = [item[0] for item in self.file_name[self.view.ui.comboBox_25.currentText()]]
                self.view.ui.comboBox_26.addItems(['全部'] + fileName)
            else:
                self.view.ui.comboBox_26.setEnabled(False)
                self.view.ui.comboBox_26.addItems(['全部'])
        elif self.set_signal=='sEEG':
            self.view.ui.comboBox_checkid.clear()
            if self.view.ui.comboBox_25.currentText() not in self.file_name.keys():
                return
            if self.view.ui.comboBox_25.currentText() != '全部':
                self.view.ui.comboBox_checkid.setEnabled(True)
                fileName = [item[0] for item in self.file_name[self.view.ui.comboBox_25.currentText()]]
                check_name=fileName[0].split('-')[0]
                self.view.ui.comboBox_checkid.addItems([check_name])

    def check_nameChange(self):
        self.view.ui.comboBox_26.clear()
        self.view.ui.comboBox_26.setEnabled(True)
        patient = self.view.ui.comboBox_25.currentText()
        checkName=self.view.ui.comboBox_checkid.currentText()
        if patient!='': #避免重置时报错
            matched_files = [
                file_name for file_name, _ in self.file_name[patient]
                if file_name.startswith(checkName)
            ]
            self.view.ui.comboBox_26.addItems(['全部'] + matched_files)
    def themeChange(self):
        print(f'themeChange')
        self.selectedTheme = [self.themeInfo[i.row() - 1] for i in self.view.ui.themeBox.get_selected()]
        print(f'selectedTheme: {self.selectedTheme}')

    def fltMenu(self, pos):
        row_num = -1
        for i in self.view.ui.tableWidget_2.selectionModel().selection().indexes():
            row_num = i.row()
        if row_num == -1:
            return
        menu = QMenu()
        item1 = menu.addAction(u"删除")
        action = menu.exec_(self.view.ui.tableWidget_2.mapToGlobal(pos))
        if action == item1:
            self.fltDelete(row_num)

    def fltDelete(self, pos):
        print(f'fltDelete pos: {pos}')
        del self.fltContent[pos]
        del self.fltContentIndex[pos]
        self.view.fltTable(self.fltContent)

        del self.addType[pos]
        del self.search_index[pos]
        print(f'fltContent: {self.fltContent}')
        print(f'addType: {self.addType}')
        print(f'search_index: {self.search_index}')

    def getSetBuildFltDataRes(self, data):
        print(f'getSetBuildFltDataRes: {data}')

        if data[0] == '0':
            QMessageBox.information(self, '提示', data[1])
            self.reset(False)
            return
        else:
            data = dict(data[1])

        self.patient_name = [info[1] for info in data['patientName']]
        self.patient_ids = [info[0] for info in data['patientName']]
        self.measure_date = [d.strftime("%Y-%m-%d") for d in data['measureDate'][0]]
        self.file_name = data['fileName']
        # tempt=[item[0][0] for item in self.file_name]
        # self.check_num = [file_name.split('-')[0] for file_name in tempt] #提取检查单号名称
        self.user = [info[1] for info in data['user']]
        self.user_ids = [info[0] for info in data['user']]

        if self.isType:
            selected_type_id = self.type_ids[self.view.ui.comboBox_2.currentIndex()]
        else:
            selected_type_id = self.state_ids[self.view.ui.comboBox_3.currentIndex()]

        self.fltAllInfo[selected_type_id] = [self.patient_name, self.patient_ids, self.measure_date, self.file_name,
                                             self.user, self.user_ids]
        print(f'fltAllInfo: {self.fltAllInfo}')

        if self.set_signal=='EEG': #头皮
            self.view.ui.comboBox_24.clear()
            self.view.ui.comboBox_24.addItems(['全部'] + self.user)
            self.view.ui.comboBox_25.clear()
            self.view.ui.comboBox_25.addItems(['全部'] + self.patient_name)
            self.view.ui.comboBox_26.addItems(['全部'])
            self.view.ui.comboBox_26.setEnabled(False)
        elif self.set_signal=='sEEG': #颅内
            self.view.ui.comboBox_24.clear()
            self.view.ui.comboBox_24.addItems(self.user)
            self.view.ui.comboBox_25.clear()
            self.view.ui.comboBox_25.addItems(self.patient_name)
            # self.view.ui.comboBox_checkid.addItems(self.check_num) #添加相应单号
            # self.view.ui.comboBox_checkid.setEnabled(False)
            # self.view.ui.comboBox_26.addItems(['全部'])
            # self.view.ui.comboBox_26.setEnabled(False)

    # 响应集合名称输入框：输入判断
    def on_lineEdit_2_text_changed(self):
        self.isLegal = True
        setName = self.view.ui.lineEdit_2.text()
        if setName != '':
            illegal_str = ["\"", r"*", r"<", r">", r"?", r"\\", r"/", r"|", r":"]
            for i in illegal_str:
                patten = r"[{}]".format(i)
                result = re.search(patten, setName)
                if result is not None:
                    self.isLegal = False
                    self.view.ui.label_9.setText('名称非法')
                    break
            if self.isLegal:
                self.view.ui.label_9.setText('')
        else:
            self.isLegal = True
            self.view.ui.label_9.setText('尚未命名')

    # 重置标注或者状态comboBox
    def reset(self, delFlt=True):
        print(f'reset')
        try:
            self.view.ui.comboBox_24.clear()
            self.view.ui.comboBox_25.clear()
            self.view.ui.comboBox_26.clear()

            self.view.clear(self.view.ui.horizontalLayout_14)
            self.view.set_add_tip(self.view.ui.comboBox_2, self.view.line_edit, self.addType, self.type_info)
            self.view.set_add_tip(self.view.ui.comboBox_3, self.view.line_edit_1, self.addType, self.state_info)
            self.view.line_edit.clear()
            self.view.line_edit_1.clear()
            self.isType = True
            self.first_select = True

            self.view.ui.comboBox_24.setEnabled(False)  # 解除锁定选中的标注用户，病人，文件
            self.view.ui.comboBox_25.setEnabled(False)
            self.view.ui.comboBox_26.setEnabled(False)
            if self.set_signal=='sEEG':
                self.view.ui.comboBox_checkid.setEnabled(False)

            if delFlt:
                self.fltContent.clear()
                self.fltContentIndex.clear()
                self.search_index.clear()
                self.addType.clear()
                self.view.fltTable(self.fltContent)

                self.view.ui.ECIC_Btn.setEnabled(True)  # 重置筛选后可以重新选择通道
                self.view.ui.refChannel.setEnabled(True)
                self.channel = []  # 重置已选通道

                self.fltview = None  # 重置筛选后匹配将清零

                self.view.ui.comboBox_24.setEnabled(False)
                self.view.ui.comboBox_25.setEnabled(False)
                self.view.ui.comboBox_26.setEnabled(False)
                self.view.ui.pushButton_checkchennel.setEnabled(False)
        except Exception as e:
            print('reset', e)

    # 获取初始数据
    def init_typeFilters(self, comboBox=None, isType=True): #T是波形 #F是状态
        print(f'init_typeFilters')
        self.isType = isType
        if comboBox.currentText() == "":
            return
        dataSource = self.dataSource
        if len(dataSource) == 0:
            comboBox.setCurrentText("")
            QMessageBox.information(self, '提示', '尚未选择数据来源')
            self.view.ui.comboBox_2.setEnabled(True)
            self.view.ui.comboBox_3.setEnabled(True)
            self.view.ui.comboBox.clear()
            self.view.ui.comboBox.addItems(['中心延拓', '极值延拓'])
            return

        print(f'data_source: {dataSource}')
        if '科研标注' in dataSource and len(self.selectedTheme) == 0:
            QMessageBox.information(self, '提示', '尚未选择主题')
            self.reset(False)
            return
        if isType:
            self.view.ui.comboBox_5.setEnabled(True)
            info = self.type_info
            self.view.ui.comboBox_2.setEnabled(True)
            self.view.ui.comboBox_3.setEnabled(False)
            self.view.ui.pushButton_3.setEnabled(True)
            self.view.ui.comboBox.clear()
            self.view.ui.comboBox.addItems(['中心延拓', '极值延拓'])
            if self.first_select:
                self.first_select = False
                self.view.clear(self.view.ui.horizontalLayout_14)
            if comboBox.currentText() not in self.type_info:
                return
        else:
            if comboBox.currentText() not in self.state_info:
                return
            if self.channel == []:
                QMessageBox.information(self, '提示', '尚未选择通道')
                self.reset(False)
                return
            info = self.state_info
            # self.view.ui.refChannel.setEnabled(True)
            self.view.ui.comboBox_2.setEnabled(False)
            self.view.ui.comboBox_3.setEnabled(True)
            self.view.ui.pushButton_3.setEnabled(False)
            self.view.ui.comboBox.clear()
            self.view.ui.comboBox.addItems(['中心延拓', '极值延拓'])
            self.view.ui.pushButton_checkchennel.setEnabled(True)
        self.view.ui.comboBox_24.setEnabled(True)
        self.view.ui.comboBox_25.setEnabled(True)
        self.view.ui.comboBox_26.setEnabled(True)

        id = -1
        for label_type in info:
            id += 1
            if label_type == comboBox.currentText():
                break
        if id in self.addType:
            comboBox.setCurrentText("")
            QMessageBox.information(self, '提示', '该标注类型已添加，请勿重复添加')
            return
        self.id = id
        self.curComboBox = comboBox

        if self.view.ui.lineEdit_3.text() == "" or self.view.ui.lineEdit_4.text() == "":
            QMessageBox.warning(self, '提示', '请输入完整的信息')
            self.view.ui.comboBox_24.setEnabled(False)
            self.view.ui.comboBox_25.setEnabled(False)
            self.view.ui.comboBox_26.setEnabled(False)
            self.view.ui.pushButton_checkchennel.setEnabled(False)
            return
        self.span = int(float(self.view.ui.lineEdit_3.text()) * self.sampling_rate)
        self.minSpan = int(float(self.view.ui.lineEdit_4.text()) * self.sampling_rate)
        print(f'span: {self.span}, minSpan: {self.minSpan}')

        self.client.getSetBuildFltData([dataSource, comboBox.itemText(id), self.span,
                                        self.minSpan, self.selectedTheme,self.set_signal])

    # 构建数据集
    def setBuild(self):
        search_table, tag = self.build_check()
        print(f'search_table: {search_table}')
        if not tag:
            return
        reply = QMessageBox.information(self, '提示', '是否构建数据集', QMessageBox.Yes | QMessageBox.No)
        if reply != 16384:
            return

        setName = self.view.ui.lineEdit_2.text()
        self.is_overlay = False
        tempSetInfo = {item[1]: item[0] for item in self.set_info}

        set_id = -1
        if setName in tempSetInfo.keys():
            QMessageBox.information(self, '提示', '集合已存在')
            return
        print(f'threadRun set_id: {set_id}')

        if self.view.ui.comboBox.currentText() == '中心延拓':
            self.extension = 'center'
        else:
            self.extension = 'max'
        self.train_ratio = int(self.view.ui.lineEdit.text()) / 100
        if int(self.view.ui.counter_ratio.currentText()) == 0:
            self.ratio = 0
        else:
            self.ratio = int(self.view.ui.positive_ratio.currentText()) / int(self.view.ui.counter_ratio.currentText())

        # 这部分开始放到服务器上面
        msg = {'is_overlay': self.is_overlay, 'reverse_scheme': self.reverse_scheme}

        if 'sample_info' in search_table:
            source = 'research'
        elif 'resLab' in search_table:
            source = 'diagnosis'
        else:
            source = 'label'

        type = 'wave' if self.isType else 'state'
        if type == 'wave':
            nChannel = 1
            if self.view.ui.comboBox_5.currentText() == 'Default':#没有删除 直接做隐藏，波形直接默认Default
                channels = ['Default']
            else:
                channels = self.montage[self.view.ui.comboBox_5.currentIndex() - 1]['channels']
        else:
            if self.set_signal == 'EEG':#头皮
                channels = self.channel
                nChannel = len(channels)
            else: #颅内
                channels=self.channel
                nChannel = len(channels)
            if channels==[]:
                QMessageBox.information(self, '提示', '尚未选择通道')
                return

        print(f'nChannel: {nChannel}, channels: {channels}, {self.channel}')

        # 重新生成content
        self.finalContent.clear()
        print(f'fltContentIndex: {self.fltContentIndex}')

        for tempIndex in self.fltContentIndex:
            # 获取对应type_id的索引值（确保总是非负）
            if self.isType:
                selected_type_id = self.type_ids[tempIndex[0]]
            else:
                selected_type_id = self.state_ids[tempIndex[0]]
            print(f'selected_type_id: {selected_type_id}')
            tempInfo = self.fltAllInfo[selected_type_id]
            print(f'tempInfo: {tempInfo}')

            file_names = {item: tempInfo[3][tempInfo[0][i]] for i, item in enumerate(tempInfo[1])}
            print(f'file_names: {file_names}') #{patient_id：[('file_name',(check_id,file_id)]}

            # 判断user_ids是否全选
            selected_user_ids = tempInfo[5] if tempIndex[1] == -1 else [tempInfo[5][tempIndex[1]]] #标注用户id
            print(f'selected_user_ids: {selected_user_ids}')
            # 判断patient_ids是否全选
            if tempIndex[2] == -1:
                print(f'病人全选')
                selected_patient_ids = tempInfo[1]
                selected_file_names = {pid: file_names[pid] for pid in tempInfo[1]}
            else:
                selected_patient_ids = [tempInfo[1][tempIndex[2]]]
                selected_file_names = {tempInfo[1][tempIndex[2]]: [file_names[tempInfo[1][tempIndex[2]]][tempIndex[3]]]}
            print(f'selected_patient_ids: {selected_patient_ids}')
            print(f'selected_file_names: {selected_file_names}')

            # 生成所有可能的组合
            for user_id in selected_user_ids:
                for patient_id in selected_patient_ids:
                    current_file_names = selected_file_names[patient_id]
                    for file_name in current_file_names:
                        self.finalContent.append((selected_type_id, user_id, patient_id, file_name[1]))

        print(self.finalContent)

        self.msg = {'type': type,
                    'sampleRate': self.sampling_rate,
                    'span': self.span,
                    'nChannel': nChannel,
                    'channels': channels,
                    'source': source,
                    'themeID': [item[0] for item in self.selectedTheme],
                    'minSpan': self.minSpan,
                    'ratio': self.ratio,
                    'trainRatio': self.train_ratio,
                    'scheme': self.reverse_scheme,
                    'extension': self.extension,
                    'content': self.finalContent}

        msgJson = json.dumps(self.msg)
        print(msgJson)

        self.view.ui.pushButton.setEnabled(False)
        self.client.buildSet([setName, msgJson, self.client.tUser[12], type,msg])

    # 构建前的检查,如果存在不符合的条件则弹出提示
    def channel_match(self):
        self.view.ui.pushButton_checkchennel.setEnabled(False)
        tempIndex = [self.curComboBox.currentIndex(),
                      self.view.ui.comboBox_24.currentIndex(),
                      self.view.ui.comboBox_25.currentIndex(),
                      self.view.ui.comboBox_26.currentIndex() - 1]
        match_content=[]
        # 获取对应type_id的索引值（确保总是非负）
        if self.isType:
            selected_type_id = self.type_ids[tempIndex[0]]
        else:
            selected_type_id = self.state_ids[tempIndex[0]]
        print(f'selected_type_id: {selected_type_id}')
        tempInfo = self.fltAllInfo[selected_type_id]
        print(f'tempInfo: {tempInfo}')

        file_names = {item: tempInfo[3][tempInfo[0][i]] for i, item in enumerate(tempInfo[1])}
        print(f'file_names: {file_names}') #{patient_id：[('file_name',(check_id,file_id)]}

        # 判断user_ids是否全选
        selected_user_ids = tempInfo[5] if tempIndex[1] == -1 else [tempInfo[5][tempIndex[1]]] #标注用户id
        print(f'selected_user_ids: {selected_user_ids}')
        # 判断patient_ids是否全选
        if tempIndex[2] == -1:
            print(f'病人全选')
            selected_patient_ids = tempInfo[1]
            selected_file_names = {pid: file_names[pid] for pid in tempInfo[1]}
        else:
            selected_patient_ids = [tempInfo[1][tempIndex[2]]]
            selected_file_names = {tempInfo[1][tempIndex[2]]: [file_names[tempInfo[1][tempIndex[2]]][tempIndex[3]]]}
        print(f'selected_patient_ids: {selected_patient_ids}')
        print(f'selected_file_names: {selected_file_names}')

        # 生成所有可能的组合
        for user_id in selected_user_ids:
            for patient_id in selected_patient_ids:
                current_file_names = selected_file_names[patient_id]
                for file_name in current_file_names:
                    match_content.append((selected_type_id, user_id, patient_id, file_name[1],file_name[0]))
        self.client.channel_match(match_content)

    def channel_matchRes(self,REPData):
        self.view.ui.pushButton_checkchennel.setEnabled(True)
        if REPData[0]=='1':
            data=REPData[1]
            self.channel_state=data
            if self.fltview:
                self.fltview.update_data(self.channel,self.channel_state)
            else:
                self.fltview=Fltselect.ChannelDataViewer(self.channel,self.channel_state)
                self.fltview.pass_btn.clicked.connect(self.flt_pass)
            self.fltview.show()
        else:
            QMessageBox.information(self, "提示","获取构建数据集所需的通道信息失败")
    def flt_pass(self):
        self.view.ui.pushButton_3.setEnabled(True)
        self.view.ui.comboBox_24.setEnabled(False) # 锁定选中的标注用户，病人，文件
        self.view.ui.comboBox_25.setEnabled(False)
        self.view.ui.comboBox_26.setEnabled(False)
        self.view.ui.comboBox_checkid.setEnabled(False)
        self.fltview.close()

    def build_check(self):
        tag = True
        search_table = []
        if self.view.ui.lineEdit_2.text() == '':
            QMessageBox.information(self, '提示', '数据集尚未命名')
            tag = False
            return search_table, tag
        elif self.view.ui.lineEdit_2.text() != '' and not self.isLegal:
            QMessageBox.information(self, '提示', '数据集命名非法')
            tag = False
            return search_table, tag
        if len(self.dataSource) == 0:
            QMessageBox.information(self, '提示', '尚未选择数据来源')
            tag = False
            return search_table, tag
        if self.view.ui.lineEdit_3.text() == '':
            QMessageBox.information(self, '提示', '尚未填写集合样本长度')
            tag = False
            return search_table, tag
        if self.view.ui.lineEdit_4.text() == '':
            QMessageBox.information(self, '提示', '尚未填写样本下沿阈值')
            tag = False
            return search_table, tag
        elif float(self.view.ui.lineEdit_4.text()) > float(self.view.ui.lineEdit_3.text()):
            QMessageBox.information(self, '提示', '下沿阈值不可大于样本长度')
            tag = False
            return search_table, tag
        elif float(self.view.ui.lineEdit_4.text()) < 0:
            QMessageBox.information(self, '提示', '下沿阈值不可小于0')
            tag = False
            return search_table, tag
        if self.view.ui.lineEdit.text() == '':
            QMessageBox.information(self, '提示', '尚未设置训练集比率')
            tag = False
            return search_table, tag
        # 添加延拓规则到description
        ruler = self.view.ui.comboBox.currentText()
        if ruler == '':
            QMessageBox.information(self, '提示', '尚未选择延拓规则')
            tag = False
            return search_table, tag
        if len(self.addType) == 0:
            QMessageBox.information(self, '提示', '尚未添加任何标注类型')
            tag = False
            return search_table, tag

        return search_table, tag

    def buildSetRes(self, data):
        print(f'buildSetRes: {data}')
        # data = ['start', 0]
        if data[0] == 'start':
            self.isBuildDone = False
            # 启动进度条
            self.progressBarView = QProgressDialog('集合构建中...', '取消', 0, 100, self)
            self.progressBarView.setWindowTitle('构建数据集')
            self.progressBarView.setFixedSize(300, 80)
            self.progressBarView.canceled.connect(self.buildSetCancel)
            self.progressBarView.show()

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.buildSetGetPg)
            # 每隔5秒联系一次服务器
            self.timer.start(3000)
        else:
            self.view.ui.pushButton.setEnabled(True)
            QMessageBox.information(self, "提示", data[0])

    # 联系服务器获取当前进度
    def buildSetGetPg(self):
        print(f'buildSetGetPg')
        self.client.buildSetGetPg([])

    def buildSetGetPgRes(self, data):
        print(f'buildSetGetPgRes data: {data}')
        if data[0] == '1':
            self.setBuildPgbValue(int(data[3][1]))
            if (int(data[3][1]) >= 100):
                print(f'buildSetGetPgRes OK')
                self.timer.stop()
                QMessageBox.information(self, "提示", "构建数据集成功")
                self.view.ui.pushButton.setEnabled(True)
                # 刷新数据集列表
                self.curPageIndex = 1
                self.view.ui.curPage.setText(str(self.curPageIndex))
                self.client.getSet([1, self.pageRows, 'home'])
        else:
            self.view.ui.pushButton.setEnabled(True)
            self.timer.stop()
            self.isBuildDone = True
            self.progressBarView.close()
            QMessageBox.information(self, "提示", data[2])

    def getSetRes(self, data):
        print(f'getSetRes: {data}')
        if data[0] == '1':
            # 设置数据集信息
            tempSetInfo = []
            for id, name, config_id, des, fileTrain, fileTest in data[1][1]:
                print(f'des: {des}')
                tempType = json.loads(des)['type']
                print(f'tempType: {tempType}')
                tempSetInfo.append(
                    [id, name, '波形' if tempType == 'wave' else '状态', fileTrain, fileTest, config_id, des])
            self.set_info = tempSetInfo
            self.view.ui.totalPage.setText(f'共{str(math.ceil(data[1][0] / self.pageRows))}页')
            self.totalPage = math.ceil(data[1][0] / self.pageRows)
            self.view.init_setTable(self.set_info)

    # 回传进度条参数
    def setPgbValue(self, i):
        self.progressBarView.pgb.setValue(i)

    # 设置表格右键可呼出菜单,包括:样本集详细信息和删除集合
    def menu_select(self, pos):
        row_num = -1
        for i in self.view.ui.tableWidget.selectionModel().selection().indexes():
            row_num = i.row()
        if row_num == -1:
            return
        set_name = self.view.ui.tableWidget.item(row_num, 0).text()
        set_type = self.view.ui.tableWidget.item(row_num, 1).text()

        set_id = self.set_info[row_num][0]
        menu = QMenu()
        item1 = menu.addAction(u"详细信息")
        # item2 = menu.addAction(u"集合重建")
        item4 = menu.addAction(u"训练集导出")
        item5 = menu.addAction(u"测试集导出")
        item3 = menu.addAction(u"删除集合")
        action = menu.exec_(self.view.ui.tableWidget.mapToGlobal(pos))
        if action == item1:
            self.showDescribe(self.set_info[row_num])
        # elif action == item2:
        #     self.setRebuild(set_name, set_type)
        if action == item3:
            self.delSet(set_id, row_num)
        elif action == item4:
            self.set_export(set_id, set_type='training')
        elif action == item5:
            self.set_export(set_id, set_type='test')

    def showDescribe(self, setInfo):
        print(f'showDescribe setInfo: {setInfo}')
        self.selectedSetDesc = setInfo
        self.client.getSetDescribe(self.selectedSetDesc.copy())

    def showDescribeRes(self, setDesc):
        print(f'showDescribeRes setDesc: {setDesc}')
        description = json.loads(self.selectedSetDesc[6])
        if description['type'] == 'wave':
            self.id_to_info = dict(zip(self.type_ids + [0], self.type_info + ['负例']))
        else:
            self.id_to_info = dict(zip(self.state_ids + [0], self.state_info + ['负例']))

        trainSetInfo = {self.id_to_info[int(k)]: v for k, v in setDesc[1][0].items() if int(k) in self.id_to_info}
        testSetInfo = {self.id_to_info[int(k)]: v for k, v in setDesc[1][1].items() if int(k) in self.id_to_info}

        print(f'trainSetInfo: {trainSetInfo}, testSetInfo: {testSetInfo}')

        self.secView = SectableView(description=description, trainSetInfo=trainSetInfo, testSetInfo=testSetInfo)
        self.secView.show()

    # 集合删除(连同npz文件一起删除)
    def delSet(self, set_id, rowIndex):
        reply = QMessageBox.information(self, '提示', '是否删除选中集合', QMessageBox.Yes | QMessageBox.No)
        if reply == 16384:
            try:
                # 删除数据库中的集合数据
                REQmsg = self.set_info[rowIndex].copy()
                self.client.delSet(REQmsg)
            except Exception as e:
                print(e)
                return

    # 集合导出
    def set_export(self, set_id, set_type='training'):
        # reply = QMessageBox.information(self, "提示", "是否导出集合", QMessageBox.Yes | QMessageBox.No)
        # if reply != 16384:
        #     return

        downloadPath = 'download'
        if not os.path.exists(downloadPath):
            os.makedirs(downloadPath)

        if os.listdir(downloadPath):
            QMessageBox.information(self, "提示", "系统正在处理未完成的下载任务，完成后才能启动新的下载任务")
            # if reply == 16384:
            # TODO 在这里继续完成之前的操作
            file_path = 'download/downloading.txt'
            pattern = r'.*?\.npz\s*, \s*.*?\.npz\s*, \s*block_id=\d+\s*, \s*blockN=\d+'
            with open(file_path, 'r') as file:
                content = file.read()
                print(content)

            if not os.path.exists(file_path) or not bool(re.match(pattern, content)):
                QMessageBox.information(self, '提示', '本地文件系统出错，下载过程需重新启动')
                if os.path.exists(file_path):
                    os.remove(file_path)
                return

            fData = content.split(', ')
            print(f'fData: {fData}')
            startBlock = int(fData[2].split('=')[1])
            blockN = int(fData[3].split('=')[1])
            print(f'startBlock: {startBlock}')

            # self.setExportThread = setExportThread(client=self.client, cAppUtil=self.cAppUtil, savePath=fData[0],
            #                                        originPath=fData[1], startBlock=startBlock, blockN=blockN)
            # self.setExportThread.progress.connect(self.setExportPgbValue)
            # self.setExportThread.start()

            self.savePath = fData[0]
            self.startBlock = startBlock
            self.originPath = fData[1]
            self.blockN = blockN
            self.client.getSetExportData(['download', self.originPath, f'block_id={self.startBlock + 1}'])

            # self.progressBarView = progressBarView(window_title="集合导出中...", hasStopBtn=False,
            #                                        maximum=100,
            #                                        speed=5)
            # self.progressBarView.ui.progressBar.setFixedSize(300, 80)
            # self.progressBarView.ui.progressBar.canceled.connect(self.onExportPgbCancel)
            # self.progressBarView.show()
            # self.progressBarView.updateProgressBar(0)

            # 启动进度条，然后向服务器获取block=1的数据
            self.progressBarView = QProgressDialog('集合导出中...', '取消', 0, 100, self)
            self.progressBarView.setWindowTitle('构建数据集模块')
            self.progressBarView.setFixedSize(300, 80)
            self.progressBarView.canceled.connect(self.onExportPgbCancel)
            self.progressBarView.show()
            # else:
            #     # 如果不想继续上传，那么就清空文件夹
            #     for filename in os.listdir(downloadPath):
            #         file_path = os.path.join(downloadPath, filename)
            #         if os.path.isfile(file_path) or os.path.islink(file_path):
            #             os.unlink(file_path)
        else:
            print(f'set_id: {set_id}')
            self.client.getSetExportInitData(['want', set_id, set_type])

    def getSetExportInitDataRes(self, data):
        print(f'getSetExportInitDataRes: {data}')
        if data[0] == 'wrongSetname':
            QMessageBox.information(self, '提示', '数据集信息有误，无法下载')
        elif data[0] == 'rightSetname':
            savePath, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "npz Files (*.npz)")
            if savePath:
                print(f"选择的保存路径是: {savePath}")
            else:
                QMessageBox.information(self, '提示', '未选择有效保存路径')
                return

            # 创建txt文件，并写入初始数据
            fileName = os.path.basename(data[1])
            content = f'{fileName}, {fileName}, block_id=1, blockN={data[2]}'
            self.cAppUtil.writeTxt(file_path='download/downloading.txt', content=content)
            # with open('download/downloading.txt', 'w', encoding='utf-8') as file:
            #     file.write(content)

            # self.client.getSetExportData(['download', data[1], f'block_id=1'])

            # self.setExportThread = setExportThread(client=self.client, cAppUtil=self.cAppUtil, savePath=savePath,
            #                                        originPath=data[1], startBlock=0, blockN=data[2])
            # self.setExportThread.progress.connect(self.setExportPgbValue)
            # self.setExportThread.start()

            self.savePath = savePath
            self.startBlock = 0
            self.originPath = data[1]
            self.blockN = data[2]
            self.client.getSetExportData(['download', self.originPath, f'block_id={self.startBlock + 1}'])

            # self.progressBarView = progressBarView(window_title="集合导出中...", hasStopBtn=False,
            #                                        maximum=100,
            #                                        speed=5)
            # self.progressBarView.ui.progressBar.setFixedSize(300, 80)
            # self.progressBarView.ui.progressBar.canceled.connect(self.onExportPgbCancel)
            # self.progressBarView.show()
            # self.progressBarView.updateProgressBar(0)

            # 启动进度条，然后向服务器获取block=1的数据
            self.progressBarView = QProgressDialog('集合导出中...', '取消', 0, 100, self)
            self.progressBarView.setWindowTitle('构建数据集模块')
            self.progressBarView.setFixedSize(300, 80)
            self.progressBarView.canceled.connect(self.onExportPgbCancel)
            self.progressBarView.show()
        else:
            pass

    def getSetExportDataRes(self, data):
        try:
            self.cAppUtil.writeByte(self.savePath, data[1])
            self.curBlockID = int(data[0].split('=')[1])
            print(f'self.curBlockID: {self.curBlockID}')
            file_path = 'download/downloading.txt'
            if self.curBlockID <= self.blockN:
                # 创建txt文件，并写入初始数据
                # fileName = os.path.basename(self.originPath)
                # saveName = os.path.basename(self.savePath)
                content = f'{self.savePath}, {self.originPath}, block_id={self.curBlockID}, blockN={self.blockN}'
                print(f'content: {content}')
                self.cAppUtil.writeTxt(file_path=file_path, content=content)
                # with open(file_path, 'w', encoding='utf-8') as file:
                #     file.write(content)

                self.setExportPgbValue(int(self.curBlockID / self.blockN * 100))
                # self.progress.emit(int(self.curBlockID / self.blockN * 100))
                if self.curBlockID + 1 > self.blockN:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"下载完成，文件 {file_path} 删除")
                else:
                    if not self.closeSig:
                        self.client.getSetExportData(['download', self.originPath, f'block_id={self.curBlockID + 1}'])
                    else:
                        print(f"下载中断")
        except Exception as e:
            print('getSetExportDataRes', e)

    # 回传进度条参数
    def setExportPgbValue(self, i):
        print(f'setPgbValue: {i}')
        if i >= 100:
            self.progressBarView.close()
            QMessageBox.information(self, '提示', '数据集下载完成')
        else:
            self.progressBarView.setValue(i)

    # 回传构建数据集进度条参数
    def setBuildPgbValue(self, i):
        print(f'setBuildPgbValue: {i}')
        if i >= 100:
            self.isBuildDone = True
            self.progressBarView.close()
        else:
            self.progressBarView.setValue(i)

    def onExportPgbCancel(self):
        print('onExportPgbCancel: ')
        # self.setExportThread.closeSig = True
        self.closeSig = True

    def buildSetCancel(self):
        print('buildSetCancel: ')
        self.view.ui.pushButton.setEnabled(True)
        if not self.isBuildDone:
            self.timer.stop()
            self.isBuildDone = True
            self.client.buildSetCancel([])

    def buildSetCancelRes(self, data):
        print(f'buildSetCancel: {data}')
        QMessageBox.information(self, '提示', data[1])

    def on_reverse_scheme_changed(self, current_scheme):
        self.reverse_scheme = current_scheme


class setExportThread(QThread):
    # 绑定进度条
    progress = pyqtSignal(int)

    def __init__(self, client, cAppUtil, savePath=None, originPath=None, startBlock=0, blockN=1):
        super(setExportThread, self).__init__()
        self.client = client
        self.cAppUtil = cAppUtil
        self.savePath = savePath
        self.startBlock = startBlock
        self.originPath = originPath
        self.blockN = blockN
        self.closeSig = False
        self.client.getSetExportDataResSig.connect(self.getSetExportDataRes)

    def run(self) -> None:
        self.getSetExportData()

    def getSetExportData(self):
        self.client.getSetExportData(['download', self.originPath, f'block_id={self.startBlock + 1}'])

    def getSetExportDataRes(self, data):
        try:
            self.cAppUtil.writeByte(self.savePath, data[1])
            self.curBlockID = int(data[0].split('=')[1])
            print(f'self.curBlockID: {self.curBlockID}')
            file_path = 'download/downloading.txt'
            if self.curBlockID <= self.blockN:
                # 创建txt文件，并写入初始数据
                # fileName = os.path.basename(self.originPath)
                # saveName = os.path.basename(self.savePath)
                content = f'{self.savePath}, {self.originPath}, block_id={self.curBlockID}, blockN={self.blockN}'
                print(f'content: {content}')
                self.cAppUtil.writeTxt(file_path=file_path, content=content)
                # with open(file_path, 'w', encoding='utf-8') as file:
                #     file.write(content)

                self.progress.emit(int(self.curBlockID / self.blockN * 100))
                if self.curBlockID + 1 > self.blockN:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"下载完成，文件 {file_path} 删除")
                else:
                    if not self.closeSig:
                        self.client.getSetExportData(['download', self.originPath, f'block_id={self.curBlockID + 1}'])
                    else:
                        print(f"下载中断")
        except Exception as e:
            print('getSetExportDataRes', e)
