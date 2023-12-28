
import time
import os
from ProgressBarWindow import ProgressThread;
from start_loading_ui import Ui_Frame;
from PyQt5 import QtCore, QtGui, QtWidgets
## 这是git_url_item的功能类
class LoadingWindow(QtWidgets.QWidget, Ui_Frame): #这里集成了Ui_MainWindow，所以组件都可以直接拿得到
    def __init__(self, target_value, callback=None, parent=None):
        super(LoadingWindow, self).__init__(parent)
        self.setupUi(self);
        self.target_value = target_value  
        self.callback = callback
        self.has_reached_target = False
        # 将图片缩放到窗口大小，这样就会自动填满整个窗口
        # self.stypesheetstr = "background-image: url(" + "assets/LoadingUI/Loading_ui.jpg" + "); background-repeat: no-repeat; background-position: center; background-size: 100% 100%;"
        # self.pixmap = QPixmap("assets/LoadingUI/Loading_ui.jpg")
        # self.Frame.setPixmap(self.pixmap)
        ######################################################### 获取路径 ##########################################################################
        # 获取当前脚本的绝对路径
        current_path = os.path.abspath(__file__)

        # 获取当前脚本的目录
        current_dir = os.path.dirname(current_path)
        # 结合目录
        image_path = os.path.join(current_dir, "../../assets/LoadingUI/Loading_ui.jpg")

        # 转成规范路径，消除..等
        image_path = os.path.normpath(image_path)
        image_path = image_path.replace("\\", "/")
        ######################################################### 获取路径 ##########################################################################

        ############################################################## 设置背景图片 #####################################################################
        # self.frame.setStyleSheet("background-image: url('"+image_path+"') 0 0 0 0 stretch stretch;"
        #                          +
        #                          """
        #                          background-position: center;
        #                          background-repeat: no-repeat;
        #                          """)
        self.pixmap = QtGui.QPixmap(image_path)
        self.pixmap = self.pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(self.pixmap))
        self.setPalette(palette)
         #################################################################################设置背景图片####################################################
        # 创建线程
        self.thread = ProgressThread()
        # 连接信号和槽
        self.thread.progress_signal.connect(self.setProgressValue)
        # 开始线程
        self.thread.start()
    
    # 重写缩放方法：
    def resizeEvent(self, event):
        # 重新调整pixmap的大小，使其等于Frame的大小
        scaledPixmap = self.pixmap.scaled(self.size())
        
        # 创建新的QPalette对象并设置背景图片
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(scaledPixmap))
        self.setPalette(palette)
            
    def setProgressValue(self,value):
        # self.thread.wait_until_done()
        self.progressBar.setValue(value)
        QtWidgets.QApplication.processEvents()
        if value >= self.target_value and not self.has_reached_target:
            self.has_reached_target = True
            if self.callback is not None:
                self.callback()
            self.close();
            