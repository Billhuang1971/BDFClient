from datetime import datetime

from PyQt5.QtCore import pyqtSignal, Qt

from controller.EEGController import EEGController
from controller.classifier import classifierController
from controller.algorithm import algorithmController
from controller.diagAssess import diagAssessController
from controller.diagTraining import diagTrainingController
from controller.diagTest import diagTestController
from controller.manualQuery import manualQueryController
from controller.modelTest import modelTestController
from controller.reserchingQuery import reserchingQueryController
from controller.sampleState import sampleStateController
from controller.userManager import userManagerController
from controller.reserching import reserchingController
from controller.modelTrain import modelTrainController
from view.main import MainView
from view.init_view import InitView
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from controller.login import loginController
from controller.pwdUpdate import pwdController
from controller.consulting import consultingController

from controller.montage import montageController
from controller.patientManager import patientManagerController

from controller.basicConfig import basicConfigController
from controller.configOptions import configOptionsController
from controller.labelType import labelTypeController
from controller.dataImport import dataImportController
from controller.setBuild import setBuildController
from controller.createCons import createConsController
from controller.createLesson import createLessonController
from controller.taskSettings import taskSettingsController
from controller.manual import manualController
# from controller.detailLook import detailLookController
from controller.auto import autoController
from controller.assessLabel import assessLabelController
from controller.clearLabel import clearLabelController

import sys

_translate = QtCore.QCoreApplication.translate


class MainController(QWidget):
    EEG_FOR_CONSULTING = 0

    # 定义模块切换信号
    switch_signal = pyqtSignal(str)

    def __init__(self, cAppUtil, client):
        super().__init__()
        self.cAppUtil = cAppUtil
        self.client = client

        # 主界面模块视图
        self.view = MainView()

        self.view.show()

        # 当前功能模块控制器
        self.controller = None
        # 当前子模块视图
        self.sub_view = None
        self.previous_controller = None
        self.study_start_time = None
        self.switch_page("LoginController")
        # self.controller.signal_login_user_info.connect(self.userLogin)
        self.client.logoutResSig.connect(self.logoutRes)
        self.client.quitResSig.connect(self.quitRes)
        self.client.serverExceptSig.connect(self.serverExcept)
        self.signalConnection()
        # 用户登录

        # 信号绑定切换操作
        self.switch_signal.connect(self.switch_page)

    def serverExcept(self):
        reply = QMessageBox.information(self, "登录", f'服务器异常', QMessageBox.Yes)
        if reply == 16384:
            app = QApplication.instance()
            app.quit()

    def userLogin(self):
        try:
            self.view.enabel_function_button()
            self.view.setUserPermission(self.client)
            self.view.setPosition(m_name=None, b_name=None)

            self.sub_view = InitView()
            self.view.verticalLayout_1.addWidget(self.sub_view)
            self.controller.disconnect_login()

        except Exception as e:
            print('userLogin', e)

    # 初始化用户权限
    def signalConnection(self):
        self.view.ui.action_UC03.triggered.connect(lambda: self.switch_page("userManagerController"))
        self.view.ui.action_UC03.triggered.connect(lambda: self.view.setPosition('系统菜单', '用户管理'))

        self.view.ui.action_UC02.triggered.connect(lambda: self.switch_page("pwdController"))
        self.view.ui.action_UC02.triggered.connect(lambda: self.view.setPosition('系统菜单', '密码修改'))

        self.view.ui.action_UC04.triggered.connect(lambda: self.view.setPosition('系统菜单', '标注类型'))
        self.view.ui.action_UC04.triggered.connect(lambda: self.switch_page("labelTypeController"))

        self.view.ui.action_UC05.triggered.connect(lambda: self.view.setPosition('系统菜单', '基本设置'))
        self.view.ui.action_UC05.triggered.connect(lambda: self.switch_page("basicConfigController"))

        self.view.ui.action_UC06.triggered.connect(lambda: self.view.setPosition('系统菜单', '配置选择'))
        self.view.ui.action_UC06.triggered.connect(lambda: self.switch_page("configOptionsController"))

        self.view.ui.action_UC07.triggered.connect(lambda: self.view.setPosition('系统菜单', '导联配置'))
        self.view.ui.action_UC07.triggered.connect(lambda: self.switch_page("montageController"))

        self.view.ui.action_UC08.triggered.connect(lambda: self.view.setPosition('系统菜单', '切换用户'))
        self.view.ui.action_UC08.triggered.connect(self.userSwitch)

        self.view.ui.action_UC09.triggered.connect(self.quit)

        self.view.ui.action_UC10.triggered.connect(lambda: self.view.setPosition('日常/远程诊断', '病人管理'))
        self.view.ui.action_UC10.triggered.connect(lambda: self.switch_page("patientManagerController"))

        self.view.ui.action_UC12.triggered.connect(lambda: self.view.setPosition('日常/远程诊断', '导入脑电'))
        self.view.ui.action_UC12.triggered.connect(lambda: self.switch_page("dataImportController"))

        # self.view.ui.action_UC13.triggered.connect(lambda: self.view.setPosition('日常/远程诊断', '标注诊断'))
        # self.view.ui.action_UC13.triggered.connect(lambda: self.switch_page("manualController"))

        self.view.ui.action_UC14.triggered.connect(lambda: self.view.setPosition('日常/远程诊断', '诊断查询'))
        self.view.ui.action_UC14.triggered.connect(lambda: self.switch_page("manualQueryController"))

        self.view.ui.action_UC15.triggered.connect(lambda: self.view.setPosition('日常/远程诊断', '创建会诊'))
        self.view.ui.action_UC15.triggered.connect(lambda: self.switch_page("createConsController"))
        self.view.ui.action_UC16.triggered.connect(lambda: self.view.setPosition('日常/远程诊断', '脑电会诊'))
        self.view.ui.action_UC16.triggered.connect(lambda: self.switch_page("consultingController"))

        self.view.ui.action_UC17.triggered.connect(lambda: self.view.setPosition('脑电诊断培训', '创建课堂'))
        self.view.ui.action_UC17.triggered.connect(lambda: self.switch_page("createLessonController"))

        self.view.ui.action_UC18.triggered.connect(lambda: self.view.setPosition('脑电诊断培训', '诊断学习'))
        self.view.ui.action_UC18.triggered.connect(lambda: self.switch_page("diagTrainingController"))
        self.view.ui.action_UC19.triggered.connect(lambda: self.view.setPosition('脑电诊断培训', '学习测试'))
        self.view.ui.action_UC19.triggered.connect(lambda: self.switch_page("diagTestController"))
        self.view.ui.action_UC20.triggered.connect(lambda: self.view.setPosition('脑电诊断培训', '学习评估'))
        self.view.ui.action_UC20.triggered.connect(lambda: self.switch_page("diagAssessController"))

        self.view.ui.action_UC21.triggered.connect(lambda: self.view.setPosition('脑电科研支撑', '样本统计'))
        self.view.ui.action_UC21.triggered.connect(lambda: self.switch_page("sampleStateController"))
        self.view.ui.action_UC22.triggered.connect(lambda: self.view.setPosition('脑电科研支撑', '任务设置'))
        self.view.ui.action_UC22.triggered.connect(lambda: self.switch_page("taskSettingsController"))
        self.view.ui.action_UC23.triggered.connect(lambda: self.view.setPosition('脑电科研支撑', '科研标注'))
        self.view.ui.action_UC23.triggered.connect(lambda: self.switch_page("reserchingController"))
        self.view.ui.action_UC24.triggered.connect(lambda: self.view.setPosition('脑电科研支撑', '执行查看'))
        self.view.ui.action_UC24.triggered.connect(lambda: self.switch_page("reserchingQueryController"))

        self.view.ui.action_UC25.triggered.connect(lambda: self.view.setPosition('脑电科研支撑', '构建集合'))
        self.view.ui.action_UC25.triggered.connect(lambda: self.switch_page("setBuildController"))

        self.view.ui.action_UC27.triggered.connect(lambda: self.view.setPosition('脑电科研支撑', '算法管理'))
        self.view.ui.action_UC27.triggered.connect(lambda: self.switch_page("algorithmController"))

        self.view.ui.action_UC28.triggered.connect(lambda: self.view.setPosition('脑电科研支撑', '模型训练'))
        self.view.ui.action_UC28.triggered.connect(lambda: self.switch_page("modelTrainController"))

        self.view.ui.action_UC29.triggered.connect(lambda: self.view.setPosition('脑电科研支撑', '模型测试'))
        self.view.ui.action_UC29.triggered.connect(lambda: self.switch_page("modelTestController"))

        self.view.ui.action_UC30.triggered.connect(lambda: self.view.setPosition('脑电科研支撑', '模型管理'))
        self.view.ui.action_UC30.triggered.connect(lambda: self.switch_page("classifierController"))

        self.view.ui.action_UC31.triggered.connect(lambda: self.view.setPosition('脑电科研支撑', '脑电扫描'))
        self.view.ui.action_UC31.triggered.connect(lambda: self.switch_page("autoController"))

        self.view.ui.action_UC32.triggered.connect(lambda: self.view.setPosition('脑电科研支撑', '评估样本'))
        self.view.ui.action_UC32.triggered.connect(lambda: self.switch_page("assessLabelController"))

        self.view.ui.action_UC33.triggered.connect(lambda: self.view.setPosition('脑电科研支撑', '删除样本'))
        self.view.ui.action_UC33.triggered.connect(lambda: self.switch_page("clearLabelController"))

    # 用户切换
    def userSwitch(self):
        if self.previous_controller == 'diagTrainingController':
            studyInfo = self.view.label_5.text()
            if studyInfo is not None and studyInfo != '':
                reply = QMessageBox.information(self, '提示',
                                                "当前正在[诊断学习]中，请先单击[诊断学习]窗口右边的”返回,才能切换用户。",
                                                QMessageBox.Yes)
                return
        reply = QMessageBox.information(self, '提示', '是否需要注销，并登录其他账户',
                                        QMessageBox.Yes | QMessageBox.No)
        if reply == 16384:
            self.view.disabel_function_button()
            self.client.logout('logout')

    # 用户切换回调
    def logoutRes(self, REPData):
        if REPData[0] == '1':
            QMessageBox.information(self, "切换用户", REPData[2], QMessageBox.Yes)
            self.view.label_2.setText(_translate("MainWindow", "当前用户: "))
            self.view.label_3.setText(_translate("MainWindow", "当前身份： "))

            if self.study_start_time != None:
                study_end_time = datetime.now().strftime("%Y-%m-%d :%H:%M:%S")
                msg = [self.class_id, self.client.tUser[0], self.study_start_time, study_end_time]
                self.client.dl_study_end(msg)
                self.study_start_time = None
                self.class_id = None

            self.controller.exit()
            self.controller = None
            self.previous_controller = None
            self.switch_page("LoginController")
            self.view.setPosition('系统菜单', '切换用户')
        else:
            QMessageBox.information(self, "切换用户", REPData[2], QMessageBox.Yes)
            self.view.enabel_function_button()

    # 退出程序

    def quit(self):
        if self.previous_controller == 'diagTrainingController':
            studyInfo = self.view.label_5.text()
            if studyInfo is not None and studyInfo != '':
                reply = QMessageBox.information(self, '提示',
                                                "当前正在[诊断学习]中，请先单击[诊断学习]窗口右边的”返回,再退出。",
                                                QMessageBox.Yes)
                return
        reply = QMessageBox.information(self, '提示', '是否退出程序??', QMessageBox.Yes | QMessageBox.No)
        if reply == 16384:
            self.client.logout('quit')

    def quitRes(self):
        app = QApplication.instance()
        # 退出应用程序
        app.quit()

    # 页面切换
    def switch_page(self, controller_name,msg=None):
        # 切换回主菜单
        if controller_name == 'MainController':
            if self.sub_view is not None:
                self.sub_view.close()
            if self.controller is not None:
                self.controller.exit()
            self.controller=None
            self.generate_controller(controller_name)
            self.sub_view = InitView()
            self.view.verticalLayout_1.addWidget(self.sub_view)
        else:
            if self.previous_controller == 'diagTrainingController':
                studyInfo = self.view.label_5.text()
                if studyInfo is not None and studyInfo != '':
                    reply = QMessageBox.information(self, '提示',
                                                    "当前正在[诊断学习]中，请先单击[诊断学习]窗口右边的”返回,再切换菜单项。",
                                                    QMessageBox.Yes)
                    return


            if self.sub_view is not None:
                self.sub_view.close()

            if self.controller is not None:
                self.controller.exit()
            self.controller=None
            if controller_name == 'EEGController':
                self.generate_controller(controller_name, msg)
            else:
                self.generate_controller(controller_name)


            if self.controller is None:
                QMessageBox.information(self, "系统提示", f'{controller_name}模块在开发中...,暂时不能使用.',
                                        QMessageBox.Yes)
                return
            self.sub_view = self.controller.view


            while self.view.verticalLayout_1.count() > 1:
                witem = self.view.verticalLayout_1.itemAt(self.view.verticalLayout_1.count() - 1)
                witem.widget().hide()
                self.view.verticalLayout_1.removeItem(witem)
            self.sub_view.showMaximized()
            self.view.verticalLayout_1.addWidget(self.sub_view)
            self.previous_controller = controller_name
            self.view.label_4.setText("")

    def generate_controller(self, controller_name,msg=None):
        if controller_name == "LoginController":
            self.controller = loginController(client=self.client, cAppUtil=self.cAppUtil)
            self.controller.signal_login_user_info.connect(self.userLogin)
        elif controller_name == "pwdController":
            self.controller = pwdController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "montageController":
            self.controller = montageController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "labelTypeController":
            self.controller = labelTypeController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "userManagerController":
            self.controller = userManagerController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "patientManagerController":
            self.controller = patientManagerController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "manualController":
            self.controller = manualController(appUtil=self.cAppUtil, Widget=self.view.label_4, client=self.client,
                                               mainMenubar=self.view.ui.menubar)

        elif controller_name == "manualQueryController":
            self.controller = manualQueryController(appUtil=self.cAppUtil, client=self.client)
            self.controller.switchToEEG.connect(self.switchToEEGPage)

        elif controller_name == "basicConfigController":
            self.controller = basicConfigController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "consultingController":
            self.controller = consultingController(appUtil=self.cAppUtil,
                                                   client=self.client)
            self.controller.switchToEEG.connect(self.switchToEEGPage)

        elif controller_name == "diagTrainingController":
            self.controller = diagTrainingController(appUtil=self.cAppUtil, client=self.client)
            self.controller.switchToEEG.connect(self.switchToEEGPage)

        elif controller_name == "diagTestController":
            self.controller = diagTestController(appUtil=self.cAppUtil, client=self.client)
            self.controller.switchToEEG.connect(self.switchToEEGPage)

        elif controller_name == "diagAssessController":
            self.controller = diagAssessController(appUtil=self.cAppUtil, Widget=self.view.label_4,
                                                   client=self.client,
                                                   mainMenubar=self.view.ui.menubar,
                                                   mainLayout=self.view.verticalLayout_1)

        elif controller_name == "reserchingController":
            self.controller = reserchingController(appUtil=self.cAppUtil, Widget=self.view.label_4,
                                                   client=self.client,
                                                   mainMenubar=self.view.ui.menubar,
                                                   mainLayout=self.view.verticalLayout_1)

        elif controller_name == "reserchingQueryController":
            self.controller = reserchingQueryController(appUtil=self.cAppUtil, Widget=self.view.label_4,
                                                        client=self.client,
                                                        mainMenubar=self.view.ui.menubar,
                                                        mainLayout=self.view.verticalLayout_1)

        elif controller_name == "dataImportController":
            self.controller = dataImportController(client=self.client, cAppUtil=self.cAppUtil,mainMenubar=self.view.ui.menubar)
            self.controller.switch_signal.connect(self.switch_signal.emit)

        elif controller_name == "configOptionsController":
            self.controller = configOptionsController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "createConsController":
            self.controller = createConsController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "createLessonController":
            self.controller = createLessonController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "taskSettingsController":
            self.controller = taskSettingsController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "sampleStateController":
            self.controller = sampleStateController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "setBuildController":
            self.controller = setBuildController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "algorithmController":
            self.controller = algorithmController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "modelTrainController":
            self.controller = modelTrainController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "classifierController":
            self.controller = classifierController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "modelTestController":
            self.controller = modelTestController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "autoController":
            self.controller = autoController(client=self.client, cAppUtil=self.cAppUtil)

        elif controller_name == "assessLabelController":
            self.controller = assessLabelController(appUtil=self.cAppUtil, Widget=self.view.label_4, client=self.client,
                                                    mainMenubar=self.view.ui.menubar)

        elif controller_name == "clearLabelController":
            self.controller = clearLabelController(client=self.client, cAppUtil=self.cAppUtil)


    def switchToEEGPage(self, msg):
        if self.sub_view is not None:
            self.sub_view.close()
        if self.controller is not None:
            self.controller.switchToEEG.disconnect()
            self.controller.exit()
        self.controller = None
        self.controller = EEGController(client=self.client, appUtil=self.cAppUtil, msg=msg, mainLabel=self.view.label_4)
        if msg[5][0] == 'diagTrainingController':
            self.class_id = msg[5][2]
            self.study_start_time = datetime.now().strftime("%Y-%m-%d :%H:%M:%S")
        self.controller.switchFromEEG.connect(self.switchFromEEGPage)
        self.sub_view = self.controller.view
        self.view.updateForEEG(self.sub_view)
        self.controller.startEEG()

    def switchFromEEGPage(self, msg):
        controller_name = msg[0]
        if self.sub_view is not None:
            self.sub_view.close()
        if self.controller is not None:
            self.controller.switchFromEEG.disconnect()
            self.controller.exit()
        self.controller = None
        if self.study_start_time != None:
            study_end_time = datetime.now().strftime("%Y-%m-%d :%H:%M:%S")
            msg = [self.class_id, self.client.tUser[0], self.study_start_time, study_end_time]
            self.client.dl_study_end(msg)
            self.study_start_time = None
            self.class_id = None
        if controller_name == "manualQueryController":
            self.controller = manualQueryController(appUtil=self.cAppUtil, client=self.client, page_number=msg[1])

        elif controller_name == "consultingController":
            self.controller = consultingController(appUtil=self.cAppUtil,
                                                   client=self.client, page=msg[1])
        elif controller_name == "diagTrainingController":
            self.controller = diagTrainingController(appUtil=self.cAppUtil, client=self.client)
        elif controller_name == "diagTestController":
            self.controller = diagTestController(appUtil=self.cAppUtil, client=self.client)
        elif controller_name == "diagAssessController":
            self.controller = diagAssessController(appUtil=self.cAppUtil, Widget=self.view.label_4,
                                                   client=self.client,
                                                   mainMenubar=self.view.ui.menubar,
                                                   mainLayout=self.view.verticalLayout_1)
        elif controller_name == "reserchingController":
            self.controller = reserchingController(appUtil=self.cAppUtil, Widget=self.view.label_4,
                                                   client=self.client,
                                                   mainMenubar=self.view.ui.menubar,
                                                   mainLayout=self.view.verticalLayout_1)
        elif controller_name == "reserchingQueryController":
            self.controller = reserchingQueryController(appUtil=self.cAppUtil, Widget=self.view.label_4,
                                                        client=self.client,
                                                        mainMenubar=self.view.ui.menubar,
                                                        mainLayout=self.view.verticalLayout_1)
        self.controller.switchToEEG.connect(self.switchToEEGPage)
        self.sub_view = self.controller.view
        self.view.updateForEEG(self.sub_view)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = MainController()
    sys.exit(app.exec_())
