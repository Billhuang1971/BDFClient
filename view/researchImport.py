import sys
from datetime import time
from functools import partial


from PyQt5 import QtGui


from view.researchImport_form.form_change_one import Ui_ResearchImportForm

from PyQt5.Qt import *
from PyQt5.QtCore import  Qt,  QEvent
from PyQt5.QtGui import QBrush
import sys

from view.researchImport_form.addform import Ui_AddForm

class ResearchImportView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ResearchImportForm()
        self.ui.setupUi(self)

        self._on_btnAddFile_clicked = None
        self._on_btnRemove_clicked = None
        self._on_btnComplete_clicked = None
        self._on_btnViewMapping_clicked = None


        self.header = ['被试姓名', '医院单号', '检查日期', '实验描述', '开单研究员', '上传研究员', '操作']
        self.field = ['pname', 'check_number', 'measure_date', 'description', 'pdoctorname', 'cdoctorname', 'actions']

        self.header_1 = ['文件名', '状态', '操作']
        self.field_1 = ['file_name', 'state', 'actions']

        self.header_2 = ['文件名', '状态']
        self.field_2 = ['file_name', 'state']

        self.width_threshold = 1872  # 窗口宽度阈值
        # self.resizeEvent = self.onResize  # 监听窗口大小变化

    def initTable(self, data, on_btnAddFile_clicked=None, on_btnRemove_clicked=None, on_btnComplete_clicked=None,
                  on_btnViewMapping_clicked=None):
        col_num = len(self.header)
        self.ui.tableWidget.setColumnCount(col_num)
        self.data = data
        self.row_buttons = []

        self._on_btnAddFile_clicked = on_btnAddFile_clicked
        self._on_btnRemove_clicked = on_btnRemove_clicked
        self._on_btnComplete_clicked = on_btnComplete_clicked
        self._on_btnViewMapping_clicked = on_btnViewMapping_clicked

        if data:
            row_num = len(data)
            self.ui.tableWidget.setRowCount(row_num)

            for i in range(col_num):
                header_item = QTableWidgetItem(self.header[i])
                font = header_item.font()
                font.setPointSize(16)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                header_item.setData(Qt.UserRole, self.field[i])
                self.ui.tableWidget.setHorizontalHeaderItem(i, header_item)

            for r in range(row_num):
                for c in range(col_num - 1):  # 排除“操作”列
                    item = QTableWidgetItem(str(data[r][c + 4]))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(16)
                    item.setFont(font)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.ui.tableWidget.setItem(r, c, item)

                self.setActionButtons(r, on_btnAddFile_clicked, on_btnRemove_clicked,
                                      on_btnComplete_clicked, on_btnViewMapping_clicked)

            # self.ui.tableWidget.currentCellChanged.connect(self.updateButtonStates)
            self.ui.tableWidget.currentCellChanged.connect(self.onCurrentCellChanged)
            self.ui.tableWidget.setColumnHidden(3, True)
            self.ui.tableWidget.horizontalHeader().setHighlightSections(False)
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        else:
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.setColumnCount(0)

    def setActionButtons(self, r, on_btnAddFile_clicked,on_btnRemove_clicked, on_btnComplete_clicked, on_btnViewMapping_clicked):
        """根据窗口大小切换操作按钮布局"""
        table = self.ui.tableWidget
        action_widget = QWidget()
        layout = QHBoxLayout(action_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # 更稳妥的回调检测方式
        has_all_callbacks = all(map(callable, [
            on_btnAddFile_clicked,
            on_btnRemove_clicked,
            on_btnComplete_clicked,
            on_btnViewMapping_clicked
        ]))

        if self.width() >= self.width_threshold and has_all_callbacks:  # 宽屏 + 所有回调都存在
            addFileButton = QPushButton("添加")
            addFileButton.clicked.connect(partial(on_btnAddFile_clicked, r))

            removeButton = QPushButton("删除")
            removeButton.clicked.connect(partial(on_btnRemove_clicked, r))

            completeButton = QPushButton("完成")
            completeButton.clicked.connect(partial(on_btnComplete_clicked, r))

            viewMappingButton = QPushButton("查看")
            viewMappingButton.clicked.connect(partial(on_btnViewMapping_clicked, r))

            layout.addWidget(addFileButton)
            layout.addWidget(removeButton)
            layout.addWidget(completeButton)
            layout.addWidget(viewMappingButton)

            self.row_buttons.append((addFileButton, removeButton, completeButton, viewMappingButton))
        else:
            menu_btn = QPushButton("操作")


            # 美化菜单
            menu = QMenu(menu_btn)

            # 动态绑定宽度
            def adjust_menu_width():
                column_index = table.columnCount() - 1
                column_width = table.columnWidth(column_index)
                menu.setFixedWidth(column_width)

            menu.aboutToShow.connect(adjust_menu_width)



            menu.setStyleSheet("""
                QMenu {
                    font-size: 16px;
                    background-color: #ffffff;
                    border: 1px solid #dcdcdc;
                    border-radius: 8px;
                    padding: 8px;
                    color: #333;
                }
                QMenu::item {
                    padding: 8px 28px;
                    border-radius: 6px;
                    background-color: transparent;
                }
                QMenu::item:selected {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                      stop:0 #cce6ff, stop:1 #99ccff);
                    color: #000000;
                }
                QMenu::separator {
                    height: 1px;
                    background: #e5e5e5;
                    margin: 4px 10px;
                }
            """)

            if callable(on_btnAddFile_clicked):
                menu.addAction("添加", partial(on_btnAddFile_clicked, r))
            if callable(on_btnRemove_clicked):
                menu.addAction("删除", partial(on_btnRemove_clicked, r))
            if callable(on_btnComplete_clicked):
                menu.addAction("完成", partial(on_btnComplete_clicked, r))
            if callable(on_btnViewMapping_clicked):
                menu.addAction("查看", partial(on_btnViewMapping_clicked, r))

            menu_btn.setMenu(menu)
            layout.addWidget(menu_btn)
            self.row_buttons.append((None, None, None, None))

        table.setCellWidget(r, table.columnCount() - 1, action_widget)

    def onCurrentCellChanged(self, currentRow, currentColumn, previousRow, previousColumn):
        """用于处理当前行变化时更新按钮状态"""
        self.updateButtonStates(previousRow, currentRow)

    def updateButtonStates(self, previousRow, currentRow):
        """只更新前一行与当前行的按钮状态，提高效率"""
        for row in (previousRow, currentRow):
            if 0 <= row < self.ui.tableWidget.rowCount():
                cell_widget = self.ui.tableWidget.cellWidget(row, self.ui.tableWidget.columnCount() - 1)
                if cell_widget:
                    buttons = cell_widget.findChildren(QPushButton)
                    for btn in buttons:
                        btn.setEnabled(row == currentRow)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.onResize(event)

    def onResize(self, event):
        """窗口大小变化时重设操作按钮布局"""
        # print("当前窗口宽度为：", self.width())
        old_width = event.oldSize().width()
        new_width = event.size().width()

        # 只有跨越阈值时才刷新按钮，避免不必要重绘
        if (old_width < self.width_threshold and new_width >= self.width_threshold) or \
           (old_width >= self.width_threshold and new_width < self.width_threshold):
            self.refreshActionButtons()

    def refreshActionButtons(self):
        """根据当前大小重绘所有行的操作按钮"""
        if not hasattr(self, 'data') or not self.data:
            return
        self.row_buttons.clear()
        for r in range(len(self.data)):
            item = self.ui.tableWidget.item(r, 0)
            if item is not None:
                # 保留原有回调方式
                self.setActionButtons(r,
                                      self._on_btnAddFile_clicked,
                                      self._on_btnRemove_clicked,
                                      self._on_btnComplete_clicked,
                                      self._on_btnViewMapping_clicked
                                      )

    def row_buttons_callback(self, row, action_index):
        """占位回调，只会被 partial 传入真实的"""
        pass



    def eventFilter(self, obj, event):
        if event.type() == QEvent.ToolTip:
            pos = event.pos()
            item = self.ui.tableWidget.itemAt(pos)
            if item:
                row = self.ui.tableWidget.row(item)
                font = item.font()
                font.setPointSize(16)
                QToolTip.setFont(font)  # 确保使用应用程序的默认字体
                # QToolTip.setStyleSheet("QToolTip { font-size: 14pt; font-style: italic; background-color: yellow; }")
                QToolTip.showText(event.globalPos(), f"实验描述: \n{self.data[row][7]}")
            else:
                QToolTip.hideText()
            return True
        return False


    def initTable_1(self, data ,on_btnDelFile_clicked = None):
        col_num = len(self.header_1)
        row_num = len(data)
        self.ui.tableWidget_1.setColumnCount(col_num)
        self.ui.tableWidget_1.setRowCount(row_num)
        # 设置表头
        for i in range(col_num):
            header_item = QTableWidgetItem(self.header_1[i])
            font = header_item.font()
            font.setPointSize(16)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            header_item.setData(Qt.UserRole, self.field_1[i])
            self.ui.tableWidget_1.setHorizontalHeaderItem(i, header_item)

        # 填充表格数据和按钮
        for r in range(row_num):
            for c in range(col_num - 1): # 不包括“操作”列
                # 具体传哪一个参数在这里修改
                item = QTableWidgetItem(str(data[r][c]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                # font = header_item.font()
                font.setPointSize(16)
                item.setFont(font)

                # 禁用编辑功能
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 禁止编辑

                self.ui.tableWidget_1.setItem(r, c, item)

                # 设置 tooltip 显示完整的文件名
                if c == 0:
                    item.setToolTip(str(data[r][c]))  # 设置 tooltip 为文件名，鼠标悬停时会显示完整文件名

                self.ui.tableWidget_1.setItem(r, c, item)

                # 在最后一列添加按钮
                action_widget = QWidget()
                layout = QHBoxLayout(action_widget)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(5)

                delFileButton = QPushButton("删除")

                # 可以根据需要添加按钮点击事件
                delFileButton.clicked.connect(partial(on_btnDelFile_clicked,  r))

                layout.addWidget(delFileButton)

                self.ui.tableWidget_1.setCellWidget(r, col_num - 1, action_widget)

        self.ui.tableWidget_1.horizontalHeader().setHighlightSections(False)
        self.ui.tableWidget_1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    # 初始化第三个表格
    def initTable_2(self, data):
        col_num = len(self.header_2)
        row_num = len(data)
        self.ui.tableWidget_2.setColumnCount(col_num)
        self.ui.tableWidget_2.setRowCount(row_num)
        for i in range(col_num):
            header_item = QTableWidgetItem(self.header_2[i])
            font = header_item.font()
            font.setPointSize(16)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            header_item.setData(Qt.UserRole, self.field_2[i])
            self.ui.tableWidget_2.setHorizontalHeaderItem(i, header_item)

        for r in range(row_num):
            for c in range(col_num):
                # 具体传哪一个参数在这里修改
                item = QTableWidgetItem(str(data[r][c]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                # font = header_item.font()
                font.setPointSize(16)
                item.setFont(font)

                # 禁用编辑功能
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 禁止编辑

                self.ui.tableWidget_2.setItem(r, c, item)

        self.ui.tableWidget_2.horizontalHeader().setHighlightSections(False)
        self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


# 添加诊断信息弹出框
class AddFormView(QWidget):
    def __init__(self, parent=None,):
        super().__init__(parent)
        self.ui = Ui_AddForm()
        self.ui.setupUi(self)

    def initTabel(self, name):
        # pass
        self.ui.label_cdoctor.setText(name)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = AddFormView()
    view.show()
    sys.exit(app.exec_())