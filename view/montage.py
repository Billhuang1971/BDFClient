import sys

from PyQt5.QtGui import QStandardItemModel, QStandardItem

from view.montage_form.form import Ui_Form
from view.montage_form.add_channels import Ui_add_channels
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QStringListModel


# 导联配置功能主页面
class montageView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 导联配置主页面ui
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.tableview_model_col = 3
        self.tableview_model_row = 0
        self.tableview_model = QStandardItemModel(self.tableview_model_row, self.tableview_model_col)
        self.listview_model_col = 1
        self.listview_model = QStringListModel()
        self.selected_montage_channels = []

    # 初始化方案列表
    def initList(self, montageData, qlist):
        try:
            # qlist = []
            for i in montageData:
                qlist.append(i['name'])
            self.listview_model_row = len(qlist)
            self.listview_model.setStringList(qlist)
            self.ui.listView.setModel(self.listview_model)
            self.ui.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        except Exception as e:
            print('initList', e)

    # 初始化方案导联信息
    def initTable(self, montageData, currentMontageName = None):
        try:
            conference_channel = []
            measure_channel = []
            # if not_first_time:
            #     self.montage_data = self.jsonUtil.get_montage()
            if currentMontageName == None:
                self.selected_montage_channels = []
            for montage_scheme in montageData:
                if montage_scheme['name'] == currentMontageName:
                    self.selected_montage_channels = montage_scheme['channels']
                    break
            self.tableview_model_row = len(self.selected_montage_channels)
            self.tableview_model = QStandardItemModel(self.tableview_model_row, self.tableview_model_col)
            self.tableview_model.setHorizontalHeaderLabels(["测量导联", "参考导联", "导联"])
            for i in range(self.tableview_model_row):
                sub_channel = self.selected_montage_channels[i].split('-')
                conference_channel.append(sub_channel[1])
                measure_channel.append(sub_channel[0])
            for i in range(self.tableview_model_row):
                self.tableview_model.setItem(i, 0, QStandardItem(measure_channel[i]))
                self.tableview_model.setItem(i, 1, QStandardItem(conference_channel[i]))
                self.tableview_model.setItem(i, 2, QStandardItem(self.selected_montage_channels[i]))
            self.ui.tableView.setModel(self.tableview_model)
            # 拉伸表格列项，使其铺满
            self.ui.tableView.horizontalHeader().setStretchLastSection(True)
            # self.view.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        except Exception as e:
            print('MontageController::init_table:', e)


    def reject(self):
        pass

class addChannelsView(QDialog, Ui_add_channels, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 导联配置主页面ui
        self.ui = Ui_add_channels()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = montageView()
    view.show()
    sys.exit(app.exec_())
