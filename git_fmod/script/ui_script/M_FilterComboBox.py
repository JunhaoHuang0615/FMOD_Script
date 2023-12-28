from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel

class FilteredComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super(FilteredComboBox, self).__init__(*args, **kwargs)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        self.source_model = QStandardItemModel()
        self.model_ = QSortFilterProxyModel()
        self.model_.setSourceModel(self.source_model)
        self.model_.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.setModel(self.model_)

    def addItems(self, items):
        self.source_model.clear()
        for i in items:
            item = QStandardItem(i)
            self.source_model.appendRow(item)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.hidePopup()

    def showPopup(self):
        if self.hasFocus():
            self.model_.setFilterFixedString(self.currentText())
            super().showPopup()

    # 获得所有的选项
    def getAllItems(self):
        return [self.source_model.item(i).text() for i in range(self.source_model.rowCount())]

    # 根据传入的字符串选择选项
    def setItemByText(self, text):
        index = self.findText(text)
        if index != -1:
            self.setCurrentIndex(index)

    # 获得当前选中的选项
    def getCurrentItem(self):
        return self.currentText()