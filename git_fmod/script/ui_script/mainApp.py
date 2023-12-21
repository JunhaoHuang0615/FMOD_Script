from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QListWidgetItem
from git_url_item import Ui_Frame
from mainwindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.add_url_groups()

    def add_url_groups(self):
        for i in range(15):  # 这里的10可以改成你需要添加的Frame的数量
            frame = QWidget()
            frame_ui = Ui_Frame()
            frame_ui.setupUi(frame)

            item = QListWidgetItem(self.listWidget_git_url_group)
            item.setSizeHint(frame.sizeHint())
            self.listWidget_git_url_group.setItemWidget(item, frame)

def main():
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()

if __name__ == '__main__':
    main()