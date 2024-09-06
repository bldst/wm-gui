import json
import os
import re
import subprocess
from fuzzywuzzy import fuzz


class RivenOcr:
    """
    用于识别图片中的紫卡信息，并返回识别结果
    传入相对路径，返回识别结果
    结果为列表
    """
    def __init__(self, img_path):
        #获得当前项目路径
        self.project_path = os.path.dirname(os.path.abspath(__file__))

        self.ocr_list = self.get_riven_ocr_name(img_path, self.project_path)
        try:
            #参考列表
            self.comparison_list = json.load(open("static/riven_cname.json", "r", encoding="utf-8"))
        except Exception as e:
            print(e)
        #comparison_list为最终需要的列表
        self.comparison_list = self.compare_name(self.ocr_list, self.comparison_list)

    def get_riven_ocr_name(self, img_path, project_path):
        full_img_path = os.path.join(project_path, img_path)
        # 定义要执行的CMD命令
        command = f".\Windows.Media.Ocr.Cli.exe {full_img_path}"

        ocr_list = []  # 用于存储识别结果
        try:
            # 执行CMD命令并获取输出
            output = subprocess.check_output(command, shell=True, text=True)
            # 使用换行符 '\n' 分割文本
            output_list = output.split('\n')
            print(output_list)
            # 过滤掉不包含汉字的元素和包含数字的元素
            filtered_lines = [line for line in output_list if
                              re.search(r"[\u4e00-\u9fff]+", line) and not re.search(r"\d+", line)]
            # 过滤每一个元素中除了汉字的部分
            for line in filtered_lines:
                ocr_list.append(re.sub(r"[^\u4e00-\u9fff]", "", line))

        except subprocess.CalledProcessError as e:
            print(f"执行CMD命令时出错: {e}")
        return ocr_list

    def compare_name(self, ocr_list, comparison_list):
        compare_result = []
        # 遍历OCR名称列表和比较名称列表，寻找相似度高于80%的名称
        for ocr_name in ocr_list:
            # 遍历比较名称列表,保存相似度最高的名称
            best_match = None
            best_ratio = 0
            for comparison_name in comparison_list:
                ratio = fuzz.ratio(ocr_name, comparison_name)
                if ratio > best_ratio and ratio > 50:
                    best_match = comparison_name
                    best_ratio = ratio
            compare_result.append(best_match)

        return compare_result

    def print_result(self, comparison_list):
        for i in comparison_list:
            print(i)
