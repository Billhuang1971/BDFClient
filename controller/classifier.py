from view.classifier import ClassifierView, clsimportView,clsuploadView,AlgorithmSelectView, LabelSelectVew,clsPrentryView,SetSelectView
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
        self.set=None #存储选择的数据集
        self.curPageIndex_al = 1  #
        self.curPageMax_al = 1  #
        self.curPageIndex_set=1
        self.curPageMax_set=1
        self.ProgressBarView = None# 进度条对象
        self.data_blocks=[]
        self.is_search = False #标记翻页时是否处于搜索
        self.tableWidget = None #存储表格
        self.curPageIndex = 1  #当前页
        self.pageRows = 12  # 每页12个
        self.curPageMax = 1  #当前最大页数
        self.row_content = [] #选中的行的数据
        self.alg_is_search=False #算法选择搜索翻页控制
        self.set_is_search = False#数据集选择界面是否属于搜索状态
        self.start_position=None #传输时从文件读取的位置
        self.block_size=5*1024*1024 #传输时指定块大小 5MB
        self.model_hash_right=None #存储模型文件的校验值
        self.root_path = os.path.dirname(os.path.dirname(__file__))+'\\'
        self.view.ui.btn_import.clicked.connect(self.on_btn_import_clicked)
        self.view.ui.btnDel.clicked.connect(self.on_btnDel_clicked)
        self.view.ui.btn_upload.clicked.connect(self.onClicked_upload)
        self.view.ui.btnSelect.clicked.connect(lambda :self.on_clicked_select_classifier(pageIndex=1))

        self.update = -1
        self.insert = -1
        self.classifier_alg_set_name = None #保存当前表格对应的数据
        self.restore_classifier=None  #保存取消查询后还原的数据
        self.search_classifier_page_info=None
        self.tempt_CurPageIndex=None
        self.algorithm_set=None #存放服务器传回的算法信息
        self.dataSet=None #存放服务器传回的数据集信息
        self.search_alg_page_info=None
        self.search_set_page_info=None
        self.tempt_alg_CurpageIndex=None
        self.tempt_set_CurpageIndex = None
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
        #self.client.add_import_classifierInfoRessig.connect(self.add_import_classifierInfoRes)
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
        self.client.upload_schemeResSig.connect(self.upload_schemeRes)
        self.client.upload_modelResSig.connect(self.upload_modelRes)
        self.init_comboCond()
        self.init_filepath()

    def init_filepath(self):
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
    def getClassifierAlgSetNameRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.classifier_alg_set_name = REPData[2]
                self.curPageMax=REPData[3]
                self.view.initTable(self.classifier_alg_set_name,self.curPageIndex)
                self.view.setPageController(self.curPageMax)  # 表格设置页码控制
                self.view.control_signal.connect(self.page_controller)
            else:
                if REPData[2]==0:
                    QMessageBox.information(self, '提示', '无模型信息', QMessageBox.Ok)
                else:
                    QMessageBox.information(self, '提示', '获取模型信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('getClassifierAlgSetNameRes', e)
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
                if  self.view.ui.btnSelect.text() == "取消查询": #在搜索时删除直接解除并返回
                    self.view.update_table(self.classifier_alg_set_name, self.curPageIndex, self.curPageMax)
                    self.view.ui.btnSelect.setText("查询")
                    self.search_classifier_page_info = None
                    self.view.clear_select()
                    self.view.ui.lineValue.clear()
                else:
                    self.view.update_table(self.classifier_alg_set_name, self.curPageIndex,self.curPageMax)

            elif REPData[0]=='2':
                QMessageBox.information(self, '提示', '删除模型信息成功', QMessageBox.Ok)
                self.clear_layout(self.view.ui.verticalLayout_2)
                QMessageBox.information(self, '提示', '无模型信息', QMessageBox.Ok)
        except Exception as e:
            print('delClassifierInfoRes', e)
    def page_controller(self, signal): #页码控制
        if "home" == signal[0]:
            if self.curPageIndex == 1:
                QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                return
            self.curPageIndex = 1
            self.view.curPage.setText(str(self.curPageIndex))
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            if self.curPageIndex <= 1:
                return
            self.curPageIndex = self.curPageIndex - 1
            self.view.curPage.setText(str(self.curPageIndex))
        elif "next" == signal[0]:
            if self.curPageMax == int(signal[1]) or self.search_classifier_page_info == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.curPageIndex = self.curPageIndex + 1
            self.view.curPage.setText(str(self.curPageIndex))
        elif "final" == signal[0]:
            if self.curPageIndex == self.curPageMax or self.search_classifier_page_info == self.curPageIndex:
                QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                return
            if self.search_classifier_page_info!=None:
                self.curPageIndex=self.search_classifier_page_info
            else:
                self.curPageIndex = self.curPageMax
            self.view.curPage.setText(str(self.curPageIndex))
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
            self.view.curPage.setText(signal[1])

        msg = [self.curPageIndex, self.pageRows, signal[0]]
        if self.view.ui.lineValue.text() != '' and self.view.ui.btnSelect.text() == "取消查询":
            self.is_search=True
            self.on_clicked_select_classifier(pageIndex=self.curPageIndex)
        else:
            self.client.classifierPaging(msg)
    def classifierPagingRes(self,REPData): #页码控制返回
        try:
            self.classifier_alg_set_name = REPData[2]
            self.view.update_table(self.classifier_alg_set_name, self.curPageIndex)
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
    def on_clicked_select_classifier(self,pageIndex):
        try:
            self.curPageIndex=pageIndex
            key_word = self.view.ui.comboCond.currentText()
            key_value = self.view.ui.lineValue.text()
            if self.view.state_select_name==None:
                QMessageBox.information(self, '提示', '请选择对应模型状态进行搜索', QMessageBox.Ok)
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
            REQmsg = [key_word, key_value,pageIndex,self.pageRows,self.view.state_select_name]
            if self.view.ui.btnSelect.text() == "查询":
                self.view.ui.btnSelect.setText("取消查询")
                self.restore_classifier=self.classifier_alg_set_name#查询前保存恢复数据
                self.client.inquiryClassifierInfo(REQmsg)
            elif self.is_search==True: #翻页时处理
                self.is_search=False
                self.client.inquiryClassifierInfo(REQmsg)
            elif self.view.ui.btnSelect.text() == "取消查询": #取消处理
                self.client.inquiryClassifierInfo(['','',1,self.pageRows,''])
                self.view.state_select_name=None
                self.view.clear_select()
                self.view.ui.btnSelect.setText("查询")
                self.search_classifier_page_info=None
                self.view.ui.lineValue.clear()
        except Exception as e:
            print('on_clicked_select_classifier', e)

    def inquiryClassifierInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                #QMessageBox.information(self, '提示', '查询模型信息成功', QMessageBox.Ok)
                self.classifier_alg_set_name = REPData[2][1]
                self.search_classifier_page_info =REPData[2][0]#总页数
                self.view.update_table(self.classifier_alg_set_name, self.curPageIndex,self.search_classifier_page_info)
            else:
                QMessageBox.information(self, '提示', '查询模型信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('inquiryClassifierInfoRes', e)
    def on_btn_import_clicked(self):
        self.import_view = clsimportView()
        self.import_view.show()
        # 只能输入数字
        # 创建 QIntValidator 类的实例对象，并设置限制范围
        validator = QIntValidator()
        validator.setRange(0, 9999)
        # 将 QIntValidator 对象设置为 QLineEdit 控件的验证器
        #self.import_view.ui.lineEdit_sample_rate.setValidator(validator)
        self.import_view.ui.lineEdit_epoch_length_name.setValidator(validator)
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
    def onClicked_upload(self):
        path = os.path.dirname(os.path.dirname(__file__)) + '\\upload\\model\\'
        flag = self.cAppUtil.isNull(path)
        if flag == False:
            QMessageBox.information(self, '提示', '系统正在处理未完成的上传任务，完成后请重新上传任务',
                                    QMessageBox.Yes)
            suffix_txt = 'txt'
            suffix_json = 'json'
            file_names = [f for f in os.listdir(self.model_path) if
                          not f.endswith(suffix_txt) and not f.endswith(suffix_json)]
            self.client.classifier_id_inquiry(file_names)  # 先检验服务器是否存在该名称的数据
            return
        reply =QMessageBox.warning(self.view, '确认上传！', '您将进行上传模型的操作！',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == 16384:
            self.row_content.clear()
            selected_rows = self.view.table.selectionModel().selectedRows()
            if selected_rows:

                selected_row = selected_rows[0].row()
                for column in range(self.view.table.columnCount()):
                    item = self.view.table.item(selected_row, column)
                    if item:
                        self.row_content.append(item.text())
                self.upload_view = clsuploadView()
                self.upload_view.show()
                self.upload_view.ui.pushButton_model_select.clicked.connect(self.on_clicked_pushButton_model_select)
                self.upload_view.ui.pushButton_upload.clicked.connect(self.on_clicked_upload)
            else:
                QMessageBox.information(self.view, ' ', '请先选中一行')
                return
        else:
            return

    def on_clicked_pushButton_model_select(self):
        try:
            self.file_model = None
            model = QFileDialog.getOpenFileName(self, "选择模型文件", self.root_path)
            # 用户成功选择算法文件
            if model[0]:
                self.file_model = model
                f_name = self.file_model[0].split('/')[-1]
                _translate = QtCore.QCoreApplication.translate
                self.upload_view.ui.label_model_path.setText(_translate("model_import",
                                                                        "<html><head/><body><p><span style=\" font-size:12pt;\">模型文件：" + f_name + "</span></p></body></html>"))
        except Exception as e:
            print('on_clicked_pushButton_model_select', e)
    def on_clicked_upload(self):
        model_file_type = self.file_model[0].split('/')[-1].split('.')[-1]  # 文件后缀
        selected_item = self.upload_view.ui.Qcombox1.currentText()
        nb_class=int(self.upload_view.ui.lineEdit_clsnum.text())
        sample_lenth=int(self.upload_view.ui.lineEdit_epoch_length_name.text())
        if selected_item=='状态':
            type='state'
        else:
            type='wave'
        msg=[self.row_content,model_file_type,type,nb_class,sample_lenth]
        self.upload_view.close()
        self.client.upload_model(msg)
    def upload_modelRes(self,REPmsg):
        if REPmsg[0]=='0':
            QMessageBox.information(self, '提示', '选择的模型不是准备上传状态', QMessageBox.Ok)
            return
        elif REPmsg[0]=='2':
            QMessageBox.information(self, '提示', '模型匹配失败,请确认模型和数据集（算法）是否匹配', QMessageBox.Ok)
            return
        else:
            self.client.checkstate([REPmsg[1]])

    def onClicked_pushButton_save(self):#保存模型
        model_name = self.import_view.ui.lineEdit_model_name.text()
        epoch_len = self.import_view.ui.lineEdit_epoch_length_name.text()
        configID = self.configID
        channel_info = self.import_view.ui.lineEdit_channel_info.text()
        if not model_name:
            QMessageBox.information(self.import_view, '提示', '请输入模型名称', QMessageBox.Yes)
            return
        if not self.algorithm:
            QMessageBox.information(self.import_view, '提示', '尚未选择模型的算法', QMessageBox.Yes)
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
        try:
            label_names = ''
            first = True
            for label_name in self.import_view.saved_EEG_names:
                if first:
                    label_names += "{}".format(str(label_name))
                    first = False
                else:
                    label_names += "|{}".format(str(label_name))
            self.configID = None
            content_label = ''  # 所选的状态通道
            for item in self.import_view.saved_EEG_names:
                content_label += item + '/'
            selected_text = self.import_view.ui.Unit_comboCond.currentText()
            self.client.upload_scheme([model_name, self.algorithm[0],self.set[0],
                                                      epoch_len,configID,content_label,selected_text])
        except Exception as result:
            QMessageBox.information(self.import_view, '提示', "失败原因: %s" % result, QMessageBox.Yes)
            return
    def upload_schemeRes(self,REPData):
        if REPData[0]=='0':
            QMessageBox.information(self.import_view, '提示', '当前模型名称已存在，请更改', QMessageBox.Yes)
            return
        else:
            QMessageBox.information(self.import_view, '提示', '模型保存成功', QMessageBox.Yes)
            self.set = None
            self.algorithm = None
            self.import_view.close()

    #上传④返回
    def checkstateRes(self,REPData):#REPData['1', REQmsg[1],classifier_info]
        if REPData[0] =='1' and REPData[2]:#模型存在且state=ready
            flag=self.copyfile(REPData[2][0][4])
            if flag==True:#开始传输①
                self.client.model_transmit_message(['start',REPData[2][0][0],REPData[2][0][4],0])#start, classifier_id, filename, block_id,本机mac地址
            else:
                QMessageBox.information(self, '提示', '文件复制失败，请重试', QMessageBox.Ok)
                return
        else:
            QMessageBox.information(self, '提示', '记录不存在或该记录state不为“ready”', QMessageBox.Ok)
    def copyfile(self,filename):
        try:
            shutil.copyfile(self.file_model[0],
                            self.model_path + filename)
            self.model_hash_right = self.check_file_hash(self.file_model[0])
            data_to_store = {"hash_value": ""}
            data_to_store["hash_value"]=self.model_hash_right
            file_path = os.path.join(self.model_path, 'hash_data.json')
            with open(file_path,'w') as json_file:
                json.dump(data_to_store, json_file)
            self.model_hash_right=None
            return True
        except Exception as result:
            QMessageBox.information(self.import_view, '提示', "失败原因: %s" % result, QMessageBox.Yes)
            return False
    def model_transmit_messageRes(self,REPData): #传输①返回
        if REPData[2][0]=='waiting': #6.1
            trans_path = self.model_path + REPData[2][2][2] #传输文件的地址
            file_size = os.path.getsize(trans_path)
            totalDataSize = math.ceil(file_size / self.block_size)  # 总块数
            if REPData[2][1]==1:#判断block_id=1
                file_path=self.model_path+'uploading.txt'
                self.cAppUtil.makeTxt(file_path)
                selected_index=[1,2,4]
                tempt_uploading=''
                for index in selected_index:
                    tempt_uploading=tempt_uploading+str(REPData[2][2][index])+','#REP=start, classifier_id, filename, block_id,本机mac地址
                self.cAppUtil.writeTxt(file_path,tempt_uploading)
                self.start_position = 0
                with open(trans_path, "rb") as file_model:
                    file_model.seek(self.start_position)
                    buffer = file_model.read(self.block_size) #从指定位置读取的数据块内容
                self.ProgressBarView = ProgressBarView(window_title="模型文件传输中", hasStopBtn=False,maximum=totalDataSize)
                self.ProgressBarView.show()
                # 开始传输数据
                self.client.model_transmit_message(['uploading',REPData[2][2][1],REPData[2][2][2],REPData[2][1],
                                                    buffer]) #“uploading，classifier_id,filename，block_id，数据块,mac”
                #第一组数据即0，故-1
            elif REPData[2][1]> totalDataSize :#判断block_id>blockN
                # 传输完成后关闭进度
                self.ProgressBarView.close()
                self.client.model_transmit_message(['uploaded',REPData[2][2][1],REPData[2][2][2],REPData[2][2][3]])#“uploaded,classifier_id,filename,block_id和本机mac地址”
            elif REPData[2][1] > 1 :
                # 更新进度条
                if self.ProgressBarView==None:
                    self.ProgressBarView = ProgressBarView(window_title="模型文件传输中", hasStopBtn=False,maximum=totalDataSize,speed=1)
                    self.ProgressBarView.show()
                self.start_position=(REPData[2][1]-1)*self.block_size
                self.ProgressBarView.updateProgressBar(REPData[2][1])
                with open(trans_path, "rb") as file_model:
                    file_model.seek(self.start_position)
                    buffer = file_model.read(self.block_size) #从指定位置读取的数据块内容
                #self.progressDialog.setValue(int((tempt_value / totalDataSize)*100))
                self.client.model_transmit_message(['uploading', REPData[2][2][1], REPData[2][2][2], REPData[2][1],
                                                    buffer])
        elif REPData[2][0] == 'uploaded':#6.3 √
            if self.ProgressBarView:
                self.ProgressBarView.close()
            self.cAppUtil.empty(self.model_path)
            self.start_position=0
            QMessageBox.information(self, '提示', '上传已完成,请刷新页面查看', QMessageBox.Ok)
        elif REPData[2][0] in ['wrongSite','unknownError','clean','wrongServer']: #6.2 √
            self.cAppUtil.empty(self.model_path)
            QMessageBox.information(self, '提示', '出现错误，传输失败', QMessageBox.Ok)
            if self.ProgressBarView:
                self.ProgressBarView.close()
        elif REPData[2][0] == 'recover':  # 6.4 √
            file_path2 = os.path.join(self.model_path, "uploading.txt")
            if os.path.exists(file_path2):
                self.cAppUtil.empty(self.model_path,filename="uploading.txt")
            self.cAppUtil.makeTxt(file_path2)
            selected_index = [1, 2, 4]
            tempt_uploading = ''
            for index in selected_index:
                tempt_uploading = tempt_uploading + str(REPData[2][index]) + ','  # REP=start, classifier_id, filename, block_id,本机mac地址
            self.cAppUtil.writeTxt(file_path2, tempt_uploading)
            if self.ProgressBarView == None:
                self.ProgressBarView = ProgressBarView(window_title="模型文件传输中", hasStopBtn=False,
                                                        speed=1)
                self.ProgressBarView.show()
                self.ProgressBarView.updateProgressBar(0)
            #self.progressDialog.setValue(0)
            self.client.model_transmit_message(['continue', REPData[2][1],REPData[2][2]])
    def classifier_id_inquiryRes(self,REPData):#步骤七（分支①第二步返回）
        if REPData[2]: #数据库存在该模型信息
            model_file = os.path.join(self.model_path,REPData[2][0][4] )
            model_hash = self.check_file_hash(model_file)
            file_path = os.path.join(self.model_path, 'hash_data.json')
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    hash_value = data.get('hash_value')
                if model_hash != hash_value:  # 协议7.1√
                    self.cAppUtil.empty(self.model_path)
                    QMessageBox.information(self, '提示', '本地文件filename出错，上传过程需重新开始',
                                            QMessageBox.Ok)
                    self.client.cls_restate([REPData[2][0][0]]) #需要去服务器删除文件和设置状态重新上传 file_name,state,block_id
                else:
                    try:
                        # 尝试打开文件并读取内容
                        with open(self.model_path + 'uploading.txt', 'r') as file:
                            content = file.read()
                        if not content: #协议7.3√
                            QMessageBox.information(self, '提示', '上传过程出错，系统将从出错位置开始继续上传',
                                                    QMessageBox.Ok)
                            self.client.model_transmit_message(['clean', REPData[2][0][0], REPData[2][0][4]])  # 7.3
                        else:  # 协议7.4 √
                            QMessageBox.information(self, '提示', '上传过程出错，系统将从出错位置开始继续上传',
                                                    QMessageBox.Ok)
                            self.client.model_transmit_message(['continue', REPData[2][0][0], REPData[2][0][4]])
                    except FileNotFoundError:  #协议 7.2 √
                        QMessageBox.information(self, '提示', '上传过程出错，系统将从出错位置开始继续上传',
                                                QMessageBox.Ok)
                        self.client.model_transmit_message(['unknown', REPData[2][0][0], REPData[2][0][4]])
                        return
                    except IOError: #协议7.3 √
                        QMessageBox.information(self, '提示', '上传过程出错，系统将从出错位置开始继续上传',
                                                QMessageBox.Ok)
                        self.client.model_transmit_message(['clean', REPData[2][0][0], REPData[2][0][4]])  # 7.3
                        return
            except FileNotFoundError:#协议7.1√
                self.cAppUtil.empty(self.model_path)
                QMessageBox.information(self, '提示', '本地文件filename出错，上传过程需重新开始',
                                        QMessageBox.Ok)
                self.client.cls_restate([REPData[2][0][0]])
        else:#模型信息不存在
            self.cAppUtil.empty(self.model_path)
            QMessageBox.information(self, '提示', '服务器无此模型信息，上传过程需重新开始',
                                    QMessageBox.Ok)

    #算法选择
    def on_clicked_pushButton_algorithm_select(self):
        if self.import_view.ui.checkbox1.isChecked() or self.import_view.ui.checkbox2.isChecked():
            self.search_alg_page_info = None
            self.import_view.ui.pushButton_algorithm_select.setEnabled(False)
            if self.import_view.ui.checkbox1.isChecked():
                self.client.getSelectAlgorithmInfo([self.curPageIndex_al, self.pageRows,'state'])
            else:
                self.client.getSelectAlgorithmInfo([self.curPageIndex_al, self.pageRows,'waveform'])

        else:
            QMessageBox.information(self, '提示', '请选择分类：状态或波形', QMessageBox.Ok)
            return

    def getSelectAlgorithmInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.algorithm_set = REPData[2]
                self.curPageMax_al=REPData[3]
                self.import_view.init_algorithm(self.algorithm_set, self.curPageIndex_al,self.curPageMax_al)
                self.import_view.algorithm.ui.btnSelect1.clicked.connect(
                    lambda: self.on_clicked_select_algorithm(pageIndex=1))
                self.import_view.algorithm.ui.tableWidget_algorithm.setSelectionBehavior(QAbstractItemView.SelectRows)#选整行
                self.import_view.algorithm.control_signal_al.connect(self.page_controller_al)
                self.import_view.algorithm.show()
                self.import_view.algorithm.ui.tableWidget_algorithm.clicked.connect(self.on_clicked_algorithm_view_item)
                self.import_view.ui.pushButton_algorithm_select.setEnabled(True)
            elif REPData[0] =='2':
                QMessageBox.information(self, '提示', '没有对应的算法', QMessageBox.Ok)
                self.import_view.ui.pushButton_algorithm_select.setEnabled(True)
            else:
                QMessageBox.information(self, '提示', '获取算法信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('getSelectAlgorithmInfo', e)
    #     # 响应函数，获取用户选择的算法信息，并关闭页面
    def on_clicked_algorithm_view_item(self):
        item_row = self.import_view.algorithm.ui.tableWidget_algorithm.currentRow()
        self.algorithm = None
        if self.search_alg_page_info!=None:
            self.algorithm = self.search_alg_info[item_row]
        else:
            self.algorithm = self.algorithm_set[item_row]
        print(1 and self.algorithm)
        print(self.import_view.algorithm.ui.tableWidget_algorithm)
        algorithm_name = self.algorithm[1]
        _translate = QtCore.QCoreApplication.translate
        self.import_view.ui.label_algorithm_name.setText(_translate("model_import",
                                                "<html><head/><body><p><span style=\" font-size:12pt;\">模型算法：" + algorithm_name + "</span></p></body></html>"))
        self.import_view.algorithm.close()
    def page_controller_al(self, signal):
        if "home" == signal[0]:
            if self.curPageIndex_al == 1:
                QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                return
            self.curPageIndex_al = 1
            self.import_view.algorithm.curPage.setText(str(self.curPageIndex_al))
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            if self.curPageIndex_al <= 1:
                return
            self.curPageIndex_al = self.curPageIndex_al - 1
            self.import_view.algorithm.curPage.setText(str(self.curPageIndex_al))
        elif "next" == signal[0]:
            if self.curPageMax_al == int(signal[1]) or self.search_alg_page_info == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.curPageIndex_al = self.curPageIndex_al + 1
            self.import_view.algorithm.curPage.setText(str(self.curPageIndex_al))
        elif "final" == signal[0]:
            if self.curPageIndex_al == self.curPageMax_al or self.search_alg_page_info == self.curPageIndex_al:
                QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                return
            if self.search_alg_page_info!=None:
                self.curPageIndex_al=self.search_alg_page_info
            else:
                self.curPageIndex_al = self.curPageMax_al
            self.import_view.algorithm.curPage.setText(str(self.curPageIndex_al))
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
            if self.import_view.algorithm.ui.lineValue.text() != '' and self.import_view.algorithm.ui.btnSelect1.text() =='取消查询':
                if self.search_alg_page_info < int(signal[1]) or int(signal[1]) <= 0:
                    QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                    return
            self.curPageIndex_al = int(signal[1])
            self.import_view.algorithm.curPage.setText(signal[1])

        if self.import_view.ui.checkbox1.isChecked():
            msg = [self.curPageIndex_al, self.pageRows, signal[0],'state']
        else:
            msg = [self.curPageIndex_al, self.pageRows, signal[0],'waveform']
        if self.import_view.algorithm.ui.lineValue.text() != '':
            self.alg_is_search=True
            self.on_clicked_select_algorithm(pageIndex=self.curPageIndex_al)
        else:
            self.client.classifierPaging_al(msg)

    def classifierPaging_alRes(self,REPData):
        try:
            if REPData[0] == '1':
                self.algorithm_set = REPData[2]
                self.import_view.algorithm.ui.tableWidget_algorithm.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.import_view.algorithm.ui.tableWidget_algorithm.clear()
                self.import_view.algorithm.update_table(self.algorithm_set,self.curPageIndex_al)
            else:
                QMessageBox.information(self, '提示', '算法信息翻页失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('getSelectAlgorithmInfo1', e)
    def inquiryCls_alg_InfoRes(self,REPData):
        try:
            if REPData[0] == '1':
                if REPData[2][1]==[]:
                    QMessageBox.information(self, '提示', '没有匹配的算法，请点击取消查询重新搜索', QMessageBox.Ok)
                self.search_alg_info = REPData[2][1]
                self.search_alg_page_info=REPData[2][0]#总页数
                self.import_view.algorithm.ui.tableWidget_algorithm.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.import_view.algorithm.ui.tableWidget_algorithm.clear()
                self.import_view.algorithm.update_table(self.search_alg_info,self.curPageIndex_al,self.search_alg_page_info)

            else:
                QMessageBox.information(self, '提示', '查询算法信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('inquiryClassifierInfoRes', e)
    def on_clicked_select_algorithm(self,pageIndex):
        try:
            if self.tempt_alg_CurpageIndex ==None:
                self.tempt_alg_CurpageIndex=self.curPageIndex_al
            self.curPageIndex_al=pageIndex
            key_value = self.import_view.algorithm.ui.lineValue.text()
            if key_value == '':
                QMessageBox.information(self, '提示', '请输入要搜索的算法信息', QMessageBox.Ok)
                return
            if self.import_view.ui.checkbox1.isChecked():
                REQmsg = [key_value,pageIndex,self.pageRows,'state']
            else:
                REQmsg = [key_value, pageIndex, self.pageRows,'waveform']
            if self.import_view.algorithm.ui.btnSelect1.text() == "查询":
                self.import_view.algorithm.ui.btnSelect1.setText("取消查询")
                self.client.inquiryCls_alg_Info(REQmsg)
            elif self.alg_is_search==True:
                self.alg_is_search=False
                self.client.inquiryCls_alg_Info(REQmsg)
            elif self.import_view.algorithm.ui.btnSelect1.text() == "取消查询":
                self.import_view.algorithm.ui.tableWidget_algorithm.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.import_view.algorithm.ui.tableWidget_algorithm.clear()
                self.curPageIndex_al=self.tempt_alg_CurpageIndex
                self.import_view.algorithm.update_table(self.algorithm_set,self.curPageIndex_al,self.curPageMax_al)
                self.import_view.algorithm.ui.btnSelect1.setText("查询")
                self.tempt_alg_CurpageIndex=None
                self.search_alg_page_info=None
                self.import_view.algorithm.ui.lineValue.clear()

        except Exception as e:
            print('on_clicked_select_algorithm', e)
    #数据集选择
    def on_clicked_pushButton_set_select(self):
        if self.import_view.ui.checkbox1.isChecked() or self.import_view.ui.checkbox2.isChecked():
            self.search_set_page_info = None
            self.import_view.ui.pushButton_set_select.setEnabled(False)
            if self.import_view.ui.checkbox1.isChecked():
                self.client.getSelectSetInfo([self.curPageIndex_set, self.pageRows,'state'])
            else:
                self.client.getSelectSetInfo([self.curPageIndex_set, self.pageRows,'wave'])

        else:
            QMessageBox.information(self, '提示', '请选择分类：状态或波形', QMessageBox.Ok)
        return
    def getSelectSetInfoRes(self,REPData):
        try:
            if REPData[0] == '1':
                self.dataSet = REPData[2]
                self.curPageMax_set=REPData[3]
                self.import_view.init_set(self.dataSet,self.curPageIndex_set,self.curPageMax_set)
                self.import_view.set.ui.tableWidget_set.setSelectionBehavior(QAbstractItemView.SelectRows)

                self.import_view.set.ui.btnSelect1.clicked.connect(
                    lambda: self.on_clicked_select_set(pageIndex=1))
                self.import_view.set.ui.tableWidget_set.setSelectionBehavior(
                    QAbstractItemView.SelectRows)  # 选整行
                self.import_view.set.control_signal_set.connect(self.page_controller_set)
                self.import_view.set.show()
                self.import_view.set.ui.tableWidget_set.clicked.connect(self.on_clicked_set_view_item)
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

    def on_clicked_set_view_item(self):
        item_row = self.import_view.set.ui.tableWidget_set.currentRow()
        self.set = None
        if self.search_set_page_info != None:
            self.set = self.search_set_info[item_row]
        else:
            self.set = self.dataSet[item_row]
        print(1 and self.set)
        print(self.import_view.set.ui.tableWidget_set)
        algorithm_name = self.set[1]
        _translate = QtCore.QCoreApplication.translate
        self.import_view.ui.label_set_name.setText(_translate("model_import",
                                                                        "<html><head/><body><p><span style=\" font-size:12pt;\">数据集：" + algorithm_name + "</span></p></body></html>"))
        self.import_view.set.close()
    def classifierPaging_setRes(self,REPData):
        try:
            if REPData[0] == '1':
                self.dataSet = REPData[2]
                self.import_view.set.ui.tableWidget_set.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.import_view.set.ui.tableWidget_set.clear()
                self.import_view.set.update_table(self.dataSet,self.curPageIndex_set)
            else:
                QMessageBox.information(self, '提示', '数据集信息翻页失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('classifierPaging_setRes', e)
    def inquiryCls_set_InfoRes(self,REPData):
        try:
            if REPData[0] == '1':
                if REPData[2][1]==[]:
                    QMessageBox.information(self, '提示', '没有匹配的数据集，请点击取消查询重新搜索', QMessageBox.Ok)
                self.search_set_info = REPData[2][1]
                self.search_set_page_info=REPData[2][0]#总页数
                self.import_view.set.ui.tableWidget_set.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.import_view.set.ui.tableWidget_set.clear()
                self.import_view.set.update_table(self.search_set_info, self.curPageIndex_set,self.search_set_page_info)
            else:
                QMessageBox.information(self, '提示', '查询数据集信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('inquiryCls_set_InfoRes', e)
    def on_clicked_select_set(self,pageIndex):
        try:
            if self.tempt_set_CurpageIndex ==None:
                self.tempt_set_CurpageIndex=self.curPageIndex_set
            self.curPageIndex_set=pageIndex
            key_value = self.import_view.set.ui.lineValue.text()
            if key_value == '':
                QMessageBox.information(self, '提示', '请输入要搜索的数据集信息', QMessageBox.Ok)
                return
            if self.import_view.ui.checkbox1.isChecked():
                REQmsg = [key_value,pageIndex,self.pageRows,'state']
            else:
                REQmsg = [key_value, pageIndex, self.pageRows,'wave']
            if self.import_view.set.ui.btnSelect1.text() == "查询":
                self.import_view.set.ui.btnSelect1.setText("取消查询")
                self.client.inquiryCls_set_Info(REQmsg)
            elif self.set_is_search==True:
                self.set_is_search=False
                self.client.inquiryCls_set_Info(REQmsg)
            elif self.import_view.set.ui.btnSelect1.text() == "取消查询":
                self.import_view.set.ui.tableWidget_set.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.import_view.set.ui.tableWidget_set.clear()
                self.curPageIndex_set=self.tempt_set_CurpageIndex
                self.import_view.set.update_table(self.dataSet,self.curPageIndex_set,self.curPageMax_set)
                self.import_view.set.ui.btnSelect1.setText("查询")
                self.tempt_set_CurpageIndex=None
                self.search_set_page_info=None
                self.import_view.set.ui.lineValue.clear()
        except Exception as e:
            print('on_clicked_select_set', e)

    def page_controller_set(self, signal):
        if "home" == signal[0]:
            if self.curPageIndex_set == 1:
                QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                return
            self.curPageIndex_set = 1
            self.import_view.set.curPage.setText(str(self.curPageIndex_set))
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            if self.curPageIndex_set <= 1:
                return
            self.curPageIndex_set = self.curPageIndex_set - 1
            self.import_view.set.curPage.setText(str(self.curPageIndex_set))
        elif "next" == signal[0]:
            if self.curPageMax_set == int(signal[1]) or self.search_set_page_info == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.curPageIndex_set = self.curPageIndex_set + 1
            self.import_view.set.curPage.setText(str(self.curPageIndex_set))
        elif "final" == signal[0]:
            if self.curPageIndex_set == self.curPageMax_set or self.search_set_page_info == self.curPageIndex_set:
                QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                return
            if self.search_set_page_info!=None:
                self.curPageIndex_set =self.search_set_page_info
            else:
                self.curPageIndex_set = self.curPageMax_set
            self.import_view.set.curPage.setText(str(self.curPageIndex_set))
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
            if self.import_view.set.ui.lineValue.text() != '':
                if self.search_set_page_info < int(signal[1]) or int(signal[1]) <= 0:
                    QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                    return
            self.curPageIndex_set = int(signal[1])
            self.import_view.set.curPage.setText(signal[1])

        if self.import_view.ui.checkbox1.isChecked():
            msg = [self.curPageIndex_set, self.pageRows,signal[0],'state']
        else:
            msg = [self.curPageIndex_set, self.pageRows,signal[0],'wave']
        if self.import_view.set.ui.lineValue.text() != '':
            self.set_is_search=True
            self.on_clicked_select_set(pageIndex=self.curPageIndex_set)
        else:
            self.client.classifierPaging_set(msg)


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

    def on_btnDel_clicked(self):
        reply=QMessageBox.warning(
                self.view, '确认删除！', '您将进行删除操作！',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == 16384:
            selected_rows = self.view.table.selectionModel().selectedRows()
            if selected_rows:
                selected_row = selected_rows[0].row()
                row_content = []
                for column in range(self.view.table.columnCount()):
                    item = self.view.table.item(selected_row, column)
                    if item:
                        row_content.append(item.text())

                self.client.delClassifierInfo([row_content, selected_row, self.curPageIndex])
            else:
                QMessageBox.information(self.view, ' ', '请先选中一行')
                return
        else:
            return

    def on_clicked_configOptions_select(self):
        self.configView=clsPrentryView()
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
        self.client.checkstateRessig.disconnect()
        self.client.model_transmit_messageRessig.disconnect()
        self.client.classifier_id_inquiryRessig.disconnect()
        self.client.classifierPagingResSig.disconnect()
        self.client.classifierPaging_alResSig.disconnect()
        self.client.inquiryCls_alg_InfoRessig.disconnect()
        self.client.getClassifier_configRessig.disconnect()
        self.client.upload_schemeResSig.disconnect()
        self.client.upload_modelResSig.disconnect()