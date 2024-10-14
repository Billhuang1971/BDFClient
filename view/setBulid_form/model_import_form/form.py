from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt
from functools import partial

from PyQt5.uic.uiparser import QtCore
from pyqt5_plugins.examplebuttonplugin import QtGui


class model_import_view(QDialog):
    import_done = pyqtSignal(str, dict)

    def __init__(self):
        super().__init__()
        # self.is_single = is_single
        self.count = 0
        self.icons = sorted(self.getEnumStrings(QStyle, QStyle.StandardPixmap).items())
        self.sub_model_dict = dict()
        self.last_cls_layout_num = 0
        self.init_view()

    def init_view(self):
        self.setWindowTitle("模型导入")
        self.resize(300, 400)


        self.center_layout = QVBoxLayout()
        self.setLayout(self.center_layout)
        """
            模型
        """
        self.horizontalLayout_1 = QHBoxLayout()
        self.model_address = QLabel("主模型：")
        self.spcify_address = QLabel("")
        self.select_button = QPushButton("选择")
        # spacerItem_1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_1.addWidget(self.model_address)
        self.horizontalLayout_1.addWidget(self.spcify_address)
        self.horizontalLayout_1.addWidget(self.select_button)
        self.horizontalLayout_1.setStretch(1, 1)
        self.center_layout.addLayout(self.horizontalLayout_1)

        font = QFont("Arial", 10)
        spacerItem_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        """
            如果是多模型
        """
        # if not self.is_single:
        control_layout = QHBoxLayout()
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        add_btn = QPushButton()
        add_index, iconinfo = self.icons[1:][51]
        add_btn.setIcon(QApplication.style().standardIcon(int(add_index)))
        add_btn.setToolTip('添加')
        del_btn = QPushButton()
        del_btn.setToolTip('删除')
        del_index, iconinfo = self.icons[1:][50]
        del_btn.setIcon(QApplication.style().standardIcon(int(del_index)))
        control_layout.addItem(spacerItem_5)
        control_layout.addWidget(add_btn)
        control_layout.addWidget(del_btn)
        control_layout.setStretch(0, 1)
        scroll_area = QScrollArea()
        # scroll_area.horizontalScrollBar().setEnabled(False)
        scroll_area.setWidgetResizable(True)
        scrollAreaWidgetContents = QWidget()
        # scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 601, 428))
        self.sub_cls_layout = QVBoxLayout(scrollAreaWidgetContents)
        scroll_area.setWidget(scrollAreaWidgetContents)
        self.center_layout.addWidget(line)
        self.center_layout.addLayout(control_layout)
        self.center_layout.addWidget(scroll_area)
        # self.sub_cls_layout_add()
        add_btn.clicked.connect(self.sub_cls_layout_add)
        del_btn.clicked.connect(self.sub_cls_layout_del)

        """
            确认与重置
        """
        self.horizontalLayout_2 = QHBoxLayout()
        self.comfirm_button = QPushButton("确认")
        self.cancel_button = QPushButton("重置")
        spacerItem_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacerItem_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacerItem_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem_2)
        self.horizontalLayout_2.addWidget(self.comfirm_button)
        self.horizontalLayout_2.addItem(spacerItem_3)
        self.horizontalLayout_2.addWidget(self.cancel_button)
        self.horizontalLayout_2.addItem(spacerItem_4)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(4, 1)
        self.center_layout.addLayout(self.horizontalLayout_2)
        """
            提示
        """
        self.horizontalLayout_5 = QHBoxLayout()
        self.note_tip = QLabel("提示：仅支持pytorch框架")
        self.note_tip.setFont(font)
        self.note_tip.setStyleSheet("color:red")
        spacerItem_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addWidget(self.note_tip)
        self.horizontalLayout_5.addItem(spacerItem_6)
        self.horizontalLayout_5.setStretch(-1, 1)

        self.center_layout.addLayout(self.horizontalLayout_5)

        self.select_button.clicked.connect(lambda: self.file_select(self.spcify_address))
        # self.select_button_2.clicked.connect(lambda: self.file_select(self.spcify_alg_pth))

        self.cancel_button.clicked.connect(self.import_reset)
        self.comfirm_button.clicked.connect(self.import_confirm)

    def import_confirm(self):
        if self.spcify_address.text() == '':
            QMessageBox.information(self, "提示", "尚未导入任何模型！")
            return
        else:
            self.sub_model_dict.clear()
            for i in range(1, self.count + 1):
                sub_model_name = eval("self.sub_model_name_{}.text()".format(i))
                if sub_model_name == '':
                    QMessageBox.information(self, "提示", "尚未导入任何子模型-{}！".format(i))
                    return
                self.sub_model_dict[i] = sub_model_name
            self.import_done.emit(self.spcify_address.text(), self.sub_model_dict)
            self.close()

    def import_reset(self):
        self.spcify_address.setText('')
        for i in range(1, self.count + 1):
            exec("self.sub_model_name_{}.setText('')".format(i))

    def file_select(self, label: QLabel):
        filePath, ok = QFileDialog.getOpenFileName(self, "模型导入", "C:/")
        if ok:
            label.setText(str(filePath))
            self.close()
            self.show()

    def sub_cls_layout_add(self):
        self.count += 1
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        horizontalLayout_1 = QHBoxLayout()

        # exec("horizontalLayout_{}".format(self.count + 5))
        exec("self.verticalLayout_{} = QVBoxLayout()".format(self.count))
        sub_model = QLabel("子模型-{}：".format(self.count))
        exec("self.sub_model_name_{} = QLabel("")".format(self.count))
        # QPushButton
        exec("model_select_button_{} = QPushButton('选择')".format(self.count))
        exec("model_select_button_{}.clicked.connect(partial(self.file_select,self.sub_model_name_{}))".format(
            self.count, self.count))

        # QHBoxLayout.addWidget()
        horizontalLayout_1.addWidget(sub_model)
        exec("horizontalLayout_1.addWidget(self.sub_model_name_{})".format(self.count))
        exec("horizontalLayout_1.addWidget(model_select_button_{})".format(self.count))
        horizontalLayout_1.setStretch(1, 1)
        spacerItem_2 = QSpacerItem(10, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        #
        # horizontalLayout_3.addItem(spacerItem_1)
        # horizontalLayout_3.setStretch(1, 1)
        if self.count != 1:
            exec("self.verticalLayout_{}.addWidget(line)".format(self.count))
            self.clear(self.sub_cls_layout, count=0)

        exec("self.verticalLayout_{}.addLayout(horizontalLayout_1)".format(self.count))
        exec("widget_{} = QWidget()".format(self.count))
        exec("widget_{}.setLayout(self.verticalLayout_{})".format(self.count, self.count))
        exec("self.sub_cls_layout.addWidget(widget_{})".format(self.count))
        self.sub_cls_layout.addItem(spacerItem_2)
        self.last_cls_layout_num = self.sub_cls_layout.count()
        self.sub_cls_layout.setStretch(self.last_cls_layout_num - 1, 0)
        self.sub_cls_layout.setStretch(self.sub_cls_layout.count() - 1, 1)

    def sub_cls_layout_del(self):

        if self.count > 0:
            self.count -= 1
        else:
            return
        spacerItem_1 = QSpacerItem(10, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # count1 = self.sub_cls_layout.count()
        self.clear(self.sub_cls_layout, count=0)
        self.clear(self.sub_cls_layout, count=0)
        self.sub_cls_layout.addItem(spacerItem_1)
        #
        self.sub_cls_layout.setStretch(self.sub_cls_layout.count() - 1, 1)

    # 清理布局
    def clear(self, layout, num=0, count=-1):
        '''
        num: 清除布局中的widget数量,从后往前数
        count：清除倒数第count个的widget
        '''
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

    def getEnumStrings(self, cls, enum):
        s = {}
        for key in dir(cls):
            value = getattr(cls, key)
            if isinstance(value, enum):
                s['{:02d}'.format(value)] = key
        return s

    # def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
    #     print('window closed')
    #     # if not self.is_single:
    #     self.sub_model_dict.clear()
    #     for i in range(1, self.count + 1):
    #         sub_model_name = eval("self.sub_model_name_{}.text()".format(i))
    #         # sub_model_alg_name = eval("self.sub_model_alg_name_{}.text()".format(i))
    #         # sub_model_class_name = eval("self.sub_model_class_name_{}.text()".format(i))
    #         self.sub_model_dict[i] = sub_model_name
    #     self.import_done.emit(self.spcify_address.text(), self.sub_model_dict)
    #     return
    # self.import_done.emit(self.spcify_address.text(), self.spcify_alg_pth.text(), self.alg_class_name.text(), None)
