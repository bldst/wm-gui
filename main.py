import Prime_ocr
import Riven_ocr
import wx_ocr


def process_wxocr_result(ocr_results):
    # 存储最终合并后的文本
    combined_texts = []
    # 存储已处理项目的索引，避免重复处理
    processed_indices = set()

    # 遍历每一个OCR识别结果
    for i, item in enumerate(ocr_results):
        # 如果当前项目已经处理过，则跳过
        if i in processed_indices:
            continue

        # 以当前项目为中心，收集与之位置相近的文本
        combined = [item['text']]
        for j, other_item in enumerate(ocr_results):
            # 如果是比较对象自身，或者已经被处理过，则跳过
            if j in processed_indices or i == j:
                continue

            # 计算两个文本在x轴和y轴上的距离
            distance_x = abs(item['pos']['x'] - other_item['pos']['x'])
            distance_y = abs(item['pos']['y'] - other_item['pos']['y'])
            #计算两个文本直接的距离
            #distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

            # 如果距离在设定范围内，则认为位置相近，将文本加入合并列表，并标记为已处理
            if distance_x <= 100 and distance_y <= 60 :
                combined.append(other_item['text'])
                processed_indices.add(j)  # 标记比较对象为已处理

        # 将合并后的文本加入结果列表，并标记当前项目为已处理
        combined_texts.append(''.join(combined))
        processed_indices.add(i)  # 标记当前项目为已处理

    return combined_texts


img_path = r"C:\Users\cc\PycharmProjects\WM-gui\static\部件1.png"
wx_ocr = wx_ocr.WxOcr(img_path)
wx_ocr.main()
result = wx_ocr.results
print(result)

process_result = process_wxocr_result(result)
print(process_result)
