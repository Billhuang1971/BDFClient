import ctypes
import inspect
import json
import math
import os.path
import pickle
import threading
from datetime import datetime

import mne
import numpy as np
from PyQt5.Qt import *
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QRect, QDateTime, QTimer
from PyQt5.QtGui import QBrush, QFont
from PyQt5.QtWidgets import *
from view.dataImport import DataImportView
from view.dataImport import AddFormView
import pyedflib
import re
import datetime

from view.dataImport_form.loadingform import LoadingDialog
from view.dataImport_form.patient_table import PatientTableWidget
from view.dataImport_form.doctor_table import DoctorTableWidget
from view.progressBarView import ProgressBarView
from PyQt5.QtCore import QRegularExpression


class dataImportController(QWidget):
    # 上传信号
    uploadFileSig = pyqtSignal()
    # 进度条相关信号
    upload_finished = pyqtSignal()
    upload_failed = pyqtSignal()
    # 定义切换信号
    switch_signal = pyqtSignal(str)
    # update_process = pyqtSignal(int)
    def __init__(self, client, cAppUtil, mainMenubar=None):
        super().__init__()

        self.client = client
        self.cAppUtil = cAppUtil
        self.view = DataImportView()
        self.mainMenubar = mainMenubar
        self.root_path = os.path.dirname(os.path.dirname(__file__))+'\\'
        # 存放处理过后的脑电文件上级目录
        self.EEG_path = os.path.join(self.root_path, 'upload', 'EEG')
        # 存放处理过后的脑电文件目录,在addUserFolder中得到拼接
        self.dir_path = None

        # 存放用户内存等待队列文件的上级目录
        self.wait_path = os.path.join(self.root_path,'upload','EEGQueue')
        # 存放等待队列文件的目录，在addUserFolder中得到拼接
        self.wait_dir_path = None
        # 内存中等待队列文件
        self.queue_file_path = None
        # 引入线程锁
        self.lock = threading.Lock()
        self.client.getPatientCheckInfoResSig.connect(self.getPatientCheckInfoRes)
        self.client.delPatientCheckInfoResSig.connect(self.delPatientCheckInfoRes)
        self.client.addCheckInfoResSig.connect(self.addCheckInfoRes)
        self.client.checkConfigResSig.connect(self.checkConfigRes)
        self.client.getUserConfigResSig.connect(self.getUserConfigRes)
        self.client.makeFileNameResSig.connect(self.makeFileNameRes)
        self.client.writeEEGResSig.connect(self.writeEEGRes)
        self.client.updateCheckInfoResSig.connect(self.updateCheckInfoRes)
        self.client.getFileInfoResSig.connect(self.getFileInfoRes)
        self.client.delFileInfoResSig.connect(self.delFileInfoRes)
        self.client.getChoosePatientInfoResSig.connect(self.get_choose_patient_infoRes)
        self.client.getChooseDoctorInfoResSig.connect(self.get_choose_doctor_infoRes)
        self.uploadFileSig.connect(self.upload_startCall)


        # 如果服务端出现异常关闭当前界面的所有线程
        self.client.serverExceptSig.connect(self.upload_failedCall)


        # 进度条值
        # 全局变量
        self.progress_value = 0

        #进度条对象
        self.progressBarView = None
        self.is_uploading = False  # 标志是否终止上传
        self.is_processing = False # 标志是否正在处理
        self.processing_lock = threading.Lock()


        # 存放当前标注类型信息列表
        self.patientCheck_info = []
        # 存放脑电数据信息列表
        self.file_info = []
        # 存放所有医生信息
        self.doctor = []
        # 存放所有病人
        self.patient = []

        # 当前文件的类型（sEEG/EEG）
        self.file_type = None

        # 当前选择行索引
        self.row = -1
        # 用来保存文件每次传的块大小(5M)
        self.block_size = 5*1024*1024
        # 用来存放当前文件大小
        self.block_num = None
        # 存放选中需要转换的脑电文件路径
        self.from_filepath = None
        # 存放传感器字段修复后的edf文件名
        self.repair_filepath = None
        # 增加bdf文件转化为edf文件后的新文件名
        self.convert_filepath = None
        # 存放返回的脑电文件名字
        self.file_path = None
        # 存放获取的文件名
        self.filename = None
        # 存放需要处理的第一条记录中的文件名
        self.fileName = None
        # 存放要上传的脑电文件check_id
        self.check_id = None
        # 存放要上传文件的file_id
        self.file_id = None
        # 存放用户当前config_id
        self.config_id = self.client.tUser[12]
        # 存放当前check_id的file_info信息
        # TODO:这个change_file最好换个名字,意味不明
        self.change_file = None
        # 内存中等待队列
        self.wait_file = []
        # 每页的样本最大数量
        self.perPageNum = 13
        # 初始进入时即对文件夹进行操作
        self.addUserFolder()
        # 获取表格的信息
        self.getPatientCheckInfo()

        # 获取当前用户的配置信息
        self.getUserConfig()

        # 获取内存等待文件
        self.initWaitFile()

        self.upload_finished.connect(self.upload_finishedCall)
        # upload_failedCall在程序里没有调用
        self.upload_failed.connect(self.upload_failedCall)


        # 进入界面設置菜单栏不可用
        self.mainMenubar.setDisabled(True)

        # # 只能选中一行
        self.view.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.ui.tableWidget.resizeRowsToContents()
        self.view.ui.tableWidget.resizeColumnsToContents()
        self.view.ui.tableWidget.clicked.connect(self.on_tableWidget_itemClicked)


        self.view.ui.tableWidget_2.setSelectionMode(QAbstractItemView.NoSelection)
        self.view.ui.tableWidget_2.resizeRowsToContents()
        self.view.ui.tableWidget_2.resizeRowsToContents()
        self.view.ui.tableWidget_2.resizeColumnsToContents()

        # 存储添加的信息
        self.addInfo = {}

        # 添加部分的槽函数链接
        # 设置选择医生
        self.view.ui.patientBtn.clicked.connect(self.onChoose_Patient)
        # self.addFormView.ui.patientBtn.clicked.connect(self.onChoose_Patient)
        self.view.ui.pdoctorBtn.clicked.connect(self.onChoose_Doctor)
        # self.addFormView.ui.pdoctorBtn.clicked.connect(self.onChoose_Doctor)

        # 设置选中病人
        # self.view.ui.btnConfirm.clicked.connect(self.onClick_ButtonToText)
        self.view.ui.btnConfirm.clicked.connect(self.on_btnConfirmAdd_clicked)
        self.view.ui.btnExit.clicked.connect(self.on_btnCancelAdd_clicked)

        # 设置当前上传脑电医生
        self.view.ui.label_cdoctor.setText(self.client.tUser[2])


        # 设置启动上传和退出上传的绑定事件
        self.view.ui.startUploadButton.clicked.connect(self.on_btnUploadStart_clicked)
        # self.view.ui.exitUploadButton.clicked.connect(self.on_btnReturn_clicked)
        # 按钮点击时发送切换信号
        self.view.ui.exitUploadButton.clicked.connect(self.on_btnExitUpload_clicked)

        # 暂存当前用户的config配置
        self.userConfig_info = []

    def on_btnExitUpload_clicked(self):
        # 返回前检查UserFolder
        self.delUserFolder()
        # 发射切换信号，切换到 MainController
        self.switch_signal.emit("MainController")
        # 打开主菜单
        self.mainMenubar.setEnabled(True)

    def delUserFolder(self):
        # 对self.dir_path判空，为空说明无待续传文件，删除该空文件夹；否则不做处理直接退出
        if self.cAppUtil.isNull(self.dir_path):
            # 确保路径存在
            if os.path.exists(self.dir_path):
                os.rmdir(self.dir_path)  # 删除空文件夹
        # 对queue_file_path判空，如果退出的时候当前用户不存在待上传文件了，就要把当前文件夹删除
        if self.cAppUtil.isNull(self.queue_file_path):
            os.remove(self.queue_file_path)
            if os.path.exists(self.wait_dir_path):
                os.rmdir(self.wait_dir_path)  # 删除空文件夹


    def addUserFolder(self):
        account = self.client.tUser[1] # 获取用户账户名称
        self.dir_path = os.path.join(self.EEG_path, account)  # 拼接完整的用户文件夹路径
        # 1.对upload/EEG下的文件夹进行遍历，查找是否存在以当前account命名的文件夹
        # 2.若存在，直接退出，否则创建该文件夹后退出
        # 检查目录是否存在，如果不存在则创建
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
        self.wait_dir_path = os.path.join(self.wait_path, account)
        if not os.path.exists(self.wait_dir_path):
            os.makedirs(self.wait_dir_path)
        self.queue_file_path = os.path.join(self.wait_dir_path, 'pending.json')

    def showMessageBoxwithTimer(self, title, message, close_time=5000, buttons=QMessageBox.Ok):
        """
        显示一个自动关闭的 QMessageBox，确保其不会闪烁。

        :param title: 窗口标题
        :param message: 消息内容
        :param close_time: 自动关闭时间（毫秒）
        :param buttons: 显示的按钮，例如 QMessageBox.Ok, QMessageBox.Yes | QMessageBox.No
        """
        # 创建消息框
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(buttons)

        # 创建定时器
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(msg_box.accept)  # 触发关闭消息框
        timer.start(close_time)

        # 显示消息框并进入事件循环
        msg_box.exec_()

    def initWaitFile(self):
        # 加载现有的任务队列
        if os.path.exists(self.queue_file_path):
            with open(self.queue_file_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    self.wait_file = data.get("task", [])
                except json.JSONDecodeError:
                    print("队列文件格式错误，初始化为空队列")
        else:
            print(f"未找到队列文件，创建新文件：{self.queue_file_path}")

    def long_task_with_dialog(self, post_callback=None):
        self.loading_dialog = LoadingDialog("正在转换 EDF 文件，请稍候...", self)
        self.loading_dialog.show()

        QApplication.processEvents()  # 强制 UI 刷新

        QTimer.singleShot(100, lambda: self._do_actual_work(post_callback))

    def _do_actual_work(self, post_callback=None):
        try:
            self.convert_edf_to_bdf()
            self.from_filepath = self.convert_filepath
            if post_callback:
                post_callback()
        finally:
            self.loading_dialog.close()
            self.loading_dialog = None

    # 测下这里上传的edf文件
    def on_btnAddFile_clicked(self, row):
        if self.row == -1:
            QMessageBox.information(self, ' ', '请先在病人诊断信息中选择一行')
            return

        get_filename_path, ok = QFileDialog.getOpenFileName(self,
                                                            "导入病人文件",
                                                            "C:/",
                                                            "脑电文件 (*.edf *.bdf *.txt)")
        if ok:
            self.from_filepath = get_filename_path
            file_extension = os.path.splitext(self.from_filepath)[1].lower()

            if file_extension == '.bdf':
                self.checkBasicConfig()

            elif file_extension == '.edf':
                # 转换完成后再执行 checkBasicConfig
                self.long_task_with_dialog(post_callback=self.checkBasicConfig)

            else:
                QMessageBox.information(self, "不支持的文件类型", "请上传有效的脑电文件格式 (.edf /.bdf).")
                return

    def checkBasicConfig(self):
        # 判断
        try:
            raw = mne.io.read_raw_bdf(self.from_filepath)
            self.duration = raw.n_times / raw.info['sfreq']
            # 存储源文件采样点数
        except Exception as e:
            # self.format_failedInport.emit()
            print('读取未成功', e)
            return

        account = self.client.tUser[1]
        user_id = self.client.tUser[0]
        check_id = self.patientCheck_info[self.row][0]
        mac = self.cAppUtil.getMacAddress()

        filemsg = ['', check_id, '', mac, self.config_id]
        freq = raw.info['sfreq']
        REQmsg = [account, user_id, filemsg, freq]
        self.client.checkConfig(REQmsg)

    def checkConfigRes(self, REPData):
        try:
            if REPData[0] == '1':
                userConfig = REPData[3][0]
                self.userConfig_info = userConfig
                print('userConfig', userConfig)
                # 获取check_number
                check_number = self.patientCheck_info[self.row][5]
                # 添加新任务到内存队列
                self.addWaitFile(check_number)
                # 这个位置有没有必要在内存等待队列文件中新增？到时候点击启动上传会更新
                self.addPending(check_number)

            elif REPData[0] == '2':
                QMessageBox.information(self, "配置检查", REPData[2], QMessageBox.Yes)
            else:
                QMessageBox.information(self, "配置检查", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('checkConfigRes', e)

    def getUserConfig(self):
        account = self.client.tUser[1]
        REQmsg = [account, self.config_id]
        self.client.getUserConfig(REQmsg)

    # 第二次进入重新获取UserConfig
    def getUserConfigRes(self, REPData):
        print("REPData:", REPData)
        try:
            if REPData[0] == '1':
                self.userConfig_info = REPData[3][0]
                print('userConfig:', self.userConfig_info)
            else:
                print('状态码非1:', REPData[0])
        except Exception as e:
            print('getUserConfigRes 错误:', e)

    def addWaitFile(self,check_number):
        # 添加新任务到内存队列
        new_task = {
            "check_number": check_number,
            "fileName": self.from_filepath
        }
        self.wait_file.append(new_task)
        print("新纪录已添加到wait_file:", self.wait_file)
        # 添加完成即刷新表格，无需等到点击item再刷新
        check_number = self.patientCheck_info[self.row][5]
        if self.wait_file:
            filtered_data = [
                [task["fileName"], "notUploaded"]  # 你需要展示的列数据
                for task in self.wait_file
                if task["check_number"] == check_number
            ]
            # 初始化第一个表格 （新加）
            self.view.initTable_1(filtered_data, on_btnDelFile_clicked=self.on_btnDelFile_clicked)

    def addPending(self,check_number):
        # 添加新任务到pending.json
        new_task = {
            "check_number": check_number,
            "fileName": self.from_filepath
        }
        if not os.path.exists(self.queue_file_path):
            print(f"{self.queue_file_path} 不存在，创建新文件")
            with open(self.queue_file_path, 'w', encoding='utf-8') as file:
                json.dump({"task": []}, file, ensure_ascii=False, indent=4)

        # 加载文件内容
        with open(self.queue_file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print(f"{self.queue_file_path} 格式错误，重置为空队列")
                data = {"task": []}

        # 添加新记录
        data["task"].append(new_task)
        # 保存回文件
        with open(self.queue_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("新记录已添加到文件")



    # 删除服务端已上传的所有文件 与该脑电检查相关的所有记录 删除与该脑电检查对应的所有待传任务
    def on_btnRemove_clicked(self,row):
        if self.row != -1:
            self.row = self.view.ui.tableWidget.currentRow()
            # 找到当前检查信息的脑电上传医生
            print("这里的patientCheckInfo:",self.patientCheck_info)
            pdoctorname = self.patientCheck_info[self.row][3]
            if pdoctorname == self.client.tUser[0]:
                answer = QMessageBox.warning(
                    self.view, '确认删除！', '您将进行删除操作！',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if answer == QMessageBox.Yes:
                    if self.row == -1:
                        QMessageBox.information(self.view, ' ', '请先选中一行')
                        return
                    # 暂时只能选中一行删除
                    print('row', self.row)
                    check_id = self.patientCheck_info[self.row][0]
                    account = self.client.tUser[1]
                    REQmsg = [account, check_id, self.row]
                    # 在这里删除了当前行 需要将ui界面上的待上传文件清空并将wait_file中属于该检查单号的文件删除
                    # 清空客户端待上传文件列表
                    self.view.ui.tableWidget_1.setRowCount(0)
                    self.view.ui.tableWidget_1.clearContents()

                    # 清空对应的wait_file中的任务和pending中对应的任务
                    check_number = self.patientCheck_info[self.row][5]
                    self.removeWaitFile(check_number)

                    self.row = -1

                    # 如果当前有上传到一半的任务进行检查单号的删除，upload/EEG中有文件残留
                    # 这个残留如果要删除的话需要做判断，如果check_id相吻合，需要删除
                    if not self.cAppUtil.isNull(self.dir_path):
                        bdfFileNameList = self.findFile(self.dir_path, '.bdf')
                        bdfFileName = bdfFileNameList[0]
                        # 匹配 _ 之前的数字，并去掉前导零
                        match = re.match(r"0*(\d+)_", bdfFileName)
                        if match:
                            check_id1 = int(match.group(1))
                            if check_id1 == check_id:
                                # 同时删除当前未上传完成的脑电文件
                                self.cAppUtil.empty(self.dir_path, filename=bdfFileName)

                    # 删除病人检查信息
                    self.client.delPatientCheckInfo(REQmsg)
                else:
                    return
            else:
                QMessageBox.information(self.view, '提示', '你不是本次检查的脑电上传医生，你无权进行删除！！！')
        else:
            QMessageBox.information(self, ' ', '请先在病人诊断信息中选择一行')
            return

    # 删除指定的wait_file,会连带着删除Pending中对应的记录
    def removeWaitFile(self,check_number):
        print("传入的check_number：", check_number)

        # 判断check_number是否在wait_file中
        if not any(task["check_number"] == check_number for task in self.wait_file):
            print(f"当前检查单号不存在待上传任务，删除完成")
            return  # 如果没有找到任务，说明当前检查单号还未创建上传任务，直接返回，不进行删除操作

        original_length = len(self.wait_file)
        print("未删除前的wait_file:", self.wait_file)
        self.wait_file = [task for task in self.wait_file if task["check_number"] != check_number]
        # 输出删除结果
        if len(self.wait_file) < original_length:
            print(f"任务 {check_number} 已成功从wait_file中删除")
            print("当前wait_file:", self.wait_file)
            # self.wait_file中删除也要从pending.json中删除
            self.removePending(check_number)
        else:
            print(f"未找到任务 {check_number}，删除失败")

    # 删除指定pending.json
    def removePending(self,check_number):
        try:
            # 读取 JSON 文件
            with open(self.queue_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # 过滤掉指定 check_number 的任务
            data['task'] = [task for task in data['task'] if task['check_number'] != check_number]
            # 将更新后的数据写回到文件
            with open(self.queue_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"成功删除{check_number}对应的task")
        except Exception as e:
            print(f"从pending.json中删除task有误: {e}")

    # 修改一下逻辑，先判断能否点击完成，再进行下列判断，也就是把当前两个提示的顺序修改一下，“是否上传完毕？”的提示放在最后
    # fixme:多个检查单号，无法点击第二个”完成“ 暂未复现
    def on_btnComplete_clicked(self,row):
        if self.row == -1:
            QMessageBox.information(self, ' ', '请先在病人诊断信息中选择一行')
            return

        # 先获取远程服务器是否存在已上传完成的脑电文件
        self.getFileInfo()
        # 已上传文件不为空
        if self.change_file:
            check_number = self.patientCheck_info[self.row][5]
            # pending.json中含有文件未上传，无法正常更新状态
            # 若当前内存等待队列中存在未上传完成的文件，需要提醒用户进行上传后再点击完成按钮
            exists = any(task["check_number"] == check_number for task in self.wait_file)
            if exists:
                    QMessageBox.information(self,"当前检查单号存在待上传文件",
                                            f"请正确上传后再点击完成按钮以完成上传或直接删除当前待上传文件！！",QMessageBox.Yes)
            else:
                reply = QMessageBox.information(self, "检查id病人脑电上传状态",
                                        f"当前检查单号为：{str(self.patientCheck_info[self.row][5])},脑电文件是否上传完毕？",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == 16384:
                    # 用户正常上传完成后正确更新状态
                    # 更新服务端状态
                    uid = self.client.tUser[0]
                    account = self.client.tUser[1]
                    check_id = self.patientCheck_info[self.row][0]
                    state = 'uploaded'
                    REQmsg = [account, 'Send', [check_id, state, uid]]
                    self.client.updateCheckInfo(REQmsg)
        # 已上传文件为空，提醒用户删除当前病人检查信息
        else:
            QMessageBox.information(self, "当前检查单号无已上传文件",
                                    f"无法完成当前病人检查信息状态的更新，请上传文件或删除当前信息！！", QMessageBox.Yes)

    # 更新病人检查信息返回
    def updateCheckInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                msg = f"当前检查单号为：{str(self.patientCheck_info[self.row][5])}\n病人：{self.patientCheck_info[self.row][self.view.field.index('pname') + 4]}\n脑电文件已经上传完毕！！！"

                self.view.ui.groupBox_4.setEnabled(True)
                # 直接从数据库获取然后更新，毕竟可能会出现一种大部分信息都添加的情况
                self.getPatientCheckInfo()
            else:
                QMessageBox.information(self, "病人检查", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('updateCheckInfoRes', e)

    def on_btnDelFile_clicked(self,row):
        file_to_delete = self.wait_file[row]
        print(f"删除文件: {file_to_delete['fileName']}")

        # 从 wait_file 中移除
        del self.wait_file[row]
        print(f"当前wait_file:", self.wait_file)

        # 从 pending.json 中删除相应的条目
        try:
            # 读取 pending.json 文件
            with open(self.queue_file_path, 'r', encoding='utf-8') as file:
                pending_data = json.load(file)

            # 删除对应 check_number 和 fileName 的条目
            new_task_list = [
                task for task in pending_data["task"]
                if not (task["check_number"] == file_to_delete["check_number"] and task["fileName"] == file_to_delete[
                    "fileName"])
            ]

            # 更新 pending.json 中的数据
            pending_data["task"] = new_task_list

            # 写回更新后的数据到 pending.json
            with open(self.queue_file_path, 'w', encoding='utf-8') as newfile:
                json.dump(pending_data, newfile, ensure_ascii=False, indent=4)

            print(f"从 pending.json 中删除了文件: {file_to_delete['fileName']}")

        except FileNotFoundError:
            print(f"文件 {self.queue_file_path} 未找到。")
        except json.JSONDecodeError:
            print(f"读取 {self.queue_file_path} 时发生错误。")

        # 更新表格
        # 最好是把这个更新表格的操作给抽出来，另外，在wait_file中删除可以先不动那个内存等待队列文件，到时点击启动上传有更新操作
        check_number = self.patientCheck_info[self.row][5]
        if self.wait_file:
            filtered_data = [
                [task["fileName"], "notUploaded"]  # 你需要展示的列数据
                for task in self.wait_file
                if task["check_number"] == check_number
            ]
            # 初始化第一个表格 （新加）
            self.view.initTable_1(filtered_data, on_btnDelFile_clicked=self.on_btnDelFile_clicked)
        # wait_file被清除，需要清空列表
        else:
            # 清空服务端待上传文件列表
            self.view.ui.tableWidget_1.setRowCount(0)
            self.view.ui.tableWidget_1.clearContents()



    # 响应点击病人诊断信息列表
    def on_tableWidget_itemClicked(self):
        self.row = self.view.ui.tableWidget.currentRow()
        if self.row != -1:
            check_id = self.patientCheck_info[self.row][0]
            check_number = self.patientCheck_info[self.row][5]
            if self.wait_file:
                filtered_data = [
                    [task["fileName"], "notUploaded"]  # 你需要展示的列数据
                    for task in self.wait_file
                    if task["check_number"] == check_number
                ]
                # 初始化第一个表格 （新加）
                self.view.initTable_1(filtered_data,on_btnDelFile_clicked=self.on_btnDelFile_clicked)
            else:
                # 清空客户端待上传文件列表
                self.view.ui.tableWidget_1.setRowCount(0)
                self.view.ui.tableWidget_1.clearContents()

            if self.change_file:
                if check_id in self.change_file.keys():
                    # 初始化第二个表格（原有）
                    self.view.initTable_2(self.change_file[check_id])
                else:
                    # 清空客户端已有文件表
                    self.view.ui.tableWidget_2.setRowCount(0)
                    self.view.ui.tableWidget_2.clearContents()
            else:
                # 清空客户端已有文件表
                self.view.ui.tableWidget_2.setRowCount(0)
                self.view.ui.tableWidget_2.clearContents()

    def on_btnUploadStart_clicked(self):
        self.view.ui.groupBox_3.setEnabled(False)
        self.view.ui.groupBox_4.setEnabled(False)
        self.view.ui.groupBox.setEnabled(False)
        self.view.ui.startUploadButton.setEnabled(False)

        # 用内存等待队列更新内存等待队列文件
        self.updatePending()

        # client_root/upload/EEG为空
        if self.cAppUtil.isNull(self.dir_path):
            # client_root/upload/EEGQueue/pending.json不为空
            if not self.cAppUtil.isNull(self.queue_file_path):
                # 1.先生成文件名
                account = self.client.tUser[1]
                user_id = self.client.tUser[0]
                # 选取第一条记录
                try:
                    with open(self.queue_file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)  # 加载 JSON 文件内容
                        # 检查 "task" 键是否存在且有数据
                        if "task" in data and data["task"]:
                            check_number = data["task"][0].get("check_number")  # 获取第一条记录的 check_number
                except Exception as e:
                    print("pickJson",e)

                REQmsg = [account, user_id, check_number]
                if self.is_processing:
                    print("上一个文件正在处理中...")
                    return
                self.client.makeFileName(REQmsg)
            # client_root/upload/EEGQueue/pending.json为空
            else:
                # 更新内存等待队列
                self.wait_file = []
                (QMessageBox.information(self, "启动上传",
                                            "当前暂无待上传文件，请选定待文件后进行上传！！！",
                                            QMessageBox.Yes))
                # 刷新界面
                # 清空客户端待上传文件列表
                self.view.ui.tableWidget_1.setRowCount(0)
                self.view.ui.tableWidget_1.clearContents()

                # 重新获取病人检查信息
                self.getPatientCheckInfo()

                # 打开所有功能键
                self.view.ui.groupBox_3.setEnabled(True)
                self.view.ui.groupBox_4.setEnabled(True)
                self.view.ui.groupBox.setEnabled(True)
                self.view.ui.startUploadButton.setEnabled(True)

        # client_root/upload/EEG不为空（被中断上传的文件只可能有一个）
        else:
            # 续传提示
            self.showMessageBoxwithTimer(
                title='续传提示',
                message='系统正在处理未完成的上传任务，完成后才能启动新的上传任务！此消息将在5秒内自动关闭',
                close_time=5000
            )
            # findFile返回不带后缀的文件名列表
            bdfFileNameList = self.findFile(self.dir_path,'.bdf')
            bdfFileName = bdfFileNameList[0]
            self.filename = bdfFileName
            self.file_path = os.path.join(self.dir_path , bdfFileName + str('.bdf'))
            ret = self.testEEGFile(self.file_path)
            # 对BDF文件名做拆解
            parts = bdfFileName.split('_')
            if len(parts) == 2:
                # 去掉前导零并将字符串转换为整数再转回字符串
                self.check_id = int(parts[0])
                self.file_id = int(parts[1])
            # bdf文件完整
            if ret[0] == '1':
                txtFileName = self.findSameFile(self.dir_path , bdfFileName + str('.txt'))
                # 存在同名的txt文件,判断是否完整
                if txtFileName:
                    try:
                        with open(os.path.join(self.dir_path , bdfFileName + str('.txt')), 'rb') as file:
                            data = pickle.load(file)
                        self.check_id = data['check_id']
                        self.file_id = data['file_id']
                        mac = str(data['mac'])
                        # .txt文件完整
                        # 重启进度条
                        self.progressBarView = ProgressBarView(window_title="上传过程出错，系统将从出错位置开始继续上传",
                                                               hasStopBtn=True,
                                                               maximum=100,
                                                               speed=100)
                        self.progressBarView.ui.stop_pushButton.clicked.connect(self.on_btnUploadExit_clicked)
                        self.progressBarView.show()
                        REQmsg = self.packMsg('continue', mac)
                        # 续传需要self.block_num和self.filename 上传标志置为true
                        self.is_uploading = True
                        self.block_num = math.ceil((os.stat(self.file_path).st_size) / self.block_size)
                        self.filename = bdfFileName
                        self.client.writeEEG(REQmsg)
                    except Exception as e:
                        # .txt文件不完整
                        # 重启进度条
                        self.progressBarView = ProgressBarView(window_title="上传过程出错，系统将从出错位置开始继续上传",
                                                               hasStopBtn=True,
                                                               maximum=100,
                                                               speed=100)
                        self.progressBarView.ui.stop_pushButton.clicked.connect(self.on_btnUploadExit_clicked)
                        self.progressBarView.show()
                        # 将续传标志置为True
                        self.is_uploading = True
                        REQmsg = self.packMsg('clean')
                        self.client.writeEEG(REQmsg)
                # 不存在同名的txt文件
                else:
                    # 重启进度条
                    self.progressBarView = ProgressBarView(window_title="上传过程出错，系统将从出错位置开始继续上传",
                                                           hasStopBtn=True,
                                                           maximum=100,
                                                           speed=100)
                    self.progressBarView.ui.stop_pushButton.clicked.connect(self.on_btnUploadExit_clicked)
                    self.progressBarView.show()
                    # 转到步骤4开始上传 正在上传标志置为true
                    self.is_uploading = True
                    self.block_num = math.ceil((os.stat(self.file_path).st_size) / self.block_size)
                    # 这个地方虽然是需要存入原始路径，但由于数据库中没有这个字段并且这是重新上传，其实不传也没关系
                    self.makeText(original_filepath="")
                    REQmsg = self.packMsg(state='start')
                    self.client.writeEEG(REQmsg)
            else:
                # bdf文件损坏
                self.showMessageBoxwithTimer(
                    title='重传提示',
                    message='本地预处理file_name的过程出错，上传过程需重新开始！此消息将在5秒内自动关闭',
                    close_time=5000
                )
                # 删除脑电记录和脑电文件
                self.cAppUtil.empty(self.dir_path, filename = bdfFileName)
                account = self.client.tUser[1]
                REQmsg = [account,self.check_id,self.file_id]
                self.client.delFileInfo(REQmsg)
                # 打开所有功能键
                self.view.ui.groupBox_3.setEnabled(True)
                self.view.ui.groupBox_4.setEnabled(True)
                self.view.ui.groupBox.setEnabled(True)
                self.view.ui.startUploadButton.setEnabled(True)

    def delFileInfoRes(self,REPData):
        print("delFileInfoRes:",REPData)
        # 更新file_info展示
        self.getFileInfo()

    # 判断.bdf文件是否损坏
    def testEEGFile(self, testfile):
        try:
            # 加载 BDF 文件
            local_raw = mne.io.read_raw_bdf(testfile, preload=False)
        except Exception as err:
            ret = ['0', '打开EEG文件无效', testfile]
            return ret
        try:
            # 提取文件头部信息
            local_sampling_rate = local_raw.info['sfreq']  # 采样率
            local_n_times = local_raw.n_times  # 总采样点数
            local_duration = local_n_times / local_sampling_rate  # 计算总时长（秒）
            # 提取文件的测量日期和时间
            meas_date = local_raw.info['meas_date']
            # 检查 meas_date 是否是 tuple
            if isinstance(meas_date, tuple):
                meas_date = datetime.datetime.fromtimestamp(meas_date[0], tz=datetime.timezone.utc)  # 转换为 datetime 对象
            elif isinstance(meas_date, datetime.datetime):
                meas_date = meas_date  # 如果已经是 datetime，直接使用
            else:
                raise ValueError("Invalid meas_date format")

            local_start_time = meas_date.strftime('%H:%M:%S')  # 开始时间
            local_end_time = meas_date + datetime.timedelta(seconds=local_duration)
            local_end_time = local_end_time.strftime('%H:%M:%S')  # 结束时间

            print( f"文件总时长: {local_duration:.2f} 秒, 开始时间: {local_start_time}, 结束时间: {local_end_time}, 采样率: {local_sampling_rate} Hz")
        except Exception as err:
            ret = ['0', '读取文件头部信息异常', testfile]
            return ret
        try:
            # 测试读取完整数据
            raw_copy = local_raw.copy()
            raw_copy.crop(tmin=0, include_tmax=True)
            raw_copy.load_data()
            data, times = raw_copy[:]
            print('data.shape:', data.shape)
            print('times:', times)
            ret = ['1', f'文件测试成功，总时长: {local_duration:.2f} 秒']
            return ret
        except Exception as e:
            ret = ['0', f'读取数据块失败: {e}.']
            return ret


    # 查找某一路径指定文件后缀文件名
    def findFile(self, filepath, suffix):
        # 获取文件夹下所有文件
        fileslist = os.listdir(filepath)
        fileName = []
        # 遍历文件夹中的文件
        for file in fileslist:
            if file.endswith(suffix):  # 判断文件名是否以指定的文件名开头
                fileName.append(file.split('.')[0])
        return fileName  # 返回不带后缀的文件名

    # 查找同名文件
    def findSameFile(self, filepath, fileName):
        # 获取文件夹下所有文件
        fileslist = os.listdir(filepath)
        # 遍历文件夹中的文件
        for file in fileslist:
            if file == fileName:
                return True
        return False

    def updatePending(self):
        # 用内存等待队列更新内存等待队列文件
        with open(self.queue_file_path, 'w', encoding='utf-8') as file:
            json.dump({"task": self.wait_file}, file, ensure_ascii=False, indent=4)

    # MakeFileName会初始化文件名的相关变量
    def makeFileNameRes(self, REPData):
        with self.processing_lock:
            if self.is_processing:
                print("正在处理任务，跳过文件名生成")
                return
            self.is_processing = True  # 设置处理中标志

        try:
            # 初始化文件名相关变量
            self.filename = REPData[3][0]
            self.file_id = REPData[3][1]
            self.check_id = REPData[3][2]
            self.make_filepath(self.filename)

            print("生成的文件名（self.file_path）是：", self.file_path)

            # 加载 JSON 队列中的第一个任务
            with open(self.queue_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if "task" in data and data["task"]:
                    self.fileName = data["task"][0].get("fileName")  # 获取第一条记录
                    if not self.fileName:
                        raise ValueError("队列中的任务文件名无效！")

            # 开始处理文件
            # 这里给出一个分支
            self.process_bdf(self.userConfig_info, self.fileName)

        except Exception as e:
            print("makeFileNameRes 错误：", e)
        finally:
            with self.processing_lock:
                self.is_processing = False  # 重置状态

    def standardize_channels(self, channels):
        """
        标准化导联名称：
        1. 将导联名称转为大写；
        2. 去掉最后一个空格之前的内容（如果存在）。
        3. 如果包含 '-' 且不包含 '-REF'，将 '-' 替换为 '_'；
        4. 如果不包含 '-REF'，则在末尾加上 '-REF'；
        """
        new_channels = []
        for ch in channels:
            temp = ch.upper()  # 转为大写
            if ' ' in temp:  # 去掉最后一个空格之前的内容
                temp = temp[temp.rfind(' ') + 1:]

            # 如果包含 '-' 且不包含 '-REF'，将 '-' 替换为 '_'
            if temp.find('-') > 0 and temp.find('-REF') < 0:
                temp = temp.replace("-", "_")

            # 如果不包含 '-REF'，在末尾加上 '-REF'
            if '-REF' not in temp:
                temp = temp + '-REF'

            # 添加到新列表
            new_channels.append(temp)

        return new_channels


    def process_bdf(self, userConfig_info, filename):
        # 初始化进度条
        self.progressBarView = ProgressBarView(window_title="正在处理文件",
                                               hasStopBtn=True,
                                               maximum=100,
                                               speed=100)
        self.progressBarView.ui.stop_pushButton.clicked.connect(self.on_btnUploadExit_clicked)
        self.progressBarView.show()

        sampling_rate = userConfig_info[0]
        notch = userConfig_info[1]
        low_pass = userConfig_info[2]
        high_pass = userConfig_info[3]

        standard_128_channels = ['C29-REF', 'F1-REF', 'C15-REF', 'A4-REF', 'T8-REF', 'C26-REF', 'T9-REF', 'C31-REF', 'F2-REF', 'D22-REF',
         'EKG-REF', 'FC3-REF', 'F9-REF', 'T6-REF', 'D14-REF', 'A7-REF', 'A11-REF', 'B32-REF', 'TP10-REF', 'A16-REF',
         'CMS-REF', 'D31-REF', 'B19-REF', 'A13-REF', 'FC1-REF', 'A24-REF', 'D20-REF', 'FT9-REF', 'C18-REF', 'PO10-REF',
         'FC2-REF', 'A1-REF', 'CP4-REF', 'D21-REF', 'D4-REF', 'FCZ-REF', 'B29-REF', 'P3-REF', 'D8-REF', 'A27-REF',
         'A23-REF', 'B28-REF', 'C30-REF', 'C23-REF', 'FACIAL-REF', 'F6-REF', 'B14-REF', 'CP5-REF', 'P8-REF', 'O1-REF',
         'B1-REF', 'P6-REF', 'F10-REF', 'T5-REF', 'INION-REF', 'D17-REF', 'VEOG-REF', 'IZ-REF', 'PO7-REF',
         'C22-REF', 'FPZ-REF', 'TP9-REF', 'AF7-REF', 'A17-REF', 'C28-REF', 'HEOG-REF', 'A29-REF', 'IBI-REF', 'D11-REF',
         'D7-REF', 'FZ-REF', 'TP8-REF', 'C7-REF', 'B4-REF', 'B2-REF', 'C4-REF', 'B5-REF', 'D9-REF', 'D25-REF',
         'D19-REF', 'D1-REF', 'B13-REF', 'CZ-REF', 'A21-REF', 'D13-REF', 'C25-REF', 'PO2-REF', 'T7-REF', 'B11-REF',
         'B31-REF', 'POZ-REF', 'I2-REF', 'D28-REF', 'PO5-REF', 'C32-REF', 'C5-REF', 'D18-REF', 'B18-REF', 'A19-REF',
         'F7-REF', 'AF5-REF', 'C11-REF', 'PO8-REF', 'FC4-REF', 'B9-REF', 'B23-REF', 'C12-REF', 'C16-REF', 'EOG-REF',
         'FP1-REF', 'NZ-REF', 'B8-REF', 'D2-REF', 'D24-REF', 'D32-REF', 'F3-REF', 'M2-REF', 'F4-REF', 'HEART-REF',
         'F8-REF', 'A20-REF', 'C1-REF', 'B10-REF', 'C8-REF', 'P7-REF', 'P5-REF', 'B25-REF', 'D23-REF', 'FC5-REF',
         'F5-REF', 'A8-REF', 'AFZ-REF', 'EMG-REF', 'CPZ-REF', 'A10-REF', 'C19-REF', 'A3-REF', 'D29-REF', 'D12-REF',
         'EYE-REF', 'C20-REF', 'A6-REF', 'PO1-REF', 'DRL-REF', 'D30-REF', 'D6-REF', 'P10-REF', 'MUSCLE-REF', 'CP3-REF',
         'O2-REF', 'AFZ-REF', 'PZ-REF', 'A5-REF', 'A14-REF', 'B16-REF', 'OZ-REF', 'B17-REF', 'B20-REF', 'B27-REF',
         'JAW-REF', 'A12-REF', 'P1-REF', 'I1-REF', 'A15-REF', 'B30-REF', 'B21-REF', 'A25-REF', 'B7-REF', 'AF8-REF',
         'AF4-REF', 'AF6-REF', 'D5-REF', 'FT7-REF', 'A9-REF', 'A28-REF', 'A31-REF', 'B24-REF', 'D26-REF', 'P9-REF',
         'C10-REF', 'A26-REF', 'C24-REF', 'PO9-REF', 'C17-REF', 'ECG-REF', 'BURST-REF', 'C6-REF', 'B22-REF', 'C27-REF',
         'B12-REF', 'C14-REF', 'D15-REF', 'CP1-REF', 'FP2-REF', 'C9-REF', 'TP7-REF', 'A32-REF', 'SUPPR-REF', 'FT10-REF',
         'FT8-REF', 'AF1-REF', 'PO3-REF', 'CP2-REF', 'D3-REF', 'FC6-REF', 'B26-REF', 'AF3-REF', 'D10-REF', 'T3-REF',
         'P2-REF', 'T4-REF', 'AF2-REF', 'D27-REF', 'B15-REF', 'C13-REF', 'CARDIO-REF', 'C2-REF', 'PO4-REF', 'B3-REF',
         'D16-REF', 'CP6-REF', 'M1-REF', 'A22-REF', 'C3-REF', 'T10-REF', 'A30-REF', 'P4-REF', 'A18-REF',
         'A2-REF', 'PO6-REF', 'C21-REF', 'B6-REF', 'LDELT1-REF', 'LDELT2-REF', 'RDELT1-REF', 'RDELT2-REF','L_DELT1-REF', 'L_DELT2-REF', 'R_DELT1-REF', 'R_DELT2-REF',
         'T1-REF', 'U1-REF', 'U2-REF', 'EMG3-REF', 'X7-REF', 'X5-REF', 'EMG2-REF', 'EMG1-REF','EMG4-REF', 'X6-REF'
         ]
        # 标准头皮电极通道列表

        is_ieeg = True  # 默认为颅内脑电

        try:
            raw = mne.io.read_raw_bdf(filename)
            with pyedflib.EdfReader(filename) as f:
                n_channels = f.signals_in_file  # 获取通道数
                physical_mins = []
                physical_maxs = []

                # 遍历每个通道，获取 physical_min 和 physical_max
                for i in range(n_channels):
                    physical_min = f.getPhysicalMinimum(i)
                    physical_max = f.getPhysicalMaximum(i)
                    prefilter = f.getPrefilter(i)  # 获取每个通道的预处理信息（如 HP, LP, N）
                    physical_mins.append(physical_min)
                    physical_maxs.append(physical_max)
                    print(f"Channel {i}: Physical Min = {physical_min}, Physical Max = {physical_max}")

                # 判断是否为头皮脑电
                channels = raw.info['ch_names']
                # 检查是否有包含 'EEG' 前缀的通道
                if any('EEG' in ch for ch in channels):
                    # 筛选掉包含 'EEG' 前缀的通道
                    non_eeg_channels = [ch for ch in channels if ch.startswith('EEG')]
                    judge_channels = self.standardize_channels(non_eeg_channels)  # 调用标准化函数
                # 不存在包含‘EEG’前缀的通道时不对通道做筛选处理
                else:
                    judge_channels = self.standardize_channels(channels)  # 调用标准化函数
                # 检查 channels 中的每个通道是否都在 standard_128_channels 中
                if set(judge_channels).issubset(set(standard_128_channels)):
                    is_ieeg = False
                    self.file_type = 'EEG'
                else:
                    is_ieeg = True
                    self.file_type = 'sEEG'
                print('当前is_ieeg的值是：',is_ieeg)

                # 从列表里把最大值和最小值拎出来
                Physical_Min = min(physical_mins)
                Physical_Max = max(physical_maxs)
                # 关闭文件
                f.close()
        except Exception as e:
            print('raw read error', e)
            return

        try:
            freq = raw.info['sfreq']
            duration = int(raw.n_times // freq)
            meas_date = raw.info['meas_date']
            if isinstance(meas_date, tuple):
                meas_date = datetime.datetime.fromtimestamp(meas_date)

            # 获取导联名称并进行标准化处理
            channels = raw.info['ch_names']
            new_channels = self.standardize_channels(channels)  # 调用标准化函数

            # 重命名导联
            raw.rename_channels(dict(zip(channels, new_channels)))  # 原通道和新通道

            # 获取映射后的通道名列表
            channels = new_channels

            stack_size = 3600
            turn = math.ceil(duration / stack_size)

            prefilter = ('HP:{}Hz LP:{}Hz N:NoneHz'.format(high_pass, low_pass))

            signal_headers = pyedflib.highlevel.make_signal_headers(channels,
                                                                    physical_min=Physical_Min,
                                                                    physical_max=Physical_Max,
                                                                    digital_min=-8388608,  # 24位格式的数字最小值
                                                                    digital_max=8388607,  # 24位格式的数字最大值
                                                                    # physical_max=6368.439, physical_min=-6337.78
                                                                    sample_rate=sampling_rate,
                                                                    # sample_rate=freq,
                                                                    # sample_frequency=sampling_rate,
                                                                    prefiler=prefilter
                                                                    )
            # 创建文件头
            header = pyedflib.highlevel.make_header(startdate=meas_date)
            header['recording_additional'] = "EEG" if not is_ieeg else "IEEG"
            with pyedflib.EdfWriter(self.file_path, file_type=pyedflib.FILETYPE_BDF, n_channels=len(channels)) as writer:
                writer.setSignalHeaders(signal_headers)
                writer.setHeader(header)
                for i in range(turn):
                    raw_copy = raw.copy()
                    start = i * stack_size
                    if i == turn - 1:
                        t_raw = raw_copy.crop(tmin=start, include_tmax=True)
                    else:
                        end = start + stack_size
                        t_raw = raw_copy.crop(tmin=start, tmax=end, include_tmax=True)
                    t_raw.load_data()
                    t_raw.filter(l_freq=high_pass, h_freq=low_pass)  # 带通滤波
                    t_raw.notch_filter(freqs=notch)
                    t_raw.resample(sampling_rate, npad='auto')
                    # channels应该是索引或通道的名称列表，而不是字符串列表。如果channels是导联名称列表，应该用mne.pick_channels来获取对应的索引
                    # t_signals, t_times = t_raw[channels, :]
                    # 获取选定通道的数据
                    index_channels = mne.pick_channels(t_raw.info['ch_names'], include=channels)
                    t_signals, t_times = t_raw[index_channels, :]  # 按通道提取信号数据
                    del t_raw

                    t_signals = t_signals * (pow(10, 6))
                    writer.writeSamples(t_signals)
                    del t_signals

                    temp = math.ceil(100 / turn)
                    if self.progress_value + temp < 100:
                        self.progress_value += temp
                    else:
                        self.progress_value = 100
                    # 每个turn更新进度条
                    self.progressBarView.updateProgressBar(self.progress_value)
                # 关闭文件
                writer.close()
                # BDF文件标志的查看方法
                # 打开 BDF 文件
                with pyedflib.EdfReader(self.file_path) as reader:
                    # 内部属性包含 recording 字段
                    recording_field = reader.recording
                    print("Recording Field:", recording_field)
                # 转换为字符串
                recording_str = recording_field.decode("ascii")
                # 提取最后一个部分（按空格分割后取最后一个部分）
                recording_additional = recording_str.split()[-1]
                print("Extracted Recording Additional Info:", recording_additional)

                # 关闭文件
                reader.close()

                # 处理完成关闭进度条
                self.progressBarView.close()
                print("处理完成")
                # self.is_processing = False
                # 释放信号，正式上传脑电文件
                self.uploadFileSig.emit()


        except Exception as e:
            print('process_bdf', e)
            return
        return

    # 正式上传脑电文件
    def upload_startCall(self):
        if self.is_uploading:
            print("当前正在上传文件，无法启动新的上传任务")
            return
        # 开始上传 需要把标志置为true ,续传同理
        self.is_uploading = True
        self.block_num = math.ceil((os.stat(self.file_path).st_size) / self.block_size)
        REQmsg = self.packMsg(state='start')
        self.client.writeEEG(REQmsg)

    # 打包消息格式[account, [脑电文件消息]]
    def packMsg(self, state='', block_id=None, data='', mac=''):
        REQmsg = []
        account = self.client.tUser[1]
        config_id = self.config_id
        file_type = self.file_type
        # TODO：动态获取config_id,注释该行
        if mac != '':
            mac = mac
        else:
            mac = self.cAppUtil.getMacAddress()

        if state == 'start':
            filemsg = ['EEGUpload', state, self.check_id, self.file_id, mac, config_id, file_type]
        elif state == 'uploading':
            filemsg = ['EEGUpload',state, self.check_id, self.file_id, mac, block_id, data]
        elif state == 'uploaded':
            filemsg = ['EEGUpload',state, self.check_id, self.file_id, mac, block_id]
        elif state == 'clean':
            filemsg = ['EEGUpload',state, self.check_id, self.file_id, mac]
        elif state == 'continue':
            filemsg = ['EEGUpload',state, self.check_id, self.file_id, mac]
        else:
            pass
        REQmsg = [account, filemsg]
        return REQmsg

    def unpack(self, REPData):
        result = REPData[0]
        repFilemsg = REPData[3][1:]
        # print("REPDATA[3]",REPData[3])
        # print("REPDATA[3][1:]",REPData[3][1:])
        # print("看看服务端传回来的消息格式：",REPData)
        return result, repFilemsg


    def delPending(self,json_path):
        with self.lock:
            try:
                # 读取 JSON 文件
                with open(json_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                # 检查 "task" 是否存在且有内容
                if "task" in data and isinstance(data["task"], list) and data["task"]:
                    # 删除第一条记录
                    removed_task = data["task"].pop(0)
                    print(f"Removed task: {removed_task}")
                    # 获取被删除记录中的 fileName
                    original_filepath = removed_task.get("fileName")
                    # 写回 JSON 文件
                    with open(json_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, indent=4, ensure_ascii=False)

                    return original_filepath
                    print("第一条记录被成功删除")
                else:
                    return None
                    print("没有记录可以删除")
            except Exception as e:
                return None
                print("delPending:", e)

    def makeText(self,original_filepath):
        # 创建上传的文件记录
        uploading_name = self.filename + '.txt'
        uploading_path = os.path.join(self.dir_path, uploading_name)
        mac = self.cAppUtil.getMacAddress()
        title = ['check_id', 'file_id', 'mac','path']
        fileMsg = [self.check_id, self.file_id, mac ,original_filepath]
        writeMsg = dict(zip(title, fileMsg))
        with open(uploading_path, 'wb') as f:
            pickle.dump(writeMsg, f)

    def writeEEGRes(self, REPData):
        result, repFilemsg = self.unpack(REPData)
        # 在writeEEGRes的回调信息里，是在继续进行上传操作的 把上传标志置为True
        if not self.is_uploading:
            print("上传终止！")
            return
        try:
            if result == '1':
                state = repFilemsg[0]
                print("state:",state)
                # 脑电文件传输协议6.1情况
                if state == 'waiting':
                    block_id = repFilemsg[1]
                    # block_id为1时删除第一条记录
                    if block_id == 1:
                        self.is_uploading = True
                        # 这里加一个条件判断 问题在于：如果本身就打算上传两个相同的文件呢？
                        # uploading.txt不存在
                        if not self.findFile(self.dir_path,'txt'):
                            # 删除第一条记录并创建txt文件
                            original_filepath = self.delPending(self.queue_file_path)
                            self.makeText(original_filepath)
                            # 开启进度条
                            # 初始化进度条
                            self.progressBarView = ProgressBarView(window_title="正在上传文件",
                                                                   hasStopBtn=True,
                                                                   maximum=100,
                                                                   speed=100)
                            self.progressBarView.ui.stop_pushButton.clicked.connect(self.on_btnUploadExit_clicked)
                            # self.progressBarView.stop_signal.connect(self.stop_upload)  # 连接停止信号
                            self.progressBarView.show()
                        # uploading.txt文件存在
                        else:
                            # FIXME:其实续传完全可以不进行校对、删除操作
                            # 说明是续传，因此需要对pending.json中的第一条记录做校对，若一致进行删除操作，否则不进行删除
                            with open(self.queue_file_path, 'r', encoding='utf-8') as file:
                                data = json.load(file)
                                if data["task"]:
                                    if "task" in data and data["task"]:
                                        fileName = data["task"][0].get("fileName")  # 获取第一条记录
                                    if fileName:
                                        if fileName == self.fileName:
                                            self.delPending(self.queue_file_path)
                                        else:
                                            print("当前续传任务并不存在于JSON文件中！！")
                                    else:
                                        print("当前续传任务后无待上传任务！！")
                                else:
                                    print("当前续传任务后无待上传任务！！")
                        # 请求文件块数超出文件总块数情况
                        if block_id > self.block_num:
                            REQmsg = self.packMsg('uploaded', block_id)
                            self.client.writeEEG(REQmsg)
                        else:
                            # 先更新进度条
                            self.progress_value = int((block_id / self.block_num ) * 100)
                            self.progressBarView.updateProgressBar(self.progress_value)
                            EEGdata = self.cAppUtil.readByte(self.file_path, self.block_size, block_id)
                            REQmsg = self.packMsg('uploading', block_id, EEGdata)
                            self.client.writeEEG(REQmsg)
                    else:
                        # 请求文件块数超出文件总块数情况
                        if block_id > self.block_num:
                            REQmsg = self.packMsg('uploaded', block_id)
                            self.client.writeEEG(REQmsg)
                        else:
                            # 先更新进度条
                            self.progress_value = int((block_id / self.block_num) * 100)
                            self.progressBarView.updateProgressBar(self.progress_value)
                            EEGdata = self.cAppUtil.readByte(self.file_path, self.block_size, block_id)
                            REQmsg = self.packMsg('uploading', block_id, EEGdata)
                            self.client.writeEEG(REQmsg)

                # 脑电文件传输协议6.2情况
                elif state == 'wrongSite' or state == 'unknownError' or state == 'cleaned' or state == 'wrongServer':
                    # 清空上传错误的脑电文件及其对应记录,正常关闭进度条后给出提示
                    self.cAppUtil.empty(self.dir_path, filename=self.filename)
                    if hasattr(self, 'progressBarView'):
                        self.progressBarView.close()
                    self.progress_value = 0
                    QMessageBox.information(self, "脑电文件上传",
                                            "脑电文件上传出错，已删除上传记录和处理过后的脑电文件！！！",
                                            QMessageBox.Yes)
                    # 该脑电文件无法上传(另一种意义上的上传完成)
                    self.upload_finished.emit()

                # 脑电文件传输协议6.3情况
                elif state == 'wrongBlock':
                    block_id = repFilemsg[1]
                    EEGdata = self.cAppUtil.readByte(self.file_path, self.block_size, block_id)
                    REQmsg = self.packMsg('uploading', block_id, EEGdata)
                    self.client.writeEEG(REQmsg)

                # 脑电文件传输协议6.4情况
                elif state == 'uploaded':
                    self.cAppUtil.empty(self.dir_path, filename=self.filename)
                    # 上传完成关闭进度条
                    if hasattr(self, 'progressBarView'):
                        self.progressBarView.close()
                    self.progress_value = 0
                    # QMessageBox.information(self, '上传完成！', '脑电文件上传完成,并且已经删除本地已经处理过后的文件！')
                    self.showMessageBoxwithTimer(
                        title='上传完成',
                        message='脑电文件上传完成,并且已经删除本地已经处理过后的文件！此消息将在5秒内自动关闭',
                        close_time=5000
                    )
                    self.view.initTable(self.patientCheck_info, on_btnAddFile_clicked = self.on_btnAddFile_clicked, on_btnRemove_clicked = self.on_btnRemove_clicked ,on_btnComplete_clicked = self.on_btnComplete_clicked)
                    # 更新File_info表展示
                    self.getFileInfo()
                    self.is_uploading = False
                    # 上传完成，释放上传完成信号
                    self.upload_finished.emit()

                # 脑电文件传输协议6.5情况
                elif state == 'recover':
                    # self.check_id = repFilemsg[1]
                    # self.file_id = repFilemsg[2]
                    fileNameList = self.findFile(self.dir_path, 'txt')
                    fileName = fileNameList[0]
                    # 存在已损坏的uploading.txt文件，删除后重新创建， 否则直接创建
                    if fileName:
                        self.cAppUtil.empty(self.dir_path, fullname = fileName + str('.txt'))
                    # 这个地方虽然是需要存入原始路径，但由于数据库中没有这个字段并且这是recover，其实不传也没关系
                    self.makeText(original_filepath="")
                    REQmsg = self.packMsg('continue')
                    self.client.writeEEG(REQmsg)

                else:
                    print(f'状态{state}:暂时无法处理服务器传回的这个状态！！！')
            else:
                if len(REPData) > 2:
                    QMessageBox.information(self, "脑电文件上传", REPData[2], QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "脑电文件上传", REPData[1], QMessageBox.Yes)
        except Exception as e:
            print('writeEEGRes', e)

    def upload_finishedCall(self):
        with self.lock:  # 加锁以保护队列访问
            if self.is_processing:
                print("文件处理尚未完成，跳过")
                return
            # client_root/upload/EEG为空
            if self.cAppUtil.isNull(self.dir_path):
                # client_root/upload/EEGQueue/pending.json不为空
                if not self.cAppUtil.isNull(self.queue_file_path):
                    # 1.先生成文件名
                    account = self.client.tUser[1]
                    user_id = self.client.tUser[0]
                    # 选取第一条记录
                    try:
                        with open(self.queue_file_path, 'r', encoding='utf-8') as file:
                            data = json.load(file)  # 加载 JSON 文件内容
                            # 检查 "task" 键是否存在且有数据
                            if "task" in data and data["task"]:
                                check_number = data["task"][0].get("check_number")  # 获取第一条记录的 check_number
                    except Exception as e:
                        print("pickJson", e)

                    REQmsg = [account, user_id, check_number]
                    if self.is_processing:
                        print("上一个文件正在处理中...")
                        return
                    self.client.makeFileName(REQmsg)
                # client_root/upload/EEGQueue/pending.json为空
                else:
                    # 更新内存等待队列
                    self.wait_file = []
                    (QMessageBox.information(self, "上传完成",
                                             "当前待上传文件上传完成，可重新选择文件上传！！！",
                                             QMessageBox.Yes))

                    self.is_uploading = False
                    # 刷新界面
                    # 清空服务端待上传文件列表
                    self.view.ui.tableWidget_1.setRowCount(0)
                    self.view.ui.tableWidget_1.clearContents()
                    # self.view.initTable(self.patientCheck_info, on_btnAddFile_clicked=self.on_btnAddFile_clicked,
                    #                     on_btnRemove_clicked=self.on_btnRemove_clicked,
                    #                     on_btnComplete_clicked=self.on_btnComplete_clicked)
                    # 打开所有功能键
                    self.view.ui.groupBox_3.setEnabled(True)
                    self.view.ui.groupBox_4.setEnabled(True)
                    self.view.ui.groupBox.setEnabled(True)
                    self.view.ui.startUploadButton.setEnabled(True)


            # client_root/upload/EEG不为空（被中断上传的文件只可能有一个）
            else:
                # 续传提示
                self.showMessageBoxwithTimer(
                    title='续传提示',
                    message='系统正在处理未完成的上传任务，完成后才能启动新的上传任务！此消息将在5秒内自动关闭',
                    close_time=5000
                )
                # 检查脑电文件是否完整
                # findFile返回不带后缀的文件名列表
                bdfFileNameList = self.findFile(self.dir_path, '.bdf')
                bdfFileName = bdfFileNameList[0]
                self.file_path = os.path.join(self.dir_path, bdfFileName + str('.bdf'))
                ret = self.testEEGFile(self.file_path)
                # bdf文件完整
                # 对BDF文件名做拆解
                parts = bdfFileName.split('_')
                if len(parts) == 2:
                    # 去掉前导零并将字符串转换为整数再转回字符串
                    self.check_id = str(int(parts[0]))
                    self.file_id = str(int(parts[1]))
                if ret[0] == '1':
                    txtFileName = self.findSameFile(self.dir_path, bdfFileName + str('.txt'))
                    # 存在同名的txt文件,判断是否完整
                    if txtFileName:
                        try:
                            with open(os.path.join(self.dir_path, bdfFileName + str('.txt')), 'rb') as file:
                                data = pickle.load(file)
                            self.check_id = data['check_id']
                            self.file_id = data['file_id']
                            mac = str(data['mac'])
                            self.fileName = data['path']
                            # .txt文件完整
                            # 重启进度条
                            self.progressBarView = ProgressBarView(window_title="上传过程出错，系统将从出错位置开始继续上传",
                                                                   hasStopBtn=False,
                                                                   maximum=100,
                                                                   speed=100)
                            self.progressBarView.ui.stop_pushButton.clicked.connect(self.on_btnUploadExit_clicked)
                            self.progressBarView.show()
                            REQmsg = self.packMsg('continue', mac)
                            # 续传需要self.block_num和self.filename 上传标志置为true
                            self.is_uploading = True
                            self.block_num = math.ceil((os.stat(self.file_path).st_size) / self.block_size)
                            self.filename = bdfFileName
                            self.client.writeEEG(REQmsg)
                        except Exception as e:
                            # .txt文件不完整
                            # 重启进度条
                            self.progressBarView = ProgressBarView(window_title="上传过程出错，系统将从出错位置开始继续上传",
                                                                   hasStopBtn=False,
                                                                   maximum=100,
                                                                   speed=100)
                            self.progressBarView.ui.stop_pushButton.clicked.connect(self.on_btnUploadExit_clicked)
                            self.progressBarView.show()
                            # 这个位置，txt文件损坏，怎么获取check_id,file_id? 协议6.5的位置，存入check_id、file_id这个位置要再推敲一下，否则容易存入其他check_id和file_id
                            # 该情况下是存在完整bdf文件的，根据BDF文件的命名可以获取到check_id和file_id
                            REQmsg = self.packMsg('clean')
                            self.client.writeEEG(REQmsg)
                    # 不存在同名的txt文件
                    else:
                        # 同样的道理，该情况下是存在完整bdf文件的，根据BDF文件的命名可以获取到check_id和file_id
                        # 重启进度条
                        self.progressBarView = ProgressBarView(window_title="上传过程出错，系统将从出错位置开始继续上传",
                                                               hasStopBtn=False,
                                                               maximum=100,
                                                               speed=100)
                        self.progressBarView.ui.stop_pushButton.clicked.connect(self.on_btnUploadExit_clicked)
                        self.progressBarView.show()
                        # 转到步骤4开始上传
                        self.block_num = math.ceil((os.stat(self.file_path).st_size) / self.block_size)
                        REQmsg = self.packMsg(state='start')
                        self.client.writeEEG(REQmsg)
                # bdf文件损坏
                self.showMessageBoxwithTimer(
                    title='重传提示',
                    message='本地预处理file_name的过程出错，上传过程需重新开始！此消息将在5秒内自动关闭',
                    close_time=5000
                )
                self.cAppUtil.empty(self.dir_path, fullname=bdfFileName + str('.bdf'))
                # 打开所有功能键
                self.view.ui.groupBox_3.setEnabled(True)
                self.view.ui.groupBox_4.setEnabled(True)
                self.view.ui.groupBox.setEnabled(True)
                self.view.ui.startUploadButton.setEnabled(True)

    def stop_upload(self):
        """终止上传"""
        # 终止上传 把上传标志置为False
        self.is_uploading = False
        self.is_processing = False
        print("终止上传逻辑被触发")
        if self.progressBarView:
            self.progressBarView.close()
        # 重置进度条对象
        self.progress_value = 0
        self.progressBarView = None
        QMessageBox.information(self, "提示", "上传任务已终止！")

    def on_btnUploadExit_clicked(self):
        """终止上传"""
        answer = QMessageBox.warning(
            self.view, '确认退出上传！', '其他功能界面会被打开！',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if answer == QMessageBox.Yes:
            if hasattr(self, 'progressBarView') and self.progressBarView is not None:
                self.progressBarView.close()
            # 重置进度条对象
            self.progressBarView = None
            self.progress_value = 0
            # 终止上传 把上传标志置为False
            self.is_uploading = False
            self.is_processing = False
            # 终止上传 把上传标志置为False
            print("终止上传逻辑被触发")

            # 打开主菜单
            self.mainMenubar.setEnabled(True)

            # 打开所有功能键
            self.view.ui.groupBox_3.setEnabled(True)
            self.view.ui.groupBox_4.setEnabled(True)
            self.view.ui.groupBox.setEnabled(True)
            self.view.ui.startUploadButton.setEnabled(True)

            # 先把表格1清空 防止用户误触，等到点击之后再刷新
            self.view.ui.tableWidget_1.setRowCount(0)
            self.view.ui.tableWidget_1.clearContents()

            # 如果有数据的话
            if self.patientCheck_info:
                # 刷新表格
                # 需要用当前pending.json更新一下self.waitfile, 否则当前上传被中断的文件会上传两次
                # 更新wait_file
                if os.path.exists(self.queue_file_path):
                    with open(self.queue_file_path, 'r', encoding='utf-8') as file:
                        try:
                            data = json.load(file)
                            self.wait_file = data.get("task", [])
                        except json.JSONDecodeError:
                            print("队列文件格式错误，初始化为空队列")
                else:
                    print(f"未找到队列文件，创建新文件：{self.queue_file_path}")
                # 获取当前check_number的wait_file
                check_number = self.patientCheck_info[self.row][5]
                if self.wait_file:
                    filtered_data = [
                        [task["fileName"], "notUploaded"]  # 你需要展示的列数据
                        for task in self.wait_file
                        if task["check_number"] == check_number
                    ]
                    # 初始化第一个表格 （新加）
                    self.view.initTable_1(filtered_data, on_btnDelFile_clicked=self.on_btnDelFile_clicked)

            self.getFileInfo()



    # 转换file_info格式(方便点击切换右下角显示)
    def changeFileInfo(self,file_info):
        changeFileInfo = {}
        for i in file_info:
            key = i[0]
            changeFileInfo[key] = []
        for i in file_info:
            key = i[0]
            file_id = i[1]
            file_name = str(file_id).rjust(3, '0') + '.bdf'
            changeFileInfo[key].append((file_name, i[2]))
        return changeFileInfo

    # 获取病人检查信息功能
    # 获取病人检查信息方法
    def getPatientCheckInfo(self, value=''):
        account = self.client.tUser[1]
        uid = self.client.tUser[0]
        REQmsg = [account, uid, value]
        self.client.getPatientCheckInfo(REQmsg)

    # 处理客户端返回的查询标注类型的结果
    def getPatientCheckInfoRes(self, REPData):
        try:
            # 存在病人检查信息
            if REPData[0] == '1':
                # 清空file_info界面
                self.view.ui.tableWidget_2.setRowCount(0)
                self.view.ui.tableWidget_2.clearContents()

                patientCheck_info_1 = REPData[3][0]
                # 增加了文件信息获取
                self.file_info = REPData[3][3]
                if len(patientCheck_info_1) != 0:
                    self.patientCheck_info = patientCheck_info_1
                    self.view.initTable(self.patientCheck_info, on_btnAddFile_clicked = self.on_btnAddFile_clicked, on_btnRemove_clicked = self.on_btnRemove_clicked ,on_btnComplete_clicked = self.on_btnComplete_clicked)
                    print("patientCheck_info:",self.patientCheck_info)
                    if len(self.file_info) != 0:
                        self.change_file=self.changeFileInfo(self.file_info)
                # 不存在病人检查信息
                else:
                    # 设置添加按钮起作用
                    self.view.ui.groupBox_4.setEnabled(True)

                    # 清空多个表格
                    self.view.ui.tableWidget_1.setRowCount(0)
                    self.view.ui.tableWidget_1.clearContents()
                    # 清空file_info界面
                    self.view.ui.tableWidget_2.setRowCount(0)
                    self.view.ui.tableWidget_2.clearContents()

                    self.view.initTable(None ,None ,None ,None)
                    self.view.ui.tableWidget.setRowCount(0)
                    self.view.ui.tableWidget.clearContents()
            else:
                QMessageBox.information(self, "病人诊断信息", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('getPatientCheckInfoRes', e)

    # 获取脑电数据文件
    def getFileInfo(self, value=''):
        account = self.client.tUser[1]
        uid = self.client.tUser[0]
        REQmsg = [account, uid, value]
        self.client.getFileInfo(REQmsg)

    # 处理客户端返回的查询获取脑电数据文件的结果
    def getFileInfoRes(self, REPData):
        print('REPData:',REPData)
        try:
            if REPData[0] == '1':
                file_info_1 = REPData[3]
                if len(file_info_1) != 0:
                    self.file_info = file_info_1
                    # TODO:暂时这样修改
                    self.change_file = self.changeFileInfo(self.file_info)
                    if self.row != -1:
                        check_id = self.patientCheck_info[self.row][0]
                        if check_id in self.change_file.keys():
                            self.view.initTable_2(self.change_file[check_id])
                        else:
                            # 该方法只能清除内容，表头还是保留的
                            # self.view.ui.tableWidget_2.clear()
                            self.view.ui.tableWidget_2.setRowCount(0)
                            self.view.ui.tableWidget_2.clearContents()
                else:
                    self.change_file = None
            else:
                QMessageBox.information(self, "脑电数据信息", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('getFileInfoRes', e)

    # 点击选择病人方法
    def onChoose_Patient(self):
        # 获取病人信息
        # self.addFormView.hide()
        self.get_choose_patient_info(flag='1')

    # 获取病人信息
    def get_choose_patient_info(self, flag='1', key_word='', key_value=''):
        # 获取病人所有信息
        if flag == '1':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum]
            self.client.getChoosePatientInfo(REQmsg)
        # 病人信息没有条件的翻页
        elif flag == '2':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.patient_start]
            self.client.getChoosePatientInfo(REQmsg)
        # 病人信息重置的首页
        elif flag == '3':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum]
            self.client.getChoosePatientInfo(REQmsg)
        # 病人信息有条件的首页
        elif flag == '4':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, key_word, key_value]
            self.client.getChoosePatientInfo(REQmsg)
        # 病人信息有搜索条件的翻页
        elif flag == '5':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.patient_start, key_word, key_value]
            self.client.getChoosePatientInfo(REQmsg)
        else:
            pass

    # 获取病人信息返回的结果
    def get_choose_patient_infoRes(self, REPData):
        try:
            if REPData[0] == '1':
                flag = REPData[3][0]
                if flag == '1':
                    patient_info = REPData[3][1]
                    self.patient_info = patient_info
                    self.patient_totalNum = REPData[3][2]
                    col_label_detail = ['姓名', '出生日期', '性别', '卡号', '操作']
                    # detail_info = [('235353', '林一', 897), ('00000', '王二', 888)]
                    # totalNumDetail = 2

                    # 初始化除了表格以外其他框架
                    self.view.tableWidget_patient = PatientTableWidget()
                    # 初始化选择框
                    self.view.tableWidget_patient.comboCond.addItems(['姓名', '卡号'])

                    self.view.tableWidget_patient.resize(1500, 800)
                    self.view.tableWidget_patient.setWindowTitle("病人相关信息")
                    # 初始化表格信息
                    self.view.tableWidget_patient.init_ui(col_label=col_label_detail,
                                                                       sampleList=self.patient_info,
                                                                       totalNum=self.patient_totalNum,
                                                                       on_clicked_selectBtn=self.patient_on_clicked_selectBtn)
                    # 返回
                    self.view.tableWidget_patient.returnBtn.triggered.connect(self.patientReturnBtnTrigger)
                    # 搜索
                    self.view.tableWidget_patient.btnSelect.clicked.connect(self.search_patient)
                    # 重置
                    self.view.tableWidget_patient.btnReSelect.clicked.connect(self.research_patient)
                    # 页码相关
                    self.patient_page = math.ceil(self.patient_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_patient.setPageController(self.patient_page)
                    self.view.tableWidget_patient.control_signal.connect(self.patient_page_controller)

                    # 设置不关闭对话框就不进行其他操作
                    self.view.tableWidget_patient.setWindowModality(Qt.ApplicationModal)
                    # 设置关闭对象自动释放资源
                    self.view.tableWidget_patient.setAttribute(Qt.WA_DeleteOnClose)

                    self.view.tableWidget_patient.show()
                elif flag == '2':
                    patient_info = REPData[3][1]
                    self.patient_info = patient_info
                    # self.theme_info = theme_info
                    if self.patient_info:
                        self.clear(self.view.tableWidget_patient.verticalLayout_1)
                        col_label_detail = ['姓名', '出生日期', '性别', '卡号', '操作']
                        # 页码不会改变是因为这里创建时候没有传入当前页码值
                        # 这里只是改变重新创建当前表格值
                        self.view.tableWidget_patient.init_ui(current_page=self.patient_cur_page, col_label=col_label_detail,
                                                            sampleList=self.patient_info, totalNum=self.patient_totalNum,
                                                            on_clicked_selectBtn=self.patient_on_clicked_selectBtn)

                        # 源代码
                        if self.patient_is_fromSkip:
                            self.view.tableWidget_patient.skipPage.setText(str(self.patient_cur_page))
                        else:
                            self.view.tableWidget_patient.skipPage.setText(str(self.patient_skip_page))
                    else:
                        QMessageBox.information(self, "分页信息查询", '下一页无信息！！', QMessageBox.Yes)
                elif flag == '3':
                    # 清除表格内容
                    self.clear(self.view.tableWidget_patient.verticalLayout_1)
                    # 清除页面控制器
                    self.view.tableWidget_patient.control_signal.disconnect(self.patient_page_controller)
                    self.clear(self.view.tableWidget_patient.control_layout)
                    patient_info = REPData[3][1]
                    self.patient_info = patient_info
                    self.patient_totalNum = REPData[3][2]
                    col_label_detail = ['姓名', '出生日期', '性别', '卡号', '操作']
                    self.view.tableWidget_patient.init_ui(col_label=col_label_detail,
                                                          sampleList=patient_info,
                                                          totalNum=self.patient_totalNum,
                                                          on_clicked_selectBtn=self.patient_on_clicked_selectBtn)
                    # 页码相关
                    self.patient_page = math.ceil(self.patient_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_patient.setPageController(self.patient_page)
                    self.view.tableWidget_patient.control_signal.connect(self.patient_page_controller)

                # 点击搜索按钮
                elif flag == '4':
                    # 清除表格内容
                    self.clear(self.view.tableWidget_patient.verticalLayout_1)
                    # 清除页面控制器
                    self.view.tableWidget_patient.control_signal.disconnect(self.patient_page_controller)
                    self.clear(self.view.tableWidget_patient.control_layout)
                    patient_info = REPData[3][1]
                    self.patient_info = patient_info
                    self.patient_totalNum = REPData[3][2]
                    col_label_detail = ['姓名', '出生日期', '性别', '卡号', '操作']
                    self.view.tableWidget_patient.init_ui(col_label=col_label_detail,
                                                          sampleList=patient_info,
                                                          totalNum=self.patient_totalNum,
                                                          on_clicked_selectBtn=self.patient_on_clicked_selectBtn)
                    # 页码相关
                    self.patient_page = math.ceil(self.patient_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_patient.setPageController(self.patient_page)
                    self.view.tableWidget_patient.control_signal.connect(self.patient_page_controller)
                elif flag == '5':
                    patient_info = REPData[3][1]
                    self.patient_info = patient_info
                    # self.theme_info = theme_info
                    if patient_info:
                        self.clear(self.view.tableWidget_patient.verticalLayout_1)
                        col_label_detail = ['姓名', '出生日期', '性别', '卡号', '操作']
                        # 页码不会改变是因为这里创建时候没有传入当前页码值
                        # 这里只是改变重新创建当前表格值
                        self.view.tableWidget_patient.init_ui(current_page=self.patient_cur_page,
                                                              col_label=col_label_detail,
                                                              sampleList=patient_info, totalNum=self.patient_totalNum,
                                                              on_clicked_selectBtn=self.patient_on_clicked_selectBtn)

                        # 源代码
                        if self.patient_is_fromSkip:
                            self.view.tableWidget_patient.skipPage.setText(str(self.patient_cur_page))
                        else:
                            self.view.tableWidget_patient.skipPage.setText(str(self.patient_skip_page))
                    else:
                        QMessageBox.information(self, "分页信息查询", '下一页无信息！！', QMessageBox.Yes)

                else:
                    pass
        except Exception as e:
            print('get_choose_patient_infoRes', e)

    # 选择具体某个病人信息后方法
    def patient_on_clicked_selectBtn(self, row):
        print("选中当前行：", row)
        id = self.patient_info[row][0]
        print("当前选中用户的id为:", id)
        name = self.patient_info[row][1]
        print("当前选中用户的姓名为:", name)
        # 将选中行的内容添加到暂存的添加
        self.addInfo['patient_id'] = id
        self.view.tableWidget_patient.hide()
        self.view.ui.patientBtn.setText(name)
        self.view.ui.patientBtn.setFont(QFont("Agency FB", 16))
        self.view.ui.patientBtn.setStyleSheet("color: blue;")

        # self.addFormView.ui.patientBtn.setText(name)
        # self.addFormView.ui.patientBtn.setFont(QFont("Agency FB", 12))
        # self.addFormView.ui.patientBtn.setStyleSheet("color: blue;")
        # self.addFormView.show()


    # 选择病人的搜索功能首页界面
    def search_patient(self):
        key_word = self.view.tableWidget_patient.comboCond.currentText()
        key_value = self.view.tableWidget_patient.lineValue.text()
        if key_word == '姓名':
            key_word = 'name'
        elif key_word == '卡号':
            key_word = 'card'
        print("key_word:", key_word)
        print("key_value:", key_value)
        # 只有当搜索框有值时候才搜索
        if key_value:
            self.get_choose_patient_info(flag='4', key_word=key_word, key_value=key_value)
        else:
            QMessageBox.information(self, "提示", "搜索框内没有填写内容!!", QMessageBox.Yes)


    # 选择病人的重置功能
    def research_patient(self):
        self.view.tableWidget_patient.comboCond.setCurrentIndex(0)
        self.view.tableWidget_patient.lineValue.clear()
        self.get_choose_patient_info(flag='3')


    # 选择病人信息的返回
    def patientReturnBtnTrigger(self):
        self.view.tableWidget_patient.hide()
        # self.addFormView.show()
        print("返回上级按键被触发！！！")

    # 病人选择信息界面相关跳转
    def patient_page_controller(self, signal):
        total_page = self.view.tableWidget_patient.showTotalPage()
        is_fromSkip = False
        if "home" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                return
            self.view.tableWidget_patient.curPage.setText("1")
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            self.view.tableWidget_patient.curPage.setText(str(int(signal[1]) - 1))
        elif "next" == signal[0]:
            if total_page == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.view.tableWidget_patient.curPage.setText(str(int(signal[1]) + 1))
        elif "final" == signal[0]:
            self.view.tableWidget_patient.curPage.setText(str(total_page))
        elif "confirm" == signal[0]:
            if total_page < int(signal[1]) or int(signal[1]) < 1:
                QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                self.view.tableWidget_patient.skipPage.setText('1')
                return
            is_fromSkip = True
            self.view.tableWidget_patient.curPage.setText(signal[1])
        self.changeTableContent_patient(is_fromSkip)  # 改变表格内容

    def changeTableContent_patient(self, is_fromSkip):
        """根据当前页改变表格的内容"""
        self.patient_is_fromSkip = is_fromSkip
        self.patient_cur_page = int(self.view.tableWidget_patient.curPage.text())
        self.patient_skip_page = int(self.view.tableWidget_patient.skipPage.text())
        self.patient_start = (self.patient_cur_page - 1) * self.perPageNum
        # theme_id = self.theme_detailID
        # row = self.row_detail

        key_word = self.view.tableWidget_patient.comboCond.currentText()
        key_value = self.view.tableWidget_patient.lineValue.text()
        if key_word == '姓名':
            key_word = 'name'
        elif key_word == '卡号':
            key_word = 'card'
        print("key_word:", key_word)
        print("key_value:", key_value)
        # 只有当搜索框有值时候才搜索
        if key_value:
            # 有搜索条件的翻页
            self.get_choose_patient_info(flag='5', key_word=key_word, key_value=key_value)
        else:
            # 无搜索条件的翻页
            self.get_choose_patient_info(flag='2')


    # 清理布局
    def clear(self, layout, num=0, count=-1):
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


    # 选择医生信息
    def onChoose_Doctor(self):
        # self.addFormView.hide()
        self.get_choose_doctor_info(flag='1')

    # 获取医生信息
    def get_choose_doctor_info(self, flag='1', key_word='', key_value=''):
        # 获取医生所有信息
        if flag == '1':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum]
            self.client.getChooseDoctorInfo(REQmsg)
        # 医生信息没有条件的翻页
        elif flag == '2':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.doctor_start]
            self.client.getChooseDoctorInfo(REQmsg)
        # 医生信息重置的首页
        elif flag == '3':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum]
            self.client.getChooseDoctorInfo(REQmsg)
        # 医生信息有条件的首页
        elif flag == '4':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, key_word, key_value]
            self.client.getChooseDoctorInfo(REQmsg)
        # 医生信息有搜索条件的翻页
        elif flag == '5':
            account = self.client.tUser[1]
            REQmsg = [account, flag, self.perPageNum, self.doctor_start, key_word, key_value]
            self.client.getChooseDoctorInfo(REQmsg)
        else:
            pass


    # 获取医生信息返回的结果
    def get_choose_doctor_infoRes(self, REPData):
        try:
            if REPData[0] == '1':
                flag = REPData[3][0]
                if flag == '1':
                    doctor_info = REPData[3][1]
                    self.doctor_info = doctor_info
                    self.doctor_totalNum = REPData[3][2]
                    col_label_detail = ['姓名', '电话', '邮箱', '操作']
                    # 初始化除了表格以外其他框架
                    self.view.tableWidget_doctor = DoctorTableWidget()
                    # 初始化选择框
                    self.view.tableWidget_doctor.comboCond.addItems(['姓名', '电话', '邮箱'])

                    self.view.tableWidget_doctor.resize(1500, 800)
                    self.view.tableWidget_doctor.setWindowTitle("医生相关信息")
                    # 初始化表格信息
                    self.view.tableWidget_doctor.init_ui(col_label=col_label_detail,
                                                          sampleList=self.doctor_info,
                                                          totalNum=self.doctor_totalNum,
                                                          on_clicked_selectBtn=self.doctor_on_clicked_selectBtn)
                    # 返回
                    self.view.tableWidget_doctor.returnBtn.triggered.connect(self.doctorReturnBtnTrigger)
                    # 搜索
                    self.view.tableWidget_doctor.btnSelect.clicked.connect(self.search_doctor)
                    # 重置
                    self.view.tableWidget_doctor.btnReSelect.clicked.connect(self.research_doctor)
                    # 页码相关
                    self.doctor_page = math.ceil(self.doctor_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_doctor.setPageController(self.doctor_page)
                    self.view.tableWidget_doctor.control_signal.connect(self.doctor_page_controller)

                    # 设置不关闭对话框就不进行其他操作
                    self.view.tableWidget_doctor.setWindowModality(Qt.ApplicationModal)
                    # 设置关闭对象自动释放资源
                    self.view.tableWidget_doctor.setAttribute(Qt.WA_DeleteOnClose)

                    self.view.tableWidget_doctor.show()
                elif flag == '2':
                    doctor_info = REPData[3][1]
                    self.doctor_info = doctor_info
                    # self.theme_info = theme_info
                    if self.doctor_info:
                        self.clear(self.view.tableWidget_doctor.verticalLayout_1)
                        col_label_detail = ['姓名', '电话', '邮箱', '操作']
                        # 页码不会改变是因为这里创建时候没有传入当前页码值
                        # 这里只是改变重新创建当前表格值
                        self.view.tableWidget_doctor.init_ui(current_page=self.doctor_cur_page,
                                                              col_label=col_label_detail,
                                                              sampleList=self.doctor_info,
                                                              totalNum=self.doctor_totalNum,
                                                              on_clicked_selectBtn=self.doctor_on_clicked_selectBtn)

                        # 源代码
                        if self.doctor_is_fromSkip:
                            self.view.tableWidget_doctor.skipPage.setText(str(self.doctor_cur_page))
                        else:
                            self.view.tableWidget_doctor.skipPage.setText(str(self.doctor_skip_page))
                    else:
                        QMessageBox.information(self, "分页信息查询", '下一页无信息！！', QMessageBox.Yes)
                elif flag == '3':
                    # 清除表格内容
                    self.clear(self.view.tableWidget_doctor.verticalLayout_1)
                    # 清除页面控制器
                    self.view.tableWidget_doctor.control_signal.disconnect(self.doctor_page_controller)
                    self.clear(self.view.tableWidget_doctor.control_layout)
                    doctor_info = REPData[3][1]
                    self.doctor_info = doctor_info
                    self.doctor_totalNum = REPData[3][2]
                    col_label_detail = ['姓名', '电话', '邮箱', '操作']
                    self.view.tableWidget_doctor.init_ui(col_label=col_label_detail,
                                                          sampleList=doctor_info,
                                                          totalNum=self.doctor_totalNum,
                                                          on_clicked_selectBtn=self.doctor_on_clicked_selectBtn)
                    # 页码相关
                    self.doctor_page = math.ceil(self.doctor_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_doctor.setPageController(self.doctor_page)
                    self.view.tableWidget_doctor.control_signal.connect(self.doctor_page_controller)

                # 点击搜索按钮
                elif flag == '4':
                    # 清除表格内容
                    self.clear(self.view.tableWidget_doctor.verticalLayout_1)
                    # 清除页面控制器
                    self.view.tableWidget_doctor.control_signal.disconnect(self.doctor_page_controller)
                    self.clear(self.view.tableWidget_doctor.control_layout)
                    doctor_info = REPData[3][1]
                    self.doctor_info = doctor_info
                    self.doctor_totalNum = REPData[3][2]
                    col_label_detail = ['姓名', '电话', '邮箱', '操作']
                    self.view.tableWidget_doctor.init_ui(col_label=col_label_detail,
                                                          sampleList=self.doctor_info,
                                                          totalNum=self.doctor_totalNum,
                                                          on_clicked_selectBtn=self.doctor_on_clicked_selectBtn)
                    # 页码相关
                    self.doctor_page = math.ceil(self.doctor_totalNum / self.perPageNum)
                    # 添加表格页面控制信息
                    self.view.tableWidget_doctor.setPageController(self.doctor_page)
                    self.view.tableWidget_doctor.control_signal.connect(self.doctor_page_controller)
                elif flag == '5':
                    doctor_info = REPData[3][1]
                    self.doctor_info = doctor_info
                    if self.doctor_info:
                        self.clear(self.view.tableWidget_doctor.verticalLayout_1)
                        col_label_detail = ['姓名', '电话', '邮箱', '操作']
                        # 页码不会改变是因为这里创建时候没有传入当前页码值
                        # 这里只是改变重新创建当前表格值
                        self.view.tableWidget_doctor.init_ui(current_page=self.doctor_cur_page,
                                                              col_label=col_label_detail,
                                                              sampleList=doctor_info, totalNum=self.doctor_totalNum,
                                                              on_clicked_selectBtn=self.doctor_on_clicked_selectBtn)

                        # 源代码
                        if self.doctor_is_fromSkip:
                            self.view.tableWidget_doctor.skipPage.setText(str(self.doctor_cur_page))
                        else:
                            self.view.tableWidget_doctor.skipPage.setText(str(self.doctor_skip_page))
                    else:
                        QMessageBox.information(self, "分页信息查询", '下一页无信息！！', QMessageBox.Yes)

                else:
                    pass
        except Exception as e:
            print('get_choose_doctor_infoRes', e)

    # 选中某个医生后方法
    def doctor_on_clicked_selectBtn(self, row):
        print("选中当前行：", row)
        id = self.doctor_info[row][0]
        print("当前选中用户的id为:", id)
        name = self.doctor_info[row][1]
        print("当前选中用户的姓名为:", name)

        self.addInfo['pUid'] = id
        self.view.tableWidget_doctor.hide()

        self.view.ui.pdoctorBtn.setText(name)
        self.view.ui.pdoctorBtn.setFont(QFont("Agency FB", 16))
        self.view.ui.pdoctorBtn.setStyleSheet("color: blue;")


    # 选择医生的搜索功能首页界面
    def search_doctor(self):
        key_word = self.view.tableWidget_doctor.comboCond.currentText()
        key_value = self.view.tableWidget_doctor.lineValue.text()
        if key_word == '姓名':
            key_word = 'name'
        elif key_word == '电话':
            key_word = 'phone'
        elif key_word == '邮箱':
            key_word = 'email'
        print("key_word:", key_word)
        print("key_value:", key_value)
        # 只有当搜索框有值时候才搜索
        if key_value:
            self.get_choose_doctor_info(flag='4', key_word=key_word, key_value=key_value)
        else:
            QMessageBox.information(self, "提示", "搜索框内没有填写内容!!", QMessageBox.Yes)

    # 选择医生的重置功能
    def research_doctor(self):
        self.view.tableWidget_doctor.comboCond.setCurrentIndex(0)
        self.view.tableWidget_doctor.lineValue.clear()
        self.get_choose_doctor_info(flag='3')

    # 选择医生信息的返回
    def doctorReturnBtnTrigger(self):
        self.view.tableWidget_doctor.hide()
        # self.addFormView.show()
        print("返回上级按键被触发！！！")

    # 医生息界面相关跳转
    def doctor_page_controller(self, signal):
        total_page = self.view.tableWidget_doctor.showTotalPage()
        is_fromSkip = False
        if "home" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                return
            self.view.tableWidget_doctor.curPage.setText("1")
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            self.view.tableWidget_doctor.curPage.setText(str(int(signal[1]) - 1))
        elif "next" == signal[0]:
            if total_page == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.view.tableWidget_doctor.curPage.setText(str(int(signal[1]) + 1))
        elif "final" == signal[0]:
            self.view.tableWidget_doctor.curPage.setText(str(total_page))
        elif "confirm" == signal[0]:
            if total_page < int(signal[1]) or int(signal[1]) < 1:
                QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                self.view.tableWidget_doctor.skipPage.setText('1')
                return
            is_fromSkip = True
            self.view.tableWidget_doctor.curPage.setText(signal[1])
        self.changeTableContent_doctor(is_fromSkip)  # 改变表格内容

    def changeTableContent_doctor(self, is_fromSkip):
        """根据当前页改变表格的内容"""
        self.doctor_is_fromSkip = is_fromSkip
        self.doctor_cur_page = int(self.view.tableWidget_doctor.curPage.text())
        self.doctor_skip_page = int(self.view.tableWidget_doctor.skipPage.text())
        self.doctor_start = (self.doctor_cur_page - 1) * self.perPageNum
        # theme_id = self.theme_detailID
        # row = self.row_detail

        key_word = self.view.tableWidget_doctor.comboCond.currentText()
        key_value = self.view.tableWidget_doctor.lineValue.text()
        if key_word == '姓名':
            key_word = 'name'
        elif key_word == '电话':
            key_word = 'phone'
        elif key_word == '邮箱':
            key_word = 'email'
        print("key_word:", key_word)
        print("key_value:", key_value)
        # 只有当搜索框有值时候才搜索
        if key_value:
            # 有搜索条件的翻页
            self.get_choose_doctor_info(flag='5', key_word=key_word, key_value=key_value)
        else:
            # 无搜索条件的翻页
            self.get_choose_doctor_info(flag='2')

    # 获取检查信息
    def on_btnConfirmAdd_clicked(self):
        # 点击添加检查信息后禁用防止用户多次点击
        self.view.ui.btnConfirm.setEnabled(False)
        self.addInfo['check_num'] = self.view.ui.check_num.text()
        # 检查单号是否为空
        result = self.check_item_pattern(self.addInfo)
        if not result:
            self.view.ui.btnConfirm.setEnabled(True)
        if result:
            # self.addFormView.close()
            strDate = self.view.ui.dateEdit.date().toString("yyyy-MM-dd")
            print(strDate)
            self.addInfo['measure_date'] = strDate
            self.addInfo['description'] = self.view.ui.checkInfo.toPlainText()
            self.addInfo['cUid'] = self.client.tUser[0]
            account = self.client.tUser[1]
            REQmsg = [account, self.addInfo['check_num'], self.addInfo['patient_id'], self.addInfo['description'],
                      self.addInfo['pUid'], self.addInfo['measure_date'], self.addInfo['cUid']]
            print(self.addInfo)
            self.client.addCheckInfo(REQmsg)


    # 取消添加标注类型信息方法
    def on_btnCancelAdd_clicked(self):
        self.addInfo = {}
        # 关闭弹出添加框
        # self.addFormView.close()
        # 清空添加内容表单中的东西
        self.view.ui.check_num.clear()
        self.view.ui.patientBtn.setText('选择病人')
        self.view.ui.patientBtn.setStyleSheet("color: black;")
        self.view.ui.patientBtn.setFont(QFont("Agency FB", 16))
        self.view.ui.pdoctorBtn.setText('选择开单医生')
        self.view.ui.pdoctorBtn.setStyleSheet("color: black;")
        self.view.ui.pdoctorBtn.setFont(QFont("Agency FB", 16))
        # self.view.ui.textEdit.clear()
        self.view.ui.checkInfo.clear()
        self.view.ui.dateEdit.setDate(QDateTime.currentDateTime().date())

    # 处理客户端传回的添加病人检查信息结果
    def addCheckInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.view.ui.tableWidget.clear()
                # 清空添加表单的东西
                self.view.ui.check_num.clear()
                self.view.ui.patientBtn.setText('选择病人')
                self.view.ui.patientBtn.setStyleSheet("color: black;")
                self.view.ui.patientBtn.setFont(QFont("Agency FB", 16))
                self.view.ui.pdoctorBtn.setText('选择开单医生')
                self.view.ui.pdoctorBtn.setStyleSheet("color: black;")
                self.view.ui.pdoctorBtn.setFont(QFont("Agency FB", 16))
                self.view.ui.checkInfo.clear()
                self.view.ui.dateEdit.setDate(QDateTime.currentDateTime().date())
                self.getPatientCheckInfo()
                result = QMessageBox.information(self, "病人检查", REPData[2], QMessageBox.Yes)
                if result == QMessageBox.Yes:
                    self.view.ui.btnConfirm.setEnabled(True)
            else:
                self.view.ui.check_num.clear()
                self.view.ui.patientBtn.setText('选择病人')
                self.view.ui.patientBtn.setStyleSheet("color: black;")
                self.view.ui.patientBtn.setFont(QFont("Agency FB", 16))
                self.view.ui.pdoctorBtn.setText('选择开单医生')
                self.view.ui.pdoctorBtn.setStyleSheet("color: black;")
                self.view.ui.pdoctorBtn.setFont(QFont("Agency FB", 16))
                self.view.ui.checkInfo.clear()
                self.view.ui.dateEdit.setDate(QDateTime.currentDateTime().date())
                result = QMessageBox.information(self, "病人检查", REPData[2], QMessageBox.Yes)
                if result == QMessageBox.Yes:
                    self.view.ui.btnConfirm.setEnabled(True)
        except Exception as e:
            print('addCheckInfo', e)


    # 删除病人检查信息功能
    # 删除病人检查信息方法
    def on_btnDel_clicked(self):

        if self.row!= -1:
            self.row = self.view.ui.tableWidget.currentRow()
            # 找到当前检查信息的脑电上传医生
            pdoctorname = self.patientCheck_info[self.row][3]
            if pdoctorname == self.client.tUser[0]:
                answer = QMessageBox.warning(
                    self.view, '确认删除！', '您将进行删除操作！',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if answer == QMessageBox.Yes:
                    if self.row == -1:
                        QMessageBox.information(self.view, ' ', '请先选中一行')
                        return
                    # 暂时只能选中一行删除
                    print('row', self.row)
                    check_id = self.patientCheck_info[self.row][0]
                    account = self.client.tUser[1]
                    REQmsg = [account, check_id, self.row]
                    self.row = -1
                    self.client.delPatientCheckInfo(REQmsg)
                else:
                    return
            else:
                QMessageBox.information(self.view, '提示', '你不是本次检查的脑电上传医生，你无权进行删除！！！')
        else:
            QMessageBox.information(self, ' ', '请先在病人诊断信息中选择一行')
            return

    # 处理客户端返回的删除病人检查信息结果
    def delPatientCheckInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                row = REPData[3][1]
                print('pop values :', self.patientCheck_info[row])
                print("当前删除病人检查信息返回的结果REPData：",REPData) # ['1', 2, '删除病人诊断信息成功', [254, 0]]

                if len(self.patientCheck_info) != 1:
                    self.patientCheck_info.pop(row)
                    self.view.initTable(self.patientCheck_info, on_btnAddFile_clicked = self.on_btnAddFile_clicked, on_btnRemove_clicked = self.on_btnRemove_clicked ,on_btnComplete_clicked = self.on_btnComplete_clicked)
                else:
                    self.view.ui.tableWidget.setRowCount(0)
                    self.view.ui.tableWidget_2.clearContents()


                self.view.ui.groupBox_4.setEnabled(True)

                #清空待上传文件表
                self.view.ui.tableWidget_1.setRowCount(0)
                self.view.ui.tableWidget_1.clearContents()

                # 清空服务端已有文件表
                self.view.ui.tableWidget_2.setRowCount(0)
                self.view.ui.tableWidget_2.clearContents()
                QMessageBox.information(self, "成功", "删除成功")

                return
            else:
                QMessageBox.information(self, "提示", REPData[2], QMessageBox.Yes)
        except Exception as e:
            print('delPatientCheckInfo', e)

    def convert_edf_to_bdf(self):
        try:
            # 生成转换后的 BDF 文件名
            directory, filename = os.path.split(self.from_filepath)
            filename_without_extension = os.path.splitext(filename)[0]
            new_filename = f"{filename_without_extension}.bdf"
            self.convert_filepath = os.path.join(directory, new_filename)

            # 使用MNE读取EDF文件并提取注释
            raw = mne.io.read_raw_edf(self.from_filepath, preload=True)
            data = raw.get_data()  # 物理数据 (单位: V)
            ch_names = raw.ch_names
            sfreq = int(raw.info["sfreq"])  # 采样率
            n_channels, n_samples = data.shape

            # 根据通道物理范围调整单位
            # 将所有数据按需调整为微伏（µV）或毫伏（mV）
            scale_factors = []  # 存储每个通道的单位转换因子
            for i in range(n_channels):
                physical_min = np.min(data[i])  # 获取当前通道的最小值
                physical_max = np.max(data[i])  # 获取当前通道的最大值

                # 根据物理范围决定单位转换
                if abs(physical_min) > 1 or abs(physical_max) > 1:  # 如果物理范围较大，使用 mV
                    scale_factors.append(1e3)  # 转换为毫伏 (mV)
                    data[i] /= 1e3  # 转换数据为毫伏
                else:  # 否则，使用 µV
                    scale_factors.append(1e6)  # 转换为微伏 (µV)
                    data[i] *= 1e6  # 转换数据为微伏

            # 修正物理范围，防止 EDF+ 限制 8 位字符
            physical_min = np.min(data, axis=1)
            physical_max = np.max(data, axis=1)

            for i in range(n_channels):
                min_str = "{:.6g}".format(physical_min[i])
                max_str = "{:.6g}".format(physical_max[i])
                physical_min[i] = float(min_str)
                physical_max[i] = float(max_str)

                if physical_min[i] == physical_max[i]:
                    print(f"通道 {ch_names[i]} 物理范围相等，微调以避免错误 ...")
                    physical_min[i] -= 1e-3
                    physical_max[i] += 1e-3

            print("物理范围检查 (已调整格式)：")
            for i in range(min(5, n_channels)):
                print(f"通道 {ch_names[i]}: min={physical_min[i]}, max={physical_max[i]}")

            # 确保 `writePhysicalSamples()按帧写入
            record_duration = 1  # 每个 BDF 记录的时长（秒）
            n_records = n_samples // sfreq  # 计算 BDF 记录数

            if n_records * sfreq != n_samples:
                print(f"警告：数据长度 {n_samples} 不是 {sfreq} 的整数倍，将填充 0 以对齐。")
                pad_length = (n_records + 1) * sfreq - n_samples
                data = np.pad(data, ((0, 0), (0, pad_length)), 'constant')
                n_samples = data.shape[1]

            # 重构数据形状，使其符合 writePhysicalSamples()
            data = data.reshape(n_channels, n_records, sfreq)

            # 4. **写入 BDF**
            print(f"正在写入 BDF: {self.convert_filepath} ...")

            channel_info = [{
                "label": ch,
                "dimension": "uV",
                "sample_rate": sfreq,
                "physical_min": physical_min[i],
                "physical_max": physical_max[i],
                "digital_min": -32768,
                "digital_max": 32767,
                "transducer": "",
                "prefilter": "",
            } for i, ch in enumerate(ch_names)]

            with pyedflib.EdfWriter(self.convert_filepath, n_channels, file_type=pyedflib.FILETYPE_BDF) as f:
                f.setSignalHeaders(channel_info)

                # **修正：逐个通道写入数据**
                for record_idx in range(n_records):
                    for ch_idx in range(n_channels):
                        f.writePhysicalSamples(data[ch_idx, record_idx, :])  # 只写入单个通道的 1D 数据

            print(f"成功将 EDF 转换为 BDF 文件: {self.convert_filepath}")

            # # 检查 BDF 结果
            # raw_bdf = mne.io.read_raw_bdf(self.convert_filepath, preload=True)
            # bdf_data = raw_bdf.get_data()
            #
            # print("BDF 文件 EEG Fp1-REF 通道的前10个数据点：")
            # print(bdf_data[0, :10])
            #
            # # **检查文件时长**
            # print(f"EDF 时长: {raw.times[-1]} 秒")
            # print(f"BDF 时长: {raw_bdf.times[-1]} 秒")

        except Exception as e:
            print('Error during EDF to BDF conversion:', e)

    # 更新进度条位置
    def update_progress_bar(self):
        self.dlgProgress.setValue(self.progress_value)

    # 创建目标文件路径
    def make_filepath(self, filename):
        # 处理过后脑电文件存放路径
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
        processFilename = filename + str('.bdf')
        self.file_path = os.path.join(self.dir_path, processFilename)

    # 查找某一路径指定文件后缀文件名
    def findFile(self, filepath, suffix):
        # fixme:这里最好做个异常处理
        # 获取文件夹下所有文件
        fileslist = os.listdir(filepath)
        fileName = []
        # 遍历文件夹中的文件
        for file in fileslist:
            if file.endswith(suffix):  # 判断文件名是否以指定的文件名开头
                fileName.append(file.split('.')[0])
        return fileName  # 返回不带后缀的文件名列表

    # 服务器端发生异常
    def upload_failedCall(self):
        if hasattr(self, 'dlgProgress'):
            self.dlgProgress.close()
        self.progress_value = 0
        QMessageBox.information(self, "脑电文件上传", "脑电文件上传出错，已删除上传记录和处理过后的脑电文件！！！", QMessageBox.Yes)

    # 检查编辑/增加 数据格式
    def check_item_pattern(self, data):
        check_num = data.get('check_num', '').strip()
        if not check_num:
            QMessageBox.information(self.view, '提示！', '请输入检查单号：检查单号不能为空！')
            return False

        # 增加：检查单号只能包含字母、数字或下划线
        pattern = QRegularExpression("^[a-zA-Z0-9_]+$")
        if not pattern.match(check_num).hasMatch():
            QMessageBox.information(self.view, '提示！', '检查单号不能包含特殊字符，只能包含字母、数字或下划线！')
            return False

        if 'patient_id' not in data:
            QMessageBox.information(self.view, '提示！', '未选择病人信息，请重新选择！')
            return False
        if 'pUid' not in data:
            QMessageBox.information(self.view, '提示！', '未选择开单医生信息，请重新选择！')
            return False

        return True

    def exit(self):
        self.client.getPatientCheckInfoResSig.disconnect()
        self.client.delPatientCheckInfoResSig.disconnect()
        self.client.addCheckInfoResSig.disconnect()
        self.client.checkConfigResSig.disconnect()
        self.client.getUserConfigResSig.disconnect()
        self.client.makeFileNameResSig.disconnect()
        self.client.writeEEGResSig.disconnect()
        self.client.updateCheckInfoResSig.disconnect()
        self.client.getFileInfoResSig.disconnect()
        self.client.delFileInfoResSig.disconnect()
        self.client.getChoosePatientInfoResSig.disconnect()
        self.client.getChooseDoctorInfoResSig.disconnect()
