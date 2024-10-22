import math

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QMessageBox

from view.modelTest import modelTestView
from view.progressBarView import ProgressBarView


class modelTestController(QWidget):
    def __init__(self, client, cAppUtil):
        try:
            super().__init__()
            self.client = client
            self.cAppUtil = cAppUtil
            self.view = modelTestView()

            # 数据初初始化
            # 页面大小
            self.pageSize = 8
            # 当前页
            self.page = 1
            # 总页数
            self.pageNum = None
            # 分类器数量
            self.count = None
            # 分类器信息
            self.classifier_info = None
            # 分类器名称
            self.classifier_name = None
            # 进度条对象
            self.progressBarView = None


            # 获取数据
            self.client.getClassifierInfo(self.pageSize, self.page, self.classifier_name)
            self.client.classifierInfoResSig.connect(self.updateClassifierTable)

            # 事件绑定
            self.view.ui.first_page.clicked.connect(self.first_page)
            self.view.ui.last_page.clicked.connect(self.last_page)
            self.view.ui.next_page.clicked.connect(self.next_page)
            self.view.ui.end_page.clicked.connect(self.end_page)
            self.view.ui.algorithm_tableWidget.itemClicked.connect(self.checked_classifier_info)
            self.view.ui.pushButton_test.clicked.connect(self.on_btn_test_clicked)
            self.view.ui.search.clicked.connect(self.on_btn_search_clicked)
            self.view.ui.reset.clicked.connect(self.on_btn_reset_clicked)
            self.client.runProcessForTestResSig.connect(self.runProcessForTestRes)
            self.client.getResultResSig.connect(self.getResultRes)

        except Exception as e:
            print('__init__', e)


    # 搜索按钮点击事件响应
    def on_btn_search_clicked(self):
        try:
            self.view.hidden_btn()
            self.classifier_name = self.view.ui.lineEdit.text()
            if self.classifier_name == '':
                self.classifier_name = None
            self.client.getClassifierInfo(self.pageSize, self.page, self.classifier_name)
        except Exception as e:
            print('on_btn_search_clicked', e)

    # 重置按钮点击时间响应
    def on_btn_reset_clicked(self):
        try:
            self.view.hidden_btn()
            self.classifier_name = None
            self.view.ui.lineEdit.clear()
            self.client.getClassifierInfo(self.pageSize, self.page, self.classifier_name)
        except Exception as e:
            print('on_btn_reset_clicked', e)

    # 获取模型测试进度
    def getResult(self):
        self.client.getResult()

    # 模型测试结果处理
    def getResultRes(self, REPData):
        try:
            print(REPData)
            if REPData[0] == '0':
                QMessageBox.information(self.view, '提示', '读取进度信息失败', QMessageBox.Yes)
                self.timer.stop()
                self.view.view_unlock()
                self.progressBarView.close()
            else:
                if REPData[3]:
                    for i in REPData[3]:
                        temp = str(i)
                        self.view.output_info(temp)
                if REPData[2] == False:
                    self.timer.stop()
                    self.progressBarView.updateProgressBar(100)
                    self.progressBarView.close()
                    if REPData[5] != 'True':
                        self.view.output_info("测试结束")
                        self.view.output_info('算法运行失败')
                        QMessageBox.information(self.view, '提示', '算法运行失败', QMessageBox.Yes)
                    else:
                        self.view.output_info("测试结束")
                        self.view.output_info('算法运行成功')
                        cur_classifier_name = REPData[4]
                        self.view.output_info(
                            '提示:' + '{}模型已测试完成，可通过模型管理功能查看模型信息'.format(cur_classifier_name))
                        QMessageBox.information(self.view, '提示', '算法运行成功', QMessageBox.Yes)
                    self.view.view_unlock()
                    self.client.getClassifierInfo(self.pageSize, self.page, None)
                else:
                    scan_num = int(REPData[4])
                    total_scan_num = int(REPData[5])
                    print(scan_num, total_scan_num)
                    self.progressBarView.updateProgressBar(100 * scan_num / total_scan_num)
        except Exception as e:
            print('getResultRes', e)


    # 模型测试开启结果处理
    def runProcessForTestRes(self, REPData):
        try:
            if REPData[0] == '0':
                self.view.view_unlock()
                QMessageBox.information(self.view, '提示', '当前服务器正在进行其他模型测试', QMessageBox.Yes)
                return
            else:
                self.progressBarView = ProgressBarView(window_title="测试中", hasStopBtn=False, maximum=100)
                self.progressBarView.show()
                self.timer = QTimer()
                self.timer.start(5000)
                self.timer.timeout.connect(self.getResult)
        except Exception as e:
            print('runProcessForTestRes', e)

    # 响应函数，用户点击测试按钮
    def on_btn_test_clicked(self):
        try:
            Fisrt_Test_flag = True
            row = self.view.ui.algorithm_tableWidget.currentRow()
            if not row > -1:
                QMessageBox.critical(self, 'Alert', '未选择测试算法')
                return
            if self.classifier_test_upload != 'uploaded':
                QMessageBox.critical(self, 'Alert', '未上传测试算法文件')
                return

            if self.classifier_test_state == '已测试':
                reply = QMessageBox.information(self, '提示', '模型已完成测试，是否需要重复进行测试？',
                                                QMessageBox.Yes | QMessageBox.No)
                if reply == 16384:
                    Fisrt_Test_flag = False
                else:
                    return

            self.view.testOutput.clear()
            self.view.view_lock()
            self.view.ui.pushButton_test.setEnabled(False)
            self.view.output_info("测试开始")

            self.client.runProcessForTest([self.classifier_info[row][0], Fisrt_Test_flag])


        except Exception as e:
            print('on_btn_test_clicked', e)

    # 更新表
    def updateClassifierTable(self, msg):
        try:
            self.view.show_btn()
            self.view.ui.algorithm_tableWidget.reset()
            self.count = msg[3][2][0]
            self.classifier_info = msg[3][2][1]
            self.pageNum = math.ceil(self.count / self.pageSize)
            self.view.updateClassifierTable(self.classifier_info, page=self.page, pageNum=self.pageNum)
        except Exception as e:
            print('updateClassifierTable', e)

    # 选中分类器
    def checked_classifier_info(self, item):
        try:
            row = item.row()
            if self.classifier_info[row][6] == 'None':
                self.classifier_test_state = '未测试'
            else:
                self.classifier_test_state = '已测试'
            self.classifier_test_upload = self.classifier_info[row][5]
            classifier_name = self.classifier_info[row][1]
            self.view.updateClassifierLabel(classifier_name, classifier_name +
                                            '|' + ('测试算法已上传' if self.classifier_test_upload == 'uploaded' else '测试算法未上传') +
                                            '|' + self.classifier_test_state)
        except Exception as e:
            print('checked_classifier_info', e)

    # 首页
    def first_page(self):
        try:
            if (self.page == 1):
                return
            self.view.hidden_btn()
            self.page = 1
            self.client.getClassifierInfo(self.pageSize, self.page, self.classifier_name)
        except Exception as e:
            print('first_page', e)

    # 上一页
    def last_page(self):
        try:
            if (self.page == 1):
                return
            self.view.hidden_btn()
            self.page = self.page - 1
            self.client.getClassifierInfo(self.pageSize, self.page, self.classifier_name)
        except Exception as e:
            print('last_page', e)

    # 下一页
    def next_page(self):
        try:
            if (self.page == self.pageNum):
                return
            self.view.hidden_btn()
            self.page = self.page + 1
            self.client.getClassifierInfo(self.pageSize, self.page, self.classifier_name)
        except Exception as e:
            print('next_page', e)

    # 末页
    def end_page(self):
        try:
            if (self.page == self.pageNum):
                return
            self.view.hidden_btn()
            self.page = self.pageNum
            self.client.getClassifierInfo(self.pageSize, self.page, self.classifier_name)
        except Exception as e:
            print('end_page', e)


    # 断开信号
    def exit(self):
        self.client.classifierInfoResSig.disconnect()
        self.client.runProcessForTestResSig.disconnect()
        self.client.getResultResSig.disconnect()