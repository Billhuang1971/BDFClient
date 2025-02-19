

from PyQt5.Qt import *

from view.diagTest import DiagListView

class diagTestController(QWidget):
    switchToEEG = pyqtSignal(list)

    def __init__(self, appUtil=None,  client=None):
        super().__init__()
        self.view = DiagListView()
        self.appUtil = appUtil
        self.client = client
        self.User = self.client.tUser

        self.client.checkTestedSig.connect(self.checkTested)

        self.client.dt_diagTest_commitResSig.connect(self.diagTest_commitRes)
        self.client.dt_get_contentsResSig.connect(self.get_contentsRes)
        self.uid = None
        self.check_id = None
        self.file_id = None
        self.measure_date = None
        self.file_name = None

        self.root_path = self.appUtil.root_path
        self.sign_InfoView = None

        self.get_contents()

    # 槽对象中的槽函数
    def exit(self):
        self.client.checkTestedSig.disconnect()
        self.client.dt_diagTest_commitResSig.disconnect()
        self.client.dt_get_contentsResSig.disconnect()

    # 客户端发送提取取学习测试信息的请求
    def get_contents(self):
        self.check_id = None
        self.measure_date = None
        self.file_name = None
        self.file_id = None
        self.page = ['file_name']
        msg = [self.client.tUser[0]]
        self.client.dt_get_contents(msg)

    # 处理客户端传回的提取取学习测试信息
    def get_contentsRes(self, REPData):

        if REPData[0] == '0':
            QMessageBox.information(self, "提取学习测试信息不成功", REPData[2], QMessageBox.Yes)
            return False

        self.diags_viewInfo = REPData[2]
        self.userNamesDict = {}
        self.paitentNamesDict = {}
        self.student_stateDict = {}
        if REPData[3] is not None:
          for u in REPData[3]:
            self.userNamesDict.setdefault(u[0],u[1])
        if REPData[4] is not None:
          for p in REPData[4]:
            self.paitentNamesDict.setdefault(p[0], p[1])
        if REPData[5] is not None:
          for st in REPData[5]:
            self.student_stateDict.setdefault(st[0], st[2])

        self.view.show()
        self.view.init_table(self.diags_viewInfo, self.userNamesDict, self.student_stateDict, self.paitentNamesDict,
                              self.on_clicked_manual_query)

    def on_clicked_manual_query(self, diags_viewInfo, patient_name, trow):
        self.class_id = diags_viewInfo[0]
        self.check_id = diags_viewInfo[6]
        self.patient_id = diags_viewInfo[8]
        self.measure_date = diags_viewInfo[9]
        self.patient_name = patient_name
        self.row = trow
        self.file_name = '{:>03}.bdf'.format(str(diags_viewInfo[10]))
        self.file_id = diags_viewInfo[10]
        self.uid = diags_viewInfo[11]
        self.page = ['file_name']
        try:
            msg = [self.check_id, self.file_id, self.uid, self.class_id, self.client.tUser[0]]
            self.client.checkTested(msg)
        except:
            QMessageBox.information(self, '提示', '打开文件失败')
            self.mainMenubar.setEnabled(True)

    def checkTested(self, msg):
        self.switchToEEG.emit([self.file_id, self.file_name, self.check_id, self.patient_id, self.measure_date,
                                   ['diagTestController', '', self.class_id], "result", self.User[0], True, False, self.class_id])

    def diagTest_commitRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "完成学习测试", REPData[2], QMessageBox.Yes)
            #self.diagListView.show()
            return False
        QMessageBox.information(self, "完成学习", REPData[2], QMessageBox.Yes)
        self.get_contents()