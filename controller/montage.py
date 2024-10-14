from view.montage import montageView
from view.montage import addChannelsView

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import sys, re


class montageController(QWidget):
    def __init__(self, client, cAppUtil):
        try:
            super().__init__()
            self.client = client
            self.cAppUtil = cAppUtil
            self.view = montageView()


            self.scheme = None
            self.current_montage_name = ''
            # self.selected_montage_channels = []
            self.is_edit = False
            self.montageData = []
            self.qlist = []

            self.client.getMontageResSig.connect(self.getMontageRes)
            self.client.addMontageSchemeResSig.connect(self.addMontageSchemeRes)
            self.client.editMontageSchemeResSig.connect(self.editMontageSchemeRes)
            self.client.delMontageSchemeResSig.connect(self.delMontageSchemeRes)
            self.client.saveMontageChannelResSig.connect(self.saveMontageChannelRes)

            self.view.ui.pushButton.clicked.connect(self.on_clicked_add_montage_scheme)
            self.view.ui.pushButton_5.clicked.connect(self.on_clicked_edit_montage_scheme)
            self.view.ui.pushButton_2.clicked.connect(self.on_clicked_del_montage_scheme)
            self.view.ui.pushButton_3.clicked.connect(self.on_clicked_add_montage_scheme_channel)
            self.view.ui.pushButton_4.clicked.connect(self.on_clicked_edit_montage_scheme_channel)
            self.view.ui.pushButton_6.clicked.connect(self.on_clicked_del_montage_scheme_channel)
            self.view.ui.listView.clicked.connect(self.on_clicked_listview)
            self.client.getMontage([self.client.tUser[0], self.client.tUser[1]])
            # self.init_list()
            # self.init_table(self.montageData, self.current_montage_name)
        except Exception as e:
            print('MontageController::__init__:', e)

    def getMontageRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.montageData = REPData[2]
                self.view.initList(self.montageData, self.qlist)
                print(self.qlist)
                print(self.montageData)
                self.view.initTable(self.montageData)
            elif REPData[0] == '0':
                QMessageBox.information(self, '提示', '打开导联配置文件无效', QMessageBox.Ok)
        except Exception as e:
            print('getMontageRes', e)

    # 点击方案列表上的方案项
    def on_clicked_listview(self, qModelIndex):
        # QMessageBox.information(self,"ListWidget","你选择了：" + self.qlist[qModelIndex.row()])
        try:
            self.current_montage_name = self.qlist[qModelIndex.row()]
            self.view.initTable(self.montageData, self.current_montage_name)
            self.view.ui.label.setText("当前选择方案:{}".format(self.current_montage_name))
        except Exception as e:
            print('MontageController.on_clicked_listview():', e)

    # 添加导联方案
    def on_clicked_add_montage_scheme(self):
        try:
            reply = QInputDialog.getText(self, "新增方案", "请输入新增方案的名称", text='new_scheme')
            name = reply[0]
            # 方案名称与现有方案名称重复
            for scheme in self.qlist:
                if name == scheme:
                    QMessageBox.critical(self, '提示', '方案名称重复', QMessageBox.Ok)
                    return
            # 用户输入名称，且点击确定
            if reply[1] == True:
                REQmsg = [name]
                self.client.addMontageScheme(REQmsg)
        except Exception as e:
            print('addMontageScheme', e)

    def addMontageSchemeRes(self, REPData):
        try:
            if REPData[0] == '1':
                QMessageBox.information(self, '提示', f'添加{REPData[2]}方案成功', QMessageBox.Ok)
                newscheme = {'channels': [], 'name': REPData[2]}
                # print(type(newscheme))
                self.montageData.append(newscheme)
                self.qlist = []
                self.view.initList(self.montageData, self.qlist)
            elif REPData[0] == '0':
                QMessageBox.information(self, '提示', f'编辑{REPData[2]}方案成功', QMessageBox.Ok)
                # self.view.initTable(self.montageData)
                self.view.initList(self.montageData, self.qlist)
        except Exception as e:
            print('addMontageSchemeRes', e)

    # 编辑导联方案
    def on_clicked_edit_montage_scheme(self):
        try:
            reply = QInputDialog.getText(self, "编辑方案", "请输入方案的名称", text=self.current_montage_name)
            name = reply[0]
            # 方案名称与现有方案名称重复
            for scheme in self.qlist:
                if name == scheme:
                    QMessageBox.critical(self, '提示', '方案名称重复', QMessageBox.Ok)
                    return
            # 用户输入名称，且点击确定
            if reply[1] == True:
                REQmsg = [self.current_montage_name, name]
                self.client.editMontageScheme(REQmsg)
        except Exception as e:
            print('editMontageScheme', e)

    def editMontageSchemeRes(self, REPData):
        try:
            old_name = REPData[2][0]
            new_name = REPData[2][1]
            if REPData[0] == '1':
                QMessageBox.information(self, '提示', f'编辑{new_name}方案成功', QMessageBox.Ok)
                for i in self.montageData:
                    if old_name == i['name']:
                        i['name'] = new_name
                        break
                self.qlist = []
                self.current_montage_name = new_name
                self.view.ui.label.setText("当前选择方案:{}".format(new_name))
                self.view.initList(self.montageData, self.qlist)
            elif REPData[0] == '0':
                QMessageBox.information(self, '提示', f'编辑{old_name}方案成功', QMessageBox.Ok)
                # self.view.initTable(self.montageData)
                self.view.initList(self.montageData, self.qlist)
        except Exception as e:
            print('editMontageSchemeRes', e)

    def on_clicked_del_montage_scheme(self):
        try:
            name = self.qlist[self.view.ui.listView.currentIndex().row()]
            reply = QMessageBox.information(self, '提示', '确认删除{}方案吗？'.format(name), QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                REQmsg = [name]
                self.client.delMontageScheme(REQmsg)
        except Exception as e:
            print("on_clicked_del_montage_scheme", e)

    def delMontageSchemeRes(self, REPData):
        try:
            name = REPData[2][0]
            if REPData[0] == '1':
                QMessageBox.information(self, '提示', f'删除{name}方案成功', QMessageBox.Ok)
                for i in range(len(self.montageData)):
                    if name == self.montageData[i]['name']:
                        self.montageData.pop(i)
                        break
                self.qlist = []
                self.view.ui.label.setText("当前选择方案:")
                self.current_montage_name = ''
                self.view.initTable(self.montageData)
                self.view.initList(self.montageData, self.qlist)
            elif REPData[0] == '0':
                QMessageBox.information(self, '提示', f'删除{name}方案成功', QMessageBox.Ok)
                # self.view.initTable(self.montageData)
                self.view.initList(self.montageData, self.qlist)
        except Exception as e:
            print('delMontageSchemeRes', e)

    def on_clicked_add_montage_scheme_channel(self):
        try:
            if self.current_montage_name == '':
                QMessageBox.information(self, '提示', '未选择导联方案', QMessageBox.Ok)
                return
            self.add_channels_view = addChannelsView()
            self.add_channels_view.ui.pushButton.clicked.connect(self.on_clicked_save_channel)
            self.add_channels_view.show()
        except Exception as e:
            print('on_clicked_add_montage_scheme_channel', e)

    def on_clicked_edit_montage_scheme_channel(self):
        try:
            if self.current_montage_name == '':
                QMessageBox.information(self, '提示', '未选择导联方案', QMessageBox.Ok)
                return
            self.is_edit = True
            current_row = self.view.ui.tableView.currentIndex().row()
            channel = self.view.selected_montage_channels[current_row].split(('-'))
            self.view.ui.tableView.selectRow(current_row)
            self.add_channels_view = addChannelsView()
            self.add_channels_view.ui.pushButton.clicked.connect(self.on_clicked_save_channel)
            self.add_channels_view.ui.lineEdit.setText(channel[0])
            self.add_channels_view.ui.lineEdit_2.setText(channel[1])
            self.add_channels_view.show()
        except Exception as e:
            print("on_clicked_edit_montage_scheme_channel:", e)

    def on_clicked_del_montage_scheme_channel(self):
        try:
            if self.current_montage_name == '':
                QMessageBox.information(self, '提示', '未选择导联方案', QMessageBox.Ok)
                return
            current_row = self.view.ui.tableView.currentIndex().row()
            self.view.ui.tableView.selectRow(current_row)
            channel = self.view.selected_montage_channels[current_row].split(('-'))
            reply = QMessageBox.information(self, '提示', '确认删除该条信息吗？', QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                self.view.selected_montage_channels = np.delete(self.view.selected_montage_channels, current_row, axis=0).tolist()
                flag = 2
                REQmsg = [self.current_montage_name, self.view.selected_montage_channels, flag, channel[0], channel[1]]
                self.client.saveMontageChannel(REQmsg)
        except Exception as e:
            print("on_clicked_del_montage_scheme_channel:", e)

    def on_clicked_save_channel(self):
        try:
            measure_channel = self.add_channels_view.ui.lineEdit.text()
            conference_channel = self.add_channels_view.ui.lineEdit_2.text()
            if measure_channel != '' and conference_channel != '':
                # 编辑导联
                if self.is_edit:
                    current_row = self.view.ui.tableView.currentIndex().row()
                    self.view.selected_montage_channels[current_row] = '{}-{}'.format(measure_channel, conference_channel)
                    self.is_edit = False
                    flag = 1
                # 新增导联
                else:
                    self.view.selected_montage_channels.append('{}-{}'.format(measure_channel, conference_channel))
                    flag = 0
                REQmsg = [self.current_montage_name, self.view.selected_montage_channels, flag, measure_channel, conference_channel]
                self.client.saveMontageChannel(REQmsg)
            else:
                QMessageBox.information(self, '提示', '请在文本框输入完成后点击确认', QMessageBox.Ok)
        except Exception as e:
            print('on_clicked_save_channel:', e)

    def saveMontageChannelRes(self, REPData):
        try:
            if REPData[0] == '1':
                name = REPData[2][0]
                channel = REPData[2][1]
                flag = REPData[2][2]
                for i in self.montageData:
                    if name == i['name']:
                        i['channels'] = channel
                        break
                if flag == 0:
                    QMessageBox.information(self, '提示', f'添加{REPData[2][3]}-{REPData[2][4]}通道成功', QMessageBox.Ok)
                    self.add_channels_view.close()
                    self.view.initTable(self.montageData, self.current_montage_name)
                elif flag == 1:
                    QMessageBox.information(self, '提示', f'编辑{REPData[2][3]}-{REPData[2][4]}通道成功',QMessageBox.Ok)
                    self.add_channels_view.close()
                    self.view.initTable(self.montageData, self.current_montage_name)
                elif flag == 2:
                    QMessageBox.information(self, '提示', f'删除{REPData[2][3]}-{REPData[2][4]}通道成功', QMessageBox.Ok)
                    self.view.initTable(self.montageData, self.current_montage_name)
            elif REPData[0] == '0':
                QMessageBox.information(self, '提示', '操作失败,打开导联配置文件无效', QMessageBox.Ok)
                self.view.initTable(self.montageData, self.current_montage_name)
        except Exception as e:
            print('saveMontageChannelRes', e)

    def exit(self):
        self.client.getMontageResSig.disconnect()
        self.client.addMontageSchemeResSig.disconnect()
        self.client.editMontageSchemeResSig.disconnect()
        self.client.delMontageSchemeResSig.disconnect()
        self.client.saveMontageChannelResSig.disconnect()
