import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget
from PyQt5.QtCore import Qt,QUrl
from PyQt5.QtGui import QDesktopServices


class FileListWindow(QWidget):
    def __init__(self, file_paths):
        super().__init__()
        self.file_paths = file_paths
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('File List Viewer')

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.file_list = QListWidget()

        for path in self.file_paths:
            self.file_list.addItem(path)

        ##connect的时候就会自动传入一个参数是item
        self.file_list.itemDoubleClicked.connect(lambda item: self.open_file(item))
        layout.addWidget(self.file_list)

    def open_file(self, item):
        selected_file = item.text()
        url = QUrl.fromLocalFile(selected_file)
        QDesktopServices.openUrl(url)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Main Window')

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.btn_show_files = QPushButton('Show Files')
        self.btn_show_files.clicked.connect(self.show_files)

        layout.addWidget(self.btn_show_files)

    def show_files(self):
        file_paths = ["F:/FMOD_Script/FMOD_Script/git_fmod/script/ui_script/local_history.py", "path2", "path3"]  # 这里使用示例路径，您可以替换为您的文件路径列表
        self.file_list_window = FileListWindow(file_paths)
        self.file_list_window.setGeometry(100, 100, 300, 200)  # 设置新窗口的位置和大小
        self.file_list_window.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()