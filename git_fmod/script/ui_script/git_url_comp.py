from git_url_item import Ui_Frame
from MyTools import git_function
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QPushButton, QLabel,QTableWidget,QHBoxLayout,QSizePolicy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from M_FilterComboBox import FilteredComboBox

## 这是git_url_item的功能类
class UI_FrameComp(QWidget, Ui_Frame): #这里集成了Ui_MainWindow，所以组件都可以直接拿得到
    def __init__(self, parent=None):
        super(UI_FrameComp, self).__init__(parent)
        #self.setupUi(self)
        self.setup_table()
        # self.horizontalHeader().sectionResized.connect(self.resizeAndupdateSize)
        # self.horizontalHeader().sectionResized.connect(self.updateWidth)
        # self.horizontalScrollBar().valueChanged.connect(self.updateWidth)
        self.register_button()
    def setup_table(self):
        # Initiate rows and columns of table widget
        self.table = QTableWidget(10, 5, self)
        self.table.setRowCount(1)
        self.table.setColumnCount(5)
        layout = QHBoxLayout()
        layout.addWidget(self.table)

        self.table.setHorizontalHeaderLabels(['URL', 'Local Path', ' ',"Branch","Pull"])
        # Create the elements and add them to the correct column in the QTableWidget
        # self.label = QtWidgets.QLabel("label")
        # self.table.setCellWidget(0, 0, self.label)  # 0 is the row number, 0 is the column number

        self.text_url = QtWidgets.QLineEdit()
        self.table.setCellWidget(0, 0, self.text_url)  # 1 for column number

        # self.label_3 = QtWidgets.QLabel("label_3")
        # self.table.setCellWidget(0, 2, self.label_3)  # 2 for column number

        self.text_repo_location = QtWidgets.QLineEdit()
        self.table.setCellWidget(0, 1, self.text_repo_location)  # 3 for column number

        self.btn_browse = QtWidgets.QPushButton("Browse")
        self.table.setCellWidget(0, 2, self.btn_browse)  # 4 for column number

        # self.label_2 = QtWidgets.QLabel("label_2")
        # self.table.setCellWidget(0, 5, self.label_2)  # 5 for column number

        self.comboBox_branch_selected = FilteredComboBox()
        self.table.setCellWidget(0, 3, self.comboBox_branch_selected)  # 6 for column number

        self.btn_pull_thisgit_only = QtWidgets.QPushButton("Pull")
        self.table.setCellWidget(0, 4, self.btn_pull_thisgit_only)  # 7 for column number
        # self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setLayout(layout)
        self.table.setRowHeight(0, self.text_url.height())
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.verticalHeader().setMinimumSectionSize(0)
        self.table.verticalHeader().setVisible(False)
        # self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # # Force the table to occupy at least the space of its contents
        self.table.setMinimumSize(self.table.horizontalHeader().length(), self.table.verticalHeader().length())
    
    # def resizeEvent(self, event):
    #     # super().resizeEvent(event)
    #     # QTimer.singleShot(0, self.updateSize)
    #     QTimer.singleShot(0, self.updateWidth)
        
    # def resizeAndupdateSize(self):
    #     self.resizeColumnsToContents()
    #     self.updateSize()
    # def updateWidth(self):
    #     width = self.viewport().width()
    #     if self.verticalScrollBar().isVisible():
    #         width += self.verticalScrollBar().width()
    #     self.setMinimumWidth(width)
        
    # def updateSize(self):
    #     self.setMinimumWidth(self.horizontalHeader().length() + self.verticalScrollBar().width())
        
    def register_button(self):
        self.btn_browse.clicked.connect(self.browse)
        ## self.comboBox_branch_selected.activated[str].connect(self.refresh_branch) 选择某个选项的时候才会触发
        pass
    
    
    def browse(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.text_repo_location.setText( folder_path )
    
    def refresh_branch(self):
        if self.text_repo_location.text != "":
            #print(self.text_repo_location.text)
            # self.comboBox_branch_selected.clear()
            branch_list = git_function.get_unique_branches(self.text_repo_location.text())
            self.comboBox_branch_selected.addItems(branch_list)
            print(branch_list)
