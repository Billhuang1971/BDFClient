from view.classifier import ClassifierView, ImportView, AlgorithmSelectView, LabelSelectVew,TableWidget,PrentryView,SetSelectView
from view.classifer_form.question.question import Question
from util.clientAppUtil import clientAppUtil

import json
import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

import os
import shutil
import numpy as np
import hashlib
from view.progressBarView import ProgressBarView

class classifierController(QWidget):
    is_reload_controller = QtCore.pyqtSignal(str)

    def __init__(self, client, cAppUtil):
        super().__init__()
        self.view = ClassifierView()
        self.client = client
        self.cAppUtil = cAppUtil
        self.model_path=cAppUtil.model_path
        self.file_model = None
        self.algorithm = None
        self.set=None
        self.curPageIndex_al = 1  #
        self.curPageMax_al = 1  #
        self.curPageIndex_set=1
        self.curPageMax_set=1
        #self.progressDialog = None
        self.ProgressBarView = None# 进度条对象
        self.data_blocks=[]
        self.is_search = False #标记是否处于搜索状态
        self.tableWidget = None #存储表格
        self.curPageIndex = 1  #当前页
        self.pageRows = 12  # 每页12个
        self.curPageMax = 1  #当前最大页数
        self.select_row = None #被选中的行
        self.alg_is_search=False #算法选择界面是否属于搜索状态
        self.set_is_search = False#数据集选择界面是否属于搜索状态
        self.root_path = os.path.join(os.path.dirname(__file__))[:-10]
        self.view.ui.btn_import.clicked.connect(self.on_btn_import_clicked)
        self.view.ui.btnDel.clicked.connect(self.on_btnDel_clicked)
        self.view.ui.btnSelect.clicked.connect(lambda :self.on_clicked_select_classifier(pageIndex=1))
        # 只能选中一行
        #self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        #self.tableWidget.resizeRowsToContents()
        #self.tableWidget.resizeColumnsToContents()
        #self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.view.ui.tableWidget.customContextMenuRequested.connect(self.menu_select)

        # 不支持双击修改
        # self.view.ui.tableWidget.cellDoubleClicked.connect(self.on_tableWidget_cellDoubleClicked)

        # update属性代表当前是否在修改状态
        self.update = -1
        self.insert = -1
        self.classifier_alg_set_name = None
        self.search_classifier_page_info=None
        self.tempt_CurPageIndex=None
        self.algorithm_set=None #存放服务器传回的算法信息
        self.dataSet=None #存放服务器传回的数据集信息
        self.search_alg_page_info=None
        self.search_set_page_info=None
        self.tempt_alg_CurpageIndex=None
        self.tempt_set_CurpageIndex = None
        #self.current_clicked=False
        self._clicked_connections = {}  # 存储已有的连接
        self.configID=None
        self.EEG_lead=['AF3','FP1','FPz','FP2','AF4',
                        'F7','F5','F3','F1','FZ','F2','F4','F6','F8',
                        'FT7','FC5','FC3','FC1','FCZ','FC2','FC4','FC6','FT8',
                        'T7/T3','C5','C3','C1','CZ','C2','C4','C6','T8/T4',
                        'M1','TP7','CP5','CP3','CP1','CPZ','CP2','CP4','CP6','TP8','M2',
                        'A1','P7/T5','P5','P3','P1','PZ','P2','P4','P6','P8/T6','A2',
                        'PO7','PO5','PO3','POZ','PO4','PO6','PO8',
                        'CB1','O1','OZ','O2','CB2']
        # header表格头 field数据库表属性
        self.header = ['分类器模型名称', '算法名称', '数据集名称', '训练性能', '测试性能']
        self.client.getClassifierAlgSetName([self.curPageIndex, self.pageRows])
        self.field = ['classifier_name', 'alg_name', 'set_name', 'train_performance', 'test_performance']
        self.client.getClassifierAlgSetNameResSig.connect(self.getClassifierAlgSetNameRes)
        self.client.inquiryClassifierInfoResSig.connect(self.inquiryClassifierInfoRes)
        self.client.delClassifierInfoResSig.connect(self.delClassifierInfoRes)
        self.client.getSelectAlgorithmInfoResSig.connect(self.getSelectAlgorithmInfoRes)
        self.client.checkClassifierInfoRessig.connect(self.checkClassifierInfoRes)
        self.client.add_import_classifierInfoRessig.connect(self.add_import_classifierInfoRes)
        self.client.checkstateRessig.connect(self.checkstateRes)
        self.client.model_transmit_messageRessig.connect(self.model_transmit_messageRes)
        self.client.classifier_id_inquiryRessig.connect(self.classifier_id_inquiryRes)
        self.client.classifierPagingResSig.connect(self.classifierPagingRes)
        self.client.classifierPaging_alResSig.connect(self.classifierPaging_alRes)
        self.client.inquiryCls_alg_InfoRessig.connect(self.inquiryCls_alg_InfoRes)
        self.client.getClassifier_configRessig.connect(self.getClassifier_configRes)
        self.client.getSelectSetInfoResSig.connect(self.getSelectSetInfoRes)
        self.client.inquiryCls_set_InfoResSig.connect(self.inquiryCls_set_InfoRes)
        self.client.classifierPaging_setResSig.connect(self.classifierPaging_setRes)


        # self.client.checkNegAlgResSig.connect(self.checkNegAlgRes)
        # self.init_table(self.classifier_alg_set_name)
        # self.init_comboCond()

    def getClassifierAlgSetNameRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.clear_layout(self.view.ui.verticalLayout_2)
                self.classifier_alg_set_name = REPData[2]
                self.curPageMax=REPData[3]
                self.tableWidget = TableWidget(self.classifier_alg_set_name,self.curPageIndex)
                self.view.ui.verticalLayout_2.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
                self.tableWidget.table.itemClicked.connect(self.set_selectRow)
                self.view.ui.verticalLayout.setStretch(0, 1)
                self.view.ui.verticalLayout.setStretch(1, 9)
                #self.view.initTable(self.classifier_alg_set_name)
                self.init_comboCond()
            else:
                if REPData[2]==0:
                    QMessageBox.information(self, '提示', '无模型信息', QMessageBox.Ok)
                else:
                    QMessageBox.information(self, '提示', '获取模型信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('getClassifierAlgSetNameRes', e)
    def page_controller(self, signal): #页码控制
        if "home" == signal[0]:
            if self.curPageIndex == 1:
                QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                return
            self.curPageIndex = 1
            self.tableWidget.curPage.setText(str(self.curPageIndex))
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            if self.curPageIndex <= 1:
                return
            self.curPageIndex = self.curPageIndex - 1
            self.tableWidget.curPage.setText(str(self.curPageIndex))
        elif "next" == signal[0]:
            if self.curPageMax == int(signal[1]) or self.search_classifier_page_info == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.curPageIndex = self.curPageIndex + 1
            self.tableWidget.curPage.setText(str(self.curPageIndex))
        elif "final" == signal[0]:
            if self.curPageIndex == self.curPageMax or self.search_classifier_page_info == self.curPageIndex:
                QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                return
            self.curPageIndex = self.curPageMax
            self.tableWidget.curPage.setText(str(self.curPageMax))
        elif "confirm" == signal[0]:
            if signal[1]=='':
                QMessageBox.information(self, "提示", "请输入数字", QMessageBox.Yes)
                return
            if self.curPageIndex == int(signal[1]):
                QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                return
            if self.curPageMax < int(signal[1]) or int(signal[1]) <= 0:
                QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                return
            if self.view.ui.lineValue.text() != '' and self.view.ui.btnSelect.text() == "取消查询":
                if self.search_classifier_page_info < int(signal[1]) or int(signal[1]) <= 0:
                    QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                    return
            self.curPageIndex = int(signal[1])
            self.tableWidget.curPage.setText(signal[1])

        msg = [self.curPageIndex, self.pageRows, signal[0]]
        if self.view.ui.lineValue.text() != '' and self.view.ui.btnSelect.text() == "取消查询":
            self.is_search=True
            self.on_clicked_select_classifier(pageIndex=self.curPageIndex)
        else:
            self.client.classifierPaging(msg)
    def classifierPagingRes(self,REPData): #页码控制返回
        try:
            self.classifier_alg_set_name = REPData[2]
            self.clear_layout(self.view.ui.verticalLayout_2)
            self.tableWidget = TableWidget(self.classifier_alg_set_name, self.curPageIndex)
            self.view.ui.verticalLayout_2.addWidget(self.tableWidget)
            self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
            self.tableWidget.control_signal.connect(self.page_controller)
            self.tableWidget.table.itemClicked.connect(self.set_selectRow)

        except Exception as e:
            print('userPagingRes', e)
    def clear_layout(self, layout, num=0, count=-1):#清理布局
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
    def init_comboCond(self):
        self.view.ui.comboCond.clear()
        # for field in fields:
        for i in range(len(self.field)):
            self.view.ui.comboCond.addItem(self.header[i], self.field[i])

    # def on_tableWidget_cellDoubleClicked(self, row, col):#无用
    #     self.view.ui.tableWidget.repaint()
    #     # 当无其他行正在编辑时设置除当前单元格外其他单元格不可编辑
    #     if self.update == -1 or self.insert == -1:
    #         self.disable_tableWidgetItem(row)
    #
    #     col = self.view.ui.tableWidget.columnCount()
    #     # 如果还未显示按钮,增加一列显示
    #     if col == self.col:
    #         self.update = row
    #         # 增加一列按钮
    #         self.view.ui.tableWidget.insertColumn(self.col)
    #         header_item = QTableWidgetItem('修改')
    #         font = header_item.font()
    #         font.setPointSize(16)
    #         header_item.setFont(font)
    #         header_item.setForeground(QBrush(Qt.black))  # 前景色，即文字颜色
    #         self.view.ui.tableWidget.setHorizontalHeaderItem(self.col, header_item)
    #         self.question = Question()
    #         self.question.ui.btnOK.clicked.connect(
    #             lambda: self.on_btnConfirmUpdate_clicked(row))
    #         # self.controller.on_btnOKUpdate_clicked)
    #         self.question.ui.btnCancel.clicked.connect(
    #             lambda: self.on_btnCancelUpdate_clicked(row))
    #         self.view.ui.tableWidget.setCellWidget(row, self.col, self.question)

    # 查询只能查出等于的情况，不支持其他大于小于之类的查询
    def on_clicked_select_classifier(self,pageIndex):
        try:
            if self.tempt_CurPageIndex == None:
                self.tempt_CurPageIndex = self.curPageIndex
            self.curPageIndex=pageIndex
            key_word = self.view.ui.comboCond.currentText()
            key_value = self.view.ui.lineValue.text()
            if key_value == '':
                QMessageBox.information(self, '提示', '请输入要搜索的模型信息', QMessageBox.Ok)
                return
            if key_word == '分类器模型名称':
                key_word = 'classifier_name'
            elif key_word == '算法名称':
                key_word = 'alg_name'
            elif key_word == '数据集名称':
                key_word = 'set_name'
            elif key_word == '训练性能':
                key_word = 'train_performance'
            elif key_word == '测试性能':
                key_word = 'test_performance'
            REQmsg = [key_word, key_value,pageIndex,self.pageRows]
            if self.view.ui.btnSelect.text() == "查询":
                self.view.ui.btnSelect.setText("取消查询")
                self.client.inquiryClassifierInfo(REQmsg)
            elif self.is_search==True:
                self.is_search=False
                self.client.inquiryClassifierInfo(REQmsg)
            elif self.view.ui.btnSelect.text() == "取消查询":
                self.clear_layout(self.view.ui.verticalLayout_2)
                self.curPageIndex=self.tempt_CurPageIndex
                self.tableWidget = TableWidget(self.classifier_alg_set_name, self.curPageIndex)
                self.view.ui.verticalLayout_2.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
                self.tableWidget.table.itemClicked.connect(self.set_selectRow)
                self.view.ui.btnSelect.setText("查询")
                self.search_classifier_page_info=None
                self.tempt_CurPageIndex=None
                self.view.ui.lineValue.clear()
        except Exception as e:
            print('on_clicked_select_classifier', e)

    def inquiryClassifierInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                QMessageBox.information(self, '提示', '查询模型信息成功', QMessageBox.Ok)
                self.search_classifier_info = REPData[2][1]
                self.search_classifier_page_info =REPData[2][0]
                self.clear_layout(self.view.ui.verticalLayout_2)
                self.tableWidget = TableWidget(self.search_classifier_info, self.curPageIndex)
                self.view.ui.verticalLayout_2.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.search_classifier_page_info)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
                self.tableWidget.table.itemClicked.connect(self.set_selectRow)
                # self.init_comboCond()
            else:
                QMessageBox.information(self, '提示', '查询模型信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('inquiryClassifierInfoRes', e)
    def on_btn_import_clicked(self):
        self.import_view = ImportView()
        self.import_view.show()
        # 只能输入数字
        # 创建 QIntValidator 类的实例对象，并设置限制范围
        validator = QIntValidator()
        validator.setRange(0, 9999)
        # 将 QIntValidator 对象设置为 QLineEdit 控件的验证器
        #self.import_view.ui.lineEdit_sample_rate.setValidator(validator)
        self.import_view.ui.lineEdit_epoch_length_name.setValidator(validator)
        self.import_view.ui.pushButton_model_select.clicked.connect(self.on_clicked_pushButton_model_select)
        self.import_view.ui.pushButton_save.clicked.connect(self.onClicked_pushButton_save)
        self.import_view.ui.pushButton_algorithm_select.clicked.connect(self.on_clicked_pushButton_algorithm_select)
        self.import_view.ui.pushButton_set_select.clicked.connect(self.on_clicked_pushButton_set_select)
        self.import_view.ui.pushButton_label_select.clicked.connect(self.on_clicked_pushButton_label_select)
        self.import_view.ui.pushButton_configOptions_select.clicked.connect(self.on_clicked_configOptions_select)
        self.import_view.ui.checkbox1.stateChanged.connect(self.clear_path)
        self.import_view.ui.checkbox2.stateChanged.connect(self.clear_path)

    # 分类任务按钮点击响应函数
    def on_clicked_pushButton_label_select(self):
        self.labelSelectView = LabelSelectVew(self.EEG_lead,
                                              self.import_view.saved_EEG_names)
        self.labelSelectView.signal_save_label_names.connect(self.respondFunction_signal_save_label_names)
        self.labelSelectView.show()
    def respondFunction_signal_save_label_names(self, label_names):
        self.import_view.saved_EEG_names = label_names
        content_label=''
        count=0
        for item in label_names:
            count+=1
            if count <=6:
                content_label += item + '/'
        content_label+=f'……共{count}个'
        self.import_view.ui.label_label_select.setText(str(content_label))
    def clear_path(self):
        self.import_view.saved_EEG_names=[]
        self.import_view.ui.label_label_select.setText(str('通道列表：无'))


    # 模型选择按钮点击响应函数
    def on_clicked_pushButton_model_select(self):
        try:
            self.file_model = None
            model = QFileDialog.getOpenFileName(self, "选择模型文件", self.root_path)
            # 用户成功选择算法文件
            if model[0]:
                self.file_model = model
                f_name = self.file_model[0].split('/')[-1]
                _translate = QtCore.QCoreApplication.translate
                self.import_view.ui.label_model_path.setText(_translate("model_import",
                                                                        "<html><head/><body><p><span style=\" font-size:12pt;\">模型文件：" + f_name + "</span></p></body></html>"))
        except Exception as e:
            print('on_clicked_pushButton_model_select', e)

    def onClicked_pushButton_save(self):#点击保存 （开始上传①）
         model_name = self.import_view.ui.lineEdit_model_name.text()
         if os.listdir(self.model_path):  # 步骤七
             QMessageBox.information(self.import_view, '提示', '系统正在处理未完成的上传任务，完成后请重新上传任务',
                                     QMessageBox.Yes)
             # 存在未完成任务，进入分支①处理
             self.step_seven()
         else:
             if not model_name:
                 QMessageBox.information(self.import_view, '提示', '请输入模型名称', QMessageBox.Yes)
                 return
             self.client.checkClassifierInfo(['filename',model_name])#检查是否已存在该模型

    def checkClassifierInfoRes(self,REPData): #检查模型同名返回，若无同名则继续（开始上传②）
            model_name = self.import_view.ui.lineEdit_model_name.text()
            epoch_len = self.import_view.ui.lineEdit_epoch_length_name.text()
            configID=self.configID
            #sample_rate = self.import_view.ui.lineEdit_sample_rate.text()
            channel_info = self.import_view.ui.lineEdit_channel_info.text()
            if not self.algorithm:
                QMessageBox.information(self.import_view, '提示', '尚未选择模型的算法', QMessageBox.Yes)
                return
            if not model_name:
                QMessageBox.information(self.import_view, '提示', '请输入模型名称', QMessageBox.Yes)
                return
            if REPData[0] =='1' and REPData[2]:#若模型名称无重复
                QMessageBox.information(self.import_view, '提示', '当前模型名称已存在，请更改', QMessageBox.Yes)
                return
            if not self.file_model:
                QMessageBox.information(self.import_view, '提示', '当前尚未选择模型文件', QMessageBox.Yes)
                return
            if not epoch_len:
                QMessageBox.information(self.import_view, '提示', '请输入扫描段长', QMessageBox.Yes)
                return
            if not configID:
                QMessageBox.information(self.import_view, '提示', '请选择配置信息', QMessageBox.Yes)
                return
            if not self.set:
                QMessageBox.information(self.import_view, '提示', '尚未选择模型的数据集', QMessageBox.Yes)
                return
            model_file_type = self.file_model[0].split('/')[-1].split('.')[-1]
            #shutil.copyfile(self.file_model[0],
                            #self.model_path + model_name + '.' + model_file_type)  # 把上传文件复制到文件夹中
            try:
                label_names = ''
                first = True
                for label_name in self.import_view.saved_EEG_names:
                    if first:
                        label_names += "{}".format(str(label_name))
                        first = False
                    else:
                        label_names += "|{}".format(str(label_name))
                model_hash_right=self.check_file_hash(self.file_model[0])
                self.configID=None
                content_label='' #所选的状态通道
                for item in self.import_view.saved_EEG_names:
                    content_label += item + '/'
                #（开启上传③）
                self.client.add_import_classifierInfo([model_name, self.algorithm[0],self.set[0],
                                                      model_name + '.' + model_file_type,
                                                      epoch_len,model_hash_right,configID,content_label])#向服务器数据库添加信息(hash值存在第四个)
             # self.DbUtil.update_alg_relate_model_info(filename=model_name + '.' + model_file_type,
             #                                          alg_id=self.algorithm[0])
            except Exception as result:
                QMessageBox.information(self.import_view, '提示', "失败原因: %s" % result, QMessageBox.Yes)
                return

    def add_import_classifierInfoRes(self,REPData):#REPData[3]='classifier_name,alg_id,filename, epoch_length'
        try: #（上传③返回）
            if REPData[0] == '1':
                QMessageBox.information(self.import_view, '提示', "导入成功", QMessageBox.Yes)
                self.set=None
                self.algorithm=None
                self.import_view.close()
                #（开始上传④）
                self.client.checkstate([REPData[2]])#步骤2
        except Exception as e:
            QMessageBox.information(self.import_view, '提示', "失败原因: %s" % e, QMessageBox.Yes)
            self.import_view.close()
            print('add_import_classifierInfoRes', e)

    #上传④返回
    def checkstateRes(self,REPData):#REPData['1', REQmsg[1],classifier_info]
        if REPData[0] =='1' and REPData[2]:#模型存在且state=ready
            shutil.copyfile(self.file_model[0],
                            self.model_path + REPData[2][0][4])  # 把上传文件复制到文件夹中
            #self.client.getClassifierAlgSetName([self.client.tUser[0]])
            #开始传输①
            self.client.model_transmit_message(['start',REPData[2][0][0],REPData[2][0][4],0])#start, classifier_id, filename, block_id,本机mac地址
        else:
            QMessageBox.information(self, '提示', '记录不存在或该记录state不为“ready”', QMessageBox.Ok)

    def model_transmit_messageRes(self,REPData): #传输①返回
        if REPData[2][0]=='waiting': #6.1
            if len(self.data_blocks)==0:
                trans_path = self.model_path + REPData[2][2][2]
                file_model = open(trans_path, "rb")
                block_size = 5*1024*1024
                file_content = file_model.read()
                self.data_blocks = [file_content[i:i + block_size] for i in range(0, len(file_content), block_size)]
                file_model.close()
            if REPData[2][1]==1:#判断block_id=1
                file_path=self.model_path+'uploading.txt'
                with open(file_path, "w") as file_txt:
                    selected_index=[1,2,4]
                    for index in selected_index:
                        file_txt.write(str(REPData[2][2][index])+ " ") #REP=start, classifier_id, filename, block_id,本机mac地址
                totalDataSize = len(self.data_blocks)  # 总块数
                self.ProgressBarView = ProgressBarView(window_title="模型文件传输中", hasStopBtn=False,maximum=totalDataSize)
                self.ProgressBarView.show()
                #self.progressDialog = QProgressDialog("传输中……", "Cancel", 0, 100)
                #self.progressDialog.setWindowModality(Qt.ApplicationModal)
                #self.progressDialog.show()
                # 开始传输数据
                self.client.model_transmit_message(['uploading',REPData[2][2][1],REPData[2][2][2],REPData[2][1],
                                                    self.data_blocks[(REPData[2][1]-1)]]) #“uploading，classifier_id,filename，block_id，数据块,mac”
                #第一组数据即0，故-1
            elif REPData[2][1]> len(self.data_blocks):#判断block_id>blockN
                # 传输完成后关闭进度
                self.ProgressBarView.close()
                #self.progressDialog.cancel()
                #file_model.close()
                self.client.model_transmit_message(['uploaded',REPData[2][2][1],REPData[2][2][2],REPData[2][2][3]])#“uploaded,classifier_id,filename,block_id和本机mac地址”
            elif REPData[2][1] > 1 :
                totalDataSize = len(self.data_blocks)
                # 更新进度条
                if self.ProgressBarView==None:
                    self.ProgressBarView = ProgressBarView(window_title="模型文件传输中", hasStopBtn=False,maximum=totalDataSize)
                    self.PogressBarView.show()
                tempt_value=REPData[2][1]-1
                self.ProgressBarView.updateProgressBar(tempt_value)
                #self.progressDialog.setValue(int((tempt_value / totalDataSize)*100))
                self.client.model_transmit_message(['uploading', REPData[2][2][1], REPData[2][2][2], REPData[2][1],
                                                    self.data_blocks[(REPData[2][1] - 1)]])
        elif REPData[2][0] == 'uploaded':#6.3
            #self.progressDialog.cancel()
            self.ProgressBarView.close()
            files = os.listdir(self.model_path)
            for file in files:
                file_path1 = os.path.join(self.model_path, file)
                if os.path.isfile(file_path1):
                    os.remove(file_path1)
                elif os.path.isdir(file_path1):
                    shutil.rmtree(file_path1)
            #self.trans_app.exec_()
            self.data_blocks = []
            QMessageBox.information(self, '提示', '上传已完成,请到尾页查看', QMessageBox.Ok)
            self.client.getClassifierAlgSetName([self.curPageIndex, self.pageRows])
        elif REPData[2][0] in ['wrongSite','unknownError','clean','wrongServer']: #6.2
            files = os.listdir(self.model_path)
            for file in files:
                file_path1 = os.path.join(self.model_path, file)
                if os.path.isfile(file_path1):
                    os.remove(file_path1)
                elif os.path.isdir(file_path1):
                    shutil.rmtree(file_path1)
            QMessageBox.information(self, '提示', '出现错误，传输失败', QMessageBox.Ok)
            #self.progressDialog.cancel()
            self.ProgressBarView.close()
        elif REPData[2][0] == 'recover':  # 6.4
            file_path2 = os.path.join(self.model_path, "uploading.txt")
            if os.path.exists(file_path2):
                os.remove(file_path2)
            with open(file_path2, 'w') as file_txt:
                selected_index = [1, 2, 4]
                for index in selected_index:
                    file_txt.write(str(REPData[2][index])+ " ")
            self.ProgressBarView.updateProgressBar(0)
            #self.progressDialog.setValue(0)
            self.client.model_transmit_message(['continue', REPData[2][1],REPData[2][2]])

    def step_seven(self):#分支① 存在未完成的上传任务
        suffix = 'txt'
        file_names = [f for f in os.listdir(self.model_path) if not f.endswith(suffix)]
        self.client.classifier_id_inquiry(file_names) #进入分支①第二步


    def classifier_id_inquiryRes(self,REPData):#步骤七（分支①第二步返回）
        if REPData[2]: #数据库存在该模型信息
            model_hash=self.check_file_hash(self.model_path+REPData[2][0][4])
            if model_hash != REPData[2][0][9] :#7.1
                files = os.listdir(self.model_path)
                for file in files:
                    file_path1 = os.path.join(self.model_path, file)
                    if os.path.isfile(file_path1):
                        os.remove(file_path1)
                    elif os.path.isdir(file_path1):
                        shutil.rmtree(file_path1)
                self.client.delClassifierInfo([[REPData[2][0][1]],0,0])#0表示不进行文件删除，中间的0为冗余
                QMessageBox.information(self, '提示', '本地文件filename出错，上传过程需重新开始',
                                        QMessageBox.Ok)
            else:
                    try:
                        # 尝试打开文件并读取内容
                        with open(self.model_path+'uploading.txt', 'r') as file:
                            content = file.read()
                    except FileNotFoundError:#7.2
                        QMessageBox.information(self, '提示', '上传过程出错，系统将从出错位置开始继续上传',
                                                QMessageBox.Ok)
                        #self.progressDialog = QProgressDialog("传输中....",
                                                             # "Cancel",0,100)
                        #self.progressDialog.setValue(0)
                        #print(f"uploading.txt文件不存在")
                        self.client.model_transmit_message(['unknown', REPData[2][0][0], REPData[2][0][4]])
                        return
                    except IOError:
                        QMessageBox.information(self, '提示', '上传过程出错，系统将从出错位置开始继续上传',
                                                QMessageBox.Ok)
                        #self.progressDialog = QProgressDialog("传输中....",
                                                             # "Cancel", 0, 100)
                        #self.progressDialog.setValue(0)
                        self.client.model_transmit_message(['clean', REPData[2][0][0], REPData[2][0][4]])#7.3
                        #print(f"文件损坏")
                        return
                    if not content:
                        QMessageBox.information(self, '提示', '上传过程出错，系统将从出错位置开始继续上传',
                                                QMessageBox.Ok)
                        #self.progressDialog = QProgressDialog("传输中....",
                                                             # "Cancel", 0, 100)
                        #self.progressDialog.setValue(0)
                        self.client.model_transmit_message(['clean', REPData[2][0][0], REPData[2][0][4]])  # 7.3
                       # print(f"文件损坏")
                    else:#7.4
                        QMessageBox.information(self, '提示', '上传过程出错，系统将从出错位置开始继续上传',
                                                QMessageBox.Ok)
                        #self.progressDialog = QProgressDialog("传输中....",
                                                              #"Cancel", 0, 100)
                        #self.progressDialog.setValue(0)
                        self.client.model_transmit_message(['continue', REPData[2][0][0], REPData[2][0][4]])
                        #print(f"文件未损坏。")

        else:#模型信息不存在
            files = os.listdir(self.model_path)
            for file in files:
                file_path1 = os.path.join(self.model_path, file)
                if os.path.isfile(file_path1):
                    os.remove(file_path1)
                elif os.path.isdir(file_path1):
                    shutil.rmtree(file_path1)
            QMessageBox.information(self, '提示', '服务器无此模型信息，上传过程需重新开始',
                                    QMessageBox.Ok)

    def on_clicked_pushButton_algorithm_select(self):
        if self.import_view.ui.checkbox1.isChecked() or self.import_view.ui.checkbox2.isChecked():
            self.search_alg_page_info = None
            self.import_view.ui.pushButton_algorithm_select.setEnabled(False)
            self.algorithmSelectView = AlgorithmSelectView(self.curPageIndex_al)
            self.algorithmSelectView.ui.tableWidget_algorithm.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.algorithmSelectView.ui.btnSelect1.clicked.connect(
                lambda: self.on_clicked_select_algorithm(pageIndex=1))
            if self.import_view.ui.checkbox1.isChecked():
                self.client.getSelectAlgorithmInfo([self.curPageIndex_al, self.pageRows,'state'])
            else:
                self.client.getSelectAlgorithmInfo([self.curPageIndex_al, self.pageRows,'waveform'])
            # self.init_algorithm_table(self.DbUtil.get_algorithmInfo(), self.algorithmSelectView.ui.tableWidget_algorithm,
            #                           self.import_view.ui.label_algorithm_name)
            # self.algorithmSelectView.show()
        else:
            QMessageBox.information(self, '提示', '请选择分类：状态或波形', QMessageBox.Ok)
            return

    def getSelectAlgorithmInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.algorithm_set = REPData[2]
                self.curPageMax_al=REPData[3]
                self.algorithmSelectView.ui.tableWidget_algorithm.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.algorithmSelectView.ui.tableWidget_algorithm.clear()
                self.init_algorithm_table(self.algorithm_set, self.algorithmSelectView.ui.tableWidget_algorithm,
                                          self.import_view.ui.label_algorithm_name)
                self.algorithmSelectView.setPageController_al(self.curPageMax_al)
                self.algorithmSelectView.control_signal_al.connect(self.page_controller_al)

                self.algorithmSelectView.show()
                self.import_view.ui.pushButton_algorithm_select.setEnabled(True)
            elif REPData[0] =='2':
                QMessageBox.information(self, '提示', '没有对应的算法', QMessageBox.Ok)
                self.import_view.ui.pushButton_algorithm_select.setEnabled(True)
            else:
                QMessageBox.information(self, '提示', '获取算法信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('getSelectAlgorithmInfo', e)
    def page_controller_al(self, signal):
        if "home" == signal[0]:
            if self.curPageIndex_al == 1:
                QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                return
            self.curPageIndex_al = 1
            self.algorithmSelectView.curPage.setText(str(self.curPageIndex_al))
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            if self.curPageIndex_al <= 1:
                return
            self.curPageIndex_al = self.curPageIndex_al - 1
            self.algorithmSelectView.curPage.setText(str(self.curPageIndex_al))
        elif "next" == signal[0]:
            if self.curPageMax_al == int(signal[1]) or self.search_alg_page_info == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.curPageIndex_al = self.curPageIndex_al + 1
            self.algorithmSelectView.curPage.setText(str(self.curPageIndex_al))
        elif "final" == signal[0]:
            if self.curPageIndex_al == self.curPageMax_al or self.search_alg_page_info == self.curPageIndex_al:
                QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                return
            self.curPageIndex_al = self.curPageMax_al
            self.algorithmSelectView.curPage.setText(str(self.curPageMax_al))
        elif "confirm" == signal[0]:
            if signal[1]=='':
                QMessageBox.information(self, "提示", "请输入数字", QMessageBox.Yes)
                return
            if self.curPageIndex_al == int(signal[1]):
                QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                return
            if self.curPageMax_al < int(signal[1]) or int(signal[1]) <= 0:
                QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                return
            if self.algorithmSelectView.ui.lineValue.text() != '' and self.algorithmSelectView.ui.btnSelect1.text() =='取消查询':
                if self.search_alg_page_info < int(signal[1]) or int(signal[1]) <= 0:
                    QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                    return
            self.curPageIndex_al = int(signal[1])
            self.algorithmSelectView.curPage.setText(signal[1])

        if self.import_view.ui.checkbox1.isChecked():
            msg = [self.curPageIndex_al, self.pageRows, signal[0],'state']
        else:
            msg = [self.curPageIndex_al, self.pageRows, signal[0],'waveform']
        if self.algorithmSelectView.ui.lineValue.text() != '':
            self.alg_is_search=True
            self.on_clicked_select_algorithm(pageIndex=self.curPageIndex_al)
        else:
            self.client.classifierPaging_al(msg)

    def classifierPaging_alRes(self,REPData):
        try:
            if REPData[0] == '1':
                self.algorithm_set = REPData[2]
                self.algorithmSelectView.ui.tableWidget_algorithm.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.algorithmSelectView.ui.tableWidget_algorithm.clear()
                self.init_algorithm_table(self.algorithm_set, self.algorithmSelectView.ui.tableWidget_algorithm,
                                          self.import_view.ui.label_algorithm_name)
                #self.algorithmSelectView.setPageController_al(self.curPageMax_al)
                #self.algorithmSelectView.control_signal_al.connect(self.page_controller_al)
                self.algorithmSelectView.show()
            else:
                QMessageBox.information(self, '提示', '算法信息翻页失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('getSelectAlgorithmInfo1', e)
    def inquiryCls_alg_InfoRes(self,REPData):
        try:
            if REPData[0] == '1':
                if REPData[2][1]!=[]:
                    QMessageBox.information(self, '提示', '查询算法信息成功', QMessageBox.Ok)
                else:
                    QMessageBox.information(self, '提示', '没有匹配的算法，请点击取消查询重新搜索', QMessageBox.Ok)
                self.search_alg_info = REPData[2][1]
                self.search_alg_page_info=REPData[2][0]
                self.algorithmSelectView.ui.tableWidget_algorithm.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.algorithmSelectView.ui.tableWidget_algorithm.clear()
                self.algorithmSelectView.updatepage(self.curPageIndex_al)
                self.clear_layout(self.algorithmSelectView.control_layout_tempt)
                self.algorithmSelectView.setPageController_al(self.search_alg_page_info)
                self.init_algorithm_table(self.search_alg_info, self.algorithmSelectView.ui.tableWidget_algorithm,
                                          self.import_view.ui.label_algorithm_name)

                self.algorithmSelectView.show()
                # self.init_comboCond()
            else:
                QMessageBox.information(self, '提示', '查询算法信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('inquiryClassifierInfoRes', e)
    def on_clicked_select_algorithm(self,pageIndex):
        try:
            if self.tempt_alg_CurpageIndex ==None:
                self.tempt_alg_CurpageIndex=self.curPageIndex_al
            self.curPageIndex_al=pageIndex
            key_value = self.algorithmSelectView.ui.lineValue.text()
            if key_value == '':
                QMessageBox.information(self, '提示', '请输入要搜索的算法信息', QMessageBox.Ok)
                return
            if self.import_view.ui.checkbox1.isChecked():
                REQmsg = [key_value,pageIndex,self.pageRows,'state']
            else:
                REQmsg = [key_value, pageIndex, self.pageRows,'waveform']
            if self.algorithmSelectView.ui.btnSelect1.text() == "查询":
                self.algorithmSelectView.ui.btnSelect1.setText("取消查询")
                self.client.inquiryCls_alg_Info(REQmsg)
            elif self.alg_is_search==True:
                self.alg_is_search=False
                self.client.inquiryCls_alg_Info(REQmsg)
            elif self.algorithmSelectView.ui.btnSelect1.text() == "取消查询":
                self.algorithmSelectView.ui.tableWidget_algorithm.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.algorithmSelectView.ui.tableWidget_algorithm.clear()
                self.clear_layout(self.algorithmSelectView.control_layout_tempt)
                self.curPageIndex_al=self.tempt_alg_CurpageIndex
                self.algorithmSelectView.updatepage(self.curPageIndex_al)
                self.algorithmSelectView.setPageController_al(self.curPageMax_al)
                self.init_algorithm_table(self.algorithm_set, self.algorithmSelectView.ui.tableWidget_algorithm,
                                          self.import_view.ui.label_algorithm_name)
                self.algorithmSelectView.ui.btnSelect1.setText("查询")
                self.tempt_alg_CurpageIndex=None
                self.search_alg_page_info=None
                self.algorithmSelectView.ui.lineValue.clear()
                self.algorithmSelectView.show()
        except Exception as e:
            print('on_clicked_select_classifier', e)

    def on_clicked_pushButton_set_select(self):
        if self.import_view.ui.checkbox1.isChecked() or self.import_view.ui.checkbox2.isChecked():
            self.search_set_page_info = None
            self.import_view.ui.pushButton_set_select.setEnabled(False)
            self.SetSelectView = SetSelectView(self.curPageIndex_al)
            self.SetSelectView.ui.tableWidget_set.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.SetSelectView.ui.btnSelect1.clicked.connect(lambda: self.on_clicked_select_set(pageIndex=1))
            if self.import_view.ui.checkbox1.isChecked():
                self.client.getSelectSetInfo([self.curPageIndex_set, self.pageRows,'state'])
            else:
                self.client.getSelectSetInfo([self.curPageIndex_set, self.pageRows,'wave'])
        # self.init_algorithm_table(self.DbUtil.get_algorithmInfo(), self.algorithmSelectView.ui.tableWidget_algorithm,
        #                           self.import_view.ui.label_algorithm_name)
        # self.algorithmSelectView.show()
        else:
            QMessageBox.information(self, '提示', '请选择分类：状态或波形', QMessageBox.Ok)
        return
    def on_clicked_select_set(self,pageIndex):
        try:
            if self.tempt_set_CurpageIndex ==None:
                self.tempt_set_CurpageIndex=self.curPageIndex_set
            self.curPageIndex_set=pageIndex
            key_value = self.SetSelectView.ui.lineValue.text()
            if key_value == '':
                QMessageBox.information(self, '提示', '请输入要搜索的数据集信息', QMessageBox.Ok)
                return
            if self.import_view.ui.checkbox1.isChecked():
                REQmsg = [key_value,pageIndex,self.pageRows,'state']
            else:
                REQmsg = [key_value, pageIndex, self.pageRows,'wave']
            if self.SetSelectView.ui.btnSelect1.text() == "查询":
                self.SetSelectView.ui.btnSelect1.setText("取消查询")
                self.client.inquiryCls_set_Info(REQmsg)
            elif self.set_is_search==True:
                self.set_is_search=False
                self.client.inquiryCls_set_Info(REQmsg)
            elif self.SetSelectView.ui.btnSelect1.text() == "取消查询":
                self.SetSelectView.ui.tableWidget_set.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.SetSelectView.ui.tableWidget_set.clear()
                self.clear_layout(self.SetSelectView.control_layout_tempt)
                self.curPageIndex_set=self.tempt_set_CurpageIndex
                self.SetSelectView.updatepage(self.curPageIndex_set)
                self.SetSelectView.setPageController_set(self.curPageMax_set)
                self.init_set_table(self.dataSet, self.SetSelectView.ui.tableWidget_set,
                                          self.import_view.ui.label_set_name)
                self.SetSelectView.ui.btnSelect1.setText("查询")
                self.tempt_set_CurpageIndex=None
                self.search_set_page_info=None
                self.SetSelectView.ui.lineValue.clear()
                self.SetSelectView.show()
        except Exception as e:
            print('on_clicked_select_classifier', e)

    def inquiryCls_set_InfoRes(self,REPData):
        try:
            if REPData[0] == '1':
                if REPData[2][1]!=[]:
                    QMessageBox.information(self, '提示', '查询数据集信息成功', QMessageBox.Ok)
                else:
                    QMessageBox.information(self, '提示', '没有匹配的数据集，请点击取消查询重新搜索', QMessageBox.Ok)
                search_set_info = REPData[2][1]
                self.search_set_page_info=REPData[2][0]
                self.SetSelectView.ui.tableWidget_set.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.SetSelectView.ui.tableWidget_set.clear()
                self.SetSelectView.updatepage(self.curPageIndex_set)
                self.clear_layout(self.SetSelectView.control_layout_tempt)
                self.SetSelectView.setPageController_set(self.search_set_page_info)
                self.init_set_table(search_set_info, self.SetSelectView.ui.tableWidget_set,
                                          self.import_view.ui.label_set_name)

                self.SetSelectView.show()
                # self.init_comboCond()
            else:
                QMessageBox.information(self, '提示', '查询数据集信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('inquiryCls_set_InfoRes', e)
    def getSelectSetInfoRes(self,REPData):
        try:
            if REPData[0] == '1':
                self.dataSet = REPData[2]
                self.curPageMax_set=REPData[3]
                self.SetSelectView.ui.tableWidget_set.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.SetSelectView.ui.tableWidget_set.clear()
                self.init_set_table(self.dataSet, self.SetSelectView.ui.tableWidget_set,
                                          self.import_view.ui.label_set_name)
                self.SetSelectView.setPageController_set(self.curPageMax_set)
                self.SetSelectView.control_signal_set.connect(self.page_controller_set)
                self.SetSelectView.show()
                self.import_view.ui.pushButton_set_select.setEnabled(True)
            elif REPData[0] =='2':
                QMessageBox.information(self, '提示', '没有数据集', QMessageBox.Ok)
                self.import_view.ui.pushButton_set_select.setEnabled(True)
            else:
                QMessageBox.information(self, '提示', '获取数据集信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('getSelectSetInfoRes', e)
            # for id, name, config_id, des, fileTrain, fileTest in data[1][1]:
            #     print(f'des: {des}')
            #     tempType = json.loads(des)['type']
            #     print(f'tempType: {tempType}')
            #     tempSetInfo.append(
            #         [id, name, '波形' if tempType == 'wave' else '状态', fileTrain, fileTest, config_id, des])
    def check_file_hash(self,file_path):
        try:
            with open(file_path, 'rb') as file:  # 检测文件完整性
                content = file.read()
                hash_value= hashlib.sha256(content).hexdigest()
                return hash_value
        except FileNotFoundError:
            print(f"无法找到文件 {file_path}。")
        except Exception as e:
            print(f"发生错误：{e}")

    def init_algorithm_table(self, algorithm_info, table, algorithm_name_label):
        item_row = -1
        if table in self._clicked_connections:
            table.clicked.disconnect(self._clicked_connections[table])

        # 响应函数，获取用户选择的算法信息，并关闭页面
        def on_clicked_algorithm_view_item():
            item_row = table.currentRow()
            self.algorithm = None
            self.algorithm = algorithm_info[item_row]
            print(1 and self.algorithm)
            print(table)
            algorithm_name = self.algorithm[1]
            _translate = QtCore.QCoreApplication.translate
            algorithm_name_label.setText(_translate("model_import",
                                                    "<html><head/><body><p><span style=\" font-size:12pt;\">模型算法：" + algorithm_name + "</span></p></body></html>"))

            self.algorithmSelectView.close()
        table.clicked.connect(on_clicked_algorithm_view_item)
        self._clicked_connections[table] = on_clicked_algorithm_view_item  # 记录新的连接
        header = ['算法名称']
        field = ['alg_name']
        data = algorithm_info
        col_num = len(header)
        row_num = 0
        if algorithm_info:
            # 删除不必要的信息，只留下算法名称和训练参数和测试参数
            data = np.delete(algorithm_info, [0, 3, 8], axis=1)
            row_num = len(data)
        table.setColumnCount(col_num)
        table.setRowCount(row_num)
        for i in range(col_num):
            header_item = QTableWidgetItem(header[i])
            font = header_item.font()
            font.setPointSize(40)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            header_item.setData(Qt.UserRole, field[i])
            table.setHorizontalHeaderItem(i, header_item)
            # 拉伸表格列项，使其铺满
            table.horizontalHeader().setStretchLastSection(True)
        for r in range(row_num):
            for c in range(col_num):
                item = QTableWidgetItem(str(data[r][c]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                font.setPointSize(24)
                item.setFont(font)
                table.setItem(r, c, item)
        table.horizontalHeader().setHighlightSections(False)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        table.setSelectionMode(QTableWidget.SingleSelection)
        #   按字段长度进行填充
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # 增加和查询的时候列数会改变，所以需要保存原来的列数
        # col = table.columnCount()
    def init_set_table(self, set_info, table, set_name_label):
        item_row = -1
        if table in self._clicked_connections:
            table.clicked.disconnect(self._clicked_connections[table])

        # 响应函数，获取用户选择的数据集信息，并关闭页面
        def on_clicked_set_view_item():
            item_row = table.currentRow()
            self.set = None
            self.set = set_info[item_row]
            print(1 and self.set)
            print(table)
            set_name = self.set[1]
            _translate = QtCore.QCoreApplication.translate
            set_name_label.setText(_translate("model_import",
                                                    "<html><head/><body><p><span style=\" font-size:12pt;\">数据集：" + set_name + "</span></p></body></html>"))

            self.SetSelectView.close()
        table.clicked.connect(on_clicked_set_view_item)
        self._clicked_connections[table] = on_clicked_set_view_item  # 记录新的连接
        header = ['数据集名称']
        field = ['set_name']
        data = set_info
        col_num = len(header)
        row_num = 0
        if set_info:
            # 删除不必要的信息，只留下算法名称和训练参数和测试参数
            data = np.delete(set_info, [0,2,3,4,5], axis=1)
            row_num = len(data)
        table.setColumnCount(col_num)
        table.setRowCount(row_num)
        for i in range(col_num):
            header_item = QTableWidgetItem(header[i])
            font = header_item.font()
            font.setPointSize(40)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            header_item.setData(Qt.UserRole, field[i])
            table.setHorizontalHeaderItem(i, header_item)
            # 拉伸表格列项，使其铺满
            table.horizontalHeader().setStretchLastSection(True)
        for r in range(row_num):
            for c in range(col_num):
                item = QTableWidgetItem(str(data[r][c]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                font.setPointSize(24)
                item.setFont(font)
                table.setItem(r, c, item)
        table.horizontalHeader().setHighlightSections(False)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        table.setSelectionMode(QTableWidget.SingleSelection)
        #   按字段长度进行填充
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # 增加和查询的时候列数会改变，所以需要保存原来的列数
        # col = table.columnCount()
    def page_controller_set(self, signal):
        if "home" == signal[0]:
            if self.curPageIndex_set == 1:
                QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                return
            self.curPageIndex_set = 1
            self.SetSelectView.curPage.setText(str(self.curPageIndex_set))
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            if self.curPageIndex_set <= 1:
                return
            self.curPageIndex_set = self.curPageIndex_set - 1
            self.SetSelectView.curPage.setText(str(self.curPageIndex_set))
        elif "next" == signal[0]:
            if self.curPageMax_set == int(signal[1]) or self.search_set_page_info == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.curPageIndex_set = self.curPageIndex_set + 1
            self.SetSelectView.curPage.setText(str(self.curPageIndex_set))
        elif "final" == signal[0]:
            if self.curPageIndex_set == self.curPageMax_set or self.search_set_page_info == self.curPageIndex_set:
                QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                return
            self.curPageIndex_set = self.curPageMax_set
            self.SetSelectView.curPage.setText(str(self.curPageMax_set))
        elif "confirm" == signal[0]:
            if signal[1]=='':
                QMessageBox.information(self, "提示", "请输入数字", QMessageBox.Yes)
                return
            if self.curPageIndex_set == int(signal[1]):
                QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                return
            if self.curPageMax_set < int(signal[1]) or int(signal[1]) <= 0:
                QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                return
            if self.SetSelectView.ui.lineValue.text() != '':
                if self.search_set_page_info < int(signal[1]) or int(signal[1]) <= 0:
                    QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                    return
            self.curPageIndex_set = int(signal[1])
            self.SetSelectView.curPage.setText(signal[1])

        if self.import_view.ui.checkbox1.isChecked():
            msg = [self.curPageIndex_set, self.pageRows,signal[0],'state']
        else:
            msg = [self.curPageIndex_set, self.pageRows,signal[0],'wave']
        if self.SetSelectView.ui.lineValue.text() != '':
            self.set_is_search=True
            self.on_clicked_select_set(pageIndex=self.curPageIndex_set)
        else:
            self.client.classifierPaging_set(msg)

    def classifierPaging_setRes(self,REPData):
        try:
            if REPData[0] == '1':
                self.dataSet = REPData[2]
                self.SetSelectView.ui.tableWidget_set.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.SetSelectView.ui.tableWidget_set.clear()
                self.init_set_table(self.dataSet, self.SetSelectView.ui.tableWidget_set,
                                          self.import_view.ui.label_set_name)
                #self.algorithmSelectView.setPageController_al(self.curPageMax_al)
                #self.algorithmSelectView.control_signal_al.connect(self.page_controller_al)
                self.SetSelectView.show()
            else:
                QMessageBox.information(self, '提示', '数据集信息翻页失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('classifierPaging_setRes', e)
    def on_btnDel_clicked(self):
        row = self.select_row
        answer = QMessageBox.warning(
            self.view, '确认删除！', '您将进行删除操作！',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if answer == QMessageBox.Yes:
            if row == -1:
                QMessageBox.information(self.view, ' ', '请先选中一行')
                return
            self.client.delClassifierInfo([self.classifier_alg_set_name[row], row,1,self.curPageIndex]) #1表示要进行文件删除
        #     file_path = os.path.join(self.Util.algorithm_path,
        #                              self.DbUtil.get_classifierInfo('classifier_name',
        #                                                             self.classifier_alg_set_name[row][0])[0][4])
        #     relate_model_file = self.DbUtil.get_classifier_file_name(
        #         classifier_name=self.classifier_alg_set_name[row][0])
        #     try:
        #         self.DbUtil.del_classifierInfo('classifier_name', self.classifier_alg_set_name[row][0])
        #     except:
        #         QMessageBox.information(self, "错误", "请将与该用户关联的全部信息删除后，在进行此操作")
        #         return
        #     else:
        #         try:
        #             os.remove(file_path)
        #         except Exception as e:
        #             pass
        #         try:
        #             self.DbUtil.del_relative_model_info(relate_model_file, self.classifier_alg_set_name[row][1])
        #         except:
        #             pass

    def delClassifierInfoRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "错误", "失败原因:%s" %REPData[2][1], QMessageBox.Ok)
                return
            elif REPData[0]=='1':
                self.curPageMax=REPData[4]
                self.curPageIndex=REPData[5]
                #self.is_reload_controller.emit("setBuildController")
                QMessageBox.information(self, '提示', '删除模型信息成功', QMessageBox.Ok)
                self.classifier_alg_set_name = REPData[3]
                self.clear_layout(self.view.ui.verticalLayout_2)
                self.tableWidget = TableWidget(self.classifier_alg_set_name, self.curPageIndex)
                self.view.ui.verticalLayout_2.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
                self.tableWidget.table.itemClicked.connect(self.set_selectRow)
                #self.client.getClassifierAlgSetName([self.curPageIndex, self.pageRows])
                #self.view.initTable(self.classifier_alg_set_name)
                print(self.classifier_alg_set_name)
            elif REPData[0]=='2':
                QMessageBox.information(self, '提示', '删除模型信息成功', QMessageBox.Ok)
                self.clear_layout(self.view.ui.verticalLayout_2)
                QMessageBox.information(self, '提示', '无模型信息', QMessageBox.Ok)
        except Exception as e:
            print('delClassifierInfoRes', e)


    # def on_btnCancelUpdate_clicked(self, row):
    #     data = self.classifier_alg_set_name[row]
    #     for i in range(len(data)):
    #         self.view.ui.tableWidget.item(row, i).setText(str(data[i]))
    #     self.view.ui.tableWidget.removeColumn(len(self.field))
    #
    #     self.update = -1
    #     #   按字段长度进行填充
    #     self.view.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    #
    #     self.enable_tableWidgetItem(row)
    #     self.view.ui.tableWidget.clear()
    #     self.init_table(self.classifier_alg_set_name)

    # 禁用除了activate_row以外的其他行
    # def disable_tableWidgetItem(self, active_row):
    #     row = self.view.ui.tableWidget.rowCount()
    #     col = self.view.ui.tableWidget.columnCount()
    #     for r in range(row):
    #         if r != active_row:
    #             self.disable_tableWidgetItem_row_col([r], range(col))
    #
    # # 禁用disable_row行disable_col列的表格项，disable_col和disable_row都为[]，如[1,2]
    # def disable_tableWidgetItem_row_col(self, disable_row, disable_col):
    #     for r in disable_row:
    #         for c in disable_col:
    #             item = self.view.ui.tableWidget.item(r, c)
    #             if item == None:
    #                 cellWidget = self.view.ui.tableWidget.cellWidget(r, c)
    #                 if cellWidget == None:
    #                     return
    #                 else:
    #                     cellWidget.setEnabled(False)
    #             else:
    #                 item.setFlags(item.flags() & (~Qt.ItemIsEnabled))

    # 启用除了activate_row以外的其他行
    # def enable_tableWidgetItem(self, active_row):
    #     row = self.view.ui.tableWidget.rowCount()
    #     col = self.view.ui.tableWidget.columnCount()
    #     for r in range(row):
    #         if r != active_row:
    #             for c in range(col):
    #                 item = self.view.ui.tableWidget.item(r, c)
    #                 if item == None:
    #                     cellWidget = self.view.ui.tableWidget.cellWidget(r, c)
    #                     if cellWidget == None:
    #                         continue
    #                     else:
    #                         cellWidget.setEnabled(True)
    #                 else:
    #                     item.setFlags(Qt.ItemIsEnabled |
    #                                   Qt.ItemIsEditable | Qt.ItemIsSelectable)

    # 保存选中行的数据
    # def save_row_data(self, row):
    #     value = []
    #     for i in range(len(self.field)):
    #         if self.view.ui.tableWidget.item(row, i):
    #             temp = self.view.ui.tableWidget.item(row, i).text()
    #         else:
    #             temp = ''
    #         value.append(temp)
    #     return value
    def set_selectRow(self, item):
        print(f'set_selectRow: {item.row()}')
        self.select_row = item.row()

    def on_clicked_configOptions_select(self):
        self.configView=PrentryView()
        self.configView.setAttribute(Qt.WA_DeleteOnClose)
        self.configView.setWindowModality(Qt.ApplicationModal)
        self.configView.show()
        self.configView.ui.btnConfirm.setEnabled(False)
        self.configView.ui.btnReturn.setEnabled(True)
        self.configView.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.configView.ui.tableWidget.resizeRowsToContents()
        self.configView.ui.tableWidget.resizeColumnsToContents()
        self.configView.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.configView.ui.tableWidget.clicked.connect(self.on_tableWidget_itemClicked)
        self.configView.ui.btnReturn.clicked.connect(self.on_btnReturn_clicked)
        self.configView.ui.btnConfirm.clicked.connect(self.on_btnConfirm_clicked)
        self.client.getClassifier_config()
    def getClassifier_configRes(self, configInfo):
        print(f'chgCurUserConfigRes: {configInfo}')
        self.configInfo = configInfo
        col_num = 5
        columnName = ['方案名', '采样率', '陷波频率', '低通滤波', '高通滤波']
        self.configView.ui.tableWidget.setColumnCount(col_num)
        for i in range(col_num):
            header_item = QTableWidgetItem(columnName[i])
            font = header_item.font()
            font.setPointSize(10)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            self.configView.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
        self.configView.ui.tableWidget.horizontalHeader().setHighlightSections(False)
        self.configView.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        row_num = len(self.configInfo)
        self.configView.ui.tableWidget.setRowCount(row_num)
        for r in range(row_num):
            for i in range(col_num):
                self.configView.ui.tableWidget.setRowHeight(r, 45)
                item = QTableWidgetItem(str(self.configInfo[r][i + 1]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                font.setPointSize(11)
                item.setFont(font)
                self.configView.ui.tableWidget.setItem(r, i, item)
        self.configView.ui.tableWidget.verticalHeader().setVisible(False)

    def on_btnConfirm_clicked(self):
        self.configView.signal_save_configID_names.connect(self.respondFunction_signal_save_configID_names)
        row = self.configView.ui.tableWidget.currentRow()
        self.configID=self.configInfo[row][0]
        configName=self.configInfo[row][1]
        self.configView.signal_save_configID_names.emit(configName)
        #self.getCurConfigDataRes(self.configInfo[row])
        self.configView.close()
    def respondFunction_signal_save_configID_names(self,configName):
        self.import_view.ui.label_configOptions_select.setText(f"配置方案：{configName}")

    def on_tableWidget_itemClicked(self):
        self.configView.ui.btnConfirm.setEnabled(True)
    def on_btnReturn_clicked(self):
        self.configView.close()
    def exit(self):
        self.client.getClassifierAlgSetNameResSig.disconnect()
        self.client.inquiryClassifierInfoResSig.disconnect()
        self.client.delClassifierInfoResSig.disconnect()
        self.client.getSelectAlgorithmInfoResSig.disconnect()
        self.client.checkClassifierInfoRessig.disconnect()
        self.client.add_import_classifierInfoRessig.disconnect()
        self.client.checkstateRessig.disconnect()
        self.client.model_transmit_messageRessig.disconnect()
        self.client.classifier_id_inquiryRessig.disconnect()
        self.client.classifierPagingResSig.disconnect()
        self.client.classifierPaging_alResSig.disconnect()
        self.client.inquiryCls_alg_InfoRessig.disconnect()
        self.client.getClassifier_configRessig.disconnect()


        # self.client.checkNegAlgResSig.disconnect()

    # def menu_select(self, pos):
    #     row_num = -1
    #     for i in self.view.ui.tableWidget.selectionModel().selection().indexes():
    #         row_num = i.row()
    #     if row_num == -1:
    #         return
    #     classifier_name = self.view.ui.tableWidget.item(row_num, 0).text()
    #     alg_name = self.view.ui.tableWidget.item(row_num, 1).text()
    #     menu = QMenu()
    #     item1 = menu.addAction(u"设置为负例识别模型")
    #     # item2 = menu.addAction(u"集合重建")
    #     # item4 = menu.addAction(u"集合导出")
    #     # item3 = menu.addAction(u"删除集合")
    #     action = menu.exec_(self.view.ui.tableWidget.mapToGlobal(pos))
    #     if action == item1:
    #         self.set_model_as_negative(classifier_name, alg_name)
            # self.set_describe(set_name, set_type)
        # elif action == item2:
        #     self.setRebuild(set_name, set_type)
        # elif action == item3:
        #     self.set_del(set_name, row_num)
        # elif action == item4:
        #     self.set_export(set_name)

    # def set_model_as_negative(self, classifier_name, alg_name):
    #     reply = QMessageBox.information(self, '提示', '是否将模型：{},设置为算法：{}的负例识别模型？'.format(classifier_name, alg_name),
    #                                     QMessageBox.Yes | QMessageBox.No)
    #     if reply == 16384:
    #         self.client.checkNegAlg([alg_name])
            # if not self.DbUtil.check_is_neg_alg(alg_name):
            #     QMessageBox.warning(self, '错误', '算法：{}不是负例识别算法，无法设置负例识别模型！'.format(alg_name))
            #     return
            # else:
            #     self.DbUtil.set_neg_model_info(classifier_name, alg_name)
            #     self.is_reload_controller.emit("setBuildController")
            #     QMessageBox.information(self, "设置成功", "已将模型：{},设置为算法：{}的负例识别模型！".format(classifier_name, alg_name))
#         else:
#             return
#
#     def checkNegAlgRes(self, REPData):
#         pass
# # 点击分类器选择按钮
# def on_btnclassifierselect_clicked(self):
#     # 已经选择过了算法，直接将算法名称显示出来
#     if self.file_model:
#         f_name = self.file_model[0].split('/')[-1]
#         self.view.ui.btnSelect.setText("{}".format(f_name))
#     # 数据库中标签添加成功，将文件复制到classifier文件夹目录下
#     classifier = QFileDialog.getOpenFileName(self, "选择文件", self.Util.root_path)
#     # 用户成功选择算法文件,将算法文件信息存储，并将算法名称显示到页面
#     if classifier[0]:
#         self.file_model = classifier
#         f_name = self.file_model[0].split('/')[-1]
#         self.question.ui.clsbtn.setText(f_name)