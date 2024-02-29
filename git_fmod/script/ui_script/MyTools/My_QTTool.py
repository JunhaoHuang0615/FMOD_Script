from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
import sys

# 方法1：打开文件夹浏览器并返回选择的文件夹路径
def open_folder():
    folder_path = QFileDialog.getExistingDirectory(None, "Select a folder.")
    return folder_path

# 方法2：根据参数message，弹出相应的消息窗口。如果error为真，则弹出错误消息窗口。否则，弹出普通消息窗口
def show_message(message, error=False):
    msg = QMessageBox()
    msg.setText(message)
    if error:
        msg.setIcon(QMessageBox.Critical)
    else:
        msg.setIcon(QMessageBox.Information)
    result = msg.exec_()
    return result