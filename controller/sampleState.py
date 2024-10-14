#!/usr/bin/python
# author bluenor
from view.sampleState import sampleStateView
from view.sampleState_form.secTable_form.form import sectableView
from view.sampleState import QComboCheckBox
from PyQt5 import QtWidgets
from PyQt5.Qt import *
import re, sys


class sampleStateController(QWidget):
    def __init__(self, client, cAppUtil):
        super().__init__()
        self.client = client
        self.cAppUtil = cAppUtil
        self.view = sampleStateView()
        # 二级表视图
        self.secView = None
        # 所有已在样本集/标注集中存在的标注类型列表
        self.type_list = list()
        self.client.getSpecificInfoResSig.connect(self.getSpecificInfoRes)
        self.client.getSpecificNumResSig.connect(self.getSpecificNumRes)
        self.client.getSpecificDetailResSig.connect(self.getSpecificDetailRes)
        self.client.getSpecNumFromFltResSig.connect(self.getSpecNumFromFltRes)
        # 数据初始化
        self.client.getSpecificInfo([])

        # 当前选中的表格行
        self.selectedRow = ''

    def exit(self):
        self.client.getSpecificInfoResSig.disconnect()
        self.client.getSpecificNumResSig.disconnect()
        self.client.getSpecificDetailResSig.disconnect()
        self.client.getSpecNumFromFltResSig.disconnect()

    def getSpecificInfoRes(self, specificInfo):
        try:
            print(f'getSpecificInfoRes: {specificInfo}')
            self.type_info = [typeInfo[1] for typeInfo in specificInfo]
            # 初始化视图
            self.view.ui.comboBox_1 = QComboCheckBox(self.type_info, default_check=False, is_research=True)
            self.view.ui.init_view(self.getTypeDetail, self.setSelectedRow, self.getSpecificNum)
        except Exception as e:
            print('getSpecificInfoRes', e)

    # 根据数据源搜索
    def getSpecificNum(self):
        try:
            source = self.view.ui.comboBox_2.currentText()
            if source == '':
                QMessageBox.information(self, '提示', '尚未选择数据来源')
                return
            type = [i.text() for i in self.view.ui.comboBox_1.get_selected()]
            self.type = type
            if len(type) == 0:
                QMessageBox.information(self, '提示', '尚未选择任何标注类型')
                return
            type_sql = ''
            if len(type) == 1:
                type_sql = "type_name = '{}'".format(type[0])
            elif len(type) > 1:
                type_sql = "type_name in {}".format(tuple(type))

            print(f'type_sql: {type_sql}')
            if source == '诊断标注':
                self.client.getSpecificNum(['sample_info', type_sql, False])
            elif source == '科研标注':
                self.client.getSpecificNum(['resLab', type_sql, False])
            # elif source == '自动标注':
            #     self.client.getSpecificNum(['label_info', type_sql, False])
            # elif source == '评估标注':
            #     self.client.getSpecificNum(['label_info', type_sql, True])
            self.view.ui.tableWideget.horizontalHeader().setVisible(True)
        except Exception as e:
            print('search_by_source_type', e)

    def getSpecificNumRes(self, typeInfo):
        print(f'searchSourceRes: {typeInfo}')
        typeList = [j[0] for j in typeInfo]
        for i in self.type:
            if i not in typeList:
                typeInfo.append((i, 0))
        self.view.ui.tableWideget.horizontalHeader().setVisible(True)
        self.view.ui.init_table(typeInfo)

    def getSpecificDetailRes(self, data):
        try:
            print(f'getSpecificDetailRes: {data}')
            self.patient_name = data['patientName']
            self.measure_date = [d.strftime("%Y-%m-%d") for d in data['measureDate']]
            self.file_name = data['fileName']
            self.user = data['user']
            self.montage = data['montage']
            if 'typeModel' in data.values():
                self.type_model = data['typeModel']

            if self.data_source == '诊断标注':
                self.secView = sectableView(data_source=self.data_source, type_name=self.type_name,
                                            patient_name=self.patient_name, measure_date=self.measure_date,
                                            file_name=self.file_name,
                                            montage=self.montage, type_user=self.user)
            elif self.data_source == '科研标注':
                self.secView = sectableView(data_source=self.data_source, type_name=self.type_name,
                                            patient_name=self.patient_name, measure_date=self.measure_date,
                                            file_name=self.file_name,
                                            montage=self.montage, type_user=self.user)
            # elif self.data_source == '自动标注':
            #     self.secView = sectableView(data_source=self.data_source, type_name=self.type_name,
            #                                 patient_name=self.patient_name, measure_date=self.measure_date,
            #                                 file_name=self.file_name,
            #                                 montage=self.montage, type_model=self.type_model, type_user=self.user)
            #
            # elif self.data_source == '评估标注':
            #     self.secView = sectableView(data_source=self.data_source, type_name=self.type_name,
            #                                 patient_name=self.patient_name, measure_date=self.measure_date,
            #                                 file_name=self.file_name,
            #                                 montage=self.montage, type_model=self.type_model, type_user=self.user,
            #                                 mtype_name=self.type_info)

            # 子窗口打开时阻塞父窗口
            # self.secView.setWindowModality(Qt.ApplicationModal)
            self.secView.show()
            self.secView.comboBox_1.activated.connect(self.initFilter_by_selected)
        except Exception as e:
            print('getSpecificDetailRes', e)

    # 设置选中的行数
    def setSelectedRow(self, item):
        self.selectedRow = item.row()

    # 查看选中标注类型的详细统计数据
    def getTypeDetail(self):
        if self.selectedRow == '':
            QMessageBox.information(self, '提示', '请先选中要查看的行')
            return

        try:
            data_source = self.view.ui.comboBox_2.currentText()
            self.data_source = data_source
            print(f'self.data_source: {self.data_source}')
            type_name = self.view.ui.tableWideget.item(self.selectedRow, 0).text()
            self.type_name = type_name
            type_num = int(self.view.ui.tableWideget.item(self.selectedRow, 1).text())
        except:
            QMessageBox.information(self, '提示', '请先选择要显示的波形')
            return

        if type_num == 0:
            QMessageBox.information(self, '提示', '要明细的标注类型数量为0，无法查看')
            return

        # 根据选择的标注类型对其他数据进行初始化
        msg = {}
        if data_source == '诊断标注':
            left_name = 'sample_info'
            type_s = 'type_id'
            msg['patientName'] = ["CONCAT(a.patient_id, '-', a.name)", 'patient_info',
                                  f"Join check_info AS ci ON a.patient_id = ci.patient_id "
                                  f"Join {left_name} as b on ci.check_id = b.check_id", f"b.{type_s} = c.type_id",
                                  type_name, '', False]
            msg['measureDate'] = ["a.measure_date", 'check_info',
                                  f'JOIN {left_name} as si on si.check_id = a.check_id',
                                  f"si.{type_s} = c.type_id", type_name, '', False]
            msg['fileName'] = ["a.check_number", 'check_info',
                               f'JOIN {left_name} as si on si.check_id = a.check_id',
                               f"si.{type_s} = c.type_id", type_name, '', False]
            msg['user'] = ["account", 'user_info', f"left join {left_name} as b on a.uid = b.uid",
                           f"b.{type_s} = c.type_id", type_name, '', False]
            msg['montage'] = ["a.channel", left_name, '', f"a.{type_s} = c.type_id", type_name, '', False]
        elif data_source == '科研标注':
            left_name = 'resLab'
            type_s = 'type_id'
            # 通过数据来源和标注类型搜索
            msg['patientName'] = ["CONCAT(a.patient_id, '-', a.name)", 'patient_info',
                                  f"Join check_info AS ci ON a.patient_id = ci.patient_id "
                                  f"Join task as b on ci.check_id = b.check_id "
                                  f"Join {left_name} as z on b.theme_id = z.theme_id ",
                                  f"z.{type_s} = c.type_id",
                                  type_name, '', False]
            msg['measureDate'] = ["a.measure_date", 'check_info',
                                  f'JOIN task as si on si.check_id = a.check_id '
                                  f'JOIN {left_name} as z on si.theme_id = z.theme_id ',
                                  f"z.{type_s} = c.type_id", type_name, '', False]
            msg['fileName'] = ["a.check_number", 'check_info',
                               f'JOIN task as si on si.check_id = a.check_id '
                               f'JOIN {left_name} as z on si.theme_id = z.theme_id',
                               f"z.{type_s} = c.type_id", type_name, '', False]
            msg['user'] = ["account", 'user_info', f"left join {left_name} as b on a.uid = b.uid",
                           f"b.{type_s} = c.type_id", type_name, '', False]
            msg['montage'] = ["a.channel", left_name, '', f"a.{type_s} = c.type_id", type_name, '', False]
        else:
            left_name = 'label_info'
            type_s = 'mtype_id'
            msg['typeModel'] = ["CONCAT(a.classifier_id, '-', a.classifier_name)", 'classifier',
                                "left join {} as b on a.classifier_id = b.mid".format(left_name),
                                "b.{} = c.type_id".format(type_s), type_name, '', False]
            # 通过数据来源和标注类型搜索
            msg['patientName'] = ["CONCAT(a.patient_id, '-', a.name)", 'patient_info',
                                  f"Join check_info AS ci ON a.patient_id = ci.patient_id "
                                  f"Join {left_name} as b on ci.check_id = b.check_id", f"b.{type_s} = c.type_id",
                                  type_name, '', False]
            msg['measureDate'] = ["a.measure_date", 'check_info',
                                  f'JOIN {left_name} as si on si.check_id = a.check_id',
                                  f"si.{type_s} = c.type_id", type_name, '', False]
            msg['fileName'] = ["a.check_number", 'check_info',
                               f'JOIN {left_name} as si on si.check_id = a.check_id',
                               f"si.{type_s} = c.type_id", type_name, '', False]
            msg['user'] = ["account", 'user_info', f"left join {left_name} as b on a.uid = b.uid",
                           f"b.{type_s} = c.type_id", type_name, '', False]
            msg['montage'] = ["a.channel", left_name, '', f"a.{type_s} = c.type_id", type_name, '', False]
        self.client.getSpecificDetail([msg])

    # 初始化二级表的过滤器组合
    def initFilter_by_selected(self):
        try:
            filters = self.secView.comboBox_1.get_selected()
            self.is_evaluate = False
            print('test')

            if len(filters) > 3:
                QMessageBox.information(self, '提示', '筛选条件不得超过3个')
                self.secView.comboBox_1.select_clear()
                self.secView.comboBox_1.select_texts(texts=self.secView.filters_text)
                return
            self.secView.filters_text = [i.text() for i in filters]
            # print(self.secView.filters_text)
            # 清空上次的布局
            self.clear()
            self.secView.col_label = []
            font = QFont()
            font.setPointSize(12)
            j = 0
            search_col = []
            for i in filters:
                # print(j)
                text = i.text()
                tool_bar = []
                if text == '病人姓名':
                    tool_bar = self.secView.patient_name
                    search_col.append('patient_id')
                elif text == '测量日期':
                    tool_bar = self.secView.measure_date
                    search_col.append('measure_date')
                elif text == '文件名':
                    tool_bar = self.secView.file_name
                    search_col.append('check_number')
                elif text == '导联':
                    tool_bar = self.secView.montage
                    search_col.append('channel')
                elif text == '标注用户':
                    tool_bar = self.secView.type_user
                    search_col.append('account')
                elif text == '标注模型':
                    tool_bar = self.secView.type_model
                    search_col.append('mid')
                elif text == '模型标注类型':
                    tool_bar = self.secView.mtype_name
                    search_col.append('type_name')
                elif text == '评估结果':
                    self.is_evaluate = True
                    tool_bar = self.secView.evaluate_result
                    search_col.append('tag')

                self.secView.label = QLabel(text + ':')
                self.secView.label.setFont(font)
                self.secView.spaceItem = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                     QtWidgets.QSizePolicy.Minimum)
                if text != '评估结果':
                    exec(
                        "self.secView.comboBox_{} = QComboCheckBox(tool_bar, default_check=False, is_research=True)".format(
                            j + 2))
                else:
                    exec("self.secView.comboBox_{} = QComboBox()".format(j + 2))
                    exec("self.secView.comboBox_{}.addItems(tool_bar)".format(j + 2))
                    exec("self.secView.comboBox_{}.setCurrentIndex(-1)".format(j + 2))
                    font1 = QFont()
                    font1.setPointSize(12)
                    exec("self.secView.comboBox_{}.setFont(font1)".format(j + 2))

                self.secView.horizontalLayout_1.addWidget(self.secView.label)
                exec("self.secView.horizontalLayout_1.addWidget(self.secView.comboBox_{})".format(j + 2))
                self.secView.horizontalLayout_1.addItem(self.secView.spaceItem)
                if j == len(filters) - 1:
                    filter_button = QPushButton('筛选')
                    filter_button.setFont(QFont(font))
                    filter_button.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                                "color: rgb(255, 255, 255);")
                    self.secView.spaceItem = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                         QtWidgets.QSizePolicy.Minimum)
                    self.secView.horizontalLayout_1.addWidget(filter_button)
                    self.secView.horizontalLayout_1.addItem(self.secView.spaceItem)
                    filter_button.clicked.connect(
                        lambda: self.search_with_filter(len(filters), search_col))
                j += 1

            exec("self.secView.horizontalLayout_1.setStretch({},7)".format(3 * len(filters) + 1))
        except Exception as e:
            print('initFilter_by_selected', e)

    # 通过过滤器组合搜索结果
    def search_with_filter(self, filter_num, search_col):
        search_values = []
        for i in range(filter_num):
            if self.is_evaluate and i == filter_num - 1:
                temp_list = eval("self.secView.comboBox_{}.currentText()".format(i + 2))
            else:
                temp_list = eval("[j.text() for j in self.secView.comboBox_{}.get_selected()]".format(i + 2))
            if len(temp_list) == 0:
                QMessageBox.information(self, '提示', '存在未选择的过滤器')
                return
            if search_col[i] == 'patient_id' or search_col[i] == 'mid':
                j = 0
                while j < len(temp_list):
                    r = re.match(r"\d+", temp_list[j])
                    temp_list[j] = int(r.group())
                    j += 1
            search_values.append(temp_list)
        search_table = None
        self.isFromEvaluate = False
        if self.secView.data_source == '诊断标注':
            search_table = 'sample_info'
        elif self.secView.data_source == '科研标注':
            search_table = 'resLab'
        elif self.secView.data_source == '自动标注' or '评估标注':
            search_table = 'label_info'
            if self.secView.data_source == '评估标注':
                self.isFromEvaluate = True

        self.client.getSpecNumFromFlt([self.secView.type_name, search_col, search_values, search_table,
                                       self.isFromEvaluate])

    def getSpecNumFromFltRes(self, sample_detail):
        try:
            print(f'getSpecNumFromFltRes: {sample_detail}')
            if len(sample_detail) == 0:
                QMessageBox.information(self, '提示', '筛选结果为空')
                return
            self.secView.init_table(sample_detail, tag=self.is_evaluate)
        except Exception as e:
            print('getSpecNumFromFltRes', e)

    # 清理布局
    def clear(self):
        item_list = list(range(self.secView.horizontalLayout_1.count()))
        item_list.reverse()
        # print(item_list)
        for i in item_list:
            item = self.secView.horizontalLayout_1.itemAt(i)
            self.secView.horizontalLayout_1.removeItem(item)
            if item.widget():
                item.widget().deleteLater()