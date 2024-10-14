from PyQt5 import QtCore
from PyQt5.QtWidgets import QComboBox, QLineEdit, QListWidgetItem, QListWidget, QCheckBox, QStyledItemDelegate
from PyQt5.QtGui import QFontMetrics, QStandardItem, QStandardItemModel


class ComboCheckBox(QComboBox):
	def __init__(self, parent, items: list):
		# items=['a','b','c']
		super(ComboCheckBox, self).__init__(parent)
		self.items = ["全选"] + items  # items list self.box_list = [] # selected items
		self.box_list = []
		self.text = QLineEdit()  # use to selected items self.state = 0 # use to record state
		self.state = 0
		q = QListWidget()
		for i in range(len(self.items)):
			self.box_list.append(QCheckBox())
			self.box_list[i].setText(self.items[i])
			item = QListWidgetItem(q)
			q.setItemWidget(item, self.box_list[i])
			if i == 0:
				self.box_list[i].stateChanged.connect(self.all_selected)
			else:
				self.box_list[i].stateChanged.connect(self.show_selected)
		# q.setStyleSheet("font-size: 20px; font-weight: bold; height: 40px; margin-left: 5px")
		# self.setStyleSheet("width: 300px; height: 50px; font-size: 21px; font-weight: bold")
		self.text.setReadOnly(True)
		self.setLineEdit(self.text)
		self.setModel(q.model())
		self.setView(q)

	def all_selected(self):
		if self.state == 0:
			self.state = 1
			for i in range(1, len(self.items)):
				self.box_list[i].setChecked(True)
		else:
			self.state = 0
			for i in range(1, len(self.items)):
				self.box_list[i].setChecked(False)
		self.show_selected()

	def get_selected(self) -> list:
		ret = []
		for i in range(1, len(self.items)):
			if self.box_list[i].isChecked():
				ret.append(self.box_list[i].text())
		return ret

	def show_selected(self):
		self.text.clear()
		ret = ';'.join(self.get_selected())
		self.text.setText(ret)

class CheckableComboBox(QComboBox):
	def __init__(self, parent, items, filter):
		super(CheckableComboBox, self).__init__(parent)
		self.setModel(QStandardItemModel(self))
		self.view().pressed.connect(self.handleItemPressed)
		self.view().clicked.connect(self.get_all)
		self.view().clicked.connect(self.getCheckItem)
		self.checkedItems = items
		self.filter = filter
		self.status = 1

		self.text = QLineEdit()
		self.text.setReadOnly(True)
		self.setLineEdit(self.text)
		self.lineEdit().installEventFilter(self)
		self.closeOnLineEditClick = False

		self.addItem("全选")
		self.addItems(items)
		self.getCheckItem()
		# self.text.setText("选择")

	def eventFilter(self, object, event):
		if object == self.lineEdit():
			if event.type() == QtCore.QEvent.MouseButtonRelease:
				if self.closeOnLineEditClick:
					self.hidePopup()
				else:
					self.showPopup()
				return True
			return False

	def showPopup(self):
		super().showPopup()
		# When the popup is displayed, a click on the lineedit should close it
		self.closeOnLineEditClick = True

	def hidePopup(self):
		super().hidePopup()
		# Used to prevent immediate reopening when clicking on the lineEdit
		# self.startTimer(100)
		# Refresh the display text when closing
		self.show_selected()
		self.closeOnLineEditClick = False

	def handleItemPressed(self, index):
		item = self.model().itemFromIndex(index)
		if item.checkState() == QtCore.Qt.Checked:
			item.setCheckState(QtCore.Qt.Unchecked)
		else:
			item.setCheckState(QtCore.Qt.Checked)

	def addItem(self, text, data=None):
		item = QStandardItem()
		item.setText(text)
		if data is None:
			item.setData(text)
		else:
			item.setData(data)
		item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)

		if text in self.filter:
			item.setData(QtCore.Qt.Checked, QtCore.Qt.CheckStateRole)
		else:
			item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
		self.model().appendRow(item)

	def addItems(self, texts, datalist=None):
		for i, text in enumerate(texts):
			try:
				data = datalist[i]
			except (TypeError, IndexError):
				data = None
			self.addItem(text, data)

	def getCheckItem(self):
		for index in range(1, self.count()):
			item = self.model().item(index)
			if item.checkState() == QtCore.Qt.Checked:
				if item.text() not in self.checkedItems:
					self.checkedItems.append(item.text())
			else:
				if item.text() in self.checkedItems:
					self.checkedItems.remove(item.text())
		# print("self.checkedItems为：",self.checkedItems)
		self.show_selected()
		return self.checkedItems

	def get_all(self):
		all_item = self.model().item(0)
		for index in range(1, self.count()):
			if self.status == 1:
				if self.model().item(index).checkState() == QtCore.Qt.Unchecked:
					all_item.setCheckState(QtCore.Qt.Unchecked)
					self.status = 0
					break

		if all_item.checkState() == QtCore.Qt.Checked:
			if self.status == 0:
				for index in range(self.count()):
					self.model().item(index).setCheckState(QtCore.Qt.Checked)
					self.status = 1

		elif all_item.checkState() == QtCore.Qt.Unchecked:
			for index in range(self.count()):
				if self.status == 1:
					self.model().item(index).setCheckState(QtCore.Qt.Unchecked)
			self.status = 0

	def show_selected(self):
		self.text.clear()
		t = "已选" + str(len(self.checkedItems)) + '项，' + '共' + str(self.count() - 1) + '项'
		self.text.setText(t)
		# if self.model().item(0).checkState() == QtCore.Qt.Checked:
		# 	self.text.setText("全选")
		# else:
		# 	t = "已选"+str(len(self.checkedItems))+'项，'+'共'+str(self.count()-1)+'项'
		# 	self.text.setText(t)
