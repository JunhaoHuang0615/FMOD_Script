import os

## ui_dir = './ui'  # 根据实际情况修改，指的是.ui文件所在的文件夹路径
current_path = os.path.abspath(__file__)

# 获取当前脚本的目录
current_dir = os.path.dirname(current_path)
# 结合目录
py_dir = os.path.join(current_dir, "../script/ui_script")

# 转成规范路径，消除..等
py_dir = os.path.normpath(py_dir)  # 根据实际情况修改，指的是生成的.py文件要存放的文件夹路径

for file in os.listdir(current_dir):
    if file.endswith('.ui'):
        print(f"File:{file} is export to {py_dir}/{os.path.splitext(file)[0]}.py")
        os.system(f'pyuic5 {current_dir}/{file} -o {py_dir}/{os.path.splitext(file)[0]}.py')