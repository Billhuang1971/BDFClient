import sys

from PyQt5.QtCore import pyqtSignal

from view.assessLabel_form.assessLabel import Ui_AssessLabelForm
from view.assessLabel_form.prentry import Ui_Prentry
from view.assessLabel_form.setting import Ui_Setting
from PyQt5.QtWidgets import *

class AssessLabelView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AssessLabelForm()
        self.ui.setupUi(self)

    # 显示病人相关信息
    def show_patient_info(self, patient, file_name, measure_date, start_time, end_time, model_name):
        name = patient[0][1]
        birth = str(patient[0][2])
        sex = patient[0][3]
        self.ui.labelPatientName.setText(name)
        self.ui.labelPatientBirth.setText(birth)
        self.ui.labelPatientSex.setText(sex)
        self.ui.labelPatientMeasure.setText(measure_date)
        self.ui.labelFileName.setText(file_name)
        meas_time = str(start_time) + ' - ' + str(end_time)
        self.ui.labelMeasureTime.setText(meas_time)
        self.ui.modelName.setText(model_name)

    # 显示样本信息
    def show_sample_detail(self, model_name='', mtype_name='', channel='', lent='', begin='', end='', amp='', user_name='', utype_name=''):
        try:
            self.ui.labelModel.setText(model_name)
            self.ui.labelMType.setText(mtype_name)
            self.ui.labelRole.setText(user_name)
            self.ui.labelUType.setText(utype_name)

            self.ui.labelChannel.setText(channel)
            if lent != '':
                lent = str(round(float(lent), 3))
            self.ui.labelLength.setText(lent)
            self.ui.labelBegin.setText(begin)
            self.ui.labelEnd.setText(end)
            if amp != '':
                amp = str(round(float(amp), 3))
            self.ui.labelAmp.setText(amp)
        except Exception as e:
            print('show_sample_detail', e)

class SettingView(QWidget):
    def __init__(self, type_name, model_name, type_filter, model_filter, parent=None):
        super().__init__(parent)
        self.ui = Ui_Setting()
        self.ui.setupUi(self, type_name, model_name, type_filter, model_filter)

class PrentryView(QWidget):
    page_control_signal = pyqtSignal(list)

    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_Prentry()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.__home_page)
        self.ui.pushButton_2.clicked.connect(self.__pre_page)
        self.ui.pushButton_3.clicked.connect(self.__next_page)
        self.ui.pushButton_4.clicked.connect(self.__final_page)
        self.ui.pushButton_5.clicked.connect(self.__confirm_skip)

    def __home_page(self):
        """点击首页信号"""
        self.page_control_signal.emit(["home", self.ui.label.text()])

    def __pre_page(self):
        """点击上一页信号"""
        self.page_control_signal.emit(["pre", self.ui.label.text()])

    def __next_page(self):
        """点击下一页信号"""
        self.page_control_signal.emit(["next", self.ui.label.text()])

    def __final_page(self):
        """尾页点击信号"""
        self.page_control_signal.emit(["final", self.ui.label.text()])

    def __confirm_skip(self):
        """跳转页码确定"""
        self.page_control_signal.emit(["confirm", self.ui.lineEdit.text()])

