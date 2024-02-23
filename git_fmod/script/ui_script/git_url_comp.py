from git_url_item import Ui_Frame
from MyTools import git_function
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QPushButton, QLabel,QTableWidget,QHBoxLayout,QSizePolicy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from M_FilterComboBox import FilteredComboBox
from Dirty_List_Window_M import DirtyListWindow
## 这是git_url_item的功能类
class UI_FrameComp(QWidget, Ui_Frame): #这里集成了Ui_MainWindow，所以组件都可以直接拿得到
    def __init__(self, git_comp_model, parent=None):
        super(UI_FrameComp, self).__init__(parent)
        #self.setupUi(self)
        self.setup_table()
        # self.horizontalHeader().sectionResized.connect(self.resizeAndupdateSize)
        # self.horizontalHeader().sectionResized.connect(self.updateWidth)
        # self.horizontalScrollBar().valueChanged.connect(self.updateWidth)
        self.register_button()
        # 为了方便修改gitcomp的属性，这里需要记住git的model
        self.git_repo_comp = git_comp_model
    def setup_table(self):
        # Initiate rows and columns of table widget
        self.table = QTableWidget(10, 5, self)
        self.table.setRowCount(1)
        self.table.setColumnCount(10)
        layout = QHBoxLayout()
        layout.addWidget(self.table)

        self.table.setHorizontalHeaderLabels(["        Name        ","  Refresh  ",'URL', 'Local Path', ' ',"        Branch Name        ","        Status       "," Check Status ","Checkout To Selected Branch","Pull"])
        # Create the elements and add them to the correct column in the QTableWidget
        # self.label = QtWidgets.QLabel("label")
        # self.table.setCellWidget(0, 0, self.label)  # 0 is the row number, 0 is the column number
        self.repo_name = QtWidgets.QLineEdit()
        self.table.setCellWidget(0, 0, self.repo_name)  # 1 for column number
        
        self.btn_refresh = QtWidgets.QPushButton("Refresh")
        self.table.setCellWidget(0, 1, self.btn_refresh) 
         
        self.text_url = QtWidgets.QLineEdit()
        self.table.setCellWidget(0, 2, self.text_url)  # 1 for column number

        # self.label_3 = QtWidgets.QLabel("label_3")
        # self.table.setCellWidget(0, 2, self.label_3)  # 2 for column number

        self.text_repo_location = QtWidgets.QLineEdit()
        self.table.setCellWidget(0, 3, self.text_repo_location)  # 3 for column number

        self.btn_browse = QtWidgets.QPushButton("Browse")
        self.table.setCellWidget(0, 4, self.btn_browse)  # 4 for column number

        # self.label_2 = QtWidgets.QLabel("label_2")
        # self.table.setCellWidget(0, 5, self.label_2)  # 5 for column number

        self.comboBox_branch_selected = FilteredComboBox()
        self.table.setCellWidget(0, 5, self.comboBox_branch_selected)  # 6 for column number

        self.status_label = QtWidgets.QLabel('<font color="red">Refresh Please!</font>')
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        # palette = QtGui.QPalette()
        # palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.red)
        # self.status_label.setPalette(palette)
        self.table.setCellWidget(0, 6, self.status_label) 
        
                
        self.btn_check_status = QtWidgets.QPushButton("Check Status")
        self.table.setCellWidget(0, 7, self.btn_check_status) 
        
        self.btn_checkout_to_this_branch = QtWidgets.QPushButton("Checkout")
        self.table.setCellWidget(0, 8, self.btn_checkout_to_this_branch) 
        
        self.btn_pull_thisgit_only = QtWidgets.QPushButton("Pull")
        self.table.setCellWidget(0, 9, self.btn_pull_thisgit_only)  # 7 for column number
        # self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setLayout(layout)
        self.table.setRowHeight(0, self.text_url.height())
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.verticalHeader().setMinimumSectionSize(0)
        self.table.resizeColumnsToContents()
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
    def check_status(self):
        #首先检查是否有修改
        # palette = QtGui.QPalette()
        if self.text_repo_location.text != "":
            result = git_function.get_modified_files(self.text_repo_location.text())
            if result['total_count']> 0:
                # 说明有改动
                self.status_label.setText('<font color="red">Dirty</font>')
                # palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.red)
                # self.status_label.setPalette(palette)
                ## 在这里还需要打开一个窗口来显示本地仓库的变化
                global dirty_list_win 
                dirty_list_win = DirtyListWindow(self.text_repo_location.text(),result)
                dirty_list_win.show()
            elif git_function.isUpdated(self.text_repo_location.text()) == False:
                self.status_label.setText('<font color="red">Pull</font>')   
                # palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.red)
                # self.status_label.setPalette(palette)
            elif git_function.isUpdated(self.text_repo_location.text()) == True:
                self.status_label.setText('<font color="green">Updated</font>')   
                # palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.green)
                # self.status_label.setPalette(palette)
        pass
    def refresh_status(self):
        #首先检查是否有修改
        # palette = QtGui.QPalette()
        if self.text_repo_location.text != "":
            result = git_function.get_modified_files(self.text_repo_location.text())
            if result['total_count']> 0:
                # 说明有改动
                self.status_label.setText('<font color="red">Dirty</font>')
                # palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.red)
                # self.status_label.setPalette(palette)
                ## 在这里还需要打开一个窗口来显示本地仓库的变化
            elif git_function.isUpdated(self.text_repo_location.text()) == False:
                self.status_label.setText('<font color="red">Pull</font>')   
                # palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.red)
                # self.status_label.setPalette(palette)
            elif git_function.isUpdated(self.text_repo_location.text()) == True:
                self.status_label.setText('<font color="green">Updated</font>')   
                # palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.green)
                # self.status_label.setPalette(palette)
        pass
        
    def register_button(self):
        self.btn_browse.clicked.connect(self.browse)
        self.btn_checkout_to_this_branch.clicked.connect(self.checkout_to_branch)
        self.btn_refresh.clicked.connect(self.refresh_branch)
        self.btn_check_status.clicked.connect(self.check_status)
        ## self.comboBox_branch_selected.activated[str].connect(self.refresh_branch) 选择某个选项的时候才会触发

    
    
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
            # get current branch
            current_branch = git_function.get_current_branch(self.text_repo_location.text())
            self.comboBox_branch_selected.setCurrentIndex(0)
            self.select_option(current_branch);
            self.refresh_status()

    def checkout_to_branch(self):
        if self.text_repo_location.text != "" and self.get_current_branch_option() != "":
            #切换分支
            git_function.switch_branch(self.text_repo_location.text(),self.get_current_branch_option())
            
            
    def select_option(self, opt):
        index = self.comboBox_branch_selected.findText(opt)
        if index >= 0:  # 如果找到了
            self.comboBox_branch_selected.setCurrentIndex(index)  # 就设置成当前选项
        else:
            print(f"没有找到选项：{opt}")
            
    def get_current_branch_option(self):
        return self.comboBox_branch_selected.currentText()
    
    def get_comp(self):
        self.git_repo_comp.setName(self.repo_name.text())
        self.git_repo_comp.setremote_url(self.text_url.text())
        self.git_repo_comp.setlocal_path(self.text_repo_location.text())
        return self.git_repo_comp
        # self.git_repo_comp.console_data()
        
    
        
