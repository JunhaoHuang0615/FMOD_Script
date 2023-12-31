##主运行窗口
import time
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QListWidgetItem
from git_url_comp import UI_FrameComp
from mainwindow import Ui_MainWindow
from ProgressBarWindow import ProgressBarWindow
from LoadingWindow import LoadingWindow

class MainWindow(QMainWindow, Ui_MainWindow): #这里集成了Ui_MainWindow，所以组件都可以直接拿得到
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.add_url_groups()
        self.registerbutton()
        self.main_window_list = []

    def add_url_groups(self):
        # for i in range(15):  # 这里的10可以改成你需要添加的Frame的数量
        if self.listWidget_git_url_group.count() == 0:
            self.add_gitwidget()
            
    def registerbutton(self):
        self.btn_delete_selected_url.clicked.connect(self.remove_gitwidget)
        self.btn_add_giturl.clicked.connect(self.add_gitwidget)
        self.btn_refresh.clicked.connect(self.refresh_git_comp)
        pass
    # 组件功能
    # gitのURLコンポーネントを追加する
    def add_gitwidget(self):
            # frame = QWidget()
            frame_ui = UI_FrameComp()
            item = QListWidgetItem(self.listWidget_git_url_group)
            item.setSizeHint(frame_ui.sizeHint())
            self.listWidget_git_url_group.setItemWidget(item, frame_ui)
    
    def get_all_UI_FrameComp(self):
        ui_framecomp_list = []
        for i in range(self.listWidget_git_url_group.count()):
            item = self.listWidget_git_url_group.item(i)
            frame_ui = self.listWidget_git_url_group.itemWidget(item)
            ui_framecomp_list.append(frame_ui)
        return ui_framecomp_list
    
    def get_selected_UI_FrameComp(self):
        ui_framecomp_list = []
        selected_items = self.listWidget_git_url_group.selectedItems()
        for item in selected_items:
            frame_ui = self.listWidget_git_url_group.itemWidget(item)
            ui_framecomp_list.append(frame_ui)
        return ui_framecomp_list
            
    # gitのURLコンポーネントを削除する        
    def remove_gitwidget(self):
        # すべての選択された項目を取得する
        selected_items = self.listWidget_git_url_group.selectedItems()

        for item in selected_items:
            # 選択した項目を削除する
            self.listWidget_git_url_group.takeItem(self.listWidget_git_url_group.row(item))
            
    def add_MainWindow(self,win):
        self.main_window_list.append(win)
    def remove_window(self,win):
        if win in self.main_window_list:
            self.main_window_list.remove(win)
    def refresh_git_comp(self):
        git_ui_comp = self.get_all_UI_FrameComp();
        for item in git_ui_comp:
            item.refresh_branch();
        pass
        
            
        
        
## 重要：如果一个窗口没有被一个实例储存下来，就会直接被垃圾回收站回收掉。
def main():
    app = QApplication([])
    splash = LoadingWindow(99,openMainWindow)
    splash.show()
    for i in range(100):
        time.sleep(0.01)
        splash.setProgressValue(i)
    #splash.close()   
    app.exec_()
def openMainWindow():
    global win
    win = MainWindow()
    win.show()
    
if __name__ == '__main__':
    main()