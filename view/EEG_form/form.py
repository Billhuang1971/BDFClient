from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtWidgets import QPushButton, QFrame, QSizePolicy, QLabel, QHBoxLayout
class Ui_EEGView(object):
    def setupUi(self, Ui_Form):
        Ui_Form.setObjectName("Ui_Form")
        #ManualForm.resize(1080, 760)
        self.gridLayout_1 = QtWidgets.QGridLayout(Ui_Form)
        self.gridLayout_1.setObjectName("gridLayout_1")

        self.groupBox1 = QtWidgets.QGroupBox(Ui_Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.groupBox1.setFont(font)
        self.groupBox1.setTitle("")
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox1)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.scrollArea_1 = QtWidgets.QScrollArea(self.groupBox1)
        self.scrollArea_1.setWidgetResizable(True)
        self.scrollArea_1.setObjectName("scrollArea_1")
        self.scrollAreaWidgetContents_1 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_1.setGeometry(QtCore.QRect(0, 0, 780, 720))
        self.scrollAreaWidgetContents_1.setObjectName("scrollAreaWidgetContents_1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.glCanvas = QtWidgets.QGridLayout()
        self.glCanvas.setSpacing(0)
        self.glCanvas.setObjectName("glCanvas")
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.glBtn = QtWidgets.QGridLayout(self.groupBox)
        self.glBtn.setObjectName("glBtn")
        # self.btnBegin = QtWidgets.QPushButton(self.groupBox)
        # self.btnBegin.setObjectName("btnBegin")
        # self.glBtn.addWidget(self.btnBegin, 0, 0, 1, 2)
        vline7 = QFrame()
        vline7.setFrameShape(QFrame.VLine)
        vline7.setFrameShadow(QFrame.Sunken)
        self.glBtn.addWidget(vline7, 0, 1,1, 1)
        self.glBtn.setColumnMinimumWidth(0, 10)
        self.btnDowning = QtWidgets.QPushButton(self.groupBox)
        self.btnDowning.setObjectName("btnDowning")
        self.glBtn.addWidget(self.btnDowning, 0, 6, 1, 2)
        self.btnDown = QtWidgets.QPushButton(self.groupBox)
        self.btnDown.setObjectName("btnDown")
        self.glBtn.addWidget(self.btnDown, 0, 2, 1, 2)
        self.btnUp = QtWidgets.QPushButton(self.groupBox)
        self.btnUp.setObjectName("btnUp")
        self.glBtn.addWidget(self.btnUp, 0, 4, 1, 2)
        self.btnUping = QtWidgets.QPushButton(self.groupBox)
        self.btnUping.setObjectName("btnUping")
        self.glBtn.addWidget(self.btnUping, 0, 9, 1, 2)
        self.moveSpeed = QtWidgets.QComboBox(self.groupBox)
        self.moveSpeed.setObjectName("moveSpeed")
        self.moveSpeed.setFixedWidth(int(self.moveSpeed.sizeHint().width() * 0.7))
        self.moveSpeed.setEditable(False)
        self.moveSpeed.setValidator(QIntValidator())
        self.glBtn.addWidget(self.moveSpeed, 0, 8, 1, 1)
        self.moveSpeed.addItem("1x")
        self.moveSpeed.addItem("2x")
        self.moveSpeed.addItem("3x")
        # self.btnEnd = QtWidgets.QPushButton(self.groupBox)
        # self.btnEnd.setObjectName("btnEnd")
        # self.glBtn.addWidget(self.btnEnd, 0, 10, 1, 2)

        vline1 = QFrame()
        vline1.setFrameShape(QFrame.VLine)
        vline1.setFrameShadow(QFrame.Sunken)
        self.glBtn.addWidget(vline1, 0, 11, 1, 1)

        self.editTimeText = QtWidgets.QLabel(self.groupBox)
        self.editTimeText.setObjectName("editTimeText")
        self.editTimeText.setAlignment(Qt.AlignCenter)
        self.glBtn.addWidget(self.editTimeText, 0, 12, 1, 1)

        self.editTime = QtWidgets.QLineEdit(self.groupBox)
        self.editTime.setObjectName("editTime")
        self.editTime.setValidator(QRegExpValidator(QRegExp(r"^([01]\d|2[0-3]):[0-5]\d:[0-5]\d$")))
        self.glBtn.addWidget(self.editTime, 0, 13, 1, 1)

        self.secondsSpanText = QtWidgets.QLabel(self.groupBox)
        self.secondsSpanText.setObjectName("secondsSpanText")
        self.secondsSpanText.setAlignment(Qt.AlignCenter)
        self.glBtn.addWidget(self.secondsSpanText, 0, 14, 1, 1)
        self.secondsSpan = QtWidgets.QComboBox(self.groupBox)
        self.secondsSpan.setObjectName("secondsSpan")
        self.secondsSpan.setFixedWidth(int(self.secondsSpan.sizeHint().width() * 0.7))
        self.secondsSpan.setEditable(True)
        self.secondsSpan.setValidator(QIntValidator())
        self.glBtn.addWidget(self.secondsSpan, 0, 15, 1, 1)

        self.editTime.setFixedWidth(int(self.secondsSpan.sizeHint().width() * 0.8))

        self.moveLengthText = QtWidgets.QLabel(self.groupBox)
        self.moveLengthText.setObjectName("moveLengthText")
        self.moveLengthText.setAlignment(Qt.AlignCenter)
        self.glBtn.addWidget(self.moveLengthText, 0, 17, 1, 1)
        self.moveLength = QtWidgets.QComboBox(self.groupBox)
        self.moveLength.setObjectName("moveLength")
        self.moveLength.setEditable(True)
        self.moveLength.setValidator(QIntValidator())
        self.moveLength.setFixedWidth(int(self.moveLength.sizeHint().width() * 0.7))
        self.glBtn.addWidget(self.moveLength, 0, 18, 1, 1)
        self.sensitivityText = QtWidgets.QLabel(self.groupBox)
        self.sensitivityText.setObjectName("sensitivityText")

        self.sensitivityText.setAlignment(Qt.AlignCenter)
        self.glBtn.addWidget(self.sensitivityText, 0, 19, 1, 1)
        self.sensitivity = QtWidgets.QComboBox(self.groupBox)
        self.sensitivity.setObjectName("sensitivity")
        self.sensitivity.setFixedWidth(int(self.sensitivity.sizeHint().width() * 0.7))
        self.sensitivity.setEditable(True)
        self.sensitivity.setValidator(QIntValidator())
        self.glBtn.addWidget(self.sensitivity, 0, 20, 1, 1)

        vline4 = QFrame()
        vline4.setFrameShape(QFrame.VLine)
        vline4.setFrameShadow(QFrame.Sunken)
        self.glBtn.addWidget(vline4, 0, 21, 1, 1)

        self.subtractAverage = QtWidgets.QRadioButton(self.groupBox)

        self.subtractAverage.setObjectName("subtractAverage")
        self.subtractAverage.setChecked(False)
        self.subtractAverage.setAutoExclusive(False)
        self.subtractAverage.setLayoutDirection(Qt.RightToLeft)
        self.subtractAverage.setStyleSheet("""
                QRadioButton::indicator {
                        width: 10px; 
                        height: 10px; 
                        border-radius: 5px; 
                        border: 0.25px solid darkgray; 
                        background: white; 
                    }

                    QRadioButton::indicator:checked {   
                        border: 0.25px solid lightgray; 
                        background: qradialgradient(  
                        cx: 0.5, cy: 0.5, fx: 0.5, fy: 0.5, 
                        radius: 0.7, 
                        stop: 0 black, 
                        stop: 0.6 rgba(255, 255, 255, 0.9),   
                        stop: 1 rgba(255, 255, 255, 0)  
                    );  
                    }

                    QRadioButton::indicator:disabled {
                        border: 1px solid lightgray; 
                        background: lightgray;
                    }""")

        self.glBtn.addWidget(self.subtractAverage, 0, 22, 1, 1)

        self.secondsLine = QtWidgets.QRadioButton(self.groupBox)
        self.secondsLine.setLayoutDirection(Qt.RightToLeft)
        self.secondsLine.setStyleSheet("""
                QRadioButton::indicator {
                        width: 10px; 
                        height: 10px; 
                        border-radius: 5px;
                        border: 0.25px solid darkgray; 
                        background: white; 
                    }

                    QRadioButton::indicator:checked {   
                        border: 0.25px solid lightgray; 
                        background: qradialgradient(  
                        cx: 0.5, cy: 0.5, fx: 0.5, fy: 0.5, 
                        radius: 0.7, 
                        stop: 0 black, 
                        stop: 0.6 rgba(255, 255, 255, 0.9), 
                        stop: 1 rgba(255, 255, 255, 0) 
                    );  
                    }

                    QRadioButton::indicator:disabled {
                        border: 1px solid lightgray; /
                        background: lightgray; 
                    }""")
        self.secondsLine.setObjectName("secondsLine")
        self.secondsLine.setChecked(True)
        self.secondsLine.setAutoExclusive(False)

        self.glBtn.addWidget(self.secondsLine, 0, 23, 1, 1)

        vline3 = QFrame()
        vline3.setFrameShape(QFrame.VLine)
        vline3.setFrameShadow(QFrame.Sunken)
        self.glBtn.addWidget(vline3, 0, 24, 1, 1)

        self.scenarioSelectionBtn = QtWidgets.QPushButton(self.groupBox)
        self.scenarioSelectionBtn.setObjectName("scenarioSelectionBtn")
        self.glBtn.addWidget(self.scenarioSelectionBtn, 0, 25, 1, 2)
        self.channelSelectionBtn = QtWidgets.QPushButton(self.groupBox)
        self.channelSelectionBtn.setObjectName("channelSelectionBtn")
        self.glBtn.addWidget(self.channelSelectionBtn, 0, 27, 1, 2)
        self.sampleSelectionBtn = QtWidgets.QPushButton(self.groupBox)
        self.sampleSelectionBtn.setObjectName("sampleSelectionBtn")
        self.glBtn.addWidget(self.sampleSelectionBtn, 0, 29, 1, 2)

        vline2 = QFrame()
        vline2.setFrameShape(QFrame.VLine)
        vline2.setFrameShadow(QFrame.Sunken)
        self.glBtn.addWidget(vline2, 0, 31, 1, 1)
        self.glBtn.setColumnMinimumWidth(32, 10)

        self.glCanvas.addWidget(self.groupBox, 1, 0, 1, 1)
        self.listView = QtWidgets.QListView(self.scrollAreaWidgetContents_1)
        self.listView.setObjectName("listView")
        self.glCanvas.addWidget(self.listView, 0, 0, 1, 1)
        self.gridLayout_1.addWidget(self.groupBox1, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.scrollArea_1, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.glCanvas, 0, 0, 1, 1)
        self.scrollArea_1.setWidget(self.scrollAreaWidgetContents_1)

        self.groupBox2 = QtWidgets.QGroupBox(Ui_Form)
        self.groupBox2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox2.sizePolicy().hasHeightForWidth())
        self.groupBox2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.groupBox2.setFont(font)
        self.groupBox2.setTitle("")
        self.groupBox2.setObjectName("groupBox2")
        # self.groupBox2.setFixedWidth(400)
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox2)#右侧总布局
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gbPatientInfo = QtWidgets.QGroupBox(self.groupBox2)
        self.gbPatientInfo.setObjectName("gbPatientInfo")
        self.glPatientInfo = QtWidgets.QGridLayout(self.gbPatientInfo)
        self.glPatientInfo.setObjectName("glPatientInfo")
        self.labelPatientNameInfo = QtWidgets.QLabel(self.gbPatientInfo)
        self.labelPatientNameInfo.setObjectName("labelPatientNameInfo")
        self.glPatientInfo.addWidget(self.labelPatientNameInfo, 1, 0, 1, 1)
        self.labelPatientName = QtWidgets.QLabel(self.gbPatientInfo)
        self.labelPatientName.setObjectName("labelPatientName")
        self.glPatientInfo.addWidget(self.labelPatientName, 1, 1, 1, 1)
        self.labelPatientSexInfo = QtWidgets.QLabel(self.gbPatientInfo)
        self.labelPatientSexInfo.setObjectName("labelPatientSexInfo")
        self.glPatientInfo.addWidget(self.labelPatientSexInfo, 1, 2, 1, 1)
        self.labelPatientSex = QtWidgets.QLabel(self.gbPatientInfo)
        self.labelPatientSex.setObjectName("labelPatientSex")
        self.glPatientInfo.addWidget(self.labelPatientSex, 1, 3, 1, 1)
        self.labelPatientBirthInfo = QtWidgets.QLabel(self.gbPatientInfo)
        self.labelPatientBirthInfo.setObjectName("labelPatientBirthInfo")
        self.glPatientInfo.addWidget(self.labelPatientBirthInfo, 2, 0, 1, 1)
        self.labelPatientBirth = QtWidgets.QLabel(self.gbPatientInfo)
        self.labelPatientBirth.setObjectName("labelPatientBirth")
        self.glPatientInfo.addWidget(self.labelPatientBirth, 2, 1, 1, 2)
        self.labelPatientMeasureInfo = QtWidgets.QLabel(self.gbPatientInfo)
        self.labelPatientMeasureInfo.setObjectName("labelPatientMeasureInfo")
        self.glPatientInfo.addWidget(self.labelPatientMeasureInfo, 3, 0, 1, 1)
        self.labelPatientMeasure = QtWidgets.QLabel(self.gbPatientInfo)
        self.labelPatientMeasure.setObjectName("labelPatientMeasure")
        self.glPatientInfo.addWidget(self.labelPatientMeasure, 3, 1, 1, 2)

        self.gbSample = QtWidgets.QGroupBox(self.groupBox2)
        self.gbSample.setObjectName("gbSample")
        self.gridLayout_4.addWidget(self.gbSample, 1, 0, 1, 1) #将显示样本添加到总布局的第一行，占据1行1列
        self.glSample = QtWidgets.QGridLayout(self.gbSample) #glSample为gbsample里的布局
        self.glSample.setObjectName("glSample")

        self.waveLayout = QHBoxLayout()  # 创建一个水平布局
        #self.waveLayout.setSpacing(1)  # 设置控件之间的间距为 5
        self.hideWaveText = QLabel("波形")
        self.hideWaveText.setMaximumWidth(35)
        self.waveLayout.addWidget(self.hideWaveText)
        #self.glSample.addWidget(self.hideWaveText, 1, 0, 1, 1)

        self.hideWave = QtWidgets.QRadioButton(self.gbSample)
        #self.hideWave.setLayoutDirection(Qt.RightToLeft)
        self.hideWave.setObjectName("hideWave")
        self.hideWave.setStyleSheet("""
                QRadioButton::indicator {
                        width: 10px; 
                        height: 10px;
                        border-radius: 5px;
                        border: 0.25px solid darkgray; 
                        background: white; 
                    }

                    QRadioButton::indicator:checked {   
                        border: 0.25px solid lightgray; 
                        background: qradialgradient(  
                        cx: 0.5, cy: 0.5, fx: 0.5, fy: 0.5,   
                        radius: 0.7, 
                        stop: 0 black, 
                        stop: 0.6 rgba(255, 255, 255, 0.9), 
                        stop: 1 rgba(255, 255, 255, 0) 
                    );  
                    }

                    QRadioButton::indicator:disabled {
                        border: 1px solid lightgray;
                        background: lightgray; 
                    }""")
        self.hideWave.setChecked(True)
        self.hideWave.setAutoExclusive(False)
        self.waveLayout.addWidget(self.hideWave)
        self.glSample.addLayout(self.waveLayout,1,0,1,1)

        self.stateLayout = QHBoxLayout()  # 创建一个水平布局
        self.hideStateText = QLabel("状态")
        # self.waveLayout.setSpacing(1)  # 设置控件之间的间距为 5
        self.hideStateText.setMaximumWidth(35)
        self.stateLayout.addWidget(self.hideStateText)
        #self.glSample.addWidget(self.hideStateText, 1, 2, 1, 1)
        self.hideState = QtWidgets.QRadioButton(self.gbSample)
        self.hideState.setObjectName("hideState")

        self.hideState.setStyleSheet("""
                QRadioButton::indicator {
                        width: 10px; 
                        height: 10px; 
                        border-radius: 5px; 
                        border: 0.25px solid darkgray; 
                        background: white; 
                    }

                    QRadioButton::indicator:checked {   
                        border: 0.25px solid lightgray; 
                        background: qradialgradient(  
                        cx: 0.5, cy: 0.5, fx: 0.5, fy: 0.5,
                        radius: 0.7, 
                        stop: 0 black,
                        stop: 0.6 rgba(255, 255, 255, 0.9), 
                        stop: 1 rgba(255, 255, 255, 0) 
                    );  
                    }

                    QRadioButton::indicator:disabled {
                        border: 1px solid lightgray; 
                        background: lightgray; 
                    }""")
        self.hideState.setChecked(True)
        self.hideState.setAutoExclusive(False)
        self.stateLayout.addWidget(self.hideState)
        self.glSample.addLayout(self.stateLayout,1,1,1,1)

        self.EventLayout = QHBoxLayout()  # 创建一个水平布局
        self.hideEventText = QLabel("事件")
        self.hideEventText.setMaximumWidth(35)
        self.EventLayout.addWidget(self.hideEventText)

        self.hideEvent = QtWidgets.QRadioButton(self.gbSample)
        self.hideEvent.setObjectName("hideWave")
        self.hideEvent.setStyleSheet("""
                        QRadioButton::indicator {
                                width: 10px; 
                                height: 10px;
                                border-radius: 5px;
                                border: 0.25px solid darkgray; 
                                background: white; 
                            }

                            QRadioButton::indicator:checked {   
                                border: 0.25px solid lightgray; 
                                background: qradialgradient(  
                                cx: 0.5, cy: 0.5, fx: 0.5, fy: 0.5,   
                                radius: 0.7, 
                                stop: 0 black, 
                                stop: 0.6 rgba(255, 255, 255, 0.9), 
                                stop: 1 rgba(255, 255, 255, 0) 
                            );  
                            }

                            QRadioButton::indicator:disabled {
                                border: 1px solid lightgray;
                                background: lightgray; 
                            }""")
        self.hideEvent.setChecked(True)
        self.hideEvent.setAutoExclusive(False)
        self.EventLayout.addWidget(self.hideEvent)
        self.glSample.addLayout(self.EventLayout,1,2,1,1)

        self.labelMeasureTimeInfo = QtWidgets.QLabel(self.gbPatientInfo)
        self.labelMeasureTimeInfo.setObjectName("labelMeasureTimeInfo")
        self.glPatientInfo.addWidget(self.labelMeasureTimeInfo, 4, 0, 1, 1)
        self.labelMeasureTime = QtWidgets.QLabel(self.gbPatientInfo)
        self.labelMeasureTime.setObjectName("labelMeasureTime")
        self.glPatientInfo.addWidget(self.labelMeasureTime, 4, 1, 1, 2)

        self.labelFileNameInfo = QtWidgets.QLabel(self.gbPatientInfo)
        self.labelFileNameInfo.setObjectName("labelFileNameInfo")
        self.glPatientInfo.addWidget(self.labelFileNameInfo, 5, 0, 1, 1)
        self.labelFileName = QtWidgets.QLabel(self.gbPatientInfo)
        self.labelFileName.setObjectName("labelFileName")
        self.glPatientInfo.addWidget(self.labelFileName, 5, 1, 1, 2)


        self.gridLayout_4.addWidget(self.gbPatientInfo, 0, 0, 1, 1)

        #将表格以及显示参数添加到显示样本的布局gl中
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox2)
        self.tableWidget.setObjectName("tableWidget")
        self.glSample.addWidget(self.tableWidget, 2, 0, 1, 3)
        self.tableWidget.setStyleSheet('''
                            QTableWidget::item:selected {
                                background-color: lightblue;
                                color: black;
                            }
                            QTableWidget::item:selected:active {
                                background-color: lightblue;
                                color: black;
                            }
                        ''')

        self.labelTypeInfo = QtWidgets.QLabel(self.gbSample)
        self.labelTypeInfo.setObjectName("labelTypeInfo")
        self.glSample.addWidget(self.labelTypeInfo, 3, 0, 1, 1)
        self.labelType = QtWidgets.QLabel(self.gbSample)
        self.labelType.setObjectName("labelType")
        self.glSample.addWidget(self.labelType, 3, 1, 1, 2)

        self.labelChannelInfo = QtWidgets.QLabel(self.gbSample)
        self.labelChannelInfo.setObjectName("labelChannelInfo")
        self.glSample.addWidget(self.labelChannelInfo, 4, 0, 1, 1)
        self.labelChannel = QtWidgets.QLabel(self.gbSample)
        self.labelChannel.setObjectName("labelChannel")
        self.glSample.addWidget(self.labelChannel, 4, 1, 1, 2)

        self.labelLengthInfo = QtWidgets.QLabel(self.gbSample)
        self.labelLengthInfo.setObjectName("labelLengthInfo")
        self.glSample.addWidget(self.labelLengthInfo, 5, 0, 1, 1)
        self.labelLength = QtWidgets.QLabel(self.gbSample)
        self.labelLength.setObjectName("labelLength")
        self.glSample.addWidget(self.labelLength, 5, 1, 1, 2)

        self.labelBeginInfo = QtWidgets.QLabel(self.gbSample)
        self.labelBeginInfo.setObjectName("labelBeginInfo")
        self.glSample.addWidget(self.labelBeginInfo, 6, 0, 1, 1)
        self.labelBegin = QtWidgets.QLabel(self.gbSample)
        self.labelBegin.setObjectName("labelBegin")
        self.glSample.addWidget(self.labelBegin, 6, 1, 1, 2)

        self.labelEndInfo = QtWidgets.QLabel(self.gbSample)
        self.labelEndInfo.setObjectName("labelEndInfo")
        self.glSample.addWidget(self.labelEndInfo, 7, 0, 1, 1)
        self.labelEnd = QtWidgets.QLabel(self.gbSample)
        self.labelEnd.setObjectName("labelEnd")
        self.glSample.addWidget(self.labelEnd, 7, 1, 1, 2)

        self.labelAmpInfo = QtWidgets.QLabel(self.gbSample)
        self.labelAmpInfo.setObjectName("labelAmpInfo")
        self.glSample.addWidget(self.labelAmpInfo, 8, 0, 1, 1)
        self.labelAmp = QtWidgets.QLabel(self.gbSample)
        self.labelAmp.setObjectName("labelAmp")
        self.glSample.addWidget(self.labelAmp, 8, 1, 1, 2)
        labelBtnstylesheet = """
                QRadioButton {
                    padding-left: 0px;  
                    padding-right: 20px;  
                    spacing: 5px; 
                    outline: 0;
                }

                QRadioButton::indicator {
                    width: 16px; 
                    height: 16px;  
                    margin-left: 0px; 
                    margin-right: -6px; 
                }
                """

        self.gbSamplelabel = QtWidgets.QGroupBox(self.groupBox2)
        self.gbSamplelabel.setObjectName("gbSample")
        self.gridLayout_4.addWidget(self.gbSamplelabel, 2, 0, 1, 1)  # 将标注添加到总布局的第2行，占据1行1列
        self.layoutgbSl=QtWidgets.QGridLayout(self.gbSamplelabel) #设置标注样本的布局
        self.layoutgbSl.setObjectName("layoutgbSl")
        self.gblabelbtngroup = QtWidgets.QButtonGroup(self.layoutgbSl)#按钮组管理
        self.gblabelbtn1=QtWidgets.QRadioButton()
        self.gblabelbtn2=QtWidgets.QRadioButton()
        self.gblabelbtn3=QtWidgets.QRadioButton()
        self.gblabelbtn4=QtWidgets.QRadioButton()#三个都不选的假按钮
        self.gblabelbtn1.setText('波形')
        self.gblabelbtn2.setText('状态')
        self.gblabelbtn3.setText('事件')
        self.gblabelbtngroup.addButton(self.gblabelbtn1)
        self.gblabelbtngroup.addButton(self.gblabelbtn2)
        self.gblabelbtngroup.addButton(self.gblabelbtn3)
        self.gblabelbtngroup.addButton(self.gblabelbtn4)
        self.layoutgbSl.addWidget(self.gblabelbtn1,1,0,1,1)
        self.layoutgbSl.addWidget(self.gblabelbtn2,1,1,1,1)
        self.layoutgbSl.addWidget(self.gblabelbtn3,1,2,1,1)
        self.gblabelbtn1.setStyleSheet(labelBtnstylesheet)
        self.gblabelbtn2.setStyleSheet(labelBtnstylesheet)
        self.gblabelbtn3.setStyleSheet(labelBtnstylesheet)
        self.gblabelbtn1.setLayoutDirection(Qt.RightToLeft)
        self.gblabelbtn2.setLayoutDirection(Qt.RightToLeft)
        self.gblabelbtn3.setLayoutDirection(Qt.RightToLeft)

        self.returnBtn = QtWidgets.QPushButton(self.groupBox2)
        self.returnBtn.setObjectName("returnBtn")
        self.gridLayout_4.addWidget(self.returnBtn, 3, 0, 1, 1)

        self.gridLayout_1.addWidget(self.groupBox2, 0, 1, 1, 1)

        self.retranslateUi(Ui_Form)
        QtCore.QMetaObject.connectSlotsByName(Ui_Form)


    def retranslateUi(self, ManualForm):
        _translate = QtCore.QCoreApplication.translate
        self.returnBtn.setText(_translate("Return", "返回"))
        #self.btnBegin.setText(_translate("Begin", "|<"))
        self.btnDowning.setText(_translate("Scroll Backward", "<<"))
        self.btnDown.setText(_translate("Backward", "<"))
        self.btnUp.setText(_translate("Forward", ">"))
        self.btnUping.setText(_translate("Scroll Forward", ">>"))
        #self.btnEnd.setText(_translate("End", ">|"))
        self.editTimeText.setText(_translate("EditTime Text", " 窗口位置:"))
        self.editTime.setText("00:00:00")
        self.secondsLine.setText(_translate("Seconds Line", "秒线 "))
        self.subtractAverage.setText(_translate("Subtract Average", "减平均 "))
        self.sensitivityText.setText(_translate("Sensitivity Text", " 灵敏度(uV/mm): "))
        self.secondsSpanText.setText(_translate("secondsSpan Text", " 秒跨度(mm/s): "))
        self.secondsSpan.setCurrentText("30")
        self.moveLengthText.setText(_translate("MoveLength Text", " 移动长度(s): "))
        self.scenarioSelectionBtn.setText(_translate("ScenarioSelection Btn", "参考方案"))
        self.channelSelectionBtn.setText(_translate("ChannelSelection", "导联选择"))
        self.sampleSelectionBtn.setText(_translate("SampleSelection Btn", "样本选择"))
        #self.btnStateAnnotate.setText(_translate("Annotate State", "标注状态"))
        ManualForm.setWindowTitle(_translate("ManualForm", "Form44"))

        self.gbPatientInfo.setTitle(_translate("Patient Info", "病人信息"))
        self.labelPatientNameInfo.setText(_translate("Name: ", "姓名："))
        self.labelPatientName.setText(" ")
        self.labelPatientSexInfo.setText(_translate("Gender: ", "性别："))
        self.labelPatientSex.setText(" ")
        self.labelPatientBirthInfo.setText(_translate("Birthday: ", "出生日期："))
        self.labelPatientBirth.setText(" ")
        self.labelPatientMeasureInfo.setText(_translate("MeasureDay: ", "测量日期："))
        self.labelPatientMeasure.setText(" ")
        self.labelMeasureTimeInfo.setText(_translate("MeasureTime: ", "测量时间："))
        self.labelMeasureTime.setText(" ")
        self.labelFileNameInfo.setText(_translate("Filename: ", "文件名称："))
        self.labelFileName.setText(" ")


        self.gbSamplelabel.setTitle(_translate("Sample Info", "标注样本"))
        self.labelTypeInfo.setText(_translate("Type: ", "类型："))
        self.labelType.setText("")
        self.labelChannelInfo.setText(_translate("Channel: ", "导联："))
        self.labelChannel.setText("")
        self.labelLengthInfo.setText(_translate("Length(s): ", "时限(s)："))
        self.labelLength.setText("")
        self.labelBeginInfo.setText(_translate("Start: ", "开始："))
        self.labelBegin.setText("")
        self.labelEndInfo.setText(_translate("End: ", "结束："))
        self.labelEnd.setText("")
        self.labelAmpInfo.setText(_translate("Amplitude(uV): ", "波幅(µV)："))
        self.labelAmp.setText("")

        self.gbSample.setTitle(_translate("Sample", "显示样本"))
        self.hideWave.setText(_translate("hideWave", " "))
        self.hideState.setText(_translate("hideState", " "))