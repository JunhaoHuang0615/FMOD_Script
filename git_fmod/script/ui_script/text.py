from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class CustomComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super(CustomComboBox, self).__init__(*args, **kwargs)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        self.source_model = QStandardItemModel()
        self.model_ = QSortFilterProxyModel()
        self.model_.setSourceModel(self.source_model)
        self.model_.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.setModel(self.model_)

    def addItems(self, items):
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


app = QApplication([])
combo = CustomComboBox()
combo.addItems(["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"])
window = QWidget()
layout = QVBoxLayout(window)
layout.addWidget(combo)
window.show()
app.exec_()