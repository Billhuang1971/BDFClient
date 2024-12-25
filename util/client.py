# -*- coding: utf-8 -*-
import threading

from PyQt5.QtCore import Qt, pyqtSignal, QObject

from threading import Thread
from util.socketClient import socketClient


class client(QObject, socketClient):
    ## dsj [ ===
    # ---执行查看 reserchingQuery ---
    rgQ_theme_commitResSig = pyqtSignal(list)
    rgQ_pagingResSig = pyqtSignal(list)
    rgQ_label_commitResSig = pyqtSignal(list)
    rgQ_get_labelsResSig = pyqtSignal(list)
    rgQ_get_type_infoResSig = pyqtSignal(list)
    rgQ_del_sampleInfo_stateResSig = pyqtSignal(list)
    rgQ_update_sampleInfo_stateResSig = pyqtSignal(list)
    rgQ_add_sampleInfo_stateResSig = pyqtSignal(list)
    rgQ_del_sample19ResSig = pyqtSignal(list)
    rgQ_init_SampleListResSig = pyqtSignal(list)
    rgQ_update_sampleInfo15ResSig = pyqtSignal(list)
    rgQ_del_sampleInfo13ResSig = pyqtSignal(list)
    rgQ_update_sampleInfo12ResSig = pyqtSignal(list)
    rgQ_load_dataDynamicalResSig = pyqtSignal(list)
    rgQ_openEEGFileResSig = pyqtSignal(list)

    # ---科研标注 reserching ---
    rg_pagingResSig = pyqtSignal(list)
    rg_label_commitResSig = pyqtSignal(list)
    rg_get_notlabelsResSig = pyqtSignal(list)
    rg_get_type_infoResSig = pyqtSignal(list)
    rg_del_sampleInfo_stateResSig = pyqtSignal(list)
    rg_update_sampleInfo_stateResSig = pyqtSignal(list)
    rg_add_sampleInfo_stateResSig = pyqtSignal(list)
    rg_del_sample19ResSig = pyqtSignal(list)
    rg_insert_sample17ResSig = pyqtSignal(list)
    rg_init_SampleListResSig = pyqtSignal(list)
    rg_update_sampleInfo15ResSig = pyqtSignal(list)
    rg_add_sampleInfo14ResSig = pyqtSignal(list)
    rg_del_sampleInfo13ResSig = pyqtSignal(list)
    rg_update_sampleInfo12ResSig = pyqtSignal(list)
    rg_load_dataDynamicalResSig = pyqtSignal(list)
    rg_openEEGFileResSig = pyqtSignal(list)

    #---学习评估  diagAssess ---
    da_get_ClassContentsResSig = pyqtSignal(list)

    da_get_diagResSig = pyqtSignal(list)
    da_del_StudentsTestResSig = pyqtSignal(list)
    da_del_ClassResSig = pyqtSignal(list)
    da_get_ClassStudentResSig = pyqtSignal(list)
    da_get_type_infoResSig = pyqtSignal(list)
    da_del_sampleInfo_stateResSig = pyqtSignal(list)
    da_update_sampleInfo_stateResSig = pyqtSignal(list)
    da_add_sampleInfo_stateResSig = pyqtSignal(list)
    da_del_sample19ResSig = pyqtSignal(list)
    da_insert_sample17ResSig = pyqtSignal(list)
    da_init_SampleListResSig = pyqtSignal(list)
    da_update_sampleInfo15ResSig = pyqtSignal(list)
    da_add_sampleInfo14ResSig = pyqtSignal(list)
    da_del_sampleInfo13ResSig = pyqtSignal(list)
    da_update_sampleInfo12ResSig = pyqtSignal(list)
    da_add_sampleInfo11ResSig = pyqtSignal(list)
    da_load_dataDynamicalResSig = pyqtSignal(list)
    da_openEEGFileResSig = pyqtSignal(list)
    da_get_contentsResSig = pyqtSignal(list)


    #---学习测试 learningTest ---
    dt_diagTest_commitResSig = pyqtSignal(list)
    dt_get_type_infoResSig = pyqtSignal(list)
    dt_del_sampleInfo_stateResSig = pyqtSignal(list)
    dt_update_sampleInfo_stateResSig = pyqtSignal(list)
    dt_add_sampleInfo_stateResSig = pyqtSignal(list)
    dt_del_sample19ResSig = pyqtSignal(list)
    dt_insert_sample17ResSig = pyqtSignal(list)
    dt_init_SampleListResSig = pyqtSignal(list)
    dt_update_sampleInfo15ResSig = pyqtSignal(list)
    dt_add_sampleInfo14ResSig = pyqtSignal(list)
    dt_del_sampleInfo13ResSig = pyqtSignal(list)
    dt_update_sampleInfo12ResSig = pyqtSignal(list)
    dt_add_sampleInfo11ResSig = pyqtSignal(list)
    dt_load_dataDynamicalResSig = pyqtSignal(list)
    dt_openEEGFileResSig = pyqtSignal(list)
    dt_get_contentsResSig = pyqtSignal(list)

    # ---诊断学习 diagLearning ---
    dl_get_studyInfoResSig = pyqtSignal(list)
    dl_get_contentsResSig = pyqtSignal(list)
    dl_get_type_infoResSig = pyqtSignal(list)
    dl_openEEGFileResSig = pyqtSignal(list)
    dl_load_dataDynamicalResSig = pyqtSignal(list)
    dl_init_SampleListResSig = pyqtSignal(list)
    dl_get_diagResSig = pyqtSignal(list)

    #---脑电会诊consulting ---
    ct_main_get_diagResSig = pyqtSignal(list)
    ct_diag_updateResSig = pyqtSignal(list)
    ct_diag_commitResSig = pyqtSignal(list)
    ct_diag_refusedResSig = pyqtSignal(list)
    ct_get_diags_notDiagResSig = pyqtSignal(list)
    ct_get_type_infoResSig = pyqtSignal(list)
    ct_del_sampleInfo_stateResSig = pyqtSignal(list)
    ct_update_sampleInfo_stateResSig = pyqtSignal(list)
    ct_add_sampleInfo_stateResSig = pyqtSignal(list)
    ct_del_sample19ResSig = pyqtSignal(list)
    ct_insert_sample17ResSig = pyqtSignal(list)
    ct_init_SampleListResSig = pyqtSignal(list)
    ct_update_sampleInfo15ResSig = pyqtSignal(list)
    ct_add_sampleInfo14ResSig = pyqtSignal(list)
    ct_del_sampleInfo13ResSig = pyqtSignal(list)
    ct_update_sampleInfo12ResSig = pyqtSignal(list)
    ct_add_sampleInfo11ResSig = pyqtSignal(list)
    ct_get_diagResSig = pyqtSignal(list)
    ct_load_dataDynamicalResSig = pyqtSignal(list)
    ct_openEEGFileResSig = pyqtSignal(list)
    ct_get_fileNameByIdDateResSig = pyqtSignal(list)

    # ---标注查询manualQuery ---
    mq_pagingResSig = pyqtSignal(list)
    mq_get_diags_DiagnosedResSig = pyqtSignal(list)
    mq_get_type_infoResSig = pyqtSignal(list)
    mq_get_fileNameByIdDateResSig = pyqtSignal(list)
    mq_openEEGFileResSig = pyqtSignal(list)
    mq_load_dataDynamicalResSig = pyqtSignal(list)
    mq_init_SampleListResSig = pyqtSignal(list)
    mq_get_diagResSig = pyqtSignal(list)

    # ---标注诊断manual ---
    diag_commitResSig = pyqtSignal(list)
    diag_refusedResSig = pyqtSignal(list)
    diag_updateResSig = pyqtSignal(list)
    get_diagResSig = pyqtSignal(list)
    get_diags_notDiagResSig = pyqtSignal(list)
    get_type_infoResSig = pyqtSignal(list)
    del_sampleInfo_stateResSig = pyqtSignal(list)
    update_sampleInfo_stateResSig = pyqtSignal(list)
    add_sampleInfo_stateResSig = pyqtSignal(list)
    del_sample19ResSig = pyqtSignal(list)
    insert_sample17ResSig = pyqtSignal(list)
    init_SampleListResSig = pyqtSignal(list)
    update_sampleInfo15ResSig = pyqtSignal(list)
    add_sampleInfo14ResSig = pyqtSignal(list)
    del_sampleInfo13ResSig = pyqtSignal(list)
    update_sampleInfo12ResSig = pyqtSignal(list)
    add_sampleInfo11ResSig = pyqtSignal(list)

    load_dataDynamicalResSig = pyqtSignal(list)
    openEEGFileResSig = pyqtSignal(list)
    get_fileNameByIdDateResSig = pyqtSignal(list)

    ## dsj ] ===
    # 服务器异常信号
    serverExceptSig = pyqtSignal()

    # 登录
    loginResSig = pyqtSignal(int, str)
    logoutResSig = pyqtSignal(list)

    # 退出
    quitResSig = pyqtSignal()

    # 密码修改
    changePwdResSig = pyqtSignal(list)

    # 用户管理
    # 回调获取用户信息的信号
    getUserInfoResSig = pyqtSignal(list)
    # 回调添加用户信息的信号
    addUserInfoResSig = pyqtSignal(list)
    # 回调编辑用户信息的信号
    updateUserInfoResSig = pyqtSignal(list)
    # 回调删除用户信息的信号
    delUserInfoResSig = pyqtSignal(list)
    userPagingResSig = pyqtSignal(list)
    inquiryUserInfoResSig = pyqtSignal(list)

    # 主界面模块
    # 基本配置
    getConfigDataResSig = pyqtSignal(list)
    # 添加基本配置信号
    addBasicConfigResSig = pyqtSignal(tuple)
    # 更新基本配置信号
    updBasicConfigResSig = pyqtSignal(list)
    # 删除基本配置信号
    delBasicConfigResSig = pyqtSignal(list)

    # 配置选择
    getCurConfigDataResSig = pyqtSignal(tuple)
    getAllConfigDataResSig = pyqtSignal(list)
    chgCurUserConfigResSig = pyqtSignal(list)

    # 标注类型
    # 回调获取标注类型信息的信号
    getTypeInfoResSig = pyqtSignal(list)
    # 回调添加标注类型的信号
    addTypeInfoResSig = pyqtSignal(list)
    # 回调删除标注类型的信号
    delTypeInfoResSig = pyqtSignal(list)
    # 回调编辑标注类型的信号
    updateTypeInfoResSig = pyqtSignal(list)

    # 创建会诊
    getDoctorInfoResSig = pyqtSignal(list)
    getSearchDoctorInfoSig = pyqtSignal(list)
    sendInvitationResSig = pyqtSignal(list)
    getCpltCheckInfoResSig = pyqtSignal(list)
    getHistoryConsResSig = pyqtSignal(list)
    createConsResSig = pyqtSignal(list)
    getAllConsInfoSig = pyqtSignal(list)
    inqConsInfoSig = pyqtSignal(list)

    # 导联配置
    # 回调获取导联配置的信号
    getMontageResSig = pyqtSignal(list)
    # 回调添加导联方案的信号
    addMontageSchemeResSig = pyqtSignal(list)
    # 回调添加导联方案的信号
    editMontageSchemeResSig = pyqtSignal(list)
    # 回调删除导联方案的信号
    delMontageSchemeResSig = pyqtSignal(list)
    # 回调添加导联方案通道的信号
    saveMontageChannelResSig = pyqtSignal(list)

    # 病人管理
    # 回调获取病人信息的信号
    getPatientInfoResSig = pyqtSignal(list)
    # 回调添加病人信息的信号
    addPatientInfoResSig = pyqtSignal(list)
    # 回调删除病人信息的信号
    delPatientInfoResSig = pyqtSignal(list)
    # 回调编辑病人信息的信号
    updatePatientInfoResSig = pyqtSignal(list)
    # 回调查询病人信息的信号
    inqPatientInfoResSig = pyqtSignal(list)
    patientPagingResSig = pyqtSignal(list)

    # 样本统计模块
    # 样本统计
    getSpecificInfoResSig = pyqtSignal(list)
    getSpecificNumResSig = pyqtSignal(list)
    getSpecificDetailResSig = pyqtSignal(dict)
    getSpecNumFromFltResSig = pyqtSignal(list)

    # 构建集合
    getSetInitDataResSig = pyqtSignal(list)
    getSetBuildFltDataResSig = pyqtSignal(list)
    getSetExportInitDataResSig = pyqtSignal(list)
    getSetExportDataResSig = pyqtSignal(list)
    delSetResSig = pyqtSignal(list)
    buildSetSig = pyqtSignal(list)
    buildSetGetPgSig = pyqtSignal(list)
    buildSetCancelSig = pyqtSignal(list)
    getSetSig = pyqtSignal(list)
    getSetSearchSig = pyqtSignal(list)
    getSetDescribeSig = pyqtSignal(list)

    # 创建课堂
    # 回调获取课堂信息的信号
    getLessonInfoResSig = pyqtSignal(list)
    # 回调获取诊断病例ID的信号
    getDiagCheckIDResSig = pyqtSignal(list)
    # 回调获取诊断病例文件名的信号
    getFileNameResSig = pyqtSignal(list)
    # 回调添加课堂信息的信号
    addLessonResSig = pyqtSignal(list)
    # 回调更新课堂信息的信号
    updateLessonResSig = pyqtSignal(list)
    # 回调删除课堂信息的信号
    delLessonResSig = pyqtSignal(list)
    # 回调获取课堂学员信息的信号
    getStudentInfoResSig = pyqtSignal(list)
    # 回调获取课堂内容信息的信号
    getContentInfoResSig = pyqtSignal(list)
    # 回调查询课堂信息的信号
    inquiryLessonInfoResSig = pyqtSignal(list)
    # 回调获取文件标注用户的信号
    getCheckUserIDResSig = pyqtSignal(list)
    addStudentResSig = pyqtSignal(list)
    getlessonStudentResSig = pyqtSignal(list)
    delStudentResSig = pyqtSignal(list)
    addLessonContentResSig = pyqtSignal(list)
    delLessonContentResSig = pyqtSignal(list)
    studentPagingResSig = pyqtSignal(list)
    searchStudentPageInfoResSig = pyqtSignal(list)
    eggPagingResSig = pyqtSignal(list)
    searchEegPageInfoResSig = pyqtSignal(list)

    # 算法管理
    # 回调获取算法信息的信号
    getAlgorithmInfoResSig = pyqtSignal(list)
    # 回调获取算法名称的信号
    getAlgorithmFileNameResSig = pyqtSignal(list)
    # 回调添加算法信息的信号
    addAlgorithmInfoResSig = pyqtSignal(list)
    # 回调删除算法的信号
    delAlgorithmInfoResSig = pyqtSignal(list)
    # 回调查询算法信息的信号
    inquiryAlgorithmInfoResSig = pyqtSignal(list)
    # 回调添加算法文件的信号
    addAlgorithmFileResSig = pyqtSignal(list)
    algorithmInfoPagingResSig = pyqtSignal(list)

    # 导入脑电
    # 回调获取脑电诊断信息信号
    getPatientCheckInfoResSig = pyqtSignal(list)
    # 回调删除脑电检查信息信号
    delPatientCheckInfoResSig = pyqtSignal(list)
    # 回调添加脑电检查信息信号
    addCheckInfoResSig = pyqtSignal(list)
    # 检查配置信息信号
    checkConfigResSig = pyqtSignal(list)
    #生成文件名信息信号
    makeFileNameResSig = pyqtSignal(list)
    # 写脑电文件信息信号
    writeEEGResSig = pyqtSignal(list)
    # 回调更新脑电检查信息
    updateCheckInfoResSig = pyqtSignal(list)
    # 回调获取脑电文件信息
    getFileInfoResSig = pyqtSignal(list)
    # 回调删除脑电文件信息
    delFileInfoResSig = pyqtSignal(list)
    # 新增
    getChoosePatientInfoResSig = pyqtSignal(list)
    getChooseDoctorInfoResSig = pyqtSignal(list)

    # 任务设置
    # 回调获取标注主题信号
    getThemeInfoResSig = pyqtSignal(list)
    # 回调添加标注主题信号
    addThemeInfoResSig = pyqtSignal(list)
    # 回调删除标注主题信号
    delThemeInfoResSig = pyqtSignal(list)
    # 回调更新标注主题信号
    updateThemeInfoResSig = pyqtSignal(list)
    # 回调获取标注任务信号
    getTaskInfoResSig = pyqtSignal(list)
    # 回调添加标注任务信号
    addTaskInfoResSig = pyqtSignal(list)
    # 回调删除标注任务信号
    delTaskInfoResSig = pyqtSignal(list)
    # 回调更新标注任务信号
    updateTaskInfoResSig = pyqtSignal(list)
    # 回调获取筛选框信息
    getChooseDetailInfoResSig = pyqtSignal(list)
    # 回调启动标注主题
    startThemeResSig = pyqtSignal(list)
    # 回调获取标注人员信息
    getChooseMarkerInfoResSig = pyqtSignal(list)

    # # 执行查看
    # # 回调获取某一用户标注主题信号
    # getUserThemeInfoResSig = pyqtSignal(list)
    # # 回调修改某一用户标注主题状态信号
    # updateUserThemeInfoResSig = pyqtSignal(list)
    # # 回调修改某一标注主题的标注状态的信号
    # updateUserTaskInfoResSig = pyqtSignal(list)
    # # 回调获取详细的标注的信息
    # getDetailInfoResSig = pyqtSignal(list)
    # # 回调删除某些详细的标注信息
    # delDetailInfoResSig = pyqtSignal(list)
    # # 回调删除某个标注任务所有详细的标注信息
    # delDetailAllResSig = pyqtSignal(list)
    # # 回调检查当前标注主题的任务评估情况
    # checkTaskStateAllResSig = pyqtSignal(list)

    # 模型训练
    # 回调获取模型界面信息的信号
    getModelInfoResSig = pyqtSignal(list)
    get_classifierInfo_by_setId_and_algIdResSig = pyqtSignal(list)
    runProcessForTrainResSig = pyqtSignal(list)
    modelAlgInfoPagingResSig = pyqtSignal(list)
    modelInquiryAlgInfoResSig = pyqtSignal(list)
    modelSetInfoPagingResSig = pyqtSignal(list)
    modelInquirySetInfoResSig = pyqtSignal(list)
    matchAlgSetResSig = pyqtSignal(list)
    getTrainPerformanceResSig = pyqtSignal(list)
    getProgressResSig = pyqtSignal(list)
    train_cancelResSig = pyqtSignal(list)

    # 模型管理
    getClassifierAlgSetNameResSig = pyqtSignal(list)
    inquiryClassifierInfoResSig = pyqtSignal(list)
    delClassifierInfoResSig = pyqtSignal(list)
    getSelectAlgorithmInfoResSig = pyqtSignal(list)
    checkClassifierInfoRessig = pyqtSignal(list)
    cls_restateRessig = pyqtSignal(list)
    checkstateRessig = pyqtSignal(list)
    model_transmit_messageRessig = pyqtSignal(list)
    classifier_id_inquiryRessig = pyqtSignal(list)
    classifierPagingResSig = pyqtSignal(list)
    classifierPaging_alResSig=pyqtSignal(list)
    inquiryCls_alg_InfoRessig=pyqtSignal(list)
    getClassifier_configRessig=pyqtSignal(list)
    getSelectSetInfoResSig =pyqtSignal(list)
    inquiryCls_set_InfoResSig=pyqtSignal(list)
    classifierPaging_setResSig=pyqtSignal(list)
    upload_schemeResSig=pyqtSignal(list)
    upload_modelResSig=pyqtSignal(list)


    # 模型测试
    classifierInfoResSig = pyqtSignal(list)
    runProcessForTestResSig = pyqtSignal(list)
    getResultResSig = pyqtSignal(list)

    # 脑电扫描
    getAutoInitDataResSig = pyqtSignal(list)
    getPatientMeasureDayResSig = pyqtSignal(list)
    getPatientFileResSig = pyqtSignal(list)
    getFileChannelsResSig = pyqtSignal(list)
    autoClassifierInfoPagingResSig = pyqtSignal(list)
    autoInquiryClassifierInfoResSig = pyqtSignal(list)
    runProcessForScanResSig = pyqtSignal(list)
    matchClassifierFileResSig = pyqtSignal(list)
    getScanProgressResSig = pyqtSignal(list)

    # 评估标注
    getAssessInfoResSig = pyqtSignal(list)
    getModelIdNameResSig = pyqtSignal(list)
    assessClassifierInfoPagingResSig = pyqtSignal(list)
    getAssessFileInfoResSig = pyqtSignal(list)
    assessOpenEEGFileResSig = pyqtSignal(list)
    assess_load_dataDynamicalResSig = pyqtSignal(list)
    assess_load_dataDynamicalResSig10 = pyqtSignal(list)
    update_labelListInfoResSig = pyqtSignal(list)
    update_labelListInfo12ResSig = pyqtSignal(list)
    update_state_labelListInfoResSig = pyqtSignal(list)
    del_labelListInfoResSig = pyqtSignal(list)
    del_labelListInfo15ResSig = pyqtSignal(list)
    del_labelListInfo16ResSig = pyqtSignal(list)

    # 清理标注
    getClearLabelInfoResSig = pyqtSignal(list)
    inquiryScanClassifierInfoResSig = pyqtSignal(list)
    scanClassifierInfoPagingResSig = pyqtSignal(list)
    getScanInfoResSig = pyqtSignal(list)
    getCurClearLabelInfoResSig = pyqtSignal(list)
    getScanFileInfoResSig = pyqtSignal(list)
    delLabelListInfoResSig = pyqtSignal(list)
    delLabelByModelFileResSig = pyqtSignal(list)
    getLabelInfoByAssessResSig = pyqtSignal(list)
    getSearchScanFileInfoResSig = pyqtSignal(list)

    def __init__(self, s_ip=None, s_port=None, cAppUtil=None):
        super().__init__()
        # tUser存放的信息顺序为
        # [uid, account, name, phone, email, administrator, labeler, student, teacher,
        # doctor, researcher, macAddr, defaultConfigID, now, curAuthority]
        self.tUser = None
        self.s_ip = s_ip
        self.s_port = s_port
        self.cAppUtil = cAppUtil
        self.macAddr = self.cAppUtil.getMacAddress()


    ## dsj [ ===

    # 学习评估/提取课程学习测试内容
    def da_get_ClassContents(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 27, self.tUser[0], REQdata]
        self.sendRequest(msg)

    def da_get_ClassContentsRes(self, REPmsg):
        self.da_get_ClassContentsResSig.emit(list(REPmsg[3]))

    # 学习评估/提取诊断信息
    def da_get_diag(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 26, self.tUser[0], REQdata]
        self.sendRequest(msg)

    def da_get_diagRes(self, REPmsg):
        self.da_get_diagResSig.emit(list(REPmsg[3]))

    # 学习评估/删除学员学习、测试记录信息
    def da_del_studentsTest(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 25, self.tUser[0], REQdata]
        self.sendRequest(msg)

    def da_del_studentsTestRes(self, REPmsg):
        self.da_del_StudentsTestResSig.emit(list(REPmsg[3]))

    # 学习评估/班级及其学员相关信息
    def da_del_class(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 24, self.tUser[0], REQdata]
        self.sendRequest(msg)

    def da_del_classRes(self, REPmsg):
        self.da_del_ClassResSig.emit(list(REPmsg[3]))

        # 学习评估/删除样本状态信息

    def da_del_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 23, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调，处理服务端回传的学习评估/删除样本状态信息 结果

    def da_del_sampleInfo_stateRes(self, REPmsg):
        self.da_del_sampleInfo_stateResSig.emit(list(REPmsg[3]))

        # 学习评估/修改样本状态信息

    def da_update_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 22, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调，处理服务端回传的学习评估/修改样本状态信息 结果

    def da_update_sampleInfo_stateRes(self, REPmsg):
        self.da_update_sampleInfo_stateResSig.emit(list(REPmsg[3]))

        # 学习评估/添加样本状态信息

    def da_add_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 21, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调，处理服务端回传的学习评估/添加样本状态信息 结果

    def da_add_sampleInfo_stateRes(self, REPmsg):
        self.da_add_sampleInfo_stateResSig.emit(list(REPmsg[3]))

        # 学习评估/删除样本信息

    def da_del_sample19(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 19, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调，处理服务端回传的学习评估/删除样本信息 结果

    def da_del_sample19Res(self, REPmsg):
        self.da_del_sample19ResSig.emit(list(REPmsg[3]))

        # 学习评估/添加样本信息

    def da_insert_sample17(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 17, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调，处理服务端回传的学习评估/添加样本信息 结果

    def da_insert_sample17Res(self, REPmsg):
        self.da_insert_sample17ResSig.emit(list(REPmsg[3]))

        # 学习评估/提取样本信息

    def da_init_SampleList(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 16, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调，处理服务端回传的学习评估/提取样本信息 结果

    def da_init_SampleListRes(self, REPmsg):
        self.da_init_SampleListResSig.emit(list(REPmsg[3]))

        # 学习评估/修改样本[脑电数据图]

    def da_update_sampleInfo15(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 15, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调，处理服务端回传的学习评估/添加样本 结果

    def da_update_sampleInfo15Res(self, REPmsg):
        self.da_update_sampleInfo15ResSig.emit(list(REPmsg[3]))

        # 学习评估/添加样本

    def da_add_sampleInfo14(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 14, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调，处理服务端回传的学习评估/添加样本 结果

    def da_add_sampleInfo14Res(self, REPmsg):
        self.da_add_sampleInfo14ResSig.emit(list(REPmsg[3]))

        # 学习评估/删除样本

    def da_del_sampleInfo13(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 13, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调，处理服务端回传的学习评估/删除样本 结果

    def da_del_sampleInfo13Res(self, REPmsg):
        self.da_del_sampleInfo13ResSig.emit(list(REPmsg[3]))

        # 学习测试/添加样本

    def da_update_sampleInfo12(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 12, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调，处理服务端回传的学习评估/添加样本 结果

    def da_update_sampleInfo12Res(self, REPmsg):
        self.da_update_sampleInfo12ResSig.emit(list(REPmsg[3]))

        # 学习评估/添加样本

    def da_add_sampleInfo11(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 11, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调，处理服务端回传的学习评估/添加样本 结果

    def da_add_sampleInfo11Res(self, REPmsg):
        self.da_add_sampleInfo11ResSig.emit(list(REPmsg[3]))

        # 学习评估/读取脑电文件数据块，拼接读取

    def da_load_dataDynamical10(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 10, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调，处理服务端回传的 学习评估/读取脑电文件数据块，拼接读取 结果

    def da_load_dataDynamical10Res(self, REPmsg):
        self.da_load_dataDynamicalResSig.emit(list(REPmsg[3]))

        # 学习评估/读取脑电文件数据块，首次读取

    def da_load_dataDynamical(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 9, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调，处理服务端回传的 学习评估/读取脑电文件数据块，首次读取结果

    def da_load_dataDynamicalRes(self, REPmsg):
        self.da_load_dataDynamicalResSig.emit(list(REPmsg[3]))

        # 学习评估/打开脑电文件

    def da_openEEGFile(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 8, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调，处理服务端回传的学习评估/打开脑电文件结果

    def da_openEEGFileRes(self, REPmsg):
        self.da_openEEGFileResSig.emit(list(REPmsg[3]))

        # 学习评估/类型、用户信息

    def da_get_type_info(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 4, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调，脑电会诊 处理服务端回传的学习评估/类型、用户信息结果

    def da_get_type_infoRes(self, REPmsg):
        self.da_get_type_infoResSig.emit(list(REPmsg[3]))

    def da_get_ClassStudent(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 2, self.tUser[0], REQdata]
        self.sendRequest(msg)

            # 回调 学习评估/提取诊断信息

    def da_get_ClassStudentRes(self, REPmsg):
        self.da_get_ClassStudentResSig.emit(list(REPmsg[3]))

        # 学习评估/提取学习测试信息
    def da_get_contents(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["testAssess", 1, self.tUser[0], REQdata]
        self.sendRequest(msg)

        # 回调 学习评估/提取诊断信息
    def da_get_contentsRes(self, REPmsg):
        self.da_get_contentsResSig.emit(list(REPmsg[3]))


    #学习测试/保存并提交诊断信息
    def dt_diagTest_commit(self,REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 28, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 学习测试/完成诊断信息
    def dt_diagTest_commitRes(self, REPmsg):
        self.dt_diagTest_commitResSig.emit(list(REPmsg[3]))

    # 学习测试/删除样本状态信息
    def dt_del_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 23, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的学习测试/删除样本状态信息 结果
    def dt_del_sampleInfo_stateRes(self, REPmsg):
        self.dt_del_sampleInfo_stateResSig.emit(list(REPmsg[3]))

    #学习测试/修改样本状态信息
    def dt_update_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 22, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的学习测试/修改样本状态信息 结果
    def dt_update_sampleInfo_stateRes(self, REPmsg):
        self.dt_update_sampleInfo_stateResSig.emit(list(REPmsg[3]))

    # 学习测试/添加样本状态信息
    def dt_add_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 21, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的学习测试/添加样本状态信息 结果
    def dt_add_sampleInfo_stateRes(self, REPmsg):
        self.dt_add_sampleInfo_stateResSig.emit(list(REPmsg[3]))

    # 学习测试/删除样本信息
    def dt_del_sample19(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 19, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的学习测试/删除样本信息 结果
    def dt_del_sample19Res(self, REPmsg):
        self.dt_del_sample19ResSig.emit(list(REPmsg[3]))

    # 学习测试/添加样本信息
    def dt_insert_sample17(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 17, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的学习测试/添加样本信息 结果
    def dt_insert_sample17Res(self, REPmsg):
        self.dt_insert_sample17ResSig.emit(list(REPmsg[3]))

    # 学习测试/提取样本信息
    def dt_init_SampleList(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 16, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的学习测试/提取样本信息 结果
    def dt_init_SampleListRes(self, REPmsg):
        self.dt_init_SampleListResSig.emit(list(REPmsg[3]))

    # 学习测试/修改样本[脑电数据图]
    def dt_update_sampleInfo15(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 15, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的学习测试/添加样本 结果
    def dt_update_sampleInfo15Res(self, REPmsg):
        self.dt_update_sampleInfo15ResSig.emit(list(REPmsg[3]))

    # 学习测试/添加样本
    def dt_add_sampleInfo14(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 14, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的学习测试/添加样本 结果
    def dt_add_sampleInfo14Res(self, REPmsg):
        self.dt_add_sampleInfo14ResSig.emit(list(REPmsg[3]))

    # 学习测试/删除样本
    def dt_del_sampleInfo13(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 13, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的学习测试/删除样本 结果
    def dt_del_sampleInfo13Res(self, REPmsg):
        self.dt_del_sampleInfo13ResSig.emit(list(REPmsg[3]))

    # 学习测试/添加样本
    def dt_update_sampleInfo12(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 12, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的学习测试/添加样本 结果
    def dt_update_sampleInfo12Res(self, REPmsg):
        self.dt_update_sampleInfo12ResSig.emit(list(REPmsg[3]))

    # 学习测试/添加样本
    def dt_add_sampleInfo11(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 11, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的学习测试/添加样本 结果
    def dt_add_sampleInfo11Res(self, REPmsg):
        self.dt_add_sampleInfo11ResSig.emit(list(REPmsg[3]))

    # 学习测试/读取脑电文件数据块，拼接读取
    def dt_load_dataDynamical10(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 10, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 学习测试/读取脑电文件数据块，拼接读取 结果
    def dt_load_dataDynamical10Res(self, REPmsg):
        self.dt_load_dataDynamicalResSig.emit(list(REPmsg[3]))

    # 学习测试/读取脑电文件数据块，首次读取
    def dt_load_dataDynamical(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 9, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 学习测试/读取脑电文件数据块，首次读取结果
    def dt_load_dataDynamicalRes(self, REPmsg):
        self.dt_load_dataDynamicalResSig.emit(list(REPmsg[3]))

    # 学习测试/打开脑电文件
    def dt_openEEGFile(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 8, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的学习测试/打开脑电文件结果
    def dt_openEEGFileRes(self, REPmsg):
        self.dt_openEEGFileResSig.emit(list(REPmsg[3]))


    # 学习测试/类型、用户信息
    def dt_get_type_info(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 4, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，脑电会诊 处理服务端回传的学习测试/类型、用户信息结果
    def dt_get_type_infoRes(self, REPmsg):
        self.dt_get_type_infoResSig.emit(list(REPmsg[3]))


    # 学习测试/提取学习测试信息
    def dt_get_contents(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTest", 1, self.tUser[0], REQdata]
        self.sendRequest(msg)

    #回调 学习测试/提取诊断信息
    def dt_get_contentsRes(self, REPmsg):
        self.dt_get_contentsResSig.emit(list(REPmsg[3]))


    # 诊断学习/提取诊断信息
    def dl_get_diag(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTraining", 25, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调 诊断学习/提取诊断信息信号
    def dl_get_diagRes(self, REPmsg):
        self.dl_get_diagResSig.emit(list(REPmsg[3]))

    # 诊断学习/提取样本信息
    def dl_init_SampleList(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTraining", 16, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的诊断学习/提取样本信息 结果
    def dl_init_SampleListRes(self, REPmsg):
        self.dl_init_SampleListResSig.emit(list(REPmsg[3]))

    # 诊断学习/读取脑电文件数据块，拼接读取
    def dl_load_dataDynamical10(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTraining", 10, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 诊断学习/读取脑电文件数据块，拼接读取 结果
    def dl_load_dataDynamical10Res(self, REPmsg):
        self.dl_load_dataDynamicalResSig.emit(list(REPmsg[3]))

    # 诊断学习/读取脑电文件数据块，首次读取
    def dl_load_dataDynamical(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTraining", 9, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 诊断学习/读取脑电文件数据块，首次读取结果
    def dl_load_dataDynamicalRes(self, REPmsg):
        self.dl_load_dataDynamicalResSig.emit(list(REPmsg[3]))


    # 诊断学习/打开脑电文件
    def dl_openEEGFile(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTraining", 8, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 诊断学习/打开脑电文件结果
    def dl_openEEGFileRes(self, REPmsg):
        self.dl_openEEGFileResSig.emit(list(REPmsg[3]))

    # 诊断学习/类型、用户信息
    def dl_get_type_info(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTraining", 4, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的诊断学习/类型、用户信息结果
    def dl_get_type_infoRes(self, REPmsg):
        self.dl_get_type_infoResSig.emit(list(REPmsg[3]))

    # 诊断学习/学习记录结束，更新结束时间，不返回
    def dl_study_end(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTraining", 3, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 诊断学习/学习记录信息
    def dl_get_studyInfo(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTraining", 2, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，诊断学习/学习记录信息
    def dl_get_studyInfoRes(self, REPmsg):
        self.dl_get_studyInfoResSig.emit(list(REPmsg[3]))

    # 诊断学习/提取诊断信息
    def dl_get_contents(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["diagTraining", 1, self.tUser[0], REQdata]
        self.sendRequest(msg)

    #回调 诊断学习/提取诊断信息
    def dl_get_contentsRes(self, REPmsg):
        self.dl_get_contentsResSig.emit(list(REPmsg[3]))

    def ct_diag_refused(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 29, self.tUser[0], REQdata]
        self.sendRequest(msg)

    def ct_diag_refusedRes(self, REPmsg):
        self.ct_diag_refusedResSig.emit(list(REPmsg[3]))

    #脑电会诊/修改诊断信息
    def  ct_diag_update(self,REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 27, self.tUser[0], REQdata]
        self.sendRequest(msg)
        # 脑电会诊/修改诊断信息

    #回调 脑电会诊/修改诊断信息
    def ct_diag_updateRes(self, REQdata):
        self.ct_diag_updateResSig.emit(list(REQdata[3]))

    #脑电会诊/保存并提交诊断信息
    def  ct_diag_commit(self,REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 28, self.tUser[0], REQdata]
        self.sendRequest(msg)
    # 诊断标注/完成诊断信息
    def  ct_diag_commitRes(self, REPmsg):
        self.ct_diag_commitResSig.emit(list(REPmsg[3]))


    # 脑电会诊/提取诊断信息
    def  ct_get_diag(self,REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 25, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调 诊断标注/提取诊断信息信号
    def ct_get_diagRes(self, REPmsg):
        self.ct_get_diagResSig.emit(list(REPmsg[3]))


    # 脑电会诊/提取未诊断信息
    def  ct_get_diags_notDiag(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 24, self.tUser[0], REQdata]
        self.sendRequest(msg)

    #回调 诊断标注/提取未诊断信息
    def  ct_get_diags_notDiagRes(self,  REPmsg):
        self.ct_get_diags_notDiagResSig.emit(list(REPmsg[3]))

    # 脑电会诊/删除样本状态信息
    def ct_del_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 23, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的脑电会诊/删除样本状态信息 结果
    def ct_del_sampleInfo_stateRes(self, REPmsg):
        self.ct_del_sampleInfo_stateResSig.emit(list(REPmsg[3]))

    # 脑电会诊/修改样本状态信息
    def ct_update_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 22, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的脑电会诊/修改样本状态信息 结果
    def ct_update_sampleInfo_stateRes(self, REPmsg):
        self.ct_update_sampleInfo_stateResSig.emit(list(REPmsg[3]))

    # 脑电会诊/添加样本状态信息
    def ct_add_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 21, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的脑电会诊/添加样本状态信息 结果
    def ct_add_sampleInfo_stateRes(self, REPmsg):
        self.ct_add_sampleInfo_stateResSig.emit(list(REPmsg[3]))

    # 脑电会诊/删除样本信息
    def ct_del_sample19(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 19, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的脑电会诊/删除样本信息 结果
    def ct_del_sample19Res(self, REPmsg):
        self.ct_del_sample19ResSig.emit(list(REPmsg[3]))

    # 脑电会诊/添加样本信息
    def ct_insert_sample17(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 17, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的脑电会诊/添加样本信息 结果
    def ct_insert_sample17Res(self, REPmsg):
        self.ct_insert_sample17ResSig.emit(list(REPmsg[3]))

    # 脑电会诊/提取样本信息
    def ct_init_SampleList(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 16, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的脑电会诊/提取样本信息 结果
    def ct_init_SampleListRes(self, REPmsg):
        self.ct_init_SampleListResSig.emit(list(REPmsg[3]))

    # 脑电会诊/修改样本[脑电数据图]
    def ct_update_sampleInfo15(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 15, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的脑电会诊/添加样本 结果
    def ct_update_sampleInfo15Res(self, REPmsg):
        self.ct_update_sampleInfo15ResSig.emit(list(REPmsg[3]))

    # 脑电会诊/添加样本
    def ct_add_sampleInfo14(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 14, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的脑电会诊/添加样本 结果
    def ct_add_sampleInfo14Res(self, REPmsg):
        self.ct_add_sampleInfo14ResSig.emit(list(REPmsg[3]))

    # 脑电会诊/删除样本
    def ct_del_sampleInfo13(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 13, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的脑电会诊/删除样本 结果
    def ct_del_sampleInfo13Res(self, REPmsg):
        self.ct_del_sampleInfo13ResSig.emit(list(REPmsg[3]))

    # 脑电会诊/添加样本
    def ct_update_sampleInfo12(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 12, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/添加样本 结果
    def ct_update_sampleInfo12Res(self, REPmsg):
        self.ct_update_sampleInfo12ResSig.emit(list(REPmsg[3]))

    # 脑电会诊/添加样本
    def ct_add_sampleInfo11(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 11, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/添加样本 结果
    def ct_add_sampleInfo11Res(self, REPmsg):
        self.ct_add_sampleInfo11ResSig.emit(list(REPmsg[3]))

    # 脑电会诊/读取脑电文件数据块，拼接读取
    def ct_load_dataDynamical10(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 10, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 脑电会诊/读取脑电文件数据块，拼接读取 结果
    def ct_load_dataDynamical10Res(self, REPmsg):
        self.ct_load_dataDynamicalResSig.emit(list(REPmsg[3]))

    # 脑电会诊/读取脑电文件数据块，首次读取
    def ct_load_dataDynamical(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 9, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 脑电会诊/读取脑电文件数据块，首次读取结果
    def ct_load_dataDynamicalRes(self, REPmsg):
        self.ct_load_dataDynamicalResSig.emit(list(REPmsg[3]))

    # 脑电会诊/打开脑电文件
    def ct_openEEGFile(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 8, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的脑电会诊/打开脑电文件结果
    def ct_openEEGFileRes(self, REPmsg):
        self.ct_openEEGFileResSig.emit(list(REPmsg[3]))

    # 脑电会诊/脑电文件
    def ct_get_fileNameByIdDate(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 7, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的脑电会诊/脑电文件结果
    def ct_get_fileNameByIdDateRes(self, REPmsg):
        self.ct_get_fileNameByIdDateResSig.emit(list(REPmsg[3]))


    # 脑电会诊/类型、用户信息
    def ct_get_type_info(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 4, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，脑电会诊 处理服务端回传的脑电会诊/类型、用户信息结果
    def ct_get_type_infoRes(self, REPmsg):
        self.ct_get_type_infoResSig.emit(list(REPmsg[3]))

    # 脑电会诊/提取诊断信息
    def ct_main_get_diag(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["consulting", 3, self.tUser[0], REQdata]
        self.sendRequest(msg)
        # 回调，脑电会诊 提取诊断信息
    def ct_main_get_diagRes(self, REPmsg):
        self.ct_main_get_diagResSig.emit(list(REPmsg[3]))

    # 诊断查询/提取诊断信息

    # 向服务器发送创建会诊的请求
    def createCons(self, REQdata):
        msg = ["createCons", 4, self.tUser[0], [self.macAddr] + REQdata]
        self.sendRequest(msg)

    def createConsRes(self, REPmsg):
        print(f'createConsRes')
        self.createConsResSig.emit([REPmsg[3][0], REPmsg[3][2]])


    # 诊断标注/提取诊断信息
    def mq_paging(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 30, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调 诊断查询/提取诊断信息信号
    def mq_pagingRes(self, REPmsg):
        self.mq_pagingResSig.emit(list(REPmsg[3]))

    # 诊断查询/提取诊断信息
    def mq_get_diag(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 25, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调 诊断查询/提取诊断信息信号
    def mq_get_diagRes(self, REPmsg):
        self.mq_get_diagResSig.emit(list(REPmsg[3]))

    # 诊断查询/提取样本信息
    def mq_init_SampleList(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 16, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的诊断查询/提取样本信息 结果
    def mq_init_SampleListRes(self, REPmsg):
        self.mq_init_SampleListResSig.emit(list(REPmsg[3]))

    # 诊断查询/读取脑电文件数据块，拼接读取
    def mq_load_dataDynamical10(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 10, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 诊断查询/读取脑电文件数据块，拼接读取 结果
    def mq_load_dataDynamical10Res(self, REPmsg):
        self.mq_load_dataDynamicalResSig.emit(list(REPmsg[3]))

    # 诊断查询/读取脑电文件数据块，首次读取
    def mq_load_dataDynamical(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 9, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 诊断查询/读取脑电文件数据块，首次读取结果
    def mq_load_dataDynamicalRes(self, REPmsg):
        self.mq_load_dataDynamicalResSig.emit(list(REPmsg[3]))


    # 诊断查询/打开脑电文件
    def mq_openEEGFile(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 8, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的诊断查询/打开脑电文件结果
    def mq_openEEGFileRes(self, REPmsg):
        self.mq_openEEGFileResSig.emit(list(REPmsg[3]))

    # 诊断查询/脑电文件
    def mq_get_fileNameByIdDate(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 7, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的诊断查询/脑电文件结果
    def mq_get_fileNameByIdDateRes(self, REPmsg):
        self.mq_get_fileNameByIdDateResSig.emit(list(REPmsg[3]))


    # 诊断查询/类型、用户信息
    def mq_get_type_info(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 4, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的诊断查询/类型、用户信息结果
    def mq_get_type_infoRes(self, REPmsg):
        self.mq_get_type_infoResSig.emit(list(REPmsg[3]))

    # 诊断查询/提取诊断信息
    def mq_get_diags_Diagnosed(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 1, self.tUser[0], REQdata]
        self.sendRequest(msg)

    #回调 诊断查询/提取诊断信息
    def mq_get_diags_DiagnosedRes(self, REPmsg):
        self.mq_get_diags_DiagnosedResSig.emit(list(REPmsg[3]))

    # 诊断标注/拒绝诊断
    def diag_refused(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 29, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调 诊断标注/拒绝诊断
    def  diag_refusedRes(self, REPmsg):
        self.diag_refusedResSig.emit(list(REPmsg[3]))

    #诊断标注/修改诊断信息
    def  diag_update(self,REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 27, self.tUser[0], REQdata]
        self.sendRequest(msg)
        # 诊断标注/完成诊断信息

    # 回调 诊断标注/修改诊断信息
    def diag_updateRes(self, REPmsg):
        self.diag_updateResSig.emit(list(REPmsg[3]))

    #诊断标注/保存并提交诊断信息
    def  diag_commit(self,REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 28, self.tUser[0], REQdata]
        self.sendRequest(msg)
    # 回调 诊断标注/完成诊断信息
    def  diag_commitRes(self, REPmsg):
        self.diag_commitResSig.emit(list(REPmsg[3]))

    # 诊断标注/提取诊断信息
    def  get_diag(self,REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 25, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调 诊断标注/提取诊断信息信号
    def get_diagRes(self, REPmsg):
        self.get_diagResSig.emit(list(REPmsg[3]))


    # 诊断标注/提取未诊断信息
    def  get_diags_notDiag(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 24, self.tUser[0], REQdata]
        self.sendRequest(msg)

    #回调 诊断标注/提取未诊断信息
    def  get_diags_notDiagRes(self,  REPmsg):
        self.get_diags_notDiagResSig.emit(list(REPmsg[3]))

    # 标注诊断/删除样本状态信息
    def del_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 23, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/删除样本状态信息 结果
    def del_sampleInfo_stateRes(self, REPmsg):
        self.del_sampleInfo_stateResSig.emit(list(REPmsg[3]))

    # 标注诊断/修改样本状态信息
    def update_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 22, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/修改样本状态信息 结果
    def update_sampleInfo_stateRes(self, REPmsg):
        self.update_sampleInfo_stateResSig.emit(list(REPmsg[3]))

    # 标注诊断/添加样本状态信息
    def add_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 21, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/添加样本状态信息 结果
    def add_sampleInfo_stateRes(self, REPmsg):
        self.add_sampleInfo_stateResSig.emit(list(REPmsg[3]))

    # 标注诊断/删除样本信息
    def del_sample19(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 19, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/删除样本信息 结果
    def del_sample19Res(self, REPmsg):
        self.del_sample19ResSig.emit(list(REPmsg[3]))

    # 标注诊断/添加样本信息
    def insert_sample17(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 17, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/添加样本信息 结果
    def insert_sample17Res(self, REPmsg):
        self.insert_sample17ResSig.emit(list(REPmsg[3]))

    # 标注诊断/提取样本信息
    def init_SampleList(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 16, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/提取样本信息 结果
    def init_SampleListRes(self, REPmsg):
        self.init_SampleListResSig.emit(list(REPmsg[3]))

    # 标注诊断/修改样本[脑电数据图]
    def update_sampleInfo15(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 15, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/添加样本 结果
    def update_sampleInfo15Res(self, REPmsg):
        self.update_sampleInfo15ResSig.emit(list(REPmsg[3]))

    # 标注诊断/添加样本
    def add_sampleInfo14(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 14, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/添加样本 结果
    def add_sampleInfo14Res(self, REPmsg):
        self.add_sampleInfo14ResSig.emit(list(REPmsg[3]))

    # 标注诊断/删除样本
    def del_sampleInfo13(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 13, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/删除样本 结果
    def del_sampleInfo13Res(self, REPmsg):
        self.del_sampleInfo13ResSig.emit(list(REPmsg[3]))

    # 标注诊断/添加样本
    def update_sampleInfo12(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 12, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/添加样本 结果
    def update_sampleInfo12Res(self, REPmsg):
        self.update_sampleInfo12ResSig.emit(list(REPmsg[3]))

    # 标注诊断/添加样本
    def add_sampleInfo11(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 11, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/添加样本 结果
    def add_sampleInfo11Res(self, REPmsg):
        self.add_sampleInfo11ResSig.emit(list(REPmsg[3]))

    # 标注诊断/读取脑电文件数据块，拼接读取
    def load_dataDynamical10(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 10, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 标注诊断/读取脑电文件数据块，拼接读取 结果
    def load_dataDynamical10Res(self, REPmsg):
        self.load_dataDynamicalResSig.emit(list(REPmsg[3]))

    # 标注诊断/读取脑电文件数据块，首次读取
    def load_dataDynamical(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 9, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 标注诊断/读取脑电文件数据块，首次读取结果
    def load_dataDynamicalRes(self, REPmsg):
        self.load_dataDynamicalResSig.emit(list(REPmsg[3]))

    # 标注诊断/打开脑电文件
    def openEEGFile(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 8, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/打开脑电文件结果
    def openEEGFileRes(self, REPmsg):
        self.openEEGFileResSig.emit(list(REPmsg[3]))

    # 标注诊断/脑电文件
    def get_fileNameByIdDate(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 7, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/脑电文件结果
    def get_fileNameByIdDateRes(self, REPmsg):
        self.get_fileNameByIdDateResSig.emit(list(REPmsg[3]))


    # 标注诊断/类型、用户信息
    def get_type_info(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manual", 4, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的标注诊断/类型、用户信息结果
    def get_type_infoRes(self, REPmsg):
        self.get_type_infoResSig.emit(list(REPmsg[3]))

    # 科研标注/提取标注信息
    def rg_paging(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 30, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调 科研标注/提取标注信息信号
    def rg_pagingRes(self, REPmsg):
        self.rg_pagingResSig.emit(list(REPmsg[3]))

    #
    # 科研标注/保存并提交标注信息
    def rg_label_commit(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 28, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调 科研标注/保存并提交标注信息
    def rg_label_commitRes(self, REPmsg):
        self.rg_label_commitResSig.emit(list(REPmsg[3]))

    # 科研标注/删除样本状态信息
    def rg_del_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 23, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的科研标注/删除样本状态信息 结果
    def rg_del_sampleInfo_stateRes(self, REPmsg):
        self.rg_del_sampleInfo_stateResSig.emit(list(REPmsg[3]))

    # 科研标注/修改样本状态信息
    def rg_update_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 22, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的科研标注/修改样本状态信息 结果
    def rg_update_sampleInfo_stateRes(self, REPmsg):
        self.rg_update_sampleInfo_stateResSig.emit(list(REPmsg[3]))

    # 科研标注/添加样本状态信息
    def rg_add_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 21, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的科研标注/添加样本状态信息 结果
    def rg_add_sampleInfo_stateRes(self, REPmsg):
        self.rg_add_sampleInfo_stateResSig.emit(list(REPmsg[3]))

    # 科研标注/删除样本信息
    def rg_del_sample19(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 19, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的科研标注/删除样本信息 结果
    def rg_del_sample19Res(self, REPmsg):
        self.rg_del_sample19ResSig.emit(list(REPmsg[3]))

    # 科研标注/添加样本信息
    def rg_insert_sample17(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 17, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的科研标注/添加样本信息 结果
    def rg_insert_sample17Res(self, REPmsg):
        self.rg_insert_sample17ResSig.emit(list(REPmsg[3]))

    # 科研标注/提取样本信息
    def rg_init_SampleList(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 16, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的科研标注提取样本信息 结果
    def rg_init_SampleListRes(self, REPmsg):
        self.rg_init_SampleListResSig.emit(list(REPmsg[3]))

    # 科研标注/修改样本[脑电数据图]
    def rg_update_sampleInfo15(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 15, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的科研标注/添加样本 结果
    def rg_update_sampleInfo15Res(self, REPmsg):
        self.rg_update_sampleInfo15ResSig.emit(list(REPmsg[3]))

    # 科研标注/添加样本
    def rg_add_sampleInfo14(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 14, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的科研标注/添加样本 结果
    def rg_add_sampleInfo14Res(self, REPmsg):
        self.rg_add_sampleInfo14ResSig.emit(list(REPmsg[3]))

    # 科研标注/删除样本
    def rg_del_sampleInfo13(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 13, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的科研标注/删除样本 结果
    def rg_del_sampleInfo13Res(self, REPmsg):
        self.rg_del_sampleInfo13ResSig.emit(list(REPmsg[3]))

    # 科研标注/添加样本
    def rg_update_sampleInfo12(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 12, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的科研标注/添加样本 结果
    def rg_update_sampleInfo12Res(self, REPmsg):
        self.rg_update_sampleInfo12ResSig.emit(list(REPmsg[3]))

    # 科研标注/读取脑电文件数据块，拼接读取
    def rg_load_dataDynamical10(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 10, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 科研标注/读取脑电文件数据块，拼接读取 结果
    def rg_load_dataDynamical10Res(self, REPmsg):
        self.rg_load_dataDynamicalResSig.emit(list(REPmsg[3]))

    # 科研标注/读取脑电文件数据块，首次读取
    def rg_load_dataDynamical(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 9, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 科研标注/读取脑电文件数据块，首次读取结果
    def rg_load_dataDynamicalRes(self, REPmsg):
        self.rg_load_dataDynamicalResSig.emit(list(REPmsg[3]))

    # 科研标注/打开脑电文件
    def rg_openEEGFile(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 8, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的科研标注/打开脑电文件结果
    def rg_openEEGFileRes(self, REPmsg):
        self.rg_openEEGFileResSig.emit(list(REPmsg[3]))

    # 科研标注/类型、用户信息
    def rg_get_type_info(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 4, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的科研标注/类型、用户信息结果
    def rg_get_type_infoRes(self, REPmsg):
        self.rg_get_type_infoResSig.emit(list(REPmsg[3]))
        # 科研标注/提取未标注信息

    def rg_get_notlabels(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserching", 1, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调科研标注/提取未标注信息
    def rg_get_notlabelsRes(self, REPmsg):
        self.rg_get_notlabelsResSig.emit(list(REPmsg[3]))

    # 执行查看/提取标注信息
    def rgQ_theme_commit(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 31, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调 执行查看/提取标注信息信号
    def rgQ_theme_commitRes(self, REPmsg):
        self.rgQ_theme_commitResSig.emit(list(REPmsg[3]))

    # 执行查看/提取标注信息
    def rgQ_paging(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 30, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调 执行查看/提取标注信息信号
    def rgQ_pagingRes(self, REPmsg):
        self.rgQ_pagingResSig.emit(list(REPmsg[3]))

    #
    # 执行查看/提交标注信息
    def rgQ_label_commit(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 28, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调 执行查看/保存并提交标注信息
    def rgQ_label_commitRes(self, REPmsg):
        self.rgQ_label_commitResSig.emit(list(REPmsg[3]))

    # 科研标注/删除样本状态信息
    def rgQ_del_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 23, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的执行查看/删除样本状态信息 结果
    def rgQ_del_sampleInfo_stateRes(self, REPmsg):
        self.rgQ_del_sampleInfo_stateResSig.emit(list(REPmsg[3]))

    # 执行查看/修改样本状态信息
    def rgQ_update_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 22, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的执行查看/修改样本状态信息 结果
    def rgQ_update_sampleInfo_stateRes(self, REPmsg):
        self.rgQ_update_sampleInfo_stateResSig.emit(list(REPmsg[3]))

    # 执行查看/添加样本状态信息
    def rgQ_add_sampleInfo_state(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 21, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的执行查看/添加样本状态信息 结果
    def rgQ_add_sampleInfo_stateRes(self, REPmsg):
        self.rgQ_add_sampleInfo_stateResSig.emit(list(REPmsg[3]))

    # 执行查看/删除样本信息
    def rgQ_del_sample19(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 19, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的执行查看/删除样本信息 结果
    def rgQ_del_sample19Res(self, REPmsg):
        self.rgQ_del_sample19ResSig.emit(list(REPmsg[3]))

    # 执行查看/提取样本信息
    def rgQ_init_SampleList(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 16, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的执行查看提取样本信息 结果
    def rgQ_init_SampleListRes(self, REPmsg):
        self.rgQ_init_SampleListResSig.emit(list(REPmsg[3]))

    # 执行查看/修改样本[脑电数据图]
    def rgQ_update_sampleInfo15(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 15, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的执行查看/添加样本 结果
    def rgQ_update_sampleInfo15Res(self, REPmsg):
        self.rgQ_update_sampleInfo15ResSig.emit(list(REPmsg[3]))

    # 科研标注/删除样本
    def rgQ_del_sampleInfo13(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 13, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的科研标注/删除样本 结果
    def rgQ_del_sampleInfo13Res(self, REPmsg):
        self.rgQ_del_sampleInfo13ResSig.emit(list(REPmsg[3]))

    # 执行查看/添加样本
    def rgQ_update_sampleInfo12(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 12, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的执行查看/添加样本 结果
    def rgQ_update_sampleInfo12Res(self, REPmsg):
        self.rgQ_update_sampleInfo12ResSig.emit(list(REPmsg[3]))

    # 执行查看/读取脑电文件数据块，拼接读取
    def rgQ_load_dataDynamical10(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 10, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 执行查看/读取脑电文件数据块，拼接读取 结果
    def rgQ_load_dataDynamical10Res(self, REPmsg):
        self.rgQ_load_dataDynamicalResSig.emit(list(REPmsg[3]))

    # 执行查看/读取脑电文件数据块，首次读取
    def rgQ_load_dataDynamical(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 9, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 执行查看/读取脑电文件数据块，首次读取结果
    def rgQ_load_dataDynamicalRes(self, REPmsg):
        self.rgQ_load_dataDynamicalResSig.emit(list(REPmsg[3]))

    # 执行查看/打开脑电文件
    def rgQ_openEEGFile(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 8, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的执行查看/打开脑电文件结果
    def rgQ_openEEGFileRes(self, REPmsg):
        self.rgQ_openEEGFileResSig.emit(list(REPmsg[3]))

    # 执行查看/类型、用户信息
    def rgQ_get_type_info(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 4, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的执行查看/类型、用户信息结果
    def rgQ_get_type_infoRes(self, REPmsg):
        self.rgQ_get_type_infoResSig.emit(list(REPmsg[3]))

    # 执行查看/提取未标注信息
    def rgQ_get_labels(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["reserchingQuery", 1, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调执行查看/提取未标注信息
    def rgQ_get_labelsRes(self, REPmsg):
        self.rgQ_get_labelsResSig.emit(list(REPmsg[3]))







    ## dsj ] ===
    # 登录功能
    # 向服务端发送用户登录请求
    def login(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["login", 1, 0, REQmsg]
        self.isConnected = True
        self.sockOpenConn(self.s_ip, self.s_port)
        threading.Thread(target=self.receive_service_data).start()
        self.sendRequest(msg)

    # 回调，处理服务端回传的登录结果
    def loginRes(self, REPmsg):
        self.tUser = REPmsg[3][2]
        case = REPmsg[3][0]
        msg = REPmsg[3][1]
        print(f"loginRes REPData[3]: {self.tUser}")
        self.loginResSig.emit(case, msg)

    # 切换用户功能
    # 向服务端发送用户退出请求
    def logout(self, cmid):
        account = self.tUser[1]
        REQmsg = [account]
        REQmsg.insert(0, self.macAddr)
        msg = [cmid, 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务端回传的登出处理结果
    def logoutRes(self, REPData):
        data = REPData[3]
        self.logoutResSig.emit(list(data))
        self.sockClose()

    # 回调，处理服务端回传的退出处理结果
    def quitRes(self, revData):
        self.quitResSig.emit()

    # 修改密码功能
    # 向服务器发送修改密码请求
    def changePwd(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["pwd", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务端回传的修改密码处理结果
    def pwdRes(self, REPData):
        self.changePwdResSig.emit(list(REPData[3]))

    # 用户管理功能
    # 向服务器发送获取用户信息请求
    def getUserInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["userManager", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务器获取用户信息结果
    def getUserInfoRes(self, REPData):
        self.getUserInfoResSig.emit(list(REPData[3]))

    # 向服务器发送新增用户信息请求
    def addUserInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["userManager", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务器新增用户信息结果
    def addUserInfoRes(self, REPData):
        self.addUserInfoResSig.emit(list(REPData[3]))

    # 向服务器发送删除用户信息请求
    def delUserInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["userManager", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务器删除用户信息结果
    def delUserInfoRes(self, REPData):
        self.delUserInfoResSig.emit(list(REPData[3]))

    # 向服务器发送编辑用户信息请求
    def updateUserInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["userManager", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务器编辑用户信息结果
    def updateUserInfoRes(self, REPData):
        self.updateUserInfoResSig.emit(list(REPData[3]))

    def userPaging(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["userManager", 5, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务器获取用户信息结果
    def userPagingRes(self, REPData):
        self.userPagingResSig.emit(list(REPData[3]))

    def inquiryUserInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["userManager", 6, self.tUser[0], REQmsg]
        self.sendRequest(msg)

        # 回调，处理服务器获取用户信息结果

    def inquiryUserInfoRes(self, REPData):
        self.inquiryUserInfoResSig.emit(list(REPData[3]))

    def getConfigData(self):
        msg = ["basicConfig", 1, self.tUser[0], [self.macAddr]]
        self.sendRequest(msg)

        # 回调，处理服务器回传的基本配置信息

    def getConfigRes(self, REPData):
        self.getConfigDataResSig.emit(list(REPData[3][3]))

        # 向服务器发送添加基本配置的请求

    def addBasicConfig(self, REQmsg):
        msg = ["basicConfig", 2, self.tUser[0], [self.macAddr] + REQmsg]
        self.sendRequest(msg)

        # 回调，处理服务器回传的基本配置信息

    def addBasicConfigRes(self, REPData):
        print(f'addBasicConfigRes: {REPData}')
        self.addBasicConfigResSig.emit(REPData[3][3])

        # 向服务器发送修改基本配置的逻辑

    def updateBasicConfig(self, REQmsg):
        msg = ["basicConfig", 4, self.tUser[0], [self.macAddr] + REQmsg]
        self.sendRequest(msg)

        # 回调，处理服务器传回来的更新基本配置结果

    def updateBasicConfigRes(self, REPData):
        self.updBasicConfigResSig.emit([REPData[3][0], REPData[3][3]])

        # 向服务器发送删除基本配置的请求

    def delBasicConfig(self, REQmsg):
        msg = ["basicConfig", 3, self.tUser[0], [self.macAddr] + REQmsg]
        self.sendRequest(msg)

        # 回调，处理服务器传回来的基本配置结果

    def delBasicConfigRes(self, REPData):
        self.delBasicConfigResSig.emit([REPData[3][0], REPData[3][3]])

        # 获取默认的基本配置

    def getCurConfigData(self):
        msg = ["configOptions", 1, self.tUser[0], [self.macAddr, self.tUser[12]]]
        print(f'getCurConfigData MSG: {msg}')
        self.sendRequest(msg)

    def getCurConfigDataRes(self, REPData):
        print(f'getCurConfigDataRes ...')
        self.getCurConfigDataResSig.emit(REPData[3][3])


    def getAllConfigData(self):
        msg = ["configOptions", 2, self.tUser[0], [self.macAddr]]
        self.sendRequest(msg)

    def getAllConfigDataRes(self, REPData):
        self.getAllConfigDataResSig.emit(list(REPData[3][3]))


    def chgCurUserConfig(self, REQmsg):
        msg = ["configOptions", 3, self.tUser[0], [self.macAddr] + REQmsg]
        self.sendRequest(msg)

    def chgCurUserConfigRes(self, REPData):
        self.chgCurUserConfigResSig.emit(list(REPData[3][0]))


    # 导联配置功能
    # 向服务器发送获取导联配置信息的请求
    def getMontage(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["montage", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取导联配置信息的结果
    def getMontageRes(self, REPData):
        self.getMontageResSig.emit(list(REPData[3]))

    # 向服务器发送添加导联配置方案的请求
    def addMontageScheme(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["montage", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器添加导联方案的结果
    def addMontageSchemeRes(self, REPData):
        self.addMontageSchemeResSig.emit(list(REPData[3]))

    # 向服务器发送编辑导联配置方案的请求
    def editMontageScheme(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["montage", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器编辑导联方案的结果
    def editMontageSchemeRes(self, REPData):
        self.editMontageSchemeResSig.emit(list(REPData[3]))

    # 向服务器发送删除导联配置方案的请求
    def delMontageScheme(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["montage", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器删除导联方案的结果
    def delMontageSchemeRes(self, REPData):
        self.delMontageSchemeResSig.emit(list(REPData[3]))

    # 向服务器发送添加导联配置方案的请求
    def saveMontageChannel(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["montage", 5, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器添加导联方案的结果
    def saveMontageChannelRes(self, REPData):
        self.saveMontageChannelResSig.emit(list(REPData[3]))

    # 病人管理功能
    # 向服务器发送获取病人信息请求

    def getPatientInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["patientManager", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getPatientInfoRes(self, REPData):
        self.getPatientInfoResSig.emit(list(REPData[3]))

        # 向服务器发送添加病人信息请求

    def addPatientInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["patientManager", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def addPatientInfoRes(self, REPData):
        self.addPatientInfoResSig.emit(list(REPData[3]))

        # 向服务器发送删除病人信息请求

    def delPatientInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["patientManager", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def delPatientInfoRes(self, REPData):
        self.delPatientInfoResSig.emit(list(REPData[3]))

        # 向服务器发送编辑病人信息请求

    def updatePatientInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["patientManager", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def updatePatientInfoRes(self, REPData):
        self.updatePatientInfoResSig.emit(list(REPData[3]))

    # 向服务器发送病人查询请求
    def inqPatientInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["patientManager", 5, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def inqPatientInfoRes(self, REPData):
        self.inqPatientInfoResSig.emit(list(REPData[3]))

    def patientPaging(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["patientManager", 6, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def patientPagingRes(self, REPData):
        self.patientPagingResSig.emit(list(REPData[3]))


    # 样本统计模块
    # 样本统计
    def getSpecificInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["sampleState", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getSpecificInfoRes(self, REPData):
        self.getSpecificInfoResSig.emit(list(REPData[3][3]))

    # 获取样本统计中各个类型的数量
    def getSpecificNum(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["sampleState", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getSpecificNumRes(self, REPData):
        self.getSpecificNumResSig.emit(list(REPData[3][3]))


    # 获取样本详细信息
    def getSpecificDetail(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["sampleState", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getSpecificDetailRes(self, REPData):
        self.getSpecificDetailResSig.emit(dict(REPData[3][3]))

    # 根据过滤信息获取数量
    def getSpecNumFromFlt(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["sampleState", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getSpecNumFromFltRes(self, REPData):
        self.getSpecNumFromFltResSig.emit(list(REPData[3][3]))


    # 构建集合
    # 获取构建数据集初始化所需要的数据
    def getSetInitData(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["setBuild", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getSetInitDataRes(self, REPData):
        self.getSetInitDataResSig.emit(list(REPData[3][3]))

    def delSet(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["setBuild", 6, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def delSetRes(self, REPData):
        self.delSetResSig.emit([REPData[3][0], REPData[3][3]])

    # 根据过滤器获取信息
    def getSetBuildFltData(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["setBuild", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getSetBuildFltDataRes(self, REPData):
        self.getSetBuildFltDataResSig.emit([REPData[3][0], REPData[3][3]])

    # 获取数据导出初始信息
    def getSetExportInitData(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["setBuild", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getSetExportInitDataRes(self, REPData):
        self.getSetExportInitDataResSig.emit(list(REPData[3][3]))

    # 根据block id来获取集合数据
    def getSetExportData(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["setBuild", 5, self.tUser[0], REQmsg]
        print(msg)
        self.sendRequest(msg)

    def getSetExportDataRes(self, REPData):
        self.getSetExportDataResSig.emit(list(REPData[3][3]))

    # 根据传入的信息来构建集合
    def buildSet(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["setBuild", 7, self.tUser[0], REQmsg]
        print(msg)
        self.sendRequest(msg)

    def buildSetRes(self, REPData):
        self.buildSetSig.emit(list(REPData[3][3]))

    # 向服务器获取当前构建的进度
    def buildSetGetPg(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["setBuild", 8, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def buildSetGetPgRes(self, REPData):
        self.buildSetGetPgSig.emit(list(REPData[3]))

    # 取消构建数据集
    def buildSetCancel(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["setBuild", 9, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def buildSetCancelRes(self, REPData):
        self.buildSetCancelSig.emit(list(REPData[3][3]))

    # 获取构建的数据集数据
    def getSet(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["setBuild", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getSetRes(self, REPData):
        self.getSetSig.emit([REPData[3][0], REPData[3][3]])

    # 获取搜索的数据集信息
    def getSetSearch(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["setBuild", 10, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getSetSearchRes(self, REPData):
        self.getSetSearchSig.emit([REPData[3][0], REPData[3][3]])

    def getSetDescribe(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["setBuild", 11, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getSetDescribeRes(self, REPData):
        self.getSetDescribeSig.emit([REPData[3][0], REPData[3][3]])


    # 标注类型模块
    # 查询标注类型模块方法
    def getTypeInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["labelType", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的查询标注类型的结果
    def getTypeInfoRes(self,REPData):
        print(REPData[3])
        self.getTypeInfoResSig.emit(list(REPData[3]))

    # 添加标注类型信息
    def addTypeInfo(self,REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["labelType", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的添加标注类型信息
    def addTypeInfoRes(self, REPData):
        self.addTypeInfoResSig.emit(REPData[3])

    # 删除标注类型信息
    def delTypeInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["labelType", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的删除标注类型信息
    def delTypeInfoRes(self, REPData):
        self.delTypeInfoResSig.emit(REPData[3])

    # 修改标注类型信息
    def updateTypeInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["labelType", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的修改标注类型信息
    def updateTypeInfoRes(self, REPData):
        print(REPData[3])
        self.updateTypeInfoResSig.emit(list(REPData[3]))
        # self.updateTypeInfoResSig.emit(list(REPData[3]))

    # 向服务器发送获取医生信息
    def getDoctorInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createCons", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务端传回的医生信息
    def getDoctorInfoRes(self, REPmsg):
        self.getDoctorInfoResSig.emit(list(REPmsg[3][2]))

    # 向服务器发送获取搜索医生的信息
    def getSearchDoctorInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createCons", 8, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务端传回的医生信息
    def getSearchDoctorInfoRes(self, REPmsg):
        self.getSearchDoctorInfoSig.emit(list(REPmsg[3][2]))


    # 向服务器发送获取完整脑电检查信息
    def getCpltCheckInfo(self):
        msg = ["createCons", 2, self.tUser[0], [self.macAddr]]
        self.sendRequest(msg)

    # 回调，处理服务端传回的完整脑电检查信息
    def getCpltCheckInfoRes(self, REPmsg):
        self.getCpltCheckInfoResSig.emit(list(REPmsg[3][2]))

    # 向服务器发送获取历史会诊信息
    def getHistoryCons(self):
        msg = ["createCons", 3, self.tUser[0], [self.macAddr]]
        self.sendRequest(msg)

    # 回调，处理服务端传回的历史会诊信息
    def getHistoryConsRes(self, REPmsg):
        self.getHistoryConsResSig.emit(list(REPmsg[3][2]))


    # 向服务器发送获取全部会诊的信息
    def getAllConsInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createCons", 6, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务端传回的历全部会诊信息
    def getAllConsInfoRes(self, REPmsg):
        self.getAllConsInfoSig.emit(list(REPmsg[3][2]))


    # 向服务器发送获取搜索的信息
    def inqConsInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createCons", 7, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务端传回的搜索的信息
    def inqConsInfoRes(self, REPmsg):
        self.inqConsInfoSig.emit(list(REPmsg[3][2]))

    # 创建课堂
    # 向服务器发送获取课堂信息请求
    def getLessonInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取课堂信息的结果
    def getLessonInfoRes(self, REPData):
        self.getLessonInfoResSig.emit(list(REPData[3]))

    # 向服务器发送获取诊断脑电文件ID请求
    def getDiagCheckID(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取诊断脑电文件ID的结果
    def getDiagCheckIDRes(self, REPData):
        self.getDiagCheckIDResSig.emit(list(REPData[3]))

    # 向服务器发送获取诊断脑电文件名称请求
    def getFileName(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取诊断脑电文件名称的结果
    def getFileNameRes(self, REPData):
        self.getFileNameResSig.emit(list(REPData[3]))

    # 向服务器发送添加课堂信息请求
    def addLesson(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器添加课堂信息的结果
    def addLessonRes(self, REPData):
        self.addLessonResSig.emit(list(REPData[3]))

    # 向服务器发送删除课堂信息请求
    def delLesson(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 5, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器删除课堂信息的结果
    def delLessonRes(self, REPData):
        self.delLessonResSig.emit(list(REPData[3]))

    # 向服务器发送更新课堂信息请求
    def updateLesson(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 6, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器更新课堂信息的结果
    def updateLessonRes(self, REPData):
        self.updateLessonResSig.emit(list(REPData[3]))

    # 向服务器发送获取课堂学员信息请求
    def getStudentInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 7, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取学员课堂信息的结果
    def getStudentInfoRes(self, REPData):
        self.getStudentInfoResSig.emit(list(REPData[3]))

    # 向服务器发送获更新课堂学员信息请求
    def updateStudentInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 8, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器更新课堂学员信息的结果
    def updateStudentInfoRes(self, REPData):
        self.updateStudentInfoResSig.emit(list(REPData[3]))

    # 向服务器发送获获取课堂内容信息请求
    def getContentInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 9, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取课堂内容信息的结果
    def getContentInfoRes(self, REPData):
        self.getContentInfoResSig.emit(list(REPData[3]))

    # 向服务器发送查询课堂信息请求
    def inquiryLessonInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 13, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器查询课堂信息的结果
    def inquiryLessonInfoRes(self, REPData):
        self.inquiryLessonInfoResSig.emit(list(REPData[3]))

    # 向服务器发送获取文件标准用户ID信息的请求
    def getCheckUserID(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 14, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取学员课堂信息的结果
    def getCheckUserIDRes(self, REPData):
        self.getCheckUserIDResSig.emit(list(REPData[3]))

    # 向服务器发送获取文件标准用户ID信息的请求
    def addStudent(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 16, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取学员课堂信息的结果
    def addStudentRes(self, REPData):
        self.addStudentResSig.emit(list(REPData[3]))

    def getlessonStudent(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 17, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取学员课堂信息的结果
    def getlessonStudentRes(self, REPData):
        self.getlessonStudentResSig.emit(list(REPData[3]))

    def delStudent(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 18, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取学员课堂信息的结果
    def delStudentRes(self, REPData):
        self.delStudentResSig.emit(list(REPData[3]))

    def addLessonContent(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 19, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取学员课堂信息的结果
    def addLessonContentRes(self, REPData):
        self.addLessonContentResSig.emit(list(REPData[3]))

    def delLessonContent(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 20, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取学员课堂信息的结果
    def delLessonContentRes(self, REPData):
        self.delLessonContentResSig.emit(list(REPData[3]))

    def studentPaging(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 21, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取学员课堂信息的结果

    def studentPagingRes(self, REPData):
        self.studentPagingResSig.emit(list(REPData[3]))

    def searchStudentPageInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 22, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def searchStudentPageInfoRes(self, REPData):
        self.searchStudentPageInfoResSig.emit(list(REPData[3]))

    def eggPaging(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 23, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def eggPagingRes(self, REPData):
        self.eggPagingResSig.emit(list(REPData[3]))

    def searchEegPageInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["createLesson", 24, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def searchEegPageInfoRes(self, REPData):
        self.searchEegPageInfoResSig.emit(list(REPData[3]))

    # 脑电导入模块
    # 查询病人诊断信息方法

    def getPatientCheckInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["dataImport", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的查询病人诊断信息的结果
    def getPatientCheckInfoRes(self, REPData):
        print(REPData[3])
        self.getPatientCheckInfoResSig.emit(list(REPData[3]))

    # 删除病人诊断信息
    def delPatientCheckInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["dataImport", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的删除标注类型信息
    def delPatientCheckInfoRes(self, REPData):
        self.delPatientCheckInfoResSig.emit(REPData[3])

    # 添加脑电检查信息
    def addCheckInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["dataImport", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的添添加脑电检查信息
    def addCheckInfoRes(self, REPData):
        self.addCheckInfoResSig.emit(REPData[3])

    # 检查配置
    def checkConfig(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["dataImport", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的检查配置信息
    def checkConfigRes(self, REPData):
        self.checkConfigResSig.emit(REPData[3])

    # 生成文件名
    def makeFileName(self,REQmsg):
        REQmsg.insert(0,self.macAddr)
        msg = ["dataImport", 10, self.tUser[0], REQmsg]
        print("生成文件名传过去的msg:",msg)
        self.sendRequest(msg)

    # 处理返回的生成文件名信息
    def makeFileNameRes(self,REPData):
        self.makeFileNameResSig.emit(REPData[3])


    # 写脑电数据请求
    def writeEEG(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["dataImport", 5, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的写脑电
    def writeEEGRes(self, REPData):
        self.writeEEGResSig.emit(REPData[3])

    # 更新脑电检查表
    def updateCheckInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["dataImport", 6, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 更新脑电检查表返回
    def updateCheckInfoRes(self, REPData):
        self.updateCheckInfoResSig.emit(REPData[3])

    # 查询脑电文件方法
    def getFileInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["dataImport", 7, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的查询脑电文件的结果
    def getFileInfoRes(self, REPData):
        print(REPData[3])
        self.getFileInfoResSig.emit(list(REPData[3]))

    # 删除脑电文件方法
    def delFileInfo(self,REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["dataImport", 11, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的删除脑电文件的结果
    def delFileInfoRes(self,REPData):
        print(REPData[3])
        self.delFileInfoResSig.emit(list(REPData[3]))


    # 查询选择的病人方法
    def getChoosePatientInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["dataImport", 8, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的查询选择的病人的结果
    def getChoosePatientInfoRes(self, REPData):
        print(REPData[3])
        self.getChoosePatientInfoResSig.emit(list(REPData[3]))

    # 查询选择的医生方法
    def getChooseDoctorInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["dataImport", 9, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的查询选择的医生的结果
    def getChooseDoctorInfoRes(self, REPData):
        print(REPData[3])
        self.getChooseDoctorInfoResSig.emit(list(REPData[3]))

    # 任务设置模块
    # 查询标注主题方法
    def getThemeInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["taskSettings", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的查查询标注主题信息的结果
    def getThemeInfoRes(self, REPData):
        print(REPData[3])
        self.getThemeInfoResSig.emit(list(REPData[3]))

    # 添加标注主题方法
    def addThemeInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["taskSettings", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的添加标注主题信息的结果
    def addThemeInfoRes(self, REPData):
        print(REPData[3])
        self.addThemeInfoResSig.emit(list(REPData[3]))

    # 删除标注主题方法
    def delThemeInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["taskSettings", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的删除标注主题信息的结果
    def delThemeInfoRes(self, REPData):
        print(REPData[3])
        self.delThemeInfoResSig.emit(list(REPData[3]))

    # 更新标注主题方法
    def updateThemeInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["taskSettings", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的更新标注主题信息的结果
    def updateThemeInfoRes(self, REPData):
        print(REPData[3])
        self.updateThemeInfoResSig.emit(list(REPData[3]))

    # 查询标注任务方法
    def getTaskInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["taskSettings", 5, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的查查询标注任务信息的结果
    def getTaskInfoRes(self, REPData):
        print(REPData[3])
        self.getTaskInfoResSig.emit(list(REPData[3]))

    # 添加标注任务方法
    def addTaskInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["taskSettings", 6, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的添加标注任务信息的结果
    def addTaskInfoRes(self, REPData):
        print(REPData[3])
        self.addTaskInfoResSig.emit(list(REPData[3]))

    # 删除标注任务方法
    def delTaskInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["taskSettings", 7, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的删除标注任务信息的结果
    def delTaskInfoRes(self, REPData):
        print(REPData[3])
        self.delTaskInfoResSig.emit(list(REPData[3]))

    # 更新标注任务方法
    def updateTaskInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["taskSettings", 8, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的更新标注任务信息的结果
    def updateTaskInfoRes(self, REPData):
        print(REPData[3])
        self.updateTaskInfoResSig.emit(list(REPData[3]))

    # 获取(添加主题详细信息)筛选框信息
    def getChooseDetailInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["taskSettings", 9, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的获取筛选框信息结果
    def getChooseDetailInfoRes(self, REPData):
        print(REPData[3])
        self.getChooseDetailInfoResSig.emit(list(REPData[3]))

    # 启动标注主题
    def startTheme(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["taskSettings", 10, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的启动标注主题信息结果
    def startThemeRes(self, REPData):
        print(REPData[3])
        self.startThemeResSig.emit(list(REPData[3]))

    # 查找标注人员信息
    def getChooseMarkerInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["taskSettings", 11, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的查找标注人员信息信息结果
    def getChooseMarkerInfoRes(self, REPData):
        print(REPData[3])
        self.getChooseMarkerInfoResSig.emit(list(REPData[3]))


    # 执行查看模块
    # 查询某一用户创建的标注主题方法
    # def getUserThemeInfo(self, REQmsg):
    #     REQmsg.insert(0, self.macAddr)
    #     msg = ["detailLook", 1, self.tUser[0], REQmsg]
    #     self.sendRequest(msg)
    #
    # # 处理客户端返回的查查询某一用户创建的标注主题信息的结果
    # def getUserThemeInfoRes(self, REPData):
    #     print(REPData[3])
    #     self.getUserThemeInfoResSig.emit(list(REPData[3]))
    #
    # # 修改某一用户创建的标注主题状态
    # def updateUserThemeInfo(self, REQmsg):
    #     REQmsg.insert(0, self.macAddr)
    #     msg = ["detailLook", 2, self.tUser[0], REQmsg]
    #     self.sendRequest(msg)
    #
    # # 处理客户端返回的修改某一用户创建的标注主题状态的结果
    # def updateUserThemeInfoRes(self, REPData):
    #     print(REPData[3])
    #     self.updateUserThemeInfoResSig.emit(list(REPData[3]))
    #
    # # 修改某一的标注主题的标注任务的状态
    # def updateUserTaskInfo(self, REQmsg):
    #     REQmsg.insert(0, self.macAddr)
    #     msg = ["detailLook", 3, self.tUser[0], REQmsg]
    #     self.sendRequest(msg)
    #
    # # 处理客户端返回的修改某一标注主题的标注任务的状态的结果
    # def updateUserTaskInfoRes(self, REPData):
    #     print(REPData[3])
    #     self.updateUserTaskInfoResSig.emit(list(REPData[3]))
    #
    # # 获取某一标注任务的某一标注用户对某一脑电文件的详细标注信息
    # def getDetailInfo(self, REQmsg):
    #     REQmsg.insert(0, self.macAddr)
    #     msg = ["detailLook", 4, self.tUser[0], REQmsg]
    #     self.sendRequest(msg)
    #
    # # 处理客户端返回的获取某一标注任务的某一标注用户对某一脑电文件的详细标注信息的结果
    # def getDetailInfoRes(self, REPData):
    #     print(REPData[3])
    #     self.getDetailInfoResSig.emit(list(REPData[3]))
    #
    # # 删除某一标注任务的某一标注用户对某一脑电文件的详细标注信息
    # def delDetailInfo(self, REQmsg):
    #     REQmsg.insert(0, self.macAddr)
    #     msg = ["detailLook", 5, self.tUser[0], REQmsg]
    #     self.sendRequest(msg)
    #
    # # 处理客户端返回的获删除某一标注任务的某一标注用户对某一脑电文件的详细标注信息的结果
    # def delDetailInfoRes(self, REPData):
    #     print(REPData[3])
    #     self.delDetailInfoResSig.emit(list(REPData[3]))
    #
    # # 删除某一标注任务的某一标注用户对某一脑电文件的所有详细标注信息
    # def delDetailAll(self, REQmsg):
    #     REQmsg.insert(0, self.macAddr)
    #     msg = ["detailLook", 6, self.tUser[0], REQmsg]
    #     self.sendRequest(msg)
    #
    # # 处理客户端返回的获删除某一标注任务的某一标注用户对某一脑电文件的所有详细标注信息的结果
    # def delDetailAllRes(self, REPData):
    #     print(REPData[3])
    #     self.delDetailAllResSig.emit(list(REPData[3]))
    #
    # # 检查某一标注主题的所有标注任务状态
    # def checkTaskStateAll(self, REQmsg):
    #     REQmsg.insert(0, self.macAddr)
    #     msg = ["detailLook", 7, self.tUser[0], REQmsg]
    #     self.sendRequest(msg)
    #
    # # 处理客户返回的检查某一标注主题的标注任务结果
    # def checkTaskStateAllRes(self, REPData):
    #     print(REPData[3])
    #     self.checkTaskStateAllResSig.emit(list(REPData[3]))

    # 算法管理
    # 向服务器发送获取算法信息请求
    def getAlgorithmInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["algorithm", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取算法信息的结果
    def getAlgorithmInfoRes(self, REPData):
        self.getAlgorithmInfoResSig.emit(list(REPData[3]))

    # 向服务器发送添加算法信息请求
    def addAlgorithmInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["algorithm", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器添加算法信息的结果
    def addAlgorithmInfoRes(self, REPData):
        self.addAlgorithmInfoResSig.emit(list(REPData[3]))

    # 向服务器发送删除算法请求
    def delAlgorithmInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["algorithm", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器删除算法的结果
    def delAlgorithmInfoRes(self, REPData):
        self.delAlgorithmInfoResSig.emit(list(REPData[3]))

    # 向服务器发送查询算法信息请求
    def inquiryAlgorithmInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["algorithm", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器查询算法信息的结果
    def inquiryAlgorithmInfoRes(self, REPData):
        self.inquiryAlgorithmInfoResSig.emit(list(REPData[3]))

    # 向服务器发送添加算法文件请求
    def addAlgorithmFile(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["algorithm", 5, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器添加算法文件的结果
    def addAlgorithmFileRes(self, REPData):
        self.addAlgorithmFileResSig.emit(list(REPData[3]))

    # 向服务器发送获取算法文件名请求
    def getAlgorithmFileName(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["algorithm", 6, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取算法信息的结果
    def getAlgorithmFileNameRes(self, REPData):
        self.getAlgorithmFileNameResSig.emit(list(REPData[3]))

    def algorithmInfoPaging(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["algorithm", 7, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取算法信息的结果
    def algorithmInfoPagingRes(self, REPData):
        self.algorithmInfoPagingResSig.emit(list(REPData[3]))

    # 模型训练
    # 向服务器发送获取模型训练界面信息请求
    def getModelInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["modelTrain", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取模型训练界面信息的结果
    def getModelInfoRes(self, REPData):
        self.getModelInfoResSig.emit(list(REPData[3]))

    # 向服务器发送获取模型训练界面信息请求
    def get_classifierInfo_by_setId_and_algId(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["modelTrain", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取算法信息的结果
    def get_classifierInfo_by_setId_and_algIdRes(self, REPData):
        self.get_classifierInfo_by_setId_and_algIdResSig.emit(list(REPData[3]))

    # 向服务器发送获取模型训练界面信息请求
    def runProcessForTrain(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["modelTrain", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取算法信息的结果
    def runProcessForTrainRes(self, REPData):
        self.runProcessForTrainResSig.emit(list(REPData[3]))

    # 向服务器发送获取模型训练算法界面分页信息请求
    def modelAlgInfoPaging(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["modelTrain", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取模型训练算法界面分页信息的结果
    def modelAlgInfoPagingRes(self, REPData):
        self.modelAlgInfoPagingResSig.emit(list(REPData[3]))

    # 向服务器发送获取模型训练算法界面分页信息请求

    def modelInquiryAlgInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["modelTrain", 5, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取模型训练算法界面分页信息的结果

    def modelInquiryAlgInfoRes(self, REPData):
        self.modelInquiryAlgInfoResSig.emit(list(REPData[3]))

    # 向服务器发送获取模型训练算法界面分页信息请求
    def modelSetInfoPaging(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["modelTrain", 6, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取模型训练算法界面分页信息的结果
    def modelSetInfoPagingRes(self, REPData):
        self.modelSetInfoPagingResSig.emit(list(REPData[3]))

    # 向服务器发送获取模型训练算法界面分页信息请求
    def modelInquirySetInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["modelTrain", 7, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取模型训练算法界面分页信息的结果
    def modelInquirySetInfoRes(self, REPData):
        self.modelInquirySetInfoResSig.emit(list(REPData[3]))

    # 向服务器发送获取模型训练算法界面分页信息请求

    def matchAlgSet(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["modelTrain", 8, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取模型训练算法界面分页信息的结果

    def matchAlgSetRes(self, REPData):
        self.matchAlgSetResSig.emit(list(REPData[3]))

    def getTrainPerformance(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["modelTrain", 9, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取模型训练算法界面分页信息的结果

    def getTrainPerformanceRes(self, REPData):
        self.getTrainPerformanceResSig.emit(list(REPData[3]))

    def getProgress(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["modelTrain", 10, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取模型训练算法界面分页信息的结果

    def getProgressRes(self, REPData):
        self.getProgressResSig.emit(list(REPData[3]))

    def train_cancel(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["modelTrain", 11, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取模型训练算法界面分页信息的结果

    def train_cancelRes(self, REPData):
        self.train_cancelResSig.emit(list(REPData[3]))

    # 模型测试
    # 向服务器发送获取模型测试界面信息请求
    def getClassifierInfo(self, pageSize, page, classifier_name):
        msg = ['modelTest', 1, self.tUser[0], [self.macAddr, pageSize, page, classifier_name]]
        self.sendRequest(msg)

    def getClassifierInfoRes(self, REPData):
        self.classifierInfoResSig.emit(list(REPData))

    def runProcessForTest(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["modelTest", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def runProcessForTestRes(self, REPData):
        self.runProcessForTestResSig.emit(list(REPData[3]))

    def getResult(self):
        msg = ["modelTest", 3, self.tUser[0], [self.macAddr]]
        self.sendRequest(msg)

    def getResultRes(self, REPData):
        self.getResultResSig.emit(list(REPData[3]))

    # 模型管理
    # 向服务器发送获取模型信息请求
    def getClassifierAlgSetName(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["classifier", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

        # 回调,处理服务器获取模型训练界面信息的结果

    def getClassifierAlgSetNameRes(self, REPData):
        self.getClassifierAlgSetNameResSig.emit(list(REPData[3]))

    def inquiryClassifierInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["classifier", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

        # 回调,处理服务器获取模型训练界面信息的结果

    def inquiryClassifierInfoRes(self, REPData):
        self.inquiryClassifierInfoResSig.emit(list(REPData[3]))

    def delClassifierInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["classifier", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

        # 回调,处理服务器获取模型训练界面信息的结果

    def delClassifierInfoRes(self, REPData):
        self.delClassifierInfoResSig.emit(list(REPData[3]))

    def getSelectAlgorithmInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["classifier", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

        # 回调,处理服务器获取模型训练界面信息的结果

    def getSelectAlgorithmInfoRes(self, REPData):
        self.getSelectAlgorithmInfoResSig.emit(list(REPData[3]))

    def checkClassifierInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["classifier", 5, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def checkClassfierInfoRes(self, REPData):
        self.checkClassifierInfoRessig.emit(list(REPData[3]))

    def cls_restate(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["classifier", 6, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def cls_restateRes(self, REPData):
        self.cls_restateRessig.emit(list(REPData[3]))

    def checkstate(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["classifier", 7, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def checkstateRes(self, REPData):
        self.checkstateRessig.emit(list(REPData[3]))

    def model_transmit_message(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        REQmsg.append(self.macAddr)
        msg = ["classifier", 8, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def model_transmit_messageRes(self, REPData):
        self.model_transmit_messageRessig.emit(list(REPData[3]))

    def classifier_id_inquiry(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        REQmsg.append(self.macAddr)
        msg = ["classifier", 9, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def classifier_id_inquiryRes(self, REPData):
        self.classifier_id_inquiryRessig.emit(list(REPData[3]))

    def classifierPaging(self,REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["classifier", 10, self.tUser[0], REQmsg]
        self.sendRequest(msg)
    def classifierPaingRes(self,REPData):
        self.classifierPagingResSig.emit(list(REPData[3]))
    def classifierPaging_al(self,REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["classifier", 11, self.tUser[0], REQmsg]
        self.sendRequest(msg)
    def classifierPaging_alRes(self,REPData):
        self.classifierPaging_alResSig.emit(list(REPData[3]))
    def inquiryCls_alg_Info(self,REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["classifier", 12, self.tUser[0], REQmsg]
        self.sendRequest(msg)
    def inquiryCls_alg_InfoRes(self,REPData):
        self.inquiryCls_alg_InfoRessig.emit(list(REPData[3]))
    def getClassifier_config(self):
        msg = ["classifier", 13, self.tUser[0], [self.macAddr]]
        self.sendRequest(msg)
    def getClassifier_configRes(self,REPData):
        self.getClassifier_configRessig.emit(list(REPData[3][3]))
    def getSelectSetInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["classifier", 14, self.tUser[0], REQmsg]
        self.sendRequest(msg)
    def getSelectSetInfoRes(self, REPData):
        self.getSelectSetInfoResSig.emit(list(REPData[3]))
    def inquiryCls_set_Info(self,REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["classifier", 15, self.tUser[0], REQmsg]
        self.sendRequest(msg)
    def inquiryCls_set_InfoRes(self, REPData):
        self.inquiryCls_set_InfoResSig.emit(list(REPData[3]))
    def classifierPaging_set(self,REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["classifier", 16, self.tUser[0], REQmsg]
        self.sendRequest(msg)
    def classifierPaging_setRes(self,REPData):
        self.classifierPaging_setResSig.emit(list(REPData[3]))

    def upload_scheme(self,REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["classifier", 17, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def upload_schemeRes(self,REPData):
        self.upload_schemeResSig.emit(list(REPData[3]))
    # 脑电扫描
    # 向服务器发送获取脑电扫描界面信息请求
    def upload_model(self,REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["classifier", 18, self.tUser[0], REQmsg]
        self.sendRequest(msg)
    def upload_modelRes(self,REPData):
        self.upload_modelResSig.emit(list(REPData[3]))

    def getAutoInitData(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["auto", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getAutoInitDataRes(self, REPData):
        self.getAutoInitDataResSig.emit(list(REPData[3]))

    def getPatientMeasureDay(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["auto", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getPatientMeasureDayRes(self, REPData):
        self.getPatientMeasureDayResSig.emit(list(REPData[3]))

    def getPatientFile(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["auto", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getPatientFileRes(self, REPData):
        self.getPatientFileResSig.emit(list(REPData[3]))

    def getFileChannels(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["auto", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getFileChannelsRes(self, REPData):
        self.getFileChannelsResSig.emit(list(REPData[3]))

    def autoClassifierInfoPaging(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["auto", 5, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取模型训练算法界面分页信息的结果
    def autoClassifierInfoPagingRes(self, REPData):
        self.autoClassifierInfoPagingResSig.emit(list(REPData[3]))

    def autoInquiryClassifierInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["auto", 6, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取模型训练算法界面分页信息的结果
    def autoInquiryClassifierInfoRes(self, REPData):
        self.autoInquiryClassifierInfoResSig.emit(list(REPData[3]))

    def runProcessForScan(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["auto", 7, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取模型训练算法界面分页信息的结果

    def runProcessForScanRes(self, REPData):
        self.runProcessForScanResSig.emit(list(REPData[3]))

    def matchClassifierFile(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["auto", 8, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取模型训练算法界面分页信息的结果

    def matchClassifierFileRes(self, REPData):
        self.matchClassifierFileResSig.emit(list(REPData[3]))

    def getScanProgress(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["auto", 9, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取模型训练算法界面分页信息的结果

    def getScanProgressRes(self, REPData):
        self.getScanProgressResSig.emit(list(REPData[3]))

    # 评估标注
    def getAssessInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["assessLabel", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getAssessInfoRes(self, REPData):
        self.getAssessInfoResSig.emit(list(REPData[3]))

    def getModelIdName(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["assessLabel", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getModelIdNameRes(self, REPData):
        self.getModelIdNameResSig.emit(list(REPData[3]))

    def assessClassifierInfoPaging(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["assessLabel", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def assessClassifierInfoPagingRes(self, REPData):
        self.assessClassifierInfoPagingResSig.emit(list(REPData[3]))

    def getAssessFileInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["assessLabel", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getAssessFileInfoRes(self, REPData):
        self.getAssessFileInfoResSig.emit(list(REPData[3]))

    def assessOpenEEGFile(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["assessLabel", 8, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def assessOpenEEGFileRes(self, REPData):
        self.assessOpenEEGFileResSig.emit(list(REPData[3]))

    def assess_load_dataDynamical(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["assessLabel", 9, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def assess_load_dataDynamicalRes(self, REPData):
        self.assess_load_dataDynamicalResSig.emit(list(REPData[3]))

    def as_load_dataDynamical10(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["assessLabel", 10, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def as_load_dataDynamicalRes10(self, REPData):
        self.assess_load_dataDynamicalResSig.emit(list(REPData[3]))

    def update_labelListInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["assessLabel", 11, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def update_labelListInfoRes(self, REPData):
        self.update_labelListInfoResSig.emit(list(REPData[3]))

    def update_labelListInfo12(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["assessLabel", 12, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def update_labelListInfo12Res(self, REPData):
        self.update_labelListInfo12ResSig.emit(list(REPData[3]))

    def update_state_labelListInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["assessLabel", 13, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def update_state_labelListInfoRes(self, REPData):
        self.update_state_labelListInfoResSig.emit(list(REPData[3]))

    def del_labelListInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["assessLabel", 14, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def del_labelListInfoRes(self, REPData):
        self.del_labelListInfoResSig.emit(list(REPData[3]))

    def del_labelListInfo15(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["assessLabel", 15, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def del_labelListInfo15Res(self, REPData):
        self.del_labelListInfo15ResSig.emit(list(REPData[3]))

    def del_labelListInfo16(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["assessLabel", 16, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def del_labelListInfo16Res(self, REPData):
        self.del_labelListInfo16ResSig.emit(list(REPData[3]))

    # 清理标注
    def getClearLabelInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["clearLabel", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getClearLabelInfoRes(self, REPData):
        self.getClearLabelInfoResSig.emit(list(REPData[3]))

    def inquiryScanClassifierInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["clearLabel", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def inquiryScanClassifierInfoRes(self, REPData):
        self.inquiryScanClassifierInfoResSig.emit(list(REPData[3]))

    def scanClassifierInfoPaging(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["clearLabel", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def scanClassifierInfoPagingRes(self, REPData):
        self.scanClassifierInfoPagingResSig.emit(list(REPData[3]))

    def getScanInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["clearLabel", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getScanInfoRes(self, REPData):
        self.getScanInfoResSig.emit(list(REPData[3]))

    def getCurClearLabelInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["clearLabel", 5, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getCurClearLabelInfoRes(self, REPData):
        self.getCurClearLabelInfoResSig.emit(list(REPData[3]))

    def getScanFileInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["clearLabel", 6, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getScanFileInfoRes(self, REPData):
        self.getScanFileInfoResSig.emit(list(REPData[3]))

    def delLabelListInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["clearLabel", 7, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def delLabelListInfoRes(self, REPData):
        self.delLabelListInfoResSig.emit(list(REPData[3]))

    def delLabelByModelFile(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["clearLabel", 8, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def delLabelByModelFileRes(self, REPData):
        self.delLabelByModelFileResSig.emit(list(REPData[3]))

    def getLabelInfoByAssess(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["clearLabel", 9, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getLabelInfoByAssessRes(self, REPData):
        self.getLabelInfoByAssessResSig.emit(list(REPData[3]))

    def getSearchScanFileInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["clearLabel", 10, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    def getSearchScanFileInfoRes(self, REPData):
        self.getSearchScanFileInfoResSig.emit(list(REPData[3]))

    def sendRequest(self, msg):
        # r = self.sockOpenConn(self.s_ip, self.s_port)
        # if r is None:
        #     msg[3] = ['0','','网络忙.']
        #     self.appMain('', msg)
        #     return
        ret = self.send_client_data(msg)
        if ret:
            return True
        else:
            self.sockClose()
            self.serverExceptSig.emit()
            return False


    def appMain(self, serverAddr, REQmsg):
        # 退出
        if REQmsg[0] == 'quit' and REQmsg[1] == 1:
            self.quitRes(REQmsg)
        # 登出
        elif REQmsg[0] == 'logout' and REQmsg[1] == 1:
            self.logoutRes(REQmsg)
        # 登录
        elif REQmsg[0] == 'login' and REQmsg[1] == 1:
            self.loginRes(REQmsg)

        # 密码修改
        elif REQmsg[0] == 'pwd' and REQmsg[1] == 1:
            self.pwdRes(REQmsg)

        # 获取用户信息
        elif REQmsg[0] == 'userManager' and REQmsg[1] == 1:
            self.getUserInfoRes(REQmsg)

        # 新增用户信息
        elif REQmsg[0] == 'userManager' and REQmsg[1] == 2:
            self.addUserInfoRes(REQmsg)

        # 删除用户信息
        elif REQmsg[0] == 'userManager' and REQmsg[1] == 3:
            self.delUserInfoRes(REQmsg)

        # 编辑用户信息
        elif REQmsg[0] == 'userManager' and REQmsg[1] == 4:
            self.updateUserInfoRes(REQmsg)

        # 编辑用户信息
        elif REQmsg[0] == 'userManager' and REQmsg[1] == 5:
            self.userPagingRes(REQmsg)

        elif REQmsg[0] == 'userManager' and REQmsg[1] == 6:
            self.inquiryUserInfoRes(REQmsg)


        # 获取导联配置信息
        elif REQmsg[0] == 'montage' and REQmsg[1] == 1:
            self.getMontageRes(REQmsg)

        # 添加导联方案
        elif REQmsg[0] == 'montage' and REQmsg[1] == 2:
            self.addMontageSchemeRes(REQmsg)

        # 编辑导联方案
        elif REQmsg[0] == 'montage' and REQmsg[1] == 3:
            self.editMontageSchemeRes(REQmsg)

        # 删除导联方案
        elif REQmsg[0] == 'montage' and REQmsg[1] == 4:
            self.delMontageSchemeRes(REQmsg)

        # 保存导联方案通道
        elif REQmsg[0] == 'montage' and REQmsg[1] == 5:
            self.saveMontageChannelRes(REQmsg)


        # 标注类型模块
        # 回调获取标注类型信息
        elif REQmsg[0] == 'labelType' and REQmsg[1] == 1:
            self.getTypeInfoRes(REQmsg)

        # 回调增加标注类型信息
        elif REQmsg[0] == 'labelType' and REQmsg[1] == 2:
            self.addTypeInfoRes(REQmsg)

        # 回调删除标注类型信息
        elif REQmsg[0] == 'labelType' and REQmsg[1] == 3:
            self.delTypeInfoRes(REQmsg)

        # 回调修改标注类型信息
        elif REQmsg[0] == 'labelType' and REQmsg[1] == 4:
            self.updateTypeInfoRes(REQmsg)

        # 基本设置

        elif REQmsg[0] == 'basicConfig' and REQmsg[1] == 1:
            self.getConfigRes(REQmsg)

        elif REQmsg[0] == 'basicConfig' and REQmsg[1] == 2:
            self.addBasicConfigRes(REQmsg)

        elif REQmsg[0] == 'basicConfig' and REQmsg[1] == 3:
            self.delBasicConfigRes(REQmsg)

        elif REQmsg[0] == 'basicConfig' and REQmsg[1] == 4:
            self.updateBasicConfigRes(REQmsg)


        # 配置选择
        elif REQmsg[0] == 'configOptions' and REQmsg[1] == 1:
            self.getCurConfigDataRes(REQmsg)
        elif REQmsg[0] == 'configOptions' and REQmsg[1] == 2:
            self.getAllConfigDataRes(REQmsg)
        elif REQmsg[0] == 'configOptions' and REQmsg[1] == 3:
            self.chgCurUserConfigRes(REQmsg)
#### dsj ==[====

        # 学习评估/删除学员测试信息
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 27:
            self.da_get_ClassContentsRes(REQmsg)
        #学习评估/删除学员测试信息
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 26:
            self.da_get_diagRes(REQmsg)
        #学习评估/删除学员测试信息
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 25:
            self.da_del_studentsTestRes(REQmsg)
        #学习评估/删除班级及其学员测试信息
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 24:
            self.da_del_classRes(REQmsg)
        #学习评估/删除样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 23:
            self.da_del_sampleInfo_stateRes(REQmsg)
        #学习评估/修改样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 22:
            self.da_update_sampleInfo_stateRes(REQmsg)
        #学习评估/添加样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 21:
            self.da_add_sampleInfo_stateRes(REQmsg)
        #学习评估/删除样本信息(脑电图中的操作)
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 19:
            self.da_del_sample19Res(REQmsg)
        #学习评估/添加样本信息(脑电图中的操作)
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 17:
            self.da_insert_sample17Res(REQmsg)
        # 学习评估/(绘图设置)提取样本信息(绘图设置)
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 16:
            self.da_init_SampleListRes(REQmsg)
        #学习评估/修改样本(脑电图中的操作)
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 15:
            self.da_update_sampleInfo15Res(REQmsg)
        #学习评估/添加样本
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 14:
            self.da_add_sampleInfo14Res(REQmsg)
        #学习评估/删除样本(样本列表中的操作)
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 13:
            self.da_del_sampleInfo13Res(REQmsg)
        #学习评估/添加样本(样本列表中的操作)
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 12:
            self.da_update_sampleInfo12Res(REQmsg)
        #学习评估/添加样本
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 11:
            self.da_add_sampleInfo11Res(REQmsg)
        #学习评估/读取脑电文件数据块
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 10:
            self.da_load_dataDynamical10Res(REQmsg)
        #学习评估/读取脑电文件数据块
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 9:
            self.da_load_dataDynamicalRes(REQmsg)
        #学习评估/打开脑电文件
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 8:
            self.da_openEEGFileRes(REQmsg)
        # 学习评估/类型、用户信息
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 4:
            self.da_get_type_infoRes(REQmsg)
        # 学习评估/提取学习测试信息
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 2:
            self.da_get_ClassStudentRes(REQmsg)
        #学习评估/提取学习测试信息
        elif REQmsg[0] == 'testAssess' and REQmsg[1] == 1:
            self.da_get_contentsRes(REQmsg)

        #学习测试/完成诊断信息
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 28:
            self.dt_diagTest_commitRes(REQmsg)
        #学习测试/删除样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 23:
            self.dt_del_sampleInfo_stateRes(REQmsg)
        #学习测试/修改样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 22:
            self.dt_update_sampleInfo_stateRes(REQmsg)
        #学习测试/添加样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 21:
            self.dt_add_sampleInfo_stateRes(REQmsg)
        #学习测试/删除样本信息(脑电图中的操作)
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 19:
            self.dt_del_sample19Res(REQmsg)
        #学习测试/添加样本信息(脑电图中的操作)
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 17:
            self.dt_insert_sample17Res(REQmsg)
        # 学习测试/(绘图设置)提取样本信息(绘图设置)
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 16:
            self.dt_init_SampleListRes(REQmsg)
        #学习测试/修改样本(脑电图中的操作)
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 15:
            self.dt_update_sampleInfo15Res(REQmsg)
        #学习测试/添加样本
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 14:
            self.dt_add_sampleInfo14Res(REQmsg)
        #学习测试/删除样本(样本列表中的操作)
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 13:
            self.dt_del_sampleInfo13Res(REQmsg)
        #学习测试/添加样本(样本列表中的操作)
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 12:
            self.dt_update_sampleInfo12Res(REQmsg)
        #学习测试/添加样本
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 11:
            self.dt_add_sampleInfo11Res(REQmsg)
        #学习测试/读取脑电文件数据块
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 10:
            self.dt_load_dataDynamical10Res(REQmsg)
        #学习测试/读取脑电文件数据块
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 9:
            self.dt_load_dataDynamicalRes(REQmsg)
        #学习测试/打开脑电文件
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 8:
            self.dt_openEEGFileRes(REQmsg)
        # 学习测试/类型、用户信息
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 4:
            self.dt_get_type_infoRes(REQmsg)
        # 学习测试/提取学习测试信息
        elif REQmsg[0] == 'diagTest' and REQmsg[1] == 1:
            self.dt_get_contentsRes(REQmsg)

        # 诊断学习/提取诊断信息
        elif REQmsg[0] == 'diagTraining' and REQmsg[1] == 25:
            self.dl_get_diagRes(REQmsg)
        # 诊断学习/(绘图设置)提取样本信息(绘图设置)
        elif REQmsg[0] == 'diagTraining' and REQmsg[1] == 16:
            self.dl_init_SampleListRes(REQmsg)

        # 诊断学习/读取脑电文件数据块
        elif REQmsg[0] == 'diagTraining' and REQmsg[1] == 10:
            self.dl_load_dataDynamical10Res(REQmsg)

        elif REQmsg[0] == 'diagTraining' and REQmsg[1] == 9:
            self.dl_load_dataDynamicalRes(REQmsg)

        # 诊断学习/打开脑电文件
        elif REQmsg[0] == 'diagTraining' and REQmsg[1] == 8:
            self.dl_openEEGFileRes(REQmsg)

        # 诊断学习/类型、用户信息
        elif REQmsg[0] == 'diagTraining' and REQmsg[1] == 4:
            self.dl_get_type_infoRes(REQmsg)

        # 诊断学习/学习记录结束，更新结束时间，不返回
        elif REQmsg[0] == 'diagTraining' and REQmsg[1] == 3:
            pass

        # 诊断学习/提取学习信息
        elif REQmsg[0] == 'diagTraining' and REQmsg[1] == 2:
            self.dl_get_studyInfoRes(REQmsg)

        # 诊断学习/提取诊断信息
        elif REQmsg[0] == 'diagTraining' and REQmsg[1] == 1:
            self.dl_get_contentsRes(REQmsg)

        #脑电会诊/拒绝诊断信息
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 29:
            self.ct_diag_refusedRes(REQmsg)
        #脑电会诊/完成诊断信息
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 28:
            self.ct_diag_commitRes(REQmsg)
        #脑电会诊/填写诊断信息
        elif REQmsg[0] == 'consulting' and (REQmsg[1] == 26 or REQmsg[1] == 27):
            self.ct_diag_updateRes(REQmsg)
        #脑电会诊/提取诊断信息
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 25:
            self.ct_get_diagRes(REQmsg)
        #脑电会诊/提取诊断信息
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 24:
            self.ct_get_diags_notDiagRes(REQmsg)
        # 标注诊断/删除样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 23:
            self.ct_del_sampleInfo_stateRes(REQmsg)
        #脑电会诊/修改样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 22:
            self.ct_update_sampleInfo_stateRes(REQmsg)
        #脑电会诊/添加样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 21:
            self.ct_add_sampleInfo_stateRes(REQmsg)
        #脑电会诊/删除样本信息(脑电图中的操作)
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 19:
            self.ct_del_sample19Res(REQmsg)
        #脑电会诊/添加样本信息(脑电图中的操作)
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 17:
            self.ct_insert_sample17Res(REQmsg)
        # 标注诊断/(绘图设置)提取样本信息(绘图设置)
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 16:
            self.ct_init_SampleListRes(REQmsg)
        #脑电会诊/修改样本(脑电图中的操作)
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 15:
            self.ct_update_sampleInfo15Res(REQmsg)
        #脑电会诊/添加样本
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 14:
            self.ct_add_sampleInfo14Res(REQmsg)
        #脑电会诊/删除样本(样本列表中的操作)
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 13:
            self.ct_del_sampleInfo13Res(REQmsg)
        #脑电会诊/添加样本(样本列表中的操作)
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 12:
            self.ct_update_sampleInfo12Res(REQmsg)
        #脑电会诊/添加样本
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 11:
            self.ct_add_sampleInfo11Res(REQmsg)
        #脑电会诊/读取脑电文件数据块
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 10:
            self.ct_load_dataDynamical10Res(REQmsg)
        #脑电会诊/读取脑电文件数据块
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 9:
            self.ct_load_dataDynamicalRes(REQmsg)
        #脑电会诊/打开脑电文件
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 8:
            self.ct_openEEGFileRes(REQmsg)
        #脑电会诊/脑电文件
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 7:
            self.ct_get_fileNameByIdDateRes(REQmsg)
        #脑电会诊/检测日期
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 6:
            self.ct_get_measureDateByIdRes(REQmsg)
        # 脑电会诊/病人信息
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 5:
            self.ct_get_patientIdNameRes(REQmsg)
        # 脑电会诊/类型、用户信息
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 4:
            self.ct_get_type_infoRes(REQmsg)
        # 脑电会诊/提取诊断信息[首窗口]
        elif REQmsg[0] == 'consulting' and REQmsg[1] == 3:
            self.ct_main_get_diagRes(REQmsg)

        # 诊断查询/查询、分页
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 30:
            self.mq_pagingRes(REQmsg)

        # 诊断查询/提取诊断信息
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 25:
            self.mq_get_diagRes(REQmsg)
        # 标注诊断/(绘图设置)提取样本信息(绘图设置)
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 16:
            self.mq_init_SampleListRes(REQmsg)

        # 诊断查询/读取脑电文件数据块
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 10:
            self.mq_load_dataDynamical10Res(REQmsg)

        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 9:
            self.mq_load_dataDynamicalRes(REQmsg)

        # 诊断查询/打开脑电文件
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 8:
            self.mq_openEEGFileRes(REQmsg)

        # 诊断查询/脑电文件
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 7:
            self.mq_get_fileNameByIdDateRes(REQmsg)
        # 诊断查询/类型、用户信息
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 4:
            self.mq_get_type_infoRes(REQmsg)

        # 诊断查询/提取诊断信息
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 1:
            self.mq_get_diags_DiagnosedRes(REQmsg)

        # 标注诊断/拒绝诊断信息
        elif REQmsg[0] == 'manual' and REQmsg[1] == 29:
            self.diag_refusedRes(REQmsg)
        # 标注诊断/完成诊断信息
        elif REQmsg[0] == 'manual' and REQmsg[1] == 28:
            self.diag_commitRes(REQmsg)
        # 标注诊断/填写诊断信息
        elif REQmsg[0] == 'manual' and (REQmsg[1] == 26 or REQmsg[1] == 27 ):
            self.diag_updateRes(REQmsg)
        # 标注诊断/提取诊断信息
        elif REQmsg[0] == 'manual' and REQmsg[1] == 25:
            self.get_diagRes(REQmsg)
        # 标注诊断/提取诊断信息
        elif REQmsg[0] == 'manual' and REQmsg[1] == 24:
            self.get_diags_notDiagRes(REQmsg)
        # 标注诊断/删除样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'manual' and REQmsg[1] == 23:
            self.del_sampleInfo_stateRes(REQmsg)
        # 标注诊断/修改样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'manual' and REQmsg[1] == 22:
            self.update_sampleInfo_stateRes(REQmsg)
        # 标注诊断/添加样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'manual' and REQmsg[1] == 21:
            self.add_sampleInfo_stateRes(REQmsg)
        # 标注诊断/删除样本信息(脑电图中的操作)
        elif REQmsg[0] == 'manual' and REQmsg[1] == 19:
            self.del_sample19Res(REQmsg)
        # 标注诊断/添加样本信息(脑电图中的操作)
        elif REQmsg[0] == 'manual' and REQmsg[1] == 17:
            self.insert_sample17Res(REQmsg)
        # 标注诊断/(绘图设置)提取样本信息(绘图设置)
        elif REQmsg[0] == 'manual' and REQmsg[1] == 16:
            self.init_SampleListRes(REQmsg)
        # 标注诊断/修改样本(脑电图中的操作)
        elif REQmsg[0] == 'manual' and REQmsg[1] == 15:
            self.update_sampleInfo15Res(REQmsg)
        # 标注诊断/添加样本
        elif REQmsg[0] == 'manual' and REQmsg[1] == 14:
            self.add_sampleInfo14Res(REQmsg)
        # 标注诊断/删除样本(样本列表中的操作)
        elif REQmsg[0] == 'manual' and REQmsg[1] == 13:
            self.del_sampleInfo13Res(REQmsg)
        # 标注诊断/添加样本(样本列表中的操作)
        elif REQmsg[0] == 'manual' and REQmsg[1] == 12:
            self.update_sampleInfo12Res(REQmsg)
        # 标注诊断/添加样本
        elif REQmsg[0] == 'manual' and REQmsg[1] == 11:
            self.add_sampleInfo11Res(REQmsg)
        # 标注诊断/读取脑电文件数据块
        elif REQmsg[0] == 'manual' and REQmsg[1] == 10:
            self.load_dataDynamical10Res(REQmsg)
        # 标注诊断/读取脑电文件数据块
        elif REQmsg[0] == 'manual' and REQmsg[1] == 9:
            self.load_dataDynamicalRes(REQmsg)
        # 标注诊断/打开脑电文件
        elif REQmsg[0] == 'manual' and REQmsg[1] == 8:
            self.openEEGFileRes(REQmsg)
        # 标注诊断/脑电文件
        elif REQmsg[0] == 'manual' and REQmsg[1] == 7:
            self.get_fileNameByIdDateRes(REQmsg)
        # 标注诊断/检测日期
        elif REQmsg[0] == 'manual' and REQmsg[1] == 6:
            self.get_measureDateByIdRes(REQmsg)
        # 标注诊断/病人信息
        elif REQmsg[0] == 'manual' and REQmsg[1] == 5:
            self.get_patientIdNameRes(REQmsg)
        # 标注诊断/类型、用户信息
        elif REQmsg[0] == 'manual' and REQmsg[1] == 4:
            self.get_type_infoRes(REQmsg)
        # 科研标注/查询、分页
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 30:
            self.rg_pagingRes(REQmsg)
            # 科研标注 /提交标注信息
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 28:
            self.rg_label_commitRes(REQmsg)
            # 科研标注/删除样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 23:
            self.rg_del_sampleInfo_stateRes(REQmsg)
            # 科研标注/修改样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 22:
            self.rg_update_sampleInfo_stateRes(REQmsg)
            # 科研标注/添加样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 21:
            self.rg_add_sampleInfo_stateRes(REQmsg)
            # 科研标注/删除样本信息(脑电图中的操作)
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 19:
            self.rg_del_sample19Res(REQmsg)
            # 科研标注/添加样本信息(脑电图中的操作)
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 17:
            self.rg_insert_sample17Res(REQmsg)
            # 科研标注/(绘图设置)提取样本信息(绘图设置)
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 16:
            self.rg_init_SampleListRes(REQmsg)
            # 科研标注/修改样本(脑电图中的操作)
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 15:
            self.rg_update_sampleInfo15Res(REQmsg)
            # 科研标注/添加样本
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 14:
            self.rg_add_sampleInfo14Res(REQmsg)
            # 科研标注/删除样本(样本列表中的操作)
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 13:
            self.rg_del_sampleInfo13Res(REQmsg)
            # 科研标注/添加样本(样本列表中的操作)
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 12:
            self.rg_update_sampleInfo12Res(REQmsg)
            # 科研标注/读取脑电文件数据块
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 10:
            self.rg_load_dataDynamical10Res(REQmsg)
            # 科研标注/读取脑电文件数据块
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 9:
            self.rg_load_dataDynamicalRes(REQmsg)
            # 科研标注/打开脑电文件
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 8:
            self.rg_openEEGFileRes(REQmsg)
            # 科研标注/类型、用户信息
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 4:
            self.rg_get_type_infoRes(REQmsg)
            # 科研标注/提取标注信息
        elif REQmsg[0] == 'reserching' and REQmsg[1] == 1:
            self.rg_get_notlabelsRes(REQmsg)

        # 执行查看/主题状态提交
        elif REQmsg[0] == 'reserchingQuery' and REQmsg[1] == 31:
            self.rgQ_theme_commitRes(REQmsg)
            # 执行查看/查询、分页
        elif REQmsg[0] == 'reserchingQuery' and REQmsg[1] == 30:
            self.rgQ_pagingRes(REQmsg)
            # 执行查看 /提交标注信息
        elif REQmsg[0] == 'reserchingQuery' and REQmsg[1] == 28:
            self.rgQ_label_commitRes(REQmsg)
            # 执行查看/删除样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'reserchingQuery' and REQmsg[1] == 23:
            self.rgQ_del_sampleInfo_stateRes(REQmsg)
            # 执行查看/修改样本状态信息(脑电图中的操作)
        elif REQmsg[0] == 'reserchingQuery' and REQmsg[1] == 22:
            self.rgQ_update_sampleInfo_stateRes(REQmsg)
            # 执行查看/删除样本信息(脑电图中的操作)
        elif REQmsg[0] == 'reserchingQuery' and REQmsg[1] == 19:
            self.rgQ_del_sample19Res(REQmsg)
            # 执行查看/(绘图设置)提取样本信息(绘图设置)
        elif REQmsg[0] == 'reserchingQuery' and REQmsg[1] == 16:
            self.rgQ_init_SampleListRes(REQmsg)
            # 执行查看/修改样本(脑电图中的操作)
        elif REQmsg[0] == 'reserchingQuery' and REQmsg[1] == 15:
            self.rgQ_update_sampleInfo15Res(REQmsg)
            # 执行查看/删除样本(样本列表中的操作)
        elif REQmsg[0] == 'reserchingQuery' and REQmsg[1] == 13:
            self.rgQ_del_sampleInfo13Res(REQmsg)
            # 执行查看/添加样本(样本列表中的操作)
        elif REQmsg[0] == 'reserchingQuery' and REQmsg[1] == 12:
            self.rgQ_update_sampleInfo12Res(REQmsg)
            # 执行查看/读取脑电文件数据块
        elif REQmsg[0] == 'reserchingQuery' and REQmsg[1] == 10:
            self.rgQ_load_dataDynamical10Res(REQmsg)
            # 执行查看/读取脑电文件数据块
        elif REQmsg[0] == 'reserchingQuery' and REQmsg[1] == 9:
            self.rgQ_load_dataDynamicalRes(REQmsg)
            # 执行查看/打开脑电文件
        elif REQmsg[0] == 'reserchingQuery' and REQmsg[1] == 8:
            self.rgQ_openEEGFileRes(REQmsg)
            # 执行查看/类型、用户信息
        elif REQmsg[0] == 'reserchingQuery' and REQmsg[1] == 4:
            self.rgQ_get_type_infoRes(REQmsg)
            # /提取标注信息
        elif REQmsg[0] == 'reserchingQuery' and REQmsg[1] == 1:
            self.rgQ_get_labelsRes(REQmsg)


        #### dsj ==]====

        # 脑电导入模块
        # 回调获取病人诊断信息信息
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 1:
            self.getPatientCheckInfoRes(REQmsg)
        # 删除病人诊断信息
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 2:
            self.delPatientCheckInfoRes(REQmsg)
        # 添加病人检查信息
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 3:
            self.addCheckInfoRes(REQmsg)
        # 检查脑电文件
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 4:
            self.checkConfigRes(REQmsg)
        # 写脑电请求
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 5:
            self.writeEEGRes(REQmsg)
        # 更新脑电检查信息
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 6:
            self.updateCheckInfoRes(REQmsg)
        # 获取脑电检查信息
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 7:
            self.getFileInfoRes(REQmsg)
        # 删除脑电文件信息
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 11:
            self.delFileInfoRes(REQmsg)

        # 创建会诊
        # 获取医生信息
        elif REQmsg[0] == 'createCons' and REQmsg[1] == 1:
            self.getDoctorInfoRes(REQmsg)
        # 获取完整的脑电检查信息
        elif REQmsg[0] == 'createCons' and REQmsg[1] == 2:
            self.getCpltCheckInfoRes(REQmsg)
        # 获取会诊记录信息
        elif REQmsg[0] == 'createCons' and REQmsg[1] == 3:
            self.getHistoryConsRes(REQmsg)
        # 创建会诊
        elif REQmsg[0] == 'createCons' and REQmsg[1] == 4:
            self.createConsRes(REQmsg)
        # 获取全部的会诊信息
        elif REQmsg[0] == 'createCons' and REQmsg[1] == 6:
            self.getAllConsInfoRes(REQmsg)
        # 获取搜索的信息
        elif REQmsg[0] == 'createCons' and REQmsg[1] == 7:
            self.inqConsInfoRes(REQmsg)
        # 获取搜索医生的信息
        elif REQmsg[0] == 'createCons' and REQmsg[1] == 8:
            self.getSearchDoctorInfoRes(REQmsg)


        # 获取病人信息
        elif REQmsg[0] == 'patientManager' and REQmsg[1] == 1:
            self.getPatientInfoRes(REQmsg)
        # 新增病人信息
        elif REQmsg[0] == 'patientManager' and REQmsg[1] == 2:
            self.addPatientInfoRes(REQmsg)
        # 删除病人信息
        elif REQmsg[0] == 'patientManager' and REQmsg[1] == 3:
            self.delPatientInfoRes(REQmsg)
        # 编辑病人信息
        elif REQmsg[0] == 'patientManager' and REQmsg[1] == 4:
            self.updatePatientInfoRes(REQmsg)
        # 查询病人信息
        elif REQmsg[0] == 'patientManager' and REQmsg[1] == 5:
            self.inqPatientInfoRes(REQmsg)
        elif REQmsg[0] == 'patientManager' and REQmsg[1] == 6:
            self.patientPagingRes(REQmsg)


        # 脑电导入模块
        # 回调获取病人诊断信息信息
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 1:
            self.getPatientCheckInfoRes(REQmsg)
        # 删除病人诊断信息
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 2:
            self.delPatientCheckInfoRes(REQmsg)
        # 添加病人检查信息
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 3:
            self.addCheckInfoRes(REQmsg)
        # 检查脑电文件配置
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 4:
            self.checkConfigRes(REQmsg)
        #生成脑电文件名
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 10:
            self.makeFileNameRes(REQmsg)
        # 写脑电请求
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 5:
            self.writeEEGRes(REQmsg)
        # 更新脑电检查信息
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 6:
            self.updateCheckInfoRes(REQmsg)
        # 获取脑电检查信息
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 7:
            self.getFileInfoRes(REQmsg)
        # 获取病人选择信息
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 8:
            self.getChoosePatientInfoRes(REQmsg)
        # 获取医生选择信息
        elif REQmsg[0] == 'dataImport' and REQmsg[1] == 9:
            self.getChooseDoctorInfoRes(REQmsg)

        # 获取课堂信息
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 1:
            self.getLessonInfoRes(REQmsg)
        # 获取诊断病例ID信息
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 2:
            self.getDiagCheckIDRes(REQmsg)
        # 获取诊断病例文件名信息
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 3:
            self.getFileNameRes(REQmsg)
        # 添加课堂信息
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 4:
            self.addLessonRes(REQmsg)
        # 删除课堂信息
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 5:
            self.delLessonRes(REQmsg)
        # 更新课堂信息
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 6:
            self.updateLessonRes(REQmsg)
        # 获取课堂学员信息
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 7:
            self.getStudentInfoRes(REQmsg)
        # 获取课堂内容信息
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 9:
            self.getContentInfoRes(REQmsg)
        # 查询课堂信息
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 13:
            self.inquiryLessonInfoRes(REQmsg)
        # 获取文件标注用户ID
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 14:
            self.getCheckUserIDRes(REQmsg)
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 16:
            self.addStudentRes(REQmsg)
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 17:
            self.getlessonStudentRes(REQmsg)
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 18:
            self.delStudentRes(REQmsg)
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 19:
            self.addLessonContentRes(REQmsg)
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 20:
            self.delLessonContentRes(REQmsg)
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 21:
            self.studentPagingRes(REQmsg)
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 22:
            self.searchStudentPageInfoRes(REQmsg)
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 23:
            self.eggPagingRes(REQmsg)
        elif REQmsg[0] == 'createLesson' and REQmsg[1] == 24:
            self.searchEegPageInfoRes(REQmsg)

        # 样本统计模块
        # 样本统计
        elif REQmsg[0] == 'sampleState' and REQmsg[1] == 1:
            self.getSpecificInfoRes(REQmsg)
        # 获取样本统计中各个类型数据的数量
        elif REQmsg[0] == 'sampleState' and REQmsg[1] == 2:
            self.getSpecificNumRes(REQmsg)
        # 获取样本统计中样本的详细信息
        elif REQmsg[0] == 'sampleState' and REQmsg[1] == 3:
            self.getSpecificDetailRes(REQmsg)
        # 根据过滤器信息获取样本的数量
        elif REQmsg[0] == 'sampleState' and REQmsg[1] == 4:
            self.getSpecNumFromFltRes(REQmsg)


        # 任务设置模块
        # 回调获取标注主题信息
        elif REQmsg[0] == 'taskSettings' and REQmsg[1] == 1:
            self.getThemeInfoRes(REQmsg)
        # 回调添加标注主题信息
        elif REQmsg[0] == 'taskSettings' and REQmsg[1] == 2:
            self.addThemeInfoRes(REQmsg)
        # 回调删除标注主题信息
        elif REQmsg[0] == 'taskSettings' and REQmsg[1] == 3:
            self.delThemeInfoRes(REQmsg)
        # 回调更新标注主题信息
        elif REQmsg[0] == 'taskSettings' and REQmsg[1] == 4:
            self.updateThemeInfoRes(REQmsg)
        # 回调获取标注任务信息
        elif REQmsg[0] == 'taskSettings' and REQmsg[1] == 5:
            self.getTaskInfoRes(REQmsg)
        # 回调添加标注任务信息
        elif REQmsg[0] == 'taskSettings' and REQmsg[1] == 6:
            self.addTaskInfoRes(REQmsg)
        # 回调删除标注任务信息
        elif REQmsg[0] == 'taskSettings' and REQmsg[1] == 7:
            self.delTaskInfoRes(REQmsg)
        # 回调更新标注任务信息
        elif REQmsg[0] == 'taskSettings' and REQmsg[1] == 8:
            self.updateTaskInfoRes(REQmsg)
        # 回调获取筛选框信息
        elif REQmsg[0] == 'taskSettings' and REQmsg[1] == 9:
            self.getChooseDetailInfoRes(REQmsg)
        # 回调启动标注主题
        elif REQmsg[0] == 'taskSettings' and REQmsg[1] == 10:
            self.startThemeRes(REQmsg)
        # 查找标注人员信息
        elif REQmsg[0] == 'taskSettings' and REQmsg[1] == 11:
            self.getChooseMarkerInfoRes(REQmsg)

        # 获取算法信息
        elif REQmsg[0] == 'algorithm' and REQmsg[1] == 1:
            self.getAlgorithmInfoRes(REQmsg)
        # 添加算法信息
        elif REQmsg[0] == 'algorithm' and REQmsg[1] == 2:
            self.addAlgorithmInfoRes(REQmsg)
        # 删除算法
        elif REQmsg[0] == 'algorithm' and REQmsg[1] == 3:
            self.delAlgorithmInfoRes(REQmsg)
        # 查询算法信息
        elif REQmsg[0] == 'algorithm' and REQmsg[1] == 4:
            self.inquiryAlgorithmInfoRes(REQmsg)
        # 添加算法文件
        elif REQmsg[0] == 'algorithm' and REQmsg[1] == 5:
            self.addAlgorithmFileRes(REQmsg)
        # 获取算法文件名称
        elif REQmsg[0] == 'algorithm' and REQmsg[1] == 6:
            self.getAlgorithmFileNameRes(REQmsg)
        elif REQmsg[0] == 'algorithm' and REQmsg[1] == 7:
            self.algorithmInfoPagingRes(REQmsg)

        # 执行查看模块
        # 回调获取某一用户创建的标注主题信息
        # elif REQmsg[0] == 'detailLook' and REQmsg[1] == 1:
        #     self.getUserThemeInfoRes(REQmsg)
        # # 回调修改某一用户创建的标注主题状态
        # elif REQmsg[0] == 'detailLook' and REQmsg[1] == 2:
        #     self.updateUserThemeInfoRes(REQmsg)
        # # 回调修改某一标注主题的标注任务的状态
        # elif REQmsg[0] == 'detailLook' and REQmsg[1] == 3:
        #     self.updateUserTaskInfoRes(REQmsg)
        # # 回调获取某一用户对于某一标注文件的所有标注的详细信息
        # elif REQmsg[0] == 'detailLook' and REQmsg[1] == 4:
        #     self.getDetailInfoRes(REQmsg)
        # # 回调删除某一详细的标注信息
        # elif REQmsg[0] == 'detailLook' and REQmsg[1] == 5:
        #     self.delDetailInfoRes(REQmsg)
        # # 回调删除某一标注主题的标注任务的所有详细的标注信息
        # elif REQmsg[0] == 'detailLook' and REQmsg[1] == 6:
        #     self.delDetailAllRes(REQmsg)
        # elif REQmsg[0] == 'detailLook' and REQmsg[1] == 7:
        #     self.checkTaskStateAllRes(REQmsg)


        # 构建集合
        elif REQmsg[0] == 'setBuild' and REQmsg[1] == 1:
            self.getSetInitDataRes(REQmsg)
        elif REQmsg[0] == 'setBuild' and REQmsg[1] == 2:
            self.getSetRes(REQmsg)
        elif REQmsg[0] == 'setBuild' and REQmsg[1] == 3:
            self.getSetBuildFltDataRes(REQmsg)
        elif REQmsg[0] == 'setBuild' and REQmsg[1] == 4:
            self.getSetExportInitDataRes(REQmsg)
        elif REQmsg[0] == 'setBuild' and REQmsg[1] == 5:
            self.getSetExportDataRes(REQmsg)
        elif REQmsg[0] == 'setBuild' and REQmsg[1] == 6:
            self.delSetRes(REQmsg)
        elif REQmsg[0] == 'setBuild' and REQmsg[1] == 7:
            self.buildSetRes(REQmsg)
        elif REQmsg[0] == 'setBuild' and REQmsg[1] == 8:
            self.buildSetGetPgRes(REQmsg)
        elif REQmsg[0] == 'setBuild' and REQmsg[1] == 9:
            self.buildSetCancelRes(REQmsg)
        elif REQmsg[0] == 'setBuild' and REQmsg[1] == 10:
            self.getSetSearchRes(REQmsg)
        elif REQmsg[0] == 'setBuild' and REQmsg[1] == 11:
            self.getSetDescribeRes(REQmsg)

        # 模型训练
        elif REQmsg[0] == 'modelTrain' and REQmsg[1] == 1:
            self.getModelInfoRes(REQmsg)
        elif REQmsg[0] == 'modelTrain' and REQmsg[1] == 2:
            self.get_classifierInfo_by_setId_and_algIdRes(REQmsg)
        elif REQmsg[0] == 'modelTrain' and REQmsg[1] == 3:
            self.runProcessForTrainRes(REQmsg)
        elif REQmsg[0] == 'modelTrain' and REQmsg[1] == 4:
            self.modelAlgInfoPagingRes(REQmsg)
        elif REQmsg[0] == 'modelTrain' and REQmsg[1] == 5:
            self.modelInquiryAlgInfoRes(REQmsg)
        elif REQmsg[0] == 'modelTrain' and REQmsg[1] == 6:
            self.modelSetInfoPagingRes(REQmsg)
        elif REQmsg[0] == 'modelTrain' and REQmsg[1] == 7:
            self.modelInquirySetInfoRes(REQmsg)
        elif REQmsg[0] == 'modelTrain' and REQmsg[1] == 8:
            self.matchAlgSetRes(REQmsg)
        elif REQmsg[0] == 'modelTrain' and REQmsg[1] == 9:
            self.getTrainPerformanceRes(REQmsg)
        elif REQmsg[0] == 'modelTrain' and REQmsg[1] == 10:
            self.getProgressRes(REQmsg)
        elif REQmsg[0] == 'modelTrain' and REQmsg[1] == 11:
            self.train_cancelRes(REQmsg)

        # 模型管理
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 1:
            self.getClassifierAlgSetNameRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 2:
            self.inquiryClassifierInfoRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 3:
            self.delClassifierInfoRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 4:
            self.getSelectAlgorithmInfoRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 5:
            self.checkClassfierInfoRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 6:
            self.cls_restateRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 7:
            self.checkstateRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 8:
            self.model_transmit_messageRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 9:
            self.classifier_id_inquiryRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 10:
            self.classifierPaingRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 11:
            self.classifierPaging_alRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 12:
            self.inquiryCls_alg_InfoRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 13:
            self.getClassifier_configRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 14:
            self.getSelectSetInfoRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 15:
            self.inquiryCls_set_InfoRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 16:
            self.classifierPaging_setRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 17:
            self.upload_schemeRes(REQmsg)
        elif REQmsg[0] == 'classifier' and REQmsg[1] == 18:
            self.upload_modelRes(REQmsg)


        # 模型测试
        elif REQmsg[0] == 'modelTest' and REQmsg[1] == 1:
            self.getClassifierInfoRes(REQmsg)
        elif REQmsg[0] == 'modelTest' and REQmsg[1] == 2:
            self.runProcessForTestRes(REQmsg)
        elif REQmsg[0] == 'modelTest' and REQmsg[1] == 3:
            self.getResultRes(REQmsg)

        # 脑电扫描
        elif REQmsg[0] == 'auto' and REQmsg[1] == 1:
            self.getAutoInitDataRes(REQmsg)
        elif REQmsg[0] == 'auto' and REQmsg[1] == 2:
            self.getPatientMeasureDayRes(REQmsg)
        elif REQmsg[0] == 'auto' and REQmsg[1] == 3:
            self.getPatientFileRes(REQmsg)
        elif REQmsg[0] == 'auto' and REQmsg[1] == 4:
            self.getFileChannelsRes(REQmsg)
        elif REQmsg[0] == 'auto' and REQmsg[1] == 5:
            self.autoClassifierInfoPagingRes(REQmsg)
        elif REQmsg[0] == 'auto' and REQmsg[1] == 6:
            self.autoInquiryClassifierInfoRes(REQmsg)
        elif REQmsg[0] == 'auto' and REQmsg[1] == 7:
            self.runProcessForScanRes(REQmsg)
        elif REQmsg[0] == 'auto' and REQmsg[1] == 8:
            self.matchClassifierFileRes(REQmsg)
        elif REQmsg[0] == 'auto' and REQmsg[1] == 9:
            self.getScanProgressRes(REQmsg)

        # 评估标注
        elif REQmsg[0] == 'assessLabel' and REQmsg[1] == 1:
            self.getAssessInfoRes(REQmsg)
        elif REQmsg[0] == 'assessLabel' and REQmsg[1] == 2:
            self.getModelIdNameRes(REQmsg)
        elif REQmsg[0] == 'assessLabel' and REQmsg[1] == 3:
            self.assessClassifierInfoPagingRes(REQmsg)
        elif REQmsg[0] == 'assessLabel' and REQmsg[1] == 4:
            self.getAssessFileInfoRes(REQmsg)
        elif REQmsg[0] == 'assessLabel' and REQmsg[1] == 8:
            self.assessOpenEEGFileRes(REQmsg)
        elif REQmsg[0] == 'assessLabel' and REQmsg[1] == 9:
            self.assess_load_dataDynamicalRes(REQmsg)
        elif REQmsg[0] == 'assessLabel' and REQmsg[1] == 10:
            self.assess_load_dataDynamicalRes(REQmsg)
        elif REQmsg[0] == 'assessLabel' and REQmsg[1] == 11:
            self.update_labelListInfoRes(REQmsg)
        elif REQmsg[0] == 'assessLabel' and REQmsg[1] == 12:
            self.update_labelListInfo12Res(REQmsg)
        elif REQmsg[0] == 'assessLabel' and REQmsg[1] == 13:
            self.update_state_labelListInfoRes(REQmsg)
        elif REQmsg[0] == 'assessLabel' and REQmsg[1] == 14:
            self.del_labelListInfoRes(REQmsg)
        elif REQmsg[0] == 'assessLabel' and REQmsg[1] == 15:
            self.del_labelListInfo15Res(REQmsg)
        elif REQmsg[0] == 'assessLabel' and REQmsg[1] == 16:
            self.del_labelListInfo16Res(REQmsg)


        # 清理标注
        elif REQmsg[0] == 'clearLabel' and REQmsg[1] == 1:
            self.getClearLabelInfoRes(REQmsg)
        elif REQmsg[0] == 'clearLabel' and REQmsg[1] == 2:
            self.inquiryScanClassifierInfoRes(REQmsg)
        elif REQmsg[0] == 'clearLabel' and REQmsg[1] == 3:
            self.scanClassifierInfoPagingRes(REQmsg)
        elif REQmsg[0] == 'clearLabel' and REQmsg[1] == 4:
            self.getScanInfoRes(REQmsg)
        elif REQmsg[0] == 'clearLabel' and REQmsg[1] == 5:
            self.getCurClearLabelInfoRes(REQmsg)
        elif REQmsg[0] == 'clearLabel' and REQmsg[1] == 6:
            self.getScanFileInfoRes(REQmsg)
        elif REQmsg[0] == 'clearLabel' and REQmsg[1] == 7:
            self.delLabelListInfoRes(REQmsg)
        elif REQmsg[0] == 'clearLabel' and REQmsg[1] == 8:
            self.delLabelByModelFileRes(REQmsg)
        elif REQmsg[0] == 'clearLabel' and REQmsg[1] == 9:
            self.getLabelInfoByAssessRes(REQmsg)
        elif REQmsg[0] == 'clearLabel' and REQmsg[1] == 10:
            self.getSearchScanFileInfoRes(REQmsg)


        else:
            print(f"{REQmsg[0]}.{REQmsg[1]}未定义")
