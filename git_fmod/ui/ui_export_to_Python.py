import os

ui_dir = './'  # 根据实际情况修改，指的是.ui文件所在的文件夹路径
py_dir = '../script/ui_script/'  # 根据实际情况修改，指的是生成的.py文件要存放的文件夹路径

for file in os.listdir(ui_dir):
    if file.endswith('.ui'):
        os.system(f'pyuic5 {ui_dir}/{file} -o {py_dir}/{os.path.splitext(file)[0]}.py')