import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget,QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt,QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMainWindow,QListWidgetItem
from dirty_list_window import Ui_DirtyListWidgetWindow
from MyTools import git_function
from diff_Text import DiffWindow

class DirtyListWindow(QMainWindow, Ui_DirtyListWidgetWindow): #这里集成了Ui_MainWindow，所以组件都可以直接拿得到
    def __init__(self,repo,retult={},parent=None):
        super(DirtyListWindow, self).__init__(parent)
        self.setupUi(self)
        self.retult = retult
        self.repo = repo
        self.setWindowTitle('File List Viewer')
        self.tableWidget_ListView.setColumnCount(2)
        self.tableWidget_ListView.setHorizontalHeaderLabels(['File State', 'File Path'])
        self.generate_table()
        # self.tableWidget_ListView.itemClicked.connect(self.on_button_clicked)  # 添加监听事件
        self.registerbutton()
    def generate_table(self):
        for i, (key, value_list) in enumerate(self.retult.items()):
            # 添加这行来跳过整数值
            if not isinstance(value_list, list):
                continue
            for value in value_list:
                self.tableWidget_ListView.insertRow(self.tableWidget_ListView.rowCount())
                self.tableWidget_ListView.setItem(self.tableWidget_ListView.rowCount()-1, 0, QTableWidgetItem(str(key)))
                self.tableWidget_ListView.setItem(self.tableWidget_ListView.rowCount()-1, 1, QTableWidgetItem(str(value)))
        self.tableWidget_ListView.resizeColumnsToContents()
        
    def on_button_clicked(self):
        # 当按钮被点击时，这个函数会被调用
        item = self.tableWidget_ListView.currentItem()  # 获取当前选中的项目体
        if item is not None:
            row = item.row()  # 获取选中的行
            column = item.column()  # 获取选中的列
            text = item.text()  # 获取选中项目体的文本
            print(f'You selected row {row}, column {column}, text {text}.')
            global diff_win_file
            print(self.repo)
            diff_win_file = DiffWindow(self.repo,text)
            diff_win_file.show()
        else:
            print('No item selected.')
        
    def registerbutton(self):
        self.btn_ShowDiff.clicked.connect(self.on_button_clicked)
        pass