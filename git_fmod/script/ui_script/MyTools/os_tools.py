import os
def get_abs_path_from_current_script(relative_path):
    current_path = os.path.abspath(__file__)

    # 获取当前脚本的目录
    current_dir = os.path.dirname(current_path)
    # 结合目录
    image_path = os.path.join(current_dir, relative_path)

    # 转成规范路径，消除..等
    image_path = os.path.normpath(image_path)
    image_path = image_path.replace("\\", "/")
    return image_path