from PyQt5.Qt import *
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import *
from view.labelType import LabelTypeView
from view.labelType_form.question.question import Question
import re


class labelTypeController(QWidget):
    def __init__(self, client, cAppUtil):
        super().__init__()
        self.client = client
        self.cAppUtil = cAppUtil
        self.view = LabelTypeView()

        self.getTypeInfo()
        self.client.getTypeInfoResSig.connect(self.getTypeInfoRes)
        self.client.addTypeInfoResSig.connect(self.addTypeInfoRes)
        self.client.delTypeInfoResSig.connect(self.delTypeInfoRes)
        self.client.updateTypeInfoResSig.connect(self.updateTypeInfoRes)

        # 存放当前标注类型信息列表
        self.type_info = []

        self.view.ui.btnAdd.clicked.connect(self.on_btnAdd_clicked)
        self.view.ui.btnDel.clicked.connect(self.on_btnDel_clicked)
        self.view.ui.btnSelect.clicked.connect(self.on_btnSelect_clicked)

        # 只能选中一行
        self.view.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.ui.tableWidget.resizeRowsToContents()
        self.view.ui.tableWidget.resizeRowsToContents()
        self.view.ui.tableWidget.resizeColumnsToContents()
        self.view.ui.tableWidget.cellDoubleClicked.connect(self.on_tableWidget_cellDoubleClicked)

        # update属性代表当前是否在修改状态
        self.update = -1
        self.insert = -1


    # 查询标注类型功能
    # 获取标注类型方法
    def getTypeInfo(self, name='', value=''):
        account = self.client.tUser[1]
        REQmsg = [account, name, value]
        self.client.getTypeInfo(REQmsg)

    # 处理客户端返回的查询标注类型的结果
    def getTypeInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                type_info_1 = REPData[3]
                if len(type_info_1) != 0:
                    if len(type_info_1) < len(self.type_info):
                        self.type_info = type_info_1
                        self.view.ui.lineValue.clear()
                        self.view.initTable(self.type_info)
                        QMessageBox.information(self, "标注类型", '查询成功！如需重新显示全部标注类型信息，请再次点击查询按钮')
                    else:
                        self.type_info = type_info_1
                        self.view.ui.lineValue.clear()
                        self.view.initTable(self.type_info)
                else:
                    self.view.ui.lineValue.clear()
                    QMessageBox.information(self, "标注类型", '未查询到符合条件的信息,请输入正确查询信息')
                    self.view.initTable(self.type_info)
            else:
                QMessageBox.information(self, "标注类型", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('getTypeInfo', e)


    # 添加标注类型功能
    # 添加标注类型信息方法
    def on_btnAdd_clicked(self):
        self.view.ui.tableWidget.scrollToBottom()
        if self.update != -1:
            QMessageBox.information(self, '未修改完成', "请确认修改！")
            return

        self.view.ui.btnAdd.setEnabled(False)
        row = self.view.ui.tableWidget.rowCount()
        self.insert = row
        self.disable_tableWidgetItem(row)
        col = self.view.ui.tableWidget.columnCount()
        self.view.ui.tableWidget.insertRow(row)
        self.view.ui.tableWidget.insertColumn(col)
        self.view.ui.tableWidget.setCurrentCell(row, 1)
        header_item = QTableWidgetItem('增加')
        font = header_item.font()
        font.setPointSize(16)
        header_item.setFont(font)
        header_item.setForeground(QBrush(Qt.black))  # 前景色，即文字颜色
        self.view.ui.tableWidget.setHorizontalHeaderItem(col, header_item)

        self.comboCategory = QComboBox()
        font = header_item.font()
        font.setPointSize(16)
        self.comboCategory.setFont(font)
        self.comboCategory.setObjectName("comboCategory")
        self.view.ui.tableWidget.setCellWidget(row, 2, self.comboCategory)
        for i in range(len(self.view.category)):
            self.comboCategory.addItem(self.view.category[i])
        self.comboCategory.setCurrentIndex(0)

        question = Question()
        question.ui.btnOK.clicked.connect(self.on_btnConfirmAdd_clicked)
        question.ui.btnCancel.clicked.connect(self.on_btnCancelAdd_clicked)
        self.view.ui.tableWidget.setCellWidget(row, col, question)
        self.view.ui.tableWidget.repaint()

    # 确认添加标注类型信息方法
    def on_btnConfirmAdd_clicked(self):
        self.view.ui.tableWidget.repaint()
        row = self.view.ui.tableWidget.currentRow()
        if not self.view.ui.tableWidget.item(row, 0):
            QMessageBox.information(self.view, '标注类型名称', "请输入标注类型名称: ")
            return

        value = self.save_row_data(row)
        data = dict(zip(self.view.field, value))
        # 校验信息
        try:
            self.check_item_pattern(data)
        except Exception as result:
            QMessageBox.information(self.view, '格式输入错误！', "%s" % result)
            return

        account = self.client.tUser[1]
        REQmsg = [account, data['type_name'], data['description'], data['category']]
        self.client.addTypeInfo(REQmsg)

    # 取消添加标注类型信息方法
    def on_btnCancelAdd_clicked(self):
        row = self.view.ui.tableWidget.rowCount()
        col = self.view.ui.tableWidget.columnCount()
        self.view.ui.tableWidget.removeRow(row - 1)
        self.view.ui.tableWidget.removeColumn(col - 1)

        self.view.ui.btnAdd.setEnabled(True)
        self.insert = -1
        self.view.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.enable_tableWidgetItem(row)
        self.view.ui.tableWidget.clear()
        self.view.initTable(self.type_info)

    # 处理客户端传回的添加标注类型信息结果
    def addTypeInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                row = self.view.ui.tableWidget.rowCount()
                self.view.ui.tableWidget.removeColumn(len(self.view.field))
                # 修改成功之后更新修改标记
                self.insert = -1
                self.view.ui.btnAdd.setEnabled(True)
                self.view.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.enable_tableWidgetItem(row)
                self.view.ui.tableWidget.clear()
                # type_row = row + 1
                # type_name = REPData[3][0]
                # description = REPData[3][1]
                # category = REPData[3][2]
                # temp = (type_row, type_name, description, category)
                # print('temp :', temp)
                # self.type_info.append(temp)
                # print('type_info :', self.type_info)
                # 重新获取，为了防止本地type_id和远程不一致情况
                self.getTypeInfo()
                self.view.initTable(self.type_info)
                QMessageBox.information(self, "标注类型", REPData[2], QMessageBox.Yes)
            else:
                QMessageBox.information(self, "标注类型", REPData[2], QMessageBox.Yes)
                row = self.view.ui.tableWidget.rowCount()
                col = self.view.ui.tableWidget.columnCount()
                self.view.ui.tableWidget.removeRow(row - 1)
                self.view.ui.tableWidget.removeColumn(col - 1)

                self.view.ui.btnAdd.setEnabled(True)
                self.insert = -1
                self.view.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                self.enable_tableWidgetItem(row)
                self.view.ui.tableWidget.clear()
                self.view.initTable(self.type_info)
        except Exception as e:
            print('addlabelType', e)


    # 删除标注类型功能
    # 删除标注类型方法
    def on_btnDel_clicked(self):
        row = self.view.ui.tableWidget.currentRow()
        answer = QMessageBox.warning(
            self.view, '确认删除！', '您将进行删除操作！',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if answer == QMessageBox.Yes:
            if row == -1:
                QMessageBox.information(self.view, ' ', '请先选中一行')
                return
            # 暂时只能选中一行删除
            print('row',row)
            type_id = self.type_info[row][0]
            account = self.client.tUser[1]
            REQmsg = [account, type_id, row]
            self.client.delTypeInfo(REQmsg)
            # result = self.DbUtil.del_typeInfo('type_id', self.type_info[row][0])
        else:
            return

    # 处理客户端返回的删除标注类型信息结果
    def delTypeInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                row = REPData[3][1]
                print('pop values :', self.type_info[row])
                self.type_info.pop(row)
                self.view.initTable(self.type_info)
                QMessageBox.information(self, "成功", "删除成功")
                return
            else:
                QMessageBox.information(self, "提示", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('delTypeInfo', e)


    # 修改标注类型功能
    # 修改标注类型方法
    def on_tableWidget_cellDoubleClicked(self, row, col):
        self.view.ui.tableWidget.repaint()
        # 当无其他行正在编辑时设置除当前单元格外其他单元格不可编辑
        if self.update == -1 or self.insert == -1:
            self.disable_tableWidgetItem(row)
        cols = self.view.ui.tableWidget.columnCount()
        # 如果还未显示按钮,增加一列显示
        if cols == self.view.col:
            self.update = row
            # # 编辑时，保存具有唯一性的标注名称，用于数据库查询修改
            # 增加一列按钮
            self.view.ui.tableWidget.insertColumn(self.view.col)
            header_item = QTableWidgetItem('修改')
            font = header_item.font()
            font.setPointSize(16)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))  # 前景色，即文字颜色
            self.view.ui.tableWidget.setHorizontalHeaderItem(self.view.col, header_item)

            self.comboCategory = QComboBox()
            font = header_item.font()
            font.setPointSize(16)
            self.comboCategory.setFont(font)
            self.comboCategory.setObjectName("comboCategory")
            for i in range(len(self.view.category)):
                self.comboCategory.addItem(self.view.category[i])
            self.comboCategory.setCurrentIndex(self.view.category.index(self.view.ui.tableWidget.item(row, 2).text()))
            self.view.ui.tableWidget.setCellWidget(row, 2, self.comboCategory)

            question = Question()
            question.ui.btnOK.clicked.connect(
                lambda: self.on_btnConfirmUpdate_clicked(row))
            # self.controller.on_btnOKUpdate_clicked)
            question.ui.btnCancel.clicked.connect(
                lambda: self.on_btnCancelUpdate_clicked(row))
            self.view.ui.tableWidget.setCellWidget(row, self.view.col, question)

    # 确认修改标注方法
    def on_btnConfirmUpdate_clicked(self, row):
        value = self.save_row_data(row)
        print('value:', value)
        data = dict(zip(self.view.field, value))
        # 校验信息
        try:
            self.check_item_pattern(data)
        except Exception as result:
            QMessageBox.information(self.view, '格式错误！', "%s" % result)
            return
        try:
            account = self.client.tUser[1]
            type_id = self.type_info[row][0]
            REQmsg = [account, value, type_id, row]
            self.client.updateTypeInfo(REQmsg)
            # self.DbUtil.update_typeInfo(value, 'type_id', self.type_info[row][0])
        except Exception as result:
            QMessageBox.information(self.view, '更新失败', "失败原因: %s" % result)

    # 取消修改标注方法
    def on_btnCancelUpdate_clicked(self, row):
        data = self.type_info[row]
        for i in range(len(data) - 1):
            self.view.ui.tableWidget.item(row, i).setText(str(data[i + 1]))
        self.view.ui.tableWidget.removeColumn(len(self.view.field))

        self.update = -1
        self.view.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.enable_tableWidgetItem(row)
        self.view.ui.tableWidget.clear()
        self.view.initTable(self.type_info)

    # 处理客户端传回的修改标注类型信息结果
    def updateTypeInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.view.ui.tableWidget.removeColumn(len(self.view.field))
                # 修改成功之后更新修改标记
                self.update = -1
                self.view.ui.btnAdd.setEnabled(True)
                self.view.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.view.ui.tableWidget.clear()
                row = REPData[3][2]
                type_id = REPData[3][1]
                temp = REPData[3][0]
                temp.insert(0, type_id)
                self.type_info[row] = tuple(temp)
                self.view.initTable(self.type_info)
                QMessageBox.information(self, "提示", REPData[2], QMessageBox.Yes)
                return
            else:
                QMessageBox.information(self, "提示", REPData[2], QMessageBox.Yes)
                return
        except Exception as e:
            print('updateTypeInfohaha', e)


    # 查询标注类型功能
    # 查询标注类型方法
    def on_btnSelect_clicked(self):
        index = self.view.ui.comboCond.currentIndex()
        cond = self.view.ui.comboCond.itemData(index)
        value = self.view.ui.lineValue.text()
        if value:
            try:
                self.getTypeInfo(cond, value)
            except Exception as e:
                print('selectTypeInfo', e)
        else:
            QMessageBox.information(self, "提示", '未输入查询所需信息，将显示所有标注类型！', QMessageBox.Yes)
            self.getTypeInfo()


    # 其它方法
    # 禁用除了activate_row以外的其他行
    def disable_tableWidgetItem(self, active_row):
        row = self.view.ui.tableWidget.rowCount()
        col = self.view.ui.tableWidget.columnCount()
        for r in range(row):
            if r != active_row:
                self.disable_tableWidgetItem_row_col([r], range(col))

    # 禁用disable_row行disable_col列的表格项，disable_col和disable_row都为[]，如[1,2]
    def disable_tableWidgetItem_row_col(self, disable_row, disable_col):
        for r in disable_row:
            for c in disable_col:
                item = self.view.ui.tableWidget.item(r, c)
                if item == None:
                    cellWidget = self.view.ui.tableWidget.cellWidget(r, c)
                    if cellWidget == None:
                        return
                    else:
                        cellWidget.setEnabled(False)
                else:
                    item.setFlags(item.flags() & (~Qt.ItemIsEnabled))

    # 启用除了activate_row以外的其他行
    def enable_tableWidgetItem(self, active_row):
        row = self.view.ui.tableWidget.rowCount()
        col = self.view.ui.tableWidget.columnCount()
        for r in range(row):
            if r != active_row:
                for c in range(col):
                    item = self.view.ui.tableWidget.item(r, c)
                    if item == None:
                        cellWidget = self.view.ui.tableWidget.cellWidget(r, c)
                        if cellWidget == None:
                            continue
                        else:
                            cellWidget.setEnabled(True)
                    else:
                        item.setFlags(Qt.ItemIsEnabled |
                                      Qt.ItemIsEditable | Qt.ItemIsSelectable)

    # 保存选中行的数据
    def save_row_data(self, row):
        value = []
        for i in range(len(self.view.field)):
            if i == 2:
                temp = self.comboCategory.currentText()
            elif self.view.ui.tableWidget.item(row, i):
                temp = self.view.ui.tableWidget.item(row, i).text()
            else:
                temp = ''
            value.append(temp)
        return value

    # 检查编辑/增加 数据格式
    def check_item_pattern(self, data):
        if data['type_name'] == '':
            raise Exception('请输入类型名：不能为空！')
        if data['category'] not in self.view.category:
            raise Exception('请正确输入类别：正常波形/异常波形/伪迹波形/正常状态/异常状态/伪迹状态！')


    def exit(self):
        self.client.getTypeInfoResSig.disconnect()
        self.client.addTypeInfoResSig.disconnect()
        self.client.delTypeInfoResSig.disconnect()
        self.client.updateTypeInfoResSig.disconnect()


