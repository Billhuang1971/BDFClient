import sys

import numpy as np

from view.auto_form.auto import Ui_AutoForm
from view.auto_form.prentry import Ui_Prentry
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import QApplication, QMessageBox

class AutoView(QWidget):
    signal_file_info_montage_setting_save = pyqtSignal(list)
    signal_file_montage_update = pyqtSignal(bool)
    page_control_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AutoForm()
        self.ui.setupUi(self)
        self.selected_montage_name = 'Default'
        self.montage_list = None
        self.file_header = ['配置方案', '脑电数据名称']
        self.file_field = ['if_select_finished', 'file_name']
        self.classifier_header = ['分类器名称', '算法类型']
        self.classifier_field = ['classifier_name', 'alg_type']
        # self.file_included_channels = ['O1-REF','O2-REF'....]
        self.file_included_channels = None
        #self.file_included_channel_list = set('O1', 'O2', 'REF', 'AV'.....)
        # 手动添加全平均通道
        self.file_included_channel_list = set(['AV'])
        # selected_file_info 当前选中脑电文件的配置信息[montage_name, file_name, selected_channel_list]
        self.selected_file_info = None
        self.ui.addchannel_pushButton.clicked.connect(self.on_clicked_addchannel_pushButton)
        self.ui.allAddchannel_pushButton.clicked.connect(self.on_clicked_allAddchannel_pushButton)
        self.ui.delchannel_pushButton.clicked.connect(self.on_clicked_delchannel_pushButton)
        self.ui.moveup_pushButton.clicked.connect(self.on_clicked_moveup_pushButton)
        self.ui.movedown_pushButton.clicked.connect(self.on_clicked_movedown_pushButton)
        self.ui.save_file_montage_setting_pushButton.clicked.connect(
            self.on_clicked_save_file_montage_setting_pushButton)
        self.ui.montage_comboBox.currentIndexChanged.connect(self.currentIndexChanged_montage_comboBox)
        self.set_enabel_state_montage_setting_buttons(False)
        self.ui.pushButton_6.clicked.connect(self.__home_page)
        self.ui.pushButton_7.clicked.connect(self.__pre_page)
        self.ui.pushButton_8.clicked.connect(self.__next_page)
        self.ui.pushButton_9.clicked.connect(self.__final_page)
        self.ui.pushButton_10.clicked.connect(self.__confirm_skip)

    def reject(self):
        pass

    def init_file_table(self, data):
        col_num = len(self.file_header)
        row_num = 0
        if data:
            row_num = len(data)
        self.ui.tableWidgetFile.setColumnCount(col_num)
        self.ui.tableWidgetFile.setRowCount(row_num)
        for i in range(col_num):
            header_item = QTableWidgetItem(self.file_header[i])
            font = header_item.font()
            font.setPointSize(16)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            header_item.setData(Qt.UserRole, self.file_field[i])
            self.ui.tableWidgetFile.setHorizontalHeaderItem(i, header_item)
            # 拉伸表格列项，使其铺满
            self.ui.tableWidgetFile.horizontalHeader().setStretchLastSection(True)
        for r in range(row_num):
            for c in range(col_num):
                if c == 0:
                    self.item = QTableWidgetItem(str(data[r][c]))
                else:
                    self.item = QTableWidgetItem(str(data[r][c][1]))
                self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = self.item.font()
                font.setPointSize(10)
                self.item.setFont(font)
                self.ui.tableWidgetFile.setItem(r, c, self.item)
        # self.init_comboCond()
        self.ui.tableWidgetFile.horizontalHeader().setHighlightSections(False)
        #   按字段长度进行填充
        self.ui.tableWidgetFile.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # 增加和查询的时候列数会改变，所以需要保存原来的列数
        self.col = self.ui.tableWidgetFile.columnCount()
        # 点击就选中整行
        self.ui.tableWidgetFile.setSelectionBehavior(QAbstractItemView.SelectRows)

    # 初始化分类器
    def init_classifier_table(self, data):
        col_num = len(self.classifier_header)
        row_num = len(data)
        if data:
            data = np.delete(data, [0, 3, 2, 4], axis=1)
        print(data)
        self.ui.tableWidgetClassifierScan.setColumnCount(col_num)
        self.ui.tableWidgetClassifierScan.setRowCount(row_num)
        for i in range(col_num):
            header_item = QTableWidgetItem(self.classifier_header[i])
            font = header_item.font()
            font.setPointSize(16)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            header_item.setData(Qt.UserRole, self.classifier_field[i])
            self.ui.tableWidgetClassifierScan.setHorizontalHeaderItem(i, header_item)
            # 拉伸表格列项，使其铺满
        self.ui.tableWidgetClassifierScan.horizontalHeader().setStretchLastSection(True)

        for r in range(row_num):
            for c in range(col_num - 1):
                self.item = QTableWidgetItem(str(data[r][c]))
                self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = self.item.font()
                font.setPointSize(10)
                self.item.setFont(font)
                self.ui.tableWidgetClassifierScan.setItem(r, c, self.item)
            self.item = QTableWidgetItem(str(data[r][10]))
            self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            font = self.item.font()
            font.setPointSize(10)
            self.item.setFont(font)
            self.ui.tableWidgetClassifierScan.setItem(r, col_num - 1, self.item)
        # self.init_comboCond()
        self.ui.tableWidgetClassifierScan.horizontalHeader().setHighlightSections(False)
        #   按字段长度进行填充
        self.ui.tableWidgetClassifierScan.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # 增加和查询的时候列数会改变，所以需要保存原来的列数
        self.col = self.ui.tableWidgetClassifierScan.columnCount()
        # 点击就选中整行
        self.ui.tableWidgetClassifierScan.setSelectionBehavior(QAbstractItemView.SelectRows)

    # 初始化参考方案下拉列表
    #montage_name_list参考方案名称列表，montage参考方案详细列表包括name，channels       file_included_channels当前选择的脑电文件中包含的通道名称列表
    #selected_file_info 当前选中脑电文件的配置信息[montage_name, file_name, selected_channel_list]
    def init_file_montage_setting_view(self,montage_name_list, montage_list, file_included_channels, selected_file_info):
        try:
            # 启用相关按钮
            self.set_enabel_state_montage_setting_buttons(True)
            self.file_included_channels = file_included_channels
            self.file_included_channel_list = set(['AV'])
            ch_tmp = set()
            for ch in file_included_channels:
                ch = ch.split('-')
                ch_tmp.add(ch[0])
                ch_tmp.add(ch[1])
            for ch in ch_tmp:
                self.file_included_channel_list.add(ch)
            self.montage_list = montage_list
            self.selected_file_info = selected_file_info
            self.montage_names_list = montage_name_list
            if 'Default' not in self.montage_names_list:
                self.montage_names_list.insert(0, 'Default')
            self.ui.montage_comboBox.addItems(self.montage_names_list)
            self.selected_montage_name = 'Default'
            self.ui.montage_comboBox.setCurrentIndex(0)
            for i in range(len(self.montage_names_list)):
                if self.montage_names_list[i] == self.selected_file_info[0]:
                    self.ui.montage_comboBox.setCurrentIndex(i)
            # 设置未选通道列表
            self.set_unselected_channel_list()
            # 设置已选用通道列表
            self.set_selected_channel_list()
        except Exception as e:
            print('init_file_montage_setting_view', e)

    def currentIndexChanged_montage_comboBox(self):
        self.selected_montage_name = self.ui.montage_comboBox.currentText()
        self.set_selected_channel_list()
        self.set_unselected_channel_list()

    def set_selected_filename(self, name):
        self.ui.label_filename.setText('当前已选择脑电文件:{}'.format(name))

    def set_unselected_channel_list(self):
        try:
            # 清空所有项
            self.ui.unselected_listWidget.clear()
            if self.selected_montage_name == 'Default':
                unselected_channels = self.get_unselected_channel_list(self.file_included_channels,
                                                                       self.selected_file_info[2])
                for us_ch in unselected_channels:
                    item = QListWidgetItem(us_ch)
                    self.ui.unselected_listWidget.addItem(item)
            else:
                for montage in self.montage_list:
                    if montage['name'] == self.selected_montage_name:
                        montage_channel_list = montage['channels']
                        unselected_channels = self.get_unselected_channel_list(montage_channel_list,
                                                                               self.selected_file_info[2])
                        for us_ch in unselected_channels:
                            item = QListWidgetItem(us_ch)
                            if self.if_add_channel_availabel(us_ch):
                                self.ui.unselected_listWidget.addItem(us_ch)
                            else:
                                item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                                item.setForeground(QColor("red"))
                                self.ui.unselected_listWidget.addItem(item)
        except Exception as e:
            print('set_unselected_channel_list', e)

    def set_selected_channel_list(self):
        try:
            self.ui.selected_listWidget.clear()
            if self.selected_file_info[0] == self.selected_montage_name:
                selected_channel_list = self.selected_file_info[2]
                if len(selected_channel_list)>0:
                    for s_ch in selected_channel_list:
                        item = QListWidgetItem(s_ch)
                        self.ui.selected_listWidget.addItem(item)
        except Exception as e:
            print('set_selected_channel_list', e)

    def get_unselected_channel_list(self, montage_channels, selected_channels):
        # unselected_channels = [x for x in motage_channels if x not in selected_channels]
        unselected_channels = [x for x in montage_channels]
        return unselected_channels

    def get_selected_channel_list_from_listwidget(self):
        channel_list = []
        return channel_list

    def on_clicked_addchannel_pushButton(self):
        self.signal_file_montage_update.emit(True)
        for item in self.ui.unselected_listWidget.selectedItems():
            # 检查该项是否已经存在于列表2中
            if not self.ui.selected_listWidget.findItems(item.text(), Qt.MatchExactly):
                self.ui.selected_listWidget.addItem(item.text())

    def on_clicked_allAddchannel_pushButton(self):
        self.signal_file_montage_update.emit(True)
        items = []
        for i in range(self.ui.unselected_listWidget.count()):
            items.append(self.ui.unselected_listWidget.item(i).text())
        for item in items:
            # 判断是否可选，在判断是否已经选择过了
            if self.if_add_channel_availabel(item) and not self.ui.selected_listWidget.findItems(item, Qt.MatchExactly):
                item = QListWidgetItem(item)
                self.ui.selected_listWidget.addItem(item)

    def on_clicked_delchannel_pushButton(self):
        self.signal_file_montage_update.emit(True)
        for item in self.ui.selected_listWidget.selectedItems():
            self.ui.selected_listWidget.takeItem(self.ui.selected_listWidget.row(item))

    def on_clicked_moveup_pushButton(self):
        self.signal_file_montage_update.emit(True)
        listWidget = self.ui.selected_listWidget
        current_row = listWidget.currentRow()
        if current_row > 0:
            item = listWidget.takeItem(current_row)
            listWidget.insertItem(current_row - 1, item)
            listWidget.setCurrentRow(current_row - 1)

    def on_clicked_movedown_pushButton(self):
        self.signal_file_montage_update.emit(True)
        listWidget = self.ui.selected_listWidget
        current_row = listWidget.currentRow()
        if current_row < listWidget.count() - 1:
            item = listWidget.takeItem(current_row)
            listWidget.insertItem(current_row + 1, item)
            listWidget.setCurrentRow(current_row + 1)

    def on_clicked_save_file_montage_setting_pushButton(self):
        if self.ui.selected_listWidget.count() < 1:
            QMessageBox.information(self, "提示", "当前没有选择任何通道，不允许保存", QMessageBox.Yes)
            return
        self.signal_file_montage_update.emit(False)
        channel_list = self.get_selected_listwidget_texts()
        self.selected_file_info[0] = self.selected_montage_name
        self.selected_file_info[2] = channel_list
        self.signal_file_info_montage_setting_save.emit(self.selected_file_info)

    # 获取self.ui.selected_listWidget中的所有内容
    def get_selected_listwidget_texts(self):
        items = []
        for i in range(self.ui.selected_listWidget.count()):
            items.append(self.ui.selected_listWidget.item(i).text())
        return items

    # 检测是否可以通过该通道扫描脑电数据
    def if_add_channel_availabel(self, add_channel):
        add_channel = add_channel.split('-')
        tag = False
        if add_channel[0] in self.file_included_channel_list and add_channel[1] in self.file_included_channel_list:
            tag = True
        return tag

    def set_enabel_state_montage_setting_buttons(self, tag:bool):
        self.ui.save_file_montage_setting_pushButton.setEnabled(tag)
        self.ui.moveup_pushButton.setEnabled(tag)
        self.ui.delchannel_pushButton.setEnabled(tag)
        self.ui.movedown_pushButton.setEnabled(tag)
        self.ui.allAddchannel_pushButton.setEnabled(tag)
        self.ui.addchannel_pushButton.setEnabled(tag)

    def __home_page(self):
        """点击首页信号"""
        self.page_control_signal.emit(["home", self.ui.label_9.text()])

    def __pre_page(self):
        """点击上一页信号"""
        self.page_control_signal.emit(["pre", self.ui.label_9.text()])

    def __next_page(self):
        """点击下一页信号"""
        self.page_control_signal.emit(["next", self.ui.label_9.text()])

    def __final_page(self):
        """尾页点击信号"""
        self.page_control_signal.emit(["final", self.ui.label_9.text()])

    def __confirm_skip(self):
        """跳转页码确定"""
        self.page_control_signal.emit(["confirm", self.ui.lineEdit_2.text()])



class PrentryView(QWidget):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_Prentry()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = AutoView()
    view.show()
    sys.exit(app.exec_())
