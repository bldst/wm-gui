import os
import subprocess


class PrimeOcr:
    def __init__(self, img_path):
        # 获得当前项目路径
        self.project_path = os.path.dirname(os.path.abspath(__file__))
        self.imgpath = img_path

    def get_prime_ocr_name(self, img_path):
        full_img_path = os.path.join(self.project_path, img_path)
        # 定义要执行的CMD命令
        command = f".\Windows.Media.Ocr.Cli.exe {full_img_path}"
        ocr_list = []  # 用于存储识别结果
        try:
            # 执行CMD命令并获取输出
            output = subprocess.check_output(command, shell=True, text=True)
            # 使用换行符 '\n' 分割文本
            output_list = output.split('\n')
            print(output_list)
        except subprocess.CalledProcessError as e:
            print(f"执行CMD命令时出错: {e}")