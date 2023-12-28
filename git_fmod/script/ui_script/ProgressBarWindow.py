import time
from PyQt5 import QtWidgets,QtCore
from progressbar import Ui_Form;

class ProgressThread(QtCore.QThread):
    # 创建信号
    progress_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.is_done = False

    def run(self):
        for i in range(100):
            # 发送信号
            self.progress_signal.emit(i)
            time.sleep(0.1) # 暂停0.01秒，便于观察进度条变化
        self.is_done = True

    def wait_until_done(self):
        while not self.is_done:
            time.sleep(0.1)

## 这是git_url_item的功能类
class ProgressBarWindow(QtWidgets.QWidget, Ui_Form): #这里集成了Ui_MainWindow，所以组件都可以直接拿得到
    def __init__(self, target_value, callback=None, parent=None):
        super(ProgressBarWindow, self).__init__(parent)
        self.setupUi(self);
        self.target_value = target_value  
        self.callback = callback
        self.has_reached_target = False
        #self.frame.setStyleSheet("background-image: url(../../assets/LoadingUI/Loading_ui.jpg);")
                # 创建线程
        self.thread = ProgressThread()
        # 连接信号和槽
        self.thread.progress_signal.connect(self.setProgressValue)
        # 开始线程
        self.thread.start()
            
    def setProgressValue(self,value):
        # self.thread.wait_until_done()
        self.progressBar.setValue(value)
        QtWidgets.QApplication.processEvents()
        if value >= self.target_value and not self.has_reached_target:
            self.has_reached_target = True
            if self.callback is not None:
                self.callback()
            self.close();
            