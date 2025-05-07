import math
from functools import partial

from PyQt5.Qt import *
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import *
from view.taskSettings import taskSettingsView
from view.taskSettings import AddThemeFormView
from view.taskSettings import TableWidget
from view.taskSettings_form.patientInfo.patient_table import PatientTableWidget
import re

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import copy
from datetime import datetime
from functools import partial


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
import numpy as np
import sys, re
from PyQt5.QtWidgets import QTableWidgetItem
from itertools import product
from view.taskSettings import PrentryView
from view.taskSettings import UserView
from view.taskSettings_form.detailInfo.detail import DetailTableWidget
from view.taskSettings_form.markerInfo.marker import MarkerTableWidget
from view.taskSettings import ThemeInfoFormView




class taskSettingsController(QWidget):
    def __init__(self, client, cAppUtil):
        super().__init__()
        self.client = client
        self.cAppUtil = cAppUtil
        self.view = taskSettingsView()


        # 每页的样本最大数量
        self.perPageNum = 13
        # 页数
        self.page = 0
        # 样本总数
        self.totalNum = 0

        self.col_label = ['标注主题名', '创建用户', '频率设置', '状态', '操作']
        self.col_label1 = ['标注主题id', '主题名称', '脑电文件信息', '标注任务用户', '任务状态']
        # 要搜选的表
        self.dataSource = []


        # 选择的创建标注主题的任务
        self.select_createUserName = []
        # 选择的标注用户
        self.select_taskUserName = []
        # 用于存取获取筛选框的显示信息
        self.filter_info = []

        # 存储标注主题信息
        self.theme_info = []
        # 存储标注任务信息
        self.task_info = None

        # 当前选择行索引
        self.row = -1

        # 存储添加的标注主题信息
        self.add_ThemeInfo = {}
        self.add_TaskInfo = {}



        # 获取
        self.client.getThemeInfoResSig.connect(self.getThemeInfoRes)
        # 删除
        self.client.delThemeInfoResSig.connect(self.delThemeInfoRes)
        # 添加
        self.client.addThemeInfoResSig.connect(self.addThemeInfoRes)
        self.client.getChooseDetailInfoResSig.connect(self.get_choose_detail_infoRes)
        self.client.addTaskInfoResSig.connect(self.addTaskInfoRes)
        # 修改
        self.client.updateThemeInfoResSig.connect(self.updateThemeInfoRes)
        # 删除标注任务
        self.client.delTaskInfoResSig.connect(self.delTaskInfoRes)
        # 启动标注主题
        self.client.startThemeResSig.connect(self.startThemeRes)
        # 查找标注人员
        self.client.getChooseMarkerInfoResSig.connect(self.get_choose_marker_infoRes)

        self.getThemeInfo('1')
        self.view.add_btn.clicked.connect(self.addThemeInfo)
        self.view.del_btn.clicked.connect(self.delThemeInfo)
        self.view.update_btn.clicked.connect(self.updateThemeInfo)
        self.view.filter_btn.clicked.connect(self.getFilterInfo)
        self.view.btnReSelect.clicked.connect(self.research_theme)
        # self.view.test_btn.clicked.connect(self.chose_marker)

        # update属性代表当前是否在修改状态
        self.update = -1
        self.insert = -1


    # 获取搜索按钮数据
    def getFilterInfo(self):

        key_word = self.view.comboCond.currentText()
        key_value = self.view.lineValue.text()
        if key_word == '主题名':
            key_word = 'theme.name'
        elif key_word == '创建用户':
            key_word = 'user_info.name'
        elif key_word == '主题状态':
            key_word = 'state'
        print("key_word:", key_word)
        print("key_value:", key_value)
        # 只有当搜索框有值时候才搜索
        if key_value:
            self.getThemeInfo(flag='4', key_word=key_word, key_value=key_value)
        else:
            QMessageBox.information(self, "提示", "搜索框内没有填写内容!!", QMessageBox.Yes)


    # 重置
    # 选择病人的重置功能
    def research_theme(self):
        self.view.comboCond.setCurrentIndex(0)
        # self.view.tableWidget_patient.comboCond.setCurrentIndex(0)
        self.view.lineValue.clear()
        # self.view.tableWidget_patient.lineValue.clear()
        self.getThemeInfo(flag='3')

    def on_clicked_lookthemeBtn(self, row):
        self.themeInfoForm = ThemeInfoFormView()

        theme_name = self.theme_info[row][3]
        theme_config = self.theme_info[row][8]
        theme_state = self.theme_info[row][6]
        theme_desc = self.theme_info[row][7]

        # 显示当前主题状态
        self.themeInfoForm .ui.themeStateLabel.setText(theme_state)
        # 设置界面内容

        self.themeInfoForm .ui.themeEdit.setText(theme_name)
        # 获取当前标注主题的配置id的index然后显示当前标注主题配置

        # config_id = int(theme_config.split('-')[0])
        # index = [i for i, config in enumerate(self.config_info) if config[0]==config_id][0]
        temp = theme_config.split('-')
        self.themeInfoForm .ui.comboConfigId.setText(f'采样频率:{temp[1]}Hz | 陷波：{temp[2]}Hz | 低通:{temp[3]}Hz | 高通：{temp[4]}Hz')
        # self.updateThemeForm.ui.comboBoxState.setCurrentText(theme_state)
        self.themeInfoForm .ui.textEdit.setText(theme_desc)


        # self.addThemeForm.initTabel()
        # 设置不关闭对话框就不进行其他操作
        self.themeInfoForm.setWindowModality(Qt.ApplicationModal)
        # 设置关闭对象自动释放资源
        self.themeInfoForm.setAttribute(Qt.WA_DeleteOnClose)

        # self.addThemeForm.ui.btnConfirm.clicked.connect(self.onClick_ButtonToText)
        # self.addThemeForm.ui.btnExit.clicked.connect(self.on_btnCancelAdd_clicked)
        self.themeInfoForm.show()


    # 获取标注主题信息
    def getThemeInfo(self, flag='1', key_word='', key_value='', theme_id = None):
        # 获取标注主题所有信息
        if flag == '1':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum]
            self.client.getThemeInfo(REQmsg)
        # 标注主题没有条件的翻页
        elif flag == '2':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.start]
            self.client.getThemeInfo(REQmsg)
        # 标注主题重置的首页
        elif flag == '3':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum]
            self.client.getThemeInfo(REQmsg)
        # 标注主题有条件的首页
        elif flag == '4':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, key_word, key_value]
            self.client.getThemeInfo(REQmsg)
        # 标注主题有搜索条件的翻页
        elif flag == '5':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.start, key_word, key_value]
            self.client.getThemeInfo(REQmsg)
        # 查询某一主题详细信息
        elif flag == '6':
            account = self.client.tUser[1]
            REQmsg = [account, flag, theme_id]
            self.client.getThemeInfo(REQmsg)
        else:
            pass

    # 处理客户端返回的获取标注主题结果
    def getThemeInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                flag = REPData[3][0]
                # theme_info = REPData[3][1]
                # 获取所有的标注主题信息
                if flag == '1':
                    theme_info = REPData[3][1]
                    self.theme_info = theme_info
                    self.totalNum = REPData[3][2]


                    if self.theme_info:
                        self.view.del_btn.setEnabled(True)
                        self.view.update_btn.setEnabled(True)
                        self.view.tableWidget = TableWidget()
                        self.view.tableWidget.init_ui(col_label=self.col_label, sampleList=self.theme_info, totalNum=self.totalNum,on_clicked_lookthemeBtn=self.on_clicked_lookthemeBtn,on_clicked_lookdetailBtn=self.on_clicked_lookdetailBtn, on_clicked_adddetailBtn=self.on_clicked_adddetailBtn, on_clicked_startTheme=self.on_clicked_startTheme,tuser=self.client.tUser[0])

                        self.view.ui.verticalLayout_3.addWidget(self.view.tableWidget)
                        self.page = math.ceil(self.totalNum / self.perPageNum)
                        self.view.tableWidget.setPageController(self.page)
                        self.view.tableWidget.control_signal.connect(self.page_controller)
                    else:
                        self.view.del_btn.setEnabled(False)
                        self.view.update_btn.setEnabled(False)
                        self.view.tableWidget = TableWidget()
                        self.view.tableWidget.init_ui(col_label=self.col_label, sampleList=self.theme_info, totalNum=self.totalNum,on_clicked_lookthemeBtn=self.on_clicked_lookthemeBtn,on_clicked_lookdetailBtn=self.on_clicked_lookdetailBtn, on_clicked_adddetailBtn=self.on_clicked_adddetailBtn, on_clicked_startTheme=self.on_clicked_startTheme,tuser=self.client.tUser[0])
                        # self.view.tableWidget = TableWidget()
                        self.view.ui.verticalLayout_3.addWidget(self.view.tableWidget)

                # 获取无条件标注主题信息分页
                elif flag == '2':
                    theme_info = REPData[3][1]
                    self.theme_info = theme_info
                    if self.theme_info:
                        self.clear(self.view.tableWidget.verticalLayout_1)
                        # 页码不会改变是因为这里创建时候没有传入当前页码值
                        self.view.tableWidget.init_ui(current_page=self.cur_page, col_label=self.col_label,
                                                            sampleList=self.theme_info, totalNum=self.totalNum,on_clicked_lookthemeBtn=self.on_clicked_lookthemeBtn,
                                                            on_clicked_lookdetailBtn=self.on_clicked_lookdetailBtn,
                                                            on_clicked_adddetailBtn=self.on_clicked_adddetailBtn,
                                                            on_clicked_startTheme=self.on_clicked_startTheme,
                                                            tuser=self.client.tUser[0])


                        # 源代码
                        if self.is_fromSkip:
                            self.view.tableWidget.skipPage.setText(str(self.cur_page))
                        else:
                            self.view.tableWidget.skipPage.setText(str(self.skip_page))

                    else:
                        QMessageBox.information(self, "分页信息查询", '下一页无信息！！', QMessageBox.Yes)

                # 重置
                elif flag == '3':
                    self.clear(self.view.tableWidget.verticalLayout_1)
                    self.view.tableWidget.control_signal.disconnect(self.page_controller)
                    # self.view.tableWidget_patient.control_signal.disconnect(self.patient_page_controller)
                    self.clear(self.view.tableWidget.control_layout)
                    # self.clear(self.view.tableWidget_patient.control_layout)

                    theme_info = REPData[3][1]
                    self.theme_info = theme_info
                    self.totalNum = REPData[3][2]

                    # 表格
                    # self.clear(self.view.ui.verticalLayout_3)
                    self.view.tableWidget.init_ui(col_label=self.col_label, sampleList=self.theme_info,
                                                        totalNum=self.totalNum,on_clicked_lookthemeBtn=self.on_clicked_lookthemeBtn, on_clicked_lookdetailBtn=self.on_clicked_lookdetailBtn, on_clicked_adddetailBtn=self.on_clicked_adddetailBtn, on_clicked_startTheme=self.on_clicked_startTheme,tuser=self.client.tUser[0])

                    # 分页
                    self.page = math.ceil(self.totalNum / self.perPageNum)
                    self.view.tableWidget.setPageController(self.page)
                    self.view.tableWidget.control_signal.connect(self.page_controller)
                    # QMessageBox.information(self, "筛选查询", REPData[2], QMessageBox.Yes)
                # 获取某条件的标注主题信息
                elif flag == '4':
                    self.clear(self.view.tableWidget.verticalLayout_1)
                    # self.clear(self.view.tableWidget_patient.verticalLayout_1)
                    # 清除页面控制器
                    self.view.tableWidget.control_signal.disconnect(self.page_controller)
                    # self.view.tableWidget_patient.control_signal.disconnect(self.patient_page_controller)
                    self.clear(self.view.tableWidget.control_layout)


                    theme_info = REPData[3][1]
                    self.theme_info = theme_info
                    self.totalNum = REPData[3][2]

                    self.view.tableWidget.init_ui(col_label=self.col_label, sampleList=self.theme_info,
                                                        totalNum=self.totalNum,on_clicked_lookthemeBtn=self.on_clicked_lookthemeBtn, on_clicked_lookdetailBtn=self.on_clicked_lookdetailBtn, on_clicked_adddetailBtn=self.on_clicked_adddetailBtn, on_clicked_startTheme=self.on_clicked_startTheme,tuser=self.client.tUser[0])
                    # 页码相关
                    self.page = math.ceil(self.totalNum / self.perPageNum)
                    self.view.tableWidget.setPageController(self.page)
                    self.view.tableWidget.control_signal.connect(self.page_controller)
                # 获取某条件标注主题信息分页
                elif flag == '5':
                    theme_info = REPData[3][1]
                    self.theme_info = theme_info
                    # self.theme_info = theme_info
                    if theme_info:
                        self.clear(self.view.tableWidget.verticalLayout_1)
                        # 页码不会改变是因为这里创建时候没有传入当前页码值
                        # 这里只是改变重新创建当前表格值
                        self.view.tableWidget.init_ui(current_page=self.cur_page, col_label=self.col_label,
                                                            sampleList=self.theme_info, totalNum=self.totalNum,on_clicked_lookthemeBtn=self.on_clicked_lookthemeBtn,
                                                            on_clicked_lookdetailBtn=self.on_clicked_lookdetailBtn,
                                                            on_clicked_adddetailBtn=self.on_clicked_adddetailBtn,
                                                            on_clicked_startTheme=self.on_clicked_startTheme,
                                                            tuser=self.client.tUser[0])

                        # 源代码
                        if self.is_fromSkip:
                            self.view.tableWidget.skipPage.setText(str(self.cur_page))
                        else:
                            self.view.tableWidget.skipPage.setText(str(self.skip_page))
                    else:
                        QMessageBox.information(self, "分页信息查询", '下一页无信息！！', QMessageBox.Yes)



                # 获取某一个标注主题详细信息
                elif flag == '6':
                    theme_id = REPData[3][2]
                    task_info = REPData[3][1]
                    # 标注主题信息
                    if task_info:
                        self.task_info = task_info
                        col_label = ['检查单号', '病人姓名', '脑电文件', '标注用户', '标注状态', '操作']
                        self.view.detailTable = DetailTableWidget()
                        self.view.detailTable.init_ui(col_label=col_label, sampleList=self.task_info,
                                                      totalNum=len(self.task_info),
                                                      on_clicked_deltaskBtn=self.on_clicked_deltaskBtn)
                        # self.detailTable = DetailTableWidget(col_label=col_label, sampleList=task_info,
                        #                                      totalNum=len(task_info),
                        #                                      on_clicked_deltaskBtn=self.on_clicked_deltaskBtn,
                        #                                      theme_id=theme_id)
                        # 设置不关闭对话框就不进行其他操作
                        self.view.detailTable.setWindowModality(Qt.ApplicationModal)
                        # 设置关闭对象自动释放资源
                        self.view.detailTable.setAttribute(Qt.WA_DeleteOnClose)

                        self.view.detailTable.resize(1500, 800)
                        self.view.detailTable.setWindowTitle("标注主题详细任务信息")

                        # 设置对不是该主题创建的用户不能删除对应标注任务的信息
                        # 方法一：设置最后一列不可编辑
                        # row = range(self.detailTable.table.rowCount())
                        # col = [5]
                        # self.disable_tableWidgetItem_row_col(self.detailTable.table, row, col)
                        # 方法二:隐藏最后一列,这一个方法用户更加友好
                        # 如果选中主题不是当前用户创建,或者不是刚创建状态（为启动），就在查看详细信息时候不显示删除列
                        if (self.theme_info[self.row][1] != self.client.tUser[0]) or (self.theme_info[self.row][6] != 'creating'):
                            self.view.detailTable.table.setColumnHidden(5, True)

                        self.view.detailTable.show()
                    else:
                        QMessageBox.information(self, "标注主题详细信息", f"当前标注主题暂无详细的标注任务信息，需要添加!!!!", QMessageBox.Yes)

            else:
                QMessageBox.information(self, "任务设置", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('getThemeInfoRes', e)


    # 添加标注主题功能
    # 添加标注主题
    def addThemeInfo(self):
        self.addThemeForm = AddThemeFormView()

        # 设置不关闭对话框就不进行其他操作
        self.addThemeForm.setWindowModality(Qt.ApplicationModal)
        # 设置关闭对象自动释放资源
        self.addThemeForm.setAttribute(Qt.WA_DeleteOnClose)

        self.addThemeForm.ui.btnConfirm.clicked.connect(self.onClick_ButtonToText)
        self.addThemeForm.ui.btnExit.clicked.connect(self.on_btnCancelAdd_clicked)
        self.addThemeForm.show()

    # 取消添加标注类型信息方法
    def on_btnCancelAdd_clicked(self):
        self.add_ThemeInfo = {}
        # 关闭弹出添加框
        self.addThemeForm.close()

    # 确认添加标注主题类信息方法
    def onClick_ButtonToText(self):
        # :删除频率选择的选项
        self.addThemeForm.close()
        self.add_ThemeInfo['theme_name'] = self.addThemeForm.ui.themeEdit.text()
        # config_index = self.addThemeForm.ui.comboConfigId.currentIndex()
        # 设置为当前频率值
        self.add_ThemeInfo['config_id'] = self.client.tUser[12]
        self.add_ThemeInfo['theme_state'] = self.addThemeForm.ui.themeStateLabel.text()
        # self.add_ThemeInfo['theme_state'] = self.addThemeForm.ui.comboBoxState.currentText()
        self.add_ThemeInfo['theme_description'] = self.addThemeForm.ui.textEdit.toPlainText()
        account = self.client.tUser[1]
        REQmsg = [account, self.client.tUser[0], self.add_ThemeInfo['theme_name'], self.add_ThemeInfo['config_id'], self.add_ThemeInfo['theme_state'],self.add_ThemeInfo['theme_description']]
        print(self.add_ThemeInfo)
        self.client.addThemeInfo(REQmsg)

    # 不知道为啥数据库themeid在删除过后不会按照已有的顺序自增，而是从删除之前开始自增，删除18的数据，自增id为19，不是18
    # 处理客户端返回的添加标注主题结果
    def addThemeInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                # 重新获取标注主题信息，并更新列表
                self.clear(self.view.ui.verticalLayout_3)
                # 清除筛选框布局试一下
                # self.clear(self.view.comBoxLayout)
                # TODO:需要修改，让更新时候自动跳到新增的标注主题信息界面
                self.getThemeInfo('1')
                QMessageBox.information(self, "标注主题", REPData[2], QMessageBox.Yes)
            else:
                QMessageBox.information(self, "标注主题", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('addThemeInfoRes', e)


    # 删除标注主题功能
    # 删除标注主题
    def delThemeInfo(self):
        row = self.view.tableWidget.table.currentRow()
        if (self.theme_info[row][1] == self.client.tUser[0]) and (self.theme_info[row][6] == 'creating'):
            if row == -1:
                QMessageBox.information(self.view, ' ', '请先选中一行')
            else:
                answer = QMessageBox.warning(
                    self.view, '确认删除！', '您将进行删除操作！',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if answer == QMessageBox.Yes:
                    # 暂时只能选中一行删除
                    print('row', row)
                    theme_id = self.theme_info[row][0]
                    account = self.client.tUser[1]
                    REQmsg = [account, theme_id, row]
                    self.client.delThemeInfo(REQmsg)

                else:
                    return
        else:
            if row == -1:
                QMessageBox.information(self.view, ' ', '请先选中一行')
            elif self.theme_info[row][1] != self.client.tUser[0]:
                QMessageBox.information(self.view, '提示', '你不是当前主题创建者，无法进行当前主题删除功能！！！')
            elif self.theme_info[row][6] != 'creating':
                QMessageBox.information(self.view, '提示', f'当前主题处于{self.theme_info[row][6]}状态，不支持删除！！！')
            else:
                pass


    # 处理客户端返回的删除标注主题结果
    def delThemeInfoRes(self, REPData):
        try:
            if REPData[0] == '1':

                self.clear(self.view.ui.verticalLayout_3)
                # 清除筛选框布局试一下
                # self.clear(self.view.comBoxLayout)
                # 重新获取是因为筛选框也要同步更改
                self.getThemeInfo('1')
                QMessageBox.information(self, "成功", "删除成功")
                return
            else:
                QMessageBox.information(self, "提示", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('delThemeInfoRes', e)


    # 更新标注主题功能
    # 更新标注主题
    def updateThemeInfo(self):
        row = self.view.tableWidget.table.currentRow()
        if (self.theme_info[row][1] == self.client.tUser[0]) and (self.theme_info[row][6] == 'creating'):
            if row == -1:
                QMessageBox.information(self.view, ' ', '请先选中一行')
                return
                # 暂时只能选中一行删除
            else:
                print('row', row)
                theme_name = self.theme_info[row][3]
                theme_config = self.theme_info[row][5]
                theme_state = self.theme_info[row][6]
                theme_desc = self.theme_info[row][7]

                self.updateThemeForm = AddThemeFormView()
                # 设置不关闭对话框就不进行其他操作
                self.updateThemeForm.setWindowModality(Qt.ApplicationModal)
                # 设置关闭对象自动释放资源
                self.updateThemeForm.setAttribute(Qt.WA_DeleteOnClose)
                # self.updateThemeForm.initTabel()
                # 显示当前主题状态
                self.updateThemeForm.ui.themeStateLabel.setText(theme_state)
                # 设置界面内容
                self.updateThemeForm.ui.themeEdit.setText(theme_name)
                # 获取当前标注主题的配置id的index然后显示当前标注主题配置

                # config_id = int(theme_config.split('-')[0])
                # index = [i for i, config in enumerate(self.config_info) if config[0]==config_id][0]
                self.updateThemeForm.ui.comboConfigId.setText(str(theme_config))
                # self.updateThemeForm.ui.comboBoxState.setCurrentText(theme_state)
                self.updateThemeForm.ui.textEdit.setText(theme_desc)
                self.updateThemeForm.show()
                # 保存theme_id信息，所以这里需要存为成员变量，因为row这里是局部变量
                self.update_ThemeInfo = {}
                self.update_ThemeInfo['theme_id'] = self.theme_info[row][0]

                self.updateThemeForm.ui.btnConfirm.clicked.connect(self.on_UpdateConfim)
                self.updateThemeForm.ui.btnExit.clicked.connect(self.on_UpdateCancle)
        else:
            if row == -1:
                QMessageBox.information(self.view, ' ', '请先选中一行')
            elif self.theme_info[row][1] != self.client.tUser[0]:
                QMessageBox.information(self.view, '提示', '你不是当前标注主题的创建者不能进行当前标注主题编辑功能！！！')
            elif self.theme_info[row][6] != 'creating':
                QMessageBox.information(self.view, '提示', f'你当前标注主题状态为{self.theme_info[row][6]},不支持编辑！！！')

    # 确认更新
    def on_UpdateConfim(self):
        self.updateThemeForm.close()
        self.update_ThemeInfo['theme_name'] = self.updateThemeForm.ui.themeEdit.text()
        # 不能修改配置
        # config_index = self.updateThemeForm.ui.comboConfigId.currentIndex()
        # self.update_ThemeInfo['config_id'] = self.config_info[config_index][0]
        # self.update_ThemeInfo['theme_state'] = self.updateThemeForm.ui.themeStateLabel.text()
        # self.update_ThemeInfo['theme_state'] = self.updateThemeForm.ui.comboBoxState.currentText()
        self.update_ThemeInfo['theme_description'] = self.updateThemeForm.ui.textEdit.toPlainText()
        # TODO:可以添加判断看看是否更改，如果没有更改就不用更新
        account = self.client.tUser[1]
        REQmsg = [account, self.client.tUser[0], self.update_ThemeInfo['theme_name'],
                   self.update_ThemeInfo['theme_description'], self.update_ThemeInfo['theme_id']]
        print(self.update_ThemeInfo)
        self.client.updateThemeInfo(REQmsg)

    # 取消更新
    def on_UpdateCancle(self):
        self.updateThemeForm.close()

    # 处理客户端返回的更新标注主题结果
    def updateThemeInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.clear(self.view.ui.verticalLayout_3)
                # 清除筛选框布局试一下
                # self.clear(self.view.comBoxLayout)
                # 重新获取是因为筛选框也要同步更改
                self.getThemeInfo('1')
                QMessageBox.information(self, "成功", "更新标注主题信息")
                return
            else:
                QMessageBox.information(self, "编辑提示", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('updateThemeInfoRes', e)


    # 更新标注任务功能
    # 更新标注任务
    def updateTaskInfo(self):
        pass

    # 处理客户端返回的更新标注任务结果
    def updateTaskInfoRes(self, REPData):
        pass


    # 查看标注主题详细信息模块
    # 显示当前标注主题详细信息
    def on_clicked_lookdetailBtn(self, row):
        self.row = row
        print("on_clicked_lookdetailBtn", row)
        # print("hahah")
        self.getThemeInfo('6', theme_id=self.theme_info[row][0])

    # 查看详细信息的删除
    def on_clicked_deltaskBtn(self, row):
        # print("on_clicked_deltaskBtn:row:", row)
        # print("on_clicked_deltaskBtn:theme_id:", theme_id)
        # print("现在开始删除")
        # print("task_info",self.task_info)
        answer = QMessageBox.information(self, '提示', '是否删除该标注任务', QMessageBox.Yes | QMessageBox.No)
        # answer = QMessageBox.information(
        #     self.view, '确认删除！', '您将进行删除操作！',
        #     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        # row = self.view.tableWidget.currentRow()
        if answer == QMessageBox.Yes:
            msg = self.task_info[row][:4]
            print("当前删除的信息：",msg)
            account = self.client.tUser[1]
            REQmsg = [account, msg, row]
            self.client.delTaskInfo(REQmsg)
        else:
            return
        #删除并未实际删除数据库内容，显示删除成功，但是有时候是真的删除成功，有时候是假的（需要连reslab表一起删除）

    # 处理客户端返回的删除标注任务结果
    def delTaskInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                row = REPData[4]
                # theme_id = REPData[]
                if len(self.task_info) == 1:
                    self.task_info = []
                    self.view.detailTable.close()
                    QMessageBox.information(self, "删除提示", "当前标注主题已经无标注任务可删除！！！", QMessageBox.Yes)
                else:
                    self.task_info.pop(row)
                    self.clear(self.view.detailTable.tableLayout)
                    # self.clear(self.view.detailTable.tableLayout)
                    col_label = ['检查单号', '病人姓名', '脑电文件', '标注用户', '标注状态', '操作']
                    self.view.detailTable.init_ui(col_label=col_label, sampleList=self.task_info,
                                             totalNum=len(self.task_info),
                                             on_clicked_deltaskBtn=self.on_clicked_deltaskBtn,
                                             )
                # self.detailTable.table.removeRow(row)
                # QMessageBox.information(self, "成功", "删除标注任务信息成功！！！")
            else:
                QMessageBox.information(self, "删除提示", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('delTaskInfoRes', e)


    # 启动任务功能
    # 点击某任务的启动任务按钮
    def on_clicked_startTheme(self, row):
        print("点击启动任务按钮生效!!!")
        print("on_clicked_startTheme:", row)
        if self.theme_info[row][6] == 'creating':
            reply = QMessageBox.information(self, "提示", f"是否确定将当前标注主题名为{self.theme_info[row][3]}的标注主题启动！！！",
                                    QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                theme_id = self.theme_info[row][0]
                account = self.client.tUser[1]
                REQmsg = [account, theme_id, row]
                self.client.startTheme(REQmsg)
        else:
            QMessageBox.information(self, "提示", f"当前标注主题已经是启动状态,不用再启动！！！",
                                    QMessageBox.Yes)

    # 设置某一标注主题启动返回
    def startThemeRes(self, REPData):
        try:
            if REPData[0] == '1':
                # 重新获取标注主题信息，并更新列表
                self.clear(self.view.ui.verticalLayout_3)
                # 清除筛选框布局试一下
                # self.clear(self.view.comBoxLayout)
                # TODO:需要修改，让更新时候自动跳到新增的标注主题信息界面
                self.getThemeInfo('1')

            else:
                # self.task_info = None
                QMessageBox.information(self, "启动标注主题失败", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print(' startThemeRes', e)



    # 添加标注任务功能
    # 添加标注任务
    def on_clicked_adddetailBtn(self, row):
        # self.addDetailInfo(row)
        # theme_id = self.theme_info[row][0]

        if (self.theme_info[row][1] == self.client.tUser[0]) and (self.theme_info[row][6] == 'creating'):
            print("on_clicked_adddetailBtn", row)
            # 用来保存后面选择的theme_id
            self.select_theme_id = None
            self.choose_theme_id = self.theme_info[row][0]
            self.choose_config_id = self.theme_info[row][2]

            self.get_choose_detail_info(flag='1')
        else:
            if self.theme_info[row][1] != self.client.tUser[0]:
                QMessageBox.information(self.view, '提示', '你不是当前标注主题的创建者不能进行当前标注主题添加详细信任务功能！！！')
            elif self.theme_info[row][6] != 'creating':
                QMessageBox.information(self.view, '提示', f'你当前标注主题状态为{self.theme_info[row][6]},不支持添加详细任务！！！')



    # 添加标注任务详细信息
    def get_choose_detail_info(self, flag='1', key_word='', key_value=''):
        # 获取医生所有信息
        if flag == '1':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.choose_theme_id, self.choose_config_id]
            self.client.getChooseDetailInfo(REQmsg)
        # 医生信息没有条件的翻页
        elif flag == '2':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.patient_start, self.choose_theme_id, self.choose_config_id]
            self.client.getChooseDetailInfo(REQmsg)
        # 医生信息重置的首页
        elif flag == '3':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.choose_theme_id, self.choose_config_id]
            self.client.getChooseDetailInfo(REQmsg)
        # 医生信息有条件的首页
        elif flag == '4':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, key_word, key_value, self.choose_theme_id, self.choose_config_id]
            self.client.getChooseDetailInfo(REQmsg)
        # 医生信息有搜索条件的翻页
        elif flag == '5':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.patient_start, key_word, key_value, self.choose_theme_id, self.choose_config_id]
            self.client.getChooseDetailInfo(REQmsg)
        else:
            pass



    def get_choose_detail_infoRes(self, REPData):
        try:
            if REPData[0] == '1':
                flag = REPData[3][0]
                if flag == '1':

                    patient_info = REPData[3][1]
                    self.patient_info = patient_info
                    self.patient_totalNum = REPData[3][2]
                    file_info = REPData[3][3]
                    self.file_info = self.change_fileDict(file_info)
                    theme_id = REPData[3][4]

                    col_label_detail = ['检查单号', '病人姓名', '检测日期', '上传脑电医生', '操作']
                    # 初始化除了表格以外其他框架
                    self.view.tableWidget_patient = PatientTableWidget()
                    # 初始化选择框
                    self.view.tableWidget_patient.comboCond.addItems(['姓名'])

                    self.view.tableWidget_patient.resize(1500, 800)
                    self.view.tableWidget_patient.setWindowTitle("病人检查单相关信息")
                    # 初始化表格信息
                    self.view.tableWidget_patient.init_ui(col_label=col_label_detail,
                                                         sampleList=self.patient_info,
                                                         totalNum=self.patient_totalNum,
                                                         on_clicked_selectBtn=self.on_clicked_choosefileBtn, theme_id=theme_id)
                    # 返回
                    # self.view.tableWidget_patient.returnBtn.triggered.connect(self.doctorReturnBtnTrigger)
                    # 搜索
                    self.view.tableWidget_patient.btnSelect.clicked.connect(self.search_patient)
                    # 重置
                    self.view.tableWidget_patient.btnReSelect.clicked.connect(self.research_patient)
                    # 页码相关
                    self.patient_page = math.ceil(self.patient_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_patient.setPageController(self.patient_page)
                    self.view.tableWidget_patient.control_signal.connect(self.patient_page_controller)

                    # 设置不关闭对话框就不进行其他操作
                    self.view.tableWidget_patient.setWindowModality(Qt.ApplicationModal)
                    # 设置关闭对象自动释放资源
                    self.view.tableWidget_patient.setAttribute(Qt.WA_DeleteOnClose)

                    self.view.tableWidget_patient.show()
                elif flag == '2':
                    patient_info = REPData[3][1]
                    self.patient_info = patient_info
                    theme_id = REPData[3][2]
                    # self.theme_info = theme_info
                    if self.patient_info:
                        self.clear(self.view.tableWidget_patient.verticalLayout_1)
                        col_label_detail = ['检查单号', '病人姓名', '检测日期', '上传脑电医生', '操作']
                        # 页码不会改变是因为这里创建时候没有传入当前页码值
                        # 这里只是改变重新创建当前表格值
                        self.view.tableWidget_patient.init_ui(current_page=self.patient_cur_page,
                                                             col_label=col_label_detail,
                                                             sampleList=self.patient_info,
                                                             totalNum=self.patient_totalNum,
                                                             on_clicked_selectBtn=self.on_clicked_choosefileBtn, theme_id=theme_id)

                        # 源代码
                        if self.patient_is_fromSkip:
                            self.view.tableWidget_patient.skipPage.setText(str(self.patient_cur_page))
                        else:
                            self.view.tableWidget_patient.skipPage.setText(str(self.patient_skip_page))
                    else:
                        QMessageBox.information(self, "分页信息查询", '下一页无信息！！', QMessageBox.Yes)
                elif flag == '3':
                    # 清除表格内容
                    self.clear(self.view.tableWidget_patient.verticalLayout_1)
                    # 清除页面控制器
                    self.view.tableWidget_patient.control_signal.disconnect(self.patient_page_controller)
                    self.clear(self.view.tableWidget_patient.control_layout)

                    patient_info = REPData[3][1]
                    self.patient_info = patient_info
                    self.patient_totalNum = REPData[3][2]
                    file_info = REPData[3][3]
                    self.file_info = self.change_fileDict(file_info)
                    theme_id = REPData[3][4]
                    col_label_detail = ['检查单号', '病人姓名', '检测日期', '上传脑电医生', '操作']
                    self.view.tableWidget_patient.init_ui(col_label=col_label_detail,
                                                         sampleList=patient_info,
                                                         totalNum=self.patient_totalNum,
                                                         on_clicked_selectBtn=self.on_clicked_choosefileBtn, theme_id=theme_id)
                    # 页码相关
                    self.patient_page = math.ceil(self.patient_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_patient.setPageController(self.patient_page)
                    self.view.tableWidget_patient.control_signal.connect(self.patient_page_controller)

                # 点击搜索按钮
                elif flag == '4':
                    # 清除表格内容
                    self.clear(self.view.tableWidget_patient.verticalLayout_1)
                    # 清除页面控制器
                    self.view.tableWidget_patient.control_signal.disconnect(self.patient_page_controller)
                    self.clear(self.view.tableWidget_patient.control_layout)

                    patient_info = REPData[3][1]
                    self.patient_info = patient_info
                    self.patient_totalNum = REPData[3][2]
                    file_info = REPData[3][3]
                    self.file_info = self.change_fileDict(file_info)
                    theme_id = REPData[3][4]

                    # patient_info = REPData[3][1]
                    # self.patient_info = patient_info
                    # self.patient_totalNum = REPData[3][2]
                    col_label_detail = ['检查单号', '病人姓名', '检测日期', '上传脑电医生', '操作']
                    self.view.tableWidget_patient.init_ui(col_label=col_label_detail,
                                                         sampleList=self.patient_info,
                                                         totalNum=self.patient_totalNum,
                                                         on_clicked_selectBtn=self.on_clicked_choosefileBtn, theme_id=theme_id)
                    # 页码相关
                    self.patient_page = math.ceil(self.patient_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_patient.setPageController(self.patient_page)
                    self.view.tableWidget_patient.control_signal.connect(self.patient_page_controller)
                elif flag == '5':
                    patient_info = REPData[3][1]
                    self.patient_info = patient_info
                    theme_id = REPData[3][2]

                    if self.patient_info:
                        self.clear(self.view.tableWidget_patient.verticalLayout_1)
                        col_label_detail = ['检查单号', '病人姓名', '检测日期', '上传脑电医生', '操作']
                        # 页码不会改变是因为这里创建时候没有传入当前页码值
                        # 这里只是改变重新创建当前表格值
                        self.view.tableWidget_patient.init_ui(current_page=self.patient_cur_page,
                                                             col_label=col_label_detail,
                                                             sampleList=patient_info, totalNum=self.patient_totalNum,
                                                             on_clicked_selectBtn=self.on_clicked_choosefileBtn, theme_id=theme_id)

                        # 源代码
                        if self.patient_is_fromSkip:
                            self.view.tableWidget_patient.skipPage.setText(str(self.patient_cur_page))
                        else:
                            self.view.tableWidget_patient.skipPage.setText(str(self.patient_skip_page))
                    else:
                        QMessageBox.information(self, "分页信息查询", '下一页无信息！！', QMessageBox.Yes)

                else:
                    pass
        except Exception as e:
            print('get_choose_doctor_infoRes', e)

    # 选择医生的搜索功能首页界面
    def search_patient(self):
        key_word = self.view.tableWidget_patient.comboCond.currentText()
        key_value = self.view.tableWidget_patient.lineValue.text()
        if key_word == '姓名':
            key_word = 'name'
        # elif key_word == '电话':
        #     key_word = 'phone'
        # elif key_word == '邮箱':
        #     key_word = 'email'
        print("key_word:", key_word)
        print("key_value:", key_value)
        # 只有当搜索框有值时候才搜索
        if key_value:
            self.get_choose_detail_info(flag='4', key_word=key_word, key_value=key_value)
        else:
            QMessageBox.information(self, "提示", "搜索框内没有填写内容!!", QMessageBox.Yes)

    # 选择医生的重置功能
    def research_patient(self):
        self.view.tableWidget_patient.comboCond.setCurrentIndex(0)
        self.view.tableWidget_patient.lineValue.clear()
        self.get_choose_detail_info(flag='3')

    # 病人选择信息界面相关跳转
    def patient_page_controller(self, signal):
        total_page = self.view.tableWidget_patient.showTotalPage()
        is_fromSkip = False
        if "home" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                return
            self.view.tableWidget_patient.curPage.setText("1")
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            self.view.tableWidget_patient.curPage.setText(str(int(signal[1]) - 1))
        elif "next" == signal[0]:
            if total_page == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.view.tableWidget_patient.curPage.setText(str(int(signal[1]) + 1))
        elif "final" == signal[0]:
            self.view.tableWidget_patient.curPage.setText(str(total_page))
        elif "confirm" == signal[0]:
            if total_page < int(signal[1]) or int(signal[1]) < 1:
                QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                self.view.tableWidget_patient.skipPage.setText('1')
                return
            is_fromSkip = True
            self.view.tableWidget_patient.curPage.setText(signal[1])
        self.changeTableContent_patient(is_fromSkip)  # 改变表格内容

    def changeTableContent_patient(self, is_fromSkip):
        """根据当前页改变表格的内容"""
        self.patient_is_fromSkip = is_fromSkip
        self.patient_cur_page = int(self.view.tableWidget_patient.curPage.text())
        self.patient_skip_page = int(self.view.tableWidget_patient.skipPage.text())
        self.patient_start = (self.patient_cur_page - 1) * self.perPageNum
        # theme_id = self.theme_detailID
        # row = self.row_detail

        key_word = self.view.tableWidget_patient.comboCond.currentText()
        key_value = self.view.tableWidget_patient.lineValue.text()
        if key_word == '姓名':
            key_word = 'name'
        # elif key_word == '电话':
        #     key_word = 'phone'
        # elif key_word == '邮箱':
        #     key_word = 'email'
        print("key_word:", key_word)
        print("key_value:", key_value)
        # 只有当搜索框有值时候才搜索
        if key_value:
            # 有搜索条件的翻页
            self.get_choose_detail_info(flag='5', key_word=key_word, key_value=key_value)
        else:
            # 无搜索条件的翻页
            self.get_choose_detail_info(flag='2')

    # 文件选择
    def on_clicked_choosefileBtn(self, row, theme_id):
        self.view.tableWidget_patient.hide()
        print("下面打印关于文件选择的信息")
        print("on_clicked_choosefileBtn", row)
        print("theme_id", theme_id)

        # 多选框展示
        check_id = self.patient_info[row][0]

        self.pre_info = self.file_info[check_id]

        # 保存最后选中的文件的[[check_id, file_id]]信息
        self.file_id = []

        self.select_file_row = []

        print(self.pre_info)
        col_num = 2
        self.prentryView = PrentryView()

        # 设置不关闭对话框就不进行其他操作
        self.prentryView.setWindowModality(Qt.ApplicationModal)
        # 设置关闭对象自动释放资源
        self.prentryView.setAttribute(Qt.WA_DeleteOnClose)
        self.prentryView.resize(600, 800)
        self.prentryView.setAttribute(Qt.WA_DeleteOnClose)
        self.prentryView.setWindowTitle("脑电数据文件")
        self.prentryView.setWindowModality(Qt.ApplicationModal)
        # self.prentryView.show()
        self.prentryView.ui.btnConfirm.setEnabled(True)
        self.prentryView.ui.btnReturn.setEnabled(True)
        self.prentryView.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.prentryView.ui.tableWidget.resizeRowsToContents()
        self.prentryView.ui.tableWidget.resizeColumnsToContents()
        self.prentryView.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.prentryView.ui.tableWidget.clicked.connect(self.on_tableWidget_itemClicked)
        self.prentryView.ui.btnConfirm.clicked.connect(partial(self.on_btnConfirm_clicked, theme_id))
        self.prentryView.ui.btnReturn.clicked.connect(self.on_btnReturn_clicked)

        self.prentryView.ui.tableWidget.setColumnCount(col_num)
        itemName = ['可选框', '病例脑电文件列表']
        row_num = len(self.pre_info)
        if row_num <= 0:
            itemName = ['病例脑电文件列表[无相关文件]']
        for i in range(0, col_num):
            header_item = QTableWidgetItem(itemName[i])
            # font = header_item.font()
            # font.setPointSize(12)
            # header_item.setFont(font)
            # header_item.setForeground(QBrush(Qt.black))
            self.prentryView.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
        self.prentryView.ui.tableWidget.setColumnWidth(0, 70)
        # self.prentryView.ui.tableWidget.setColumnWidth(1, 20)
        # self.prentryView.ui.tableWidget.resizeColumnToContents(1)
        self.prentryView.ui.tableWidget.horizontalHeader().setHighlightSections(False)
        self.prentryView.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.prentryView.ui.tableWidget.horizontalHeader().setStyleSheet(
            '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
        # self.prentryView.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.prentryView.ui.tableWidget.setRowCount(row_num)
        for r in range(row_num):
            for i in range(1, col_num):
                fn = '{:>03}.bdf'.format(self.pre_info[r][1])
                item = QTableWidgetItem(fn)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                font.setPointSize(12)
                item.setFont(font)
                self.prentryView.ui.tableWidget.setItem(r, 1, item)
            self.add_checkBox(r)
            self.prentryView.ui.tableWidget.setRowHeight(r, 50)
        self.prentryView.ui.tableWidget.verticalHeader().setVisible(False)
        self.prentryView.show()

    def add_checkBox(self, row):
        exec('self.item_checked_{} = QCheckBox()'.format(row))
        exec('self.item_checked_{}.setCheckState(QtCore.Qt.Unchecked)'.format(row))
        exec('self.item_checked_{}.setCheckable(True)'.format(row))
        exec("self.item_checked_{}.setStyleSheet('''margin:10px''')".format(row))
        exec("self.item_checked_{}.clicked.connect(partial(self.rowSelected,{}))".format(row, row))
        exec("self.prentryView.ui.tableWidget.setCellWidget({}, 0, self.item_checked_{})".format(row, row))

    def rowSelected(self, row):
        tag = eval("self.item_checked_{}.isChecked()".format(row))
        # print(tag)
        if tag:
            self.select_file_row.append(row)
            self.select_file_row.sort()
        else:
            if row in self.select_file_row:
                self.select_file_row.remove(row)

    def on_btnConfirm_clicked(self, theme_id):
        try:
            if self.select_file_row == []:
                QMessageBox.information(self, '提示', '未选择文件', QMessageBox.Yes | QMessageBox.No)
                return
            reply = QMessageBox.information(self, '提示', '是否选择添加当前文件', QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                self.prentryView.hide()

                # 保存选择的theme_id的信息
                self.select_theme_id = theme_id
                # 展示标注人员信息
                self.chose_marker()

        except Exception as e:
            print("on_btnConfirm_clicked", e)

    # 选择文件返回上一级
    def on_btnReturn_clicked(self):
        self.prentryView.hide()
        self.view.tableWidget_patient.show()


    # 处理客户端返回的添加标注任务结果
    def addTaskInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                QMessageBox.information(self, "标注主题", REPData[2], QMessageBox.Yes)
            else:
                QMessageBox.information(self, "标注主题", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('addTaskInfoRes', e)


    # 选择标注人员信息
    # 标注人员显示信息框
    def chose_marker(self):
        self.get_choose_marker_info(flag='1')

    # 获取标注人员信息
    def get_choose_marker_info(self, flag='1', key_word='', key_value=''):
        # 获取病人所有信息
        if flag == '1':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum]
            self.client.getChooseMarkerInfo(REQmsg)
        # 病人信息没有条件的翻页
        elif flag == '2':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.marker_start]
            self.client.getChooseMarkerInfo(REQmsg)
        # 病人信息重置的首页
        elif flag == '3':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum]
            self.client.getChooseMarkerInfo(REQmsg)
        # 病人信息有条件的首页
        elif flag == '4':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, key_word, key_value]
            self.client.getChooseMarkerInfo(REQmsg)
        # 病人信息有搜索条件的翻页
        elif flag == '5':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.marker_start, key_word, key_value]
            self.client.getChooseMarkerInfo(REQmsg)
        else:
            pass

    # 获取标注人员信息返回的结果
    def get_choose_marker_infoRes(self, REPData):
        try:
            if REPData[0] == '1':
                flag = REPData[3][0]
                # 标注人员信息没有条件的首页
                if flag == '1':
                    marker_info = REPData[3][1]
                    self.marker_info = marker_info
                    self.marker_totalNum = REPData[3][2]
                    col_label_detail = ['姓名', '电话', '邮箱', '操作']
                    # detail_info = [('235353', '林一', 897), ('00000', '王二', 888)]
                    # totalNumDetail = 2

                    # 初始化除了表格以外其他框架
                    self.view.tableWidget_marker = MarkerTableWidget()
                    # 初始化选择框
                    self.view.tableWidget_marker.comboCond.addItems(['姓名', '电话', '邮箱'])

                    self.view.tableWidget_marker.resize(1500, 800)
                    self.view.tableWidget_marker.setWindowTitle("标注人员相关信息")
                    # 初始化表格信息
                    self.view.tableWidget_marker.init_ui(col_label=col_label_detail,
                                                          sampleList=self.marker_info,
                                                          totalNum=self.marker_totalNum,
                                                          on_clicked_selectBtn=self.marker_on_clicked_selectBtn)
                    # 返回
                    # self.view.tableWidget_patient.returnBtn.triggered.connect(self.patientReturnBtnTrigger)
                    # 搜索
                    self.view.tableWidget_marker.btnSelect.clicked.connect(self.search_marker)
                    # 重置
                    self.view.tableWidget_marker.btnReSelect.clicked.connect(self.research_marker)
                    # 确认这些标注人员
                    self.view.tableWidget_marker.btnConfirm.clicked.connect(self.marker_on_clicked_selectConfirm)
                    # 返回上级
                    self.view.tableWidget_marker.btnReturn.clicked.connect(self.marker_on_clicked_selectReturn)
                    # 页码相关
                    self.marker_page = math.ceil(self.marker_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_marker.setPageController(self.marker_page)
                    self.view.tableWidget_marker.control_signal.connect(self.marker_page_controller)


                    # 被选中的标注人员信息
                    self.select_marker_info = []
                    # 被选中的标注人员的id
                    self.select_marker_index = []
                    # 初始化选中的表格信息
                    self.view.tableWidget_marker.init_selectedTable(col_label=col_label_detail, sampleList=self.select_marker_info,
                                                                    on_clicked_deleteBtn=self.marker_on_clicked_deleteBtn)

                    # 设置不关闭对话框就不进行其他操作
                    self.view.tableWidget_marker.setWindowModality(Qt.ApplicationModal)
                    # 设置关闭对象自动释放资源
                    self.view.tableWidget_marker.setAttribute(Qt.WA_DeleteOnClose)

                    self.view.tableWidget_marker.show()
                # 标注人员信息没有条件的翻页
                elif flag == '2':
                    marker_info = REPData[3][1]
                    self.marker_info = marker_info
                    # self.theme_info = theme_info
                    if self.marker_info:
                        self.clear(self.view.tableWidget_marker.verticalLayout_1)
                        col_label_detail = ['姓名', '电话', '邮箱', '操作']
                        # 页码不会改变是因为这里创建时候没有传入当前页码值
                        # 这里只是改变重新创建当前表格值
                        self.view.tableWidget_marker.init_ui(current_page=self.marker_cur_page,
                                                              col_label=col_label_detail,
                                                              sampleList=self.marker_info,
                                                              totalNum=self.marker_totalNum,
                                                              on_clicked_selectBtn=self.marker_on_clicked_selectBtn)

                        # 源代码
                        if self.marker_is_fromSkip:
                            self.view.tableWidget_marker.skipPage.setText(str(self.marker_cur_page))
                        else:
                            self.view.tableWidget_marker.skipPage.setText(str(self.marker_skip_page))
                    else:
                        QMessageBox.information(self, "分页信息查询", '下一页无信息！！', QMessageBox.Yes)
                # 标注人员信息重置的首页
                elif flag == '3':
                    # 清除表格内容
                    self.clear(self.view.tableWidget_marker.verticalLayout_1)
                    # 清除页面控制器
                    self.view.tableWidget_marker.control_signal.disconnect(self.marker_page_controller)
                    self.clear(self.view.tableWidget_marker.control_layout)
                    marker_info = REPData[3][1]
                    self.marker_info = marker_info
                    self.marker_totalNum = REPData[3][2]
                    col_label_detail = ['姓名', '电话', '邮箱', '操作']
                    self.view.tableWidget_marker.init_ui(col_label=col_label_detail,
                                                          sampleList=self.marker_info,
                                                          totalNum=self.marker_totalNum,
                                                          on_clicked_selectBtn=self.marker_on_clicked_selectBtn)
                    # 页码相关
                    self.marker_page = math.ceil(self.marker_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_marker.setPageController(self.marker_page)
                    self.view.tableWidget_marker.control_signal.connect(self.marker_page_controller)
                # 标注人员信息有条件的首页
                elif flag == '4':
                    # 清除表格内容
                    self.clear(self.view.tableWidget_marker.verticalLayout_1)
                    # 清除页面控制器
                    self.view.tableWidget_marker.control_signal.disconnect(self.marker_page_controller)
                    self.clear(self.view.tableWidget_marker.control_layout)
                    marker_info = REPData[3][1]
                    self.marker_info = marker_info
                    self.marker_totalNum = REPData[3][2]
                    col_label_detail = ['姓名', '电话', '邮箱', '操作']
                    self.view.tableWidget_marker.init_ui(col_label=col_label_detail,
                                                          sampleList=self.marker_info,
                                                          totalNum=self.marker_totalNum,
                                                          on_clicked_selectBtn=self.marker_on_clicked_selectBtn)
                    # 页码相关
                    self.marker_page = math.ceil(self.marker_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_marker.setPageController(self.marker_page)
                    self.view.tableWidget_marker.control_signal.connect(self.marker_page_controller)
                # 标注人员信息有搜索条件的翻页
                elif flag == '5':
                    marker_info = REPData[3][1]
                    self.marker_info = marker_info
                    # self.theme_info = theme_info
                    if marker_info:
                        self.clear(self.view.tableWidget_marker.verticalLayout_1)
                        col_label_detail = ['姓名', '电话', '邮箱', '操作']
                        # 页码不会改变是因为这里创建时候没有传入当前页码值
                        # 这里只是改变重新创建当前表格值
                        self.view.tableWidget_marker.init_ui(current_page=self. marker_cur_page,
                                                              col_label=col_label_detail,
                                                              sampleList= marker_info, totalNum=self.marker_totalNum,
                                                              on_clicked_selectBtn=self.marker_on_clicked_selectBtn)

                        # 源代码
                        if self.marker_is_fromSkip:
                            self.view.tableWidget_marker.skipPage.setText(str(self.marker_cur_page))
                        else:
                            self.view.tableWidget_marker.skipPage.setText(str(self.marker_skip_page))
                    else:
                        QMessageBox.information(self, "分页信息查询", '下一页无信息！！', QMessageBox.Yes)

                else:
                    pass
        except Exception as e:
            print('get_choose_marker_infoRes', e)

    # 选中某个具体的标注人员时候
    def marker_on_clicked_selectBtn(self, row):
        print('选择具体标注人员信息，当前选中的行为：', row)
        print('选中人员的id为：', self.marker_info[row][0])
        id = self.marker_info[row][0]
        print('选中人员的信息为：', self.marker_info[row])
        info= self.marker_info[row]
        if id in self.select_marker_index:
            QMessageBox.information(self, "提示", f'{self.marker_info[row][1]}已经添加到标注人员内，不用重复添加！！', QMessageBox.Yes)
        else:
            self.select_marker_index.append(id)
            self.select_marker_info.append(info)
            # 清除原来信息
            self.clear(self.view.tableWidget_marker.selectVInfo)
            col_label_detail = ['姓名', '电话', '邮箱', '操作']
            # 更新已经选择的标注人员的列表信息
            self.view.tableWidget_marker.init_selectedTable(col_label=col_label_detail,
                                                            sampleList=self.select_marker_info,
                                                            on_clicked_deleteBtn=self.marker_on_clicked_deleteBtn)


    # 选中删除的时候
    def marker_on_clicked_deleteBtn(self, row):
        print('删除某个标注人员信息当前选中的行为：', row)
        print('选中要删除人员的id为：', self.select_marker_info[row][0])
        print('选中要删除人员的姓名为：', self.select_marker_info[row][1])
        self.select_marker_index.pop(row)
        self.select_marker_info.pop(row)
        # 清除原来信息
        self.clear(self.view.tableWidget_marker.selectVInfo)
        col_label_detail = ['姓名', '电话', '邮箱', '操作']
        # 更新已经选择的标注人员的列表信息
        self.view.tableWidget_marker.init_selectedTable(col_label=col_label_detail,
                                                        sampleList=self.select_marker_info,
                                                        on_clicked_deleteBtn=self.marker_on_clicked_deleteBtn)


    # 确认添加这些标注人员时候
    def marker_on_clicked_selectConfirm(self):
        try:
            # if not self.is_edit_file:
            # for i in self.select_user_row:
            #     self.user_id.append(self.user_info[i][0])
            # self.select_file_row = list(set(self.select_file_row))
            # 解决前面的文件选择信息返回会出现重复的情况
            for i in self.select_file_row:
                self.file_id.append([self.pre_info[i][0], self.pre_info[i][1]])
            reply = QMessageBox.information(self, '提示', '是否选择添加当前标注用户', QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                self.view.tableWidget_marker.hide()
                self.view.tableWidget_marker.close()
                self.view.tableWidget_patient.close()
                self.prentryView.close()
                # 文件信息保存在self.file_id，用户信息保存在self.user_id
                # 下面进行运算将两个列表连在一起
                print("这里显示选中的文件信息：", self.file_id)
                print("用户信息：",  self.select_marker_index)
                task_info = self.chage_fileUser(self.file_id,  self.select_marker_index)
                print("task_info:", task_info)
                # theme_id = self.theme_info[self.row][0]
                account = self.client.tUser[1]
                REQmsg = [account, self.select_theme_id, task_info]
                self.client.addTaskInfo(REQmsg)

        except Exception as e:
            print('marker_on_clicked_selectConfirm', e)

    # 取消添加这些标注人员时候
    def marker_on_clicked_selectReturn(self):
        # TODO:20240504返回
        self.view.tableWidget_marker.hide()
        # 解决出现重复情况
        # self.select_file_row = []
        self.prentryView.show()
        # return

    # 选择病人的搜索功能首页界面
    def search_marker(self):
        key_word = self.view.tableWidget_marker.comboCond.currentText()
        key_value = self.view.tableWidget_marker.lineValue.text()
        if key_word == '姓名':
            key_word = 'name'
        elif key_word == '电话':
            key_word = 'phone'
        elif key_word == '邮箱':
            key_word = 'email'
        print("key_word:", key_word)
        print("key_value:", key_value)
        # 只有当搜索框有值时候才搜索
        if key_value:
            self.get_choose_marker_info(flag='4', key_word=key_word, key_value=key_value)
        else:
            QMessageBox.information(self, "提示", "搜索框内没有填写内容!!", QMessageBox.Yes)

    # 选择病人的重置功能
    def research_marker(self):
        self.view.tableWidget_marker.comboCond.setCurrentIndex(0)
        self.view.tableWidget_marker.lineValue.clear()
        self.get_choose_marker_info(flag='3')

    # 病人选择信息界面相关跳转
    def marker_page_controller(self, signal):
        total_page = self.view.tableWidget_marker.showTotalPage()
        is_fromSkip = False
        if "home" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                return
            self.view.tableWidget_marker.curPage.setText("1")
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            self.view.tableWidget_marker.curPage.setText(str(int(signal[1]) - 1))
        elif "next" == signal[0]:
            if total_page == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.view.tableWidget_marker.curPage.setText(str(int(signal[1]) + 1))
        elif "final" == signal[0]:
            self.view.tableWidget_marker.curPage.setText(str(total_page))
        elif "confirm" == signal[0]:
            if total_page < int(signal[1]) or int(signal[1]) < 1:
                QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                self.view.tableWidget_marker.skipPage.setText('1')
                return
            is_fromSkip = True
            self.view.tableWidget_marker.curPage.setText(signal[1])
        self.changeTableContent_marker(is_fromSkip)  # 改变表格内容

    def changeTableContent_marker(self, is_fromSkip):
        """根据当前页改变表格的内容"""
        self.marker_is_fromSkip = is_fromSkip
        self.marker_cur_page = int(self.view.tableWidget_marker.curPage.text())
        self.marker_skip_page = int(self.view.tableWidget_marker.skipPage.text())
        self.marker_start = (self.marker_cur_page - 1) * self.perPageNum
        # theme_id = self.theme_detailID
        # row = self.row_detail

        key_word = self.view.tableWidget_marker.comboCond.currentText()
        key_value = self.view.tableWidget_marker.lineValue.text()
        if key_word == '姓名':
            key_word = 'name'
        elif key_word == '电话':
            key_word = 'phone'
        elif key_word == '邮箱':
            key_word = 'email'
        print("key_word:", key_word)
        print("key_value:", key_value)
        # 只有当搜索框有值时候才搜索
        if key_value:
            # 有搜索条件的翻页
            self.get_choose_marker_info(flag='5', key_word=key_word, key_value=key_value)
        else:
            # 无搜索条件的翻页
            self.get_choose_marker_info(flag='2')

    # 获取标注主题相关分页
    # 设置分页
    def page_controller(self, signal):
        total_page = self.view.tableWidget.showTotalPage()
        is_fromSkip = False
        if "home" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                return
            self.view.tableWidget.curPage.setText("1")
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            self.view.tableWidget.curPage.setText(str(int(signal[1]) - 1))
        elif "next" == signal[0]:
            if total_page == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.view.tableWidget.curPage.setText(str(int(signal[1]) + 1))
        elif "final" == signal[0]:
            self.view.tableWidget.curPage.setText(str(total_page))
        elif "confirm" == signal[0]:
            if total_page < int(signal[1]) or int(signal[1]) < 1:
                QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                self.view.tableWidget.skipPage.setText('1')
                return
            is_fromSkip = True
            self.view.tableWidget.curPage.setText(signal[1])
        self.changeTableContent(is_fromSkip)  # 改变表格内容

        # # 改变表格内容并检查结果
        # if not self.changeTableContent(is_fromSkip):
        #     # 如果没有数据，将页码恢复为之前的值
        #     self.view.tableWidget.curPage.setText(str(previous_page))

    def changeTableContent(self, is_fromSkip):
        """根据当前页改变表格的内容"""
        self.is_fromSkip = is_fromSkip
        self.cur_page = int(self.view.tableWidget.curPage.text())
        self.skip_page = int(self.view.tableWidget.skipPage.text())
        self.start = (self.cur_page - 1) * self.perPageNum
        print('cur_page', self.cur_page)
        print('skip_page', self.skip_page)


        key_word = self.view.comboCond.currentText()
        key_value = self.view.lineValue.text()
        if key_word == '主题名':
            key_word = 'theme.name'
        elif key_word == '创建用户':
            key_word = 'user_info.name'
        elif key_word == '主题状态':
            key_word = 'state'
        print("key_word:", key_word)
        print("key_value:", key_value)

        # 只有当搜索框有值时候才搜索
        if key_value:
            # 有搜索条件的翻页
            self.getThemeInfo(flag='5', key_word=key_word, key_value=key_value)
        else:
            # 无搜索条件的翻页
            self.getThemeInfo(flag='2')

        # # 如果没有数据，恢复页码并返回 False
        # if not has_data:
        #     return False
        # return True

    # 清理布局
    def clear(self, layout, num=0, count=-1):
        item_list = list(range(layout.count()))
        item_list.reverse()
        # print(item_list)
        j = 0
        for i in item_list:
            if num == 0 and count == -1:
                item = layout.itemAt(i)
                layout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
            elif num != 0 and count == -1:
                item = layout.itemAt(i)
                layout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
                j += 1
                if j == num:
                    return
            elif num == 0 and count != -1:
                if j == count:
                    item = layout.itemAt(i)
                    layout.removeItem(item)
                    if item.widget():
                        item.widget().deleteLater()
                    return
                j += 1

    # 检查编辑/增加 数据格式
    def check_item_pattern(self, data):
        if data['type_name'] == '':
            raise Exception('请输入类型名：不能为空！')
        if data['category'] not in self.view.category:
            raise Exception('请正确输入类别：正常波形/异常波形/伪迹波形/正常状态/异常状态/伪迹状态！')


    # 添加详细信息中返回的file_info信息转换为以check_id为键的字典信息
    def change_fileDict(self,data):
        file_info = {}
        for i in data:
            file = i[1].split(",")
            file_info[i[0]] = [(i[0], int(j)) for j in file]
        return file_info

    # 将选择的文件信息和用户信息组合，返回需要添加的信息
    def chage_fileUser(self, file_info, user_info):
        task_info = []
        for i in file_info:
            for j in user_info:
                task_info.append(i + [j] + ['notStarted'])
        return task_info

    # 禁用disable_row行disable_col列的表格项，disable_col和disable_row都为[]，如[1,2]
    def disable_tableWidgetItem_row_col(self, table, disable_row, disable_col):
        for r in disable_row:
            for c in disable_col:
                item = table.item(r, c)
                if item == None:
                    cellWidget = table.cellWidget(r, c)
                    if cellWidget == None:
                        return
                    else:
                        cellWidget.setEnabled(False)
                else:
                    item.setFlags(item.flags() & (~Qt.ItemIsEnabled))

    def exit(self):
        # 如果这个退出方法里面写了没有使用的信号，没有绑定的信号，切换用户的时候会出错
        self.client.getThemeInfoResSig.disconnect()
        self.client.addThemeInfoResSig.disconnect()
        self.client.delThemeInfoResSig.disconnect()
        self.client.updateThemeInfoResSig.disconnect()
        # self.client.getTaskInfoResSig.disconnect()
        self.client.addTaskInfoResSig.disconnect()
        self.client.delTaskInfoResSig.disconnect()
        # self.client.updateTaskInfoResSig.disconnect()
        self.client.getChooseDetailInfoResSig.disconnect()
        self.client.startThemeResSig.disconnect()
        self.client.getChooseMarkerInfoResSig.disconnect()


