import sys
from functools import partial

from view.taskSettings_form.form import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QComboBox, QLineEdit, QListView, QCompleter
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QMouseEvent, QFont, QBrush, QIntValidator
import sys
from PyQt5 import QtWidgets, QtGui

from view.taskSettings_form.addTheme import Ui_addTheme
from view.taskSettings_form.chooseInfo.choose import Ui_Prentry
from view.taskSettings_form.themeInfo import Ui_themeInfo

class taskSettingsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # self.themeName = themeName
        # self.createUserName = createUserName
        # self.taskUserName = taskUserName

        # self.montage = montage
        # self.model = None

        self.init_view()



    def init_view(self):
        font = QFont()
        font.setFamily("Arial Black")
        font.setPixelSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.font1 = QFont()
        self.font1.setPixelSize(18)


        self.filter_btn = QPushButton('搜索')
        self.filter_btn.setFont(QFont(self.font1))
        # self.filter_btn.setFont(QFont('', 16))

        self.btnReSelect = QPushButton('重置')
        self.btnReSelect.setFont(QFont(self.font1))
        # self.btnReSelect.setFont(QFont('', 16))
        # self.filter_btn.setStyleSheet("background-color: rgb(255, 0, 0);\n"
        #                               "color: rgb(255, 255, 255);")

        self.add_btn = QPushButton('添加')
        self.add_btn.setFont(QFont(self.font1))
        # self.add_btn.setFont(QFont('', 16))
        # self.add_btn.setStyleSheet("background-color: rgb(255, 0, 0);\n"
        #                               "color: rgb(255, 255, 255);")

        self.del_btn = QPushButton('删除')
        self.del_btn.setFont(QFont(self.font1))
        # self.del_btn.setFont(QFont('', 16))
        # self.del_btn.setStyleSheet("background-color: rgb(255, 0, 0);\n"
        #                               "color: rgb(255, 255, 255);")

        self.update_btn = QPushButton('编辑')
        self.update_btn.setFont(QFont(self.font1))
        # self.update_btn.setFont(QFont('', 16))
        # self.update_btn.setStyleSheet("background-color: rgb(255, 0, 0);\n"
        #                               "color: rgb(255, 255, 255);")

        # self.test_btn = QPushButton('测试')
        # self.test_btn.setFont(QFont(font))
        # self.test_btn.setStyleSheet("background-color: rgb(255, 0, 0);\n"
        #                               "color: rgb(255, 255, 255);")

        # horizontalLayout_1 = QHBoxLayout()
        horizontalLayout_2 = QHBoxLayout()
        self.comBoxLayout = QHBoxLayout()
        horizontalLayout_3 = QHBoxLayout()

        spaceItem_1 = QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        spaceItem_2 = QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        spaceItem_6 = QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        spaceItem_7 = QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        spaceItem_8 = QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        # 搜索筛选框
        self.comboCond = QtWidgets.QComboBox()
        self.comboCond.setFixedWidth(int(4 * 16 * 1.67))
        font = QtGui.QFont()
        font.setPixelSize(18)
        self.comboCond.setFont(font)
        self.comboCond.setObjectName("comboCond")
        self.comboCond.addItems(['主题名', '创建用户', '主题状态'])
        self.comBoxLayout.addWidget(self.comboCond)
        self.lineValue = QtWidgets.QLineEdit()
        self.lineValue.setFixedWidth(int(6 * 16 * 1.67))
        font = QtGui.QFont()
        font.setPixelSize(18)
        self.lineValue.setFont(font)
        self.lineValue.setObjectName("lineValue")
        self.comBoxLayout.addWidget(self.lineValue)




        horizontalLayout_2.addLayout(self.comBoxLayout)
        horizontalLayout_2.addWidget(self.filter_btn)
        horizontalLayout_2.addItem(spaceItem_6)
        horizontalLayout_2.addWidget(self.btnReSelect)
        horizontalLayout_2.addItem(spaceItem_6)
        horizontalLayout_2.addWidget(self.add_btn)
        horizontalLayout_2.addItem(spaceItem_6)
        horizontalLayout_2.addWidget(self.del_btn)
        horizontalLayout_2.addItem(spaceItem_6)
        horizontalLayout_2.addWidget(self.update_btn)
        horizontalLayout_2.addItem(spaceItem_6)
        # horizontalLayout_2.addWidget(self.test_btn)
        # horizontalLayout_2.addItem(spaceItem_6)


        horizontalLayout_2.setStretch(horizontalLayout_2.count() - 1, 1)

        # horizontalLayout_3.addWidget(isOutPutFile)
        # horizontalLayout_3.addWidget(self.yesRadioButton)
        # horizontalLayout_3.addWidget(self.noRadioButton)
        horizontalLayout_3.addItem(spaceItem_8)
        horizontalLayout_3.setStretch(horizontalLayout_3.count() - 1, 1)

        # TODO：放开
        # self.comBoxGroup('标注主题')

        # self.ui.verticalLayout_2.addLayout(horizontalLayout_1)
        self.ui.verticalLayout_2.addLayout(horizontalLayout_2)
        self.ui.verticalLayout_2.addLayout(horizontalLayout_3)





    # 清除布局内所有控件
    def deleteAll(self, thisLayout):
        item_list = list(range(thisLayout.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序

        for i in item_list:
            item = thisLayout.itemAt(i)
            if item is not None:
                if item.widget() is not None:
                    item.widget().deleteLater()
                elif isinstance(item, QSpacerItem):
                    thisLayout.removeItem(item)
                else:
                    self.deleteAll(item.layout())
                thisLayout.removeItem(item)





class TableWidget(QWidget):
    control_signal = pyqtSignal(list)

    def __init__(self, *args, **kwargs, ):
        super(TableWidget, self).__init__(*args, **kwargs)
        self.addOther()



    def init_ui(self,current_page=1, col_label=None, sampleList=None, totalNum=0,on_clicked_lookthemeBtn=None, on_clicked_lookdetailBtn=None,
                 on_clicked_adddetailBtn=None, on_clicked_startTheme=None, tuser=None,):

        # if sampleList:
        self.tableRow = len(sampleList)
        self.tableCol = len(col_label)
        self.col_label = col_label
        self.sampleList = sampleList
        self.current_page = current_page
        self.totalNum = totalNum
        self.tuser = tuser

        self.table = QTableWidget(self.tableRow, self.tableCol)
        self.table.setHorizontalHeaderLabels(self.col_label)
        font = QtGui.QFont()
        font.setPixelSize(18)
        # print(self.col_label)
        for row in range(0, self.tableRow):
            for col in range(0, self.tableCol-1):
                if isinstance(self.sampleList[row][col+3], int):
                    self.text_item = QTableWidgetItem(str(self.sampleList[row][col+3]))
                else:
                    self.text_item = QTableWidgetItem(self.sampleList[row][col+3])
                self.text_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.text_item.setFont(font)
                self.table.setItem(row, col, self.text_item)
            # 设置最后一列信息
            layout = QHBoxLayout()
            self.table.setCellWidget(row, self.tableCol - 1, QWidget())

            lookthemeBtn = QPushButton('查看主题信息')
            lookthemeBtn.clicked.connect(partial(on_clicked_lookthemeBtn, row))
            lookthemeBtn.setStyleSheet('border: none;color:blue')
            lookthemeBtn.setFont(font)
            lookthemeBtn.setCursor(Qt.PointingHandCursor)
            lookthemeBtn.setToolTip('查看主题信息')  # 添加鼠标悬停提示
            layout.addWidget(lookthemeBtn)


            lookdetailBtn = QPushButton('查看任务信息')
            lookdetailBtn.clicked.connect(partial(on_clicked_lookdetailBtn, row))
            lookdetailBtn.setStyleSheet('border: none;color:blue')
            lookdetailBtn.setFont(font)
            lookdetailBtn.setCursor(Qt.PointingHandCursor)
            lookdetailBtn.setToolTip('查看任务信息')  # 添加鼠标悬停提示
            layout.addWidget(lookdetailBtn)

            adddetailBtn = QPushButton('添加详细任务')
            adddetailBtn.clicked.connect(partial(on_clicked_adddetailBtn, row))
            adddetailBtn.setStyleSheet('border: none;color:blue')
            adddetailBtn.setFont(font)
            adddetailBtn.setCursor(Qt.PointingHandCursor)
            adddetailBtn.setToolTip('添加详细任务')  # 添加鼠标悬停提示
            layout.addWidget(adddetailBtn)

            startThemeBtn = QPushButton('启动任务')
            startThemeBtn.clicked.connect(partial(on_clicked_startTheme, row))
            startThemeBtn.setStyleSheet('border: none;color:blue')
            startThemeBtn.setFont(font)
            startThemeBtn.setCursor(Qt.PointingHandCursor)
            startThemeBtn.setToolTip('启动任务')  # 添加鼠标悬停提示
            layout.addWidget(startThemeBtn)


            # 如果当前行的主题创建用户不是当前用户就不显示添加详细任务信息按钮
            if self.sampleList[row][1] != self.tuser:
                # adddetailBtn.hide()
                # 当前用户不是创建该标注任务的人员
                adddetailBtn.setDisabled(True)
                adddetailBtn.setStyleSheet('border: none; color:grey')
                adddetailBtn.setFont(font)
                # 启动任务状态按钮变灰
                startThemeBtn.setDisabled(True)
                startThemeBtn.setStyleSheet('border: none; color:grey')
                startThemeBtn.setFont(font)
            # 如果当前标注主题已经启动，就直接变为灰色
            if self.sampleList[row][6] != 'creating':
                # 启动任务过后添加详细任务按钮也变灰
                adddetailBtn.setDisabled(True)
                adddetailBtn.setStyleSheet('border: none; color:grey')
                adddetailBtn.setFont(font)


                # 启动任务状态按钮变灰
                startThemeBtn.setDisabled(True)
                startThemeBtn.setStyleSheet('border: none; color:grey')
                startThemeBtn.setFont(font)

            layout.setStretch(0, 1)
            layout.setStretch(1, 1)
            # layout.setStretch(2, 1)
            # layout.setStretch(3, 1)
            self.table.cellWidget(row, self.tableCol - 1).setLayout(layout)
            # 设置行高
            self.table.setRowHeight(row, 50)

        self.table.horizontalHeader().setStyleSheet(
            '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应宽度
        self.table.horizontalHeader().setDefaultSectionSize(200)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 某一列按照内容自适应宽度
        self.table.resizeColumnToContents(0)
        self.table.resizeColumnToContents(1)
        self.table.resizeColumnToContents(2)
        self.table.resizeColumnToContents(3)

        self.table.resizeColumnToContents(4)
        # self.table.setColumnWidth(3, 700)



        # 设置除最后一列之外的列的宽度
        # for i in range(0, self.tableCol-1):
        #     self.table.setColumnWidth(self.tableCol-1, 50)



        # 设置一次选择一行
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.verticalLayout_1.addWidget(self.table)
        # else:
        #     self.tableCol = len(col_label)
        #     self.col_label = col_label
        #     self.table.setColumnCount(self.tableCol)
        #     # self.table = QTableWidget(self.tableRow, self.tableCol)
        #     self.table.setHorizontalHeaderLabels(self.col_label)
        #     self.verticalLayout_1.addWidget(self.table)






    # def initTable(self, data):
    #     pass

    def addOther(self):
        style_sheet = """
                    QLineEdit{
                        max-width: 40px
                    }
                    QLabel{
                        font-size: 14px;
                    }
                """
        self.verticalLayout_1 = QVBoxLayout()
        self.__layout = QVBoxLayout()
        self.__layout.addLayout(self.verticalLayout_1)
        self.setStyleSheet(style_sheet)
        self.setLayout(self.__layout)

    def setPageController(self, page):
        """自定义页码控制器"""
        self.control_layout = QHBoxLayout()
        font = QtGui.QFont()
        font.setPixelSize(16)
        homePage = QPushButton("首页")
        prePage = QPushButton("<上一页")
        self.curPage = QLabel("{}".format(self.current_page))
        nextPage = QPushButton("下一页>")
        finalPage = QPushButton("尾页")
        self.totalPage = QLabel("共" + str(page) + "页")
        self.totalNum = QLabel("共" + str(self.totalNum) + "条样本")
        skipLable_0 = QLabel("跳到")
        self.skipPage = QLineEdit()
        intValidator = QIntValidator(self)
        self.skipPage.setValidator(intValidator)
        self.skipPage.setText('1')
        skipLabel_1 = QLabel("页")
        confirmSkip = QPushButton("确定")
        homePage.setFont(font)
        prePage.setFont(font)
        self.curPage.setFont(font)
        nextPage.setFont(font)
        finalPage.setFont(font)
        self.totalPage.setFont(font)
        skipLable_0.setFont(font)
        skipLabel_1.setFont(font)
        confirmSkip.setFont(font)
        homePage.clicked.connect(self.__home_page)
        prePage.clicked.connect(self.__pre_page)
        nextPage.clicked.connect(self.__next_page)
        finalPage.clicked.connect(self.__final_page)
        confirmSkip.clicked.connect(self.__confirm_skip)
        self.control_layout.addStretch(1)
        self.control_layout.addWidget(homePage)
        self.control_layout.addWidget(prePage)
        self.control_layout.addWidget(self.curPage)
        self.control_layout.addWidget(nextPage)
        self.control_layout.addWidget(finalPage)
        self.control_layout.addWidget(self.totalPage)
        self.control_layout.addWidget(self.totalNum)
        self.control_layout.addWidget(skipLable_0)
        self.control_layout.addWidget(self.skipPage)
        self.control_layout.addWidget(skipLabel_1)
        self.control_layout.addWidget(confirmSkip)
        self.control_layout.addStretch(1)
        self.__layout.addLayout(self.control_layout)

    def __home_page(self):
        """点击首页信号"""
        self.control_signal.emit(["home", self.curPage.text()])

    def __pre_page(self):
        """点击上一页信号"""
        self.control_signal.emit(["pre", self.curPage.text()])

    def __next_page(self):
        """点击下一页信号"""
        self.control_signal.emit(["next", self.curPage.text()])

    def __final_page(self):
        """尾页点击信号"""
        self.control_signal.emit(["final", self.curPage.text()])

    def __confirm_skip(self):
        """跳转页码确定"""
        self.control_signal.emit(["confirm", self.skipPage.text()])

    def showTotalPage(self):
        """返回当前总页数"""
        return int(self.totalPage.text()[1:-1])



def show_text(function):
    def wrapped(self, *args, **kwargs):
        if self.vars["showTextLock"]:
            self.vars["showTextLock"] = False
            result = function(self, *args, **kwargs)
            items = self.get_selected()
            # 选中的数量
            l = len(items)
            # 总复选框数量
            l_ = self.vars["listViewModel"].rowCount() - 1
            self.vars["listViewModel"].item(0).setCheckState(
                Qt.Checked if l == l_ else Qt.Unchecked if l == 0 else Qt.PartiallyChecked)
            # set_text = "(全选)" if l == l_ else "(无选择)" if l == 0 else ";".join((item.text() for item in items))
            set_tip = "(未选择)" if l == 0 else "(全选)" if l == l_ else "已添加：\n\t" + "\n\t".join(
                (item.text() for item in items))
            # set_tip = "(全选)" if l == l_ else "(无选择)" if l == 0 else "已添加：\n\t" + "\n\t".join((item.text() for item in items))
            # self.vars["lineEdit"].setText("")
            if self.is_research:
                self.vars["lineEdit"].setPlaceholderText("点击可搜索,移动至此有提示")
            else:
                self.vars["lineEdit"].setPlaceholderText("移动至此显示已添加项目")

            self.vars["lineEdit"].setToolTip(set_tip)
            self.vars["showTextLock"] = True
        else:
            result = function(self, *args, **kwargs)
        return result

    return wrapped


class QComboCheckBox(QComboBox):
    class MyListView(QListView):
        def __init__(self, parent: QWidget = None, vars=None):
            super().__init__(parent)
            self.vars = vars

        def mousePressEvent(self, event: QMouseEvent):
            self.vars["lock"] = False
            super().mousePressEvent(event)

        def mouseDoubleClickEvent(self, event: QMouseEvent):
            self.vars["lock"] = False
            super().mouseDoubleClickEvent(event)

    # tool_bar传入选项list, default_check是否默认全选， np_list(无用), is_research是否在输入框中开启搜索功能
    def __init__(self, tool_bar, default_check=True, np_list=None, is_research=False, index=None, parent: QWidget = None):
        super(QComboCheckBox, self).__init__(parent)
        self.vars = dict()
        self.np_list = np_list
        self.tool_bar = tool_bar
        self.default_check = default_check
        self.vars["lock"] = True
        self.vars["showTextLock"] = True
        # 装饰器锁，避免批量操作时重复改变lineEdit的显示
        self.vars["lineEdit"] = QLineEdit(self)
        self.vars["lineEdit"].setFont(QFont("Arial", 9))
        self.setFocusPolicy(Qt.StrongFocus)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.is_research = is_research
        if not self.is_research:
            self.vars["lineEdit"].setReadOnly(True)
        # self.setEditable(True)
        self.vars["listView"] = self.MyListView(self, self.vars)
        self.vars["listViewModel"] = QStandardItemModel(self)
        self.setModel(self.vars["listViewModel"])
        self.setView(self.vars["listView"])
        self.setLineEdit(self.vars["lineEdit"])
        self.vars['completer'] = QCompleter(self.tool_bar, self)
        self.vars['completer'].setFilterMode(Qt.MatchContains)
        self.vars["lineEdit"].setCompleter(self.vars['completer'])
        self.vars['completer'].setCaseSensitivity(Qt.CaseInsensitive)
        self.activated.connect(self.__show_selected)
        self.setFixedWidth(180)
        self.setMinimumHeight(28)
        self.add_item("(全选)")

        self.add_items(tool_bar)
        self.setCompleter(self.vars['completer'])
        # 设置多选框的最多显示条数
        self.setMaxVisibleItems(4)

        # 设置某些索引为选中的索引
        if index:
            self.select_indexs(index, True)


        i = 0
        for item in tool_bar:
            self.vars["listViewModel"].item(i).setToolTip(item)
            i += 1
        # self.vars["listViewModel"].item(0).setCheckState(True)
        # self.vars["lineEdit"].setPlaceholderText("点击可搜索,移动至此有提示")

    def count(self):
        # 返回子项数
        return super().count() - 1

    @show_text
    def add_item(self, text: "str"):
        # 根据文本添加子项
        item = QStandardItem()
        item.setText(text)
        item.setCheckable(True)
        if self.default_check:
            item.setCheckState(Qt.Checked)
        else:
            # 设置默认全选
            # 设置默认不选中
            item.setCheckState(Qt.Unchecked)
        self.vars["listViewModel"].appendRow(item)

    @show_text
    def add_items(self, texts: "tuple or list"):
        # 根据文本列表添加子项
        for text in texts:
            self.add_item(text)

    @show_text
    def clear_items(self):
        # 清空所有子项
        self.vars["listViewModel"].clear()
        self.add_item("(全选)")

    def find_index(self, index: "int"):
        # 根据索引查找子项
        return self.vars["listViewModel"].item(index if index < 0 else index + 1)

    def find_indexs(self, indexs: "tuple or list"):
        # 根据索引列表查找子项
        return [self.find_index(index) for index in indexs]

    def find_text(self, text: "str"):
        # 根据文本查找子项
        tempList = self.vars["listViewModel"].findItems(text)
        tempList.pop(0) if tempList and tempList[0].row() == 0 else tempList
        return tempList

    def find_texts(self, texts: "tuple or list"):
        # 根据文本列表查找子项
        return {text: self.find_text(text) for text in texts}

    def get_text(self, index: "int"):
        # 根据索引返回文本
        return self.vars["listViewModel"].item(index if index < 0 else index + 1).text()

    def get_texts(self, indexs: "tuple or list"):
        # 根据索引列表返回文本
        return [self.get_text(index) for index in indexs]

    def change_text(self, index: "int", text: "str"):
        # 根据索引改变某一子项的文本
        self.vars["listViewModel"].item(index if index < 0 else index + 1).setText(text)

    @show_text
    def select_index(self, index: "int", state: "bool" = True):
        # 根据索引选中子项，state=False时为取消选中
        self.vars["listViewModel"].item(index if index < 0 else index + 1).setCheckState(
            Qt.Checked if state else Qt.Unchecked)

    @show_text
    def select_indexs(self, indexs: "tuple or list", state: "bool" = True):
        # 根据索引列表选中子项，state=False时为取消选中
        for index in indexs:
            self.select_index(index, state)

    @show_text
    def select_text(self, text: "str", state: "bool" = True):
        # 根据文本选中子项，state=False时为取消选中
        for item in self.find_text(text):
            item.setCheckState(Qt.Checked if state else Qt.Unchecked)

    @show_text
    def select_texts(self, texts: "tuple or list", state: "bool" = True):
        # 根据文本列表选中子项，state=False时为取消选中
        for text in texts:
            self.select_text(text, state)

    @show_text
    def select_reverse(self):
        # 反转选择
        if self.vars["listViewModel"].item(0).checkState() == Qt.Unchecked:
            self.select_all()
        elif self.vars["listViewModel"].item(0).checkState() == Qt.Checked:
            self.select_clear()
        else:
            for row in range(1, self.vars["listViewModel"].rowCount()):
                self.__select_reverse(row)

    def __select_reverse(self, row: "int"):
        item = self.vars["listViewModel"].item(row)
        item.setCheckState(Qt.Unchecked if item.checkState() == Qt.Checked else Qt.Checked)

    @show_text
    def select_all(self):
        # 全选
        for row in range(0, self.vars["listViewModel"].rowCount()):
            self.vars["listViewModel"].item(row).setCheckState(Qt.Checked)

    @show_text
    def select_clear(self):
        # 全不选
        for row in range(0, self.vars["listViewModel"].rowCount()):
            self.vars["listViewModel"].item(row).setCheckState(Qt.Unchecked)

    @show_text
    def remove_index(self, index: "int"):
        # 根据索引移除子项
        return self.vars["listViewModel"].takeRow(index if index < 0 else index + 1)

    @show_text
    def remove_indexs(self, indexs: "tuple or list"):
        # 根据索引列表移除子项
        return [self.remove_index(index) for index in sorted(indexs, reverse=True)]

    @show_text
    def remove_text(self, text: "str"):
        # 根据文本移除子项
        items = self.find_text(text)
        indexs = [item.row() for item in items]
        return [self.vars["listViewModel"].takeRow(index) for index in sorted(indexs, reverse=True)]

    @show_text
    def remove_texts(self, texts: "tuple or list"):
        # 根据文本列表移除子项
        return {text: self.remove_text(text) for text in texts}

    def get_selected(self):
        # 获取当前选择的子项
        items = list()
        for row in range(1, self.vars["listViewModel"].rowCount()):
            item = self.vars["listViewModel"].item(row)
            if item.checkState() == Qt.Checked:
                items.append(item)
        return items

    def is_all(self):
        # 判断是否是全选
        return True if self.vars["listViewModel"].item(0).checkState() == Qt.Checked else False

    def sort(self, order=Qt.AscendingOrder):
        # 排序，默认正序
        self.vars["listViewModel"].sort(0, order)

    @show_text
    def __show_selected(self, index):
        # print(index)
        # print(self.vars["lock"])
        # print('---3---')
        if not self.vars["lock"]:
            if index == 0:
                if self.vars["listViewModel"].item(0).checkState() == Qt.Checked:
                    self.select_clear()
                else:
                    self.select_all()
            else:
                self.__select_reverse(index)

            self.vars["lock"] = True

    def hidePopup(self):
        if self.vars["lock"]:
            super().hidePopup()


# 脑电文件选择列表
class PrentryView(QWidget):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_Prentry()
        self.ui.setupUi(self)

# 标注用户选择列表
class UserView(QWidget):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_Prentry()
        self.ui.setupUi(self)


# 添加标注主题
class AddThemeFormView(QWidget):
    def __init__(self, parent=None,):
        super().__init__(parent)
        self.ui = Ui_addTheme()
        self.ui.setupUi(self)
        # self.state = ['labelling','evaluating','notUsable','usable']

    # def initTabel(self):
    #     # 设置频率值为当前基本配置值
    #     # self.ui.comboConfigId.setText(config_info)
    #     # for item in config_info:
    #     #     self.ui.comboConfigId.addItem(item[1])
    #     for item in self.state:
    #         self.ui.comboBoxState.addItem(item)

# 添加标注主题
class ThemeInfoFormView(QWidget):
    def __init__(self, parent=None,):
        super().__init__(parent)
        self.ui = Ui_themeInfo()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = AddThemeFormView()
    view.show()
    sys.exit(app.exec_())