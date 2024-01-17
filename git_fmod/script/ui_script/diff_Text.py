from PyQt5 import QtGui, QtWidgets,QtCore
from git import Repo
import difflib, sys,os
from MyTools import git_function
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QCoreApplication, QRect, QPoint,QSize
from PyQt5.QtGui import QScreen

class SyncScrollTextEdit(QtWidgets.QTextEdit):
    def __init__(self, parent = None, buddy = None):
        super(SyncScrollTextEdit,self).__init__(parent)
        self.buddy = buddy

    def wheelEvent(self, event):
        super().wheelEvent(event)  
        if(self.buddy != None):     
            self.buddy.verticalScrollBar().setValue(self.verticalScrollBar().value())
    def setBuddy(self,buddy):
        self.buddy = buddy


class DiffWindow(QtWidgets.QMainWindow):
    def __init__(self, repo_path, file_path):
        super().__init__()

        self.repo_path = repo_path
        self.file_path = file_path

        self.initUI()

    def initUI(self):
        # 设置窗口标题为文件路径
        self.setWindowTitle(self.file_path)

        self.originalFile = SyncScrollTextEdit(self)
        self.modifiedFile = SyncScrollTextEdit(self, self.originalFile)
        self.originalFile.setBuddy(self.modifiedFile)
        self.originalFile.setReadOnly(True)
        self.modifiedFile.setReadOnly(True)
  
        # 创建打开文件按钮
        openFileButton = QPushButton("Open File", self)
        openFileButton.clicked.connect(self.openFile)

        # 创建布局并添加组件
        editorLayout = QHBoxLayout()
        editorLayout.addWidget(self.originalFile)
        editorLayout.addWidget(self.modifiedFile)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(openFileButton)
        windowLayout.addLayout(editorLayout)

        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(windowLayout)

        self.show_diff()
        
        # 获取屏幕大小
        screen = QCoreApplication.instance().screens()[0]
        screenSize = screen.geometry()

        # 设置窗口尺寸为屏幕的一半
        windowSize = QSize(screenSize.width() // 2, screenSize.height() // 2)
        self.resize(windowSize)

        # 移动窗口到屏幕的中央
        windowRect = self.frameGeometry()
        centerPoint = screenSize.center()
        windowRect.moveCenter(centerPoint)
        self.move(windowRect.topLeft())
        
    def get_relative_path(self,repo_path, file_absolute_path):
        relative_path = os.path.relpath(file_absolute_path, repo_path)
        relative_file_path = os.path.normpath(relative_path)
        relative_file_path = relative_file_path.replace('\\', '/')
        return relative_file_path
    
    def openFile(self):
        # QPushButton 的 clicked 信号会调用这个方法
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.file_path))

    def show_diff(self):
        relative_path = self.get_relative_path(self.repo_path,self.file_path)
        # print(git_function.check_git_status(self.repo_path,relative_path))
        if self.repo_path != "" and git_function.check_git_status(self.repo_path,relative_path) != git_function.GitFileStatus.UNTRACKED:
            original_lines = git_function.get_original_file(self.repo_path, relative_path)
            modified_lines = git_function.get_modified_file(self.repo_path, relative_path)

            differ = difflib.Differ()
            diff = list(differ.compare(original_lines, modified_lines))

            lineno = 1  # 计数变量，初始化为 1
            for line in diff:
                span_template = "<span style='background-color:{}'>{}</span>"
                if line.startswith('- '):
                    self.originalFile.append(span_template.format('#FFC0CB', f"{lineno} - " + line[2:]))  # 在行前添加行号和 "-"，颜色已修改为淡红色
                    self.modifiedFile.append(f"{lineno} ")
                    lineno += 1
                elif line.startswith('+ '): 
                    self.modifiedFile.append(span_template.format('#90EE90', f"{lineno} + " + line[2:]))  # 在行前添加行号和 "+"，颜色已修改为淡绿色
                    self.originalFile.append(f"{lineno} ")
                    lineno += 1
                elif line.startswith('  '):  # 没有修改的行以空格开始
                    self.originalFile.append(f"{lineno} " + line[2:]) 
                    self.modifiedFile.append(f"{lineno} " + line[2:]) 
                    lineno += 1

# app = QtWidgets.QApplication([])
# window = DiffWindow('F:/FMOD_Script/FMOD_Script', 'git_fmod/script/ui_script/MyTools/git_function.py')  
# window.show()
# sys.exit(app.exec_())