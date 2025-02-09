from PyQt5.QtWidgets import QWidget, QDialog
from view.EEG_form.RefForm import Ui_Ref
from view.EEG_form.sampleForm import Ui_Sample
from view.EEG_form.channelForm import Ui_channel


class QDialogRef(QDialog):
    def __init__(self, dgroup, curRef, parent=None):
        super().__init__(parent)
        self.ui = Ui_Ref()
        self.ui.setupUi(self, dgroup, curRef)

class QDialogSample(QDialog):
    def __init__(self, dgroup,samplefilter, parent=None):
        super().__init__(parent)
        self.ui = Ui_Sample()
        self.ui.setupUi(self, dgroup, samplefilter)

class QDialogChannel(QDialog):
    def __init__(self,montage,dgroup, dgroupFilter, parent=None):
        super().__init__(parent)
        self.ui = Ui_channel()
        self.ui.setupUi(self, montage, dgroup, dgroupFilter)

